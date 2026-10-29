# Bauteilblatt T50 pumpe (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/pumpe.json` und `designs/components/pumpe.sc`, nicht von Hand aendern)

**Funktion:** Pump-/Filtermodule an den Tanks (Rolle laut docs/components.md Annahme): Pumpenmodul = Montagetafel mit Kreiselpumpe fuer den Umlauf; Filtermodul = flache Filterkassette mit Siebeinsatz (Feinfilter, Matte) im Wasserweg zwischen Absetzer und Biofilter. Ob die OBJ-Platten wirklich Pumpentafeln und die 384-mm-Kassetten Filter sind, ist offen.

**Datei:** `designs/components/pumpe.sc` · **Teilenummer:** T50 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche (Tafel/Gehaeuse-Unterkante), X Laengsachse der Tafel, Y Tafeldicke (Pumpe/Anschluesse auf +Y), Z Hoehe

**Anzahl (Instanzen):** Pumpenmodul klein 4, gross 4, Filtermodul 10 (Quelle: data/layout.json tanks[].modules)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `foot_h` | 40 | mm | [A] Fussleiste unter der Tafel (Standfuesse 2 x 60 x 40 x 5) |
| `wall` | 3 | mm | [A] Gehaeuse PP/PE 3 mm |
| `bracket_w` | 150 | mm | [A] Pumpenkonsole 150 breit (Winkel 5 mm) |
| `bracket_t` | 5 | mm | [A] |
| `pump_z` | 120 | mm | [A] Pumpenachse 120 mm ueber der Tafelunterkante (Konsole darunter) |
| `cable_d` | 8 | mm | [A] Kabel 3 x 1,5 mm2, D8 |
| `plug_l` | 55 | mm | [A] Schutzkontaktstecker 55 x 45 x 40 |
| `mat_clear` | 4 | mm | [A] Spiel Siebeinsatz zur Gehaeusewand |
| `lid_t` | 5 | mm | [A] Deckel der Filterkassette |

| Typ | art | tafel_l | tafel_t | tafel_h | motor_d | motor_l | kopf_d | kopf_l | saug_d | druck_d | anzahl | herkunft | box_l | box_t | box_h | port_d |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| pumpe_klein | pumpe | 502 | 5 | 345 | 90 | 150 | 110 | 70 | 40 | 32 | 4 | layout.json tanks 1 und 4: je 2 Tafeln 502 x 5 x 345 (Duplikate zusammengefasst), Pumpe A |  |  |  |  |
| pumpe_gross | pumpe | 693 | 7 | 463 | 110 | 180 | 130 | 80 | 50 | 40 | 4 | layout.json tanks 2 und 3: je 2 Tafeln 693 x 7 x 463 (Duplikate zusammengefasst), Pumpe A |  |  |  |  |
| filtermodul | filter |  |  |  |  |  |  |  |  |  | 10 | layout.json tanks 2 und 3: je 5 Module 384 x 44 x 419 (z0 249-256) rund um den Tank, Rolle Feinfilter-Matte [A] | 384 | 44 | 419 | 50 |

Gesamt-Box (Messung): X -315.0 bis 251.0, Y -82.5 bis 119.5, Z 0.0 bis 345.0 mm; Koerper: 15.

- Box (Messung) pumpe_klein: X -315 bis 251, Y -82 bis 120, Z 0 bis 345
- Box (Messung) pumpe_gross: X -346 bis 346, Y -84 bis 140, Z 0 bis 463
- Box (Messung) filtermodul: X -252 bis 222, Y -27 bis 26, Z 0 bis 479
**Toleranzen / Spiel:** Tafel-/Gehaeusemasse = OBJ (Pruefung +-0,5 mm); Siebeinsatz 4 mm Spiel zur Gehaeusewand; Pumpensockel liegt auf der Konsole (tangentialer Kontakt Motor/Sockel).

## Werkstoff und Gewicht

