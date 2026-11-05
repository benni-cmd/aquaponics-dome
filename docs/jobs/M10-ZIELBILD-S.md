# M10-ZIELBILD-S: Montage-Kette ab M10-S3 auf Zielbild S mit eingelassenem Pool umplanen (D88)

Planer 05.11.2026 (Opus 5.5), nach `docs/jobs/vorlagen/planung.md`. Nur gelesen. Ausnahme: das reine Rechenskript `scripts/m10_zielbild_s_rechnung.py`, das jede [E]-Zahl dieses Blatts nachrechenbar macht (Abschnittsnummer in Klammern). Paket: `docs/packages/m10-zielbild-s.md`. Ersetzt die Blaetter `docs/jobs/M10-S3.md` bis `M10-S7.md` (A+) und schliesst `M10-S2V` (Subtank). [Q] Quelle im Repo · [E] eigene Rechnung · [A] Annahme. Z relativ zum Flur, absolut = relativ + 400.

**Problem:** Die Kette M10-S3 bis S7 plant A+ weiter: Heber, Feinfilter in Gruben, Absetzerkreis, Notbypass mit Schaechten, Beet-Suempfe mit Pumpen. Ben hat mit D88 Zielbild S beschlossen: Der Pool wird der tiefste Punkt, gleich gross und 665 mm tiefer eingelassen; es gibt nur noch eine Pumpstufe. Die Blaetter passen nicht mehr, und im Modell stehen 56,3 m Leitung, die entfallen.
**Intent:** Das Modell zeigt die Anlage, die gebaut werden soll: Wasser wird einmal gehoben und fliesst dann frei in den Pool zurueck; wenig Graben, wenig Teile, Technik innen, alles nach Leitungsordnung v2 und den Designprinzipien.
**Ziel (ein Satz):** Nach den Schritten M10-Z1 bis Z7 enthaelt `designs/dome.sc` den Pool nach D88 mit Aufkantung und Gelaender, Beete auf dem Flur, 4 Tauchpumpen im Pool mit Druckschlauch zum Siebkorb, je Linie eine Wasserstation, alle Ruecklaeufe als freie Schwerkraft-Leitungen in den Pool und den Schlamm draussen, und die Pruefpunkte in Abschnitt 6 sind gruen.

## Aktualitaetspruefung (W44), 05.11.2026
Ergebnis: **angepasst** (Plan gilt als freigegeben; Abweichungen von R57 stehen mit Grund in Abschnitt 2).
1. D88 (Zielbild S, Pool gleich gross und eingelassen, Gelaender, Absetzer streichen als Annahme) und D89 (schwere Laeufe nur unter 3 GB RAM warten) gelesen. D85 (lebensmittelecht), D86 (Ordnung v2) und D87 (Schrank-Kasten innen) gelten.
2. Leitungsordnung v2 ist gepusht (f17f6d1, KW-Korridor nach D88 in 5a3da4d). Dieses Blatt plant nur nach v2.
3. Designprinzipien `docs/designprinzipien.md` sind Pflicht-Check (01ffd54), siehe Abschnitt 7.
4. Roadmap: M10-S3 bis S7 stehen noch auf A+ (geplant, teils "GESTOPPT bis E20"). Der Orchestrator ersetzt sie durch M10-Z1 bis Z7 und schliesst M10-S2V.
5. Laufend und betroffen: (a) N-AUTOBAHN-V2 R1 ist gebaut (404e499). Ring B2 erbt den gemeinsamen Bestand, also auch Pool, Beete und Pumpen aus Z1/Z2; (b) N-TECHNIK-INNEN legt Luft und Frischwasser neu (9 Kanten); (c) M10-S2N hat Schaechte, Revisionsstutzen und Spuelanschluesse gebaut, die mit Z1 wieder entfallen.
6. Netzliste ist Version 3 (57 Kanten). Netz v4 legt der Orchestrator an (Abschnitt 5).

