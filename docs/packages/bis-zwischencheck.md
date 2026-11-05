# Paket: Bis zum Zwischencheck (Ben 05.11.2026, D81)

**Problem:** Viele Roadmap-Schritte vor dem Zwischencheck warten auf Bens Entscheidungen (E20, E13, E19 und weitere).
**Intent:** Ben will beim Zwischencheck ein moeglichst vollstaendiges Modell sehen; fehlende Entscheidungen werden als Annahme getroffen und dort bestaetigt.
**Goal:** Alle Roadmap-Schritte mit Phase `vor_zwischencheck` sind erledigt oder ausdruecklich benannt geparkt; jede Annahme steht in D81 und im Zwischencheck-Bericht.

## Plan (Wellen; Gesamtmodell baut nur eine Sitzung zugleich, sonst bis 7 parallel, D80)
1. Modell-Kette (nacheinander): check_latte 69 -> Pruefer Luft A -> Montage Strebe + Werkstoffe -> Montage Luft Teil B (E13-Annahme) -> M10-S2N -> M10-S3 -> M10-S4 (mit Beet-Sumpf) -> M10-S5 Rest -> M10-S6 -> M10-S7 -> CHECK; je Montage ein fremder Pruefer.
2. Parallel dazu: Planer-Buendel M10 nach A+ (Blaetter S2N bis S7 auf A+ und D81), Werkstatt W37-1 Beet-Sumpf/Schlammfass, SPECS-R45 + HEBER-SKRIPT, N-PREIS-PRUEF (Recherche -> Werkstatt -> Pruefer), Auflagen Detailansicht.
3. Danach: V-MESS (Viewer Messstellen, Export kleiner), W65-Tabelle, Zwischencheck-Bericht mit allen Annahmen.
4. Geparkt: M10-S2V Subtank (Ben), E16/E17, R46 nach dem Zwischencheck.

## Warteschlange (bereit wenn -> starten; Orchestrator fuellt bis 7 Plaetze)
| Schritt | bereit wenn | Rolle, Modell | Stand |
|---|---|---|---|
| Montage Strebe + Werkstoffe (N-MODELL-KOMPLETT 3) | Strebe-.sc im Repo (bdaccb4) | Montage, Opus mittel | bereit, als Erstes nach der Pause |
| Pruefer N-MODELL-KOMPLETT | Montage Strebe fertig | Pruefer, Sonnet hoch | wartet |
| Pruefer Luft A (M10-S5-LUFT) | check_latte 69 in Kopie fertig | Pruefer, Sonnet hoch | wartet |
| Pruefer N-PREIS-PRUEF | Werkstatt Schritt 2 fertig | Pruefer, Sonnet hoch | wartet |
| Werkstatt V1a Varianten-Skripte | Werkstatt Preis Schritt 2 fertig (bom.py frei) | Werkstatt, Sonnet hoch | wartet |
| Montage Luft Teil B (M10-S5-LUFT-B) | Montage Strebe fertig | Montage, Opus mittel | wartet |
| Werkstatt V1b gen_dome-Weiche | Montage Luft B fertig | Werkstatt, Opus mittel | wartet |
| Montage M10-S2N | V1b fertig und tiefer Schacht gebaut | Montage, Opus mittel | wartet |
| Montage M10-S3, S4, S5, S6, S7 | jeweils Vorgaenger + dessen Pruefer gestartet | Montage, Opus mittel | wartet |
| Viewer VV Varianten-Schalter | V1a fertig | Viewer, Sonnet hoch | wartet |
| Montage Ring R1, R2 | M10-S7 fertig, V2-Bauteile gebaut | Montage, Opus mittel | wartet |
| Maengel-Inventur N-REWORK im Viewer (W71) | naechster freier Platz (leicht, nur Viewer und Screenshots) | Pruefer, Sonnet hoch | wartet, Prioritaet 1 |
| Planer Leitungsordnung + Umbau S0-S2 (W71), Nachtrag zu planer-m10-aplus | Maengel-Inventur fertig | Planer, Opus mittel | wartet |
| Werkstatt Bauteil-Fixes aus Maengel-Inventur (Absetzer-Durchbrueche u. a.) | Maengel-Inventur fertig | Werkstatt, Opus mittel | wartet |
| Auflage A4 Detailansicht (Stand geruest in 19 Dateien) | freier leichter Platz | Daten, Sonnet hoch | wartet |
| CHECK je Variante, V-MESS, W65-Tabelle, Zwischencheck-Bericht | Kette fertig | gemischt | wartet |

