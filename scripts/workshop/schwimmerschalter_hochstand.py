"""Schwimmerschalter Hochstand T105 (U2, D105, A20): Kabel-Schwimmerschalter (Kugel Ø 70), Kabelklemme PA, Meldeleitung (Kabel Ø 7, Ausschnitt).
KS: Mitte des Schwimmers im Ursprung = Schaltpunkt (Sumpf: Z -110); Kabel nach oben. Aufruf: python -X utf8 scripts/workshop/schwimmerschalter_hochstand.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U

NAME = "schwimmerschalter_hochstand"
MAT = {"Schwimmer orange": (0.91, "#e07a2f"), "PA schwarz": (1.14, "#222222"), "Kabel schwarz": (1.2, "#1a1a1a")}


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T105_Schwimmerschalter_Hochstand"
    b.add("component.create", name=root, grounded=True)
    r, s, kd = p["schwimmer_d"] / 2, p["klemme_s"], p["kabel_d"]
    U.kugel(b, "Schwimmer", p["schwimmer_d"], (0, 0, 0), "Schwimmer orange")
    U.box(b, "Kabelklemme", (s, s, s), (0, 0, r + s / 2), "PA schwarz")
    U.cyl(b, "Kabelklemme_Bohrung", kd, s + 2, (0, 0, r - 1), (0, 0, 1), None, schneiden=["Kabelklemme"])
    U.cyl(b, "Kabel", kd, p["kabel_l"], (0, 0, r), (0, 0, 1), "Kabel schwarz")
    U.fertig(b, root, "T105", d, "PP / PA / PVC")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, 150], 0.7, 0.3, 900, None)])
