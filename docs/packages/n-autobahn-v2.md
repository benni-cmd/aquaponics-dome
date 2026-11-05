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

**Stand Montage R1/R2 (05.11.2026):** beide Runden gebaut, Pruefpunkte gemessen. Bau: `solidcraft-cli run scripts/dome-script-ring_b2.json --save designs/dome-ring_b2.sc` (R1 Exit 0 in 3:39 min, R2 Exit 0 in 5:25 min; erzeugt mit `AUTOBAHN_RUNDE=r1|r2 python -X utf8 scripts/gen_dome.py 5 scripts/dome-script-ring_b2.json --variante ring_b2`). Geometrie-Pruefung: `python -X utf8 scripts/check_autobahn_montage.py r1|r2`.

Pruefpunkte R1 (Tragwerk, Ring, Einspeisung), 13 PASS, 2 FAIL:
| Pruefpunkt | Ist | Soll | Ergebnis |
|---|---|---|---|
| Stuetzpunkte | 7 Joche, 3 Stelzen, 10 Schienen, 10 Verbinder, 10 Ring-Ecken | 7 / 3 / 10 / 10 / 10 | PASS |
| Ring-Schellen, groesster Abstand entlang der Achse | 30 Schellen, 955 mm | <= 1000 (R6) | PASS (Blatt schaetzte 22; mit einer Schelle je Seite waeren es 1077 mm) |
| Einspeisung | 2 Pegelschaechte auf Podest Z 820, 4 Booster, 4 Rueckschlagventile d50, Steigleitungen d63 | wie Blatt 2.1 | PASS |
| Haehne und Entluefter | 2 Kupplungs-, 2 Ring-Ende-, 2 Entleerungshaehne d63, 2 Entluefter d75 | je 2 | PASS |
| Ring- und Schellen-Unterkante | Z 2107,5 / 2101,5 rel | >= 2100 | PASS |
| Stelzen ausserhalb der Gaenge | 0 mm Ueberdeckung (r 3108, 3108, 3801) | 0 | PASS |
| Pegelschacht ausserhalb der Gaenge | Linie 1 r 2581: 464 mm in Gang A; Linie 2 r 4134: 425 mm in Gang B | 0 | **FAIL** |
| Interferenz Autobahn-Teile | Gesamtlauf: 4 Treffer (Anker der 3 Stelzen im Erdkoerper, gewollt), aber abgeschnitten bei 20.000 Kandidatenpaaren; gezielter Lauf (920 neue Koerper, 3.246 Paare mit Box-Ueberlappung): 0 Treffer > 0,5 mm3, Ring, Joche, Stelzen, Einspeisung gegen Tische, Beete, Tanks und Pumpen frei | 0 | PASS (ohne Huelle, siehe R2) |
| Gangkarte `check_walkways_voll.py --variante ring_b2` gegen A+ | Knie rot 56 (A+ 60), Kopf rot 5 (A+ 2); NICHT erreichbar: 6 Aussenbeete, 4 Booster, Pumpe_gross:1/:4, Pumpe_klein:3 (A+: 0) | keine neue rote Engstelle | **FAIL** |
| `check_leitungen.py --variante ring_b2` | 55 Verstoesse = 52 EINGABE (Kanten K60 bis K76 fehlen im Netz, O1) + 3 wie A+ | 0 ausser benannt | offen bis O1 |
| `check_leitungsordnung.py` (B2 gegen A+) | R1 32, R6 18, R9 16 Verstoesse mehr (Zehneck-Ring, 30-Grad-Saugleitungen, Hahnabgaenge unter Z 2100); Ausnahmen aus Blatt 2.6 kennt das Skript nicht | 0 ausser 2.6 | offen |

