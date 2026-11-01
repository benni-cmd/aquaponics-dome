# W39 Leitungsteile-Kleinteile (Werkstatt A2, eine Sitzung, Reihenfolge: ZUERST, vor W37)

Problem: Fuer S3 (Beete, Rinnen) und S6 (Leerrohr) fehlen Kleinteile der Leitungsbibliothek (Luecke L22, `docs/workshop-state.md` OFFEN (0)); dazu fehlt ein Rueckschlagventil, das W37 (Sumpf K58/K59, Luft) braucht (`docs/parts/leitungsteile.md` Zeile 178: "Rueckschlagventil ... fehlen"). Intent: Die Montage soll Beete, Rinnen und Kabelwege mit Normteilen verlegen koennen, ohne Eigenbauten; Handelsteile vor Eigenkonstruktion (Wunsch W43). Ziel in einem Satz: Zehn neue Dateien `lt_*.sc` mit Ports im Bibliotheksformat, Check gruen, Blatt-Abschnitt, JSON und Bild, damit L22 schliessbar ist und W37 das Rueckschlagventil und die Kabeleinfuehrung nutzen kann.

## Aktualitaetspruefung (01.11.2026, Planer)
Ergebnis: **angepasst** (Plan gilt als freigegeben).
- Roadmap W39/L22 unveraendert gueltig; `git log` zeigt keine Aenderung an `leitung.py`/`leitung_w36.py` seit W36 Teil 6 (9f3d8ab).
- Neu gegenueber L22: (a) **Rueckschlagventil d40 und d25/d20** ergaenzt (W37 braucht es dreifach: Foerderleitung K58/K59 d40, Luft-Hauptverteiler 6 Abgaenge, Pool-Verteiler); (b) **Kabeleinfuehrung** wird hier gebaut und von W37-3 (Schaltschrank) verwendet, daher W39 vor W37-3; (c) Stopfen/Kappe als eine Funktion `kappe(d)` fuer d20 und d50 (Netz: Reserveabgang d50 und Messkreis-Abgang d20 am Verteiler d50 der Linie 2).
- Entscheidungen D70 bis D72 und E12 bis E18 beruehren W39 nicht. Standort Schaltschrank bleibt OFFEN (Ben, E13); W39 plant nur das Teil, nicht den Ort.

## Eingaben (nur diese)
- `docs/parts/leitungsteile.md`: Konvention Zeilen 7 bis 30, W36-Teil ab Zeile 220 (Mini-Plan-Format, Herkunftstabelle), Pruefung Tropfrohr/Schlauch Zeilen 400 bis 410.
- `scripts/workshop/leitung.py` (Helfer `rohr`, `kupplung`, `reduzierung`, `kugelhahn`, `schlauch`, `klemme`, `save`, `wall_p`, `od_f`) und `scripts/workshop/leitung_w36.py` (Muster fuer neue Teile: `FILES`, `ports()`, `json_entries()`, `write_json()`, `write_descriptions()`); Check-Muster `scripts/workshop/check_lt_w36.py`.
- `data/components/leitungsteile.json` (Struktur `w36_teile` ansehen; neue Teile in eigenen Schluessel `w39_teile`).

## Teile (Reihenfolge = Commit-Reihenfolge; je Teil Mini-Plan vor dem Bau im Blatt-Abschnitt)
Neuer Generator `scripts/workshop/leitung_w39.py` (nutzt Helfer aus `leitung.py`, `FILES`-Liste wie W36; `leitung.ports()` bekommt einen Fallback wie in W36), Check `check_lt_w39.py`, Teilenummern T70 fortfuehren.

