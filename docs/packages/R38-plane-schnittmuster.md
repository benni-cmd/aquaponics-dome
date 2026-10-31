# Arbeitspaket R38: Plane — moeglichst simples Schnitt- und Nahtmuster

**Problem:** Die Huelle ist eine Plane (D39): im Modell eine Folie je Dreiecksfeld, aber ohne Schnittmuster, Nahtfuehrung und Bahnenaufteilung. Ben (D64, 31.10.): das Muster muss moeglichst simpel sein.
**Intent:** Ein Laie soll die Plane nach Bauplan zuschneiden und verbinden koennen; wenige verschiedene Zuschnitte, wenige und kurze Naehte, wenig Verschnitt.
**Goal:** `docs/research/R38.md` (Variantenvergleich mit Zahlen, Empfehlung, Bauanleitungs-Abschnitt B10), `scripts/plane_nesting.py` (reproduzierbare Rechnung), `data/plane-zuschnitt.json`, Schnittmuster-SVG unter `docs/plane/`. Das Modell bleibt unveraendert.

## Plan

1. [x] Auftrag, R24, Bauteilblaetter huelle_folie/keilschiene, Layout und Felddaten gelesen
2. [x] Web: Rollenbreiten, Nahttechnik, Kanal/Lagen, Aufblasen (je Zahl zwei Quellen angestrebt)
3. [ ] `scripts/plane_nesting.py`: Geometrie, Abwicklung, Einheiten (Dreieck, Raute, Sektor), Kennzahlen, Nesting
4. [ ] `data/plane-zuschnitt.json` und SVG unter `docs/plane/` erzeugen
5. [ ] `docs/research/R38.md` schreiben (Tabelle, Empfehlung, Quellen, Konfidenz, Bauanleitung B10)
6. [ ] Committen mit Pfad, pushen

## Status

31.10.2026 — Schritte 1 und 2 erledigt; Rechnung in Arbeit.

## Definition of Done

Geprueft gegen: Lauf von `python scripts/plane_nesting.py` (Kennzahlen, Selbsttests), Flaechensumme gegen R24 (208 m2), Sichtpruefung der SVG
Offen: (wird beim Abschluss nachgefuehrt)
