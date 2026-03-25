# Debug-Startup-Modus

Diese Version von `FusionBridge.py` ist absichtlich minimal.

## Ziel

Prüfen, ob das Add-in grundsätzlich geladen und `run()` überhaupt ausgeführt wird.

## Verhalten

- keine Bridge
- kein HTTP-Server
- keine Queue
- keine Custom Events
- keine Timer
- nur sehr früher Datei-Log + Popup

## Erwartete Datei

Im Add-in-Ordner sollte nach dem Start entstehen:

```text
fusion_bridge_boot.log
```

## Erwartetes Popup

```text
FusionBridge Debug-Start erfolgreich
```

## Wenn es weiterhin direkt verschwindet

Dann ist der Fehler noch vor oder während `run()` selbst zu suchen, z. B.:

- Add-in-Strukturproblem
- Manifest-/Fusion-Ladeproblem
- Python-Umgebung / Modulpfad
- Fusion-spezifisches Problem beim Start
