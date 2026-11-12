import json
import os
import subprocess
import sys
from pathlib import Path

OPTIONS = Path("/data/options.json")
CONFIG = Path("/data/config.json")
BINARY = "/usr/local/bin/sing-box"


def main():
    options = json.loads(OPTIONS.read_text(encoding="utf-8"))
    raw = options.get("sing_box_config")
    # Upgrade-compatible: older installs store a JSON string.
    # New installs use a native mapping for HAOS raw YAML/JSON editor.
    if isinstance(raw, str):
        config = json.loads(raw)
    elif isinstance(raw, dict):
        config = raw
    else:
        raise ValueError("sing_box_config must be a JSON string or YAML object")

    if not isinstance(config, dict):
        raise ValueError("sing_box_config must contain a configuration object")

    temp = Path("/data/config.json.tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")
    temp.chmod(0o600)
    os.replace(temp, CONFIG)

    print("[sing-box] Checking configuration...", flush=True)
    result = subprocess.run([BINARY, "check", "-c", str(CONFIG)])
    if result.returncode:
        sys.exit(result.returncode)
    print("[sing-box] Starting...", flush=True)
    os.execv(BINARY, [BINARY, "run", "-D", "/data", "-c", str(CONFIG)])


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[sing-box] Error: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
