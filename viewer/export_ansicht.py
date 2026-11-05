"""Schreibt viewer/ansicht.json: die Nebendatei fuer die Ansicht Visuell/Technisch des Viewers (W68, N-STUECKLISTE 5b).

Inhalt (alles nur gelesen aus data/, nichts geraten):
  komponenten[<definition>] = { gruppe: Bauteilgruppe, werkstoff: { <Koerpername>: <Werkstoff> } }   aus data/parts/<definition>.json
  leitungsart[<definition>] = [ Leitungsart je Instanz, in der Reihenfolge von viewer/instances.json ]  fuer die Rohrteile lt_*
Leitungsart (Zulauf, Ruecklauf, Luft, Frischwasser): Die Instanz liegt auf der Mittellinie (`pfad`) einer Trasse aus data/leitungstrassen.json
(naechste Trasse, Abstand gemessen); die Trasse gehoert zu einer Kante K<nn> aus data/leitungsnetz.json. Art je Kante:
  medium Luft -> Luft; Kante beginnt an frischwasser oder aktivkohle -> Frischwasser; Kante endet an pool, ruecklauf_*, beet_sumpf_* oder zweitbecken -> Ruecklauf
  (ausser sie beginnt am pool: Ablauf aus dem Pool zum Filter = Zulauf); alle uebrigen Kanten (Pool, Filter, Pumpen bis zu den Pflanzen) -> Zulauf.
Kabel haben keine Rohrteile; der Viewer faerbt sie ueber den Werkstoff kabel_pvc.
kreislauf (N-VIEWER-KREISLAEUFE, W87): welche Teile zu Wasser-, Luft- und Stromkreislauf gehoeren (Schalter im Viewer), nur aus Daten:
  instanz[<lt_*-Definition>] = [ "wasser" | "luft" | null je Instanz ]   aus leitungsart; fehlt sie: Feld `linie` des naechsten Eintrags `teile` in leitungstrassen.json
  stamm[<Definition>]        = [ Kreislaeufe, zu denen alle Instanzen gehoeren ]   Tanks, Pumpen, Filter ...: Knoten (bauteil/id) an Kanten mit Medium Wasser oder Luft in leitungsnetz.json;
                               Strom: Kabelliste (Medium Strom) in leitungsnetz.json und Teiletitel mit "Kabel"; Gruppe Leitungen ohne Knoten: naechste Trasse
  koerper[<Definition>]      = { <Koerpername>: [ "strom" ] }   Kabel, Stecker (Werkstoff kabel_pvc oder Name) in Teilen, die sonst nicht am Strom haengen
Aufruf: python viewer/export_ansicht.py [--variante ring_b2]   (wird von export_model.py am Ende und von serve.py bei veralteter Datei aufgerufen)
"""
import glob, json, math, os, re, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get('ANSICHT_ROOT') or os.path.abspath(os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(os.path.abspath(os.path.join(HERE, '..')), 'scripts'))
import variante as V   # N-VARIANTEN V1a
VAR = V.aktiv()
VIEWER = os.environ.get('ANSICHT_VIEWER') or V.pfad('viewer_dir', VAR, root=os.path.abspath(os.path.join(HERE, '..')))   # a_plus: viewer/, ring_b2: viewer/varianten/ring_b2/
ABSTAND_MAX_MM = 150   # weiter von jeder Trasse entfernt: Art unbekannt (None)
TEIL_NAH_MM = 100      # Kreislauf-Rueckfall: Rohrteil liegt so nah an einem Eintrag `teile` der Trassendatei


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

KREISE = ('wasser', 'luft', 'strom')
KABEL_KOERPER = re.compile(r'^(netz)?kabel(_\d+)?$|^stecker', re.I)   # Kabel und Stecker, nicht Kabelverschraubung


def art_zu_kreis(a):
    return {'Luft': 'luft', 'Zulauf': 'wasser', 'Ruecklauf': 'wasser', 'Frischwasser': 'wasser'}.get(a)


def linie_zu_kreis(linie):
    if isinstance(linie, str):
        return 'luft' if linie.startswith('luft') else ('wasser' if linie == 'frisch' else None)
    return 'wasser' if isinstance(linie, int) else None


def passt(stem, key):
    return bool(key) and (stem == key or stem.startswith(key + '_') or stem.startswith(key + '-'))   # '-ring_b2': Variantenname


