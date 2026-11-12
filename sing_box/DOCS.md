# sing-box for Home Assistant OS

## Native expanded configuration editor

The entire **sing-box configuration** is now the root of the Home Assistant add-on's **Configuration** tab. Click the three-dot menu and select **Edit in YAML** if necessary. No `sing_box_config` wrapper and no Ingress are needed for new configurations.

Example, in the add-on's YAML editor:

```yaml
log:
  level: info
inbounds:
  - type: socks
    tag: keenetic-socks
    listen: "0.0.0.0"
    listen_port: 1080
    users:
      - username: keenetic
        password: CHANGE_THIS_PASSWORD
outbounds:
  - type: direct
    tag: direct
route:
  final: direct
```

Valid JSON is also valid YAML; you can paste the complete existing sing-box JSON *without* the `sing_box_config` key. HAOS stores the data as an object, and the runner writes normal `config.json` for sing-box.

**Migration:** older `sing_box_config: >-` with JSON string or a nested YAML mapping will still be accepted by the runner. Back up your currently working configuration before switching from nested settings to root keys. Do not replace an existing VLESS/REALITY configuration with the demonstration above.

The internal SOCKS port is 1080/tcp. Change the externally published host port under the add-on's **Network** settings. Keep `listen_port: 1080` unchanged in sing-box unless the add-on manifest is updated too.

Always change the sample password. Never forward the SOCKS5 port to the public Internet.

**Experimental:** configuration migration and restart require a live HAOS test.
