# Experimental Keenetic Hev UDP bridge

This is **not a stable release**. Main branch stays at sing-box 1.14.4-7.

KeeneticOS 5 built-in SOCKS5 client may send command 0x05, proprietary Hev UDP-in-TCP. Standard sing-box SOCKS5 inbound rejects this command. See https://github.com/heiher/hev-socks5-core#udp-in-tcp .

This experimental bridge listens on port 1080 (TCP) and relays:
- SOCKS5 CONNECT to the existing sing-box SOCKS5 inbound, moved **at runtime only** to loopback port 1081.
- Hev command 0x05 frames to a sing-box SOCKS5 UDP ASSOCIATE. It frames the UDP replies back into Hev UDP-in-TCP.

No TUN, TPROXY, NET_ADMIN, extra UDP host-port mapping, or manual per-WireGuard-server routes.

## Build/test

From `sing_box/bridge`: `go test -race -v`. Dockerfile contains a multistage Go builder. The add-on is not built or verified on HAOS yet.

## Enabling

Experimental add-on option: `hev_udp_bridge: true`. Other add-on setting `sing_box_config` remains a JSON string, unchanged. The inbound on 1080 must be a single `socks` or `mixed` inbound with exactly one user/password. Other sing-box inbounds are untouched. sing-box runtime config is written to `/data/bridge-config.json` and original `/data/config.json` remains unchanged.

Run alongside a **separately installed experimental copy**, not as an update over the only functioning add-on. Check the logs; then test WireGuard to 5.253.63.222. Results depend on the target VLESS server's UDP relay support and Keenetic's actual Hev implementation.

## Known limitations

- Unsupported SOCKS5 commands beyond CONNECT and Hev 0x05 are rejected.
- Password auth with a single user is required in bridge mode.
- Does not implement UDP fragmentation or ordinary UDP ASSOCIATE on the bridge frontend.
- Relies on sing-box returning a UDP relay address reachable within the same container.
- No production robustness/throughput tests yet. WireGuard on Keenetic has not been tested.
- Bridge test implementation is experimental and should not be exposed to untrusted networks.
