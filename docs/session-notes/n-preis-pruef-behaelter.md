# N-PREIS-PRUEF 1C: Behaelter und Pumpen (Notiz Fachrecherche)

Stand 05.11.2026. Bezugsdatei `data/beschaffung/behaelter.json` (28 Zeilen: 19 bestehende, 9 neu angelegt). Blatt `docs/jobs/N-PREIS-PRUEF.md`, Start-Auftrag `docs/jobs/start/N-PREIS-PRUEF-recherche.md` (25c2eed).

**Problem:** In der Gruppe C waren 11 platzierte Hauptangebote FEHLER, VERDACHT oder GESPERRT, neun Zeilen hatten keine Bezugsdatei, und fuer IBC und Faesser fehlte die Lebensmittel-Vorgeschichte.
**Intent:** Jede Zeile soll ein real bestellbares, zum Bauteil passendes Teil sein (D76: mindestens Europa, zwei unabhaengige Quellen).
**Ziel:** Jede der 28 Zeilen ist ersetzt, bestaetigt oder als OFFEN mit Grund eingetragen. Gemessen: Skript ueber `behaelter.json`, jede Zeile hat `angebote` oder `luecke`, keine Zeile ohne beides.

Methode: drei parallele Recherche-Agenten (Pumpen und Luft; Tanks, Filter, Acryl; IBC, Faesser, Becken), jede Seite geoeffnet, RS und TME im Browser-Pane gelesen. Zwei Seiten mit Texten an KI-Assistenten (Kingfisher, Bestand) sind nicht mehr im Angebot. "gerechnet" = Netto x 1,19 vom Agenten, nicht von der Seite (konfidenz E). Nichts gekauft, nirgends angemeldet.

## Ersetzt (Bestand falsch oder ungeeignet)
1. `BEH-ibc-1000l`, `BEH-ibc-beetwanne`: Monopoel (gebraucht, "Restanhaftungen") und Hornbach GRAF (Gefahrgut-IBC ohne Lebensmittelangabe) fallen weg. Neu: Fasswulf DE 229,94 ("FDA Lebensmittelzulassung: Ja"), Rekubik DE 299,99 ("Lebensmittelecht: Ja", derzeit nicht verfuegbar), Faesser.de 187,63 (gerechnet). Gebrauchte IBC "zuvor nur Lebensmittel" ohne Nachweis zaehlen nicht.
2. `BEH-fass-hdpe`: Bestand war ein 220-l-Fass (580 x 980), das Modell hat d500 x 788 = 120 l. Neu: richter & hess DE 55,22 (gerechnet), Rekubik DE 43,99.
3. `BEH-kanister-hdpe`: eBay und Kaufland (403, Verkaeufer unklar) ersetzt durch richter & hess DE 8,66 (gerechnet) und subolab DE 18,09 (gerechnet).
4. `BEH-tank-pe-673x1075`: tanksdirekt 200 l (zu klein) und UK-Enduramaxx fallen weg. Neu: Aricon TCO 3/L (Hersteller DE) und CGK TCO3/L (BE), beide ohne Preis (Anfrage).
5. `BEH-messbecher-pp`: Naeherung 5 l: Bueromarkt-AG 13,49 und barstuff 13,09 (beide DE).
6. `BEH-halter-box-gehaeuse`: Naeherung Polycarbonat-Gehaeuse: RS Deutschland 67,27, TME Germany (kein Preis, nicht lagernd). Bestand Spelsberg (IE) entfaellt.
7. `BEH-feinfilter-pp-630x440x610`: der eBay-Link zeigte eine Fehlerseite; Angebot entfernt, siehe OFFEN.
8. `BEH-pool-zentral`: Hornbach-Poolsets (Hoehe 107 bis 120 cm) sind nur Preis-Orientierung und stehen jetzt in der Zeilen-Bemerkung, nicht mehr als Angebot.
9. `PMP-dosierpumpe`: Funduino (429) und ManoMano (403) nicht lesbar; Angebote entfernt, siehe OFFEN.

