# Bauteilblatt: Scherenknoten T60S (W74) — zur Abnahme durch Ben, NICHT im Gesamtmodell

**Funktion:** Die Lochplatte verbindet die Streben eines Knotens. Jede Strebe haengt mit einer Schere aus zwei gekreuzten Laschen an einem Plattenloch. Liegen beide Laschenaugen deckungsgleich auf der Platte und sind mit EINER Schraube verschraubt, stehen die zwei Nasen durch zwei gegenueberliegende Gegenloecher 3 mm aus dem Rohr: Die Strebe ist eingerastet. Ohne Plattenschraube oeffnet sich die Schere, die Nasen ziehen ein, das Rohr laesst sich abziehen (R56 Abschnitt 1).

**Gebaut als EIN Bauteil, die Montage setzt nur Instanzen:**
| Datei | Inhalt | Teilenummer | Menge Kuppel |
|---|---|---|---|
| `designs/components/knoten_schere_platte.sc` | Lochplatte | T60S-P | 26 |
| `designs/components/knoten_schere_arm_a.sc` | Schere + Normteile + Rohrende 250 mm, Knick A | T60S-A | 60 Enden |
| `designs/components/knoten_schere_arm_b.sc` | dasselbe, Knick B | T60S-B | 70 Enden |
| `designs/components/knoten_schere.sc` | Detailmodell fuer den Viewer: Platte + ein Arm B | T60S | 0 (nur Ansicht) |

**Generator:** `scripts/workshop/knoten_schere.py` (Parameter und Knotentabelle `data/components/knoten_schere.json`, Teiledaten `data/parts/knoten_schere.json`) · **Pruefung:** `scripts/workshop/check_knoten_schere.py` · **Bilder:** `scripts/workshop/render_knoten_schere.py` (Aufruf ueber `knoten_schere.py --render`) · **Bericht:** `docs/research/R56-scherenknoten.md` · **Blatt:** `docs/jobs/N-VERBINDER.md`.

## Bezugspunkt und Montage
- Alle vier Dateien haben denselben Rahmen: Ursprung = Knotenpunkt, Z = Kuppelnormale n (aussen), Platte in der Tangentialebene.
- Arm: Plattenschraube auf +X bei r 37, Strebe in +X, nach innen (-Z) abgekantet. Die Rohrachse geht durch den Ursprung (gemessen A 0,004 mm, B 0,001 mm).
- **Montage je Knoten:** 1 Platte an `ursprung`, Z auf `normale`, X auf `x_richtung`. Je Arm 1 Instanz A oder B: erst um Z um `drehwinkel_loch_grad` drehen (Plattenschraube sitzt dann im Loch `loch`), dann um die Achse der Plattenschraube um `drehung_um_plattenschraube_grad` (echte Strebenrichtung). Alle Werte in `data/components/knoten_schere.json` → `knoten`.
- Strebenzahl je Knoten = Zahl der Arm-Instanzen (4, 5 oder 6), Winkel = die zwei Drehungen. Kein Teil wird je Knoten neu gebaut.

## Masse und Parameter (Kopfmasse [A] aus dem Foto ohne Massstab, R56 Abschnitt 2)
| Teil | Mass |
|---|---|
| Lochplatte | D 110 x 8, 6 Loecher D 11 auf Lochkreis r 37 (60-Grad-Raster), Mittelbohrung D 20; Unterkante 15,5 mm unter dem Knotenpunkt |
| Lasche (2 je Arm) | Flachstahl 20 x 5, Auge bis Drehpunkt 50, Drehpunkt bis Nase 58, Nase 10 breit, Laschenende 3 hinter der Nase |
| Knick A | 15,9 Grad, Knicklinie bei r 72,1, Drehpunkt 14,9 mm hinter dem Knick |
| Knick B | 18,0 Grad, Knicklinie bei r 63,0, Drehpunkt 24,0 mm hinter dem Knick |
| Rohrende | Rund 42,4 x 2,6 (EN 10255), Probestueck 250 mm; Rohrmund 12 mm hinter dem Drehpunkt; Knotenpunkt bis Rohrmund A 101,9 / B 102,2 mm |
| Gegenloecher | 2 x D 13 gegenueber, 46 mm hinter dem Rohrmund, je auf der Mittelebene ihrer Lasche |
| Plattenschraube | M10 x 35 ISO 4017 8.8, 2 Scheiben ISO 7089, Mutter ISO 4032; Kopf auf der Platte |
| Drehpunktschraube | M8 x 25 ISO 4017 8.8, 2 Scheiben, Mutter |

