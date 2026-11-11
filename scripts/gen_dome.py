"""Erzeugt das SolidCraft-Befehlsskript fuer designs/dome.sc (Stufe 1-4 = Plan-Schritte 2-5).
Aufruf: python gen_dome.py <stufe> <out.json> [--variante a_plus|ring_b2]. Masse in mm; alle Annahmen stehen in P."""
import json, math, os, sys
from geo import build
import leitungen as LTG   # M10-S2a
import variante           # N-VARIANTEN V1b: Kreislauf-Variante (Schalter --variante, Umgebung KREISLAUF_VARIANTE, Standard params.json)
V = variante.aktiv()      # a_plus (Standard, Pfade wie bisher) | ring_b2

P = variante.parameter(V)   # Zahlen stehen einmal in data/params.json (Herkunft, Reife dort); U4/D119: Eintraege mit `varianten`/`varianten_werte` je Variante (a_plus = Werte vor U3, ring_b2 = Soll der Oasis-Quelle)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cmds = []
names = []
def add(c, **p):
    cmds.append({"command": c, "params": p})
    if p.get("body_name"): names.append(p["body_name"])

COLORS = [  # (Namenspraefix, Farbe, Deckkraft) - Schicht 1
    ("T1_", "#b9c0c8", 1), ("T3_", "#cfcfca", 1), ("T13_", "#7a5c3a", 1), ("T4_", "#1c1c1c", 1), ("T5_Wasser", "#3c8ed0", 0.85), ("T6_Wasser", "#3c8ed0", 0.85),
    ("T7_Plattform", "#9a9a96", 1), ("T7_Pumpe", "#555a60", 1), ("T5_Stutzen", "#2f6fb0", 1), ("T5_", "#93b49a", 1), ("T6_", "#93b49a", 1), ("T7_", "#93b49a", 1), ("T8_", "#f3f3f1", 1), ("T9_", "#ffffff", 1),
    ("T10_Zulaufrohr", "#5fa8e0", 1), ("T10_Schlauch", "#8cc8f0", 1), ("T11_", "#8b9096", 1), ("T12_", "#4c9a3c", 1)]

def colors():
    left = list(names)
    for pre, col, op in COLORS:
        grp = [n for n in left if n.startswith(pre)]
        left = [n for n in left if n not in grp]
        if grp: add("appearance.assign", bodies=grp, color=col, opacity=op)
def rot(x, y, a): c, s = math.cos(a), math.sin(a); return (x*c - y*s, x*s + y*c)
def pol(r, az): a = math.radians(az); return (r*math.cos(a), r*math.sin(a))

def params():
    for k, v in P.items():
        if isinstance(v, bool) or not isinstance(v, (int, float)): continue   # Text-Schalter (z. B. kreislauf_variante "a_plus", d0819fe) sind keine CAD-Ausdruecke
        add("parameters.add", name=k, expression=str(v), comment="dome-build Parameter")

def rect_body(name, cx, cy, z0, az_deg, along, across, h, op="new", targets=None):
    """Quader um (cx,cy), Laengsachse 'along' in Richtung az, ab Hoehe z0 (rotierte Skizzenebene)."""
    a = math.radians(az_deg)
    xd = [round(math.cos(a), 6), round(math.sin(a), 6), 0]
    yd = [round(-math.sin(a), 6), round(math.cos(a), 6), 0]
    add("sketch.create", plane={"origin": [cx, cy, z0], "x_dir": xd, "y_dir": yd}, name=name+"_sk")
    add("sketch.rectangle.center", center=[0, 0], corner=[along/2, across/2])
    add("sketch.finish")
    if op == "new": add("solid.extrude", distance=h, operation="new", name=name, body_name=name)
    else: add("solid.extrude", distance=h, operation=op, targets=targets, name=name)

def component_file(fname, cls, assembly, fn):
    """Bauteilklasse als eigene Datei designs/components/<fname>.sc bauen (fn erzeugt Koerper in Weltlage) und im Dom verknuepfen (Instanz im Ursprung)."""
    global cmds, names
    saved, savedn = cmds, names; cmds, names = [], []
    fn(); colors()
    data = cmds; cmds, names = saved, savedn
    tmp = os.path.join(ROOT, "scripts", "_comp.json"); json.dump({"commands": data}, open(tmp, "w"))
    out = os.path.join(ROOT, "designs", "components", fname + ("" if V == "a_plus" else "-" + V) + ".sc")   # V1b: B2 schreibt eigene Dateien (Graeben in erdflaeche haengen an der Variante); A+ unveraendert
    r = __import__("subprocess").run([r"C:\Program Files\SolidCraft\solidcraft-cli.exe", "run", tmp, "--save", out, "--quiet"], capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"Komponente {fname} fehlgeschlagen: {r.stderr[-400:]}{r.stdout[-400:]}")
    os.remove(tmp)
    act(assembly); add("component.insert_design", path=out.replace("\\", "/"), name=cls)

ASSEMBLIES = ["01_Layout", "02_Gelaende", "03_Kuppel", "04_Wasserbecken", "05_Beete", "06_NFT", "07_Tanks", "08_Leitungen", "09_Technik", "10_Pflanzen", "11_Referenz", "12_Huelle", "13_Messstellen", "14_Technik_E13"]   # 14: Technikgruppe "vorlaeufig, E13" (M10-S5-LUFT-B, D81)

def act(name):
    """Baugruppe aktivieren: neue Koerper/Instanzen entstehen darin (Wurzel bleibt frei von losen Koerpern)."""
    add("component.activate", component=name)

def place_matrix(cls, path, mats):
    """Komponente einmal verknuepfen und je 12er-Matrix eine Instanz setzen (erst alle Kopien am Ursprung, dann absolut verschieben)."""
    add("component.insert_design", path=path.replace("\\", "/"), name=cls)
    for _ in range(len(mats) - 1): add("occurrence.copy", component=cls)
    for i, mat in enumerate(mats, 1): add("occurrence.move", occurrence=f"{cls}:{i}", matrix=mat, tolerance=1e-6, move_grounded=True)

def place_struts(segs):
    """D91 (N-VERBINDER Montage): Streben als Rundrohr-Instanzen strebe_a/strebe_b (scripts/components/strebe.py), mittig zwischen den
    Rohrmuendern der zwei Scheren (scripts/knoten_montage.py); X = Kuppel aussen, Y = Nasenrichtung (Gegenloecher)."""
    import knoten_montage as KM
    LEN = KM.rohrlaengen(segs, ROT)   # gleiche Rohrlaenge wie scripts/components/strebe.py
    _, _, streben, _ = KM.montage(segs, ROT)
    base_z = min(min(A[2], B[2]) for A, B in segs)   # Kuppelmitte (0, 0, cz): Basisknoten liegen auf cz
    moves = {"A": [], "B": []}
    for st in streben:
        m, _ = KM.strebe_matrix(st, [0.0, 0.0, base_z], LEN[st["typ"]][0]); moves[st["typ"]].append(m)
    for key in ("A", "B"):
        place_matrix(f"Strebe_{key}", os.path.join(ROOT, "designs", "components", f"strebe_{key.lower()}.sc"), moves[key])

ERDE_SEITE = 19000 if V == "ring_b2" else 15000   # U4 (D123): Sumpf-Gruben im Vorbau reichen bis y -9032; die Erdflaeche waechst nur in ring_b2 (A+ bleibt 15000)

