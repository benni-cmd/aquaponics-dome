"""Pruefung Tauchpumpen-Modul T110 (U2): Koerperzahl, Fussabdruck Ø 275 (Zeichnung), Rueckschlagventil d50 mit Port oben, Hub je Pumpstelle aus data/oasis-soll.json, Eintauchtiefe gegen 4 m (R59),
Kennlinien-Rechnung aus Qmax/Hmax (nur Rechnung, Nachweis offen), Sumpf-Ueberflutung, Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_tauchpumpe_modul.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U
import leitung as L


def reibung_m(q_l_min, laenge_m, di_mm=45.2, c_hw=150):
    """Hazen-Williams: Druckhoehe in m fuer Rohr d50 PVC-U (Innen 45,2)."""
    q = q_l_min / 60000
    return 10.67 * laenge_m * q ** 1.852 / (c_hw ** 1.852 * (di_mm / 1000) ** 4.87)


def kennlinie(q_max, h_max, h):
    x = h / h_max
    if x >= 1:
        return 0.0, 0.0, 0.0
    return q_max * (1 - x), q_max * (1 - x * x), q_max * math.sqrt(1 - x * x)      # linear, Parabel, Ellipse (wie R59)


def main():
    c = U.Pruefung("tauchpumpe_modul")
    p = c.p
    c.koerper(["Ansaugkorb", "Gehaeuse", "Druckstutzen", "Rueckschlagventil", "Kabel"])
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    b = {x["id"]: x["hoehen"] for x in soll["bauteile"] if x["id"] in ("fish", "vortex_1", "sump_1")}
    c.eq("Fussabdruck Ø 275 = Zeichnung Pumpe Radius 137,5", c.ausdehnung("Ansaugkorb", 0), 275, 0.1)
    c.eq("Standflaeche Z 0", c.unten("Ansaugkorb"), 0, 0.1)
    c.eq("Gehaeuse Ø 230", c.ausdehnung("Gehaeuse", 0), 230, 0.1)
    c.eq("Gehaeuse-Oberkante Z 240", c.oben("Gehaeuse"), 240, 0.1)
    c.eq("Druckstutzen Ø 50", c.ausdehnung("Druckstutzen", 0), 50, 0.1)
    t = L.DEPTH[50]
    c.eq(f"Stutzen steckt {t} mm im Rueckschlagventil (Ventil-Unterkante = Stutzen-Oberkante - {t})", c.unten("Rueckschlagventil"), c.oben("Druckstutzen") - t, 0.1)
    c.eq("Rueckschlagventil Ø 63", c.ausdehnung("Rueckschlagventil", 0), 63, 0.1)
    c.zylinder("Ventil Muffe oben d50", "Rueckschlagventil", 25)
    top = c.oben("Rueckschlagventil")
    c.port("Druckleitung (Muffe d50, oben)", "Rueckschlagventil", (0, 0, top), (0, 0, 1))
    c.eq("Rueckschlagventil in der Druckleitung: Oberkante Z 389", top, 389, 0.1)
    # Hub je Pumpstelle aus der Soll-Datei
    h1 = (b["vortex_1"]["wsp_ueber_fussboden_mm"] - b["fish"]["wsp_ueber_fussboden_mm"]) / 1000
    h2 = (b["fish"]["wsp_ueber_fussboden_mm"] - b["sump_1"]["wsp_ueber_fussboden_mm"]) / 1000
    c.eq("Hub Pumpstelle 1 = Vortex 1900 - Fischtank 750 = 1,15 m", h1, 1.15, 1e-9)
    c.eq("Hub Pumpstelle 2 = Fischtank 750 - Sumpf -250 = 1,00 m", h2, 1.00, 1e-9)
    # Eintauchtiefe gegen 4 m (R59 Handbuch)
    tiefe_fisch = b["fish"]["wsp_ueber_fussboden_mm"] - b["fish"]["boden_ueber_fussboden_mm"]
    c.wahr(f"Eintauchtiefe im Fischtank {tiefe_fisch} mm <= {p['tiefe_max_mm']} mm (R59: wasserdicht bis 4 m)", tiefe_fisch <= p["tiefe_max_mm"])
    c.interferenz()
    # Rechnung (kein PASS erfunden): Foerderleistung aus Qmax/Hmax gegen Soll 110 l/min je Linie
    q_soll = 110
    hf = reibung_m(q_soll, 6.0)
    hz = 3.0 * (q_soll / 60000 / (math.pi * 0.0452 ** 2 / 4)) ** 2 / (2 * 9.81)
    print(f"INFO Rechnung Reibung d50, 110 l/min, 6 m Rohr [A]: {hf:.2f} m (Hazen-Williams C 150), Einzelverluste Zeta 3,0 [A]: {hz:.2f} m")
    for nm, hstat, extra, txt in (("Pumpstelle 1 (Fischtank -> Vortex)", h1, 0.0, ""), ("Pumpstelle 2 ohne Venturi (Sumpf -> Fischtank)", h2, 0.0, ""),
                                  ("Pumpstelle 2 mit Venturi 3,5 m gesamt (Quelle A19, Annahme)", 0, 3.5, ""), ("Pumpstelle 2 mit Mazzei 1583 bei 10 psi (R60)", h2, 10 * 0.70307, "")):
        H = (hstat + hf + hz) if not extra else (extra if "3,5" in nm else hstat + hf + hz + extra)
        ql, qp, qe = kennlinie(p["qmax_l_min"], p["hmax_m"], H)
        print(f"INFO {nm}: Foerderhoehe {H:.2f} m -> Q linear {ql:.0f} / Parabel {qp:.0f} / Ellipse {qe:.0f} l/min gegen Soll {q_soll} (Qmax {p['qmax_l_min']}, Hmax {p['hmax_m']} m, R59)")
    print("INFO Ergebnis: nur die optimistischen Formen erreichen 110 l/min an Pumpstelle 1; mit Venturi (3,5 m) und erst recht mit Mazzei 10 psi (7 m) reicht Hmax 4,1 m nicht -> Nachweis offen, Rechnung: python -X utf8 scripts/workshop/check_tauchpumpe_modul.py")
    # Sumpf: Ueberflutung bei Soll-Pegel (Pumpe auf Sockel 30)
    wassertiefe_sumpf = b["sump_1"]["wsp_ueber_fussboden_mm"] - b["sump_1"]["boden_ueber_fussboden_mm"]
    sockel = json.load(open(os.path.join(sc.ROOT, "data", "components", "sumpftank.json"), encoding="utf-8"))["parameter"]["sockel_h"]["wert"]
    ueber = c.oben("Gehaeuse") + sockel - wassertiefe_sumpf
    print(f"{'WARN' if ueber > 0 else 'INFO'} Sumpf: Wasser {wassertiefe_sumpf} mm ueber dem Boden, Gehaeuse-Oberkante auf dem Sockel {c.oben('Gehaeuse') + sockel:g} mm -> {'ragt ' + format(ueber, 'g') + ' mm aus dem Wasser (Trockenlaufschutz noetig, flachere Pumpe oder Sockel anpassen, offen)' if ueber > 0 else 'ganz untergetaucht'}")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