## 1. Was im Modell steht und was entfaellt (gemessen)
Befehl: `python -X utf8 scripts/m10_zielbild_s_rechnung.py`.
1. **Rueckbau Wasser (1):** 63 Trassen mit 56,3 m, davon 45,3 m unter Flur. Das sind Heber K01/K17, Filter-Stamm K02/K06/K18/K22, Absetzerkreis K03 bis K05 und K19 bis K21, Schlamm K07/K23, Notbypass K56/K57, Revisionsstrecken REV1/REV2, Spuelanschluesse SP/KSP, Bodenablauf-Kappen KB. Dazu 20 von 29 Zusatzteilen (Schacht, Federhaehne, Revisionskappen, Schlammfaesser) und 3 Gruben.
2. **Bauteile, die entfallen:** 2 Feinfilter-Kaesten mit Gruben, 2 Absetzer (`Tank_klein`), 4 Kleinpumpen (`Pumpe_klein`), 2 Schlammfaesser in Gruben, die Poolwand-Stutzen `T5_Stutzen_SA_*` und `BA_Mitte`. Die Beet-Suempfe (W37-1) sind nur als Bauteil vorhanden, nicht gesetzt; sie werden nicht eingebaut.
3. **Umbau statt Rueckbau:** Pumpe -> Biofilter (K08/K09/K24/K25, 6 Trassen, 8,5 m) wird Druckschlauch Art B. Luft und Frischwasser (17 Trassen, 129,3 m, davon 105,9 m unter Flur) werden Schlauch ueber Flur (R57 G18/G19).
4. **Pool (2):** heute Spiegel Z 515, Rand Z 650, Innenboden Z -1705, Wassertiefe 2220 mm. Neu Spiegel Z -150, Rand Z 0 mit Aufkantung bis Z 150, Innenboden Z -2370. Wasser bleibt 26,4 m3. In den Daten: `data/layout.json` `pool.water_z` 515 -> -150, `data/params.json` `pool_rim` 650 -> 150; `pool_depth` bleibt 2340 (Spiegel bis Unterkante Bodenplatte). Das Zweitbecken behaelt Spiegel Z 515, sein Ueberlauf faellt jetzt 665 mm.
5. **Beete (3):** 14 Beete stehen heute mit Unterkante Z -209 bis -162 eingelassen. Neu stehen sie auf dem Flur (Z 0), also 162 bis 209 mm hoeher; die Taschen `T9_Tasche_*` im Erdkoerper entfallen. Folge laut R57 G11: Ablauf Z +62, Beetrand Z 637, Kopffreiheit ueber den Aussenbeeten 1181 mm.

## 2. Fachliche Festlegungen (mit Abweichungen von R57)

### 2.1 Gelaender: nur auf der Aufkantung, hoechstens 750 mm hoch
Die Innentische stehen mit der Fussplatte 30 mm neben dem Poolrand, ihr Kragarm reicht ueber das Wasser [Q `docs/parts/nft_tisch.md` leg_clearance_innen] (4). Neben dem Pool ist also kein Platz fuer Pfosten. Das Gelaender sitzt deshalb **auf der Aufkantung** (Wandkrone 150 mm breit). Unter dem Kragarm ist Platz bis Z 940; mit 40 mm Luft bleiben **hoechstens 750 mm Gelaender ueber der Aufkantung**, Oberkante Z 900 (4).
**OFFEN (Ben, nach Recherche):** Uebliche Absturz-Gelaender sind etwa 1000 mm hoch; ob fuer "nicht hineinfallen" an einem Becken weniger reicht, ist nicht recherchiert. Zwei Wege: (a) 750 mm reichen, weil die 10 Innentische mit ihren Rinnen den Rand zusaetzlich abschirmen; (b) 1000 mm in den Luecken zwischen den Tischen, 750 mm unter den Kragarmen. Bis zur Antwort baut die Werkstatt (a) mit Hoehe als Parameter.

### 2.2 Wasserstation je Linie: Haehne je Strang, nicht je Abnehmer (Abweichung von R57 2a)
R57 2a sieht an der Station einen Hahn je Abnehmer vor: 19 je Linie plus Ueberlauf und Messkreis. Jeder Hahn hat dann eine eigene Leitung zu seinem Abnehmer. Gemessen braucht dieser Stern **123 m (Linie 1) und 127 m (Linie 2)**, ein Strang mit T je Abnehmer nur **31 und 29 m** (Faktor 4,0 bis 4,4) (6). Das widerspricht Prinzip 3 (wenig Teile, guenstig).
Festlegung [A]: Die Station traegt je Linie **einen beschrifteten Hahn je Strang**: Beete Aussenzone, Beete Mittelzone, NFT innen, NFT Mitte, NFT aussen, Ueberlauf, Messkreis (7 Haehne). Am Abnehmer bleibt ein kleiner Regelhahn (wie M10-S3: T d40, Reduzierung, Kugelhahn d20 je Beet). Damit gilt W82 sinngemaess: ein Ort je Linie, an dem jeder Strang abgesperrt wird. **OFFEN (Ben):** Wer jeden Abnehmer an der Station haben will, waehlt den Stern mit etwa 100 m mehr Leitung je Linie.

