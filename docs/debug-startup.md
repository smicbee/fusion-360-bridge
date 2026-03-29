# Startup and troubleshooting guide

## What the add-in does now

The add-in starts the HTTP bridge and background queue processor in a single run.
No launch-only debug mode exists anymore.

## Startup checks

On startup, check:

- add-in status in Fusion
- file `fusion_bridge_boot.log` exists in the add-in folder
- `/ping` responds
- `/state` returns valid JSON

## If startup fails

1. Confirm `FusionBridge` is present in:
   - `%appdata%\\Autodesk\\Autodesk Fusion\\API\\AddIns\\` (Windows)
   - `~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/` (macOS)
2. Open Fusion **Scripts and Add-Ins** and ensure the add-in is allowed to run.
3. If reachable locally but not remotely, verify LAN and firewall settings for port `8765`.
4. Open and inspect `fusion_bridge_boot.log` for import or pump initialization errors.
