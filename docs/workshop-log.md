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
