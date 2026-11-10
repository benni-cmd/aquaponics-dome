# Paket N-UNIFY-AUTOBAHN: ein Wasserkreislauf, exakt nach Leons Oasis-Showcase

**Problem:** Das Modell hat zwei Wasserkreisläufe (A+ mit Zielbild S und Ring B2 als Wasserautobahn), umschaltbar in
Skripten, Modell und Viewer. Leon hat den Kreislauf im Oasis-Showcase ausgearbeitet (Bauteile, Draufsicht,
Seitenprofil, Höhenschnitt, Höhenstufen 0 bis 5, Wasserspiegel über Fußboden, Wasserwege). Modell und Quelle stimmen
nicht überein, und wir sind uns über den Kreislauf nicht einig.
**Intent:** Ein einziger, richtiger Wasserkreislauf, auf den sich Ben und Leon einigen, der Schwerkraft nutzt und
im 3D-Modell, in Teileliste, Bestellliste und Bauteilbeschreibungen einheitlich und vollständig steht.
**Goal (prüfbar):** Jede Wasser-Komponente und jeder Wasserweg der Quelle ist im Gesamtmodell an der Stelle und Höhe
der Quelle gebaut (Abweichung je Wasserspiegel höchstens ±50 mm zum Wert der Quelle, Stufenreihenfolge 0 bis 5 exakt),
es gibt nur noch eine Variante, Teileliste/Bestellliste/Beschreibungen decken jedes neue Teil ab,
`check_latte` zeigt keine neuen Kollisionen durch den Kreislauf, und ein fremder Prüfer bestätigt das gegen eine
Soll-Ist-Tabelle aller Quell-Bauteile.

**Quelle:** `docs/quellen/oasis-showcase-2026-11-10/` (Commit f11a92d, SHA256 im README) und Nachtrag
`docs/quellen/oasis-showcase-2026-11-10-nachtrag/` (`flow-diagram.html`: Höhenschnitt, Annahmen A1 bis A32, JSON-Daten). Entscheidung D93, Wunsch W89.
**Daten und Bericht:** `data/oasis-soll.json` (erzeugt von `scripts/oasis_soll.py`, 45/45 Prüfungen) · `docs/research/R61-oasis-wasserkreislauf.md` · Annahmen D94 bis D107 in `docs/decisions.md` · Bauplan `docs/jobs/N-UNIFY-AUTOBAHN.md`.
**Arbeitsweise:** Agent-SDK-Runner auf API-Guthaben (`tools/agent-sdk-runner` der Werkbank), Sonnet 5.5, einfache
Aufgaben Haiku 5.5, kein Opus. Phasen wie bisher: Planer → Bau (Werkstatt, Montage, Daten, Viewer) → fremder Prüfer.
Ein Lauf zur Zeit (das Gesamtmodell baut immer nur einer). Der Orchestrator legt die Läufe in die Warteschlange,
liest Ergebnis und Verbrauch und meldet Ben Zwischenstände.

## Plan
| Phase | Lauf (Auftragsdatei in `docs/jobs/api/`) | Inhalt | Budget (Obergrenze) | Stand |
|---|---|---|---|---|
| P0 | im Planer-Lauf | WIP-Stand Ring B2 gesichert (16 Dateien seit 05.11.) | – | **erledigt** (35e3948) |
| P1 | `unify-1-planer.md` | Quelle → `data/oasis-soll.json` + R61; Soll-Ist; Bauplan; Abweichungen | 12 USD | **erledigt** (e0dca88, 0aa5bb9, 99ce5b0, c9646ac) |
| U1 | `unify-u1-daten.md` | Lage-Probe: Soll-Lage gegen gebaute Teile, Bauplatz je Bauteil (`data/oasis-lage.json`), nichts gebaut | 8 USD | **teilweise** (10.11.): Mess-Skript und Lage-Probe laufen; 40 Bauplätze, davon 19 nur per ANNAHME D108–D110 (Technik passt nicht in die Kuppel, Ben entscheidet) |
| U2 | `unify-u2-werkstatt.md` | neue Bauteile: Sumpftank mit Pufferzonen, Podeste, Venturi, Schwimmerschalter, Schlamm-Sammelbehälter, Regentank, Nachspeise-Ventil, Notluft, Beet-Siphon-Details | 15 USD | **teilweise** (10.11.): alle 11 Komponenten gebaut und geprueft (213 Pruefungen PASS, Stand unten); NICHT erfuellt: Europa-Bezug und Lebensmittel-Nachweis je Kaufteil sind nur teilweise belegt (0 von 12 Lebensmittel belegt, 3 von 12 ohne Angebot), Venturi mit Tauchpumpe ist rechnerisch nicht belegt; `check_components.py` meldet Exit 1 (Altbefund am unveraenderten `dome.sc`) |
| U3 | `unify-u3-werkstatt.md` | Becken und Tische: Fischtank (Rand 1200, Boden −1000), Anzucht-/Lebendfutterbecken, Überläufe, Tisch- und Beethöhen als Parameter | 15 USD | offen |
| U4 | `unify-u4-montage.md` | Gesamtmodell: Becken, Sumpftanks, Gruben, Tische und Beete auf Soll-Höhe | 20 USD | offen |
| U5 | `unify-u5-montage.md` | Gesamtmodell: Technik (Vortex, Biofilter auf Podest, Pumpstellen, Venturi, Schwimmer, Luft, Schlamm), Entfernen der Ist-Teile ohne Soll | 20 USD | offen |
| U6 | `unify-u6-montage.md` | Gesamtmodell: Wasserautobahn auf 1550 mm, Einspeisung, Rückläufe, Beckenkette, Nachspeisung, Notüberlauf, Luft-/Schlammleitungen | 20 USD | offen |
| U7 | `unify-u7-montage.md` | Variantenumschaltung abbauen (`variante.py`, `gen_dome.py`, `build.sh`, Viewer, `viewer_dist.py`): nur noch eine Variante | 12 USD | offen |
| U8 | `unify-u8-daten.md` | Teileliste, Bestellliste (Europa, Link, lebensmittelecht), Bauteilbeschreibungen, Katalog | 12 USD | offen |
| U9 | `unify-u9-montage.md` | `check_latte` in Kopie, Kollisionen beheben (Verschiebung höchstens 750 mm), Gangkarte | 18 USD | offen |
| U10 | `unify-u10-viewer.md` | Viewer-Export, Kreislauf-Schalter mit Soll-Wegen, Browser-Screenshot, `viewer_dist.py` | 10 USD | offen |
| P-Prüf | eigener Lauf, nicht der Bauer (Vorlage `docs/jobs/vorlagen/pruefung.md`) | Soll-Ist-Tabelle aller Quell-Bauteile, Kollisionen, Listen | 8 USD | offen |

Summe der Obergrenzen: U1 bis U10 = 150 USD, mit Prüfer 158 USD. Das sind Obergrenzen je Lauf, keine Erwartung; gemessen wird in `tools/agent-sdk-runner/usage.jsonl`. Anhaltspunkt: dieser Planer-Lauf hat bis zum Planende etwa 5,7 USD verbraucht (Budgetzähler des Runners, 12 USD Obergrenze).

