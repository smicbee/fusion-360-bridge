# Architektur

## Überblick

Die Bridge besteht aus drei Hauptteilen:

1. **Fusion Add-in**
   - läuft in Autodesk Fusion 360
   - stellt Fusion-API-Kontext bereit
   - arbeitet Requests aus einer Queue ab

2. **HTTP-Listener**
   - nimmt lokale Netzwerk-Requests an
   - Endpunkte: `/ping`, `/state`, `/exec`
   - legt Jobs in die Ausführungs-Queue

3. **Executor**
   - führt Python-Code im Fusion-Kontext aus
   - fängt `stdout`, Exceptions und optionale `result`-Objekte ab

## Ablauf

1. Client sendet `POST /exec`
2. Listener erzeugt einen Job und legt ihn in die Queue
3. Add-in verarbeitet Jobs seriell
4. Code wird via `exec(...)` im vorbereiteten Kontext ausgeführt
5. Ergebnis wird dem wartenden HTTP-Request zurückgegeben

## Exec-Kontext

Dem auszuführenden Code werden typischerweise diese Objekte bereitgestellt:

- `adsk`
- `app`
- `ui`
- `product`
- `design`
- `rootComp`
- `result` (optional vom Skript zu setzen)

## Wichtige Designentscheidung

Kein restriktives DSL-Protokoll im MVP. Stattdessen offener Python-Exec-Modus, damit beliebige Fusion-API-Aktionen möglich sind.

## Bekannte Risiken

- Keine Authentifizierung
- Beliebiger Python-Code kann im Fusion-Kontext laufen
- Fehlerhafte Skripte können aktive Designs verändern
- Threading in Fusion muss vorsichtig behandelt werden
