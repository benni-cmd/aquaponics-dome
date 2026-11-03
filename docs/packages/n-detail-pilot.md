# Work package: N-DETAIL-PILOT Detailansicht im Viewer (Feinfilter und Absetzer)

**Problem:** Ben kann die Funktion von Bauteilen im Viewer nicht beurteilen: Feinfilter (55 Koerper) und Absetzer (33 Koerper, davon 8 unbenannt `Body1..8`) erscheinen nur als Huellform; es gibt weder Teile-Datenmodell noch benannte Einzelkoerper im Export noch eine Detailansicht (B1 bis B3 im Gross-Paket `bauanleitung-teileliste-detailansicht.md`).
**Intent:** Ben (03.11.2026, D56): Detailansicht jetzt fertig machen, damit Filter und danach Subtank, Siphon, Pumpen nach Funktion beurteilt werden koennen; Pilot vorgezogen, voller Katalog und Gesamtansicht bleiben N-KATALOG und N-DETAIL.
**Goal:** Rechtsklick auf Feinfilter oder Absetzer, Menue "Detailansicht", Explosionsdarstellung mit Schieber, Teileliste, Klick auf Teil oder Zeile zeigt Infokarte, "Zurueck"; Detailmodell nur bei Bedarf geladen, Hauptexport waechst nicht (defs 316,4 MB +- 1 %). Blatt: `docs/jobs/N-DETAIL-PILOT.md` (Datenformat, UI, fuenf Pruefpunkte).

## Plan

1. [x] Werkstatt A (1a): `tank.py` Schrauben benennen, Material setzen, `tank_klein.sc` neu, `check_tank.py` gruen
2. [x] Werkstatt A (1b): `data/katalog.json` (Stand Pilot, nur was die zwei Bauteile brauchen)
3. [x] Werkstatt A (1c): `data/parts/feinfilter.json` und `scripts/workshop/check_parts.py` (Koerper 55, jeder genau einmal)
4. [x] Werkstatt A (1d): `data/parts/tank_klein.json` (Koerper 33)
5. [x] Viewer (2a, parallel zu 2 bis 4): `viewer/export_detail.py`, zwei Durchreichen in `serve.py` (`/parts/`, `/katalog.json`)
6. [x] Viewer (2b, nach 3): Rechtsklick-Menue, Detailszene, Schieber, Teileliste, Infokarte, Zurueck; dann tank_klein (nach 4)
7. [x] Viewer (2c): Screenshots Feinfilter und Absetzer gegen `..\..\docs\ui-standard.md`, Pruefpunkte 1 bis 5 selbst durchlaufen
8. [ ] Pruefer: `docs/jobs/pruefung/N-DETAIL-PILOT.md` nach den fuenf Pruefpunkten
9. [ ] Orchestrator: Roadmap nachfuehren, `V-MESS` hinter den Pilot, `N-DETAIL-R50` und Subtank/Siphon/Pumpen als Daten-Folgeschritte eintragen

## Status

03.11.2026: Planer-Blatt geschrieben, Aktualitaet angepasst (D75: Feinfilter wird mit M10-S2V vom Subtank abgeloest, Siebkorb-Teil bleibt wiederverwendbar). OFFEN (Ben): Biofilter (`tank_gross`) in den Pilot? (Vorschlag: nein.)

03.11.2026, Werkstatt A (Sonnet 5.5): **Schritt 1 (1a bis 1d) fertig und gepusht**, Commits 8e16da5 (1a), 2ded566 (1b), 161d9ad (1c), 6d3f691 (1d).
- 1a: `tank.py` hat `name_bolts()` (nutzt den vorhandenen Befehl `body.rename`, ordnet die 8 `Body<n>` nach Lage der Fussplatte zu, Name `Schraube_<Platte>_<x>`, Material Stahl verzinkt); `sc.py` blieb unberuehrt. `tank_klein.sc` neu: 33 Koerper, 0 Namen `Body<n>`, `check_tank.py klein` 34/34 PASS. Schraubenmasse 3 g (Default) auf 17,9 g (Stahl verzinkt); die Gesamtmasse des Absetzers steigt um etwa 0,12 kg, `docs/parts/tank.md` (37,24 kg) zieht beim naechsten `partsheet.py`-Lauf nach (nicht Teil des Piloten).
- 1b: `data/katalog.json` (`"stand": "pilot"`): 7 Werkstoffe (je mit `sc_material` = Werkstoffnamen im `.sc`), 2 Profile, 5 Rohre, 3 Normteile; `bezug: "offen (R52)"` nach D76; alle Normverweise `angenommen` (nur DIN 8062/EN 1452, EN 10088-2, DIN ISO 9044, ISO 4017 stehen im Repo, die uebrigen aus Fachwissen, nicht belegt).
- 1c/1d: `data/parts/feinfilter.json` (55 Koerper in 29 Teilen, 9 Gruppen) und `data/parts/tank_klein.json` (33 Koerper in 14 Teilen, 4 Gruppen); `scripts/workshop/check_parts.py` prueft 19 Punkte je Komponente (jeder Koerper des `.sc` in genau einer Zeile, Menge, Pflichtfelder, Werkstoff gegen Katalog UND gegen das Material im `.sc`, Explosion, `folgt`-Zyklen, Gruppen, `bezug` bei Normteil/Kaufteil) und ist gegen absichtlich eingebaute Fehler geprueft (Exit 1).
- Abweichungen vom Blatt (alle datenseitig, der Viewer muss sie kennen): (1) 29 statt rund 20 Teile beim Feinfilter (Kugelhahn und Hebel, Spannbock und Spannhebel sind eigene Koerper mit eigenem Werkstoff). (2) Neuer Typ `kaufteil` neben `profil/platte/rohr/normteil/sonderteil` (D76). (3) Zusatzfelder je Teil: `norm_konfidenz` und `lebensmittelkontakt_konfidenz` (immer `angenommen`, die Infokarte zeigt sie als Wort), `katalog` (Verweis auf `data/katalog.json`, optional), `bezug` (nur Normteil/Kaufteil), Gruppen mit `kurz`. (4) `explosion.richtung` ist ein Vektor oder `"radial"`; `folgt` nennt eine Teil-ID. Anzeigetexte stehen mit echten Umlauten (wie `descriptions.json`), IDs und Koerpernamen in ASCII.
- Bereit fuer die Viewer-Sitzung (2a bis 2c): beide `data/parts/*.json` und `data/katalog.json`; Koerpernamen im `.sc` == `koerper`-Listen (per `check_parts.py` abgesichert); Hinweis zur Optik: im Feinfilter liegen Gewebe, Staebe, Einlaufwinkel, Flansch innen und Spritzrohr im Behaelter (verdeckt, Behaelter in der Detailansicht halbtransparent zeigen); bei Schieber 1 steht der Siebkorb (Unterkante z 1315) ueber dem Deckelgriff (Oberkante z 1243), gerechnet aus bbox und Explosionswerten; `viewer/defs` unveraendert 316,4 MB.

