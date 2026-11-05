# Pruefung N-AUTOBAHN-V2 Werkstatt WA-T (Tragwerk) und WA-S (Schlauch) — Befund

Pruefer: frische Sitzung, hat nichts gebaut. 05.11.2026. Gegenstand: `docs/jobs/N-AUTOBAHN-V2.md` Abschnitt 3 (Teile WA1 bis WA9, Spalte "Pruefung (im Check)"), Teileblatt `docs/parts/autobahn.md`, Teiledaten `data/components/autobahn_teile.json`. Commits: WA-S 95438aa (und 0a574ff), WA-T b0d634b und der spaetere 2649467 ("Check 104/104", Teileblatt-Abschnitt WA-T). Auftrag nannte b0d634b; HEAD hat WA-T seither abgeschlossen, ich habe auf dem aktuellen Stand gemessen.
Nur diese Befund-Datei geschrieben. Alle Befehle aus `user-projects/aquaponics-dome`. Nicht Gegenstand: Montage R1/R2 und die Gesamt-Pruefpunkte 1 bis 5 aus Blatt Abschnitt 6 (Ring B2 ist noch nicht gebaut).
Hinweis zu den Checks: Der Gesamtlauf `check_autobahn_t.py` ohne Argument braucht mehr als 900 s (bei meinem Lauf Zeitgrenze erreicht, Ausgabe endete mitten im Podest); ich habe ihn deshalb teilweise einzeln gestartet (siehe unten).

## Urteil

| Teil | Urteil | Begruendung |
|---|---|---|
| WA1 `portal_joch_mitte` (A und B) | **PASS** | Check 20/20, Interferenz 0 gegen echte `nft_tisch_mitte`-Geometrie (157 Koerper), Kopfverschiebung 0,73/1,11 mm gegen 4,7 mm Grenze |
| WA2 `ausleger_schlauch` (3 Laengen) und WA2b `ringstuetze_d75_b` | **PASS** | Check 32/32 und stelze 12/12; Laengen 1020/1210/1370 weichen vom Blatt (1490/1680 ab Ring) ab, begruendet durch Apothem 3377 |
| WA3 `montageschiene_41` und `lt_klemme_d75` (3 Varianten) | **PASS** | schiene 7/7, klemme 15/15; Durchbiegung 6,06 mm gegen 13,9 mm |
| WA4 `ring_ecke_d75` | **PASS** | Check 7/7; Biegeradius 1875 = 25 x d, strengerer von zwei Werten |
| WA7 `pegelschacht_podest` | **PASS mit Auflagen** | Check 7/7; Hoehe 820 statt Blatt-Soll 950, Gefaelle genau am Grenzwert 1,00 %, Lage am A+-Verteiler liegt im Gang |
| WA5 `schlauch_fall_*` (5 Typen) | **PASS mit Auflagen** | Weg im Soll +-50 mm; ID19 statt ID16, Schlauchschelle fuer ID25 fehlt |
| WA6 `lt_schnellkupplung_id19/_id25` | **PASS mit Auflagen** | Ports und Masse im Check; EPDM-Dichtung nur [A], ID19-Mass aus Faktor |
| WA8 `lt_rueckschlagventil_d50` | **PASS** | im Check; Dateiname nach Bibliothek statt `lt_rsv_d50` |
| WA9 `ruecklauf_rinne`, `bodenrinne_rost_*`, `lt_schlauch_d50` | **PASS mit Auflagen** | Check im Soll; Bodenrinne 150 mm nur [A], Weiterfuehrung unter dem Pool-Spiegel offen |
| **Lebensmitteleignung D85, Regelhahn** | **FAIL** | zweite Quelle fehlt (`check_autobahn_s.py` FAIL, nur ein Hersteller-Datenblatt) |
| **Gesamt WA-T** | **PASS mit Auflagen** | |
| **Gesamt WA-S** | **PASS mit Auflagen, ein FAIL (Regelhahn D85)** | |

## Messung je Teil

### WA-T Tragwerk

Befehl je Zeile: `python -X utf8 scripts/workshop/check_autobahn_t.py <teil>` (Argument `joch|ausleger|stelze|schiene|klemme|verbinder|ecke|podest`), Ausgaben im Scratchpad. Soll des Blatts in der Spalte "Soll".

