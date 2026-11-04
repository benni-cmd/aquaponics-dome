"""Schreibt viewer/ansicht.json: die Nebendatei fuer die Ansicht Visuell/Technisch des Viewers (W68, N-STUECKLISTE 5b).

Inhalt (alles nur gelesen aus data/, nichts geraten):
  komponenten[<definition>] = { gruppe: Bauteilgruppe, werkstoff: { <Koerpername>: <Werkstoff> } }   aus data/parts/<definition>.json
  leitungsart[<definition>] = [ Leitungsart je Instanz, in der Reihenfolge von viewer/instances.json ]  fuer die Rohrteile lt_*
Leitungsart (Zulauf, Ruecklauf, Luft, Frischwasser): Die Instanz liegt auf der Mittellinie (`pfad`) einer Trasse aus data/leitungstrassen.json
(naechste Trasse, Abstand gemessen); die Trasse gehoert zu einer Kante K<nn> aus data/leitungsnetz.json. Art je Kante:
  medium Luft -> Luft; Kante beginnt an frischwasser oder aktivkohle -> Frischwasser; Kante endet an pool, ruecklauf_*, beet_sumpf_* oder zweitbecken -> Ruecklauf
  (ausser sie beginnt am pool: Ablauf aus dem Pool zum Filter = Zulauf); alle uebrigen Kanten (Pool, Filter, Pumpen bis zu den Pflanzen) -> Zulauf.
Kabel haben keine Rohrteile; der Viewer faerbt sie ueber den Werkstoff kabel_pvc.
Aufruf: python viewer/export_ansicht.py   (wird von export_model.py am Ende und von serve.py bei veralteter Datei aufgerufen)
"""
import glob, json, math, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('ANSICHT_ROOT') or os.path.abspath(os.path.join(HERE, '..'))
VIEWER = os.environ.get('ANSICHT_VIEWER') or HERE
ABSTAND_MAX_MM = 150   # weiter von jeder Trasse entfernt: Art unbekannt (None)


def jl(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def kanten_art(netz):
    art = {}
    for k in netz['kanten']:
        v, n = k['von'], k['nach']
        if k.get('medium') == 'Luft':
            a = 'Luft'
        elif v in ('frischwasser', 'aktivkohle'):
            a = 'Frischwasser'
        elif v != 'pool' and (n in ('pool', 'zweitbecken') or n.startswith('ruecklauf_') or n.startswith('beet_sumpf_')):
            a = 'Ruecklauf'
        else:
            a = 'Zulauf'
        art[k['id']] = a
    return art


def punkt_strecke(p, a, b):
    ab = [b[i] - a[i] for i in range(3)]
    ap = [p[i] - a[i] for i in range(3)]
    ll = sum(x * x for x in ab) or 1e-9
    u = max(0.0, min(1.0, sum(ap[i] * ab[i] for i in range(3)) / ll))
    return math.dist(p, [a[i] + u * ab[i] for i in range(3)])


def bauen():
    komp = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'parts', '*.json'))):
        d = jl(f)
        w = {}
        for t in d.get('teile', []):
            for k in t.get('koerper', []):
                w[k] = t.get('werkstoff')
        komp[os.path.splitext(os.path.basename(f))[0]] = {'gruppe': d.get('bauteilgruppe'), 'werkstoff': w}
    inst = jl(os.path.join(VIEWER, 'instances.json'))
    netz = jl(os.path.join(ROOT, 'data', 'leitungsnetz.json'))
    trassen = jl(os.path.join(ROOT, 'data', 'leitungstrassen.json'))['trassen']
    art_von_kante = kanten_art(netz)
    pfade = []
    for t in trassen:
        m = re.match(r'K\d+', t['id'])
        kante = t.get('kante') or (m.group(0) if m else None)
        if kante in art_von_kante and len(t.get('pfad', [])) > 1:
            pfade.append((art_von_kante[kante], t['pfad']))
    arten = {}
    unbekannt = 0
    for i in inst['instances']:
        if not i['d'].lower().startswith('lt_'):
            continue
        p = [i['m'][3], i['m'][7], i['m'][11]]
        best, art = None, None
        for a, pf in pfade:
            dmin = min(punkt_strecke(p, pf[k], pf[k + 1]) for k in range(len(pf) - 1))
            if best is None or dmin < best:
                best, art = dmin, a
        if best is None or best > ABSTAND_MAX_MM:
            art = None
            unbekannt += 1
        arten.setdefault(i['d'], []).append(art)
    return {'built': inst.get('built'), 'komponenten': komp, 'leitungsart': arten, 'leitungsart_unbekannt': unbekannt}


def main():
    out = bauen()
    ziel = os.path.join(VIEWER, 'ansicht.json')
    with open(ziel + '.tmp', 'w', encoding='utf-8') as f:
        json.dump(out, f, ensure_ascii=False, separators=(',', ':'))
    os.replace(ziel + '.tmp', ziel)
    n = sum(len(v) for v in out['leitungsart'].values())
    zaehl = {}
    for v in out['leitungsart'].values():
        for a in v:
            zaehl[a] = zaehl.get(a, 0) + 1
    print(f"ansicht.json: {len(out['komponenten'])} Komponenten, {n} Rohrteil-Instanzen, Arten {zaehl}, unbekannt {out['leitungsart_unbekannt']}")


if __name__ == '__main__':
    main()