## Bestaetigt
1. `PMP-pumpe-gross` (Eheim Universal 3400): drei Haendlerseiten gelesen: shop-meeresaquaristik.de DE 276,90; aquaristikshop.com 195,95 (Land nicht auf der Seite); Hornbach AT 299,00. greenaqua.hu 233,79 vom 04.11. (heute 429, nicht neu gelesen).
2. `PMP-pumpe-klein` (Eheim Universal 1200): aquacomputer.de DE 95,90 (nicht lagernd, bis 90 Tage) und greenaqua.hu 117,10 (Bestand sagte 130,11).
3. `BEH-ak-sedimentfilter` (neu): Alfiltra DE 38,00 (Gehaeuse 10" plus Kerze) und WilTec DE 20,72 (20"-Set, 5 um).
4. `TOP-aktivkohle` (neu): Ecosoft DE 350,00 je 25-kg-Sack (Kokosnuss, ca. 315 EUR fuer 42 l) und silica-gel.it IT 123,88 (Packung unklar, nennt EN 12915).

## Von Hand gelesen 05.11.2026: passt, weil ...
Platzierte Zeilen der Gruppe (Bedarf > 0), deren altes Hauptangebot VERDACHT oder GESPERRT war:
1. `BEH-fass-hdpe`: Rekubik-Seite nennt 490 x 800, 120 l, "Lebensmittelecht: Ja"; richter & hess nennt d496 x 800, "Lebensmittelzulassung: Ja". Modell d500 x 788 weicht um unter 1 cm ab.
2. `BEH-kanister-hdpe`: richter & hess nennt 20 l, Muendung R61, "Lebensmittelzulassung: Ja"; der Modell-Deckel 60 mm passt zur 61-mm-Muendung.
3. `BEH-messbecher-pp`: beide Seiten nennen PP, 5 l mit Skala; Mass weicht ab (siehe OFFEN (Ben)).
4. `BEH-ibc-beetwanne`: beide neuen Seiten nennen neuen IBC mit Lebensmittelangabe; Schneidbarkeit der Wanne offen (siehe OFFEN (Ben)).
5. `BEH-halter-box-gehaeuse`: Bedarf 0 (nicht platziert); RS-Seite nennt 201 x 163 x 98, PC, Klardeckel, IP65.
6. `PMP-pumpe-gross`, `PMP-pumpe-klein`: waren OK; Typ, Leistung und Foerderhoehe jetzt am Herstellerwert gegengelesen.

## OFFEN mit Grund (Quelle)
1. `PMP-dosierpumpe`: keine lesbare Quelle; naechster Schritt Kamoer-Datenblatt plus EU-Haendler (ICH, nicht ausgefuehrt).
2. `BEH-tank-pe-673x1075` und `BEH-tank-pe-673-deckel`: Preis nur auf Angebotsanfrage bei Aricon und CGK.
3. `BEH-tank-pe-930x1444` und `BEH-tank-pe-930-deckel`: kein Europa-Tank mit d930; Aricon liefert ab 500 l nur d1290.
4. `PMP-geblaese-luft`: ein Haendler (tanks.ie IE, 372,70 NETTO, Preis brutto gerechnet 458,42) plus BIBUS-Datenblatt ohne Preis; Lieferung nach DE unbekannt.
5. `SON-luftverteiler-4`, `SON-luftverteiler-6`: kein Kaufteil, Eigenbau aus PVC-U d25; Einzelpreise stehen in `leitung.json`.
6. `SON-scheibenbelueftung-270`: Jaeger JetFlex HD 270 per Herstellerdatenblatt identifiziert, kein EU-Haendler mit Preis.
7. `BEH-messzelle-acryl`: 5-mm-Zuschnittpreis nicht ablesbar (Hornbach 57,7 bis 66,5 EUR/m2 als Plattenpreis).
8. `BEH-ak-kompositbehaelter-254x790`: kein EU-Haendlerpreis; Pentair Q-1035-A hat d257 x 903.
9. `SON-ak-konsole`: Eigenbau aus Normprofilen, Preis aus `stahl.json`.
10. Katalytische Aktivkohle (Chloramin): kein EU-Haendlerpreis.
11. `BEH-zweitbecken`: Preis der passenden PP-C-Variante (d1750 x 1250 oder d1950 x 1250) nicht genannt.
12. Lebensmitteleignung: bei Tanks, Faessern, IBC und Aktivkohle liegt nur die Haendler- oder Herstellerangabe vor, kein gelesenes EU-10/2011-Dokument. Die Konformitaetserklaerung ist vor dem Kauf anzufordern; "OFFEN (Quelle): Eignung nicht angegeben" gilt fuer Scheibenbeluefter, Sedimentfilter und die PP-C-Becken.

