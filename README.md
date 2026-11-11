# sing-box for Home Assistant OS

Lightweight sing-box add-on with a **full JSON text configuration field** in the native Home Assistant add-on **Configuration** tab. No Ingress, GUI web service, TUN, host networking or privileged container.

## Installation

Add repository `https://github.com/OlegVekhov/haos-singbox` in Home Assistant add-on store, install **sing-box**, open **Configuration**, and edit `sing_box_config` with your sing-box JSON.

The default configuration runs a SOCKS5 listener at `0.0.0.0:1080`. Change `CHANGE_THIS_PASSWORD` before use.

Under the add-on **Network** section select the host TCP port mapped to internal `1080/tcp`. Host and internal ports can differ. UDP mapping is optional, depending on Keenetic SOCKS5 UDP support.

The add-on validates the JSON via `sing-box check` and then starts sing-box directly. It uses a Debian-based image to avoid the glibc dynamic-loader failure observed in the original Alpine build.

**Note:** the add-on currently declares internal port 1080. To use a different internal port you must change the add-on manifest and rebuild. DNS, IPv6 and UDP traffic still require separate consideration.

**Experimental** — full Supervisor installation and networking have not yet been verified. The old Ingress UI has been removed. Previously saved Ingress configuration will not be migrated automatically.

See [configuration notes](sing_box/DOCS.md).
