# Architecture

## Overview

The bridge has four main parts:

1. **Fusion Add-in**
   - Runs in Autodesk Fusion 360.
   - Provides a real Fusion API context (`adsk`, active document, design, etc.).
   - Pulls jobs from an in-process queue.

2. **HTTP listener**
   - Exposes network endpoints:
     - `/ping`
     - `/state`
     - `/logs`
     - `/exec`

3. **Executor**
   - Executes Python code in Fusion context.
   - Captures stdout, exceptions, optional return values, and runtime metadata.

4. **Runtime pump**
   - Triggers job processing in the UI thread context.
   - Uses `custom-event` by default and falls back to timer mode when needed.

## Flow

1. OpenClaw tool or CLI sends a `POST /exec` request.
2. Add-in queue creates a job and schedules it.
3. Runtime pump wakes and executes one pending job.
4. Executor runs Python code in prepared context.
5. Execution result is returned to the waiting HTTP request.

## Execution context

Executed snippets typically receive:

- `adsk`
- `app`
- `ui`
- `product`
- `design`
- `rootComp`
- `document`
- `result` (optional return object)
- `helpers` module and convenience wrappers

## Design choice

There is no restrictive DSL in this bridge version.
Raw Python is intentionally supported so every Fusion capability remains available.

## Runtime strategy

Fusion event handling differs between machines and versions.
The bridge uses a two-stage strategy:

- Primary: custom event pump
- Fallback: timer-based pump

The active pump mode is exposed in `/state` as `pumpMode`.

## Known risks

- No authentication by default.
- Any Python code sent to `/exec` is executed in Fusion.
- A failed script can modify the active design.
- HTTP timeout does not cancel already running in-application Python immediately.
- Behavior still depends on validation in a real Fusion environment.
