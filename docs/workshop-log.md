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

### nft_tisch, Spec-Pruefer (FAIL) 29.10. ~07:25
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Standort der Beine (innen ueber dem Pool, Stuetzung Innenring) fehlt im Blatt | **gueltig (components.md Z.44)** | im Blatt als OFFEN mit Beinabstand und Bockabstand je Typ; Entscheidung Orchestrator/Integrator (Innenring Apothem 1733-1995 ueber Pool-Wasserradius 1945) |
| 2 | gross: Gewicht widerspruechlich (Volumen x 7,85 gegen 42,9 kg) | **falsch gelesen** (Masse je Koerper nach Werkstoff, Rinnen PVC 1,4) | Hinweis im Blatt, gefuellt in kg |
| 3 | klein: Stueckliste/Ports nicht bestellbar | **gueltig** | Stueckliste mit Laengen je Typ, Schrauben je Bock korrigiert (4 M6), Anker-Port mit Koordinaten |
| 4 | klein: Portrichtung mehrdeutig, DN, Gefaelle Sammelrohr | **gueltig** | "Wasser tritt ein/verlaesst, Oeffnung +Y", DN genannt, Sammelrohr horizontal als offen |
| 5 | klein: Herkunft (Mitte/gemittelt statt Unterkante, Ben bei 3 Rinnen, leere Wertspalten, fehlende Zeilen) | **gueltig** | Texte korrigiert, Ben genannt, Wertspalten gefuellt, 4 Zeilen ergaenzt |
| H | Scope-Card/detail-standard 1 cm/m gegen R06 1,5 % | **andere Klasse (Orchestrator)** | im Blatt vermerkt |

### ibc_beet, Bild-Kritiker (Kontextpaket) 29.10. ~07:35: Urteil "Modell"
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: 2953 mm gegen "halbe IBC" (ca. 1200 x 1000) | **gueltig als Dokumentationsluecke**, Mass aus OBJ (Ben > OBJ) | Blatt: Sonderwanne, Klaerung Orchestrator |
| 2 | gross, vermutet: Siebboden 5 mm / zwei Stuetzen tragen 300 mm Medium nicht | **gueltig** | Siebboden 8 mm, Stuetzen 8 x 3 (aussen) / 5 x 3 (innen), Abstand <= 420 mm |
| 3 | klein, vermutet: Randsims breit und flach in der Referenz | **gueltig (klein)** | Randsims 20 x 14 mm |
| 4 | klein, sicher: Zulaufrohr ohne Fitting/Dichtung; Tropfloecher quadratisch | **gueltig, offen** | im Blatt offen (Gummitulle, quadratische Vereinfachung begruendet: Zylinder-Zylinder-Schnitt > 1 min je Loch) |
| 5 | klein, sicher: Querschnitt 06 zeigt nur leere Wand | **gueltig (Render)** | Schnitt jetzt durch die Siphonebene (x = Siphon) |
| Hinweis | Pflanzen, NFT, Einbautiefe | **andere Klasse** | - |

### ibc_beet, Spec-Pruefer (FAIL) 29.10. ~07:55
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Gewicht leer 759 kg enthielt das Medium; gefuellt in kg fehlt | **gueltig** | Leermasse ohne Medium (72-74 kg), Medium und Wasser getrennt, gefuellt je Variante in kg (aussen_933 ca. 1,6 t) |
| 2 | gross: Pruefung innen maskiert Abweichung (Z 365-404 statt 400) | **gueltig (Doku)** | im Blatt: Medienoberflaeche innen absolut 365-404 (z0 -209..-170), Toleranz 40 mm begruendet |
| 3 | gross, vermutet: Wasserstand/Standrohr widersprechen sich (R03 Befund 4/5, SRAC) | **gueltig, unklar** | im Blatt als offen mit Spannweite 3-6 cm, Konfidenz niedrig; Hoehe 220 (R03 Befund 5) bleibt |
| 4 | gross: Herkunft/Detail unvollstaendig (Wertspalten, Rohrwaende, DN, Normen, Stueckliste-Mengen, Renders leer, PP/HDPE) | **gueltig** | 7 Herkunftszeilen, DN/Normen, Stueckliste mit Mengen, Render-Liste ueber alle Variantenordner, Werkstoffzeile |
| 5 | klein: Zulaufport x -1526 gegen Box -1516,5; Rohr laengs statt quer | **gueltig** | Ports aus aktuellen Parametern neu berechnet; laengs als Auslegung E begruendet |
| H | 288 je Aussenbeet / Montage Netztoepfe | **andere Klasse (Integrator)** | im Blatt klargestellt (144 beim Beet Azimut 113) |

### ibc_beet, Orchestrator-Vorgaben 29.10. ~08:00 (nach Abnahme)
Standrohr `standpipe_over` = media_depth - 35 = 265 (FarmHub 220 als Variante vermerkt), Glocke 295 (Standrohr + 30), Bezeichnung "IBC-Wanne (Sondermass nach OBJ)", Zulauf laengs als A. Beete neu gebaut, check_ibc_beet.py 66/66 PASS.

### tank (klein/gross), Bild-Kritiker (Kontextpaket) 29.10. ~08:05: Urteil "Modell"
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, vermutet: Biomediumkorb schwebt, keine Auflage | **gueltig** | 4 Konsolen unter dem Tragrost (40x40x30 an die Tankwand) |
| 2 | klein, sicher: Randwulst nur duenne Doppellinie, Referenz dicker Wulst | **gueltig** | Wulst 25 x 40 mm, Deckel buendig (lid_over 0) |
| 3 | klein, vermutet: Beine ragen 250 mm ueber die Plattform | **unklar** (OBJ-Mass 751) | bleibt, im Blatt offen |
| 4 | klein, sicher: Diagonalenenden ragen ueber die Beine | **gueltig** | Diagonalen um Beinhalbbreite + 8 mm gekuerzt |
| 5 | klein, vermutet: Revisionszugang fehlt | **gueltig** | Revisionsoeffnung D200 im Deckel |
| Hinweis | Schlaeuche, Wasserspiegel, Pumpe | **andere Klasse** | - |

### tank, Spec-Pruefer (FAIL) 29.10. ~08:25
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Gewichte widersprechen sich (136 gegen "leer 95 / ohne Biomedium 41"), Box nur fuer klein, Z -24 | **gueltig (Blatt)** | Text falsch beschriftet (Biomedium-Masse als "ohne Biomedium"); Boxen und Gewichte je Variante; Schraubenenden 24 mm im Boden vermerkt |
| 2 | gross: Text widerspricht Parametern (47 Grad, Randwulst 20x30, D633, Deckel 8 mm Ueberstand), Kegel A statt E | **gueltig (Blatt)** | Blatt jetzt aus Parametern berechnet; Kegel E (R09-Nachtrag); Check 45-60 Grad |
| 3 | gross: Klein-Auslauf z 1288 ueber dem Rand; R09: 100 mm unter dem Rand; Leitrohrende 833 statt 1/3 Zylinderhoehe; Checks fehlen | **gueltig (Modell)** | Auslaufrohr radial durch die Wand 100 mm unter dem Rand (beide Tanks), Leitrohr endet 1/3 Zylinderhoehe ueber der Spitze, Check-Zeilen fuer Auslauf/Ueberlauf/Leitrohr (60/60 PASS) |
| 4 | klein: Herkunft unvollstaendig (Wulst, Revision, Konsolen, Spiel, Auslaufhoehe, Leitrohr; R09 nur klein; Dichte) | **gueltig** | 20 Herkunftszeilen, R09 nur klein vermerkt, Dichte Fachwert |
| 5 | klein: Ports/Stueckliste (DN, d55 kein Normmass, Schrauben ISO, Konsolen, Revisionsdeckel, Bulkheads, kein Leitrohr im Biofilter, Instanz-Versatz) | **gueltig** | DN ergaenzt, Hahn gross d50, ISO-Nummern, Stueckliste ergaenzt, Biofilter ohne Leitrohr als offen, Versatz bis 5 mm im Blatt |
| H | Wasserfuellung gehoert DRAUSSEN | **Hinweis** | nur als Gewichtsangabe (nicht modelliert) |

### pumpe (pumpe_klein, pumpe_gross, filtermodul), Spec-Pruefer (FAIL) 29.10. ~08:50
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Rolle "384er Kassette = Filter" widerspricht der Lage (radial zur Tankachse, r 84-468, Oberkante = Plattform-OK, innerhalb der Plattform) -> Stuetzrippen der Klasse Tank? | **gueltig, unklar** | Gegenindizien im Blatt (funktion/abweichung/offen/Herkunft), Frage an den Orchestrator; Bauteil bleibt als Annahme gebaut |
| 2 | gross: Anzahl nicht konsistent (components.md 4-8; hydraulics 4 Pumpen + 2 Siebe) | **gueltig** | Duplikate-Logik erklaert (4/8 OBJ-Eintraege -> 2 bzw. 1 Duplikate), Abweichung zur Hydraulik als offen |
| 3 | gross: Herkunft formal unvollstaendig (Wertspalten, Stecker, Kabel, Gewichte, Farbe, Ports) | **gueltig** | 19 Zeilen mit Werten |
| 4 | klein: Gewicht/Foerderdaten (Mischdichte, gefuellt, "Foerderstrom offen" gegen hydraulics 12/30 l/min) | **gueltig** | Dichten ausgewiesen, Foerderstrom 12/30 l/min [E] aus hydraulics.md 2.3 |
| 5 | klein: Kleinigkeiten (foot_h, Kabelport x, "0 mm", yaw, Stueckliste, +Y-Ausrichtung) | **gueltig** | alle korrigiert (Steckerende x, <= 1 mm, yaw 0/45/90/135, Schrauben/Dichtung in der Stueckliste, +Y vom Tank weg) |
| H | Durchdringung Kassette/Plattform, Rohrnetz Pumpe A/B, Elektrik | **andere Klasse** | im Blatt als offen |