### 2.3 Beet-Ruecklauf: frei auf dem Flur, Einmuendung durch die Wand ueber dem Ruhepegel
Der Beetablauf liegt bei Z +62, die Aufkantung bei +150: Ueber den Rand kann Beetwasser nicht frei fliessen. Es muendet deshalb **durch die Poolwand bei Z -60**, also unter dem Flur und 90 mm ueber dem Ruhepegel (Art C mit `grund: pool_einmuendung`, R13). Das Gefaelle reicht: Der laengste Weg vom Aussenbeet ist etwa 5,4 m, braucht bei 1 % 54 mm, verfuegbar sind 122 mm (5). Bei Stromausfall steigt der Pegel auf Z -39 (R57 Nachtrag D88), die Einmuendung liegt dann unter Wasser: **Belueftungsloch als Siphonbrecher ist Pflicht** (`docs/hydraulics.md` Abschn. 2.9). Je Linie eine Sammel-Einmuendung, also 2 Wanddurchfuehrungen ueber dem Wasser statt heute 3 unter Wasser (Heber 2, Bodenablauf 1).

### 2.4 Ueberall sonst Zielbild S wie R57
1. **Hauptkreislauf:** je Linie 2 Tauchpumpen am Poolboden mit Ansaugkorb und Seil (Zug von oben ohne Werkzeug), Druckschlauch Art B ueber die Aufkantung frei fallend in den Siebkorb 100 µm oben im Biofilter. Kein Rueckschlagventil (Ordnung v2, Abschnitt Siphon Punkt 2). Foerderhoehe 2,28 m, 328 W fuer alle 4 Pumpen [Q R57, `python -X utf8 scripts/r57_rechnung.py pumpen`].
2. **Bedingung 1 (D88):** 2 Pool-Pegelschalter (tief schaltet die Pumpen ab, hoch meldet) und 1 Durchflusswaechter je Linie; Ablassmodus per Schluesselschalter fuer den Ablasshahn an der Station (R57 W86).
3. **Bedingung 2 (D88):** Siebkorb ist von oben ziehbar; der Platz fuer einen Vortex vor dem Sieb bleibt am Biofilter frei (nur Freiraum im Modell, kein Teil).
4. **NFT-Ruecklauf:** Sektorsammler am Tischbein (KT), Halbring auf der Aufkantung (KW), freier Fall 0,30 bis 0,35 m in den Pool.
5. **Schlamm:** Spuelwanne des Siebkorbs und Kegelboden-Hahn des Biofilters -> Schlauch Art C -> Durchfuehrung im Fundamentring -> Fass 220 l draussen ueber dem Boden (Ausnahme 6 der Ordnung v2).
6. **Gangquerungen:** nur als Art F (Kanal mit Rost oder Leerrohr DN100 mit Zugang), Summe unter Flur hoechstens 25 m (R13).
7. **Luft im Pool:** Die Scheiben-Ausstroemer folgen dem Boden 665 mm tiefer; die Luftleitung bleibt im Becken ein Schlauch an der Innenwand (KB).

## 3. Werkstatt vor der Montage (zwei Sitzungen parallel, Dateien getrennt)
Vorhanden und wiederverwendet: Schlauch-Pfad mit Biegeradius aus N-AUTOBAHN WA-S (`scripts/workshop/autobahn_s.py`, R14), `bodenrinne_rost` (WA9), `schwimmerventil_pool`, `lt_kugelhahn_*`, `lt_schlauchschelle_*`, `tank_gross` (Biofilter).

