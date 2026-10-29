# Werkstatt-Log (Rolle W, Komponenten-Werkstatt Innenraum)

Beginn 29.10.2026 ~03:50. Befunde zu SolidCraft v0.25.1 (Headless, `solidcraft-cli run`) und Entscheidungen. Annahmen sind mit [A] markiert.

## Befunde zu den Komponentenbefehlen
- `component.create` (name, grounded), `parameters.add` (name, expression "50 mm"), `component.metadata.set` (part_number, description, revision, properties), `material.create`/`material.assign` (PP etc. fehlen in den Standardmaterialien, daher `material.create`), `appearance.assign` laufen im Headless-Lauf. Ausdruecke wie `"pot_d/2"` und Parameternamen werden in Primitiven (`solid.cylinder`, `solid.box`) akzeptiert.
- Skizze auf Ebene `XZ`: sketch-y bildet auf **-Z** ab (Koerper liegt bei Z < 0). Abhilfe: explizite Ebene `{"origin":[0,0,0],"x_dir":[1,0,0],"y_dir":[0,0,1]}`; dann ist sketch-y = Welt-Z. Revolve-Achse in Skizzenkoordinaten: `"y"` (klein), nicht `"Y"` (Welt).
- Werkzeug-Pfad: Python 3.12 liegt unter `C:\Users\benkn\AppData\Local\Programs\Python\Python312\python` (`python` im PATH ist der Store-Stub); Ausgabe mit `PYTHONIOENCODING=utf-8`.
- Arbeitsweise (Entscheidung W-1): Der Generator `scripts/workshop/<klasse>.py` liest `data/components/<klasse>.json` und schreibt ein Befehlsskript; `solidcraft-cli run --save` erzeugt die `.sc`. Die Parameter stehen zusaetzlich als `parameters.add` in der `.sc` (Primitive nutzen sie per Ausdruck; Skizzenprofile sind aus den JSON-Zahlen berechnet, nicht ueber Skizzen-Bemassung gebunden -> Aenderung = JSON aendern + Generator neu laufen lassen).
- `parameters.add` ohne `unit` macht jeden Wert zur Laenge (mm); dimensionslose Faktoren brauchen `unit: ""`.
- Primitive (`solid.box/cylinder/sphere`) und `solid.pattern.rectangular` (`count1`, `spacing1`) akzeptieren Parameter-Ausdruecke -> Lochzahl der NFT-Rinne ist ueber `n_holes`/`pitch` parametrisch; Laenge ueber `len_l`.
- `config.configure`/`config.row` legt Konfigurationen an (Salatkopf S/M/L). Laufzeit: Salatkopf (13 Kugel-Booleans + Zeilen) ca. 3 min, NFT-Rinne 6 s.
- Schachtelung funktioniert: `component.create` mit aktiver Komponente als Elternteil, `component.activate` zum Zurueckwechseln; `component.insert_design` des Rinne/Netztopf/Salatkopf in eine Testdatei klappt (auch mit `reuse: true`).
- Schnittansicht: `snapshot --section XZ` mit `yaw 3.14159` zeigt die Wandstaerken; Test: Netztopf sitzt im Topfloch, Kragen liegt auf der Rippenebene.
- Annahme [A]: Topf-Kragenunterseite liegt auf der Deckelflaeche (Z 95), Kragen 3,5 mm; Salat-Ursprung = Kragenoberkante.
- Befund: Die 2160 Pflanztoepfe des OBJ stehen in den Beeten (Z 407-506, 288 je Aussenbeet), nicht in den Rinnen; die Rinnen im OBJ haben keine Toepfe -> Topfzahl der Rinnen ist unsere Auslegung (Raster 200 mm).

## Triage der Kritiker-Luecken (docs/review-protocol.md Abschnitt 5; Stand 29.10. ~04:50)

