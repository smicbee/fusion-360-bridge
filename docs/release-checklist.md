# Fusion 360 Bridge – Release Checklist

## Purpose
Release both parts:
1. Fusion 360 add-in (`fusion-addin/FusionBridge`)
2. OpenClaw plugin (`openclaw-plugin`)

## 1) Preflight
- [ ] Working tree is clean or intentionally staged
- [ ] Version/tag is set (`SemVer`)
- [ ] No secrets in repo (`.env`, tokens, local logs)
- [ ] Debug popups in add-in are removed/disabled

## 2) Add-in validation
- [ ] Add-in starts without UI blockers
- [ ] `/ping` returns `ok`
- [ ] `/state` returns runtime status
- [ ] `/exec` runs a test script (e.g. `app_info()`)
- [ ] Error paths return structured responses

## 3) OpenClaw plugin validation
- [ ] Plugin installed and enabled in OpenClaw
- [ ] Plugin tools (`fusion_bridge_ping`, `fusion_bridge_state`, `fusion_bridge_logs`, `fusion_bridge_exec`) work
- [ ] Raw-Python fallback remains documented and usable
- [ ] Basic workflows from `examples/*` tested
- [ ] Troubleshooting section is up to date

## 4) Documentation
- [ ] `README.md` updated (architecture + quick start)
- [ ] `docs/install.md` updated (including network/port requirement)
- [ ] `docs/api.md` updated
- [ ] Plugin README and changelog entry prepared

## 5) GitHub release
- [ ] Create tag (`vX.Y.Z`)
- [ ] Add release notes
- [ ] Include install notes and known limitations

## 6) Post-release
- [ ] Smoke test after tag/release
- [ ] Announce to community/Discord if applicable
- [ ] Capture early issues and prioritize
