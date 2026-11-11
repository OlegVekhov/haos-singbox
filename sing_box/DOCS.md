# sing-box Proxy & GUI

Start the add-on, then click **Open Web UI**. The GUI is protected by Home Assistant Ingress.

The editor supports SOCKS5 credentials, VLESS + REALITY, Hysteria2, route final outbound, and full JSON.

By default the proxy uses direct routing only. Add remote outbounds and route rules through the JSON editor.

Use **Check** before **Save and restart**. sing-box validates configuration before applying changes. A backup of the previous configuration is written.

SOCKS5 is exposed at TCP port 1080. Optional UDP/1080 can be enabled under add-on network settings. Restrict access to trusted LAN clients.

For Keenetic use the HAOS host IP, TCP/1080, username keenetic and the randomly generated password visible in the SOCKS5 tab.

**Experimental:** installation and Docker networking still require testing on an actual HAOS Supervisor.