### salatkopf, Bild-Kritiker Runde 3 (Kontextpaket) 29.10. ~09:00: Urteil "Referenz"
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: Silhouette aus regelmaessigen glatten Scallops, Referenz fransig/unregelmaessig | **gueltig** | 36 Blaetter einzeln mit deterministischem Zufallsversatz (Azimut +-8 Grad, Radius +-14 %, Neigung +-4,5 Grad, Hoehe), Gruppen ohne Muster |
| 2 | gross, vermutet: glatter Kuppelkern, Referenz buschiger Huegel | **gueltig** | Kern 0,27 statt 0,32, Herzblaetter ueberdecken |
| 3 | gross, vermutet: Blaetter als horizontal gestapelte Teller | **gueltig** | Neigungen gestreut, Saum haengt nach unten |
| 4 | klein, sicher: Randblaetter in der Referenz haengen nach unten | **gueltig** | Saum alpha -14 Grad |
| 5 | klein, vermutet: Hals sichtbar | **unklar** | Hals steckt im Topf (Z<0); Saum reicht bis 7 mm ueber den Topfkragen |
| Hinweis | Instanzen gleich gedreht/gross | **andere Klasse** (Layout/Tisch) | an Integrator: Instanzen mit variierender Drehung/Konfiguration setzen |

### salatkopf, Bild-Kritiker Runde 4 (29.10. ~09:10): Urteil "Referenz" (vier Runden erschoepft)
Luecken: glatte runde Scheiben / Scalloprand (gross, sicher), konzentrische Schichtung ohne unregelmaessigen Huegel (gross), Instanzen identisch (gross, Layout = andere Klasse), Kern zu hoch (klein), einfarbig (klein, Stil). Einstufung: **gueltig, mit Facettenbudget nicht weiter loesbar** (gekraeuselte Blaetter brauchen viele Flaechen; jeder Koerper hat < 8 Flaechen, 37 Koerper); **Layout/Integrator**: variierende Drehung und S/M/L-Mischung. Stand: nicht bestanden im Sinn "Kritiker waehlt Modell", Restluecken im Blatt offen; Orchestrator entscheidet ueber die Abnahme.

### netztopf + salatkopf, Spec-Pruefer 29.10. ~09:15: netztopf FAIL, salatkopf PASS
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross (netztopf): Anzahl 2160 nur Beete; Rinnen 556 fehlen (gesamt ~2716); Board "Salatkopf ca. 240+" passt zu keiner Zahl | **gueltig** | Anzahl 2160 + 556 = 2716 im Blatt; Board-Widerspruch und D04 (Rinnen ueber Beeten) an den Orchestrator |
| 2 | gross (netztopf): Scope-Card nur eine Zeile; Schlitze/Bodenloch nur A; Bild-Kritiker nie gelaufen | **gueltig (Doku)** | Scope-Card-Ergaenzung beantragt; Herkunftszeilen Schlitze/Bodenloch/Konus; Bild-Kritiker nicht moeglich (Netztopf in keiner Referenz sichtbar), im Blatt begruendet |
| 3 | klein (netztopf): Render-Verweis netztopf-01.png existiert nicht; check prueft Wand/Kragen nicht | **gueltig (klein)** | Verweise auf -02-schnitt korrigiert; Wand/Kragen als offene Pruefzeile (Schnittbild) |
| 4 | klein (salatkopf): Widersprueche (4 Blattgruppen/33 Blaetter/Hoehe 0,7 x Breite, Gewicht "leer") | **gueltig** | JSON-Beschreibung, Herkunft und quelle_masse auf 36 Blaetter/7 Gruppen/0,5 x Breite; Masse = Frischmasse-Naeherung |
| 5 | klein (salatkopf): Kern/Blattdicke/Gruppen/Jitter ohne Herkunftszeile | **gueltig** | 4 Zeilen ergaenzt |
| H | Rinne D52 gegen Card D50 (dokumentiert), "288 je Aussenbeet" (Beet Az 113 hat 144), Raster 24 x 12 gegen distinct_along 64 | **andere Klasse** | im Blatt als offen (Integrator/Orchestrator) |

### knoten, Spec-Pruefer (FAIL) 29.10. ~08:40
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Abweichung Kugel statt Platten nicht gemeldet; Ankerlasche fehlt in der Card | **gueltig (Meldung)** | an den Orchestrator gemeldet; ANGENOMMEN (decisions D15, Scope-Card Revision 08:40) |
| 2 | klein: Gewicht 5,77 gegen 6,08 kg (Normteile mit Standarddichte 1,29) | **gueltig** | Normteile nachtraeglich auf Stahl (`sc.assign_part_materials`), Blatt 6,03 kg = Volumen x 7,85; Vollkugel 4,1 kg im Blatt |
| 3 | klein, vermutet: Passung 23,6 zu eng nach Verzinken/Schweissen | **gueltig** | Steckarm 23,0 (0,5 mm Spiel je Seite), alle 26 Knoten neu gebaut |
| 4 | klein: Ports nur fuer 3 Knoten ausgeschrieben, Ankerlasche-Achse mehrdeutig, Bolzenachse fehlt | **gueltig** | docs/parts/knoten-ports.md (alle 26 Knoten mit Spitzen, Richtung, Bolzenachse, Azimut), Lochachse tangential = umlaufend |
| 5 | klein: Montage (Anzugsmoment, Zink, Toleranz) | **gueltig** | M10 8.8 49 Nm, M12 85 Nm, Zink-Nacharbeit, Vorrichtung +-0,5 Grad |
| H | Tuer-Sturz, Gabel M12/D14, Strebenwand 3 | **andere Klasse** | Hinweis |

### Orchestrator-Entscheidung D-Punkt 4 (29.10. ~08:55) umgesetzt
Die 10 Kassetten 384 x 44 x 419 sind Stuetzrippen/Konsolen der Tankplattform (Klasse Tank): tank_gross.sc (Tank 2, Rippenphase 11,0 Grad) und tank_gross_t3.sc (Tank 3, 53,6 Grad) haben je 5 Stuetzrippen (Kantholz 44, Dreiecksknaggen unter dem Kegel, radial, Winkel 0/90/135/180/225 Grad), check_tank.py 100/100 PASS. Die Klasse filtermodul entfaellt (Datei und Renders entfernt), pumpe bleibt mit 4 Pumpentafeln (check_pumpe.py 28/28 PASS).
Herleitung der Rippenform: Bounding-Box 384 x 419 mit Steigung 419/384 = 47,5 Grad entspricht dem Kegel (47 Grad): rechtwinkliges Dreieck mit der Hypotenuse entlang der Kegelflanke; aussen r 440 statt 468, damit die Rippe die Querstreben nicht durchdringt; Oberkante Plattform-Unterkante statt -Oberkante (die hohle Plattform nimmt die Rippe auf).

### fundamentanker, Spec-Pruefer (FAIL) 29.10. ~08:50
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Herkunft Lochhoehe/Ausrichtung als E/hoch ueberzeichnet | **gueltig** | E + A, Konfidenz mittel; Lochachse tangential als A |
| 2 | klein: "235 mm unter Gelaende" nicht herleitbar | **gueltig** | ersetzt: Ankerplatte OK z -243, Betonkopf z -258 (Welt, Knoten bei -14); Gelaende offen (Montage) |
| 3 | klein: Montage/Stueckliste (Mutter, Anzugsmoment, Bolzenueberstand 2 mm) | **gueltig** | Gewindestange mit Mutter, Anzugsmomente, M12x55 (7 mm Ueberstand) |
| 4 | klein: Diagonale ++/-- unklar, ISO 273 M16 = 17,5 | **gueltig** | beide Angaben korrigiert (Loch D17,5) |
| 5 | klein: Herkunftskategorie "Scope-Card" unzulaessig | **gueltig** | "A (Scope-Card)" |

### W10 Leitungsteile-Bibliothek 29.10. ~09:20
49 Definitionen (Rohr, Kupplung, Bogen 90/45, T-Stueck, Kugelhahn, Klemme je d25/32/40/50/63/110; Schlauch ID16/25 gerade + Bogen 90 (R = 5 x AD); Verteiler d32 n2-4), check_leitungsteile.py 78/78 PASS (Volumen = Ringflaeche x Mittellinie nach Pappus), Sammelblatt docs/parts/leitungsteile.md. Befunde zu SolidCraft: Revolve-Cut an deckungsgleichen Stirnflaechen scheitert -> Bohrung als Werkzeugkoerper + `solid.combine` (cut); zweiter Bogenschenkel ueber `solid.extrude face=...` (Endflaeche verlaengern) statt Cylinder-Union an schraegen Flaechen (45 Grad scheitert).

