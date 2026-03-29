# Changelog

## [Unreleased]

### Changed
- Removed startup/status UI popups from the Fusion add-in (`FusionBridge.py`) to avoid UI interruption during automation.
- `show_message(...)` in `fusion_helpers.py` no longer opens popups and now returns `False` to keep execution headless-safe.
- Repository documentation is now fully in English.

### Added
- Added OpenClaw plugin package at `openclaw-plugin/` with tools:
  - `fusion_bridge_ping`
  - `fusion_bridge_state`
  - `fusion_bridge_logs`
  - `fusion_bridge_exec`
- Expanded docs with deployment, API, architecture, installation, and startup guidance.
- Added explicit deployment note: Fusion host must be reachable from OpenClaw on port `8765`.

## [0.1.0] - Initial public release
- Fusion 360 HTTP Bridge add-in (`/ping`, `/state`, `/logs`, `/exec`)
- Bridge client (`bridge-client/call_exec.py`)
- API and installation documentation plus examples
