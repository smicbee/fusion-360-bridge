# Fusion 360 Bridge

Offene Bridge für Autodesk Fusion 360, damit ein externes System Python-Code im Fusion-Kontext ausführen kann.

## Ziel

Das Projekt stellt eine lokale Exec-Bridge bereit:

- Fusion-360-Add-in läuft direkt in Fusion
- lokaler HTTP-Server nimmt Requests entgegen
- Python-Code wird im Fusion-Kontext ausgeführt
- Antworten liefern `ok`, `stdout`, `result`, Laufzeit und Fehlerdetails zurück

## MVP-Umfang

- `GET /ping`
- `GET /state`
- `GET /logs`
- `POST /exec`
- serielle Job-Queue
- Timeout pro Request
- einfacher Datei-Logger
- offener Python-Exec-Modus ohne Auth
- Runtime Pump mit bevorzugtem Custom-Event-Modus und Timer-Fallback
- Beispielskripte für einfache Modell-Erzeugung

## Projektstruktur

```text
fusion-360-bridge/
├─ docs/
├─ examples/
├─ bridge-client/
└─ fusion-addin/
   └─ FusionBridge/
```

## Sicherheitsmodell

Bewusst offen für lokales/vertrautes Netzwerk. Keine Authentifizierung im MVP.

## Nächste Schritte

1. Add-in in Fusion 360 installieren
2. Bridge starten und `/ping` + `/state` prüfen
3. Sicherstellen, dass `pumpMode` sinnvoll gesetzt ist
4. Beispielskripte via `/exec` ausführen
5. Logs und Laufzeitverhalten im echten Fusion-Setup validieren
6. Danach freie Modellierungs-Workflows aufbauen
