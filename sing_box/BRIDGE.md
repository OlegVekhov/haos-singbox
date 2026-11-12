# Keenetic Hev UDP-in-TCP bridge

The bridge is available as an **opt-in feature** in add-on version **1.14.4-8**. It was tested by the maintainer with WireGuard connecting successfully; this is not a long-duration reliability guarantee.

KeeneticOS 5 built-in SOCKS5 client may send command 0x05, proprietary Hev UDP-in-TCP. Standard sing-box SOCKS5 inbound rejects this command. See https://github.com/heiher/hev-socks5-core#udp-in-tcp .

This experimental bridge listens on port 1080 (TCP) and relays:
- SOCKS5 CONNECT to the existing sing-box SOCKS5 inbound, moved **at runtime only** to loopback port 1081.
- Hev command 0x05 frames to a sing-box SOCKS5 UDP ASSOCIATE. It frames the UDP replies back into Hev UDP-in-TCP.

No TUN, TPROXY, NET_ADMIN, extra UDP host-port mapping, or manual per-WireGuard-server routes.

## Build/test

From `sing_box/bridge`: `go test -race -v`. Dockerfile contains a multistage Go builder. The add-on is not built or verified on HAOS yet.

## Enabling

Add-on option: `hev_udp_bridge: true`. Other add-on setting `sing_box_config` remains a JSON string, unchanged. The inbound on 1080 must be a single `socks` or `mixed` inbound with exactly one user/password. Other sing-box inbounds are untouched. sing-box runtime config is written to `/data/bridge-config.json` and original `/data/config.json` remains unchanged.

Back up your current add-on configuration, enable `hev_udp_bridge: true`, restart, check the logs, and test WireGuard through Keenetic. Results depend on the upstream sing-box route's UDP support.

## Known limitations

- Unsupported SOCKS5 commands beyond CONNECT and Hev 0x05 are rejected.
- Password auth with a single user is required in bridge mode.
- Does not implement UDP fragmentation or ordinary UDP ASSOCIATE on the bridge frontend.
- Relies on sing-box returning a UDP relay address reachable within the same container.
- No long-duration robustness/throughput certification; maintainer confirmed WireGuard connection on the experimental build.
- Bridge test implementation is experimental and should not be exposed to untrusted networks.
