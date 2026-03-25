# HTTP-API

## `GET /ping`

Prüft, ob die Bridge läuft.

### Response

```json
{
  "ok": true,
  "service": "fusion-bridge",
  "version": "0.2.0"
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
  "currentJobId": null
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
  "timeoutSeconds": 120
}
```

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