## Stand
- 05.11. ~01:00: Paket angelegt, Annahmen D81, Welle 2 startet.
- 05.11. SPECS-R45 + HEBER-SKRIPT (Werkstatt, Aktualitaetspruefung W44: Blatt gueltig, D81 A+ und E19 Reserve gelten, Fischmenge 346 kg wie gebaut unveraendert). Werte, jeweils mit Befehl: Beet-Sumpf 108 W Mittel (2 x 60 W x 0,9; Reserve 2 x 60 W Anschluss, 0 W Betrieb) und Gesamtleistung 764 W / 18,3 kWh/Tag / Spanne 450 bis 980 W (vorher 656 W / 15,7 kWh/Tag / 370 bis 860 W, gemessen am Stand HEAD vor dem Nachtrag) = `python -X utf8 scripts/system_specs.py`, Feld `leistung` in `data/system-specs.json`; Hauptpumpen Anschluss 4 x 110 W Premium-Klasse, Rechenwert 72 W je Pumpe bleibt; Gebläse N+1 (2 Geraete, 100-215 W je Geraet, Rechenwert 204 W) und Kabelzeilen (Beet-Sumpf 54 W, Reserve 0 W, Gebläse, Hauptpumpe 110 W) = `python -X utf8 scripts/check_netz.py` (Exit 0, 23 -> 25 Kabelzeilen); Heber gebaut (dn aus JSON, T d75, Reduziermuffen, Bögen einzeln, gealtert, Crane-Gehrung/T 0,9): K01 Reserve 65 mm, K17 68 mm = `python -X utf8 scripts/r45_heber.py` (Zeilen `gebaut schlecht`); BEFUND: unter der alten Vorgabe 85 mm (-20 / -17 mm), ueber der Grenze 30 mm (+35 / +38 mm); die 85/88 mm der Pruefung M10-S2R kamen aus dem pauschalen Zusatzverlust 0,3 und Austritt bei d75 statt am d63-Stutzen. Mittel-Fall 103 / 107 mm.
- 05.11. HEBER-RESERVE Loesungsvarianten (nur gerechnet, nichts gebaut; Befehl `python -X utf8 scripts/r45_heber.py`, Abschnitt `LOESUNGSVARIANTEN`; schlechter Fall gealtert/Crane-Gehrung/T 0,9; Bezug gebaut K01 65 / K17 68 mm, Vorgabe 85, Grenze 30): V1 Langbogen kb 0,2 = 109/113 mm; V1b Spritzgussbogen glatt (Crane 0,57) = 91/95 mm; V2 Filter-Einlauf d75 statt d63 = 82/85 mm (reicht allein nicht); V3 V1+V2 = 126/130 mm; V4 Einlaufachse 50 mm tiefer = 115/118 mm; V5 100 mm tiefer = 165/168 mm; V6 Heber d90 = 105/106 mm; V7 Langradius-T = 81/85 mm (reicht nicht). EMPFEHLUNG: V1b, also die Bogen d75 als Spritzguss-Bogen (glatter Innenradius) kaufen statt Gehrungs- oder Segmentbogen; gleiches Teil, kein Umbau am Modell, 91/95 mm halten die 85 mm. Bis die Beschaffung das belegt (Bogen-Datenblatt, Kategorie in `data/beschaffung/`), gilt der Mittelfall 103/107 mm. Falls nur Gehrungsbogen lieferbar: V4 (Einlaufachse 50 mm tiefer, aendert Modell Feinfilter-Einlauf) oder V1 mit Langradius-Bogen. Nicht empfohlen: V6 (alle Rohre, Bogen, T neu), V7 (zu wenig). Die Annahme kb (0,57 / 0,2) stammt aus Crane/Engineering Toolbox fuer Metallformstuecke, fuer PVC-Muffenbogen ohne Herstellerbeleg [A].

## DoD
Roadmap `vor_zwischencheck` ohne offene Bauschritte; Pruefer-Befunde je Montage; Zwischencheck-Bericht mit Annahmen-Liste; Commit und Push je Schritt.

- 05.11. Nacht: erledigt Strebe Runde 70 (Pruefer: FAIL nur BOM-Flag, behoben 7417910), Maengel-Inventur (7d59462, 12 Maengel), Leitungsordnung + M10-UMBAU (4f16d13), W37-1 Sumpf/Schlammfass (6da69f3), tiefer Schacht + Ring-Bauteile (0462ec8, 721b607), Preisliste neu (7d3fd5d, Pruefer PASS mit Auflagen 101277e), Anschluesse sichtbar (a980ae1), A4 (d324fb6). Laeuft: Montage M10-UMBAU Runde 71 (montage-strebe-70), V1a Varianten-Skripte (preis-werkstatt-2), Werkstatt Ruecklauf-Sammler/Tank (werkstatt-strebe), check_latte 69 in Kopie (Runde 3/6). Danach: Pruefer UMBAU, Pruefer Luft A, Montage Luft B, V1b, M10-S2N.
- 05.11. Nacht: Pruefer-Auflage 1 N-PREIS-PRUEF entschieden (Orchestrator): Pruefpunkt 1 gilt mit 'Entscheidung je Zeile in der Gruppen-Notiz' als erfuellt, kein Wortlaut-Nachtrag. Auflagen 2-5 und 7 an die Recherche-Sitzungen, 6 (drift) nach dem naechsten Modellbau.
