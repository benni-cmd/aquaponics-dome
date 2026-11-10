"""Nachspeise-Ventil T108 (U2, D107, D114): zwei Schwimmerventile aus schwimmerventil_pool (Regenwasser Eingang A y 0, Frischwasser Eingang B y 120); die Frischwasser-Kugel haengt 30 mm tiefer.
KS: Port A im Ursprung, Rohrachse +X, Z hoch; Spiegel liegt ventil_h = 510 unter der Rohrachse. Aufruf: python -X utf8 scripts/workshop/nachspeise_ventil.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import schwimmerventil_pool as T84
import leitung as L

NAME = "nachspeise_ventil"
MAT = {"SV PVC": (1.4, "#8d9296"), "SV PP": (0.91, "#e8e5d8"), "SV Kugel": (0.35, "#e07a2f")}


def ventil(b, p, y, suf, kugel_auf):
    """ein Ventil bei Achse y: Uebergang, Gehaeuse, zwei Wangen, Hebelarm mit Kugel (Namen mit Suffix _regen/_frisch)."""
    q = dict(p, kugel_auf=kugel_auf)
    g = T84.geom(q)
    dp = p["pipe_d"]
    of, t = L.od_f(dp), L.DEPTH[dp]
    U.cyl(b, "Uebergang_" + suf, of, p["uebergang_l"], (0, y, 0), (1, 0, 0), "SV PVC")
    U.cyl(b, "Muffe_" + suf, dp, t + 1, (-1, y, 0), (1, 0, 0), None, schneiden=["Uebergang_" + suf])
    U.cyl(b, "Durchgang_" + suf, 16, p["uebergang_l"] + 2, (-1, y, 0), (1, 0, 0), None, schneiden=["Uebergang_" + suf])
    U.cyl(b, "Ventilgehaeuse_" + suf, p["ventil_d"], p["ventil_l"], (p["uebergang_l"], y, 0), (1, 0, 0), "SV PP")
    w, rr, zt = p["wange_t"], p["arm_d"] / 2, -p["ventil_d"] / 2
    for sy, nm in ((1, "L"), (-1, "R")):
        U.box(b, f"Wange_{nm}_{suf}", (16, w, 21), (p["hebel_x"], y + sy * (rr + w / 2), zt - 10.5), "SV PP")
    u = g["u"]
    U.cyl(b, "Hebelarm_mit_Kugel_" + suf, p["arm_d"], round(g["arm_l"], 3), (p["hebel_x"], y, round(g["z0"], 3)), [round(c, 6) for c in u], "SV Kugel")
    b.add("solid.sphere", diameter=p["kugel_d"], center=[round(g["xk"], 3), y, round(g["zk"], 3)], operation="join", targets=["Hebelarm_mit_Kugel_" + suf], name="R_Kugel_" + suf)
    return g


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T108_Nachspeise_Ventil"
    b.add("component.create", name=root, grounded=True)
    ventil(b, p, 0, "regen", p["kugel_auf"])
    ventil(b, p, p["abstand_y"], "frisch", p["kugel_auf"] - p["staffel"])
    U.fertig(b, root, "T108", d, "PP / PVC-U")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [180, 60, -220], 0.7, 0.35, 1100, None), ("02-seite", [180, 60, -220], 0.0, 0.0, 1100, None)])
