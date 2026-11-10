# R61: Leons Oasis-Showcase als Soll des Wasserkreislaufs (Planer N-UNIFY-AUTOBAHN, 10.11.2026)

**Problem:** Das Modell hat zwei Wasserkreisläufe (A+ und Ring B2); Leons Showcase beschreibt einen dritten, ausgearbeiteten. **Intent:** Ein einziger Kreislauf nach der Quelle (D93, W89). **Goal:** Eine geprüfte, maschinenlesbare Fassung der Quelle (`data/oasis-soll.json`) mit allem, was sie festlegt, was sie offen lässt und wo sie sich widerspricht, plus eine Annahme je offener Stelle.

[Q] Quelle im Repo · [E] eigene Rechnung (Befehl daneben) · [A] Annahme dieses Berichts (in `docs/decisions.md` als D94 bis D107). „A1 bis A32“ sind die Annahmen der Quelle selbst (Leon/Ben), „E“ und „Q“ mit Zahl sind deren Quellenliste.

## 1. Quellen und Prüfung
1. `docs/quellen/oasis-showcase-2026-11-10/index.html` (SHA256 im README): Draufsicht und Seitenprofil als Inline-SVG, `nodeDatabase` (27 Bauteile), `sollStufen`, `sollWasserspiegel`.
2. `docs/quellen/oasis-showcase-2026-11-10-nachtrag/flow-diagram.html` (neu gesichert, SHA256 `68e358…1799`): Höhenschnitt (maßstäblich, 150 Einheiten je m), Annahmen A1 bis A32, Änderungen C1 bis C20, Quellenliste Q1 bis Q24 und zwei JSON-Blöcke (`flow-data`: 43 Bauteile, 90 Wege, Teile; `schema-data`: Stufen, Wasserspiegel, Antrieb). Die erste Sicherung kannte diese Datei nicht: `index.html` Zeile 3144 bindet Höhenschnitt und Diagramm nur über einen Rahmen auf sie ein.
3. `model.glb` (Leons 3D-Modell) wurde nicht ausgelesen: Die Quelle sagt selbst, ihre Höhen und Behältermaße daraus seien „kein Maßstab“ (A4, A15, C1).
4. Beide Dateien stammen von derselben Hand (Leon, Owner-Aufträge Ben). Die Zwei-Quellen-Regel (Designprinzip 10) ist für **physikalische** Aussagen damit nicht erfüllt; die Quelle gilt hier als Auftrag (D93), nicht als Messung. Fachlich offene Zahlen (Pumpen, Venturi) stehen unter 4 als offen.
5. Prüfung: `python -I -X utf8 scripts/oasis_soll.py` → 45 von 45 Prüfungen bestanden, darunter: beide Dateien stimmen in Stufen, Wasserspiegeln, Wegen (von/nach/Medium) überein; Mengenbilanz 110 = 38 + 54,5 + 17,5 l/min je Halbring; 24 + 14 = 38 Abnehmer = 8 + 6 + 10 Tische und 8 + 6 Beete; jede Schwerkraft-Kante fällt, jede Pumpe fördert nach oben (Hub 1150 und 1000 mm), Überläufe 50 mm, Freibord Fischtank 450 mm, Sumpf 250 mm.

