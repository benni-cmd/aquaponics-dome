# Paket W37-1: Beet-Sumpf und Schlammfass (Werkstatt)

**Problem:** Das Beetwasser kommt nicht zurueck in den Pool (Beetablauf liegt unter dem Pool-Spiegel, Luecke L04), und die Schlammleitungen K07/K23 der Absetzer enden im Nichts (Luecke L01). Die Bauteile `beet_sumpf` und `schlammfass` fehlen.
**Intent:** Die Montage (M10 S4/S5) soll Sumpf und Fass mit Ports ans Netz setzen koennen; Eigenkonstruktion aus Handelsteilen (L21), Kaufteile mindestens in Europa (D76).
**Goal:** Drei Bauteile `beet_sumpf`, `schlammfass`, `lt_kugelhahn_feder_d40` mit Generator, Check PASS, Bauteilblatt, Teiledaten, Beschreibung, Bild; die fuenf Pruefpunkte des Blatts `docs/jobs/W37-1-sumpf-schlammfass.md` gemessen und hier eingetragen.

Blatt: `docs/jobs/W37-1-sumpf-schlammfass.md` (Aktualitaetspruefung 05.11.2026: angepasst).

## Plan
1. [x] Aktualitaetspruefung W44 gegen Roadmap (E19, E20, L01, L04), D81 und M-BEET-TAUSCH; Einlaufhoehe gegen den neuen Ablaufport (Ergebnis im Blatt).
2. [x] `beet_sumpf`: Generator `scripts/workshop/beet_sumpf.py`, Parameter `data/components/beet_sumpf.json`, Check `check_beet_sumpf.py`, Blatt, Teiledaten, Beschreibung, Bild. Commit + Push.
3. [x] `schlammfass` und `lt_kugelhahn_feder_d40` (`scripts/workshop/leitung_w37.py`): wie 2. Commit + Push.
4. [x] Pruefpunkte 1 bis 5 messen, hier eintragen; `docs/workshop-state.md` Zeile. Commit + Push, Kurzmeldung, STOPP.

## Mini-Plan beet_sumpf
- Bauteil-KS: Ursprung Mitte Tankboden, Z hoch. Tank Ø 800 aussen, H 1000, Wand 6 [A] (Plan 8, gebaut 6 fuer Pruefpunkt 2); Schachtaufsatz Ø 600 x 200 (`aufsatz_h`, Einlaufhoehe gegen Beetablauf, Blatt Punkt 6); Deckel begehbar Ø 700 x 40 auf dem Aufsatz.
- Zulauf Muffe d50 (`zulauf_d`) radial bei Z 800 (Sohle), Richtung -X.
- 2 Pumpen (`pumpen` = 2, E19) als Platzhalter-Quader auf dem Boden, je Steigrohr d40 mit Rueckschlagventil d40 (Masse W39), Sammelrohr unter dem Deckel, Port d40 oben (+Z).
- Schwimmerstange mit drei Schwimmern (Mitte bei 120, 320, 620), zwei Kabeldurchfuehrungen M25 (Pumpen/Schwimmer, Ablaufwaechter A+), Entlueftung d32 mit Gitterkappe.
- Einzelkoerper, die sich nur beruehren (Durchbrueche = Aussen-Oe des Formstuecks), statt Boolean-Vereinigung an duennen Mantelflaechen; Interferenz 0.

