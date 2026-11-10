"""Tauchpumpen-Modul T110 (U2, D92, D102, A14): vereinfachter Koerper der Oase AquaMax Eco Premium 8000 (Kandidat R59) mit Gehaeuse 340 x 280 x 165 (Maße laut Hersteller-Shop, Q), Druckstutzen d50, Rueckschlagventil d50 und Netzkabel.
KS: Mitte der Standflaeche (Unterkante Gehaeuse), Z 0 = Boden des Beckens; Druckleitung senkrecht nach oben (Port Z 314), Kabel +X. Aufruf: python -X utf8 scripts/workshop/tauchpumpe_modul.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import leitung as L

NAME = "tauchpumpe_modul"
MAT = {"PP grau": (0.91, "#9a9ea3"), "Pumpe blau": (1.5, "#3a5f9a"), "Ventil blau": (1.4, "#3a6ea8"), "Kabel schwarz": (1.2, "#1a1a1a")}


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T110_Tauchpumpe_Modul"
    b.add("component.create", name=root, grounded=True)
    gh = p["geh_h"]
    z_g = gh                                                            # Oberkante Gehaeuse (165)
    U.box(b, "Gehaeuse", (p["geh_l"], p["geh_b"], gh), (0, 0, gh / 2), "Pumpe blau")     # Maße laut Oase-Teichbau-Seite (Q): 340 x 280 x 165, Ansaugkorb darin enthalten
    U.cyl(b, "Druckstutzen", 50, p["stutzen_l"], (0, 0, z_g), (0, 0, 1), "PP grau")
    z_v = z_g + p["stutzen_l"] - L.DEPTH[50]                            # Ventil beginnt 31 mm unter der Stutzenspitze (Stutzen steckt in der unteren Muffe)
    U.cyl(b, "Rueckschlagventil", p["rv_d"], p["rv_l"], (0, 0, z_v), (0, 0, 1), "Ventil blau")
    U.cyl(b, "Ventil_Muffe_unten", 50.4, L.DEPTH[50] + 1, (0, 0, z_v - 1), (0, 0, 1), None, schneiden=["Rueckschlagventil"])
    U.cyl(b, "Ventil_Durchgang", 36, p["rv_l"] + 2, (0, 0, z_v - 1), (0, 0, 1), None, schneiden=["Rueckschlagventil"])
    U.cyl(b, "Ventil_Muffe_oben", 50, L.DEPTH[50] + 1, (0, 0, z_v + p["rv_l"] - L.DEPTH[50]), (0, 0, 1), None, schneiden=["Rueckschlagventil"])
    U.cyl(b, "Kabel", p["kabel_d"], p["kabel_l"], (p["geh_l"] / 2 + 0.5, 0, 80), (1, 0, 0), "Kabel schwarz")
    U.fertig(b, root, "T110", d, "Pumpengehaeuse / PP / PVC-U")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, 200], 0.7, 0.35, 1300, None), ("02-schnitt", [0, 0, 200], 0.0, 0.0, 1200, "y=0")])
