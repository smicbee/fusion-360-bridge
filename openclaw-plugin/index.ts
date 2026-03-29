import { definePluginEntry } from "openclaw/plugin-sdk/plugin-entry";

type PluginConfig = {
  baseUrl?: string;
  timeoutMs?: number;
};

type BridgeResponse = {
  ok?: boolean;
  [key: string]: unknown;
};

type Dict = Record<string, unknown>;

const DEFAULT_BASE_URL = "http://127.0.0.1:8765";
const DEFAULT_TIMEOUT_MS = 10_000;
const MAX_EXEC_TIMEOUT_SECONDS = 300;

function normalizeBaseUrl(input?: string): string {
  const raw = (input ?? DEFAULT_BASE_URL).trim();
  if (!raw) {
    return DEFAULT_BASE_URL;
  }

  const withScheme = /^https?:\/\//i.test(raw) ? raw : `http://${raw}`;
  const url = new URL(withScheme);
  return `${url.origin}`;
}

function resolveConfig(cfg: PluginConfig, overrideUrl?: string, overrideTimeoutMs?: number) {
  const baseUrl = normalizeBaseUrl(overrideUrl ?? cfg.baseUrl ?? DEFAULT_BASE_URL);

  const timeoutMs =
    typeof overrideTimeoutMs === "number" && Number.isFinite(overrideTimeoutMs) && overrideTimeoutMs > 0
      ? overrideTimeoutMs
      : typeof cfg.timeoutMs === "number" && cfg.timeoutMs > 0
        ? cfg.timeoutMs
        : DEFAULT_TIMEOUT_MS;

  return { baseUrl, timeoutMs };
}

async function fetchWithTimeout<T>(url: string, timeoutMs: number, options: RequestInit = {}): Promise<T> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, {
      ...options,
      signal: options.signal ?? controller.signal,
      headers: {
        Accept: "application/json",
        ...(options.headers ?? {}),
      },
    });

    const text = await response.text();
    if (!text) {
      if (!response.ok) {
        throw new Error(`Bridge request failed with HTTP ${response.status}`);
      }
      return {} as T;
    }

    let parsed: T;
    try {
      parsed = JSON.parse(text) as T;
    } catch {
      if (response.ok) {
        throw new Error(`Bridge returned non-JSON response: ${text.slice(0, 200)}`);
      }
      throw new Error(`Bridge request failed with HTTP ${response.status}: ${text.slice(0, 200)}`);
    }

    if (!response.ok) {
      throw new Error(`Bridge request failed with HTTP ${response.status}: ${JSON.stringify(parsed)}`);
    }

    return parsed;
  } catch (error) {
    if (error instanceof DOMException && error.name === "AbortError") {
      throw new Error(`Bridge request timed out after ${timeoutMs} ms`);
    }
    throw error as Error;
  } finally {
    clearTimeout(timer);
  }
}

function toResult(data: unknown): string {
  return JSON.stringify(data, null, 2);
}

function clampExecTimeout(seconds?: number): number {
  if (typeof seconds !== "number" || !Number.isFinite(seconds) || seconds <= 0) {
    return 300;
  }

  if (seconds > MAX_EXEC_TIMEOUT_SECONDS) {
    return MAX_EXEC_TIMEOUT_SECONDS;
  }

  return seconds;
}

function normalizePayload(params: { code?: string; timeoutSeconds?: number }): Dict {
  const code = (params.code ?? "").trim();
  if (!code) {
    throw new Error("code is required and must be a non-empty string");
  }

  return {
    code,
    timeoutSeconds: clampExecTimeout(params.timeoutSeconds),
  };
}

