# Changelog

All notable changes to the Home Assistant sing-box add-on are documented here. The add-on version is distinct from the bundled upstream sing-box version.

## [Unreleased]

_No changes yet._

## [1.14.4-9] - 2026-11-12

### Added
- Read-only Home Assistant Supervisor SSL directory mount (`map: [{type: ssl, read_only: true}]`).
- Certificate-chain and private-key file references are now possible via `/ssl/...` in sing-box TLS configuration.

### Compatibility
- No changes to the runner, Dockerfile, `sing_box_config` schema, bridge implementation, or network port mappings.
- Existing embedded TLS certificates continue to work. SSL files are optional; the add-on does not manage renewals.


## [1.14.4-8] - 2026-11-12

### Added
- Optional KeeneticOS 5 Hev UDP-in-TCP (`0x05`) bridge, allowing UDP applications such as WireGuard to traverse the SOCKS5 proxy.
- Go bridge binary with TCP CONNECT forwarding, upstream SOCKS5 UDP association and bidirectional datagram encapsulation.
- `hev_udp_bridge: bool` Supervisor setting (disabled by default).
- Optional `8443/tcp` port declaration for independently configured VLESS inbounds.
- Bridge-specific documentation and Go tests.

### Compatibility
- Kept the production add-on slug `sing_box` and preserved `sing_box_config` as multiline JSON string.
- Standard mode remains the default, with the bridge opt-in. The original JSON config is not modified when bridge mode starts.
- WireGuard connection was confirmed by the maintainer using the experimental build; full platform-specific build and stability checks are still recommended.



### Documentation
- Reconcile the README and detailed setup instructions with the shipped, working `sing_box_config` **multiline JSON string** schema.
- Document network port publishing, private-network routing, diagnostics and safe handling of credentials.
- Add an explicit changelog and repository maintenance guidance.

_No runtime code, add-on manifest or version change in this documentation update._

## [1.14.4-7] - 2026-11-12

### Fixed
- Restored the Supervisor `schema: sing_box_config: str` field after the unsuccessful root-level YAML settings experiment.
- Restored reliable multiline JSON option parsing.
- Preserve the last validated `/data/config.json` and avoid replacing it on a failed validation.
- Fall back to saved validated JSON if the configuration option is missing.

### Notes
- The maintainer subsequently confirmed the add-on works on HAOS.
- The root-level sing-box YAML example in older documentation was incorrect for this release.

## [1.14.4-3 to 1.14.4-6] - 2026-11-11 / 2026-11-12

### Changed
- Iterated on native Supervisor configuration handling and error reporting.
- Removed the experimental Ingress GUI and used the Supervisor Configuration tab.
- Added the add-on icon.
- Fixed binary startup/packaging issues by switching to a Debian-based image with upstream sing-box binaries.

These entries summarize the repository's development history. Intermediate packaging revisions were experimental.

## Initial development - 2026-11-11

- Created the Home Assistant add-on repository and manifest.
- Added a sing-box launcher, upstream binary installation and basic SOCKS5 example.

[Unreleased]: https://github.com/OlegVekhov/haos-singbox/commits/main/
[1.14.4-7]: https://github.com/OlegVekhov/haos-singbox/commit/2b28321e768410db7ab838e0ae685c37a720fffc
