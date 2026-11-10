"""Pruefsatz der Podeste (U2): Koerperzahl 24, Hoehe = Parameter, Hoehe gegen Soll (Wsp minus Tankoberkante), Standflaeche, Auflage, Stuetzendruck und Knicken (gerechnet), Interferenz 0.
Benutzt von check_podest_vortex.py und check_podest_biofilter.py."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U


def pruefen(name, hkey, h_min_soll):
    c = U.Pruefung(name)
    p, u2 = c.p, c.d["u2"]
    h = p[hkey]
    namen = [f"Fussplatte_{i}" for i in range(1, 5)] + [f"Stuetze_{i}" for i in range(1, 5)] + [f"Fussrahmen_{i}" for i in range(1, 5)] + [f"Kopfrahmen_{i}" for i in range(1, 5)] + [f"Knotenblech_{i}" for i in range(1, 9)]
    c.koerper(namen)
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    bt = {x["id"]: x for x in soll["bauteile"]}
    wsp = bt["vortex_1" if "vortex" in name else "bio_1"]["hoehen"]["wsp_ueber_fussboden_mm"]
    c.eq(f"Parameter Wsp-Soll {u2['wsp']} = Soll-Datei", u2["wsp"], wsp)
    c.eq(f"Soll-Hoehe = Wsp {wsp} minus Tank-Oberkante {u2['tank_ok']} = {wsp - u2['tank_ok']}", h_min_soll, wsp - u2["tank_ok"])
    c.wahr(f"Hoehe {h} mm ist mindestens die Soll-Hoehe {h_min_soll} (D100)", h >= h_min_soll)
    c.eq("Auflage: Oberkante der Kopfrahmen = Parameter Hoehe", max(c.oben(f"Kopfrahmen_{i}") for i in range(1, 5)), h, 0.1)
    c.eq("Oberkante der Stuetzen = Parameter Hoehe", c.oben("Stuetze_1"), h, 0.1)
    c.eq("Unterkante der Fussplatten = Z 0", c.unten("Fussplatte_1"), 0, 0.1)
    mn, mx = sc.bbox_all(c.ev)
    c.eq(f"Standflaeche X = span {p['span']} + 2 x 30 (Fussplatte 100 steht 30 ueber den Rahmen, Knotenblech 6 liegt innerhalb)", mx[0] - mn[0], p["span"] + 60, 0.1)
    c.eq(f"Standflaeche Y = span {p['span']} + 60", mx[1] - mn[1], p["span"] + 60, 0.1)
    c.wahr(f"Plattform {u2['plat']} des Tanks liegt innerhalb der Rahmenmitte (Rahmen innen {p['span'] - 80} >= {u2['plat']} - 60)", p["span"] - 80 >= u2["plat"] - 60)
    c.eq("Stuetze Querschnitt 40 x 40", c.ausdehnung("Stuetze_1", 0), 40, 0.1)
    c.eq("Rahmenstuecke zwischen den Stuetzen: Laenge span - 80", c.ausdehnung("Kopfrahmen_1", 0), p["span"] - 80, 0.1)
    # Rechnung: Stuetzendruck und Knicken (Euler, beidseitig gelenkig), Stahl S235 [A]
    A = 40 ** 2 - 34 ** 2                                           # Vierkantrohr 40 x 40 x 3
    I = (40 ** 4 - 34 ** 4) / 12
    F = u2["last_kg"] * 9.81 / 4
    druck = F / A
    pcr = math.pi ** 2 * 210000 * I / (h - 6) ** 2
    c.wahr(f"Stuetzendruck {druck:.1f} N/mm2 bei {u2['last_kg']} kg gefuellt (4 Stuetzen) unter 235/3 = 78 N/mm2", druck < 235 / 3)
    c.wahr(f"Knicklast je Stuetze {pcr / 1000:.0f} kN gegen {F / 1000:.1f} kN: Faktor {pcr / F:.0f} >= 5", pcr / F >= 5)
    print(f"INFO Rechnung: python -X utf8 -I -c \"import math;A=444;I=(40**4-34**4)/12;print(math.pi**2*210000*I/({h}-6)**2)\" ; Last {u2['last_kg']} kg gefuellt inkl. Tank [A]; Kippen und Horizontalkraefte: N-STATIK offen")
    c.interferenz()
    return c.fertig()
