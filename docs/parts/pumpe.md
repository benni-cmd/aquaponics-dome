# Bauteilblatt T50 pumpe (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/pumpe.json` und `designs/components/pumpe.sc`, nicht von Hand aendern)

**Funktion:** Pumpenmodul an den Tanks (Rolle ANNAHME): Montagetafel mit Kreiselpumpe fuer den Umlauf; Foerderstrom laut docs/hydraulics.md 2.3 [E]: kleiner Tank ca. 12 l/min, grosser ca. 30 l/min, statische Hoehe ca. 1,3 m plus Reibung. ENTSCHEIDUNG Orchestrator 29.10.: Die 10 Kassetten 384 x 44 x 419 (layout.json tanks 2/3) sind KEINE Filtermodule, sondern Stuetzrippen/Konsolen der Tankplattform (Klasse Tank, Annahme A); die Klasse filtermodul entfaellt (Alternative Filterkassette: Entwurf entfernt).

**Datei:** `designs/components/pumpe.sc` · **Teilenummer:** T50 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche (Tafel/Gehaeuse-Unterkante), X Laengsachse der Tafel, Y Tafeldicke (Pumpe/Anschluesse auf +Y), Z Hoehe

**Anzahl (Instanzen):** Pumpenmodul klein 4, gross 4 (Quelle: data/layout.json tanks[].modules (Duplikate zusammengefasst))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `foot_h` | 40 | mm | [A] (derzeit ungenutzt) Standwinkel statt Fussleiste: 2 Winkel 50 x 100 x 5 hinten an der Tafel |
| `bracket_w` | 150 | mm | [A] Pumpenkonsole 150 breit (Winkel 5 mm) |
| `bracket_t` | 5 | mm | [A] |
| `pump_z` | 120 | mm | [A] Pumpenachse 120 mm ueber der Tafelunterkante (Konsole darunter) |
| `cable_d` | 8 | mm | [A] Kabel 3 x 1,5 mm2, D8 |
| `plug_l` | 55 | mm | [A] Schutzkontaktstecker 55 x 45 x 40 |

| Typ | art | tafel_l | tafel_t | tafel_h | motor_d | motor_l | kopf_d | kopf_l | saug_d | druck_d | anzahl | herkunft |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pumpe_klein | pumpe | 502 | 5 | 345 | 90 | 150 | 110 | 70 | 40 | 32 | 4 | layout.json tanks 1 und 4: je 2 Tafeln 502 x 5 x 345 (Duplikate zusammengefasst), Pumpe A |
| pumpe_gross | pumpe | 693 | 7 | 463 | 110 | 180 | 130 | 80 | 50 | 40 | 4 | layout.json tanks 2 und 3: je 2 Tafeln 693 x 7 x 463 (Duplikate zusammengefasst), Pumpe A |

Gesamt-Box (Messung): X -315.0 bis 251.0, Y -82.5 bis 119.5, Z 0.0 bis 345.0 mm; Koerper: 15.

- Box (Messung) pumpe_klein: X -315 bis 251, Y -82 bis 120, Z 0 bis 345
- Box (Messung) pumpe_gross: X -346 bis 346, Y -84 bis 140, Z 0 bis 463
**Toleranzen / Spiel:** Tafel-/Gehaeusemasse = OBJ (Pruefung +-0,5 mm); Siebeinsatz 4 mm Spiel zur Gehaeusewand; Pumpensockel liegt auf der Konsole (tangentialer Kontakt Motor/Sockel).

## Werkstoff und Gewicht

- Werkstoff: PP/PE (Tafel, Gehaeuse), PVC (Stutzen), Pumpe Kunststoffgehaeuse, Dichte 0.91 g/cm3, Farbe #2a5da8 (ref-4/5: Module sind im Bild nicht erkennbar; Farbe Annahme)
- Volumen (Messung, `solidcraft-cli eval`): 2885.5 cm3 · Masse leer: 5281 g (5.28 kg)
- Variante `pumpe_klein`: 5.28 kg leer
- Variante `pumpe_gross`: 8.53 kg leer
- Gefuellt/in Betrieb: pumpe_klein: leer 5.3 kg (Tafel PP, Pumpe Kunststoff, Konsole Stahl); Pumpe real je nach Fabrikat 4-9 kg [A]; Betriebsfuellung der Pumpe ca. 0,5 l | pumpe_gross: leer 8.5 kg (Tafel PP, Pumpe Kunststoff, Konsole Stahl); Pumpe real je nach Fabrikat 4-9 kg [A]; Betriebsfuellung der Pumpe ca. 0,5 l

