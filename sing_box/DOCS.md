# Configuration and troubleshooting

This page documents the **current working add-on** (`1.14.4-7`). The authoritative options schema is [config.yaml](config.yaml).

## Editing the full JSON in Home Assistant

Open the add-on **Configuration** tab. The single field `sing_box_config` accepts the **entire sing-box JSON as text**. In **Edit in YAML**, its value must be a YAML multiline string:

```yaml
sing_box_config: |
  {
    "log": {"level": "info"},
    "inbounds": [
      {
        "type": "socks",
        "tag": "socks-in",
        "listen": "0.0.0.0",
        "listen_port": 1080,
        "users": [
          {"username": "proxy-user", "password": "CHANGE_THIS_PASSWORD"}
        ]
      }
    ],
    "outbounds": [{"type": "direct", "tag": "direct"}],
    "route": {"final": "direct"}
  }
```

- The outer `sing_box_config: |` belongs to **Home Assistant Supervisor**; the JSON inside belongs to **sing-box**.
- **Do not** paste `inbounds:`, `outbounds:`, etc. at the top level of add-on options. That schema was tried in development and **reverted**.
- **Do not** replace a working configuration with the example: the example contains no VLESS or REALITY inbound.
- A JSON object is expected; the runner checks that `inbounds` and `outbounds` are arrays and runs `sing-box check` before replacing the saved `/data/config.json`.
- The option is a string. Legacy object-shaped `sing_box_config` data is accepted by the runner when present, but new edits should use the documented multiline JSON string.

## Changing a configuration

1. Make a backup of your working `sing_box_config` in a **private** location.
2. Edit only the necessary JSON.
3. Save the add-on options and restart the add-on.
4. Open **Log**. Successful startup prints `[sing-box] Checking configuration...` followed by `[sing-box] Starting...`.
5. If checking fails, correct the JSON; the saved validated file is not overwritten by the failed check.

If the `sing_box_config` setting is absent entirely, the runner may reuse the last valid `/data/config.json`, logging an explicit warning. This is a fallback, **not** a replacement for keeping a backup.

## Network and port publishing

| Configuration | Meaning |
| --- | --- |
| `1080/tcp` | Published internal SOCKS5 TCP listener; its external host port is configurable in the add-on Network tab |
| `1080/udp` | Optional internal SOCKS5 UDP port mapping |
| `8443/tcp`, etc. | **Not published** by the current manifest |
| `listen: 0.0.0.0` | Listen on container interfaces, not automatically on the public router's WAN |
| `route: ... direct` | Traffic leaves via the container/HAOS networking context |

If you configure a VLESS inbound on a different internal port, you must arrange the corresponding port publishing and firewall/NAT. Do not assume the add-on's external `1080` port exposes an internal `8443` listener.

For LAN destinations such as `192.168.249.39`, check the HAOS-side route and destination firewall/return route. A `direct` log entry confirms routing selection, **not** successful reachability.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Add-on fails immediately | Look for `[sing-box] Startup error` and the output of `sing-box check`; fix JSON or unsupported options |
| `sing_box_config` missing | Restore the multiline JSON field in the Configuration tab |
| SOCKS5 unreachable | Match container `listen_port: 1080` to manifest's internal `1080/tcp`; check the external host-port setting |
| VLESS client times out before handshake | Verify the client's public IP/port, router forwarding and published container listener; this can also be packet loss or ISP filtering |
| Client can reach HAOS but not LAN hosts | Verify routing and reverse-path/firewall permissions from the HAOS network |
| `mux connection closed: EOF` | Peer closed a multiplexed stream; this message alone is not enough to identify its cause |
| `dial tcp ... i/o timeout` | TCP establishment to that endpoint failed; diagnose connectivity before changing DNS or geographic routing |
| DNS queries work but web pages stall | Inspect TCP/UDP separately; DNS success does not prove application traffic succeeds |

For diagnosis, collect **both** the client sing-box log and the add-on log around the same incident, noting which VPN processes were restarted.

## Security and privacy

- Change `CHANGE_THIS_PASSWORD` immediately.
- Do not commit production JSON with REALITY private keys, user UUIDs, passwords, or private endpoints.
- Do not expose the example SOCKS listener directly on WAN.
- Firewall public VLESS/REALITY endpoints; use only intended exposed ports.
- Treat copied logs as sensitive: they may include IP addresses and hostnames.

## Scope

This is a sing-box **add-on**, not a Home Assistant integration or a general-purpose VPN management GUI. No Ingress, TUN, privileged host networking or automatic LAN route management is provided. See the official [sing-box configuration reference](https://sing-box.sagernet.org/configuration/).