## Stand
- 10.11.2026: Quelle gesichert (f11a92d), D93 und W89 eingetragen, Planer-Auftrag geschrieben.
- 10.11.2026, Planer-Lauf (Sonnet 5.5, Agent-SDK):
  1. P0: 14 von 16 ungesicherten Dateien als WIP gesichert (`35e3948`: 6 `*-ring_b2.sc`, `scripts/dome-script-ring_b2.json`, 5 neu gespeicherte Komponenten, `viewer/extras.json`, `docs/session-notes/orchestrator.md`). Gemessen: alle mit Zeitstempel 05.11. 17:50 bis 20:40, aus dem Ring-B2-Bau (Paket n-autobahn-v2, Commit 4965331). Nicht committet, aus gutem Grund: `viewer/detail/` (laut `viewer/export_detail.py` Zeile 5 „wird nie committet“, 670 MB OBJ ignoriert, 306 erzeugte JSON) und `viewer/varianten/` (erzeugter Export wie die ignorierte `viewer/instances.json`). Beides bleibt als ungesichert stehen, nichts gelöscht.
  2. Fehlende Quelle gefunden und gesichert: `flow-diagram.html` (555 031 Byte, SHA256 `68e358…1799`, öffentlich abrufbar) = Höhenschnitt, Annahmen A1 bis A32, JSON mit 43 Bauteilen und 90 Wegen. Commit `e0dca88`.
  3. P1a `data/oasis-soll.json` (`0aa5bb9`, `99ce5b0`): 43 Bauteile (40 im Umfang), 90 Wege (77 im Umfang: 53 Wasser, 9 Luft, 6 Schlamm, 9 Strom für Pumpen/Belüftung/Schwimmer), 97 Armaturen-Zeilen (406 gezählte Stück); 45 von 45 Selbstprüfungen (`python -I -X utf8 scripts/oasis_soll.py`).
  4. P1b R61 und 14 Annahmen D94 bis D107 (`99ce5b0`). P1c Soll-Ist und P1d Abweichungen siehe unten, P1e Bauplan `docs/jobs/N-UNIFY-AUTOBAHN.md` mit 10 Runden-Aufträgen und 1 Prüfer-Auftrag in `docs/jobs/api/unify-*.md` (`c9646ac`).
  5. Wichtigste Befunde: (a) Fußboden der Quelle = Modell-Z 400, nicht 0 (D94); (b) Ring B2 im Modell ist exakt die Quell-Zeichnung um 18° gedreht (D95); (c) die Quelle zeigt Höhenschnitt und Annahmen nur in `flow-diagram.html`.

- 10.11.2026, Daten-Lauf U1 (Sonnet 5.5, Agent-SDK): `scripts/oasis_lagepruefung.py`, `data/oasis-lage.json`, `scripts/check_oasis_soll.py`, `data/oasis-messung.json`, `renders/oasis-lage.png`, Annahmen D108–D111. Prüfbefehle: (1) `python -I -X utf8 scripts/oasis_lagepruefung.py --pruefen` → Exit 0, 40 Bauteile mit Bauplatz, 0 Regelverletzungen, größte Verschiebung „Zeichnung" 667 mm, 19 Ausnahmen mit D-Nummer; (2) `python -I -X utf8 scripts/check_oasis_soll.py --liste` → 16 Messpunkte, `--teil alle` → Ausgangsmessung (Tabelle unten, Exit 1); (3) `python -I -X utf8 scripts/oasis_soll.py --pruefen` → 45 OK, 0 FAIL; (4) `git diff --stat designs/ scripts/gen_dome.py data/params.json` → leer. Wörtlich nicht erfüllt: „größte Verschiebung ≤ 750 mm" gilt nur für 6 Teile; 8 Teile liegen darüber (D110), 5 Teile außen (D109), 6 Einbauten zählen gegen den Wirt (D108). Commits: `287fadb` (Skripte, Daten, Bild), `14b6f7a` (Bereinigung des Skripts), `08da1a5` (Paket-Stand, D108–D111). Fortsetzungspunkt: Ben entscheidet D109/D111; U2 (`unify-u2-werkstatt.md`) kann sofort starten.

