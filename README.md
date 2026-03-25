# Fusion 360 Bridge

Offene Bridge für Autodesk Fusion 360, damit ein externes System Python-Code im Fusion-Kontext ausführen kann.

## Aktueller Status

Das Projekt enthält aktuell zusätzlich einen **Debug-Startup-Modus**, um Add-in-Startprobleme in Fusion sauber zu isolieren. Die volle Bridge-Struktur bleibt im Repo, aber `FusionBridge.py` ist momentan absichtlich minimal gehalten, bis der Grundstart auf dem Zielsystem bestätigt ist.

## Ziel

Das Projekt stellt langfristig eine lokale Exec-Bridge bereit:

- Fusion-360-Add-in läuft direkt in Fusion
- lokaler HTTP-Server nimmt Requests entgegen
- Python-Code wird im Fusion-Kontext ausgeführt
- Antworten liefern `ok`, `stdout`, `result`, Laufzeit und Fehlerdetails zurück

## Nächster praktischer Schritt

1. Debug-Add-in in Fusion starten
2. prüfen, ob das Popup erscheint
3. prüfen, ob `fusion_bridge_boot.log` erzeugt wird
4. danach die volle Bridge schrittweise wieder aktivieren