## OFFEN (Ben): Mass und Werkstoff (das Modell wird nicht geaendert)
1. `BEH-tank-pe-673x1075`: d675 statt 673; die Hoehe 1360 (TCO) oder 1500 (TCC) enthaelt ein Stahlgestell, das Modell hat ein eigenes. Empfehlung: TCC 3/L ohne Gestell; dann entfaellt der Deckel-Posten.
2. `BEH-tank-pe-930x1444`: d1290 Standard (Aufstellflaeche +360 mm), Sonderfertigung oder stueckeln.
3. `BEH-feinfilter-pp-630x440x610`: Eigenbau aus PP-Platte oder Handelsmass PE 700 x 600 x 625 (tanksdirekt 208,85).
4. `BEH-ibc-beetwanne`: Beetwanne 2640 mm ist aus einem IBC (Laenge 1200) nicht schneidbar; Anzahl IBC je Wanne.
5. `BEH-fass-hdpe` d496 x 800; `BEH-kanister-hdpe` Hoehe 380 statt 300; `BEH-messbecher-pp` 5 l d196 bis 203 x 257 bis 270; `BEH-halter-box-gehaeuse` 201 x 163 x 98 PC; `SON-gummifuss-40` Hoehe 40 statt 15 mm; `SON-scheibenbelueftung-270` 268 mm; `BEH-ak-kompositbehaelter-254x790` reale Hoehe ca. 903.
6. `BEH-pool-zentral`: Wellblech-Rundtank mit EPDM-Liner d4,02 x 2,29 m (28 m3) oder x 3,05 m (38 m3) statt 4,19 x 2,475; Werkstoff und Bauart.
7. `BEH-zweitbecken`, `BEH-becken-dritt`: PP-C-Rundbecken d1750 x 1250 bzw. d1250 x 1250. `BEH-becken-dritt` hat keine Instanz im Modell; Bedarf pruefen.
8. `BEH-drittbecken-klein`: Beton oder 500-l-PE-Rundbehaelter d740 x 1230 (ANDO DE 689,72, DENIOS DE 680,68 gerechnet).
9. `PMP-pumpe-klein`: Universal 1200 gedrosselt (20 l/min, 28 W) oder Soll aendern; Universal 600 liegt unter Soll. `PMP-geblaese-luft`: Leistung 115 W (tanks.ie), 180 W (R53), 204 W (Bestand) widersprechen sich. `PMP-dosierpumpe`: Dosiermenge und Medium.
10. `TOP-aktivkohle`: normale Kokoskohle (nur freies Chlor) oder katalytische Kohle (Chloramin).

## Hinweise an den Orchestrator
1. `python -X utf8 scripts/check_bom.py` liefert aktuell Exit 1 wegen Instanzen und Stueckliste (4880 gegen 4914 Instanzen, fehlende Komponenten); das liegt am Modell- und Stuecklistenstand, nicht an dieser Datei. Schritt 2 (Werkstatt) laesst `bom.py` neu laufen.
2. Preise ohne `preis_eur` (Aricon, CGK, TME, Polyvantis) erscheinen in der Einkaufsliste weiter als "Preis fehlt"; das ist gewollt.
3. Konfidenz `E` steht nur dort, wo ich Netto x 1,19 oder die irische MwSt gerechnet habe.

