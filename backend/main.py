
import asyncio
import contextvars
import json
import logging
import os
import random
import re
import socket
import threading
import time
from collections import defaultdict, deque
from typing import Annotated, Optional

import httpx
import joblib
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict
from starlette.middleware.base import BaseHTTPMiddleware

try:
    import sentry_sdk
except Exception:
    sentry_sdk = None

try:
    from prometheus_client import CONTENT_TYPE_LATEST, Counter, Histogram, generate_latest
except Exception:
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4"
    Counter = None
    Histogram = None
    generate_latest = None

try:
    import psutil
except Exception:
    psutil = None

try:
    import sklearn
except Exception:
    sklearn = None

# --- Force IPv4 for all DNS lookups ---
# Fixes: Python prefers IPv6 which times out on some networks
_original_getaddrinfo = socket.getaddrinfo

def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if family == 0:
        family = socket.AF_INET  # Force IPv4
    return _original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = _ipv4_getaddrinfo

request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="-")
trace_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar("trace_id", default="-")


class JsonLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_ctx_var.get(),
            "trace_id": trace_id_ctx_var.get(),
        }
        return json.dumps(payload, ensure_ascii=True)


root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
if root_logger.handlers:
    root_logger.handlers[0].setFormatter(JsonLogFormatter())
else:
    handler = logging.StreamHandler()
    handler.setFormatter(JsonLogFormatter())
    root_logger.addHandler(handler)

logger = logging.getLogger("truthshield-api")
logger.info("DNS forced to IPv4 (IPv6 workaround active).")
START_TIME = time.time()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore")

    environment: str = "development"
    force_https: bool = False
    trusted_hosts: Annotated[list[str], NoDecode] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])

    cors_allow_origins: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: ["http://localhost:5173", "http://127.0.0.1:5173"]
    )
    cors_allow_credentials: bool = False
    cors_dev_allow_all: bool = True

    max_request_body_bytes: int = 100_000
    max_text_chars: int = 20_000
    min_text_chars: int = 50

    predict_window_seconds: int = 60
    predict_global_limit: int = 120
    predict_per_ip_limit: int = 20
    predict_burst_window_seconds: int = 10
    predict_burst_limit: int = 8
    predict_block_seconds: int = 300

    captcha_enabled: bool = False
    captcha_provider: str = "turnstile"
    captcha_secret_key: str = ""
    captcha_verify_url: str = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
    captcha_timeout_seconds: int = 5

    security_csp: str = (
        "default-src 'self'; img-src 'self' data: https:; style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; connect-src 'self' https:; frame-ancestors 'none'; base-uri 'self'; form-action 'self'"
    )
    cache_max_items: int = 200
    cache_ttl_seconds: int = 900
    model_version: str = "v3"
    retention_days_submitted_text: int = 0
    no_store_mode: bool = False
    privacy_contact_email: str = "privacy@truthshield.ai"

    metrics_enabled: bool = True
    sentry_dsn: str = ""
    alert_latency_ms: int = 1500
    alert_5xx_per_minute: int = 20

    gemini_timeout_seconds: int = 12
    gemini_max_retries: int = 2
    gemini_retry_jitter_ms: int = 250
    gemini_circuit_fail_threshold: int = 5
    gemini_circuit_open_seconds: int = 60

    gemini_api_key: str = ""
    gemini_models: Annotated[list[str], NoDecode] = Field(
        default_factory=lambda: [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-2.5-flash-lite",
            "gemini-3-flash-preview",
        ]
    )

    @field_validator("trusted_hosts", "cors_allow_origins", "gemini_models", mode="before")
    @classmethod
    def split_list_values(cls, value):
        if isinstance(value, str):
            text = value.strip()
            if not text:
                return []
            if text.startswith("["):
                try:
                    parsed = json.loads(text)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed if str(item).strip()]
                except json.JSONDecodeError:
                    # Fall back to CSV parsing for operator mistakes in env values.
                    pass
            return [item.strip() for item in text.split(",") if item.strip()]
        return value

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_environment(cls, value):
        if not value:
            return "development"
        return str(value).strip().lower()

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @property
    def effective_force_https(self) -> bool:
        return self.force_https or self.is_production


settings = Settings()

ENVIRONMENT = settings.environment
IS_PRODUCTION = settings.is_production
FORCE_HTTPS = settings.effective_force_https
TRUSTED_HOSTS = settings.trusted_hosts

CORS_ALLOW_ORIGINS = settings.cors_allow_origins
CORS_ALLOW_CREDENTIALS = settings.cors_allow_credentials
CORS_DEV_ALLOW_ALL = settings.cors_dev_allow_all