### leitungsteile (W10), Spec-Pruefer Runde 2 (FAIL knapp) 29.10. ~13:35
Runde 1 (FAIL, 5 Befunde) wurde im Blatt behoben; Runde 2 rechnete 5+ Stichproben nach (Wasser l/m, Reduzierlaengen, Bogenradius, Port-Lagen, Dateizahl 63) ohne Abweichung.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Wandabweichung "bis 0,6 mm" falsch beziffert (Leitrohr d110 Wand 3 gegen 5,2; Pumpe d40/d32; Tisch d25) | **gueltig (Doku)** | Abschnitt "Wandstaerken-Abweichung" im Blatt mit allen Klassen; Abgleich beim Orchestrator offen |
| 2 | gross: Tisch-Verteiler (d25, Stutzen D16, Teilung 262-288) gleich Bibliotheks-Verteiler d32/Teilung 120? | **gueltig, andere Klasse** | Verbraucher-Tabelle korrigiert: Tisch-Verteiler gehoert der Tisch-Klasse, Bibliothek hat keinen d25 mit Abgang D16 (offene Frage) |
| 3 | klein: "49 Dateien" in der Pruefung, Klemme fehlt in der Port-Ausnahme | **gueltig** | 63, Klemme als Ausnahme |
| 4 | klein: Herkunft fehlt (Mittelsteg, T-Arm, Hahn-Gehaeuse, Verteiler-Abgang, d20 als PVC statt PE), Dichten "mittel" | **gueltig** | 6 Zeilen ergaenzt, Dichten niedrig; Spindel/Hebel-Kommentar "Schweissverbindung" meint 3 mm Einschub (Kommentar, kein Modellfehler) |
| 5 | klein: Farbkonflikt selbst gemacht, SDR 21 = PN12,5 ohne Quelle | **gueltig** | als Annahme A (ID16 hellblau/ID25 dunkelblau) umformuliert, SDR 21 mit PN10/12,5 je Tabelle, Konfidenz niedrig |
| H | Kupplung nicht per `parts.insert` (Scope-Card); Bibliothek d20 PVC statt PE; Rohrwand 3 mm in Tank/Pumpe/Tisch | **andere Klasse / unklar** | im Blatt als offene Fragen, Orchestrator entscheidet |

### leitungsteile (W10), Spec-Pruefer Runde 3 (PASS knapp) 29.10. ~13:55
Die 5 Punkte aus Runde 2 bestaetigt behoben; Nachrechnung (Wand, Port-Lagen, Wasser l/m, 63 Dateien, 231/231) ohne Abweichung.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | klein: Leitrohr d110 in der Verbraucher-Tabelle beim Biofilter (gross) statt beim Absetzer (klein) | **gueltig** | `tank.md` 104/172: Leitrohr nur Absetzer; Tabelle korrigiert, Belueftung d16 als Nicht-Bibliotheksteil vermerkt |
| 2 | klein: Wandabweichung nicht vollstaendig (Rinne d32 W2, Beet d20 W2, Pumpe gross d50 W3) | **gueltig** | drei Eintraege ergaenzt |
| 3 | klein: Herkunftsmarken "R"/"Bild + hydraulics" statt Marke + Bezug; Zeilen fehlen (Schlauchbogen-Schenkel/-Wand, Standardlaenge 1000, DN-Zuordnung) | **gueltig** | Marken auf OBJ/Bild/A mit Bezug in der Bezugsspalte, 3 Zeilen ergaenzt |
| 4 | klein: Pruefungsabschnitt nennt nur Runde 1 | **gueltig** | Runden 1-3 eingetragen |
| H | tank.md 73 "DN30" fuer d40 (sonst DN32); `.bak`-Dateien in designs/components | **andere Klasse / Hinweis** | Tank-Blatt Hinweis an den Orchestrator; .bak sind gitignored |

### pumpe (W12), Spec-Pruefer Runde 2 (FAIL) 29.10. ~14:05
Kernzahlen (Anzahl 4/4, Tafelmasse, Stutzen-DN, Port-Koordinaten, Masse 5,28/8,53 kg) nachgerechnet ohne Abweichung.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Pumpenkopf dringt 2 mm in die Konsole (Kopf-D > Motor-D + 16) | **gueltig (Modell)** | pumpe.py: Sockelhoehe = (Kopf-D - Motor-D)/2 + 1 = 11 mm statt 8 (Achse bleibt z 120, Ports unveraendert), neue Pruefzeile Kopf/Konsole, check_pumpe 30/30 PASS; Bild pumpe_gross-02 |
| 2 | gross: Konsolenmass 150x100x5 + 40 falsch (gemessen 150 x 117/137 x 5), Sockelmasse fehlen, Steckerende -316/-336 (-315/-335), "PVC-U d40/d50" | **gueltig** | Stueckliste/Herkunft aus Messung, Steckerenden und Stutzen-d korrigiert |
| 3 | gross: Reste der Filtermodul-Klasse (Siebeinsatz, 10 Tafeln, build_filter, Filter-Zweig im Check) | **gueltig** | aus Blatt, pumpe.py, check_pumpe.py entfernt; Doku ausserhalb (scope-cards 34/37, components.md 22, detail-standard 28/40) -> Orchestrator |
| 4 | klein: Stueckliste/Befestigung (Dichtung ID16 ohne Port, Scheiben/Muttern, M6x16 zu kurz, Standwinkel-Untergrund) | **gueltig** | M6x20 im Modell (Klemmlaenge 15,2/17,2), Dichtung gestrichen (Rohrnetz), Scheiben/Muttern [A], Untergrund Erde als offen |
| 5 | klein: Dichte 0,91 gegen gemessene ~1,9, Gewicht/Hydraulik (4-9 kg), Anzahl "4 Module" statt 8, Foerderstrom 30 gegen 12 l/min | **gueltig / teils vermutet** | Dichten-Mischung und Herkunft, Gewicht modelliert/real getrennt, Anzahl 8 gegen 4 Pumpen, 30 l/min = Tankumwaelzung (hydraulics 2.3) vs 12 l/min je Pool-Linie (2.4) im Blatt |
| H | D16-Reste in Scope-Card/components/detail-standard; Kassetten im Tank-Blatt; Rohrwand 3 mm; Kabel 150 mm; Pumpe/Tankkegel | **andere Klasse** | Orchestrator/Tank/Integrator, im Blatt unter Offene Fragen |

### pumpe (W12), Spec-Pruefer Runde 3 (FAIL knapp) 29.10. ~14:30
Runde-2-Punkte in Sache behoben (Kopf/Konsole 1 mm Luft, Masse, Filter-Reste im Code, Dichten, Anzahl).
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Pumpenschrauben M6x20 zu kurz (Klemmlaenge Sockel 11 + Konsole 5 + Mutter 5,2 = 21,2) | **gueltig** | M6x30 (24,4 mm mit 2 Scheiben), nicht modelliert [A] |
| 2 | gross: Konsole war ein T (Vertikalschenkel mittig auf der Platte, z 39-79), Schraubenkoepfe zur Haelfte in der Platte; Normteile mit Dichte 1,29 | **gueltig (Modell)** | Vertikalschenkel haengt nach unten (z_s-40..z_s), Schrauben mittig im Schenkel; `assign_part_materials` auf Stahl; neue Pruefzeile Konsole = Winkel; Bilder 04-seite, check 32/32 PASS |
| 3 | gross: check.txt veraltet (28/28) | **gueltig** | check.txt neu aus dem Lauf, Blatt nennt 32/32 |
| 4 | klein: 384er/Tafelnmasse-Reste in der Abweichungszeile | **gueltig** | Zeile bereinigt, Tippfehler korrigiert |
| 5 | klein: "Pumpe A" fuer die grosse Tafel (hydraulics.md: Pumpe B hinter dem grossen Tank) | **gueltig (Annahme)** | gross = Pumpe B, Herkunftszeile A |
| H | hydraulics.md 51/61 fuehren "Filtermodul" weiter; Pumpen-A/B-Positionen, Siebe, Untergrund Erde | **andere Klasse** | Orchestrator/Hydraulik/Integrator, im Blatt offen |

### pumpe (W12), Spec-Pruefer Runde 4 (PASS knapp) 29.10. ~15:00
Runde-3-Punkte per Messung bestaetigt (Konsole z 24..64 Winkel, Kopf 1 mm Luft, keine Durchdringung ausser gewollt, check 32/32, Normteile Stahl, A/B konsistent).
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | klein: Body1 (linke Konsolenschraube) in pumpe_gross.sc hat D6-Stummel (12 statt 10 Flaechen) | **gueltig (Modell)** | parts.insert-Eigenheit am ersten Bolzen (auch bei vertauschter Reihenfolge); pumpe.py schneidet ihn per Werkzeugkoerper + solid.combine ab; neue Pruefzeile Schraubenvolumen gleich, check 34/34 |
| 2 | klein: Klemmlaengen-Rechnung M6x20 mit/ohne Scheibe uneinheitlich (gross 1,2 mm Ueberstand) | **gueltig** | Scheiben bei den Konsolenschrauben gestrichen, Ueberstand 4,8/2,8 mm im Blatt |
| 3 | klein: Standwinkel-Befestigung an der Tafel fehlt, waagerechter Schenkel 80 mm nicht im Blatt | **gueltig** | M6x16 Winkel/Tafel, Bodenschrauben, Masse 50x100x5 / 50x80x5 in Stueckliste und Herkunft |
| 4 | klein, vermutet: Pumpenbefestigung auf dem Sockel offen, M6x30 ohne Herkunftszeile | **gueltig** | Fuss/Spannband als offene Frage, Herkunftszeile E |
| H | Template zeigt Box/Volumen nur der ersten Variante unbeschriftet | **gueltig (eigenes Skript)** | partsheet.py beschriftet "Variante pumpe_klein" |

