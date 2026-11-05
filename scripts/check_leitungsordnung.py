"""Pruefskript Leitungsordnung v2 (docs/leitungsordnung.md, D86/W75; v1 aus M10-UMBAU Schritt 1): R1 bis R9, R11 bis R14 plus R10 Abdeckung, nur lesen.
Eingaben: data/leitungstrassen.json (Pfade, ueber leitungen.bauen() in Instanzen mit Trassen-Zuordnung umgerechnet), scripts/dome-script.json (Halter-Instanzen,
Bogen-Klassen), scripts/.segs.json (Strebenachsen), viewer/instances.json + data/bom_koerper.json (Bauteil-Kaesten fuer R9), data/leitungsnetz.json (R10).
Aufruf: python -X utf8 scripts/check_leitungsordnung.py [--json <aus.json>] [--trassen <andere Trassenliste, z. B. Vorher-Stand>] [--nur-v2]   (Exit 1 bei Verstoss in R1 bis R9, R11 bis R14)
v2: Feld "art" je Trasse (A Druck starr, B Druckschlauch, C Schwerkraft frei, D Luft, E Heber/Siphon, F Leerrohr/Kanal); ohne "art" = Bestand v1 (wie A).
Schlauch- und Leerrohr-Trassen (B, C, D, F) gehen NICHT in leitungen.bauen() (beliebige Knickwinkel) und nicht in R1 bis R5/R8; fuer sie gelten R6 (Schlauch), R9, R11 bis R14.
Messgrenzen: R7 prueft Halterhoehe (< Z 2500) und Abstand >= 150 mm zu jeder Strebenachse, nicht den Kontakt zum Befestigungsgrund;
R9 wertet Probepunkte ueber Flur (Z 400 bis 2500) als Gang, wenn sie ausserhalb von Pool, Beet-Portalen und 250 mm um jedes Bauteil liegen (Naeherung der Gangkarte)."""
import collections, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import leitungen as LG

FZ, KOPF = 400.0, 2500.0
DOC = json.load(open(sys.argv[sys.argv.index("--trassen") + 1], encoding="utf-8")) if "--trassen" in sys.argv else LG.laden_variante()   # M10-S2N: Variante filtern (geteilte Trassen haben eine ring_b2-Kopie)
FREI = ("B", "C", "D", "F")                                    # v2: frei gefuehrte Arten (Schlauch, Leerrohr)
ALLE = DOC["trassen"]
if "--nur-v2" in sys.argv: ALLE = [t for t in ALLE if t.get("art")]
V2 = [t for t in ALLE if t.get("art")]                        # R11 bis R14
DOC = dict(DOC); DOC["trassen"] = [t for t in ALLE if t.get("art") not in FREI]   # R1 bis R8 und bauen(): Art A, E und Bestand
KANTEN = json.load(open(os.path.join(ROOT, "data", "leitungsnetz.json"), encoding="utf-8"))["kanten"]
CMDS = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
MV = {c["params"]["occurrence"]: c["params"]["matrix"] for c in CMDS if c["command"] == "occurrence.move"}
SEGS = json.load(open(os.path.join(ROOT, "scripts", ".segs.json")))

def sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def nrm(a): return math.sqrt(dot(a, a))
def unit(a): n = nrm(a); return tuple(v / n for v in a)
def deg(c): return math.degrees(math.acos(max(-1.0, min(1.0, c))))
def rd(p): return [round(v) for v in p]

def korridor(tr, a, b):
    """Korridor eines Teilstuecks: Feld 'korridor' der Trasse (Liste je Segment oder ein Wert), sonst aus Linie und Hoehe abgeleitet."""
    k = tr.get("korridor")
    if isinstance(k, list): return k[tr["_i"]]
    if k: return k
    if tr.get("linie") == "luft" and min(a[2], b[2]) < FZ: return "KB"
    if abs(unit(sub(b, a))[2]) > 0.999: return "KS"
    return "KG" if max(a[2], b[2]) < FZ else "KH"

def richtung(u, kor):
    """Winkel zur naechsten erlaubten Richtung (lotrecht, Weltachsen; KW zusaetzlich 45 Grad) und Neigung gegen die Waagerechte."""
    if abs(u[2]) > math.cos(math.radians(1.0)): return 0.0, 90.0
    neig = math.degrees(math.asin(min(1.0, abs(u[2]))))
    az = math.degrees(math.atan2(u[1], u[0])); raster = 45 if kor == "KW" else 90
    return abs(((az + raster / 2) % raster) - raster / 2), neig