### nft_rinne, Kritiker Runde 1 (vor Scope-Card)
| Nr | Luecke (Kritiker) | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: zwei versetzte Lochreihen je Rinne | **andere Klasse / falsch gelesen** (Zickzack = Nachbarrinnen im Tisch) | Scope-Card nft_rinne, review-lessons 03:55; Umbau ZURUECKGENOMMEN: eine Lochreihe, Phase A/B (`shift` +-62,5) fuer den Tisch |
| 2 | gross: Endkappe/Spalt, Dichtung fehlt | **unklar/klein**: Klebefuge ist im Bauteilblatt dokumentiert (2 mm Kehlnaht, 0,5 mm Spalt), nicht als Koerper | Bauteilblatt Abschnitt Toleranzen; nicht umgebaut |
| 3 | gross: Ablaufstutzen tief, Tuelle nur duenner Stift | **gueltig** | Ablauf z 20 (3,5 mm Restfilm), Tuelle Wand 3 mm (inlet_id 10); gilt weiter |
| 4 | klein: Rippen zu schmal, unklar | **gueltig** | vier Rippen 5 x 5 mm statt zwei 8 x 5 |
| 5 | klein: Loecher zu nah an Kappe | **gueltig** | Loch 1 in mind. 179 mm Abstand (Reihe zentriert) |

### nft_rinne, Kritiker Runde 2 (Zickzack-Variante, jetzt verworfen)
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Wand wie Doppelschale, Deckel steht als Kragen vor | **falsch gelesen**: Schnitt zeigt Endkappen-Zapfen im Profil (Stopfen mit 0,5 mm Spiel), Deckel = Profil, Boxen gleich breit (bbox 130) | `nft_rinne-07-querschnitt.png`, check.txt Breite 130 |
| 2 | gross: Mittelrippe lose, duenn | **gueltig, erledigt durch Entfernung** (Rippe gehoert nicht zur Referenz) | Mittelrippe entfernt, Rippen jetzt 4 x 5 mm seitlich |
| 3 | mittel: Salatkoepfe so gross wie Rinnenbreite | **andere Klasse** (salatkopf) | Scope-Card salatkopf; Kopfbreite M ca. 115 mm bei Rinne 130: an Salatkopf weitergereicht (Konfiguration S 70 / M 100 / L 130) |
| 4 | klein: Stopfen mit sichtbarem Spalt | **falsch gelesen** (0,5 mm radial gewollt, Platte liegt auf Anschlag) | check: Kappenplatte buendig am Profilende |
| 5 | klein: Lochrand ~9 mm | **falsch gelesen** (Kritiker widerspricht sich selbst; Rand bei y=30 war 35 mm) | rechnerisch |

### salatkopf, Kritiker Runde 1 und 2 (vor Protokoll)
| Nr | Luecke | Einstufung | Folge |
|---|---|---|---|
| R1-1,2 | gross: glatter Kugelhaufen, keine Blattstruktur | **gueltig** | Umbau auf Blattrosette aus geneigten Scheiben |
| R1-3 | gross: zu kompakt/hoch | **widerspruechlich** (R2-2 fordert hoeher, Verhaeltnis 0,6) | Kompromiss Hoehe 61 / Breite 115 (0,53) |
| R2-1 | gross: wirkt wie Rose, 12+ Blaetter | **gueltig** | von 25 auf 33 Blaetter, 7 Gruppen |
| R2-3 | gross: Kern und Streben sichtbar | **gueltig** | Kernkugel kleiner, Herzblaetter steiler |
| R2-4,5 | klein: Blattraender glatt, Hals sichtbar | **gueltig, offen** | Ellipsen/Zacken offen; Hals D16 (bleibt, steckt im Topf) |

### netztopf: Kritiker noch nicht gelaufen (offen).