- 10.11.2026, Werkstatt-Lauf U2 (Sonnet 5.5, Agent-SDK; die Beschaffungs-Recherche lief als Unter-Agent): **Problem:** Die neuen Bauteile der Quelle fehlten als Komponenten. **Intent:** jedes Teil einzeln gebaut und geprueft, bevor das Gesamtmodell sie braucht (D80). **Goal:** 10 Komponenten plus Beet-Siphon-Daten nach dem Muster der Werkstatt, Gesamtmodell unveraendert.
  1. Gebaut (je `designs/components/<name>.sc`, `data/components/<name>.json`, `data/parts/<name>.json`, `docs/parts/<name>.md`, `scripts/workshop/<name>.py`, `check_<name>.py`, Eintrag in `data/descriptions.json`); Pruefung je `python -X utf8 scripts/workshop/check_<name>.py`:
     | Komponente | Teile-Nr | Koerper | Check |
     |---|---|---|---|
     | `sumpftank` (Grube 1125 x 2975 x 500, 4 Pufferzonen, Deckel 3 Platten, Pumpensockel, Zulaeufe ID25, Halter bei -110) | T101 | 19 | 46 PASS |
     | `podest_vortex` (Hoehe 577 = 1900 - 1323, Parameter `podest_vortex_h`) | T102 | 24 | 16 PASS |
     | `podest_biofilter` (Hoehe 230 = 1800 - 1570, Parameter `podest_biofilter_h`) | T103 | 24 | 16 PASS |
     | `venturi_belueffter` (Injektor Klasse Mazzei 1583 im Druckrohr d50, Rueckschlagventil, Filter) | T104 | 6 | 19 PASS |
     | `schwimmerschalter_hochstand` (Schaltpunkt -110, Meldeleitung) | T105 | 3 | 14 PASS |
     | `schlamm_sammelbehaelter` (350 l, oberirdisch, Ablasshahn von Hand) | T106 | 7 | 17 PASS |
     | `regentank_5m3` (Platzhalter, innen 4,97 m3) | T107 | 5 | 20 PASS |
     | `nachspeise_ventil` (aus T84, zweiter Eingang, Frischwasser-Kugel 30 mm tiefer) | T108 | 10 | 20 PASS |
     | `notluftpumpe` (Pumpe, Rueckschlagventil, Schlauchschleife ueber Rand 1200, Luftstein auf Boden -1000) | T109 | 8 | 17 PASS |
     | `tauchpumpe_modul` (340 x 280 x 165, Rueckschlagventil d50, Hub 1,15 m und 1,00 m aus der Soll-Datei) | T110 | 4 | 16 PASS |
     | `permakultur_modul` (elfte, D116: Kompostbox 1500 x 525, Futterzuchtkiste) | T111 | 3 | 12 PASS |
     Beet-Siphon nach A21: `data/components/ibc_beet.json` (8 Parameter `a21_*`, Teileliste, Herkunft, Funktion, Offen) und `docs/parts/ibc_beet.md` ersetzen die Lochblech-Schutzkorb-Beschreibung (ueberholt, D115); die .sc der vier Beete sind unveraendert (Geometrie in U3).
  2. Pruefbefehle (Soll, Ist), Abnahme am 10.11.2026 streng nacheinander:
     1. `python -X utf8 scripts/workshop/check_<name>.py` fuer die Komponenten: Soll alle PASS, Ist alle PASS, zusammen 213 Pruefungen, 0 FAIL-Zeilen (Tabelle oben). Teiledaten: `python -X utf8 scripts/workshop/check_parts.py <11 Namen>` -> 253 PASS, 0 FAIL.
     2. `python -X utf8 scripts/check_components.py`: Soll Exit 0, **Ist Exit 1** (nicht erfuellt): `FAIL 10 Baugruppen in der Wurzel: Ist 14, Soll 10`, Strebe B 34 statt 35. Ursache: `designs/dome.sc` (A+), unveraendert seit Commit df2f39d vom 05.11.2026; der Check liest nur diese Datei, die neuen Komponenten sind darin nicht enthalten. Der Altbefund ist nicht durch U2 entstanden und nicht von mir behoben (A+ bleibt bis U7 byte-gleich). Ersatz fuer 'keine Komponente ohne Teiledatei oder Beschreibung': `python -I -X utf8 scripts/workshop/check_u2_vollstaendig.py` -> 11 Komponenten, fehlende Dateien: keine, Exit 0.
     3. `git diff --stat designs/dome.sc designs/dome-ring_b2.sc scripts/gen_dome.py data/params.json`: Soll leer, Ist leer.
     4. `python -I -X utf8 scripts/check_oasis_soll.py --teil technik`: Exit 1 (erwartet: Altmodell steht noch auf Ausgangswerten, vortex_1/_2 -577, bio_1/_2 -230, 2 Stufenpaare verletzt; kein Absturz). Ergaenzt in diesem Lauf: Abschnitt 'Komponenten (U2)' mit den Hoehenparametern: 9 Werte aus 8 Komponenten stimmen mit der Soll-Datei ueberein (Podeste 577 und 230; Sumpf Boden -500, Pegel -250, Hochstand -110; Schwimmerschalter -110; Nachspeise-Ventil 510; Notluft-Schleife 1300; Venturi-Achse 500 ueber dem Spiegel), 4 Komponenten ohne feste Hoehe in der Quelle; Gesamtmodell 'ausstehend'. Exit-Code und Messung unveraendert.
     5. `python -X utf8 scripts/workshop/check_ibc_beet.py` (Beet-Blaetter geaendert, .sc nicht): Exit 0, == ibc_beet: 210/210 PASS.
  3. Befunde (nicht geloest, siehe Offen 11 bis 14):
     1. Venturi mit Tauchpumpe nicht belegt (D113): `check_venturi_belueffter.py` und `check_tauchpumpe_modul.py`: Mazzei 1583 braucht rund 0,69 bar Differenz (10 psi, 55 l/min), die Pumpe liefert nur 0,32 bis 0,40 bar bei null Foerderung (Hmax 3,3 bis 4,1 m); Kennlinie aus Qmax/Hmax (R59, Formeln linear, Parabel, Ellipse): Pumpstelle 1 (1,53 m) 84 / 115 / 124 l/min gegen Soll 110; Pumpstelle 2 ohne Venturi (1,38 m) 88 / 118 / 126; mit Venturi 3,5 m (A19) 20 / 36 / 69; mit Mazzei bei 10 psi (8,4 m) 0.
     2. Beschaffung (`data/beschaffung/u2_wasserkreislauf.json`, 12 Artikel, Stand 10.11.2026): 9 mit Angebot, 6 mit selbst gelesener Haendlerseite, 3 ohne Angebot in Europa (Mazzei 1583, Schlammbehaelter rund 350 l, Gitterrost 1229 x 1026 x 40), **Lebensmittel-Nachweis 0 von 12 belegt**. Oase Eco Premium 8000: beim Hersteller-Shop nicht lieferbar (Nachfolger 9000), Maße 340 x 280 x 165 gelesen und uebernommen (ersetzen die Annahme Ø 230 x 190); Luftpumpe Kerry KEA3600 (Hornbach DE, 230 V, 60 l/min, 330 x 230 x 320) als Kandidat, eine 12-V-Pumpe mit 60 l/min nicht gefunden.
     3. Parallele Checks stoeren sich: `sc.faces` und `interference` schreiben feste Dateinamen nach `sc.TMP`; ein Lauf mit zwei gleichzeitigen Checks lieferte `no body Tuelle`. Abhilfe: je Lauf eigenes `WORKSHOP_TMP` setzen oder nacheinander laufen (so geschehen).
  4. Annahmen: D112 (Pufferzonen-Durchstroemung), D113 (Venturi-Groesse, Befund), D114 (Nachspeise-Ventil gestaffelt), D115 (Beet-Siphon nur Daten, Geometrie U3), D116 (elfte Komponente Permakultur, Platzhalter-Maße); Details in `docs/decisions.md`.
  5. Designprinzipien-Check U2 (1-10): 1 Physik vor Strom: Podeste statt Pumpe, Nachspeise mechanisch, Venturi passiv; Befund: der Antriebsdruck des Venturi ist mit der Tauchpumpe nicht belegt (D113). 2 Graben: Sumpftank im Boden nur wegen der Quelle (D105), Schlamm oberirdisch, kein Bodenablauf (im Check geprueft). 3 Teile: jedes Teil mit Funktion; Permakultur als elftes Teil begruendet (D116). 4 Technik in die Kuppel: Regentank und Permakultur ausserhalb (D107), Lage der anderen offen bis U4/U5 (Verstoss U1/D109 bleibt). 5 Leitungen: Zulauf Schlauch ID25 mit freiem Auslauf, Druckrohr d50, Luftschlauch mit Schleife ueber Rand. 6 Lebensmittelecht: **Verstoss**: 0 von 12 recherchierten Artikeln mit gelesenem Herstellernachweis, als offen gefuehrt statt behauptet (D85). 7 Kaufen vor Selbstbau: Pumpen, Venturi, Schwimmerschalter, Tanks, Ventile gekauft, Selbstbau nur Podeste und Sumpf-Grube; Europa-Bezug 6 von 12 mit gelesener Seite, 3 ohne Angebot. 8 Wartbar: Deckel in 3 abhebbare Platten, Pumpe im Sumpf erreichbar; Verstoss durch die Quelle: Sumpftank im Boden schwerer zu reinigen. 9 Sicherheit: Deckel begehbar (Tragklasse und Abhebesicherung offen), Hochstand-Schalter, Notluft mit Siphon-Schleife und Rueckschlagventil; Notstrom fuer die 230-V-Pumpe offen. 10 Ehrlich messen: jede Zahl mit Befehl, Annahmen D112 bis D116, Befunde oben.
  6. Commits: `12cf486` (Sumpftank, Podeste), `a068776` (Venturi, Schwimmerschalter, Notluft, Nachspeise), `ca133f2` (Schlamm, Regentank, Permakultur, Tauchpumpe), weitere Commits dieses Laufs: `git log --oneline -6` (Teiledaten, Blaetter, Beschaffung, Beet-Siphon, Paket-Stand). Verbrauch: etwa 8,6 USD (Budgetzaehler bei Abschluss, Obergrenze 15).
  7. Fortsetzungspunkt: U2 bleibt 'teilweise', bis Offen 11 bis 14 entschieden sind; Lauf U3 (`docs/jobs/api/unify-u3-werkstatt.md`) haengt von U2 nicht ab und kann sofort starten. Naechster Befehl: `python -X utf8 scripts/workshop/check_sumpftank.py` (Gegenprobe), dann Lauf U3.

## Soll-Ist (P1c)
Ist-Messung: `python -I -X utf8 scripts/oasis_istmessung.py` (Export `viewer/varianten/ring_b2/instances.json`, Stand 05.11.2026 21:18, 5570 Instanzen; Höhen relativ zum Fußboden Z 400). Soll: `data/oasis-soll.json` (gedreht, Modellkoordinaten). Urteil: **übernehmen** (passt wie gebaut) · **verschieben** (gleiches Bauteil, andere Höhe oder Lage) · **umbauen** (Maß oder Funktion ändert sich) · **neu** · **entfernen**.
Ergebnis in Zahlen: von 40 Soll-Bauteilen im Umfang **2 übernehmen · 8 verschieben · 17 umbauen · 13 neu**; von 77 Soll-Wegen **0 passen · 20 verschieben · 32 umbauen · 25 neu**. Die Zählung steht unter den Tabellen.

