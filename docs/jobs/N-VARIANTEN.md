# N-VARIANTEN: Kreislauf A+ und Ring B2 als umschaltbare Projekt-Varianten (W70)

Planer 05.11.2026 (Start-Auftrag `docs/jobs/start/N-VARIANTEN-planer.md`, Commit 5a97c1e). Paket: `docs/packages/n-varianten.md`. [Q] Quelle im Repo · [E] eigene Rechnung/Messung · [A] Annahme dieses Blatts.

**Problem:** Ben hat E20 (Wasserkreislauf) nicht entschieden. Das Projekt kennt heute nur einen Kreislauf; ein zweiter waere nur als Viewer-Spielerei denkbar, nicht in Einkaufsliste, Kennzahlen und Pruefungen.
**Intent:** Ben soll beim Zwischencheck beide Wege vollstaendig vergleichen koennen: A+ (Empfehlung R47b, Annahme D81) und die beste Wasserautobahn B2 (R47c 7.5: Rangfolge A+ > B2 > B1 > B3), und mit EINEM Schalter jedes Projekt-Ergebnis in der einen oder anderen Fassung sehen.
**Ziel (ein Satz):** Ein Parameter `kreislauf_variante` (`a_plus` | `ring_b2`) erzeugt je Variante ein eigenes Modell, eine eigene Einkaufsliste, eigene Kennzahlen, einen eigenen Viewer-Export und eigene Pruefergebnisse; A+ bleibt dabei byte-gleich zum heutigen Weg.

## Aktualitaetspruefung (W44), 05.11.2026
Ergebnis: **gueltig, angepasst**.
1. Roadmap-Eintrag `N-VARIANTEN` (status laeuft, phase vor_zwischencheck, reihenfolge 9.5) deckt sich mit dem Start-Auftrag.
2. D81: E20 = A+ als Annahme bis zum Zwischencheck. Dieses Blatt aendert daran nichts: A+ bleibt Standard (`params.json` Wert `a_plus`), B2 ist zusaetzlich.
3. Die A+-Blaetter M10-S2N bis S7 (Planer `planer-m10-aplus`) stehen beim Schreiben NOCH NICHT im Repo (`ls docs/jobs | grep S2N` leer, `git log HEAD..origin/main` leer). Dieses Blatt doppelt sie nicht; es legt nur fest, welche A+-Teile variantenabhaengig markiert werden (Abschnitt 3). Wer V1b oder R1 startet, liest die dann vorhandenen M10-S2N..S7-Blaetter zuerst.
4. Angepasst gegen den Start-Auftrag: (a) Booster = vorhandenes Bauteil `pumpe_gross` statt neues Bauteil [A, Begruendung 2.2]; (b) Pegelregelung = Pegelschacht mit Schwimmer statt Schwimmer im Biofilter [A, 2.3]; (c) B4 (Ring auf Tischhoehe) wird keine dritte Variante (2.5); (d) Ring als zwei Halbringe d75 statt d90 (R47 Abschnitt 1, Tabelle "Ein Ring gegen zwei Halbringe": je Halbring 110 l/min, d75 reicht).

## 1. Architektur (festgelegt)

### 1.1 Schalter
- `data/params.json` bekommt `kreislauf_variante` = `{"value": "a_plus", "unit": "-", "origin": "A", "source": "D81 / W70", "werte": ["a_plus", "ring_b2"], "used_by": "scripts/variante.py"}`. Der Wert in der Datei ist nur der Standard.
- **Gebaut und exportiert wird nie durch Aendern von `params.json`** (mehrere Sitzungen lesen die Datei). Jede Stufe nimmt die Variante als Schalter `--variante <v>` oder Umgebungsvariable `KREISLAUF_VARIANTE`; fehlt beides, gilt der Wert aus `params.json`.
- Neues Modul `scripts/variante.py` ist die EINE Stelle fuer: `aktiv()` (Schalter > Umgebung > params), `gilt(eintrag, v)` (Eintrag ohne Feld `varianten` gilt fuer alle; sonst nur, wenn `v` in der Liste steht), `pfad(art, v)` (Ausgabepfade nach 1.3). Kein Skript baut Pfade selbst zusammen.

