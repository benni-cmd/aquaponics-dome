"""Netztopf T10: Rotationskoerper (Konus, Kragen, Wand, Boden) mit Schlitzen. Aufruf: python scripts/workshop/netztopf.py [--render]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("netztopf")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("component.create", name="T10_Netztopf", grounded=True)
    ro, rb, rf = p["rim_d"]/2, p["base_d"]/2, p["flange_d"]/2
    H, ft, w, fl = p["cup_h"], p["flange_t"], p["wall"], p["floor_t"]
    zr = H - ft                                  # Unterkante Kragen
    # Innen-Konus parallel zur Aussenseite: Wandstaerke senkrecht ~ waagerecht (flacher Konus), Innenradius = aussen - w
    ri_top, ri_base = ro - w, rb - w
    pts = [[0, 0], [rb, 0], [ro, zr], [rf, zr], [rf, H], [ri_top, H], [ri_base, fl], [0, fl]]
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 0, 1]}, name="Profil")
    b.add("sketch.line", points=pts, closed=True)
    b.add("sketch.finish")
    b.add("solid.revolve", axis="y", angle="360 deg", name="Korpus", body_name="Netztopf")
    # Schlitze: Box radial durch die Wand, dann kreisfoermig mustern
    b.add("solid.box", length=20, width="slot_w", height="slot_h", center=[22, 0, p["slot_z0"] + p["slot_h"]/2],
          operation="cut", targets=["Netztopf"], name="Schlitz1")
    b.add("solid.pattern.circular", features=["Schlitz1"], axis="Z", count=int(p["slot_count"]))
    # Bodenloch
    b.add("solid.cylinder", diameter=10, height=fl*3, base=[0, 0, -fl], operation="cut", targets=["Netztopf"], name="Bodenloch")
    b.add("material.create", name="PP", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    b.add("material.assign", bodies=["Netztopf"], material="PP")
    b.add("component.metadata.set", component="T10_Netztopf", part_number="T10", description=d["beschreibung"], revision="A",
          values={}, properties={"Werkstoff": d["werkstoff"]["name"], "Wandstaerke": f'{w} mm', "Anzahl": str(d["anzahl"]["soll"])})
    return b

if __name__ == "__main__":
    b = build()
    script = b.write("netztopf")
    out = os.path.join(sc.ROOT, "designs", "components", "netztopf.sc")
    sc.run(script, out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], round(x["volume_mm3"], 1), "mm3", round(x["mass_g"], 2), "g", x["bbox"]["min"], x["bbox"]["max"])
    if "--render" in sys.argv:
        sc.snapshot(out, os.path.join(sc.ROOT, "renders", "components", "netztopf", "netztopf-01.png"), [0, 0, 30], 0.6, 0.5, 260, w=700, h=600)