MAX_REQUEST_BODY_BYTES = settings.max_request_body_bytes
MAX_TEXT_CHARS = settings.max_text_chars
MIN_TEXT_CHARS = settings.min_text_chars

PREDICT_WINDOW_SECONDS = settings.predict_window_seconds
PREDICT_GLOBAL_LIMIT = settings.predict_global_limit
PREDICT_PER_IP_LIMIT = settings.predict_per_ip_limit
PREDICT_BURST_WINDOW_SECONDS = settings.predict_burst_window_seconds
PREDICT_BURST_LIMIT = settings.predict_burst_limit
PREDICT_BLOCK_SECONDS = settings.predict_block_seconds

CAPTCHA_ENABLED = settings.captcha_enabled
CAPTCHA_PROVIDER = settings.captcha_provider.strip().lower()
CAPTCHA_SECRET_KEY = settings.captcha_secret_key.strip()
CAPTCHA_VERIFY_URL = settings.captcha_verify_url.strip()
CAPTCHA_TIMEOUT_SECONDS = max(1, settings.captcha_timeout_seconds)
GEMINI_TIMEOUT_SECONDS = max(1, settings.gemini_timeout_seconds)
GEMINI_MAX_RETRIES = max(0, settings.gemini_max_retries)
GEMINI_RETRY_JITTER_MS = max(0, settings.gemini_retry_jitter_ms)
GEMINI_CIRCUIT_FAIL_THRESHOLD = max(1, settings.gemini_circuit_fail_threshold)
GEMINI_CIRCUIT_OPEN_SECONDS = max(1, settings.gemini_circuit_open_seconds)
MODEL_VERSION = settings.model_version.strip() or "v3"

METRICS_ENABLED = settings.metrics_enabled
CACHE_TTL_SECONDS = max(1, settings.cache_ttl_seconds)
ALERT_LATENCY_MS = max(100, settings.alert_latency_ms)
ALERT_5XX_PER_MINUTE = max(1, settings.alert_5xx_per_minute)
RETENTION_DAYS_SUBMITTED_TEXT = max(0, settings.retention_days_submitted_text)
NO_STORE_MODE = settings.no_store_mode
PRIVACY_CONTACT_EMAIL = settings.privacy_contact_email.strip() or "privacy@truthshield.ai"
API_V1_PREFIX = "/api/v1"

SECURITY_CSP = settings.security_csp.strip()

if METRICS_ENABLED and Counter is not None:
    REQUEST_COUNT = Counter("truthshield_requests_total", "Total HTTP requests", ["method", "path", "status"])
    REQUEST_LATENCY = Histogram("truthshield_request_latency_seconds", "HTTP request latency", ["method", "path"])
    REQUEST_ERRORS = Counter("truthshield_request_errors_total", "Total 5xx responses", ["path"])
    GEMINI_SUCCESS = Counter("truthshield_gemini_success_total", "Successful Gemini analyses")
    GEMINI_FALLBACK = Counter("truthshield_gemini_fallback_total", "Gemini fallback to local model")
else:
    REQUEST_COUNT = None
    REQUEST_LATENCY = None
    REQUEST_ERRORS = None
    GEMINI_SUCCESS = None
    GEMINI_FALLBACK = None


class RequestSizeLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, max_bytes: int):
        super().__init__(app)
        self.max_bytes = max_bytes

    async def dispatch(self, request: Request, call_next):
        if request.method in {"POST", "PUT", "PATCH"}:
            header_size = request.headers.get("content-length")
            if header_size:
                try:
                    if int(header_size) > self.max_bytes:
                        return JSONResponse(
                            status_code=413,
                            content={
                                "error": "payload_too_large",
                                "message": f"Request body exceeds {self.max_bytes} bytes.",
                            },
                        )
                except ValueError:
                    pass
        return await call_next(request)


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = SECURITY_CSP
        if NO_STORE_MODE:
            response.headers["Cache-Control"] = "no-store"
            response.headers["Pragma"] = "no-cache"
        if IS_PRODUCTION:
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        return response


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("x-request-id") or f"req-{int(time.time() * 1000)}-{random.randint(1000,9999)}"
        trace_id = request.headers.get("x-trace-id") or request.headers.get("traceparent", "")
        if not trace_id:
            trace_id = request_id

        token_req = request_id_ctx_var.set(request_id)
        token_trace = trace_id_ctx_var.set(trace_id)
        start = time.perf_counter()
        try:
            response = await call_next(request)
        finally:
            duration = max(0.0, time.perf_counter() - start)
            status_code = 500
            try:
                status_code = response.status_code  # type: ignore[name-defined]
            except Exception:
                pass
            path = request.url.path
            if REQUEST_COUNT is not None:
                REQUEST_COUNT.labels(method=request.method, path=path, status=str(status_code)).inc()
            if REQUEST_LATENCY is not None:
                REQUEST_LATENCY.labels(method=request.method, path=path).observe(duration)
            if REQUEST_ERRORS is not None and status_code >= 500:
                REQUEST_ERRORS.labels(path=path).inc()

            if duration * 1000 > ALERT_LATENCY_MS:
                logger.warning(
                    "High request latency detected: path=%s duration_ms=%.2f threshold_ms=%d",
                    path,
                    duration * 1000,
                    ALERT_LATENCY_MS,
                )

            if status_code >= 500:
                now = time.time()
                recent_5xx_events.append(now)
                while recent_5xx_events and now - recent_5xx_events[0] > 60:
                    recent_5xx_events.popleft()
                if len(recent_5xx_events) >= ALERT_5XX_PER_MINUTE:
                    logger.error(
                        "5xx alert threshold exceeded: last_minute_count=%d threshold=%d",
                        len(recent_5xx_events),
                        ALERT_5XX_PER_MINUTE,
                    )

            request_id_ctx_var.reset(token_req)
            trace_id_ctx_var.reset(token_trace)

        response.headers["X-Request-ID"] = request_id
        response.headers["X-Trace-ID"] = trace_id
        return response


class GeminiCircuitBreaker:
    def __init__(self, fail_threshold: int, open_seconds: int):
        self.fail_threshold = fail_threshold
        self.open_seconds = open_seconds
        self.fail_count = 0
        self.open_until = 0.0
        self.lock = threading.Lock()

    def allow(self) -> bool:
        with self.lock:
            if self.open_until > time.time():
                return False
            if self.open_until > 0:
                self.open_until = 0
            return True

    def record_success(self) -> None:
        with self.lock:
            self.fail_count = 0
            self.open_until = 0.0

    def record_failure(self) -> None:
        with self.lock:
            self.fail_count += 1
            if self.fail_count >= self.fail_threshold:
                self.open_until = time.time() + self.open_seconds


class TTLCache:
    def __init__(self, max_items: int, ttl_seconds: int):
        self.max_items = max_items
        self.ttl_seconds = ttl_seconds
        self.store: dict[str, tuple[float, PredictionResponse]] = {}
        self.lock = threading.Lock()

    def get(self, key: str) -> Optional["PredictionResponse"]:
        now = time.time()
        with self.lock:
            item = self.store.get(key)
            if not item:
                return None
            expires_at, value = item
            if expires_at <= now:
                self.store.pop(key, None)
                return None
            return value

    def set(self, key: str, value: "PredictionResponse") -> None:
        with self.lock:
            if len(self.store) >= self.max_items:
                oldest_key = next(iter(self.store))
                self.store.pop(oldest_key, None)
            self.store[key] = (time.time() + self.ttl_seconds, value)


class SimpleRateLimiter:
    def __init__(self):
        self.lock = threading.Lock()
        self.global_events = deque()
        self.per_ip_events = defaultdict(deque)
        self.per_ip_burst_events = defaultdict(deque)
        self.blocked_ips = {}
        self.per_ip_violations = defaultdict(int)

    @staticmethod
    def _prune(events: deque, window_seconds: int, now: float) -> None:
        while events and now - events[0] > window_seconds:
            events.popleft()

    def check(self, client_ip: str) -> tuple[bool, Optional[str], Optional[int]]:
        now = time.time()
        with self.lock:
            blocked_until = self.blocked_ips.get(client_ip)
            if blocked_until and blocked_until > now:
                retry_after = int(blocked_until - now)
                return False, "ip_temporarily_blocked", retry_after
            if blocked_until and blocked_until <= now:
                self.blocked_ips.pop(client_ip, None)
                self.per_ip_violations.pop(client_ip, None)

            self._prune(self.global_events, PREDICT_WINDOW_SECONDS, now)
            ip_events = self.per_ip_events[client_ip]
            burst_events = self.per_ip_burst_events[client_ip]
            self._prune(ip_events, PREDICT_WINDOW_SECONDS, now)
            self._prune(burst_events, PREDICT_BURST_WINDOW_SECONDS, now)

            if len(self.global_events) >= PREDICT_GLOBAL_LIMIT:
                return False, "global_rate_limit_exceeded", PREDICT_WINDOW_SECONDS

            if len(burst_events) >= PREDICT_BURST_LIMIT:
                self.blocked_ips[client_ip] = now + PREDICT_BLOCK_SECONDS
                self.per_ip_violations[client_ip] += 1
                return False, "burst_abuse_detected", PREDICT_BLOCK_SECONDS

            if len(ip_events) >= PREDICT_PER_IP_LIMIT:
                self.per_ip_violations[client_ip] += 1
                if self.per_ip_violations[client_ip] >= 3:
                    self.blocked_ips[client_ip] = now + PREDICT_BLOCK_SECONDS
                    return False, "ip_temporarily_blocked", PREDICT_BLOCK_SECONDS
                return False, "ip_rate_limit_exceeded", PREDICT_WINDOW_SECONDS

            self.global_events.append(now)
            ip_events.append(now)
            burst_events.append(now)
            return True, None, None