### 1.2 Datenmodell: gemeinsamer Bestand plus Varianten-Feld
- **Ein** Netz und **eine** Trassenliste, kein Kopieren. Neues optionales Feld `varianten: ["a_plus"]` oder `["ring_b2"]` an Kanten (`data/leitungsnetz.json`), Knoten, Trassen, `t_stuecke` und `r_stuecke` (`data/leitungstrassen.json`). Ohne Feld = beide Varianten (heute alle 40 Trassen und 57 Kanten, [E] `len(n['kanten'])`).
- Begruendung: 40 gemeinsame Trassen (Pool bis Biofilter, Absetzerkreis, Bypass, Luft) und der ganze Ruecklauf sind in beiden Varianten gleich [Q R47c 7.2: K01 bis K06/K22, K08/K09 bleiben]. Getrennte Dateien wuerden sie doppeln und auseinanderlaufen lassen.
- Bauteil-Setzungen in `scripts/gen_dome.py`: eine Funktion je Variante fuer das, was nur dort steht (`verteiler_a_plus()` fuer Verteiler d50 je Linie; `ring_b2()` fuer Pegelschacht, Booster, Steigleitung, Ringstuetzen, Entluefter). Die Setzung fragt `variante.aktiv()`; alle anderen Setzungen bleiben unveraendert.
- Graeben in `erde_fn` kommen aus den Trassen, also automatisch nur aus den Trassen der aktiven Variante (in B2 entfallen die Graeben der Beet-Zuleitung K11/K27).
- `scripts/trassen_linie.py` schreibt nur die Trassen seiner Linie und laesst fremde stehen (heute schon so); neu: er laesst zusaetzlich alle Eintraege mit `varianten: ["ring_b2"]` stehen. Die Ring-Trassen leitet ein eigenes Skript `scripts/trassen_ring.py <linie>` ab (gleiches Prinzip: Koordinaten aus Instanzmatrizen und Port-Tabellen, nie von Hand).

### 1.3 Ausgaben je Variante
A+ behaelt alle heutigen Pfade (nichts bricht, Viewer, Roadmap und Einkaufsliste-Verknuepfung bleiben gueltig). B2 bekommt eigene Pfade:

| Ausgabe | A+ (wie heute) | Ring B2 |
|---|---|---|
| Bau-Skript | `scripts/dome-script.json` | `scripts/dome-script-ring_b2.json` |
| Modell | `designs/dome.sc` | `designs/dome-ring_b2.sc` |
| Bilder | `renders/round-NN.png`, `section-NN.png` | `renders/ring_b2/round-NN.png`, `section-NN.png` |
| Viewer-Export | `viewer/instances.json`, `extras.json`, `ansicht.json` | `viewer/varianten/ring_b2/instances.json`, `extras.json`, `ansicht.json` |
| Geometrie Viewer | `viewer/defs/`, `viewer/detail/` | **gemeinsam** (gleiche Definition = gleiche Datei; neue Ring-Teile kommen dazu) |
| Stueckliste | `data/stueckliste.json`, `docs/stueckliste.md` | `data/stueckliste-ring_b2.json`, `docs/stueckliste-ring_b2.md` |
| Einkaufsliste | `docs/einkaufsliste.html` | `docs/einkaufsliste-ring_b2.html` |
| Vergleich | – | `docs/varianten-vergleich.md` (Mehr/Weniger B2 gegen A+: Artikel, Kosten, Kennzahlen) |
| Kennzahlen | `data/system-specs.json` | `data/system-specs-ring_b2.json` |
| Pruefergebnisse | wie heute | Ausgabe des Pruefskripts mit Variantenname in der Kopfzeile; Karten `renders/ring_b2/walkway-map-*.png` |

