"""Blatt-Text fuer data/components/tank.json (Ports, Gewichte, Stueckliste, Herkunft) aus den Parametern berechnet."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
sys.path.insert(0, os.path.dirname(__file__))
import tank as tk
p = os.path.join(sc.ROOT, "data", "components", "tank.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
ports, gew, sl, legs = [], [], [], []
for typ, T in d["typen"].items():
    G = tk.geometry(T, P)
    R, w, z0, H = T["R"] - P["rim_w"], T["wall"], T["z0"], T["H"]            # R = Koerperradius
    z_top = z0 + H
    di = T["inlet_d"]
    xin = R - w - di / 2
    yin = math.sqrt(R ** 2 - xin ** 2)
    z_in = z_top - P["inlet_below_top"]
    nm = "Vortex-Absetzer" if not T["biofilter"] else "Biofilter"
    ports.append([f"{typ}: Zulauf tangential (Rohr d{di:.0f})", f"Rohr PVC-U d{di:.0f} (etwa DN{di - 10:.0f}), Wand 3", f"x {xin:.1f}, y {-yin - 220:.0f}, z {z_in:.0f} (Rohrachse parallel Y, Rohrende aussen)", "Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall)"])
    if not T["biofilter"]:
        ports.append([f"{typ}: Auslauf am Leitrohr", "Rohr d50 (etwa DN40), Leitrohr d110", f"x {P['guide_d'] / 2 + 140:.0f}, y 0, z {z_top + P['lid_t'] + 35:.0f}", "Wasser verlaesst den Absetzer nach +X (Oeffnung zeigt +X)"])
    else:
        ports.append([f"{typ}: Ueberlauf (Auslauf)", "Rohr d63 (etwa DN50), 80 mm unter dem Rand", f"x {R + 130:.0f}, y 0, z {z_top - 80:.0f}", "Wasser verlaesst den Biofilter nach +X (Oeffnung zeigt +X)"])
        ports.append([f"{typ}: Belueftungsanschluss im Deckel", "Rohr d16 (Luftschlauch 16 mm)", f"x {R / 2:.0f}, y 0, z {z_top + P['lid_t']:.0f}", "Luft tritt ein, Oeffnung zeigt +Z"])
    zv = z0 - 12 - P["valve_len"] - 40
    ports.append([f"{typ}: Schlammablass (Kugelhahn an der Kegelspitze)", f"Kugelhahn d{T['valve_d']}, Ablaufstutzen d{T['valve_d']} (Verschraubung)", f"x 0, y 0, z {zv:.0f} (Stutzenende); Kegelspitze z {z0}", "Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X"])
    lx, ly = T["plat_l"] / 2 - T["leg_w"] / 2, T["plat_w"] / 2 - T["leg_w"] / 2
    ports.append([f"{typ}: Fussplatten-Anker (4 Fuesse, je 2 x M8)", "M8, Loch D9, Platte 100 x 100 x 6", f"x +-{lx:.0f}, y +-{ly:.0f}, z {P['foot_t']:.0f} (Diagonalversatz +-35)", "Befestigung auf Boden/Betonpunkt, Richtung -Z"])
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"tank_{typ}.sc"))
    sep = ["Biomedium"] if T["biofilter"] else []
    leer = sum(b["mass_g"] for b in ev["bodies"] if not any(b["name"].startswith(x) for x in sep)) / 1000
    bio = sum(b["mass_g"] for b in ev["bodies"] if any(b["name"].startswith(x) for x in sep)) / 1000
    Ri = R - w
    cyl = math.pi * Ri ** 2 * (z_top - G["z_c"]) / 1e6
    cone = math.pi * Ri ** 2 * (G["z_c"] - G["z_t"]) / 3 / 1e6
    vol = cyl + cone
    gew.append(f"{typ}: leer {leer:.0f} kg" + (f" (ohne Biomedium {bio:.0f} kg)" if bio else "") + f"; Wasserfuellung bis Rand {vol:.0f} l = {vol:.0f} kg (Zylinder {cyl:.0f} l + Kegel {cone:.0f} l); gefuellt gesamt {leer + bio + vol:.0f} kg [E]")
    legs.append(f"{typ}: Beine 4 x {T['leg_w']}x{T['leg_w']}x{T['leg_wall']} Laenge {T['leg_h'] - P['foot_t']:.0f}; Plattform {T['plat_l']}x{T['plat_w']}x{T['plat_t']} Blech 4 mm hohl mit Kegelsitz")
    sl.append(f"{typ} (Stueck je Tank): Tank PE ({T['wall']} mm Wand, Aussen-D{2 * (R + P['rim_w']):.0f} x H{H}, Randwulst) 1; Deckel 1; Zulaufrohr d{di:.0f} 1; " + ("Leitrohr d110 x 420 mit Auslauf d50 1; " if not T["biofilter"] else "Ueberlauf d63 1, Biomediumkorb mit Tragrost 1, Belueftungsrohr d16 1; ") + f"Kugelhahn d{T['valve_d']} mit 2 Stutzen 1; Plattform 1; Beine {T['leg_w']}x{T['leg_w']} 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 + Mutter nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30")
bl = {
    "funktion": "Tank mit Kegelboden: klein = Vortex-Absetzer (tangentialer Zulauf, Leitrohr, Schlamm sinkt zur Spitze und wird dort abgelassen), gross = Biofilter (Biomediumkorb auf Tragrost, Belueftung, Ueberlauf, Schlammablass); steht auf Plattform und 4 Beinen.",
    "querschnitt": "Tank PE: Zylinder (Koerper D633/D890) ueber Kegel (ca. 47 Grad ab Horizontal, Spitze mit Stutzen D44/D56); gerollter Randwulst 20 x 30 mm (Aussendurchmesser D673/D930 laut OBJ); Wand 4/5 mm; Deckel 6 mm mit 8 mm Ueberstand. Plattform: Blechkasten 4 mm, innen hohl, Kegelsitz 2 mm Spiel, Eckenaussparungen fuer die Beine; Beine Rechteckrohr verzinkt; vier Querstreben auf Hoehe 250/300 und vier Diagonalen.",
    "toleranzen": "Kegelsitz in der Plattform 2 mm Spiel; Zulaufrohr beruehrt die Innenwand tangential (Pruefung +-0,5 mm); Tankhoehe und Kegelspitze +-1 mm gegen layout.json.",
    "ports": ports,
    "verbindungen": ["Tank sitzt mit dem Kegel im Kegelsitz der Plattform (Kegel-Zylinder-Uebergang auf der Plattform-Oberkante), Haltegurt/Schellen nicht modelliert [A]", "Beine laufen durch Eckenaussparungen der Plattform, geschweisst (MAG), danach verzinkt [A]", "Fussplatten: je 2 Schrauben M8x30 (hex_bolt), Loch D9", "Rohre PVC-U (DIN 8062/EN 1452) mit Bulkhead-Durchfuehrung und Dichtung durch die Tankwand [A, im Modell nur Durchbruch + Rohr]", "Schlammventil: Kugelhahn PVC-U mit Verschraubung an Stutzen d40/d55"],
    "abweichung": "layout.json tanks: Durchmesser, Hoehe, Kegelspitze Z, Plattform (Mass und Z), Beinhoehe stimmen (Pruefung check_tank.py). Kegel: OBJ liefert nur Spitze Z 172/226 und Gesamthoehe; das Ende des Kegels ist Annahme A (Plattform-Oberkante -> 45 Grad ab Horizontal, Absetzer-Praxis); Alternative laut R09-Auslegung: Kegelende an der Plattform-Unterkante (256 mm hoch, 37 Grad ab Horizontal / Halbwinkel 53 Grad) -> zu flach fuer Schlamm. Beine 751/1008 laufen bis ueber die Plattform (OBJ-Mass). Fittings: OBJ 4 Stueck Z 143-177, hier Schlammstutzen + Kugelhahn + Ablaufstutzen.",
    "montage": ["Plattform mit Beinen am Boden ausrichten, Fussplatten mit M8 verschrauben, Streben und Diagonalen einsetzen", "Tank in den Kegelsitz setzen (zu zweit), Deckel und Leitrohr bzw. Biomediumkorb einsetzen", "Zulauf-Rohr tangential und Auslauf/Ueberlauf durch die Wand fuehren, Dichtungen setzen", "Kugelhahn mit Verschraubung an den Kegelstutzen, Ablaufrohr anschliessen", "Dichtheit pruefen (Wasserprobe), Biomedium und Belueftung einbauen (gross)"],
    "werkzeug": "Lochsaege (d63/d50), Bohrer, Schluessel M6/M8, Wasserwaage, Schweissgeraet (Rahmen) oder Winkelverbinder",
    "stueckliste": sl + ["Tanks gesamt: klein 2, gross 2 (Azimute 123/213 und 108/229, layout.json)"],
    "lokal": "Tank: handelsueblicher Konus-Boden-Tank (Kunststoff, 500-1000 l); Plattform/Beine aus Baustahl-Rechteckrohr (Metallbauer) oder Alu-Systemprofil; Rohre und Kugelhaehne PVC-U aus dem Sanitaerhandel.",
    "referenz": "reference/ref-4-dome-clean.jpg und ref-5 (gruene Tanks auf duennen Beinen mit Kegelboden); data/layout.json tanks; docs/research/R09.md",
    "varianten": ["tank_klein", "tank_gross"],
    "gewicht_gefuellt": " | ".join(gew),
    "massen_getrennt": ["Biomedium"],
    "pruefung": ["scripts/workshop/check_tank.py (Ergebnis renders/components/tank_klein/check.txt)", "Triage in docs/workshop-log.md"],
    "offen": ["Kegelende (Plattform-Oberkante vs. -Unterkante) und Kegelwinkel: nur Annahme, R09 Konfidenz niedrig", "Rohrmasse (Zulauf d50/d63, Leitrohr d110, Auslauf d50/d63, Wand 3 mm) ohne Quelle (R09)", "Beine 751/1008 bis ueber die Plattform: Zweck (Tankfuehrung) aus OBJ nicht ableitbar", "Haltegurt/Schellen, Dichtungen, Verschraubungen der Diagonalen (M6x40) nicht modelliert", "Biofilter: Biomediumkorb und Belueftung als Platzhalter, keine Quelle zur Auslegung (R09)", "Rolle der Pumpen/Filtermodule (eigene Klasse pumpe)"],
}
d["blatt"] = bl
d["herkunft_tabelle"] = [
    ["Tankdurchmesser 673 / 930", "673 / 930 mm", "OBJ", "layout.json tanks d (Tank 1/4 und 2/3)", "hoch"],
    ["Tankhoehe 1075 / 1444 (inkl. Kegel)", "1075 / 1444 mm", "OBJ", "layout.json tanks h", "hoch"],
    ["Kegelspitze Z 172 / 226", "172 / 226 mm", "OBJ", "layout.json tanks z0 (167-172, 226-229)", "hoch"],
    ["Plattform 706x707x73 auf Z 428 / 977x976x98 auf Z 570", "mm", "OBJ", "layout.json tanks platform", "hoch"],
    ["Beine 4 x 30x30xh751 / 40x40xh1008", "mm", "OBJ", "layout.json tanks legs; Querschnitt aus oasis-obj-analysis", "hoch"],
    ["Kegel 45 Grad ab Horizontal, endet auf der Plattform-Oberkante", "45 Grad", "A", "OBJ liefert nur Spitze und Gesamthoehe; Scope-Card 45-60 Grad; Absetzer-Praxis; Alternative Unterkante = 37 Grad (R09-Auslegung)", "niedrig"],
    ["Tankwand 4 / 5 mm, Deckel 6 mm", "4 / 5 / 6 mm", "A", "PE-Tank Wanddicke; OBJ nur Huelle", "niedrig"],
    ["Zulauf tangential d50 / d63, 250 mm unter dem Rand", "d50 / d63", "R09 + A", "R09: tangentialer Zulauf, DN50 oben (Konfidenz niedrig); Masse A", "niedrig"],
    ["Leitrohr d110 x 420 mit Auslauf d50 (klein)", "d110 / d50", "R09 + A", "R09: Leitrohr D110, Auslass oben seitlich DN50; Tiefe A", "niedrig"],
    ["Schlammventil Kugelhahn d40 / d55 an der Kegelspitze", "d40 / d55", "OBJ + R09", "layout.json tanks fittings (Groessen 30-56 an der Spitze); R09: Schlammablass Bulkhead 32-40 mit Hahn", "mittel"],
    ["Biofilter: Biomediumkorb (EIN Koerper) auf Tragrost, Belueftung d16, Ueberlauf d63", "-", "A", "Scope-Card tank_gross: Platzhalter; keine Quelle (R09)", "niedrig"],
    ["Plattform als Blechkasten 4 mm, hohl, mit Kegelsitz und Eckenaussparungen", "4 mm", "A", "OBJ-Plattform 73/98 mm dick (massiv unwahrscheinlich); Konstruktionsannahme", "niedrig"],
    ["Querstreben auf Hoehe 250 / 300, 4 Diagonalen 25x3", "250 / 300 mm", "Bild + A", "ref-4/ref-5: Tanks auf Beinen mit Diagonalstreben (Scope-Card: Diagonalen)", "mittel"],
    ["Fussplatten 100x100x6 mit M8", "100x100x6", "A", "Standard", "niedrig"],
    ["Anzahl 2 klein, 2 gross", "2 + 2", "OBJ", "layout.json tanks (Azimut 123/213 und 108/229)", "hoch"],
    ["Farbe gruen #9db89c, Werkstoff PE 0,95", "0,95 g/cm3", "Bild", "ref-4/ref-5 gruene Tanks", "mittel"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("tank.json gepflegt")
