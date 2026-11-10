"""Venturi-Belueffter T104 (U2, D103, A19): Injektor (Klasse Mazzei 1583) im Druckrohr d50 mit Klebemuffen, Ansaugstutzen, Rueckschlagventil Luft und Luftfilter.
KS: Port A (Mitte Muffenoeffnung Eintritt) im Ursprung, Stroemung +X, Z hoch. Aufruf: python -X utf8 scripts/workshop/venturi_belueffter.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import leitung as L

NAME = "venturi_belueffter"
MAT = {"PVC grau": (1.4, "#8d9296"), "PP weiss": (0.91, "#e8e5d8"), "PP grau": (0.91, "#9a9ea3"), "Ventil blau": (1.4, "#3a6ea8")}


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T104_Venturi_Belueffter"
    b.add("component.create", name=root, grounded=True)
    dp, t, ml = p["pipe_d"], L.DEPTH[p["pipe_d"]], p["muffe_l"]
    of = L.od_f(dp)
    x_inj, x_end = ml, ml + p["inj_l"]
    # Muffe Ein: Oeffnung bei x 0, Durchgang bis zum Injektor
    U.cyl(b, "Muffe_Ein", of, ml, (0, 0, 0), (1, 0, 0), "PVC grau")
    U.cyl(b, "Muffe_Ein_Tasche", dp, t + 1, (-1, 0, 0), (1, 0, 0), None, schneiden=["Muffe_Ein"])
    U.cyl(b, "Muffe_Ein_Durchgang", p["inj_bohr"], ml + 2, (-1, 0, 0), (1, 0, 0), None, schneiden=["Muffe_Ein"])
    # Injektorkoerper mit Durchgang und Ansaugstutzen (eigene Koerper, stossen an)
    U.cyl(b, "Injektor", p["inj_d"], p["inj_l"], (x_inj, 0, 0), (1, 0, 0), "PP weiss")
    U.cyl(b, "Injektor_Durchgang", p["inj_bohr"], p["inj_l"] + 2, (x_inj - 1, 0, 0), (1, 0, 0), None, schneiden=["Injektor"])
    # Muffe Aus: Oeffnung bei x_end + ml
    U.cyl(b, "Muffe_Aus", of, ml, (x_end, 0, 0), (1, 0, 0), "PVC grau")
    U.cyl(b, "Muffe_Aus_Tasche", dp, t + 1, (x_end + ml - t, 0, 0), (1, 0, 0), None, schneiden=["Muffe_Aus"])
    U.cyl(b, "Muffe_Aus_Durchgang", p["inj_bohr"], ml + 2, (x_end - 1, 0, 0), (1, 0, 0), None, schneiden=["Muffe_Aus"])
    # Luftstrang senkrecht auf der Injektormitte
    xm = x_inj + p["inj_l"] / 2
    z0 = p["inj_d"] / 2
    U.cyl(b, "Saugstutzen", p["saug_d"], p["saug_l"], (xm, 0, z0), (0, 0, 1), "PP grau")
    U.cyl(b, "Saugstutzen_Bohrung", p["luft_bohr"], p["saug_l"] + 2, (xm, 0, z0 - 1), (0, 0, 1), None, schneiden=["Saugstutzen"])
    z1 = z0 + p["saug_l"]
    U.cyl(b, "Rueckschlagventil", p["rv_d"], p["rv_l"], (xm, 0, z1), (0, 0, 1), "Ventil blau")
    U.cyl(b, "Rueckschlagventil_Bohrung", p["luft_bohr"], p["rv_l"] + 2, (xm, 0, z1 - 1), (0, 0, 1), None, schneiden=["Rueckschlagventil"])
    z2 = z1 + p["rv_l"]
    U.cyl(b, "Luftfilter", p["filter_d"], p["filter_l"], (xm, 0, z2), (0, 0, 1), "PP weiss")
    U.fertig(b, root, "T104", d, "PP / PVC-U")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [135, 0, 60], 0.7, 0.35, 650, None), ("02-schnitt", [135, 0, 60], 0.0, 0.0, 650, "y=0")])
