"""N-UNIFY-AUTOBAHN P1c: misst den Ist-Stand der wasserfuehrenden Bauteile im Ring-B2-Export (Grundlage der Soll-Ist-Tabelle).

Aufruf (Projektordner):  python -I -X utf8 scripts/oasis_istmessung.py [--variante a_plus|ring_b2]   (Standard ring_b2)
Eingabe: viewer/varianten/ring_b2/instances.json bzw. viewer/instances.json (A+), von `viewer/export_model.py` erzeugt (Stand im Feld `built`).
Ausgabe: je Bauteil-Definition Anzahl, Hoehe der Instanz-Ursprungs ueber dem Fussboden (Modell-Z 400, `walk_z`), Radius und Azimut um die Kuppelmitte.
Hinweis: Instanz-Ursprung = Bauteil-Nullpunkt (meist Standflaeche), nicht Wasserspiegel; Wasserspiegel und Hoehen der Bauteile stehen in der Soll-Ist-Tabelle mit Quelle.
"""
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = sys.argv[sys.argv.index("--variante") + 1] if "--variante" in sys.argv else "ring_b2"
P = os.path.join(ROOT, "viewer", "varianten", "ring_b2", "instances.json") if V == "ring_b2" else os.path.join(ROOT, "viewer", "instances.json")
WASSER = re.compile(r"^(pool|zweitbecken|becken_dritt|biofilter|tank_|pumpe_|feinfilter|schlammfass|pegelschacht|puffer|schwimmer|ring_|ringstuetze|entluefter|"
                    r"nft_tisch|ibc_beet|geblaese|luftverteiler|luft_|aktivkohle|zulaufrohr|schaltschrank|ausleger|lt_(kugelhahn|rueckschlag)|sonde_level|beet_sumpf|portal_joch|"
                    r"podest_|tauchpumpe|venturi|schwimmerschalter|notluft|schlamm_sammel|regentank|permakultur|nachspeise|sumpftank)")
VERBOTEN = ("feinfilter", "pumpe_klein", "pumpe_gross", "pegelschacht", "schlammfass")   # U5 (D101): Altbestand ohne Gegenstueck in der Quelle, in ring_b2 entfernt


def main():
    d = json.load(open(P, encoding="utf-8"))
    rc = 0
    fz = d.get("walk_z", 400)
    g = {}
    for i in d["instances"]:
        if WASSER.match(i["d"]):
            g.setdefault(i["d"], []).append(i["m"])
    print("Variante %s, Export %s, Instanzen %d, Fussboden Z %s" % (V, d["built"], len(d["instances"]), fz))
    print("%-26s %4s  %-16s %-14s %-14s" % ("Definition", "n", "z ueber Boden", "Radius mm", "Azimut Grad"))
    for k in sorted(g):
        m = g[k]
        z = [x[11] - fz for x in m]
        r = [math.hypot(x[3], x[7]) for x in m]
        a = [math.degrees(math.atan2(x[7], x[3])) for x in m]
        print("%-26s %4d  %6.0f..%-8.0f %5.0f..%-8.0f %5.0f..%-5.0f" % (k, len(m), min(z), max(z), min(r), max(r), min(a), max(a)))
    if V == "ring_b2":   # U5: Soll = keine Definition des entfernten Altbestands mehr (Pruefbefehl 2, Exit 1 bei Treffer)
        alle = {i["d"].split("-ring_b2")[0] for i in d["instances"]}
        treffer = sorted(x for x in alle if x.startswith(VERBOTEN))
        print("Altbestand ohne Soll (%s): %s" % (", ".join(v + "*" for v in VERBOTEN), ", ".join(treffer) if treffer else "keine Definition vorhanden (OK)"))
        rc = 1 if treffer else 0
    return rc


if __name__ == "__main__":
    sys.exit(main())