## 2. Was die Quelle festlegt (Kreislauf in einem Satz je Weg)
1. **Start:** Haupt-Fischtank, teilversenkt, Ø 4 m, Boden −1,00 m, Rand 1,20 m, Wasserspiegel 0,75 m über Fußboden (22 m³, A26). Er ist der tiefste Punkt der Anlage.
2. **Pumpstelle 1:** je Linie eine Pumpe saugt aus dem Fischtank und hebt 1,15 m in den Vortex (1,90 m); Rückschlagventil in der Druckleitung (A14, A30).
3. **Schwerkraft ab dort:** Vortex → Überlauf (10 cm) → Biofilter (1,80 m) → Einspeisung d63 → **Wasserautobahn** (Rohrachse 1,55 m) → Abfahrten → Schlauch-Fallleitungen → Anbauringe → Rückläufe in die Sumpftanks (nur NFT Innen direkt in den Fischtank).
4. **Wasserautobahn:** ein einziger geschlossener Ring (Zehneck, 2 Halbringe à 4 Seiten und 5 Ecken, 2 Kupplungsstrecken mit je einem Kugelhahn d63, **im Betrieb offen**), Ring d75 auf Schellen, je Halbring 110 l/min: 12 NFT-Abzweige d32 (38 l/min), 7 Flood-and-Drain-Abzweige d40 (54,5 l/min), Ring-Ende-Hahn d63 (17,5 l/min Überschuss in den Sumpf der eigenen Linie), 1 Entlüfter d75, 1 Entleerungshahn d63 (A29).
5. **Anbauringe:** Außen 8 NFT + 8 Beete, Mitte 6 + 6, Innen 10 NFT (auf dem Poolrand, kein Beet). Wasserspiegel NFT 1,05 / 0,90 / 1,25 m, Beete 0,25 m (Flutstand); je Beet ein Siphon mit Abtropfgitter, Vlies, Sieb und etwas Belüftung unten (A21).
6. **Sumpf:** 2 Tanks im Boden (Boden −0,50 m, Rand 0,00 m, Deckel begehbar), 1680 l, Soll-Pegel −0,25 m (850 l), Hochstand −0,11 m, je 4 Pufferzonen zu 10 % (Kalk, Aktivkohle, frei, frei; Auf-und-ab-Fluss), je ein Hochstand-Schwimmerschalter, der über die Steuerung die Pumpe Fischtank → Filter **derselben Linie** abschaltet (A20, A31).
7. **Pumpstelle 2:** je Sumpf eine Pumpe (+1,00 m), Rückschlagventil, **passiver Venturi-Belüfter** unmittelbar vor dem Einlauf in den Fischtank (A19, A23).
8. **Beckenkette:** Biofilter 1 → Lebendfutterbecken (Ø 1 m, 0,85 m) → Überlauf → Anzuchtbecken (Ø 2 m, 0,80 m) → Überlauf → Fischtank; alle drei auf einer Ebene, von außen nach innen jeweils 5 cm tiefer (A13).
9. **Notüberlauf** je Biofilter in den Sumpf der Linie (fällt 2,05 m, nur bei verstopftem Halbring, A27). Der Fischtank braucht keinen.
10. **Nachspeisung:** Regenwassertank 5 m³ vor Frischwasser, über ein mechanisches Nachspeise-Ventil in den Fischtank (A8).
11. **Luft:** Notluftpumpe (Luftstein im Fischtank, Notstrom), dazu als Alternative zu den Venturis eine Belüftungsanlage aus 2 großen Luftpumpen mit je 4 Armen (Biofilter, Sumpf, ein Becken, Fischtank); nicht in den Vortex (A23, A24, A32).
12. **Schlamm:** Schlammreaktor je Linie ist ein Sammelbehälter mit Ablasshahn von Hand, **außerhalb** des Wasserkreislaufs; der Schlamm geht von Hand an das Permakultur-Modul, kein Rückweg (A11).
13. **Stufen:** Fischtank/Anzucht/Futter/Pumpen/Venturi/Sumpf 0 · Beete 1 · NFT 2 · Ring, Abfahrten, Ring-Ende, Kupplung 3 · Biofilter 4 · Vortex 5 (A15). Stufen sind nur Reihenfolge, das Maß steht in den Wasserspiegeln (A25).

Zählung (aus der Datei): 43 Bauteile (40 im Umfang; PV, Batteriespeicher, Steuerung nur als Referenz), 90 Wege (77 im Umfang: 53 Wasser, 9 Luft, 6 Schlamm, 9 Strom für Pumpen, Belüftung, Schwimmer), 97 Armaturen-Zeilen mit 406 gezählten Stück (`python -I -X utf8 scripts/oasis_soll.py`).

