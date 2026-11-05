# Auftragsblatt N-VERBINDER: Scherenknoten als EIN Bauteil (W74)

**Problem:** Das Modell verbindet die 65 Streben mit Kugelknoten D100, Steckarm 23 x 23 und Querbolzen (`docs/parts/knoten.md`). Das echte Verbindungsstueck (Foto `reference/chemnitz/laschenknoten-foto.jpg`) ist ein Scherenknoten: Lochplatte, je Strebe eine Schere mit zwei Nasen durch zwei Gegenloecher im Rohr.
**Intent:** Ben soll den echten Verbinder im Modell sehen und abnehmen koennen, bevor die Montage 26 Knoten tauscht.
**Ziel in einem Satz:** Die Werkstatt baut den Scherenknoten EINMAL als Bauteil (Lochplatte, Schere, Rohrende), so dass die Montage nur Instanzen an die 26 Knotenpunkte setzt und Strebenzahl und Winkel allein ueber Zahl und Drehung der Scheren um die Plattenschraube einstellt.

## Aktualitaetspruefung (05.11.2026)
**Angepasst, Plan gilt als freigegeben.**
1. Roadmap `data/roadmap.json` Eintrag N-VERBINDER (Commit b63c92e): KEINE Serie; Knoten einmal bauen, Montage setzt Instanzen, Strebenzahl und Winkel ueber Scherenzahl und Drehung (Ben 05.11.). Das ersetzt die fruehere Lesart „Prototyp, dann Serie" im Start-Prompt.
2. Ben 05.11. mittags: Recherche, Planer und Werkstatt getrennt. Die Planer-Sitzung hat vor dieser Nachricht bereits einen Vorentwurf gebaut und gepusht (Commit 927d171): `designs/components/knoten_schere_proto.sc`, `scripts/components/knoten_schere_proto.py`, `docs/parts/knoten_schere_proto.md`, 5 Bilder unter `renders/components/knoten_schere_proto/`. **Status: Vorentwurf, keine Werkstatt-Abnahme.** Die Werkstatt darf Geometrie und Skript uebernehmen, baut aber das Bauteil nach diesem Blatt neu und entscheidet, ob der Vorentwurf geloescht wird (Commit mit Begruendung).
3. Letzte Entscheidungen D85 bis D87 betreffen den Verbinder nicht. Strebenprofil im Modell: 30 x 30 x 3 (`docs/parts/strebe.md`, Wand 3 mm entschieden 05.11. bis N-STATIK).

## Eingaben (nur diese lesen)
1. `docs/research/R56-scherenknoten.md` Abschnitte 1 bis 4 (Funktion, Masse [A], Rund gegen Vierkant, Statik) und 6 (offene Fragen).
2. `scripts/r56_scherenknoten.py` (Neigung, Rohrlaengen, Einziehwinkel der Nasen; `python -X utf8 scripts/r56_scherenknoten.py`, Selbsttest 6/6).
3. `scripts/components/knoten_schere_proto.py` (Vorentwurf: Laschen mit Knick, Nasen, Wandloecher, Normteile, Check, Render).
4. `docs/parts/knoten-ports.md` und `data/components/knoten_arme.json`: Armrichtungen u je Knoten (Drehwinkel der Scheren daraus berechnen).
5. `docs/cad-standard.md`, `docs/detail-standard.md` (Werkstatt-Pflicht); Foto `reference/chemnitz/laschenknoten-foto.jpg` nur fuer den Bildvergleich.

## Bauteil-Aufbau (Vorgabe)
1. **`designs/components/knoten_schere_platte.sc`:** Lochplatte D 110 x 8, 6 Loecher D 11 auf Lochkreis r 37, Mittelbohrung D 20 [A, R56]. Eine Datei fuer alle 26 Knoten.
2. **`designs/components/knoten_schere_arm_a.sc` und `_b.sc`:** je eine Schere (2 Laschen, Drehpunktschraube M8, Plattenschraube M10 mit Scheiben und Mutter) plus Rohrende (Probestueck 250 mm) mit zwei Gegenloechern, Nasen ausgefahren. A und B unterscheiden sich NUR im Knickwinkel (A 15,9 Grad, B 18,0 Grad, asin(L/2R)). Bezugspunkt = Knotenpunkt, Plattenschraube auf +X (r 37), so dass die Montage die Instanz nur um die Plattennormale dreht.
3. **Scherenzahl und Drehung:** Die Montage setzt je Knoten 1 Platte und 4, 5 oder 6 Arme. Drehwinkel je Arm = Azimut der Armrichtung u in der Plattenebene. Die Werkstatt liefert `data/components/knoten_schere.json` mit je Knoten: Plattenlage (Ursprung, Normale), je Arm Typ A/B, Drehwinkel, Lochnummer.
4. **Lochbild-Frage:** Die 6 Loecher liegen im 60-Grad-Raster; die echten Armrichtungen weichen bis 24 Grad davon ab (R41). Die Werkstatt misst je Arm den Achsversatz zum Knotenpunkt, wenn die Schere um ihre Plattenschraube auf die echte Richtung gedreht wird, und meldet den Groesstwert. Liegt er ueber 5 mm: Variante „Lochbild je Knotentyp" (3 Platten) als Befund melden, NICHT selbst umbauen.
5. **Profil-Parameter:** Rohr aussen/Wand und Laschendicke als Parameter in `data/components/knoten_schere.json`; Standard Rund 42,4 x 2,6 und Lasche 20 x 5 laut R56 bis zur Entscheidung (siehe OFFEN).

