"""Podest Biofilter T103 (U2, D100): Stahlrahmen fuer tank_gross (Standflaeche 821 x 821), Hoehe = Parameter podest_biofilter_h (230 mm = Wsp 1800 - gebauter Ueberlauf 1570).
Aufruf: python -X utf8 scripts/workshop/podest_biofilter.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import podest_lib as P

NAME = "podest_biofilter"


def build(ueber=None):
    return P.bauen(NAME, "T103_Podest_Biofilter", "T103", "podest_biofilter_h", ueber)


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, 120], 0.7, 0.4, 1700, None), ("02-seite", [0, 0, 120], 0.0, 0.0, 1700, None)])
