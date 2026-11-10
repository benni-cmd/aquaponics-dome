"""Pruefung Regentank 5 m3 T107 (Platzhalter, U2): Innenvolumen aus dem Koerpervolumen gemessen gegen 5000 l der Quelle (rain), Maße als Annahme, Stutzen d25 und d63 (Muffe, Port), Dom,
Ueberlauf ueber dem Auslauf, Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_regentank_5m3.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U
import leitung as L


def main():
    c = U.Pruefung("regentank_5m3")
    p = c.p
    c.koerper(["Tank", "Dom", "Domdeckel", "Auslaufstutzen", "Ueberlaufstutzen"])
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    rain = next(x for x in soll["bauteile"] if x["id"] == "rain")
    kap = rain["kennzahlen_index"]["Tank-Kapazität"]
    c.wahr(f"Quelle nennt 5 m3 ('{kap}')", "5.0 m" in kap)
    c.eq("Parameter volumen_l = 5000 (Quelle)", p["volumen_l"], 5000)
    c.eq("Aussen-Ø 1700 (Annahme)", c.ausdehnung("Tank", 0), 1700, 0.1)
    c.eq("Tankhoehe 2300 (Annahme)", c.ausdehnung("Tank", 2), 2300, 0.1)
    c.eq("Unterkante Fussboden Z 0", c.unten("Tank"), 0, 0.1)
    # Innenvolumen = Aussenzylinder minus Koerper minus Loecher (Dom, Stutzen), aus gemessenem Koerpervolumen
    ro, hh = 850, c.ausdehnung("Tank", 2)
    loecher = math.pi * 220 ** 2 * 15 + math.pi * (L.od_f(25) + 0.4) ** 2 / 4 * 15 + math.pi * (L.od_f(63) + 0.4) ** 2 / 4 * 15
    ist = (math.pi * ro ** 2 * hh - c.B["Tank"]["volume_mm3"] - loecher) / 1e6
    soll_l = math.pi * 835 ** 2 * 2270 / 1e6
    c.eq(f"Innenvolumen aus Koerpervolumen {ist:.0f} l = Rechnung {soll_l:.0f} l", ist, soll_l, 6)
    c.eq(f"Innenvolumen {soll_l:.0f} l gegen Quelle 5000 l (+-1 Prozent)", 1 if abs(soll_l - 5000) <= 50 else 0, 1)
    c.eq("Dom Ø 500", c.ausdehnung("Dom", 0), 500, 0.1)
    c.eq("Dom sitzt auf dem Tank (Unterkante 2300)", c.unten("Dom"), 2300, 0.1)
    c.eq("Domdeckel sitzt auf dem Dom (Unterkante 2450)", c.unten("Domdeckel"), 2450, 0.1)
    c.eq("Auslauf Aussen-Ø = Formstueck d25", c.ausdehnung("Auslaufstutzen", 2), L.od_f(25), 0.1)
    c.eq("Ueberlauf Aussen-Ø = Formstueck d63", c.ausdehnung("Ueberlaufstutzen", 2), L.od_f(63), 0.1)
    c.zylinder("Auslauf Muffe d25", "Auslaufstutzen", 12.5)
    c.zylinder("Ueberlauf Muffe d63", "Ueberlaufstutzen", 31.5)
    xa = c.B["Auslaufstutzen"]["bbox"]["max"][0]
    c.port("Auslauf (Muffe d25)", "Auslaufstutzen", (xa, 0, p["auslauf_z"]), (1, 0, 0))
    xu = c.B["Ueberlaufstutzen"]["bbox"]["max"][0]
    c.port("Ueberlauf (Muffe d63)", "Ueberlaufstutzen", (xu, 0, p["ueberlauf_z"]), (1, 0, 0))
    c.wahr("Ueberlauf liegt ueber dem Auslauf und unter dem Rand", p["auslauf_z"] < p["ueberlauf_z"] < 2300)
    c.interferenz()
    print("INFO Hoehe, Lage und Typ sind ANNAHME (Quelle: Hoehe nicht festgelegt, Zeichnung nur Rechteck 1625 x 500); Last gefuellt 5 t + Tank")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