## 3. Widersprüche
**In der Quelle**
1. W1 Sumpf „tiefster Punkt“: `index.html` `nodeDatabase.sump.desc` nennt ihn „der tiefste Punkt des Wasserkreislaufs“; A26 sagt, der Fischtank sei der tiefste (Boden −1,00 m gegen −0,50 m). → A26 gilt (Owner 07.11.).
2. W2 Notüberlauf: A7 sagt, ein Notüberlauf-Wasserweg sei „nicht definiert und darf nicht erfunden werden“; A27/C15 zeichnen ihn (Owner 09.11.). → A27 gilt (neuer).
3. W3 Pool-Rand: Q17 zitiert „Der Pool Rand liegt auf Fußbodenhöhe“; A26 und Q18 („Ja, B umsetzen“) legen den Rand auf 1,20 m. → A26 gilt (Entscheidung nach dem Zitat).
4. W4 Fischtank-Maß: Text Ø 4 m (A26), Leons Modell 4,06 m (Q14), Zeichnung Radius 180 Einheiten = Ø 4,5 m, Ring-B2-Modell 3,89 m (`data/layout.json` pool.d). Die Zeichnung ist an Becken schematisch (A16), der Sumpf dagegen maßstäblich (1125 × 2975 mm = 3,35 m², passt zu 1680 l bei 0,50 m). → Text vor Zeichnung (D96).
5. W5 Abfahrten je Ecke: A17 nennt „bis zu fünf je Ecke“ und zugleich Quellen, die „kein Platz“ sagen; die Zeichnung verteilt 1/2/3/3/3 (NFT). Die Lage je Ecke ist ausdrücklich nicht belegt.
6. W6 Simulationsparameter `flowRate`: `index.html` 13,2 m³/h (= 220 l/min, Soll), `flow-diagram.html` 3,8 m³/h (Vorgabe des Showcase). Der Soll-Wert passt zu 2 × 110 l/min.
7. W7 Asymmetrie der Linien: nur Biofilter 1 speist das Lebendfutterbecken; Luftpumpe 1 bedient das Anzuchtbecken, Luftpumpe 2 das Lebendfutterbecken. Kein Fehler, aber nicht symmetrisch.
8. W8 Lage außerhalb der Kuppel: Regenwasser, Frischwasser, Permakultur, Notluftpumpe und beide Belüftungspumpen liegen in der Zeichnung außerhalb des Kuppelkreises (Radius 6564 bis 7216 mm); Steuerung ebenso. Die Quelle begründet es mit kurzen Leitungen (A16).

**Quelle gegen Altbestand** (Auswahl, vollständige Liste im Paket, Abschnitt „Abweichungen zum Altbestand“)
9. W9 Der Ring im Modell liegt auf 2,145 m, die Quelle 1,55 m; das Modell setzt Pegelschacht, Booster und Steigleitung dazwischen, die Quelle lässt den Biofilter höher stehen als den Ring (Schwerkraft).
10. W10 Kupplungsstrecken: Blatt N-AUTOBAHN-V2 „im Betrieb geschlossen“, Quelle „im Betrieb offen“ (A29).
11. W11 Pool: Zielbild S (D88) setzt ihn 665 mm tiefer ein (Rand ≈ Flur); die Quelle legt Rand 1,20 m und Boden −1,00 m, also flacher und höher.
12. W12 Biomasse: D40 plant 475 kg Fisch in 26,4 bis 27,8 m³; Showcase rechnet 120 Fische/85 kg in 22 m³. Das ist kein Teil des Kreislaufs und überholt D40 nicht, verlangt aber eine Neurechnung (offen).

