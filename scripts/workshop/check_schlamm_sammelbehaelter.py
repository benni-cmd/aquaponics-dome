"""Pruefung Schlamm-Sammelbehaelter T106 (U2): 350 l (Innenvolumen aus Wandvolumen gerechnet), oberirdisch (Unterkante Z 0), Fussabdruck Ø 900 = Zeichnung sludge_1 (Radius 450),
Einlauf unter dem Schlammstutzen des Vortex (Gefaelle abwaerts), Ablasshahn von Hand (Hahn d40 am Boden), Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_schlamm_sammelbehaelter.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U
import leitung as L


def main():
    c = U.Pruefung("schlamm_sammelbehaelter")
    p = c.p
    c.koerper(["Behaelter", "Deckel", "Einlaufstutzen", "Entlueftung", "Auslaufrohr", "Kugelhahn", "Hahnhebel"])
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    s1 = next(x for x in soll["bauteile"] if x["id"] == "sludge_1")
    rz = s1["lage"]["zeichnung_primitive"][0]["radius_mm"]
    c.eq("Fussabdruck Ø 900 = 2 x Zeichnung sludge_1 Radius 450", c.ausdehnung("Behaelter", 0), 2 * rz, 0.1)
    c.eq("Oberirdisch: Unterkante Behaelter = Fussboden Z 0", c.unten("Behaelter"), 0, 0.1)
    c.eq("Behaelterhoehe 585 (Boden 10 + innen 575)", c.ausdehnung("Behaelter", 2), 585, 0.1)
    # Innenvolumen: Hohlzylinder aus Aussenvolumen minus Wandvolumen (Koerpervolumen messen, unabhaengig von der Parameterformel)
    r_o = c.ausdehnung("Behaelter", 0) / 2
    hoehe = c.ausdehnung("Behaelter", 2)
    bohrung = math.pi * 20.2 ** 2 * 10                                # Rohrdurchgang in der Wand (d40,4 x 10)
    innen = math.pi * (r_o - 10) ** 2 * 575 / 1e6
    ist = (math.pi * r_o ** 2 * hoehe - c.B["Behaelter"]["volume_mm3"] - bohrung) / 1e6    # Litern des Hohlraums ab Boden bis Rand
    c.eq(f"Hohlraum {ist:.1f} l = Innenvolumen Ø 880 x 575 + Boden 0 = {innen:.1f} l (Messung aus Koerpervolumen)", ist, innen, 1.5)
    c.eq(f"Nutzvolumen {innen:.0f} l gegen Quelle 350 l (+-1 Prozent)", 1 if abs(innen - 350) <= 3.5 else 0, 1)
    # Gefaelle: Einlauf-Oberkante unter dem Schlammstutzen des Vortex
    top_einlauf = c.oben("Einlaufstutzen")
    c.wahr(f"Einlauf-Oberkante Z {top_einlauf:g} liegt unter dem Schlammstutzen des Vortex Z {p['vortex_schlammstutzen_z']} (Schlamm laeuft per Schwerkraft abwaerts)", top_einlauf < p["vortex_schlammstutzen_z"])
    c.eq("Einlaufstutzen Aussen-Ø = Formstueck d40", c.ausdehnung("Einlaufstutzen", 0), L.od_f(40), 0.1)
    c.port("Einlauf (Muffe d40)", "Einlaufstutzen", (0, 0, top_einlauf), (0, 0, 1))
    c.zylinder("Einlauf-Muffe d40", "Einlaufstutzen", 20)
    # Ablasshahn von Hand: Hahn am Boden, Hebel nur von Hand
    c.wahr(f"Ablaufachse Z {c.mitte('Kugelhahn', 2):g} nahe am Boden (<= 60), Ablass nur ueber den Handhahn", c.mitte("Kugelhahn", 2) <= 60)
    c.eq("Kugelhahn-Gehaeuse Ø 52", c.ausdehnung("Kugelhahn", 1), 52, 0.1)
    c.eq("Ablaufrohr ragt aus der Wand: Aussenende x = 450 + 4 + 26", c.B["Auslaufrohr"]["bbox"]["max"][0], 480, 0.1)
    c.zylinder("Hahn-Muffe d40 mit 0,2 mm Klebespalt", "Kugelhahn", 20.2)
    c.wahr("Gesamthoehe mit Deckel und Einlaufstutzen <= 700", c.oben("Einlaufstutzen") <= 700)
    c.interferenz()
    print("INFO Restmenge unter dem Ablauf: pi x 0,44^2 x 0,03 m = 18 l (Ablauf Z 40, Innenboden Z 10)")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
