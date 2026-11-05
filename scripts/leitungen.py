"""M10-S2a: Leitungsbau. Aus der Trassenliste data/leitungstrassen.json (Format: scripts/check_leitungen.py) werden Instanzen der Bibliothek
designs/components/lt_*.sc (Rohr, Bogen 90/45, T, Reduziermuffe, Kupplung) berechnet; gen_dome.leitungen() setzt sie in die Assembly 08_Leitungen.
Rohre gibt es in der Bibliothek nur zu 1000 mm und eine Instanz darf nicht skaliert werden: jede gebrauchte Laenge wird einmal mit dem Generator der Bibliothek
(scripts/workshop/leitung.rohr(d, L), gleicher Querschnitt, gleiche Wand) als lt_rohr_d<d>_L<mm>.sc neben die Bibliothek gelegt.

Konvention der Bibliothek (docs/parts/leitungsteile.md): Port A im Ursprung, Oeffnung -Z; Rohr ist ein Zapfen (wird je t in die Muffe gesteckt), Bogen/T/Reduzierung/Kupplung sind Muffen.
Trassenpunkte sind Kreuzungspunkte der Achsen. Bogen: Schenkel k = Abstand Kreuzungspunkt - Muffenebene (aus leitung.ports()); Rohr zwischen zwei Muffen: Laenge = Abstand - k1 - k2 + 2 t.
Stutzenspitze ("stutzen"): Zapfen des Bauteils (Pool, Filter, Pumpe), das Rohrnetz steckt darauf: ein Bogen sitzt direkt auf dem Stutzen, wenn der Kreuzungspunkt R = k - t von der Spitze entfernt liegt,
sonst steckt eine Kupplung auf dem Stutzen und das Rohr in der Kupplung (Rohrende 6 mm von der Spitze).
T-Stueck ("t:<id>", M10-S2b allgemein): T der Groesse d + je Port mit kleinerem Rohr ein Rohrstueck d (2 t) + Reduziermuffe d/d_klein; die Muffen von T und Reduziermuffe passen nicht Muffe auf Muffe.
  Eintrag in "t_stuecke": {"id", "pos", "d", "ports": [{"trasse", "ende": "start"|"ende", "d"}, ...]}; zwei Ports muessen auf einer Geraden liegen, der dritte steht senkrecht (beliebige Richtung, auch senkrecht).
Reduziermuffe ("r:<id>", M10-S2b): Eintrag in "r_stuecke": {"id", "pos_a", "dir", "d_gross", "d_klein"}; pos_a = Muffenebene A (grosse Seite), dir von A nach B; die Trasse beginnt/endet auf der Muffenebene B.
  Mit "art": "kugelhahn" steht derselbe Eintrag fuer einen Kugelhahn (lt_kugelhahn_d<d_gross>, Doppelmuffe, Laenge aus der Bibliothek); die Trassen davor/dahinter enden/beginnen auf den Muffenebenen A/B.
Offenes Ende ("offen"): das Rohr endet am Trassenpunkt, kein Fitting."""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import leitung as LT

TRASSEN = os.path.join(ROOT, "data", "leitungstrassen.json")
COMP = os.path.join(ROOT, "designs", "components")
FARBEN = {"dunkelblau": "#2a5da8", "hellblau": "#7fc4ea", "grau": "#8d9296", "gruen": "#4c9a5a"}   # Plan 4 Regel 8: Filterlinie dunkelblau, Frischwasser hellblau, Ruecklauf grau
TOL = 0.6   # mm, Passung "Bogen direkt auf dem Stutzen"

def laden():
    return json.load(open(TRASSEN, encoding="utf-8")) if os.path.exists(TRASSEN) else None

def add(a, b, s=1.0): return tuple(a[i] + s * b[i] for i in range(3))
def sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def nrm(a): return math.sqrt(dot(a, a))
def unit(a): n = nrm(a); return tuple(v / n for v in a)

