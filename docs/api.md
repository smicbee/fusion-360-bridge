# HTTP-API

## Netzwerkbindung

Aktuell bindet die Bridge auf `0.0.0.0:8765`, damit sie im lokalen Netzwerk erreichbar ist.

- lokal: `http://127.0.0.1:8765`
- LAN: `http://<deine-ip>:8765`

Wenn aus dem LAN kein Zugriff klappt, ist meist die Host-Firewall der Grund.

## `GET /ping`

Prüft, ob die Bridge läuft.

### Response

```json
{
  "ok": true,
  "service": "fusion-bridge",
  "version": "0.3.0"
}
```

## `GET /state`

Liefert einfachen Laufzeitstatus.

### Beispiel-Response

```json
{
  "ok": true,
  "fusionRunning": true,
  "documentName": "Unnamed",
  "hasActiveDesign": true,
  "rootComponentName": "RootComponent",
  "queueSize": 0,
  "busy": false,
  "currentJobId": null,
  "pumpMode": "custom-event"
}
```

## `GET /logs`

Liefert die letzten Logzeilen des Add-ins.

### Beispiel-Response

```json
{
  "ok": true,
  "lines": [
    "{\"ts\":\"...\",\"event\":\"addin_started\"}"
  ]
}
```

## `POST /exec`

Führt Python-Code im Fusion-Kontext aus.

### Request

```json
{
  "code": "print('hello from fusion')",
  "timeoutSeconds": 300
}
```

- `timeoutSeconds` ist optional.
- Werte > `300` werden auf `300` begrenzt.
- Es gibt keine feste Obergrenze für die Code-Länge im Body.

### Erfolgs-Response

```json
{
  "ok": true,
  "stdout": "hello from fusion\n",
  "result": null,
  "error": null,
  "durationMs": 3,
  "jobId": "..."
}
```

### Fehler-Response

```json
{
  "ok": false,
  "stdout": "",
  "result": null,
  "error": "Traceback ...",
  "durationMs": 3,
  "jobId": "..."
}
```

### Timeout-Response

```json
{
  "ok": false,
  "error": "execution timeout",
  "jobId": "..."
}
```