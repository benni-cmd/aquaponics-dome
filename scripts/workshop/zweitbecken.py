"""Anzuchtbecken (T6, N-UNIFY-AUTOBAHN U3, D118): Wrapper um becken_soll.py. Aufruf: python -X utf8 scripts/workshop/zweitbecken.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import becken_soll

if __name__ == "__main__":
    becken_soll.main("zweitbecken")