### nft_tisch (W16), Bild-Kritiker Runde 1 (FAIL) 29.10. ~17:50
Bilder: Ecke Draufsicht/Iso, Querschnitt Bock + Beet, Innentisch oben, Aussentisch iso (Erstfassung, Y radial nach aussen gedacht).
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Verteiler und Sammelrohr kreuzen sich an der Ecke (V in der Draufsicht) | **gueltig (Modell/Konvention)** | Ursache: Tisch-KS Y war radial AUSSEN gedacht, die Platzierung mit yaw = az + 90 (= OBJ-yaw) ergibt aber Y radial INNEN (Y = Z x X); das Pruefskript rechnete mit gespiegelter Abbildung. Konvention umgedreht (Y innen), Reihenlaengen/Rohrschraege/Ausleger/check_nft_fit angepasst; Bild nach Korrektur: Rohre parallel zur Sektorgrenze, Abstand gleichmaessig 171-190 mm |
| 2 | gross, vermutet: Schraegstellung/Rinnenlaengen passen nicht zur Sektorform (gespiegelt) | **gueltig** | dieselbe Ursache wie 1 |
| 3 | mittel, vermutet: Fussplatten schweben ueber der Beet-Unterkante | **falsch gelesen** | Beete liegen laut layout.json 162 mm unter dem Boden (Erdtaschen, z0 -162), Fusspunkte z 0 = Gelaende |
| 4 | mittel, vermutet: Verteiler/Sammelrohr ohne Halterung, Innen-Ausleger ohne Kippsicherung/Diagonalen | **gueltig, als Annahme dokumentiert** | Rohrschellen und Statik sind im Blatt unter Offene Fragen; kein weiteres Bauteil (Platzhalter A) |
| 5 | klein, vermutet: Laengsaussteifung nur unterer Riegel, nur einseitige Diagonale | **gueltig** | Laengsdiagonalen 25x3 je Beinseite (portal 2, innen 1) eingebaut, Pruefzeile |
| H | Beet innen leer, Ablaufoeffnung unter dem Rinnen-Eckbereich, Pflanzen fehlen | **andere Klasse** | Beet/Pflanzen |

### nft_tisch (W16), Bild-Kritiker Runde 2 (PASS) + Spec-Pruefer (FAIL) 29.10. ~18:45
Teil A (Bild): PASS; Ecke parallel, Luft ca. 190 mm, Beine ausserhalb der Beete (Luecken nur klein: Beetbreite im Bild 933 gegen 993 gerechnet, Luft nicht im Bild lesbar, Gehweg offen = schon im Blatt). Teil B (Spec): Nachrechnung (Rinnenlaengen, Beinabstand, Pfosten ap 2205, 466 Topfloecher, Lochphasen, Ports, Holm 16 N/mm2) ohne Abweichung; 5 Befunde:
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross: Herkunftstabelle doppelt (fix_tisch_blatt3 lief zweimal), veraltete Beinlage 587/557 gegen 606/576, doppelte Saetze in funktion/strut_z | **gueltig** | fix_tisch_blatt4.py (idempotent): Duplikate entfernt (40 -> 34 Zeilen), erste/aktuelle Fassung behalten; blatt3 mit Warnung versehen |
| 2 | mittel: leg_inset und "Holm 30 mm ueber die Beine" ohne Wirkung im Portalbock | **gueltig** | leg_inset gestrichen, holm_overhang nur als Kragarm-Ueberstand innen, Zeile "Holmueberstand/Beineinzug" ersetzt |
| 3 | mittel: "yaw = az + 90 = OBJ-yaw" gilt nur modulo 180 (layout.json yaw 0-180, aussen Sektor 3/6-9 az - 90) | **gueltig** | Blatt: yaw = az + 90 in vollen 360 Grad; OBJ-yaw woertlich = Tisch um 180 Grad gedreht (genau der Spiegelfehler von Runde 1); Hinweis an Integrator in der Fertigmeldung |
| 4 | klein: Marken "[Orchestrator D18]", "Scope-Card + A", "A + Normteil"; Herkunftszeilen fehlen (corner_gap, leg_clearance, Beckenrand Z 650, foot_hole) | **gueltig** | Marken auf A (mit Bezug D18/Scope-Card), 6 Zeilen ergaenzt |
| 5 | klein: Kopf "Revision A" bei Rev. B | **gueltig (eigenes Skript)** | partsheet.py liest revision aus dem JSON (B) |
| H | Wasserfuellung/Topfloecher-Summe/Lochplanung liegen im Tisch statt Rinne; Beet-Tropfrohr im Bild; Fundament fuer 10 Auslegerpfosten (Boden = Erde); Pool-Wand 150 ist Platzhalter | **andere Klasse / Hinweis** | Integrator/Beet/Pool/Orchestrator |

### salatkopf (W07 Rev. B), Bild-Kritiker Runde 5 29.10. ~19:40: Urteil "Referenz" (B)
Modell Rev. B (72 Polygonblaetter, 12-Eck, Fibonacci auf Halbellipsoid). Proportion keine Luecke (0,53).
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: zu wenig Fuelle/Feinheit, Blaetter ca. 1/3 Kopfbreite, dunkle Spalten | **gueltig** | Rev. B2: 96 statt 72 Blaetter, 18 x 15,5 statt 21 x 18 mm, Huegel b 34; check 18/18, 98 Koerper, 1357 Flaechen, OBJ-Export 8756 Dreiecke (gemessen, `solidcraft-cli run salatkopf.sc --out x.obj`); Flaechenbudget im Check 1200 -> 1500 |
| 2 | gross, sicher: Krone wie Artischocke, steile Lamellen oben | **gueltig** | Anstellwinkel 16 + 0,5 x Hoehenwinkel (vorher 15 + 0,55), Streuung +-13 statt +-21 Grad; Seitenbild salatkopf-03 zeigt geschlossene Kuppe (Hoehe 51,5, Breite 102) |
| 3 | klein, sicher: Ausreisser/Stabblaetter an der Silhouette | **gueltig** | Streuung Laenge 22 -> 14 %, Breite 18 -> 12 %, Roll +-65 -> +-50, Azimut +-55 -> +-50 |
| 4 | klein, vermutet: Hals frei sichtbar, kein haengender Saum | **falsch gelesen / teils andere Klasse** | Hals liegt per Bezug bei Z < 0 im Netztopf (im Elternkontext verdeckt); Einzelbild zeigt ihn nur, weil der Topf fehlt; Saum haengt nicht tiefer, weil Blaetter nicht in den Kragen eindringen duerfen (check Z >= -1) |
| H | Instanzen gleich gross/gedreht, Topf sichtbar, Rinnenbreite | **andere Klasse** | Layout/Tisch, Netztopf, Rinne |
Kein zweiter Bild-Kritiker-Lauf (Pruefer-Budget, ein Lauf je Komponente); Gesamtstand: Kritiker waehlte die Referenz, Luecken 1-3 danach in Sache umgesetzt und nicht erneut abgenommen. Orchestrator entscheidet.

### netztopf (W07), Spec-Pruefer Runde 2 29.10. ~19:45: FAIL
Kernzahlen (Box, Volumen/Masse, Anzahl 2160/556/2716, Spiel D52/D50) nachgerechnet ohne Abweichung.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, vermutet: Herkunft "OBJ/hoch" fuer 63/50/64 ueberzogen (size_mm Konstante, Check liest sie nur zurueck, oasis-obj-analysis nennt 0,05 x 0,06 x 0,06 m) | **gueltig** | extract_layout.py:78 hartcodiert; Herkunft auf "OBJ-Box + E", Konfidenz mittel; Achszuordnung als offene Frage; Check-Zeile benennt "kein unabhaengiger Beleg" |
| 2 | klein: Pruefzeile 14/14 veraltet, Spiel nicht geprueft | **gueltig** | check_pflanze 18/18 (neu: Spiel hole_d - rim_d = 2 mm), check.txt neu |
| 3 | klein: erledigte offene Fragen (Scope-Card, Board 240+), Stueckliste "Orchestrator entscheidet" | **gueltig** | entfernt, D17 genannt |
| 4 | klein: Werkstoff doppelte Marke [E]/[A] | **gueltig** | auf A |
| 5 | klein: Salatkopf-Gauntlet im Netztopf-Blatt | **gueltig** | Pruefzeilen und Kritiker-Feld bereinigt |
| H | Hals-Check nahm Innen-D 47 (oben), in Halstiefe 40,7 | **gueltig (eigener Check)** | Check rechnet den konischen Innen-D in Halstiefe (40,7 > 16); Hinweise zu Rinne (Topfboden/Film) und Beet-Raster im Blatt unter Offene Fragen |