rate_limiter = SimpleRateLimiter()
runtime_config_errors: list[str] = []
gemini_circuit = GeminiCircuitBreaker(GEMINI_CIRCUIT_FAIL_THRESHOLD, GEMINI_CIRCUIT_OPEN_SECONDS)
recent_5xx_events: deque[float] = deque()

# Configure Gemini API (Primary analysis engine)
GEMINI_API_KEY = settings.gemini_api_key.strip()
gemini_client = None
if not GEMINI_API_KEY:
    logger.warning("GEMINI_API_KEY not found. Will rely on local model only.")
else:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        logger.info("Gemini API client initialized (primary analyzer).")
    except Exception as e:
        logger.warning("Gemini client init failed: %s", e)

# Model fallback chain — try each in order
GEMINI_MODELS = settings.gemini_models

# --- Directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")
MODEL_METADATA_PATH = os.path.join(MODEL_DIR, "model_metadata.json")

# --- Load Local Model (secondary / fallback) ---
USE_LOCAL_MODEL = False
MODEL_METADATA: dict = {}
model_integrity_errors: list[str] = []
try:
    logger.info("Loading local model...")
    local_model = joblib.load(MODEL_PATH)
    local_vectorizer = joblib.load(VECTORIZER_PATH)
    if os.path.exists(MODEL_METADATA_PATH):
        with open(MODEL_METADATA_PATH, "r", encoding="utf-8") as metadata_file:
            MODEL_METADATA = json.load(metadata_file)
    logger.info("Local model loaded successfully (fallback analyzer).")
    USE_LOCAL_MODEL = True
except Exception as e:
    logger.warning("Could not load local model: %s", e)

if settings.sentry_dsn and sentry_sdk is not None:
    sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.05, environment=ENVIRONMENT)
    logger.info("Sentry initialized.")


def validate_runtime_configuration() -> None:
    errors = []

    if USE_LOCAL_MODEL:
        if not hasattr(local_model, "predict") or not hasattr(local_model, "predict_proba"):
            errors.append("Local model artifact is incompatible: missing predict/predict_proba")
        if not hasattr(local_vectorizer, "transform"):
            errors.append("Vectorizer artifact is incompatible: missing transform")

        trained_sklearn_version = MODEL_METADATA.get("sklearn_version")
        runtime_sklearn_version = getattr(sklearn, "__version__", "unknown") if sklearn else "unknown"
        if trained_sklearn_version and trained_sklearn_version != runtime_sklearn_version:
            errors.append(
                f"Model sklearn version mismatch: trained={trained_sklearn_version}, runtime={runtime_sklearn_version}"
            )

    if MIN_TEXT_CHARS < 1:
        errors.append("MIN_TEXT_CHARS must be >= 1")
    if MAX_TEXT_CHARS <= MIN_TEXT_CHARS:
        errors.append("MAX_TEXT_CHARS must be greater than MIN_TEXT_CHARS")
    if MAX_REQUEST_BODY_BYTES < 1024:
        errors.append("MAX_REQUEST_BODY_BYTES is too low for valid JSON payloads")

    if IS_PRODUCTION:
        if CORS_DEV_ALLOW_ALL:
            errors.append("CORS_DEV_ALLOW_ALL must be false in production")
        if not CORS_ALLOW_ORIGINS:
            errors.append("CORS_ALLOW_ORIGINS must be set in production")
        if "*" in CORS_ALLOW_ORIGINS:
            errors.append("CORS_ALLOW_ORIGINS cannot contain '*' in production")
        if not TRUSTED_HOSTS:
            errors.append("TRUSTED_HOSTS must be set in production")
        if not FORCE_HTTPS:
            errors.append("FORCE_HTTPS must be true in production")

    if CAPTCHA_ENABLED and not CAPTCHA_SECRET_KEY:
        errors.append("CAPTCHA_SECRET_KEY is required when CAPTCHA_ENABLED=true")

    if gemini_client is None and not USE_LOCAL_MODEL:
        errors.append("No analyzer available. Configure GEMINI_API_KEY or local model artifacts.")

    runtime_config_errors.extend(errors)
    model_integrity_errors.extend(errors)
    if IS_PRODUCTION and errors:
        raise RuntimeError("Invalid production configuration: " + "; ".join(errors))