**Aenderungen gegenueber dem Vorentwurf (927d171):**
1. Die Platte liegt wie auf dem Foto OBEN auf den Laschen (Vorentwurf: unter den Laschen). Schraubenkopf auf der Platte, Mutter unter Lasche 1.
2. **A und B unterscheiden sich nicht nur im Knickwinkel, sondern auch in der Lage der Knicklinie** (A r 72,1, B r 63,0). Grund: Eine gemeinsame Platte erzwingt eine gemeinsame Plattenhoehe; nur mit verschobener Knicklinie geht die Rohrachse bei beiden durch den Knotenpunkt. Der Laschenzuschnitt (Laserteil flach) bleibt fuer A und B gleich, nur die Biegelinie wandert. Das weicht vom Blatt ab („NUR im Knickwinkel“) und ist geometrisch zwingend.
3. Schraubenlaengen werden aus Klemmlaenge und Laschendicke gerechnet (bei 8-mm-Laschen automatisch M10 x 40 und M8 x 30).
4. Rohrlaenge in der Kuppel: A 3075 mm, B 3504 mm (Knoten-zu-Knoten minus 2 x Knotenpunkt bis Rohrmund; R56 nannte 3076 / 3504).

## Werkstoff und Gewicht (gemessen mit `solidcraft-cli eval`, 7,85 g/cm3)
| Teil | Masse |
|---|---|
| Lochplatte | 541 g |
| Lasche 1 / Lasche 2 | 96 / 97 g |
| Schrauben, Scheiben, Muttern je Arm | 74 g |
| Rohrstueck 250 mm (nur Probestueck) | 632 g |
| Knoten ohne Rohr: 4- / 5- / 6-wertig | 1,61 / 1,88 / 2,14 kg |
| Alle 26 Platten + 130 Scheren mit Schrauben | 48,8 kg (gegen 155 kg Kugelknoten, `docs/parts/knoten.md`) |
Werkstoffe: Laserteile S235 feuerverzinkt (`Stahl Laserteil`), Rohr EN 10255 verzinkt (`Stahl verzinkt`), Schrauben 8.8 verzinkt (`Stahl Schraube`).

## Lochbild-Frage (Blatt Bauteil-Aufbau 4) — BEFUND
Die Plattendrehung je Knoten ist so gewaehlt, dass der groesste Winkelfehler halbiert wird (`x_richtung`). Danach wird jeder Arm um seine Plattenschraube auf die echte Richtung gedreht; dabei wandert die Rohrachse vom Knotenpunkt weg.
| Wertigkeit | Knoten | groesste Drehung um die Plattenschraube | groesster Achsversatz |
|---|---|---|---|
| 4 | 10 | 1,7 Grad | 1,11 mm |
| 5 | 6 | 24,0 Grad | **15,07 mm** (n02) |
| 6 | 10 | 1,7 Grad | 1,12 mm |
Befehl: `python -X utf8 scripts/workshop/knoten_schere.py --table` (Ergebnis in `data/components/knoten_schere.json` → `auswertung`).
**Sollwert 5 mm ueberschritten, nur bei den 6 fuenfwertigen Knoten:** Ihre Arme stehen im 72-Grad-Raster, die Platte hat ein 60-Grad-Raster. Variante zur Entscheidung (nicht gebaut, Blatt: melden statt umbauen): eine zweite Platte mit 5 Loechern im 72-Grad-Raster fuer die 6 fuenfwertigen Knoten. Dann liegen alle Knoten bei hoechstens 1,1 mm. Die 4-wertigen Basisknoten passen auf die 6-Loch-Platte (1,1 mm).

## Pruefung (05.11.2026)
`python -X utf8 scripts/workshop/check_knoten_schere.py` → Ergebnis siehe Paket `docs/packages/n-verbinder.md` Abschnitt Stand. Prueft:
1. Platte, Arm A, Arm B: alle Koerper geschlossen; Nasenspitze = Rohraussenradius + 3 mm (+-0,05); Rohrachse durch den Knotenpunkt (aus der Zylinderflaeche gemessen, <= 0,01 mm); Neigung A/B; Oberseite Lasche 2 = Plattenunterkante.
2. Probe-Knoten n01 (1 Platte + 6 verknuepfte Arm-Instanzen, gedreht wie in der Tabelle, Datei nur im Arbeitsordner): `inspect.interference` ohne Durchdringung ueber 0,1 mm3.
3. Tabelle: 26 Knoten an den Lagen aus `data/layout.json`, Armzahl = Wertigkeit (10 x 4, 6 x 5, 10 x 6), 130 Arme, A 60 / B 70, kein Loch doppelt belegt.
4. Groesster Achsversatz (Befund-Zeile, kein Fehler).
Teiledaten: `python -X utf8 scripts/workshop/check_parts.py knoten_schere` → 22/22.

