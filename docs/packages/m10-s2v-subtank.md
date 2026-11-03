# Work package: M10-S2V Subtank-Umbau (V4)

**Problem:** Vor dem Biofilter liegen je Linie Feinfilterkasten in der Grube, blind vergrabener Filter-Stamm mit zwei Pumpenzweigen und ein ungetesteter Notbypass (K56/K57): 10,33 m der 30,30 m vergrabenen Rohre, 6 von 12 Einzelpfaden, vier Pumpentafeln (gemessen aus `data/leitungstrassen.json`, 03.11.2026).
**Intent:** Ben entschied E21 = ja (D75, 03.11.2026): eine Wartungsstelle je Linie, weniger Vergrabenes, gleicher Strom (430 W), Hoehen unveraendert.
**Goal:** Je Linie ein Subtank mit Siebkorb am Einlauf und zwei Tauchpumpen; vergrabenes Rohr 12,66 m (+-0,2), Netzliste 51 Kanten, 6 Einzelpfade, `check_netz.py`, `check_leitungen.py`, `check_walkways.py`, `r45_heber.py` gruen. Blatt: `docs/jobs/M10-S2V.md`.

## Plan

1. [ ] Orchestrator: Netzliste Version 4 (6 Kanten raus, Knoten `subtank_*`, MS14/MS15, Bodenablauf-Z -1975)
2. [ ] Werkstatt: `scripts/s2v_pegel.py`, Annahmen A1 bis A9 klaeren
3. [ ] Werkstatt: Bauteile `siebkorb`, `subtank`, `tauchpumpe`, Grube/Auflage, Bauteilblaetter
4. [ ] Montage: `gen_dome.py`, Check-Skripte (Subtank statt Feinfilter, Pumpentafeln gross raus)
5. [ ] Montage: `trassen_linie.py` Linie 1, dann 2; Build Runde 67; Pruefskripte; Bild
6. [ ] Pruefer: `docs/jobs/pruefung/M10-S2V.md` nach den fuenf Pruefpunkten
7. [ ] Orchestrator: M10-S2N neu planen (nur Kappen/Revision), Roadmap nachfuehren

## Status

03.11.2026: Planer-Blatt geschrieben, Aktualitaet gueltig; offen: A8 (Rueckstausicherung am Heber) bei Ben, Tauchpumpen-Fabrikat (W47). Nichts gebaut.

## Definition of Done

Geprueft gegen: `python -X utf8 scripts/check_netz.py` (51 Kanten, 0 Stoerfall), Vergrabungs-Snippet im Blatt (12,66 m), `check_leitungen.py` (0 Verstoesse), `check_walkways.py` (PASS), `r45_heber.py` (Reserve >= 85/88 mm), `s2v_pegel.py`.
Offen: Umbau selbst, A1 bis A10 im Blatt, A8 (Ben), Netzliste v4 (Orchestrator).
