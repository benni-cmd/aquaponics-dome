# Work package: dome-build

**Problem:** Es gibt vier Referenzbilder einer Geodaetischen Kuppel mit Aquaponik-System (aus Blender), aber kein parametrisches CAD-Modell davon.
**Intent:** Ein sauberes, parametrisches SolidCraft-Modell, aus dem sich Teile, Masse und Varianten ableiten lassen; Claude baut es per MCP und verfeinert es in einer Schleife gegen die Referenzen.
**Goal:** `designs/dome.sc` enthaelt alle Teile der Teileliste (v1-Umfang) als benannte, parametrisierte Bauteile; der Screenshot aus der Kamera von `ref-4-dome-clean.jpg` stimmt in Gruppierung, Anzahl und Proportionen mit der Referenz ueberein (Latte unten).

## Quellen

1. `reference/ref-4-dome-clean.jpg` — Hauptreferenz: saubere Ansicht der Kuppel mit Innenleben
2. `reference/ref-1-blender-views.jpg` — Blender-Ansichten, gleiche Kuppel, zwei Perspektiven
3. `reference/ref-2-site-with-solar.jpg`, `ref-3-site-trees.jpg` — Umgebung (Fluss, Wehr, Solarfeld); v1 ausserhalb

## Teileliste (aus den Bildern erkannt; Masse = Annahmen, an Referenz zu kalibrieren)

| # | Teil | Beobachtung | Annahme |
|---|---|---|---|
| T1 | Kuppelgeruest | Geodaetisch, Streben aus Metallprofil, 5 Streben am Scheitel (ikosaedrisch), flache Kuppel (ca. 5/8-Kugel) | Durchmesser 7 m, Hoehe 3,5 m, Frequenz 3V, Rundstab 40 mm |
| T2 | Kuppelhaut | transparent, dreieckige Felder (Glas/Folie) | spaeter, v1 nur als duenne Flaechen optional |
| T3 | Sockel | zehneckiger Betonring unter der Kuppel | Hoehe 0,4 m, Breite 0,5 m |
| T4 | Tuer | schwarzer Rahmen, verglast, vorne rechts im Sockelring | 0,9 x 2,0 m |
| T5 | Zentraltank | grosser runder gruener Fischtank, Mitte | Durchmesser 2,6 m, Hoehe 0,9 m |
| T6 | Mitteltank | flacher runder Tank vor dem Zentraltank | Durchmesser 1,4 m, Hoehe 0,7 m |
| T7 | Fass-Tanks | 6 zylindrische gruene Tanks auf Staendern (je 2 links, mitte, rechts) | Durchmesser 0,7 m, Hoehe 1,0 m, Staender 0,4 m |
| T8 | Anbaubetten-Ring | weisse Hydroponik-Tische mit Pflanzloechern in Reihen, ringfoermig um die Mitte, ca. 10 Segmente | je 1,6 x 0,5 m, Hoehe 0,9 m, Reihen mit Netztopf-Loechern |
| T9 | Substratbeete | 2 weisse Wannen mit Erde und Gemuese (vorne links, vorne rechts) | 1,5 x 0,6 m, Hoehe 0,4 m |
| T10 | Zulaufrohr | blaues Rohr kommt von aussen (Wehr) schraeg durch die Kuppel | Durchmesser 0,2 m |
| T11 | Schaltschrank | graue Box aussen am Sockel | 0,5 x 0,3 x 0,8 m |

**Phase 2 (nicht v1):** Pflanzen als Mesh, Wasserflaechen, Wehr und Fluss, Solarfeld (5 Module), Gelaende, Baeume.

## Plan

1. [x] Sitzung in diesem Repo: SolidCraft-MCP pruefen, Parameter-Tabelle (Durchmesser, Hoehe, Frequenz) anlegen
2. [x] Geruest T1 + Sockel T3 + Tuer T4 bauen, Screenshot, gegen `ref-4` pruefen
3. [x] Tanks T5-T7 bauen, pruefen
4. [x] Anbaubetten-Ring T8 + Substratbeete T9, pruefen
5. [x] Rohr T10 + Schaltschrank T11, pruefen
6. [~] Verfeinerungsschleife (4 von 8 Runden, siehe docs/loop-log.md) (Latte unten), je Runde in `docs/loop-log.md` protokollieren
7. [~] (STEP + Renders da, Schluss-Push nach Klaerung Bett/Tuer) Export `designs/dome.step`, Render-Screenshots in `renders/`, committen und pushen

## Verfeinerungsschleife (Latte)

Jede Runde: bauen -> Screenshot aus Kamera wie `ref-4` -> Referenz und Screenshot nebeneinander ansehen -> Abweichungen in Zahlen auflisten -> beheben. Abbruch, wenn alle sechs Punkte stimmen oder nach 8 Runden (dann Rest als Offen listen):

1. Geruest: gleiche Zahl Streben-Ebenen, 5 Streben am Scheitel
2. Sockel hat 10 Seiten, Tuer an derselben Stelle (vorne rechts)
3. Tank-Gruppierung: 1 grosser Zentraltank, 1 Mitteltank, 6 Fass-Tanks, gleiche Anordnung
4. Anbaubetten: 10 Segmente ringfoermig, Reihen mit Pflanzloechern
5. Hoehen-Breiten-Verhaeltnis der Kuppel stimmt auf 10 % mit der Referenz
6. Alle Teile haben Namen T1-T11 im Design und liegen im richtigen Verhaeltnis zueinander (keine Durchdringungen ausser Rohr durch die Haut)

## Kalibrierte Masse (Aenderungen gegenueber den Annahmen)

Kuppel 5/8-3V, Basis-D 7,0 m, Hoehe 4,2 m (statt 3,5; Verhaeltnis 0,6 wie Bild) · Zentraltank D2,4 · Mitteltank D1,2 · Betten r=2,85 m, 1,5x0,7 m, 2x4 Loecher · Substratwanne 1,5x0,56x0,4 · Rohr aus Westen. Streben als Einzelkoerper T1_Strebe_nnn (157, 8 im Tuerbereich entfallen). Bauweise: `scripts/build.sh`, Parameter in `scripts/gen_dome.py` (Tabelle `P`; Tank-/Bett-Masse als Parameter-Ausdruecke im Design, Strebenpositionen numerisch aus dem Skript).

## Status

29.10.2026 — Stufen 1-4 gebaut, STEP exportiert, Latte 1-5 erfuellt, 6 offen (Bett 09 vor der Tuer). Repo angelegt, Teileliste aus den vier Bildern erstellt. Masse sind Annahmen; echte Masse fehlen.

## Definition of Done

Geprueft gegen: Screenshot gegen `reference/ref-4-dome-clean.jpg` (Latte 1-6), `designs/dome.sc`, `git log`
Offen: Schritte 1-7; echte Masse (DEINE ENTSCHEIDUNG, falls bekannt)