## Querschnitt / Profil

Montagetafel PP (502x5x345 bzw. 693x7x463) stehend auf zwei Standwinkeln; Konsole aus Winkel 5 mm mit Pumpensockel; Pumpe: Motor (D90 x 150 / D110 x 180) + Pumpenkopf (D110 x 70 / D130 x 80), Saugstutzen axial, Druckstutzen nach oben; Kabel mit Stecker.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| pumpe_klein: Saugstutzen (Pumpenkopf) | PVC-U d40 (DN32), Wand 3 | x 176, y 64, z 120 | Wasser tritt ein, Oeffnung zeigt +X |
| pumpe_klein: Druckstutzen (Pumpenkopf oben) | PVC-U d32 (DN25), Wand 3 | x 75, y 64, z 245 | Wasser tritt aus, Oeffnung zeigt +Z |
| pumpe_klein: Stromanschluss (Kabel 3 x 1,5 mm2 mit Schutzkontaktstecker) | 230 V, Stecker 55 x 45 x 40 | x -288, y 64, z 120 (Steckermitte; Steckerende x -316, Kabel 150 mm) | Strom ein; Kabel laeuft nach -X (Laenge 150 modelliert, real 1,5-3 m) |
| pumpe_klein: Standwinkel (Befestigung am Boden) | 2 Winkel 50 x 100 x 5 hinten an der Tafel | x +-191, y -42, z 0 | Befestigung auf dem Boden (Schrauben nicht modelliert), Richtung -Z |
| pumpe_gross: Saugstutzen (Pumpenkopf) | PVC-U d50 (DN40), Wand 3 | x 196, y 76, z 120 | Wasser tritt ein, Oeffnung zeigt +X |
| pumpe_gross: Druckstutzen (Pumpenkopf oben) | PVC-U d40 (DN32), Wand 3 | x 90, y 76, z 255 | Wasser tritt aus, Oeffnung zeigt +Z |
| pumpe_gross: Stromanschluss (Kabel 3 x 1,5 mm2 mit Schutzkontaktstecker) | 230 V, Stecker 55 x 45 x 40 | x -308, y 76, z 120 (Steckermitte; Steckerende x -336, Kabel 150 mm) | Strom ein; Kabel laeuft nach -X (Laenge 150 modelliert, real 1,5-3 m) |
| pumpe_gross: Standwinkel (Befestigung am Boden) | 2 Winkel 50 x 100 x 5 hinten an der Tafel | x +-286, y -44, z 0 | Befestigung auf dem Boden (Schrauben nicht modelliert), Richtung -Z |

## Verbindungen und Befestigungen

