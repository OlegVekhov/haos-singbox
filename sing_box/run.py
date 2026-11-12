"""sing-box HAOS runner: validated JSON options with existing-config protection."""
import json
import os
import subprocess
import sys
from pathlib import Path

OPTIONS = Path("/data/options.json")
CONFIG = Path("/data/config.json")
BINARY = "/usr/local/bin/sing-box"


def load():
    opts = json.loads(OPTIONS.read_text(encoding="utf-8"))
    raw = opts.get("sing_box_config") if isinstance(opts, dict) else None
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw.strip():
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in sing_box_config: {exc}") from exc
        return parsed
    if CONFIG.is_file():
        print("[sing-box] WARNING: sing_box_config missing; reusing saved /data/config.json", flush=True)
        return json.loads(CONFIG.read_text(encoding="utf-8"))
    raise ValueError("Missing sing_box_config: paste complete JSON into the Configuration tab")


def main():
    cfg = load()
    if not isinstance(cfg, dict) or not isinstance(cfg.get("inbounds"), list) or not isinstance(cfg.get("outbounds"), list):
        raise ValueError("Configuration must contain JSON object with inbounds and outbounds")
    tmp = CONFIG.with_suffix(".json.tmp")
    with tmp.open("w", encoding="utf-8") as fp:
        json.dump(cfg, fp, ensure_ascii=False, indent=2)
        fp.write("\n")
    os.chmod(tmp, 0o600)
    print("[sing-box] Checking configuration...", flush=True)
    try:
        subprocess.run([BINARY, "check", "-c", str(tmp)], check=True)
    except Exception:
        tmp.unlink(missing_ok=True)
        raise
    os.replace(tmp, CONFIG)
    print("[sing-box] Starting...", flush=True)
    os.execv(BINARY, [BINARY, "run", "-D", "/data", "-c", str(CONFIG)])


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[sing-box] Startup error: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