## Schritte (einzeln committbar)
1. Generator `scripts/workshop/knoten_schere.py` + Parameter `data/components/knoten_schere.json` (aus dem Vorentwurf ableiten).
2. Platte und Arm A/B bauen, Check `scripts/workshop/check_knoten_schere.py`.
3. Probe-Zusammenbau EINES 6-wertigen Knotens (n01) aus 1 Platte + 6 Armen in einer Scratchpad-Szene: nur fuer Bild und Kollision, nicht ins Gesamtmodell.
4. Bilder `renders/components/knoten_schere/`: drei Richtungen (iso, Draufsicht, Seite), Explosionsbild (Platte, Laschen, Schrauben, Rohr auseinandergezogen), Nasen-Detail; Detailansicht im Viewer nach `docs/detail-standard.md`.
5. Bauteilblatt `docs/parts/knoten_schere.md`; Vorentwurf `knoten_schere_proto*` loeschen oder als Vorentwurf belassen (begruenden).

## Pruefpunkte (fremd nachmessbar)
1. `python -X utf8 scripts/workshop/check_knoten_schere.py` Exit 0: alle Koerper geschlossen, Nasen reichen Rohraussenradius + 3,0 mm (+-0,05), Rohrachse durch den Knotenpunkt fuer A und B (Abstand <= 0,01 mm bei Drehung 0).
2. `inspect.interference` im Probe-Knoten n01 (Platte + 6 Arme): 0 Durchdringungen ueber 0,1 mm3 (Gewindeberuehrung Schraube/Mutter ausgenommen).
3. `data/components/knoten_schere.json`: 26 Knoten, Armzahl je Knoten = Wertigkeit aus `data/layout.json` (10 x 4, 6 x 5, 10 x 6), 130 Arme, Typ A 60 / B 70 Enden.
4. Groesster Achsversatz nach Drehung um die Plattenschraube steht im Bauteilblatt mit Befehl; Sollwert <= 5 mm, sonst Befund.
5. Mindestens 5 Bilder unter `renders/components/knoten_schere/` inklusive Explosionsbild, optisch geprueft gegen das Foto (Pruefer vergleicht danach).

## Nicht anfassen
`scripts/gen_dome.py`, `designs/dome.sc`, `build.sh`, `docs/parts/knoten.md`, `scripts/workshop/knoten.py`, `designs/components/knoten_*_n*.sc`, `data/params.json` (Strebenprofil), `data/roadmap.json`. Kein Einbau ins Gesamtmodell: das macht die Montage nach Bens Freigabe.

## OFFEN (Ben) — Teile ohne Entscheidung werden trotzdem gebaut, als Parameter
1. Lesart der Funktion: Augen deckungsgleich verschraubt = Nasen aussen (R56 Abschnitt 1).
2. Rohr Rund 42,4 x 2,6 statt Vierkant 30 x 30 x 3 (in 30 x 30 x 3 passt die Schere nicht; R56 Abschnitt 3).
3. Laschendicke 5 oder 8 mm (Knick ist der Engpass: 4,6 gegen 11,8 kN; R56 Abschnitt 4).
4. Keilschiene der Folie auf Rundrohr: Sattel oder Schaumband.

## Ergebnis
`scripts/workshop/knoten_schere.py`, `scripts/workshop/check_knoten_schere.py`, `data/components/knoten_schere.json`, `designs/components/knoten_schere_platte.sc`, `knoten_schere_arm_a.sc`, `knoten_schere_arm_b.sc`, `renders/components/knoten_schere/`, `docs/parts/knoten_schere.md`, Viewer-Detailansicht.

## Danach
Pruefer (Bildvergleich mit dem Foto, Pruefpunkte 1 bis 5) → Ben-Abnahme → Montage setzt Instanzen an die 26 Knoten und kuerzt die Streben auf A 3076 / B 3504 (R56, nur bei Rundrohr-Entscheidung).

## Start-Hinweis fuer die Werkstatt
1. Knick der Laschen: Die innere Lasche braucht einen Biegewulst (Zylinder r 2,3 unter beiden Oberflaechen), sonst scheitert `join` an Kantenberuehrung; die aeussere Lasche bekommt 1 mm Zugabe auf beiden Seiten (Vorentwurf Zeilen mit `Knick_`).
2. `parts.insert` benennt Koerper `Body<n>` in Einfuegereihenfolge; direkt danach `body.rename`.
3. Durchsichtiges Rohr im Bild: `snapshot --body Rohrstueck:opacity=0.25`.
4. Bild-Abstand 330 mm fuer einen Arm; ganzer Knoten etwa 700 mm.
5. Leichter Lauf (unter 1 min je Bauteil); kein schwerer SolidCraft-Lauf im Sinne von D82.