### winkelhalter (W11) + nft_tisch, Spec-Pruefer Runde 1 29.10. ~20:20: FAIL
Masse, Anzahl 76, Lage und 180-Grad-Drehung nachgerechnet ohne Abweichung; Auslegerbock innen: Winkel 69 mm ueber dem Beckenrand Z 650, 30 mm Radialluft.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: Winkelschraube M6 (z -45) durchdringt die Diagonalenschraube M6x40 (z -40) im Bein, 56 Stellen | **gueltig (Modell)** | Loecher im senkrechten Flansch jetzt z -10 / -26 (wh_edge_v 10, wh_pitch_v 16); inspect.interference im Check: 0 Treffer in innen/mitte/aussen |
| 2 | gross, sicher: Mutter/Schraubenspitze der unteren Winkelschraube durchdringen die Laengsdiagonale (Ende z -45), 38 Stellen | **gueltig (Modell)** | gleiche Aenderung (Mutter bis z -31,8, Diagonale endet ca. -33,6); Interferenzcheck 0 |
| 3 | gross, sicher: Blatt sagt Bein/Holm geschweisst, Winkel sagt "lag nur auf" | **gueltig (Konzept)** | Entscheidung: Fussplatte-Bein geschweisst, Holm/Kragarm am Bein geschraubt ueber T23 (Bohren vor dem Verzinken); nft_tisch- und Winkelblatt angeglichen; Statik innen (Winkel nahe dem Kragarm-Drehpunkt) offen |
| 4 | klein, sicher: Check liest Platzierungskonstanten, misst Holmunterkante nicht, Breite/Dicke ungeprueft, keine Interferenz | **gueltig (eigener Check)** | Beininnenflaeche aus Bein-bbox, Unterkante Holm/Kragarm gemessen, Breite/Schenkel/Masse, inspect.interference; 196/196 PASS. Gesamtzahl 76 nicht im Check (Tischzahlen kommen aus components.md, nicht aus dem Modell) |
| 5 | klein, sicher: Tischzahlen-Quelle falsch zitiert (hydro_tables ist Beispielliste), Marke "nft_tisch", M6x50 nur 0,8 mm Ueberstand, Gewicht mit/ohne Normteile, Material im Tisch Default 1,29, Scope-Card ohne Masse/Fehlinterpretation, Hoehe 718,7 statt 721 | **gueltig** | Quelle docs/components.md, Marke A, M6x55, Blatt nennt 127 g Winkel / 174 g gesamt, nft_tisch.py weist Normteile/Winkel Stahl zu (sc.assign_part_materials mit Muster), Scope-Card ergaenzt, Z 719-781 |
| H | Bein/Holm ohne Schraubenloecher, Normteile durchdringen die Rohrwaende | **vereinfacht, im Blatt genannt** | Interferenzcheck ignoriert Bein/Holm/Kragarm bewusst |

### W17 Radialbudget (nft_tisch, ibc_beet aussen_800) 29.10. ~21:30: Pruefer NICHT gelaufen
Grund: Wochenlimit 93 % / 5h-Fenster 91 % (Regel Wochenlimit, docs/endless-mechanics.md); Orchestrator entscheidet ueber Nachpruefung (ein Bild-Kritiker Draufsicht + Spec-Pruefer nur fuer die neuen Parameter). Eigene Messungen: check_nft_fit 40/40 (Laufweg A 600, B 600, Wandluft 218, NFT-Summe 462 >= 459, Beine >= 30 mm von den verschobenen OBJ-Beeten), check_nft_tisch 196/196 inkl. Interferenzlauf Winkelhalter, check_ibc_beet aussen_800 22/22.
Eigener Fund beim Bau (Lehre): Die Hintergrundkette las die Parameter beim Start des Tischbaus; eine Parameteraenderung waehrend des Laufs liess die ersten Tische mit alten Werten (80/35) bauen, der Check (Beinlage y) fand es -> Tische neu gebaut. Regel: Parameter erst aendern, dann die Kette starten, nie waehrend des Laufs.

### W18 Lochabstand pitch 200 (nft_rinne, nft_tisch) 29.10. ~22:30: Pruefer NICHT gelaufen
Grund: Wochenlimit 94 % (Regel Wochenlimit). Eigene Messungen: check_nft_rinne 93/93 (Lochzahl = floor(L/200), Teilung 200, Phase +-50, Zickzack 100), check_nft_tisch 196/196 (Lochlage gegen Rechnung, Zickzack pitch/2, Interferenz Winkelhalter 0), check_nft_fit 40/40 (586 Topfloecher >= 459, Laufwege unveraendert 600/600, Wandluft 218). Randabstand der Loecher zum Rinnenende 64 (Job), Rinnenabstand 262 > pitch/2: kollisionsfrei.
Eigene Fehler/Funde: (1) nft_rinne.py hatte die Konfigurationszeilen M/K/L_B mit 12/7/5 Loechern und +-62,5 fest eingetragen -> jetzt aus pitch gerechnet; check_nft_rinne hatte +-62,5 fest -> jetzt pitch/4 (zwei Altlasten aus pitch 250, vom Check gefunden, nicht vom Pruefer). (2) Zahlen im Netztopf-Blatt (556/2716) auf 586/2746 nachgefuehrt; D20 (466/462) ersetzt durch 586.

### W17 + W18 gemeinsamer Pruefer (Bild-Kritiker Draufsicht + Spec-Pruefer, ein Unteragent) 29.10. ~23:00: Teil B FAIL
Nachgerechnet ohne Abweichung: Radialbudget (2095/600/2695..3858/600/4458..5488/218/5706), Rinnenlaengen aller 9 Reihen, Lochzahl 15/14/13 + 9/8/7/6 + 4/3 = 586, Netztopf 2746, Zickzack kollisionsfrei (Diagonale 280, Kragen 64), Aussenbeet 800 x 2640 gegen Zehneck-Grenze.
Teil A (Bild):
| Nr | Luecke | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: Rinnen im Modell mit Luecken (132-158 mm), in ref-6 buendig | **bekannt / Owner-Entscheid** | Widerspruch OBJ (Rinnenabstand 262-288) gegen Bild; OBJ gilt (provenance); steht seit W16 als offene Frage in nft_tisch.md |
| 2 | gross, vermutet: ref-6 zeigt Staffel (Nachbarrinne in gleicher Richtung um ca. pitch/3 versetzt), Modell alternierend pitch/2 | **unklar** | Bens Definition (review-protocol: halber Topfabstand, Zickzack) gilt; an den Orchestrator: ob Ben "Zickzack" als Staffel meint |
| 3 | klein, vermutet: Tisch hoch (Z 1,4 m, Beine ca. 1250) gegen ref-6 niedriger | **andere Klasse / OBJ** | z_rinne_mitte 1300 aus layout.json hydro_tables (OBJ); Beine sind Annahme (Portalbock) |
| 4 | klein, sicher: Schlaeuche gerade, Referenz gebogen | **bekannt** | offene Frage seit W16 |
| 5 | klein: Topfdichte | **Folge von 1** | keine eigene Ursache |
| Hinweis | Draufsichtbild vor W18 gerendert (pitch 250) | **gueltig** | neu gerendert (render_radialbudget.py, pitch 200, 15/14/13) |
Teil B (Spec):
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: Laufweg A am Innenpfosten nur 486 mm (< 500), Plattenkante nur 4 mm vom exzentrischen Beckenrand; check_nft_fit rechnete nur Beckenrand bis Innenportal = 600 | **gueltig** | Check misst jetzt am Pfosten (Plattenaussenkante 2210) und die Plattenkante zum Becken: 2 neue FAIL (40/42), im Blatt offen mit Abhilfe (Innenbeete 40 mm nach aussen oder Becken zentrieren); die Entscheidung liegt beim Orchestrator/Montage (D30-Parameter) |
| 2 | gross, sicher: alte Zahlen in Blatt/JSON/Scope-Card (Fussplatte 100, y +-606/576, pitch 250, 125, 62,5, 12/7/5, 5/7/12, 2716, floor(L/250), Randabstand 46) | **gueltig** | fix_w18_blatt2.py: Ports/Fussplatten neu aus der Geometrie, Herkunftszeilen, Netztopf/Salatkopf, Scope-Card-Nachtrag W17/W18 (aeltere Zeilen bleiben als Historie, Nachtrag nennt den Stand) |
| 3 | klein/mittel: check_nft_fit teils tautologisch (Rinne <= Zehneck-Seite folgt aus der Formel; Laufwege aus Budgetparametern; NFT nur Untergrenze; Aussenkante 1,3 m gegen Strebenabstand fehlt) | **gueltig, teilweise** | Check um Pfosten/Becken, NFT >= 580 erweitert, Tautologie im Blatt benannt; Strebenabstand = Montage M7; check_walkways.py (Dom) ist die Platzierungs-Messung |
| 4 | klein: Scope-Card "Lochzahl = floor(L/pitch)" gilt fuer Reihenvarianten nicht (Mitte 9/8/7/6) | **gueltig** | Nachtrag in Scope-Card und nft_rinne-Blatt (Zustaendigkeit Lochzahl: Tisch/hole_plan) |
| 5 | klein, vermutet: Netztopf-Gesamtzahl 2746 gehoert zum Integrator, mischt alte Beete und neue Rinnen | **gueltig (andere Klasse)** | Scope-Card-Nachtrag: Gesamtzahl ist Sache des Integrators/Layouts; Blatt vermerkt das Raster als offen |
| H | check_walkways.py (Dom) zeigt A 580, B 476 FAIL, Wandluft 82 | **andere Klasse (Montage M7)** | Dom-Skript hat noch alte Beetmasse; M7 |

### Laufweg A (Pruefer-Befund 1 W17/W18) 29.10. ~23:45: behoben im kleinsten Eingriff
Eingriff: neuer Parameter `leg_clearance_innen` 30 mm (nur Innen-Pfosten; sonst leg_clearance 45): Plattenaussenkante 2195 statt 2210, Laufweg A frei am Pfosten 500 mm (Innenportal 2695,5 - 2195; D29 nie unter 500, Ziel 600 gilt am Beckenrand). Innentisch neu gebaut (check_nft_tisch 46/46 innen, 196/196 gesamt inkl. Interferenz 0), check_nft_fit 42/42. Grenzen, offen benannt: (1) Rand-Reserve null (500,5 gegen 500); (2) gilt fuer das zentrierte Becken des Budgets: mit dem OBJ-Becken (cx -36, cy 20, 41 mm exzentrisch) wuerde die Platte den Beckenrand um 11 mm beruehren — der Check meldet das als HINWEIS; M7 muss das Becken zentrieren oder die Innenbeete 40 mm nach aussen setzen (`inner_bed_shift` 66 -> 26, dann Laufweg A 540 am Pfosten). Alternativen verworfen: Fussplatte kleiner (Loecher lagen unter dem Rohr, nicht schraubbar), clearance < 30 (Plattenkontakt am Becken).

