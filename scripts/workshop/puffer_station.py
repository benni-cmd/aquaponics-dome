"""Puffer-Station T81 (W28, D46): 2 IBC (T80) uebereinander auf Stapelrahmen, Verbindungsrohr DN50, Messplatz, Dosierkonsole, Wartungsplattform mit Leiter.
KS wie puffer_ibc (Ursprung Mitte Standflaeche der unteren IBC am Boden; X Messplatz -X / Dosierkonsole +X, vorn -Y, hinten +Y).
Aufruf: python scripts/workshop/puffer_station.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

STEEL = "Stahl verzinkt"

def bar(b, name, a, z_, dims, material=STEEL):
    """Achsparalleles Rechteckrohr von Punkt a bis Punkt z_ (Mittellinie); dims = dict(width, height, wall)."""
    ax = [i for i in range(3) if abs(z_[i] - a[i]) > 1e-9]
    assert len(ax) == 1, (name, a, z_)
    i = ax[0]
    lo, hi = (a, z_) if a[i] < z_[i] else (z_, a)
    plane = {0: ([0, 1, 0], [0, 0, 1]), 1: ([0, 0, 1], [1, 0, 0]), 2: ([1, 0, 0], [0, 1, 0])}[i]
    b.add("sketch.create", plane={"origin": list(lo), "x_dir": plane[0], "y_dir": plane[1]}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind="rect_tube", **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    b.add("solid.extrude", distance=abs(hi[i] - lo[i]), name="F_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=material)

def box(b, name, cx, cy, z0, lx, ly, h, material):
    b.add("solid.box", length=lx, width=ly, height=h, center=[cx, cy, z0 + h / 2], operation="new", name="B_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=material)

def build():
    p, d = sc.load_params("puffer_station")
    pi, di = sc.load_params("puffer_ibc")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in ((STEEL, 7.85, "#aeb4b8"), ("Blech", 7.85, "#9aa0a4"), ("Kanister HDPE", 0.95, "#e8e2c8"), ("Pumpe Schlauch", 1.2, "#3a6ea5"), ("Sonde", 1.6, "#d9b13b"), ("Becher PP", 0.91, "#dfe3e6"), ("PVC grau", 1.4, "#8d9296"), ("Kanal PVC", 1.4, "#c8ccd0"), ("HDPE Palette", 0.2, "#6f767a"), ("PE Blase", 0.95, "#e9edf0"), ("PVC blau", 1.4, "#2a5da8"), ("Wasser", 1.0, "#6fb6e8")):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col, **({"pbr": {"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5}} if nm == STEEL else {}))
    root = "T81_Puffer_Station"
    b.add("component.create", name=root, grounded=True)
    # --- die zwei IBC
    b.add("component.create", name="T81a_IBC")
    for nm, z in (("IBC_unten", 0), ("IBC_oben", p["sta_z_up"])):
        b.add("component.insert_design", path="designs/components/puffer_ibc.sc", name=nm)
        if z:
            b.add("occurrence.move", occurrence=f"{nm}:1", translate=[0, 0, z])
    # --- Stapelrahmen
    b.add("component.activate", component=root)
    b.add("component.create", name="T81b_Stapelrahmen")
    t, w = p["sta_leg"], p["sta_wall"]
    dims = dict(width=t, height=t, wall=w)
    lx, ly, f = p["sta_leg_x"], p["sta_leg_y"], p["sta_foot"]
    zb0, zx0 = p["sta_beam_z"], p["sta_xbeam_z"]
    for sx in (-1, 1):
        for sy in (-1, 1):
            tag = f"{'p' if sx > 0 else 'm'}{'p' if sy > 0 else 'm'}"
            box(b, f"Fussplatte_{tag}", sx * lx, sy * ly, 0, f, f, 8, STEEL)
            bar(b, f"Bein_{tag}", [sx * lx, sy * ly, 8], [sx * lx, sy * ly, zb0], dims)
    for sx in (-1, 1):
        bar(b, f"Stirnbalken_{'p' if sx > 0 else 'm'}", [sx * lx, -(ly + t / 2), zb0 + t / 2], [sx * lx, ly + t / 2, zb0 + t / 2], dims)
    for k, y in enumerate((-420, 0, 420), 1):
        bar(b, f"Traeger_{k}", [-(lx + t / 2), y, zx0 + t / 2], [lx + t / 2, y, zx0 + t / 2], dims)
    dd = dict(width=p["sta_diag"], height=p["sta_diag"], wall=2)
    import math
    for sx in (-1, 1):                                                       # Diagonale ausserhalb der Beine (x = +-(640 + 30 + 15)), von Fuss zu Kopf der gegenueberliegenden Beine
        y0, z0, y1, z1 = -ly, 150.0, ly, zb0 - 60.0
        ln = math.hypot(y1 - y0, z1 - z0)
        dy, dz = (y1 - y0) / ln, (z1 - z0) / ln
        xo = sx * (lx + t / 2 + p["sta_diag"] / 2)
        nm = f"Diagonale_{'p' if sx > 0 else 'm'}"
        b.add("sketch.create", plane={"origin": [xo, y0, z0], "x_dir": [1, 0, 0], "y_dir": [0, dz, -dy]}, name="S_" + nm)
        b.add("frame.profile.insert", profile=dict(kind="rect_tube", **dd), at=[0, 0], anchor="center")
        b.add("sketch.finish")
        b.add("solid.extrude", distance=ln, name="F_" + nm, body_name=nm)
        b.add("material.assign", bodies=[nm], material=STEEL)
    # --- Verbindungsrohr DN50 (Platzhalter): oberer Ablauf (y -615, z 1470) -> y -660 -> hinab -> unterer Zulauf (y -545, z 1100)
    b.add("component.activate", component=root)
    b.add("component.create", name="T81c_Verbindung")
    od, px, py = pi["stub_od"], pi["port_x"], p["pipe_y"]
    zo = p["sta_z_up"] + pi["ablauf_z"]
    yo = -(pi["ibc_w"] / 2 + 5) - pi["hahn_l"] - 40                          # Ende des Ablaufzapfens (-615)
    zu = pi["zulauf_z"]
    yu = -(pi["blase_w"] / 2 + pi["stub_len_side"])                           # Ende des Zulaufzapfens (-545)
    b.add("solid.cylinder", diameter=od, height=abs(py - yo), base=[px, yo, zo], axis=[0, -1, 0], operation="new", name="V1", body_name="Verbindungsrohr")
    b.add("solid.cylinder", diameter=od, height=zo - zu + od, base=[px, py, zu - od / 2], axis=[0, 0, 1], operation="join", targets=["Verbindungsrohr"], name="V2")
    b.add("solid.cylinder", diameter=od, height=abs(py - yu), base=[px, py, zu], axis=[0, 1, 0], operation="join", targets=["Verbindungsrohr"], name="V3")
    b.add("material.assign", bodies=["Verbindungsrohr"], material="PVC grau")
    # --- Messplatz
    b.add("component.activate", component=root)
    b.add("component.create", name="T81d_Messplatz")
    mx = p["mess_x"]
    d40 = dict(width=40, height=40, wall=2)
    box(b, "Mess_Fussplatte", mx, 0, 0, 200, 200, 8, STEEL)
    bar(b, "Mess_Staender", [mx, 0, 8], [mx, 0, 1300], d40)
    bar(b, "Mess_Tellerarm", [mx + 20, 0, 870], [-1000, 0, 870], d40)
    bar(b, "Mess_Haltearm", [mx + 20, 0, 1280], [-1020, 0, 1280], d40)
    bar(b, "Mess_Querarm", [-1000, -100, 1280], [-1000, 100, 1280], d40)
    b.add("solid.cylinder", diameter=160, height=310, base=[-1000, 0, 890], axis=[0, 0, 1], operation="new", name="Becher_R", body_name="Messbecher")
    b.add("solid.cylinder", diameter=150, height=311, base=[-1000, 0, 895], axis=[0, 0, 1], operation="cut", targets=["Messbecher"], name="Becher_Hohl")
    b.add("material.assign", bodies=["Messbecher"], material="Becher PP")
    for nm, y in (("pH", -60), ("EC", -20), ("Temperatur", 20), ("O2", 60)):
        b.add("solid.cylinder", diameter=36, height=40, base=[-1000, y, 1220], axis=[0, 0, 1], operation="new", name=f"H_{nm}", body_name=f"Sondenhalter_{nm}")
        b.add("solid.cylinder", diameter=15, height=42, base=[-1000, y, 1219], axis=[0, 0, 1], operation="cut", targets=[f"Sondenhalter_{nm}"], name=f"HB_{nm}")
        b.add("material.assign", bodies=[f"Sondenhalter_{nm}"], material="Kanal PVC")
        b.add("solid.cylinder", diameter=14, height=245, base=[-1000, y, 1000], axis=[0, 0, 1], operation="new", name=f"S_{nm}", body_name=f"Sonde_{nm}")
        b.add("material.assign", bodies=[f"Sonde_{nm}"], material="Sonde")
    box(b, "Kabelkanal", mx - 35, 0, 300, 30, 60, 1000, "Kanal PVC")
    # --- Dosierkonsole
    b.add("component.activate", component=root)
    b.add("component.create", name="T81e_Dosierkonsole")
    kx = p["kon_x"]
    for sy in (-1, 1):
        tag = "p" if sy > 0 else "m"
        box(b, f"Kon_Fussplatte_{tag}", kx, sy * 440, 0, 150, 150, 8, STEEL)
        bar(b, f"Kon_Pfosten_{tag}", [kx, sy * 440, 8], [kx, sy * 440, 1300], d40)
    for k, z in enumerate((580, 1080), 1):
        bar(b, f"Kon_Traeger_{k}", [kx, -420, z], [kx, 420, z], d40)
        box(b, f"Kon_Boden_{k}", kx, 0, z + 20, 400, 840, 5, "Blech")
    for sy in (-1, 1):
        tag = "p" if sy > 0 else "m"
        box(b, f"Kanister_{tag}", kx, sy * 180, 605, 250, 300, 280, "Kanister HDPE")
        box(b, f"Dosierpumpe_{tag}", kx, sy * 180, 1105, 140, 120, 100, "Pumpe Schlauch")
    # --- Wartungsplattform mit Leiter (Rueckseite +Y)
    b.add("component.activate", component=root)
    b.add("component.create", name="T81f_Plattform")
    pz, gh = p["plat_z"], p["gel_h"]
    for sx in (-1, 1):
        tag = "p" if sx > 0 else "m"
        for y, nm in ((650, "v"), (1170, "h")):
            box(b, f"Plat_Fuss_{tag}{nm}", sx * lx, y, 0, 80, 80, 8, STEEL)
            bar(b, f"Plat_Bein_{tag}{nm}", [sx * lx, y, 8], [sx * lx, y, pz - 40], d40)
        bar(b, f"Plat_Arm_{tag}", [sx * lx, 630, pz - 20], [sx * lx, 1190, pz - 20], d40)
    bar(b, "Plat_Quer", [-(lx - 20), 1170, pz - 60], [lx - 20, 1170, pz - 60], d40)
    box(b, "Plat_Boden", 0, 910, pz, 1360, 580, 6, "Blech")
    g25 = dict(width=25, height=25, wall=2)
    ztop = pz + 6
    for x, y in ((-660, 640), (660, 640), (-660, 1185), (660, 1185), (-300, 1185), (300, 1185)):
        bar(b, f"Gel_Pfosten_{int(x)}_{y}", [x, y, ztop], [x, y, ztop + gh], g25)
    for k, zr in enumerate((ztop + gh - 12.5, ztop + gh / 2), 1):
        for sx in (-1, 1):
            bar(b, f"Gel_Seite_{k}_{'p' if sx > 0 else 'm'}", [sx * 660, 652.5, zr], [sx * 660, 1172.5, zr], g25)
            bar(b, f"Gel_Hinten_{k}_{'p' if sx > 0 else 'm'}", [sx * 300 + sx * 12.5, 1185, zr], [sx * 660 - sx * 12.5, 1185, zr], g25)
    d30 = dict(width=30, height=30, wall=2)
    for sx in (-1, 1):
        bar(b, f"Leiter_Holm_{'p' if sx > 0 else 'm'}", [sx * 250, 1215, 8], [sx * 250, 1215, 1900], d30)
    for k, z in enumerate((300, 580, 860, 1140, 1420), 1):
        b.add("solid.cylinder", diameter=20, height=470, base=[-235, 1215, z], axis=[1, 0, 0], operation="new", name=f"Sprosse_{k}_R", body_name=f"Leiter_Sprosse_{k}")
        b.add("material.assign", bodies=[f"Leiter_Sprosse_{k}"], material=STEEL)
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T81", d["beschreibung"]), ("T81a_IBC", "T81a", "2 x Puffer-IBC T80 uebereinander"), ("T81b_Stapelrahmen", "T81b", "Stahlrahmen 60 x 60 x 3 fuer die obere IBC"), ("T81c_Verbindung", "T81c", "Verbindungsrohr DN50 (Platzhalter)"), ("T81d_Messplatz", "T81d", "Messplatz: Staender, 4 Sonden, Becher, Kabelkanal"), ("T81e_Dosierkonsole", "T81e", "Dosierkonsole: 2 Pumpen, 2 Kanister 20 l"), ("T81f_Plattform", "T81f", "Wartungsplattform, Gelaender, Leiter")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": "Stahl verzinkt"})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "puffer_station.sc")
    sc.run(build().write("puffer_station"), out)
    for mat, pat in ((STEEL, r"(Rahmen_.*|Pfosten_(mm|mp|pm|pp)|Stab_.*)( \(2\))?"), ("HDPE Palette", r"(Kufe_\d|Deckplatte)( \(2\))?"), ("PE Blase", r"(Blase|Deckel)( \(2\))?"),
                     ("PVC grau", r"(Zulauf|Ueberlauf|Belueftung|Sensorstutzen|Ablauf_Stutzen|Ablauf_Zapfen)( \(2\))?"), ("PVC blau", r"(Kugelhahn|Hahn_Hebel)( \(2\))?"), ("Wasser", r"Wasser( \(2\))?")):
        sc.assign_part_materials(out, mat, pat)        # eingefuegte Komponenten verlieren das Material (Standarddichte 1,29): nachtraeglich zuweisen
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], "Masse leer", round(sum(x["mass_g"] for x in ev["bodies"] if "Wasser" not in x["name"]) / 1000), "kg")
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "puffer_station")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "puffer_station-01-schraeg.png"), [0, 400, 1200], 0.6, 0.3, 9000, w=1100, h=800)
        sc.snapshot(out, os.path.join(rd, "puffer_station-02-seite.png"), [0, 0, 1200], 0.0, 0.0, 9500, w=1100, h=800)