viol = collections.defaultdict(list); info = {}
trs = DOC["trassen"]
# ---------------- R1, R3, R4, R5 je Trasse (Pfadsegmente), Ausnahmen 1 (Heber) und 2 (schraeger Port, erstes/letztes Stueck <= 300 mm)
azs = set(); n_seg = 0
AUF = {r["id"] for r in DOC.get("r_stuecke", []) if r.get("auf_stutzen")}   # Reduziermuffe direkt auf einem Bauteil-Stutzen: zaehlt fuer Ausnahme 2 wie der Stutzen
def am_port(e): return e in ("stutzen", "muffe") or (e.startswith("r:") and e[2:] in AUF)   # "muffe": Bauteil-Muffe (M10-S5-LUFT-B)
for tr in trs:
    pts = [tuple(map(float, p)) for p in tr["pfad"]]; d = float(tr["dn"]); heber = bool(tr.get("heber"))
    L = [nrm(sub(pts[i + 1], pts[i])) for i in range(len(pts) - 1)]
    for i in range(len(pts) - 1):
        tr["_i"] = i; a, b = pts[i], pts[i + 1]; u = unit(sub(b, a)); kor = korridor(tr, a, b); n_seg += 1
        aw, ng = richtung(u, kor)
        rand = (i == 0 and am_port(tr.get("start", "stutzen"))) or (i == len(pts) - 2 and am_port(tr.get("ende", "stutzen")))
        if heber or (rand and L[i] <= 300.0 + 1e-6): continue
        if ng < 89.0 and ng <= 2.0 and aw <= 1.0:
            if ng < 2.0: azs.add(round(math.degrees(math.atan2(u[1], u[0])) / 5) * 5 % 360)
            continue
        if ng >= 89.0: continue
        viol["R1"].append("%s Teilstueck %d (%s): %.1f Grad neben der Achse, Neigung %.1f Grad, %s bis %s" % (tr["id"], i + 1, kor, aw, ng, rd(a), rd(b)))
    if heber: continue
    ecken = list(range(1, len(pts) - 1))
    for j in range(len(ecken) - 1):                           # R3 zwischen zwei Boegen
        i = ecken[j]; seg = L[i]; vert = abs(unit(sub(pts[i + 1], pts[i]))[2]) > 0.999
        if seg < max(3 * d, 100.0) and not vert: viol["R3"].append("%s: Gerade %.0f mm zwischen Boegen bei %s (Soll >= %.0f)" % (tr["id"], seg, rd(pts[i]), max(3 * d, 100.0)))
    lg = sum(L); soll = 4 + math.ceil(lg / 5000.0)
    if len(ecken) > soll: viol["R5"].append("%s: %d Boegen bei %.1f m (Soll <= %d)" % (tr["id"], len(ecken), lg / 1000, soll))
info["Pfadsegmente"] = n_seg; info["waagerechte Richtungen (5-Grad-Klassen)"] = len(azs)
if len(azs) > 8: viol["R1"].append("waagerechte Richtungen %d (Soll <= 8 Welt)" % len(azs))
# ---------------- Instanzen aus der Trassenliste (wie gen_dome sie setzt): schraege Rohre (Vergleich Inventur), R2, R6
T, _ = LG.bauen(DOC)
heber_ids = {t["id"] for t in trs if t.get("heber")}
schwan_ids = {t["id"] for t in trs if t.get("schwanenhals")}
rohre = []
for (art, d, Lr), liste in T.items.items():
    if art == "rohr":
        for m, _, tid in liste:
            z = (m[2], m[6], m[10]); A = (m[3], m[7], m[11]); rohre.append(dict(d=d, L=Lr, A=A, B=tuple(A[i] + z[i] * Lr for i in range(3)), u=z, tid=tid))