def tangent(kind, d):
    """Schenkel k: Abstand vom Kreuzungspunkt der Achsen bis zur Muffenebene (Port A bzw. B)."""
    B = LT.ports("lt_%s_d%d" % (kind, d))[1]
    if kind == "bogen90": return B[1][0]
    s = B[1][0] / B[2][0]                                  # Bogen 45: Gerade ab B zurueck bis x = 0 (Achse von A)
    return B[1][2] - s * B[2][2]

class Teile:
    """Sammelt Instanzen je Bibliotheksteil: key (art, d, L) -> Liste (Matrix, Farbe, Trasse)."""
    def __init__(self): self.items = {}
    def put(self, art, d, L, origin, zc, xhint, farbe, tid):
        zc = unit(zc)
        xc = tuple(xhint[i] - dot(xhint, zc) * zc[i] for i in range(3))
        if nrm(xc) < 1e-6: xc = cross(zc, (0.0, 0.0, 1.0) if abs(zc[2]) < 0.9 else (1.0, 0.0, 0.0))
        xc = unit(xc); yc = cross(zc, xc)
        m = [round(v, 9) for v in (xc[0], yc[0], zc[0], origin[0], xc[1], yc[1], zc[1], origin[1], xc[2], yc[2], zc[2], origin[2])]
        m[3], m[7], m[11] = round(origin[0], 2), round(origin[1], 2), round(origin[2], 2)
        self.items.setdefault((art, d, L), []).append((m, farbe, tid))

def rohr(T, p0, p1, d, farbe, tid):
    v = sub(p1, p0); L = nrm(v)
    if L < 1.0: raise SystemExit("%s: Rohr d%d mit Laenge %.1f" % (tid, d, L))
    T.put("rohr", d, int(round(L)), p0, v, (1.0, 0.0, 0.0), farbe, tid)

def bogen(T, corner, din, dout, d, farbe, tid):
    ang = math.degrees(math.acos(max(-1.0, min(1.0, dot(din, dout)))))
    art = "bogen90" if abs(ang - 90) < 1.0 else "bogen45" if abs(ang - 45) < 1.0 else None
    if not art: raise SystemExit("%s: Knick von %.1f Grad bei %s: die Bibliothek hat nur 45 und 90" % (tid, ang, [round(v) for v in corner]))
    k = tangent(art, d)
    T.put(art, d, 0, add(corner, din, -k), din, dout, farbe, tid)
    return k

def t_stueck(T, ts, doc, farbe):
    """T der Groesse ts["d"] an ts["pos"] mit den Ports aus ts["ports"]; Ports mit kleinerem Rohr bekommen Rohrstueck (2 t) + Reduziermuffe. Gibt {d_port: Schenkel k} zurueck (Abstand T-Mitte -> Muffenebene des Rohrs)."""
    tid = ts["id"]; t0 = tuple(ts["pos"]); d1 = int(ts["d"]); tr = {t["id"]: t for t in doc["trassen"]}
    dirs = []
    for p in ts["ports"]:
        pf = tr[p["trasse"]]["pfad"]
        dirs.append(unit(sub(tuple(pf[-2] if p["ende"] == "ende" else pf[1]), t0)))   # Richtung von der T-Mitte entlang des Rohrs
    paar = [(i, j) for i in range(3) for j in range(i + 1, 3) if abs(dot(dirs[i], dirs[j]) + 1) < 1e-3]
    if len(paar) != 1: raise SystemExit("%s: zwei Ports muessen gegenueber liegen, der dritte senkrecht (Richtungen %s)" % (tid, [[round(v, 3) for v in d] for d in dirs]))
    k = [x for x in range(3) if x not in paar[0]][0]
    if abs(dot(dirs[k], dirs[paar[0][0]])) > 1e-3: raise SystemExit("%s: dritter Port steht nicht senkrecht zur Geraden" % tid)
    T.put("t", d1, 0, t0, dirs[k], dirs[paar[0][0]], farbe, tid)
    a = LT.ports("lt_t_d%d" % d1)[0][1][0] * -1.0; t1 = LT.DEPTH[d1]; ks = {}
    for p, v in zip(ts["ports"], dirs):
        dp = int(p["d"])
        if dp == d1: ks[dp] = a; continue
        lred = LT.ports("lt_reduzierung_d%d_d%d" % (d1, dp))[1][1][2]
        T.put("rohr", d1, int(round(2 * t1)), add(t0, v, a - t1), v, (1.0, 0.0, 0.0), farbe, tid)
        T.put("reduzierung", d1, dp, add(t0, v, a), v, (1.0, 0.0, 0.0), farbe, tid)
        ks[dp] = a + lred
    return ks

