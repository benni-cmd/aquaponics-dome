"""Pruefung Sumpftank T101 (U2): Koerperzahl, Masse der Grube gegen data/oasis-soll.json (sump_1), Wasserkoerper-Hoehe und Inhalt, vier Pufferzonen zu 212 mm
mit Fluss auf/ab, Hochstand-Aufnahme, Zulaeufe oben ID25, Deckel Oberkante 0, kein Bodenablauf, Interferenz 0. Erwartungen aus Quelle/Soll-Datei und Rechnung, nicht aus dem Generator.
Aufruf: python -X utf8 scripts/workshop/check_sumpftank.py   (exit 1 bei FAIL)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import u2_lib as U
import sumpftank as G


def main():
    c = U.Pruefung("sumpftank")
    p = c.p
    soll = json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
    s = next(x for x in soll["bauteile"] if x["id"] == "sump_1")["hoehen"]
    c.koerper(["Sumpf_Wanne", "Sumpf_Folie", "Wasser", "Trennwand_1", "Trennwand_2", "Trennwand_3", "Trennwand_4", "Pumpensockel", "Zulauf_1", "Zulauf_2", "Zulauf_3",
               "Schwimmerhalter", "Deckel_1", "Deckel_2", "Deckel_3", "Zonenschild_1", "Zonenschild_2", "Zonenschild_3", "Zonenschild_4"])
    # --- Hoehen gegen die Quelle (Fussboden-Bezug; Modell-Z = 400 + Z)
    c.eq("Parameter Boden = Soll sump_1 boden_ueber_fussboden_mm", -p["pit_d"], s["boden_ueber_fussboden_mm"])
    c.eq("Parameter Soll-Pegel = Soll wsp_ueber_fussboden_mm", p["wsp"], s["wsp_ueber_fussboden_mm"])
    c.eq("Parameter Hochstand = Soll hochstand_ueber_fussboden_mm", p["hochstand"], s["hochstand_ueber_fussboden_mm"])
    c.eq("Wasserkoerper Unterkante = Boden -500", c.unten("Wasser"), s["boden_ueber_fussboden_mm"], 0.1)
    c.eq("Wasserkoerper Oberkante = Soll-Pegel -250 (Modell-Z 150)", c.oben("Wasser"), s["wsp_ueber_fussboden_mm"], 0.1)
    d1 = c.oben("Deckel_1")
    c.eq("Deckel Oberkante = Rand 0 (Fussboden, A18)", d1, s["rand_ueber_fussboden_mm"], 0.1)
    c.eq("Deckel Dicke 40", c.ausdehnung("Deckel_1", 2), 40, 0.1)
    # --- Grubenmasse (innen = Wasserkoerper-Querschnitt) und Wanne aussen
    c.eq("Grube innen Breite X 1125 (Quelle A22)", c.ausdehnung("Wasser", 0), 1125, 0.1)
    c.eq("Grube innen Laenge Y 2975 (Quelle A22)", c.ausdehnung("Wasser", 1), 2975, 0.1)
    c.eq("Wanne aussen X = 1125 + 2 x (Folie 2 + Wand 100) = 1329", c.ausdehnung("Sumpf_Wanne", 0), 1329, 0.1)
    c.eq("Wanne aussen Y = 2975 + 204 = 3179", c.ausdehnung("Sumpf_Wanne", 1), 3179, 0.1)
    c.eq("Wannenboden -602 (Boden -500, Folie 2, Beton 100)", c.unten("Sumpf_Wanne"), -602, 0.1)
    # --- Inhalt: Rechnung aus Parametern gegen Messung; Soll 850 l, Gesamt bis Rand 1680 l
    abzug = sum((10 * 1125 * (G.wand_z(p, k)[1] - G.wand_z(p, k)[0] if G.wand_z(p, k)[1] <= p["wsp"] else p["wsp"] - G.wand_z(p, k)[0])) for k in range(4)) + 400 * 400 * p["sockel_h"]
    soll_l = (1125 * 2975 * 250 - abzug) / 1e6
    ist_l = c.B["Wasser"]["volume_mm3"] / 1e6
    c.eq(f"Wasserinhalt {ist_l:.1f} l = Rechnung aus Parametern {soll_l:.1f} l", ist_l, soll_l, 0.5)
    c.eq(f"Wasserinhalt {ist_l:.0f} l gegen Soll 850 l (Quelle): innerhalb 5 Prozent", 1 if abs(ist_l - 850) <= 42.5 else 0, 1)
    c.eq("Gesamtinhalt bis Rand 1125 x 2975 x 500 = 1673 l gegen Quelle 1680 l (+-1 Prozent)", 1 if abs(1125 * 2975 * 500 / 1e6 - 1680) <= 16.8 else 0, 1)
    # --- vier Pufferzonen zu 212 mm, Fluss auf/ab
    ws = [c.B[f"Trennwand_{k}"]["bbox"] for k in range(1, 5)]
    for k in range(3):
        c.eq(f"Zone {k + 1}: lichte Breite zwischen Wand {k + 1} und {k + 2} = 212", ws[k + 1]["min"][1] - ws[k]["max"][1], 212, 0.1)
    c.eq("Zone 4: lichte Breite bis zur Grubenwand (+Y) = 212", 2975 / 2 - ws[3]["max"][1], 212, 0.1)
    c.eq("Hauptkammer Laenge = 2975 - 4 x 212 - 4 x 10 = 2087", ws[0]["min"][1] - (-2975 / 2), 2087, 0.1)
    for k in (1, 3):    # bodenoffen: Zone 1 und 3 werden von unten durchstroemt (aufwaerts)
        c.eq(f"Wand {k}: Oeffnung am Boden 80 (Unterkante -420), Oberkante {p['trenn_oben']} ueber Hochstand", c.unten(f"Trennwand_{k}"), -420, 0.1)
        c.wahr(f"Wand {k}: Oberkante {c.oben(f'Trennwand_{k}'):g} liegt ueber dem Hochstand -110 (Wasser kann nicht ueber die Wand)", c.oben(f"Trennwand_{k}") > p["hochstand"])
    for k in (2, 4):    # Wehr: Wasser laeuft oben hinein und unten in der naechsten Zone ab (abwaerts)
        c.eq(f"Wand {k}: Wehr auf dem Boden (Unterkante -500)", c.unten(f"Trennwand_{k}"), -500, 0.1)
        c.wahr(f"Wand {k}: Wehr-Oberkante {c.oben(f'Trennwand_{k}'):g} unter dem Soll-Pegel -250 (ueberstroemt)", c.oben(f"Trennwand_{k}") < p["wsp"])
    # --- Zulaeufe oben, Pumpenplatz, Hochstand-Aufnahme
    for i in (1, 2, 3):
        z = c.mitte(f"Zulauf_{i}", 2)
        c.wahr(f"Zulauf {i}: Achse Z {z:g} ueber dem Hochstand -110 und unter dem Deckel -40", p["hochstand"] < z < -40)
        c.eq(f"Zulauf {i}: Aussen-Ø 32", c.ausdehnung(f"Zulauf_{i}", 2), 32, 0.1)
        c.zylinder(f"Zulauf {i} Bohrung ID25 (D106)", f"Zulauf_{i}", 12.5)
    c.wahr("Schwimmerhalter umfasst den Hochstand -110", c.unten("Schwimmerhalter") <= -110 <= c.oben("Schwimmerhalter"))
    c.eq("Pumpensockel steht auf dem Boden (Unterkante -500)", c.unten("Pumpensockel"), -500, 0.1)
    c.wahr("Pumpensockel liegt in der Hauptkammer (y unter Wand 1)", c.B["Pumpensockel"]["bbox"]["max"][1] < ws[0]["min"][1])
    # --- kein Bodenablauf: keine Zylinderflaeche mit senkrechter Achse an Wanne und Folie
    for k in ("Sumpf_Wanne", "Sumpf_Folie"):
        senk = [f for f in sc.faces(c.path, k) if f.get("cylinder") and abs(f["cylinder"]["axis"][2]) > 0.99]
        c.eq(f"{k}: keine senkrechte Bohrung im Boden (kein Bodenablauf, Designprinzip 2)", len(senk), 0)
    c.wahr("Zonenschilder liegen auf dem Deckel (Unterkante 0)", abs(c.unten("Zonenschild_1")) < 0.1)
    c.interferenz()
    mn, mx = sc.bbox_all(c.ev)
    print(f"INFO Box X {mn[0]:.0f} bis {mx[0]:.0f}, Z {mn[2]:.0f} bis {mx[2]:.0f}; Modell-Z = 400 + Z: Boden {400 - 500}, Soll-Pegel 150, Rand 400")
    print("INFO Deckel im Modell als Vollplatte (396 kg je Platte); reales Gitterrost 30/10 rund 35 kg [A]")
    return c.fertig()


if __name__ == "__main__":
    sys.exit(main())
