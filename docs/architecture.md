# Architektur

## Überblick

Die Bridge besteht aus vier Hauptteilen:

1. **Fusion Add-in**
   - läuft in Autodesk Fusion 360
   - stellt Fusion-API-Kontext bereit
   - arbeitet Requests aus einer Queue ab

2. **HTTP-Listener**
   - nimmt lokale Netzwerk-Requests an
   - Endpunkte: `/ping`, `/state`, `/logs`, `/exec`
   - legt Jobs in die Ausführungs-Queue

3. **Executor**
   - führt Python-Code im Fusion-Kontext aus
   - fängt `stdout`, Exceptions und optionale `result`-Objekte ab

4. **Runtime Pump**
   - stößt die Abarbeitung der Queue regelmäßig im Fusion-Kontext an
   - bevorzugt **Custom Events**
   - hat einen **Timer-Fallback**, falls Custom Events auf dem Zielsystem nicht wie erwartet funktionieren

## Ablauf

1. Client sendet `POST /exec`
2. Listener erzeugt einen Job und legt ihn in die Queue
3. Runtime Pump triggert die Queue-Abarbeitung im Fusion-Kontext
4. Add-in verarbeitet Jobs seriell
5. Code wird via `exec(...)` im vorbereiteten Kontext ausgeführt
6. Ergebnis wird dem wartenden HTTP-Request zurückgegeben

## Exec-Kontext

Dem auszuführenden Code werden typischerweise diese Objekte bereitgestellt:

- `adsk`
- `app`
- `ui`
- `product`
- `design`
- `rootComp`
- `document`
- `result` (optional vom Skript zu setzen)

## Wichtige Designentscheidung

Kein restriktives DSL-Protokoll im MVP. Stattdessen offener Python-Exec-Modus, damit beliebige Fusion-API-Aktionen möglich sind.

## Laufzeitstrategie

Weil die konkrete Event-/Timer-Anbindung in Fusion je nach Umgebung und API-Verhalten empfindlich sein kann, verwendet das Projekt jetzt eine zweistufige Strategie:

- Primär: `CustomEvent`-basierter Pump-Mechanismus
- Fallback: `TimerEvent`-basierter Pump-Mechanismus

Der aktive Modus wird über `/state` als `pumpMode` sichtbar.

## Bekannte Risiken

- Keine Authentifizierung
- Beliebiger Python-Code kann im Fusion-Kontext laufen
- Fehlerhafte Skripte können aktive Designs verändern
- Timeout auf HTTP-Ebene beendet nicht automatisch schon laufenden Fusion-Code
- Reales Verhalten muss weiterhin auf dem echten Fusion-System validiert werden
