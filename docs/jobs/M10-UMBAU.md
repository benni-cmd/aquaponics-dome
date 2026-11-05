# M10-UMBAU Gebaute Leitungen S0 bis S2 und Luft A nach der Leitungsordnung neu verlegen, Schlammablass und Ueberlauf schliessen (Montage)

Planer: Opus 5.5, 05.11.2026 (planer-m10-aplus, Folgeauftrag `docs/jobs/start/N-REWORK-folge.md` Abschnitt A, 72dc3d3). Nur gelesen. Kette: **M10-UMBAU** -> LUFT-B -> S2N -> S3 -> S4 -> S5 -> S6 -> S7 -> CHECK.

**Problem:** Die gebauten 21 Kanten (K01 bis K06, K08 bis K10, K17 bis K22, K24 bis K26, K44, K56, K57) liegen schraeg, in Bogenketten und ohne Halter (Maengel M05, M06, M10, M04); die Schlammablaesse an den vier Tanks enden blind (M03); der Biofilter-Ueberlauf K10/K26 endet frei in Z 1970 (M08); die Luftrohre K44 laufen in Bogenketten (M07, M10); zwei d75-Steiger stehen im Kasten von Tischen (M09).
**Intent:** Ben (W71) will saubere, realistische Leitungen; alle folgenden Schritte (S2N bis S7) bauen auf diesem Bestand auf, deshalb zuerst umbauen.
**Ziel in einem Satz:** Der ganze Bestand ist nach `docs/leitungsordnung.md` neu verlegt (R1 bis R9 0 Verstoesse), mit Haltern, K07/K23 mit Schlammfass gebaut, die Biofilter-Ablaesse geschlossen, die Verteiler am K10/K26-Ende gesetzt, Heber-Reserve unveraendert >= 85 mm.

## Aktualitaetspruefung (05.11.2026, Regel W44)
Ergebnis: **angepasst**.
1. Maengel-Inventur (7d59462) und Folgeauftrag (72dc3d3) gelesen; D82 Nachtmodus (hoechstens 2 schwere SolidCraft-Laeufe, freier Arbeitsspeicher >= 10 GB vor dem Build).
2. Subtank M10-S2V bleibt geparkt (D81). Die Inventur ordnete M05/M06 an K02, K06, K18, K22, K56, K57 dem Subtank-Umbau zu; weil der geparkt ist, verlegt M10-UMBAU diese Strecken neu.
3. Werkstatt geliefert: `schlammfass.sc` (220 l, Stutzen d40 Mitte Deckel, Grube Ø 800 / 950), `lt_kugelhahn_feder_d40.sc` (f7fd740), `lt_schacht_kugelhahn_d63_tief_senkrecht/_waagerecht.sc` (0462ec8). Befund 14a: auf K22-T ist heute keine Gerade fuer den Stamm-Hahn frei (K18 laeuft 68 mm daneben); die Neuverlegung loest das (Schritt 3).
4. N-VARIANTEN (W70): A+ bleibt Grundstellung; liegt die Varianten-Weiche V1b vor dem Start vor, tragen A+-only-Teile `varianten: ["a_plus"]` (`docs/jobs/N-VARIANTEN.md`).
5. **M07 bewertet (Planer):** Luft im Poolwasser ist gewollt (Scheiben liegen am Boden, R45/W37-3). Keine Durchfuehrung durch Poolwand oder -boden (Leckage-Risiko ohne Nutzen). Neu: je Strang Verteiler -> ein Etagenbogen ueber die Krone -> lotrechter Steiger an der Innenwand (Halter `lt_klemme_d25` an der Wand) -> ein 90-Grad-Bogen am Boden -> waagerecht zur Scheibe; der Wasserkoerper zaehlt nicht als Kollision.

## Eingaben (nur diese)
- `docs/leitungsordnung.md` (ganz), `docs/model-maengel.md` Tabelle M01 bis M12.
- `data/leitungstrassen.json` (Bestand), `scripts/trassen_linie.py`, `scripts/trassen_luft.py`, `scripts/leitungen.py`, `scripts/check_leitungen.py`, `scripts/r45_heber.py`, `renders/maengel/inventur.py` (Messskript der Inventur, Aufruf `python -I -X utf8 renders/maengel/inventur.py <Repo-Wurzel> <aus.json>`).
- `docs/leitungsnetz-umhaengen.md` (Linie 1 Ost: Tank_klein:2, Pumpe_klein:3/4, Pumpe_gross:1/2, Tank_gross:1; Linie 2 West: Tank_klein:1, Pumpe_klein:1/2, Pumpe_gross:3/4, Tank_gross_t3:1).
- `docs/parts/schlammfass.md`, `docs/parts/leitungsteile.md` (Federhahn d40, Kappe, Klemme, Verteiler d50), `docs/parts/schacht_kugelhahn_tief.md` (Platzbedarf), `docs/packages/m10-leitungen.md` Abschnitte 13 und 14a.