- Werkstoff: PP/PE (Tafel, Gehaeuse), PVC (Stutzen), Pumpe Kunststoffgehaeuse, Dichte 0.91 g/cm3, Farbe #2a5da8 (ref-4/5: Module sind im Bild nicht erkennbar; Farbe Annahme)
- Volumen (Messung, `solidcraft-cli eval`): 2885.5 cm3 · Masse leer: 5281 g (5.28 kg)
- Variante `pumpe_klein`: 5.28 kg leer
- Variante `pumpe_gross`: 8.53 kg leer
- Variante `filtermodul`: 1.81 kg leer
- Gefuellt/in Betrieb: pumpe_klein: leer 5.3 kg (Tafel PP, Pumpe Kunststoff, Konsole Stahl); Pumpe real je nach Fabrikat 4-9 kg [A]; Betriebsfuellung der Pumpe ca. 0,5 l | pumpe_gross: leer 8.5 kg (Tafel PP, Pumpe Kunststoff, Konsole Stahl); Pumpe real je nach Fabrikat 4-9 kg [A]; Betriebsfuellung der Pumpe ca. 0,5 l | filtermodul: leer 1.81 kg; gefuellt: Wasserraum 5.6 l = ca. 5.6 kg (Siebeinsatz als Matte, Porenanteil nicht abgezogen) [E]

## Querschnitt / Profil

Pumpenmodul: Montagetafel PP (502x5x345 bzw. 693x7x463) stehend auf zwei Standwinkeln; Konsole aus Winkel 5 mm mit Pumpensockel; Pumpe: Motor (D90 x 150 / D110 x 180) + Pumpenkopf (D110 x 70 / D130 x 80), Saugstutzen axial, Druckstutzen nach oben; Kabel mit Stecker. Filtermodul: Gehaeuse 384x39x419 PP, Wand 3 mm, Deckel 5 mm, Siebeinsatz 4 mm Spiel; Einlass oben, Auslass seitlich unten; vier Montagelaschen.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| pumpe_klein: Saugstutzen (Pumpenkopf) | PVC-U d40 (DN32), Wand 3 | x 176, y 64, z 120 | Wasser tritt ein, Oeffnung zeigt +X |
| pumpe_klein: Druckstutzen (Pumpenkopf oben) | PVC-U d32 (DN25), Wand 3 | x 75, y 64, z 245 | Wasser tritt aus, Oeffnung zeigt +Z |
| pumpe_klein: Stromanschluss (Kabel 3 x 1,5 mm2 mit Schutzkontaktstecker) | 230 V, Stecker 55 x 45 x 40 | x -288, y 64, z 120 | Strom ein; Kabel laeuft nach -X (Laenge 150 modelliert, real 1,5-3 m) |
| pumpe_klein: Standwinkel (Befestigung am Boden) | 2 Winkel 50 x 100 x 5 hinten an der Tafel | x +-191, y -42, z 0 | Befestigung auf dem Boden (Schrauben nicht modelliert), Richtung -Z |
| pumpe_gross: Saugstutzen (Pumpenkopf) | PVC-U d50 (DN40), Wand 3 | x 196, y 76, z 120 | Wasser tritt ein, Oeffnung zeigt +X |
| pumpe_gross: Druckstutzen (Pumpenkopf oben) | PVC-U d40 (DN32), Wand 3 | x 90, y 76, z 255 | Wasser tritt aus, Oeffnung zeigt +Z |
| pumpe_gross: Stromanschluss (Kabel 3 x 1,5 mm2 mit Schutzkontaktstecker) | 230 V, Stecker 55 x 45 x 40 | x -308, y 76, z 120 | Strom ein; Kabel laeuft nach -X (Laenge 150 modelliert, real 1,5-3 m) |
| pumpe_gross: Standwinkel (Befestigung am Boden) | 2 Winkel 50 x 100 x 5 hinten an der Tafel | x +-286, y -44, z 0 | Befestigung auf dem Boden (Schrauben nicht modelliert), Richtung -Z |
| filtermodul: Einlass (Stutzen oben, +X-Ende) | PVC-U d50 (DN40), Wand 3 | x 132, y -2.5, z 479 | Wasser tritt ein, Oeffnung zeigt +Z |
| filtermodul: Auslass (Stutzen seitlich unten, -X-Wand) | PVC-U d50 (DN40), Wand 3 | x -252, y -2.5, z 70 | Wasser tritt aus, Oeffnung zeigt -X |
| filtermodul: Montagelaschen (4 Stueck, je 1 Schraube M6x16) | M6x16 ISO 4017, Loch D7, Lasche 30 x 5 x 40 | x +-207, y -22, z 63 und 356 | Befestigung an der Montageflaeche (z. B. Tankbein), Richtung -Y |

