"""M10-S0: Pruefung der Leitungstrassen (Rohre, Schlaeuche, Leerrohre) gegen Hindernisse, Hoehenbaender, Gaenge und Gefaelle. Nur Lesen, kein CAD-Lauf, nur Standardbibliothek.
Aufruf:   python -X utf8 scripts/check_leitungen.py [trassen.json]     (Standard: data/leitungstrassen.json; fehlt sie, gilt die Liste als leer)
          python -X utf8 scripts/check_leitungen.py --selbsttest     (leere Liste auf dem echten Modell plus kuenstliche Trassen mit bekanntem Ergebnis)
Ausgang 0 = keine Verstoesse, 1 = Verstoss oder Selbsttest fehlgeschlagen.

HOEHENPROBE (M10-S0, 01.11.2026, ohne CAD-Lauf) — Annahme "absolut = Netzlisten-Z (Flur-relativ) + 400" ist BESTAETIGT:
  data/params.json sock_h = 400 (Bodenniveau). scripts/dome-script.json, occurrence.move Pumpe_gross:1: Matrix dreht nur um Z (Spalte 3 = 0/0/1), Verschiebung x 3372,6 / y -765,1 / z 400.
  docs/parts/pumpe.md Port-Tabelle: pumpe_gross Saugstutzen Lage Bauteil-KS x 196 / y 76 / z 120. Weltpunkt = Matrix x Port = x 3176,7 / y -841,4 / z 520 (= 400 + 120); alle vier Pumpe_gross:1..4 messen Z 520.
  Stuetzen: Beet_aussen_800:1 Instanz-Z 238 = 400 - 162 (Netz: Beetboden -162); Pool (gen_dome.py pool_dims) Wasserspiegel fz + water_z = 400 + 515 = 915, Rand 400 + 650 = 1050,
  Innenboden z_bot + 120 = -1305 absolut = -1705 relativ, Netz-Bodenablauf -1685 liegt 20 mm darueber (passt). Komponenten-Nullpunkt = Standflaeche (.compbox.json pumpe_gross Z 0..463).
  Grenze: Die Port-Lage selbst ist ein Tabellenwert (docs/parts/pumpe.md, Quelle E aus den Parametern), nicht am Koerper gemessen; belegt ist die Z-Abbildung der Instanz (Rotation nur um Z, Versatz 400).
  Die Selbsttest-Stufe A rechnet die Probe bei jedem Lauf nach (Zeile "Hoehenprobe").

EINGABEFORMAT der Trassenliste (JSON, Koordinaten in mm im Modellrahmen, Ursprung Kuppelmitte; Z absolut, oder "z_bezug": "flur" = Netzlisten-Z, das Skript addiert sock_h):
  {"z_bezug": "absolut" | "flur",
   "regeln": {"nah_w": 500},                                  (optional, siehe RULES)
   "trassen": [ {"id": "K01-a", "kante": "K01" | null,        (Kante der Netzliste; null = Kabel/Leerrohr ohne Kante, dann "dn" Pflicht)
                 "dn": 63,                                    (Aussendurchmesser mm; Standard = dn der Kante, Abweichung wird gemeldet)
                 "pfad": [[x, y, z], [x, y, z], ...],         (Rohrachse als Linienzug, Fliessrichtung = Pfadrichtung)
                 "band": "U" | "W" | "T" | "UE",              (ein Band fuer alle Teilstuecke) ODER "baender": [Band je Teilstueck]
                 "gefaelle_pct": 1.0,                         (optional: Schwerkraftleitung, jedes Teilstueck muss in Pfadrichtung mindestens so fallen)
                 "heber": false,                              (optional: Pipe-voll-Heber, Gefaelle-Pruefung entfaellt)
                 "anschluss": ["Pumpe_gross:1", "Zentralpool"] } ]   (Hindernisse, die diese Trasse beruehren darf: Port, Rand)
  Baender (Plan Abschnitt 4 Regel 1, Z relativ zum Flur): U = Unterflur -400..-100; W = am Bauteil 0..1000 und hoechstens nah_w vom Tank/Pumpe/Puffer/Beckenrand;
  T = Tischebene 900..1100 und im Grundriss unter einem Tisch; UE = ueber Kopf >= 2100. Senkrechte Teilstuecke (Grundriss < 20 mm) sind Steigleitungen: kein Bandtest, aber Kollision und Gang.
REGELN, die geprueft werden (Kennung im Bericht):
  KOLL     Rohrachse (Zylinder, Radius dn/2, Abtastung 10 mm) gegen Hindernisse (Bauteile als Bounding-Box je Instanz aus .compbox.json, Portale/Beete, Tischfuesse, Becken als Zylinder)
           und Rohr gegen Rohr (Abstand der Achsen < Summe der Radien; Abzweige: Beruehrung bis 150 mm vom Trassenende wird als T-Stueck gewertet). Nicht modelliert: Rinnen und Verteilerrohre der Tische, Haut, Streben, Pflanzen.
  BAND     Hoehenband je Teilstueck, W-Naehe, T unter Tisch.
  GANG     Achspunkt mit 0 <= Z rel < 2100 auf freiem Boden (innerhalb Zehneck, ausserhalb jedes Hindernis-Grundrisses und Tisches): verboten; Ausnahme nur Band W im Abstand nah_w zum Bauteil.
  GEFAELLE Teilstueck mit Grundriss >= 100 mm faellt um mindestens gefaelle_pct; kuerzere und senkrechte Teilstuecke duerfen nicht steigen.
  EINGABE  Formfehler (unbekannte Kante, falsches Band, weniger als 2 Punkte) und Abweichung dn gegen Kante.
Grenzen: Hindernisse sind Bounding-Boxen (Tank mit Kegel, Pumpe mit Konsole: grob); Gangbreite 500 mm wird nicht gerechnet, nur "freier Boden" (die Laufwegkarte check_walkways_voll.py bleibt der Massstab fuer Engstellen); Biegeradius der Schlaeuche und Geschwindigkeit (check_netz.py) nicht."""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NETZ = os.path.join(ROOT, "data", "leitungsnetz.json")
DEFAULT_TRASSEN = os.path.join(ROOT, "data", "leitungstrassen.json")
BANDS = {"U": (-400.0, -100.0), "W": (0.0, 1000.0), "T": (900.0, 1100.0), "UE": (2100.0, 1e9)}   # Z relativ zum Flur (Plan 4.1)
RULES = {"nah_w": 500.0, "gang_z_max": 2100.0, "tol": 2.0, "step": 10.0, "gang_step": 50.0, "junction": 150.0, "steig_xy": 20.0, "min_xy": 100.0}
TECH = ("Tank_klein", "Tank_gross", "Tank_gross_t3", "Pumpe_klein", "Pumpe_gross", "Puffer_Klein", "Feinfilter")   # M10-S2a: Feinfilter ergaenzt (S1 stellte ihn ins Modell)


