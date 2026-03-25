# HTTP-API

## `GET /ping`

Prüft, ob die Bridge läuft.

### Response

```json
{
  "ok": true,
  "service": "fusion-bridge",
  "version": "0.1.0"
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
  "rootComponentName": "RootComponent"
}
```

## `POST /exec`

Führt Python-Code im Fusion-Kontext aus.

### Request

```json
{
  "code": "print('hello from fusion')"
}
```

### Erfolgs-Response

```json
{
  "ok": true,
  "stdout": "hello from fusion\n",
  "result": null,
  "error": null
}
```

### Fehler-Response

```json
{
  "ok": false,
  "stdout": "",
  "result": null,
  "error": "Traceback ..."
}
```
