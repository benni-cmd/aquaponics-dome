"""Notluftpumpe T109 (U2, D103, A24): Luftpumpe-Gehaeuse, Ausgangstuelle, Rueckschlagventil, Luftschlauch (vier Stuecke) mit Schleife ueber den Rand des Fischtanks (Z 1300), Luftstein am Boden (Z -980).
KS: Mitte der Pumpen-Standflaeche, Z 0 = Fussboden; Schlauch +X. Aufruf: python -X utf8 scripts/workshop/notluftpumpe.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U

NAME = "notluftpumpe"
MAT = {"PS grau": (1.05, "#777777"), "PP weiss": (0.91, "#e8e5d8"), "Ventil blau": (1.4, "#3a6ea8"), "Schlauch hellblau": (1.25, "#8fd3f0"), "PE Tank": (0.95, "#d9d4c0")}


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T109_Notluftpumpe"
    b.add("component.create", name=root, grounded=True)
    l, bb, h = p["pumpe_l"], p["pumpe_b"], p["pumpe_h"]
    U.box(b, "Pumpe", (l, bb, h), (0, 0, h / 2), "PS grau")
    x0 = l / 2
    z = p["tuelle_z"]
    U.cyl(b, "Tuelle", p["tuelle_d"], p["tuelle_l"], (x0, 0, z), (1, 0, 0), "PP weiss")
    x1 = x0 + p["tuelle_l"]
    U.cyl(b, "Rueckschlagventil", p["rv_d"], p["rv_l"], (x1, 0, z), (1, 0, 0), "Ventil blau")
    x2 = x1 + p["rv_l"]
    sd, sx, sz, tx = p["schlauch_d"], p["schleife_x"], p["schleife_z"], p["tank_x"]
    z_stein_u = -1000 + p["stein_ueber_boden"]
    z_stein_o = z_stein_u + p["stein_l"]
    # Schlauch in vier Stuecken (Stoss an Stoss, Knicke als Beruehrung; gleichgrosse Zylinder lassen sich nicht sauber verschmelzen): waagerecht, hinauf, ueber den Rand, hinab bis Oberkante Luftstein
    r = sd / 2
    U.cyl(b, "Luftschlauch_1", sd, sx - r - x2, (x2, 0, z), (1, 0, 0), "Schlauch hellblau")
    U.cyl(b, "Luftschlauch_2", sd, sz + r - (z - r), (sx, 0, z - r), (0, 0, 1), "Schlauch hellblau")
    U.cyl(b, "Luftschlauch_3", sd, tx - sx - 2 * r, (sx + r, 0, sz), (1, 0, 0), "Schlauch hellblau")
    U.cyl(b, "Luftschlauch_4", sd, sz + r - z_stein_o, (tx, 0, z_stein_o), (0, 0, 1), "Schlauch hellblau")
    U.cyl(b, "Luftstein", p["stein_d"], p["stein_l"], (tx, 0, z_stein_u), (0, 0, 1), "PE Tank")
    U.fertig(b, root, "T109", d, "PS / PVC-P / PE")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-seite", [380, 0, 150], 0.0, 0.0, 4200, None), ("02-pumpe", [200, 0, 120], 0.7, 0.35, 900, None)])