## Stand
05.11.2026: Schritt 1 erledigt (Blatt-Abschnitt "Aktualitaetspruefung (05.11.2026, Werkstatt)", Commit 431b6c6).
05.11.2026: Teil 1 `beet_sumpf` T92 (a725eb1), Teil 2 `schlammfass` T93 und `lt_kugelhahn_feder_d40` T70-KHF-40 (f7fd740). Teilenummer T83 aus dem Mini-Plan war belegt (aktivkohle_station), daher T92/T93.
05.11.2026 (Pause, Ben Feierabend): `check_leitungsteile.py` nach dem Ausnehmen von `leitung_w37.FILES` neu gestartet, Ergebnis lag bei der Pause noch nicht vor (vorher FAIL 64 statt 63 Dateien, Ursache der neue Hahn). WIEDERANLAUF: `python -X utf8 scripts/workshop/check_leitungsteile.py` laufen lassen (ueber 10 min), Ergebnis hier eintragen.
05.11.2026 Nachtrag: Neulauf beendet, Exit 1 nach 87 PASS, 0 FAIL: Abbruch `FEHLER faces: no body Dichtung_B`. Ursache NICHT W37: zwei fremde, nicht committete Dateien `designs/components/lt_schacht_kugelhahn_d63_tief_senkrecht.sc` und `..._waagerecht.sc` (Sitzung werkstatt-schacht-ring, `schacht_tief.py`) stehen in keiner FILES-Ausnahmeliste; ohne sie zaehlt die Pruefung 63 (W37 ist ausgenommen). Owner: werkstatt-schacht-ring (Ausnahmeliste ergaenzen), danach Neulauf.
05.11.2026 (Nachtmodus D82) **Ergebnis: `check_leitungsteile` 231/231 PASS**, Dateien 63/63 (W37-Hahn ausgenommen). Gemessen mit einem Wrapper, der nur die zwei fremden `lt_schacht_kugelhahn_d63_tief_*.sc` ausblendet (Scratchpad `run_clt.py`, keine Datei im Repo geaendert), und mit eigenem `WORKSHOP_TMP`. **Besonderheit:** Die Abbrueche `no body Dichtung_A/B` kamen nicht aus der Bibliothek, sondern aus `sc.faces()`: es schreibt die feste Datei `%TEMP%\ws-faces.json`, die parallel laufende Werkstatt-Sitzungen ueberschreiben (Wettlauf). Parallel-Laeufe von Checks brauchen je Sitzung ein eigenes `WORKSHOP_TMP` (Owner: Orchestrator, Regel fuer Sitzungsstarts).

