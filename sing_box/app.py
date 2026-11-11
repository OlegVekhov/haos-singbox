import json, os, secrets, shutil, subprocess, tempfile, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
ROOT=Path("/config"); CONF=ROOT/"config.json"; BINARY="/usr/local/bin/sing-box"
LOCK=threading.RLock(); state={"proc":None}
def initial():
    p=secrets.token_urlsafe(24)
    return {"log":{"level":"info"},"inbounds":[{"type":"socks","tag":"keenetic-socks","listen":"0.0.0.0","listen_port":1080,"users":[{"username":"keenetic","password":p}]}],"outbounds":[{"type":"direct","tag":"direct"}],"route":{"final":"direct"}}
def check(config):
    if not isinstance(config,dict): raise ValueError("Expected JSON object")
    fd,name=tempfile.mkstemp(dir=ROOT,suffix=".json")
    try:
        with os.fdopen(fd,"w") as f: json.dump(config,f)
        p=subprocess.run([BINARY,"check","-c",name],capture_output=True,text=True,timeout=30)
        if p.returncode: raise ValueError((p.stdout+p.stderr)[-6000:])
    finally: os.unlink(name)
def restart():
    with LOCK:
        old=state["proc"]
        if old and old.poll() is None:
            old.terminate()
            try: old.wait(timeout=8)
            except subprocess.TimeoutExpired: old.kill();old.wait()
        state["proc"]=subprocess.Popen([BINARY,"run","-D",str(ROOT),"-c",str(CONF)])
def save(cfg):
    with LOCK:
        check(cfg)
        fd,name=tempfile.mkstemp(dir=ROOT,prefix=".new-")
        try:
            with os.fdopen(fd,"w") as f:
                json.dump(cfg,f,indent=2);f.write("\n");f.flush();os.fsync(f.fileno())
            os.chmod(name,0o600)
            if CONF.exists(): shutil.copy2(CONF,ROOT/"config.json.bak")
            os.replace(name,CONF)
            restart()
        finally:
            if os.path.exists(name): os.unlink(name)
class Handler(BaseHTTPRequestHandler):
    def reply(self,status,body,kind="application/json"):
        data=body if isinstance(body,bytes) else json.dumps(body).encode()
        self.send_response(status)
        for k,v in {"Content-Type":kind,"Cache-Control":"no-store","X-Content-Type-Options":"nosniff","Content-Security-Policy":"default-src 'self' 'unsafe-inline'; connect-src 'self'","Content-Length":str(len(data))}.items():self.send_header(k,v)
        self.end_headers();self.wfile.write(data)
    def authorized(self):
        return self.client_address[0] in ("172.30.32.2","127.0.0.1","::1")
    def do_GET(self):
        if not self.authorized(): return self.reply(403,{"error":"Ingress only"})
        path=urlparse(self.path).path.rstrip("/")
        if path in ("","/index.html"):return self.reply(200,Path("/opt/ui.html").read_bytes(),"text/html; charset=utf-8")
        if path=="/api/config":return self.reply(200,json.loads(CONF.read_text()))
        if path=="/api/status":
            proc=state["proc"];return self.reply(200,{"running":bool(proc and proc.poll() is None)})
        self.reply(404,{"error":"Not found"})
    def do_POST(self):
        if not self.authorized():return self.reply(403,{"error":"Ingress only"})
        path=urlparse(self.path).path.rstrip("/")
        if path not in ("/api/config","/api/check"):return self.reply(404,{"error":"Not found"})
        try:
            size=int(self.headers.get("Content-Length","0"))
            if size<1 or size>1048576:return self.reply(413,{"error":"Invalid size"})
            cfg=json.loads(self.rfile.read(size))
            if path=="/api/config":save(cfg)
            else:check(cfg)
            self.reply(200,{"ok":True,"message":"Saved and restarted" if path=="/api/config" else "Configuration valid"})
        except (ValueError,subprocess.TimeoutExpired) as e:self.reply(400,{"error":str(e)})
        except Exception as e:self.reply(500,{"error":str(e)})
def main():
    ROOT.mkdir(parents=True,exist_ok=True)
    if not CONF.exists():
        CONF.write_text(json.dumps(initial(),indent=2)+"\n");CONF.chmod(0o600)
    check(json.loads(CONF.read_text()));restart()
    ThreadingHTTPServer(("0.0.0.0",8099),Handler).serve_forever()
if __name__=="__main__": main()
