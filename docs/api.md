# HTTP API

## Network binding

The bridge binds to `0.0.0.0:8765` by default.

OpenClaw (or any client) must be able to reach this host on this port.
If needed, adjust the port in the add-in and plugin config together.

- Local: `http://127.0.0.1:8765`
- LAN: `http://<fusion-host-ip>:8765`

## `GET /ping`

Health check endpoint.

### Response

```json
{
  "ok": true,
  "service": "fusion-bridge",
  "version": "0.3.0"
}
```

## `GET /state`

Returns runtime status including queue and execution state.

### Example response

```json
{
  "ok": true,
  "fusionRunning": true,
  "documentName": "Unnamed",
  "hasActiveDesign": true,
  "rootComponentName": "RootComponent",
  "queueSize": 0,
  "busy": false,
  "currentJobId": null,
  "pumpMode": "custom-event"
}
```

## `GET /logs`

Returns recent add-in log lines.

### Example response

```json
{
  "ok": true,
  "lines": [
    "{\"ts\":\"...\",\"event\":\"addin_started\"}"
  ]
}
```

## `POST /exec`

Execute Python code in Fusion context.

### Request

```json
{
  "code": "print('hello from fusion')",
  "timeoutSeconds": 300
}
```

- `code` is required and must be a non-empty string.
- `timeoutSeconds` is optional.
- Values above `300` are clamped to `300`.
- No artificial limit on script length is enforced by the bridge.

### Success response

```json
{
  "ok": true,
  "stdout": "hello from fusion\n",
  "result": null,
  "error": null,
  "durationMs": 3,
  "jobId": "..."
}
```

### Error response

```json
{
  "ok": false,
  "stdout": "",
  "result": null,
  "error": "Traceback ...",
  "durationMs": 3,
  "jobId": "..."
}
```

### Timeout response

```json
{
  "ok": false,
  "error": "execution timeout",
  "jobId": "..."
}
```

## OpenClaw plugin

The OpenClaw plugin in this repository exposes equivalent tools:

- `fusion_bridge_ping`
- `fusion_bridge_state`
- `fusion_bridge_logs`
- `fusion_bridge_exec`

## Client convenience

The local CLI also supports inline code:

```bash
python3 bridge-client/call_exec.py --code "print(app_info())"
```
