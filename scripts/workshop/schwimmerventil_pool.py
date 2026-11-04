"""Schwimmerventil Pool T84 (W37-2, K40): Handelsteil 3/4 Zoll mit Klebemuffen-Uebergang d25, Ventilgehaeuse, Wangenhalter, Hebelarm mit Schwimmerkugel (ein Koerper).
KS: Port A (Mitte Muffenoeffnung) im Ursprung, Rohrachse +X (Zulauf aus -X), Z hoch; der Spiegel liegt ventil_h = 195 unter der Rohrachse (Einbau: Achse Z 710, Spiegel Z 515 aus layout.json).
Zulauf OFFEN (E20). Aufruf: python -X utf8 scripts/workshop/schwimmerventil_pool.py [--render]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

def geom(p):
    """Hebelarm und Kugellage: Drehpunkt (hebel_x, 0, z_arm0), Kugelmitte (hebel_x + arm_dx, 0, -ventil_h + kugel_auf)."""
    z0 = -(p["ventil_d"] / 2 + 11)                                 # Armanfang 11 mm unter dem Gehaeuse (Wangen 21 mm hoch)
    xk, zk = p["hebel_x"] + p["arm_dx"], -p["ventil_h"] + p["kugel_auf"]
    dx, dz = xk - p["hebel_x"], zk - z0
    ln = math.hypot(dx, dz)
    u = (dx / ln, 0.0, dz / ln)
    r = p["kugel_d"] / 2
    return dict(z0=z0, xk=xk, zk=zk, u=u, ln=ln, arm_l=ln - r + 5)    # Arm endet 5 mm in der Kugel

def build(p=None):
    p0, d = sc.load_params("schwimmerventil_pool")
    p = dict(p0, **(p or {}))
    g = geom(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in (("SV PVC", 1.4, "#8d9296"), ("SV PP", 0.91, "#e8e5d8"), ("SV Kugel", 0.35, "#e07a2f")):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = "T84_Schwimmerventil_Pool"
    b.add("component.create", name=root, grounded=True)
    dp = p["pipe_d"]; of = L.od_f(dp); t = L.DEPTH[dp]
    # Uebergang: Klebemuffe d25 (Tiefe 19), Durchgang d16 bis zum Ventil
    b.add("solid.cylinder", diameter=of, height=p["uebergang_l"], base=[0, 0, 0], axis=[1, 0, 0], operation="new", name="R_Uebergang", body_name="Uebergang")
    b.add("solid.cylinder", diameter=dp, height=t + 1, base=[-1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Uebergang"], name="Muffe_A")
    b.add("solid.cylinder", diameter=16, height=p["uebergang_l"] + 2, base=[-1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Uebergang"], name="Durchgang")
    b.add("material.assign", bodies=["Uebergang"], material="SV PVC")
    # Ventilgehaeuse (Platzhalter, innen nicht modelliert)
    b.add("solid.cylinder", diameter=p["ventil_d"], height=p["ventil_l"], base=[p["uebergang_l"], 0, 0], axis=[1, 0, 0], operation="new", name="R_Ventil", body_name="Ventilgehaeuse")
    b.add("material.assign", bodies=["Ventilgehaeuse"], material="SV PP")
    # Wangenhalter: zwei Wangen links/rechts des Arms
    w, rr = p["wange_t"], p["arm_d"] / 2
    zt = -p["ventil_d"] / 2
    for sy, nm in ((1, "L"), (-1, "R")):
        b.add("solid.box", length=16, width=w, height=21, center=[p["hebel_x"], sy * (rr + w / 2), zt - 10.5], operation="new", name="R_Wange_" + nm, body_name="Wange_" + nm)
        b.add("material.assign", bodies=["Wange_" + nm], material="SV PP")
    # Hebelarm mit Kugel (ein Koerper)
    u = g["u"]
    b.add("solid.cylinder", diameter=p["arm_d"], height=round(g["arm_l"], 3), base=[p["hebel_x"], 0, round(g["z0"], 3)], axis=[round(c, 6) for c in u], operation="new", name="R_Arm", body_name="Hebelarm_mit_Kugel")
    b.add("solid.sphere", diameter=p["kugel_d"], center=[round(g["xk"], 3), 0, round(g["zk"], 3)], operation="join", targets=["Hebelarm_mit_Kugel"], name="R_Kugel")
    b.add("material.assign", bodies=["Hebelarm_mit_Kugel"], material="SV Kugel")
    b.add("component.metadata.set", component=root, part_number="T84", description=d["beschreibung"], revision="A", properties={"Werkstoff": "Kunststoff PP / PVC-U"})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "schwimmerventil_pool.sc")
    sc.run(build().write("schwimmerventil_pool"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx], [(x["name"], round(x["volume_mm3"] / 1000, 1), "cm3") for x in ev["bodies"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "schwimmerventil_pool")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "schwimmerventil_pool-01-schraeg.png"), [180, 0, -80], 0.7, 0.35, 700, w=1000, h=700)
        sc.snapshot(out, os.path.join(rd, "schwimmerventil_pool-02-seite.png"), [180, 0, -80], 0.0, 0.0, 700, w=1000, h=700)
