"""Exportiert ein Bauteil als Detailmodell fuer die Detailansicht des Viewers (alle Koerper, einzeln benannt).
Aufruf: python viewer/export_detail.py <komponente> [<komponente> ...]
Liest data/parts/<komponente>.json (Feld `datei` = .sc-Pfad), exportiert ALLE Koerper (kein MIN_DIAG) nach viewer/detail/<komponente>.obj
und schreibt viewer/detail/<komponente>.json (je Koerper name, material, farbe, opacity, masse_g, bbox, teil).
Zwischenspeicher nach Aenderungszeit der .sc und der Teiledatei. viewer/detail/ wird nie committet; der Hauptexport (export_model.py) bleibt unberuehrt.
Bricht ab, wenn Koerpernamen im .sc und in data/parts nicht genau zusammenpassen."""
import json, os, subprocess, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
CLI = r'C:\Program Files\SolidCraft\solidcraft-cli.exe'
OUT = os.path.join(HERE, 'detail')
fw = lambda p: os.path.abspath(p).replace(chr(92), '/')

def find(o, key):
    if isinstance(o, dict):
        if key in o and isinstance(o[key], list): return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None: return r

def build(comp):
    pj = os.path.join(ROOT, 'data', 'parts', comp + '.json')
    parts = json.load(open(pj, encoding='utf-8'))
    sc = os.path.join(ROOT, parts['datei'])
    os.makedirs(OUT, exist_ok=True)
    obj, meta = os.path.join(OUT, comp + '.obj'), os.path.join(OUT, comp + '.json')
    key = f'{os.path.getmtime(sc)}|{os.path.getmtime(pj)}'
    if os.path.exists(obj) and os.path.exists(meta) and json.load(open(meta, encoding='utf-8')).get('cache') == key:
        print(f'{comp}: aktuell (Zwischenspeicher)'); return
    ev = os.path.join(OUT, '_ev.json')
    subprocess.run([CLI, 'eval', fw(sc), '--json-out', ev], capture_output=True)
    bodies = find(json.load(open(ev, encoding='utf-8')), 'bodies') or []; os.remove(ev)
    names = [b['name'] for b in bodies]
    zd = json.loads(zipfile.ZipFile(sc).read('document.json'))
    mats = {m['name']: m['appearance'] for m in zd.get('user_materials', [])}
    owner = {}
    for t in parts['teile']:
        for k in t['koerper']:
            if k in owner: sys.exit(f'{comp}: Koerper {k} doppelt in data/parts')
            owner[k] = t['id']
    fehlt, zuviel = sorted(set(names) - set(owner)), sorted(set(owner) - set(names))
    if fehlt or zuviel or len(names) != len(set(names)):
        sys.exit(f'{comp}: Koerper passen nicht: nur im .sc {fehlt}, nur in parts {zuviel}')
    tmp = os.path.join(OUT, '_job.json')
    json.dump({'commands': [{'command': 'doc.open', 'params': {'path': fw(sc), 'read_only': True}},
                            {'command': 'file.export', 'params': {'path': fw(obj + '.tmp'), 'format': 'obj', 'bodies': names}}]}, open(tmp, 'w'))
    r = subprocess.run([CLI, 'run', tmp, '--quiet'], capture_output=True, text=True); os.remove(tmp)
    if r.returncode or not os.path.exists(obj + '.tmp'):
        sys.exit(f'{comp}: Export fehlgeschlagen {(r.stdout + r.stderr)[-300:]}')
    os.replace(obj + '.tmp', obj)
    out = []
    for b in bodies:
        mn = b.get('material') or zd['materials'].get(b['name'], '')
        ap = mats.get(mn, {})
        c = ap.get('color', [176, 184, 192])
        out.append({'name': b['name'], 'material': mn, 'farbe': '#%02x%02x%02x' % tuple(c), 'opacity': ap.get('opacity', 1),
                    'masse_g': b.get('mass_g'), 'bbox': b['bbox'], 'teil': owner[b['name']]})
    json.dump({'komponente': comp, 'cache': key, 'koerper': out}, open(meta, 'w', encoding='utf-8'), ensure_ascii=False)
    print(f'{comp}: {len(out)} Koerper, {os.path.getsize(obj)/1e6:.2f} MB')

for c in sys.argv[1:] or ['feinfilter', 'tank_klein']:
    build(c)
