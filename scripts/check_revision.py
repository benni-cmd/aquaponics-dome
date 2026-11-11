"""M10-S2N (R47 M1/M2, A+): Zugaenge am vergrabenen Hauptkreislauf. Nur Lesen, nur Standardbibliothek.
Aufruf: python -X utf8 scripts/check_revision.py [trassen.json] [--linie 1|2] [--json]
Misst im Leitungsnetz der Linien 1 und 2 (Trassen verbunden ueber T-Stuecke und Reduzier-/Hahn-Eintraege) den Abstand ENTLANG DER ACHSE zum naechsten Zugang:
  1. je vergrabener Wasserstrecke (Teilstueck-Mitte unter Flur Z 400) den groessten Abstand eines Punktes zum naechsten Zugang, Soll <= 3000 mm;
  2. je vergrabenem Knick (Richtungswechsel > 1 Grad, Punkt unter Flur) den Abstand zum naechsten Zugang, Soll <= 1000 mm.
Zugang (docs/leitungsordnung.md Begriffe, Blatt docs/jobs/M10-S2N.md Schritt 1):
  Hahn      Eintrag in r_stuecke mit art kugelhahn (Schacht oder oberirdisch);
  Stutzen   Revisionssteiger (Trasse mit Feld "revision"): gemessen bis zum T auf der Leitung (das Steigrohr steht lotrecht darueber bis zur Kappe am Flur);
  Port      Trassenende an einem Bauteil-Port (stutzen, muffe, Reduziermuffe auf dem Stutzen) mit Z >= 400 (ueber Flur);
  Grube     Auslauf eines Feinfilters (offene Feinfilter-Grube): Trassenanfang am Stutzen mit Anschluss Feinfilter.
  Bodenablauf  Anfang am Pool-Bodenablauf (Spirale vom Becken aus) [A].
  Ein Hahn unter Flur zaehlt nur mit Schacht (lt_schacht_kugelhahn*, Grundriss <= 300 mm).
Nicht gezaehlt: Kappe auf einem Stumpf unter Flur. Ausgenommen (eigener Zweck, kein Hauptkreislauf): Schlammleitungen K07/K23, Wartungsablass KB*.
Ausgang 0 = keine Verstoesse, 1 = Verstoss."""
import heapq, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FZ = 400.0
MAX_STRECKE = 3000.0
MAX_KNICK = 1000.0
AUS = ("K07", "K23", "KB")
HAHN_L = {20: 0, 25: 0, 40: 0, 50: 112.0, 63: 125.0}   # Baulaenge Kugelhahn (scripts/workshop/leitung.ports lt_kugelhahn_d<d>, Port B)

def wasser(t): return t.get("linie") in (1, 2) and not t["id"].startswith(AUS)

def netz(doc):
    """Graph (Knoten -> [(Nachbar, Laenge)]), Zugangsknoten {Knoten: Art}, Teilstuecke [(tid, i, a, b, Knoten a, Knoten b)], Knicke [(tid, i, Punkt, Knoten)]."""
    adj, zug, segs, knicke = {}, {}, [], []
    def kante(u, v, L):
        adj.setdefault(u, []).append((v, L)); adj.setdefault(v, []).append((u, L))
    ts = {t["id"]: t for t in doc.get("t_stuecke", [])}
    rs = {r["id"]: r for r in doc.get("r_stuecke", [])}
    schacht = [e["pos"] for e in doc.get("teile", []) if e["datei"].startswith("lt_schacht_kugelhahn")]
    for r in rs.values():
        if r.get("linie") not in (1, 2): continue
        if r.get("art") == "kugelhahn":                                   # Hahn zaehlt nur erreichbar: ueber Flur oder mit Schacht (Hahnmitte <= 300 mm im Grundriss)
            if r["pos_a"][2] >= FZ - 100: zug[("R", r["id"])] = "Hahn " + r["id"]
            elif any(math.hypot(s[0] - r["pos_a"][0], s[1] - r["pos_a"][1]) <= 300 for s in schacht): zug[("R", r["id"])] = "Hahn im Schacht " + r["id"]
        elif r.get("auf_stutzen") and r["pos_a"][2] >= FZ: zug[("R", r["id"])] = "Port " + r["id"]
    enden = []                                                            # offene Enden / Kupplungen unter Flur: gleich liegende Enden verschiedener Trassen sind verbunden (K19 steckt auf dem Linie-2-Stumpf)
    for t in doc["trassen"]:
        if not wasser(t): continue
        tid, P = t["id"], [tuple(map(float, p)) for p in t["pfad"]]; n = len(P)
        for i in range(n - 1):
            kante((tid, i), (tid, i + 1), math.dist(P[i], P[i + 1]))
            segs.append((tid, i, P[i], P[i + 1], (tid, i), (tid, i + 1)))
        for i in range(1, n - 1):
            u = [P[i][k] - P[i - 1][k] for k in range(3)]; w = [P[i + 1][k] - P[i][k] for k in range(3)]
            c = sum(u[k] * w[k] for k in range(3)) / (math.hypot(*u) * math.hypot(*w))
            if math.degrees(math.acos(max(-1.0, min(1.0, c)))) > 1.0 and P[i][2] < FZ: knicke.append((tid, i, P[i], (tid, i)))
        for lage, j in (("start", 0), ("ende", n - 1)):
            art = t.get(lage, "stutzen")
            if art.startswith("t:") and art[2:] in ts: kante((tid, j), ("T", art[2:]), math.dist(P[j], ts[art[2:]]["pos"]))
            elif art.startswith("r:") and art[2:] in rs:
                r = rs[art[2:]]; L = math.dist(P[j], r["pos_a"])
                if r.get("art") == "kugelhahn": L = min(L, math.dist(P[j], [r["pos_a"][k] + r["dir"][k] * HAHN_L.get(int(r["d_gross"]), 0) for k in range(3)]))   # Hahn: Abstand bis zur naeheren Muffe
                kante((tid, j), ("R", art[2:]), L)
            elif art in ("stutzen", "muffe", "offen"):
                enden.append(((tid, j), P[j]))
                if t.get("revision") and lage == "ende": zug[(tid, 0)] = "Stutzen " + tid     # Revisionsstutzen: Zugang zur Leitung am T (Steigrohr lotrecht darueber)
                elif P[j][2] >= FZ: zug[(tid, j)] = "Port " + tid
                elif lage == "start" and art == "stutzen" and any("Feinfilter" in a for a in t.get("anschluss", [])): zug[(tid, j)] = "Grube " + tid
                elif lage == "start" and art == "stutzen" and "Zentralpool" in t.get("anschluss", []): zug[(tid, j)] = "Bodenablauf " + tid   # [A] Bodenablauf im Pool: Spirale vom Becken aus
    for a in range(len(enden)):
        for b in range(a + 1, len(enden)):
            if enden[a][0][0] != enden[b][0][0] and math.dist(enden[a][1], enden[b][1]) < 1.0: kante(enden[a][0], enden[b][0], 0.0)
    return adj, zug, segs, knicke

