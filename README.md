# Fusion 360 Bridge

Offene Bridge für Autodesk Fusion 360, damit ein externes System Python-Code im Fusion-Kontext ausführen kann.

## Status

Die Bridge läuft jetzt als nutzbarer Remote-Exec-Stack:

- HTTP-Server (`/ping`, `/state`, `/logs`, `/exec`)
- serielle Job-Queue
- Runtime-Pump mit beobachtbarem Modus
- LAN-Zugriff möglich
- rohes Python bleibt erlaubt
- zusätzliche Helper-Funktionen für häufige Aufgaben sind verfügbar

## Exec-Kontext

Neben dem offenen Python-Kontext stehen jetzt auch Helper bereit:

- `helpers`
- `app_info()`
- `show_message(text)`
- `list_occurrences()`
- `list_bodies()`
- `create_box(width, height, depth)`

Wichtig: Diese Helper sind Komfortfunktionen. Rohes Python bleibt jederzeit möglich und ist weiterhin der Escape Hatch für alles, was noch nicht abstrahiert wurde.

## Nützliche Beispiele

- `examples/app_info.py`
- `examples/list_bodies.py`
- `examples/list_occurrences.py`
- `examples/show_popup.py`
- `examples/create_demo_box.py`
- `examples/create_box.py`
- `examples/get_state.py`

## Client

Der kleine CLI-Client unterstützt jetzt:

- Dateiausführung
- `--code` für Inline-Python
- `--state`
- `--logs`
- `--timeout`

Beispiel:

```bash
python3 bridge-client/call_exec.py --code "print(app_info())"
```