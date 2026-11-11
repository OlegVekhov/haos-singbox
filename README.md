# sing-box Proxy & GUI for Home Assistant OS

Experimental Home Assistant add-on running sing-box with a SOCKS5 listener and an embedded Ingress configuration editor.

## Install

1. Home Assistant → **Settings → Add-ons → Add-on Store → ⋮ → Repositories**.
2. Add `https://github.com/OlegVekhov/haos-singbox`.
3. Install **sing-box Proxy & GUI**.
4. Start the add-on and click **Open Web UI**.

## Features

- SOCKS5 server on TCP port 1080 for Keenetic or other trusted LAN devices (optional UDP exposure).
- Native Home Assistant Ingress GUI for SOCKS5 credentials, VLESS + REALITY, Hysteria2, and default outbound.
- Advanced JSON editor with validation via `sing-box check` before saving.
- Restart of sing-box when configuration changes, plus a backup of the previous configuration.
- No TUN or host networking necessary.

## Important limitations

- Initial routing is **direct only**. Configure your remote outbound and RU/World rules through advanced JSON before using foreign routing.
- SOCKS5 is not a full-device IP tunnel. DNS, UDP and IPv6 behavior depends on the client (including Keenetic).
- Do not expose TCP/1080 to the public Internet. Restrict it to trusted LAN subnets.
- The add-on is **experimental and has not yet been verified on a real HAOS installation**. Open an issue with the Supervisor build log if installation fails.
- sing-box is pinned to version 1.14.4 for this version of the add-on; new sing-box releases will require a package update.

## Source

- `repository.yaml`: Home Assistant add-on repository metadata.
- `sing_box/config.yaml`: add-on manifest.
- `sing_box/Dockerfile`: container build.
- `sing_box/app.py`: manager process, configuration validation, Ingress API.
- `sing_box/ui.html`: GUI.
- `sing_box/DOCS.md`: add-on help.

Contributions and issue reports welcome.
