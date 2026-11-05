# Paket: N-AUTOBAHN-V2 — Wasserautobahn mit Stelzen, Schlauch-Abzweigen und Schlauch-Ruecklauf bauen (W78)

**Problem:** Die Wasserautobahn (Ring B2) gibt es nur als Bauteile und Rechnung; im Modell fehlt sie, und der alte Plan R1/R2 kannte weder passende Stelzen noch Schlaeuche noch einen fairen Zahlenvergleich.
**Intent:** Ben und Leon sehen beide Kreislaeufe im Viewer so, wie sie gebaut wuerden, und entscheiden E20 auf gemessenen Zahlen.
**Goal:** `designs/dome-ring_b2.sc` enthaelt Ring, 10 Stuetzpunkte, 18 Ausleger, 38 Schlauch-Fallleitungen, Einspeisung je Linie und Schlauch-Ruecklauf; die Pruefpunkte aus `docs/jobs/N-AUTOBAHN-V2.md` Abschnitt 6 sind fuer beide Varianten gruen; die Vergleichstabelle traegt Messwerte.

Auftragsblatt: `docs/jobs/N-AUTOBAHN-V2.md`. Rechnung: `python -X utf8 scripts/n_autobahn_rechnung.py`. Vorgaenger: `docs/packages/n-varianten.md` (V1a, V1b, VV, V2 gebaut).

## Plan
1. [x] Planer: Blatt, Rechnung, Vergleich und Empfehlung (05.11.2026).
2. Werkstatt WA-T Tragwerk: Portal-Joch, Ausleger, Montageschiene mit `lt_klemme_d75`, Ring-Ecke 36 Grad, Pegelschacht-Podest (sofort, parallel).
3. Werkstatt WA-S Schlauch: Fallleitung ID16/ID25, Schnellkupplung, Rueckschlagventil d50, Ruecklauf-Rinne, Bodenrinne, Schlauch d50 (sofort, parallel).
4. Orchestrator O1: Netz-Delta K60 bis K76 (Blatt 2.7), Roadmap-Eintrag.
5. Montage R1: Tragwerk, Ring, Einspeisung beider Linien (nach WA-T und Leitungsordnung v2).
6. Montage R2: Ausleger, 38 Fallleitungen, Ruecklauf, Viewer-Export, Screenshots (nach R1 und WA-S).
7. Pruefer: Pruefpunkte 1 bis 5 beider Varianten; Vergleichstabelle mit Messwerten nachtragen.

## Stand
- 05.11.2026, Planer: Blatt und Rechenskript geschrieben, nichts gebaut. Ergebnisse der Rechnung:
  1. Ring als Zehneck ueber der Mittelzone: 21,3 m, 10 Ecken, 7 Portal-Joche und 3 eigene Stelzen, kein Stuetzpunkt im Gang.
  2. 38 Fallleitungen: 12 direkt unter dem Ring, 26 ueber 18 Ausleger; Schlauch ID25 38,6 m, ID16 60,8 m.
  3. Pumpen: 617 W gegen 430 W (A+), wenn der Pegelschacht auf einem Podest steht; am Boden 754 W.
  4. Teile Zulauf 540 gegen 267; Mehrkosten mindestens 2.769 EUR (6 Posten ohne Preis); Graben Zulauf 0 gegen 4,6 bis 29,6 m.
  5. Empfehlung: A+ bleibt Bau-Empfehlung; Autobahn wird als vollwertige Anschauungs-Variante gebaut. Umkehr-Ausloeser stehen im Blatt Abschnitt 5.

### WA-S Schlauch (Werkstatt, 05.11.2026, Plan)
**Problem:** Fallleitungen, Kupplungen, Rueckschlagventil d50 und Schlauch-Ruecklauf gibt es nicht als Bauteile. **Intent:** R2 setzt nur fertige Teile, die Koordinaten kommen aus einer Schlauch-Funktion statt von Hand. **Goal:** Die WA-S-Pruefpunkte aus Blatt Abschnitt 3 sind in `scripts/workshop/check_autobahn_s.py` gemessen (Exit 0).
1. Generator `scripts/workshop/autobahn_s.py`: Schlauch-Pfad (Polylinie mit Biegeradius, R14), WA6 Schnellkupplung ID16/ID25, WA8 Rueckschlagventil d50, WA5 fuenf Fallleitungs-Typen (Tisch innen/mitte/aussen, Beet innen/aussen), WA9 Ruecklauf-Rinne, Bodenrinne mit Rost, Schlauch d50.
2. Werkstoffe D85 mit zwei Quellen (Recherche-Agent, Ergebnis ins Teileblatt).
3. Check, Teiledaten `data/components/autobahn_teile.json` (Abschnitt `wa_s`), Bilder `renders/components/autobahn/`, Teileblatt `docs/parts/autobahn.md` Abschnitt WA-S.

