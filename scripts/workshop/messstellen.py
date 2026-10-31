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
        "Sonde schwarz": (1.2, "#2b2b2b"), "Platine gruen": (1.8, "#1f7a3a"), "Schwimmer orange": (0.6, "#e8801a"), "Kontakt rot": (1.4, "#b3302b")}

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