`build.sh` bekommt die Variante als drittes Argument: `sh scripts/build.sh <stufe> <runde> [variante]` (Standard `a_plus`).

### 1.4 Viewer-Schalter
- Auswahl "Kreislauf: A+ | Ring B2" in der Kopfleiste von `viewer/index.html`, gespiegelt in der Adresse (`?variante=ring_b2`), Wahl im `localStorage` gemerkt.
- Beim Wechsel laedt `load()` `instances.json`/`extras.json`/`ansicht.json` aus dem Varianten-Ordner neu; Definitionen kommen aus dem gemeinsamen `defs/` und dem Browser-Zwischenspeicher, also kein Neuladen der 282 MB [Q `docs/packages/n-viewer-laden.md`: 164 Definitionen, 282,1 MB].
- Kennzahlen: `serve.py` liefert `/system-specs.json?variante=ring_b2` aus `data/system-specs-ring_b2.json` (heute fest auf `data/system-specs.json`, `viewer/serve.py:95`). Gleiches fuer Einkaufsliste-Verknuepfung, falls der Viewer sie verlinkt.
- `serve.py` beobachtet beide Modelle (`designs/dome.sc`, `designs/dome-ring_b2.sc`) und exportiert die geaenderte Variante; `export_model.py --variante <v>` und `export_ansicht.py --variante <v>` schreiben in die Pfade aus 1.3.
- Sichtbares Etikett im Viewer, welche Variante gerade gezeigt wird (keine Verwechslung bei Screenshots).

### 1.5 Pruefskripte je Variante
Alle nehmen `--variante <v>` und filtern ueber `variante.gilt`: `check_leitungen.py`, `check_netz.py` (Bilanz je Linie mit den Kanten der Variante), `check_walkways.py` und `check_walkways_voll.py` (lesen das Bau-Skript der Variante), `check_latte.py` (Pfad des Modells der Variante), `check_bom.py`, `model_inventar.py`. Neu: `scripts/check_varianten.py` prueft das Zusammenspiel (Pruefpunkte P1 bis P3).

### 1.6 Kosten (geschaetzt, Zahlen mit Herkunft)
| Posten | je zusaetzlicher Variante | Herkunft |
|---|---|---|
| Bau (gen_dome + CLI run) | etwa 3 min (185 s) | [E] Dateizeiten `scripts/dome-script.json` 10:30:48 -> `designs/dome.sc` 10:33:53 (`ls -la --time-style=+%H:%M:%S`); `docs/loop-state.md:7` nennt 132 s fuer Stufe 5 |
| Modell `dome-ring_b2.sc` | etwa 16 MB | [E] `du -sh designs/dome.sc` = 16M |
| Bau-Skript | etwa 1,5 MB | [E] `du -sh scripts/dome-script.json` |
| Viewer-Export | etwa 0,6 MB (`instances.json` 552K) plus nur die neuen Ring-Definitionen; `defs/` (485 MB) und `detail/` (667 MB) NICHT doppelt | [E] `du -sh viewer/defs viewer/instances.json viewer/detail` |
| check_walkways_voll | etwa 7,5 min | [Q] `docs/loop-state.md:32` |
| check_latte | bis etwa 35 min beim ersten Lauf | [Q] `docs/loop-state.md:17` |
Folge: Jede Montage, die beide Varianten nachzieht, kostet etwa 3 min Bau plus Pruefzeit doppelt. Deshalb baut die A+-Kette (M10-S2N..S7) nur A+; B2 wird erst ab Schritt R1 und dann bei jedem Meilenstein mitgebaut (Abschnitt 4).

## 2. Ring B2 fachlich (Grundlage R47c 7.2, 7.3, 7.5; R47 Abschnitt 1)

