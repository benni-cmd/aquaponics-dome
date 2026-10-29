# Kontextpaket Kritiker: tank (klein = Vortex-Absetzer, gross = Biofilter; Werkstatt, 29.10.2026)

## 1. Scope-Card (aus `docs/scope-cards.md`)
- **DRIN:** Zylinder + Kegel (Winkel 45-60 Grad), tangentialer Zulauf, Mittelrohr (Leitrohr), Schlammventil an der Kegelspitze (Bulkhead), Deckel/Oeffnung, Plattform mit 4 Beinen, Diagonalen, Fussplatten.
- **DRAUSSEN:** Rohrnetz und Schlaeuche (Integrator/Montage), Pumpe/Filtermodul (eigene Klasse), Wasserfuellung.
- **Anzahl:** klein 2 (D673, Hoehe 1075 inkl. Kegel; Plattform 706 x 707 x 73 auf Z 428, Beine 30 x 30 x 751), gross 2 (D930, Hoehe 1444; Plattform 977 x 976 x 98 auf Z 570, Beine 40 x 40 x 1008). Azimute 123/213 und 108/229.
- **Fehlinterpretation:** Tank als reiner Zylinder ohne Kegel; Fittings am Rand statt an der Kegelspitze.

## 2. System in fuenf Zeilen
Geodaetische Aquaponik-Kuppel (12 m). Vier Kegelbodentanks stehen auf der Tuerseite um 108-229 Grad auf Plattformen mit Beinen. Wasserweg (Annahme): Pool -> Pumpe -> kleiner Tank (Vortex-Absetzer: tangentialer Zulauf, Feststoffe sinken zur Kegelspitze und werden dort abgelassen) -> grosser Tank (Biofilter mit Biomedium, Belueftung) -> Verteiler -> NFT-Tische und Beete. Hierarchie: Tank > Plattform > Beine; Pumpen/Rohre sind andere Klassen.

## 3. Bilder (`renders/components/tank_klein/critic/` und `renders/components/tank_klein/`, `tank_gross/`)
- `critic/k1-referenz-gesamt-markiert.png`: ref-4 mit roten Rahmen um die Tanks (links Vortex/klein-gross Paar, rechts vorn ein Paar).
- `critic/k2-referenz-ausschnitt-tanks-ref4.png` und `k2b-referenz-ausschnitt-tanks-ref5.png`: Referenzausschnitte der gruenen Tanks (ref-5: Randwulst, offen/Wasserspiegel sichtbar, Beine verdeckt; ref-4: Tanks auf duennen Beinen mit Diagonalstreben).
- Modell: `tank_klein/tank_klein-01-iso.png`, `-02-kegel.png` (Kegel, Plattform, Beine, Schlammventil), `-03-zulauf.png` (tangentialer Zulauf), `-04-deckel.png` (Deckel mit Leitrohr und Auslauf), `-05-schnitt.png` (Laengsschnitt); dasselbe fuer `tank_gross/` (Biomediumkorb auf Tragrost, Ueberlauf, Belueftung).

## 4. Messwerte (`scripts/workshop/check_tank.py`, `renders/components/tank_klein/check.txt`)
Durchmesser 673 / 930 (inkl. Randwulst 20), Hoehe 1075 / 1444, Kegelspitze Z 172 / 226, Kegel ca. 46-48 Grad ab Horizontal, Plattform 706x707x73 auf Z 428 bzw. 977x976x98 auf Z 570, Beine 4 x 30 / 40 mm bis Z 751 / 1008, Zulauf tangential (Rohr beruehrt die Innenwand), Schlammventil an der Spitze (Stutzen umschliesst Z 172 bzw. 226), 4 Streben, 4 Diagonalen, 4 Fussplatten; klein: Leitrohr D110, gross: Biomedium als EIN Koerper.

## 5. Soll
`data/layout.json` tanks, Scope-Card, R09 (Konfidenz niedrig: keine Quelle fuer Zulauf-DN, Leitrohr, Kegelwinkel). Kegelende auf der Plattform-Oberkante (45 Grad, vom Orchestrator bestaetigt), Rohrmasse, Wand, Randwulst, Plattform als Blechkasten sind Annahmen [A].

## 6. Bekannte Fehlinterpretationen
Pumpen/Rohre/Schlaeuche gehoeren nicht zum Tank; Pflanzen nicht; im OBJ ist die Plattform nur eine Box 73/98 mm dick (hier hohler Blechkasten); die Tanks in der Referenz sind teils offen (Wasserspiegel sichtbar), unser Modell hat einen Deckel (Scope-Card: Deckel/Oeffnung).

## 7. Frage und Antwortformat
Siehe `docs/review-protocol.md` Abschnitt 4: Referenz oder Modell, hoechstens fuenf Luecken, je gross/klein, Bezug, Sicherheit; fremde Klassen unter "Hinweis fuer andere Klasse".
