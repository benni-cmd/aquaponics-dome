"""Pruefung Nachspeise-Ventil T108 (U2): zwei Ventile (Regen, Frisch) je 5 Koerper, Ports A (y 0) und B (y 120) als Muffe d25, Rohrachse = Rand - Spiegel + 60 aus data/oasis-soll.json (fish),
Kugelmitte Regenwasser 20 ueber dem Spiegel, Frischwasser 30 mm tiefer (Regenwasser zuerst), Kugeln ohne Beruehrung, Interferenz 0. Aufruf: python -X utf8 scripts/workshop/check_nachspeise_ventil.py   (exit 1 bei FAIL)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U
import leitung as L


def main():
    c = U.Pruefung("nachspeise_ventil")
    p = c.p
    namen = [f"{n}_{s}" for s in ("regen", "frisch") for n in ("Uebergang", "Ventilgehaeuse", "Wange_L", "Wange_R", "Hebelarm_mit_Kugel")]
    c.koerper(namen)
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    f = next(x for x in soll["bauteile"] if x["id"] == "fish")["hoehen"]
    rand, wsp = f["rand_ueber_fussboden_mm"], f["wsp_ueber_fussboden_mm"]
    c.eq(f"Parameter Spiegel {p['spiegel']} = Soll fish Wsp {wsp}", p["spiegel"], wsp)
    c.eq(f"Rohrachse ueber dem Spiegel: Rand {rand} - Wsp {wsp} + 60 = {rand - wsp + 60}", p["ventil_h"], rand - wsp + 60)
    of = L.od_f(25)
    for s, y in (("regen", 0), ("frisch", p["abstand_y"])):
        c.eq(f"Uebergang {s}: Aussen-Ø = Formstueck d25 (32,25)", c.ausdehnung(f"Uebergang_{s}", 1), of, 0.1)
        c.eq(f"Ventilgehaeuse {s}: Ø 38", c.ausdehnung(f"Ventilgehaeuse_{s}", 1), 38, 0.1)
        c.eq(f"Ventilgehaeuse {s}: Laenge 80", c.ausdehnung(f"Ventilgehaeuse_{s}", 0), 80, 0.1)
        c.port(f"{'A Regenwasser' if s == 'regen' else 'B Frischwasser'} (Muffe d25)", f"Uebergang_{s}", (0, y, 0), (-1, 0, 0))
        c.zylinder(f"Muffe {s} d25", f"Uebergang_{s}", 12.5)
    # Kugeln: Mitte = Unterkante + 55; Regen 20 ueber dem Spiegel, Frisch 30 mm tiefer
    zr = c.unten("Hebelarm_mit_Kugel_regen") + p["kugel_d"] / 2
    zf = c.unten("Hebelarm_mit_Kugel_frisch") + p["kugel_d"] / 2
    c.eq(f"Regenwasser-Kugelmitte {zr:g} = Spiegel + 20 (Achse - 510 + 20)", zr, -p["ventil_h"] + p["kugel_auf"], 0.5)
    c.eq(f"Frischwasser-Kugel haengt {zr - zf:g} mm tiefer (Staffelung 30: Regenwasser zuerst)", zr - zf, p["staffel"], 0.5)
    c.wahr("Regenwasser-Kugel haengt hoeher als die Frischwasser-Kugel (Regen oeffnet zuerst)", zr > zf)
    ky_r = c.mitte("Hebelarm_mit_Kugel_regen", 1); ky_f = c.mitte("Hebelarm_mit_Kugel_frisch", 1)
    c.wahr(f"Kugeln ohne Beruehrung: Achsabstand {ky_f - ky_r:g} > Kugel-Ø {p['kugel_d']}", ky_f - ky_r > p["kugel_d"])
    mn, mx = sc.bbox_all(c.ev)
    c.eq(f"Gesamt-Box Y {mn[1]:.0f} bis {mx[1]:.0f}: Breite = Achsabstand + Kugel-Ø", mx[1] - mn[1], p["abstand_y"] + p["kugel_d"], 0.5)
    print(f"INFO Einbau: Spiegel {p['ventil_h']} mm unter der Rohrachse; Rohrachse Modell-Z {400 + wsp + p['ventil_h']} (Spiegel Modell-Z {400 + wsp}, D94: Fussboden Z 400)")
    c.interferenz()
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
