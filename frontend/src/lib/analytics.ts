type TelemetryValue = string | number | boolean | null;
type TelemetryPayload = Record<string, TelemetryValue>;

const ANALYTICS_ENDPOINT = import.meta.env.VITE_ANALYTICS_ENDPOINT || '';
const ANALYTICS_ENABLED = import.meta.env.VITE_ANALYTICS_ENABLED !== 'false';

const BLOCKED_KEYS = ['text', 'article', 'body', 'content'];

const sanitizePayload = (payload: TelemetryPayload): TelemetryPayload => {
  const sanitized: TelemetryPayload = {};
  for (const [key, value] of Object.entries(payload)) {
    const lowerKey = key.toLowerCase();
    if (BLOCKED_KEYS.some((blocked) => lowerKey.includes(blocked))) {
      continue;
    }
    if (typeof value === 'string') {
      sanitized[key] = value.slice(0, 120);
    } else {
      sanitized[key] = value;
    }
  }
  return sanitized;
};

export const trackEvent = (event: string, payload: TelemetryPayload = {}): void => {
  if (!ANALYTICS_ENABLED) {
    return;
  }

  const eventPayload = {
    event,
    timestamp: new Date().toISOString(),
    ...sanitizePayload(payload),
  };

  if (!ANALYTICS_ENDPOINT) {
    if (import.meta.env.DEV) {
      console.info('[telemetry]', eventPayload);
    }
    return;
  }

  try {
    const body = JSON.stringify(eventPayload);
    if (navigator.sendBeacon) {
      const blob = new Blob([body], { type: 'application/json' });
      navigator.sendBeacon(ANALYTICS_ENDPOINT, blob);
      return;
    }

    void fetch(ANALYTICS_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
    });
  } catch {
    // Telemetry should never block user flows.
  }
};