### A. Bauteile (40 im Umfang)
| Soll-ID (Anzahl) | Soll: Wasserspiegel · Lage (Modell) | Ist: Komponente · Lage · Höhe | Urteil |
|---|---|---|---|
| `fish` (1) Fischtank | Wsp 750, Rand 1200, Boden −1000; Mitte | `pool_zentral(-ring_b2).sc`: Ø 3890, Wsp +515, Rand +650, Innenboden −1705, Mitte (`layout.json`, `params.json` pool_rim, `loop-state.md`) | umbauen (+235 / +550 / +705; 20,8 statt 26,4 m³; D96) |
| `nursery` (1) | Wsp 800, Rand 1000, Ø 2000; r 3550 Az −72, auf dem Boden | `zweitbecken(-ring_b2).sc`: Ø 1747, Wsp +515, Tiefe 1000 im Boden, r 4820 Az −54 | umbauen + verschieben (D96) |
| `feed` (1) | Wsp 850, Rand 1000, Ø 1000; r 5300 Az −72 | `becken_dritt_klein.sc`: Ø 800, Wanne im Boden (Z −405), r 4970 Az −30 | umbauen + verschieben (D96) |
| `filterpumpe_1/_2` (2) | Pumpe Fischtank→Vortex, +1150; r 2662 Az −44/−100 | `pumpe_gross` ×4 (Hauptkreislauf, Saugseite aus Pool über Feinfilter, Z 0), Tauchpumpe nur als Kandidat R59/D92, nicht gebaut | neu (D102) |
| `vortex_1/_2` (2) | Wsp 1900; r 4475 Az −34/−110 | `tank_klein` ×2 (Absetzer): r 4047 Az −77 und r 3287 Az −30, Standfläche Z 0, Oberkante 1323 | umbauen (Podest ≥ 577 mm, Zulauf von Pumpe; D100) |
| `bio_1/_2` (2) | Wsp 1800; r 5301 Az −23/−121 | `tank_gross`, `tank_gross_t3`: r 3385 Az −5 und r 3365 Az −98, Oberkante 1756, Überlauf gebaut 1570 | umbauen (Podest 230 mm; Lage um 1,9 m radial, Probe U1; D99, D100) |
| `sludge_1/_2` (2) | Sammelbehälter 350 l oberirdisch; r 5433 Az −42/−102 | `schlammfass` ×2 im Boden (Z −1233), r 4188 Az −20 / r 3349 Az −67 | umbauen (aus dem Boden; D104) |
| `permakultur` (1) | Platzhalter außen; r 6612 Az −72 | nicht vorhanden | neu (D104, D107) |
| `sump_1/_2` (2) | im Boden, Boden −500, Rand 0, Wsp −250, Hochstand −110, 1125 × 2975, 4 Pufferzonen; r 4329 Az −51/−93 | nicht vorhanden (`beet_sumpf` nur als Bauteil, nie gesetzt) | neu (D105) |
| `hauptpumpe_1/_2` (2) | Pumpe Sumpf→Venturi→Fischtank, +1000; r 3946 Az −50/−94 | nicht vorhanden (Rücklauf heute frei in den Pool) | neu (D102) |
| `venturi_1/_2` (2) | im Druckrohr vor dem Fischtank; r 3132 Az −43/−101 | nicht vorhanden (R60: Gebläse bleibt) | neu (D103) |
| `schwimmer_1/_2` (2) | Hochstand −110 im Sumpf; r 5588 Az −54/−90 | `sonde_level_float` ×3 (Messstellen an Pool und Becken, Z +365/+665, nicht im Sumpf) | neu (D105) |
| `nachspeise` (1) | Schwimmerventil am Fischtank, Regen vor Frisch; r 3068 | `schwimmerventil_pool`: r 2070 Az −10, Z +710, Frischwasser über `aktivkohle_station` (K39/K40) | umbauen (zweiter Eingang; D107) |
| `rain` (1) | Tank 5 m³ außen; r 6621 | nicht vorhanden | neu (D107) |
| `tap` (1) | Frischwasseranschluss; r 6564 | `aktivkohle_station` r 7906 Az −92 (K39) | übernehmen |
| `ring_1/_2` (2) | Rohrachse 1550, Ecken Az 18 + 36 k, Eckradius 3550 (gezeichnet) | `ring_ecke_d75` ×10: Eckradius 3394, Ecken Az 18 + 36 k, Rohrachse +2145; Entlüfter ×2 +2145 | umbauen (−595 mm; Radius bleibt, D98) |
| `kupplungshahn` (2) | 2 Kugelhähne d63, im Betrieb offen, Az 108 / −72, Achse 1550 | `lt_kugelhahn_d63` ×2 bei Az −73 / 107, Z +2145, laut V2 „geschlossen“ | umbauen (−595 mm, Hahnstellung/Text; D98) |
| `ringende_1/_2` (2) | Hahn d63 → Sumpf; Az 90 / 126 | `lt_kugelhahn_d63` ×4 bei +1823 (Ring-Ende und Entleerung), Ziel Pool-Rücklauf | umbauen (Ziel Sumpf; D98) |
| `abf_nft_1/_2` (2×12) | 12 Abzweige d32 je Halbring, 38 l/min | `ring_abzweig_d32` ×24, Z +2145 (r 3379 bis 3454) | verschieben (−595 mm) |
| `abf_fd_1/_2` (2×7) | 7 Abzweige d40 je Halbring, 54,5 l/min | `ring_abzweig_d40` ×14, Z +2145 | verschieben (−595 mm) |
| `nft_aussen` (8) | Wsp 1050 | `nft_tisch_aussen` ×8 (r 5074), Rinnenunterkante +1000 (D60), Film etwa +1020 [E] | übernehmen (Höhe in U4 messen, Abweichung etwa +30) |
| `nft_mitte` (6) | Wsp 900 | `nft_tisch_mitte` ×6 (r 3377), Rinnenunterkante +1000 | verschieben (≈ −120 mm; hebt D60 auf, D97) |
| `nft_innen` (10) | Wsp 1250 auf dem Poolrand (Rand 1200) | `nft_tisch_innen` ×10 (r 1864), Rinnenunterkante +1000, Kragarm über dem Pool | verschieben (≈ +230 mm, D97) |
| `fd_aussen` (8) | Flutstand 250, Beet-Boden 70, Rand 460 | `ibc_beet_aussen_800` ×8 (r 5074), Boden −162, Oberkante +475, Siphon mit Schutzkorb (W40) | verschieben (Beet +162 auf den Flur, Flutstand über Standrohr; D97) |
| `fd_mitte` (6) | Flutstand 250, Boden 70, Rand 420 | `ibc_beet_innen_933` ×6 (r 3377), Boden −209…−170, Oberkante +475 | verschieben (Beet +170…209 auf den Flur; D97) |
| `luftpumpe_1/_2` (2) | je 4 Arme (Biofilter, Sumpf, Becken, Fischtank); r 7216 (Zeichnung) | `geblaese_luft` ×2 (r 6857…7235 Az −110), `luftverteiler_6` (r 6982), `luftverteiler_4` (r 2036), `luft_scheibenbelueftung` ×4 im Pool (Z −1605) | umbauen (Arme neu verteilen, in die Kuppel; D103, D107) |
| `luftpumpe` Notluft (1) | Luftpumpe + Luftstein im Fischtank | nicht vorhanden | neu (D103) |

Zählung (`grep` auf die Urteilsspalte): übernehmen 2 (`tap`, `nft_aussen`) · verschieben 8 (`abf_nft` ×2, `abf_fd` ×2, `nft_mitte`, `nft_innen`, `fd_aussen`, `fd_mitte`) · umbauen 17 (`fish`, `nursery`, `feed`, `vortex` ×2, `bio` ×2, `sludge` ×2, `nachspeise`, `ring` ×2, `kupplungshahn`, `ringende` ×2, `luftpumpe_1/_2`) · neu 13 (`filterpumpe` ×2, `permakultur`, `sump` ×2, `hauptpumpe` ×2, `venturi` ×2, `schwimmer` ×2, `rain`, `luftpumpe`) = 40.