| Teil | Sitzung | Inhalt | Pruefung im Check |
|---|---|---|---|
| ZW1 `pool_aufkantung` + `pool_gelaender` | ZW-A Becken | Aufkantung 150 mm auf der Wandkrone; Gelaender auf der Aufkantung, Hoehe Parameter (Standard 750), Pfosten nur auf der Krone | Interferenz 0 mit allen 10 Innentischen (Kragarm, Rinnen, Fussplatten); Oberkante <= Z 900 |
| ZW2 `pool_einmuendung` | ZW-A | Wanddurchfuehrung d50 bei Z -60 mit Belueftungsloch und Tuelle | Unterkante Rohr > Ruhepegel -150; Belueftung ueber Z -39 + 50 |
| ZW3 `pegelschalter_pool`, Halter Durchflusswaechter | ZW-A | Pegel tief und hoch an der Innenwand, Kabelweg ueber die Aufkantung | Schaltpunkte als Parameter; tief >= 2 m Ueberdeckung der Pumpe (R57 K2) |
| ZW4 `tauchpumpe` mit Ansaugkorb und Seil | ZW-B Wasserweg | Huelle nach Pumpenwahl (Recherche ZR1), bis dahin Masse der Eheim 3400 als Platzhalter [A] | Stand auf Innenboden Z -2370; Port Druckseite |
| ZW5 `siebkorb_biofilter` + Spuelwanne + Kegelboden-Hahn | ZW-B | Korb 100 µm im Deckel Ø 930 [A, R57 Abschn. 8 Punkt 3], Einlauf offen, Spuelwanne mit Schlauchabgang | Korb passt in den Deckel; Ports Druckschlauch und Schlamm |
| ZW6 `wasserstation_hahntafel` | ZW-B | Hahntafel am Biofilter, 7 Haehne je Linie nach 2.2, Schilder, Ablasshahn | Ports je Strang; Bedienhoehe 800 bis 1400; Bedienzone 650 mm frei (D70) |
| ZW7 `schlamm_durchfuehrung` + `schlammfass_aussen` | ZW-B | Durchfuehrung im Fundamentring, Fass 220 l lebensmittelecht auf Sockel draussen | Gefaelle >= 1 % moeglich; Fass ausserhalb der Huelle |
| ZW8 Schlauch-Bibliothek | ZW-B | Schlauch-Pfad aus `autobahn_s.py` als allgemeine Funktion `scripts/workshop/schlauch.py`; Tuellen d40/d50 lebensmittelecht | Funktion erzeugt dieselbe Geometrie wie WA-S fuer dessen Testfaelle |
| ZW9 Kanal-Querung | ZW-B | `bodenrinne_rost` Rev. B: tief genug fuer d50 mit Gefaelle (WA-S-Befund "Handelsrinne zu flach") | Rost buendig; Rinnenboden Gefaelle >= 1 % |

Recherche vor ZW4 und ZW1 (Fachrecherche, eine Sitzung): **ZR1** Tauchpumpe 55 l/min bei 2,3 m, lebensmittelecht, in Europa bestellbar, mit Kennlinie (R57 Folge 4); **ZR2** Gelaenderhoehe an Becken und Wasserflaechen (zwei Quellen).

## 4. Montage-Kette (ersetzt M10-S3 bis S7)
Nur EINE Sitzung baut das Gesamtmodell (D80). Jeder Schritt baut `sh scripts/build.sh 5 <runde>` und danach `... ring_b2`, weil Ring B2 den Bestand erbt; beide Bauten muessen Exit 0 haben. Teile, die nur A+ hatte (Verteiler VT1/VT2), bleiben mit `varianten: ["a_plus"]` die Wasserstation dieser Variante.

