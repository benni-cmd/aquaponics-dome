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

## Verfeinerungsschleife v3 (Detail-Schichten)

Pro Schicht: bauen -> `python scripts/check_latte.py` (muss PASS bleiben) -> Screenshot -> Commit+Push. Abbruch: alle Schichten durch oder zwei ohne sichtbare Verbesserung.
- [x] 1 Farben/Materialien je Teil · [ ] 2 Pflanzen (Salatkoepfe, 3 gestaffelte Reihen; Substratwannen) · [ ] 3 Tankraender gerundet, Wasserflaeche blau · [ ] 4 Schlaeuche/Rohr sauber verlegt · [ ] 5 Haut T2 transparent (falls moeglich) · [ ] 6 Rippen/Neigung der Tische
Latte 1-13 (Mass-Pruefung) gelten als erfuellt: `check_latte.py` 23/23 PASS. Photoreal: img2img gescheitert (`renders/failed-photoreal-01.png`), noetig ControlNet (Canny/Depth), nach den Schichten.

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
12. Pflanztische wie ref-6 — weitgehend erfuellt (Runde 8): 10 Tische, 3 gestaffelte Reihen x 6 Loecher, 4 Substratwannen, 6 Schlaeuche (T10_Schlauch_n) von Fasstanks zum Zentraltank; offen: Neigung, gerippte Oberseite, Winkelstuetzen, Schlaeuche zwischen Tischen, 10-12 Tische bleibt bei 10 (Tuer)
13. Tanks wie ref-5 — weitgehend erfuellt (Runde 8): Wand 160 mm, Wasserscheibe T5_Wasser, 6 Fasstanks + Mitteltank; offen: gerundeter Rand, Farben (SolidCraft-Aussehen nicht gesetzt)

## Bauteil-Katalog (wiederkehrend, Anzahl) — Komponenten-Umbau
Wahl: echte Instanzen via `component.insert_design` (+ `occurrence.move`), Bauteile in `designs/components/<name>.sc`. Reihenfolge: Pflanztisch (ref-6) -> Salatkopf -> Fasstank (ref-5) -> Zentralpool + Mitteltank -> Substratwanne -> Strebe/Knoten -> Tuer -> Schlauch/Rohr -> Haut T2.
| Bauteil | Anzahl | Referenz |
|---|---|---|
| Strebe | 63 | ref-5 |
| Pflanztisch T8 | 10 | ref-6 |
| Fasstank T7 | 6 | ref-5 |
| Zentralpool T5 / Mitteltank T6 | 1 / 1 | ref-5 |
| Substratwanne T9 | 4 | ref-6 |
| Salatkopf | 210 | ref-6 |
| Schlauch T10 | 6 | ref-6 |
| Tuer T4 / Rohr T10 / Schaltschrank T11 | 1 / 1 / 1 | ref-5 |