def bauen(doc):
    """Rechnet alle Trassen in Instanzen um; gibt (Teile, Bericht) zurueck. Bricht mit SystemExit ab, wenn ein Knick oder ein Abstand nicht zur Bibliothek passt."""
    T = Teile(); bericht = []
    tk = {}
    for ts in doc.get("t_stuecke", []): tk[ts["id"]] = t_stueck(T, ts, doc, FARBEN[[t for t in doc["trassen"] if t["id"] == ts["ports"][0]["trasse"]][0].get("farbe", "dunkelblau")])
    for r in doc.get("r_stuecke", []):
        if r.get("art") == "kugelhahn": T.put("kugelhahn", int(r["d_gross"]), 0, tuple(r["pos_a"]), tuple(r["dir"]), (1.0, 0.0, 0.0), FARBEN[r.get("farbe", "dunkelblau")], r["id"])   # Doppelmuffe L = 50 + 2 t
        else: T.put("reduzierung", int(r["d_gross"]), int(r["d_klein"]), tuple(r["pos_a"]), tuple(r["dir"]), (1.0, 0.0, 0.0), FARBEN[r.get("farbe", "dunkelblau")], r["id"])
    for tr in doc["trassen"]:
        tid, d, farbe = tr["id"], int(tr["dn"]), FARBEN[tr.get("farbe", "dunkelblau")]
        pts = [tuple(float(v) for v in p) for p in tr["pfad"]]; n = len(pts)
        dirs = [unit(sub(pts[i + 1], pts[i])) for i in range(n - 1)]; D = [nrm(sub(pts[i + 1], pts[i])) for i in range(n - 1)]
        t = LT.DEPTH[d]
        ks, ke = [0.0] * (n - 1), [0.0] * (n - 1)
        for j in range(1, n - 1):
            k = bogen(T, pts[j], dirs[j - 1], dirs[j], d, farbe, tid); ke[j - 1] = k; ks[j] = k
        start, ende = tr.get("start", "stutzen"), tr.get("ende", "stutzen")
        if start.startswith("t:"): ks[0] = tk[start[2:]][d]
        if ende.startswith("t:"): ke[-1] = tk[ende[2:]][d]
        s0 = [ks[i] - t for i in range(n - 1)]; s1 = [D[i] - ke[i] + t for i in range(n - 1)]   # Rohr von s0 bis s1 entlang des Teilstuecks (ab Anfangspunkt)
        if start == "offen": s0[0] = 0.0                              # offenes Ende: Rohr endet am Trassenpunkt
        if ende == "offen": s1[-1] = D[-1]
        kein = set()                                                  # Teilstuecke ohne Rohr: Bogen sitzt direkt auf dem Stutzen
        for lage, tipp, o, i in (("start", pts[0], dirs[0], 0), ("ende", pts[-1], dirs[-1], n - 2)):
            if (start if lage == "start" else ende) != "stutzen": continue
            g = D[i] - (ke[i] if lage == "start" else ks[i])        # Abstand Stutzenspitze - Muffenebene des naechsten Fittings (negativ = ueberlappt)
            if abs(g + t) <= TOL: kein.add(i); continue              # Bogen direkt auf dem Stutzen
            if g < t + 6: raise SystemExit("%s: %s-Stutzen: Abstand %.1f passt weder direkt (%.1f) noch mit Kupplung (>= %.1f)" % (tid, lage, g, -t, t + 6))
            lk = LT.ports("lt_kupplung_d%d" % d)[1][1][2]
            if lage == "start": T.put("kupplung", d, 0, add(tipp, o, -t), o, (1.0, 0.0, 0.0), farbe, tid); s0[i] = 6.0
            else: T.put("kupplung", d, 0, add(tipp, o, -(lk - t)), o, (1.0, 0.0, 0.0), farbe, tid); s1[i] = D[i] - 6.0
        for i in range(n - 1):
            if i in kein: continue
            if s1[i] - s0[i] < t: raise SystemExit("%s: Teilstueck %d: Fittings ueberlappen (Rohr %.1f mm, Teilstueck %.1f, Schenkel %.1f + %.1f)" % (tid, i + 1, s1[i] - s0[i], D[i], ks[i], ke[i]))
            rohr(T, add(pts[i], dirs[i], s0[i]), add(pts[i], dirs[i], s1[i]), d, farbe, tid)
        bericht.append((tid, d, n - 1))
    for e in doc.get("teile", []):                                    # M10-UMBAU: weitere Bauteile ohne Trasse (Schlammfass, Federhahn, Verteiler, Kappen, Klemmen von Hand)
        kl = e["datei"].startswith("lt_klemme_d")                    # Klemmen von Hand teilen die Klasse mit den Klemmen aus halter() (eine Definition je Durchmesser)
        T.put("klemme" if kl else "teil:" + e["datei"], int(e["datei"][11:]) if kl else 0, 0, tuple(e["pos"]), tuple(e["z"]), tuple(e.get("x", (1.0, 0.0, 0.0))), FARBEN.get(e.get("farbe")), e["id"])
    if not doc.get("halter_aus"): halter(T, bericht)
    return T, bericht

