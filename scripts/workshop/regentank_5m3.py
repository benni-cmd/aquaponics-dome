"""Regentank 5 m3 T107 (Platzhalter, U2, D107, A8): stehender PE-Tank Ø 1700 x 2300 (innen Ø 1670 x 2270 = 4,97 m3), Domschacht, Domdeckel, Auslaufstutzen d25 (zum Nachspeise-Ventil), Ueberlaufstutzen d63.
KS: Mitte der Standflaeche, Z 0 = Fussboden; Stutzen bei +X. Maße sind Annahme (Quelle legt Hoehe und Lage nicht fest). Aufruf: python -X utf8 scripts/workshop/regentank_5m3.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import leitung as L

NAME = "regentank_5m3"
MAT = {"PE Tank": (0.95, "#d9d4c0"), "PVC grau": (1.4, "#8d9296")}


def stutzen(b, name, dn, z, r_i, l):
    """Stutzen d<dn> durch die Wand (Bohrung +0,4 mm), Muffe aussen, Durchgang innen."""
    of, t = L.od_f(dn), L.DEPTH[dn]
    U.cyl(b, name + "_Bohrung", of + 0.4, l, (r_i - 1, 0, z), (1, 0, 0), None, schneiden=["Tank"])
    U.cyl(b, name, of, l + 15, (r_i, 0, z), (1, 0, 0), "PVC grau")
    U.cyl(b, name + "_Muffe", dn, t + 1, (r_i + l + 15 - t, 0, z), (1, 0, 0), None, schneiden=[name])
    U.cyl(b, name + "_Durchgang", dn - 8, l + 17, (r_i - 1, 0, z), (1, 0, 0), None, schneiden=[name])


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T107_Regentank_5m3"
    b.add("component.create", name=root, grounded=True)
    D, w, h = p["aussen_d"], p["wand"], p["h"]
    U.cyl(b, "Tank", D, h, (0, 0, 0), (0, 0, 1), "PE Tank")
    U.cyl(b, "Tank_Innen", D - 2 * w, h - 2 * w, (0, 0, w), (0, 0, 1), None, schneiden=["Tank"])
    U.cyl(b, "Tank_Domloch", 440, w + 2, (0, 0, h - w - 1), (0, 0, 1), None, schneiden=["Tank"])
    U.cyl(b, "Dom", p["dom_d"], p["dom_h"], (0, 0, h), (0, 0, 1), "PE Tank")
    U.cyl(b, "Dom_Bohrung", 440, p["dom_h"] + 2, (0, 0, h - 1), (0, 0, 1), None, schneiden=["Dom"])
    U.cyl(b, "Domdeckel", p["domdeckel_d"], 30, (0, 0, h + p["dom_h"]), (0, 0, 1), "PE Tank")
    r_i = D / 2 - w
    stutzen(b, "Auslaufstutzen", 25, p["auslauf_z"], r_i, w + p["stutzen_l"] - 15)
    stutzen(b, "Ueberlaufstutzen", 63, p["ueberlauf_z"], r_i, w + p["stutzen_l"] - 15)
    U.fertig(b, root, "T107", d, "PE / PVC-U")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, 1200], 0.7, 0.3, 6500, None), ("02-schnitt", [0, 0, 1200], 0.0, 0.0, 6000, "y=0")])