### 2.1 Wasserweg je Linie
Pool -> Heber K01/K17 -> Feinfilter -> Hauptpumpen (H 2,0 m wie heute) -> Biofilter (Ueberlauf Z 1570 rel, gebaut) -> K10/K26 (gebaut, endet heute offen am Verteilerplatz) -> **Pegelschacht** -> **2 Booster** (je 55 l/min, H etwa 1,0 m) -> **Steigleitung d63** (110 l/min, v 0,9 m/s [E R47c 7.3 Punkt 5]) in der Technikgruppe -> **Druck-Halbring d75** (Unterkante Z 2100, Achse 2145, Hochpunkt etwa 2190 mit Entluefter, r 3,4 m) -> **Abzweige** je Beet und je Tisch (T, Reduzierung, Kugelhahn als Regler, Fallleitung) -> Abnehmer -> Ruecklauf wie A+ -> Pool. Z relativ zum Innenboden; absolut = relativ + 400.

### 2.2 Booster = Bauteil `pumpe_gross` [A]
Zwei Booster je Linie parallel, gleiche Klasse wie die Hauptpumpen (D38: 4 x 55 l/min). Gruende: gleiches Redundanzmuster (eine Pumpe faellt aus, halber Ringstrom bleibt), Bauteil mit Port-Tabelle existiert (`scripts/trassen_linie.py` PORTS `pumpe_gross`), Ersatzteil gleich. Foerderhoehe 1,0 m liegt unter der heutigen 2,0 m, also in der Klasse. Fabrikat bleibt offen wie bei den Hauptpumpen (R47c Offen 1). Standort: Pumpenplattform der Technikgruppe je Linie (Z 570 rel), sonst eigener Stand; nie an Tank- oder Pumpentafeln befestigt (Regel 7).

### 2.3 Pegelregelung = Pegelschacht [A]
R47c 7.2 nennt zwei Wege: Sammelschacht oder Schwimmerregelung. Gewaehlt: kleiner Sammelbehaelter (Standardfass etwa 60 l, Werkstatt waehlt Mass aus der Bibliothek oder als Handelsteil) unter dem Biofilter-Ueberlauf. K10 muendet oben ein; die Booster saugen unten (geflutet); Schwimmerschalter schaltet die Booster bei Tiefstand ab; ein Notueberlauf d50 fuehrt bei Booster-Stillstand in den Ruecklauf (Wasser hat den Biofilter durchlaufen, EINHEIT (c) bleibt, R47c 7.2). Grund gegen Schwimmer im Biofilter: Eine Pumpe direkt am Wehr saugt Luft, sobald sie mehr zieht als zulaeuft; der Schacht entkoppelt das.

### 2.4 Ring und Stuetzen
- Zwei Halbringe d75 (Linie Ost, Linie West), je etwa 10,7 m [Q R47 Abschnitt 1]. Kein gemeinsamer Ring: Leckage naehme sonst beide Linien.
- Stuetzabstand hoechstens 1,65 m (d75, kleinerer Wert aus zwei Quellen, 20 Grad) [Q R47 Abschnitt 1, Georg Fischer und plasticpipeshop]; im warmen Dach weniger (GF d63 1,3 m bei 60 Grad). Daraus mindestens 7 Stuetzen je Halbring [E: 10,7 / 1,65 = 6,5 -> 7]. R47 nannte 12 Stuetzen fuer d90 bei 1,8 m; fuer d75 gilt die neue Zahl.
- Stuetzen eigene Bodenstuetzen; Auflage OBEN auf Konsole oder Haengebuegel, nichts unter dem Rohr (Gang ab Z 2100 frei, R47 Abschnitt 1). Rohre nicht an Streben (M10-Blatt Aktualitaet 1 Punkt 5, N-STATIK offen).
- Je Halbring: Entluefter am Hochpunkt, Entleerungs-Kugelhahn am Tiefpunkt in den Ruecklauf (Frost, R47 Abschnitt 1), Ring-Ende mit Kugelhahn als Ueberschuss in den Ruecklauf (Ersatz fuer K13/K29).
- Abnehmer: 38 (14 Beete, 24 Tische) [Q R47 Gesamturteil 4]; Fallleitung Beet bis Z 650 etwa 1,5 m, Tisch bis Z 1090 etwa 1,05 m [Q R47 Abschnitt 1].

