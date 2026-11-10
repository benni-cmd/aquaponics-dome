"""Schlamm-Sammelbehaelter T106 (U2, D104, A11): oberirdischer PE-Behaelter 350 l (innen Ø 880 x 575), Deckel, Einlaufstutzen d40, Entlueftung, Ablaufrohr d40 durch die Wand mit Kugelhahn und Hebel.
KS: Mitte der Standflaeche, Z 0 = Fussboden; Ablasshahn bei +X. Aufruf: python -X utf8 scripts/workshop/schlamm_sammelbehaelter.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import leitung as L

NAME = "schlamm_sammelbehaelter"
MAT = {"PE Tank": (0.95, "#d9d4c0"), "PVC grau": (1.4, "#8d9296"), "LT hahn": (1.4, "#3a6ea8"), "PA schwarz": (1.14, "#222222"), "PP grau": (0.91, "#9a9ea3")}


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T106_Schlamm_Sammelbehaelter"
    b.add("component.create", name=root, grounded=True)
    D, w, hi, dt = p["aussen_d"], p["wand"], p["innen_h"], p["deckel_t"]
    h = w + hi                                                           # Behaelterhoehe (Boden + Innenhoehe)
    U.cyl(b, "Behaelter", D, h, (0, 0, 0), (0, 0, 1), "PE Tank")
    U.cyl(b, "Behaelter_Innen", D - 2 * w, hi + 1, (0, 0, w), (0, 0, 1), None, schneiden=["Behaelter"])
    U.cyl(b, "Deckel", D, dt, (0, 0, h), (0, 0, 1), "PE Tank")
    # Einlaufstutzen d40 mittig auf dem Deckel (Muffe oben), Bohrung durch Stutzen und Deckel
    of, t = L.od_f(40), L.DEPTH[40]
    U.cyl(b, "Einlaufstutzen", of, p["einlauf_l"], (0, 0, h + dt), (0, 0, 1), "PVC grau")
    U.cyl(b, "Einlauf_Muffe", 40, t + 1, (0, 0, h + dt + p["einlauf_l"] - t), (0, 0, 1), None, schneiden=["Einlaufstutzen"])
    U.cyl(b, "Einlauf_Bohrung", 36, p["einlauf_l"] + dt + 2, (0, 0, h - 1), (0, 0, 1), None, schneiden=["Einlaufstutzen", "Deckel"])
    # Entlueftung exzentrisch
    U.cyl(b, "Entlueftung", p["ent_d"], 30, (250, 0, h + dt), (0, 0, 1), "PP grau")
    U.cyl(b, "Entlueftung_Bohrung", 10, 30 + dt + 2, (250, 0, h - 1), (0, 0, 1), None, schneiden=["Entlueftung", "Deckel"])
    # Ablaufrohr d40 (Aussen 40) durch die Wand bei Z auslauf_z, 10 mm in den Behaelter, 30 mm heraus
    r_o, r_i = D / 2, D / 2 - w
    z = p["auslauf_z"]
    U.cyl(b, "Auslauf_Bohrung", 40.4, w + 2, (r_i - 1, 0, z), (1, 0, 0), None, schneiden=["Behaelter"])
    U.cyl(b, "Auslaufrohr", 40, 50, (r_i - 10, 0, z), (1, 0, 0), "PVC grau")
    U.cyl(b, "Auslaufrohr_Bohrung", 34, 52, (r_i - 11, 0, z), (1, 0, 0), None, schneiden=["Auslaufrohr"])
    # Kugelhahn: Muffe d40 nimmt das Rohrende auf (0,2 mm Klebespalt, sonst fallen die Zylinderflaechen zusammen); Hebel oben
    xh = r_o + 4
    U.cyl(b, "Kugelhahn", p["hahn_d"], 70, (xh, 0, z), (1, 0, 0), "LT hahn")
    U.cyl(b, "Hahn_Muffe", 40.4, 28, (xh - 1, 0, z), (1, 0, 0), None, schneiden=["Kugelhahn"])
    U.cyl(b, "Hahn_Durchgang", 26, 72, (xh - 1, 0, z), (1, 0, 0), None, schneiden=["Kugelhahn"])
    U.box(b, "Hahnhebel", (12, 90, 10), (xh + 35, 0, z + p["hahn_d"] / 2 + 5), "PA schwarz")
    U.fertig(b, root, "T106", d, "PE / PVC-U")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, 300], 0.8, 0.4, 2400, None), ("02-schnitt", [0, 0, 300], 0.0, 0.0, 2200, "y=0")])