| Teil | Messwert (Checkausgabe) | Soll (Blatt Abschn. 3) | Ergebnis |
|---|---|---|---|
| WA1 Joch A und B | `joch` 20/20 PASS (exit 0): Koerperzahl 28, Ports Schiene (Z 2253) und Ausleger innen/aussen (Z 2277, y +-575), Oberkante 2297 <= 2300; Interferenz 0 gegen `nft_tisch_mitte`, Innenbeet, Ring, Schiene, Ausleger (157 Koerper) und im Joch; Kopfverschiebung radial 0,73 mm (Restmoment 31,1 Nm), tangential 1,11 mm bei 50 N, Grenze L/300 = 4,7 mm; Biegespannung Stiel 6,9 MPa gegen 160; Klemmen 6,0 kN je Stiel gegen 3 x 155 N; Kippmoment 115 Nm auf den Tisch (Zug 53 N je Seite) als INFO | Ports, Interferenz 0, Kopfverschiebung <= L/300, Kippen | PASS (Kippen nur als Lastangabe, Tisch-Nachweis offen: A5) |
| WA2 Ausleger 1020/1210/1370 | `ausleger` 32/32 PASS: Koerper 9/11/13, Halterabstand max 337 mm gegen 400, Biegespannung am Flansch 7,3 MPa, Durchbiegung Ende 0,52 mm gegen 10, Sattelradius 192,5 = Biegeradius 210 minus AD/2, Arm-Unterkante Z 2257 gegen Gang 2100; Interferenz 0 mit Testschlaeuchen; Massen 5,55 / 6,33 / 6,89 kg | Biegespannung, Durchbiegung <= 10 mm, Halter <= 400, Unterkante >= 2100 | PASS |
| WA2b Stelze Rev. B | `stelze` 12/12 PASS: Interferenz 0 mit Schiene, Verbinder, Ring am Scheitel; Masse 15,5 kg | Ausleger-Anschluss, Interferenz | PASS |
| WA3 Schiene und Klemme | `schiene` 7/7: Laenge 2179,2 = Seite 2194,5 minus Gehrungsluft, Querschnitt 41 x 41, Masse 2,59 kg/m gegen Datenblatt 2,53 (+-10 %), 10 Stuetzpunkte (7 Joche, 3 Stelzen), groesste Spannweite 2786 mm: Durchbiegung 6,06 mm gegen L/200 = 13,9, Biegespannung 34,5 MPa; Schellenabstand max 976 mm <= 1000. `klemme` 15/15 (3 Varianten): tiefster Punkt 2101,5 >= 2100, Einlage umschliesst d75, Interferenz 0 | Durchbiegung bei 2,13 m und 6 kg/m; Schelle umschliesst d75 | PASS; Spannweite 2,13 m des Blatts ist 2,19 bis 2,79 m (Apothem 3377, Joch-Abstaende), trotzdem im Soll |
| WA3b `schienenverbinder_36` | `verbinder` 4/4 PASS: 1 Koerper, Dicke 4, Bohrung ueber dem Bogenscheitel (Stich 96,5 mm), 4 Bohrungen M8 plus 1 | – (Zusatzteil) | PASS |
| WA4 `ring_ecke_d75` | `ecke` 7/7 PASS: 1 Koerper, Biegeradius 1875 >= 25 x d = 1875 (PE100+ Association 25 x DN, Firat und Ostendorf 20 x d: strengerer Wert), Ports A und B, Volumen 1,4454e6 gegen Rechnung 1,4456e6 mm3 (+-0,5 %), Tangente 609 mm, gerade Strecke zwischen Boegen 976 mm >= 300, Interferenz 0 | Biegeradius belegt, Ports d75 | PASS |
| WA7 `pegelschacht_podest` | `podest` 7/7 PASS (4 min 41 s): 18 Koerper, Deckplatte oben Z 820, Port Fass, K10-Gefaelle 1,00 % auf 1200 mm (Achse 1570 minus Bogen 91 minus Rohrstueck 72 gegen Zulauf-Muffe 1395), Interferenz 0 mit Pegelschacht T94, Standsicherheit 2,2 gegen 1,5, Druck je Bein 0,51 MPa. BEFUND-Zeilen: Fass am Ende von K10 liegt 500 mm in Gang A, am Ende von K26 482 mm in Gang B | Fassboden Z 950; K10-Gefaelle >= 1 %; Interferenz 0 mit Biofilter, Pumpen, Bedienzone | PASS mit Auflagen (A2, A3) |
| Summe | 20 + 32 + 12 + 7 + 15 + 4 + 7 + 7 = 104 PASS, 0 FAIL | Commit 2649467: "Check 104/104" | Behauptung belegt (`python -X utf8 -c "print(20+32+12+7+15+4+7+7)"` = 104) |
| Gesamtlauf ohne Argument | Zeitgrenze 900 s erreicht (exit 124), bis dahin 101 PASS, dann `FEHLER interference:` ohne Text im Podest-Abschnitt (Lauf auf dem Stand vor 2649467) | vollstaendiger Lauf | nicht belegt, siehe A6 |