### 2.5 B4 geprueft, keine eigene Variante
B4 (Ring auf Tischhoehe, Schwerkraft) erreicht die Beete nicht ohne Gangquerung; R47c 7.2 nennt sie "technisch A mit laengerem K12". Sie bringt also gegen A+ nichts Sichtbares. Ergebnis: nicht als Variante gebaut, im Vergleich `docs/varianten-vergleich.md` mit einem Satz erwaehnt.

### 2.6 Netz-Delta (Vorschlag an den Orchestrator, er besitzt `data/leitungsnetz.json`)
| Netz | Linie 1 / Linie 2 | Variante | Inhalt |
|---|---|---|---|
| Knoten | `verteiler_1/2` | a_plus | Feld `varianten` setzen |
| Kanten | K10..K13 / K26..K29 | a_plus | K10/K26 = Biofilter -> Verteiler; Ziel bleibt nur in A+ |
| Knoten neu | `pegelschacht_1/2`, `booster_1a/1b`, `booster_2a/2b`, `ring_1/2` | ring_b2 | Typen Behaelter, Pumpe, Leitung |
| Kanten neu | K60 / K68 | ring_b2 | Biofilter -> Pegelschacht, d50 (gleiche Trasse wie K10 bis zum Schacht), 110 l/min |
| | K61, K62 / K69, K70 | ring_b2 | Pegelschacht -> Booster a/b, Saug d50, je 55 l/min |
| | K63 / K71 | ring_b2 | Booster -> Ring (Steigleitung d63), 110 l/min |
| | K64 / K72 | ring_b2 | Ring -> Beete der Linie (Abzweige d40) |
| | K65 / K73 | ring_b2 | Ring -> NFT der Linie (Abzweige d32) |
| | K66 / K74 | ring_b2 | Ring-Ende -> Ruecklauf (Ueberschuss, Kugelhahn), d50 |
| | K67 / K75 | ring_b2 | Pegelschacht -> Ruecklauf (Notueberlauf), d50, Soll 0 im Normalbetrieb |
| Kabel neu | Schaltschrank -> Booster x4, Schwimmer x2 | ring_b2 | Leistung nach 3.1 |
Kanten-IDs ab K60, weil die hoechste heute K59 ist [E `python -X utf8 -c "...sorted(k['id'] for k in n['kanten'])[-1]"` = K59]. Durchmesser sind Vorschlag [A]; die Werkstatt bestaetigt sie gegen die Pumpen-Ports.

### 2.7 Was in beiden Varianten gleich bleibt
Pool, Heber, Feinfilter, Hauptpumpen, Biofilter, K01..K09/K17..K25, Absetzerkreis, Notbypass K56/K57, alle A+-Massnahmen M1..M7 an diesen Strecken (Revisionsstutzen, Schaechte, Absperrhaehne, Alarm: sie betreffen die 30,3 m vergrabenes Rohr VOR dem Verteiler, R47b 6.0 Punkt 2), Ruecklauf K14..K16/K30..K32, Beet-Sumpf K58/K59, Luft, Messstellen, Frischwasser.

