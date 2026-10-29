"""Lokaler Live-Viewer-Server fuer das Kuppel-Modell.
Aufruf: python viewer/serve.py [port]   (Standard 4410), dann im Browser http://localhost:4410/
Beobachtet designs/dome.sc; nach jeder Speicherung (Aenderungszeit stabil) wird neu exportiert (viewer/export_model.py),
die Seite fragt /api/state ab und laedt das Modell neu, ohne die Kamera zu verlieren."""
import http.server, json, os, socketserver, subprocess, sys, threading, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
DESIGN = os.path.join(ROOT, 'designs', 'dome.sc')
EXPORT = os.path.join(HERE, 'export_model.py')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4410
state = {'version': 0, 'built': '', 'busy': False, 'error': '', 'design_saved': ''}

def do_export():
    state['busy'] = True
    r = subprocess.run([sys.executable, '-I', EXPORT], capture_output=True, text=True)
    state['error'] = '' if r.returncode == 0 else (r.stdout + r.stderr)[-400:]
    if r.returncode == 0:
        state['version'] += 1
        state['built'] = time.strftime('%H:%M:%S')
    state['busy'] = False

def watch():
    last = None
    while True:
        try:
            m = os.path.getmtime(DESIGN)
        except OSError:
            time.sleep(1); continue
        if m != last:
            time.sleep(2.5)                      # warten, bis der Schreibvorgang fertig ist
            try:
                m2 = os.path.getmtime(DESIGN)
            except OSError:
                continue
            if m2 == m:
                state['design_saved'] = time.strftime('%H:%M:%S', time.localtime(m))
                do_export(); last = m
        time.sleep(1)

def board():
    rows = []
    try:
        for l in open(os.path.join(ROOT, 'docs', 'integration-board.md'), encoding='utf-8'):
            if l.startswith('|') and not l.startswith('|---'):
                c = [x.strip() for x in l.strip().strip('|').split('|')]
                if len(c) >= 5 and c[0] != 'Klasse':
                    rows.append({'klasse': c[0], 'n': c[1], 'wer': c[2], 'status': c[3], 'meldung': c[5] if len(c) > 5 else ''})
    except OSError:
        pass
    return rows

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k): super().__init__(*a, directory=HERE, **k)
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store'); super().end_headers()
    def do_GET(self):
        if self.path.startswith('/api/board'):
            b = json.dumps(board()).encode()
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b)))
            self.end_headers(); self.wfile.write(b); return
        if self.path.startswith('/api/state'):
            b = json.dumps(state).encode()
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b)))
            self.end_headers(); self.wfile.write(b); return
        super().do_GET()
    def translate_path(self, path):
        # /history/... liefert den Bildverlauf (renders/history), alles andere kommt aus viewer/
        p = path.split('?', 1)[0]
        if p == '/descriptions.json':
            return os.path.join(ROOT, 'data', 'descriptions.json')
        if p == '/system-specs.json':
            return os.path.join(ROOT, 'data', 'system-specs.json')
        if p == '/history' or p.startswith('/history/'):
            rel = p[len('/history'):].lstrip('/') or 'index.html'
            full = os.path.abspath(os.path.join(ROOT, 'renders', 'history', rel))
            if full.startswith(os.path.join(ROOT, 'renders', 'history')):
                return full
        return super().translate_path(path)
    def log_message(self, *a): pass

threading.Thread(target=watch, daemon=True).start()
with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), H) as s:
    s.allow_reuse_address = True
    print(f'Viewer auf http://localhost:{PORT}/', flush=True)
    s.serve_forever()