### WA-S Schlauch

`python -X utf8 scripts/workshop/check_autobahn_s.py`: **101/102 PASS, exit 1**. Einziger FAIL: "d85 Teileblatt: Regelhahn lebensmittelecht mit >= 2 Quellen: Ist 0, Soll 1" (zweimal gemeldet, dieselbe Pruefung).

| Teil | Messwert | Soll | Ergebnis |
|---|---|---|---|
| WA5 `schlauch_fall_*` | Weg Ring-Achse bis Abnehmer: id19_mitte 1354,9 (Soll 1355), id19_innen 3027,2 (3027,4), id19_aussen 3220,7 (3220,9), id25_mitte 1784,9 (1795), id25_aussen 3650,6 (3660,9), jeweils +-50; Biegeradius 160 (ID19) und 210 (ID25) >= 6 x AD (159,6 / 207,6); Halterluecke max 400 mm | Laenge = Rechnung +-50 mm; Biegeradius; Kupplung belegt | PASS. Zuschnitte kuerzer als die Rechnung (Blatt rechnete Formstuecke als Schlauch): neu gerechnet `python -X utf8 -I -c "print(779*6+2451*10+2644*8, 1193*6+3058*8)"` = 50 336 mm ID19 und 31 622 mm ID25, Teileblatt 50,3 und 31,6 m |
| WA6 Schnellkupplung | Ports A/B, Masse ID25 94 / 97,5 mm, gekuppelt 155 [A]; Material Edelstahl 1.4401, EPDM-Dichtung statt NBR als [A] | Ports; Werkstoff mit Quelle | PASS mit Auflage (A7) |
| WA8 `lt_rueckschlagventil_d50` | Check PASS: GF 562 PVC-U d50, Muffentiefe 31, Masse 704 g; Zulassungsnachweis mit zwei Quellen PASS | Ports, Baulaenge aus Herstellerblatt | PASS |
| WA9 Ruecklauf | Rinne: Gefaelle einstellbar bis 4,14 % >= 1 %; Gefaellebedarf 128 mm bei 1 % gegen verfuegbar >= 225 mm; Bodenrinne Gang A und B: Rost-Oberkante Z 0 (Abweichung < 1e-13), Laenge 1200 und 1100 >= Gang + 2 x 300; `lt_schlauch_d50` Biegeradius 385 >= 6 x AD | Gefaelle >= 1 %; Rost = Boden +-2 mm | PASS; INFO: Schlauch-Sohle am Rinnenende Z -98/-97 liegt unter dem Pool-Spiegel Z 515 (Befund 4) |
| D85 Regelhahn | GF Kugelhahn Typ 546 Pro, eine Quelle (Hersteller-Datenblatt) | >= 2 Quellen | **FAIL** |

## Drei Stichproben ausserhalb der Pruefpunkte

1. **Zahl der Selbstauskunft gegen Datei:** Teileblatt "Schlauch ID19 50,3 m und ID25 31,6 m": gerechnet aus den Zuschnitten und Stueckzahlen 6/10/8 und 6/8 = 50 336 und 31 622 mm = PASS. Commit 95438aa "101/102" = reproduziert.
2. **Teil gegen sein Blatt:** Blatt WA7 verlangt Fassboden Z 950; gebaut Z 820. Das Teileblatt WA-T Befund 4 begruendet es (K10 passt bei 950 nicht in den Fassdeckel: 1570 - 91 - 72 - 575 = 832; mit 1 % Gefaelle auf 1,2 m 820) und rechnet 206 statt 187 W je 4 Booster, gesamt 636 statt 617 W [E]. Nachgerechnet: 1570 - 91 - 72 - 575 = 832 = PASS. Die 636 W selbst habe ich nicht gegengerechnet (A4).
3. **Commit gegen `git diff`:** `git show --stat 95438aa` (28 Dateien): nur Autobahn-Bauteile, `docs/parts/autobahn.md`, `docs/packages/n-autobahn-v2.md`, `scripts/workshop/autobahn_s.py`; `b0d634b` loescht `ausleger_schlauch_1520.sc` und fuehrt drei Laengen ein (wie im Text). Nichts Fremdes. Der Commit-Text von b0d634b "55/55 ohne Joch" ist veraltet, der Check enthaelt die Joch-Pruefungen heute (20/20). PASS.

## Behauptungen, die sich nicht belegen lassen