def abstaende(adj, zug):
    d = {u: 0.0 for u in zug}; q = [(0.0, u) for u in zug]; heapq.heapify(q)
    while q:
        du, u = heapq.heappop(q)
        if du > d.get(u, 1e18): continue
        for v, L in adj.get(u, []):
            if du + L < d.get(v, 1e18): d[v] = du + L; heapq.heappush(q, (du + L, v))
    return d

def pruefen(doc, linie=None):
    """Gibt (Strecken-Verstoesse, Knick-Verstoesse, Bericht) zurueck; Strecke = (tid, i, groesster Abstand, Punkt), Knick = (tid, i, Abstand, Punkt)."""
    adj, zug, segs, knicke = netz(doc)
    d = abstaende(adj, zug)
    lin = {t["id"]: t.get("linie") for t in doc["trassen"]}
    vs, vk, rep = [], [], {"zugaenge": sorted(set(zug.values())), "strecken": [], "knicke": []}
    for tid, i, a, b, u, v in segs:
        if linie and lin[tid] != linie: continue
        if (a[2] + b[2]) / 2 >= FZ: continue
        L = math.dist(a, b); du, dv = d.get(u, 1e18), d.get(v, 1e18)
        x = min(max((dv + L - du) / 2, 0.0), L)                       # Ort des groessten Abstands auf dem Teilstueck
        m = min(du + x, dv + L - x); p = tuple(a[k] + (b[k] - a[k]) * (x / L if L else 0) for k in range(3))
        rep["strecken"].append((tid, i, round(m), [round(c) for c in p]))
        if m > MAX_STRECKE + 0.5: vs.append((tid, i, m, p))
    for tid, i, p, u in knicke:
        if linie and lin[tid] != linie: continue
        m = d.get(u, 1e18); rep["knicke"].append((tid, i, round(m), [round(c) for c in p]))
        if m > MAX_KNICK + 0.5: vk.append((tid, i, m, p))
    return vs, vk, rep

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    linie = int(sys.argv[sys.argv.index("--linie") + 1]) if "--linie" in sys.argv else None
    if linie: a = [x for x in a if x != str(linie)]
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    if a: doc = json.load(open(a[0], encoding="utf-8"))
    else:
        import leitungen; doc = leitungen.laden_variante()
    vs, vk, rep = pruefen(doc, linie)
    if "--json" in sys.argv: print(json.dumps(rep, indent=1)); sys.exit(1 if vs or vk else 0)
    print("Zugaenge %d: %s" % (len(rep["zugaenge"]), ", ".join(rep["zugaenge"])))
    print("Vergrabene Teilstuecke %d, groesster Abstand zum Zugang %d mm (Soll <= %d)" % (len(rep["strecken"]), max([s[2] for s in rep["strecken"]] or [0]), MAX_STRECKE))
    print("Vergrabene Knicke %d, groesster Abstand zum Zugang %d mm (Soll <= %d)" % (len(rep["knicke"]), max([s[2] for s in rep["knicke"]] or [0]), MAX_KNICK))
    for tid, i, m, p in vs: print("  STRECKE %s Teilstueck %d: %.0f mm bis zum Zugang, Stelle %s" % (tid, i + 1, m, [round(c) for c in p]))
    for tid, i, m, p in vk: print("  KNICK %s Punkt %d: %.0f mm bis zum Zugang, Stelle %s" % (tid, i, m, [round(c) for c in p]))
    print("Verstoesse: Strecken %d, Knicke %d" % (len(vs), len(vk)))
    sys.exit(1 if vs or vk else 0)
