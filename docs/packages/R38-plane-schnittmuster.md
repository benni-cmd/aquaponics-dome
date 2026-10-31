# Arbeitspaket R38: Plane — moeglichst simples Schnitt- und Nahtmuster

**Problem:** Die Huelle ist eine Plane (D39): im Modell eine Folie je Dreiecksfeld, aber ohne Schnittmuster, Nahtfuehrung und Bahnenaufteilung. Ben (D64, 31.10.): das Muster muss moeglichst simpel sein.
**Intent:** Ein Laie soll die Plane nach Bauplan zuschneiden und verbinden koennen; wenige verschiedene Zuschnitte, wenige und kurze Naehte, wenig Verschnitt.
**Goal:** `docs/research/R38.md` (Variantenvergleich mit Zahlen, Empfehlung, Bauanleitungs-Abschnitt B10), `scripts/plane_nesting.py` (reproduzierbare Rechnung), `data/plane-zuschnitt.json`, Schnittmuster-SVG unter `docs/plane/`. Das Modell bleibt unveraendert.

## Plan

1. [x] Auftrag, R24, Bauteilblaetter huelle_folie/keilschiene, Layout und Felddaten gelesen
2. [x] Web: Rollenbreiten, Nahttechnik, Kanal/Lagen, Aufblasen (je Zahl zwei Quellen angestrebt)
3. [x] `scripts/plane_nesting.py`: Geometrie, Abwicklung, Einheiten (Dreieck, Raute, Sektor), Kennzahlen, Nesting
4. [x] `data/plane-zuschnitt.json` und SVG unter `docs/plane/` erzeugen
5. [x] `docs/research/R38.md` schreiben (Tabelle, Empfehlung, Quellen, Konfidenz, Bauanleitung B10)
6. [x] Committen mit Pfad, pushen

## Status

31.10.2026 — Rechnung (`scripts/plane_nesting.py`, Selbsttest 21/21), `data/plane-zuschnitt.json`, 5 SVG unter `docs/plane/` und `docs/research/R38.md` liegen vor und sind gepusht. Empfehlung V2: 20 Rautenkissen, 40 Zuschnitte (Z1 x10, Z2 x10 davon 1 mit Tuerausschnitt), 287,9 m Umfangsnaht, Rolle 8 m x 38,2 m je Lage (Verschnitt 21,9 %).

## Definition of Done

Geprueft gegen: Lauf von `python scripts/plane_nesting.py` (Kennzahlen, Selbsttests), Flaechensumme gegen R24 (208 m2), Sichtpruefung der SVG
Offen:
1. Probeschweissung 150-µm-PE mit Heizkeil-Geraet (Parameter, Abschaelprobe) — DEINE HANDLUNG (Ben), vor dem Rollenkauf
2. Entscheidung V2 gegen V1/V3 — DEINE ENTSCHEIDUNG
3. Modell umstellen (20 Kissen statt 40 Folien, 45 statt 65 Schienen, Doppelschiene an Fugen) — Werkstatt/Montage nach Entscheidung
4. Leckrate, Tuellenlage, Abdichtung am Tuerausschnitt, Bodenbefestigung — Montage/Werkstatt
