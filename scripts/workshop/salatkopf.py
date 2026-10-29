"""Salatkopf T12: Rosette aus geneigten Blattscheiben (je Gruppe ein Koerper, Muster um Z; Vereinigung ueberlappender flacher Scheiben scheitert im Kernel) um eine Kernkugel, bei Z=0 abgeschnitten, Wurzelhals nach -Z. Konfigurationen S/M/L."""
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
    b.add("solid.sphere", radius=f"{D}*core_r_f", center=[0, 0, f"{D}*core_h_f"], operation="new", name="Kern", body_name="Salatkopf")
    jt = d["blatt_gruppen"]["jitter"]
    rnd = lambda i: (math.sin(i * 12.9898) * 43758.5453) % 1.0 - 0.5        # deterministisch in [-0.5, 0.5)
    leaf_names = []
    cnt = 0
    for g in d["blatt_gruppen"]["gruppen"]:
        for k in range(g["n"]):
            cnt += 1
            ph = math.radians(g["phase"] + k * 360.0 / g["n"] + jt["az"] * rnd(cnt * 5 + 1))
            al = math.radians(g["alpha"] + jt["alpha"] * rnd(cnt * 5 + 2))
            rho = g["rho"] * (1 + jt["rho"] * 2 * rnd(cnt * 5 + 3))
            rad = g["rad"] * (1 + jt["rad"] * rnd(cnt * 5 + 4))
            hh = g["h"] + jt["h"] * rnd(cnt * 5 + 5)
            n = (-math.sin(al) * math.cos(ph), -math.sin(al) * math.sin(ph), math.cos(al))      # Blattnormale
            cx, cy = rho * math.cos(ph), rho * math.sin(ph)
            base = [f"{D}*({cx:.5f}) - {n[0]:.5f}*{D}*leaf_t_f/2", f"{D}*({cy:.5f}) - {n[1]:.5f}*{D}*leaf_t_f/2", f"{D}*{hh:.5f} - {n[2]:.5f}*{D}*leaf_t_f/2"]
            nm = f"Blatt{g['name']}_{k + 1}"
            b.add("solid.cylinder", radius=f"{D}*{rad:.5f}", height=f"{D}*leaf_t_f", base=base, axis=[round(v, 5) for v in n], operation="new", name=nm, body_name=nm)
            leaf_names.append(nm)
    b.add("solid.box", length=f"{D}*3", width=f"{D}*3", height=f"{D}", center=[0, 0, f"-{D}/2"], operation="cut", targets=["Salatkopf"], name="Boden")
    b.add("solid.cylinder", diameter="neck_d", height="neck_len + 5", base=[0, 0, "-neck_len"], operation="join", targets=["Salatkopf"], name="Hals")
    b.add("material.create", name="Salat", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    leaves = ["Salatkopf"] + leaf_names
    b.add("material.assign", bodies=leaves, material="Salat")
    b.add("appearance.assign", bodies=leaves, color=d["werkstoff"]["farbe"])
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
        print(x["name"], round(x["volume_mm3"], 1), "mm3", x["faces"], "Flaechen", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        r = os.path.join(sc.ROOT, "renders", "components", "salatkopf")
        for i, (yaw, pitch) in enumerate(((0.6, 0.4), (2.2, 0.15), (0.0, 1.45)), 1):
            sc.snapshot(out, os.path.join(r, f"salatkopf-0{i+1}.png"), [0, 0, 32], yaw, pitch, 230, w=800, h=650)
