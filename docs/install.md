# Installation and deployment

## 1) Install the Fusion add-in

Copy the folder `fusion-addin/FusionBridge` into your Fusion add-ins directory:

### Windows

```text
%appdata%\\Autodesk\\Autodesk Fusion\\API\\AddIns\\
```

### macOS

```text
~/Library/Application Support/Autodesk/Autodesk Fusion/API/AddIns/
```

In Fusion, open **Scripts and Add-Ins**, select `FusionBridge`, and click **Run**.

## 2) Network reachability check (required)

The add-in binds to `0.0.0.0:8765` by default.
OpenClaw must be able to reach this machine on port **8765**.

- On same machine: `http://127.0.0.1:8765`
- On LAN: `http://<fusion-host-ip>:8765`

If remote checks fail:
- check Windows/macOS firewall rules
- check that Fusion is still running
- check that the add-in is loaded and `fusion_bridge_boot.log` exists

## 3) Install and configure the OpenClaw plugin

```bash
cd /home/smicbee/.openclaw/workspace
openclaw plugins install --link /home/smicbee/Ideenschmiede/projektFiles/fusion-360-bridge/openclaw-plugin
```

Then in OpenClaw config:

```yaml
plugins:
  entries:
    fusion-360-bridge:
      enabled: true
      config:
        # Example if Fusion runs on another machine in the LAN
        baseUrl: http://192.168.2.113:8765
        timeoutMs: 10000
```

## 4) Configure a different port (optional)

If you need a different port than `8765`, edit `_BIND_PORT` in `fusion-addin/FusionBridge/FusionBridge.py`, restart Fusion, and update the OpenClaw plugin config `baseUrl` to the same port.