## 3. Pflicht fuer die A+-Kette (M10-S2N bis S7), damit sie nicht doppelt gebaut wird
1. Ab dem ersten Montage-Schritt NACH V1b tragen alle Trassen, T- und R-Stuecke, die nur zu A+ gehoeren, `varianten: ["a_plus"]`: Verteiler-Anschluss am K10/K26-Ende, K11/K27 (Beet-Zuleitung samt Graeben), K12/K28 (NFT-Zuleitung), K13/K29 (Ueberschuss). Die Setzung des Verteilers d50 laeuft in `verteiler_a_plus()`.
2. Was beide Varianten nutzen (Ruecklauf, Revisionsteile, Kabel zu gemeinsamen Teilen), bleibt ohne Feld.
3. Montage-Schritte VOR V1b bauen wie heute; V1b markiert deren A+-Eintraege nachtraeglich (Liste im Ergebnis von V1b).
4. Die A+-Kette baut nur A+; sie muss B2 nicht mitbauen.

## 4. Schritte je Rolle (Reihenfolge)
Modell-Kette laut `docs/packages/bis-zwischencheck.md` Plan 1: ... -> M10-S2N -> S3 -> S4 -> S5 Rest -> S6 -> S7 -> CHECK. Nur EINE Sitzung baut das Gesamtmodell (D80). Einordnung:

| ID | Rolle | wann | Dateien (nur diese) | Inhalt |
|---|---|---|---|---|
| **V1a** | Werkstatt Skripte/Daten (Sonnet hoch) | **sofort, parallel** zur Kette (keine Ueberschneidung) | neu `scripts/variante.py`, `scripts/check_varianten.py`; `data/params.json` (nur der eine Eintrag); `scripts/bom.py`, `scripts/bom_seite.py`, `scripts/check_bom.py`, `scripts/system_specs.py`, `scripts/check_netz.py`, `viewer/export_model.py`, `viewer/export_ansicht.py` | Modul und Schalter (1.1); Pfade (1.3) in den Ausgabe-Skripten; `system_specs.py` bekommt Block `kreislauf` (3.1); `scripts/bom_vergleich.py` -> `docs/varianten-vergleich.md`. Beweis: ohne Schalter erzeugen alle Skripte dieselben Dateien wie vorher (P1). Kein Bau, kein `designs/dome.sc`. |
| **V1b** | Werkstatt Skripte (Opus mittel) | **im Slot der Modell-Kette**, zwischen zwei Montage-Schritten (Empfehlung: direkt nach dem gerade laufenden Schritt, vor dem naechsten M10-S-Schritt) | `scripts/gen_dome.py` (nur Varianten-Weiche und Ausgabepfad), `scripts/build.sh`, `scripts/leitungen.py`, `scripts/trassen_linie.py`, `scripts/check_leitungen.py`, `scripts/check_walkways.py`, `scripts/check_walkways_voll.py`, `scripts/check_latte.py`, `data/leitungstrassen.json` (nur Feld `varianten` an A+-Eintraegen) | Filter `variante.gilt` in Leitungsbau, Graeben und Pruefungen; `build.sh` 3. Argument; `gen_dome.py` mit `--variante`; Funktion `verteiler_a_plus()` (zunaechst leer oder mit dem schon Gesetzten). Beweis P1 (A+ byte-gleich) und ein B2-Bau, der sich nur durch fehlende A+-Teile unterscheidet. |
| **V2** | Werkstatt Bauteile (Opus mittel) | parallel ab sofort | `designs/components/`, `scripts/workshop/`, `docs/parts/`, `data/components/` | Pegelschacht mit Schwimmer und Notueberlauf (Ports-Tabelle), Ringstuetze mit Auflagekonsole d75 (Hoehe parametrisch, Fussplatte), Entluefter d75, Ring-Abzweig (T d75 auf d40/d32 + Kugelhahn, aus Bibliothek zusammengesetzt, kein neues Teil wenn moeglich). Booster = `pumpe_gross` (kein neues Teil). Bauteilblaetter mit Port-Tabelle, Check, Bild. |
| **O1** | Orchestrator | vor R1 | `data/leitungsnetz.json` | Netz-Delta nach 2.6 eintragen, `check_netz.py --variante ring_b2` gruen. |
| **R1** | Montage Ring B2, Linie 1 (Opus mittel) | **nach M10-S7** der A+-Kette, vor CHECK | `scripts/gen_dome.py` (`ring_b2()`), neu `scripts/trassen_ring.py`, `data/leitungstrassen.json` (nur Eintraege `ring_b2`), `designs/dome-ring_b2.sc`, `renders/ring_b2/` | Pegelschacht, 2 Booster, Steigleitung, Halbring Ost mit Stuetzen, Abzweige zu 7 Beeten und 12 Tischen, Ueberschuss/Entleerung/Notueberlauf; `sh scripts/build.sh 5 <runde> ring_b2`; check_leitungen, check_walkways_voll, Interferenz Ring gegen Streben. |
| **R2** | Montage Ring B2, Linie 2 | nach R1 | wie R1 | `trassen_ring.py 2`, Halbring West, Rest wie R1. |
| **VV** | Viewer-Sitzung (Sonnet hoch) | nach V1a, parallel zur Kette | `viewer/index.html`, `viewer/serve.py` | Schalter nach 1.4; Probe mit einem B2-Export (sobald V1b gelaufen ist, reicht ein B2-Bau ohne Ring); Screenshot beider Varianten im Browser. |
| **PV1** | Pruefer (Sonnet hoch) | nach V1a + V1b + VV | `docs/jobs/pruefung/N-VARIANTEN-1.md` | P1, P2, P5. |
| **PV2** | Pruefer | nach R2 | `docs/jobs/pruefung/N-VARIANTEN-2.md` | P3, P4, P5 mit Ring. |
| CHECK | Montage/Pruefer der Kette | danach | – | laeuft fuer BEIDE Varianten (`check_latte.py` je Variante, Zeitbedarf 1.6). |

