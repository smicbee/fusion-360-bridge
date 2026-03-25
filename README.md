# Fusion 360 Bridge

Offene Bridge für Autodesk Fusion 360, damit ein externes System Python-Code im Fusion-Kontext ausführen kann.

## Aktueller Status

Die Add-in-Datei ist aktuell im **nuklearen Minimal-Testmodus**: `FusionBridge.py` versucht nur noch, beim Laden von `run()` einen kleinen Boot-Log zu schreiben.

Damit isolieren wir, ob Fusion den Add-in-Aufruf selbst überhaupt ausführt.

## Ziel

Langfristig soll die Bridge:

- HTTP-Server (ping/state/logs/exec) bereitstellen
- Fusion-API-Aufrufe im Python-Exec-Modus ausführen

## Nächster Schritt

1. Add-in mit minimaler `FusionBridge.py` starten
2. prüfen, ob `fusion_bridge_boot.log` erzeugt wird
3. falls ja: schrittweise mehr Funktionalität wieder aktivieren
4. falls nein: Manifest/Ordner-Pfad nochmal hart prüfen