schraeg = sum(1 for r in rohre if min(deg(abs(r["u"][k])) for k in range(3)) > 3.0)
info["Rohr-Instanzen"] = len(rohre); info["Rohre schraeg > 3 Grad (wie Inventur M05)"] = schraeg
info["Boegen"] = sum(len(l) for k, l in T.items.items() if k[0].startswith("bogen"))
bad = [k for k in T.items if k[0].startswith("bogen") and k[0] not in ("bogen90", "bogen45")]
bad += sorted({c["params"]["name"] for c in CMDS if c["command"] == "component.insert_design" and c["params"].get("name", "").startswith("LT_Bogen") and not c["params"]["name"].startswith(("LT_Bogen90", "LT_Bogen45"))})
for k in bad: viol["R2"].append("Bogenklasse %s" % (k,))
# R4 Bogenkette wie die Inventur (renders/maengel/inventur.py): Bauteile Bogen, Rohr <= 300 mm, Kupplung, Reduzierung; verbunden, wenn Anschlusspunkte <= Muffentiefe t (kleinerer Durchmesser) + 10 mm (Rohr steckt t in der Muffe); >= 3 Boegen je Verbund
glied = []
for (art, d, Lr), liste in T.items.items():
    for m, _, tid in liste:
        z = (m[2], m[6], m[10]); x = (m[0], m[4], m[8]); o = (m[3], m[7], m[11])
        if art.startswith("bogen"):
            k = LG.tangent(art, d); c = tuple(o[i] + z[i] * k for i in range(3))
            dout = x if art == "bogen90" else unit(tuple(z[i] + x[i] for i in range(3)))
            glied.append((True, [o, tuple(c[i] + dout[i] * k for i in range(3))], tid, d))
        elif art == "rohr" and Lr <= 300 or art in ("kupplung", "reduzierung"):
            ln = Lr if art == "rohr" else LG.LT.ports("lt_kupplung_d%d" % d if art == "kupplung" else "lt_reduzierung_d%d_d%d" % (d, Lr))[1][1][2]
            glied.append((False, [o, tuple(o[i] + z[i] * ln for i in range(3))], tid, d))
grp = list(range(len(glied)))
def wurzel(i):
    while grp[i] != i: grp[i] = grp[grp[i]]; i = grp[i]
    return i
for i in range(len(glied)):
    for j in range(i + 1, len(glied)):
        if any(nrm(sub(p, q)) <= 10.0 + LG.LT.DEPTH[min(glied[i][3], glied[j][3])] for p in glied[i][1] for q in glied[j][1]): grp[wurzel(i)] = wurzel(j)
verb = collections.defaultdict(list)
for i, g in enumerate(glied): verb[wurzel(i)].append(g)
for v in verb.values():
    b = [g for g in v if g[0]]
    if len(b) >= 3 and not all(g[2] in heber_ids for g in b) and not all(g[2] in schwan_ids for g in b):   # Ausnahme 5: Schwanenhals ueber einen Beckenrand (Feld "schwanenhals")
        viol["R4"].append("%d Boegen (%s) bei %s" % (len(b), ", ".join(sorted({g[2] for g in b})), rd(b[0][1][0])))
# R6 Halter: Instanzen LT_Klemme*/LT_Schelle* im Modell
halter = [(n, (m[3], m[7], m[11])) for n, m in MV.items() if n.split(":")[0].startswith(("LT_Klemme", "LT_Schelle", "LT_Schlauchschelle"))]
info["Halter-Instanzen"] = len(halter)
def abst(d): return 600.0 if d <= 32 else 800.0 if d <= 63 else 1000.0
luecken = 0
for r in rohre:
    if min(r["A"][2], r["B"][2]) <= FZ: continue
    vert = abs(r["u"][2]) > 0.999; s_max = abst(r["d"]) * (1.5 if vert else 1.0)
    st = sorted(dot(sub(p, r["A"]), r["u"]) for _, p in halter if -50 <= dot(sub(p, r["A"]), r["u"]) <= r["L"] + 50
                and nrm(sub(sub(p, r["A"]), tuple(r["u"][i] * dot(sub(p, r["A"]), r["u"]) for i in range(3)))) <= r["d"] / 2 + 60)
    pkt = [0.0] + [max(0.0, min(r["L"], s)) for s in st] + [float(r["L"])]
    gap = max(pkt[i + 1] - pkt[i] for i in range(len(pkt) - 1))
    if not st and r["L"] < 300: continue                      # Kurzstueck im Formstueck-Zusammenbau (Halter am Nachbarrohr)
    if gap > s_max or not st:
        luecken += 1
        if luecken <= 40: viol["R6"].append("%s Rohr d%d L%d bei %s: Halterabstand %.0f mm (Soll <= %.0f)" % (r["tid"], r["d"], r["L"], rd(r["A"]), gap, s_max))
