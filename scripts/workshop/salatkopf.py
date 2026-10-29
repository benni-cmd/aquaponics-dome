"""Salatkopf T12: wenige ueberlappende Kugeln (Kern + 2 Blattringe), unten bei Z=0 abgeflacht, Wurzelhals nach -Z. Konfigurationen S/M/L."""
import sys, os, math
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("salatkopf")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("component.create", name="T12_Salatkopf", grounded=True)
    D = "head_d"
    b.add("solid.sphere", radius=f"{D}*core_r_f", center=[0, 0, f"{D}*0.30"], operation="new", name="Kern", body_name="Salatkopf")
    b.add("solid.sphere", radius=f"{D}*ring1_r_f", center=[f"{D}*ring1_d_f", 0, f"{D}*0.25"], operation="join", targets=["Salatkopf"], name="Ring1")
    b.add("solid.pattern.circular", features=["Ring1"], axis="Z", count=6)
    c30, s30 = math.cos(math.radians(30)), math.sin(math.radians(30))
    b.add("solid.sphere", radius=f"{D}*ring2_r_f", center=[f"{D}*ring2_d_f*{c30:.6f}", f"{D}*ring2_d_f*{s30:.6f}", f"{D}*0.14"], operation="join", targets=["Salatkopf"], name="Ring2")
    b.add("solid.pattern.circular", features=["Ring2"], axis="Z", count=6)
    b.add("solid.box", length=f"{D}*2", width=f"{D}*2", height=f"{D}", center=[0, 0, f"-{D}/2"], operation="cut", targets=["Salatkopf"], name="Boden")
    b.add("solid.cylinder", diameter="neck_d", height="neck_len + 5", base=[0, 0, "-neck_len"], operation="join", targets=["Salatkopf"], name="Hals")
    b.add("material.create", name="Salat", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    b.add("material.assign", bodies=["Salatkopf"], material="Salat")
    b.add("config.configure", params=["head_d"])
    b.add("config.row", name="M")
    b.add("config.row", name="S", **{"from": "M"}, values={"param:head_d": "70 mm"})
    b.add("config.row", name="L", **{"from": "M"}, values={"param:head_d": "130 mm"})
    b.add("config.activate", row="M")
    b.add("component.metadata.set", component="T12_Salatkopf", part_number="T12", description=d["beschreibung"], revision="A",
          properties={"Werkstoff": d["werkstoff"]["name"], "Bezugspunkt": "Z=0 Kragenoberkante Netztopf"})
    return b

if __name__ == "__main__":
    b = build()
    script = b.write("salatkopf")
    out = os.path.join(sc.ROOT, "designs", "components", "salatkopf.sc")
    sc.run(script, out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], round(x["volume_mm3"], 1), "mm3", x["faces"], "Flaechen", x["bbox"]["min"], x["bbox"]["max"])
    if "--render" in sys.argv:
        sc.snapshot(out, os.path.join(sc.ROOT, "renders", "components", "salatkopf", "salatkopf-01.png"), [0, 0, 35], 0.6, 0.5, 330, w=700, h=600)
