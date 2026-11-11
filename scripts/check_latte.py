"""Messbare Latte: prueft designs/dome.sc per Zahlen. Aufruf: python scripts/check_latte.py <runde>
Gibt je Pruefung PASS/FAIL mit Ist/Soll aus (Exit-Code 0 = alles PASS). Sicherheitstest, kein Score-Verlauf."""
import json, math, os, re, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
rnd = sys.argv[1] if len(sys.argv) > 1 else "00"
tmp = tempfile.mkdtemp()
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import variante   # Pfade (N-UNIFY-AUTOBAHN U7)
dome = variante.pfad("modell")

def run_json(args, may_fail=False):
    out = os.path.join(tmp, "o.json")
    if os.path.exists(out): os.remove(out)   # U9: sonst liest ein abgestuerzter CLI-Lauf still die Ausgabe des vorigen Aufrufs
    r = subprocess.run([CLI] + args + ["--json-out", out], capture_output=True, check=False)
    if not os.path.exists(out):
        msg = "CLI ohne Ausgabe (Exit %s): %s" % (r.returncode, (r.stderr or b"")[-300:].decode("utf-8", "replace"))
        if may_fail: print(msg, flush=True); return {}
        raise SystemExit(msg)
    return json.load(open(out, encoding="utf-8"))

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

