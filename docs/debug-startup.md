# Debug-Startup-Modus

## Aktueller Stand: Debug-Stufe 2

Diese Version von `FusionBridge.py` ist weiterhin reduziert, aber etwas größer als die Minimalversion.

## Ziel

Prüfen, ob folgende Teile sauber funktionieren, ohne schon die volle Bridge zu starten:

- Basis-`run()`
- `logging_utils`
- `Executor`-Import und Instanziierung
- Datei-Logging vor und nach diesen Schritten

## Verhalten

- kein HTTP-Server
- keine Queue
- keine Custom Events
- keine Timer
- Datei-Log in `fusion_bridge_boot.log`
- zusätzlich JSONL-Logging über `fusion_bridge.log`

## Erwartete Signale

### Popup

```text
FusionBridge Debug-Stufe 2 erfolgreich
```

### Dateien

- `fusion_bridge_boot.log`
- `fusion_bridge.log`

## Aussagekraft

Wenn Debug-Stufe 2 funktioniert, liegt der ursprüngliche Crash sehr wahrscheinlich erst in:

- Server-Start
- Queue-Aufbau
- Runtime-Pump / Custom Events / Timer