03.11.2026, Viewer-Sitzung (Sonnet 5.5): **Schritte 2a bis 2c fertig, gepusht**, Commits 152f740 (2a: `viewer/export_detail.py`, `serve.py` +2 Durchreichen), 383a611 (2b: `viewer/index.html`).
- Bedienung: Rechtsklick auf eine Instanz (durchsichtige Treffer wie die Plane werden uebersprungen) oder Schaltflaeche "Detailansicht" im Bedienfeld nach Auswahl; Detailmodell vorher bauen: `python -I -X utf8 viewer/export_detail.py feinfilter tank_klein` (ohne Argument beide). Esc oder "Zurueck zum Gesamtmodell" kehrt zurueck. Messhilfe fuer die Pruefung: `window.detailState()` (Rahmen der Detailgruppe, Kamera, Auswahl).
- Abweichungen vom Blatt: (1) Das graue Menue "Detailansicht (noch keine Teiledaten)" entfaellt, weil ein Vorab-Request auf `/parts/` Pruefpunkt 3 verletzen wuerde; stattdessen erscheint nach dem Klick ein Hinweis mit dem Befehl. (2) Farben kommen aus `user_materials` im `.sc` (kein Farbtabelle im Skript). (3) Bezugsteile (ohne `explosion`) sind standardmaessig durchsichtig (Haken "Bezugsteil durchsichtig"), Klick im Modell nimmt das erste nicht durchsichtige Teil. (4) Zusatzknopf "Ansicht einpassen". (5) Beim Oeffnen wird zusaetzlich `/katalog.json` geladen (Werkstoffnamen, Katalogeintrag).
- Pruefpunkte selbst gemessen:
  1. `python -X utf8 scripts/workshop/check_parts.py feinfilter tank_klein`: 19/19 + 19/19 PASS, Exit 0.
  2. Summe `viewer/defs/*.obj` 316,42 MB (Befehl aus dem Blatt), `instances.json` 152 Definitionen, 4880 Instanzen; Detail-OBJ 6,78 MB (feinfilter), 8,22 MB (tank_klein), beide unter 10 MB.
  3. Vor dem Klick 0 Requests auf `detail/` und `/parts/` (`performance.getEntriesByType('resource')`), danach `/parts/<def>.json`, `/detail/<def>.json`, `/detail/<def>.obj`; `grep -c "^o " viewer/detail/<def>.obj` = 55 / 33.
  4. Schieber 0: Rahmen der Detailgruppe min [-375,-340,0], max [385,325,903] = Vereinigung der `.sc`-Koerper; Schieber 1: Siebkorb ueber dem Deckel (Screenshot); Zurueck: Kamera-Abweichung unter 1e-11 mm. Echte Klicks im Browser (Rechtsklick, Menue, Schieber ziehen, Zeile, Modellklick, Zurueck) geprueft.
  5. `grep -nE "feinfilter|tank_klein" viewer/index.html` = 0 Treffer; Probe mit einer dritten Datei (`data/parts/zulaufrohr.json`, 1 Koerper): Detailansicht oeffnet ohne Viewer-Aenderung, Probe danach geloescht.
- Bilder (nicht committen): `renders/n-detail-pilot-1-gesamtansicht-menue.jpg`, `renders/n-detail-pilot-2-detailansicht-infokarte.jpg`. Oeffnen: `python viewer/serve.py`, http://localhost:4410/ (laufender Viewer neu starten, damit `serve.py` die neuen Durchreichen kennt).

## Definition of Done

Geprueft gegen: `python -X utf8 scripts/workshop/check_parts.py feinfilter tank_klein` (55 / 33 Koerper, Exit 0), `viewer/defs` Summe 316,4 MB +- 1 %, Netzwerklog (kein `detail/`-Request vor dem Klick), `grep -c "^o " viewer/detail/<komp>.obj`, vier Screenshots gegen `ui-standard.md`, Kopier-Probe einer dritten `data/parts`-Datei ohne Viewer-Aenderung.
Offen: Pruefer (8), Orchestrator (9), Normverweise und Lebensmittelkontakt `angenommen` bis R31/B6/R50, Biofilter-Entscheidung (Ben).