def erde_fn(sock_z):
    add("solid.box", length=ERDE_SEITE, width=ERDE_SEITE, height=2600, center=[0, 0, sock_z - 1300], operation="new", name="T13_Erde", body_name="T13_Erde")
    # U4 (D93, D118): ring_b2 sperrt nur den Fischtank in den Boden; Anzucht- und Lebendfutterbecken stehen auf dem Boden (keine Aussparung), Beete auf dem Flur (keine Taschen)
    for nm, src, wall, depth in ((("Pool", LAYOUT["pool"], P["wall"], P["pool_depth"]),) if V == "ring_b2" else (("Pool", LAYOUT["pool"], P["wall"], P["pool_depth"]), ("Zweitbecken", LAYOUT["pool2"], 60, P["pool2_depth"]), ("Dritt", POOL3, 60, P["pool3_depth"]))):
        x, y, d_out, z_bot, total = pool_dims(sock_z, src, wall, depth, nm)
        add("solid.cylinder", diameter=d_out + 20, height=total + 10, base=[x, y, z_bot - 5], operation="cut", targets=["T13_Erde"], name=nm + "_Aussparung")
    if V == "ring_b2":   # U4 (D105): Sumpf-Gruben (Wanne aussen 1329 x 3179, Boden -602 unter dem Fussboden, Deckel buendig), Spiel +20 wie bei den Becken
        for k, (x, y, yaw, long_az) in enumerate(sumpf_orte(), 1):
            rect_body(f"T101_Grube_{k:02d}", x, y, sock_z - SUMPF_WANNE_TIEFE - 5, long_az, SUMPF_WANNE_L + 20, SUMPF_WANNE_B + 20, SUMPF_WANNE_TIEFE + 6, op="cut", targets=["T13_Erde"])
    for k, b in enumerate([] if V == "ring_b2" else LAYOUT["ibc_beds"], 1):
        x, y = bed_xy(b); ln, wd = bed_dims(k, b)
        rect_body(f"T9_Tasche_{k:02d}", x, y, sock_z + b["z0"] - 200, bed_yaw(b), ln + 20, wd + 20, -b["z0"] + 201, op="cut", targets=["T13_Erde"])
    if V == "ring_b2":   # U4 (D122): die Wannen stehen auf dem Flur; nur die Auslass-Armaturen (Reduktion bis -80) reichen unter den Flur: kleine Tasche 160 x 160 x 85 je Beet statt der Wannengrube
        for k, b in enumerate(LAYOUT["ibc_beds"], 1):
            x, y = bed_xy(b); yaw = bed_yaw(b); u, v = BEET_AUSLASS["aussen" if "plants" in b else "innen"]; c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
            rect_body(f"T9_Auslass_{k:02d}", round(x + u * c - v * s, 1), round(y + u * s + v * c, 1), sock_z - BEET_AUSLASS_TIEFE - 5, yaw, 160, 160, BEET_AUSLASS_TIEFE + 6, op="cut", targets=["T13_Erde"])
    for k, (x, y, yaw) in enumerate(feinfilter_orte(), 1):   # M10-S1: Feinfilter-Gruben (Boden = Standflaeche), Drehung wie der Filter
        rect_body(f"T55_Grube_{k:02d}", x, y, sock_z + P["ff_z"], yaw, P["ff_grube_l"], P["ff_grube_w"], -P["ff_z"] + 1, op="cut", targets=["T13_Erde"])
    doc = LTG.laden_variante(V)   # M10-S2a: Graeben der Unterflur-Leitungen (Bettung je Seite lt_graben_zuschlag/2), Steigleitungen als Schacht
    for g in (LTG.graben(doc, sock_z) if doc else []):
        if g[0] == "box": rect_body(g[1], g[2], g[3], g[4], g[5], g[6], g[7], g[8], op="cut", targets=["T13_Erde"])
        else: add("solid.cylinder", diameter=g[5], height=g[6], base=[g[2], g[3], g[4]], operation="cut", targets=["T13_Erde"], name=g[1])

def feinfilter_orte():
    """M10-S1 (D72, Bedienzone-Regel): Feinfilter Ost A (Linie 1) und West B (Linie 2); Rueckgabe [(x, y, yaw_grad)]. Drehung nach scripts/place_feinfilter_zone.py: Bauteil-X = Einlauf zu Auslauf, Bedienseite -Y."""
    return [(P["ff_a_x"], P["ff_a_y"], P["ff_a_yaw"]), (P["ff_b_x"], P["ff_b_y"], P["ff_b_yaw"])]

def feinfilter(fz):
    """M10-S1: 2 x T55 (designs/components/feinfilter.sc) in 09_Technik; Ursprung = Mitte Standflaeche am Boden, Z = Flur + ff_z (-496 relativ, im Modell absolut -96); Gruben siehe erde_fn."""
    place_instances("Feinfilter", os.path.join(ROOT, "designs", "components", "feinfilter.sc"), [(x, y, fz + P["ff_z"], yaw) for x, y, yaw in feinfilter_orte()], "09_Technik")

