"""N-TECHNIK-INNEN (Planer, 05.11.2026): Platzsuche innen fuer die Technikgruppe und Schaetzung Rohrlaenge, Boegen, Geblaesedruck vorher (Runde 74) / nachher.
Nur lesen: scripts/dome-script.json, scripts/.compbox.json, data/params.json, data/leitungstrassen.json. Schreibt nichts.

Aufrufe:
  python -X utf8 scripts/n_technik_innen.py suche [streng|gang300]   Platzsuche (je Regelsatz etwa 1 Minute)
  python -X utf8 scripts/n_technik_innen.py laengen                  Rohrlaenge und Boegen je Kante, V0 (Runde 74) gegen V1 (Turm im Tuerkeil)
  python -X utf8 scripts/n_technik_innen.py druck                    Reibungsverlust Luft und Geblaeseleistung V0 gegen V1
  python -X utf8 scripts/n_technik_innen.py huelle                   Abstand Turm/Schrank zur Huelle je Hoehe

Regeln der Suche (D70, D72, Wandluft, Tuergang D62): Koerper >= 150 mm zu Tanks/Pumpen/Puffer/Filtern/Schlammfass, >= 500 zu Beet-Portalen und
Becken (gang300: 300), >= 700 zum Zentralpool (Laufweg A), Tuerachse >= 450 (Tuergang 900), Bedienzone 650 vor der Front frei von Koerpern,
Abstand zur Huelle: Wandluft 110 am Boden plus Neigung der Tuerfacette 0,191 mm je mm Hoehe (Knoten n25/n23 r 6000 Z 475, n07 r 5104 Z 3629).
[A] = Annahme des Planers."""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def J(*p): return json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
P = {k: v["value"] for k, v in J("data", "params.json").items()}
APO = 5706.0                       # Fundamentring-Innenflaeche (Zehneck-Apothem)
NEIG = (5706.0 - 5104.0) / (3629.0 - 475.0)   # Tuerfacette: Einzug je mm Hoehe (0,191)
FZ = 400.0                         # Flur absolut

# ---------------------------------------------------------------- Platzsuche
def hindernisse(gang_beet):
    cmds = J("scripts", "dome-script.json")["commands"]
    mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
    box = J("scripts", ".compbox.json")
    def bx(n): return next(v for k, v in box.items() if k.split(":")[0] == n)
    rects, circs = [], []
    def rect(cx, cy, yaw, x0, y0, x1, y1, gang, lab):
        c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        rects.append(([(cx + u * c - v * s, cy + u * s + v * c) for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))], gang, lab))
    circs.append((-36.0, 20.0, 1945 + 150, 700.0, "Zentralpool"))
    for nm, r_, az_, rr in (("Zweitbecken", P["pool2_r"], P["pool2_az"], 1747 / 2 + 60), ("Drittbecken", P["pool3_r"], P["pool3_az"], P["pool3_d"] / 2 + 60)):
        circs.append((r_ * math.cos(math.radians(az_)), r_ * math.sin(math.radians(az_)), rr, gang_beet, nm))
    src = {"Tank_gross": "tank_gross", "Tank_gross_t3": "tank_gross_t3", "Tank_klein": "tank_klein", "Pumpe_klein": "pumpe_klein", "Pumpe_gross": "pumpe_gross", "Puffer_Klein": "puffer_klein", "Feinfilter": "feinfilter"}
    for k, m in mv.items():
        cl = k.split(":")[0]; yaw = math.degrees(math.atan2(m[4], m[0]))
        if cl in src: b = bx(src[cl]); rect(m[3], m[7], yaw, b[0], b[1], b[3], b[4], 150.0, k)
        elif cl == "Beet_aussen_800": rect(m[3], m[7], yaw, -1320, -515, 1320, 515, gang_beet, k)
        elif cl == "Beet_innen_933": rect(m[3], m[7], yaw, -932, -581, 932, 581, gang_beet, k)
        elif cl == "Tisch_innen": rect(m[3], m[7], yaw, -900, -500, 900, 500, gang_beet, k)
        elif cl == "Schlammfass": circs.append((m[3], m[7], 330.0, 150.0, k))
    for x, y, yaw in ((P["ff_a_x"], P["ff_a_y"], P["ff_a_yaw"]), (P["ff_b_x"], P["ff_b_y"], P["ff_b_yaw"])):
        l, w = (P["ff_grube_l"] + 40) / 2, (P["ff_grube_w"] + 40) / 2; rect(x, y, yaw, -l, -w, l, w, 150.0, "Feinfilter-Grube")
    return rects, circs