**Stand WA-S 05.11.2026:** 12 Teile gebaut, Check 101/102 PASS (`python -X utf8 scripts/workshop/check_autobahn_s.py`); einziger FAIL: Regelhahn GF 546 Pro nur eine Quelle fuer D85. Befunde im Teileblatt: Tische ID19 statt ID16, Anstieg auf Ausleger Z 2277, Bodenrinne unter Pool-Spiegel (Planer-Frage), Handels-Bodenrinne zu flach.

### Montage R1/R2 (05.11.2026, Plan)
**Problem:** Die Bauteile von WA-T und WA-S liegen vor, im Modell `designs/dome-ring_b2.sc` fehlt die Autobahn. **Intent:** Ben und Leon schalten im Viewer zwischen A+ und Autobahn um und sehen sie so, wie sie gebaut wuerde. **Goal:** `sh scripts/build.sh 5 <runde> ring_b2` baut Ring, Stuetzpunkte, Einspeisung (R1) und Ausleger, Fallleitungen, Ruecklauf (R2); die Pruefpunkte aus Blatt Abschnitt 4 und 6 sind gemessen und hier eingetragen; A+ (`scripts/dome-script.json`) bleibt byte-gleich.
1. `scripts/trassen_ring.py`: alle Lagen aus Instanzmatrizen und Port-Tabellen (Ring, Joche, Stelzen, Schienen, Schellen, Einspeisung, Ausleger, Abzweige, Fallleitungen); Trassen mit `quelle: trassen_ring` und `varianten: ["ring_b2"]` in `data/leitungstrassen.json`.
2. `gen_dome.ring_b2()` setzt die Bauteile; `leitungen.halter()` laesst Trassen mit `halter: false` aus (Ring haengt an eigenen Schellen).
3. R1: Bau, Interferenz, `check_walkways*`, `check_leitungen`, `check_leitungsordnung`, Bilder Draufsicht und Schnitt.
4. R2: Ausleger, 38 Abzweige und Fallleitungen, Ruecklauf; Bau, alle Pruefungen, Viewer-Export, Screenshots.
5. A+-Pruefsumme vorher (13:34, `sha256sum` der Ausgabe von `gen_dome.py 5 <scratch>/a.json`): `1a3e4ac0d0b8b468204d5434a6b4d099a6bbc92e5b6a05ed80fae23b19c7d7b9`.

### WA-T Tragwerk (Werkstatt, 05.11.2026)
**Problem:** Joch, Ausleger, Schiene mit Schelle, Ring-Ecke und Podest fehlen als Bauteile. **Intent:** R1/R2 setzen nur fertige Teile. **Goal:** Die WA-T-Pruefpunkte aus Blatt Abschnitt 3 sind in `scripts/workshop/check_autobahn_t.py` gemessen (Exit 0).

**Stand WA-T 05.11.2026:** 14 Teile gebaut (`scripts/workshop/autobahn_t.py`), Check 104/104 PASS (`python -X utf8 scripts/workshop/check_autobahn_t.py`). Lage je Ringecke steht in `data/components/autobahn_teile.json` -> `tragwerk.lagen`. Befunde im Teileblatt `docs/parts/autobahn.md` Abschnitt WA-T:
1. Ring-Apothem 3377 statt 3277 (D63): Seite 2194,5 mm, Umfang 21,95 m.
2. Der Ring haengt unter der Schiene; sonst laege die Schiene unter Z 2100.
3. Ring-Ecke PE-100 kalt gebogen mit R 1875. Abzweige muessen mindestens 609 mm von der Ecke weg; PP-Klemm-T statt PVC kleben.
4. Podest auf Z 820 statt 950; Pumpen etwa 636 statt 617 W.
5. Podest am heutigen Verteilerplatz liegt im Gang: Die Lage klaert Montage R1c.

## DoD
1. Pruefpunkte 1 bis 5 aus dem Blatt von einem fremden Pruefer als PASS belegt (`docs/jobs/pruefung/N-AUTOBAHN-V2.md`).
2. Viewer-Screenshot beider Varianten im echten Browser, Ring mit Schlaeuchen nur in Ring B2.
3. Vergleichstabelle im Blatt mit Messwerten aus den Trassen statt Rechnung.
4. Jeder Schritt mit Pfad-Commit und Push.