## Nachtrag 05.11.2026: Auflage 7 und Bezug fuer beet_sumpf, schlammfass, biofilter_dritt
Auftrag: Pruefbefund `docs/jobs/pruefung/N-PREIS-PRUEF.md` (bdfbe93). `behaelter.json` hat jetzt 36 Zeilen (8 neu).

Auflage 7 (erledigt, Commit 1a51f88):
1. `BEH-drittbecken-klein`: beide Angebote tragen jetzt "ERSATZ (Abweichung: PE-Rundbehaelter 500 l statt Beton-Wanne ...)".
2. `BEH-ibc-1000l`, `BEH-ibc-beetwanne`: Rekubik steht auf `lieferung_de: nein` mit "NICHT BESTELLBAR am 05.11.2026"; `bom.py` waehlt es damit nicht.

Neu, bestaetigt:
1. `PMP-teichpumpe-5300` (2 Stk, Beet-Sumpf): Oase AquaMax Eco Classic 5500. OBI DE 220,49, Galaxus DE 365,15. Die Kennlinie bei 2 m Foerderhoehe liegt laut UK-Seite nur bei 1500 l/h; Hydraulik R45 gegen diese Kennlinie pruefen (DEINE ENTSCHEIDUNG / Planer).
2. `BEH-tank-pe-580x865` (Schlammfass): Rekubik DE 74,99 (580 x 980, lebensmittelecht ja), faesser.de-Datenblatt, toom/Graf. OFFEN (Ben): Mass 580 x 980 statt 580 x 865; alle 220-l-Faesser sind 978 bis 980 hoch.
3. `BEH-fass-pe-60l` (neu, Biofilter Drittbecken): Graf 824410 (d398 x 615, passt zur Massskizze). richter & hess DE 39,07 (gerechnet), eBay-Haendler DE 39,36. Verschluss ist ein Spannring, kein Schraubdeckel.

Neu, OFFEN:
1. `BEH-tank-pe-800x1000` (Beet-Sumpf-Tank): kein 500-l-Erdtank d800 x 1000. Naechstes Handelsmass tanksdirekt RPV 500 l, 700 x 700 x 1460 (281,79), nur eine Quelle, nur fuer stehende Aufstellung beschrieben. OFFEN (Ben): Mass oder Sonderanfertigung.
2. `BEH-pe-schachtaufsatz-600x200`: nur ein Haendler (Rewatec VS 20, baustoffshop.de 144,95 plus 49 Versand), Hoehe 200 oder 250 widerspruechlich. OFFEN (Ben): Mass.
3. `BEH-tank-pe-700-deckel`: kein Handelsdeckel d700 x 40 mit vier Durchbruechen. Vorschlag Standard-Domdeckel d600 mit selbst gesetzten Durchbruechen.
4. `BEH-tank-pe-580-deckel`, `BEH-fass-pe-60l-deckel`: im Fass-Satz enthalten; Spannring-Werkstoff nicht belegt.

Hinweise an die Werkstatt und die Gruppe E:
1. `BEH-fass-pe-60l` und `BEH-fass-pe-60l-deckel` sind neue Artikel-IDs von mir und stehen noch nicht in `data/stueckliste.json`; `bom.py` muss danach neu laufen und die Komponente `biofilter_dritt` den IDs zuordnen.
2. Bioballs (`TOP-biomedium`) liegen in `huelle_pflanze.json` (Gruppe E), nicht hier. Befund der Recherche: Bioballs in Litergebinden sind nicht zu finden; Vorschlag Oase Hel-X 13 Biomedium (baustoffshop.de DE 25 l = 43,40 plus 6,90 Versand, vijverleven.nl NL 100 l = 209). Das ist Bewegtbett-Medium statt starrer Bioballs; das Volumen 37 l ist neu zu bewerten, Lebensmitteleignung nicht belegt. Weitergabe an Gruppe E durch den Orchestrator.

Geprueft gegen: `data/beschaffung/behaelter.json` per Skript (28 Zeilen, jede mit Angebot oder `luecke`), drei Agentenberichte mit geoeffneten Seiten, `docs/jobs/N-PREIS-PRUEF.md`, D76
Offen: siehe Listen oben