def abst_halter(d): return 600.0 if d <= 32 else 800.0 if d <= 63 else 1000.0   # docs/leitungsordnung.md R6 [A]

def halter(T, bericht):
    """M10-UMBAU Schritt 9 (R6): je Rohr ueber Flur (beide Enden Z > 400) Rohrklemmen lt_klemme_d<d> in gleichen Abstaenden, Abstand <= R6 (senkrecht x 1,5); Rohre < 300 mm
    gelten als Formstueck-Zusammenbau (Halter am Nachbarrohr). Waagerechte Rohre: Klemmenfuss unten (Konsole/Boden); senkrechte: Fuss in -X (Wand/Tafel) [A].
    Fehlt die Klemme fuer den Durchmesser (d75), steht das Rohr im Bericht als OFFEN (Werkstatt: Halter)."""
    neu = []
    for (art, d, L), liste in list(T.items.items()):
        if art != "rohr" or L < 300: continue
        for m, farbe, tid in liste:
            z = (m[2], m[6], m[10]); A = (m[3], m[7], m[11]); B = add(A, z, L)
            if min(A[2], B[2]) <= 400.0: continue
            vert = abs(z[2]) > 0.999; smax = abst_halter(d) * (1.5 if vert else 1.0)
            k = max(1, int(math.ceil(L / smax - 1.0 - 1e-9)))
            if not os.path.exists(os.path.join(COMP, "lt_klemme_d%d.sc" % d)):
                bericht.append(("OFFEN (Werkstatt: Halter) lt_klemme_d%d fuer %s" % (d, tid), d, k)); continue
            fuss = (-1.0, 0.0, 0.0) if vert else (0.0, 0.0, -1.0)
            for i in range(1, k + 1):
                p = add(A, z, L * i / (k + 1))
                neu.append((d, add(p, fuss, 4.0 + (d + 6) / 2.0), tuple(-v for v in fuss), z, farbe, tid))
    for d, o, zc, xc, farbe, tid in neu:
        T.put("klemme", d, 0, o, zc, xc, FARBEN["grau"], tid)