Pruefpunkte R2 (Ausleger, Abzweige, Schlaeuche), zusaetzlich 7 PASS, 3 FAIL:
| Pruefpunkt | Ist | Soll | Ergebnis |
|---|---|---|---|
| Ausleger / Abzweige d40 / d32 | 18 / 14 / 24 | 18 / 14 / 24 | PASS |
| Fallleitungen je Linie | je Linie 7 Beete, 12 Tische (38) | 7 + 12 | PASS |
| Schlauch-Unterkante ueber Gang A/B | Z 2128 rel (Beet_aussen_800:5, Gang B) | >= 2100 | PASS |
| freier Fall bis Regelhahn | hoechstens 1072 mm | <= 1500 | PASS |
| Schlauchende am Port | 0,0 mm | <= 1 | PASS |
| frei vom Abzweig bis zum ersten Clip | hoechstens 601 mm, 21 von 26 ueber Soll | <= 400 (R6) | **FAIL** |
| Schlauch im ersten Clip | 19 von 26 > 5 mm daneben; insgesamt 72 von 95 Clip-Plaetzen belegt | im Clip | **FAIL** |
| Kollision mit der Kuppelhaut (Abstand zur Facettenebene durch die Knotenmitten, aus den Ausleger-Matrizen) | alle 8 Aussen-Ausleger ragen hinaus: 1370 an der Stelze -17,7: 254 mm, 1210: 61 bis 152 mm; Schlauch bis 209 mm (Tisch_aussen:5); CAD: 97 von 157 Paaren Folie x Ausleger "shell boundaries intersect or touch" | innerhalb | **FAIL** |
| Interferenz Ausleger, Abzweige, Schlaeuche gegen Bestand (gezielt) | 0 Treffer in den pruefbaren Paaren; 2.054 Paare Huelle x Ausleger ungeprueft (Zeitbudget) | 0 | PASS ohne Huelle |
| Schlauchmeter aus den Wegen | ID19 87,0 m (Rechnung ID16 60,8), ID25 51,3 m (Rechnung 38,6) | Messwert | INFO |
| Rohrmeter aus den Trassen | Ring 20,6 m (PE-Ecken 14,8 + PVC 5,8), d63 10,4, d50 8,6, d40 0,5 | Messwert | INFO |
| A+ unberuehrt | SHA-256 der Ausgabe von `gen_dome.py 5` vorher = nachher `1a3e4ac0...c7d7b9` (`cmp` gleich) | gleich | PASS |

Viewer (echter Browser, `http://localhost:4410/?variante=ring_b2`, 05.11.2026 16:39): Export `python -X utf8 viewer/export_model.py --variante ring_b2` (Exit 0, 5.442 Instanzen, 322 Definitionen, 338 MB); Etikett "Kreislauf: Ring B2", Ring mit Auslegern sichtbar, nach Umschalten auf A+ kein Ring (`renders/ring_b2/viewer-ring_b2.jpg`, `viewer-a_plus.png`). Bilder des Modells: `renders/ring_b2/round-02.png`, `section-02.png`, `r2-draufsicht.png`, `r2-ecke.png` (R1: `round-01.png`, `section-01.png`, `r1-draufsicht.png`, `r1-ecke-schnitt.png`).

Befunde (Montage):
1. **Einspeisung hat keinen Platz ausserhalb der Gaenge.** Am K10/K26-Ende (Vorschlag WA-T) steht der Pegelschacht mitten in Gang A bzw. B; mit Podest und Boostern schneidet er den Rundgang ab (6 Aussenbeete nicht erreichbar). Frei ist nur der Tuer-Korridor (gruen in der Gangkarte), dort wird K10 ueber 2 m lang und das Podest sinkt.
2. **Abzweige sitzen auf dem PE-Bogen** (Annahme Montage: Anbohrschelle, Abweichung der T-Achse zur Bogenlinie <= 2 mm). WA-T verlangt mindestens 609 mm Abstand zur Ecke; dort ist kein Platz fuer bis zu 5 Abzweige je Ecke neben Schellen, Hahn- und Einspeise-T.
3. **Clips:** Die Ausleger-Clips beginnen 158 bis 178 mm hinter dem Flansch; der Schlauch erreicht die Armhoehe erst nach Versatz (bis 507 mm, weil an einer Ecke bis zu 5 Abzweige liegen) und 45-Grad-Anstieg. Abhilfe: Clip-Raster je Ausleger erst ab 700 mm oder zusaetzliche Haenger am Joch-Querriegel (WA-T).
4. **Ruecklauf R2c nicht gebaut:** WA-S Befund 4 zeigt, dass die Bodenrinne unter dem Pool-Spiegel liegt; der Schlauch-Ruecklauf aus Blatt 2.5 laeuft so nicht frei. Ring B2 behaelt den gemeinsamen starren Ruecklauf K15/K31 (wie A+). Ring-Ende- und Notueberlauf-Leitungen enden offen ueber dem Boden.
5. **Aussen-Ausleger durchstossen die Kuppel.** Ueber Gang B auf Z 2277 rel ist bei r 5,1 bis 5,5 m kein Platz mehr unter den Facetten (Blatt Abschnitt 4 R2a nannte es "knapp"). Abhilfe (Planer/WA-T): Aussen-Ausleger kuerzer und Schlauch frueher fallen lassen (dann quert er Gang B tiefer als Z 2100) oder Aussen-Abnehmer von unten speisen.
6. **Schlauch-Komponente ist Darstellungsgeometrie** (`designs/components/ring_b2_schlauchwege.sc`, vorher `ring_b2_schlaeuche.sc`; neuer Name, weil die alte 622-MB-Definition im laufenden Viewer gesperrt blieb): Achtkant-Prismen ohne Bohrung. Die Werkstatt-Teile mit Bohrung ergaben im Viewer 622 MB OBJ (17 MB je Fallleitung) und luden nicht ("Invalid string length"); jetzt 4,9 MB. Wege und Laengen sind unveraendert.

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