validate_runtime_configuration()

# --- App Initialization ---
app = FastAPI(
    title="TruthShield API",
    description=(
        "TruthShield fake-news analysis API with Gemini as primary analyzer and local ML fallback. "
        "Preferred stable namespace: /api/v1. Legacy unversioned routes remain for backward compatibility."
    ),
    version="2.1.0",
    contact={"name": "TruthShield API Support", "email": "support@truthshield.ai"},
    license_info={"name": "Proprietary"},
    openapi_tags=[
        {"name": "Health Check", "description": "Liveness, readiness, and metrics endpoints."},
        {"name": "AI Analysis", "description": "News verification and confidence scoring."},
        {"name": "Governance", "description": "Versioning and privacy governance controls."},
    ],
)

app.add_middleware(RequestContextMiddleware)

if FORCE_HTTPS:
    app.add_middleware(HTTPSRedirectMiddleware)

if IS_PRODUCTION:
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=TRUSTED_HOSTS)

app.add_middleware(RequestSizeLimitMiddleware, max_bytes=MAX_REQUEST_BODY_BYTES)
app.add_middleware(SecurityHeadersMiddleware)

# --- CORS Middleware (split dev/prod behavior) ---
cors_origins = CORS_ALLOW_ORIGINS
if not IS_PRODUCTION and CORS_DEV_ALLOW_ALL:
    cors_origins = ["*"]

if "*" in cors_origins and CORS_ALLOW_CREDENTIALS:
    logger.warning("CORS credentials disabled because wildcard origin is in use.")
    CORS_ALLOW_CREDENTIALS = False

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=CORS_ALLOW_CREDENTIALS,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"]
)

# --- In-memory Cache ---
cache: Optional[TTLCache] = None if NO_STORE_MODE else TTLCache(max_items=settings.cache_max_items, ttl_seconds=CACHE_TTL_SECONDS)


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for", "")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


async def verify_captcha(token: str, client_ip: str) -> bool:
    if not CAPTCHA_ENABLED:
        return True
    if not CAPTCHA_SECRET_KEY:
        logger.error("CAPTCHA is enabled but CAPTCHA_SECRET_KEY is missing.")
        return False

    if CAPTCHA_PROVIDER != "turnstile":
        logger.error("Unsupported CAPTCHA_PROVIDER configured: %s", CAPTCHA_PROVIDER)
        return False

    payload = {"secret": CAPTCHA_SECRET_KEY, "response": token}
    if client_ip and client_ip != "unknown":
        payload["remoteip"] = client_ip

    try:
        async with httpx.AsyncClient(timeout=CAPTCHA_TIMEOUT_SECONDS) as client:
            response = await client.post(CAPTCHA_VERIFY_URL, data=payload)
            response.raise_for_status()
            data = response.json()
            return bool(data.get("success"))
    except Exception as exc:
        logger.warning("CAPTCHA verification failed: %s", exc)
        return False


def get_runtime_stats() -> dict:
    uptime_seconds = int(max(0, time.time() - START_TIME))
    memory_mb = None
    if psutil is not None:
        try:
            process = psutil.Process(os.getpid())
            memory_mb = round(process.memory_info().rss / (1024 * 1024), 2)
        except Exception:
            memory_mb = None
    return {
        "uptime_seconds": uptime_seconds,
        "memory_rss_mb": memory_mb,
    }


def get_dependencies_status() -> dict:
    model_files_present = os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH)
    return {
        "gemini_configured": bool(GEMINI_API_KEY),
        "gemini_client_initialized": gemini_client is not None,
        "model_files_present": model_files_present,
        "model_loaded": USE_LOCAL_MODEL,
        "model_version": MODEL_METADATA.get("model_version", MODEL_VERSION),
        "model_integrity_errors": model_integrity_errors,
        "no_store_mode": NO_STORE_MODE,
    }


def get_data_governance_status() -> dict:
    return {
        "submitted_text_retention_days": RETENTION_DAYS_SUBMITTED_TEXT,
        "request_text_persistence": "none" if RETENTION_DAYS_SUBMITTED_TEXT == 0 else "configured",
        "no_store_mode": NO_STORE_MODE,
        "dpa_contact_email": PRIVACY_CONTACT_EMAIL,
        "storage_policy": "No request body content is persisted by the API",
    }