def _pin(p, q):
    s = [(q[(i + 1) % 4][0] - q[i][0]) * (p[1] - q[i][1]) - (q[(i + 1) % 4][1] - q[i][1]) * (p[0] - q[i][0]) for i in range(4)]
    return all(v >= 0 for v in s) or all(v <= 0 for v in s)
def _seg(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy or 1)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def rdist(A, B):
    if any(_pin(p, B) for p in A) or any(_pin(p, A) for p in B): return 0.0
    return min(_seg(p, Q[i], Q[(i + 1) % 4]) for PP, Q in ((A, B), (B, A)) for p in PP for i in range(4))
def cdist(A, cx, cy, r): return (0.0 if _pin((cx, cy), A) else min(_seg((cx, cy), A[i], A[(i + 1) % 4]) for i in range(4))) - r
def wand(A): return min(APO - (x * math.cos(math.radians(-72 + 36 * k)) + y * math.sin(math.radians(-72 + 36 * k))) for x, y in A for k in range(10))
TA = math.radians(-72)
def tuerachse(A):
    a = (2095 * math.cos(TA), 2095 * math.sin(TA)); b = (APO * math.cos(TA), APO * math.sin(TA))
    return min(_seg(p, a, b) for p in A)

def frei(H, cx, cy, w, d, front, gang_beet):
    rects, circs = H
    body = [(cx - w / 2, cy - d / 2), (cx + w / 2, cy - d / 2), (cx + w / 2, cy + d / 2), (cx - w / 2, cy + d / 2)]
    fx, fy = front[0]; hoehe = front[1]
    if fx: zone = [(cx + fx * w / 2, cy - d / 2), (cx + fx * (w / 2 + 650), cy - d / 2), (cx + fx * (w / 2 + 650), cy + d / 2), (cx + fx * w / 2, cy + d / 2)]
    else: zone = [(cx - w / 2, cy + fy * d / 2), (cx + w / 2, cy + fy * d / 2), (cx + w / 2, cy + fy * (d / 2 + 650)), (cx - w / 2, cy + fy * (d / 2 + 650))]
    wb = wand(body)
    if wb < 110 + NEIG * (hoehe + FZ - 475) or wand(zone) < 0 or tuerachse(body) < 450: return None
    mind = 1e9
    for pts, gang, lab in rects:
        db = rdist(body, pts)
        if db < gang or rdist(zone, pts) < 1: return None
        mind = min(mind, db)
    for x2, y2, r, gang, lab in circs:
        db = cdist(body, x2, y2, r)
        if db < gang or cdist(zone, x2, y2, r) < 1: return None
        mind = min(mind, db)
    return round(mind), round(wb - NEIG * (hoehe + FZ - 475))

TEILE = {"turm 800x500 H2000": (800, 500, 2000), "schrank 800x500 H1200": (800, 500, 1200), "geblaese_paar 532x680 H730": (532, 680, 730),
         "aktivkohle 1700x500 H929": (1700, 500, 929), "regal 1000x500 H1200": (1000, 500, 1200)}