def klasse(fname):
    """Klassenname fuer ein Bauteil aus designs/components: lt_kugelhahn_feder_d40 -> LT_Kugelhahn_Feder_d40, schlammfass -> Schlammfass."""
    t = fname.split("_")
    return "LT_" + "_".join(x if x[:1] == "d" and x[1:2].isdigit() else x.capitalize() for x in t[1:]) if t[0] == "lt" else "_".join(x.capitalize() for x in t)

def dateien(T):
    """(Klassenname, Dateipfad, [Matrizen], {Farbe: [Instanzindizes]}) je Bibliotheksteil; legt fehlende Rohr-Laengen an."""
    out = []
    for (art, d, L), liste in sorted(T.items.items()):
        if art == "rohr":
            fname = "lt_rohr_d%d_L%d" % (d, L)
            if not os.path.exists(os.path.join(COMP, fname + ".sc")):
                b, nm = LT.rohr(d, L); LT.save(b, nm, fname)
            cls = "LT_Rohr_d%d_L%d" % (d, L)
        elif art.startswith("teil:"):
            fname = art[5:]; cls = klasse(fname)
        elif art == "klemme":
            fname = "lt_klemme_d%d" % d; cls = "LT_Klemme_d%d" % d
        elif art == "reduzierung":
            fname = "lt_reduzierung_d%d_d%d" % (d, L); cls = "LT_Reduzierung_d%d_d%d" % (d, L)
        else:
            fname = "lt_%s_d%d" % (art, d); cls = "LT_%s_d%d" % (art.capitalize(), d)
        farben = {}
        for i, (m, f, tid) in enumerate(liste, 1): farben.setdefault(f, []).append("%s:%d" % (cls, i))
        out.append((cls, os.path.join(COMP, fname + ".sc"), [m for m, _, _ in liste], farben))
    return out

def _graben_trassen(trs):
    """M10-S2c: Linie-2-Trassen derselben Netzkante, die lueckenlos aneinander anschliessen (T-Teilungen K17 / K17-m / K17-b), werden fuer die Grabenschnitte wieder zu einer Trasse; gerade Zwischenpunkte entfallen.
    Aneinandergereihte gleichbreite Kaesten mit deckungsgleichen Seiten- und Bodenflaechen liessen den Boolean-Schnitt (Erdflaeche) mit einem querenden Graben scheitern. Linie 1 bleibt unveraendert."""
    out = []
    for tr in trs:
        if tr.get("linie", 1) not in (1, 2):   # M10-UMBAU: Linie 1 wie Linie 2 (neue Grabenlagen schnitten sonst deckungsgleich, Build Runde 71)
            out.append(tr); continue
        v = out[-1] if out else None
        if v and v.get("linie", 1) == tr.get("linie", 1) and tr.get("kante") and v.get("kante") == tr["kante"] and v["dn"] == tr["dn"] and math.dist(v["pfad"][-1], tr["pfad"][0]) < 0.6:
            out[-1] = dict(v, pfad=[list(p) for p in v["pfad"]] + [list(p) for p in tr["pfad"][1:]])
        else: out.append(dict(tr, pfad=[list(p) for p in tr["pfad"]]))
    for tr in out:
        if tr.get("linie", 1) not in (1, 2): continue
        pf = tr["pfad"]; keep = [pf[0]]
        for i in range(1, len(pf) - 1):
            a, b, c = keep[-1], pf[i], pf[i + 1]
            u, w = sub(b, a), sub(c, b); k = cross(u, w)
            if nrm(k) <= 3e-3 * nrm(u) * nrm(w) and dot(u, w) > 0: continue
            keep.append(b)
        keep.append(pf[-1]); tr["pfad"] = keep
    return out

