"""Lokaler Live-Viewer-Server fuer das Kuppel-Modell.
Aufruf: python viewer/serve.py [port]   (Standard 4410), dann im Browser http://localhost:4410/  (Variante Ring B2: ?variante=ring_b2)
Beobachtet designs/dome.sc und designs/dome-ring_b2.sc (N-VARIANTEN VV); nach jeder Speicherung (Aenderungszeit stabil) wird die geaenderte
Variante neu exportiert (viewer/export_model.py --variante <v>), die Seite fragt /api/state?variante=<v> ab und laedt das Modell neu, ohne die Kamera zu verlieren.
Ausgabepfade, Kennzahlen und Stueckliste je Variante kommen aus scripts/variante.py (Tabelle 1.3 in docs/jobs/N-VARIANTEN.md)."""
import http.server, json, os, socketserver, subprocess, sys, threading, time
from urllib.parse import parse_qs, urlsplit
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import variante as V   # nur pfad() und VARIANTEN; der Schalter dieser Datei ist die Adresse ?variante=, nie die Kommandozeile
EXPORT = os.path.join(HERE, 'export_model.py')
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 4410
export_lock = threading.Lock()                      # nie zwei Exporte zugleich (CLI und defs/ gemeinsam)
states = {v: {'version': 0, 'built': '', 'busy': False, 'error': '', 'design_saved': ''} for v in V.VARIANTEN}
P = lambda art, v: V.pfad(art, v, root=ROOT)

# Nach einem Neustart sofort das zuletzt exportierte Modell anbieten (die Seite laedt erst ab version > 0); der neue Export laeuft nur, wenn das Modell neuer ist
for _v in V.VARIANTEN:
    _inst = P('instances', _v)
    if os.path.exists(_inst):
        states[_v]['version'] = 1
        states[_v]['built'] = time.strftime('%H:%M:%S', time.localtime(os.path.getmtime(_inst)))
        try:   # "Modell gespeichert": ohne Export seit dem Start die Zeit aus instances.json zeigen (A6), Datum nur wenn nicht heute
            _b = str(json.load(open(_inst, encoding='utf-8')).get('built', ''))
            if _b: states[_v]['design_saved'] = _b[11:19] if _b[:10] == time.strftime('%Y-%m-%d') else f'{_b[8:10]}.{_b[5:7]}. {_b[11:19]}'
        except (OSError, ValueError): pass

def do_export(v):
    st = states[v]
    st['busy'] = True
    try:
        with export_lock:
            r = subprocess.run([sys.executable, '-I', EXPORT, '--variante', v], capture_output=True, text=True)
        st['error'] = '' if r.returncode == 0 else (r.stdout + r.stderr)[-400:]
        if r.returncode == 0:
            st['version'] += 1
            st['built'] = time.strftime('%H:%M:%S')
    finally:
        st['busy'] = False

def watch(v):
    design, inst, last = P('modell', v), P('instances', v), None
    try:   # Start: nur exportieren, wenn das Modell neuer ist als der letzte Export (sonst Export ohne Anlass, W66)
        if os.path.exists(inst) and os.path.getmtime(inst) >= os.path.getmtime(design): last = os.path.getmtime(design)
    except OSError: pass
    while True:
        try:
            m = os.path.getmtime(design)
        except OSError:
            time.sleep(1); continue
        if m != last:
            time.sleep(2.5)                      # warten, bis der Schreibvorgang fertig ist
            try:
                m2 = os.path.getmtime(design)
            except OSError:
                continue
            if m2 == m:
                states[v]['design_saved'] = time.strftime('%H:%M:%S', time.localtime(m))
                do_export(v); last = m
        time.sleep(1)

def ansicht_pruefen(v):
    # ansicht.json der Variante (Werkstoff, Gruppe, Leitungsart) neu erzeugen, wenn sie fehlt oder aelter ist als instances.json oder eine Teiledatei
    ziel, inst = P('ansicht', v), P('instances', v)
    try:
        if not os.path.exists(inst): return
        jung = os.path.getmtime(ziel) if os.path.exists(ziel) else 0
        stand = max([os.path.getmtime(inst), os.path.getmtime(os.path.join(ROOT, 'data', 'leitungstrassen.json')), os.path.getmtime(os.path.join(ROOT, 'data', 'leitungsnetz.json'))] +
                    [e.stat().st_mtime for e in os.scandir(os.path.join(ROOT, 'data', 'parts')) if e.name.endswith('.json')])
        if jung < stand:
            subprocess.run([sys.executable, '-I', os.path.join(HERE, 'export_ansicht.py'), '--variante', v], capture_output=True, text=True, timeout=60)
    except Exception:
        pass

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

def variante_der_anfrage(path):
    q = parse_qs(urlsplit(path).query).get('variante', ['a_plus'])[0]
    return q if q in V.VARIANTEN else 'a_plus'

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
            v = variante_der_anfrage(self.path)
            b = json.dumps(dict(states[v], variante=v)).encode()
            self.send_response(200); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(b)))
            self.end_headers(); self.wfile.write(b); return
        super().do_GET()
    def translate_path(self, path):
        # /history/... liefert den Bildverlauf (renders/history), Kennzahlen und Stueckliste je Variante, alles andere kommt aus viewer/ (auch varianten/<v>/...)
        p = path.split('?', 1)[0]
        v = variante_der_anfrage(path)
        if p == '/descriptions.json':
            return os.path.join(ROOT, 'data', 'descriptions.json')
        if p == '/system-specs.json':
            return P('system_specs', v)
        if p == '/stueckliste.json':
            return P('stueckliste_json', v)
        if p == '/ansicht.json' or p.endswith('/ansicht.json'):
            vv = 'ring_b2' if '/varianten/ring_b2/' in p else v
            ansicht_pruefen(vv)
            return P('ansicht', vv)
        if p == '/katalog.json':
            return os.path.join(ROOT, 'data', 'katalog.json')
        if p.startswith('/parts/') and p.endswith('.json') and '/' not in p[len('/parts/'):] and '..' not in p:
            return os.path.join(ROOT, 'data', 'parts', p[len('/parts/'):])
        if p == '/history' or p.startswith('/history/'):
            rel = p[len('/history'):].lstrip('/') or 'index.html'
            full = os.path.abspath(os.path.join(ROOT, 'renders', 'history', rel))
            if full.startswith(os.path.join(ROOT, 'renders', 'history')):
                return full
        return super().translate_path(path)
    def log_message(self, *a): pass

for _v in V.VARIANTEN:
    threading.Thread(target=watch, args=(_v,), daemon=True).start()
with socketserver.ThreadingTCPServer(('127.0.0.1', PORT), H) as s:
    s.allow_reuse_address = True
    print(f'Viewer auf http://localhost:{PORT}/', flush=True)
    s.serve_forever()