# --- Helper Functions ---
def clean_text(text):
    """Advanced text preprocessing matching train_v3.py exactly."""
    if not isinstance(text, str):
        return ""

    # Count stylistic signals BEFORE lowering
    excl_count = text.count('!')
    question_count = text.count('?')
    caps_words = len([w for w in text.split() if w.isupper() and len(w) > 2])
    caps_ratio = sum(1 for c in text if c.isupper()) / max(len(text), 1)
    has_all_caps_phrases = bool(re.search(r'\b[A-Z]{3,}\b.*\b[A-Z]{3,}\b', text))

    text = text.lower()
    text = re.sub(r'http\S+|www\S+|https\S+', ' URL ', text, flags=re.MULTILINE)
    text = re.sub(r'@\w+', ' MENTION ', text)
    text = re.sub(r'#\w+', ' HASHTAG ', text)
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())

    # Append engineered pseudo-features as tokens
    if excl_count >= 2:
        text += ' FEAT_MANY_EXCLAMATIONS'
    if excl_count >= 5:
        text += ' FEAT_EXTREME_EXCLAMATIONS'
    if caps_ratio > 0.15:
        text += ' FEAT_HIGH_CAPS'
    if caps_ratio > 0.30:
        text += ' FEAT_EXTREME_CAPS'
    if caps_words >= 3:
        text += ' FEAT_MANY_CAPS_WORDS'
    if has_all_caps_phrases:
        text += ' FEAT_CAPS_PHRASES'
    if question_count >= 2:
        text += ' FEAT_MANY_QUESTIONS'
    if excl_count + question_count >= 4:
        text += ' FEAT_HEAVY_PUNCTUATION'

    # Detect urgency patterns
    urgency_words = ['breaking', 'urgent', 'alert', 'warning', 'exposed', 'leaked', 'banned', 'shocking', 'bombshell']
    urgency_count = sum(1 for w in urgency_words if w in text)
    if urgency_count >= 2:
        text += ' FEAT_HIGH_URGENCY'

    # Detect vague sourcing
    vague_sources = ['they don', 'they won', 'they are hiding', 'they don\'t want', 'doctors hate', 'doctors won', 'wake up', 'open your eyes', 'sheeple']
    if any(vs in text for vs in vague_sources):
        text += ' FEAT_VAGUE_SOURCE'

    return text


GEMINI_PROMPT = """You are an expert fact-checker, journalist, and misinformation analyst.

Your job is to determine whether the following text is REAL (factually accurate, from a credible source) or FAKE (misinformation, fabricated, misleading, sensationalized, or factually incorrect).

ANALYSIS RULES — check ALL of these:
1. FACTUAL ACCURACY — Are the claims in the text true? If the text contains false, misleading, or unverifiable claims, classify as "Fake".
2. SENSATIONALISM — Exaggerated language like "SHOCKING", "BREAKING", "You won't believe", all-caps, excessive exclamation marks = likely Fake.
3. CREDIBILITY MARKERS — Real news cites sources, uses measured language, and reports verifiable events.
4. LOGICAL CONSISTENCY — Does the text make internally consistent, logical claims?
5. CONSPIRACY PATTERNS — Unfounded conspiracy theories, anti-science claims, cover-up narratives without evidence = Fake.
6. SCIENTIFIC ACCURACY — Claims contradicting well-established science (flat earth, anti-vax misinformation, etc.) = Fake.

Article Text:
\"\"\"{text}\"\"\"

Respond with ONLY valid JSON (no markdown, no backticks, no explanation outside JSON):
{{"prediction": "Real" or "Fake", "confidence": float between 0.5 and 0.99, "explanation": "2-3 sentences explaining your reasoning with specific evidence from the text."}}"""