def graben(doc, fz):
    """Grabenschnitte fuer alle Teilstuecke unterhalb des Flurs: [("box", name, cx, cy, z0, az_grad, laenge, breite, hoehe)] und [("zyl", name, x, y, z0, durchm, hoehe)] (z absolut, bis fz + 1)."""
    zus = 160.0; out = []
    try:
        zus = float(json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8"))["lt_graben_zuschlag"]["value"])
    except (OSError, KeyError): pass
    k2 = {}
    for tr in _graben_trassen(doc["trassen"]):
        if tr.get("linie") == "luft": continue                      # M10-S5-LUFT: Luftrohre liegen im Becken (kein Graben in der Erde)
        d = float(tr["dn"]); w = d + zus; pts = [tuple(float(v) for v in p) for p in tr["pfad"]]
        ex = 1.0                                                    # M10-UMBAU: auch Linie 1 (vorher 0)               # M10-S2c: Linie 2 je Ende 1 mm laenger: an 90-Grad-Ecken und Steigleitungen fiel sonst die Stirnflaeche in die Seitenflaeche des Nachbarn (Boolean-Schnitt ohne Ergebnis)
        if ex:                                                      # Linie 2: je Netzkante (Teilstuecke derselben Kante teilen die Breite, wie koaxiale Steigleitungen) eine eigene Breite, +0,4 mm je Kante: sonst deckungsgleiche Seiten- und Bodenflaechen verschiedener Nachbarn
            w += 0.4 * k2.setdefault(tr.get("kante") or tr["id"], len(k2) + 1)
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]
            if min(a[2], b[2]) >= fz - 1.0: continue
            name = "T10_Graben_%s_%d" % (tr["id"].replace("-", "_"), i + 1)
            dxy = math.hypot(b[0] - a[0], b[1] - a[1])
            if dxy < 20.0:                                              # Steigleitung
                z0 = min(a[2], b[2]) - w / 2
                ent = ("zyl", name, round(a[0], 1), round(a[1], 1), round(z0, 1), round(w + 2 * ex, 1), round(fz + 1 - z0, 1))
                if ex:                                                  # Linie 2: koaxiale Steigleitungen gleichen Durchmessers (Abzweig und Kugelhahn-Zug) nur einmal, der tiefste Schacht enthaelt den flacheren
                    vor = [e for e in out if e[0] == "zyl" and e[2:4] == ent[2:4] and e[5] == ent[5]]
                    if vor:
                        if ent[4] < vor[0][4]: out[out.index(vor[0])] = ent
                        continue
                out.append(ent)
            else:
                z = (a[2] + b[2]) / 2; z0 = min(a[2], b[2]) - w / 2
                out.append(("box", name, round((a[0] + b[0]) / 2, 1), round((a[1] + b[1]) / 2, 1), round(z0, 1), round(math.degrees(math.atan2(b[1] - a[1], b[0] - a[0])), 3), round(dxy + w + 2 * ex, 1), round(w, 1), round(fz + 1 - z0, 1)))
    for g in doc.get("gruben", []):                                   # M10-UMBAU Schritt 5: Grube Schlammfass (Zylinder bis Flur + 1)
        out.append(("zyl", "T93_Grube_%s" % g["id"].replace("-", "_"), round(g["x"], 1), round(g["y"], 1), round(g["sohle"], 1), round(g["d"], 1), round(fz + 1 - g["sohle"], 1)))
    return out

if __name__ == "__main__":
    doc = laden()
    if not doc: raise SystemExit("keine Trassenliste")
    T, bericht = bauen(doc)
    for art_d_l, liste in sorted(T.items.items()): print(art_d_l, len(liste))
    print("Rohre %d, Bogen %d, T %d, Reduzierungen %d, Kupplungen %d" % tuple(sum(len(l) for k, l in T.items.items() if k[0] == a) for a in ("rohr", "bogen90", "t", "reduzierung", "kupplung")), "Bogen45", sum(len(l) for k, l in T.items.items() if k[0] == "bogen45"))
    for g in graben(doc, 400.0): print(g)