### B. Wege (77 im Umfang)
| Weg-Gruppe der Quelle (Anzahl) | Ist (Netz `data/leitungsnetz.json`, Ring B2) | Urteil |
|---|---|---|
| Nachspeisung e17, e18, e19 (3) | K39/K40 Frischwasser → Aktivkohle → Pool; Schwimmerventil am Pool; kein Regenwasser | umbauen |
| Pumpstelle 1 e20, e21, e22, e84 (4) | K01/K03/K17/K19/K56/K57: Pool → Feinfilter und Pumpen (Pool-Seitenablauf d75) | neu |
| Vortex → Biofilter e23, e24 (2) | K05/K06/K08/K09: Absetzer → Feinfilter → Pumpe → Biofilter | neu |
| Biofilter → Ring e25, e26 (2) | K10/K26 Biofilter → Pegelschacht → 2 Booster → Steigleitung d63 → Ring | umbauen (direkter Überlauf d63) |
| Ring, Kupplung e27 bis e32 (6) | Ring d75, 10 Ecken, 2 Kupplungsstrecken (geschlossen), Ring-Ende-Hähne (Z +2145) | verschieben |
| Ring-Ende → Sumpf e33, e34 (2) | Ring-Ende → Rücklauf Pool | neu |
| Abfahrten e35 bis e38 (4) | 24 + 14 `ring_abzweig_*` auf Z +2145 | verschieben |
| Fallleitungen e39 bis e48 (10 Wege, 38 Stück) | 38 Schlauch-Fallleitungen, 18 Ausleger (`ring_b2_schlauchwege`) | verschieben (Länge, Höhe −595) |
| Rückläufe e49 bis e57 (9) | Schlauch-Rücklauf zum Pool (FIX-c „nicht baubar“, offen) | umbauen (in die Sumpftanks, NFT Innen in den Fischtank) |
| Pumpstelle 2 e58, e59, e60, e61, e71, e72 (6) | nicht vorhanden | neu |
| Beckenkette e62, e63, e70 (3) | K33/K34 Rücklauf 1 → Zweitbecken → Pool | umbauen |
| Notüberlauf e81, e82 (2) | nicht vorhanden | neu |
| Luft e77, e86 bis e89, e91 bis e94 (9) | K44 bis K51 Gebläse → Pool, Biofilter, Absetzer, Zweit-, Drittbecken | umbauen |
| Schlamm e64 bis e69 (6) | K07/K23 Absetzer → Schlammfass (im Boden); Schlamm von Hand zum Kompost | umbauen |
| Strom/Meldung e13, e14, e15, e75, e76, e80, e83, e85, e90 (9) | Kabel `kabel` im Netz für Pumpen und Gebläse; keine Schwimmer-Meldung | neu |

Zählung: verschieben 6 + 4 + 10 = 20 · umbauen 3 + 2 + 9 + 3 + 9 + 6 = 32 · neu 4 + 2 + 2 + 6 + 2 + 9 = 25 · passt 0 = 77.

### C. Ist ohne Gegenstück in der Quelle (entfernen oder begründet behalten, D101)
| Ist-Bauteil (Anzahl) | Befund | Urteil |
|---|---|---|
| `feinfilter` ×2 (Gruben Z −496) | Quelle kennt keinen Feinfilter; D51/D55/D72 überholt | entfernen (Designprinzip 3) |
| `pumpe_klein` ×4 | Absetzer-Teilstrom entfällt (Vortex hängt in der Linie) | entfernen |
| `pumpe_gross` ×8 (4 Hauptkreislauf + 4 Booster) | ersetzt durch 4 Pumpen (2 + 2) | entfernen |
| `pegelschacht` ×2 samt Podest | Quelle: Biofilter höher als Ring, kein Zwischenbehälter | entfernen |
| `schlammfass` ×2 im Boden | → Sammelbehälter oberirdisch (siehe A) | entfernen (W79) |
| A+-Leitungen (Rückbau-Umfang 63 Trassen, 56,3 m laut `docs/packages/m10-zielbild-s.md`), Heber, Verteiler | nicht im Soll; Wege neu nach B | entfernen |
| Pool-Geländer (Zielbild S, nicht gebaut) | Rand 1200 mm ≥ 1000 mm (D90), Designprinzip 9 erfüllt durch die Wand | entfällt |
| `aktivkohle_station` | Chlor im Frischwasser tötet Fische und Nitrifikanten; Quelle nennt nur Regenwasser salzfrei und chlorfrei | behalten (Designprinzip 9) |
| `puffer_klein`, Messzelle, Dosierung, Messstellen/Sonden | Messtechnik, nicht im Kreislauf verschaltet (D65, W76, Designprinzip 10) | behalten (offene Frage an Ben) |
| `schaltschrank` | Steuerung der Quelle liegt gezeichnet am Rand, D87 innen | behalten (D87) |
| Ringtragwerk: `ringstuetze_d75_b` ×3, Portal-Joche ×8, Montageschienen ×10 | Quelle: „Ring d75 auf Schellen“ | behalten, Höhe −595 mm |
| `luft_scheibenbelueftung` ×4 im Pool (Z −1605) | Quelle: Belüftung über Venturi, Notluftstein, Anlage mit Armen | verschieben (Pool-Boden −1000) |

## Abweichungen zum Altbestand (P1d)
Die Quelle gewinnt (D93). Reihenfolge nach Gewicht; „Folge“ nennt die Runde, in der es umgesetzt wird.
| Nr | Altbestand (Entscheidung/Wunsch/Blatt) | alt | neu (Quelle) | Folge |
|---|---|---|---|---|
| 1 | D88, W85 Zielbild S (Pool) | Pool 665 mm tiefer, Rand ≈ Flur, Geländer, eine Pumpstufe | Fischtank teilversenkt: Boden −1000, Rand 1200, Wsp 750, zwei Pumpstellen, Fischtank bleibt tiefster Punkt | U3, U4 |
| 2 | N-AUTOBAHN-V2, D92 (Ring, Pegelschacht, Booster) | Ring auf 2145; Biofilter-Überlauf 1570 → Pegelschacht → 2 Booster → Steigleitung; Kupplung geschlossen | Ring 1550; Biofilter 1800 und Vortex 1900 höher als der Ring, Überlauf d63 direkt; Kupplung offen; Pumpe nur Fischtank → Vortex (+1150) | U5, U6 |
| 3 | A+-Rücklauf in den Pool (K16/K32), Beet-Sumpf nur Bauteil, D75 Subtank (V4) | alle Rückläufe frei in den Pool | Rückläufe in zwei Sumpftanks im Boden, Pumpstelle 2 + Venturi hebt 1,00 m in den Fischtank; nur NFT Innen direkt in den Fischtank | U4, U5, U6 |
| 4 | D38, D51, D55, D71, D72 (Pumpen klein, Feinfilter, Absetzer-Kreis) | Feinfilter ×2, Pumpe klein ×4, Absetzer im Teilstrom | entfallen; Vortex in der Linie, Schlamm per Schwerkraft in den Sammelbehälter | U5 |
| 5 | W70, D81 E20, W78 (A+ und Ring B2 umschaltbar) | zwei Varianten, Schalter in Skripten, Modell, Viewer | nur noch eine Variante | U7 |
| 6 | D58, D60, D61 (Tischhöhe) | Rinnenunterkante 1000 für alle drei Ringe | Wsp NFT Außen 1050, Mitte 900, Innen 1250 (auf dem Poolrand) | U3, U4 |
| 7 | D08, D13, D26 (Pool-Tiefe, „zum Teil eingelassen“) | Tiefe 2200 bis 2340, Wsp +515 | Wassertiefe 1750, Wsp 750, 20,8 m³ (Quelle 22 m³) | U3, U4 |
| 8 | D36, D42, D46, D48, D50, D63, D66, D70 (Zweit-, Drittbecken) | Zweitbecken Fische r 4820 Az −54; Drittbecken klein Quarantäne r 4970 Az −30, im Boden | Anzuchtbecken Ø 2000 und Lebendfutterbecken Ø 1000 in einer Reihe auf Az −72, auf dem Boden, Überläufe von außen nach innen; Quarantäne-Funktion entfällt | U3, U4 |
| 9 | W79, D88 (Schlamm) | Schlammfass im Boden | oberirdischer Sammelbehälter, Permakultur-Modul außen | U2, U5 |
| 10 | D84, W72, W82, D90 (Wasserstation, Hahn je Strang) | Wasserstation je Linie am Biofilter, 7 Hähne je Linie | entfällt; Abzweig-Kugelhahn am Ring + Regelhahn d25 auf Greifhöhe je Abnehmer (38 + 38) | U6 |
| 11 | D90 (Geländer 1,0 m am Pool) | Geländer auf der Aufkantung | entfällt, Rand 1200 mm | U3 |
| 12 | N-AUTOBAHN-V2 Abschnitt 2.2, D98 | Ring-Ende leitet in den Pool-Rücklauf | Ring-Ende-Hahn in den Sumpf der eigenen Linie | U6 |
| 13 | R60, Belüftung: Gebläse ×2 außen | Gebläse außen, Verteiler 6 und 4 Arme | Belüftungsanlage 2 × 4 Arme zu Biofilter, Sumpf, Becken, Fischtank; Venturi ×2; Notluftpumpe ×1; alles in der Kuppel | U5 |
| 14 | W40-BEET, D77 (Beet-Siphon) | Standrohr d25, Lochblech-Schutzkorb | Siphon mit Abtropfgitter, Vlies, Sieb, Belüftung unten (A21); Flutstand 250 | U2 (Daten und Blatt erledigt, D115), U3 (Geometrie), U4 |
| 15 | D86, W75 (Leitungsordnung v2, Schläuche), W87, W88 | – | **bestätigt**, nicht überholt (Fallleitungen frei hängend, Rücklauf Schlauch) | – |
| 16 | D40 (Fischmenge 475 kg in 26,4 bis 27,8 m³) | Auslegung 475 kg, 680 Fische | Quelle rechnet 120 Fische/85 kg in 22 m³ (Showcase-Parameter, nicht Teil des Kreislaufs): D40 bleibt, Biomasse in 20,8 m³ neu rechnen | U8 (Daten), offen |

