# Fusion 360 Bridge

Offene Bridge für Autodesk Fusion 360, damit ein externes System Python-Code im Fusion-Kontext ausführen kann.

## Aktueller Status

Das Projekt läuft aktuell im **Debug-Startup-Modus, Stufe 2**. Die volle Bridge-Struktur bleibt im Repo, aber `FusionBridge.py` aktiviert im Moment nur den Add-in-Grundstart plus Logging- und Executor-Checks.

## Ziel

Das Projekt stellt langfristig eine lokale Exec-Bridge bereit:

- Fusion-360-Add-in läuft direkt in Fusion
- lokaler HTTP-Server nimmt Requests entgegen
- Python-Code wird im Fusion-Kontext ausgeführt
- Antworten liefern `ok`, `stdout`, `result`, Laufzeit und Fehlerdetails zurück

## Nächster praktischer Schritt

1. Debug-Stufe 2 in Fusion starten
2. prüfen, ob Popup erscheint
3. prüfen, ob `fusion_bridge_boot.log` und `fusion_bridge.log` entstehen
4. danach Server und Runtime-Pump schrittweise wieder zuschalten