# ---------------------------------------------------------------- Modell einlesen (Einlesecode wie place_feinfilter.py / check_walkways_voll.py)
def poly(m, bx):
    x0, y0, z0, x1, y1, z1 = bx; c, s = m[0], m[4]
    return [(m[3] + u * c - v * s, m[7] + u * s + v * c) for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))], (m[11] + z0, m[11] + z1)

def mk_poly(name, kind, pg, z0, z1):
    xs, ys = [p[0] for p in pg], [p[1] for p in pg]
    return {"name": name, "kind": kind, "pg": pg, "c": None, "z0": z0, "z1": z1, "bb": (min(xs), min(ys), max(xs), max(ys))}

def mk_circle(name, kind, cx, cy, r, z0, z1):
    return {"name": name, "kind": kind, "pg": None, "c": (cx, cy, r), "z0": z0, "z1": z1, "bb": (cx - r, cy - r, cx + r, cy + r)}

class World:
    def __init__(self, fz, ap, door, obst, tables):
        self.fz, self.ap, self.door, self.obst, self.tables = fz, ap, door, obst, tables   # tables: Liste Grundriss-Polygone
        self.normals = [(math.cos(math.radians(door + 36 * k)), math.sin(math.radians(door + 36 * k))) for k in range(10)]

def load_world():
    cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
    P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
    lay = json.load(open(os.path.join(ROOT, "data", "layout.json")))
    mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
    fz = P["sock_h"]; ap = P["dome_base_d"] / 2 * math.cos(math.radians(18)); rim = fz + P["pool_rim"]
    box = {k.split(":")[0]: v for k, v in json.load(open(os.path.join(ROOT, "scripts", ".compbox.json"))).items()}
    warn = []
    tg = None
    try:
        sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop")); import sc as WSC, tisch_geom as TG
        tg = (TG, *WSC.load_params("nft_tisch"))
    except Exception as e:
        warn.append("Tischgeometrie nicht lesbar (%s): Tischfuesse und Tischflaechen fehlen" % e)
    obst, tables = [], []
    for k, m in mv.items():
        cls = k.split(":")[0]
        if cls in ("Beet_aussen_800", "Beet_innen_933"):
            l, w = (2640, 800 + 230) if cls == "Beet_aussen_800" else (1865, 933 + 230)
            pg, _ = poly(m, (-l / 2, -w / 2, 0, l / 2, w / 2, 0)); obst.append(mk_poly(k, "beet", pg, m[11], fz + 1500))
        elif cls.startswith("Tisch_") and tg:
            TG, tp, td = tg; typ = cls.split("_")[1]
            G = TG.geometry(typ, tp, td["typen"][typ]); fp = tp["foot_plate"] / 2
            for (x, y) in G["legs"]:
                pg = [(m[0] * (x + sx * fp) + m[1] * (y + sy * fp) + m[3], m[4] * (x + sx * fp) + m[5] * (y + sy * fp) + m[7]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
                obst.append(mk_poly(k + " Fuss", "tischfuss", pg, fz, fz + G["zc"]))
            x0 = min(r["xc"] - r["L"] / 2 - 29 for r in G["rows"]); x1 = max(r["xc"] + r["L"] / 2 + 34 for r in G["rows"])
            y0, y1 = G["ymid"] - G["Wt"] / 2 - 60, G["ymid"] + G["Wt"] / 2 + 60
            tables.append((k, [(m[0] * u + m[1] * v + m[3], m[4] * u + m[5] * v + m[7]) for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]))
        elif cls in TECH:
            if cls.lower() not in box: warn.append("Box fehlt fuer %s" % cls); continue
            pg, (za, zb) = poly(m, box[cls.lower()]); obst.append(mk_poly(k, "technik", pg, za, zb))
    # Becken als Vollzylinder von Boden (z_bot = fz + water_z - depth) bis Rand (fz + pool_rim), Radius = Wasserradius + Wand
    w = lay["pool2"]["water_z"]
    for nm, (cx, cy), r, wz, dep in (("Zentralpool", (0.0, 0.0), lay["pool"]["d"] / 2 + P["wall"], lay["pool"]["water_z"], P["pool_depth"]),
            ("Zweitbecken", (P["pool2_r"] * math.cos(math.radians(P["pool2_az"])), P["pool2_r"] * math.sin(math.radians(P["pool2_az"]))), lay["pool2"]["d"] / 2 + 60, w, P["pool2_depth"]),
            ("Drittbecken", (P["pool3_r"] * math.cos(math.radians(P["pool3_az"])), P["pool3_r"] * math.sin(math.radians(P["pool3_az"]))), P["pool3_d"] / 2 + 60, w, P["pool3_depth"])):
        obst.append(mk_circle(nm, "becken", cx, cy, r, fz + wz - dep, rim))
    wd = World(fz, ap, P["door_edge_az"], obst, tables); wd.warn = warn; wd.mv = mv
    return wd


# ---------------------------------------------------------------- Geometrie
def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def clamp(v): return 0.0 if v < 0 else 1.0 if v > 1 else v
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t, a[2] + (b[2] - a[2]) * t)
def az_r(x, y): return "Az %.0f / r %.0f" % (math.degrees(math.atan2(y, x)), math.hypot(x, y))

def seg_seg(p1, q1, p2, q2):
    """Naechste Punkte zweier Strecken (Ericson): (Abstand, Punkt auf 1, Punkt auf 2)."""
    d1, d2, r = sub(q1, p1), sub(q2, p2), sub(p1, p2)
    a, e, f = dot(d1, d1), dot(d2, d2), dot(d2, r)
    if a <= 1e-9 and e <= 1e-9: s = t = 0.0
    elif a <= 1e-9: s, t = 0.0, clamp(f / e)
    else:
        c = dot(d1, r)
        if e <= 1e-9: t, s = 0.0, clamp(-c / a)
        else:
            b = dot(d1, d2); den = a * e - b * b
            s = clamp((b * f - c * e) / den) if den > 1e-9 else 0.0
            t = (b * s + f) / e
            if t < 0: t, s = 0.0, clamp(-c / a)
            elif t > 1: t, s = 1.0, clamp((b - c) / a)
    c1, c2 = lerp(p1, q1, s), lerp(p2, q2, t)
    return math.dist(c1, c2), c1, c2

def poly_dist(x, y, pg):
    """Abstand eines Punktes zu einem konvexen Polygon (0 innen)."""
    side, best = 0, 1e18
    for i in range(len(pg)):
        a, b = pg[i], pg[(i + 1) % len(pg)]; ex, ey = b[0] - a[0], b[1] - a[1]
        side |= 1 if ex * (y - a[1]) - ey * (x - a[0]) >= 0 else 2
        t = clamp(((x - a[0]) * ex + (y - a[1]) * ey) / (ex * ex + ey * ey)) if ex or ey else 0.0
        best = min(best, math.hypot(x - a[0] - t * ex, y - a[1] - t * ey))
    return 0.0 if side != 3 else best   # alle Kreuzprodukte gleichen Vorzeichens = innen

def dist_xy(o, x, y):
    """Waagerechter Abstand zum Hindernis-Grundriss (0 innen)."""
    if o["c"]: return max(math.hypot(x - o["c"][0], y - o["c"][1]) - o["c"][2], 0.0)
    return poly_dist(x, y, o["pg"])

def dist_3d(o, x, y, z):
    dz = max(o["z0"] - z, 0.0, z - o["z1"])
    return math.hypot(dist_xy(o, x, y), dz)

def near_bb(o, x, y, r): b = o["bb"]; return b[0] - r <= x <= b[2] + r and b[1] - r <= y <= b[3] + r

def samples(a, b, step):
    n = max(1, int(math.ceil(math.dist(a, b) / step)))
    return [lerp(a, b, i / n) for i in range(n + 1)]

def in_dome(w, x, y): return max(x * n[0] + y * n[1] for n in w.normals) <= w.ap

def free_floor(w, x, y):
    """Boden innerhalb des Zehnecks, nicht unter einem Hindernis- oder Tisch-Grundriss."""
    if not in_dome(w, x, y): return False
    for o in w.obst:
        if near_bb(o, x, y, 0) and dist_xy(o, x, y) == 0.0: return False
    return not any(poly_dist(x, y, pg) == 0.0 for _, pg in w.tables)

def near_tech(w, x, y, nah):
    for o in w.obst:
        if o["kind"] not in ("technik", "becken"): continue
        if o["kind"] == "becken": d = abs(math.hypot(x - o["c"][0], y - o["c"][1]) - o["c"][2])
        else:
            if not near_bb(o, x, y, nah): continue
            d = dist_xy(o, x, y)
        if d <= nah: return True
    return False

def under_table(w, x, y): return any(poly_dist(x, y, pg) == 0.0 for _, pg in w.tables)


# ---------------------------------------------------------------- Pruefung
def pruefe(w, netz, doc):
    """Gibt (Verstoesse, Infozeilen) zurueck; Verstoss = (Regel, Trasse, Text)."""
    R = dict(RULES); R.update(doc.get("regeln", {}))
    fl = 1.0 if doc.get("z_bezug", "absolut") == "flur" else 0.0
    kanten = {k["id"]: k for k in netz["kanten"]}
    viol, info = [], []
    tr = []
    for t in doc.get("trassen", []):
        tid = t.get("id", "?")
        if len(t.get("pfad", [])) < 2: viol.append(("EINGABE", tid, "weniger als 2 Punkte")); continue
        pts = [(float(p[0]), float(p[1]), float(p[2]) + fl * w.fz) for p in t["pfad"]]
        ks = t.get("kante")
        if ks and ks not in kanten: viol.append(("EINGABE", tid, "Kante %s nicht in der Netzliste" % ks)); continue
        dn = t.get("dn") or (kanten[ks]["dn"] if ks else None)
        if not dn: viol.append(("EINGABE", tid, "dn fehlt (Trasse ohne Kante)")); continue
        if ks and t.get("dn") and float(t["dn"]) != float(kanten[ks]["dn"]): viol.append(("EINGABE", tid, "dn %s weicht von %s d%s ab (Reduzierung dokumentieren)" % (t["dn"], ks, kanten[ks]["dn"])))
        nseg = len(pts) - 1
        bands = t.get("baender") or [t.get("band")] * nseg
        if len(bands) != nseg or any(b not in BANDS for b in bands): viol.append(("EINGABE", tid, "Band fehlt/unbekannt oder 'baender' hat nicht %d Eintraege" % nseg)); continue
        tr.append({"id": tid, "kante": ks, "r": float(dn) / 2, "pts": pts, "bands": bands, "pct": t.get("gefaelle_pct"), "heber": bool(t.get("heber")), "ok": set(t.get("anschluss", []))})
    covered = {t["kante"] for t in tr if t["kante"]}
    info.append("Trassen: %d, Teilstuecke: %d, Laenge %.1f m; Kanten mit Trasse %d von %d" % (len(tr), sum(len(t["pts"]) - 1 for t in tr), sum(math.dist(t["pts"][i], t["pts"][i + 1]) for t in tr for i in range(len(t["pts"]) - 1)) / 1000, len(covered), len(kanten)))
    if tr and len(covered) < len(kanten): info.append("Kanten ohne Trasse: " + ", ".join(k for k in kanten if k not in covered))
    nah = R["nah_w"]
    for t in tr:
        tid, r, pts = t["id"], t["r"], t["pts"]
        # KOLL gegen Hindernisse
        hit = {}
        for i in range(len(pts) - 1):
            for p in samples(pts[i], pts[i + 1], R["step"]):
                for o in w.obst:
                    if any(o["name"] == a or o["name"].startswith(a + " ") for a in t["ok"]): continue
                    if not near_bb(o, p[0], p[1], r + R["tol"]): continue
                    if dist_3d(o, *p) < r - R["tol"]:
                        h = hit.setdefault(o["name"], [p, 0]); h[1] += 1
        for name, (p, n) in hit.items(): viol.append(("KOLL", tid, "Rohr d%g trifft %s, erste Stelle %s Z %.0f, etwa %d mm Achslaenge" % (2 * r, name, az_r(p[0], p[1]), p[2], n * R["step"])))
        # BAND, GANG, GEFAELLE je Teilstueck
        gang, bad_near, bad_tab = [], [], []
        for i in range(len(pts) - 1):
            a, b = pts[i], pts[i + 1]; b_ = t["bands"][i]; dxy = math.hypot(b[0] - a[0], b[1] - a[1]); steig = dxy < R["steig_xy"] and abs(b[2] - a[2]) >= R["steig_xy"]
            lo, hi = BANDS[b_]
            if not steig:
                for z in (a[2], b[2]):
                    if not (lo - R["tol"] <= z - w.fz <= hi + R["tol"]): viol.append(("BAND", tid, "Teilstueck %d Band %s: Z rel %.0f ausserhalb %g..%g" % (i + 1, b_, z - w.fz, lo, hi if hi < 1e8 else float("inf")))); break
            for p in samples(a, b, R["gang_step"]):
                zr = p[2] - w.fz
                if not steig and b_ == "W" and not near_tech(w, p[0], p[1], nah): bad_near.append(p)
                if not steig and b_ == "T" and not under_table(w, p[0], p[1]): bad_tab.append(p)
                if 0.0 <= zr < R["gang_z_max"] and free_floor(w, p[0], p[1]):
                    if (b_ == "W" or steig) and near_tech(w, p[0], p[1], nah): continue
                    gang.append(p)
            if t["pct"] and not t["heber"]:
                dz = b[2] - a[2]
                if steig or dxy < R["min_xy"]:
                    if dz > R["tol"] / 2: viol.append(("GEFAELLE", tid, "Teilstueck %d steigt um %.0f mm gegen die Fliessrichtung (%s)" % (i + 1, dz, az_r(a[0], a[1]))))
                elif -dz < t["pct"] / 100 * dxy - 0.5: viol.append(("GEFAELLE", tid, "Teilstueck %d: Gefaelle %.2f %% (%.0f mm auf %.0f mm), verlangt %.2f %%" % (i + 1, -dz / dxy * 100, -dz, dxy, t["pct"])))
        if bad_near: viol.append(("BAND", tid, "Band W: %d Punkte weiter als %.0f mm vom Bauteil, erste Stelle %s" % (len(bad_near), nah, az_r(bad_near[0][0], bad_near[0][1]))))
        if bad_tab: viol.append(("BAND", tid, "Band T: %d Punkte nicht unter einem Tisch, erste Stelle %s" % (len(bad_tab), az_r(bad_tab[0][0], bad_tab[0][1]))))
        if gang: viol.append(("GANG", tid, "%d Punkte (etwa %.1f m) quer auf freiem Boden zwischen Z 0 und %.0f, erste Stelle %s Z %.0f" % (len(gang), len(gang) * R["gang_step"] / 1000, R["gang_z_max"], az_r(gang[0][0], gang[0][1]), gang[0][2] - w.fz)))
    # Rohr gegen Rohr
    segs = [(t, i) for t in tr for i in range(len(t["pts"]) - 1)]
    for ai in range(len(segs)):
        ta, i = segs[ai]; pa, qa = ta["pts"][i], ta["pts"][i + 1]
        for bi in range(ai + 1, len(segs)):
            tb, j = segs[bi]
            if ta is tb and abs(i - j) <= 1: continue
            pb, qb = tb["pts"][j], tb["pts"][j + 1]; rr = ta["r"] + tb["r"]
            if any(min(u[k] for u in (pa, qa)) - rr > max(u[k] for u in (pb, qb)) or min(u[k] for u in (pb, qb)) - rr > max(u[k] for u in (pa, qa)) for k in range(3)): continue
            d, c1, c2 = seg_seg(pa, qa, pb, qb)
            if d >= rr - R["tol"]: continue
            if min(math.dist(c1, e) for e in (ta["pts"][0], ta["pts"][-1])) <= R["junction"] or min(math.dist(c2, e) for e in (tb["pts"][0], tb["pts"][-1])) <= R["junction"]: continue
            viol.append(("KOLL", ta["id"], "Rohr trifft Rohr %s (Achsabstand %.0f < %.0f) bei %s Z %.0f" % (tb["id"], d, rr, az_r(c1[0], c1[1]), c1[2])))
    return viol, info


def report(viol, info, title):
    print("== check_leitungen: " + title)
    for l in info: print("  " + l)
    for rule in ("EINGABE", "KOLL", "BAND", "GANG", "GEFAELLE"):
        vs = [v for v in viol if v[0] == rule]
        print("  %-9s %d Verstoesse" % (rule, len(vs)))
        for _, tid, txt in vs: print("    [%s] %s: %s" % (rule, tid, txt))
    print("  Ergebnis: " + ("OK" if not viol else "%d VERSTOESSE" % len(viol)))


# ---------------------------------------------------------------- Selbsttest
def selbsttest():
    netz = json.load(open(NETZ, encoding="utf-8")); ok = True
    # Stufe A: echtes Modell, leere Liste, Hoehenprobe nachgerechnet, Einlesen der Hindernisse
    w = load_world(); m = w.mv["Pumpe_gross:1"]; x, y, zz = 196.0, 76.0, 120.0   # Saugstutzen, docs/parts/pumpe.md
    wz = [(m[8] * x + m[9] * y + m[10] * zz + m[11]) for m in (w.mv["Pumpe_gross:%d" % i] for i in (1, 2, 3, 4))]
    wx, wy = m[0] * x + m[1] * y + m[2] * zz + m[3], m[4] * x + m[5] * y + m[6] * zz + m[7]
    print("Hoehenprobe: Saugstutzen Pumpe_gross:1 relativ Z 120, sock_h %.0f -> Matrix x %.1f / y %.1f / z %.1f; Pumpe_gross:1..4 z = %s -> %s" % (w.fz, wx, wy, wz[0], wz, "BESTAETIGT (400 + 120 = 520)" if all(abs(v - 520) < 0.01 for v in wz) else "WIDERLEGT"))
    ok &= all(abs(v - 520) < 0.01 for v in wz)
    print("Modell: %d Hindernisse, %d Tischflaechen%s" % (len(w.obst), len(w.tables), "; " + "; ".join(w.warn) if w.warn else ""))
    viol, info = pruefe(w, netz, {"trassen": []}); report(viol, info, "Stufe A: leere Trassenliste, echtes Modell"); ok &= not viol
    pm = w.mv["Pumpe_gross:1"]; inside = (pm[0] * 0 + pm[1] * 30 + pm[3], pm[4] * 0 + pm[5] * 30 + pm[7], 600.0)
    v2, _ = pruefe(w, netz, {"trassen": [{"id": "A-pumpe", "kante": None, "dn": 20, "band": "W", "pfad": [list(inside), [inside[0], inside[1], 650.0]]}]})
    print("  Probe echtes Modell: Rohr durch die Pumpe -> KOLL %s" % ("erkannt" if any(v[0] == "KOLL" and "Pumpe_gross:1" in v[2] for v in v2) else "NICHT erkannt")); ok &= any(v[0] == "KOLL" and "Pumpe_gross:1" in v[2] for v in v2)
    # Stufe B: kuenstliche Welt, bekannte Ergebnisse. Flur 400, Zehneck wie im Modell, Kasten 0..1000 (technik), Tisch x 2000..3500 / y -500..500
    sw = World(400.0, 12000 / 2 * math.cos(math.radians(18)), -72.0, [mk_poly("Kasten:1", "technik", [(0, 0), (1000, 0), (1000, 1000), (0, 1000)], 400, 1400)], [("Tisch:1", [(2000, -500), (3500, -500), (3500, 500), (2000, 500)])])
    def T(i, band, pfad, **kw): d = {"id": i, "kante": None, "dn": 63, "band": band, "pfad": pfad}; d.update(kw); return d
    cases = [
        (T("ok_unter", "U", [[-3000, -3000, 100], [-3000, 1000, 55]], gefaelle_pct=1.0), set()),
        (T("flach", "U", [[-2500, -3000, 100], [-2500, 1000, 80]], gefaelle_pct=1.0), {"GEFAELLE"}),
        (T("durch_kasten", "W", [[-500, 500, 900], [1500, 500, 900]]), {"KOLL"}),
        (T("an_kasten", "W", [[-500, 500, 900], [1500, 500, 900]], anschluss=["Kasten:1"]), set()),
        (T("quer_gang", "W", [[-3000, -2000, 900], [-1500, -2000, 900]]), {"BAND", "GANG"}),
        (T("ueber_kopf", "UE", [[-3000, -2500, 2600], [-1500, -2500, 2600]]), set()),
        (T("tisch_ok", "T", [[2200, 0, 1400], [3300, 0, 1400]]), set()),
        (T("tisch_falsch", "T", [[2200, 2000, 1400], [3300, 2000, 1400]]), {"BAND", "GANG"}),
        (T("u_zu_hoch", "U", [[-3000, 3000, 350], [-2000, 3000, 350]]), {"BAND"}),
        (T("steigt", "U", [[-2000, -3500, 60], [-2000, -3500, 160], [-2000, -3000, 100]], gefaelle_pct=1.0), {"GEFAELLE"}),
        (T("kreuz_a", "UE", [[4000, -3000, 2600], [4000, 3000, 2600]]), {"KOLL"}),
        (T("kreuz_b", "UE", [[3000, 0, 2630], [5000, 0, 2630]]), set()),
        (T("abzweig", "UE", [[4000, 3000, 2600], [4000, 3500, 2600], [4400, 3500, 2600]]), set()),
        (T("t_stueck", "UE", [[4000, -1000, 2632], [4400, -1000, 2632], [4400, -1000, 2900]]), set()),   # Abzweig-T: Anfang liegt 32 mm neben der Achse von kreuz_a (Rohr d63), Beruehrung am Trassenanfang -> T-Stueck, kein Verstoss
    ]
    doc = {"trassen": [c for c, _ in cases]}; v3, i3 = pruefe(sw, netz, doc)
    # kreuz_a und kreuz_b: KOLL wird beim ersten Rohr (a) gemeldet; kreuz_b als Partner. Erwartung nach Rohr, die den Eintrag fuehrt.
    got = {}
    for rule, tid, _ in v3: got.setdefault(tid, set()).add(rule)
    exp = {c["id"]: e for c, e in cases if e}
    report(v3, i3, "Stufe B: kuenstliche Trassen")
    for tid, e in exp.items():
        g = got.get(tid, set())
        if g != e: ok = False; print("  FEHLER Selbsttest %s: erwartet %s, gefunden %s" % (tid, sorted(e), sorted(g)))
    extra = set(got) - set(exp)
    if extra: ok = False; print("  FEHLER Selbsttest: unerwartete Verstoesse bei " + ", ".join(sorted(extra)))
    # Z-Bezug "flur": Netzlisten-Z -300 -> absolut 100, muss wie ok_unter laufen
    v4, _ = pruefe(sw, netz, {"z_bezug": "flur", "trassen": [T("flur", "U", [[-3000, -3000, -300], [-3000, 1000, -345]], gefaelle_pct=1.0)]})
    print("  Z-Bezug flur: %s" % ("OK" if not v4 else v4)); ok &= not v4
    print("SELBSTTEST " + ("BESTANDEN" if ok else "FEHLGESCHLAGEN")); return ok


if __name__ == "__main__":
    if "--selbsttest" in sys.argv: sys.exit(0 if selbsttest() else 1)
    arg = [a for a in sys.argv[1:] if not a.startswith("--")]; path = arg[0] if arg else DEFAULT_TRASSEN
    netz = json.load(open(NETZ, encoding="utf-8"))
    if os.path.exists(path): doc = json.load(open(path, encoding="utf-8")); title = os.path.relpath(path, ROOT)
    else: doc = {"trassen": []}; title = "keine Trassenliste (%s fehlt) = leer" % os.path.relpath(path, ROOT)
    w = load_world(); viol, info = pruefe(w, netz, doc)
    for wm in w.warn: info.append("WARNUNG " + wm)
    report(viol, info, title); sys.exit(1 if viol else 0)
