# Test-Checkliste für erstes echtes Fusion-Setup

## Start

1. Add-in in Fusion laden
2. Popup "FusionBridge gestartet ..." erscheint
3. `curl http://127.0.0.1:8765/ping`
4. `python3 bridge-client/call_exec.py --state`

## Prüfen

- Antwort kommt ohne Hänger zurück
- `pumpMode` ist gesetzt (`custom-event` oder `timer`)
- `busy` ist im Idle `false`
- `queueSize` ist im Idle `0`

## Exec-Test

```bash
python3 bridge-client/call_exec.py examples/ping.py
python3 bridge-client/call_exec.py examples/get_state.py
python3 bridge-client/call_exec.py examples/create_box.py
```

## Wenn etwas hakt

```bash
python3 bridge-client/call_exec.py --logs
```

Zusätzlich die Datei `fusion_bridge.log` im Add-in-Ordner prüfen.

## Ziel für den ersten Test

- `/ping` funktioniert
- `/state` funktioniert
- mindestens `examples/ping.py` läuft erfolgreich
- idealerweise erzeugt `examples/create_box.py` einen Body in Fusion
