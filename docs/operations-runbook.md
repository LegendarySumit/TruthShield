# TruthShield Operations Runbook

## Incident Response Runbook

1. Detect
- Trigger sources: 5xx alert threshold, high latency alerts, failed health checks, or user-reported outage.
- Confirm blast radius: check `/api/v1/health`, `/api/v1/ready`, and frontend availability.

2. Triage
- Classify severity:
- `SEV-1`: full outage or incorrect predictions at scale.
- `SEV-2`: degraded performance or partial feature failure.
- `SEV-3`: minor issue with workaround.
- Open incident channel and assign incident commander + comms owner.

3. Contain
- If Gemini provider is unstable, rely on local model fallback and reduce retry pressure.
- If traffic abuse is detected, tighten rate-limit env variables and redeploy.
- If a bad release is suspected, start rollback immediately.

4. Recover
- Validate `/api/v1/ready` becomes healthy.
- Confirm frontend can submit and receive predictions.
- Monitor metrics for 30 minutes after mitigation.

5. Review
- Publish post-incident report within 48 hours.
- Document root cause, customer impact, timeline, and corrective actions.

## Backup and Rollback Strategy

1. Artifact discipline
- Keep model artifacts versioned with `model_version` metadata.
- Keep immutable container image tags for each release.

2. Backup
- Persist training metadata and evaluation reports from `backend/models/`.
- Export environment variables securely from host platform before major changes.

3. Rollback
- Roll back backend to previous known-good image or git SHA.
- Roll back frontend to previous successful deployment.
- Re-run smoke checks immediately after rollback.

## Post-Deploy Verification Checklist

1. API verification
- `GET /api/v1/health` returns `alive`.
- `GET /api/v1/ready` returns `ready`.
- `POST /api/v1/predict` succeeds on a known-good sample.

2. Functional verification
- Confirm timeout/retry UX works for simulated network delays.
- Confirm offline banner appears when browser is offline.
- Confirm error boundary fallback screen renders if a crash is triggered.
- Confirm browser E2E prediction flow passes in CI (`frontend-e2e` job) using `VITE_CAPTCHA_BYPASS=true` test-mode bypass.

3. Trust and governance verification
- Confirm response contains `model_version`.
- Confirm no telemetry payload contains submitted article text.
- Confirm `NO_STORE_MODE=true` disables cache behavior and emits `Cache-Control: no-store`.

4. Security verification
- Run CI security scans and ensure all jobs are green.
- Verify CORS and trusted host settings match production domains.
