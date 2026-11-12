# Changelog

All notable changes to the Home Assistant sing-box add-on are documented here. The add-on version is distinct from the bundled upstream sing-box version.

## [Unreleased]

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

[Unreleased]: https://github.com/OlegVekhov/haos-singbox/compare/main...main
[1.14.4-7]: https://github.com/OlegVekhov/haos-singbox/commits/main/
