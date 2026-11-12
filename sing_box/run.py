"""Start sing-box; optionally add an experimental Hev UDP-in-TCP bridge."""
import copy
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

OPTIONS = Path("/data/options.json")
CONFIG = Path("/data/config.json")
BRIDGE_CONFIG = Path("/data/bridge-config.json")
BINARY = "/usr/local/bin/sing-box"
BRIDGE = "/usr/local/bin/hevbridge"


def load(options):
    raw = options.get("sing_box_config") if isinstance(options, dict) else None
    if isinstance(raw, dict):
        cfg = raw
    elif isinstance(raw, str) and raw.strip():
        cfg = json.loads(raw)
    elif CONFIG.is_file():
        print("[sing-box] Warning: options missing; reusing saved config.json", flush=True)
        cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    else:
        raise ValueError("Missing sing_box_config")
    if not isinstance(cfg, dict) or not isinstance(cfg.get("inbounds"), list) or not isinstance(cfg.get("outbounds"), list):
        raise ValueError("Configuration must contain inbounds and outbounds arrays")
    return cfg


def validated_save(config, dest):
    tmp = dest.with_suffix(".json.tmp")
    try:
        with tmp.open("w", encoding="utf-8") as fh:
            json.dump(config, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        tmp.chmod(0o600)
        print(f"[sing-box] Checking {dest.name}...", flush=True)
        subprocess.run([BINARY, "check", "-c", str(tmp)], check=True)
        os.replace(tmp, dest)
    finally:
        tmp.unlink(missing_ok=True)


def bridge_config(original):
    cfg = copy.deepcopy(original)
    inbounds = cfg["inbounds"]
    eligible = [
        inbound for inbound in inbounds
        if inbound.get("listen_port") == 1080 and inbound.get("type") in ("socks", "mixed")
    ]
    if len(eligible) != 1:
        raise ValueError("Bridge requires exactly one socks/mixed inbound listening on port 1080")
    inbound = eligible[0]
    users = inbound.get("users", [])
    if len(users) != 1:
        raise ValueError("Bridge currently requires exactly one SOCKS5 username/password")
    username = users[0].get("username", "")
    password = users[0].get("password", "")
    if not username or not password:
        raise ValueError("Bridge requires nonempty SOCKS5 username/password")
    # Only this inbound moves: all routing/DNS/outbounds remain unchanged.
    inbound["listen"] = "127.0.0.1"
    inbound["listen_port"] = 1081
    return cfg, username, password


def run_bridge(config, username, password):
    # Password is passed via the child process environment, not argv.
    env = dict(os.environ)
    env["HEVBRIDGE_USERNAME"] = username
    env["HEVBRIDGE_PASSWORD"] = password
    sing = subprocess.Popen([BINARY, "run", "-D", "/data", "-c", str(BRIDGE_CONFIG)])
    bridge = None
    try:
        for _ in range(60):
            if sing.poll() is not None:
                raise RuntimeError(f"sing-box exited early: {sing.returncode}")
            try:
                with socket.create_connection(("127.0.0.1", 1081), timeout=0.25):
                    break
            except OSError:
                time.sleep(0.2)
        else:
            raise RuntimeError("sing-box did not open 127.0.0.1:1081")
        bridge = subprocess.Popen([BRIDGE, "-listen", "0.0.0.0:1080", "-upstream", "127.0.0.1:1081"], env=env)
        print("[hevbridge] Both processes started; waiting for exit", flush=True)
        while True:
            if sing.poll() is not None:
                raise RuntimeError(f"sing-box exited: {sing.returncode}")
            if bridge.poll() is not None:
                raise RuntimeError(f"hevbridge exited: {bridge.returncode}")
            time.sleep(0.5)
    finally:
        if bridge and bridge.poll() is None:
            bridge.terminate()
            try:
                bridge.wait(timeout=5)
            except subprocess.TimeoutExpired:
                bridge.kill()
        if sing.poll() is None:
            sing.terminate()
            try:
                sing.wait(timeout=5)
            except subprocess.TimeoutExpired:
                sing.kill()


def main():
    options = json.loads(OPTIONS.read_text(encoding="utf-8"))
    config = load(options)
    enabled = options.get("hev_udp_bridge", False) is True
    if enabled:
        modified, username, password = bridge_config(config)
        validated_save(modified, BRIDGE_CONFIG)
        print("[hevbridge] Experimental UDP-in-TCP mode ON", flush=True)
        run_bridge(modified, username, password)
    else:
        validated_save(config, CONFIG)
        print("[sing-box] Standard mode ON", flush=True)
        os.execv(BINARY, [BINARY, "run", "-D", "/data", "-c", str(CONFIG)])


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[sing-box] Startup error: {exc}", file=sys.stderr, flush=True)
        sys.exit(1)