## 4. Was die Quelle offen lässt („nicht festgelegt“) und unsere Annahme
Zählung aus der Datei: 8 Bauteile mit offener Stufe (Sumpf 1/2, Pumpen am Sumpf 1/2, Schwimmerschalter 1/2, Schlammreaktor 1/2), 6 ohne Höhenangabe (Regen, Frisch, Permakultur, 3 Luftpumpen), 22 von 53 Wasserwegen mit Nennweite, 8 mit Durchflusszahl.

| Nr | Offene Stelle (Quelle) | Annahme | Prinzip | D |
|---|---|---|---|---|
| O1 | Pumpen: Anzahl und Leistung (A3) | 4 Pumpen (2 + 2), Tauchpumpen im Fischtank bzw. Sumpf; Typ bleibt Kandidat Oase AquaMax Eco Premium 8000 (D92, R59), Werkstatt prüft Hub 1,15 m und 1,00 m + Venturi (A19: etwa 3,5 m) | 1, 3, 7 | D102 |
| O2 | Höhe der Behälter Vortex/Biofilter | vorhandene Tanks (`tank_klein` 1323 mm, `tank_gross` 1756 mm) wiederverwenden und auf Podeste stellen, bis Überlauf = Soll-Wasserspiegel | 3 | D100 |
| O3 | Venturi: Größe, Luftmenge, Druckabfall (A19) | Werkstatt wählt Injektor nach R60 (Mazzei-Tabelle); Lufteinlass mit Filter und Rückschlagschutz | 6, 9 | D103 |
| O4 | Schwimmerschalter: Wiedereinschaltpunkt (A20) | Hochstand −110 mm (Quelle), Wiedereinschalten bei −180 mm [A]; im Modell zählt der Hochstand | 9 | D105 |
| O5 | Schlammreaktor: Höhe (Stufe 1 offen), Maße (350 l) | oberirdischer Sammelbehälter 350 l auf dem Flur, Ablasshahn von Hand; Zulauf vom Vortex fällt aus 1,90 m | 2, 8 | D104 |
| O6 | Rohrnennweiten außer Ring/Abfahrten/Einspeisung | Saug- und Druckleitung Pumpstelle 1 und 2 d50, Überläufe der Becken und Notüberlauf d63, Sumpf-Zuläufe Schlauch ID25, Luftleitungen d20 [A, nach Leitungsbibliothek `lt_*`]; Werkstatt bestätigt mit Durchfluss | 3, 5 | D106 |
| O7 | Lage der Abnehmer je Ring-Ecke (A17) | Lage des Modells behalten (Tisch-Zulauf an den Sektorgrenzen, 38 Abnehmer an 10 Ecken) | 5, 8 | D98 |
| O8 | Pufferzonen: Füllung, Menge, Durchfluss | vier Kammern zu je 17 Einheiten = 212 mm (A31: 10 % der alten Länge 170 Einheiten), Füllung als Beschriftung, keine Mengen | 3 | D105 |
| O9 | Regenwassertank: Lage, Anschluss; Permakultur: Lage, Maße | Tank 5 m³ und Permakultur-Modul als einfache Platzhalter außerhalb der Kuppel an der Technikseite; Anschluss d25 an das Nachspeise-Ventil | 3 | D107 |
| O10 | Biofilter-/Vortex-Zeichnungsgröße | Ø aus Zeichnung (Vortex 1050 mm, Biofilter 1150 mm) gilt nicht; vorhandene Tankdurchmesser behalten | 3 | D100 |
| O11 | Notluftpumpe, Belüftungsanlage: Leistung, Luftmenge | Gebläse und Verteiler des Modells (`geblaese_luft` ×2, `luftverteiler_4/_6`) werden Belüftungsanlage; Notluftpumpe klein neu; Leistung offen wie in der Quelle | 3, 9 | D103 |
| O12 | Ring: Werkstoff, Waagerechte oder Gefälle (A9) | Ring waagerecht, Werkstoff wie Modell (PE-100/PVC nach N-AUTOBAHN-V2 2.2) | 3, 5 | D98 |
| O13 | Fischtank-Durchmesser (W4) und Volumen | Ø 3890 mm innen bleibt (Radialbudget D28/D29); Wassertiefe 1750 mm → 20,8 m³ statt 22 m³ der Quelle (−5 %) | 10 | D96 |
| O14 | Beete: Maße, Takt Ebbe/Flut (A21) | Beetkörper des Modells (800 × 2640 × 637 bzw. 933-Typ) bleibt; Flutstand 250 mm über Flur über das Standrohr; Takt aus Zulauf 7,8 l/min und Volumen | 3, 8 | D97 |
| O15 | Lage der Technik (Vortex, Biofilter, Sumpf, Schlamm) | Zeichnung, um 18° gedreht (D95); bei Kollision höchstens 750 mm verschieben (A16: „höchstens 60 von 1000 Einheiten“) | 4 | D99 |
| O16 | Fußboden-Bezug | Modell-Z 400 mm (`walk_z`), nicht Z 0 | 10 | D94 |