async def analyze_with_gemini(text: str) -> dict | None:
    """Use Gemini AI to fact-check and analyze the news text. Returns None on failure."""
    if not gemini_client:
        return None

    if not gemini_circuit.allow():
        logger.warning("Gemini circuit breaker open. Skipping Gemini call.")
        return None

    prompt = GEMINI_PROMPT.format(text=text)

    for model_name in GEMINI_MODELS:
        try:
            for attempt in range(GEMINI_MAX_RETRIES + 1):
                logger.info("Trying Gemini model: %s (attempt %d)", model_name, attempt + 1)
                response = await asyncio.wait_for(
                    asyncio.to_thread(
                        gemini_client.models.generate_content,
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.1,
                            max_output_tokens=500,
                        ),
                    ),
                    timeout=GEMINI_TIMEOUT_SECONDS,
                )
                response_text = response.text.strip()

                # Clean markdown wrappers
                if response_text.startswith("```json"):
                    response_text = response_text[7:]
                if response_text.startswith("```"):
                    response_text = response_text[3:]
                if response_text.endswith("```"):
                    response_text = response_text[:-3]
                response_text = response_text.strip()

                result = json.loads(response_text)

                prediction = result.get("prediction", "Fake")
                if prediction not in ["Real", "Fake"]:
                    prediction = "Fake"

                confidence = float(result.get("confidence", 0.75))
                confidence = max(0.5, min(0.99, confidence))

                explanation = result.get("explanation", "No detailed explanation available.")

                gemini_circuit.record_success()
                if GEMINI_SUCCESS is not None:
                    GEMINI_SUCCESS.inc()
                logger.info("Gemini (%s) result: %s (%.2f%%)", model_name, prediction, confidence * 100)
                return {
                    "prediction": prediction,
                    "confidence": confidence,
                    "explanation": f"[AI Fact-Check] {explanation}",
                    "model_version": MODEL_VERSION,
                }

        except Exception as e:
            error_msg = str(e)
            gemini_circuit.record_failure()
            logger.warning("Gemini model %s failed: %s", model_name, error_msg[:200])
            retryable = "quota" in error_msg.lower() or "429" in error_msg or "rate" in error_msg.lower() or "timeout" in error_msg.lower()
            if retryable and GEMINI_RETRY_JITTER_MS > 0:
                jitter = random.uniform(0, GEMINI_RETRY_JITTER_MS / 1000.0)
                await asyncio.sleep(jitter)
            continue

    logger.warning("All Gemini models failed. Falling back to local model.")
    return None


def analyze_with_local_model(text: str) -> dict:
    """Use local TF-IDF + Ensemble model as fallback for any type of claim."""
    cleaned = clean_text(text)
    vectorized = local_vectorizer.transform([cleaned])
    prediction = local_model.predict(vectorized)[0]
    probability = local_model.predict_proba(vectorized)[0]
    confidence = float(max(probability))
    prediction_text = "Fake" if prediction == 1 else "Real"

    return {
        "prediction": prediction_text,
        "confidence": confidence,
        "explanation": f"[ML Ensemble] Analysis based on linguistic patterns, writing style, sourcing quality, and textual features across multiple claim categories (confidence: {confidence:.2%}). Trained on 24,000+ diverse samples covering news, health, science, history, technology, and social media claims. Gemini AI is temporarily unavailable.",
        "model_version": MODEL_VERSION,
    }


# --- Pydantic Models ---
class NewsArticle(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        description="News article body to analyze.",
        examples=[
            "The Senate voted 67-33 to approve the Infrastructure Investment Act, allocating funds for bridge and road repairs."
        ],
    )
    captcha_token: Optional[str] = Field(default=None, description="Optional Turnstile token when captcha is enabled.")

class PredictionResponse(BaseModel):
    prediction: str = Field(..., examples=["Real"])
    confidence: float = Field(..., examples=[0.87])
    explanation: str = Field(..., examples=["[AI Fact-Check] The article uses source-attributed and internally consistent claims."])
    model_version: str = Field(default=MODEL_VERSION, examples=["v3"])


class ErrorResponse(BaseModel):
    error: str = Field(..., examples=["validation_error"])
    message: str = Field(..., examples=["Request validation failed."])


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    detail = exc.detail
    if isinstance(detail, dict):
        error = detail.get("error", "http_error")
        message = detail.get("message", "Request failed.")
    else:
        error = "http_error"
        message = str(detail)
    return JSONResponse(status_code=exc.status_code, content={"error": error, "message": message})


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Request validation failed.",
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled server exception: %s", exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected server error occurred.",
        },
    )

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
@app.get(f"{API_V1_PREFIX}", tags=["Health Check"])
def read_root():
    return {
        "status": "API is running",
        "gemini_enabled": gemini_client is not None,
        "local_model_loaded": USE_LOCAL_MODEL,
        "primary_analyzer": "gemini" if gemini_client else "local_model",
        "api_namespace": API_V1_PREFIX,
    }

@app.get("/health", tags=["Health Check"])
@app.get(f"{API_V1_PREFIX}/health", tags=["Health Check"])
def health_check():
    dependency_status = get_dependencies_status()
    return {
        "status": "alive",
        "environment": ENVIRONMENT,
        "dependencies": dependency_status,
        "runtime": get_runtime_stats(),
        "config_errors": runtime_config_errors,
        "data_governance": get_data_governance_status(),
    }


