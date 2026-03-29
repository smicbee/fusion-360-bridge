# Initial verification checklist

## 1) Start and connect

1. Load `FusionBridge` in Fusion.
2. Confirm `/state` and `/ping` respond:

```bash
curl http://127.0.0.1:8765/ping
curl http://127.0.0.1:8765/state
```

3. If Fusion is on another host, replace `127.0.0.1` with that host IP and ensure port `8765` is reachable.

## 2) Sanity checks

- Response returns quickly.
- `/state` shows valid fields (`pumpMode`, `busy`, `queueSize`).
- `busy` is `false` on idle.
- `queueSize` is `0` on idle.

## 3) Execution tests

```bash
python3 bridge-client/call_exec.py examples/ping.py
python3 bridge-client/call_exec.py examples/get_state.py
python3 bridge-client/call_exec.py examples/create_box.py
```

## 4) OpenClaw plugin checks (if installed)

From within OpenClaw, run the plugin tools:

- `fusion_bridge_ping`
- `fusion_bridge_state`
- `fusion_bridge_exec`

Use `fusion_bridge_exec` with a small script such as:

```python
print("hello from fusion")
```

If execution fails, read logs:

```bash
python3 bridge-client/call_exec.py --logs
```

Also inspect `fusion_bridge_boot.log` in the add-in folder.

## 5) Acceptance

- `/ping` works.
- `/state` works.
- `examples/ping.py` succeeds.
- `fusion_bridge_exec` from OpenClaw or CLI can run a minimal print.