Geschaetzt: 7 Bau-/Pruefsitzungen (V1a, V1b, V2, VV, R1, R2 + 2 Pruefer, wobei V1b kurz ist) plus O1.

### 3.1 Kennzahlen je Variante (`system_specs.py`, Block `kreislauf`)
| Kennzahl | A+ | Ring B2 | Herkunft |
|---|---|---|---|
| Pumpstufen Linienwasser | 1 | 2 | [Q R47c 7.5] |
| Pumpenleistung elektrisch, eta 25 % (eta 18 %) | 430 W | 577 W (635 W) | [Q R47c 7.5, `scripts/r47_pumpen.py`] |
| Foerderhoehe Hauptpumpe / Booster | 2,0 m / – | 2,0 m / etwa 1,0 m | [Q R47c 7.2] |
| Meter Rohr ueber Kopf (Leiter) | 0 | Ring 2 x 10,7 m + Abzweige | [Q R47b 6.6]; im Skript aus den Trassen der Variante gemessen |
| Rohrlaenge Zulauf-Verteilung | aus Trassen | aus Trassen | [E] Summe der Trassen der Variante (nicht mehr R47-Schaetzung 80/109 m) |
| Wasser in Rohren | aus Trassen | aus Trassen | [E] statt fester 225 l (`PIPE_WATER_L` [A]) |
| Graeben Zulauf zu Beeten | ja | nein | [Q R47 Gesamturteil 5] |
Feste Werte bleiben mit Herkunft im Skript; gemessene kommen aus den gefilterten Trassen.

