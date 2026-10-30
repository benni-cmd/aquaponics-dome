"""Puffer-IBC T80 (W28, D46): Standard-IBC 1000 l mit Palette, Stahlgitterkaefig, PE-Blase, Deckel/Einfuelloeffnung DN150, Ablaufhahn DN50 und DN50-Seitenstutzen.
KS: Ursprung Mitte der Standflaeche am Boden, X Laenge 1200, Y Breite 1000 (vorn = -Y: Ablauf, Zulauf; hinten = +Y: Ueberlauf), Z hoch.
Aufruf: python scripts/workshop/puffer_ibc.py [--render]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def geom(p):
    """Abgeleitete Masse (gemeinsam mit check_puffer.py): Innenkontur der Blase, Wasserstand fuer das Nutzvolumen."""
    wi, li = p["blase_w"] - 2 * p["blase_wall"], p["blase_l"] - 2 * p["blase_wall"]
    ri = p["blase_r"] - p["blase_wall"]
    area = li * wi - (4 - math.pi) * ri * ri
    z0 = p["pal_h"] + p["blase_wall"]
    depth = p["nutz_l"] * 1e6 / area
    return dict(li=li, wi=wi, ri=ri, area=area, z_boden=z0, z_wasser=z0 + depth, z_top_in=p["pal_h"] + p["blase_h"] - p["blase_wall"], z_blase_top=p["pal_h"] + p["blase_h"])

def rr(b, z, w, l, r, name):
    b.add("sketch.create", plane={"origin": [0, 0, z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name=name)
    b.add("sketch.rectangle.rounded", p0=[-l / 2, -w / 2], p1=[l / 2, w / 2], radius=r)

def tube_member(b, name, dims, origin, xdir, ydir, dist, material="Stahl verzinkt"):
    b.add("sketch.create", plane={"origin": origin, "x_dir": xdir, "y_dir": ydir}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind="rect_tube", **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    b.add("solid.extrude", distance=dist, name="F_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=material)

def pipe(b, name, od, idia, base, axis, length, material):
    b.add("solid.cylinder", diameter=od, height=length, base=base, axis=axis, operation="new", name="R_" + name, body_name=name)
    if idia:
        b.add("solid.cylinder", diameter=idia, height=length + 2, base=[base[i] - axis[i] for i in range(3)], axis=axis, operation="cut", targets=[name], name="B_" + name)
    b.add("material.assign", bodies=[name], material=material)

def build():
    p, d = sc.load_params("puffer_ibc")
    G = geom(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    L, W = p["ibc_l"], p["ibc_w"]
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=7.85, color="#aeb4b8", pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    b.add("material.create", name="HDPE Palette", density_g_cm3=0.95, color="#6f767a")
    b.add("material.create", name="PE Blase", density_g_cm3=0.95, color="#e9edf0")
    b.add("material.create", name="PVC grau", density_g_cm3=1.4, color="#8d9296")
    b.add("material.create", name="PVC blau", density_g_cm3=1.4, color="#2a5da8")
    b.add("material.create", name="Wasser", density_g_cm3=1.0, color="#6fb6e8")
    root = "T80_Puffer_IBC"
    b.add("component.create", name=root, grounded=True)
    # --- Palette: 3 Kufen laengs + Deckplatte
    b.add("component.create", name="T80a_Palette")
    rh = p["pal_h"] - p["deck_t"]
    for k, y in enumerate((-420, 0, 420), 1):
        b.add("solid.box", length=L, width=p["runner_w"], height=rh, center=[0, y, rh / 2], operation="new", name=f"K_{k}", body_name=f"Kufe_{k}")
    b.add("solid.box", length=L, width=W, height=p["deck_t"], center=[0, 0, rh + p["deck_t"] / 2], operation="new", name="Deck_R", body_name="Deckplatte")
    b.add("material.assign", bodies=["Kufe_1", "Kufe_2", "Kufe_3", "Deckplatte"], material="HDPE Palette")
    # --- Kaefig: Rahmen unten/oben, 4 Eckpfosten, Gitterstaebe
    b.add("component.activate", component=root)
    b.add("component.create", name="T80b_Kaefig")
    r, rw = p["rail"], p["rail_wall"]
    dims = dict(width=r, height=r, wall=rw)
    zb, zt = p["pal_h"], p["ibc_h"] - r                                   # Unterkante Bodenrahmen, Unterkante Kopfrahmen
    xc, yc = L / 2 - r / 2, W / 2 - r / 2
    for tag, z0 in (("u", zb), ("o", zt)):
        for sg in (-1, 1):
            tube_member(b, f"Rahmen_{tag}_x{sg:+d}".replace("+", "p").replace("-", "m"), dims, [-L / 2, sg * yc, z0 + r / 2], [0, 1, 0], [0, 0, 1], L)
            tube_member(b, f"Rahmen_{tag}_y{sg:+d}".replace("+", "p").replace("-", "m"), dims, [sg * xc, -(W / 2 - r), z0 + r / 2], [0, 0, 1], [1, 0, 0], W - 2 * r)
    for sx in (-1, 1):
        for sy in (-1, 1):
            nm = f"Pfosten_{'p' if sx > 0 else 'm'}{'p' if sy > 0 else 'm'}"
            tube_member(b, nm, dims, [sx * xc, sy * yc, zb + r], [1, 0, 0], [0, 1, 0], zt - zb - r)
    rod, hz0 = p["rod_d"], p["rod_z0"]
    nv = int((L - 2 * r) // p["rod_pitch_v"])                              # senkrechte Staebe Langseite: x -400 .. 400
    nvs = int((W - 2 * r) // p["rod_pitch_v"])                            # Stirnseite: y -300 .. 300 (4 Staebe)
    nhz = int((zt - hz0) // p["rod_pitch_h"])                             # waagerechte Staebe (8)
    for tag, sg in (("v", -1), ("h", 1)):
        b.add("solid.cylinder", diameter=rod, height=zt - zb - r, base=[-(nv - 1) / 2 * p["rod_pitch_v"], sg * (W / 2 - 12.5), zb + r], axis=[0, 0, 1], operation="new", name=f"StabV_{tag}", body_name=f"Stab_V_{tag}")
        b.add("solid.pattern.rectangular", bodies=[f"Stab_V_{tag}"], dir1=[1, 0, 0], count1=nv, spacing1=p["rod_pitch_v"])
        b.add("solid.cylinder", diameter=rod, height=L - 2 * r, base=[-(L / 2 - r), sg * (W / 2 - 4), hz0], axis=[1, 0, 0], operation="new", name=f"StabH_{tag}", body_name=f"Stab_H_{tag}")
        b.add("solid.pattern.rectangular", bodies=[f"Stab_H_{tag}"], dir1=[0, 0, 1], count1=nhz, spacing1=p["rod_pitch_h"])
    for tag, sg in (("a", -1), ("b", 1)):
        b.add("solid.cylinder", diameter=rod, height=zt - zb - r, base=[sg * (L / 2 - 12.5), -(nvs - 1) / 2 * p["rod_pitch_v"], zb + r], axis=[0, 0, 1], operation="new", name=f"StabS_{tag}", body_name=f"Stab_S_{tag}")
        b.add("solid.pattern.rectangular", bodies=[f"Stab_S_{tag}"], dir1=[0, 1, 0], count1=nvs, spacing1=p["rod_pitch_v"])
        b.add("solid.cylinder", diameter=rod, height=W - 2 * r, base=[sg * (L / 2 - 4), -(W / 2 - r), hz0], axis=[0, 1, 0], operation="new", name=f"StabT_{tag}", body_name=f"Stab_T_{tag}")
        b.add("solid.pattern.rectangular", bodies=[f"Stab_T_{tag}"], dir1=[0, 0, 1], count1=nhz, spacing1=p["rod_pitch_h"])
    # --- Blase (hohl, Wand 2,5), Deckel und Hals
    b.add("component.activate", component=root)
    b.add("component.create", name="T80c_Blase")
    rr(b, p["pal_h"], p["blase_w"], p["blase_l"], p["blase_r"], "Blase_Aussen"); b.add("sketch.finish")
    b.add("solid.extrude", distance=p["blase_h"], name="Blase_Koerper", body_name="Blase")
    rr(b, G["z_boden"], G["wi"], G["li"], G["ri"], "Blase_Innen"); b.add("sketch.finish")
    b.add("solid.extrude", distance=G["z_top_in"] - G["z_boden"], operation="cut", targets=["Blase"], name="Blase_Hohlraum")
    zbt = G["z_blase_top"]
    b.add("solid.cylinder", diameter=p["neck_od"], height=p["neck_h"], base=[p["neck_x"], 0, zbt - 0.0], axis=[0, 0, 1], operation="join", targets=["Blase"], name="Hals_R")
    b.add("solid.cylinder", diameter=p["neck_id"], height=p["neck_h"] + 2 * p["blase_wall"] + 2, base=[p["neck_x"], 0, G["z_top_in"] - 1], axis=[0, 0, 1], operation="cut", targets=["Blase"], name="Hals_Bohrung")
    b.add("material.assign", bodies=["Blase"], material="PE Blase")
    b.add("solid.cylinder", diameter=p["lid_d"], height=p["lid_t"], base=[p["neck_x"], 0, zbt + p["neck_h"]], axis=[0, 0, 1], operation="new", name="Deckel_R", body_name="Deckel")
    b.add("material.assign", bodies=["Deckel"], material="PE Blase")
    # --- Anschluesse: Seitenstutzen vorn/hinten, Dachstutzen, Ablauf mit Kugelhahn
    b.add("component.activate", component=root)
    b.add("component.create", name="T80d_Anschluesse")
    od, idia, px, sl = p["stub_od"], p["stub_id"], p["port_x"], p["stub_len_side"]
    yw = p["blase_w"] / 2                                                   # Blasen-Aussenwand (y), Stutzenfuss liegt aussen auf der Wand
    zbt_ = zbt
    for nm, z, sg in (("Zulauf", p["zulauf_z"], -1), ("Ueberlauf", p["ueberlauf_z"], 1)):
        pipe(b, nm, od, idia, [px, sg * yw, z], [0, sg, 0], sl, "PVC grau")
        b.add("solid.cylinder", diameter=idia, height=p["blase_wall"] + 2, base=[px, sg * (yw + 1), z], axis=[0, -sg, 0], operation="cut", targets=["Blase"], name=f"Loch_{nm}")
    for nm, x, y, dd, ii in (("Belueftung", -420, -300, p["vent_d"], p["vent_d"] - 5), ("Sensorstutzen", -420, 300, od, idia)):
        pipe(b, nm, dd, ii, [x, y, zbt_], [0, 0, 1], p["stub_up"], "PVC grau")
        b.add("solid.cylinder", diameter=ii, height=p["blase_wall"] + 2, base=[x, y, zbt_ + 1], axis=[0, 0, -1], operation="cut", targets=["Blase"], name=f"Loch_{nm}")
    az, y0 = p["ablauf_z"], -yw
    yh = -(W / 2 + 5)                                                       # Hahn beginnt 5 mm ausserhalb des Kaefigs
    pipe(b, "Ablauf_Stutzen", od, idia, [px, y0, az], [0, -1, 0], abs(yh) - abs(y0), "PVC grau")
    b.add("solid.cylinder", diameter=idia, height=p["blase_wall"] + 2, base=[px, y0 - 1, az], axis=[0, 1, 0], operation="cut", targets=["Blase"], name="Loch_Ablauf")
    b.add("solid.cylinder", diameter=p["hahn_d"], height=p["hahn_l"], base=[px, yh, az], axis=[0, -1, 0], operation="new", name="Hahn_R", body_name="Kugelhahn")
    b.add("solid.box", length=130, width=18, height=8, center=[px + 55, yh - p["hahn_l"] / 2, az + p["hahn_d"] / 2 + 4], operation="new", name="Hebel_R", body_name="Hahn_Hebel")
    pipe(b, "Ablauf_Zapfen", od, idia, [px, yh - p["hahn_l"], az], [0, -1, 0], 40, "PVC grau")
    b.add("material.assign", bodies=["Kugelhahn", "Hahn_Hebel"], material="PVC blau")
    # --- Wasser (Nutzvolumen)
    b.add("component.activate", component=root)
    b.add("component.create", name="T80e_Wasser")
    rr(b, G["z_boden"], G["wi"], G["li"], G["ri"], "Wasser_Kontur"); b.add("sketch.finish")
    b.add("solid.extrude", distance=G["z_wasser"] - G["z_boden"], name="Wasser_Koerper", body_name="Wasser")
    b.add("material.assign", bodies=["Wasser"], material="Wasser")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T80", d["beschreibung"]), ("T80a_Palette", "T80a", "Palette 1200 x 1000 x 150: Deckplatte und 3 Kufen"), ("T80b_Kaefig", "T80b", "Stahlgitterkaefig: Rahmen 25 x 25 x 1,5, 4 Pfosten, Staebe D8"), ("T80c_Blase", "T80c", "PE-Blase mit Hals DN150 und Deckel"), ("T80d_Anschluesse", "T80d", "Stutzen DN50 und Ablaufhahn"), ("T80e_Wasser", "T80e", "Nutzwasser 900 l (Wasserkoerper)")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": "Stahl/PE/HDPE"})
    return b, G

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "puffer_ibc.sc")
    b, G = build()
    sc.run(b.write("puffer_ibc"), out)
    sc.assign_part_materials(out, "Stahl verzinkt", r"Stab_.*")
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx], "Wasser z", round(G["z_wasser"], 1))
    for x in ev["bodies"]:
        if not x["name"].startswith("Stab_"):
            print(x["name"], round(x["mass_g"] / 1000, 2), "kg", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "puffer_ibc")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "puffer_ibc-01-schraeg.png"), [0, 0, 600], 0.9, 0.35, 4200, w=1000, h=800)
        sc.snapshot(out, os.path.join(rd, "puffer_ibc-02-seite.png"), [0, 0, 600], 0.0, 0.0, 4200, w=1000, h=800)