export default definePluginEntry({
  id: "fusion-360-bridge",
  name: "Fusion 360 Bridge",
  description: "Controls an installed Fusion 360 add-in bridge instance from OpenClaw.",
  register(api) {
    const cfg = (api.pluginConfig ?? {}) as PluginConfig;

    api.registerTool(
      () => ({
        name: "fusion_bridge_ping",
        description: "Check if the Fusion 360 Bridge add-in is reachable and healthy.",
        parameters: {
          type: "object" as const,
          properties: {
            baseUrl: {
              type: "string",
              description: "Optional override for the bridge base URL (defaults to plugin config).",
            },
            timeoutMs: {
              type: "number",
              description: "HTTP timeout in milliseconds.",
            },
          },
          required: [],
        },
        async execute(_toolCallId: string, params: { baseUrl?: string; timeoutMs?: number }) {
          const { baseUrl, timeoutMs } = resolveConfig(cfg, params?.baseUrl, params?.timeoutMs);
          const response = await fetchWithTimeout<BridgeResponse>(`${baseUrl}/ping`, timeoutMs);
          return toResult(response);
        },
      }),
      { names: ["fusion_bridge_ping"] },
    );

    api.registerTool(
      () => ({
        name: "fusion_bridge_state",
        description: "Read runtime state from the bridge: queue, busy flag, active job id and pump mode.",
        parameters: {
          type: "object" as const,
          properties: {
            baseUrl: {
              type: "string",
              description: "Optional override for the bridge base URL (defaults to plugin config).",
            },
            timeoutMs: {
              type: "number",
              description: "HTTP timeout in milliseconds.",
            },
          },
          required: [],
        },
        async execute(_toolCallId: string, params: { baseUrl?: string; timeoutMs?: number }) {
          const { baseUrl, timeoutMs } = resolveConfig(cfg, params?.baseUrl, params?.timeoutMs);
          const response = await fetchWithTimeout<BridgeResponse>(`${baseUrl}/state`, timeoutMs);
          return toResult(response);
        },
      }),
      { names: ["fusion_bridge_state"] },
    );

    api.registerTool(
      () => ({
        name: "fusion_bridge_logs",
        description: "Read recent bridge log lines from the add-in-side buffer.",
        parameters: {
          type: "object" as const,
          properties: {
            baseUrl: {
              type: "string",
              description: "Optional override for the bridge base URL (defaults to plugin config).",
            },
            timeoutMs: {
              type: "number",
              description: "HTTP timeout in milliseconds.",
            },
          },
          required: [],
        },
        async execute(_toolCallId: string, params: { baseUrl?: string; timeoutMs?: number }) {
          const { baseUrl, timeoutMs } = resolveConfig(cfg, params?.baseUrl, params?.timeoutMs);
          const response = await fetchWithTimeout<BridgeResponse>(`${baseUrl}/logs`, timeoutMs);
          return toResult(response);
        },
      }),
      { names: ["fusion_bridge_logs"] },
    );

    api.registerTool(
      () => ({
        name: "fusion_bridge_exec",
        description: "Execute raw Python code in the active Fusion 360 session via `/exec`.",
        parameters: {
          type: "object" as const,
          properties: {
            code: {
              type: "string",
              description: "Python code to execute in Fusion.",
            },
            timeoutSeconds: {
              type: "number",
              description: "Execution timeout in seconds (max 300).",
            },
            baseUrl: {
              type: "string",
              description: "Optional override for the bridge base URL (defaults to plugin config).",
            },
            timeoutMs: {
              type: "number",
              description: "HTTP timeout in milliseconds.",
            },
          },
          required: ["code"],
        },
        async execute(
          _toolCallId: string,
          params: { code?: string; timeoutSeconds?: number; baseUrl?: string; timeoutMs?: number },
        ) {
          const { baseUrl, timeoutMs } = resolveConfig(cfg, params?.baseUrl, params?.timeoutMs);
          const payload = normalizePayload({
            code: params?.code,
            timeoutSeconds: params?.timeoutSeconds,
          });

          const response = await fetchWithTimeout<BridgeResponse>(`${baseUrl}/exec`, timeoutMs, {
            method: "POST",
            body: JSON.stringify(payload),
            headers: {
              "Content-Type": "application/json",
            },
          });

          return toResult(response);
        },
      }),
      { names: ["fusion_bridge_exec"] },
    );
  },
});
