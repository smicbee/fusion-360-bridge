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

- Popup: `FusionBridge Debug-Stufe 2 erfolgreich`
- Datei im Add-in-Ordner: `fusion_bridge_boot.log`
- zusätzliche Datei: `fusion_bridge.log`

## 4. Wenn es nicht klappt

- prüfen, ob `fusion_bridge_boot.log` entstanden ist
- prüfen, ob `fusion_bridge.log` entstanden ist
- Inhalte auslesen

## Hinweis

Die volle Bridge-Logik bleibt weiter deaktiviert. In Debug-Stufe 2 testen wir nur, ob Logging und `Executor`-Import/Instanziierung auf deinem Fusion-System sauber funktionieren.
