"""Pruefung Permakultur-Modul T111 (Platzhalter, U2): Rechteck 1500 x 525 aus data/oasis-soll.json (permakultur), Hoehe und Wandstaerken als Annahme, Innenvolumen aus dem Koerpervolumen,
Kiste neben der Box ohne Beruehrung, Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_permakultur_modul.py   (exit 1 bei FAIL)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U


def main():
    c = U.Pruefung("permakultur_modul")
    p = c.p
    c.koerper(["Kompostbox", "Kompostdeckel", "Futterzuchtkiste"])
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    r = next(x for x in soll["bauteile"] if x["id"] == "permakultur")["lage"]["zeichnung_primitive"][0]
    c.eq("Kompostbox Laenge = Zeichnung permakultur breite_mm 1500", c.ausdehnung("Kompostbox", 0), r["breite_mm"], 0.1)
    c.eq("Kompostbox Tiefe = Zeichnung permakultur hoehe_mm 525", c.ausdehnung("Kompostbox", 1), r["hoehe_mm"], 0.1)
    c.eq("Kompostbox Hoehe 600 (Annahme)", c.ausdehnung("Kompostbox", 2), 600, 0.1)
    c.eq("Unterkante Fussboden Z 0", c.unten("Kompostbox"), 0, 0.1)
    # Innenvolumen: Quader minus Koerpervolumen
    aussen = 1500 * 525 * 600
    innen_box = (aussen - c.B["Kompostbox"]["volume_mm3"]) / 1e6
    erw = (1450 * 475 * 575) / 1e6
    c.eq(f"Kompostbox Hohlraum {innen_box:.0f} l = 1450 x 475 x 575 = {erw:.0f} l", innen_box, erw, 0.5)
    c.eq("Deckel liegt auf der Box (Unterkante 600)", c.unten("Kompostdeckel"), 600, 0.1)
    c.eq("Deckel Dicke 25", c.ausdehnung("Kompostdeckel", 2), 25, 0.1)
    kiste = (800 * 525 * 350 - c.B["Futterzuchtkiste"]["volume_mm3"]) / 1e6
    erw_k = (788 * 513 * 344) / 1e6
    c.eq(f"Futterzuchtkiste Hohlraum {kiste:.0f} l = 788 x 513 x 344 = {erw_k:.0f} l", kiste, erw_k, 0.5)
    spalt = c.B["Futterzuchtkiste"]["bbox"]["min"][0] - c.B["Kompostbox"]["bbox"]["max"][0]
    c.eq("Kiste steht 50 mm neben der Box", spalt, 50, 0.1)
    c.interferenz()
    print("INFO Platzhalter: Hoehen, Wandstaerken und Futterzuchtkiste sind Annahme (Quelle nur Rechteck und Stichworte)")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