## Verbindungen und Befestigungen

- Konsole an der Tafel: je 2 Schrauben M6x16 ISO 4017 mit Mutter ISO 4032 (im Modell), Tafel steht auf 2 Standwinkeln (am Boden/Tankbein zu verschrauben, nicht modelliert)
- Pumpe auf dem Sockel: 4 Schrauben M6 (nicht modelliert) [A]
- Filtermodul: 4 Montagelaschen mit Schrauben M6x16; Deckel mit 4 Schrauben M6x14 (im Modell; Gewindeeinsaetze/Flansch nicht modelliert)
- Stutzen PVC-U d40/d50 (DIN 8062): geklebt oder mit Verschraubung am Rohrnetz (Montage)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tafel klein 502 x 5 x 345 (2 je Tank, 4 gesamt) | 502x5x345 mm | OBJ | layout.json tanks 1 und 4 modules (Duplikate zusammengefasst) | hoch |
| Tafel gross 693 x 7 x 463 (2 je Tank, 4 gesamt) | 693x7x463 mm | OBJ | layout.json tanks 2 und 3 modules | hoch |
| Filterkassette 384 x 44 x 419 (5 je Tank gross, 10 gesamt) | 384x44x419 mm | OBJ | layout.json tanks 2 und 3 modules (z0 249-256, yaw je 90 Grad versetzt) | hoch |
| Rolle: Tafel = Pumpenmodul, Kassette = Filtermodul | - | A | docs/components.md: Bedeutung Annahme; docs/hydraulics.md: Pumpen, Feinfilter (Matten) im Wasserweg | niedrig |
| Kreiselpumpe: Motor D90 x 150 / D110 x 180, Kopf D110 x 70 / D130 x 80, Achse 120 ueber der Tafelunterkante | mm | A | typische Teich-/Umwaelzpumpen; keine Quelle (R07 pausiert) | niedrig |
| Saug-/Druckstutzen d40/d32 (klein) und d50/d40 (gross) | d40/d32; d50/d40 | A | Rohr d50/d63 am Tank (R09 A); DN der Pumpen Annahme | niedrig |
| Konsole Winkel 5 mm, 150 breit; Pumpensockel | 150 x 5 mm | A | Konstruktionspraxis | niedrig |
| Standwinkel 50 x 100 x 5 (2 je Tafel) | 50x100x5 | A | gegen Kippen | niedrig |
| Kabel 3 x 1,5 mm2 (D8) mit Schutzkontaktstecker | D8 | A | 230 V Standard; Laenge modelliert 150 mm | niedrig |
| Filtergehaeuse Wand 3 mm, Deckel 5 mm, Siebeinsatz mit 4 mm Spiel | 3 / 5 / 4 mm | A | Kunststoffgehaeuse Praxis | niedrig |
| Ein-/Auslass d50 (DN40): Einlass oben, Auslass seitlich unten | d50 | A | Wasserweg: Zulauf oben, Ablauf unten (Schwerkraft); keine Quelle | niedrig |
| Montagelaschen 30x5x40 mit M6x16 | M6 | A | Befestigung an Tankbein/Wand (OBJ: Kassetten stehen an den Tankbeinen) | niedrig |
| Werkstoffe PP 0,91, Stahl 7,85, PVC 1,4 | g/cm3 | Fachwert | Handbuchwerte | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-4/ref-5: Module im Bild nicht erkennbar; data/layout.json tanks[].modules (nur Boxen); docs/components.md (Rolle Annahme); docs/hydraulics.md (Wasserweg)
- Quelle der Masse: data/layout.json tanks[].modules: klein 502 x 5 x 345 (2 je Tank), gross 693 x 7 x 463 (2 je Tank) und 384 x 44 x 419 (5 je Tank, z0 249-256); Rolle der Module ist Annahme (docs/components.md), Pumpe/Filter aus Hydraulik-Konzept (docs/hydraulics.md)
- Abweichung zum OBJ: layout.json tanks[].modules: Tafel- und Kassettenmasse 502x5x345 / 693x7x463 / 384x44x419 stimmen (0 mm Abweichung); Lage und Drehung je Modul stehen in layout.json (yaw, z0: Tafeln am Boden Z -6..3, Kassetten z0 249-256 an den Tankbeinen) und sind Sache des Integrators. Die Rolle der Module ist Annahme (docs/components.md); im OBJ sind es nur Platten/Kassetten ohne Pumpe, Anschluesse oder Kabel; Pumpe, Konsole, Stutzen, Kabel sind [A].

