# Debug-Startup-Modus

## Aktueller Stand: Nuklearer Minimal-Test

Dieses `FusionBridge.py` ist jetzt auf eine **absolut minimale Form** reduziert.

## Ziel

- Prüfen, ob Fusion den Add-in-Ladepfad überhaupt ausführt
- Ausschluss, dass `adsk`/andere Module-Importe beim Start sofort crashen

## Verhalten

- **`run(context)` schreibt nur in** `fusion_bridge_boot.log`
- **kein** HTTP-Server
- **kein** Popup
- keine weiteren Module-Importe

## Erwartete Signale

Nach `Run` sollte `fusion_bridge_boot.log` im Add-in-Ordner mindestens enthalten:

```text
run() entered
context type: ...
```

Wenn das nicht passiert, ist das Add-in vermutlich noch nicht korrekt geladen (Struktur/Manifest/Pfad).
