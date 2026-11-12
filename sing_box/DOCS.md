# sing-box for Home Assistant OS

The whole sing-box configuration is edited through Home Assistant's native expanded YAML/JSON add-on Configuration editor. No Ingress or additional web UI is required.

## Editing a configuration

1. Open the add-on's **Configuration** tab.
2. Edit `sing_box_config` as a YAML mapping. YAML maps/lists are converted internally to sing-box JSON.
3. Save and restart the add-on. The start script validates the generated JSON with `sing-box check` before launching.
4. In the **Network** section set the external host port for internal `1080/tcp`. Your SOCKS5 inbound must still listen on `0.0.0.0:1080`.

**Important for upgrades:** if the earlier version stored `sing_box_config` as a JSON *string*, it is still supported. Do not delete your existing configuration. You can optionally convert that string into a YAML mapping when convenient. Back up the current configuration before editing.

Example:

```yaml
sing_box_config:
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

The complete `sing_box_config` structure is passed to sing-box, so VLESS REALITY, Hysteria2, rule sets and DNS can be configured without the add-on defining individual fields.

SOCKS5 port 1080 must not be forwarded publicly. Choose a strong password and limit access to trusted LAN clients.

Status: experimental. The add-on has not been independently tested across all HAOS architectures.
