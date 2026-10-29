"""Blatt pumpe nach Spec-Pruefer Runde 2 (W12, 29.10. ~14:10): Sockelhoehe (Kopf/Konsole), Konsolenmasse, Schrauben M6x20, Filtermodul-Reste, Dichten, Gewicht, Anzahl.
Aendert data/components/pumpe.json aus Messung (.sc) und Parametern; danach partsheet.py pumpe ausfuehren."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

p = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
B, V = d["blatt"], {}
meas = {}
for typ, T in d["typen"].items():
    ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"{typ}.sc"))
    bodies = {b["name"]: b for b in ev["bodies"]}
    mass = sum(b["mass_g"] for b in ev["bodies"]) / 1000
    vol = sum(b["volume_mm3"] for b in ev["bodies"]) / 1000
    mn, mx = sc.bbox_all(ev)
    kon = bodies["Konsole"]["bbox"]
    sock = bodies["Pumpensockel"]["bbox"]
    pump = (bodies["Motor"]["mass_g"] + bodies["Pumpenkopf"]["mass_g"]) / 1000
    meas[typ] = dict(mass=mass, vol=vol, box=(mn, mx), kon=[round(kon["max"][i] - kon["min"][i], 1) for i in range(3)],
                     sock=[round(sock["max"][i] - sock["min"][i], 1) for i in range(3)], pump=pump, dens=mass / vol * 1000 if vol else 0)

def rep(s, old, new):
    assert old in s, old[:50]
    return s.replace(old, new)

# Funktion
B["funktion"] = rep(B["funktion"], " (Alternative Filterkassette: Entwurf entfernt)", "")
B["funktion"] = rep(B["funktion"], "statische Hoehe ca. 1,3 m plus Reibung.", "statische Hoehe ca. 1,3 m plus Reibung (hydraulics.md 2.8 [E]); die 30 l/min sind die Umwaelzung des grossen Tanks bei 30 min Verweilzeit, nicht der Linienstrom 12 l/min je Pool-Linie aus 2.4.")
# Toleranzen / Kollision
B["toleranzen"] = ("Tafel-/Gehaeusemasse = OBJ (Pruefung +-0,5 mm); Pumpensockel 11 mm hoch (= Kopfueberstand 10 mm + 1 mm Luft), Motor ruht tangential auf dem Sockel, der Pumpenkopf (D110/D130) hat 1 mm Luft zur Konsole (Vorpruefung, keine Durchdringung); "
                   "Pumpenachse bleibt bei z 120 (Konsole liegt entsprechend tiefer).")
# Ports: Steckerenden
for i, row in enumerate(B["ports"]):
    row[2] = row[2].replace("Steckerende x -316", "Steckerende x -315").replace("Steckerende x -336", "Steckerende x -335")
    if "Standwinkel" in row[0]:
        row[3] = row[3].replace("Befestigung auf dem Boden (Schrauben nicht modelliert)", "Befestigung auf tragfaehigem Untergrund (Boden ist Erde: Betonplatte/Tankbein, Montage/Integrator; Schrauben nicht modelliert)")
# Verbindungen
B["verbindungen"] = [
    "Konsole an der Tafel: je 2 Schrauben M6x20 ISO 4017 mit Mutter ISO 4032 (im Modell; Klemmlaenge Tafel 5/7 + Konsole 5 + Mutter 5,2 = 15,2/17,2 mm, Schraube 20 mm steht >= 2 Gewindegaenge ueber), Scheiben ISO 7089 (nicht modelliert) [A]",
    "Tafel steht auf 2 Standwinkeln; je Winkel 2 Schrauben M6 mit Duebel/Mutter (4 je Tafel, nicht modelliert) [A], am tragfaehigen Untergrund zu verschrauben",
    "Pumpe auf dem Sockel: 4 Schrauben M6x20 mit Mutter und Scheibe (nicht modelliert) [A]",
    "Stutzen PVC-U d40/d32 (klein), d50/d40 (gross) (DIN 8062): geklebt oder mit Verschraubung am Rohrnetz (Montage); Uebergang auf Tankrohr d50/d63 mit Reduziermuffe aus `leitungsteile`",
]
# Abweichung: Anzahl und Kassetten klar trennen
a = B["abweichung"]
i0 = a.index("Anzahl: OBJ listet")
i1 = a.index("Im OBJ sind es nur Boxen")
B["abweichung"] = a[:i0] + ("Anzahl: OBJ listet je kleinem Tank 4 und je grossem Tank 3 Pumpentafel-Eintraege, davon 2 bzw. 1 Duplikate an derselben Position (Abstand <= 5 mm) -> 2 Tafeln je Tank, gesamt 4 klein + 4 gross = 8 Pumpenmodule. "
    "docs/hydraulics.md 3 sieht je Linie Pumpe A und Pumpe B vor (4 Pumpen) und 2 Siebe: Abweichung 8 gegen 4 Pumpen offen, die Siebe haben kein Bauteil. ") + a[i1:]
# Stueckliste
for k, typ in ((0, "pumpe_klein"), (1, "pumpe_gross")):
    m = meas[typ]
    s = B["stueckliste"][k]
    s = rep(s, "Pumpenkonsole 150x100x5 + 40 hoch 1, Pumpensockel 1", f"Pumpenkonsole (Winkel 5 mm: Horizontalschenkel {m['kon'][0]:.0f} x {m['kon'][1]:.0f}, Vertikalschenkel 150 x 40) 1, Pumpensockel {m['sock'][0]:.0f} x {m['sock'][1]:.0f} x {m['sock'][2]:.0f} 1")
    s = rep(s, "Schrauben M6x16 ISO 4017 mit Muttern ISO 4032 2; zusaetzlich 4 Schrauben M6x20 fuer die Pumpe, 2 Schrauben M6 fuer die Standwinkel, Dichtung ID 16 (nicht modelliert)",
            "Schrauben M6x20 ISO 4017 mit Muttern ISO 4032 2 und Scheiben ISO 7089 2 (Scheiben nicht modelliert); zusaetzlich nicht modelliert: 4 Schrauben M6x20 mit Mutter und Scheibe fuer die Pumpe, 4 Schrauben M6 fuer die Standwinkel (je Winkel 2). Dichtungen/Verschraubungen der Stutzen gehoeren zum Rohrnetz (leitungsteile, Montage)")
    B["stueckliste"][k] = s
# Gewicht, Box, Werkstoff
mk, mg = meas["pumpe_klein"], meas["pumpe_gross"]
B["gewicht_gefuellt"] = (f"pumpe_klein: leer {mk['mass']:.1f} kg (Tafel PP, Pumpe Kunststoff, Konsole Stahl), davon modellierte Pumpe (Motor + Kopf, Volumen x 1,5 g/cm3) {mk['pump']:.1f} kg; gefuellt/in Betrieb ca. {mk['mass'] + 0.5:.1f} kg (Betriebsfuellung der Pumpe ca. 0,5 l [A]) | "
                         f"pumpe_gross: leer {mg['mass']:.1f} kg, davon Pumpe {mg['pump']:.1f} kg; gefuellt ca. {mg['mass'] + 0.5:.1f} kg. Reale Pumpen je nach Fabrikat 4-9 kg [A]: das modellierte Pumpenvolumen ist nur eine Huellform, das reale Gewicht liegt hoeher (Gewichtsbudget der Montage mit 4-9 kg je Pumpe rechnen).")
B["boxen"] = [f"{t}: X {m['box'][0][0]:.0f} bis {m['box'][1][0]:.0f}, Y {m['box'][0][1]:.0f} bis {m['box'][1][1]:.0f}, Z {m['box'][0][2]:.0f} bis {m['box'][1][2]:.0f}" for t, m in meas.items()]
d["werkstoff"]["dichte_g_cm3"] = f"Mischung: PP 0,91 (Tafel) / Pumpe 1,5 / PVC 1,4 (Stutzen) / Stahl 7,85 (Konsole, Sockel, Winkel) / Kabel 1,2; Mittel klein {mk['dens']:.2f}, gross {mg['dens']:.2f}"
# Pruefung und Offen
B["pruefung"] = [
    "scripts/workshop/check_pumpe.py: 30/30 PASS fuer beide Varianten (Ergebnis `renders/components/pumpe_klein/check.txt`; eine Datei deckt klein und gross), inkl. Kopf/Konsole ohne Durchdringung",
    "Kein Bild-Kritiker: die Module sind in keiner Referenz sichtbar; Spec-Pruefer Runde 1 (FAIL, behoben, 29.10. ~08:50) und Runde 2 (FAIL, 5 Befunde, eingearbeitet; Triage in `docs/workshop-log.md`); Orchestrator-Entscheidung D16 zur Rolle",
]
B["offen"] = [
    "Rolle der 502/693er-Tafeln als Pumpentafeln ist Annahme (OBJ liefert nur Boxen; Tafeln stehen tangential am Boden: alternativ Seitenbleche/Spritzschutz)",
    "Anzahl 8 Pumpenmodule (4 klein + 4 gross, OBJ) gegen 4 Pumpen A/B + 2 Siebe (hydraulics.md 3): Siebe ohne Bauteil, Orchestrator/Hydraulik",
    "Pumpenfabrikat, Leistung (R07 pausiert); Foerderstrom 12 / 30 l/min nur [E]; Reale Pumpe 4-9 kg [A]",
    "Schrauben der Pumpe auf dem Sockel (4 x M6x20), Scheiben, Standwinkel-Befestigung nicht modelliert; Untergrund der Standwinkel (Erde) klaert Montage/Integrator",
    "Kabel gerade und 150 mm kurz modelliert (real 1,5-3 m); Elektrik/Zufuehrung: Schaltschrank-Klasse",
    "Kollision Pumpe/Tankkegel und Tafel-Ausrichtung (+Y weg vom Tank): Integrator pruefen",
    "Uebergang Stutzen d40/d32 bzw. d50/d40 auf Tankrohr d50/d63: Reduziermuffen aus `leitungsteile`, Verlegung Montage",
    "Rohrwand 3 mm der Stutzen gegen SDR 21 der Bibliothek leitungsteile (Abweichung dort dokumentiert)",
]
# Herkunft
H = d["herkunft_tabelle"]
for row in H:
    if row[0].startswith("Anzahl 4 / 4"):
        row[0], row[1], row[3] = "Anzahl 4 / 4 (Pumpentafeln klein/gross) = 8 Module", "4 / 4", "Duplikate (<= 5 mm Versatz) zusammengefasst; hydraulics.md 3 nennt 4 Pumpen + 2 Siebe (8 gegen 4, Abweichung offen)"
    if row[0].startswith("Foerderstrom"):
        row[3] = "docs/hydraulics.md 2.3 (Tankumwaelzung bei 30 min Verweilzeit); 2.4 nennt 12 l/min je Pool-Linie; statische Hoehe 1,3 m: hydraulics.md 2.8"
    if row[0].startswith("Konsole Winkel"):
        row[0] = "Konsole Winkel 5 mm: Horizontalschenkel 150 x {kt} x 5, Vertikalschenkel 150 x 40 x 5".format(kt="117 (klein) / 137 (gross)")
        row[1], row[2], row[3] = "150 x 117/137 x 5; 150 x 40 x 5", "A", "Konstruktionspraxis; Tiefe = Pumpenachse vor der Tafel + Motorradius + 10 (E aus pumpe.py)"
H.insert(next(i for i, r in enumerate(H) if r[0].startswith("Standwinkel")), [
    "Pumpensockel {0:.0f} x {1:.0f} x {2:.0f} (klein) / {3:.0f} x {4:.0f} x {5:.0f} (gross)".format(*meas["pumpe_klein"]["sock"], *meas["pumpe_gross"]["sock"]),
    "Hoehe 11 mm", "E", "Hoehe = (Kopf-D - Motor-D)/2 + 1 mm Luft, damit der Pumpenkopf nicht in die Konsole ragt; Laenge 0,7 x Motorlaenge, Breite 0,6 x Motor-D (A)", "mittel"])
H.append(["Schrauben M6x20 an der Konsole (statt M6x16)", "M6x20 ISO 4017 + Mutter ISO 4032", "E", "Klemmlaenge Tafel + Konsole 5 + Mutter 5,2 = 15,2 (klein) / 17,2 (gross); M6x16 stand 0,8 mm bzw. gar nicht ueber der Mutter", "mittel"])
H.append(["Dichten: PP 0,91, Pumpe 1,5, PVC 1,4, Stahl 7,85, Kabel 1,2 g/cm3", "g/cm3", "A", "Handbuchwerte, keine Quelle abgerufen; Mittelwerte im Abschnitt Werkstoff", "niedrig"])
H.append(["Pumpe real 4-9 kg, Betriebsfuellung ca. 0,5 l", "4-9 kg; 0,5 l", "A", "typische Teich-/Umwaelzpumpe; keine Quelle (R07 pausiert); modellierte Huellform ist leichter", "niedrig"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pumpe.json aktualisiert", {t: round(m["mass"], 2) for t, m in meas.items()})