| Schritt | ersetzt | Inhalt | nach |
|---|---|---|---|
| **M10-Z1** Rueckbau, Becken, Beete | S2N-Teile, S2V | Rueckbau nach Abschnitt 1 Punkt 1 und 2 (Trassen, Teile, Gruben, Stutzen, Kaesten); Pool-Daten nach Punkt 4; Aufkantung, Gelaender, Einmuendungen; Beete auf den Flur, Taschen weg; Luft-Ausstroemer auf den neuen Boden | ZW-A |
| **M10-Z2** Hauptkreislauf | S2-Teile | 4 Tauchpumpen, Druckschlaeuche Art B (K08/K09/K24/K25) ueber die Aufkantung zum Siebkorb; Siebkorb, Spuelwanne; Pegelschalter, Durchflusswaechter | Z1, ZW-B, ZR1 |
| **M10-Z3** Wasserstation und Verteilung | S3 | Hahntafel je Linie; Straenge Beete (Art A an den Beetfuessen, KF) und NFT (Art A, KT) mit Regelhahn je Abnehmer; Ueberlauf K13/K29 Art C in den Pool; Messkreis K35; Gangquerungen Art F | Z2 |
| **M10-Z4** Ruecklaeufe | S4 | Beet-Ruecklauf Art C auf dem Flur zur Einmuendung; NFT-Sektorsammler und Halbring auf der Aufkantung; Zweitbecken K33/K34; Messzelle K37 | Z3 |
| **M10-Z5** Schlamm und Rest | S5 | Schlamm Art C nach draussen zum Fass; Dosierleitungen K38, K53 bis K55; Drittbecken K42/K43 | Z4 |
| **M10-Z6** Kabel und Alarm | S6 | Kabel nur ueber Flur oder in den Querungen (Art F); Pegel-tief-Abschaltung und Ablassmodus im Schaltplan; Durchflusswaechter mit Alarm | Z5, N-TECHNIK-INNEN |
| **M10-Z7** Abschluss | S7 | alle Pruefskripte beider Varianten, Prinzipien-Check, Bilanz unter Flur, Stueckliste, Bilder, `docs/model-description.md` | Z6 |

**Luft und Frischwasser** legt N-TECHNIK-INNEN neu. Es verlegt sie gleich als Schlauch nach Ordnung v2 (Art D/B) und raeumt die 105,9 m im Graben mit ab. Laeuft N-TECHNIK-INNEN nicht vor Z5, uebernimmt Z5 diesen Teil.
**Reihenfolge zur Autobahn (Empfehlung an den Orchestrator):** N-AUTOBAHN-V2 haelt nach R1 an; Z1 laeuft; danach R2 auf dem neuen Bestand. Grund: Z1 hebt die Beete um 162 bis 209 mm, und die 38 Fallschlaeuche von R2 messen bis zum Beet; vor Z1 gebaut wuerden sie danach falsch lang.

## 5. Netz v4 (Vorschlag an den Orchestrator, er besitzt `data/leitungsnetz.json`)
1. Kanten streichen: K01 bis K07, K17 bis K23, K47, K48, K56 bis K59.
2. Knoten streichen: `feinfilter_1/2`, `absetzer_1/2`, `pumpe_klein_1..4`, `beet_sumpf_1/2`; `schlammfass_1/2` werden `schlammfass_aussen_1/2`.
3. Knoten aendern: `pumpe_gross_1..4` Typ Tauchpumpe, Ort Pool; `pool` Spiegel Z -150, kein Seiten- oder Bodenablauf.
4. Kanten aendern: K08/K09/K24/K25 Art B (Druckschlauch, H 2,28 m); K14/K30 `beete -> pool` Art C; K16/K32 Halbring auf der Aufkantung; K13/K29 `verteiler -> pool` Art C.
5. Kanten neu ab K77 (K60 bis K76 sind Ring B2): K77/K78 `biofilter -> schlammfass_aussen` (Art C, Schlamm); Kabel Pegelschalter tief/hoch und Durchflusswaechter je Linie.

## 6. Pruefpunkte (fremd nachmessbar)
1. **Topologie:** `python -X utf8 scripts/check_netz.py` (Netz v4) Bilanz je Linie ohne Abweichung; in `scripts/dome-script.json` 0 Instanzen von `Feinfilter`, `Tank_klein`, `Pumpe_klein`, `Schlammfass` unter Flur und 0 Koerper `T5_Stutzen_*`; 4 `Tauchpumpe` auf dem Innenboden.
2. **Hoehen:** Oberkante Wasserkoerper Pool Z 250 absolut (= -150), Aufkantung Z 550, 14 Beete mit Unterkante Z 400 absolut; Gelaender-Oberkante <= Z 1300 absolut und Interferenz 0 mit allen `Tisch_innen`.
3. **Ordnung v2:** `python -X utf8 scripts/check_leitungsordnung.py` 0 Verstoesse in R1 bis R9 und R11 bis R14; Summe unter Flur (R13) <= 25 m, heute 151 m gebaut [Q R57 Abschn. 4].
4. **Gaenge und Kollision:** `python -X utf8 scripts/check_walkways_voll.py` (beide Varianten) keine neue rote Engstelle; `check_leitungen.py` 0 Verstoesse; `check_latte` in der Scratchpad-Kopie ohne neue Kollision.
5. **Kennzahlen und Einkaufsliste:** `data/system-specs.json` zeigt 4 Pumpen, 328 W +- 10 %, Pool 26,4 m3; die Einkaufsliste enthaelt keinen entfallenen Artikel (Absetzer, Kleinpumpe, Feinfilterkasten, Sumpf, Schacht) mehr; `python -X utf8 scripts/check_varianten.py` meldet beide Varianten gebaut.

