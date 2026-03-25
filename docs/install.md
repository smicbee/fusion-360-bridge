# Installation (aktueller Debug-Stand)

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

## 3. Erwartung im aktuellen Debug-Stand

- Popup: `FusionBridge Debug-Start erfolgreich`
- Datei im Add-in-Ordner: `fusion_bridge_boot.log`

## 4. Wenn es nicht klappt

- prüfen, ob `fusion_bridge_boot.log` entstanden ist
- dessen Inhalt auslesen
- falls keine Datei entsteht, crasht Fusion sehr früh beim Laden des Add-ins

## Hinweis

Die volle Bridge-Logik ist vorübergehend aus `FusionBridge.py` herausgenommen, damit der Start isoliert getestet werden kann. Nach erfolgreichem Grundstart wird sie schrittweise wieder aktiviert.