## U1: Ausgangsmessung und Lage-Probe (Daten-Lauf, 10.11.2026)
**Problem:** Ob die Soll-Lage in die gebaute Kuppel passt, und wie der Wasserspiegel am gebauten Modell gemessen wird, war offen. **Intent:** vor jedem Bau Bauplatz und Messvorschrift festlegen (D99). **Goal:** 40 Bauplätze ohne Kollision und ein Mess-Skript für 16 Wasserspiegel (±50 mm).

### Ausgangsmessung (Altmodell, Export 05.11.2026 21:18)
Befehl: `python -I -X utf8 scripts/check_oasis_soll.py --teil alle` (Exit 1 = Abweichung, erwartet). Ist = Mittel der Instanzen, in mm über Fußboden (Z-Bezug 400); Messvorschrift je Punkt in `data/oasis-messung.json`.
| Punkt | Soll | Ist | Abweichung | Urteil |
|---|---|---|---|---|
| `fish` | 750 | 515 | -235 | ABWEICHUNG |
| `nursery` | 800 | 515 | -285 | ABWEICHUNG |
| `feed` | 850 | 515 | -335 | ABWEICHUNG |
| `vortex_1` | 1900 | 1323 | -577 | ABWEICHUNG |
| `vortex_2` | 1900 | 1323 | -577 | ABWEICHUNG |
| `bio_1` | 1800 | 1570 | -230 | ABWEICHUNG |
| `bio_2` | 1800 | 1570 | -230 | ABWEICHUNG |
| `ring_1` | 1550 | 2145 | +595 | ABWEICHUNG |
| `ring_2` | 1550 | 2145 | +595 | ABWEICHUNG |
| `nft_aussen` | 1050 | 1020 | -30 | OK |
| `nft_mitte` | 900 | 1020 | +120 | ABWEICHUNG |
| `nft_innen` | 1250 | 1020 | -230 | ABWEICHUNG |
| `fd_aussen` | 250 | 365 | +115 | ABWEICHUNG |
| `fd_mitte` | 250 | 354 | +104 | ABWEICHUNG |
| `sump_1` | -250 | fehlt (keine Komponente `sumpftank`) | – | FEHLT |
| `sump_2` | -250 | fehlt (keine Komponente `sumpftank`) | – | FEHLT |

Ergebnis: 1 von 16 Punkten innerhalb ±50 mm (`nft_aussen`), 13 mit Abweichung, 2 fehlen (Sumpftank ist nicht gebaut). Stufenreihenfolge: 15 Paare, davon 7 erfüllt, 6 verletzt (Vortex > Biofilter ×2, Biofilter > Ring ×2, Anzucht > Fischtank und Lebendfutter > Anzucht, weil alle drei Becken heute +515 stehen) und 2 nicht prüfbar (Sumpf fehlt). Zeile des Skripts: `ERGEBNIS: ABWEICHUNG (23 Abweichungen oder fehlende Werte)`.

### Lage-Probe (nach dem Entfernen der Ist-Teile aus Abschnitt C)
Befehle: `python -I -X utf8 scripts/oasis_lagepruefung.py` (rechnet, schreibt `data/oasis-lage.json`, etwa 2 Minuten), `... --pruefen` (misst die Datei neu, Sekunden), Bild `renders/oasis-lage.png` (rot = Zeichnung, grün = Bauplatz, blau = Tür-Gang). Regeln: 150 mm Luft zu allem, was in Z berührt oder überlappt; Wandluft 100 mm zur Zehneck-Wand (Apothema 5706); Kuppelkugel 5800 mm auch in der Höhe; Tür-Gang 900 mm von der Tür (Az −72) bis zum Zentralpool; Laufweg 500 mm als Flutung von der Tür (50-mm-Raster, Knie- und Kopfscheibe). Suche: Raster 50 mm bis 750 mm, darüber 100 mm bis 3600 mm; vier Reihenfolgen, die beste zählt.

**Befund: Die Soll-Technik passt in der gebauten Kuppel nicht vollständig hinein.** Die Lücke im Außenring ist 72° breit (8 von 10 Tischen), die Zeichnung rechnet mit 120°. Gemessen: Von 19 frei stehenden Teilen haben je nach Reihenfolge 4 bis 7 keinen kollisionsfreien Platz in der Kuppel; die erste Fassung (4 Teile außen) schnürte den Zugang ab (34 Tische, Beete und Teile über 500-mm-Gänge nicht mehr erreichbar), erst mit 5 Teilen außen sind es 0.