| Nr | Datei(en) | Ports (Bibliotheksformat) | Mass-Hinweis | Beleg |
|---|---|---|---|---|
| 1 | `lt_reduzierung_d40_d20` | A gross Muffe d40, B klein Muffe d20, L = t40 + t20 + 6 | `leitung.reduzierung(40, 20)`; ersetzt die Kette 40/32, 32/25, 25/20 (142 mm, drei Klebestellen je Beet, 14 Beete) | Bauweise belegt (Bibliothek); Handelsteil im Katalog [A], Nachweis N-BESCHAFFUNG |
| 2 | `lt_uebergang_pe_pvc_d20` (PE-Rohr d20 auf Klebemuffe d20) | A Klemme PE d20 (Einstecktiefe ca. 30), B Muffe d20 (Klebemuffe); Mutter/Klemmring sichtbar modelliert | Handelsteil "Klemmverbinder PE-PVC"; Laenge, Mutter-Aussen als [A] | A (kein Katalog gelesen); Tropfrohr ist PE, nicht klebbar |
| 3 | `lt_schlauch_id16_L100` | A/B Schlauchende ID16, L = 100 | `leitung.schlauch(16, 100)`; 76 Stueck; Check ignoriert Laengenvarianten (80b61d3) | belegt (Tisch-Blatt `hose_gap` 70 mm plus Aufsteckenden) |
| 4 | `lt_kappe_d20`, `lt_kappe_d50` | ein Port Muffe, Richtung -Z, Boden geschlossen; Funktion `kappe(d)` parametrisch | Boden 3 mm [A], Aussen wie Formstueck `od_f(d)` | A (SDR-21-Naeherung der Bibliothek) |
| 5 | `lt_schlauchschelle_id16` (Schneckengewinde-Schelle, Spannbereich 12 bis 22) | ein Port Aufnahme (Schlauch AD20), Achse wie die Klemme | Band 9 breit, Gehaeuse [A]; 152 Stueck laut Bibliothek-Stuecklistenzeile | A; ID25-Variante (Spannbereich 20 bis 32) nur, wenn dieselbe Funktion sie ohne Mehraufwand liefert |
| 6 | `lt_rueckschlagventil_d40`, `lt_rueckschlagventil_d25`, `lt_rueckschlagventil_d20` (Kugel-/Klappen-Rueckschlagventil, Klebemuffen) | A/B Muffe, Flussrichtung +Z als Pfeil im Namen vermerkt und im Blatt; Laenge wie Kugelhahn (50 + 2 t) | `leitung.kugelhahn(d)` als Vorbild, ohne Hebel | Bauweise A, Handelsteil [A]; Einbaulage waagerecht oder senkrecht aufwaerts im Blatt |
| 7 | `lt_leerrohr_red_dn100_dn50` | A Muffe DN100 (AD 110), B Zapfen oder Muffe DN50 (AD 50) wie die Leerrohr-Konvention (Stange Muffe B) | Konvention aus Blatt-Abschnitt Leerrohr (Zeile 317 ff.) uebernehmen | A (Katalog nicht gelesen) |
| 8 | `lt_leerrohr_t_dn50`, `lt_leerrohr_t_dn100` (Abzweig 90 Grad, gleich gross) | drei Muffen wie `lt_t_d*`, Kabel-tauglicher Radius dokumentiert (Abzweigradius ist hart; im Blatt vermerken, dass Kabel sie nur mit Zugdose durchlaufen) | Teilung wie die Leerrohr-Bogen | A |
| 9 | `lt_kabeleinfuehrung_dn50`, `lt_kabeleinfuehrung_dn100` | A Muffe (Leerrohr), B Flansch-Aufnahme (Schaltschrank-Boden), Dichtung und Gegenmutter modelliert; Aussen, Gewindelaenge [A] | Handelsteil "Kabeleinfuehrung/Wanddurchfuehrung mit Dichtung"; wird von W37-3 verwendet | A |

Falls der Platz (Kontext ueber 60 Prozent) vor Teil 9 endet: Stand in `docs/workshop-state.md`, naechste Sitzung macht dort weiter; Teil 9 hat Vorrang vor Teil 5 und 8, weil W37-3 darauf wartet. Reihenfolge dann: 1, 2, 3, 4, 6, 9, 5, 7, 8.

