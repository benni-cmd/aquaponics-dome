"""Pruefung Venturi-Belueffter T104 (U2): Koerperzahl, Muffen d50 (Ports, Tiefe 31), Gesamtlaenge, Luftstrang oben (Lufteinlass ueber dem Fischtank-Spiegel), Bohrungen, Interferenz 0;
Hydraulik als INFO gegen R60/R59 (Antriebsdruck und Durchsatz bleiben offen, kein PASS erfunden). Erwartungen aus Quelle/Rechnung, nicht aus dem Generator.
Aufruf: python -X utf8 scripts/workshop/check_venturi_belueffter.py   (exit 1 bei FAIL)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U
import leitung as L


def main():
    c = U.Pruefung("venturi_belueffter")
    p = c.p
    c.koerper(["Muffe_Ein", "Injektor", "Muffe_Aus", "Saugstutzen", "Rueckschlagventil", "Luftfilter"])
    of, t = L.od_f(50), L.DEPTH[50]
    c.eq("Muffe Eintritt: Aussen-Ø = Formstueck d50 (58,5)", c.ausdehnung("Muffe_Ein", 1), of, 0.1)
    c.eq("Muffe Austritt: Aussen-Ø = Formstueck d50", c.ausdehnung("Muffe_Aus", 1), of, 0.1)
    c.zylinder("Muffe Eintritt Tasche d50", "Muffe_Ein", 25)
    c.zylinder("Muffe Austritt Tasche d50", "Muffe_Aus", 25)
    c.port("A Eintritt (Muffe d50)", "Muffe_Ein", (0, 0, 0), (-1, 0, 0))
    ende = 2 * p["muffe_l"] + p["inj_l"]
    c.port("B Austritt (Muffe d50)", "Muffe_Aus", (ende, 0, 0), (1, 0, 0))
    mn = min(b["bbox"]["min"][0] for b in c.B.values()); mx = max(b["bbox"]["max"][0] for b in c.B.values())
    c.eq(f"Gesamtlaenge Port A bis Port B = {ende:g} (2 x Muffe 60 + Injektor 150)", mx - mn, ende, 0.1)
    c.eq("Injektorkoerper Ø 64 x 150", c.ausdehnung("Injektor", 1), 64, 0.1)
    c.eq("Injektor Laenge 150", c.ausdehnung("Injektor", 0), 150, 0.1)
    c.zylinder("Injektor Durchgang Ø 36", "Injektor", 18)
    c.eq("Luftstrang mittig ueber dem Injektor (x 135)", c.mitte("Luftfilter", 0), p["muffe_l"] + p["inj_l"] / 2, 0.1)
    c.eq("Stapel Injektor-Stutzen-Ventil-Filter lueckenlos: Stutzen-Unterkante = Injektor-Oberseite", c.unten("Saugstutzen"), 32, 0.1)
    c.eq("Rueckschlagventil sitzt auf dem Stutzen", c.unten("Rueckschlagventil"), c.oben("Saugstutzen"), 0.1)
    c.eq("Luftfilter sitzt auf dem Rueckschlagventil", c.unten("Luftfilter"), c.oben("Rueckschlagventil"), 0.1)
    c.zylinder("Luftweg Ø 8 im Ansaugstutzen", "Saugstutzen", 4)
    # Hoehe gegen Spiegel: Lufteinlass (Filter-Oberkante) liegt ueber der Rohrachse, Achse 500 ueber dem Spiegel
    c.wahr(f"Lufteinlass Z {c.oben('Luftfilter'):g} ueber der Rohrachse; mit Achse {p['achse_ueber_spiegel']} mm ueber dem Spiegel liegt er {p['achse_ueber_spiegel'] + c.oben('Luftfilter'):g} mm ueber dem Wasser", c.oben("Luftfilter") > 0 and p["achse_ueber_spiegel"] > 0)
    c.interferenz()
    # Hydraulik: nur Rechnung, keine Bestaetigung (offen)
    h_max_bar = (3.3, 4.1)
    print(f"INFO Antriebsdruck: Mazzei 1583 braucht >= 10 psi = {10 * 0.0689476:.2f} bar Differenz (R60 Tabelle, 55 l/min); tauchpumpe_modul Hmax 3,3 bis 4,1 m = {h_max_bar[0] * 0.0981:.2f} bis {h_max_bar[1] * 0.0981:.2f} bar bei null Foerderung -> nicht belegt, offen (Rechnung: python -X utf8 -I -c \"print(10*0.0689476, 3.3*0.0981, 4.1*0.0981)\")")
    print(f"INFO Durchsatz: Soll {p['durchfluss_l_min']} l/min je Linie gegen 55 l/min Tabellenwert 1583 bei 10 psi -> Faktor {p['durchfluss_l_min'] / 55:.1f}, offen")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