| Bauteil | Ort | Soll r / Az (Zeichnung, gedreht) | Bauplatz r / Az | Drehung ° | Z Modell | Verschiebung mm | Modus |
|---|---|---|---|---|---|---|---|
| `rain` | aussen (Platzhalter) | 6620.6 / -169.6 | 7064.0 / -170.3 | 18.0 | 400.0 | 450 | Zeichnung (≤ 750) |
| `tap` | aussen (Platzhalter) | 6563.6 / -163.1 | 7229.4 / -163.5 | 18.0 | 400.0 | 667 | Zeichnung (≤ 750) |
| `nachspeise` | innen | 3068.1 / -176.2 | 2502.9 / -169.5 | 0.0 | 1150.0 | 650 | Zeichnung (≤ 750) |
| `fish` | innen | 0.0 / 0.0 | 0.0 / 0.0 | 0.0 | -600.0 | 0 | bleibt |
| `nursery` | innen | 3550.0 / -72.0 | 4461.6 / -51.2 | 108.0 | 400.0 | 1703 | ANNAHME D110 |
| `feed` | innen | 5300.0 / -72.0 | 4048.0 / -86.6 | 108.0 | 400.0 | 1720 | ANNAHME D110 |
| `filterpumpe_1` |  | 2661.8 / -44.0 | 1702.5 / -44.0 | 0.0 | -600.0 | 959 | Einbau D108 im Wirt `fish` |
| `filterpumpe_2` |  | 2661.8 / -100.0 | 1702.5 / -100.0 | 0.0 | -600.0 | 959 | Einbau D108 im Wirt `fish` |
| `vortex_1` | innen | 4475.3 / -34.5 | 2958.6 / -24.7 | 7.4 | 977.0 | 1640 | ANNAHME D110 |
| `vortex_2` | aussen (Vorbau) | 4475.3 / -109.5 | 6873.0 / -120.6 | -151.4 | 977.0 | 2625 | ANNAHME D109 |
| `bio_1` | innen | 5301.2 / -22.6 | 4841.8 / -27.5 | 157.4 | 630.0 | 632 | Zeichnung (≤ 750) |
| `bio_2` | innen | 5301.2 / -121.4 | 3872.4 / -110.6 | 73.6 | 630.0 | 1664 | ANNAHME D110 |
| `sludge_1` | aussen (Vorbau) | 5432.8 / -41.9 | 6811.7 / -51.5 | 0.0 | 400.0 | 1712 | ANNAHME D109 |
| `sludge_2` | aussen (Vorbau) | 5432.8 / -102.1 | 7433.2 / -85.7 | 0.0 | 400.0 | 2702 | ANNAHME D109 |
| `permakultur` | aussen (Platzhalter) | 6612.5 / -72.0 | 7721.9 / -73.1 | 18.0 | 400.0 | 1118 | ANNAHME D110 |
| `ringende_1` | innen | 3225.2 / 90.0 | 3225.2 / 90.0 | 90.007 | 1950.0 | 0 | Zeichnung (≤ 750) |
| `ringende_2` | innen | 3225.2 / 126.0 | 3225.2 / 126.0 | 125.993 | 1950.0 | 0 | Zeichnung (≤ 750) |
| `sump_1` | aussen (Vorbau) | 4329.3 / -50.8 | 7560.7 / -44.1 | 93.0 | -100.0 | 3302 | ANNAHME D109 |
| `hauptpumpe_1` |  | 3946.2 / -49.7 | 7190.2 / -43.0 | 0.0 | -100.0 | 3302 | Einbau D108 im Wirt `sump_1` |
| `venturi_1` | innen | 3132.5 / -43.4 | 3247.9 / -40.3 | 0.0 | 1650.0 | 206 | Zeichnung (≤ 750) |
| `sump_2` | aussen (Vorbau) | 4329.3 / -93.2 | 7550.1 / -104.1 | 123.0 | -100.0 | 3400 | ANNAHME D109 |
| `hauptpumpe_2` |  | 3946.2 / -94.3 | 7190.3 / -105.3 | 0.0 | -100.0 | 3400 | Einbau D108 im Wirt `sump_2` |
| `venturi_2` | innen | 3132.5 / -100.6 | 3066.3 / -98.9 | 0.0 | 1650.0 | 112 | Zeichnung (≤ 750) |
| `schwimmer_1` |  | 5587.6 / -54.2 | 8775.3 / -47.1 | 0.0 | 290.0 | 3302 | Einbau D108 im Wirt `sump_1` |
| `schwimmer_2` |  | 5587.6 / -89.8 | 8732.9 / -100.5 | 0.0 | 290.0 | 3400 | Einbau D108 im Wirt `sump_2` |
| `luftpumpe` | innen | 6937.5 / -143.1 | 4398.2 / -160.5 | 36.9 | 400.0 | 3041 | ANNAHME D110 |
| `luftpumpe_1` | innen | 7215.7 / -6.6 | 4284.4 / 5.0 | -171.6 | 400.0 | 3139 | ANNAHME D110 |
| `luftpumpe_2` | innen | 7215.7 / -137.4 | 4375.4 / -125.1 | 27.6 | 400.0 | 3087 | ANNAHME D110 |

Bleibende Gruppen (Lage nach Modell, nur die Höhe ändert sich; Plätze samt Z in der Datei): `ring_1` (5 Plätze, Z 1950.0), `ring_2` (5 Plätze, Z 1950.0), `kupplungshahn` (2 Plätze, Z 1950.0), `abf_nft_1` (12 Plätze, Z 1950.0), `abf_fd_1` (7 Plätze, Z 1950.0), `abf_nft_2` (12 Plätze, Z 1950.0), `abf_fd_2` (7 Plätze, Z 1950.0), `nft_aussen` (8 Plätze, Z 400.0), `fd_aussen` (8 Plätze, Z 400.0), `nft_mitte` (6 Plätze, Z 400.0), `fd_mitte` (6 Plätze, Z 400.0), `nft_innen` (10 Plätze, Z 400.0).
Zählung (`--pruefen`): 40 Bauteile mit Bauplatz, 0 Regelverletzungen nach Verschiebung, größte Verschiebung im Modus „Zeichnung" 667 mm (6 Teile, Grenze 750); 19 Teile mit ANNAHME: 6 Einbauten (D108), 5 Vorbau außen (D109), 8 über 750 mm (D110). Befund Tür-Gang: Der Ring auf 1550 kreuzt die Tür-Achse (Kupplungsstrecke Az −72) unterhalb der Kopfscheibe 1,7 m (D111).

**Designprinzipien-Check U1 (1–10):** 1 Physik vor Strom: nicht berührt (keine Pumpe geändert; Fischtank bleibt tiefster Punkt, Rücklaufwege werden in U6 geprüft). 2 Graben: Sumpf-Gruben entstehen außen statt innen, Aushubmenge gleich (D105). 3 Teile: kein Teil neu, keines gestrichen (Streichen nur als Option (b)). 4 Technik in die Kuppel: **VERSTOSS** bei 5 Teilen (Sumpftank 1 und 2, Vortex 2, Schlamm 1 und 2), begründet durch Platz (gemessen, D109). 5 Leitungen: nicht berührt (U6). 6 Lebensmittelecht: nicht berührt (U2, U8). 7 Kaufen vor Selbstbau: nicht berührt. 8 Wartbar: Tür-Gang 900 mm frei, alle Tische, Beete und Soll-Teile über 500-mm-Gänge erreichbar (0 gesperrt), Vorbau-Teile von außen zugänglich. 9 Sicherheit: Rand 1200 bleibt; Sumpf-Deckel außen müssen gesichert werden (U2); Notluftpumpe steht in der Kuppel. 10 Ehrlich messen: jede Zahl mit Befehl; Annahmen [A] genannt; Greedy-Suche ist kein Optimum.

Vergleichsrechnungen (je `... --ohne <Hindernisse>`, nichts geschrieben): ohne Puffer klein → 4 Teile ohne Platz (Vortex 2, Schlamm 2, Anzucht, Lebendfutter; beide Sumpftanks passen dann hinein); ohne Puffer klein und ohne Außentisch/Außenbeet Az −108 → 5 Teile ohne Platz (nicht besser). Die Suche ist ein Greedy-Verfahren, keine Optimierung: sie zeigt, dass diese Anordnung nicht gefunden wurde, nicht dass es keine gibt.

**Grenzen (Designprinzip 10):** Fußabdrücke aus den Körper-Boxen (`viewer/detail`, Pool aus der A+-Datei: Hülle Radius 2095), Podest-Überstand 50 mm, Behälterwand 60 mm, Tür-Vorplatz 900 × 1500 und Notluftpumpe 300 × 250 sind Annahmen [A]; Tauchpumpen-Größe aus der Zeichnung (Ø 275); Portale als Beet + 115 mm (D54). Die Zufahrt der Zulaufleitung außen ist nicht geprüft (U6).

