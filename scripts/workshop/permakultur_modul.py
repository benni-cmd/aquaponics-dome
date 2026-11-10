"""Permakultur-Modul T111 (Platzhalter, U2, D104, D107): Kompostbox aus Fichte 1500 x 525 x 600 (offen, mit Deckel) und Futterzuchtkiste PE 800 x 525 x 350 daneben.
KS: Mitte der Kompostbox in X/Y, Z 0 = Fussboden; Kiste bei +X. Maße Annahme, Rechteck 1500 x 525 aus der Zeichnung. Aufruf: python -X utf8 scripts/workshop/permakultur_modul.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U

NAME = "permakultur_modul"
MAT = {"Holz Fichte": (0.45, "#c8a878"), "PE Tank": (0.95, "#d9d4c0")}


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T111_Permakultur_Modul"
    b.add("component.create", name=root, grounded=True)
    L, B, H, t = p["kompost_l"], p["kompost_b"], p["kompost_h"], p["holz_t"]
    U.box(b, "Kompostbox", (L, B, H), (0, 0, H / 2), "Holz Fichte")
    U.box(b, "Kompostbox", (L - 2 * t, B - 2 * t, H - t + 1), (0, 0, t + (H - t + 1) / 2), None, schneiden=["Kompostbox"])
    U.box(b, "Kompostdeckel", (L, B, t), (0, 0, H + t / 2), "Holz Fichte")
    kl, kh, kw = p["kiste_l"], p["kiste_h"], p["kiste_wand"]
    xk = L / 2 + p["abstand"] + kl / 2
    U.box(b, "Futterzuchtkiste", (kl, B, kh), (xk, 0, kh / 2), "PE Tank")
    U.box(b, "Futterzuchtkiste", (kl - 2 * kw, B - 2 * kw, kh - kw + 1), (xk, 0, kw + (kh - kw + 1) / 2), None, schneiden=["Futterzuchtkiste"])
    U.fertig(b, root, "T111", d, "Fichtenholz / PE")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [600, 0, 300], 0.7, 0.4, 3600, None)])