- Konsole an der Tafel: je 2 Schrauben M6x16 ISO 4017 mit Mutter ISO 4032 (im Modell), Tafel steht auf 2 Standwinkeln (am Boden/Tankbein zu verschrauben, nicht modelliert)
- Pumpe auf dem Sockel: 4 Schrauben M6 (nicht modelliert) [A]
- Stutzen PVC-U d40/d50 (DIN 8062): geklebt oder mit Verschraubung am Rohrnetz (Montage)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tafel klein 502 x 5 x 345 (2 je Tank, 4 gesamt) | 502 x 5 x 345 mm | OBJ | layout.json tanks 1 und 4 modules (4 Eintraege je Tank, 2 Duplikate zusammengefasst; OBJ 501-502) | hoch |
| Tafel gross 693 x 7 x 463 (2 je Tank, 4 gesamt) | 693 x 7 x 463 mm | OBJ | layout.json tanks 2 und 3 modules (3 Eintraege je Tank, 1 Duplikat) | hoch |
| Anzahl 4 / 4 (Pumpentafeln klein/gross) | 4 / 4 | OBJ + E | Duplikate (<= 5 mm Versatz) zusammengefasst; hydraulics.md 3 nennt 4 Pumpen + 2 Siebe (Abweichung offen) | mittel |
| Kreiselpumpe klein: Motor D90 x 150, Kopf D110 x 70, Achse 120 ueber der Tafelunterkante | D90/150, D110/70, z 120 | A | typische Teich-/Umwaelzpumpe; keine Quelle (R07 pausiert) | niedrig |
| Kreiselpumpe gross: Motor D110 x 180, Kopf D130 x 80 | D110/180, D130/80 | A | typische Umwaelzpumpe; keine Quelle | niedrig |
| Foerderstrom klein ca. 12 l/min, gross ca. 30 l/min | 12 / 30 l/min | E | docs/hydraulics.md 2.3 (Verweilzeit 30 min im Absetzer) | niedrig |
| Saug-/Druckstutzen d40/d32 (klein), d50/d40 (gross) | d40/d32; d50/d40 | A | Rohr d50/d63 am Tank (R09 A); Pumpen-DN Annahme | niedrig |
| Konsole Winkel 5 mm, 150 breit; Pumpensockel 8 mm | 150 x 5 mm; 8 mm | A | Konstruktionspraxis | niedrig |
| Standwinkel 50 x 100 x 5 (2 je Tafel) | 50 x 100 x 5 mm | A | gegen Kippen der stehenden Tafel | niedrig |
| Kabel 3 x 1,5 mm2 D8, 150 mm modelliert; Schutzkontaktstecker 55 x 45 x 40 | D8 x 150; 55 x 45 x 40 mm | A | 230 V Standard; Laenge kuerzer als real (1,5-3 m) | niedrig |
| Farbe Pumpe #2a5da8, Tafel grau, Stutzen grau | #2a5da8 | A | Module in keiner Referenz sichtbar | niedrig |
| Port-Koordinaten (Saug-, Druckstutzen, Strom, Standwinkel) | siehe Ports | E | berechnet aus den Parametern (fix_pumpe_blatt.py), Ursprung = Mitte der Standflaeche | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-4/ref-5: Module im Bild nicht erkennbar; data/layout.json tanks[].modules (nur Boxen); docs/components.md (Rolle Annahme); docs/hydraulics.md (Wasserweg)
- Quelle der Masse: data/layout.json tanks[].modules: klein 502 x 5 x 345 (2 je Tank), gross 693 x 7 x 463 (2 je Tank); Rolle Pumpentafel ist Annahme (docs/components.md); Pumpe aus Hydraulik-Konzept (docs/hydraulics.md)
- Abweichung zum OBJ: layout.json tanks[].modules: Tafel- und Tafelnmasse stimmen auf <= 1 mm (OBJ 501/502 x 5 x 345, 693 x 7 x 463, 384 x 43/44 x 418/419; Bauteil 502/693/384 mit Dicke 5/7/44); Lage je Modul: layout.json (yaw: Tafeln 22,9/40,7 bzw. 22,9/41,1 Grad, Tafeln z0 -6..3) - Integrator. Anzahl: OBJ listet je Tank 4 (klein) bzw. 8 (gross) Eintraege (components.md: 4-8), davon 2 bzw. 1 Duplikate an derselben Position (Abstand <= 5 mm) -> 2 Tafeln je kleinem Tank, 2 Tafeln + 5 Tafeln je grossem Tank; gesamt 4 / 4 / 10. docs/hydraulics.md 3 sieht je Linie Pumpe A, Pumpe B und ein Feinsieb vor (4 Pumpen, 2 Siebe): Abweichung zu 8 Tafeln und 10 Tafeln offen. Im OBJ sind es nur Boxen ohne Pumpe, Anschluesse oder Kabel: Pumpe, Konsole, Stutzen, Kabel sind [A]. Ausrichtung: Pumpenseite +Y; im OBJ steht die Tafel tangential zum Tank, +Y soll vom Tank weg zeigen (yaw des Integrators). Die 384er-Kassetten sind Stuetzrippen der Tankplattform (Klasse Tank, Entscheidung Orchestrator 29.10.) und gehoeren nicht zu dieser Klasse.

## Montage (L4)

