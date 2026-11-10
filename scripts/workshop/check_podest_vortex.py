"""Pruefung Podest Vortex T102 (U2): Aufbau, Hoehe 577 gegen Soll (1900 - 1323), Stuetzendruck/Knicken, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_podest_vortex.py   (exit 1 bei FAIL)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import podest_check_lib as P

if __name__ == "__main__":
    sys.exit(P.pruefen("podest_vortex", "podest_vortex_h", 577))
