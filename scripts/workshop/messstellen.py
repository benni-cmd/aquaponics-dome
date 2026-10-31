"""Messstellen-Bauteile T90/T91 (W35, R39, D65): 8 Halter (H_TAUCH, H_BERUHIG, H_ZELLE, H_INLINE d32/d50, H_HAHN, H_DRUCK, H_MAST, H_BOX) und 14 Sonden-Platzhalter, alle aus der Tabelle COMPS.
Halter: Standard vor Sonderloesung (Rohre d20..d63 PVC-U, Kugelhahn, Klemmen, IP65-Gehaeuse). Sonden: EIN schlichter Koerper je Typ in Hersteller-Farbe, Masse Annahme [A] (messstellen.json hat keine Abmessungen).
KS je Bauteil: siehe 'ks' der Komponente; Ports: (Name, Mass, Lage der Spitze/Anlage, Richtung, Koerper, Spitze=True: Lage ist die aeusserste Stelle des Koerpers in Richtung).
Aufruf: python scripts/workshop/messstellen.py [schluessel ...] [--json] [--blatt]   (ohne Schluessel: alle bauen; --json schreibt data/components/messstellen.json, --blatt docs/parts/messstellen.md)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as LT

STEEL = "Stahl verzinkt"
MATS = {STEEL: (7.85, "#aeb4b8"), "Edelstahl": (7.9, "#c8ccd0"), "PVC grau": (1.4, "#8d9296"), "PVC blau": (1.4, "#2a5da8"), "PP schwarz": (0.91, "#2b2b2b"), "PA schwarz": (1.14, "#1f1f1f"),
        "Messing": (8.5, "#c9a227"), "PS grau": (1.05, "#b9bfc4"), "Acryl klar": (1.19, "#cfe6ee"), "Sonde blau": (1.6, "#2a5da8"), "Sonde grau": (1.6, "#5a5f66"), "Sonde gelb": (1.6, "#d9b13b"),
        "Sonde schwarz": (1.2, "#2b2b2b"), "PP weiss": (0.91, "#e8e8e8"), "Platine gruen": (1.8, "#1f7a3a"), "Schwimmer orange": (0.6, "#e8801a"), "Kontakt rot": (1.4, "#b3302b")}

def cyl(b, nm, d, h, base, axis=(0, 0, 1), op="new", targets=None, body=None, mat=None):
    kw = dict(diameter=d, height=h, base=[round(v, 3) for v in base], axis=list(axis), operation=op, name=nm)
    if op == "new":
        kw["body_name"] = body or nm
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)
    if op == "new" and mat:
        b.add("material.assign", bodies=[body or nm], material=mat)

def bx(b, nm, x0, x1, y0, y1, z0, z1, op="new", targets=None, body=None, mat=None):
    kw = dict(length=x1 - x0, width=y1 - y0, height=z1 - z0, center=[round((x0 + x1) / 2, 3), round((y0 + y1) / 2, 3), round((z0 + z1) / 2, 3)], operation=op, name=nm)
    if op == "new":
        kw["body_name"] = body or nm
    else:
        kw["targets"] = targets
    b.add("solid.box", **kw)
    if op == "new" and mat:
        b.add("material.assign", bodies=[body or nm], material=mat)

# ---------------------------------------------------------------- Halter
def c_tauch(b, p):
    r, L, w = p["rohr_d"], p["laenge"], p["rohr_wall"]
    cyl(b, "R", r, L, [0, 0, 0], body="Tauchrohr", mat="PVC grau")
    cyl(b, "RB", r - 2 * w, L + 2, [0, 0, -1], op="cut", targets=["Tauchrohr"])
    for k, z in enumerate((30, 70), 1):                                           # Wasserzutritt: Querbohrungen unten
        cyl(b, f"QB{k}", p["bohr_d"], r + 4, [-(r + 4) / 2, 0, z], axis=(1, 0, 0), op="cut", targets=["Tauchrohr"])
    cyl(b, "K", p["kappe_d"], p["kappe_h"], [0, 0, L], body="Kappe", mat="PA schwarz")
    cyl(b, "KB", p["kabel_d"], p["kappe_h"] + 2, [0, 0, L - 1], op="cut", targets=["Kappe"])
    zs, so = p["schelle_z"], p["schelle_od"]
    cyl(b, "S", so, p["schelle_h"], [0, 0, zs], body="Klemme", mat=STEEL)
    cyl(b, "SB", r, p["schelle_h"] + 2, [0, 0, zs - 1], op="cut", targets=["Klemme"])
    bx(b, "Arm", so / 2 - 4, so / 2 + p["arm_len"], -p["arm_w"] / 2, p["arm_w"] / 2, zs, zs + p["schelle_h"], op="join", targets=["Klemme"])
    bx(b, "Haken", so / 2 + p["arm_len"] - 20, so / 2 + p["arm_len"], -p["arm_w"] / 2, p["arm_w"] / 2, zs - p["haken_h"], zs + 1, op="join", targets=["Klemme"])

def c_beruhig(b, p):
    r, L, w = p["rohr_d"], p["laenge"], p["rohr_wall"]
    cyl(b, "R", r, L, [0, 0, 0], body="Rohr", mat="PVC grau")
    cyl(b, "RB", r - 2 * w, L + 2, [0, 0, -1], op="cut", targets=["Rohr"])
    z0 = (L - p["schlitz_l"]) / 2
    bx(b, "SX", -r / 2 - 2, r / 2 + 2, -p["schlitz_w"] / 2, p["schlitz_w"] / 2, z0, z0 + p["schlitz_l"], op="cut", targets=["Rohr"])
    bx(b, "SY", -p["schlitz_w"] / 2, p["schlitz_w"] / 2, -r / 2 - 2, r / 2 + 2, z0, z0 + p["schlitz_l"], op="cut", targets=["Rohr"])
    cyl(b, "BK", p["kappe_d"], p["kappe_h"], [0, 0, -p["kappe_h"]], body="Bodenkappe", mat="PVC grau")
    cyl(b, "DK", p["kappe_d"], p["dkappe_h"], [0, 0, L], body="Deckelkappe", mat="PVC grau")
    for k, x in enumerate((-p["kabel_abst"] / 2, p["kabel_abst"] / 2), 1):
        cyl(b, f"DB{k}", p["kabel_d"], p["dkappe_h"] + 2, [x, 0, L - 1], op="cut", targets=["Deckelkappe"])
    for k, z in enumerate((p["schelle_z1"], p["schelle_z2"]), 1):
        nm = f"Schelle_{k}"
        cyl(b, f"S{k}", p["schelle_od"], p["schelle_h"], [0, 0, z], body=nm, mat=STEEL)
        cyl(b, f"SB{k}", r, p["schelle_h"] + 2, [0, 0, z - 1], op="cut", targets=[nm])
        bx(b, f"Ohr{k}", p["schelle_od"] / 2 - 4, p["schelle_od"] / 2 + p["ohr_len"], -p["ohr_w"] / 2, p["ohr_w"] / 2, z, z + p["schelle_h"], op="join", targets=[nm])

def c_zelle(b, p):
    L, H, W = p["laenge"], p["hoehe"], p["breite"]
    bx(b, "Z", 0, L, -W / 2, W / 2, -H / 2, H / 2, body="Zellkoerper", mat="PVC grau")
    cyl(b, "ZB", p["bohr_d"], L + 2, [-1, 0, 0], axis=(1, 0, 0), op="cut", targets=["Zellkoerper"])
    for k, x in enumerate(p["stutzen_x"], 1):
        cyl(b, f"ST{k}", p["stutzen_d"], p["stutzen_h"] + 1, [x, 0, H / 2 - 1], op="join", targets=["Zellkoerper"])
    for k, x in enumerate(p["stutzen_x"], 1):
        cyl(b, f"STB{k}", p["stutzen_id"], H / 2 + p["stutzen_h"] + 2, [x, 0, 0], op="cut", targets=["Zellkoerper"])
    for nm, x0, ax in (("Anschluss_Zulauf", 0, -1), ("Anschluss_Ablauf", L, 1)):
        cyl(b, nm + "_R", p["anschl_d"], p["anschl_l"], [x0, 0, 0], axis=(ax, 0, 0), body=nm, mat="PVC grau")
        cyl(b, nm + "_B", p["anschl_id"], p["anschl_l"] + 2, [x0 + ax * -1, 0, 0], axis=(ax, 0, 0), op="cut", targets=[nm])
    xh = L + p["anschl_l"]
    bx(b, "H", xh, xh + p["hahn_l"], -p["hahn_b"] / 2, p["hahn_b"] / 2, -p["hahn_b"] / 2, p["hahn_b"] / 2, body="Absperrhahn", mat="PVC blau")
    cyl(b, "HB", p["anschl_id"], p["hahn_l"] + 2, [xh - 1, 0, 0], axis=(1, 0, 0), op="cut", targets=["Absperrhahn"])
    cyl(b, "HS", 8, 15, [xh + p["hahn_l"] / 2, 0, p["hahn_b"] / 2 - 1], op="join", targets=["Absperrhahn"])
    bx(b, "HH", xh + p["hahn_l"] / 2 - 4, xh + p["hahn_l"] / 2 + 4, -35, 35, p["hahn_b"] / 2 + 12, p["hahn_b"] / 2 + 18, op="join", targets=["Absperrhahn"])        # Hebel quer zur Strömung = geschlossen

# ---------------------------------------------------------------- Spezifikation
def P(**kw):
    return kw

def tauch_ports(p):
    L, so = p["laenge"], p["schelle_od"]
    return [("Kabeldurchfuehrung (Kappe, Sonde haengt im Rohr d40)", f"Bohrung d{p['kabel_d']}", (0, 0, L + p["kappe_h"]), (0, 0, 1), "Kappe", True),
            ("Beckenrand-Anlage (Unterkante Klemmarm auf dem Rand)", "Arm 30 breit, Haken 80", (so / 2 + 100, 0, p["schelle_z"]), (0, 0, -1), "Klemme", False)]

def beruhig_ports(p):
    L = p["laenge"]
    out = [(f"Kabeldurchfuehrung {k} (Deckelkappe, Schwimmerkabel)", f"Bohrung d{p['kabel_d']}", (x, 0, L + p["dkappe_h"]), (0, 0, 1), "Deckelkappe", True)
           for k, x in enumerate((-p["kabel_abst"] / 2, p["kabel_abst"] / 2), 1)]
    out += [(f"Wandbefestigung {k} (Ohr der Rohrschelle)", "Ohr 25 breit", (p["schelle_od"] / 2 + p["ohr_len"], 0, z), (1, 0, 0), f"Schelle_{k}", True) for k, z in enumerate((p["schelle_z1"] + p["schelle_h"] / 2, p["schelle_z2"] + p["schelle_h"] / 2), 1)]
    return out

def zelle_ports(p):
    L, H = p["laenge"], p["hoehe"]
    out = [("Zulauf (Anschluss d20, Abzweig Sammelrohr)", "Stutzen d20, ID 14", (-p["anschl_l"], 0, 0), (-1, 0, 0), "Anschluss_Zulauf", True),
           ("Ablauf (hinter dem Absperrhahn)", "Hahn d20, ID 14", (L + p["anschl_l"] + p["hahn_l"], 0, 0), (1, 0, 0), "Absperrhahn", True)]
    out += [(f"Sondenstutzen {k} ({['pH', 'EC', 'Temperatur'][k - 1]})", f"d{p['stutzen_d']}, Bohrung {p['stutzen_id']}", (x, 0, H / 2 + p["stutzen_h"]), (0, 0, 1), "Zellkoerper", True) for k, x in enumerate(p["stutzen_x"], 1)]
    return out

COMPS = {}
def add(key, **kw):
    COMPS[key] = kw

add("halter_tauch", id="H_TAUCH", kind="halter", nr="T90a", titel="Beckenrand-Tauchhalter", fn=c_tauch, ports=tauch_ports,
    ks="Z hoch; Ursprung = Mitte der unteren Rohrkante (Tauchende); +X zeigt vom Rohr ueber den Beckenrand",
    funktion="Rohr d40 mit Klemme am Beckenrand, 0,3-0,7 m Eintauchtiefe, Sonde ohne Werkzeug herausziehbar (R39 H_TAUCH, 5 Stueck)",
    params={"laenge": (1000, "mm", "[E] Rohrlaenge: Klemme bei 640 mm, Beckenrand Z 650 minus Spiegel 515 = 135 mm Freibord, Eintauchtiefe 505 mm (R39: 0,3-0,7 m)"),
            "rohr_d": (40, "mm", "[E] Rohr PVC-U d40 (R39 H_TAUCH; Bibliothek T70)"), "rohr_wall": (LT.wall_p(40), "mm", "[E] PVC-U SDR 21 (leitung.wall_p)"),
            "bohr_d": (10, "mm", "[A] zwei Querbohrungen d10 am Tauchende (Wasserzutritt, Z 30 und 70)"), "kappe_d": (44, "mm", "[A] Kappe PA schwarz"), "kappe_h": (20, "mm", "[A]"),
            "kabel_d": (8, "mm", "[A] Kabelbohrung d8 (Atlas-Kabel 1-3 m)"), "schelle_z": (640, "mm", "[E] Unterkante Klemmarm = Beckenrand-Auflage (Rand Z 650: Eintauchtiefe 505)"),
            "schelle_od": (52, "mm", "[A] Klemmring Stahl, Wand 6"), "schelle_h": (20, "mm", "[A]"), "arm_len": (190, "mm", "[A] Arm ueber den Rand (Beckenwand 150 mm + 40 Luft)"),
            "arm_w": (30, "mm", "[A]"), "haken_h": (80, "mm", "[A] Haken aussen am Rand")},
    teile=[("Tauchrohr", "PVC-U d40 x 1,9, 1000 lang, 2 Querbohrungen d10", "PVC grau", "E"), ("Kappe", "Kappe d44 x 20 mit Kabelbohrung d8", "PA schwarz", "A"),
           ("Klemme", "Klemmring d52 mit Arm 190 x 30 und Haken 80 (ein Stahlteil)", STEEL, "A")])
add("halter_beruhig", id="H_BERUHIG", kind="halter", nr="T90b", titel="Beruhigungsrohr fuer Schwimmerschalter", fn=c_beruhig, ports=beruhig_ports,
    ks="Z hoch; Ursprung = Mitte der Rohrunterkante (Boden des Rohrs, Bodenkappe darunter); +X zur Wand",
    funktion="PVC-U d63 senkrecht, geschlitzt, 2 Schwimmerschalter (Niedrig/Hoch) (R39 H_BERUHIG, 14 Stueck)",
    params={"laenge": (600, "mm", "[A] Rohrlaenge: zwei Schwimmer im Abstand bis 300 mm im geschlitzten Bereich"), "rohr_d": (63, "mm", "[E] Rohr PVC-U d63 (R39)"), "rohr_wall": (LT.wall_p(63), "mm", "[E] PVC-U SDR 21"),
            "schlitz_l": (360, "mm", "[A] Schlitzlaenge, mittig"), "schlitz_w": (8, "mm", "[A] Schlitzbreite, 4 Schlitze (je 2 durch das Rohr)"), "kappe_d": (70, "mm", "[A] Bodenkappe"), "kappe_h": (20, "mm", "[A]"),
            "dkappe_h": (30, "mm", "[A] Deckelkappe"), "kabel_d": (12, "mm", "[A] 2 Kabelbohrungen d12"), "kabel_abst": (24, "mm", "[A]"),
            "schelle_z1": (100, "mm", "[A] untere Rohrschelle"), "schelle_z2": (480, "mm", "[A] obere Rohrschelle"), "schelle_od": (75, "mm", "[A] Rohrschelle Stahl 6 mm Wand"), "schelle_h": (15, "mm", "[A]"),
            "ohr_len": (30, "mm", "[A] Befestigungsohr"), "ohr_w": (25, "mm", "[A]")},
    teile=[("Rohr", "PVC-U d63 x 3,0, 600 lang, 4 Schlitze 8 x 360", "PVC grau", "E"), ("Bodenkappe", "Kappe d70 x 20, geschlossen", "PVC grau", "A"), ("Deckelkappe", "Kappe d70 x 30 mit 2 Kabelbohrungen d12", "PVC grau", "A"),
           ("Schelle_1", "Rohrschelle d75 x 15 mit Ohr (unten)", STEEL, "A"), ("Schelle_2", "Rohrschelle d75 x 15 mit Ohr (oben)", STEEL, "A")])
add("halter_zelle", id="H_ZELLE", kind="halter", nr="T90c", titel="Durchflusszelle mit 3 Sondenstutzen", fn=c_zelle, ports=zelle_ports,
    ks="X = Strommrichtung (Zulauf -X, Ablauf +X), Z hoch; Ursprung = Mitte der Zulaufseite des Zellkoerpers",
    funktion="Durchflusszelle am Abzweig d20 des Sammelrohrs mit 3 Sondenstutzen (pH, EC, Temperatur) und Absperrhahn (R39 H_ZELLE, 2 Stueck: MS40, MS41)",
    params={"laenge": (220, "mm", "[A] Zellkoerper PVC-Block 220 x 44 x 44"), "breite": (44, "mm", "[A]"), "hoehe": (44, "mm", "[A]"), "bohr_d": (28, "mm", "[A] Durchgangsbohrung d28 (Zellvolumen ca. 0,13 l)"),
            "stutzen_x": ([40, 110, 180], "mm", "[A] Lage der Sondenstutzen (pH, EC, Temperatur)"), "stutzen_d": (25, "mm", "[E] Stutzen d25 wie die Sondenstutzen im Deckel der Messzelle (puffer_klein)"),
            "stutzen_id": (16, "mm", "[A] Bohrung fuer Sonde mit Kabelverschraubung"), "stutzen_h": (30, "mm", "[A]"), "anschl_d": (20, "mm", "[E] Anschlussstutzen d20 (R39)"),
            "anschl_id": (14, "mm", "[A]"), "anschl_l": (30, "mm", "[A]"), "hahn_l": (40, "mm", "[A] Absperrhahn Gehaeuse 40 x 28 x 28"), "hahn_b": (28, "mm", "[A]")},
    teile=[("Zellkoerper", "PVC-Block 220 x 44 x 44, Bohrung d28, 3 Stutzen d25 mit Bohrung d16", "PVC grau", "A"), ("Anschluss_Zulauf", "Stutzen d20 x 30, ID 14", "PVC grau", "E"),
           ("Anschluss_Ablauf", "Stutzen d20 x 30, ID 14", "PVC grau", "E"), ("Absperrhahn", "Kugelhahn d20 (Block 40 x 28 x 28) mit Spindel und Hebel", "PVC blau", "E")])

# ---------------------------------------------------------------- Halter, Teil 2
def c_inline(b, p):
    d = p["d"]; w = LT.wall_p(d); idd = d - 2 * w; ob = p["block"]; h = ob / 2
    for nm, x0 in (("Verschraubung_A", -p["nut_l"]), ("Verschraubung_B", p["x_end"])):
        cyl(b, nm + "_R", d + 22, p["nut_l"], [x0, 0, 0], axis=(1, 0, 0), body=nm, mat="PVC blau")
        cyl(b, nm + "_B", idd, p["nut_l"] + 2, [x0 - 1, 0, 0], axis=(1, 0, 0), op="cut", targets=[nm])
    bx(b, "VF", 0, p["filter_l"], -h, h, -h, h, body="Vorfilter", mat="PVC grau")
    cyl(b, "VFB", idd, p["filter_l"] + 2, [-1, 0, 0], axis=(1, 0, 0), op="cut", targets=["Vorfilter"])
    kd = p["kappe_d"]; xm = p["filter_l"] / 2
    cyl(b, "FK", kd, p["kappe_h"] + 1, [xm, 0, -h + 1], axis=(0, 0, -1), op="join", targets=["Vorfilter"])
    cyl(b, "FKB", kd - 8, 46, [xm, 0, -h - p["kappe_h"] - 1], op="cut", targets=["Vorfilter"])
    ztop = -h + 5                                                                 # Oberkante der Kappenhoehlung (Sieb liegt oben an)
    cyl(b, "SIEB", kd - 10, 30, [xm, 0, ztop - 30], body="Sieb", mat="Edelstahl")
    cyl(b, "SIEBB", kd - 14, 29, [xm, 0, ztop - 31], op="cut", targets=["Sieb"])
    bx(b, "BS", p["filter_l"], p["filter_l"] + p["strecke_l"], -h, h, -h, h, body="Beruhigungsstrecke", mat="PVC grau")
    cyl(b, "BSB", idd, p["strecke_l"] + 2, [p["filter_l"] - 1, 0, 0], axis=(1, 0, 0), op="cut", targets=["Beruhigungsstrecke"])
    x1 = p["filter_l"] + p["strecke_l"]
    bx(b, "SB", x1, x1 + p["sensor_l"], -h, h, -h, h, body="Sensorblock", mat="PVC grau")
    cyl(b, "SBB", idd, p["sensor_l"] + 2, [x1 - 1, 0, 0], axis=(1, 0, 0), op="cut", targets=["Sensorblock"])
    cyl(b, "SS", p["sitz_d"], p["sitz_h"] + 1, [x1 + p["sensor_l"] / 2, 0, h - 1], op="join", targets=["Sensorblock"])
    cyl(b, "SSB", p["sitz_id"], h + p["sitz_h"] + 2, [x1 + p["sensor_l"] / 2, 0, 0], op="cut", targets=["Sensorblock"])

def inline_ports(p):
    h = p["block"] / 2
    x1 = p["filter_l"] + p["strecke_l"]
    return [("Zulauf (Verschraubung, Rohr d%d)" % p["d"], f"Rohr d{p['d']}", (-p["nut_l"], 0, 0), (-1, 0, 0), "Verschraubung_A", True),
            ("Ablauf (Verschraubung, Rohr d%d)" % p["d"], f"Rohr d{p['d']}", (p["x_end"] + p["nut_l"], 0, 0), (1, 0, 0), "Verschraubung_B", True),
            ("Sensorsitz (Paddelrad / Ultraschall, Bohrung d%d)" % p["sitz_id"], f"d{p['sitz_d']}", (x1 + p["sensor_l"] / 2, 0, h + p["sitz_h"]), (0, 0, 1), "Sensorblock", True),
            ("Filterwechsel / Entleerung (Kappe unten)", f"Kappe d{p['kappe_d']}", (p["filter_l"] / 2, 0, -h - p["kappe_h"]), (0, 0, -1), "Vorfilter", True)]

def inline_params(d):
    wl = LT.wall_p(d)
    ob = d + 20
    return {"d": (d, "mm", "[E] Rohr-Aussendurchmesser PVC-U (R39 H_INLINE; flow_12 an d32, flow_gross an d50, K10/K26)"), "wand": (wl, "mm", "[E] PVC-U SDR 21"), "block": (ob, "mm", "[A] Vierkantblock d + 20 (Messstueck und Vorfilter aus PVC-Block gebohrt)"),
            "nut_l": (30, "mm", "[A] Verschraubung (Union) 30 lang, Aussen d + 22"), "filter_l": (110, "mm", "[A] Vorfilterblock"), "strecke_l": (200, "mm", "[R] 20 cm gerade Strecke vor dem Messer (R39 H_INLINE: Herstellervorgabe Paddelrad)"),
            "sensor_l": (100, "mm", "[A] Messblock mit Sensorsitz"), "x_end": (110 + 200 + 100, "mm", "[R] Ende des Messblocks = filter_l + strecke_l + sensor_l"),
            "kappe_d": (int(round(ob * 0.7)), "mm", "[A] Filterkappe 0,7 x Block"), "kappe_h": (40, "mm", "[A] Kappe unter dem Block; Sieb >= 80 um (R39) Edelstahlgewebe, Maschenweite nicht modelliert"),
            "sitz_d": (30, "mm", "[A] Sensorsitz (Gewindestutzen fuer Atlas-Paddelrad 1/2 Zoll, Hersteller-Datenblatt nicht gelesen)"), "sitz_id": (22, "mm", "[A] Bohrung Sensorsitz"), "sitz_h": (25, "mm", "[A]")}

def c_hahn(b, p):
    bx(b, "AS", -p["sattel_l"] / 2, p["sattel_l"] / 2, -p["sattel_b"] / 2, p["sattel_b"] / 2, 0, p["sattel_h"], body="Anbohrschelle", mat="PVC grau")
    cyl(b, "AST", p["stutzen_d"], p["stutzen_h"] + 1, [0, 0, p["sattel_h"] - 1], op="join", targets=["Anbohrschelle"])
    cyl(b, "ASB", p["bohr_d"], p["sattel_h"] + p["stutzen_h"] + 2, [0, 0, -1], op="cut", targets=["Anbohrschelle"])
    z0 = p["sattel_h"] + p["stutzen_h"]; kb = p["hahn_b"]
    bx(b, "KH", -kb / 2, kb / 2, -kb / 2, kb / 2, z0, z0 + p["hahn_h"], body="Kugelhahn", mat="PVC blau")
    cyl(b, "KHB", p["bohr_d"], p["hahn_h"] + 2, [0, 0, z0 - 1], op="cut", targets=["Kugelhahn"])
    cyl(b, "KHS", 8, 9, [0, 0, z0 + p["hahn_h"] - 1], op="join", targets=["Kugelhahn"])
    bx(b, "KHH", -5, p["hebel_l"], -4, 4, z0 + p["hahn_h"] + 8, z0 + p["hahn_h"] + 13, op="join", targets=["Kugelhahn"])
    cyl(b, "TU", p["tuelle_d"], p["tuelle_l"], [kb / 2, 0, z0 + p["hahn_h"] / 2], axis=(1, 0, 0), body="Schlauchtuelle", mat="PVC grau")
    cyl(b, "TUB", p["tuelle_id"], p["tuelle_l"] + 2, [kb / 2 - 1, 0, z0 + p["hahn_h"] / 2], axis=(1, 0, 0), op="cut", targets=["Schlauchtuelle"])

def hahn_params():
    return {"sattel_l": (60, "mm", "[A] Anbohrschelle 60 x 50 x 20 (flache Platte statt Rohrsattel; Rohr d20-d63)"), "sattel_b": (50, "mm", "[A]"), "sattel_h": (20, "mm", "[A]"), "stutzen_d": (25, "mm", "[A] Stutzen d25 (R3/4)"),
            "stutzen_h": (20, "mm", "[A]"), "bohr_d": (12, "mm", "[A] Durchgang d12"), "hahn_b": (30, "mm", "[A] Kugelhahn d16/d20 Gehaeuse 30 x 30 x 36 (R39 hahn_probe)"), "hahn_h": (36, "mm", "[A]"),
            "hebel_l": (65, "mm", "[A] Hebel 70 lang, 8 breit"), "tuelle_d": (14, "mm", "[A] Schlauchtuelle d14 fuer Schlauch ID 12 (Probenahme per Hand)"), "tuelle_id": (8, "mm", "[A]"), "tuelle_l": (40, "mm", "[A]")}

def hahn_ports(p):
    z0 = p["sattel_h"] + p["stutzen_h"]
    return [("Rohr-Anlage (Unterkante Anbohrschelle auf dem Rohr)", "Anbohrschelle d20-d63", (0, 0, 0), (0, 0, -1), "Anbohrschelle", True),
            ("Probenahme (Schlauchtuelle)", f"Tuelle d{p['tuelle_d']}", (p["hahn_b"] / 2 + p["tuelle_l"], 0, z0 + p["hahn_h"] / 2), (1, 0, 0), "Schlauchtuelle", True)]

def c_druck(b, p):
    bx(b, "AS", -p["sattel_l"] / 2, p["sattel_l"] / 2, -p["sattel_b"] / 2, p["sattel_b"] / 2, 0, p["sattel_h"], body="Anbohrschelle", mat="PVC grau")
    cyl(b, "AST", p["stutzen_d"], p["stutzen_h"] + 1, [0, 0, p["sattel_h"] - 1], op="join", targets=["Anbohrschelle"])
    cyl(b, "ASB", p["bohr_d"], p["sattel_h"] + p["stutzen_h"] + 2, [0, 0, -1], op="cut", targets=["Anbohrschelle"])
    z0 = p["sattel_h"] + p["stutzen_h"]
    cyl(b, "NI", p["sechs_d"], p["sechs_h"], [0, 0, z0], body="Gewindenippel", mat="Messing")
    cyl(b, "NIG", p["gewinde_d"], p["gewinde_h"] + 1, [0, 0, z0 + p["sechs_h"] - 1], op="join", targets=["Gewindenippel"])
    cyl(b, "NIB", p["nippel_id"], p["sechs_h"] + p["gewinde_h"] + 2, [0, 0, z0 - 1], op="cut", targets=["Gewindenippel"])

def druck_params():
    d = hahn_params()
    out = {k: d[k] for k in ("sattel_l", "sattel_b", "sattel_h", "stutzen_d", "stutzen_h", "bohr_d")}
    out.update({"sechs_d": (19, "mm", "[A] Sechskantteil des Nippels (Schluesselweite 19, als Zylinder)"), "sechs_h": (12, "mm", "[A]"),
                "gewinde_d": (13.2, "mm", "[E] Gewinde R1/4 Aussen 13,157 mm (DIN EN 10226)"), "gewinde_h": (15, "mm", "[A] Gewindelaenge"), "nippel_id": (6, "mm", "[A] Durchgang d6")})
    return out

def druck_ports(p):
    z0 = p["sattel_h"] + p["stutzen_h"]
    return [("Rohr-Anlage (Unterkante Anbohrschelle auf Rohr oder Luftleitung)", "Anbohrschelle d20-d63", (0, 0, 0), (0, 0, -1), "Anbohrschelle", True),
            ("Druckanschluss R1/4 (Druckschalter)", "R1/4 aussen", (0, 0, z0 + p["sechs_h"] + p["gewinde_h"]), (0, 0, 1), "Gewindenippel", True)]

def c_mast(b, p):
    bx(b, "FP", -p["platte"] / 2, p["platte"] / 2, -p["platte"] / 2, p["platte"] / 2, 0, p["platte_t"], body="Fussplatte", mat=STEEL)
    cyl(b, "MR", p["rohr_d"], p["hoehe"] - p["platte_t"], [0, 0, p["platte_t"]], body="Mastrohr", mat="PVC grau")
    cyl(b, "MRB", p["rohr_d"] - 2 * p["rohr_wall"], p["hoehe"] + 2, [0, 0, p["platte_t"] - 1], op="cut", targets=["Mastrohr"])
    cyl(b, "SP", p["spindel_d"], p["schirm_h"], [0, 0, p["hoehe"]], body="Strahlungsschutz", mat="PP weiss")
    for k in range(3):
        cyl(b, f"SD{k}", p["schirm_d"], 3, [0, 0, p["hoehe"] + 4 + 14 * k], op="join", targets=["Strahlungsschutz"])

def mast_params():
    return {"hoehe": (1700, "mm", "[E] Kopfhoehe 1,7 m (R39 H_MAST), Oberkante Mastrohr"), "rohr_d": (32, "mm", "[E] Rohr PVC-U d32 (R39)"), "rohr_wall": (LT.wall_p(32), "mm", "[E] PVC-U SDR 21"),
            "platte": (100, "mm", "[A] Fussplatte Stahl 100 x 100 x 6, 4 Duebel (nicht modelliert)"), "platte_t": (6, "mm", "[A]"), "spindel_d": (20, "mm", "[A] Strahlungsschutz Spindel"),
            "schirm_d": (90, "mm", "[A] Lamellenscheiben d90, 3 Stueck im Abstand 14"), "schirm_h": (36, "mm", "[A] Hoehe des Strahlungsschutzes")}

def mast_ports(p):
    return [("Fuss (Unterkante Fussplatte auf dem Boden)", "Platte 100 x 100", (0, 0, 0), (0, 0, -1), "Fussplatte", True),
            ("Sensoraufnahme (Strahlungsschutz oben)", "Spindel d20, SCD41-Platine / PAR-Sensor", (0, 0, p["hoehe"] + p["schirm_h"]), (0, 0, 1), "Strahlungsschutz", True)]

def c_box(b, p):
    l, w, h, wa = p["l"], p["w"], p["h"], p["wand"]
    bx(b, "G", -l / 2, l / 2, -w / 2, w / 2, 0, h, body="Gehaeuse", mat="PS grau")
    bx(b, "GH", -l / 2 + wa, l / 2 - wa, -w / 2 + wa, w / 2 - wa, wa, h + 1, op="cut", targets=["Gehaeuse"])
    for k, x in enumerate(p["kabel_x"], 1):
        cyl(b, f"GL{k}", p["kabel_id"], wa + 2, [x, p["kabel_y"], -1], op="cut", targets=["Gehaeuse"])
    bx(b, "D", -l / 2, l / 2, -w / 2, w / 2, h, h + p["deckel_t"], body="Deckel", mat="Acryl klar")
    bx(b, "HS", -p["schiene_l"] / 2, p["schiene_l"] / 2, -17.5, 17.5, wa, wa + 7.5, body="Hutschiene", mat=STEEL)
    for k, x in enumerate(p["kabel_x"], 1):
        nm = f"Verschraubung_{k}"
        cyl(b, f"V{k}", p["kabel_d"], p["kabel_l"], [x, p["kabel_y"], -p["kabel_l"]], body=nm, mat="PA schwarz")
        cyl(b, f"VB{k}", p["kabel_id"], p["kabel_l"] + 2, [x, p["kabel_y"], -p["kabel_l"] - 1], op="cut", targets=[nm])
    for k, sx in enumerate((-1, 1), 1):
        nm = f"Wandlasche_{k}"
        x0, x1 = (l / 2, l / 2 + p["lasche_l"]) if sx > 0 else (-l / 2 - p["lasche_l"], -l / 2)
        bx(b, f"WL{k}", x0, x1, -15, 15, p["lasche_z"], p["lasche_z"] + p["lasche_t"], body=nm, mat=STEEL)
        cyl(b, f"WLB{k}", 6, p["lasche_t"] + 2, [sx * (l / 2 + p["lasche_l"] - 15), 0, p["lasche_z"] - 1], op="cut", targets=[nm])

def box_params():
    return {"l": (200, "mm", "[A] IP65-Gehaeuse 200 x 150 x 100 (ESP32/Rechner, EZO-Schaltkreise, Isolatoren, R39 H_BOX; Handelsmass ueblich)"), "w": (150, "mm", "[A]"), "h": (100, "mm", "[A]"), "wand": (4, "mm", "[A] Wand PS"),
            "deckel_t": (4, "mm", "[A] Klardeckel Acryl"), "schiene_l": (150, "mm", "[E] Hutschiene TS35 35 x 7,5 (DIN EN 60715), 150 lang"), "kabel_x": ([-60, -20, 20, 60], "mm", "[A] 4 Kabelverschraubungen M16 in der Bodenwand"),
            "kabel_y": (-50, "mm", "[A]"), "kabel_d": (20, "mm", "[A] Verschraubung M16 aussen d20"), "kabel_id": (10, "mm", "[A] Durchgang d10 (Atlas-Koaxkabel, Bus 4 Adern + 24 V)"), "kabel_l": (12, "mm", "[A]"),
            "lasche_l": (30, "mm", "[A] Wandlasche 30 x 30 x 3"), "lasche_t": (3, "mm", "[A]"), "lasche_z": (40, "mm", "[A]")}

def box_ports(p):
    out = [("Trunk (RS-485 4 Adern + 24 V DC 2 Adern)", "Verschraubung M16", (p["kabel_x"][0], p["kabel_y"], -p["kabel_l"]), (0, 0, -1), "Verschraubung_1", True)]
    out += [(f"Sondenanschluss {k - 1} (Koax / Kabel)", "Verschraubung M16", (x, p["kabel_y"], -p["kabel_l"]), (0, 0, -1), f"Verschraubung_{k}", True) for k, x in enumerate(p["kabel_x"][1:], 2)]
    out += [(f"Wandbefestigung {k}", "Lasche 30 x 30 x 3, Loch d6", (sx * (p["l"] / 2 + p["lasche_l"]), 0, p["lasche_z"] + p["lasche_t"] / 2), (sx, 0, 0), f"Wandlasche_{k}", True) for k, sx in enumerate((-1, 1), 1)]
    return out

add("halter_inline_d32", id="H_INLINE", variant="d32", kind="halter", nr="T90d", titel="Einbaustueck Durchflussmesser d32 mit Vorfilter", fn=c_inline, ports=inline_ports,
    ks="X = Stroemungsrichtung (Zulauf -X), Z hoch; Ursprung = Achse an der Vorfilter-Eintrittsseite",
    funktion="Rohrstueck mit Verschraubung, 20 cm gerade Strecke vor dem Messer und Vorfilter >= 80 um (R39 H_INLINE, 9 Stueck: MS12/13, MS34-39, MS50), Groesse d32 (flow_12)",
    params=inline_params(32),
    teile=[("Verschraubung_A", "Union d54 x 30 (Zulauf), Rohr d32", "PVC blau", "A"), ("Vorfilter", "Block 52 x 52 x 110 mit Filterkappe d36 x 40", "PVC grau", "A"), ("Sieb", "Siebkorb Edelstahl d26 x 30 (>= 80 um, Gewebe nicht modelliert)", "Edelstahl", "A"),
           ("Beruhigungsstrecke", "Block 52 x 52 x 200, Bohrung = Rohr-ID (20 cm gerade Strecke)", "PVC grau", "R"), ("Sensorblock", "Block 52 x 52 x 100 mit Sensorsitz d30 x 25", "PVC grau", "A"),
           ("Verschraubung_B", "Union d54 x 30 (Ablauf), Rohr d32", "PVC blau", "A")])
add("halter_inline_d50", id="H_INLINE", variant="d50", kind="halter", nr="T90e", titel="Einbaustueck Durchflussmesser d50 mit Vorfilter", fn=c_inline, ports=inline_ports,
    ks="X = Stroemungsrichtung (Zulauf -X), Z hoch; Ursprung = Achse an der Vorfilter-Eintrittsseite",
    funktion="wie H_INLINE d32, Groesse d50 fuer die Hauptleitungen K10/K26 (110 l/min, flow_gross)",
    params=inline_params(50),
    teile=[("Verschraubung_A", "Union d72 x 30 (Zulauf), Rohr d50", "PVC blau", "A"), ("Vorfilter", "Block 70 x 70 x 110 mit Filterkappe d49 x 40", "PVC grau", "A"), ("Sieb", "Siebkorb Edelstahl d39 x 30 (>= 80 um, Gewebe nicht modelliert)", "Edelstahl", "A"),
           ("Beruhigungsstrecke", "Block 70 x 70 x 200, Bohrung = Rohr-ID (20 cm gerade Strecke)", "PVC grau", "R"), ("Sensorblock", "Block 70 x 70 x 100 mit Sensorsitz d30 x 25", "PVC grau", "A"),
           ("Verschraubung_B", "Union d72 x 30 (Ablauf), Rohr d50", "PVC blau", "A")])
add("halter_hahn", id="H_HAHN", kind="halter", nr="T90f", titel="Probenahmehahn", fn=c_hahn, ports=hahn_ports,
    ks="Z hoch; Ursprung = Mitte der Unterseite der Anbohrschelle (Anlage am Rohr); Tuelle zeigt nach +X",
    funktion="Kugelhahn d16/d20 mit Schlauchtuelle an einer Anbohrschelle, Handmessung mit Tropfentest oder Photometer (R39 H_HAHN, 5 Stueck)", params=hahn_params(),
    teile=[("Anbohrschelle", "Platte 60 x 50 x 20 mit Stutzen d25 x 20", "PVC grau", "A"), ("Kugelhahn", "Gehaeuse 30 x 30 x 36 mit Spindel und Hebel", "PVC blau", "A"), ("Schlauchtuelle", "Tuelle d14 x 40 mit Bohrung d8", "PVC grau", "A")])
add("halter_druck", id="H_DRUCK", kind="halter", nr="T90g", titel="Druckschalter-Stutzen R1/4", fn=c_druck, ports=druck_ports,
    ks="Z hoch; Ursprung = Mitte der Unterseite der Anbohrschelle; Gewinde zeigt nach +Z",
    funktion="Anschlussstutzen R1/4 am Rohr bzw. an der Luftleitung fuer den Druckschalter (R39 H_DRUCK, 6 Stueck)", params=druck_params(),
    teile=[("Anbohrschelle", "Platte 60 x 50 x 20 mit Stutzen d25 x 20", "PVC grau", "A"), ("Gewindenippel", "Messing, Sechskant d19 x 12 mit Gewinde R1/4 x 15, Durchgang d6", "Messing", "E")])
add("halter_mast", id="H_MAST", kind="halter", nr="T90h", titel="Sensor-Mast Kuppel", fn=c_mast, ports=mast_ports,
    ks="Z hoch; Ursprung = Mitte der Unterseite der Fussplatte (Boden)",
    funktion="Rohr d32 mit Strahlungsschutz, Hoehe 1,7 m (Kopfhoehe) bzw. am Scheitel (R39 H_MAST, 5 Stueck: MS59-MS62)", params=mast_params(),
    teile=[("Fussplatte", "Stahl 100 x 100 x 6", STEEL, "A"), ("Mastrohr", "PVC-U d32 x 1,5, Oberkante Z 1700", "PVC grau", "E"), ("Strahlungsschutz", "Spindel d20 mit 3 Lamellenscheiben d90 (weiss)", "PP weiss", "A")])
add("halter_box", id="H_BOX", kind="halter", nr="T90i", titel="Messknoten-Gehaeuse IP65", fn=c_box, ports=box_ports,
    ks="Z hoch; Ursprung = Mitte der Gehaeuse-Unterseite; Verschraubungen zeigen nach -Z (Kabel nach unten), Laschen +-X",
    funktion="Messknoten-Gehaeuse IP65 mit Hutschiene (ESP32/Rechner, EZO-Schaltkreise, Isolatoren) neben dem Halter (R39 H_BOX, 7 Stueck, Messknoten mk_*)", params=box_params(),
    teile=[("Gehaeuse", "PS 200 x 150 x 100, Wand 4, 4 Durchgaenge d10", "PS grau", "A"), ("Deckel", "Klardeckel Acryl 200 x 150 x 4", "Acryl klar", "A"), ("Hutschiene", "TS35 35 x 7,5 x 150", STEEL, "E"),
           ("Verschraubung_1", "Kabelverschraubung M16 (Trunk)", "PA schwarz", "A"), ("Verschraubung_2", "Kabelverschraubung M16 (Sonde 1)", "PA schwarz", "A"), ("Verschraubung_3", "Kabelverschraubung M16 (Sonde 2)", "PA schwarz", "A"),
           ("Verschraubung_4", "Kabelverschraubung M16 (Sonde 3)", "PA schwarz", "A"), ("Wandlasche_1", "Stahl 30 x 30 x 3, Loch d6", STEEL, "A"), ("Wandlasche_2", "Stahl 30 x 30 x 3, Loch d6", STEEL, "A")])

# ---------------------------------------------------------------- Bau
def build(key):
    c = COMPS[key]
    p = {k: v[0] for k, v in c["params"].items()}
    b = sc.Build()
    for k, (v, u, _h) in c["params"].items():
        if u in ("mm", "deg") and not isinstance(v, list):
            b.add("parameters.add", name=k, expression=f"{v} {u}")
    for nm, (dens, col) in MATS.items():
        b.add("material.create", name=nm, density_g_cm3=dens, color=col, **({"pbr": {"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5}} if nm == STEEL else {}))
    root = f"{c['nr']}_{c['id']}" if "variant" not in c else f"{c['nr']}_{c['id']}_{c['variant']}"
    b.add("component.create", name=root, grounded=True)
    c["fn"](b, p)
    b.add("component.metadata.set", component=root, part_number=c["nr"], description=f"{c['titel']}: {c['funktion']}", revision="A", properties={"Werkstoff": "PVC-U / Stahl verzinkt / PA nach Teil"})
    return b, p

def main(keys):
    for key in keys:
        b, p = build(key)
        out = os.path.join(sc.ROOT, "designs", "components", key + ".sc")
        sc.run(b.write(key), out)
        ev = sc.evaluate(out)
        mn, mx = sc.bbox_all(ev)
        print(key, "Koerper", len(ev["bodies"]), [b_["name"] for b_ in ev["bodies"]], "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx], "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 3), "kg", flush=True)

if __name__ == "__main__":
    keys = [a for a in sys.argv[1:] if not a.startswith("--")] or list(COMPS)
    main(keys)