### haut_paneel (T40) + haut_profil (T41), W19 29.10. ~00:10: Pruefer NICHT gelaufen
Auftrag W19 (D35, R11) klein in vier Schritten: (1) Typen aus layout.json: 65 Streben aus Knotenabstaenden (A 3279 / B 3708, Toleranz 15 mm), 40 Dreiecke (Euler), AAB 30 + BBB 10; die Tuer (OBJ Azimut 167) sitzt auf Basisknoten 22 (Azimut 167,2) und beruehrt zwei Basisfelder (149,2 BBB und 185,2 AAB) — kein einzelnes Tuerfeld; (2) haut_paneel_AAB/BBB.sc: Dicke 8, Rand 15 mm vor der Strebenachse (Inkreis-Verkleinerung), 5 Flaechen, 38,9 / 46,3 l, 7,4 / 8,8 kg bei 0,19 g/cm3; (3) haut_profil.sc: Alu-Kappe 30 x 8, Wand 2, A 3279 (0,74 kg) / B 3708 (0,84 kg) als Konfiguration; (4) check_haut.py 27/27 PASS (Euler, Kanteninzidenz, Heron-Flaeche, Randkanten, Randabstand ueber Inkreisradius, Profil A/B) und Blaetter. Eigene Korrektur: eine erste Pruefzeile verglich einen Wert mit sich selbst (Tautologie) und wurde durch die Kanteninzidenz (3 x Felder = 2 x Streben - Randkanten) ersetzt. Kein Spec-/Bild-Kritiker (Wochenlimit 96 %).

### tuer_komplett (T50) + haut_paneel_BBB_tuer, W20 (D36, R13) 30.10.: Pruefer NICHT gelaufen (Auftrag)
Fuenf Schritte, je WIP-Commit: (1) Geometrie Feld BBB 149,2 (Knoten 24, 22, 6): Basis 3708, Hangkante 3211, Feldebene 10,8 Grad zur Senkrechten, Lichte 1016 x 2008, Zarge 1076 x 2068, Feldbreite in Sturzhoehe 1320 (Reserve 122 mm je Seite); `door` nur noch bei BBB 149,2 (haut_typen.py, DOOR_AZ 149,2); (2) Zarge Rohr 30 x 30 x 2 (Schwelle, 2 Pfosten, Sturz); (3) Blatt 1000 x 2000 x 40 (24,8 kg), Anschlag, Dichtung, 3 Aufschraubbaender, Druecker; (4) haut_paneel_BBB_tuer.sc (Ausschnitt = Zarge, 9 Flaechen, 5,4 kg); (5) check_tuer 25/25 und check_haut 27/27 PASS, Blaetter tuer_komplett/haut_paneel. Entscheidung [A]: Zarge liegt in der Feldebene (geneigt) statt senkrecht (R13: senkrechter Rahmen braeuchte Tiefe bis 603 mm).
Eigene Funde: der Check fand zwei echte Fehler im ersten Wurf (Druecker-Hals ueberlappte den Hebel 4580 mm3; Bolzen D10 stand 1 mm im Blatt) -> korrigiert; Pruefzeile "Bolzen verbindet Laschen" scheiterte an Gleitkomma (Toleranz 0,01 statt 1e-6). tuer.json heisst jetzt tuer_komplett.json (partsheet haette sonst den alten Platzhalter tuer.sc gemessen).

### W21 Pruefer fuer W19 + W20 (haut_paneel, haut_profil, tuer_komplett, haut_paneel_BBB_tuer) 30.10. ~04:30: Teil B FAIL
Alle Zahlen nachgerechnet ohne Abweichung (65 Streben, 40 Felder AAB 30/BBB 10, Flaechen, Kappe 84 mm2, Lichte 1016 x 2008, Zarge 1076 x 2068, Reserve 122 mm zur Strebenachse, Neigung 10,82 Grad). Schwaechen liegen in Schnittstellen und Pruefzeilen.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| B1 | gross, sicher: Auflage Paneel auf Kappe = 0 mm (Paneelrand 15 mm vor der Achse = Kappenkante), Blaetter behaupteten 15 mm Auflage; Pruefzeile tautologisch | **gueltig** | Blaetter korrigiert (Kappe = buendige Fugenleiste, Auflage 0, Halt nicht modelliert); neue Pruefzeile edge_inset = cap_w/2 (T41) in check_haut 28/28; Entscheid beim Orchestrator: edge_inset 0 oder Klemmleiste (R11 widerspricht sich) |
| B2 | gross: Kappenzahl 65 gegen entfallende Basisstrebe; Blatt "entfaellt" gegen "Reststrecke 1316"; Paneelkanten am Ausschnitt ohne Kappe | **gueltig (Doku), teils andere Klasse** | Klar gestellt: nur das Mittelstueck entfaellt, Reststrecken 1316 je Seite mit je einer Kappe (66 Kappen, Parameter len); Streifen neben der Zarge haengen an den Hangstreben und den Reststrecken; Dom/Montage rechnet 64/65/66 |
| B3 | klein, sicher: Dichtung neben statt auf dem Anschlag (x sx-17 statt auf Anschlag), Schwellendichtung fehlt | **gueltig (Modell)** | tuer.py: Dichtung auf dem Anschlag (x 494..500), Dichtung_Schwelle ergaenzt; check_tuer prueft Lage innerhalb des Anschlags und alle drei Anschlagseiten |
| B4 | klein: Marke E/mittel fuer die Wahl der Feldebene; "Tiefe 603" (stimmt nur an der Spitze, am Sturz 388); Spitze Z 3140/3150/3154; Pfeilhoehe 0,2 m falsch (0,34/0,40 m) | **gueltig** | Marke A/niedrig (Neigung gerechnet E, Wahl der Ebene Annahme), Zahlen korrigiert, Umrechnung absolut/relativ zu base_z -14 im Blatt |
| B5 | klein: Spiel oben/unten als Konstanten, Reserve nur zur Achse, Summenzeile Blatt, Gesamtflaeche 204 m2 mit vollem Tuerpaneel, schwelle_h-Herkunft | **gueltig** | Parameter spiel_oben 6 / spiel_unten 2 (tuer_komplett.json), Reserve zur Strebenkante >= 100 (105), Blatt-Masse in drei Zeilen, Gesamtflaeche 201,5 m2 |
| P | Pflichtfrage: cap_w/cap_h doppelt, felder/Tuerflag Eltern-Wissen, Tuerausschnitt gehoert dem Paneel | **teils uebernommen** | edge_inset gegen cap_w/2 geprueft; Zustaendigkeit Ausschnitt (T40 statt T50) als offene Frage im Blatt |
| A | Bild: Blatt in ref-4 verglast, Schloss fehlt, Render zeigt Zarge nicht | **gueltig, klein (Annahme/Darstellung)** | Blatt Sandwich bleibt Annahme A; Schloss nicht modelliert (Blatt offen) |
| H | docs/components.md, model-description.md, next-steps-workshop.md, loop-log R21, designs/components/tuer.sc mit alter Tuerlage (167, zwei Felder, Spitze 3150) | **andere Klasse** | Orchestrator/Montage nachfuehren |

### W22 Haut-Nacharbeit (Entscheidung D37) 30.10.: kein Pruefer noetig (nur Parameter)
(1) `edge_inset` 15 -> 0: Paneel bis zur Strebenachse, Kappe klemmt beide Kanten, Auflage 15 mm je Seite (Pruefzeile jetzt cap_w/2 - edge_inset = 15); Paneele neu (AAB 7,6 / BBB 9,1 / BBB_tuer 5,7 kg, Gesamtflaeche 207,7 m2 = 39 volle + Tuerpaneel 3,73 m2), check_haut 29/29, check_tuer 30/30 (Tuerausschnitt, Interferenz 0 unveraendert); Blaetter mit R11-Widerspruch als Herkunft; Schnittbild haut_profil-03 (zwei Paneele, eine Kappe). (2) Kappenzahl 66 = 30 x A + 34 x B + 2 Reststuecke je 1316 mm (check_haut: Reststrecke und 64 + 2); Strebenzahl im Dom unveraendert (Montage). (3) Doku auf D36: components.md (Z. 4, 25), model-description.md (Z. 35), next-steps-workshop.md (Z. 43), loop-log nur Hinweis; designs/components/tuer.sc nicht angefasst. (4) T40/T50: Tuerausschnitt bleibt beim Paneel (D37), im Blatt tuer_komplett eingetragen.

