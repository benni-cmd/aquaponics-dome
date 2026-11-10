"""Podest Vortex T102 (U2, D100): Stahlrahmen fuer tank_klein (Standflaeche 619 x 619), Hoehe = Parameter podest_vortex_h (mindestens 577 mm = Wsp 1900 - Tankoberkante 1323).
Aufruf: python -X utf8 scripts/workshop/podest_vortex.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import podest_lib as P

NAME = "podest_vortex"


def build(ueber=None):
    return P.bauen(NAME, "T102_Podest_Vortex", "T102", "podest_vortex_h", ueber)


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, 300], 0.7, 0.4, 1900, None), ("02-seite", [0, 0, 300], 0.0, 0.0, 1900, None)])