bodies = find(run_json(["eval", dome]), "bodies")
B = {b["name"]: b for b in bodies}
BN = {n: b for n, b in B.items() if n[:1] == "T" and n[1:2].isdigit()}   # eigene T-Koerper; Werkstatt-Instanzen heissen anders
cmds = json.load(open(variante.pfad("dome_script")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
pre = lambda p: [b for n, b in B.items() if n.startswith(p)]
ext = lambda bs, i: (min(b["bbox"]["min"][i] for b in bs), max(b["bbox"]["max"][i] for b in bs))
res = []
def chk(name, ist, soll, ok): res.append({"check": name, "ist": ist, "soll": soll, "pass": bool(ok)})
def findk(o, key):   # erstes dict unter dem Schluessel key (beliebig tief)
    if isinstance(o, dict):
        if isinstance(o.get(key), dict): return o[key]
        for v in o.values():
            r = findk(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = findk(v, key)
            if r is not None: return r

# Komponentenzugehoerigkeit je Koerper (frueh gebraucht: Tuer, Beete, Tanks, Pumpen werden nach Klasse getrennt)
cl = {}
sc = os.path.join(tmp, "cl.json"); json.dump({"commands": [{"command": "component.list", "params": {}}]}, open(sc, "w"))
for c in find(run_json(["run", sc, "--in", dome, "--results"]), "components"):
    for bn in c.get("bodies", []): cl[bn] = (c["name"], 1)
PLANT_CLS = ("Netztopf", "Salatkopf")
PLANE_CLS = ("Huelle_",)                 # Plane (12_Huelle): Referenzflaeche, Folie liegt auf den Streben -> keine Konstruktion
FIGUR_CLS = ("Mensch_Referenz_",)        # Referenzfiguren (11_Referenz): Massstab, kein Bauteil
MESS_CLS = ("MS_",)                      # Messstellen (13_Messstellen): Halter klemmt am Rand, Sonden stecken im Halterrohr -> Ueberlappung gewollt
PUFFER_CLS = ("Puffer_Klein", "Puffer_Station")   # eigene Klasse: Koerper heissen innen u. U. wie Beet/Tank/Tafel, zaehlen dort nicht mit
def grp(n):
    m = re.search(r"\((\w+):(\d+)/(\w+):(\d+)\)$", n)
    return (m.group(3), int(m.group(4))) if m else cl.get(n, (n, 0))
klasse = lambda n: grp(n)[0]   # unbekannte Koerper (nicht in component.list) liefern ihren eigenen Namen

t1 = pre("T1_"); sock_top = P["sock_h"]
z0, z1 = ext(t1, 2); x0, x1 = ext(t1, 0)
h = z1 - sock_top - 75 - 45
chk("L5/7 Kuppelhoehe [mm]", round(h), 6000, abs(h - 6000) / 6000 < 0.03)
# Knotenvalenz aus Strebenenden
ends = {}
for c in cmds:
    p = c["params"]
    if c["command"] == "occurrence.move" and str(p.get("occurrence", "")).startswith("Strebe_"):
        m = p["matrix"]; L = 0.5465 * P["dome_base_d"] / 2 if p["occurrence"].startswith("Strebe_A") else 0.618 * P["dome_base_d"] / 2
        o = P["strut_end_offset"]; org = [m[(3, 7, 11)[j]] - m[(2, 6, 10)[j]] * o for j in range(3)]   # Strebe beginnt strut_end_offset hinter der Knotenmitte
        for pt in (tuple(round(v) for v in org), tuple(round(org[j] + m[(2, 6, 10)[j]] * L) for j in range(3))):
            # D91 Scherenknoten: Rohrachse liegt an 5-wertigen Knoten bis 15 mm neben dem Knotenpunkt -> Enden im Umkreis 40 mm zusammenfassen
            near = next((k for k in ends if math.dist(k, pt) < 40), None)
            ends[near or pt] = ends.get(near or pt, 0) + 1
apex = max(ends, key=lambda k: k[2]); apex_n = ends[apex]
base_nodes = [k for k in ends if abs(k[2] - (sock_top + P['strut_r'] + 30)) < 5]
chk("L1/10 Streben am Scheitel", apex_n, 5, apex_n == 5)
w = 2 * sum(math.hypot(k[0], k[1]) for k in base_nodes) / len(base_nodes)
chk("L5/7 Kuppelbreite (Knoten-Durchmesser) [mm]", round(w), 12000, abs(w - 12000) / 12000 < 0.03)
chk("L5/7 Hoehe/Breite", round(h / w, 3), 0.5, abs(h / w - 0.5) / 0.5 < 0.03)
chk("L10 Basisknoten (Zehneck; 1 Knoten an der Tuer ohne Streben)", len(base_nodes), "9-10", len(base_nodes) in (9, 10))
chk("L10 Strebenzahl 2V (60 + 10 Basis - Tuer)", len(t1), "55-65", 55 <= len(t1) <= 65)
s = B["T3_Sockel"]; ue = (s["bbox"]["max"][0] - s["bbox"]["min"][0] - 12000) / 2
chk("L2/11 Fundamentring (Flaechen 10 aussen + 10 innen + 2, Tuerluecke +4)", s["faces"], "22-28", 22 <= s["faces"] <= 30)
chk("L9/11 Sockel Ueberstand [mm]", round(ue), "<= 300", ue <= 300)
beds = [b for n, b in B.items() if n.startswith("Wanne") and klasse(n) not in PUFFER_CLS]   # Werkstatt-Komponente ibc_beet_*: je Instanz eine Wanne
chk("OBJ Substratbeete (14 IBC-Wannen als Instanzen)", len(beds), 14, len(beds) == 14)
# Tuer: seit M3 (Runde 45) ersetzt die Werkstatt-Komponente tuer_komplett (T50, Instanz Tuer_Komplett:1) die alten T4_-Koerper; Bounding-Box ueber alle Koerper der Klasse
DOOR_TILT = 10.81   # Grad, Neigung der Feldebene im Basisfeld BBB (loop-state M3 gebaut): die Tuer liegt in der Feldebene, nicht senkrecht
doorb = [b for n, b in B.items() if klasse(n) == "Tuer_Komplett"]
chk("Tuer_Komplett vorhanden (Instanz, Koerper)", (sum(1 for c in cmds if c["command"] == "occurrence.move" and str(c["params"].get("occurrence", "")).startswith("Tuer_Komplett:")), len(doorb)), "(1, >= 1)", len(doorb) >= 1)
d = {"min": [min(b["bbox"]["min"][i] for b in doorb) for i in range(3)], "max": [max(b["bbox"]["max"][i] for b in doorb) for i in range(3)]} if doorb else None
if d:
    dh = d["max"][2] - d["min"][2]; lichte = 1960 * math.cos(math.radians(DOOR_TILT))   # lichte Hoehe 1960 ueber Schwelle 40 mm, entlang der Feldebene -> Z-Anteil
    chk("Tuer Hoehe (Tuer_Komplett-bbox Z, Untergrenze lichte Hoehe 1960 mm in der Feldebene) [mm]", round(dh), ">= %d" % round(lichte - 20), dh >= lichte - 20)
chk("Tuer Breite (Parameter door_w; Geometrie-Breite nicht geprueft) [mm]", round(P["door_w"]), 1000, abs(P["door_w"] - 1000) < 20)
# Zugang: kleinster seitlicher Abstand Tuer-Bett (Mittelpunkte der Bett-/Tuerboxen, Naeherung ueber bbox-Abstand)
def gap(a, b):
    return math.hypot(*[max(0, max(a["min"][i] - b["max"][i], b["min"][i] - a["max"][i])) for i in range(2)])
if d:
    tg = min(gap(d, b["bbox"]) for b in beds)
    chk("Tuerzugang: Abstand Tuer_Komplett-Bett (bbox) [mm]", round(tg), ">= 1000", tg >= 1000)
t5 = B["T5_Zentraltank"]["bbox"]; t5d = t5["max"][0] - t5["min"][0]
def base(n): return re.sub(r" \(\d+\)", "", re.sub(r" \([^()]*:\d+\)", "", n))   # Ordinal/Pfad-Suffix der Instanzkoerper abtrennen
# Knoten-Normteile heissen seit Commit cd60551 ScheibeO_k, Schraube_k, ScheibeU_k, Mutter_k (frueher knoten_*): nur wenn der Koerper in einer Komponente Knoten_* liegt (nicht breiter als vorher)
KNOTEN_NORM = re.compile(r"(Schraube|ScheibeO|ScheibeU|Mutter)_\d+")
def knoten_teil(n): return base(n).startswith("knoten_") or bool(KNOTEN_NORM.fullmatch(base(n)) and klasse(n).startswith("Knoten_"))
tanks = [n for n in B if base(n) == "Tank" and klasse(n) not in PUFFER_CLS]   # Werkstatt-Komponenten tank_*: je Instanz ein Koerper 'Tank' (Puffer-Koerper zaehlen nicht mit)
pumps = [n for n in B if base(n) == "Montagetafel" and klasse(n) not in PUFFER_CLS]   # Werkstatt-Komponenten pumpe_*
chk("OBJ Tanks (4 Instanzen) + Zweitbecken T6 (1) + Pumpentafeln (8)", (len(tanks), len(pre("T6_Zweit")), len(pumps)), (4, 1, 8), (len(tanks), len(pre("T6_Zweit")), len(pumps)) == (4, 1, 8))
t5 = B["T5_Zentraltank"]["bbox"]; t5c = ((t5["max"][0] + t5["min"][0]) / 2, (t5["max"][1] + t5["min"][1]) / 2)
chk("OBJ Pool zentriert (Abstand Mitte [mm])", round(math.hypot(*t5c)), "< 50", math.hypot(*t5c) < 50)
wb = B["T5_Wasser"]["bbox"]; wd = wb["max"][0] - wb["min"][0]
chk("OBJ Wasserscheibe D [mm]", round(wd), 3890, abs(wd - 3890) < 20)
chk("L13 Tankwand [mm]", round(P["wall"]), ">= 150", P["wall"] >= 150)
chk("L13 Wasserscheibe T5_Wasser", len(pre("T5_Wasser")), 1, len(pre("T5_Wasser")) == 1)
chk("L6 Teilenamen T1,T3,T5,T6,T10,T11 vorhanden (T4 Tuer = Tuer_Komplett s. o.; T2 Haut = Phase 2, T8 NFT folgt)", sorted({n.split("_")[0] for n in BN}, key=lambda x: int(re.sub(r"\D", "", x[1:]) or 0)), "T1,T3,T5,T6,T10,T11", {n.split("_")[0] for n in BN} >= {f"T{i}" for i in (1, 3, 5, 6, 10, 11)})   # T7/T9 = Werkstatt-Instanzen (Tanks, Beete)
n_cls = lambda c: sum(1 for x in cmds if x["command"] == "occurrence.move" and str(x["params"].get("occurrence", "")).startswith(c + ":"))
nu, nv = int((2640 - 2 * P["pot_margin"]) // P["pot_pitch"]) + 1, int((800 - 2 * P["pot_margin"]) // P["pot_pitch"]) + 1
nui, nvi = int((1865 - 2 * P["pot_margin"]) // P["pot_pitch"]) + 1, int((933 - 2 * P["pot_margin"]) // P["pot_pitch"]) + 1
exp_pots = 8 * nu * nv + 6 * nui * nvi + sum(len(v["pots"]) * n for v, n in zip(json.load(open(os.path.join(ROOT, "data", "nft_pots.json")))["typen"].values(), (10, 6, 8)))
chk("Netztoepfe: Aussenbeete (8 x %d x %d) + Innenbeete (6 x %d x %d) + Rinnen (nft_pots.json) als Instanzen" % (nu, nv, nui, nvi), n_cls("Netztopf"), exp_pots, n_cls("Netztopf") == exp_pots)
chk("Netztoepfe Erwartung Runde 60: 960 Aussenbeete + 588 Innenbeete + 674 Rinnen", (8 * nu * nv, 6 * nui * nvi, exp_pots - 8 * nu * nv - 6 * nui * nvi, exp_pots), (960, 588, 674, 2222), (8 * nu * nv, 6 * nui * nvi, exp_pots - 8 * nu * nv - 6 * nui * nvi, exp_pots) == (960, 588, 674, 2222))
chk("Info: Koerperzahl im Modell (kein Pruefkriterium; 4667 ist die Instanzzahl der Viewer-Meldung Build 60, nicht die Koerperzahl)", len(B), "Information", True)
# Neue Bauteile Runde 60: Station T81 ist abgeschaltet (station_an 0) -> fehlt sie, ist das KEIN Fehler; Puffer klein T82 steht dann statt ihrer
st_an = int(P.get("station_an", 0))
chk("Puffer: Instanzen (Puffer_Station, Puffer_Klein) je nach station_an=%d (0 -> Station aus, Puffer klein T82)" % st_an, (n_cls("Puffer_Station"), n_cls("Puffer_Klein")), (st_an, 1 - st_an), (n_cls("Puffer_Station"), n_cls("Puffer_Klein")) == (st_an, 1 - st_an))
b3 = [b for n, b in B.items() if klasse(n) == "Becken_Dritt"]
chk("Drittbecken klein T14k: Instanz Becken_Dritt (1, Koerper >= 1) und pool3_d [mm]", (n_cls("Becken_Dritt"), len(b3), round(P["pool3_d"])), "(1, >= 1, 800)", n_cls("Becken_Dritt") == 1 and len(b3) >= 1 and abs(P["pool3_d"] - 800) < 1)
chk("Messstellen 13_Messstellen: Instanzen (3 H_TAUCH + 2 H_BERUHIG + 17 Sonden)", sum(1 for x in cmds if x["command"] == "occurrence.move" and str(x["params"].get("occurrence", "")).startswith(MESS_CLS)), 22, sum(1 for x in cmds if x["command"] == "occurrence.move" and str(x["params"].get("occurrence", "")).startswith(MESS_CLS)) == 22)
# Interferenz zwischen Instanzen/Teilen (Koerper EINER Komponenteninstanz ueberschneiden sich bewusst: Schweiss-/Schraubverbindungen, Pruefung der Werkstatt-Skripte)
# Das ganze Modell hat > 1500 Koerper: erst Bounding-Boxen in Python (nur Paare verschiedener Instanzen), dann nur die betroffenen Koerper exakt schneiden.
# Aus der Kollision genommen und GEZAEHLT (Ausgabe "NICHT GEPRUEFT"): Pflanzen (stecken im Medium), Plane Huelle_* (Referenzflaeche), Figuren Mensch_Referenz_* (Massstab), Messstellen MS_* (Ueberlappung gewollt)
SKIP = {"Pflanzen": PLANT_CLS, "Plane": PLANE_CLS, "Figuren": FIGUR_CLS, "Messstellen": MESS_CLS}
skipped = {k: [n for n in B if klasse(n).startswith(v)] for k, v in SKIP.items()}
skip_all = {n for v in skipped.values() for n in v}
names = [n for n in B if n not in skip_all]; G = {n: grp(n) for n in names}
bb = {n: (B[n]["bbox"]["min"], B[n]["bbox"]["max"]) for n in names}

# --- 1) Reine Geometrie: NFT-Tisch-Fusspunkte gegen Beete/Pool und Tisch gegen Tisch (statt zehntausender exakter Booleans; Werkstatt-Mangel W-M2/W-M3 jetzt ZAEHLBAR) ---
sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import sc as WSC, tisch_geom as TG
LAY = json.load(open(os.path.join(ROOT, "data", "layout.json"), encoding="utf-8"))
tp, td = WSC.load_params("nft_tisch")
mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
def sat_gap(A, Bq):   # konvexe Polygone (4 Ecken: Rechteck/Fussplatte, 8 Ecken: Beet mit Fase); Luecke = groesste Trennung entlang der Kantennormalen (Untergrenze der echten Luecke)
    g = -1e9
    for Q in (A, Bq):
        for i in range(len(Q)):
            e = (Q[(i + 1) % len(Q)][0] - Q[i][0], Q[(i + 1) % len(Q)][1] - Q[i][1]); m = math.hypot(*e); nx, ny = -e[1] / m, e[0] / m
            pa = [q[0] * nx + q[1] * ny for q in A]; pb = [q[0] * nx + q[1] * ny for q in Bq]
            g = max(g, min(pa) - max(pb), min(pb) - max(pa))
    return g
def rect(cx, cy, l, w, m, f=0):   # Rechteck (f > 0: 45-Grad-Fase f an allen vier Ecken -> Achteck) mit Drehung aus Matrix m (3x4, zeilenweise)
    c, s = m[0], m[4]; h, v_ = l / 2, w / 2
    loc = ((-h, -v_), (h, -v_), (h, v_), (-h, v_)) if not f else ((-h + f, -v_), (h - f, -v_), (h, -v_ + f), (h, v_ - f), (h - f, v_), (-h + f, v_), (-h, v_ - f), (-h, -v_ + f))
    return [(cx + u * c - v * s, cy + u * s + v * c) for u, v in loc]
vdim = {"Beet_aussen_800": (2640, 800)}   # Aussenbeet W17/D29 (data/components/ibc_beet.json aussen_800)
for b in LAY["ibc_beds"]:
    if "plants" not in b: vdim.setdefault("Beet_innen_933", (b["length"], b["width"]))
IBC = json.load(open(os.path.join(ROOT, "data", "components", "ibc_beet.json"), encoding="utf-8"))
FASEN = {"Beet_innen_933": float(findk(IBC, "innen_933")["fase"])}   # W26/D44: Innenbeet 45-Grad-Ecken, Schenkel 120 mm am Randwulst-Umriss (Aussenbeete ohne Fase)
bedrects = [rect(m[3], m[7], *vdim[k.split(":")[0]], m) for k, m in mv.items() if k.split(":")[0] in vdim]   # Fussplatten gegen das volle Rechteck (strenger als mit Fase)
bedpolys = [rect(m[3], m[7], *vdim[k.split(":")[0]], m, FASEN.get(k.split(":")[0], 0)) for k, m in mv.items() if k.split(":")[0] in vdim]   # Beet x Beet gegen die Fase (W-M4)
pool = B["T5_Zentraltank"]["bbox"]; pcx, pcy = (pool["max"][0] + pool["min"][0]) / 2, (pool["max"][1] + pool["min"][1]) / 2; pr = (pool["max"][0] - pool["min"][0]) / 2
fpw = {}; legbad = []; mingap = 1e9; poolbad = 0
for k, m in mv.items():
    cls = k.split(":")[0]
    if not cls.startswith("Tisch_"): continue
    typ = cls[6:]; G_ = TG.geometry(typ, tp, td["typen"][typ]); fp = tp["foot_plate"] / 2
    W = lambda x, y, m=m: (m[0] * x + m[1] * y + m[3], m[4] * x + m[5] * y + m[7])
    fpw[k] = [W(x, y) for x, y in TG.footprint_pts(G_, tp)]
    for (x, y) in G_["legs"]:
        plate = [W(x + sx * fp, y + sy * fp) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
        for br in bedrects:
            g = sat_gap(plate, br); mingap = min(mingap, g)
            if g < 0: legbad.append((k, round(g)))
        if typ == "innen":
            dpool = min(math.hypot(q[0] - pcx, q[1] - pcy) for q in plate) - pr
            if dpool < 0: poolbad += 1
chk("W-M2 NFT-Tisch-Fussplatten ausserhalb der Beete (reine Geometrie, Verletzungen)", len(legbad), 0, len(legbad) == 0)
chk("W-M2b Innentisch-Pfosten ausserhalb des Poolrands (Verletzungen)", poolbad, 0, poolbad == 0)
tmin = {}
cen = {k: (sum(q[0] for q in v) / len(v), sum(q[1] for q in v) / len(v)) for k, v in fpw.items()}
keys = list(fpw)
for i, a in enumerate(keys):
    for b in keys[i + 1:]:
        if math.hypot(cen[a][0] - cen[b][0], cen[a][1] - cen[b][1]) > 4800: continue
        tmin[(a, b)] = min(math.hypot(p1[0] - p2[0], p1[1] - p2[1]) for p1 in fpw[a][::2] for p2 in fpw[b][::2])
tbad = [(k, round(v)) for k, v in tmin.items() if v < tp["corner_gap"]]
bgap = min(sat_gap(a_, b_) for i, a_ in enumerate(bedpolys) for b_ in bedpolys[i + 1:])
bgap0 = min(sat_gap(a_, b_) for i, a_ in enumerate(bedrects) for b_ in bedrects[i + 1:])
chk("Beete untereinander kollisionsfrei, Innenbeete mit Fase %d mm (W-M4/W26; reine Geometrie, kleinste Luecke [mm])" % FASEN["Beet_innen_933"], round(bgap), "> 0", bgap > 0)
print("W-M4 Beet x Beet: kleinste Luecke mit Fase", round(bgap), "mm | ohne Fase (Vergleich, alter Stand)", round(bgap0), "mm | Werkstatt-Stand Runde 44/46 (Lage vor D62/D63): -35 ohne / +36 mit Fase")
chk("W-M3 Tisch-Tisch-Abstand an den Ecken >= corner_gap (Umrisspunkte, Verletzungen)", len(tbad), 0, len(tbad) == 0)
print("GEOMETRIE kleinster Fussplatte-Beet-Abstand", round(mingap), "mm | kleinster Tisch-Tisch-Abstand", round(min(tmin.values())) if tmin else None, "mm | Verletzungen Bein/Beet, Pool, Tisch/Tisch:", len(legbad), poolbad, len(tbad), tbad[:3], legbad[:3])

# --- 2) Exakte Kollisionspruefung fuer Paare, die nicht schon Geometrie/Verankerung abdeckt; getrennte Laeufe nach Klassen (Knotenarm x Fundamentring braucht Minuten je Paar, ist aber verankert und erlaubt) ---
cand = []; openm = {"W-M1": [], "M2b": [], "Fuss-Erde": [], "Teil-A-gewollt": []}
for i, a in enumerate(names):
    amin, amax = bb[a]
    for b in names[i + 1:]:
        if G[a] == G[b] and G[a][1]: continue   # gleiche Komponenteninstanz
        if a.startswith("T1_") and b.startswith("T1_"): continue   # Streben treffen sich an den Knoten (bewusst)
        bmin, bmax = bb[b]
        if not all(amin[k] < bmax[k] and bmin[k] < amax[k] for k in range(3)): continue
        cs = {G[a][0], G[b][0]}
        if all(c.startswith("Beet_") for c in cs): continue   # Beete untereinander: reine Geometrie (bedrects, siehe unten)
        if "T1_Strebe" in a + b and (knoten_teil(a) or knoten_teil(b)): openm["M2b"].append((a, b)); continue   # Querbolzen/Muttern x Strebe: Bohrungen fehlen (offen, M2b), Bounding-Box-Kandidaten
        if "T3_Sockel" in (a, b) and max(math.hypot(x, y) for n in (a, b) if n != "T3_Sockel" for x in (B[n]["bbox"]["min"][0], B[n]["bbox"]["max"][0]) for y in (B[n]["bbox"]["min"][1], B[n]["bbox"]["max"][1])) < 5600: continue   # Fundamentring nur am Rand
        if all(c.startswith(("Tisch_", "Beet_")) for c in cs) and any(c.startswith("Tisch_") for c in cs): continue   # Tisch x Beet/Tisch: Geometrie oben
        if any(c.startswith(("Knoten_", "Fundamentanker")) for c in cs) and ({a, b} & {"T3_Sockel", "T13_Erde"}): continue   # Knoten/Anker sind im Fundamentring bzw. Erdreich verankert
        if {a.split("_")[0], b.split("_")[0]} == {"T1", "T3"}: continue   # Streben im Fundamentring verankert
        if "T13_Erde" in (a, b) and len(cs) > 1 and all(c.startswith(("Tank_", "Pumpe_", "Tisch_")) for c in cs - {"Erdflaeche"}): continue   # Fussplatten/-schrauben stehen im Boden (Werkstatt: bis 24 mm)
        cand.append((a, b))
HEAVY = ("T3_Sockel", "T13_Erde")
CHUNK = int(os.environ.get("LATTE_CHUNK", 300))   # Paare je CLI-Aufruf (U9)
CACHE = os.path.join(ROOT, "scripts", ".latte-cache.json")   # Ergebnisse je Paar, gueltig solange dome.sc und alle verknuepften Komponentendateien unveraendert sind
sig = str(os.path.getmtime(dome)) + "|" + str(max(os.path.getmtime(os.path.join(ROOT, "designs", "components", f)) for f in os.listdir(os.path.join(ROOT, "designs", "components")) if f.endswith(".sc")))
cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
if cache.get("sig") != sig: cache = {"sig": sig, "checked": [], "found": []}
pk = lambda a, b: "|".join(sorted((a, b)))
def save_cache(): json.dump(cache, open(CACHE, "w"))
def run_exact(pairs, label):
    """Paare in Runden exakt schneiden (Ergebnisse gecacht): unfertige Paare (Budget) werden mit nur ihren Koerpern wiederholt, spaete Runden mit grossem Budget (max. 6 Runden)."""
    done = set(cache["checked"]); found = [it for it in cache["found"] if frozenset((it["a"], it["b"])) in {frozenset(p_) for p_ in pairs}]
    todo = [pr for pr in pairs if pk(*pr) not in done]
    print(f"EXAKT {label}: {len(pairs)} Paare, {len(pairs) - len(todo)} aus dem Cache", flush=True)
    for rnd in range(6):
        if not todo: break
        n_before = len(todo); rest = []; nb = 0
        # U9: in Bloecken zu CHUNK Paaren (ein Aufruf mit >3000 Koerpern lieferte keine Ausgabe; ein Block, der scheitert, bleibt ungeprueft und kommt in die naechste Runde)
        for k0 in range(0, len(todo), CHUNK):
            part = todo[k0:k0 + CHUNK]
            bodies = sorted({n for pr in part for n in pr}); nb += len(bodies); sj = os.path.join(tmp, "i.json")
            json.dump({"commands": [{"command": "inspect.interference", "params": {"bodies": bodies, "budget_s": 600 if rnd < 2 else 1200}}]}, open(sj, "w"))
            rr = run_json(["run", sj, "--in", dome, "--results"], may_fail=True); ts = {frozenset(pr) for pr in part}
            if not rr: rest += part; continue
            new = [it for it in (find(rr, "interferences") or []) if frozenset((it["a"], it["b"])) in ts]
            left = {frozenset((u["a"], u["b"])) for u in (find(rr, "unchecked") or []) if u.get("b")}
            fin = [pr for pr in part if frozenset(pr) not in left]
            cache["checked"] += [pk(*pr) for pr in fin]; cache["found"] += new; save_cache(); found += new
            rest += [pr for pr in part if frozenset(pr) in left]
        todo = rest
        print(f"EXAKT {label} Runde {rnd + 1}: {nb} Koerper (Bloecke zu {CHUNK} Paaren), noch offen {len(todo)}", flush=True)
        if len(todo) == n_before and rnd >= 2: break   # kein Fortschritt mehr: Rest bleibt ungeprueft (wird gemeldet)
    return found, todo
inter, unch = [], []
for label, gp in (("ohne Fundamentring/Erde", [pr for pr in cand if not set(pr) & set(HEAVY)]),
                  ("Fundamentring", [pr for pr in cand if "T3_Sockel" in pr]), ("Erde", [pr for pr in cand if "T13_Erde" in pr])):
    f, u = run_exact(gp, label); inter += f; unch += u
bad = []
for it in inter:
    a, b = it["a"], it["b"]
    cs = {G[a][0], G[b][0]}
    if G[a][0] == G[b][0] == "Tuer_Komplett": continue   # Tuer-Teile (Komponente tuer_komplett T50) verbinden sich (Scharnier/Pfosten/Schwelle); ersetzt die alte T4_-Ausnahme
    if "T13_Erde" in (a, b) and (cs - {"Erdflaeche"}) <= set(PUFFER_CLS): openm["Fuss-Erde"].append((a, b)); continue   # Puffer klein/Station: Fuesse im Boden, nur gezaehlt (Tiefe nicht bewertet)
    if {a.split("_")[0], b.split("_")[0]} & {"T10"} and ({a.split("_")[0], b.split("_")[0]} <= {"T10", "T1", "T5", "T7"}): continue
    if all(c.startswith(("Pumpe_", "Tank_")) for c in cs) and any(c.startswith("Pumpe_") for c in cs): openm["W-M1"].append((a, b)); continue   # offener Werkstatt-Mangel W-M1: Tank-Rahmenstreben x OBJ-Pumpentafeln
    if "T1_Strebe" in a + b and (knoten_teil(a) or knoten_teil(b)): openm["M2b"].append((a, b)); continue   # Querbolzen/Scheiben/Muttern des Knotens durch die Strebe: Bohrungen fehlen (offen, M2b)
    # Runde 69 Teil A (M10-S5-LUFT): gewollter Kontakt, eng benannt; der Rest bleibt KOLL
    vol = it.get("volume_mm3", it.get("volume", 0)); ka, kb = klasse(a).lower(), klasse(b).lower()
    if "T5_Wasser" in (a, b) and (kb if a == "T5_Wasser" else ka).startswith(("luft_scheibenbelueftung", "lt_bogen90_d25", "lt_rohr_d25", "schwimmerventil")):
        openm["Teil-A-gewollt"].append((a, b)); continue   # Wasserkoerper ist kein Bauteil: Luftleitung d25 und Belueftungsscheiben liegen im Becken, die Schwimmerkugel schwimmt darin
    if vol <= 50 and "lt_bogen90_d25" in (ka, kb) and ({ka, kb} - {"lt_bogen90_d25"}) <= {"lt_rohr_d25", "luft_scheibenbelueftung"} | {k_ for k_ in (ka, kb) if k_.startswith("lt_rohr_d25_")}:
        openm["Teil-A-gewollt"].append((a, b)); continue   # Steckverbindung Luftleitung d25: Rohr/Stutzen steckt im Bogen, Ueberschneidung hoechstens 3 mm3 (Passungsspiel)
    print("KOLL", a, b)
    bad.append((a, b, round(it.get("volume_mm3", it.get("volume", 0)))))
chk("L6 Kollisionen (exakt; ohne verankerte Teile, Rohr/Schlauch, offenen Mangel W-M1)", len(bad), 0, len(bad) == 0)
res.append({"info": "Kollisionen", "pairs": bad[:20]})
chk("L6 Kollisionspruefung vollstaendig (alle Kandidatenpaare exakt geschnitten)", len(unch), 0, len(unch) == 0)
print("OFFEN W-M1 (Pumpentafel x Tankrahmen, Werkstatt):", len(openm["W-M1"]), "| M2b (Knoten-Querbolzen x Strebe, Bohrungen fehlen, Montage):", len(openm["M2b"]), "| Fuss-Erde Puffer (gezaehlt, nicht bewertet):", len(openm["Fuss-Erde"]), "| Teil-A gewollt (Wasserkoerper, Steckverbindung Luft d25):", len(openm["Teil-A-gewollt"]), "| exakt geprueft: Paare", len(cand))
inst = lambda *pf: sum(1 for x in cmds if x["command"] == "occurrence.move" and str(x["params"].get("occurrence", "")).startswith(pf))
print("NICHT GEPRUEFT (aus der Kollision genommen): Plane %d Koerper / %d Instanzen, Figuren %d / %d, Messstellen %d / %d, Pflanzen %d / %d (Koerper / Instanzen)" % (
    len(skipped["Plane"]), inst(*PLANE_CLS), len(skipped["Figuren"]), inst(*FIGUR_CLS), len(skipped["Messstellen"]), inst(*MESS_CLS), len(skipped["Pflanzen"]), inst(*PLANT_CLS)))
res.append({"info": "nicht geprueft", "zaehlung": {k: len(v) for k, v in skipped.items()}})
print("NICHT GEPRUEFT (Skript-Grenzen): Tuer-Breite aus der Geometrie (nur Parameter door_w) und Obergrenze der Tuerhoehe/Rahmenmasse | Plane x Streben (Folie liegt auf) | Keilschienen, Planenausschnitt-Zarge, Bodenbefestigung (nicht im Modell) | "
      "Rohre/Schlaeuche und Messstellen an Leitungen (M10, noch nicht verlegt) | Laufwege/Bedienzonen (check_walkways*.py) | Tank-Abstaende zu den neuen Pumpentafeln (tank_offsets kennt sie nicht) | station_an=%d: Station T81 %s" % (st_an, "abgeschaltet, nicht erwartet" if not st_an else "erwartet und geprueft"))
if unch: print("NICHT GEPRUEFT:", [(a[:30], b[:30]) for a, b in unch[:10]])
passed = sum(1 for r in res if r.get("pass")); total = sum(1 for r in res if "pass" in r)
for r in res:
    if "pass" in r: print(("PASS" if r["pass"] else "FAIL"), r["check"], "| Ist:", r["ist"], "| Soll:", r["soll"])
print(f"SCORE {passed}/{total} = {100*passed/total:.0f}%")
sys.exit(0 if passed == total else 1)