## Schritte (je Schritt ein Pfad-Commit)
1. **Pruefskript:** `scripts/check_leitungsordnung.py` nach `docs/leitungsordnung.md` (R1 bis R9 plus R10 Abdeckung: Netz-Kanten ohne Trasse, Liste wie M01). Lauf auf dem Bestand, Zahlen als "vorher" ins Paket (Soll vorher etwa: 74 schraeg, 4 Ketten, 0 Halter, 36 Kanten ohne Rohr).
2. **Router:** 15-Grad-Raster in `scripts/trassen_linie.py` ersetzen: Manhattan-Wege im Welt-Rahmen (KG, KH), 90-Grad-Ecken, Feld `korridor` je Segment; Bauteil-Ports, Pool-Stutzen und Achshoehen bleiben.
3. **Linie 1 neu** (K01 bis K06, K08 bis K10, K56): Graeben KG achsparallel und gebuendelt (K06-T, K02, K56, K03, K05 so weit moeglich in einem Graben); Heber nach Ausnahme 1; **Reserve fuer S2N:** je Stamm (K06-T) eine Gerade >= 262 mm frei fuer `lt_schacht_kugelhahn_d63_tief_waagerecht` plus 100 mm Luft zu jeder Nachbartrasse, Platz fuer die Schaechte an KH1 (senkrecht, innen 188 x 400). Pumpen-Saug und -Druck (KH) achsparallel an der Pumpentafel, Halter nach R6.
4. **Linie 2 neu** (K17 bis K22, K24 bis K26, K57) gleich; K18 nicht mehr parallel in 68 mm neben K22-T, damit der Stamm-Hahn Linie 2 Platz hat.
5. **Schlammablass M03:** K07/K23: je Linie `schlammfass` in Grube neben dem Absetzer (ausserhalb Gang A/B, nicht ueber den Graeben aus Schritt 3/4), `lt_kugelhahn_feder_d40` an der Kegelspitze, Rohr d40 mit Gefaelle >= 1 % zum Deckelstutzen. Biofilter-Tanks `Tank_gross:1` und `Tank_gross_t3:1`: Kegel-Ablass ohne Netz-Kante bekommt Kugelhahn plus `lt_kappe_*` (Wartungsablass, Befund an den Orchestrator: Netz-Knoten fehlt).
6. **Ueberlauf M08:** je Linie `lt_verteiler_d50` mit Muffe A auf dem K10/K26-Ende (KH, Halter je Seite), alle vier Abgaenge vorerst mit Kappe (`lt_kappe_d50`, `lt_kappe_d20`; d40/d32-Kappe fehlt: Reduzierung plus Kappe oder OFFEN Werkstatt); kein Rohr endet frei.
7. **Luft A neu (M07, M10):** K44-S1..S4 nach Befund 5; Pool-Verteiler, Scheiben, Schwimmerventil bleiben stehen.
8. **M09:** die d75-Steiger bei 3780 / 1365 und -1720 / -2635 gegen die Tischbeine von `Tisch_mitte:3/:4` per Interferenz pruefen; echte Kollision: Steiger verschieben (Ausnahme 1 beachten), sonst im Paket als Kasten-Kandidat schliessen.
9. **Halter:** alle oberirdischen Bestandsrohre nach R6/R7; fehlende Halter-Teile als OFFEN (Werkstatt: Halter).
10. Build `sh scripts/build.sh 5 <naechste Runde>` (D82: RAM >= 10 GB pruefen), Pruefungen, Inventur-Skript neu, Bilder (Draufsicht technisch, Detail Absetzer mit Fass, Detail Pool-Rand), `docs/loop-state.md` Abschnitt "M10-UMBAU", Paket `docs/packages/m10-leitungen.md` Abschnitt 14b (vorher/nachher-Zahlen).

## Nicht anfassen
Lagen der Bauteile (Pumpen, Tanks, Feinfilter, Pool, Pool-Stutzen, Puffer, Becken, Teil-A-Bauteile); Hoehen der Ports; `data/leitungsnetz.json`, `data/roadmap.json`, `data/params.json` ausser neuen `schlammfass_*`-Lagen; `designs/components/*.sc` (fehlt etwas: Werkstatt-Notiz); M10-S2V.