## 7. Pflicht-Check Designprinzipien (`docs/designprinzipien.md`)
| Nr | Prinzip | Dieses Blatt | Erfuellt? |
|---|---|---|---|
| 1 | Physik vor Strom | eine Pumpstufe, alles andere frei; Ablassen ueber die vorhandenen Pumpen (Siphon geht ohne tieferen Auslass nicht, R57 W86) | ja |
| 2 | wenig graben | 45,3 m Wasser und 105,9 m Luft/Frischwasser aus dem Graben; neu unter Flur nur Querungen und 2 Einmuendungen, Summe <= 25 m; Ausnahme tieferer Pool (D88) | ja, Ausnahme benannt |
| 3 | wenig Teile | Strang statt Stern spart etwa 190 m Leitung (2.2); 12 -> 4 Pumpen | ja |
| 4 | Technik innen, Station je Linie | Wasserstation am Biofilter (2.2), Schrank-Kasten innen (D87) | ja |
| 5 | Leitungen nach v2 | Arten A bis F je Trasse, Pruefpunkt 3 | ja |
| 6 | lebensmittelecht | Schlaeuche EU 10/2011, Tuellen, Fass, Pumpe; Pumpenwerkstoff offen bis ZR1 | teilweise, offen benannt |
| 7 | Kaufen vor Selbstbau | Hahntafel, Aufkantung und Siebkorb-Aufnahme sind einfache Werkstattteile; Pumpe und Gelaender ohne Link bis ZR1/ZR2 | teilweise |
| 8 | wartbar, Schlamm draussen | Pumpe am Seil, Korb von oben, Schlamm ins Fass draussen, kein Schacht | ja |
| 9 | Sicherheit | Gelaender und Aufkantung; Pegel-tief-Abschaltung; Gelaenderhoehe 750 mm unter den Kragarmen ist offen (2.1); Notluft offen (R55) | teilweise |
| 10 | ehrlich messen | jede Zahl mit Befehl; Annahmen [A]; Abweichung von R57 2a begruendet | ja |

## 8. Nicht anfassen
`data/leitungsnetz.json`, `data/roadmap.json`, `docs/decisions.md` (Orchestrator); `docs/leitungsordnung.md` (nur ueber Systemreview); die Ring-B2-Eintraege und -Bauteile (N-AUTOBAHN-V2); `data/beschaffung/*.json` nur lesen; Biofilter-Lage und K10/K26 (bleiben).

## 9. OFFEN
1. OFFEN (Ben): Gelaenderhoehe unter den Kragarmen der Innentische (2.1).
2. OFFEN (Ben): Haehne je Strang (Festlegung) oder je Abnehmer an der Station (2.2).
3. OFFEN (Ben, aus D88): Absetzer streichen bestaetigen (D71) beim Zwischencheck.
4. OFFEN (Recherche ZR1/ZR2): Tauchpumpe mit Kennlinie; Gelaendernorm.
5. OFFEN (Statik): tiefere Grube 30 mm neben den Pfosten der Innentische (Verbundanker) und Auftrieb des leeren Beckens (R57 Nachtrag Punkt 3).

## Start-Hinweis fuer die Bau-Sitzungen
1. Python immer `python -X utf8`; Skripte per Write, keine Heredocs mit `!` oder Backslashes.
2. Z-Falle: Pool-Spiegel steht in `data/layout.json` (`water_z`), der Rand in `params.json` (`pool_rim`); `pool_depth` NICHT aendern, sonst wird der Pool flacher.
3. Ring B2 erbt jede Aenderung: nach jedem Bau auch `ring_b2` bauen und `check_varianten.py` laufen lassen.
4. Nie `viewer/extras.json`, `designs/dome.sc` fremder Builds oder `*-ring_b2.sc` mitcommitten; nur Pfad-Commits mit `git -C`.
5. Limit: vor jedem Start `get_usage`; Z1 ist der groesste Schritt (Rueckbau plus Becken), notfalls in zwei Runden.