## Je Teil (Bibliothekskonvention)
Bauteil `.sc`, Check (Masse, Ports, Interferenz 0), Abschnitt in `docs/parts/leitungsteile.md` mit Mini-Plan, Ports-Tabelle, Herkunftstabelle (belegt / gerechnet / Annahme je Mass), Eintrag `w39_teile` in `data/components/leitungsteile.json`, Eintrag in `data/descriptions.json` (Gruppen vor die Sammelgruppe `^lt_` einsortieren, der Viewer nimmt den ersten Treffer; Muster `^lt_verteiler_d50$` bei Zeile 540, Sammelgruppe bei Zeile 699), Bild per `scripts/archive_render.py --role werkstatt --subject leitungsteile`. Je Teil ein Commit.

## Nicht anfassen
`designs/dome.sc`, `scripts/gen_dome.py`, `scripts/leitungen.py`, `data/leitungsnetz.json`, `data/roadmap.json`, `leitung.py` und `leitung_w36.py` (nur lesen), alle gebauten Dateien der W36-Teile, die fremden Dateien aus `docs/workshop-state.md` (Montage/Integrator).

## Ergebnis
`scripts/workshop/leitung_w39.py`, `check_lt_w39.py`, 14 bis 17 `designs/components/lt_*.sc` (je nach ID25-Variante), Blatt-Abschnitt "Ergaenzung W39", JSON, descriptions, Bilder, Zeile in `docs/workshop-state.md` (L22 geschlossen, Rest offen). Kurzmeldung: je Teil eine Zeile mit Masse, Ports, offenen Fragen; "Besonderheit: ..." falls etwas auffaellt.

## Pruefpunkte (fuer den Pruefer)
1. `python scripts/workshop/check_lt_w39.py` meldet alle Pruefungen PASS (Soll: keine FAIL-Zeile; Ausgabe in `renders/components/leitungsteile/check_w39.txt`).
2. Jede neue Datei hat in `data/components/leitungsteile.json` unter `w39_teile` einen Eintrag mit mindestens zwei Ports (Kappe: einer) und `herkunft` je Mass; `python -c` zaehlt Eintraege gegen `leitung_w39.FILES` (Soll: gleich).
3. Interferenz 0 und Port-Koordinaten: Kappe d50 steckt auf dem Zapfen von `lt_verteiler_d50` Abgang 4 ohne Ueberlappung ausser der Einstecktiefe 31 mm (Messung per CLI-Boolean oder Check-Funktion).
4. Reduzierung d40/d20: Baulaenge laut Port-Differenz gleich t40 + t20 + 6 (Soll aus `leitung.py` Tabelle t(d)); weniger als die 142 mm der Kette.
5. `git diff HEAD --stat` zeigt keine Aenderung an den Nicht-anfassen-Dateien; `data/descriptions.json` bleibt gueltiges JSON (`python -c "import json;json.load(open('data/descriptions.json',encoding='utf-8'))"`).

## Start-Hinweis fuer die Bau-Sitzung
1. Lies `docs/workshop-state.md` (GELERNT-Zeile: Heredoc bricht, Skripte per Write-Datei; Python 3.12 mit PYTHONIOENCODING=utf-8; Commit nur `git commit ... -- <pfade>`, neue Dateien vorher `git add -N`).
2. W36 hat 36/36 und 29/29 Checks; `check_leitungsteile.py` zaehlt W36/W39-Dateien nicht zu den 63 Bibliotheksteilen (Liste `FILES` pflegen, sonst schlaegt der Gesamtcheck an).
3. Boolean-Vereinigung duenner Zylindermaentel scheitert; Teile aus getrennten Koerpern mit 1 mm Ueberlappung bauen.
4. Alle Handelsteil-Masse (Klemmverbinder, Schelle, Rueckschlagventil, Kabeleinfuehrung) sind [A]; keine Fabrikat erfinden, im Blatt "Katalog offen, Nachweis N-BESCHAFFUNG" vermerken (L21).
5. Limit: eine Sitzung, kleine Teile bauen in 2 bis 10 s; bei Kontext ueber 60 Prozent stoppen und Stand eintragen.
