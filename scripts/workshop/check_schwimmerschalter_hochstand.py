"""Pruefung Schwimmerschalter Hochstand T105 (U2): Schaltpunkt (Schwimmermitte) im Ursprung = Hochstand -110 der Soll-Datei, Klemme liegt in der Aufnahme des sumpftank (Z -120 bis -40),
Kabel durch die Klemme, Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_schwimmerschalter_hochstand.py   (exit 1 bei FAIL)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U


def main():
    c = U.Pruefung("schwimmerschalter_hochstand")
    p = c.p
    c.koerper(["Schwimmer", "Kabelklemme", "Kabel"])
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    hoch = next(x for x in soll["bauteile"] if x["id"] == "sump_1")["hoehen"]["hochstand_ueber_fussboden_mm"]
    c.eq("Parameter Schaltpunkt = Soll sump_1 Hochstand -110", p["schaltpunkt"], hoch)
    c.eq("Schwimmer Ø 70 (x-Ausdehnung)", c.ausdehnung("Schwimmer", 0), 70, 0.1)
    c.eq("Schwimmermitte Z 0 (= Schaltpunkt)", c.mitte("Schwimmer", 2), 0, 0.1)
    c.eq("Klemme sitzt auf dem Schwimmer (Unterkante Z 35)", c.unten("Kabelklemme"), 35, 0.1)
    c.zylinder("Klemmenbohrung Ø 7 (Kabel)", "Kabelklemme", 3.5)
    c.eq("Kabel Ø 7", c.ausdehnung("Kabel", 0), 7, 0.1)
    c.eq("Kabelende Z 435 (Ausschnitt 400)", c.oben("Kabel"), 435, 0.1)
    c.port("Meldeleitung (Kabelende)", "Kabel", (0, 0, 435), (0, 0, 1))
    # Lage im Sumpf: Fussboden-Z = Bauteil-Z + Schaltpunkt; Halter des sumpftank (Z -120 bis -40) muss die Klemme umfassen und den Hochstand
    sp = json.load(open(os.path.join(sc.ROOT, "data", "components", "sumpftank.json"), encoding="utf-8"))["parameter"]
    h0, h1 = sp["halter_z"]["wert"] - 40, sp["halter_z"]["wert"] + 40
    k0, k1 = c.unten("Kabelklemme") + hoch, c.oben("Kabelklemme") + hoch
    c.wahr(f"Klemme im Sumpf Z {k0:g} bis {k1:g} liegt in der Halter-Aufnahme Z {h0:g} bis {h1:g}", h0 <= k0 and k1 <= h1)
    c.wahr("Hochstand -110 liegt ueber dem Soll-Pegel -250 und unter dem Zulauf -75 (Sumpftank-Hoehen)", sp["wsp"]["wert"] < hoch < sp["tuelle_z"]["wert"])
    c.wahr("Wiedereinschaltpunkt -180 liegt unter dem Hochstand und ueber dem Soll-Pegel -250 (D105)", sp["wsp"]["wert"] < p["wiederein"] < hoch)
    c.interferenz()
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