1. Beschaffbarkeit, Zulassungen und Biegeradien der Hersteller (REHAU T-Flex, Semperit LM1S, Kamlok, GF 562/546, PE100+ Association, Firat und Ostendorf): nur gegen die Quellenlisten im Teileblatt auf Konsistenz geprueft, die Quellen selbst nicht geoeffnet.
2. "Pumpenleistung 636 statt 617 W": Herleitung nicht nachgerechnet (Planer-Modell Abschn. 5 nicht gelesen).
3. "Kippen auf den Tisch beherrschbar": das Check meldet nur die Last (115 Nm, 53 N Zug je Seite); der Nachweis der Tisch-Klemmen steht bei N-STATIK.
4. Interferenz des Podests gegen Biofilter, Pumpen und Bedienzone (Blatt-Soll): die Check-Pruefung nennt nur den Pegelschacht auf der Deckplatte; die Lage der Montage ist offen.
5. Gesamtlauf `check_autobahn_t.py` ohne Argument bis zum Ende: nicht belegt (Zeitgrenze).

## Auflagen

| Nr | Auflage | Owner |
|---|---|---|
| A1 | Regelhahn D85: zweite Quelle fuer die Trinkwasser-Zulassung des GF 546 Pro suchen oder anderen Kugelhahn mit angeformten Tuellen und Nachweis waehlen; Check danach 102/102 | ICH (Beschaffung N-PREIS-PRUEF) |
| A2 | Podest-Hoehe 820 statt Blatt 950: Auftragsblatt (WA7, Abschn. 2.1 und 5) anpassen, Pumpenleistung 636 W und Pegel EIN Z 1160 uebernehmen; das K10-Gefaelle liegt mit 1,00 % genau am Grenzwert ohne Reserve | ICH (Planer/Orchestrator) |
| A3 | Podest-Lage am heutigen A+-Verteiler liegt 500 mm in Gang A (K10) und 482 mm in Gang B (K26): R1c muss Platz ausserhalb der Gaenge finden, K10/K26 bis 1,2 m verlaengern; danach Interferenz Podest gegen Biofilter, Pumpen, Bedienzone messen | ICH (Montage R1c) |
| A4 | Leistungsrechnung 617 gegen 636 W nachrechnen und im Kennzahlen-Panel fuer Ring B2 Soll 617 W +-10 % anpassen (636 liegt noch innerhalb, 3,1 %) | ICH (Planer) |
| A5 | Joch-Klemmen und Stelzen-Anker nachweisen (Vorspannung M8 5 kN [A], Kippmoment 115 Nm, Zug 53 N je Seite) | ICH (N-STATIK) |
| A6 | `check_autobahn_t.py` ohne Argument bricht bei 900 s mit leerer Meldung `FEHLER interference:` ab; Laufzeit ausweisen oder Teile einzeln aufrufbar in der Vorlage nennen; der Pruefer startet die Teile einzeln (Argument `joch|ausleger|...`) | ICH (Werkstatt WA-T) |
| A7 | Schnellkupplung: EPDM-Dichtung und gekuppelte Laenge beim Hersteller (Riegler) anfragen; ID19 aus Faktor 0,85 [A] gegen Katalog; Schlauchschelle fuer AD 34,6 (ID25) in der Bibliothek ergaenzen; ID19 statt ID16 im Blatt nachziehen | ICH (Werkstatt WA-S, Beschaffung) |
| A8 | Bodenrinne: Handelsteil mit >= 110 mm lichter Tiefe suchen (Modell 150 [A]); Weiterfuehrung der Schlauch-Sohle Z -98 unter dem Pool-Spiegel entscheiden (Einmuendung unter Wasser, Leitungsordnung R13) | DEINE ENTSCHEIDUNG (Ben/Planer): Einmuendung unter Wasser oder Rinne tiefer legen; Empfehlung: Einmuendung unter Wasser |
| A9 | Abschnitt 1.2 und 2.2 des Auftragsblatts: Ringmasse (Apothem 3377, Seite 2194,5, Umfang 21,95 m, Ausleger-Ziele 1591/1784 mm) und Ringhaengung unter der Schiene nachziehen | ICH (Planer) |

## Abschluss

Geprueft gegen: `check_autobahn_t.py` je Teil (104 PASS), `check_autobahn_s.py` (101/102), eigene Rechnungen (Schlauchsummen, 832 mm Fassdeckel, Summe 104), `git show --stat` von 95438aa, b0d634b, 2649467, `data/components/autobahn_teile.json`, Teileblatt `docs/parts/autobahn.md`.
Offen: A1 bis A9 (siehe Tabelle); A8 DEINE ENTSCHEIDUNG (Ben); Gesamtlauf `check_autobahn_t.py` und Herstellerquellen nicht belegt.
