"""M10-S5-LUFT-B: Technikgruppe "vorlaeufig, E13" (D81) und ihre Leitungen K39, K40, K41, K44 (Zuleitung), K45, K46, K49, K51, K52.

Lage (Befund Runde 74, Paket docs/packages/m10-s5-luft.md): innen ist zwischen Tuer (Az -72, Huelle_BBB_tuer) und Ecke Az -90 nur ein Streifen von etwa
1,35 x 1,2 m frei (Pumpe_klein:2 steht 1380 mm vor der Wand), die Gruppe passt dort nicht. D81 sagt "aussen am Fundamentring neben der Tuer (Az -85)": die Gruppe
steht AUSSEN vor dem Fundamentring, achsparallel (Leitungsordnung R1), Schrankmitte Az -85 (Parameter technik_az). Alle Teile haengen an einem Gruppen-Ursprung
(technik_x, technik_y): eine Verschiebung beider Parameter versetzt die ganze Gruppe; die Leitungen werden dabei neu geroutet (dieses Skript neu laufen lassen).

Leitungen: von den Bauteil-Ports senkrecht in den Graben (Luft Z 290, Frischwasser Z 190 absolut, Band U), dort Manhattan-Router auf 50-mm-Raster gegen
Becken, Beet-Taschen, Feinfilter-Gruben, Schlammfass-Gruben, Schrank-Einfuehrung und alle vorhandenen Trassen; am Ziel senkrecht hoch und mit
Port-Stuecken (<= 300 mm, Leitungsordnung Ausnahme 2) an den Port. Aufruf: python -X utf8 scripts/technik_e13.py   (schreibt data/leitungstrassen.json, idempotent)."""
import heapq, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import leitung as LT

FZ = 400.0
Z_LUFT, Z_FRISCH = 290.0, 190.0          # Rohrachse im Graben (Band U: Z rel -400 bis -100); Frischwasser 100 mm tiefer, damit Luft und Wasser sich kreuzen duerfen
Z_LUFT_K = 240.0                         # kleine Luftstraenge K46, K49, K51: eigene Lage, damit sie die Hauptstraenge K44/K45 (Z 290) kreuzen duerfen (>= 47 mm Luft)
Z_K39 = 140.0                            # Hausanschluss K39 unter dem Frischwasser der Station (Z 190, 25 mm Luft zwischen den Rohren)
STEP = 50.0                              # Raster des Routers
KLAR = 30.0                              # lichter Abstand zu Hindernissen [A]
KNICK = 4000.0                           # Kosten je Bogen im Router (mm-Aequivalent), drueckt die Bogenzahl (R5)
NAH = 280.0                              # R8: fremde Leitung in anderer Hoehe naeher als 250 mm (Achsabstand) kostet je Rasterschritt NAH_KOST: Kreuzen ja, parallel fahren nein
NAH_KOST = 400.0
SCHLEIFE_Z = 1110.0                      # Geblaese-Austritt und Hauptverteiler: Schleife ueber dem Spiegel (Geblaese-Blatt: Rohrachse 710 ueber der Aufstellflaeche)

def P_():
    return {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}

def gruppe(P):
    """Lagen der Gruppe im Modellrahmen (Z absolut). Gruppen-Ursprung = Schrankmitte am Boden (technik_x, technik_y)."""
    ox, oy = float(P["technik_x"]), float(P["technik_y"])
    g = {"schrank": (ox, oy), "cab": (P["cab_x"], P["cab_y"], P["cab_z"])}
    g["einfuehrung"] = (ox, oy, FZ, 0.0)
    ga = (ox - 2800.0, oy + 30.0); gb = (ox - 2800.0, oy - 370.0)        # Geblaese A/B westlich (yaw 0: Austritt zeigt +X), Fussabdruck x -120..+412, y -190..+90
    g["geblaese"] = [(ga[0], ga[1], FZ, 0.0), (gb[0], gb[1], FZ, 0.0)]
    g["austritt"] = [(ga[0] + 412.0, ga[1], FZ + 710.0), (gb[0] + 412.0, gb[1], FZ + 710.0)]
    g["x_t"] = ox - 2150.0                                               # T d20 der beiden Geblaese-Straenge
    g["red_a"] = ox - 2000.0                                             # Reduziermuffe d40/d20: Muffenebene A (gross), kleine Seite zeigt nach Westen
    g["vert"] = (ox - 1800.0, gb[1], SCHLEIFE_Z)                         # Hauptverteiler luftverteiler_6: Muffe A (Einlauf) im Westen, Sammler +X, Abgaenge nach unten
    g["station"] = (ox - 800.0, oy - 1410.0, FZ, 90.0)                   # aktivkohle_station gedreht: Bauteil-X = Welt +Y (Ausgang K40 zeigt zur Kuppel, K52 nach Osten)
    return g

def verteiler_matrix(v):
    """luftverteiler_6 um die Sammlerachse gedreht: Bauteil-X = Welt +X, Bauteil-Z = Welt -Z (Abgaenge zeigen nach unten), Bauteil-Y = Welt -Y."""
    return [1.0, 0.0, 0.0, v[0], 0.0, -1.0, 0.0, v[1], 0.0, 0.0, -1.0, v[2]]