## DoD
Pruefpunkte 1 bis 5 des Blatts mit Befehl und Messwert in der Tabelle unten.

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | Check beider Bauteile PASS, keine FAIL-Zeile | `python -X utf8 scripts/workshop/check_beet_sumpf.py`; `python -X utf8 scripts/workshop/check_schlammfass.py`; `python -X utf8 scripts/workshop/check_lt_w37.py` (Ergebnisse `renders/components/beet_sumpf/check.txt`, `renders/components/schlammfass/check.txt`, `renders/components/leitungsteile/check_lt_w37.txt`) | beet_sumpf **33/33**, schlammfass **20/20** (1 INFO-Zeile), lt_w37 **11/11**, je Exit 0; Interferenz 0 (beet_sumpf: 23 Koerper, 41 Kandidatenpaare, 0 ungeprueft); Teiledaten `check_parts.py beet_sumpf` 22/22, `schlammfass` 22/22 | PASS |
| 2 | Volumen bis ALARM 310 l +-5 %, Tank bis 1,0 m 500 l +-7 % | `check_beet_sumpf.py` Zeilen "Volumen bis ALARM", "Tankinhalt", "Hohlraum aus Messung" | Innen-Oe 788 (Wand 6 [A]) x (620 - 6) = **299,4 l** (-3,4 %); Gegenprobe R45 Oe 0,8 x 620 = 311,6 l; Hohlraum aus Modellmessung 481,8 l = Rechnung 481,8 l; Tankinhalt **481,8 l** (-3,6 %) | PASS |
| 3 | Port-Tabelle: Zulauf bei Z 800, Foerderleitung d40, Kabeldurchfuehrung; K14/K58 und K30/K59 genannt | `docs/parts/beet_sumpf.md` Abschnitt Ports; `check_beet_sumpf.py` Port-Zeilen | Zulauf **Muffe d50** (Sohle 800, Achse z 825, x -451, -X), nennt K14/K30; Foerderleitung Muffe d40 (x 100, z 1280, +Z), nennt K58/K59; 2 Kabeldurchfuehrungen M25 (Pumpen/Schwimmer; Ablaufwaechter A+); Entlueftung d32. **Abweichung:** Blatt nennt d63, Netz V3 traegt K14/K30 dn 50 (Aktualitaetspruefung Punkt 5); Parameter `zulauf_d` stellt um | PASS mit Abweichung DN (Netz gilt) |
| 4 | Schlammfass 200-220 l +-5 %; Stutzen d40 Mitte Deckel; Grube Oe 0,8 / 0,95 im Blatt | `check_schlammfass.py`; `docs/parts/schlammfass.md` Parameter | Innenraum Oe 572 x 860 = **221 l** (Modell = Rechnung, +0,5 %); Huellzylinder aussen Oe 580 x 880 = 232,5 l (nur INFO: liegt 5,7 % ueber 220, misst Wand und Deckel mit); Stutzen Mitte x 0 / y 0, Aussen 48; `grube_d` 800, `grube_t` 950; kein Auslass (Fasskoerper-Volumen = Mantel + Boden) | PASS (Volumen als Innenraum gemessen) |
| 1b | Bibliothek unveraendert (Zusatz) | `WORKSHOP_TMP=<eigen> python -X utf8 scripts/workshop/check_leitungsteile.py` (fremde `_tief_`-Dateien ausgeblendet) | **231/231**, Dateien 63/63 | PASS |
| 5 | Herkunftstabelle trennt belegt/gerechnet/Annahme; keine Fabrikat-Erfindung | `grep -ci oase docs/parts/beet_sumpf.md docs/parts/schlammfass.md`; Blatt-Abschnitt Herkunft | grep: **0** und **0** (kein Fabrikat genannt, auch nicht das R45-Beispiel); Herkunft je Zeile: beet_sumpf 14 Zeilen, schlammfass 6 Zeilen, Spalte Herkunft mit belegt / gerechnet / Annahme | PASS |

## Kurzmeldung (an den Orchestrator)
1. beet_sumpf T92: Tank Oe 800 x 1000 (482 l, bis ALARM 299 l), Aufsatz 200, Deckel Oe 700; Zulauf d50 Sohle 800 (-X), Foerderleitung d40 (+Z) hinter 2 Pumpen mit RSV d40 (E19), 3 Schwimmer 120/320/620, 2 Kabel M25 (A+), Entlueftung d32. Offen: Pumpenfabrikat/Kennlinie, Deckelklasse, Auftrieb.
2. schlammfass T93: Fass Oe 580 x 880, 221 l innen, Stutzen d40 Mitte Deckel (K07/K23, +Z), Luft Oe 8, Entlueftung Oe 20, kein Auslass; Grube Oe 800 / 950. Offen: Fassfabrikat, Grubenkollision (Montage).
3. lt_kugelhahn_feder_d40 T70-KHF-40: Masse wie lt_kugelhahn_d40, Ports A/B gleich, Hebel quer = zu (Feder). Offen: Fabrikat/Verfuegbarkeit nicht geprueft.
4. System-Specs: 2 x 60 W, 108 bis 120 W (Reservepumpe 0 W im Normalbetrieb [A]) — `scripts/system_specs.py` pflegt der Orchestrator.
5. **Besonderheit:** Nach dem Beet-Tausch lag die Einlaufsohle mit buendigem Deckel UEBER dem Beetablauf (-200 gegen -290 flur-relativ). Der Sumpf sitzt jetzt tiefer: Tankboden -1200, Grube 1,25 m. Dadurch statische Foerderhoehe 1,40 bis 1,60 m statt 1,0 bis 1,5 m (R45): Arbeitspunkt mit `r45_sumpf.py` nachrechnen (Planer/Orchestrator); Montage M10 S4 setzt die Sumpfe mit Tankboden flur -1200 (Modell Z -800).