## Bilder `renders/components/knoten_schere/` (angesehen, gegen das Foto verglichen)
1. `knoten_schere-01-knoten-n01-iso.png` — ganzer 6-wertiger Knoten n01 schraeg von oben
2. `knoten_schere-02-knoten-n01-draufsicht.png` — von aussen: 6 Plattenschrauben, je Arm eine Drehpunktschraube am Rohrmund, Nasen seitlich am Rohr (wie Foto links)
3. `knoten_schere-03-knoten-n01-seite.png` — Seite: Streben nach innen geneigt
4. `knoten_schere-04-explosion-iso.png` — Explosion: Platte mit Schraube, Lasche 1 und 2 mit Nasen und Knick, Drehpunktschraube, Rohr mit Gegenloch
5. `knoten_schere-05-explosion-draufsicht.png` — Explosion von oben: beide Laschen mit Nase nebeneinander
6. `knoten_schere-06-nase-detail.png` — Nase im Gegenloch (Rohr durchsichtig)
7. `knoten_schere-07-arm-b-seite.png`, `knoten_schere-08-arm-a-seite.png` — Knick B 18,0 Grad gegen A 15,9 Grad
**Bildvergleich mit dem Foto:** Draufsicht zeigt dieselbe Ordnung wie das Foto (Platte innen, Schraubenkranz, Drehpunktschraube kurz vor dem Rohrmund, nur EINE Laschenbreite sichtbar). Unterschiede: Foto-Platte wirkt groesser im Verhaeltnis; Foto zeigt Flanschschrauben statt Sechskant mit Scheibe; im Foto ist kein Knick zu sehen (flach liegender Knoten, Chemnitz vermutlich flacher). Der fremde Pruefer vergleicht danach.

**Viewer-Detailansicht:** `http://localhost:4410/#detail=knoten_schere` (Teiledaten `data/parts/knoten_schere.json`, Modell `python viewer/export_detail.py knoten_schere`; das Bauteil steht nicht im Gesamtmodell, darum nur ueber diesen Link).

## Montageschritte (je Strebenende)
1. Schere offen (Augen etwa 6,5 Grad je Seite auseinander) ins Rohr schieben, bis die Nasen vor den Gegenloechern stehen.
2. Augen zusammenfuehren: die Nasen rasten in die Gegenloecher.
3. Augen von unten an das Plattenloch der Tabelle legen, M10 von oben mit Scheibe, unten Scheibe und Mutter; locker lassen.
4. Wenn alle Streben eines Knotens sitzen: Streben ausrichten (Drehung um die Plattenschraube), Plattenschrauben anziehen.
Werkzeug: 2 Ringschluessel SW 16 (M10) und SW 13 (M8). Gegenloecher mit Bohrlehre (Prisma) bohren.

## Vorentwurf
`knoten_schere_proto` (Commit 927d171) ist geloescht: Er hatte die Platte unter den Laschen, nur Arm B und keine gemeinsame Plattenhoehe fuer A und B; zwei Modelle desselben Teils wuerden Montage und Pruefer verwirren. Der Stand bleibt in Git (927d171) erhalten.

## Offen (Ben)
1. Lesart der Funktion: Augen deckungsgleich verschraubt = Nasen aussen (R56 Abschnitt 1).
2. Rohr Rund 42,4 x 2,6 statt Vierkant 30 x 30 x 3 (Schere passt nicht in 30 x 30 x 3).
3. Laschendicke 5 oder 8 mm (Parameter `link_t`; Knick traegt 4,6 gegen 11,8 kN).
4. Keilschiene der Folie auf Rundrohr: Sattel oder Schaumband.
5. **Neu:** Lochbild der 5-wertigen Knoten: zweite Platte mit 5 Loechern (72 Grad), sonst 15 mm Achsversatz.