ABG = [(75, 40, "K44"), (195, 25, "K45"), (315, 25, "K46"), (435, 20, None), (555, 20, "K51"), (675, 20, "K49")]   # Abgaenge luftverteiler_6 (x, d, Kante) von West nach Ost; 4 = K47/K48 Kappe; Reihenfolge so, dass sich die Wege nicht kreuzen

def k90(d): return LT.ports("lt_bogen90_d%d" % d)[1][1][0]

# ---------------------------------------------------------------- Hindernisse unter Flur (2D) fuer den Router
def hindernisse(P, doc):
    lay = json.load(open(os.path.join(ROOT, "data", "layout.json"), encoding="utf-8"))
    cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
    mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
    kreise, rechtecke, kapseln = [], [], []
    kreise.append((0.0, 0.0, lay["pool"]["d"] / 2 + P["wall"] + 10, "Zentralpool"))
    a2 = math.radians(P["pool2_az"]); kreise.append((P["pool2_r"] * math.cos(a2), P["pool2_r"] * math.sin(a2), lay["pool2"]["d"] / 2 + 60 + 10, "Zweitbecken"))
    a3 = math.radians(P["pool3_az"]); kreise.append((P["pool3_r"] * math.cos(a3), P["pool3_r"] * math.sin(a3), P["pool3_d"] / 2 + 60 + 10, "Drittbecken"))
    for k, m in mv.items():
        cls = k.split(":")[0]
        if cls in ("Beet_aussen_800", "Beet_innen_933"):
            l, w = (2953 + 20, 933 + 20) if cls == "Beet_aussen_800" else (1865 + 20, 933 + 20)   # Tasche in der Erde (erde_fn: Wanne + 20)
            rechtecke.append((m[3], m[7], math.degrees(math.atan2(m[4], m[0])), l, w, k))
    for x, y, yaw in ((P["ff_a_x"], P["ff_a_y"], P["ff_a_yaw"]), (P["ff_b_x"], P["ff_b_y"], P["ff_b_yaw"])):
        rechtecke.append((x, y, yaw, P["ff_grube_l"] + 40, P["ff_grube_w"] + 40, "Feinfilter-Grube"))
    for gr in doc.get("gruben", []): kreise.append((gr["x"], gr["y"], gr["d"] / 2, "Grube " + gr["id"]))
    g = gruppe(P); sx, sy = g["schrank"]
    rechtecke.append((sx - 112.0, sy, 0.0, 1244.0 + 40, 500.0 + 40, "Schrank-Einfuehrung"))
    for tr in doc["trassen"]:
        if tr.get("linie") in ("luft_b", "frisch"): continue
        pts = [tuple(map(float, p)) for p in tr["pfad"]]; r = float(tr["dn"]) / 2
        for a, b in zip(pts[:-1], pts[1:]):
            if min(a[2], b[2]) > FZ + 50 and tr.get("linie") != "luft": continue
            kapseln.append((a, b, r, tr["id"]))
    return kreise, rechtecke, kapseln