1. Standwinkel an der Tafelrueckseite anschrauben, Tafel am vorgesehenen Platz ausrichten und befestigen
2. Konsole an die Tafel schrauben, Pumpe mit Sockel aufsetzen und fixieren
3. Saug- und Druckstutzen mit dem Rohrnetz verbinden (Montage-Sitzung), Kabel zum Schaltschrank fuehren, Stecker anschliessen

**Werkzeug:** Akkuschrauber, Schluessel M6, Wasserwaage, Rohrschneider, PVC-Kleber

## Stueckliste-Zeile

- pumpe_klein (je Modul, Menge 4 gesamt = 2 je Tank): Montagetafel PP 502x5x345 1, Standwinkel 50x100x5 2, Pumpenkonsole 150x100x5 + 40 hoch 1, Pumpensockel 1, Kreiselpumpe (Motor D90 x 150, Kopf D110 x 70) 1 mit Stutzen d40 und d32, Kabel mit Stecker 1, Schrauben M6x16 ISO 4017 mit Muttern ISO 4032 2; zusaetzlich 4 Schrauben M6x20 fuer die Pumpe, 2 Schrauben M6 fuer die Standwinkel, Dichtung ID 16 (nicht modelliert)
- pumpe_gross (je Modul, Menge 4 gesamt = 2 je Tank): Montagetafel PP 693x7x463 1, Standwinkel 50x100x5 2, Pumpenkonsole 150x100x5 + 40 hoch 1, Pumpensockel 1, Kreiselpumpe (Motor D110 x 180, Kopf D130 x 80) 1 mit Stutzen d50 und d40, Kabel mit Stecker 1, Schrauben M6x16 ISO 4017 mit Muttern ISO 4032 2; zusaetzlich 4 Schrauben M6x20 fuer die Pumpe, 2 Schrauben M6 fuer die Standwinkel, Dichtung ID 16 (nicht modelliert)
- Module gesamt: Pumpenmodul klein 4, gross 4 (layout.json tanks[].modules; Duplikate zusammengefasst)

## Alternative lokale Fertigung

Pumpe: handelsuebliche Kreiselpumpe (Teich-/Umwaelzpumpe) auf Montagebrett.

## Renders

- `renders/components/pumpe_gross/pumpe_gross-01-iso.png`
- `renders/components/pumpe_gross/pumpe_gross-02-pumpe.png`
- `renders/components/pumpe_gross/pumpe_gross-03-rueckseite.png`
- `renders/components/pumpe_gross/pumpe_gross-04-seite.png`
- `renders/components/pumpe_gross/pumpe_gross-05-schnitt.png`
- `renders/components/pumpe_klein/pumpe_klein-01-iso.png`
- `renders/components/pumpe_klein/pumpe_klein-02-pumpe.png`
- `renders/components/pumpe_klein/pumpe_klein-03-rueckseite.png`
- `renders/components/pumpe_klein/pumpe_klein-04-seite.png`
- `renders/components/pumpe_klein/pumpe_klein-05-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Spec-Pruefer: FAIL behoben; Orchestrator-Entscheidung 29.10.: Kassetten = Stuetzrippen (Klasse Tank), Klasse filtermodul entfaellt
- scripts/workshop/check_pumpe.py (Ergebnis renders/components/pumpe_klein/check.txt)
- Kein Bild-Kritiker: die Module sind in keiner Referenz sichtbar; Spec-Pruefer (FAIL -> behoben); Orchestrator-Entscheidung 29.10. zur Rolle

## Offene Fragen

- Rolle der 502/693er-Tafeln als Pumpentafeln ist Annahme (OBJ liefert nur Boxen; Tafeln stehen tangential am Boden: alternativ Seitenbleche/Spritzschutz)
- Anzahl 4 Pumpenmodule (OBJ) gegen 4 Pumpen A/B + 2 Siebe (hydraulics.md 3): Siebe ohne Bauteil
- Pumpenfabrikat, Leistung (R07 pausiert); Foerderstrom 12 / 30 l/min nur [E]
- Schrauben der Pumpe auf dem Sockel (4 x M6), Standwinkel-Befestigung nicht modelliert
- Kabel gerade und 150 mm kurz modelliert (real 1,5-3 m); Elektrik/Zufuehrung: Schaltschrank-Klasse
- Kollision Pumpe/Tankkegel: Integrator pruefen
