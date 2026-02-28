
import json
import socket
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import joblib
import re
import string
import numpy as np
import traceback

# --- Force IPv4 for all DNS lookups ---
# Fixes: Python prefers IPv6 which times out on some networks
_original_getaddrinfo = socket.getaddrinfo

def _ipv4_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    if family == 0:
        family = socket.AF_INET  # Force IPv4
    return _original_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = _ipv4_getaddrinfo
print("DNS forced to IPv4 (IPv6 workaround active).")

# --- Configuration ---
load_dotenv()

# Configure Gemini API (Primary analysis engine)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_client = None
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found. Will rely on local model only.")
else:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        print("Gemini API client initialized (primary analyzer).")
    except Exception as e:
        print(f"WARNING: Gemini client init failed: {e}")

# Model fallback chain — try each in order
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.0-flash",
    "gemini-2.5-flash-lite",
    "gemini-3-flash-preview",
]

# --- Directories ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
VECTORIZER_PATH = os.path.join(MODEL_DIR, "vectorizer.pkl")

# --- Load Local Model (secondary / fallback) ---
USE_LOCAL_MODEL = False
try:
    print("Loading local model...")
    local_model = joblib.load(MODEL_PATH)
    local_vectorizer = joblib.load(VECTORIZER_PATH)
    print("Local model loaded successfully (fallback analyzer).")
    USE_LOCAL_MODEL = True
except Exception as e:
    print(f"WARNING: Could not load local model: {e}")

# --- App Initialization ---
app = FastAPI(
    title="Fake News Detector API",
    description="An API to detect fake news using Gemini AI with local ML fallback.",
    version="2.0.0"
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --- In-memory Cache ---
cache = {}

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

    prompt = GEMINI_PROMPT.format(text=text)

    for model_name in GEMINI_MODELS:
        try:
            print(f"  Trying Gemini model: {model_name}")
            response = gemini_client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.1,
                    max_output_tokens=500,
                )
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

            print(f"  Gemini ({model_name}) result: {prediction} ({confidence:.2%})")
            return {
                "prediction": prediction,
                "confidence": confidence,
                "explanation": f"[AI Fact-Check] {explanation}"
            }

        except Exception as e:
            error_msg = str(e)
            print(f"  Gemini model {model_name} failed: {error_msg[:200]}")
            # If quota exceeded, try next model
            if "quota" in error_msg.lower() or "429" in error_msg or "rate" in error_msg.lower():
                continue
            # For other errors, try next model too
            continue

    print("  All Gemini models failed. Falling back to local model.")
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
        "explanation": f"[ML Ensemble] Analysis based on linguistic patterns, writing style, sourcing quality, and textual features across multiple claim categories (confidence: {confidence:.2%}). Trained on 24,000+ diverse samples covering news, health, science, history, technology, and social media claims. Gemini AI is temporarily unavailable."
    }


# --- Pydantic Models ---
class NewsArticle(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    prediction: str
    confidence: float
    explanation: str

# --- API Endpoints ---
@app.get("/", tags=["Health Check"])
def read_root():
    return {
        "status": "API is running",
        "gemini_enabled": gemini_client is not None,
        "local_model_loaded": USE_LOCAL_MODEL,
        "primary_analyzer": "gemini" if gemini_client else "local_model"
    }

@app.post("/predict", response_model=PredictionResponse, tags=["AI Analysis"])
async def predict(article: NewsArticle):
    """Analyze news text using Gemini AI (primary) with local ML fallback."""
    if not article.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    # Check cache
    if article.text in cache:
        return cache[article.text]

    print(f"\n--- New prediction request ({len(article.text)} chars) ---")

    # --- PRIMARY: Gemini AI (fact-checks content + writing style) ---
    result = await analyze_with_gemini(article.text)

    # --- FALLBACK: Local ML model (style-based only) ---
    if result is None and USE_LOCAL_MODEL:
        try:
            result = analyze_with_local_model(article.text)
        except Exception as e:
            print(f"  Local model also failed: {e}")

    if result is None:
        raise HTTPException(
            status_code=503,
            detail="Analysis unavailable. Gemini API quota may be exhausted and local model failed. Please try again later."
        )

    response = PredictionResponse(**result)

    # Cache it
    if len(cache) > 200:
        cache.pop(next(iter(cache)))
    cache[article.text] = response

    return response