def suche(regel):
    gb = 500.0 if regel == "streng" else 300.0
    H = hindernisse(gb)
    print("Regelsatz", regel, "(Gang zu Beeten/Becken %d mm)" % gb)
    for name, (w0, d0, h) in TEILE.items():
        hits = []
        for rot in (0, 90):
            w, d = (w0, d0) if rot == 0 else (d0, w0)
            for f in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                for ix in range(-40, 61):
                    for iy in range(-60, 11):
                        x, y = ix * 100.0, iy * 100.0
                        if not 2100 <= math.hypot(x, y) <= 5700 or not -125 <= math.degrees(math.atan2(y, x)) <= -5: continue
                        r = frei(H, x, y, w, d, (f, h), gb)
                        if r: hits.append((x, y, rot, f, r))
        print("  %-28s %3d Lagen" % (name, len(hits)) + ("" if not hits else ": x %d..%d, y %d..%d; Beispiel Mitte (%d, %d) Drehung %d Front %s, kleinster Abstand %d, Huellenluft oben %d" % (
            min(h_[0] for h_ in hits), max(h_[0] for h_ in hits), min(h_[1] for h_ in hits), max(h_[1] for h_ in hits), *hits[len(hits) // 2][:4], *hits[len(hits) // 2][4])))

# ---------------------------------------------------------------- Laengen
TURM = (600.0, -4900.0)            # V1: Turmmitte (Ergebnis der Suche gang300), Front +X zum Tuergang
V1_PORT = {"luft": (600.0, -4750.0, 2150.0), "frisch": (600.0, -5050.0, 1240.0)}   # [A] Verteiler oben (Geblaese auf Rost Z rel 1000), Station unten (Koepfe wie Runde 74)
GRABEN = 300.0                     # Punkte bis Z 300 gelten als Graben
LUFT = {"K44": 130.0, "K45": 20.0, "K46": 20.0, "K49": 2.0, "K51": 10.0, "K47": 5.0, "K48": 5.0}   # l/min; K44/K49 Netz, Rest [A]
ID = {20: 16.2, 25: 21.2, 32: 28.2, 40: 36.2}   # Innen-Ø [A] Wand 1,9 wie luftverteiler_6

def boegen(p):
    n = 0
    for a, b, c in zip(p, p[1:], p[2:]):
        u = [b[i] - a[i] for i in range(3)]; v = [c[i] - b[i] for i in range(3)]
        lu, lv = math.sqrt(sum(x * x for x in u)), math.sqrt(sum(x * x for x in v))
        if lu > 1 and lv > 1 and sum(u[i] * v[i] for i in range(3)) / lu / lv < 0.999: n += 1
    return n

def zerlegen(p, rueck=False):
    """Startstueck (bis zum ersten Grabenpunkt), Grabenstrecke, Zielstueck; rueck=True: Gruppe ist das Ende (K39)."""
    if rueck: p = p[::-1]
    g = [i for i, q in enumerate(p) if q[2] <= GRABEN]
    i0, i1 = g[0], g[-1]
    L = lambda s: sum(math.dist(a, b) for a, b in zip(s, s[1:]))
    return L(p[:i0 + 1]), L(p[i0:i1 + 1]), L(p[i1:]), p[i0], p[i1], p

def laengen(ausgabe=True):
    tr = [t for t in J("data", "leitungstrassen.json")["trassen"] if t.get("linie") in ("luft_b", "frisch")]
    zeilen = []
    kanten = {}
    for t in tr: kanten.setdefault(t["kante"], []).append(t)
    for k, ts in kanten.items():
        L0 = sum(sum(math.dist(a, b) for a, b in zip(t["pfad"], t["pfad"][1:])) for t in ts); B0 = sum(boegen(t["pfad"]) for t in ts)
        haupt = max(ts, key=lambda t: len(t["pfad"]))
        if k == "K44":
            intern = L0 - sum(math.dist(a, b) for a, b in zip(haupt["pfad"], haupt["pfad"][1:]))   # Geblaese-Verbindung bleibt
        else: intern = 0.0
        rueck = k == "K39"
        s0, g0, e0, a0, b0, _ = zerlegen(haupt["pfad"], rueck)
        m0 = abs(b0[0] - a0[0]) + abs(b0[1] - a0[1])
        umweg = g0 / m0 if m0 > 1 else 1.0
        port = V1_PORT["frisch" if haupt["linie"] == "frisch" else "luft"]
        s1 = abs(port[2] - a0[2]) + 200.0                             # senkrecht in den Graben + Port-Stueck [A]
        m1 = abs(b0[0] - port[0]) + abs(b0[1] - port[1])
        g1 = max(m1, m1 * umweg)
        L1 = intern + s1 + g1 + e0
        zeilen.append((k, haupt["dn"], L0, B0, L1, umweg))
    # K47/K48 (Runde 74 nicht verlegt): Ziel Deckel Absetzer, Steiger am Tank bis Z 1723 + Port 200, Umweg 1,2 [A]
    cmds = J("scripts", "dome-script.json")["commands"]
    mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
    v0 = (-1225.0 + 480.0, -6860.0, 1036.0)                          # V0: Abgang 4 des Verteilers (Kappe)
    for k, tk in (("K47", "Tank_klein:1"), ("K48", "Tank_klein:2")):
        m = mv[tk]; z = (m[3], m[7])
        f = lambda p: abs(p[2] - 240.0) + 200.0 + 1.2 * (abs(z[0] - p[0]) + abs(z[1] - p[1])) + (FZ + 1323.0 - 240.0) + 200.0
        zeilen.append((k, 20, f(v0), 6, f(V1_PORT["luft"]), 1.2))
    if ausgabe:
        print("Kante  dn   V0 Runde74 [m]  Boegen V0   V1 Turm innen [m]  Umweg-Faktor   (K47/K48: V0 nicht verlegt, beide Werte geschaetzt)")
        for k, dn, L0, B0, L1, u in sorted(zeilen):
            print("%-5s %3d   %8.2f        %3d        %8.2f          %.2f" % (k, dn, L0 / 1000, B0, L1 / 1000, u))
        s0 = sum(z[2] for z in zeilen if z[0] not in ("K47", "K48")); s1 = sum(z[4] for z in zeilen if z[0] not in ("K47", "K48"))
        print("Summe der 9 verlegten Kanten: V0 %.1f m, V1 %.1f m, Differenz %.1f m (%.0f %%)" % (s0 / 1000, s1 / 1000, (s1 - s0) / 1000, 100 * (s1 - s0) / s0))
        for med in ("luft_b", "frisch"):
            ks = {t["kante"] for t in tr if t["linie"] == med}
            a = sum(z[2] for z in zeilen if z[0] in ks); b = sum(z[4] for z in zeilen if z[0] in ks)
            print("  %s: V0 %.1f m, V1 %.1f m" % ("Luft" if med == "luft_b" else "Frischwasser", a / 1000, b / 1000))
        a = sum(z[2] for z in zeilen); b = sum(z[4] for z in zeilen)
        print("Mit K47/K48: V0 %.1f m, V1 %.1f m" % (a / 1000, b / 1000))
    return zeilen

# ---------------------------------------------------------------- Druck
def dp_rohr(q_l_min, d_mm, L_mm, nb):
    """Darcy-Weisbach, Luft 25 C (rho 1,18, ny 1,55e-5), glattes Rohr (Blasius / laminar 64/Re); Bogen = 30 x d gleichwertige Laenge [A]."""
    if q_l_min <= 0: return 0.0
    d = d_mm / 1000.0; A = math.pi * d * d / 4; v = q_l_min / 60000.0 / A; Re = v * d / 1.55e-5
    lam = 64 / Re if Re < 2300 else 0.3164 / Re ** 0.25
    Le = L_mm / 1000.0 + nb * 30 * d
    return lam * Le / d * 1.18 * v * v / 2   # Pa

def druck():
    z = {k: (dn, L0, B0, L1) for k, dn, L0, B0, L1, u in laengen(False)}
    stat = 1000 * 9.81 * 2.17   # Pa, R45: Ausstroemer 2,17 m unter dem Spiegel
    print("Statischer Druck Pool (R45, 2,17 m): %.1f kPa; Diffusor [A] 3 kPa (R45 Spanne 3-5)" % (stat / 1000))
    print("Kante  Q l/min  dn   dp V0 [Pa]   dp V1 [Pa]   (V1: gleiche Bogenzahl angenommen; V1-Steiger +1,1 m je Luftkante)")
    for k in ("K44", "K45", "K46", "K49", "K51", "K47", "K48"):
        dn, L0, B0, L1 = z[k]; di = ID[dn]
        print("%-5s %6.0f  %3d   %8.0f     %8.0f" % (k, LUFT[k], dn, dp_rohr(LUFT[k], di, L0, B0), dp_rohr(LUFT[k], di, L1, B0)))
    for q in (130.0, 205.0):
        a = dp_rohr(q, ID[40], z["K44"][1], z["K44"][2]); b = dp_rohr(q, ID[40], z["K44"][3], z["K44"][2])
        p0 = stat + 3000 + a; p1 = stat + 3000 + b
        w = lambda p: q / 60000 * p / 0.45
        print("Pool-Strang K44 bei %3.0f l/min: Gesamtdruck V0 %.2f kPa, V1 %.2f kPa; Luftleistung/0,45 = elektrisch V0 %.0f W, V1 %.0f W (Differenz %.1f W)" % (q, p0 / 1000, p1 / 1000, w(p0), w(p1), w(p1) - w(p0)))
    def dp_wasser(q, di, L, nb):   # Wasser 20 C, rho 998, ny 1,0e-6, Bogen 30 x d [A]
        d = di / 1000.0; v = q / 60000.0 / (math.pi * d * d / 4); Re = v * d / 1.0e-6; lam = 64 / Re if Re < 2300 else 0.3164 / Re ** 0.25
        return lam * (L / 1000.0 + nb * 30 * d) / d * 998 * v * v / 2
    for k, q in (("K39", 4.0), ("K40", 4.0), ("K41", 2.0)):
        dn, L0, B0, L1 = z[k]
        print("Frischwasser %s bei %.0f l/min (Hausdruck, keine Pumpe): Reibung V0 %.0f Pa, V1 %.0f Pa" % (k, q, dp_wasser(q, ID[dn], L0, B0), dp_wasser(q, ID[dn], L1, B0)))

def huelle():
    for name, (cx, cy, w, d, rot) in {"Turm V1 (600,-4900)": (600, -4900, 800, 500, 0), "Schrank Tuerkeil streng (800,-5100) gedreht": (800, -5100, 500, 800, 0)}.items():
        body = [(cx - w / 2, cy - d / 2), (cx + w / 2, cy - d / 2), (cx + w / 2, cy + d / 2), (cx - w / 2, cy + d / 2)]
        wb = wand(body)
        print(name, "Abstand zur Fundamentring-Innenflaeche am Boden %d mm;" % wb, ", ".join("Hoehe %d: %d mm" % (h, wb - NEIG * (h + FZ - 475)) for h in (0, 930, 1200, 1730, 2000)))

def pruef():
    """Pruefpunkt fuer Montage/Pruefer: Turm 800 x 500 x 2000 um (turm_x, turm_y) aus data/params.json (Rueckfall technik_x/technik_y)."""
    cx = float(P.get("turm_x", P["technik_x"])); cy = float(P.get("turm_y", P["technik_y"]))
    R_, C_ = hindernisse(300.0)
    b = [(cx - 400, cy - 250), (cx + 400, cy - 250), (cx + 400, cy + 250), (cx - 400, cy + 250)]
    ab = sorted([(round(rdist(b, p)), l) for p, g, l in R_] + [(round(cdist(b, x, y, r)), l) for x, y, r, g, l in C_])[:5]
    beet = min(d for d, l in ab + [(9999, "Beet")] if l.startswith("Beet"))
    tank = min(d for d, l in ab + [(9999, "x")] if not l.startswith(("Beet", "Zentral", "Zweit", "Dritt")))
    hl = wand(b) - NEIG * (2000 + FZ - 475)
    ok = beet >= 300 and tank >= 150 and tuerachse(b) >= 450 and hl >= 110
    print("Turm um (%d, %d): naechste %s; Beet-Portal %d (Soll >= 300), Tank/Pumpe %d (>= 150), Tuerachse %d (>= 450), Huellenluft in 2000 mm Hoehe %d (>= 110): %s"
          % (cx, cy, ab, beet, tank, tuerachse(b), hl, "PASS" if ok else "FAIL"))
    return ok

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "laengen"
    if cmd == "pruef": sys.exit(0 if pruef() else 1)
    if cmd == "suche": suche(sys.argv[2] if len(sys.argv) > 2 else "streng")
    elif cmd == "druck": druck()
    elif cmd == "huelle": huelle()
    else: laengen()