## 5. Pruefpunkte (fremd nachmessbar)
- **P1 A+ unveraendert:** vor V1a/V1b SHA-256 von `scripts/dome-script.json` (aus `python -X utf8 scripts/gen_dome.py 5 <scratch>/a.json`), `data/stueckliste.json`, `data/system-specs.json`, `viewer/instances.json` notieren; danach dieselben Befehle ohne Schalter: **alle Hashes gleich**, ausser `system-specs.json`, das nur um den Block `kreislauf` waechst (Rest gleich, `python -X utf8 scripts/check_varianten.py --a-plus-gleich`).
- **P2 Schalter wirkt ueberall:** `python -X utf8 scripts/check_varianten.py` meldet fuer `ring_b2`: alle 8 Ausgaben aus Tabelle 1.3 existieren und sind juenger als das Modell; keine Datei von A+ wurde durch einen B2-Lauf veraendert (Zeitstempel vor/nach); Zahl der Instanzen in `08_Leitungen` unterscheidet sich zwischen den Varianten; Assembly-Liste sonst gleich.
- **P3 Ring B2 vollstaendig:** `check_netz.py --variante ring_b2`: Bilanz je Linie 0 Abweichung; `check_leitungen.py --variante ring_b2`: 0 Verstoesse oder jeder benannt; je Linie 7 Beet- und 12 Tisch-Abzweige (`check_varianten.py --abzweige`), Stuetzabstand <= 1,65 m, Ring-Unterkante >= Z 2100 rel und nichts darunter.
- **P4 Gaenge und Kollision B2:** `check_walkways_voll.py --variante ring_b2`: keine NEUE rote Engstelle gegen A+ (Liste der Engstellen beider Laeufe verglichen); Interferenz Ring/Stuetzen gegen Streben, Tische, Tanks = 0.
- **P5 Sichtbar im ganzen Projekt:** Einkaufsliste B2 enthaelt Booster (4), Pegelschacht (2), Ringrohr d75, Stuetzen; A+ enthaelt keinen davon; `docs/varianten-vergleich.md` listet Mehr/Weniger; Viewer-Screenshot beider Varianten (echter Browser, `docs/ui-standard.md`) zeigt Etikett und den Ring nur in B2; Kennzahlen-Panel zeigt 430 W gegen 577 W.

## 6. Nicht anfassen
`designs/dome.sc` ausser durch die eine Montage-Sitzung der Kette; `data/leitungsnetz.json` und `data/roadmap.json` (Orchestrator); die Blaetter M10-S2N..S7 (anderer Planer); `data/beschaffung/*.json` (nur lesen); M10-S2V Subtank (geparkt, D81); E20 selbst (Ben entscheidet beim Zwischencheck, B2 ist Anschauung, keine Vorentscheidung).

## 7. OFFEN (Ben) und offene Fachpunkte
1. OFFEN (Ben): E20 bleibt offen; dieses Paket liefert nur die Vergleichsgrundlage.
2. Fabrikat Booster und Hauptpumpe (R47c Offen 1); Kennlinie nur Parabel-Naeherung.
3. Ringstuetzen-Statik und Kragarm (R47 Offen); Werkstatt V2 legt Profil als [A] fest, N-STATIK prueft spaeter.
4. Pegelschacht-Groesse 60 l ist [A]; Werkstatt prueft gegen Nachlauf des Rings bei Booster-Stopp (Ringinhalt d75 2 x 10,7 m etwa 77 l [E: 0,0678^2 x pi/4 x 21,4 m x 1000]).
5. Ob V1b vor oder nach M10-S2N laeuft, entscheidet der Orchestrator nach dem Stand der Kette (Empfehlung oben).

## Start-Hinweis fuer die Bau-Sitzungen
1. Python immer `python -X utf8`; Skripte per Write als Datei, keine Heredocs mit `!` oder Backslashes.
2. V1a/V1b: zuerst die Hashes fuer P1 nehmen, DANN aendern; gen_dome in den Scratchpad schreiben lassen, nie `build.sh` in V1a.
3. Z-Konvention: Netz und R47 relativ zum Innenboden, Trassen und Skripte absolut (+400); Fehlerquelle der Vorgaenger.
4. `viewer/extras.json`, `designs/dome.sc` und erzeugte `lt_rohr_*.sc` fremder Builds nie mitcommitten; nur Pfad-Commits.
5. Limit: vor jedem Start `get_usage`; R1/R2 sind Montage-Laeufe (etwa 600 Nachrichten = 35 %), V1b ist kurz.