if luecken > 40: viol["R6"].append("... insgesamt %d Rohre ohne ausreichende Halter" % luecken)
info["Rohre ueber Flur ohne ausreichende Halter (R6)"] = luecken
# ---------------- R7 Befestigungsgrund (Naeherung): nicht ueber Kopf, nicht an Strebe
for n, p in halter:
    sd = min(nrm(sub(p, tuple(A[i] + max(0, min(1, dot(sub(p, A), sub(B, A)) / dot(sub(B, A), sub(B, A)))) * (B[i] - A[i]) for i in range(3)))) for A, B in SEGS)
    if p[2] >= KOPF or sd < 150: viol["R7"].append("%s bei %s: Z %.0f, Strebenabstand %.0f" % (n, rd(p), p[2], sd))
# ---------------- R8 Buendel: parallele waagerechte Nachbarn im selben Korridor, Achsabstand < 250 mm -> lichter Abstand 25 bis 60
segs = []
for tr in trs:
    pts = [tuple(map(float, p)) for p in tr["pfad"]]
    for i in range(len(pts) - 1):
        tr["_i"] = i; a, b = pts[i], pts[i + 1]; u = unit(sub(b, a))
        if abs(u[2]) < 0.035 and nrm(sub(b, a)) > 200: segs.append((tr["id"], tr.get("kante") or tr["id"], float(tr["dn"]), a, b, u, korridor(tr, a, b), tr.get("buendel")))
for x in range(len(segs)):
    for y in range(x + 1, len(segs)):
        s1, s2 = segs[x], segs[y]
        if s1[1] == s2[1] or s1[6] != s2[6] or abs(abs(dot(s1[5], s2[5])) - 1) > 1e-3: continue
        if s1[7] and s1[7] == s2[7]: continue                   # Ausnahme 4: Abgaenge eines Verteilers behalten dessen Teilung (Feld "buendel")
        t0, t1 = sorted((dot(sub(s2[3], s1[3]), s1[5]), dot(sub(s2[4], s1[3]), s1[5])))
        if min(t1, nrm(sub(s1[4], s1[3]))) - max(t0, 0) < 200: continue
        w = sub(s2[3], s1[3]); q = nrm(sub(w, tuple(s1[5][i] * dot(w, s1[5]) for i in range(3))))
        licht = q - s1[2] / 2 - s2[2] / 2
        if q < 250 and not (25 <= licht <= 60): viol["R8"].append("%s / %s (%s): lichter Abstand %.0f mm bei %s" % (s1[0], s2[0], s1[6], licht, rd(s1[3])))
# ---------------- R9 Gaenge (Naeherung, siehe Kopf)
try:
    inst = json.load(open(os.path.join(ROOT, "viewer", "instances.json"), encoding="utf-8"))["instances"]
    bomk = json.load(open(os.path.join(ROOT, "data", "bom_koerper.json"), encoding="utf-8"))["komponenten"]
    SKIP = ("lt_", "netztopf", "salatkopf", "huelle_", "strebe_", "knoten_", "erdflaeche", "mensch_", "fundamentring", "fundamentanker", "luft_scheibe", "tuer")
    kast = []
    for a in inst:
        b = bomk.get(a["d"])
        if a["d"].startswith(SKIP) or not b or not b["bodies"]: continue
        lo = [min(x["bbox_min"][i] for x in b["bodies"]) for i in range(3)]; hi = [max(x["bbox_max"][i] for x in b["bodies"]) for i in range(3)]
        kast.append((a["m"], lo, hi))
    def nah(p, m, lo, hi, tol):
        dd = [p[0] - m[3], p[1] - m[7], p[2] - m[11]]; q = [m[0] * dd[0] + m[4] * dd[1] + m[8] * dd[2], m[1] * dd[0] + m[5] * dd[1] + m[9] * dd[2], m[2] * dd[0] + m[6] * dd[1] + m[10] * dd[2]]
        return all(lo[i] - tol <= q[i] <= hi[i] + tol for i in range(3))
    g9 = 0
    for r in rohre:
        if max(r["A"][2], r["B"][2]) <= FZ: continue
        for k in range(1, 6):
            p = tuple(r["A"][i] + (r["B"][i] - r["A"][i]) * k / 6 for i in range(3))
            if not FZ < p[2] < KOPF or math.hypot(p[0], p[1]) < 2095 + 50: continue
            if max(p[0] * math.cos(math.radians(-72 + 36 * k)) + p[1] * math.sin(math.radians(-72 + 36 * k)) for k in range(10)) > 6000 * math.cos(math.radians(18)): continue   # R9 gilt im Dom (Zehneck, Apothem 5706); aussen kein Gang
            if not any(nah(p, m, lo, hi, 250.0) for m, lo, hi in kast):
                g9 += 1; viol["R9"].append("%s Rohr d%d bei %s frei im Gang" % (r["tid"], r["d"], rd(p))); break
    info["R9 Kaesten"] = len(kast)