### W23 Spec-Pruefer W17+W18 (nft_tisch, nft_rinne) 30.10. ~07:00: FAIL
Nachgerechnet ohne Abweichung: Topfzahl 586 (8 x 42 + 6 x 30 + 10 x 7), Rinnenzahl 68, Rinnenlaengen aller 9 Reihen, Radialbudget, Laufweg A am Innenpfosten 500,5 (Behebung stimmt), Tischmasse, Gefaelle, Zickzack kollisionsfrei, Winkelhalter 76, Aussenbeet 2851,7.
| Nr | Befund | Einstufung | Beleg / Folge |
|---|---|---|---|
| 1 | gross, sicher: check_nft_fit lief nicht (KeyError inner_bed_shift: D37 zweite hat die Parameter entfernt), Zahlen 40/40, "95 mm", "Beine 32/37" nicht reproduzierbar | **gueltig** | check_nft_fit auf D37 (Beete exakt auf der Sektorachse aus ap_c, Becken zentriert D35, kein shift): Footprint nominal 114 (die 95 waren Streuartefakt der OBJ-Beete), Beine-Beet 45; Schwellen auf 112 bzw. 40 gesetzt |
| 2 | gross: Tischkanten in 1,3 m Hoehe nie gegen die Kuppelhaut gemessen (D25/D29 "5370..5550" ohne Herleitung) | **gueltig, echter Befund (offen)** | neuer Check (Feldebenen der 40 Dreiecke aus haut_paneel.json/layout.json, Strebenachsen, >= 15 mm): Aussentisch -87 mm (Rinnenenden der aeussersten Reihe, Sektor 6; in BBB-Sektoren Holm-Aussenseite +-0, in AAB +79), mitte +1493, innen +3303 -> FAIL (44/45). Abhilfe braucht Entscheidung (Orchestrator/Montage), siehe Fertigmeldung |
| 3 | klein: Blatt/JSON verschmutzt: Herkunftszeile 5-fach (Fix-Skript haengte nicht idempotent an), Phase 125, ap_c 5209/3343 in den Typzeilen, Beetbreite 933-993, "M7 muss Becken zentrieren / inner_bed_shift", outer/inner_bed_shift, Hinweis im Check | **gueltig** | blatt6: Zeile idempotent + Dedupe, Typzeilen aus der Geometrie, D37-/D35-Texte; blatt2: Phase = pitch/2, Beetbreite, leg_clearance_innen-Herkunft; Hinweiszeile im Check entfernt |
| 4 | klein: nft_rinne-Blatt: Stueckliste/Herkunft 1304/1983/3232, Gefaelle 1 cm/m, Rinnen 2/4/2-3, Eckengehrung 1304; Zickzack-Marke "Bild/hoch" gegen Log (ref-6 evtl. pitch/3) | **gueltig** | nft_rinne-Blatt: Tischreihen 758-3051 (Master nur Vorlage), 1,5 %, 2/4/3, Gehrung durch Reihenlaengen geloest; Zickzack-/Lochraster-Marke "Ben (D35)", Konfidenz mittel |
| 5 | klein: Pruefzeilen locker/tautologisch (Footprint 60 gegen 114, Lochlage 1,5 gegen 1,4-1,5 systematisch, hole_d-Literal, Rinne <= Zehneck folgt aus der Formel); Konstanten E_IN/E_OUT/margin im Tisch; Docstring 46 gegen 64 | **gueltig, teils uebernommen** | Footprint- und Beine-Schwellen angeglichen (112 / 40); Docstring margin 64; Rest bleibt als bekannte Schwaeche im Blatt (Lochlage-Toleranz auf Gefaelle kalibriert, hole_d-Literal und Konstanten E_IN/E_OUT/margin nicht parametrisiert) |
| H | Layout/Montage: ap_c/Sektoren/Laufwege sind Layout-Wissen; Montage-Lauf zeigte A 568 B 573 Wandluft 149 (vor D37); R15 offene Ben-Fragen (Innenring 6/10, Aussenrinnen 2/3: 28 Toepfe); decisions.md fuehrt D37 doppelt; Netztopf 2746 mischt altes Raster; Randabstand 64 gehoert zu Rinne/Kragen; Winkelhalter-Check in check_nft_tisch; Beet-Laenge 2640 begruendet mit ueberholtem D25 | **andere Klasse** | Hinweise an Orchestrator/Montage in der Fertigmeldung |

### Tische nach innen (Ben 30.10.; W23-Befund 2 behoben) ~08:30
Auftrag Ben "Tische nach innen": `ap_c` aussen 4973 -> 4874 (99 mm; Beete folgen ap_c nach D37). Rechnung (Sweep 95-120 mm): Abstand der Rinnenenden zur Kuppelhaut (Feldebenen der Strebenachsen, Oberkante Rinne = Boden + 100) 21 mm statt -87 (Soll >= 15 = halbes Strebenrohr); Laufweg B = 4359 - 3858,5 = 500,5 mm (harte Untergrenze D29: 500; 100 mm Verschiebung ergaebe 499,5, 103 mm fuer 15 mm Haut-Abstand ergaebe 497: deshalb 99); Wandluft 317; Aussenreihen 2986 / 2799 / 2612 mm (vorher 3051 / 2864 / 2676), Loecher 14/13/13 statt 15/14/13, Topfzahl gesamt 570 statt 586 (D33 ca. 580 -> Schwelle 563 = -3 %). Konflikt benannt: Laufweg B hat damit KEINE Reserve (0,5 mm) und liegt 100 mm unter dem Ziel 600; wer 600 will, muss Mittelportal oder Beete schmaler machen. Messmarge: die Pruefpunkte nutzen jetzt die wahre Rinnenoberkante (Boden + 100) statt +130; bei +130 waeren es 15,5 mm bei 103 mm Verschiebung. check_nft_fit 45/45, check_nft_tisch 196/196 (Interferenz 0), Rinnenvarianten aussen_r1..r3 und nft_tisch_aussen.sc neu; Mitte/Innen unveraendert. Skripte: fix_w25_aussen_innen.py, fix_w25_blatt.py. Kein Pruefer-Lauf (Auftrag/Limit).

### W24 Aussentisch 4 Rinnen (Variante aussen4) 30.10. ~09:10: kein Pruefer (nur Parameter/Tabellen)
Variante `aussen4` in nft_tisch.json (n 4, Abstand 220, reihen_versatz +42, ap_c 4874), tisch_geom.geometry kennt `reihen_versatz`, check_nft_fit rechnet beide Varianten (Standard 47/47, aussen4 48/48 PASS; neue Pruefzeile Rinnenkante gegen Beininnenflaeche >= 15). Symmetrisch 220-240 kollidiert mit der Kuppelhaut (-20..-50 mm), Ap_c nach innen sprengt Laufweg B (476,5); daher aeusserste Reihe wie Standard (Ap 5162), Gruppe 42 mm nach innen, Luft Rinne-Bein 23 mm (Abstand 230 stiesse ans Bein). Topfzahl 674 statt 570 (+104), Rinnen 76, Rinnenlaenge Aussenring 88 712 statt 67 176 mm, Laufweg B 500,5 und Wandluft 317 unveraendert, Erreichbarkeit entfernteste Reihe 803 wie Standard. Statik nur Abschaetzung (A). NICHT gebaut: nft_tisch.py/check_nft_tisch kennen ymid nicht. Bericht docs/packages/W24-aussentisch-4-rinnen.md, Bild renders/components/nft_passung/aussen4-querschnitt.png.

### W25a/W26/W25 Spec-Pruefer (ein gemeinsamer Lauf, Sonnet-Unteragent, 31.10.): kein grosser Rechenfehler, Bestand und Blaetter nachgezogen
Nachgerechnet ohne Abweichung: Reihen-Apothem 5162/4942/4722/4502, Rinnenlaengen 2986/2844/2701/2558, Loecher 14/14/13/12 = 53, 674 gesamt, 76 Rinnen, 2834 Netztoepfe, Kuppelhaut-Abstand 21,4 mm, Laufweg B 500,5, Wandluft 317, Rinnenkante/Bein 23 mm, nft_pots 7/30/53, Beet-Beet 37,4 mm exakt (SAT-Untergrenze 35,6), Medium 469,74 l, crect-Geometrie, Pumpenzahlen 220-240 / 110-120 je Linie / 1,46-1,72 l/min je Rinne.
| Nr | Befund | Einstufung | Folge |
|---|---|---|---|
| 1c | gross, sicher: Ports/Stueckliste des Aussentisches noch im 3-Reihen-Stand (Verteiler 869, Laengsstreben 2072, Fussplatten x -1011/1101, Zulauf y 413, n=3) | **gueltig** | fix_w25a_blatt2.py: 957 / 2018 / -984, 1074 / y 497, x -1349, n=4, Stutzen x -1547..-1333 (aus tisch_geom/nft_tisch.py; gegen die gebaute .sc: Laengs 2018, Fussplatten -984/1074) |
| 1d | klein: Herkunft aussen widerspricht sich (Standard / Standard bleibt 3 Rinnen) | **gueltig** | Text auf D43/aussen3 |
| 1e | klein: alte Zahlen als aktuelle Aussage (570/2730, 2/4/3, Abstand 288, 2612-2986) in netztopf, nft_tisch, nft_rinne, salatkopf | **gueltig** | alle Stellen per Skript; historische Zeilen bleiben |
| 1b | Geschmack: 53 gilt wegen n <= floor(L/pitch) (D32), geometrisch waeren 54 | kein Befund | Regel D32 |
| 2b | gross, sicher (Modellfehler): Zulauf-Tropfrohr von innen_933 bei y -392,5 in der Fasenzone, Bohrung 55 mm ausserhalb der schraegen Wand, check_ibc_beet blind | **gueltig** | y_in bei Fase vor den Fasenbeginn (-298), neue Pruefzeile Tropfrohr vor der Fase, Beet neu gebaut |
| 2c | Geschmack: Fase 60 genuegt knapp | kein Befund | 120 bleibt (D44) |
| 3b | klein: Pumpenblatt fuehrt 12/30 l/min in der Herkunft weiter | **gueltig** | Zeile ersetzt |
| 3c | klein: 12-13 l/min je Pumpe gegen je Tank (2 Pumpen je Tank, Faktor 2) | **gueltig** | je Tank 12-13, Aufteilung offen |
| 3d/3e | klein/Geschmack: nft_tisch rechnet 0,5 l/min je Rinne; Pflanzenstrom = Beete + NFT; ENTSCHEIDUNG vs vorlaeufig | **teils uebernommen** | Hinweise im Blatt (offen), "vorlaeufig", NFT-Strom |