## 5. Umrechnung Zeichnung → Modell (Annahmen D94, D95)
1. [E] Maßstab: Kuppelkreis r 480 Einheiten = 6000 mm → **12,5 mm je Einheit**. Probe: Sumpf 90 × 238 Einheiten = 1125 × 2975 mm = 3,35 m²; A22 nennt 1680 l bei 0,50 m Tiefe = 3,36 m² (`oasis_soll.py`, Quelltext A22).
2. [E] Fußboden: `viewer/instances.json` `walk_z` = 400; Tische, Tanks, Pumpen, Podeste stehen bei Z 400 (`python -I -X utf8 scripts/oasis_istmessung.py`). Der Auftrag nannte „Z 0“; das ist die Sockelunterkante. Alle `z_modell_mm` der Datei = 400 + Höhe über Fußboden. Eine Zahl (`FUSSBODEN_Z_MM`) genügt zum Umstellen.
3. [E] Drehung: Die Ecken des Ring-B2-Modells liegen bei Az 18 + 36 k und die Kupplungsstrecken bei Az 108 und −72 (`ring_ecke_d75` ×10, Eckradius 3394 mm). Die Zeichnung hat Ecken bei Az 0 und ±36 k und Kupplungsstrecken bei ±90. Gedreht um **+18°** deckt sich der Halbring 1 der Zeichnung mit Az −54, −18, 18, 54, 90 (Prüfung in `oasis_soll.py`). Die Quelle bestätigt die Drehung selbst: „Zehneck so gedreht, dass die Kupplungsstrecken auf der Achse liegen; die Winkel aus Bens Konzept sind nicht übernommen“ (A16).
4. Zeichnung oben = Modell +Y; die Technik der Zeichnung liegt unten (−Y), wie die Technik-Sektoren des Modells (Az −90 bis −18).
5. Der Eckradius der Zeichnung (3550 mm) liegt 104 bis 156 mm über dem des Modells (3394 bis 3446 mm); die Zeichnung ist schematisch (A16). Der Ring behält die Lage des Modells, nur die Höhe ändert sich (D98).

## 6. Was dieser Bericht nicht belegt
1. Dass die Soll-Lage der Technik (Vortex, Biofilter, Sumpf, Schlamm im Süden, Radius bis 5,4 m) in der gebauten Kuppel kollisionsfrei passt. Das prüft Runde U1 (`docs/jobs/N-UNIFY-AUTOBAHN.md`) per Skript, bevor etwas gebaut wird.
2. Pumpenleistung, Venturi-Größe, Rohrdurchmesser außerhalb von Ring und Abfahrten: offen wie in der Quelle.
3. Statik der Podeste (Vortex mindestens 577 mm = 1900 − 1323 mm Tankoberkante [E, `viewer/detail/tank_klein.json`], Biofilter 230 mm = 1800 − 1570 mm gebauter Überlauf [Q N-AUTOBAHN-V2 2.1]) und des tieferen Rings über den Tischen: N-STATIK, nicht Teil dieses Plans.