class Router:
    def __init__(self, P, doc):
        self.kreise, self.rechtecke, self.kapseln = hindernisse(P, doc)
        self.eigene = []                              # schon geroutete Leitungen dieser Sitzung: (a, b, r, tag)

    def raster(self, x0, y0, ex, ey):
        """Gestrecktes Raster: Start (x0, y0) und Ziel (ex, ey) liegen genau auf Rasterpunkten (Schritt je Achse 45 bis 55 mm), kein Einrasten noetig."""
        def schritt(d):
            n = int(round(abs(d) / STEP))
            return d / n if n >= 1 and abs(d) > 0.5 else STEP
        self.sx, self.sy = abs(schritt(ex - x0)), abs(schritt(ey - y0))
        self.i0 = int(math.floor((-9000 - x0) / self.sx)); self.j0 = int(math.floor((-9500 - y0) / self.sy))
        self.NX = int(math.ceil((9000 - x0) / self.sx)) - self.i0 + 1; self.NY = int(math.ceil((7500 - y0) / self.sy)) - self.j0 + 1
        self.x0, self.y0 = x0, y0

    def xy(self, i, j): return (self.x0 + (i + self.i0) * self.sx, self.y0 + (j + self.j0) * self.sy)

    def eigene_kapseln(self, pfad, r, tag):
        for a, b in zip(pfad[:-1], pfad[1:]): self.eigene.append((a, b, r, tag))

    def _mark(self, B, bb, test):
        """Zellen im Rechteck bb = (xmin, ymin, xmax, ymax) markieren, fuer die test(x, y) wahr ist."""
        i_a = max(0, int(math.floor((bb[0] - self.x0) / self.sx)) - self.i0); i_b = min(self.NX - 1, int(math.ceil((bb[2] - self.x0) / self.sx)) - self.i0)
        j_a = max(0, int(math.floor((bb[1] - self.y0) / self.sy)) - self.j0); j_b = min(self.NY - 1, int(math.ceil((bb[3] - self.y0) / self.sy)) - self.j0)
        for i in range(i_a, i_b + 1):
            x = self.x0 + (i + self.i0) * self.sx; row = i * self.NY
            for j in range(j_a, j_b + 1):
                if test(x, self.y0 + (j + self.j0) * self.sy): B[row + j] = 1

    def gesperrt(self, r, z, tag):
        B = bytearray(self.NX * self.NY); self.N = bytearray(self.NX * self.NY)
        for cx, cy, R, _ in self.kreise:
            q = R + r + KLAR + 30; self._mark(B, (cx - q, cy - q, cx + q, cy + q), lambda x, y, cx=cx, cy=cy, q=q: math.hypot(x - cx, y - cy) < q)
        for cx, cy, yaw, l, w, _ in self.rechtecke:
            c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); hl, hw = l / 2 + r + KLAR + 30, w / 2 + r + KLAR + 30; q = math.hypot(hl, hw)
            self._mark(B, (cx - q, cy - q, cx + q, cy + q), lambda x, y, cx=cx, cy=cy, c=c, s=s, hl=hl, hw=hw: abs((x - cx) * c + (y - cy) * s) < hl and abs(-(x - cx) * s + (y - cy) * c) < hw)
        def kapsel(a, b, rr, klar):
            q = rr + r + klar
            if abs(a[2] - b[2]) > 1 and math.hypot(b[0] - a[0], b[1] - a[1]) < 1:          # senkrecht: Punkt, wenn er die Grabenhoehe kreuzt
                if min(a[2], b[2]) - rr - r - 10 <= z <= max(a[2], b[2]) + rr + r + 10:
                    self._mark(B, (a[0] - q, a[1] - q, a[0] + q, a[1] + q), lambda x, y: math.hypot(x - a[0], y - a[1]) < q)
                return
            zlo, zhi = min(a[2], b[2]), max(a[2], b[2])
            if z < zlo - rr - r - 15 or z > zhi + rr + r + 15: return                       # andere Hoehe: darf kreuzen
            dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy
            def t_(x, y):
                t = ((x - a[0]) * dx + (y - a[1]) * dy) / L2 if L2 > 0 else 0.0
                t = 0.0 if t < 0 else 1.0 if t > 1 else t
                return math.hypot(x - a[0] - t * dx, y - a[1] - t * dy) < q
            self._mark(B, (min(a[0], b[0]) - q, min(a[1], b[1]) - q, max(a[0], b[0]) + q, max(a[1], b[1]) + q), t_)
        for a, b, rr, _ in self.kapseln: kapsel(a, b, rr, KLAR)
        for a, b, rr, tg in self.eigene: kapsel(a, b, rr, KLAR if tg and tg == tag or math.hypot(b[0] - a[0], b[1] - a[1]) < 1 else 300.0 - rr - r)   # Steigleitungen: nur kollisionsfrei (R8 gilt fuer waagerechte Laeufe)   # R8: fremde parallele Leitungen >= 250 mm Achsabstand, Buendel-Partner nur kollisionsfrei
        for a, b, rr, tg in self.eigene + [(a_, b_, r_, "bestand") for a_, b_, r_, _ in self.kapseln]:   # R8 in anderer Hoehe und zu Bestandsleitungen: Naehe nur kreuzend (Kostenaufschlag)
            if tg and tg == tag or math.hypot(b[0] - a[0], b[1] - a[1]) < 1 or tg != "bestand" and abs((a[2] + b[2]) / 2 - z) < 1 or max(a[2], b[2]) > FZ: continue
            dx, dy = b[0] - a[0], b[1] - a[1]; L2 = dx * dx + dy * dy
            if L2 < 1: continue
            def t2(x, y, a=a, dx=dx, dy=dy, L2=L2):
                t = ((x - a[0]) * dx + (y - a[1]) * dy) / L2; t = 0.0 if t < 0 else 1.0 if t > 1 else t
                return math.hypot(x - a[0] - t * dx, y - a[1] - t * dy) < NAH
            self._mark(self.N, (min(a[0], b[0]) - NAH, min(a[1], b[1]) - NAH, max(a[0], b[0]) + NAH, max(a[1], b[1]) + NAH), t2)
        return B

    def route(self, start, ende, r, z, tag, frei=()):
        self.raster(start[0], start[1], ende[0], ende[1])
        B = self.gesperrt(r, z, tag)
        i0 = (-self.i0, -self.j0)
        i1 = (int(round((ende[0] - self.x0) / self.sx)) - self.i0, int(round((ende[1] - self.y0) / self.sy)) - self.j0)
        NX, NY = self.NX, self.NY
        for (px, py, rad) in frei:                                                           # Start- und Zielumgebung freigeben (eigene Steigleitungen)
            ia, ib = int((px - rad - self.x0) // self.sx) - self.i0, int((px + rad - self.x0) // self.sx) + 1 - self.i0
            ja, jb = int((py - rad - self.y0) // self.sy) - self.j0, int((py + rad - self.y0) // self.sy) + 1 - self.j0
            for i in range(max(0, ia), min(NX, ib + 1)):
                for j in range(max(0, ja), min(NY, jb + 1)):
                    x, y = self.xy(i, j)
                    if math.hypot(x - px, y - py) < rad: B[i * NY + j] = 0
        D = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        LAUF = 4                                                            # mindestens 4 Rasterschritte (~200 mm) zwischen zwei Boegen (R3, Bogenschenkel d40 74 mm)
        best = {}; pq = []
        for k in range(4): heapq.heappush(pq, (0.0, i0[0], i0[1], k, 0)); best[(i0[0], i0[1], k, 0)] = 0.0   # auch das erste Grabenstueck nach der Steigleitung braucht den Mindestlauf
        prev = {}; ziel = None
        while pq:
            c, x, y, k, n = heapq.heappop(pq)
            if c > best.get((x, y, k, n), 1e18): continue
            if (x, y) == i1 and n >= LAUF: ziel = (x, y, k, n); break
            for k2, (dx, dy) in enumerate(D):
                if k2 // 2 == k // 2 and k2 != k: continue                    # nicht umkehren
                if k2 != k and n < LAUF: continue                             # zu kurz seit dem letzten Bogen
                nx_, ny_ = x + dx, y + dy
                if not (0 <= nx_ < NX and 0 <= ny_ < NY) or B[nx_ * NY + ny_] and (nx_, ny_) != i1: continue
                n2 = min(LAUF, n + 1) if k2 == k else 1
                nc = c + STEP + (KNICK if k2 != k else 0.0) + (NAH_KOST if self.N[nx_ * NY + ny_] else 0.0)
                if nc < best.get((nx_, ny_, k2, n2), 1e18):
                    best[(nx_, ny_, k2, n2)] = nc; prev[(nx_, ny_, k2, n2)] = (x, y, k, n); heapq.heappush(pq, (nc, nx_, ny_, k2, n2))
        if not ziel: raise SystemExit("Router: kein Weg %s -> %s (Tag %s)" % ([round(v) for v in start], [round(v) for v in ende], tag))
        zellen = [ziel]
        while zellen[-1] in prev: zellen.append(prev[zellen[-1]])
        zellen.reverse()
        pts = [self.xy(z_[0], z_[1]) for z_ in zellen]
        ecken = [pts[0]] + [pts[i] for i in range(1, len(pts) - 1) if (round(pts[i][0] - pts[i - 1][0], 3), round(pts[i][1] - pts[i - 1][1], 3)) != (round(pts[i + 1][0] - pts[i][0], 3), round(pts[i + 1][1] - pts[i][1], 3))] + [pts[-1]]
        ecken = [list(p) for p in ecken]; ecken[0] = [start[0], start[1]]; ecken[-1] = [ende[0], ende[1]]
        return [(p[0], p[1], z) for p in ecken]

# ---------------------------------------------------------------- Ziele (Port-Stuecke im Modell, gemessen aus den Instanzmatrizen)
def welt(m, p): return (m[0] * p[0] + m[1] * p[1] + m[2] * p[2] + m[3], m[4] * p[0] + m[5] * p[1] + m[6] * p[2] + m[7], m[8] * p[0] + m[9] * p[1] + m[10] * p[2] + m[11])
def richt(m, v): return (m[0] * v[0] + m[1] * v[1] + m[2] * v[2], m[4] * v[0] + m[5] * v[1] + m[6] * v[2], m[8] * v[0] + m[9] * v[1] + m[10] * v[2])

def ziele(P):
    cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
    mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
    lay = json.load(open(os.path.join(ROOT, "data", "layout.json"), encoding="utf-8"))
    Z = {}
    # K44: Pool-Verteiler Muffe A zeigt schraeg (Az 65): Port-Stueck 150 mm, Bogen nach oben, -X ueber den Rand, Steigleitung aussen am Becken
    m = mv["Luftverteiler_4:1"]; o = welt(m, (0, 0, 0)); d = richt(m, (-1, 0, 0)); q = (o[0] + d[0] * 150, o[1] + d[1] * 150)
    Z["K44"] = dict(s=(q[0] + 150.0, q[1]), auf=[(q[0] + 150.0, q[1], 1260.0), (q[0], q[1], 1260.0), (q[0], q[1], o[2]), o], ende="muffe", anschluss=["Zentralpool"])
    # K40: Schwimmerventil Port A (Muffe) zeigt radial nach aussen (Az -10): Port-Stueck 280 mm
    m = mv["Schwimmerventil_Pool:1"]; o = welt(m, (0, 0, 0)); d = richt(m, (-1, 0, 0)); q = (o[0] + d[0] * 280, o[1] + d[1] * 280)
    Z["K40"] = dict(s=q, auf=[(q[0], q[1], o[2]), o], ende="muffe", anschluss=["Zentralpool"])
    # K45/K46: Biofilter-Deckel Luftanschluss d16 (tank.md, Bauteil x 220 / z 1676), von oben; Steigleitung neben dem Tank (Abstand >= Tankradius 465 + 42)
    for k, nm, sx in (("K45", "Tank_gross:1", None), ("K46", "Tank_gross_t3:1", None)):
        m = mv[nm]; p = welt(m, (220, 0, 1676)); c = (m[3], m[7]); dx, dy = p[0] - c[0], p[1] - c[1]; need = 465 + 12.5 + 30
        cand = []
        for ax, sg in ((1, -1), (1, 1), (0, 1), (0, -1)):            # Steigleitung in +-Y oder +-X vom Port aus
            if ax == 1:
                if abs(dx) >= need: continue
                off = math.sqrt(need * need - dx * dx) * sg; s = (p[0], c[1] + off); L = abs(s[1] - p[1])
            else:
                if abs(dy) >= need: continue
                off = math.sqrt(need * need - dy * dy) * sg; s = (c[0] + off, p[1]); L = abs(s[0] - p[0])
            cand.append((L, s))
        Z[k] = dict(kandidaten=[s for _, s in sorted(cand)], port=p, ende="offen", anschluss=[nm])
    # K49: Drittbecken Tuelle (Bauteil x 0 / y -530 / z 1085, zeigt -Y), K41: Stutzen K41 Muffe d20 (x 530, zeigt +X)
    m = mv["Becken_Dritt:1"]; t49 = welt(m, (0, -530, 1085)); t41 = welt(m, (530, 0, 1085))
    Z["K49"] = dict(s=(t49[0], t49[1] - 250.0), auf=[(t49[0], t49[1] - 250.0, t49[2]), t49], ende="stutzen", anschluss=["Drittbecken"])
    Z["K41"] = dict(s=(t41[0] + 250.0, t41[1]), auf=[(t41[0] + 250.0, t41[1], t41[2]), t41], ende="muffe", anschluss=["Drittbecken"])
    # K51: Zweitbecken ohne Stutzen: Steigleitung aussen (-X), ueber den Rand, im Wasser 300 mm unter dem Spiegel offen (Ausstroemer-Platzhalter fehlt, Werkstatt)
    a2 = math.radians(P["pool2_az"]); c2 = (P["pool2_r"] * math.cos(a2), P["pool2_r"] * math.sin(a2)); r2 = lay["pool2"]["d"] / 2 + 60
    s51 = (c2[0] - r2 - 150.0, c2[1]); i51 = (c2[0] - r2 + 250.0, c2[1])
    Z["K51"] = dict(s=s51, auf=[(s51[0], s51[1], FZ + P["pool_rim"] + 100.0), (i51[0], i51[1], FZ + P["pool_rim"] + 100.0), (i51[0], i51[1], FZ + lay["pool2"]["water_z"] - 300.0)], ende="offen", anschluss=["Zweitbecken"])
    # K52: Fuellstelle vor dem Puffer (Bedienseite puffer_front), Steigleitung mit Kugelhahn d25 oben; das Fass wird von Hand mit Schlauch gefuellt (Netz K52)
    m = mv["Puffer_Klein:1"]; af = math.radians(P["puffer_front"]); s52 = (m[3] + 520 * math.cos(af), m[7] + 520 * math.sin(af))
    Z["K52"] = dict(s=s52, auf=[(s52[0], s52[1], FZ + 900.0)], ende="r:KH_K52", anschluss=["Puffer_Klein:1"], hahn=(s52[0], s52[1], FZ + 900.0))
    # K39: Anfang am Ende des Platzhalters T10_Zulaufrohr (Hausanschluss aussen, gen_dome.rohr_fn P2 = 6120 / Az -58, Rohr liegt auf dem Boden)
    a = math.radians(-58.0); Z["K39"] = dict(s=(6120 * math.cos(a), 6120 * math.sin(a)), z0=FZ + P["pipe_d"] / 2)
    return Z

# ---------------------------------------------------------------- Trassen
def band(a, b, aussen):
    zr = max(a[2], b[2]) - FZ
    if max(a[2], b[2]) <= FZ - 99: return "U"
    if aussen: return "AU"
    return "W" if zr <= 1000 else "WH"

def ausserhalb(P, x, y):
    ap = P["dome_base_d"] / 2 * math.cos(math.radians(18))
    return max(x * math.cos(math.radians(P["door_edge_az"] + 36 * k)) + y * math.sin(math.radians(P["door_edge_az"] + 36 * k)) for k in range(10)) > ap

def eintrag(P, tid, kante, d, farbe, pfad, start, ende, linie, anschluss, notiz, buendel=None):
    pf = [list(map(lambda v: round(v, 2), p)) for p in pfad]
    keep = [pf[0]]
    for i in range(1, len(pf) - 1):
        a, b, c = keep[-1], pf[i], pf[i + 1]
        u = [b[j] - a[j] for j in range(3)]; w = [c[j] - b[j] for j in range(3)]
        cr = [u[1] * w[2] - u[2] * w[1], u[2] * w[0] - u[0] * w[2], u[0] * w[1] - u[1] * w[0]]
        if math.sqrt(sum(v * v for v in cr)) < 1e-6 * (1 + math.dist(a, b) * math.dist(b, c)) and sum(u[j] * w[j] for j in range(3)) > 0: continue
        if math.dist(a, b) < 0.5: continue
        keep.append(b)
    keep.append(pf[-1]); pf = keep
    bd = [band(a, b, ausserhalb(P, (a[0] + b[0]) / 2, (a[1] + b[1]) / 2)) for a, b in zip(pf[:-1], pf[1:])]
    e = {"id": tid, "kante": kante, "dn": d, "farbe": farbe, "start": start, "ende": ende, "baender": bd, "anschluss": anschluss, "pfad": pf, "linie": linie, "notiz": notiz}
    if buendel: e["buendel"] = buendel
    return e

def bauen(P, doc):
    g = gruppe(P); Zl = ziele(P); out_t, out_r, out_ts, out_teile = [], [], [], []
    vx, vy, vz = g["vert"]
    # ---- Geblaese: Rueckschlagventil d20 auf dem Austritt, Straenge zum T, Reduziermuffe d40/d20, Hauptleitung d40 in die Muffe A des Verteilers
    lrsv = 82.0; t20 = LT.DEPTH[20]
    rsv_b = []
    for i, (ax, ay, az) in enumerate(g["austritt"]):
        pa = (ax - t20, ay, az)                                             # Muffenebene A: Zapfen steckt t in der Muffe, Austritt zeigt +X
        out_r.append({"id": "RSV_G%d" % (i + 1), "art": "teil", "datei": "lt_rueckschlagventil_d20", "pos_a": list(pa), "dir": [1.0, 0.0, 0.0], "d_gross": 20, "d_klein": 20, "farbe": "gruen", "linie": "luft_b",
                      "notiz": "Rueckschlagventil d20 auf dem Geblaese-Austritt %s (N+1: stehendes Geblaese zieht keine Luft zurueck)" % "AB"[i]})
        rsv_b.append((pa[0] + lrsv, ay, az))
    xt = g["x_t"]; ta = (xt, rsv_b[1][1], vz)
    DN_G = "Geblaese-Austritt d20 (Bauteilblatt geblaese_luft), zwei Straenge ueber T d20, dann Reduziermuffe d40/d20 auf die Hauptleitung d40 (K44)"
    out_t.append(eintrag(P, "K44-GA", "K44", 20, "gruen", [rsv_b[0], (xt, rsv_b[0][1], vz), ta], "r:RSV_G1", "t:TG", "luft_b", [], "Geblaese A: Rueckschlagventil -> T d20", ))
    out_t.append(eintrag(P, "K44-GB", "K44", 20, "gruen", [rsv_b[1], ta], "r:RSV_G2", "t:TG", "luft_b", [], "Geblaese B: Rueckschlagventil -> T d20 (Durchgang)"))
    lred = LT.ports("lt_reduzierung_d40_d20")[1][1][2]; ra = (g["red_a"], vy, vz)
    out_t.append(eintrag(P, "K44-GT", "K44", 20, "gruen", [ta, (ra[0] - lred, vy, vz)], "t:TG", "r:RED_G", "luft_b", [], "T d20 -> Reduziermuffe d40/d20"))
    out_r.append({"id": "RED_G", "pos_a": list(ra), "dir": [-1.0, 0.0, 0.0], "d_gross": 40, "d_klein": 20, "farbe": "gruen", "linie": "luft_b"})
    out_t.append(eintrag(P, "K44-GV", "K44", 40, "gruen", [ra, (vx, vy, vz)], "r:RED_G", "muffe", "luft_b", [], "Reduziermuffe -> Muffe A Hauptverteiler luftverteiler_6 (Schleife Z 1110 ueber dem Spiegel)"))
    out_ts.append({"id": "TG", "pos": list(ta), "d": 20, "ports": [{"trasse": "K44-GA", "ende": "ende", "d": 20}, {"trasse": "K44-GB", "ende": "ende", "d": 20}, {"trasse": "K44-GT", "ende": "start", "d": 20}], "linie": "luft_b"})
    for e in out_t:
        if e["dn"] == 20: e["dn_abweichung"] = DN_G
    # ---- Router-Starts
    st = {}
    for x, d, k in ABG:
        tip = (vx + x, vy, vz - 74.0)
        if k is None:
            out_teile.append({"id": "KAPPE_V6_6", "datei": "lt_kappe_d20", "pos": [tip[0], tip[1], tip[2] + LT.DEPTH[20]], "z": [0.0, 0.0, -1.0], "x": [1.0, 0.0, 0.0], "farbe": "gruen", "linie": "luft_b",
                              "notiz": "Kappe auf Abgang 6 (K47/K48 optional, Absetzer ohne Luftanschluss im Bauteil: OFFEN Werkstatt)"})
            continue
        st[k] = dict(d=d, src=[tip], start="stutzen", z=Z_LUFT if k in ("K44", "K45") else Z_LUFT_K, farbe="gruen", linie="luft_b", buendel="V6")
    sx_, sy_, _, _ = g["station"]
    stn = {"K39": ((-800, 0), (-1, 0)), "K40": ((900, 0), (1, 0)), "K41": ((560, 250), (0, 1)), "K52": ((700, -250), (0, -1))}
    cy_, sy__ = math.cos(math.radians(g["station"][3])), math.sin(math.radians(g["station"][3]))
    for k, ((lx, ly), (dx, dy)) in stn.items():
        wx, wy = lx * cy_ - ly * sy__, lx * sy__ + ly * cy_; wdx, wdy = dx * cy_ - dy * sy__, dx * sy__ + dy * cy_
        tip = (sx_ + wx, sy_ + wy, FZ + 839.5); q = (tip[0] + wdx * 200, tip[1] + wdy * 200, tip[2])
        st[k] = dict(d=25 if k != "K41" else 20, src=[tip, q], start="stutzen", z=Z_FRISCH if k != "K39" else Z_K39, farbe="hellblau", linie="frisch", buendel=None)
    # ---- Reihenfolge: mehrere Reihenfolgen probieren, Bewertung = Laenge + 2000 mm je Bogen (R5), beste gewinnt
    import itertools, check_leitungen as CL
    FEHL = []
    welt_ = CL.load_world()
    def steiger_frei(x, y, r, z1, eigen):
        """Steigleitung (x, y) von Grabenhoehe bis z1 gegen Bauteile (Pumpen, Tanks, Puffer, Feinfilter, Becken), ausser dem eigenen Ziel."""
        for o in welt_.obst:
            if o["name"] in eigen or o["kind"] == "tischfuss": continue
            for z in range(int(Z_LUFT), int(z1) + 1, 50):
                if CL.dist_3d(o, x, y, z) < r + KLAR: return False
        return True
    for k in ("K45", "K46"):
        Zl[k]["kandidaten"] = [s for s in Zl[k]["kandidaten"] if steiger_frei(s[0], s[1], 12.5, 2250.0, Zl[k]["anschluss"])]
    def versuch(reihe):
        ro = Router(P, doc)
        for k in st:                                                        # Start- und Ziel-Steigleitungen aller Leitungen vorab als eigene Hindernisse (gleiches Buendel nur kollisionsfrei)
            s = st[k]; a0 = s["src"][-1]; ro.eigene_kapseln(list(s["src"]) + [(a0[0], a0[1], s["z"])], s["d"] / 2.0, s["buendel"] or k)
            for zs in (Zl[k].get("kandidaten") or [Zl[k]["s"]])[:1]:
                ro.eigene.append(((zs[0], zs[1], s["z"]), (zs[0], zs[1], 2250.0), s["d"] / 2.0, "ziel:" + k))
        erg, summe = {}, 0.0
        for k in reihe:
            s = st[k]; zt = s["z"]; r = s["d"] / 2.0; zz = Zl[k]
            a0 = s["src"][-1]; start2 = (a0[0], a0[1])
            ro.eigene = [e for e in ro.eigene if e[3] not in (k, "ziel:" + k)]   # eigene Start- und Ziel-Steigleitung nicht als Hindernis
            last = None
            for ziel in (zz.get("kandidaten") or [zz["s"]]):
                try:
                    wege = ro.route(start2, ziel, r, zt, s["buendel"], [(start2[0], start2[1], r + 60), (ziel[0], ziel[1], r + 60)]); last = ziel; break
                except SystemExit: pass
            if last is None:
                FEHL.append(k); return None
            if k in ("K45", "K46"):
                p_ = zz["port"]; auf = [(last[0], last[1], 2250.0), (p_[0], p_[1], 2250.0), (p_[0], p_[1], p_[2] + 20.0)]
            elif k == "K39": auf = []
            else: auf = zz["auf"]
            pfad = list(s["src"]) + [(a0[0], a0[1], zt)] + [(w[0], w[1], zt) for w in wege[1:]]
            if auf: pfad += [(wege[-1][0], wege[-1][1], auf[0][2])] + list(auf[1:])
            ro.eigene_kapseln(pfad, r, s["buendel"] or k)
            erg[k] = pfad; summe += sum(math.dist(a, b) for a, b in zip(wege[:-1], wege[1:])) + 2000.0 * (len(wege) - 2)
        return summe, erg
    frisch = ["K40", "K41", "K52", "K39"]
    folgen = [list(a) + list(b) for a in itertools.permutations(["K44", "K45"]) for b in itertools.permutations(["K46", "K51", "K49"])]
    folgen += [f[2:] + f[:2] for f in folgen]
    beste_l = None
    for perm in folgen:                                                     # Stufe 1: Luft allein
        v = versuch(list(perm))
        if v and (beste_l is None or v[0] < beste_l[0]): beste_l = (v[0], list(perm))
    if not beste_l: raise SystemExit("Router: keine Luft-Reihenfolge ohne Sackgasse; scheitert an %s" % sorted(set(FEHL)))
    beste = None
    for perm in itertools.permutations(frisch):                            # Stufe 2: Frischwasser zur besten Luft-Reihenfolge
        v = versuch(beste_l[1] + list(perm))
        if v and (beste is None or v[0] < beste[0]): beste = (v[0], v[1], tuple(beste_l[1]) + perm)
    if not beste: raise SystemExit("Router: keine Reihenfolge ohne Sackgasse; scheitert an %s" % sorted(set(FEHL)))
    print("Reihenfolge Luft", beste[2], "Bewertung %.0f" % beste[0])
    for k in ["K44", "K45", "K46", "K51", "K49"] + frisch:
        s = st[k]; zz = Zl[k]; pfad = beste[1][k]; zt = s["z"]
        if k == "K39":                                                      # Fliessrichtung Hausanschluss -> Station: Pfad umdrehen, Anfang am T10-Ende auf dem Boden
            z0 = zz["z0"]; pfad = list(reversed(pfad)) ; pfad = [(zz["s"][0], zz["s"][1], z0)] + pfad
            start, ende = "offen", "stutzen"
        else:
            start, ende = s["start"], zz["ende"]
        if k == "K52":
            h = zz["hahn"]; out_r.append({"id": "KH_K52", "art": "kugelhahn", "pos_a": list(h), "dir": [0.0, 0.0, 1.0], "d_gross": 25, "d_klein": 25, "farbe": "hellblau", "linie": "frisch",
                                          "notiz": "Zapfhahn d25 vor dem Puffer: Fass wird von Hand mit Schlauch gefuellt (Netz K52, kein Dauerfluss)"})
        if k == "K39":
            notiz = "Frischwasser Hausanschluss (Ende Platzhalter T10_Zulaufrohr, Az -58) -> Aktivkohle-Station Eingang, Graben Z %g" % zt
            anschl = []
        else:
            notiz = {"K44": "Luft Hauptverteiler Abgang 1 -> Pool-Verteiler Muffe A (Port-Stueck 150 mm, ueber den Rand)", "K45": "Luft -> Biofilter 1 Deckel (Uebergang d25 auf Luftschlauch 16 offen: Tuellen-Reduzierung fehlt, Werkstatt)",
                     "K46": "Luft -> Biofilter 2 Deckel (Uebergang d25 auf Luftschlauch 16 offen: Tuellen-Reduzierung fehlt, Werkstatt)", "K49": "Luft -> Drittbecken Tuelle ID16 (d20 statt Schlauch, Uebergang wie Bauteil)",
                     "K51": "Luft -> Zweitbecken: ueber den Rand, offenes Ende 300 mm unter dem Spiegel (Ausstroemer-Platzhalter fehlt, Werkstatt)", "K40": "Frischwasser Station -> Schwimmerventil Port A (Port-Stueck 280 mm)",
                     "K41": "Frischwasser Station -> Drittbecken Stutzen K41", "K52": "Frischwasser Station -> Zapfhahn vor dem Puffer"}[k]
            anschl = zz.get("anschluss", [])
        out_t.append(eintrag(P, k + ("-V" if k in ("K44",) else ""), k, s["d"], s["farbe"], pfad, start, ende, s["linie"], anschl, notiz, s["buendel"]))
        if k == "K44": out_t[-1]["schwanenhals"] = True                    # Leitungsordnung Ausnahme 5: Schwanenhals ueber den Beckenrand an die schraege Muffe A des Pool-Verteilers
    return out_t, out_r, out_ts, out_teile

def schreiben():
    raise SystemExit("Abgeloest durch N-UNIFY-AUTOBAHN U7 (D141): schreibt Leitungen des Altbestands, die der eine Kreislauf nach der Quelle nicht hat. Die Lagefunktionen bleiben fuer gen_dome.py.")
    P = P_(); pfad = os.path.join(ROOT, "data", "leitungstrassen.json")
    doc = json.load(open(pfad, encoding="utf-8"))
    alt = lambda e: e.get("linie") in ("luft_b", "frisch")
    doc["trassen"] = [t for t in doc["trassen"] if not alt(t)]; doc["r_stuecke"] = [t for t in doc["r_stuecke"] if not alt(t)]
    doc["t_stuecke"] = [t for t in doc["t_stuecke"] if not alt(t)]; doc["teile"] = [t for t in doc.get("teile", []) if not alt(t)]
    t, r, ts, te = bauen(P, doc)
    doc["trassen"] += t; doc["r_stuecke"] += r; doc["t_stuecke"] += ts; doc["teile"] += te
    open(pfad, "w", encoding="utf-8", newline="").write(json.dumps(doc, ensure_ascii=False, indent=1) + chr(10))
    for e in t: print(e["id"], e["dn"], len(e["pfad"]) - 1, "Teilstuecke", round(sum(math.dist(a, b) for a, b in zip(e["pfad"][:-1], e["pfad"][1:]))), "mm", e["baender"])

if __name__ == "__main__":
    schreiben()
