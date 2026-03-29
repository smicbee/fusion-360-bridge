# Fusion 360 Bridge (OpenClaw Plugin)

This package exposes the Fusion 360 Bridge endpoints to OpenClaw as tools.
It is intended to be used only when the Fusion 360 add-in is installed and running on a machine reachable from OpenClaw.

## Tools

- `fusion_bridge_ping`
  - `GET /ping` health check
- `fusion_bridge_state`
  - `GET /state` runtime status, queue status and pump state
- `fusion_bridge_logs`
  - `GET /logs` debug/event log output
- `fusion_bridge_exec`
  - `POST /exec` raw Python execution in Fusion

## Install from local checkout

```bash
cd /home/smicbee/.openclaw/workspace
openclaw plugins install --link /home/smicbee/Ideenschmiede/projektFiles/fusion-360-bridge/openclaw-plugin
```

## Minimal plugin config

```yaml
plugins:
  entries:
    fusion-360-bridge:
      enabled: true
      config:
        # IP of machine running Fusion 360
        baseUrl: http://192.168.2.113:8765
        # HTTP timeout for plugin requests
        timeoutMs: 10000
```

## Notes

- The default bridge port is **8765**.
- For remote calls, the Fusion host must be reachable on that port from the OpenClaw machine.
- The add-in executes raw Python directly. Keep scripts idempotent for safer automation.
- No authentication is implemented yet; do not expose the bridge publicly.
