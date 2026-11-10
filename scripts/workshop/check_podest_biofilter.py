"""Pruefung Podest Biofilter T103 (U2): Aufbau, Hoehe 230 gegen Soll (1800 - 1570), Stuetzendruck/Knicken, Interferenz 0.
Aufruf: python -X utf8 scripts/workshop/check_podest_biofilter.py   (exit 1 bei FAIL)"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import podest_check_lib as P

if __name__ == "__main__":
    sys.exit(P.pruefen("podest_biofilter", "podest_biofilter_h", 230))
