"""Winkelhalter T23 (W11): Stahlwinkel am Beinkopf der NFT-Tische. Ursprung = Ecke aus Beininnenflaeche (Y=0) und Holmunterkante (Z=0), X Winkelbreite (Mitte), Y vom Bein weg unter den Holm.
Senkrechter Flansch nach -Z am Bein (2 x M6x55 mit Mutter durch das Bein, Kopf auf der Winkelseite), waagerechter Flansch unter dem Holm (2 x M6x16 von unten).
Aufruf: python scripts/workshop/winkelhalter.py [--render]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("winkelhalter")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    w, t, lv, lh = p["wh_w"], p["wh_t"], p["wh_lv"], p["wh_lh"]
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"], pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    root = "T23_Winkelhalter"
    b.add("component.create", name=root, grounded=True)
    b.add("component.create", name="T23a_Winkel")
    b.add("solid.box", length=w, width=lh, height=t, center=[0, lh / 2, -t / 2], operation="new", name="Waagerecht_R", body_name="Winkel")
    b.add("solid.box", length=w, width=t, height=lv, center=[0, t / 2, -lv / 2], operation="join", targets=["Winkel"], name="Senkrecht_R")
    ys = [p["wh_edge"] + t, p["wh_edge"] + t + p["wh_pitch"]]                       # Loecher im waagerechten Flansch (hinter dem senkrechten Flansch)
    zs = [-p["wh_edge_v"], -p["wh_edge_v"] - p["wh_pitch_v"]]
    for k, y in enumerate(ys, 1):
        b.add("solid.cylinder", diameter=p["wh_hole"], height=t + 2, base=[0, y, -t - 1], operation="cut", targets=["Winkel"], name=f"LochH_{k}")
    for k, z in enumerate(zs, 1):
        b.add("solid.cylinder", diameter=p["wh_hole"], height=t + 2, base=[0, -1, z], axis=[0, 1, 0], operation="cut", targets=["Winkel"], name=f"LochV_{k}")
    b.add("material.assign", bodies=["Winkel"], material="Stahl verzinkt")
    b.add("component.activate", component=root)
    b.add("component.create", name="T23b_Normteile")
    lw = p["leg_w"]
    for k, y in enumerate(ys, 1):                                                   # Kopf unter dem Flansch, Schaft nach oben in den Holm
        b.add("parts.insert", family="hex_bolt", size="M6", length=p["wh_bolt_h"], point=[0, y, -t], direction=[0, 0, -1], name=f"SchraubeH_{k}")
    for k, z in enumerate(zs, 1):                                                   # Kopf auf der Winkelseite (+Y), Schaft durch das Bein, Mutter auf der Aussenseite
        b.add("parts.insert", family="hex_bolt", size="M6", length=p["wh_bolt_v"], point=[0, t, z], direction=[0, 1, 0], name=f"SchraubeV_{k}")
        b.add("parts.insert", family="hex_nut", size="M6", point=[0, -lw, z], direction=[0, -1, 0], name=f"MutterV_{k}")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T23", d["beschreibung"]), ("T23a_Winkel", "T23a", "Stahlwinkel 36 x 60 x 60 x 4 mit 2 + 2 Loechern D6,6"), ("T23b_Normteile", "T23b", "2 x M6x55 + Mutter (Bein), 2 x M6x16 (Holm)")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

if __name__ == "__main__":
    b = build()
    out = os.path.join(sc.ROOT, "designs", "components", "winkelhalter.sc")
    sc.run(b.write("winkelhalter"), out)
    sc.assign_part_materials(out, "Stahl verzinkt")
    import normteile_benennen   # W60 5a: Normteile Body<n> -> Schraube_M6x16_k usw. (Gestalt), Teiledaten data/parts/winkelhalter.json
    normteile_benennen.benennen(out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], x["faces"], round(x["mass_g"], 1), "g", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        r = os.path.join(sc.ROOT, "renders", "components", "winkelhalter")
        os.makedirs(r, exist_ok=True)
        for n, (yaw, pitch) in {"01-iso": (0.7, 0.4), "02-unten": (0.7, -0.5), "03-seite": (1.5708, 0.0)}.items():
            sc.snapshot(out, os.path.join(r, f"winkelhalter-{n}.png"), [0, 5, -25], yaw, pitch, 260, w=900, h=700)