## Offen (an Ben, nicht blockierend: Annahmen D94 bis D107 gelten bis zum Zwischencheck, D81-Regel)
1. DEINE ENTSCHEIDUNG: Pool-Rand 1200 mm (Quelle, A26/Q18 „Ja, B umsetzen“) statt „ebenerdig“ (D88, W85)? Empfehlung: Quelle, weil Ben es am 09.11. so bestätigt hat und 5,0 m³ weniger Aushub entstehen.
2. DEINE ENTSCHEIDUNG: Quarantäne-Funktion des Drittbeckens (D46) entfällt zugunsten des Lebendfutterbeckens? Empfehlung: ja, ein Becken weniger; bei Bedarf Anzuchtbecken.
3. DEINE ENTSCHEIDUNG: 20,8 statt 22 m³ Fischtank (Radialbudget des Modells, D96) und 475 kg Biomasse (D40) neu rechnen? Empfehlung: ja, in U8.
4. DEINE ENTSCHEIDUNG: Messtechnik (`puffer_klein`, Dosierung) im Modell behalten (Empfehlung) oder streichen.
5. ICH (Orchestrator), empfohlener nächster Schritt: Läufe U1 bis U10 in die Warteschlange legen, ein Lauf zur Zeit; nächster Lauf: U1 (`docs/jobs/api/unify-u1-daten.md`). Dazu den Roadmap-Eintrag `N-UNIFY-AUTOBAHN` anlegen und W89 im Wunschbuch auf „in Arbeit“ setzen (der Planer ändert `data/roadmap.json` nicht).
6. DEINE HANDLUNG (Ben): Leon die Abweichungen von seiner Quelle zeigen (`docs/research/R61-oasis-wasserkreislauf.md` Abschnitt 3 und 4, Annahmen D94 bis D107; besonders Fußboden Z 400, Drehung 18°, Fischtank 20,8 statt 22 m³, Quarantäne entfällt), bevor U4 baut: die Quelle ist seine, das Ziel ist ein Kreislauf, auf den sich beide einigen.
7. ICH (Orchestrator) oder DEINE ENTSCHEIDUNG: `.gitignore` um `viewer/detail/*.json` und `viewer/varianten/` ergänzen? Beide Ordner stehen seit dem 05.11. als ungesichert im `git status`; `viewer/export_detail.py` Zeile 5 sagt „wird nie committet“. Empfehlung: ja, damit der Hinweis „NICHT COMMITTET“ nicht dauerhaft auf Erzeugtes zeigt.
8. DEINE ENTSCHEIDUNG (U1, D109): Soll-Technik passt nicht in die Kuppel. Optionen: (a) Sumpftank 1 und 2, Vortex 2 und beide Schlamm-Sammelbehälter als Vorbau außen (Annahme, verstößt gegen Designprinzip 4); (b) Puffer klein (Messtechnik) entfällt, dann stehen nur Vortex 2, Schlamm 2, Anzucht- und Lebendfutterbecken außen und beide Sumpftanks innen; (c) Quelle ändern (weniger Teile). Die Daten in `data/oasis-lage.json` gelten für (a), weil (b) ein Teil streicht, das du nicht freigegeben hast (offene Frage 4). Empfehlung: (b), weil die Sumpftanks mit Pumpe und Venturi dann im Kreislauf bleiben und nur die Messtechnik wegfällt; ICH setze es auf dein Ja um (Lauf U1 mit entferntem `puffer_klein:1` wiederholen, Anzucht- und Lebendfutterbecken kämen dann nach außen).
9. DEINE ENTSCHEIDUNG (U1, D111): Ring auf 1550 kreuzt die Tür-Achse mit etwa 1,51 m lichter Höhe. Optionen: so lassen (Bücken an der Tür-Achse) oder Ring-Stück an der Tür-Achse auf mindestens 2100 anheben. Empfehlung: anheben; ICH plane es in U6.
10. ICH (nächster Schritt, empfohlen): Lauf U2 (`docs/jobs/api/unify-u2-werkstatt.md`) starten; er hängt von keiner der beiden Entscheidungen ab (Bauteile, nicht Lage). U4/U5 warten auf Entscheidung 8.
11. DEINE ENTSCHEIDUNG (U2, D113): Der Venturi-Belueffter ist mit der Tauchpumpe nicht belegt (0,69 bar noetig, 0,32 bis 0,40 bar verfuegbar; 110 gegen 55 l/min). Optionen: (a) Niederdruck-Venturi (Teichbelueftung) statt Mazzei; (b) Injektor im Nebenstrom mit staerkerer Pumpe; (c) Venturi weglassen und die Belueftungsanlage tragen lassen (weicht von der Quelle ab, R60: Venturi allein deckt den Bedarf nicht). Empfehlung: (a); ICH suche in U8 einen Niederdruck-Typ mit Europa-Bezug und rechne ihn gegen die Pumpenkennlinie.
12. DEINE ENTSCHEIDUNG (U2): Oase Eco Premium 8000 ist beim Hersteller-Shop nicht lieferbar (Nachfolger 9000), die Kennlinie ist nur aus Qmax/Hmax gerechnet. Optionen: (a) Eco Premium 9000 pruefen; (b) Aquaforte EC-10000 (R59-Rueckfall); (c) Pumpentyp offen lassen bis U8. Empfehlung: (c) mit ICH-Auftrag in U8, Datenblatt des 9000 lesen und Kennlinie belegen.
13. ICH (U8): Beschaffung nachziehen: Mazzei-/Niederdruck-Haendler, runder Schlammbehaelter um 350 l, Gitterrost nach Maß, Lebensmittel-Nachweis je Artikel; wo kein Herstellernachweis vorliegt, steht 'offen' mit Rueckfall in `data/beschaffung/u2_wasserkreislauf.json`.
14. DEINE HANDLUNG (Ben, optional): Herstelleranfragen per E-Mail fuer D85 (schriftliche Auskunft zu Fisch- und Lebensmittelvertraeglichkeit): Oase (Pumpe), Mazzei (Injektor), Hersteller der EPDM-Folie. Empfehlung: ja, ein Satz je Hersteller; ICH formuliere die Texte auf Zuruf.

## Verbrauch (aus `tools/agent-sdk-runner/usage.jsonl`, je Lauf)
| Lauf | Modell | USD | Token Eingabe/Ausgabe/Cache gelesen/geschrieben |
|---|---|---|---|
| P1 Planer (unify-1) | Sonnet 5.5 | etwa 5,7 (Budgetzähler des Runners bei Planende, Obergrenze 12); die genaue Zeile trägt der Runner nach | – |
| U1 Daten (unify-u1) | Sonnet 5.5 | etwa 6,3 (Budgetzähler des Runners bei Abschluss, Obergrenze 8); die genaue Zeile trägt der Runner nach | – |
| U2 Werkstatt (unify-u2) | Sonnet 5.5 (plus Recherche-Agent Sonnet, 130 000 Token laut Rueckmeldung) | etwa 8,6 (Budgetzaehler des Runners bei Abschluss, Obergrenze 15); die genaue Zeile traegt der Runner nach | - |

## DoD
- [ ] Soll-Ist-Tabelle: alle Wasser-Bauteile und -Wege der Quelle gebaut, Wasserspiegel ±50 mm, Stufen exakt
- [ ] Nur noch eine Variante in Skripten, Modell, Viewer (A+/Ring-B2-Schalter entfernt oder auf eine Variante gesetzt)
- [ ] Teileliste, Bestellliste (Europa, Link, lebensmittelecht D85), Bauteilbeschreibungen für jedes neue Teil
- [ ] `check_latte`: keine neue Kollision durch den Kreislauf
- [ ] Fremder Prüfer PASS
- [x] Abweichungen Altbestand ↔ Quelle vollständig notiert, Annahmen in `docs/decisions.md` (D94 bis D107, 10.11.2026)
