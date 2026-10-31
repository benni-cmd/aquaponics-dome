"""Drittbecken klein T14k (W34, R37 Befund 10, D66): Wanne Ø 920 (Ring 60) mit Hohlraum Ø 800 ab 120 mm Bodenstaerke, Wasserkoerper Ø 790 x 800, Rand 135 mm ueber dem Wasserspiegel; 0,4 m3.
KS: Ursprung Mitte der Beckenunterkante (Z 0); Einbau: Wasserspiegel Z 515 im Modellrahmen = Z 920 im Bauteil. Der Bestand becken_dritt.sc (gen_dome.py, Montage) bleibt unberuehrt.
Aufruf: python scripts/workshop/becken_dritt_klein.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("becken_dritt_klein")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("material.create", name="Beton", density_g_cm3=2.4, color="#9a9a96")
    b.add("material.create", name="Wasser", density_g_cm3=1.0, color="#6fb6e8")
    root = "T14k_Drittbecken_klein"
    b.add("component.create", name=root, grounded=True)
    d_out = p["wasser_d"] + 2 * p["ring"]
    z_wasser = p["boden"] + p["wasser_tiefe"]                       # Wasserspiegel ueber der Unterkante (920)
    total = z_wasser + p["rand_ueber_wasser"]                       # Rand (1055)
    b.add("solid.cylinder", diameter=d_out, height=total, base=[0, 0, 0], axis=[0, 0, 1], operation="new", name="T14k_Wanne", body_name="T14k_Wanne")
    b.add("solid.cylinder", diameter=p["wasser_d"], height=total - p["boden"] + 1, base=[0, 0, p["boden"]], axis=[0, 0, 1], operation="cut", targets=["T14k_Wanne"], name="T14k_Hohlraum")
    b.add("material.assign", bodies=["T14k_Wanne"], material="Beton")
    b.add("solid.cylinder", diameter=p["wasser_d"] - p["wasser_spiel"], height=p["wasser_tiefe"], base=[0, 0, p["boden"]], axis=[0, 0, 1], operation="new", name="T14k_Wasser", body_name="Wasser")
    b.add("material.assign", bodies=["Wasser"], material="Wasser")
    b.add("component.metadata.set", component=root, part_number="T14k", description=d["beschreibung"], revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "becken_dritt_klein.sc")
    sc.run(build().write("becken_dritt_klein"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], [(x["name"], round(x["volume_mm3"] / 1e6, 1), "l") for x in ev["bodies"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "becken_dritt_klein")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "becken_dritt_klein-01-schraeg.png"), [0, 0, 500], 0.7, 0.4, 2600, w=1000, h=700)
        sc.snapshot(out, os.path.join(rd, "becken_dritt_klein-02-schnitt.png"), [0, 0, 500], 0.0, 0.0, 2400, w=1000, h=700, section="y=0")
