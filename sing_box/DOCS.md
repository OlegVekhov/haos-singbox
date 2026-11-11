# sing-box HAOS add-on

There is no Ingress panel or separate web UI. Paste the complete sing-box JSON into the **Configuration → sing_box_config** field.

The container listens on `1080/tcp` by default. Under **Network**, choose the external host port. For example, host `11080` can map to container `1080/tcp` while JSON retains `"listen_port": 1080`.

Optional `1080/udp` can be exposed separately. Additional internal ports cannot be published from the add-on UI unless they are declared in its manifest.

Save your configuration, restart the add-on and check the log. The add-on validates it with `sing-box check` before starting. Keep your SOCKS5 password secret and never forward the SOCKS5 port to the public Internet.

**Upgrade:** Previous Ingress editor config is not migrated automatically. Copy the old `config.json` into the new configuration field before updating if needed.

**Status:** experimental, not yet tested in a real HAOS installation.
