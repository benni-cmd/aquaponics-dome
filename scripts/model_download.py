"""Download-Pakete des SolidCraft-Modells fuer den gehosteten Viewer (Wunsch Ben 10.11.2026: Leon soll das Modell herunterladen koennen).
Aufruf: python -X utf8 scripts/model_download.py [--ref a_plus=<commit>] [--ref ring_b2=<commit>] [--out viewer/dist/download]
Je Variante ein ZIP kuppel-<variante>.zip mit dem Gesamtmodell (designs/dome*.sc), allen darin verknuepften Komponenten
(designs/components/*.sc, relativ verlinkt) und LIESMICH.txt. Inhalt kommt aus Git (Standard HEAD), nie aus ungesicherten
Arbeitsdateien; so passt der Download zum Stand, aus dem der Viewer exportiert wurde. Dazu download.json fuer den Button."""
import argparse, io, json, os, re, subprocess, sys, time, zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import variante  # noqa: E402

NAMEN = {'a_plus': 'Kreislauf A+', 'ring_b2': 'Kreislauf Ring B2'}

def git(*a, binary=False):
    r = subprocess.run(['git', '-C', ROOT, *a], capture_output=True)
    if r.returncode: raise SystemExit('git ' + ' '.join(a) + ': ' + r.stderr.decode('utf-8', 'ignore'))
    return r.stdout if binary else r.stdout.decode('utf-8').strip()

def paket(v, ref, out):
    modell = variante.pfad('modell', v, root='.').replace('\\', '/').lstrip('./')
    sc = git('show', f'{ref}:{modell}', binary=True)
    doc = zipfile.ZipFile(io.BytesIO(sc)).read('document.json').decode('utf-8', 'ignore')
    comps = sorted(set(re.findall(r'components/[\w.-]+\.sc', doc)))
    commit = git('rev-parse', '--short', ref); datum = git('log', '-1', '--format=%ci', ref)
    liesmich = (f'Aquaponik-Kuppel, {NAMEN[v]}\nStand: Commit {commit} vom {datum}\n\n'
                f'Oeffnen mit SolidCraft (kostenlos, Open Source): https://solidcraft.io , Version 0.25.1 oder neuer.\n'
                f'1. ZIP komplett entpacken, Ordnerstruktur beibehalten.\n'
                f'2. In SolidCraft die Datei {os.path.basename(modell)} oeffnen.\n'
                f'   Sie verweist auf {len(comps)} Bauteile im Unterordner components/ und laedt sie von dort.\n'
                f'Hinweis: Wird die Datei in einer neueren SolidCraft-Version gespeichert, oeffnet sie nicht mehr in aelteren.\n')
    os.makedirs(out, exist_ok=True)
    ziel = os.path.join(out, f'kuppel-{v}.zip')
    with zipfile.ZipFile(ziel, 'w', zipfile.ZIP_STORED) as z:   # .sc sind selbst ZIP-komprimiert
        for name, data in [(f'kuppel-{v}/{os.path.basename(modell)}', sc)] + \
                          [(f'kuppel-{v}/{c}', git('show', f'{ref}:designs/{c}', binary=True)) for c in comps]:
            info = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0)); z.writestr(info, data)
        z.writestr(zipfile.ZipInfo(f'kuppel-{v}/LIESMICH.txt', (1980, 1, 1, 0, 0, 0)), liesmich.encode('utf-8'))
    mb = os.path.getsize(ziel) / 1e6
    print(f'{v}: {ziel}  {mb:.1f} MB  {len(comps)} Bauteile  Commit {commit}')
    return {'datei': f'download/kuppel-{v}.zip', 'mb': round(mb, 1), 'commit': commit, 'datum': datum, 'bauteile': len(comps)}

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--ref', action='append', default=[], help='variante=commit, Standard HEAD')
    ap.add_argument('--out', default=os.path.join(ROOT, 'viewer', 'dist', 'download'))
    ap.add_argument('--varianten', default='a_plus,ring_b2')
    a = ap.parse_args(argv)
    refs = dict(x.split('=', 1) for x in a.ref)
    t0 = time.time(); info = {}
    for v in a.varianten.split(','):
        try: info[v] = paket(v, refs.get(v, 'HEAD'), a.out)
        except SystemExit as e:   # z. B. Variantenbauteile nicht in Git: lieber kein Knopf als ein unvollstaendiges Modell
            print(f'{v}: kein Download ({e})')
            if os.path.exists(os.path.join(a.out, f'kuppel-{v}.zip')): os.remove(os.path.join(a.out, f'kuppel-{v}.zip'))
    json.dump(info, open(os.path.join(a.out, 'download.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'download.json geschrieben, {time.time() - t0:.0f} s')

if __name__ == '__main__':
    main()
