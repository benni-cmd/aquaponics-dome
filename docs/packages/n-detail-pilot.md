# Work package: N-DETAIL-PILOT Detailansicht im Viewer (Feinfilter und Absetzer)

**Problem:** Ben kann die Funktion von Bauteilen im Viewer nicht beurteilen: Feinfilter (55 Koerper) und Absetzer (33 Koerper, davon 8 unbenannt `Body1..8`) erscheinen nur als Huellform; es gibt weder Teile-Datenmodell noch benannte Einzelkoerper im Export noch eine Detailansicht (B1 bis B3 im Gross-Paket `bauanleitung-teileliste-detailansicht.md`).
**Intent:** Ben (03.11.2026, D56): Detailansicht jetzt fertig machen, damit Filter und danach Subtank, Siphon, Pumpen nach Funktion beurteilt werden koennen; Pilot vorgezogen, voller Katalog und Gesamtansicht bleiben N-KATALOG und N-DETAIL.
**Goal:** Rechtsklick auf Feinfilter oder Absetzer, Menue "Detailansicht", Explosionsdarstellung mit Schieber, Teileliste, Klick auf Teil oder Zeile zeigt Infokarte, "Zurueck"; Detailmodell nur bei Bedarf geladen, Hauptexport waechst nicht (defs 316,4 MB +- 1 %). Blatt: `docs/jobs/N-DETAIL-PILOT.md` (Datenformat, UI, fuenf Pruefpunkte).

## Plan

1. [ ] Werkstatt A (1a): `tank.py` Schrauben benennen, Material setzen, `tank_klein.sc` neu, `check_tank.py` gruen
2. [ ] Werkstatt A (1b): `data/katalog.json` (Stand Pilot, nur was die zwei Bauteile brauchen)
3. [ ] Werkstatt A (1c): `data/parts/feinfilter.json` und `scripts/workshop/check_parts.py` (Koerper 55, jeder genau einmal)
4. [ ] Werkstatt A (1d): `data/parts/tank_klein.json` (Koerper 33)
5. [ ] Viewer (2a, parallel zu 2 bis 4): `viewer/export_detail.py`, zwei Durchreichen in `serve.py` (`/parts/`, `/katalog.json`)
6. [ ] Viewer (2b, nach 3): Rechtsklick-Menue, Detailszene, Schieber, Teileliste, Infokarte, Zurueck; dann tank_klein (nach 4)
7. [ ] Viewer (2c): Screenshots Feinfilter und Absetzer gegen `..\..\docs\ui-standard.md`, Pruefpunkte 1 bis 5 selbst durchlaufen
8. [ ] Pruefer: `docs/jobs/pruefung/N-DETAIL-PILOT.md` nach den fuenf Pruefpunkten
9. [ ] Orchestrator: Roadmap nachfuehren, `V-MESS` hinter den Pilot, `N-DETAIL-R50` und Subtank/Siphon/Pumpen als Daten-Folgeschritte eintragen

## Status

03.11.2026: Planer-Blatt geschrieben, Aktualitaet angepasst (D75: Feinfilter wird mit M10-S2V vom Subtank abgeloest, Siebkorb-Teil bleibt wiederverwendbar). Nichts gebaut. OFFEN (Ben): Biofilter (`tank_gross`) in den Pilot? (Vorschlag: nein.)

## Definition of Done

Geprueft gegen: `python -X utf8 scripts/workshop/check_parts.py feinfilter tank_klein` (55 / 33 Koerper, Exit 0), `viewer/defs` Summe 316,4 MB +- 1 %, Netzwerklog (kein `detail/`-Request vor dem Klick), `grep -c "^o " viewer/detail/<komp>.obj`, vier Screenshots gegen `ui-standard.md`, Kopier-Probe einer dritten `data/parts`-Datei ohne Viewer-Aenderung.
Offen: Bau (nichts begonnen), Normverweise und Lebensmittelkontakt `angenommen` bis R31/B6/R50, Biofilter-Entscheidung (Ben).
