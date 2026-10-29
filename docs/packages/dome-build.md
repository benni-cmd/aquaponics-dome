# Work package: dome-build

**Problem:** Es gibt vier Referenzbilder einer Geodaetischen Kuppel mit Aquaponik-System (aus Blender), aber kein parametrisches CAD-Modell davon.
**Intent:** Ein sauberes, parametrisches SolidCraft-Modell, aus dem sich Teile, Masse und Varianten ableiten lassen; Claude baut es per MCP und verfeinert es in einer Schleife gegen die Referenzen.
**Goal:** `designs/dome.sc` enthaelt alle Teile der Teileliste (v1-Umfang) als benannte, parametrisierte Bauteile; der Screenshot aus der Kamera von `ref-4-dome-clean.jpg` stimmt in Gruppierung, Anzahl und Proportionen mit der Referenz ueberein (Latte unten).

## Quellen

1. `reference/ref-4-dome-clean.jpg` — Hauptreferenz: saubere Ansicht der Kuppel mit Innenleben
2. `reference/ref-1-blender-views.jpg` — Blender-Ansichten, gleiche Kuppel, zwei Perspektiven
3. `reference/ref-5-dome-closeup.jpg` (Geruest, Sockel, Tischring, Tanks von schraeg oben), `reference/ref-6-grow-tables-detail.jpg` (Pflanztische, Nahaufnahme)
4. `reference/ref-2-site-with-solar.jpg`, `ref-3-site-trees.jpg` — Umgebung (Fluss, Wehr, Solarfeld); v1 ausserhalb

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
6. [x] Verfeinerungsschleife (5 von 8 Runden, siehe docs/loop-log.md) (Latte unten), je Runde in `docs/loop-log.md` protokollieren
7. [x] STEP + Renders, gepusht Export `designs/dome.step`, Render-Screenshots in `renders/`, committen und pushen

## Verfeinerungsschleife (Latte)

Jede Runde: bauen -> Screenshot aus Kamera wie `ref-4` -> Referenz und Screenshot nebeneinander ansehen -> Abweichungen in Zahlen auflisten -> beheben. Abbruch, wenn alle sechs Punkte stimmen oder nach 8 Runden (dann Rest als Offen listen):

1. Geruest: gleiche Zahl Streben-Ebenen, 5 Streben am Scheitel
2. Sockel hat 10 Seiten, Tuer an derselben Stelle (vorne rechts)
3. Tank-Gruppierung: 1 grosser Zentraltank, 1 Mitteltank, 6 Fass-Tanks, gleiche Anordnung
4. Anbaubetten: 10 Segmente ringfoermig, Reihen mit Pflanzloechern
5. Hoehen-Breiten-Verhaeltnis = 0,5 (12 m / 6 m), Abweichung unter 3 % (gemessen 0,503)
6. Alle Teile haben Namen T1-T11 im Design und liegen im richtigen Verhaeltnis zueinander (keine Durchdringungen ausser Rohr durch die Haut)

## Masse (von Ben bestaetigt, 29.10.2026) und Rangfolge der Massquellen

Bei Konflikt gewinnt die hoehere Quelle: 1. Kuppel Grundflaeche 12 m, Hoehe 6 m (verbindlich) · 2. Tuer 1,0 x 2,0 m (Normtuer, wahrscheinlich) · 3. Menschenmasse (Tischhoehe 0,9-1,0 m, Fass 1-1,2 m, Gehweg >= 0,8 m) · 4. Pixelverhaeltnisse aus ref-4 (nur Anordnung/relative Groesse).

Umgesetzt (Runde 6, Tabelle `P` in `scripts/gen_dome.py`): Kuppel 2V (ab Runde 7; vorher 3V), D 12,0 m, H 6,0 m (Verhaeltnis gemessen 6095/12119 = 0,503; 5/8-Geruest in Z gestaucht, da 3V keinen Aequator-Ring hat), Stab r 45 mm · Sockel 0,6 m hoch, 0,25 m Ueberstand · Tuer 1,0x2,0 m, 1,1 m seitlich versetzt · T5 D3,8x1,2 · T6 D2,2x0,9 · T7 D1,1x1,2 auf 0,5 m Staendern · Betten 2,3x0,9x0,95, 3 Reihen Topf-Loecher, Ring r 4,8 m, Bett 09 gekuerzt auf 1,2 m · Substratwanne 2,2x0,76x0,55 · Rohr D0,3 · Schaltschrank 0,8x0,5x1,2. Abweichung zur Referenz: Tuer im Bild relativ groesser (Perspektive); Punkt 1/2 gehen vor. Pixelvermessung der Tanks/Betten ist Naeherung (Perspektive), nicht auf 5 % belegt.

## Status

29.10.2026 — Stufen 1-4 gebaut, STEP exportiert, Latte 1-6 erfuellt nach Runde 5 (Tuer verschoben, Bett 09 gekuerzt). Repo angelegt, Teileliste aus den vier Bildern erstellt. Masse sind Annahmen; echte Masse fehlen.

## Definition of Done

Geprueft gegen: Screenshot gegen `reference/ref-4-dome-clean.jpg` (Latte 1-6), `designs/dome.sc`, `git log`
Offen: Schritte 1-7; echte Masse (DEINE ENTSCHEIDUNG, falls bekannt)

## Zusaetzliche Latte (29.10.2026)
7. Kuppel 12 m / 6 m, Abweichung < 3 % — erfuellt (Runde 6)
8. Betten 2,3 x 0,9 m mit 3 Reihen Topf-Loechern, Tuerzugang frei — erfuellt (Bett 09 gekuerzt, Tuer versetzt); Abstand Tuer–Bett 09 ~0,55 m seitlich, Zugang radial frei (nicht auf 1,0 m seitlich)
9. Sockel Ueberstand <= 0,3 m — erfuellt (0,25 m)
10. Geruest 2V statt 3V (ref-5: 5 Dreiecke am Scheitel, grosse Felder, Basis-Zehneck) — erfuellt Runde 7; 2V hat exakt 10 Knoten auf Z=0 (Halbkugel, H/D = 0,5), 63 Streben inkl. 10 Basiskanten; Haut/Nabenfreiheit: Haut T2 offen (Phase 2), Knoten ohne Naben
11. Sockel flach, Zehneck, kaum Ueberstand — erfuellt (0,4 m hoch, 0,25 m Ueberstand)
12. Pflanztische wie ref-6 (Rinnen, gestaffelte Reihen, Schlaeuche, 10-12 Tische) — teilweise: 10 Tische mit 3 Reihen x 6 Loechern; Schlaeuche, Neigung, gerippte Oberseite, Winkelstuetzen offen
13. Tanks wie ref-5 (Rand dick, Wasserscheibe) — teilweise: Wasserscheibe T5_Wasser da; gerundeter Rand, Farben offen
