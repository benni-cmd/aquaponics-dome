# Paket W24 — Aussentisch mit 4 statt 3 Rinnen (Werkstatt, Auftrag docs/jobs/W24-aussentisch-4-rinnen.md, Ben 30.10., D40)

## PIG
- **Problem:** Ben will mehr Pflanzflaeche (Engpass der Fischmenge). Der Aussentisch hat 3 Rinnen, die Reihen liegen auf Rinnenabstand 288 nach dem Radialbudget (Laufweg B 500,5, Kuppelhaut-Abstand 21 mm) ohne Reserve.
- **Intent:** pruefen, ob eine 4. Rinne ohne Laufweg-B-Verlust, ohne Kollision mit Beinen und Kuppelhaut passt; Entscheidungsgrundlage mit Zahlen, keine Platzierung im Dom.
- **Goal:** Variante `aussen4` als Parameter-Konfiguration in `data/components/nft_tisch.json` (Standard bleibt `aussen`); `check_nft_fit.py` rechnet beide Varianten PASS; Querschnittsbild; Kurzbericht.

## Ergebnis (gemessen: `python scripts/workshop/check_nft_fit.py`)
| | Standard aussen | aussen4 |
|---|---|---|
| Rinnen je Tisch / Aussenring | 3 / 24 | 4 / 32 (gesamt 68 -> 76) |
| Rinnenabstand | 288 | **220** (Jobblatt 230-240 siehe unten) |
| Reihengruppe gegen Tischmitte | 0 | **+42 mm nach innen** (`reihen_versatz`) |
| Reihen (Apothem) | 5162 / 4874 / 4586 | 5162 / 4942 / 4722 / 4502 |
| Rinnenlaenge je Reihe | 2986 / 2799 / 2612 | 2986 / 2844 / 2701 / 2558 |
| Rinnenlaenge je Tisch / Aussenring | 8397 / 67 176 mm | 11 089 / 88 712 mm (gesamt aller Ringe 126 312 -> 147 848 mm) |
| Topfloecher je Tisch (Pitch 200) | 14 / 13 / 13 = 40 | 14 / 14 / 13 / 12 = 53 |
| Topfloecher gesamt (innen 70 + mitte 180 + aussen) | 570 | **674 (+104, +18 %)**; Netztoepfe gesamt 2730 -> 2834 |
| Rinnenband / Tischbreite ueber die Beine | 706 / 1030 | 790 / 1030 (Portal unveraendert) |
| Kuppelhaut-Abstand Rinnenende | 21 mm | 21 mm (aeusserste Reihe bleibt auf Ap 5162) |
| Laufweg B / Wandluft | 500,5 / 317 | 500,5 / 317 (unveraendert) |
| Rinnenkante innen gegen Beininnenflaeche 460 | 353 (Luft 107) | 437 (Luft 23, Soll >= 15) |
| entfernteste Reihe vom Laufweg B (Portalrand 4359) | 803 | 803 (die neue Reihe liegt naeher) |

## Warum 220 und Versatz +42 (und nicht 230-240 symmetrisch)
Gerechnet mit `tisch_geom.geometry` und den Feldebenen (Skriptlauf am 30.10., Ap_c 4874 fest):
- **Symmetrisch um die Tischmitte** (Rinnenabstand 220-240): die aeusserste Reihe wandert nach aussen (Ap 5204-5227), Kuppelhaut-Abstand -20 (220) bis -50 mm (240): Kollision. Ap_c nach innen schieben macht Laufweg B kleiner als 500 (4850: 476,5). Keine Loesung.
- **Aeusserste Reihe wie im Standard lassen** (Ap 5162, Abstand 21 mm) und die Gruppe um 42 mm nach innen versetzen: Reihen y = -288 / -68 / 152 / 372; die innerste Rinnenkante liegt bei 437, die Beininnenflaeche bei 460 (Luft 23 mm). Rinnenabstand 230 gaebe y = 402, Kante 467 gegen 460: die Rinne stiesse an das Bein. 225 liesse nur 8 mm Luft. Daher 220.
- Rinnen 130 breit, Luft zwischen Rinnen 90 mm; Salatkopf 100 mm Durchmesser, Zickzack pitch/2: kleinster Abstand Topf zu Topf der Nachbarreihe sqrt(220^2 + 100^2) = 242 mm > Kopf 100: Querabstand der Pflanzen kein Problem (Annahme: Kopfbreite 100 aus salatkopf.json, Streuung der Pflanzen nicht modelliert).

## Erreichbarkeit und Statik (Abschaetzung, Annahmen A)
- Erreichbarkeit: die entfernteste Reihe liegt wie im Standard 803 mm vom Portalrand (Laufweg-B-Seite) auf Rinnenhoehe 1,3 m, die 4. Reihe liegt naeher. Gegen die 800-mm-Regel (D29, gilt fuer Beete einseitig) ist das knapp ueber 800 bis zur Rinnenmitte; Wert gilt schon fuer den Standard, Ben entscheidet.
- Statik: Annahmen Wasserfilm 25 mm (3,25 kg/m), Rinne 1,2 kg/m, Pflanze+Topf 0,4 kg: Standard ca. 53 kg, aussen4 ca. 70 kg je Tisch (+17 kg). Holm 40 x 60 (Wandstaerke 3 angenommen) ueber 960 mm Spannweite, 35 kg je Holm verteilt: Biegespannung ca. 5 MPa gegen 235 MPa; Beine 40 x 40 x 3 mit ca. 18 kg je Bein: weit unter Knicklast. Keine rechnerische Statik, Befuellungsschwankung, Wind und Einschaltstoss nicht betrachtet.

## Was NICHT getan ist (offen)
- Kein CAD-Bau der Variante: `nft_tisch.py`/`check_nft_tisch.py` kennen den Versatz (`G["ymid"]`) noch nicht (Zulaufverteiler/Sammelrohr nutzen `+-Wt/2`); `rinnen_reihen.py aussen4` und `nft_tisch_aussen4.sc` entstehen erst, wenn Ben die Variante waehlt.
- Keine Platzierung in `dome.sc` (Montage); keine Aenderung von Layout-Radien und Beeten. Kein Pruefer-Lauf (Auftrag).
- Entscheidung Ben/Orchestrator: Standard 3 Rinnen (570 Toepfe, Luft 107 zu den Beinen) oder aussen4 (674 Toepfe, 23 mm Luft zu den Beinen, Rinnenabstand 220 statt 288).

## Stand
30.10.: Variante in `nft_tisch.json`, `tisch_geom.geometry` (`reihen_versatz`), `check_nft_fit.py` (beide Varianten, Pruefzeile Rinnenkante-Bein) fertig: Standard 47/47 PASS, aussen4 48/48 PASS. Bild `renders/components/nft_passung/aussen4-querschnitt.png` (`render_aussen4_schnitt.py`, im Bildverlauf).

## DoD
check_nft_fit beide Varianten PASS (erfuellt), Querschnitt im Bildverlauf (erfuellt), Kurzbericht (diese Datei), Fertigmeldung und Stand (nachgefuehrt).