@app.get("/ready", tags=["Health Check"])
@app.get(f"{API_V1_PREFIX}/ready", tags=["Health Check"])
def readiness_check():
    dependency_status = get_dependencies_status()
    analyzer_ready = dependency_status["gemini_client_initialized"] or dependency_status["model_loaded"]
    config_ready = len(runtime_config_errors) == 0
    ready = analyzer_ready and config_ready
    payload = {
        "status": "ready" if ready else "not_ready",
        "environment": ENVIRONMENT,
        "dependencies": dependency_status,
        "runtime": get_runtime_stats(),
        "config_errors": runtime_config_errors,
    }
    if ready:
        return payload
    return JSONResponse(status_code=503, content=payload)


@app.get("/metrics", tags=["Health Check"])
@app.get(f"{API_V1_PREFIX}/metrics", tags=["Health Check"])
def metrics_endpoint():
    if generate_latest is None:
        return JSONResponse(
            status_code=503,
            content={"error": "metrics_unavailable", "message": "prometheus_client is not installed."},
        )
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get(f"{API_V1_PREFIX}/version-policy", tags=["Governance"])
def version_policy():
    return {
        "preferred_namespace": API_V1_PREFIX,
        "legacy_routes_supported": True,
        "policy": "New integrations should use /api/v1 routes. Legacy unversioned routes are maintained for backward compatibility and may be deprecated with notice.",
        "deprecation_notice_min_days": 180,
        "contact": PRIVACY_CONTACT_EMAIL,
    }


@app.post(
    "/predict",
    response_model=PredictionResponse,
    tags=["AI Analysis"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        413: {"model": ErrorResponse, "description": "Payload too large"},
        429: {"model": ErrorResponse, "description": "Rate limited"},
        503: {"model": ErrorResponse, "description": "Analysis unavailable"},
    },
)
@app.post(
    f"{API_V1_PREFIX}/predict",
    response_model=PredictionResponse,
    tags=["AI Analysis"],
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        413: {"model": ErrorResponse, "description": "Payload too large"},
        429: {"model": ErrorResponse, "description": "Rate limited"},
        503: {"model": ErrorResponse, "description": "Analysis unavailable"},
    },
)
async def predict(article: NewsArticle, request: Request):
    """Analyze news text using Gemini AI (primary) with local ML fallback."""
    client_ip = get_client_ip(request)

    allowed, reason, retry_after = rate_limiter.check(client_ip)
    if not allowed:
        headers = {}
        if retry_after:
            headers["Retry-After"] = str(retry_after)
        raise HTTPException(
            status_code=429,
            detail={
                "error": reason or "rate_limit_exceeded",
                "message": "Too many requests. Please retry later.",
            },
            headers=headers,
        )

    text = article.text.strip()
    if not text:
        raise HTTPException(
            status_code=400,
            detail={"error": "empty_text", "message": "Text cannot be empty."},
        )
    if len(text) < MIN_TEXT_CHARS:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "text_too_short",
                "message": f"Text must be at least {MIN_TEXT_CHARS} characters.",
            },
        )
    if len(text) > MAX_TEXT_CHARS:
        raise HTTPException(
            status_code=413,
            detail={
                "error": "text_too_long",
                "message": f"Text exceeds maximum length of {MAX_TEXT_CHARS} characters.",
            },
        )

    if CAPTCHA_ENABLED:
        if not article.captcha_token:
            raise HTTPException(
                status_code=400,
                detail={"error": "captcha_required", "message": "Captcha token is required."},
            )
        captcha_ok = await verify_captcha(article.captcha_token, client_ip)
        if not captcha_ok:
            raise HTTPException(
                status_code=400,
                detail={"error": "captcha_failed", "message": "Captcha verification failed."},
            )

    # Check cache (disabled in no-store mode)
    if cache is not None:
        cached = cache.get(text)
        if cached is not None:
            return cached

    logger.info("New prediction request (%d chars).", len(text))

    # --- PRIMARY: Gemini AI (fact-checks content + writing style) ---
    result = await analyze_with_gemini(text)

    # --- FALLBACK: Local ML model (style-based only) ---
    if result is None and USE_LOCAL_MODEL:
        try:
            result = analyze_with_local_model(text)
            if GEMINI_FALLBACK is not None:
                GEMINI_FALLBACK.inc()
        except Exception as e:
            logger.warning("Local model also failed: %s", e)

    if result is None:
        raise HTTPException(
            status_code=503,
            detail={
                "error": "analysis_unavailable",
                "message": "Analysis unavailable. Gemini API may be unavailable and local model failed.",
            },
        )

    response = PredictionResponse(**result)

    # Cache it
    if cache is not None:
        cache.set(text, response)

    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
