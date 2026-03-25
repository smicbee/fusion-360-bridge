# Installation (PoC)

## 1. Add-in-Dateien ablegen

Den Ordner `fusion-addin/FusionBridge` in den Fusion-Add-ins-Ordner kopieren.

Typische Pfade:

### Windows

```text
%appdata%\Autodesk\Autodesk Fusion\API\AddIns\FusionBridge
```

### macOS

```text
~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/FusionBridge
```

## 2. Fusion starten

- Fusion 360 öffnen
- `Scripts and Add-Ins` öffnen
- Add-in `FusionBridge` auswählen
- `Run` klicken

## 3. Bridge testen

Im Browser oder Terminal:

```bash
curl http://127.0.0.1:8765/ping
python3 bridge-client/call_exec.py --state
```

## 4. Beispielcode ausführen

```bash
python3 bridge-client/call_exec.py examples/ping.py
python3 bridge-client/call_exec.py examples/create_box.py
python3 bridge-client/call_exec.py --logs
```

## 5. Logdatei

Das Add-in schreibt eine einfache JSONL-Logdatei in den Add-in-Ordner:

```text
fusion-addin/FusionBridge/fusion_bridge.log
```

## Hinweis

Das ist weiter ein frühes PoC-Gerüst. Die kritischsten Teile für Requests, Logging und Timeout-Verhalten sind jetzt vorbereitet, aber die konkrete Timer-/Event-Anbindung in Fusion muss auf deinem echten Setup validiert werden.
