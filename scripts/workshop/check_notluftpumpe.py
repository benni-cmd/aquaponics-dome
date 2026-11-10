"""Pruefung Notluftpumpe T109 (U2): Koerperzahl, Luftstein auf dem Boden des Fischtanks (Soll-Datei fish Boden -1000), Schlauchschleife ueber dem Rand 1200 (Siphonbrecher), Stein unter dem Spiegel 750,
Ausgangstuelle und Rueckschlagventil am Pumpengehaeuse, Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_notluftpumpe.py   (exit 1 bei FAIL)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U


def main():
    c = U.Pruefung("notluftpumpe")
    p = c.p
    c.koerper(["Pumpe", "Tuelle", "Rueckschlagventil", "Luftschlauch_1", "Luftschlauch_2", "Luftschlauch_3", "Luftschlauch_4", "Luftstein"])
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    f = next(x for x in soll["bauteile"] if x["id"] == "fish")["hoehen"]
    boden, rand, wsp = f["boden_ueber_fussboden_mm"], f["rand_ueber_fussboden_mm"], f["wsp_ueber_fussboden_mm"]
    c.eq("Pumpe steht auf Z 0 (Fussboden)", c.unten("Pumpe"), 0, 0.1)
    for i, (n, v) in enumerate((("Laenge", 210), ("Breite", 150), ("Hoehe", 170))):
        c.eq(f"Gehaeuse {n} {v}", c.ausdehnung("Pumpe", i), v, 0.1)
    c.eq(f"Luftstein-Unterkante {c.unten('Luftstein'):g} = Boden des Fischtanks {boden} + 20", c.unten("Luftstein"), boden + p["stein_ueber_boden"], 0.1)
    c.wahr(f"Luftstein-Oberkante {c.oben('Luftstein'):g} liegt unter dem Spiegel {wsp} (eingetaucht)", c.oben("Luftstein") < wsp)
    c.eq("Luftstein Ø 40", c.ausdehnung("Luftstein", 0), 40, 0.1)
    c.eq("Luftstein Hoehe 100", c.ausdehnung("Luftstein", 2), 100, 0.1)
    c.wahr(f"Schlauch-Hoechstpunkt {c.oben('Luftschlauch_2'):g} liegt ueber dem Rand {rand} + 50 (Siphonbrecher, Designprinzip 9)", c.oben("Luftschlauch_2") >= rand + 50)
    c.eq("Schlauch-Aussen-Ø 12", c.ausdehnung("Luftschlauch_1", 1), 12, 0.1)
    c.wahr("Schlauch endet auf dem Luftstein (Unterkante Schlauch = Oberkante Stein)", abs(c.unten("Luftschlauch_4") - c.oben("Luftstein")) < 0.2)
    c.eq("Tuelle sitzt an der Pumpenseite (x = Gehaeuse-Halblaenge 105)", c.B["Tuelle"]["bbox"]["min"][0], 105, 0.1)
    c.eq("Rueckschlagventil schliesst an die Tuelle an", c.B["Rueckschlagventil"]["bbox"]["min"][0], c.B["Tuelle"]["bbox"]["max"][0], 0.1)
    c.port("Luftausgang (Tuelle)", "Tuelle", (105 + p["tuelle_l"], 0, p["tuelle_z"]), (1, 0, 0))
    c.interferenz()
    print(f"INFO Luftmenge: Richtwert {p['luft_l_min']} l/min (R55), Quelle offen (A24); Spitzenbedarf 71 g O2/h aus R55, Deckung 24 bis 49 Prozent laut R55 Tabelle")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