def ring_fn(sock_z):
    rs = P["dome_base_d"]/2 + P["sock_w"]; ri = P["dome_base_d"]/2
    ring = lambda r: [[round(r*math.cos(math.radians(36*i + 18)), 2), round(r*math.sin(math.radians(36*i + 18)), 2)] for i in range(10)]
    add("sketch.create", plane={"origin": [0, 0, sock_z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="T3_Sockel_sk")
    add("sketch.line", points=ring(rs), closed=True)
    add("sketch.line", points=ring(ri), closed=True)
    add("sketch.finish")
    add("solid.extrude", distance=P["ring_h"], operation="new", name="T3_Sockel", body_name="T3_Sockel")
    gx, gy = pol(P["dome_base_d"]/2*math.cos(math.radians(18)) + 150, P["door_edge_az"])
    rect_body("T3_Tuerluecke", round(gx, 1), round(gy, 1), sock_z - 10, P["door_edge_az"] + 90, P["door_w"] + 200, 700, P["ring_h"] + 20, op="cut", targets=["T3_Sockel"])

def station_pose():
    """D62: Puffer-Station als Technikvorbau AUSSERHALB der Plane rechts neben der Tuer (Flaeche door_edge_az + 36): Front (Y -691,5) zur Kuppel im Abstand `station_out_gap` zur Aussenkante des Fundamentrings. Station-KS: X = -t, Y radial nach aussen. Rueckgabe (x, y, az)."""
    a = P["door_edge_az"] + 36.0; ar = math.radians(a); n = (math.cos(ar), math.sin(ar))
    r = (P["dome_base_d"]/2 + P["sock_w"]) * math.cos(math.radians(18)) + P["station_out_gap"] + 691.5
    return r * n[0], r * n[1], a

def puffer_station(fz):
    """M8 (D46, W28, D62): Puffer-Station T81 (2 gestapelte IBC) als Vorbau aussen; Station-KS: X = -t, Y radial nach aussen (Rueckseite/Plattform von der Kuppel weg)."""
    x, y, a = station_pose()
    place_instances("Puffer_Station", os.path.join(ROOT, "designs", "components", "puffer_station.sc"), [(round(x, 1), round(y, 1), fz, a - 90.0)], "09_Technik")

def puffer_pose():
    """D66: Puffer klein (T82, 700 x 700 x 1203) im Dom, Front (lokal -Y, Pumpen/Fass herausziehen) zeigt in Richtung `puffer_front`; Rueckgabe (x, y, yaw, X, Y) mit Achsen im Modellrahmen. Lage aus der Abstandssuche (D70)."""
    x, y = P["puffer_r"] * math.cos(math.radians(P["puffer_az"])), P["puffer_r"] * math.sin(math.radians(P["puffer_az"])); yaw = P["puffer_front"] + 90.0; a = math.radians(yaw)
    return x, y, yaw, (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))

def puffer_klein(fz):
    x, y, yaw, _, _ = puffer_pose()
    place_instances("Puffer_Klein", os.path.join(ROOT, "designs", "components", "puffer_klein.sc"), [(round(x, 1), round(y, 1), fz, yaw)], "09_Technik")

def messstellen(fz):
    """M-SETZEN Schritt 5 (D65, W35): Halter und Sonden-Platzhalter an gesetzten Bauteilen (Pool, Zweitbecken, Drittbecken, Puffer-Messzelle, Leckagesonden); Lage nach Ortsangabe in data/messstellen.json (Annahme A).
    Beckenrand: H_TAUCH (X vom Rohr ueber den Rand, Klemme auf dem Rand Z fz + pool_rim), H_BERUHIG im Wasser am Rand; Sonden im Halterrohr. Rohr-/Tank-/Pumpen-Messstellen (H_INLINE, H_HAHN, H_DRUCK, Tank-Auslass) bleiben fuer M10."""
    items = {}   # Dateiname (ohne .sc) -> [(x, y, z, yaw)]
    add_i = lambda f, x, y, z, yaw=0.0: items.setdefault(f, []).append((round(x, 1), round(y, 1), round(z, 1), round(yaw, 1)))
    rim_z = fz + P["pool_rim"]; wat_z = fz + LAYOUT["pool2"]["water_z"]
    rim2, rim3, wat3 = fz + P.get("pool2_rim", P["pool_rim"]), fz + P.get("pool3_rim", P["pool_rim"]), fz + POOL3["water_z"]   # U4: Becken mit eigenem Rand und Spiegel (ring_b2); A+: gleiche Werte wie bisher
    def tauch(c, inner, wall, phi, sonden, extra=(), rim_z=rim_z):   # H_TAUCH am Beckenrand, c Beckenmitte, phi Richtung der Rohrlage von der Mitte (X zeigt ueber den Rand nach aussen)
        r = inner + wall / 2 - 126.0; x, y = c[0] + r * math.cos(math.radians(phi)), c[1] + r * math.sin(math.radians(phi)); z0 = rim_z - 640.0
        add_i("halter_tauch", x, y, z0, phi)
        for k, sn in enumerate(list(sonden) + list(extra)): add_i("sonde_" + sn, x + (k % 2) * 8 - 4, y + (k // 2) * 8 - 4, z0 + 30.0)
    def beruhig(c, inner, phi, sonden, wat_z=wat_z):   # H_BERUHIG im Wasser an der Beckenwand, Unterkante 300 mm unter dem Spiegel, +X zur Wand
        r = inner - 60.0; x, y = c[0] + r * math.cos(math.radians(phi)), c[1] + r * math.sin(math.radians(phi)); z0 = wat_z - 300.0
        add_i("halter_beruhig", x, y, z0, phi)
        for k, sn in enumerate(sonden): add_i("sonde_" + sn, x, y, z0 + 150.0 + 300.0 * k)
    pi, pw = LAYOUT["pool"]["d"] / 2, P["wall"]
    tauch((0, 0), pi, pw, 160.0, ["do_ind", "temp_ds", "level_druck", "ph"])            # MS01, MS02, MS04, MS05 (MS02/04/05 ohne eigenen Halter -> im Rohr von MS01)
    beruhig((0, 0), pi, 100.0, ["level_float", "level_float"])                              # MS03
    c2 = pool_dims(fz, LAYOUT["pool2"], 60, P["pool2_depth"], "Zweit")[:2] if V == "ring_b2" else (P["pool2_r"] * math.cos(math.radians(P["pool2_az"])), P["pool2_r"] * math.sin(math.radians(P["pool2_az"])))   # U4: ring_b2 am Bauplatz
    tauch(c2, LAYOUT["pool2"]["d"] / 2, 60.0, math.degrees(math.atan2(-c2[1], -c2[0])), ["do_mini"], rim_z=rim2)   # MS07 (zur Kuppelmitte)
    c3 = pool_dims(fz, POOL3, 60, P["pool3_depth"], "Dritt")[:2] if V == "ring_b2" else (P["pool3_r"] * math.cos(math.radians(P["pool3_az"])), P["pool3_r"] * math.sin(math.radians(P["pool3_az"]))); f3 = math.degrees(math.atan2(-c3[1], -c3[0]))
    tauch(c3, P["pool3_d"] / 2, 60.0, f3, ["do_mini", "ph"], rim_z=rim3)                                  # MS08, MS09
    beruhig(c3, P["pool3_d"] / 2, f3 + 60.0, ["level_float"], wat_z=wat3)                                  # MS10
    px, py, pyaw, X, Y = puffer_pose()
    pw_ = lambda lx, ly: (px + lx * X[0] + ly * Y[0], py + lx * X[1] + ly * Y[1])
    for sn, (lx, ly) in zip(("ph", "ec", "temp_ds", "do_mini"), ((-230, 115), (-120, 115), (-230, 225), (-120, 225))):   # MS46: 4 Sondenstutzen im Messzellendeckel (Ports T82)
        x, y = pw_(lx, ly); add_i("sonde_" + sn, x, y, fz + 1203.0 - 100.0)
    x, y = pw_(0, 0); add_i("sonde_leck", x, y, fz + 1.0, pyaw)                              # MS55 Boden unter dem Puffer
    for k, nm in enumerate(("Tank_gross:1", "Tank_gross_t3:1")):                              # MS53, MS54 Boden unter dem Tankstand
        m = next((c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move" and c["params"].get("occurrence") == nm), None)
        if m: add_i("sonde_leck", m[3], m[7], fz + 1.0, math.degrees(math.atan2(m[4], m[0])))
    for f, its in items.items():
        place_instances("MS_" + f, os.path.join(ROOT, "designs", "components", f + ".sc"), its, "13_Messstellen")
    print("messstellen:", {f: len(v) for f, v in items.items()})

def mensch_referenz(fz):
    """M9 (D47, W29): zwei Referenzfiguren 1,80 m (Fussmitte am Boden, Blick +Y). messen: vor der Dosierkonsole der Puffer-Station (Station-KS), Blick zur Konsole; arbeiten: Laufweg B, Azimut Station + 180, Blick nach aussen zum Aussentisch."""
    px, py, pyaw, X, Y = puffer_pose() if not P.get("station_an", 0) else (0, 0, 0, (1, 0), (0, 1))
    if P.get("station_an", 0): sx, sy, a = station_pose(); ar = math.radians(a); n = (math.cos(ar), math.sin(ar)); t = (-math.sin(ar), math.cos(ar)); px, py, pyaw, X, Y = sx, sy, a - 90.0, (-t[0], -t[1]), n
    mx, my = px + P["mensch_mes_x"] * X[0] + P["mensch_mes_y"] * Y[0], py + P["mensch_mes_x"] * X[1] + P["mensch_mes_y"] * Y[1]   # Puffer-KS: Figur vor der Front (-Y), Blick zur Messzelle (+Y)
    place_instances("Mensch_Referenz_messen", os.path.join(ROOT, "designs", "components", "mensch_referenz_messen.sc"), [(round(mx, 1), round(my, 1), fz, pyaw)], "11_Referenz")
    wa = P["door_edge_az"] + 36.0 + 180.0; wr = math.radians(wa)   # gegenueber der alten Station-Flaeche (Laufweg B)
    place_instances("Mensch_Referenz_arbeiten", os.path.join(ROOT, "designs", "components", "mensch_referenz_arbeiten.sc"), [(round(P["mensch_arb_r"] * math.cos(wr), 1), round(P["mensch_arb_r"] * math.sin(wr), 1), fz, wa - 90.0)], "11_Referenz")

def tuer_komplett(segs, base_z):
    """M3 (D36, W20): Werkstatt-Komponente tuer_komplett.sc (T50) als Instanz im Basisfeld BBB. Feld-KS der Komponente: Ursprung Mitte der Basiskante (Knoten 24 -> 22) auf Basisknotenhoehe,
    X tangential (24 -> 22 = gegen den Uhrzeigersinn), Y hangaufwaerts in der Feldebene, Z Feldnormale nach aussen; Neigung der Feldebene aus dem Modell (Basismitte -> Feldspitze, Knoten 6)."""
    az = math.radians(P["door_edge_az"]); ap = P["dome_base_d"]/2 * math.cos(math.radians(18))
    n = (math.cos(az), math.sin(az)); t = (-math.sin(az), math.cos(az))
    ends = {tuple(round(v / 20) for v in q): q for A, B in segs for q in (A, B)}
    apex = min((q for q in ends.values() if abs((math.degrees(math.atan2(q[1], q[0])) - P["door_edge_az"] + 180) % 360 - 180) < 1 and q[2] > base_z + 1000), key=lambda q: q[2])
    tilt = math.atan2(ap - math.hypot(apex[0], apex[1]), apex[2] - base_z); c, s = math.cos(tilt), math.sin(tilt)
    print(f"tuer_komplett: Feldspitze Z {apex[2]:.0f} r {math.hypot(apex[0], apex[1]):.0f}, Neigung {math.degrees(tilt):.2f} Grad")
    act("03_Kuppel"); add("component.insert_design", path=os.path.join(ROOT, "designs", "components", "tuer_komplett.sc").replace("\\", "/"), name="Tuer_Komplett")
    X, Y, Z = (t[0], t[1], 0.0), (-s*n[0], -s*n[1], c), (c*n[0], c*n[1], s)
    add("occurrence.move", occurrence="Tuer_Komplett:1", matrix=[round(v, 9) for v in (X[0], Y[0], Z[0], ap*n[0], X[1], Y[1], Z[1], ap*n[1], X[2], Y[2], Z[2], base_z)], tolerance=1e-6, move_grounded=True)

def huelle(segs):
    """M11/D39 (W27): Plane als 40 Folienfelder (huelle_folie_AAB/BBB/BBB_tuer, T42) je Dreiecksfeld aus data/components/haut_paneel.json felder. Feld-KS der Komponente: Ursprung Inkreismittelpunkt, Z = Aussennormale,
    Z 0 = Ebene der Strebenachsen, P0 -> P1 (Kante kanten_nominal[0]; beim Tuerfeld die Basiskante) parallel X; Dreieck P0 P1 P2 gegen den Uhrzeigersinn von aussen (tri_points der Werkstatt)."""
    ends = {}
    for A, B in segs:
        for q in (A, B): ends.setdefault(tuple(round(v / 20) for v in q), []).append(q)
    E = [tuple(sum(v[i] for v in l)/len(l) for i in range(3)) for l in ends.values()]
    NP = []
    for n in LAYOUT["dome"]["nodes_list"]:
        x, y = rot(n["x"], n["y"], math.radians(ROT)); NP.append(min(E, key=lambda e: math.hypot(e[0] - x, e[1] - y)))
    hp = json.load(open(os.path.join(ROOT, "data", "components", "haut_paneel.json"), encoding="utf-8")); typen = hp["typen"]
    sub = lambda a, b: tuple(a[i] - b[i] for i in range(3)); dot = lambda a, b: sum(a[i]*b[i] for i in range(3))
    cross = lambda a, b: (a[1]*b[2] - a[2]*b[1], a[2]*b[0] - a[0]*b[2], a[0]*b[1] - a[1]*b[0]); unit = lambda a: tuple(v / math.sqrt(dot(a, a)) for v in a)
    items = {"AAB": [], "BBB": [], "BBB_tuer": []}; base_z = min(e[2] for e in E)
    for f in hp["felder"]:
        P3 = [NP[i] for i in f["nodes"]]; cen = tuple(sum(p[i] for p in P3)/3 for i in range(3))
        if dot(cross(sub(P3[1], P3[0]), sub(P3[2], P3[0])), cen) < 0: P3 = [P3[0], P3[2], P3[1]]   # gegen den Uhrzeigersinn von aussen
        typ = f["typ"] + ("_tuer" if f.get("door") else ""); kn = typen[f["typ"]]["kanten_nominal"]; best = None
        for r in range(3):
            Q = [P3[(r + j) % 3] for j in range(3)]
            if f.get("door") and not (abs(Q[0][2] - base_z) < 5 and abs(Q[1][2] - base_z) < 5): continue
            err = abs(math.dist(Q[0], Q[1]) - kn[0]) + abs(math.dist(Q[1], Q[2]) - kn[1]) + abs(math.dist(Q[2], Q[0]) - kn[2])
            if best is None or err < best[0]: best = (err, Q)
        Q = best[1]; la, lb, lc = math.dist(Q[1], Q[2]), math.dist(Q[2], Q[0]), math.dist(Q[0], Q[1])
        inc = tuple((la*Q[0][i] + lb*Q[1][i] + lc*Q[2][i]) / (la + lb + lc) for i in range(3))
        Z = unit(cross(sub(Q[1], Q[0]), sub(Q[2], Q[0]))); X = unit(sub(Q[1], Q[0])); Y = cross(Z, X)
        items[typ].append([round(v, 9) for v in (X[0], Y[0], Z[0], inc[0], X[1], Y[1], Z[1], inc[1], X[2], Y[2], Z[2], inc[2])])
    act("12_Huelle")
    for typ, mats in items.items():
        if not mats: continue
        cls = "Huelle_" + typ
        add("component.insert_design", path=os.path.join(ROOT, "designs", "components", f"huelle_folie_{typ}.sc").replace("\\", "/"), name=cls)
        for _ in range(len(mats) - 1): add("occurrence.copy", component=cls)
        for i, m in enumerate(mats, 1): add("occurrence.move", occurrence=f"{cls}:{i}", matrix=m, tolerance=1e-6, move_grounded=True)
    print("huelle:", {k: len(v) for k, v in items.items()})

NODE_FILES = {}   # Knoten-Index (1-26 wie layout.json nodes_list) -> Dateiname
def knoten_anker(segs):
    """D91 (N-VERBINDER Montage): 26 Scherenknoten statt Kugelknoten. Je Knoten 1 Plattenpaar (knoten_schere_platte.sc) und je Strebe 1 Arm
    (knoten_schere_arm_a/b_montage.sc, ohne Probe-Rohr), Lage aus data/components/knoten_schere.json ueber scripts/knoten_montage.py;
    dazu 10 Fundamentanker an den Basisknoten (X radial nach aussen)."""
    import knoten_montage as KM
    platten, arme, _, K = KM.montage(segs, ROT)
    D = os.path.join(ROOT, "designs", "components")
    place_matrix("Knoten_Platte", os.path.join(D, "knoten_schere_platte.sc"), [m for _, m in platten])
    for t in ("A", "B"):
        place_matrix(f"Schere_{t}", os.path.join(D, f"knoten_schere_arm_{t.lower()}_montage.sc"), [m for _, _, m in arme[t]])
    E = [o for o, _, _ in K.values()]; base_z = min(e[2] for e in E)
    anchors = [(round(e[0], 1), round(e[1], 1), round(e[2], 1), math.degrees(math.atan2(e[1], e[0]))) for e in E if abs(e[2] - base_z) < 5]
    place_instances("Fundamentanker", os.path.join(ROOT, "designs", "components", "fundamentanker.sc"), anchors, "02_Gelaende")

def t1_t3_t4(sock_z):
    pts, edges = build(P["freq"])
    zcut = -0.01
    keep = {k for k, p in pts.items() if p[2] >= zcut}
    zb = 0.0
    # Radius so, dass der Basisring-Umkreis = dome_base_d/2
    R = (P["dome_base_d"]/2) / math.sqrt(1 - zb*zb)
    zsq = P['dome_h']/((1-zb)*R)   # Hoehe/Breite = 0,5: Kuppel in Z gestaucht
    cz = sock_z + P['base_axis_h'] - zb*R*zsq   # Basisring liegt auf dem Sockel (Achshoehe 75 = alter Rundstab strut_r 45 + 30, seit Schritt 3 entkoppelt)
    # Basisring auf gleiche Hoehe setzen; Drehung: Basisknoten bei Azimut 0
    base = [k for k in keep if abs(pts[k][2]) < 1e-3]
    a0 = math.atan2(pts[base[0]][1], pts[base[0]][0])
    def V(k):
        x, y, z = pts[k]
        if abs(z) < 1e-3: z = zb
        x, y = rot(x, y, -a0 + math.radians(18))   # Knoten bei door_az + 36k (OBJ: Tuer sitzt an einem Basisknoten)
        return (x*R, y*R, z*R*zsq + cz)
    # Tuerflaeche: Streben, die den Tuerquader kreuzen, entfallen
    da = math.radians(P["door_az"]); rd = R*math.sqrt(1-zb*zb) - 100
    n = 0; dropped = 0; segs = []
    for a, b in sorted(edges):
        if a not in keep or b not in keep: continue
        A, B = V(a), V(b)
        if a in base and b in base:   # Basiskante des Tuerdreiecks (R13) entfaellt: Schwelle/Pfosten ersetzen sie
            ma = math.degrees(math.atan2((A[1]+B[1])/2, (A[0]+B[0])/2))
            if abs((ma - P["door_edge_az"] + 180) % 360 - 180) < 2: dropped += 1; continue
        segs.append((A, B))
    json.dump(segs, open(os.path.join(ROOT, "scripts", ".segs.json"), "w"))   # Strebenachsen (Knoten-Knoten) fuer scripts/place_m8.py und Abstandsrechnungen
    act("03_Kuppel"); place_struts(segs); knoten_anker(segs)
    act("02_Gelaende")
    # 02_Gelaende: Erdflaeche (mit Aussparungen fuer Becken und Beete) und Fundamentring (Streben hier verankert) als Komponenten
    component_file("erdflaeche", "Erdflaeche", "02_Gelaende", lambda: erde_fn(sock_z))
    component_file("fundamentring", "Fundamentring", "02_Gelaende", lambda: ring_fn(sock_z))
    act("03_Kuppel")
    tuer_komplett(segs, cz)
    if P.get("huelle_an", 1): huelle(segs)
    return n, dropped

LAYOUT = json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "layout.json")))
BAUPLATZ = {}   # Soll-ID -> Bauplatz (x_mm, y_mm, drehung_grad, ...) aus data/oasis-lage.json (U1, D99); nur ring_b2
if V == "ring_b2":
    # U4 (D93, D119): Becken- und Beethoehen der Quelle aus dem Block `ring_b2` in data/layout.json (A+ liest ihn nicht); Lage der Becken = Bauplatz aus data/oasis-lage.json
    _rb = LAYOUT["ring_b2"]
    POOL2_D_ALT = LAYOUT["pool2"]["d"]   # tank_offsets rechnet weiter mit dem alten Zweitbecken-Hindernis: die Altbestand-Tanks (Technik, U5) bleiben in U4 genau, wo sie waren
    for _k in ("pool", "pool2"): LAYOUT[_k].update(_rb[_k])   # d, water_z
    for _b in LAYOUT["ibc_beds"]: _b["z0"] = _rb["ibc_beds_z0"]; _b["height"] = _rb["ibc_beds_hoehe"]["aussen" if "plants" in _b else "innen"]
    BAUPLATZ = {b["id"]: b["bauplatz"] for b in json.load(open(os.path.join(ROOT, "data", "oasis-lage.json"), encoding="utf-8"))["bauteile"] if b.get("bauplatz")}
POOL2_D_ALT = locals().get("POOL2_D_ALT", LAYOUT["pool2"]["d"])
ROT = P["door_az"] - 167   # Layout-Drehung (docs/components.md)

BEET_AUSLASS = {"aussen": (1040.0, 0.0), "innen": (650.0, 65.0)}   # Siphon/Auslass im Beetrahmen (u laengs, v quer; Ursprung Mitte Wannenunterseite): scripts/workshop/ibc_beet.py shaft_cell, gemessen an Reduktion/Standrohr in viewer/detail/ibc_beet_*.json (aussen_800 x 1040 / y 0, innen_933 x 650 / y 65)
BEET_AUSLASS_TIEFE = 80    # Reduktion reicht bis -80 unter den Flur (viewer/detail/ibc_beet_aussen_800.json: Z -80)
SUMPF_WANNE_L, SUMPF_WANNE_B, SUMPF_WANNE_TIEFE = 3179, 1329, 602   # Sumpftank aussen (data/components/sumpftank.json: pit 2975 x 1125 + 2 x (Folie 2 + Wand 100); Boden -(500 + 2 + 100))

def sumpf_orte():
    """U4 (D105, D109, D123): Sumpftank 1 und 2 am Bauplatz aus data/oasis-lage.json; Rueckgabe [(x, y, yaw_komponente, azimut_langachse)].
    Komponente: Langachse = lokales Y (Pufferzonen am +Y-Ende), Zulauefe an der -X-Wand. Die Lage-Probe legt die Langachse fest (drehung_grad, +-180 gleichwertig);
    gewaehlt wird die Drehung, bei der die -X-Wand (Zulauf-Seite) naeher zur Kuppelmitte zeigt (Schlaeuche kommen aus der Kuppel)."""
    out = []
    for sid in ("sump_1", "sump_2"):
        bp = BAUPLATZ[sid]; x, y, L = bp["x_mm"], bp["y_mm"], bp["drehung_grad"]
        ziel = math.degrees(math.atan2(-y, -x)); diff = lambda a: abs((a - ziel + 180) % 360 - 180)
        yaw = min((L - 90.0, L + 90.0), key=lambda yw: diff(yw + 180.0))   # -X zeigt in Richtung yaw + 180
        out.append((x, y, yaw % 360.0, L))
    return out
DOOR_OBJ_AZ = 149.2   # D36: Tuer im Basisfeld BBB; im Modell door_edge_az = DOOR_OBJ_AZ + ROT (-72 = 149,2 - 221,2)

def LXY(cx, cy):
    """Layout-Koordinate (OBJ-Azimut) -> Modell-Koordinate (um ROT gedreht)."""
    x, y = rot(cx, cy, math.radians(ROT)); return round(x, 1), round(y, 1)

POOL3 = None   # nach params(): {"d", "water_z"} wie Zweitbecken, Durchmesser aus pool3_d

def pool_dims(fz, src, wall, depth, nm):
    x, y = LXY(src["cx"], src["cy"])
    if V == "ring_b2" and nm.startswith("Zweit"): x, y = BAUPLATZ["nursery"]["x_mm"], BAUPLATZ["nursery"]["y_mm"]
    elif V == "ring_b2" and nm.startswith("Dritt"): x, y = BAUPLATZ["feed"]["x_mm"], BAUPLATZ["feed"]["y_mm"]
    elif nm.startswith("Zweit"): x, y = P["pool2_r"] * math.cos(math.radians(P["pool2_az"])), P["pool2_r"] * math.sin(math.radians(P["pool2_az"]))   # D62: Zweitbecken von der Tuerachse (Gang Tuer -> Zentralpool frei), Modellrahmen
    elif nm.startswith("Dritt"): x, y = P["pool3_r"] * math.cos(math.radians(P["pool3_az"])), P["pool3_r"] * math.sin(math.radians(P["pool3_az"]))   # D48: Sektor neben der Tuer, Mittelring frei
    else: x, y = 0.0, 0.0   # D35: Zentralpool auf der Kuppelachse (alle Ringe konzentrisch; OBJ-Abweichung 41 mm)
    d_out = src["d"] + 2*wall; z_bot = fz + src["water_z"] - depth
    return x, y, d_out, z_bot, fz + P["pool_rim"] - z_bot

def bed_obj(b):
    """D41: Beet exakt auf der Sektorachse (OBJ-Azimut 5,3 + 36 k, Apothem = ap_c der Tische aus nft_tisch.json = Radialbudget, yaw = Azimut + 90): Tischmitte = Beetmitte ohne OBJ-Streuung (Beetlage nur ~100 mm genau, D21). Rueckgabe (x, y, yaw) im OBJ-Rahmen."""
    az = 5.3 + 36.0 * round((b["az"] - 5.3) / 36.0); ap = NFT_APC["aussen" if "plants" in b else "mitte"]
    return ap * math.cos(math.radians(az)), ap * math.sin(math.radians(az)), az + 90.0

def bed_xy(b):
    x, y = LXY(*bed_obj(b)[:2]); return x, y

def bed_yaw(b): return bed_obj(b)[2] + ROT

def bed_dims(k, b):
    return (BED_OUT_L, BED_OUT_W) if "plants" in b else (b["length"], b["width"])   # echte Wannenmasse der Werkstatt-Beete (Tasche +20 mm Spiel); Aussenbeet 2640 x 800 (W17, D29)
BED_OUT_L, BED_OUT_W = 2640, 800

POOL_BODEN = 120   # Bodenplatte der Becken (Innenboden = z_bot + POOL_BODEN)

def pool_ports(fz):
    """M10-S1b: Anschlussstutzen am Zentralpool (Pool-Mitte 0/0). Netz K01/K17 Seitenablauf d63 je Linie (Plan F2, Azimut des Feinfilters), K03/K19 ein gemeinsamer Bodenablauf d50 (Netz: Knoten pool hat einen Bodenablauf, die Teilung auf zwei Pumpen kommt in S2).
    Rueckgabe: Liste von dict (name, kante, dn, wand, von = Muendung innen in der Wandflaeche, ende = offenes Ende aussen, axis = Flussrichtung aus dem Pool, durch = Dicke der Durchfuehrung); Welt-mm, Z absolut."""
    ri, ue = LAYOUT["pool"]["d"] / 2, P["pool_ueberstand"]; out = []
    for nm, kante, az in (("SA_Ost_A", "K01", P["pool_sd_a_az"]), ("SA_West_B", "K17", P["pool_sd_b_az"])):
        u = (math.cos(math.radians(az)), math.sin(math.radians(az))); z = fz + P["pool_sd_z"]; L = P["wall"] + ue
        out.append({"name": nm, "kante": kante, "dn": P["pool_sd_d"], "wand": P["pool_sd_wand"], "von": (ri*u[0], ri*u[1], z), "ende": ((ri + L)*u[0], (ri + L)*u[1], z), "axis": (u[0], u[1], 0.0), "durch": P["wall"]})
    z_in = pool_dims(fz, LAYOUT["pool"], P["wall"], P["pool_depth"], "Pool")[3] + POOL_BODEN
    out.append({"name": "BA_Mitte", "kante": "K03/K19", "dn": P["pool_bd_d"], "wand": P["pool_bd_wand"], "von": (0.0, 0.0, z_in), "ende": (0.0, 0.0, z_in - POOL_BODEN - ue), "axis": (0.0, 0.0, -1.0), "durch": POOL_BODEN})
    return out

def pool_stutzen(fz, tn):
    """M10-S1b: je Port ein Loch in der Wand/Bodenplatte (Aussen-d des Rohrs) und ein Rohrstueck (T5_Stutzen_*, eigener Koerper, Bohrung Innen-d) von der Muendung bis zum offenen Ende; Wasser fliesst aus dem Pool nach aussen."""
    for p in pool_ports(fz):
        sx, sy, sz = p["von"]; ax = list(p["axis"]); L =math.dist(p["von"], p["ende"]); nm = "T5_Stutzen_" + p["name"]
        add("solid.cylinder", diameter=p["dn"], height=round(p["durch"] + 2, 1), base=[round(sx - ax[0], 2), round(sy - ax[1], 2), round(sz - ax[2], 2)], axis=ax, operation="cut", targets=[tn], name=nm + "_Loch")
        add("solid.cylinder", diameter=p["dn"], height=round(L, 1), base=[round(sx, 2), round(sy, 2), round(sz, 2)], axis=ax, operation="new", name=nm, body_name=nm)
        add("solid.cylinder", diameter=round(p["dn"] - 2*p["wand"], 2), height=round(L + 2, 1), base=[round(sx - ax[0], 2), round(sy - ax[1], 2), round(sz - ax[2], 2)], axis=ax, operation="cut", targets=[nm], name=nm + "_Bohrung")

def pool_fn(fz, nm, src, wall, depth, tn):
    x, y, d_out, z_bot, total = pool_dims(fz, src, wall, depth, nm)
    add("solid.cylinder", diameter=d_out, height=total, base=[x, y, z_bot], operation="new", name=tn, body_name=tn)
    add("solid.cylinder", diameter=d_out - 2*wall, height=total, base=[x, y, z_bot + POOL_BODEN], operation="cut", targets=[tn], name=tn + "_Hohlraum")
    if nm == "Pool": pool_stutzen(fz, tn)   # M10-S1b
    wn = tn.split("_")[0] + "_Wasser"
    add("solid.cylinder", diameter=src["d"] - 10, height=fz + src["water_z"] - (z_bot + POOL_BODEN), base=[x, y, z_bot + POOL_BODEN], operation="new", name=wn, body_name=wn)

def pools_ring_b2(fz):
    """U4 (D93, D118, D120): 04_Wasserbecken nach der Quelle. Fischtank (T5, Wsp 750, Rand 1200, Innenboden -1000) und Anzuchtbecken (T6, Wsp 800, Rand 1000, auf dem Boden) sind in Weltlage gebaute
    Komponenten von U3 (Lage aus data/oasis-lage.json im Bauskript scripts/workshop/becken_soll.py) und werden im Ursprung eingefuegt; das Lebendfutterbecken (T14k, Wsp 850, Rand 1000, auf dem Boden)
    steht am Bauplatz feed, Drehung 0 (die Ueberlauf-Tuelle ist im Weltazimut zum Anzuchtbecken gebaut). Ports der Tuellen: data/becken-ports.json."""
    act("04_Wasserbecken")
    comp = lambda n: os.path.join(ROOT, "designs", "components", n + ".sc").replace("\\", "/")
    add("component.insert_design", path=comp("pool_zentral"), name="Pool")
    add("component.insert_design", path=comp("zweitbecken"), name="Zweitbecken")
    f = BAUPLATZ["feed"]
    place_instances("Becken_Dritt", comp("becken_dritt_klein"), [(round(f["x_mm"], 1), round(f["y_mm"], 1), fz, 0.0)], "04_Wasserbecken")

def sumpftanks(fz):
    """U4 (D105): zwei Sumpftanks (T101) im Boden, Komponentenursprung = Grubenmitte, Z 0 = Fussboden; Gruben in erde_fn."""
    items = [(round(x, 1), round(y, 1), fz, round(yaw, 3)) for x, y, yaw, _ in sumpf_orte()]
    place_instances("Sumpftank", os.path.join(ROOT, "designs", "components", "sumpftank.sc"), items, "04_Wasserbecken")

def becken_ports(fz):
    """U4 (Aufgabe 3): Ports fuer U6 in Weltkoordinaten (Z absolut): Ueberlauf-Tuellen d63 der Beckenkette (e63 Lebendfutter -> Anzucht, e70 Anzucht -> Fischtank), Zulauf-Tuellen ID25 (3 je Sumpf, Schlauch aus den Fallleitungen),
    Pumpensockel und Schwimmerhalter im Sumpf (U5). Quelle der Lagen: Komponenten-Parameter (data/components/*.json), Bauplaetze (data/oasis-lage.json), Placement (sumpf_orte)."""
    sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
    import becken_soll as BS, sc
    out = {"_hinweis": "erzeugt von scripts/gen_dome.py (ring_b2, U4); Weltkoordinaten in mm, Z absolut (Fussboden Z %g); nicht von Hand aendern" % fz, "ueberlaeufe": [], "sumpf_zulaeufe": [], "sumpf_einbauten": []}
    for klasse, sid, ziel, nm in (("zweitbecken", "nursery", "fish", "T6_Ueberlauf"), ("becken_dritt_klein", "feed", "nursery", "T14k_Ueberlauf")):
        p, _ = sc.load_params(klasse); az = BS.ue_azimut(sid, ziel); u = (math.cos(math.radians(az)), math.sin(math.radians(az))); bp = BAUPLATZ[sid]
        r = p["wasser_d"] / 2.0 + p["ring"] + p["stutzen_len"]; z = fz + P["pool2_wsp" if sid == "nursery" else "pool3_wsp"] + p["ue_id"] / 2.0
        out["ueberlaeufe"].append({"name": nm, "von": sid, "nach": ziel, "weg": "e70" if sid == "nursery" else "e63", "dn": "d%d" % p["ue_dn"], "port_mm": [round(bp["x_mm"] + r * u[0], 1), round(bp["y_mm"] + r * u[1], 1), round(z, 1)], "richtung": [round(u[0], 4), round(u[1], 4), 0.0]})
    sp, _ = sc.load_params("sumpftank"); w, lt, wt = sp["pit_w"], sp["liner_t"], sp["wall_t"]
    for k, (x, y, yaw, _) in enumerate(sumpf_orte(), 1):
        c, s_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw)); W = lambda lx, ly, lz: [round(x + lx * c - ly * s_, 1), round(y + lx * s_ + ly * c, 1), round(fz + lz, 1)]
        for i, yt in enumerate((-1100, -700, -300), 1):
            out["sumpf_zulaeufe"].append({"name": "sump_%d_zulauf_%d" % (k, i), "dn_innen": sp["tuelle_id"], "port_mm": W(-(w / 2 + lt + wt), yt, sp["tuelle_z"]), "richtung": [round(c, 4), round(s_, 4), 0.0]})
        out["sumpf_einbauten"].append({"name": "sump_%d" % k, "grube_mitte_mm": W(0, 0, 0), "yaw_grad": round(yaw, 3), "pumpensockel_mm": W(sp["sockel_x"], sp["sockel_y"], -sp["pit_d"] + sp["sockel_h"]), "schwimmerhalter_mm": W(w / 2 - 30, sp["halter_y"], sp["halter_z"]), "wasserspiegel_z": round(fz + sp["wsp"], 1), "hochstand_z": round(fz + sp["hochstand"], 1)})
    json.dump(out, open(os.path.join(ROOT, "data", "becken-ports.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("becken-ports:", len(out["ueberlaeufe"]), "Ueberlaeufe,", len(out["sumpf_zulaeufe"]), "Sumpf-Zulaeufe")

def pools(fz):
    """04_Wasserbecken: Zentralpool (T5) und Zweitbecken (T6) als Komponenten; eingelassen, Rand Z 650, Wasserspiegel Z 515."""
    if V == "ring_b2": return pools_ring_b2(fz)
    component_file("pool_zentral", "Pool", "04_Wasserbecken", lambda: pool_fn(fz, "Pool", LAYOUT["pool"], P["wall"], P["pool_depth"], "T5_Zentraltank"))
    component_file("zweitbecken", "Zweitbecken", "04_Wasserbecken", lambda: pool_fn(fz, "Zweitbecken", LAYOUT["pool2"], 60, P["pool2_depth"], "T6_Zweitbecken"))
    x3, y3, _, zb3, _ = pool_dims(fz, POOL3, 60, P["pool3_depth"], "Dritt")
    place_instances("Becken_Dritt", os.path.join(ROOT, "designs", "components", "becken_dritt_klein.sc"), [(round(x3, 1), round(y3, 1), round(zb3, 1), 0.0)], "04_Wasserbecken")   # D66: Werkstatt-Komponente becken_dritt_klein (T14k, Z 0 = Unterkante)

def rect_corners(cx, cy, l, w, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return [(cx + u*c - v*s, cy + u*s + v*c) for u, v in ((-l/2, -w/2), (l/2, -w/2), (l/2, w/2), (-l/2, w/2))]

def rect_gap(A, B):
    """Trennabstand zweier Rechtecke im Grundriss (SAT; negativ = Ueberlappung)."""
    g = -1e9
    for Q in (A, B):
        for i in range(4):
            e = (Q[(i+1) % 4][0] - Q[i][0], Q[(i+1) % 4][1] - Q[i][1]); m = math.hypot(*e); n = (-e[1]/m, e[0]/m)
            pa = [p[0]*n[0] + p[1]*n[1] for p in A]; pb = [p[0]*n[0] + p[1]*n[1] for p in B]
            g = max(g, min(pa) - max(pb), min(pb) - max(pa))
    return g

def tank_offsets():
    """D22: OBJ-Plattformen von Tank 1/3 (-83 mm) und Tank 2 / Innenbeet 12 (-77 mm) ueberlappen im Grundriss, die Werkstatt-Rahmen (Beine an den Ecken) stossen dort durch Nachbarplattform bzw. Beet.
    Der kleinere Tank samt Pumpentafeln rueckt um (tank_clear - Luecke) von der Nachbarplattform bzw. dem Beet weg (Layout-Koordinaten)."""
    T = LAYOUT["tanks"]; pl = [t["platform"][0] for t in T]; off = {i: [0.0, 0.0] for i in range(len(T))}
    rc = lambda i: rect_corners(pl[i]["cx"] + off[i][0], pl[i]["cy"] + off[i][1], pl[i]["length"], pl[i]["width"], pl[i]["yaw"])
    portal = lambda k, b: (rect_corners(*bed_obj(b)[:2], bed_dims(k, b)[0], bed_dims(k, b)[1] + 230, bed_obj(b)[2]), bed_obj(b)[:2], P["tank_walk_clear"])   # Portal = Beet + 115 je Seite, D62: >= 500 mm Gang
    obstacles = lambda i: [(rc(j), (pl[j]["cx"] + off[j][0], pl[j]["cy"] + off[j][1]), P["tank_clear"]) for j in range(len(T)) if j != i and pl[j]["length"] >= pl[i]["length"] and not (pl[j]["length"] == pl[i]["length"] and j < i)] + [portal(k, b) for k, b in enumerate(LAYOUT["ibc_beds"], 1)]
    p2 = rot(P["pool2_r"] * math.cos(math.radians(P["pool2_az"])), P["pool2_r"] * math.sin(math.radians(P["pool2_az"])), -math.radians(ROT)); p2h = POOL2_D_ALT / 2 + 60
    def pool2_obst(i):   # D42: Zweitbecken als Quadrat (Seite = Aussendurchmesser) mit einer Seite zum Tank gedreht = beruehrt den Kreis nur in Tankrichtung
        yaw = math.degrees(math.atan2(pl[i]["cy"] + off[i][1] - p2[1], pl[i]["cx"] + off[i][0] - p2[0])); return (rect_corners(p2[0], p2[1], 2 * p2h, 2 * p2h, yaw), p2, P["tank_walk_clear"])
    p0h = LAYOUT["pool"]["d"] / 2 + P["wall"]
    def pool0_obst(i):   # D62: Zentralpool (Rand 2095 + Innentisch-Pfosten bei 2160) wie das Zweitbecken als zum Tank gedrehtes Quadrat
        yaw = math.degrees(math.atan2(pl[i]["cy"] + off[i][1], pl[i]["cx"] + off[i][0])); return (rect_corners(0.0, 0.0, 2 * p0h, 2 * p0h, yaw), (0.0, 0.0), P["tank_walk_clear"])
    for _ in range(12):
        for i in range(len(T)):
            for R, (ox, oy), clr in obstacles(i) + [pool2_obst(i), pool0_obst(i)]:
                gap = rect_gap(rc(i), R)
                if gap < clr:
                    dx, dy = pl[i]["cx"] + off[i][0] - ox, pl[i]["cy"] + off[i][1] - oy; d = math.hypot(dx, dy); mv = clr - gap
                    off[i][0] += dx/d*mv; off[i][1] += dy/d*mv
    return off

def tanks(fz):
    """07_Tanks/09_Technik: 4 Tanks (Werkstatt: tank_klein x2, tank_gross, tank_gross_t3) und 8 Pumpentafeln (pumpe_klein/gross, je Tank 2) als Instanzen; Ursprung Tank = Mitte Standflaeche am Boden, Drehung = Plattform-yaw; Positionen aus layout.json plus tank_offsets."""
    tk = {"klein": [], "gross": [], "gross_t3": []}; pk = {"klein": [], "gross": []}; off = tank_offsets()
    for i, t in enumerate(LAYOUT["tanks"]):
        dx, dy = off[i]; x, y = LXY(t["cx"] + dx, t["cy"] + dy); yaw = t["platform"][0]["yaw"] + ROT
        tk["klein" if t["d"] < 800 else ("gross_t3" if i == 2 else "gross")].append((x, y, fz, yaw))
        placed = []
        for m in t["modules"]:
            if m["l"] < 500: continue   # 384-mm-Kassetten = Stuetzrippen der Plattform (D16, Teil der Tank-Komponente)
            mx, my = LXY(m["cx"] + dx, m["cy"] + dy)
            if any(math.hypot(mx - px, my - py) < 100 for px, py in placed): continue   # OBJ-Duplikate zusammenfassen
            placed.append((mx, my))
            yw = math.radians(m["yaw"] + ROT); yp = (-math.sin(yw), math.cos(yw)); dn = (mx - x) * yp[0] + (my - y) * yp[1]   # W30: Tafel steht seitlich am Stand, Mittelabstand (Tafelnormale) >= Plattformhalbbreite + 25 + tafel_gap
            need = (619 if t["d"] < 800 else 821) / 2 + 25 + 30
            if abs(dn) < need: sg = 1 if dn >= 0 else -1; mx, my = mx + sg * (need - abs(dn)) * yp[0], my + sg * (need - abs(dn)) * yp[1]
            pk["klein" if t["d"] < 800 else "gross"].append((round(mx, 1), round(my, 1), fz, m["yaw"] + ROT))
    for v, items in tk.items():
        if items: place_instances("Tank_" + v, os.path.join(ROOT, "designs", "components", f"tank_{v}.sc"), items, "07_Tanks")
    for v, items in pk.items():
        place_instances("Pumpe_" + v, os.path.join(ROOT, "designs", "components", f"pumpe_{v}.sc"), items, "09_Technik")

def place_instances(cls, path, items, assembly):
    """Werkstatt-Komponente verknuepfen (eine Definition) und je Eintrag (x, y, z, yaw_grad) eine Instanz setzen (erst alle Kopien am Ursprung, dann absolut verschieben)."""
    act(assembly); add("component.insert_design", path=path.replace("\\", "/"), name=cls)
    for _ in range(len(items) - 1): add("occurrence.copy", component=cls)
    for i, (x, y, z, yaw) in enumerate(items, 1):
        c, s_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        add("occurrence.move", occurrence=f"{cls}:{i}", matrix=[round(v, 9) for v in (c, -s_, 0, x, s_, c, 0, y, 0, 0, 1, z)], tolerance=1e-6, move_grounded=True)

def place_matrices(cls, path, mats, assembly):
    """Wie place_instances, aber mit fertigen 3x4-Matrizen (Rohre/Bogen in beliebiger Raumlage)."""
    act(assembly); add("component.insert_design", path=path.replace("\\", "/"), name=cls)
    for _ in range(len(mats) - 1): add("occurrence.copy", component=cls)
    for i, m in enumerate(mats, 1): add("occurrence.move", occurrence=f"{cls}:{i}", matrix=m, tolerance=1e-6, move_grounded=True)

def leitungen(fz):
    """M10-S2a: Rohre, Bogen, T, Reduziermuffen und Kupplungen aus data/leitungstrassen.json als Instanzen der Bibliothek lt_*.sc (Rechnung: scripts/leitungen.py), Assembly 08_Leitungen, Farbe nach Funktion."""
    doc = LTG.laden_variante(V)   # V1b: nur Trassen, Formstuecke und Teile der aktiven Variante
    if not doc: return
    teile, _ = LTG.bauen(doc)
    for cls, path, mats, farben in LTG.dateien(teile):
        place_matrices(cls, path, mats, "08_Leitungen")
        for hexfarbe, occ in farben.items():
            if hexfarbe: add("appearance.assign", components=occ, color=hexfarbe)

def verteiler_a_plus():
    """N-VARIANTEN V1b (Blatt 1.2): Setzung nur in A+. Der Verteiler d50 je Linie steht als `teile` VT1/VT2 (samt Kappen und Klemme) mit
    `varianten: ["a_plus"]` in data/leitungstrassen.json und wird von leitungen() gesetzt; hier entsteht kein eigener Befehl (A+ bleibt byte-gleich).
    Liefert die Ids der A+-eigenen Teile fuer Bericht und Pruefung."""
    doc = LTG.laden() or {}
    return [e["id"] for key in LTG.VAR_LISTEN for e in doc.get(key, []) if e.get("varianten") == ["a_plus"]]

def ring_b2(fz):
    """N-AUTOBAHN-V2 R1/R2: Setzungen nur in Ring B2 aus scripts/trassen_ring.py (Lage aus Instanzmatrizen und Port-Tabellen): Joche, Stelzen, Montageschienen,
    Verbinder, Schellen, Ring-Ecken, Podeste, Pegelschaechte, Booster, Entluefter (R1), ab R2 Ausleger, Abzweige und Fallleitungen.
    Rohre, Formstuecke und Haehne kommen als Eintraege mit `varianten: ["ring_b2"]` ueber leitungen(). Runde ueber Umgebung AUTOBAHN_RUNDE (r1 | r2, Standard r2)."""
    import trassen_ring as TRR
    gesetzt = []
    for cls, path, mats, asm in TRR.tragwerk(os.environ.get("AUTOBAHN_RUNDE", "r2")):
        if mats: place_matrices(cls, path, mats, asm); gesetzt.append((cls, len(mats)))
    return gesetzt

# T9: 14 halbe IBC-Wannen (layout.json) als Instanzen der Werkstatt-Komponenten ibc_beet_{aussen_933,aussen_993,innen_933}; Ursprung = Mitte Wannenunterseite
def t9(fz):
    groups = {}
    for k, b in enumerate(LAYOUT["ibc_beds"], 1):
        x, y = bed_xy(b)
        v = "innen_933" if "plants" not in b else "aussen_800"
        groups.setdefault(v, []).append((x, y, fz + b["z0"], bed_yaw(b)))
    for v, items in groups.items():
        place_instances("Beet_" + v, os.path.join(ROOT, "designs", "components", f"ibc_beet_{v}.sc"), items, "05_Beete")

# T8: 24 NFT-Tische Rev. B (W16, D18) als Instanzen nft_tisch_{aussen,mitte,innen}: je Sektor eine Tischinstanz, Tischkoordinaten X tangential, Y radial INNEN, yaw = Azimut + 90 Grad (volle 360 Grad); Ursprung = Mitte Standflaeche am Boden.
# Portaltische (aussen, mitte) stehen auf der Beetmitte (Radius des Beets auf der Sektorachse), wie die Beete um outer_bed_shift/inner_bed_shift nach innen (Radialbudget D28/D29, M7); innen auf ap_c 1864.
SECTORS = {"innen": list(range(10)), "mitte": [0, 1, 2, 7, 8, 9], "aussen": [0, 1, 2, 3, 6, 7, 8, 9]}
NFT_APC = {k: v["ap_c"] for k, v in json.load(open(os.path.join(ROOT, "data", "components", "nft_tisch.json"), encoding="utf-8"))["typen"].items()}   # Radialbudget (W17): Tischmitte = Beetmitte
NFT_APC["mitte"] += P["ring_shift_mid"]; NFT_APC["aussen"] += P["ring_shift_out"]   # D63: Laufweg A effektiv nur 501 mm (Innentisch-Pfosten bei r 2160 stehen im Gang) -> Mittel- und Aussenring um die Wandluft nach aussen
NFT_POTS = []                                                # Rinnen-Topfpositionen (x, y, z Topfboden), von nft() gefuellt, von pots() gesetzt

def nft(fz):
    tp = json.load(open(os.path.join(ROOT, "data", "nft_pots.json" if V == "a_plus" else "nft_pots-%s.json" % V)))["typen"]   # U4: ring_b2 = Topfhoehen der Tische von U3 (Rinnenunterkante 1030/880/1230), extract_nft_pots.py --variante ring_b2
    for typ, sectors in SECTORS.items():
        items = []
        for i in sectors:
            az = 5.3 + 36.0 * i; ap = NFT_APC[typ]
            x, y = LXY(ap * math.cos(math.radians(az)), ap * math.sin(math.radians(az))); yaw = az + 90 + ROT; c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
            items.append((x, y, fz, yaw))
            for u, v, z in tp[typ]["pots"]: NFT_POTS.append((round(x + u*c - v*s, 1), round(y + u*s + v*c, 1), round(fz + z, 1)))
        place_instances("Tisch_" + typ, os.path.join(ROOT, "designs", "components", f"nft_tisch_{typ}.sc"), items, "06_NFT")

# T10/T12: Netztoepfe und Salatkoepfe in den 8 Aussenbeeten als Instanzen (Positionen je Topf aus data/pots.json = OBJ, Beet-Koordinaten); Netztopf-Ursprung Mitte Boden, Salatkopf-Ursprung Kragenoberkante (Boden + 63)
PLANTS = json.load(open(os.path.join(ROOT, "data", "pots.json")))
def bed_pot_grid(l=None, w=None):
    """Topfraster im Beet (Aussenbeet 2640 x 800, D34; Innenbeet 1865 x 933, D52): quadratisches Raster `pot_pitch` (Salatkopf 95-125 mm breit), `pot_margin` zur Wanne, symmetrisch zur Beetmitte; (u laengs, v quer)."""
    l, w = l or BED_OUT_L, w or BED_OUT_W
    nu, nv = int((l - 2*P["pot_margin"]) // P["pot_pitch"]) + 1, int((w - 2*P["pot_margin"]) // P["pot_pitch"]) + 1
    return [((i - (nu - 1)/2) * P["pot_pitch"], (j - (nv - 1)/2) * P["pot_pitch"]) for i in range(nu) for j in range(nv)]

BED_MEDIA_DEPTH = json.load(open(os.path.join(ROOT, "data", "components", "ibc_beet.json"), encoding="utf-8"))["parameter"]["media_depth"]["wert"]
BED_RIM_GAP = json.load(open(os.path.join(ROOT, "data", "components", "ibc_beet.json"), encoding="utf-8"))["parameter"]["rim_gap"]["wert"]   # Medienoberkante = Wannenhoehe - rim_gap (75)
def pots(fz, with_heads):
    pots_, heads = [], []
    for k, b in enumerate(LAYOUT["ibc_beds"]):
        grid = bed_pot_grid() if "plants" in b else bed_pot_grid(b["length"], b["width"])   # D52: auch die 6 Innenbeete tragen Toepfe
        cx, cy = bed_xy(b); yaw = bed_yaw(b); c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        for u, v in grid:
            x, y = round(cx + u*c - v*s, 1), round(cy + u*s + v*c, 1)
            zb = round(fz + b["z0"] + b["height"] - BED_RIM_GAP, 1) if V == "a_plus" else round(fz + P["beet_boden"] + BED_MEDIA_DEPTH, 1)   # U4/D122: ring_b2 Medienoberflaeche = Beetboden 70 + media_depth 300 = 370 ueber dem Flur   # D79: Topf steht auf der Medienoberkante DIESES Beets (aussen 800, innen 765 bis 801 abs.); NFT-Toepfe unveraendert
            pots_.append((x, y, zb, 0)); heads.append((x, y, zb + 63, 0))
    for x, y, zb in NFT_POTS: pots_.append((x, y, zb, 0)); heads.append((x, y, round(zb + 63, 1), 0))   # Rinnen-Toepfe (D33: 586, Lochabstand 200)
    place_instances("Netztopf", os.path.join(ROOT, "designs", "components", "netztopf.sc"), pots_, "10_Pflanzen")
    if with_heads: place_instances("Salatkopf", os.path.join(ROOT, "designs", "components", "salatkopf.sc"), heads[:int(P["salat_n"])], "10_Pflanzen")

plants = [0]
def plant(x, y, z, r=90):
    plants[0] += 1
    add("solid.sphere", radius=r, center=[x, y, z], operation="new", name=f"T12_Salat_{plants[0]:03d}", body_name=f"T12_Salat_{plants[0]:03d}")

def rohr_fn():
    # Zulaufrohr (Frischwasser) nur AUSSEN: flach auf dem Boden, Bogen zur Fundamentringwand nahe dem Zweitbecken (OBJ-Azimut 166 -> Modell -55)
    pr = P["pipe_d"]/2; z = P["sock_h"] + pr
    P0 = pol(9500, -90); P1 = pol(7600, -58); P2 = pol(6120, -58)
    def seg(A, B, nm, op, **kw):
        d = [B[0]-A[0], B[1]-A[1]]; L = math.hypot(*d)
        add("solid.cylinder", radius=pr, height=round(L, 1), base=[round(A[0], 1), round(A[1], 1), z], axis=[round(d[0]/L, 6), round(d[1]/L, 6), 0], operation=op, name=nm, **kw)
    seg(P0, P1, "T10_Zulaufrohr", "new", body_name="T10_Zulaufrohr")
    add("solid.sphere", radius=round(pr*1.15, 1), center=[round(P1[0], 1), round(P1[1], 1), z], operation="join", targets=["T10_Zulaufrohr"], name="T10_Knie")
    seg(P1, P2, "T10_Zulaufrohr_2", "join", targets=["T10_Zulaufrohr"])

def schrank_fn():
    if "technik_x" in P:   # M10-S5-LUFT-B (D81, E13 vorlaeufig): Schrank in der Technikgruppe aussen neben der Tuer, achsparallel (Breite cab_x in X)
        rect_body("T11_Schaltschrank", P["technik_x"], P["technik_y"], P["sock_h"], 0, P["cab_x"], P["cab_y"], P["cab_z"]); return
    az = 0; apo = (P["dome_base_d"]/2 + P["sock_w"])*math.cos(math.radians(18))   # D62: Schaltschrank neben den Vorbau (Flaeche 0 statt -36)
    cx, cy = pol(apo + P["cab_y"]/2 + 20, az)
    rect_body("T11_Schaltschrank", round(cx, 1), round(cy, 1), P["sock_h"], az+90, P["cab_x"], P["cab_y"], P["cab_z"])

def technik_e13(fz):
    """M10-S5-LUFT-B: Technikgruppe "vorlaeufig, E13" aussen vor dem Fundamentring (Lage aus scripts/technik_e13.py, Ursprung technik_x/technik_y): Schrank-Einfuehrung T89,
    Geblaese T85 x2, Hauptverteiler luftverteiler_6 T86 (Abgaenge nach unten), Aktivkohle-Station T83; alle in 14_Technik_E13. Leitungen kommen aus data/leitungstrassen.json (linie luft_b, frisch)."""
    import technik_e13 as TE
    g = TE.gruppe(P); comp = lambda n: os.path.join(ROOT, "designs", "components", n + ".sc")
    place_instances("Schrank_Einfuehrung", comp("schrank_einfuehrung"), [g["einfuehrung"]], "14_Technik_E13")
    place_instances("Geblaese_Luft", comp("geblaese_luft"), g["geblaese"], "14_Technik_E13")
    place_matrices("Luftverteiler_6", comp("luftverteiler_6"), [TE.verteiler_matrix(g["vert"])], "14_Technik_E13")
    place_instances("Aktivkohle_Station", comp("aktivkohle_station"), [g["station"]], "14_Technik_E13")

def luft_a(fz):
    """M10-S5-LUFT Teil A: Pool-Verteiler luftverteiler_4 (T87) auf dem Beckenrand, 4 Scheibenbelueftungen (T88) auf dem Beckenboden, Schwimmerventil (T84) am Rand; Lagen (Annahmen [A]) aus scripts/trassen_luft.py, die Rohre d25 kommen als Trassen K44-S1..S4 aus data/leitungstrassen.json."""
    import trassen_luft as TL
    g = TL.geometrie(fz, LAYOUT["pool"]["d"], P["wall"], P["pool_rim"], LAYOUT["pool"]["water_z"], P["pool_depth"], POOL_BODEN)
    comp = lambda n: os.path.join(ROOT, "designs", "components", n + ".sc")
    place_instances("Luftverteiler_4", comp("luftverteiler_4"), [tuple(round(v, 2) for v in g["verteiler"])], "09_Technik")
    place_instances("Luft_Scheibenbelueftung", comp("luft_scheibenbelueftung"), [(round(x, 2), round(y, 2), round(z, 2), 0.0) for x, y, z in g["scheiben"]], "04_Wasserbecken")
    place_instances("Schwimmerventil_Pool", comp("schwimmerventil_pool"), [tuple(round(v, 2) for v in g["ventil"])], "04_Wasserbecken")

def t10_t11(fz):
    component_file("zulaufrohr", "Zulaufrohr", "08_Leitungen", rohr_fn)
    component_file("schaltschrank", "Schaltschrank", "14_Technik_E13" if "technik_x" in P else "09_Technik", schrank_fn)

if __name__ == "__main__":
    stage = int(sys.argv[1]); out = sys.argv[2]
    params(); POOL3 = {"cx": 0, "cy": 0, "d": P["pool3_d"], "water_z": LAYOUT["ring_b2"]["pool3"]["water_z"] if V == "ring_b2" else LAYOUT["pool2"]["water_z"]}
    add("component.rename", component=0, name="Kuppel_Aquaponik")
    for nm in ASSEMBLIES: add("component.create", name=nm, activate=False)
    t1_t3_t4(P["sock_h"]) if False else None
    n, dropped = t1_t3_t4(P["sock_h"])
    if stage >= 2: pools(P["sock_h"]); (sumpftanks(P["sock_h"]), becken_ports(P["sock_h"])) if V == "ring_b2" else None; tanks(P["sock_h"])
    if stage >= 3: t9(P["sock_h"]); nft(P["sock_h"])
    if stage >= 5: pots(P["sock_h"], P["salat_n"] > 0)
    if stage >= 4: t10_t11(P["sock_h"]); (puffer_station(P["sock_h"]) if P.get("station_an", 0) else puffer_klein(P["sock_h"])); feinfilter(P["sock_h"]); luft_a(P["sock_h"]); technik_e13(P["sock_h"]); (verteiler_a_plus() if V == "a_plus" else ring_b2(P["sock_h"])); leitungen(P["sock_h"]); mensch_referenz(P["sock_h"]); messstellen(P["sock_h"])
    colors()
    json.dump({"commands": cmds}, open(out, "w"), indent=0)
    print(f"variante {V}, stufe {stage}: {len(cmds)} befehle, {n} streben, {dropped} fuer tuer entfernt")
