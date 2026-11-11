"""N-VIEWER-HOSTING: baut die statische Viewer-Ausgabe viewer/dist/ reproduzierbar (Hosting ohne serve.py).
Aufruf: python -X utf8 scripts/viewer_dist.py [--nur-messen]
Eingaben: viewer/ (index.html, *.json, defs/, detail/, varianten/<v>/), data/ (parts, katalog, descriptions, messstellen, stueckliste*, system-specs*).
Ausgabe viewer/dist/ (nie committen, steht in .gitignore; .vercel und .vercelignore bleiben beim Neubau erhalten):
  index.html            Kopie von viewer/index.html mit <meta name="viewer-modus" content="statisch">
  defs/*.obj.gz, detail/*.obj.gz   OBJ-Text, Koordinaten auf 0,01 mm (Normalen 0,001) gerundet, gzip -9; der Browser entpackt per DecompressionStream
  alle JSON-Dateien     unveraendert (Viewer liest sie ueber die Namen, die der fetch-Umschalter in index.html abbildet)
  download/             kuppel-<variante>.zip + download.json (scripts/model_download.py, Inhalt aus Git HEAD)
  statik.json           Stand und vorhandene Varianten;  vercel.json  Header (kein Cache-Zwang, noindex)
Messung: Groesse vorher (Quellordner) und nachher (dist) wird am Ende gedruckt."""
import gzip, json, os, re, shutil, sys, time
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = os.path.join(ROOT, 'viewer'); D = os.path.join(ROOT, 'data'); OUT = os.path.join(V, 'dist')
BEHALTEN = ('.vercel', '.vercelignore')   # Deploy-Zustand, wird beim Neubau nicht geloescht
ZAHL = re.compile(r'-?\d+\.\d+(?:e-?\d+)?')

def runde(n):
    def f(m):
        t = ('%.*f' % (n, float(m.group(0)))).rstrip('0').rstrip('.')
        return '0' if t in ('-0', '') else t
    return f
R_POS, R_NRM = runde(2), runde(3)

def obj_kompakt(text):
    out = []
    for l in text.split('\n'):
        if l.startswith('v '): l = ZAHL.sub(R_POS, l)
        elif l.startswith('vn '): l = ZAHL.sub(R_NRM, l)
        out.append(l)
    return '\n'.join(out).encode('utf-8')

def job(a):
    src, dst = a
    with open(src, encoding='utf-8') as f: b = obj_kompakt(f.read())
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'wb') as f: f.write(gzip.compress(b, 9, mtime=0))     # mtime=0: gleiche Eingabe -> gleiche Bytes
    return os.path.getsize(src), os.path.getsize(dst)

def dirsize(p):
    return sum(os.path.getsize(os.path.join(a, f)) for a, _, fs in os.walk(p) for f in fs)

def kopie(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(src, dst)

def main():
    t0 = time.time()
    # Inhalt leeren, den Ordner selbst und die Deploy-Dateien behalten: .vercel (Projektbindung) bleibt, .vercelignore wird bei Bedarf geschrieben
    os.makedirs(OUT, exist_ok=True)
    for name in os.listdir(OUT):
        if name in BEHALTEN: continue
        pfad = os.path.join(OUT, name)
        shutil.rmtree(pfad) if os.path.isdir(pfad) else os.remove(pfad)
    if not os.path.exists(os.path.join(OUT, '.vercelignore')):
        open(os.path.join(OUT, '.vercelignore'), 'w', encoding='utf-8', newline='\n').write('.env*\n.vercel\n')
    jobs = []
    for sub in ('defs', 'detail'):
        for f in sorted(os.listdir(os.path.join(V, sub))):
            p = os.path.join(V, sub, f)
            if f.endswith('.obj'): jobs.append((p, os.path.join(OUT, sub, f + '.gz')))
            elif f.endswith('.json'): kopie(p, os.path.join(OUT, sub, f))
    with Pool() as pool: res = pool.map(job, jobs, chunksize=8)
    # Seite und Nebendateien
    html = open(os.path.join(V, 'index.html'), encoding='utf-8').read()
    html = html.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="viewer-modus" content="statisch">', 1)
    assert 'viewer-modus' in html.split('<script', 1)[0]
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(html)
    for f in ('instances.json', 'ansicht.json', 'extras.json', 'farben.json', 'anschluesse.json'):
        if os.path.exists(os.path.join(V, f)): kopie(os.path.join(V, f), os.path.join(OUT, f))
    for f in ('descriptions.json', 'katalog.json', 'messstellen.json', 'stueckliste.json', 'system-specs.json'):
        if os.path.exists(os.path.join(D, f)): kopie(os.path.join(D, f), os.path.join(OUT, f))
    for f in os.listdir(os.path.join(D, 'parts')):
        if f.endswith('.json'): kopie(os.path.join(D, 'parts', f), os.path.join(OUT, 'parts', f))
    built = json.load(open(os.path.join(V, 'instances.json'), encoding='utf-8')).get('built', '')
    json.dump({'stand': built, 'gebaut': time.strftime('%Y-%m-%d %H:%M:%S')}, open(os.path.join(OUT, 'statik.json'), 'w'))
    json.dump({'headers': [{'source': '/(.*)', 'headers': [{'key': 'X-Robots-Tag', 'value': 'noindex, nofollow'}]},
                           {'source': '/(.*)\\.gz', 'headers': [{'key': 'Cache-Control', 'value': 'public, max-age=0, must-revalidate'}]}]},
              open(os.path.join(OUT, 'vercel.json'), 'w'), indent=1)
    import model_download                                  # Download-Knopf: SolidCraft-Modell aus Git (HEAD)
    model_download.main(['--out', os.path.join(OUT, 'download')])
    vor, nach = sum(r[0] for r in res), sum(r[1] for r in res)
    print(f'OBJ-Dateien: {len(res)}  roh {vor/1e6:.1f} MB -> gzip {nach/1e6:.1f} MB  (Faktor {vor/max(nach,1):.1f})')
    print(f'Quelle viewer/defs+detail: {(dirsize(os.path.join(V,"defs"))+dirsize(os.path.join(V,"detail")))/1e6:.1f} MB;  dist gesamt: {dirsize(OUT)/1e6:.1f} MB;  Dateien: {sum(len(fs) for _,_,fs in os.walk(OUT))};  groesste Datei: {max(os.path.getsize(os.path.join(a,f)) for a,_,fs in os.walk(OUT) for f in fs)/1e6:.1f} MB;  {time.time()-t0:.0f} s')

if __name__ == '__main__':
    main()