except FileNotFoundError as e:
    viol["R9"].append("nicht messbar: %s" % e)
# ---------------- R9 fuer frei gefuehrte Trassen (Schlauch auf dem Flur zaehlt auch: Z ab 0 rel)
try:
    for tr in [t for t in V2 if t.get("art") in ("B", "C", "D")]:
        pts = [tuple(map(float, p)) for p in tr["pfad"]]
        for a, b in zip(pts, pts[1:]):
            hit = None
            for k in range(1, 6):
                p = tuple(a[i] + (b[i] - a[i]) * k / 6 for i in range(3))
                if not FZ - 1 <= p[2] < KOPF or math.hypot(p[0], p[1]) < 2095 + 50: continue
                if max(p[0] * math.cos(math.radians(-72 + 36 * j)) + p[1] * math.sin(math.radians(-72 + 36 * j)) for j in range(10)) > 6000 * math.cos(math.radians(18)): continue
                if not any(nah(p, m, lo, hi, 250.0) for m, lo, hi in kast): hit = p; break
            if hit: viol["R9"].append("%s (Art %s) bei %s frei im Gang" % (tr["id"], tr["art"], rd(hit))); break
except NameError:
    pass
# ---------------- R11 Gefaelle, R12 Hochpunkt, R13 Vergraben mit Grund, R14 Schlauchbiegung (v2, nur Trassen mit "art")
unter_m = 0.0
for tr in ALLE:                                               # Summe unter Flur (alle Trassen, Info)
    pts = [tuple(map(float, p)) for p in tr["pfad"]]
    unter_m += sum(nrm(sub(b, a)) for a, b in zip(pts, pts[1:]) if (a[2] + b[2]) / 2 < FZ) / 1000.0