### W28 Puffer-Station (D46) 31.10.
puffer_ibc (T80): Standard-IBC 1200 x 1000 x 1165 mit Palette 150, Gitterkaefig (Rahmen 25 x 25, 50 Staebe D8), PE-Blase 2,5 mm, Hals DN150, Ablauf DN50 mit Kugelhahn unten, Zulauf/Ueberlauf DN50 seitlich oben (Dachstutzen nur <= 1190, sonst passt der Stapel nicht unter 2,5 m), Belueftung d32, Sensorstutzen; Wasserkoerper 900 l. puffer_station (T81): 2 IBC auf Stapelrahmen 60 x 60 x 3 (Laengstraeger unter den Kufen, Oberkante 1255), Stapelhoehe 2445 (<= 2500), Verbindungsrohr DN50 (Platzhalter), Messplatz (4 Sonden, Becher, Kabelkanal), Dosierkonsole (2 Schlauchpumpen, 2 Kanister 20 l), Plattform z 1506 mit Leiter, Gelaender 900. check_puffer ibc 17/17, station 27/27 (Interferenz 0 beide). Gelernt: eingefuegte Komponenten verlieren das Material (Standarddichte 1,29): in der Station per assign_part_materials nachziehen; Palette als Vollkoerper mit Ersatzdichte 0,2.

### W29 Menschenfigur 1,80 m (D47) 31.10.: Selbstcheck, kein Pruefer
mensch_referenz T90 mit Konfigurationen aufrecht (Hoehe 1800, Schulterbreite 466), messen (Lean 10 Grad, rechte Hand Brusthoehe 1242, linke Hand Messgeraet) und arbeiten (Lean 20 Grad, beide Haende 1242); Proportionen Drillis/Contini als Anteile H, Arme per Zwei-Knochen-IK, 55-61 Flaechen, 14-15 Koerper je Figur. Beim Check gefunden und behoben: Oberarmlaenge (Ellbogen lag 40 mm zu tief, l1 = Schultergelenk - Ellbogenhoehe), Scheitelhoehe-Pruefung bei 10 Grad Neigung, eigene Tautologie in der Kopf-Pruefzeile (ersetzt durch Scheitel 1800 und Kugel D190); Masse mit Ersatzdichte 0,87 auf ca. 80 kg. Offen: Querschnitte/Posen Annahme A, Platzierung M9.

### W30 Tank-Staende verkleinern (D50) 31.10.: Selbstcheck, kein Pruefer
Plattform = 2 x (Konusradius auf Plattform-Unterkante + 2 Spiel + 60): klein 619 (Konus 247,3), gross 821 (348,7); das Jobblatt nannte ca. 632 / 810 aus einer 45-Grad-Naeherung (r = Z - Spitze), gerechnet ist mit dem gebauten Kegel (48,7 / 47,0 Grad). Beine, Querstreben, Diagonalen, Fussplatten folgen der Plattform; Rippenradius 440 -> 367 (Innenkante der Querstreben minus 3). Tank, Z und Dicke der Plattform unveraendert. check_tank 114/114 (neu: Plattform aus Konusradius, kleiner als OBJ, Beine ausserhalb des Wulstes, Tafel <= Plattform, Rippenradius gegen Strebe). Gefunden: Pumpentafeln (Tank 1: Rand 327 gegen Plattformhalbbreite 310, Tank 3: 486 gegen 410) passen nicht mehr unter die Plattform -> Montage setzt sie seitlich. Konstruktiv: der Tankzylinder ueberragt die Plattform; der Kegel sitzt im Kegelsitz (Kontaktring ca. 60 mm), Tragfaehigkeit/Haltegurt nicht nachgewiesen.

### W31 Feinfilter T55 (D51) 31.10.: Selbstcheck, kein Pruefer
Behaelter PP 400 x 300 x 500 (Wand 5, Blatt-Mass), Siebkorb Edelstahl 340 x 240 x 330 auf Auflageleisten (3 mm Spalt), Deckel mit EPDM-Dichtung und 4 Spannverschluessen, Standrahmen 250 hoch (Eimer unter dem Ablass), Einlauf d50 mit Winkel in den Korb, Auslauf d50 unter dem Korbboden, Ablass d40 mit Kugelhahn. Netzliste gegen Blatt: das Blatt nennt 'DN 50', die Netzliste meint mit dn 50 den Aussendurchmesser d50 (DN40): Netzliste gilt, im Blatt vermerkt. Der erste Bau brach ab (Bohrung des Einlauf-Winkels schnitt die Gegenwand durch: 'implausible result volume'), Bohrlaenge korrigiert. Check zuerst 38/41: drei Fehler waren meine Erwartungen (Inhalt 55,98 l statt 49,7, Korb-Summe 910, Gesamthoehe 793), nachgerechnet und korrigiert, zwei Tautologie-Zeilen durch Messungen ersetzt; check_feinfilter 42/42, Interferenz 0. Offen: Hoehe gegen den Absetzer-Auslass (M10), kein Notueberlauf, Gewebe/Verschluesse/Hahn als Ersatzformen.

### W27 Huelle Plane (D39, R24) 31.10.: Selbstcheck, kein Pruefer
keilschiene T43: Alu-Kanal 25 x 15 mit Lippen, Federdraht D2 (eigener Koerper), Schaumband; A 3019 / B 3448 = Knotenabstand minus 2 x 130, Summe 211,3 m gegen R24 228 m (-7 %, Knotenfreiraum). huelle_folie T42: je Dreiecksform eine Datei (Skizzen nehmen nur Zahlen), 2 Lagen 0,15 im Abstand 100, Ueberstand 100 je Seite (Parameter overlap 200), Lage 1 bei Z 64 ueber der Keilschiene; netto 207,7 m2 gegen R24 208 (+-3 %), mit Ueberstand 251,8 m2 je Lage, 69,5 kg. tuer_zarge_planenausschnitt T44: Aufsatzrahmen, Dichtband, Klemmleiste im Feld-KS der Tuer; das gemeinsame Tuerfeld (Zarge + Tuerblatt + Rahmen + Folie, insert_design + occurrence.move) ergab beim ersten Lauf 3 Interferenzen mit den Scharnier-Zargenlaschen (je 1080 mm3): Ausklinkungen im Steg, Lage aus tuer_komplett.sc gemessen. check_huelle 68/68 (21 + 31 + 16). Offen: Montage platziert, Luftpolster nur als Parallelebenen, Schrauben nicht modelliert, Tuer-Schwenkbereich ueber dem Rahmen nicht geprueft.

### W32 Biofilter-Schwebebett und Feinfilter im Hauptstrom (R30, D55) 31.10.: Selbstcheck, kein Pruefer
Feinfilter: Der Bestand W31 war fuer 12,5 l/min gebaut. Neu rechnet feinfilter.py die Siebflaeche aus Q / Siebbelastung (110 l/min = 6,6 m3/h, 8 m/h = 0,825 m2) und leitet Korb 560 x 370 x 400 (0,84 m2), Behaelter 630 x 440 x 610 (Wand 10), Hoehen und Ports d63 ab und schreibt sie in feinfilter.json zurueck; neu Spuelanschluss d25 mit Spritzrohr. Die Siebbelastung ist Annahme: R30 nennt keine belegte Auslegungsgroesse (Bestand 1,6 m/h haette 4,1 m2 verlangt). Blatt W32 'Ports DN 63' gelesen als d63 (wie in W31 'DN 50' = d50). Der Check fand einen Rechenfehler im Stegraster des Standrahmens (Abstand der Endring-MITTEN, nicht der Innenkanten: 118 statt 150 mm Raster). Parallel laufender Check las die alte Datei (Bau und Check nie gleichzeitig).
Tank: tank_gross und tank_gross_t3 mit Schwebebett statt Korb: ein Koerper 470 l (0,67 x 702 l, Z 489..1353, 3 mm Spalt), Belueftungsgitter D20 (Ring + 2 Arme, Arme D18 wegen Boolean-Tangentialfehler) am Konus, Steigrohr D16, Zulaufsieb (Schlitzkappe) und Auslaufsieb (Kappe D110); Tragrost und Konsolen entfallen. check_tank 154/154 mit neuem check_bed. Gegenprobe gegen den Stand vor W32: Interferenz Tank/Schlammstutzen (857,8 mm3) war schon da (gewollter Sitz, aus dem Check genommen), die frueheren Interferenzen Konsolen und Zulaufrohr/Korb entfallen. BEFUND: Das Tankprofil fasst 687 l bis zum Rand und 628 l bis zum Ueberlauf-Mittelpunkt, nicht 702 l: das Bett fuellt 68 % bzw. 75 % des Modellwassers (K1 meist <= 67-70 %): Ueberlauf tiefer oder Fuellung 421 l, offen (Orchestrator/Ben). Offen sonst: Netzliste noch d50/12,5 l/min, Notueberlauf am Feinfilter, K1-Datenblatt. fix_tank_blatt.py kennt das Schwebebett nicht und ist als nicht auszufuehren vermerkt.