Geprüft gegen: `python -I -X utf8 scripts/oasis_soll.py` (45/45), Quelltext beider Dateien, `scripts/oasis_istmessung.py`, `docs/decisions.md`, `docs/designprinzipien.md`.

## 7. Nachtrag U3 (11.11.2026, Werkstatt-Lauf): Becken, Tische, Beete als Komponenten und Parameter
**Problem:** U3 sollte Fischtank, Anzucht-, Lebendfutterbecken, NFT-Tische und Beete auf die Soll-Hoehen bringen. **Intent:** U4 setzt sie nur noch. **Goal:** `python -X utf8 scripts/workshop/check_pool_soll.py` PASS mit 0 mm Abweichung der Parameter (Messwerte im Paket, Abschnitt Stand, Lauf U3).
1. [E] Fischtank: Innenboden -1000 bei Wasserspiegel 750 gibt `pool_depth` = 750 + 1000 + 120 (Bodenplatte) = **1870**; Aussenunterkante -1120, Rand 1200, Aussenhoehe 2320; Wasserkoerper Ø 3880 x 1750 = 20,7 m3 (gebaut: 20 689,9 l, `python -X utf8 scripts/workshop/pool_zentral.py`). Keine Wanddurchfuehrungen (D102).
2. Anzucht- und Lebendfutterbecken stehen auf dem Boden (Standflaeche 0, Innenboden 120): Tiefenparameter `pool2_depth` 800 und `pool3_depth` 850; Ueberlauf-Tuellen d63 auf Wasserspiegelhoehe, je 50 mm tiefer (Weg e63, e70; A13). Befund [E]: Die Quelle nennt Ø und Boden ohne Hinweis, ob innen oder aussen; gewaehlt Innen-Ø (D118).
3. [E] Innentische am Poolrand: Rinnen-Wasserspiegel 1250 gibt Rinnenunterkante 1230 (Film 20, Messvorschrift `data/oasis-messung.json`); der Poolrand liegt bei 1200, also 30 mm darunter. Ein Holm 60 hoch (Unterkante 1170) ragt 30 mm in die Poolwand, Pfosten auf der 150 mm breiten Wand haetten 5 mm Laenge. Gebaut: Pfosten ausserhalb der Wand wie bisher, Holm und Kragarm 40 x 20 x 3 (`typen.innen.holm_h` 20); gemessen Kragarm-Unterkante 1208,1 am tiefsten Bock, also 8,1 mm ueber dem Rand (`check_nft_fit.py`, Zeile 'Kragarm-Unterkante'). Der Kragarm entfaellt nicht, er wird flacher (Bedenken B8).
4. Ergonomie nach `python -X utf8 scripts/table_height.py` (R35: Topfebene gegen Ellbogen, Toleranz 950 bis 1050): Aussen 1030 gelb nur bei 1,55 m; Mitte 880 gruen bei 1,55 und 1,60 m, gelb bei 1,75 m, rot bei 1,90 m (Topfebene 263 bis 303 mm unter dem Ellbogen); **Innen 1230 rot bei 1,55 und 1,60 m** (Haende auf Schulterhoehe), gelb bei 1,75 m, gruen bei 1,90 m. Nicht umgesetzt, nur notiert (Bedenken B10, D117).
5. [E] Beete: Sperrboden-Oberkante = Wannenhoehe - rim_gap - media_depth = 637 - 75 - 300 = 262 ueber der Wannenunterkante; mit der Wanne auf dem Flur liegt das Medium 12 mm ueber dem Soll-Flutstand 250, das Beet wuerde nicht fluten. Gewaehlt (D122): Sperrboden-Oberkante 70 (Quelle Beet-Boden), Wanne 460 / 420 (Quelle Rand), Standrohr 180 ueber dem Sperrboden = Flutstand 250. Der Siphon-Auslass unter der Wanne (Z -30 und tiefer) reicht damit in den Fussboden (Bedenken B9).