## Dateiliste (darf schreiben)
`scripts/check_leitungsordnung.py` (neu), `scripts/trassen_linie.py`, `scripts/trassen_luft.py`, `scripts/leitungen.py`, `scripts/check_leitungen.py` (nur Wasserkoerper-Ausnahme KB), `data/leitungstrassen.json`, `scripts/gen_dome.py` (Graeben, Fass-Gruben, Verteiler-Setzung), `data/params.json` (nur `schlammfass_*`), `designs/dome.sc`, `scripts/dome-script.json`, neue `lt_rohr_d*_L*.sc` (Werkzeug), `docs/loop-state.md`, `docs/packages/m10-leitungen.md`, `renders/`.

## Ergebnis
Bestand geordnet und gehalten, vier Tanks ohne blinde Ablaesse, Verteiler gesetzt, Schlammfaesser verlegt, Pruefskript fuer alle Folgeschritte; Kurzmeldung mit vorher/nachher (schraeg, Ketten, Boegen, Halter, Kanten ohne Rohr).

## Pruefpunkte (fremd messbar)
1. `python -X utf8 scripts/check_leitungsordnung.py`: R1 bis R9 0 Verstoesse (vorher 74 schraege Rohre, 4 Bogenketten, 0 Halter); R10 meldet genau die Kanten, die laut Abdeckungs-Tabelle unten spaeteren Blaettern gehoeren (Soll 34: 36 minus K07, K23).
2. `python -I -X utf8 renders/maengel/inventur.py <Wurzel> <aus.json>`: `frei_ins_leere` = 0; `tank_anschluesse` Schlamm/Ablauf aller vier Tanks <= 25 mm zum naechsten Leitungsteil (vorher 290 bis 379 mm).
3. `python -X utf8 scripts/r45_heber.py`: Reserve ungünstig K01 >= 85 mm und K17 >= 88 mm; Heber-Laenge je Linie <= 3076 / 2216 mm (Stand S2R).
4. `python -X utf8 scripts/check_leitungen.py` 0 Verstoesse; `python -X utf8 scripts/check_walkways.py` PASS (A >= 700, B >= 600, Wandluft >= 110).
5. Instanzen (`scripts/dome-script.json`): `schlammfass` = 2, `lt_kugelhahn_feder_d40` = 2, `lt_verteiler_d50` = 2; je Stamm K06-T/K22-T eine Gerade >= 262 mm mit >= 100 mm Luft zu Nachbartrassen (Laenge und Abstand im Paket mit Befehl).

## Abdeckung M01 (wer baut welche Kante; Ziel nach S7: 0 Netz-Kanten ohne Rohr)
| Blatt | Kanten |
|---|---|
| M10-UMBAU | Bestand K01 bis K06, K08 bis K10, K17 bis K22, K24 bis K26, K44, K56, K57 (neu verlegt); neu K07, K23 |
| M10-S5-LUFT-B | K39, K40, K41, K45, K46, K47, K48, K49, K51, K52 (K44-Zuleitung vom Hauptverteiler) |
| M10-S3 | K11, K12, K13, K27, K28, K29, K35 |
| M10-S4 | K14, K15, K16, K30, K31, K32, K33, K34, K58, K59 |
| M10-S5 | K37, K38, K42, K43, K53, K54, K55 |
Summe 21 + 2 + 10 + 7 + 10 + 7 = 57 = alle Netz-Kanten (`len(kanten)` in `data/leitungsnetz.json`). Einzige erlaubte Luecke am Ende: K42/K43, falls das Bauteil Biofilter Drittbecken (Werkstatt, Folgeauftrag Abschnitt B) fehlt, dann als OFFEN mit Owner.

## Start-Hinweis fuer die Montage-Sitzung
1. Schwerer Lauf: vor dem Build freier Arbeitsspeicher >= 10 GB (`Get-CimInstance Win32_OperatingSystem`), sonst warten (D82); nur eine Modell-Sitzung zugleich.
2. Zuerst Pruefskript und Router (Schritte 1 und 2) committen; dann Linie 1, Bild ansehen, erst dann Linie 2.
3. Falle S2R: jedes zusaetzliche Formstueck im Heber kostet Reserve; Heber nur kuerzer oder gleich.
4. Falle Kopie-Lauf: `scripts/dome-script.json` ist gitignored, aus dem Arbeitsbaum kopieren (a4d9043).
5. Limit: bei Kontext > 35 Prozent nach Linie 1 Stand schreiben und stoppen; Meldung hoechstens sechs Zeilen.
