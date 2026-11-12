"""HAOS sing-box runner: raw options as configuration, with legacy migrations."""
import json
import os
import subprocess
import sys
from pathlib import Path

OPTIONS = Path("/data/options.json")
CONFIG = Path("/data/config.json")
BINARY = "/usr/local/bin/sing-box"


def decode(value):
    # HAOS prior releases used a JSON string nested under sing_box_config.
    # Handle both a native mapping and strings; accept top-level raw JSON too.
    for _ in range(4):
        if isinstance(value, str):
            value = json.loads(value)
        elif isinstance(value, dict) and "sing_box_config" in value:
            value = value["sing_box_config"]
        else:
            break
    if not isinstance(value, dict):
        raise ValueError("Home Assistant options must contain a sing-box JSON object")
    if not isinstance(value.get("inbounds"), list) or not isinstance(value.get("outbounds"), list):
        raise ValueError(
            "Missing inbounds/outbounds. Paste the complete sing-box config "
            "into the add-on YAML editor (or keep sing_box_config for migration)."
        )
    return value


def main():
    config = decode(json.loads(OPTIONS.read_text(encoding="utf-8")))
    tmp = CONFIG.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
        f.write("\n")
    tmp.chmod(0o600)
    os.replace(tmp, CONFIG)
    print("[sing-box] Checking configuration...", flush=True)
    subprocess.run([BINARY, "check", "-c", str(CONFIG)], check=True)
    print("[sing-box] Starting...", flush=True)
    os.execv(BINARY, [BINARY, "run", "-D", "/data", "-c", str(CONFIG)])


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[sing-box] Startup error: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