info["R13 Summe unter Flur (alle Trassen) m"] = round(unter_m, 1)
info["v2-Trassen (Feld art)"] = len(V2)
for tr in V2:
    pts = [tuple(map(float, p)) for p in tr["pfad"]]; d = float(tr["dn"]); art = tr["art"]
    if art == "C":
        smin = 0.005 if d >= 75 else 0.01
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            lh = math.hypot(b[0] - a[0], b[1] - a[1])
            if lh < 1.0:
                if b[2] > a[2] + 0.5: viol["R11"].append("%s Teilstueck %d steigt senkrecht um %.0f mm" % (tr["id"], i + 1, b[2] - a[2]))
                continue
            g = (a[2] - b[2]) / lh
            if g < smin - 1e-9: viol["R11"].append("%s Teilstueck %d: Gefaelle %.2f %% (Soll >= %.1f %%) bei %s" % (tr["id"], i + 1, 100 * g, 100 * smin, rd(a)))
        top = max(p[2] for p in pts[1:])
        if top > pts[0][2] + 0.5: viol["R12"].append("%s: Hochpunkt Z %.0f ueber Start Z %.0f (Art C darf nicht steigen)" % (tr["id"], top, pts[0][2]))
    if art in ("C", "E") and tr.get("quelle_spiegel") is not None:
        top = max(p[2] for p in pts)
        if top > float(tr["quelle_spiegel"]) and tr.get("siphon") not in ("entlueftet", "anfahrhilfe"):
            viol["R12"].append("%s: steigt auf Z %.0f ueber den Quellspiegel Z %.0f ohne Feld siphon" % (tr["id"], top, float(tr["quelle_spiegel"])))
    for i, (a, b) in enumerate(zip(pts, pts[1:])):
        L = nrm(sub(b, a))
        if (a[2] + b[2]) / 2 < FZ:
            if art != "F" and tr.get("grund") not in ("gangquerung", "pool_einmuendung", "unter_wasserspiegel"):
                viol["R13"].append("%s Teilstueck %d (Art %s) unter Flur ohne Grund bei %s" % (tr["id"], i + 1, art, rd(a)))
            if L > 3000 and not tr.get("kanal"):
                viol["R13"].append("%s Teilstueck %d: %.1f m unter Flur ohne Zugang (Soll <= 3 m oder Feld kanal)" % (tr["id"], i + 1, L / 1000))
    if art in ("B", "C", "D"):
        r = 6.0 * d                                       # Planwert 6 x d: Spiralschlauch 40 mm 260, 51 mm 270 mm Biegeradius (esska), R57 Abschn. 7
        for i in range(1, len(pts) - 1):
            u1 = unit(sub(pts[i], pts[i - 1])); u2 = unit(sub(pts[i + 1], pts[i]))
            w = deg(dot(u1, u2))
            if w < 1.0: continue
            t = r * math.tan(math.radians(w) / 2)
            l1, l2 = nrm(sub(pts[i], pts[i - 1])), nrm(sub(pts[i + 1], pts[i]))
            if t > min(l1 if i == 1 else l1 / 2, l2 if i == len(pts) - 2 else l2 / 2) + 1e-6:
                viol["R14"].append("%s Ecke %d: Knick %.0f Grad braucht %.0f mm Gerade (Radius %.0f), vorhanden %.0f" % (tr["id"], i, w, t, r, min(l1, l2)))
    if art in ("B", "C", "D") and not tr.get("aufliegend"):  # R6 fuer Schlauch: Schlauchschellen <= 400 mm
        hs = [p for n, p in halter if n.startswith("LT_Schlauchschelle")]
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            if min(a[2], b[2]) <= FZ: continue
            L = nrm(sub(b, a)); u = unit(sub(b, a))
            st = sorted(dot(sub(p, a), u) for p in hs if -50 <= dot(sub(p, a), u) <= L + 50 and nrm(sub(sub(p, a), tuple(u[k] * dot(sub(p, a), u) for k in range(3)))) <= d / 2 + 60)
            pk = [0.0] + [max(0.0, min(L, x)) for x in st] + [L]
            gap = max(pk[k + 1] - pk[k] for k in range(len(pk) - 1))
            if gap > 400:
                luecken += 1; viol["R6"].append("%s Schlauch Teilstueck %d: Schellenabstand %.0f mm (Soll <= 400 oder Feld aufliegend)" % (tr["id"], i + 1, gap))
info["Rohre ueber Flur ohne ausreichende Halter (R6)"] = luecken
# ---------------- R10 Abdeckung (Info, kein Exit)
gebaut = {t.get("kante") for t in ALLE if t.get("kante")} | {t["id"].split("-")[0] for t in ALLE}
ohne = [k["id"] for k in KANTEN if k["id"] not in gebaut]
info["R10 Netz-Kanten ohne Trasse"] = "%d: %s" % (len(ohne), ", ".join(ohne))

print("Leitungsordnung (docs/leitungsordnung.md) | Trassen %d" % len(trs))
for k, v in info.items(): print("  %s: %s" % (k, v))
fehler = 0
for r in ("R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9", "R11", "R12", "R13", "R14"):
    v = viol.get(r, []); n = len(v) if r != "R6" else luecken; fehler += n
    print("%s %s: %d Verstoesse" % ("PASS" if not n else "FAIL", r, n))
    for z in v[:12]: print("    " + z)
    if len(v) > 12: print("    ... %d weitere" % (len(v) - 12))
if "--json" in sys.argv:
    json.dump({"info": info, "verstoesse": {k: v for k, v in viol.items()}, "r6_luecken": luecken, "r10_ohne": ohne}, open(sys.argv[sys.argv.index("--json") + 1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(1 if fehler else 0)
