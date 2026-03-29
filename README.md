# Fusion 360 Bridge

A small HTTP bridge for Autodesk Fusion 360 that executes Python inside the Fusion context.

This repository contains:

1. **Fusion 360 Add-in** in `fusion-addin/FusionBridge`
2. **CLI helpers** in `bridge-client`
3. **OpenClaw plugin** in `openclaw-plugin`

The add-in exposes four endpoints:

- `GET /ping`
- `GET /state`
- `GET /logs`
- `POST /exec`

The bridge runs on TCP port `8765` by default.

## Quick start

### 1) Install the Fusion add-in

Copy `fusion-addin/FusionBridge` into your local Fusion Add-ins directory:

- **Windows**: `%appdata%\\Autodesk\\Autodesk Fusion\\API\\AddIns\\`
- **macOS**: `~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/`

Then in Fusion:

1. Open **Scripts and Add-Ins**
2. Load `FusionBridge`
3. Click **Run**

> **Important (network):** the machine running Fusion must be reachable from OpenClaw on **port 8765**.
> If OpenClaw runs on another host, open/firewall rules must allow access to `TCP 8765`.

### 2) Install the OpenClaw plugin

```bash
cd <path-to-openclaw-workspace>
openclaw plugins install --link <path-to-repo>/openclaw-plugin
```

Then enable and configure it in OpenClaw (example):

```yaml
plugins:
  entries:
    fusion-360-bridge:
      enabled: true
      config:
        baseUrl: http://<fusion-host-ip>:8765
        timeoutMs: 10000
```

If your bridge runs locally and you run OpenClaw on the same machine, `http://<bridge-host>:8765` is enough.

### 3) Verify connectivity

```bash
curl http://<fusion-host-or-local>:8765/ping
curl http://<fusion-host-or-local>:8765/state
python3 bridge-client/call_exec.py --code "print(app_info())"
```

## Execution model

- The HTTP server receives jobs on `/exec`.
- Jobs are queued.
- A runtime pump inside Fusion processes jobs serially.
- Execution is in raw Python context (`adsk`, `app`, `ui`, `design`, etc. are available).

This intentionally stays **unrestricted** by default: raw Python is allowed whenever helpers are not enough.

## Available helpers

In addition to full raw Python, the helper layer exposes:

- `app_info()`
- `show_message(text)`
- `list_occurrences()`
- `list_bodies()`
- `create_box(width, height, depth)`

These are convenience wrappers and **not required**.

## Example files

- `examples/app_info.py`
- `examples/list_bodies.py`
- `examples/list_occurrences.py`
- `examples/show_popup.py`
- `examples/create_demo_box.py`
- `examples/create_box.py`
- `examples/get_state.py`
- `examples/ping.py`

## Docs

- `docs/install.md`
- `docs/architecture.md`
- `docs/api.md`
- `docs/testing-checklist.md`
- `docs/release-checklist.md`

## Client

The Python CLI supports inline code and file-based execution:

```bash
python3 bridge-client/call_exec.py --code "print(app_info())"
python3 bridge-client/call_exec.py examples/get_state.py
python3 bridge-client/call_exec.py --state
python3 bridge-client/call_exec.py --logs
```