### nft_rinne, Kontextpaket-Runde (Bild-Kritiker: Modell gewaehlt; Spec-Pruefer: FAIL) 29.10. ~05:10
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| B1 | Hoehe wirkt flacher als 130:100 (vermutet) | **unklar/falsch gelesen**: Mass aus OBJ (102-103), Bild ohne Mass | layout.json hydro_tables; bleibt |
| B2 | Rippenbild: nur eine Naht je Rinnengrenze (vermutet) | **unklar**, klein | vier 5x5-Rippen bleiben (A), im Tisch pruefen |
| B3 | Befestigungspunkte an der Seitenwand (sicher) | **andere Klasse** (Tisch: Rinnenhalter/Nieten) | im NFT-Tisch umgesetzt (Rinnenhalter mit Schraube M5) |
| B4 | Tuelle am Stirnende nicht im Bild, Schlaeuche von oben/seitlich (vermutet) | **unklar**: Scope-Card verlangt Stutzen am Ende; ref-6 zeigt Schlaeuche am Tischende | bleibt, beim Orchestrator gemeldet |
| S1 | Herkunftstabelle fehlt im Blatt (sicher) | **gueltig, Eigenfehler**: Ersetzung in `partsheet.py` war beim ersten Mal wirkungslos (Zeichenfolge), Commit ef0c25e behauptete es faelschlich | behoben (Tabelle im Blatt, 19 Zeilen), 5 fehlende Merkmale ergaenzt |
| S2 | Eltern-Merkmale in der Rinne (slope_pct, Montageschritt Gefaelle, Zickzack-Checks) | **gueltig** | slope_pct aus der Rinne entfernt, Montage umformuliert, Zickzack-Check wandert in `check_nft_tisch.py`; Phase A/B der Rinne ist neu und gehoert in die Scope-Card (Orchestrator informiert) |
| S3 | Gewicht nur leer, Varianten, Stueckliste ohne Mengen, Kleber ohne Norm (sicher) | **gueltig** | Varianten-Gewichte, Fuellung, Mengen (68 Rinnen), Kleber DIN EN 14814 |
| S4 | Tuelle D16 vs. PE-Rohr 16; DN32 vs. d32 (vermutet) | **gueltig** | Schlauch ID 16 (5/8 Zoll), "Muffe d32 (etwa DN25)" |
| S5 | Lochabstand-Herkunft "2 Topfbreiten" falsch; Anzahl aussen 2/3 nicht als A | **gueltig** | Text korrigiert (3-4 Kragenbreiten = 200-250), 2/3 als A |

### nft_tisch, Bild-Kritiker (Kontextpaket) 29.10. ~05:30: Urteil "Referenz"
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, vermutet: 3 Boecke/lange Beine/Bodenrahmen, Referenz zwei Endboecke | **gueltig (Scope-Card)**: Card sagt 4 Beine | Boecke auf 2 (4 Beine) umgestellt; Laengsstreben als statische Aussteifung (A) beibehalten, in ref-6 durch Beete verdeckt |
| 2 | gross, vermutet: Rinnen schliessen fast buendig zu einer Platte, Modell mit Spalten | **unklar / Widerspruch OBJ-Bild**: OBJ hydro_tables Rinnenabstand 262-288 bei Breite 130; ref-6 zeigt Platte | Rangfolge provenance: OBJ vor Bild -> bleibt; Frage an Orchestrator/Ben |
| 3 | klein, sicher: Halter am Beinkopf breite Winkel statt Klammern | **gueltig, offen** | Kopfplatten/Winkelhalter nicht modelliert (L4), im Blatt "offen" |
| 4 | klein, sicher: Schlaeuche weich gebogen, Modell gerade starr | **gueltig, Zwischenbauteil** (Montage-Sitzung baut Schlaeuche/Verteiler nach Scope-Teilung) | gerade Stutzen bleiben als Platzhalter |
| 5 | klein, vermutet: Beine flache Profile statt Rechteckrohr | **unklar** | ref-6 verdeckt; Rechteckrohr 30x30 aus OBJ-Analyse (Tanks) bleibt (A) |
| Hinweis | Rinnenprofil flach/gerillt vs. hohes Kasten; Verteiler ueber Tischende hinaus, Schlaeuche zu Nachbartischen | **andere Klasse** (Rinne; Rohrnetz Integrator) | Rinne abgenommen; Verteiler als Platzhalter |