## Montage (L4)

1. Standwinkel an der Tafelrueckseite anschrauben, Tafel am vorgesehenen Platz ausrichten und befestigen
2. Konsole an die Tafel schrauben, Pumpe mit Sockel aufsetzen und fixieren
3. Saug- und Druckstutzen mit dem Rohrnetz verbinden (Montage-Sitzung), Kabel zum Schaltschrank fuehren, Stecker anschliessen
4. Filtermodul: Laschen anschrauben (z. B. am Tankbein), Ein-/Auslass anschliessen, Siebeinsatz einsetzen, Deckel verschrauben

**Werkzeug:** Akkuschrauber, Schluessel M6, Wasserwaage, Rohrschneider, PVC-Kleber

## Stueckliste-Zeile

- pumpe_klein (je Modul, Menge 4 gesamt = 2 je Tank): Montagetafel PP 502x5x345 1, Standwinkel 50x100x5 2, Pumpenkonsole 150x100x5 + 40 hoch 1, Pumpensockel 1, Kreiselpumpe (Motor D90 x 150, Kopf D110 x 70) 1 mit Stutzen d40 und d32, Kabel mit Stecker 1, Schrauben M6x16 ISO 4017 mit Muttern ISO 4032 2
- pumpe_gross (je Modul, Menge 4 gesamt = 2 je Tank): Montagetafel PP 693x7x463 1, Standwinkel 50x100x5 2, Pumpenkonsole 150x100x5 + 40 hoch 1, Pumpensockel 1, Kreiselpumpe (Motor D110 x 180, Kopf D130 x 80) 1 mit Stutzen d50 und d40, Kabel mit Stecker 1, Schrauben M6x16 ISO 4017 mit Muttern ISO 4032 2
- filtermodul (je Modul, Menge 10 gesamt = 5 je Tank gross): Gehaeuse PP 384x39x419 (Wand 3) 1, Deckel PP 384x5x419 1, Siebeinsatz (Filtermatte) 1, Stutzen d50 2, Montagelaschen 4, Schrauben M6x16 ISO 4017 4, Deckelschrauben M6x14 ISO 4017 4 (im Modell, 2 Stueck mehr in Reserve)
- Module gesamt: Pumpenmodul klein 4, gross 4, Filtermodul 10 (layout.json tanks[].modules; Duplikate des OBJ zusammengefasst)

## Alternative lokale Fertigung

Pumpe: handelsuebliche Kreiselpumpe (Teich-/Umwaelzpumpe) auf Montagebrett; Filtermodul: Kunststoff-Kassette aus dem Aquaristik-/Teichbedarf mit Filtermatte (Feinfilter).

## Renders

- `renders/components/filtermodul/filtermodul-01-iso.png`
- `renders/components/filtermodul/filtermodul-02-anschluesse.png`
- `renders/components/filtermodul/filtermodul-03-rueckseite.png`
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

- Gauntlet-Urteil: Spec-Pruefer laeuft; kein Bild-Kritiker (Module in keiner Referenz sichtbar)
- scripts/workshop/check_pumpe.py (Ergebnis renders/components/pumpe_klein/check.txt)
- Kein Bild-Kritiker: die Module sind in keiner Referenz sichtbar; Spec-Pruefer und Orchestrator-Stichprobe

## Offene Fragen

- Rolle der Module (Pumpentafel/Filterkassette) ist Annahme; OBJ liefert nur Boxen
- Pumpenfabrikat, Foerderstrom und Leistung offen (R07 pausiert)
- Schrauben der Pumpe auf dem Sockel, Standwinkel-Befestigung und Deckel-Flansch nicht modelliert
- Kabel gerade und 150 mm kurz modelliert (real 1,5-3 m)
- Lage der 693-mm-Tafeln am Boden und der Kassetten an den Tankbeinen: Integrator