def kreislauf_bauen(inst, netz, trassen_roh, komp, arten, pfade):
    """Siehe Kopf der Datei (kreislauf). Gibt (daten, zaehlung) zurueck."""
    stems = sorted({i['d'] for i in inst['instances']})
    n_inst = {}
    for i in inst['instances']:
        n_inst[i['d']] = n_inst.get(i['d'], 0) + 1
    knoten_kreis = {}
    for k in netz['kanten']:
        if k.get('medium') == 'Luft':
            knoten_kreis.setdefault(k['von'], set()).add('luft')    # nur die Quelle (Gebloese); belueftete Becken gehoeren zum Wasser
        elif k.get('medium') == 'Wasser':
            for n in (k['von'], k['nach']):
                knoten_kreis.setdefault(n, set()).add('wasser')
    knoten_schluessel = []
    for kn in netz['knoten']:
        c = knoten_kreis.get(kn['id'])
        if c:
            knoten_schluessel.append((kn.get('bauteil'), kn['id'], c))
    # Strom: Namen aus der Kabelliste (Medium Strom); 'pumpe_gross_1..4' -> 'pumpe_gross'; 'geblaese_fisch' -> Wortanfang 'geblaese'
    strom_namen = set()
    for kb in netz.get('kabel', []):
        if kb.get('medium') != 'Strom':
            continue
        for n in (kb['von'], kb['nach']):
            strom_namen.add(re.sub(r'(_\d+\.\.\d+|_\d+)$', '', n))
    stamm, koerper, instanz = {}, {}, {}
    naechste_trasse = {}
    for stem in stems:
        P = komp.get(stem, {})
        if stem.lower().startswith('lt_'):
            continue
        k = set()
        for bauteil, nid, c in knoten_schluessel:
            if passt(stem, bauteil) or passt(stem, nid):
                k |= c
        if any(passt(stem, n) or (stem.split('_')[0] == n.split('_')[0] and stem.split('_')[0] in ('pumpe', 'geblaese')) for n in strom_namen):
            k.add('strom')
        if P.get('gruppe') == 'Messtechnik und Elektrik' and 'kabel' in (P.get('titel') or '').lower():
            k.add('strom')
        if not k and P.get('gruppe') == 'Leitungen':
            # keine Netzknoten: je Instanz die naechste Trasse (Luftverteiler, Scheibenbelueftung); nur wenn sie auf der Mittellinie liegt
            res = []
            for i in inst['instances']:
                if i['d'] == stem:
                    p = [i['m'][3], i['m'][7], i['m'][11]]
                    best, art = None, None
                    for a, pf in pfade:
                        dmin = min(punkt_strecke(p, pf[j], pf[j + 1]) for j in range(len(pf) - 1))
                        if best is None or dmin < best:
                            best, art = dmin, a
                    res.append(art_zu_kreis(art) if best is not None and best <= ABSTAND_MAX_MM else None)
            if any(res):
                naechste_trasse[stem] = res
                continue
        if k:
            stamm[stem] = [c for c in KREISE if c in k]
        if 'strom' not in k:
            kb = {n: ['strom'] for n, w in P.get('werkstoff', {}).items() if w == 'kabel_pvc' or KABEL_KOERPER.search(n)}
            if kb:
                koerper[stem] = kb
    teile = [(t['datei'], t['pos'], t.get('linie')) for t in trassen_roh.get('teile', []) if t.get('datei') and t.get('pos')]
    zaehl = {c: 0 for c in KREISE}
    ohne = 0
    pos_je = {}
    for i in inst['instances']:
        pos_je.setdefault(i['d'], []).append([i['m'][3], i['m'][7], i['m'][11]])
    for stem, liste in arten.items():
        out = []
        for idx, a in enumerate(liste):
            c = art_zu_kreis(a)
            if c is None:
                best = None
                for d, tp, linie in teile:
                    if d == stem:
                        dd = math.dist(pos_je[stem][idx], tp)
                        if dd <= TEIL_NAH_MM and (best is None or dd < best[0]):
                            best = (dd, linie)
                c = linie_zu_kreis(best[1]) if best else None
            if c is None:
                ohne += 1
            else:
                zaehl[c] += 1
            out.append(c)
        instanz[stem] = out
    for stem, res in naechste_trasse.items():
        instanz[stem] = res
        for c in res:
            if c:
                zaehl[c] += 1
    for stem, ks in stamm.items():
        for c in ks:
            zaehl[c] += n_inst.get(stem, 0)
    return ({'instanz': instanz, 'stamm': stamm, 'koerper': koerper},
            {'instanzen_je_kreis': zaehl, 'rohrteile_ohne_zuordnung': ohne,
             'stamm_definitionen': {c: sum(1 for v in stamm.values() if c in v) for c in KREISE}})


def bauen():
    komp = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'data', 'parts', '*.json'))):
        d = jl(f)
        w = {}
        for t in d.get('teile', []):
            for k in t.get('koerper', []):
                w[k] = t.get('werkstoff')
        komp[os.path.splitext(os.path.basename(f))[0]] = {'gruppe': d.get('bauteilgruppe'), 'werkstoff': w, 'titel': d.get('titel')}
    inst = jl(os.path.join(VIEWER, 'instances.json'))
    netz = jl(os.path.join(ROOT, 'data', 'leitungsnetz.json'))
    netz['kanten'] = V.filtere(netz['kanten'], VAR)   # Eintraege ohne Feld `varianten` gelten fuer beide
    trassen_roh = jl(os.path.join(ROOT, 'data', 'leitungstrassen.json'))
    trassen = V.filtere(trassen_roh['trassen'], VAR)
    trassen_roh = dict(trassen_roh, teile=V.filtere(trassen_roh.get('teile', []), VAR))
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
    kreis, kzaehl = kreislauf_bauen(inst, netz, trassen_roh, komp, arten, pfade)
    for v in komp.values():
        v.pop('titel', None)    # nur fuer die Zuordnung gebraucht, bleibt aus der Datei
    return {'built': inst.get('built'), 'komponenten': komp, 'leitungsart': arten, 'leitungsart_unbekannt': unbekannt, 'kreislauf': kreis}, kzaehl


def main():
    out, kzaehl = bauen()
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
    print('kreislauf:', json.dumps(kzaehl))


if __name__ == '__main__':
    main()
