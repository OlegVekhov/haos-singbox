# sing-box for Home Assistant OS

[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-Add--on-41BDF5?logo=homeassistant&logoColor=white)](https://www.home-assistant.io/)
[![sing-box](https://img.shields.io/badge/sing--box-1.14.4-blue)](https://sing-box.sagernet.org/)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/OlegVekhov/haos-singbox)

A lightweight, configurable **sing-box proxy add-on** for Home Assistant OS / Supervisor. It runs the official sing-box binary in a dedicated container, with the full sing-box JSON configuration supplied through the native add-on **Configuration** tab.

**Add-on version:** `1.14.4-7` · **sing-box version:** `1.14.4` · **Status:** tested by the maintainer on HAOS; not a Home Assistant official add-on.

## Features

- Use the native Supervisor Configuration editor: one multiline **`sing_box_config`** text field containing a complete sing-box JSON document.
- Run arbitrary supported sing-box inbound/outbound/route/DNS configurations; SOCKS5 and VLESS/REALITY are examples, not hard-coded modes.
- Validate with `sing-box check` before starting. Invalid configuration prevents startup rather than silently replacing the last working file.
- Keep the last successfully validated JSON in `/data/config.json`. The add-on can reuse it if the `sing_box_config` option is missing.
- Default SOCKS5 listener: internal TCP port `1080`; optional UDP mapping.
- Debian-based multi-architecture container: `amd64`, `aarch64`, `armv7`.
- No Ingress web interface, privileged container, or host networking.

## Install

1. Open **Home Assistant → Settings → Add-ons → Add-on Store**.
2. Open the menu **⋮ → Repositories** and add:
   `https://github.com/OlegVekhov/haos-singbox`
3. Find **sing-box**, install it, and open its **Configuration** tab.
4. Replace the demonstration JSON in **`sing_box_config`** with your own valid sing-box JSON. Change the example password before first use.
5. Under **Network**, configure the host port published for internal `1080/tcp`, and optionally `1080/udp`.
6. Save, start the add-on, and check **Log** for configuration validation and startup.

> **Important:** Keep the **`sing_box_config`** option name. Paste the entire sing-box JSON **as the value of this field**. Do **not** replace the entire add-on options object with sing-box keys or remove the wrapper.

Example add-on options:

```yaml
sing_box_config: |
  {
    "log": {"level": "info"},
    "inbounds": [{
      "type": "socks",
      "tag": "socks-in",
      "listen": "0.0.0.0",
      "listen_port": 1080,
      "users": [{"username": "proxy-user", "password": "CHANGE_THIS_PASSWORD"}]
    }],
    "outbounds": [{"type": "direct", "tag": "direct"}],
    "route": {"final": "direct"}
  }
```

This is a **minimal demonstration**, not a production-ready public proxy. You can supply your existing VLESS/REALITY, DNS, and routing JSON through the same field.

## Ports and network boundaries

The manifest currently publishes **internal `1080/tcp`** and optionally **`1080/udp`**. Publishing an external host port is separate from the `listen_port` defined in your sing-box JSON. Additional inbound ports (such as a VLESS listener on `8443`) are **not automatically exposed** by this manifest; they require explicit network/publishing configuration and possibly a manifest update.

**Routing note:** sing-box `direct` means the add-on container/HAOS network, not the phone's mobile network. Reaching a private LAN address requires routes, firewall rules and a working return path from the HAOS host/network.

## Documentation

- [Detailed configuration & troubleshooting](sing_box/DOCS.md)
- [Changelog](sing_box/CHANGELOG.md)
- [Issue tracker](https://github.com/OlegVekhov/haos-singbox/issues)
- [Official sing-box documentation](https://sing-box.sagernet.org/)

## Security

Do not commit your actual `sing_box_config`, credentials, UUIDs, REALITY private keys, or logs containing secrets. The default SOCKS password must be changed. Avoid exposing SOCKS5 directly to the Internet. Protect your HAOS access and ensure only intended inbound ports are published.

## Updates and compatibility

The add-on release number and upstream sing-box version are separate: `1.14.4-7` means add-on packaging revision `7` for sing-box `1.14.4`. Back up your working configuration before an update. This repository uses source builds at installation time; the version in `sing_box/config.yaml` controls what Supervisor offers as an update.

**Not affiliated with or endorsed by the Home Assistant project or the sing-box maintainers.**
