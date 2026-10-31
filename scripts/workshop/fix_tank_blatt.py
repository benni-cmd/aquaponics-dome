"""Blatt-Text fuer data/components/tank.json (Ports, Gewichte, Stueckliste, Herkunft) aus den Parametern und dem Modell berechnet (Stand nach Spec-Pruefer 29.10.).
ACHTUNG seit W32 (31.10.): NICHT mehr ausfuehren. Es kennt das Schwebebett nicht (Biomediumkorb, Tragrost, bio_h) und wuerde die von Hand fortgeschriebenen Texte in tank.json ueberschreiben (scripts/workshop/tank.py bed_geometry, check_tank.py check_bed)."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tank as tk
p = os.path.join(sc.ROOT, "data", "components", "tank.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
ports, gew, sl, legs, geo, boxes = [], [], [], [], [], []
for typ, T in {k: v for k, v in d["typen"].items() if k != "gross_t3"}.items():
    G = tk.geometry(T, P)
    Rb, w, z0, H = T["R"] - P["rim_w"], T["wall"], T["z0"], T["H"]
    z_top = z0 + H
    di = T["inlet_d"]
    xin = Rb - w - di / 2
    yin = math.sqrt(Rb ** 2 - xin ** 2)
    z_in = z_top - P["inlet_below_top"]
    zo = z_top - P["outlet_below_top"]
    dn_in = {50: "DN40", 63: "DN50"}.get(int(di), "")
    ports.append([f"{typ}: Zulauf tangential (Rohr d{di:.0f}, {dn_in})", f"PVC-U d{di:.0f} nach DIN 8062 ({dn_in}), Wand 3", f"x {xin:.1f}, y {-yin - 220:.0f}, z {z_in:.0f} (Rohrachse parallel Y, Rohrende aussen)", "Wasser tritt ein, Oeffnung zeigt -Y; Rohr beruehrt die Innenwand tangential (Drall)"])
    if not T["biofilter"]:
        ports.append([f"{typ}: Auslauf (Auslaufrohr vom Leitrohr durch die Tankwand)", "PVC-U d50 (DN40)", f"x {Rb + 130:.0f}, y 0, z {zo:.0f} (100 mm unter dem Rand, R09)", "Wasser verlaesst den Absetzer nach +X (Oeffnung zeigt +X)"])
    else:
        ports.append([f"{typ}: Ueberlauf (Auslauf)", "PVC-U d63 (DN50)", f"x {Rb + 130:.0f}, y 0, z {zo:.0f} (100 mm unter dem Rand, R09)", "Wasser verlaesst den Biofilter nach +X (Oeffnung zeigt +X)"])
        ports.append([f"{typ}: Belueftungsanschluss im Deckel", "Rohr d16 (Luftschlauch 16 mm, etwa DN10)", f"x {Rb / 2:.0f}, y 0, z {z_top + P['lid_t']:.0f}", "Luft tritt ein, Oeffnung zeigt +Z"])
    zv = z0 - 12 - P["valve_len"] - 40
    ports.append([f"{typ}: Schlammablass (Kugelhahn an der Kegelspitze)", f"PVC-U d{T['valve_d']} (DN{T['valve_d'] - 10}), Kugelhahn mit Verschraubung", f"x 0, y 0, z {zv:.0f} (Stutzenende); Kegelspitze z {z0}", "Schlamm laeuft nach unten ab (Oeffnung zeigt -Z), Hebel +X"])
    lx, ly = T["plat_l"] / 2 - T["leg_w"] / 2, T["plat_w"] / 2 - T["leg_w"] / 2
    ports.append([f"{typ}: Fussplatten-Anker (4 Fuesse, je 2 x M8)", "Schrauben M8x30 ISO 4017, Loch D9, Platte 100 x 100 x 6; im Boden Duebel/Betonpunkt M8", f"x +-{lx:.0f}, y +-{ly:.0f}, z {P['foot_t']:.0f} (Diagonalversatz +-35); Schraubenenden z {P['foot_t'] - 30:.0f}", "Befestigung auf Boden/Betonpunkt, Richtung -Z"])
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"tank_{typ}.sc"))
    mn, mx = sc.bbox_all(ev)
    boxes.append(f"{typ}: X {mn[0]:.0f} bis {mx[0]:.0f}, Y {mn[1]:.0f} bis {mx[1]:.0f}, Z {mn[2]:.0f} (Schraubenenden 24 mm im Boden) bis {mx[2]:.0f}")
    bio = sum(b["mass_g"] for b in ev["bodies"] if b["name"].startswith("Biomedium")) / 1000
    tot = sum(b["mass_g"] for b in ev["bodies"]) / 1000
    leer = tot - bio
    Ri = Rb - w
    cyl = math.pi * Ri ** 2 * (z_top - G["z_c"]) / 1e6
    cone = math.pi * Ri ** 2 * (G["z_c"] - G["z_t"]) / 3 / 1e6
    vol = cyl + cone
    gew.append(f"{typ}: leer {leer:.0f} kg" + (f", Biomedium (Schuettung 0,15 g/cm3) {bio:.0f} kg" if bio else "") + f"; Wasserfuellung bis Rand {vol:.0f} l = {vol:.0f} kg (Zylinder {cyl:.0f} l + Kegel {cone:.0f} l; Wasserfuellung gehoert zu DRAUSSEN, nur Gewichtsangabe) [E]; gefuellt gesamt {tot + vol:.0f} kg")
    geo.append(f"{typ}: Kegel {G['ang']:.1f} Grad ab Horizontal (Spitze Z {z0}, Ende Z {G['z_c']}), Koerperradius {Rb:.1f} (D{2 * Rb:.0f}) plus Randwulst {P['rim_w']:.0f} = Aussen-D{2 * T['R']:.0f}")
    di_ = T["inlet_d"]
    sl.append(f"{typ} (je Tank): Tank PE ({T['wall']} mm Wand, Aussen-D{2 * T['R']:.0f} x H{H}, Randwulst) 1; Deckel mit Revisionsoeffnung D200 1 (Revisionsdeckel nicht modelliert, 1 Stueck); Zulaufrohr d{di_:.0f} 1 + Bulkhead mit Dichtung 1; " + ("Leitrohr d110 mit Auslaufrohr d50 1 + Bulkhead mit Dichtung 1; " if not T["biofilter"] else "Ueberlauf d63 1 + Bulkhead mit Dichtung 1, Biomediumkorb 1 mit Tragrost 1 und 4 Konsolen 40x40x30, Belueftungsrohr d16 1; 5 Stuetzrippen Kantholz 44 (Dreiecksknaggen radial unter dem Kegel, Fichte, T40g) 1 Satz; ") + f"Kugelhahn d{T['valve_d']} mit Verschraubung und 2 Stutzen 1; Plattform 1; Beine {T['leg_w']}x{T['leg_w']} 4; Streben 4; Diagonalen 25x3 4 (je 2 Schrauben M6x40 ISO 4017 + Mutter ISO 4032, nicht modelliert); Fussplatten 4 mit 8 Schrauben M8x30 ISO 4017 und 8 Duebeln M8")
    legs.append(f"{typ}: Beine 4 x {T['leg_w']}x{T['leg_w']}x{T['leg_wall']} Laenge {T['leg_h'] - P['foot_t']:.0f}")
ev3 = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", "tank_gross_t3.sc"))
mn3, mx3 = sc.bbox_all(ev3)
boxes.append(f"gross_t3 (Tank 3, Rippenmuster gedreht): X {mn3[0]:.0f} bis {mx3[0]:.0f}, Y {mn3[1]:.0f} bis {mx3[1]:.0f}, Z {mn3[2]:.0f} bis {mx3[2]:.0f}")
G1 = tk.geometry(d["typen"]["klein"], P)
bl = {
    "funktion": "Tank mit Kegelboden: klein = Vortex-Absetzer (tangentialer Zulauf, Leitrohr, Schlamm sinkt zur Spitze und wird dort abgelassen), gross = Biofilter (Biomediumkorb auf Tragrost, Belueftung, Ueberlauf, Schlammablass); steht auf Plattform und 4 Beinen.",
    "querschnitt": "Tank PE: Zylinder ueber Kegel, gerollter Randwulst " + f"{P['rim_w']:.0f} x {P['rim_h']:.0f} mm, Wand 4/5 mm, Deckel {P['lid_t']:.0f} mm buendig mit dem Wulst, Revisionsoeffnung D{P['rev_d']:.0f}. Geometrie je Tank: " + " | ".join(geo) + ". Plattform: Blechkasten 4 mm, innen hohl, Kegelsitz 2 mm Spiel, Eckenaussparungen fuer die Beine; Beine Rechteckrohr verzinkt; vier Querstreben auf Hoehe 250/300 und vier Diagonalen (an den Beinkanten gekuerzt).",
    "toleranzen": "Kegelsitz in der Plattform 2 mm Spiel; Zulaufrohr beruehrt die Innenwand tangential (+-0,5 mm); Tankhoehe und Kegelspitze +-1 mm gegen layout.json im Bauteil; Instanzen: layout.json hat je Tank eine eigene Spitze (klein 167-172, gross 226-229): der Integrator setzt z so, dass die Spitze stimmt (Versatz bis 5 mm gegenueber dem Bauteil, z. B. Tank 4: -5 mm), die Plattform liegt je Tank 424-428 bzw. 570-572.",
    "ports": ports,
    "verbindungen": ["Tank sitzt mit dem Kegel im Kegelsitz der Plattform (Kegel-Zylinder-Uebergang auf der Plattform-Oberkante), Haltegurt/Schellen nicht modelliert [A]", "Beine laufen durch Eckenaussparungen der Plattform, geschweisst (MAG), danach verzinkt [A]", "Fussplatten: je 2 Schrauben M8x30 ISO 4017 mit Duebel M8 im Boden/Betonpunkt, Loch D9", "Rohre PVC-U nach DIN 8062/EN 1452 mit Bulkhead-Durchfuehrung und Dichtung durch die Tankwand [A, im Modell nur Durchbruch + Rohr]", "Schlammventil: Kugelhahn PVC-U mit Verschraubung an Stutzen d40/d50", "Biomediumkorb (gross): Tragrost auf 4 Konsolen 40x40x30 (an die Tankwand geschweisst/geklebt) [A]"],
    "abweichung": "layout.json tanks: Durchmesser (inkl. Randwulst), Hoehe, Kegelspitze Z, Plattform-Z und Beinhoehe stimmen (check_tank.py); das Plattform-MASS ist seit W30/D50 absichtlich kleiner als im OBJ (klein 619 statt 706, gross 821 statt 977: Konusdurchmesser auf Plattform-Unterkante + 2 x 60). Kegel: OBJ liefert nur Spitze und Gesamthoehe; Kegelende auf der Plattform-Oberkante, 45 Grad ab Horizontal als Auslegung E (R09-Nachtrag 29.10. 07:55, vom Orchestrator bestaetigt; Gegenprobe Spitze klein 165 gegen OBJ 167-172, gross 203 gegen 226-229); gebaut 48,7 / 47,0 Grad, weil der Randwulst den Koerperradius gegenueber dem OBJ-Durchmesser verkleinert. Leitrohr und Auslauf nach R09 (A, Konfidenz niedrig, R09 behandelt nur den kleinen Tank, fuer gross analog). Beine 751/1008 laufen bis ueber die Plattform (OBJ-Mass). STUETZRIPPEN (gross): die 5 Kassetten 384 x 44 x 419 je grossem Tank aus layout.json tanks[].modules sind nach Orchestrator-Entscheidung 29.10. (D-Punkt 4) Stuetzrippen/Konsolen der Plattform: radial zur Tankachse, Winkel 0/90/135/180/225 Grad (Phase 11,0 Grad bei Tank 2, 53,6 Grad bei Tank 3: Dateien tank_gross.sc und tank_gross_t3.sc), Dreiecksknaggen von z 249 bis zur Plattform-Unterkante 570 (OBJ: bis Plattform-Oberkante 668, also in die hohle Plattform hinein), aussen r 367 statt 468 (Innenkante der Querstreben minus 3 mm, W30), Hypotenuse entlang des Tankkegels mit 3 mm Spiel; Alternative (nicht gebaut): Filterkassetten, Entwurf entfernt. Fittings: OBJ 4 Stueck Z 143-177 mit 30-56 mm, hier Schlammstutzen + Kugelhahn (d40 / d50 Norm statt OBJ 55) + Ablaufstutzen.",
    "montage": ["Plattform mit Beinen am Boden ausrichten, Fussplatten mit M8 verschrauben, Streben und Diagonalen einsetzen", "Tank in den Kegelsitz setzen (zu zweit), Deckel und Leitrohr bzw. Biomediumkorb einsetzen", "Zulauf-Rohr tangential und Auslauf/Ueberlauf durch die Wand fuehren, Dichtungen setzen", "Kugelhahn mit Verschraubung an den Kegelstutzen, Ablaufrohr anschliessen", "Dichtheit pruefen (Wasserprobe), Biomedium und Belueftung einbauen (gross)"],
    "werkzeug": "Lochsaege (d63/d50), Bohrer, Schluessel M6/M8, Wasserwaage, Schweissgeraet (Rahmen) oder Winkelverbinder",
    "stueckliste": sl + ["Tanks gesamt: klein 2, gross 2 (Azimute 123/213 und 108/229, layout.json); Normschrauben: M8x30 ISO 4017, M6x40 ISO 4017, Muttern ISO 4032"],
    "lokal": "Tank: handelsueblicher Konus-Boden-Tank (Kunststoff, 500-1000 l); Plattform/Beine aus Baustahl-Rechteckrohr (Metallbauer) oder Alu-Systemprofil; Rohre und Kugelhaehne PVC-U aus dem Sanitaerhandel.",
    "referenz": "reference/ref-4-dome-clean.jpg und ref-5 (gruene Tanks mit gerolltem Randwulst auf duennen Beinen mit Kegelboden); data/layout.json tanks; docs/research/R09.md",
    "varianten": ["tank_klein", "tank_gross", "tank_gross_t3"],
    "gewicht_gefuellt": " | ".join(gew),
    "massen_getrennt": ["Biomedium"],
    "boxen": boxes,
    "pruefung": ["scripts/workshop/check_tank.py (Ergebnis renders/components/tank_klein/check.txt)", "Bild-Kritiker: Modell; Spec-Pruefer: FAIL (Gewicht, Text gegen Parameter, Auslaufhoehe, Herkunft, Ports) -> behoben, Triage in docs/workshop-log.md"],
    "offen": ["Kegelwinkel/Kegelende: Auslegung E (45 Grad, Plattform-OK), R09 Konfidenz niedrig", "Rohrmasse (Zulauf d50/d63, Leitrohr d110, Auslauf d50/d63, Wand 3 mm) ohne Quelle (R09)", "Beine 751/1008 bis ueber die Plattform: Zweck (Tankfuehrung) aus OBJ nicht ableitbar", "Haltegurt/Schellen, Dichtungen, Verschraubungen der Diagonalen (M6x40), Revisionsdeckel nicht modelliert", "Biofilter (gross): Biomediumkorb, Konsolen, Belueftung als Platzhalter ohne Quelle; kein Leitrohr im Biofilter (R09 nennt es nur fuer den Absetzer, Scope-Card fuehrt es gemeinsam)", "Rolle der Stuetzrippen: Annahme A (Orchestrator), Werkstoff Holz Fichte nur wegen der Dicke 44 mm; Alternative Filterkassette; Rippen enden an der Plattform-Unterkante, im OBJ bis Plattform-Oberkante", "Rolle der Pumpen (eigene Klasse pumpe)", "W30/D50: Plattform 619 / 821 statt 706 / 977; der Kegel sitzt in einem kegeligen Sitz, der Tankzylinder (R 311,5 / 440) ueberragt die Plattform (Kontaktring nur ca. 60 mm hoch im unteren Plattformteil): Tragfaehigkeit des Sitzes und Haltegurt nicht nachgewiesen [A]", "W30: Pumpentafeln 502 x 345 / 693 x 463 passen nicht mehr unter die Plattform (Tank 1: Tafelrand 327 gegen Plattformhalbbreite 310); Montage setzt sie seitlich am Stand, Tafelmittelabstand >= Plattformhalbbreite + 25 + tafel_gap (tank_offsets pruefen)"],
}
d["blatt"] = bl
d["werkstoff"]["herkunft"] = "ref-4/ref-5: gruene Kunststofftanks mit Randwulst; PE-Dichte 0,95 g/cm3 Handbuchwert; Stahl 7,85; PVC-U 1,4"
d["herkunft_tabelle"] = [
    ["Tankdurchmesser 673 / 930 (inkl. Randwulst)", "673 / 930 mm", "OBJ", "layout.json tanks d (Tank 1/4 und 2/3)", "hoch"],
    ["Tankhoehe 1075 / 1444 (inkl. Kegel)", "1075 / 1444 mm", "OBJ", "layout.json tanks h", "hoch"],
    ["Kegelspitze Z 172 / 226", "172 / 226 mm", "OBJ", "layout.json tanks z0 (167-172, 226-229)", "hoch"],
    ["Plattform OBJ 706x707x73 auf Z 428 / 977x976x98 auf Z 570 (Z und Dicke gelten weiter)", "706x707x73 / 977x976x98", "OBJ", "layout.json tanks platform", "hoch"],
    ["Plattform Breite/Laenge 619 (klein) / 821 (gross) = 2 x (Konusradius auf Plattform-Unterkante + 2 + 60)", "619 / 821", "Ben + R", "Ben 31.10./D50 (Stand zu gross), Rechnung aus der Tankgeometrie (fix_w30_tank.py)", "mittel"],
    ["Pumpentafel steht seitlich am Stand (Abstand 30 mm von der Strebenaussenkante), Tafellaenge <= Plattform", "502 <= 619 / 693 <= 821", "A", "W30: Tafel passt nicht mehr unter die Plattform (Tank 1: 327 gegen 310), Montage setzt sie seitlich", "niedrig"],
    ["Beine 4 x 30x30xh751 / 40x40xh1008", "751 / 1008 mm", "OBJ", "layout.json tanks legs; Querschnitt aus oasis-obj-analysis", "hoch"],
    ["Kegel 45 Grad ab Horizontal, Ende auf der Plattform-Oberkante (gebaut 48,7 / 47,0 Grad wegen Randwulst)", "45 Grad", "E", "R09-Nachtrag 29.10. 07:55 (Orchestrator): Gegenprobe Spitze klein 165 gegen OBJ 167-172, gross 203 gegen 226-229; Scope-Card 45-60 Grad", "mittel"],
    ["Randwulst 25 x 40 mm", "25 x 40", "Bild + A", "ref-5: dicker gerollter Randwulst der gruenen Tanks; Mass Annahme", "niedrig"],
    ["Tankwand 4 / 5 mm, Deckel 6 mm buendig", "4 / 5 / 6 mm", "A", "PE-Tank Wanddicke; OBJ nur Huelle", "niedrig"],
    ["Revisionsoeffnung im Deckel D200", "D200", "Scope-Card + A", "Scope-Card: Deckel/Oeffnung; Mass Annahme", "niedrig"],
    ["Zulauf tangential d50 / d63, 250 mm unter dem Rand", "d50 / d63", "R09 + A", "R09: tangentialer Zulauf, DN50 oben (Konfidenz niedrig, nur fuer klein); gross analog [A]", "niedrig"],
    ["Leitrohr d110, endet 1/3 Zylinderhoehe ueber der Spitze (klein)", "d110", "R09", "R09: Leitrohr D110, endet ca. 1/3 der Zylinderhoehe ueber der Kegelspitze (A, Konfidenz niedrig)", "niedrig"],
    ["Auslauf d50 (klein) / Ueberlauf d63 (gross) 100 mm unter dem Rand", "d50 / d63, 100 mm", "R09 + A", "R09: Auslass oben seitlich, 100 mm unter dem Rand (A); gross analog", "niedrig"],
    ["Schlammventil Kugelhahn d40 / d50 an der Kegelspitze", "d40 / d50", "OBJ + R09 + A", "layout.json tanks fittings (Groessen 30-56 an der Spitze); R09: Schlammablass Bulkhead 32-40 mit Hahn; gross d50 Norm statt OBJ 55", "mittel"],
    ["Biofilter: Biomediumkorb (EIN Koerper) auf Tragrost mit 4 Konsolen 40x40x30, Belueftung d16", "520 mm hoch", "A", "Scope-Card tank_gross: Platzhalter; keine Quelle (R09)", "niedrig"],
    ["Plattform als Blechkasten 4 mm, hohl, mit Kegelsitz (Spiel 2) und Eckenaussparungen", "4 mm / 2 mm", "A", "OBJ-Plattform 73/98 mm dick (massiv unwahrscheinlich); Konstruktionsannahme", "niedrig"],
    ["Querstreben auf Hoehe 250 / 300, 4 Diagonalen 25x3", "250 / 300 mm", "Bild + A", "ref-4/ref-5: Tanks auf Beinen mit Diagonalstreben (Scope-Card: Diagonalen)", "mittel"],
    ["Fussplatten 100x100x6 mit M8x30", "100x100x6", "A", "Standard", "niedrig"],
    ["Stuetzrippen: 5 je grossem Tank, 384 x 44 x 419, radial, Winkel 0/90/135/180/225 Grad", "5 Rippen, 44 mm", "OBJ + A", "layout.json tanks 2/3 modules (384 x 43/44 x 418/419, z0 249-256, radial im Abstand 276); Rolle Stuetzrippe: Orchestrator-Entscheidung 29.10. (A)", "mittel"],
    ["Anzahl 2 klein, 2 gross", "2 + 2", "OBJ", "layout.json tanks (Azimut 123/213 und 108/229)", "hoch"],
    ["Farbe gruen #9db89c", "#9db89c", "Bild", "ref-4/ref-5 gruene Tanks", "mittel"],
    ["Werkstoffdichten: PE 0,95, Stahl 7,85, PVC-U 1,4, Biomedium 0,15", "g/cm3", "Fachwert + A", "Handbuchwerte Kunststoffe/Stahl; Biomedium Schuettdichte Annahme", "mittel"],
]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("tank.json gepflegt")
