# Pruefung N-PREIS-PRUEF (Pruefer, 05.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md` und `docs/jobs/start/N-REWORK-folge.md` Abschnitt E. Gegenstand: Blatt `docs/jobs/N-PREIS-PRUEF.md` (Pruefpunkte 1 bis 5), Stand Commit 7d3fd5d (Start-Commit der Recherche: d23125f). Ich habe nichts davon gebaut. Alle Zahlen sind in dieser Sitzung neu gemessen, in einer Kopie `git archive 7d3fd5d` im Scratchpad (`viewer/instances.json` aus dem Arbeitsbaum dazu, da nicht versioniert); geschrieben ist nur diese Datei. Seiten wurden von zwei Lese-Helfern geoeffnet (nur lesen); ihre Angaben sind unten als solche gekennzeichnet.

## Urteil: PASS mit Auflagen

Alle fuenf Pruefpunkte sind nach Wortlaut des Blatts erfuellt oder mit einer benannten Form-Abweichung erfuellt. Die Stichproben zeigen aber, dass "OK" aus `check_links.py` nicht "passt" heisst: Bei 3 von 11 zufaelligen OK-Zeilen weicht das Angebot vom Bauteil ab oder ist nicht lesbar, und die NFT-Rinne steht in der Einkaufsliste noch mit dem alten Mass und der falschen Lagerlaenge.

## Pruefpunkte

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | Platzierte Zeilen mit Hauptangebot FEHLER = 0; VERDACHT/GESPERRT je mit Notizzeile "von Hand gelesen <Datum>: passt, weil ..." | `python -X utf8 scripts/check_links.py` (Kopie, Exit 0): "Zeilen 273, mit Link 168, Links 289, URLs 241, OK 189, GESPERRT 13, VERDACHT 87"; `python -c` ueber `data/preis_pruefung_links.json` `link_liste`, `rang == "1"`, platziert nach `stueckliste.json` (`nicht_platziert` nicht gesetzt) | 136 platzierte Zeilen, 93 mit Hauptangebot: 67 OK, 22 VERDACHT, 4 GESPERRT, **0 FEHLER**. Fuer die 26 VERDACHT/GESPERRT hat nur ein kleiner Teil (BEH-fass-hdpe, drei MES-Zeilen) eine Notiz mit dem Wortlaut "von Hand gelesen"; alle 26 stehen aber mit Entscheidung in einer Gruppen-Notiz (ersetzt, bestaetigt oder OFFEN mit Grund; 21 davon OFFEN, nicht "passt") | PASS fuer FEHLER = 0; Wortlaut-Teil nur teilweise, Ziel-Satz (OK oder benannter Grund) erfuellt (Auflage 1) |
| 2 | `PRF-pvcu-rinne-130x100`: kein "Kabelkanal"; zwei NFT-Kanal-Angebote mit Europa-Bezug oder OFFEN | `grep -c Kabelkanal data/beschaffung/stahl.json`; `python -c` ueber `stahl.json` | 0 Treffer "Kabelkanal"; zwei Angebote (GrowKing24, Golden Green Club), Urban Hydro 100x50, Art.-Nr. 23644, `luecke` mit OFFEN (Ben) Mass, OFFEN (Quelle) Eignung und Lagerlaenge. Beide Seiten geoeffnet: 100x50 mm, UPVC, innen weiss, 290 cm, 24,40 EUR (GrowKing24, = 8,41 EUR/m) und 20,77 EUR (Golden Green Club, = 7,16 EUR/m); keine Zertifizierung genannt; Versand nach DE nur bei GrowKing24 ausdruecklich | PASS (Auflage 2 zur Anzeige) |
| 3 | Jedes neue oder ersetzte Angebot hat zwei unabhaengige Quellen | Python-Diff der `angebote[].url` je Artikel zwischen `d23125f` und `7d3fd5d` ueber alle fuenf Dateien | 101 Zeilen mit neuen Angebots-URLs; 86 davon mit mindestens zwei Angeboten auf verschiedenen Domains (0 mit gleicher Domain); 15 mit nur einem Angebot, alle 15 tragen `luecke` "OFFEN (Quelle): zweite Quelle ..." (Bevo-Rohre d20 bis d75, Bevo-Bulkheads d40/d63/Pool, Kugelhahn d110, Lochblech Medienschutz, Geblaese, Schaltschrank, drei Huelle-Zeilen). Stichprobe 7 Zeilen mit je zwei Angeboten per Seitenabruf: siehe Stichproben | PASS mit Auflagen (3, 4) |
| 4 | Wasser-/Pflanzenkontakt (ROH, FIT, ARM, BEH, PRF, FOL, TOP): Spalte "Lebensmittel" `belegt` oder Notiz "OFFEN (Quelle): Eignung nicht angegeben" | `python -c` ueber `plausi[]` (`lebensmittel`) fuer platzierte Zeilen dieser Typen; `grep -i Eignung docs/session-notes/n-preis-pruef-*.md` | 77 platzierte Zeilen: 4 `belegt` (BEH), 73 `OFFEN` (FIT 34, ROH 10, ARM 8, BEH 8, PRF 7, FOL 3, TOP 3). Die Notizen nennen den Satz gruppenweise: Leitung "Rohre, Fittings", Behaelter "Tanks, Faesser, IBC, Aktivkohle ... Scheibenbeluefter, Sedimentfilter, PP-C-Becken", Huelle "Blaehton, Netztopf, Folie", Stahl "NFT-Kanal, PP-Platten". Armaturen (ARM) und Stahlprofile (PRF) sind nicht ausdruecklich benannt | PASS mit Auflage (5) |
| 5 | `check_bom.py` Exit 0; `docs/einkaufsliste.html` zeigt die Summe von `data/stueckliste.json` (Screenshot) | `python -X utf8 scripts/check_bom.py` (Kopie); Browser-Pane `file:///.../docs/einkaufsliste.html`, Screenshot | "14 von 14 Pruefungen PASS", Exit 0. Seite: 26.870,92 EUR, 136 Zeilen im Modell, 43 Preis fehlt, 137 nur in nicht platzierten Komponenten; `stueckliste.json`: `summe_eur_platziert` 26870.92, 136 platziert (273 - 137), 43 ohne Preis. Gleich | PASS (Auflage 6: Drift-Hinweis) |

## Stichproben

Zufallsauswahl (`random.seed(68)`, 2 platzierte Zeilen mit Hauptangebot OK je Gruppe; Mess/Elektrik hat nur 1 solche Zeile) und 7 Zeilen mit je zwei Angeboten aus dem Diff. Die Seiten wurden von Lese-Helfern geoeffnet; wo eine Seite 403 oder 429 lieferte, steht "nicht lesbar".

OK-Zeilen (11 Seiten):
1. `FIT-stutzen-d40` (Schwarte 75276): PVC-U, d40 mit 1 1/4"-Aussengewinde, 2,95 EUR: PASST.
2. `FIT-t-d63` (Schwarte 75047): die Seite beschreibt ein **reduziertes** 90-Grad-T, Abzweigmass nicht genannt: UNKLAR, ob gleich grosses T d63 gemeint ist. Dasselbe bei `FIT-t-d50` (Schwarte 75046, Baenninger, "T-Stueck 90 Grad reduziert"); die Bevo-Zweitquelle dort ist ausdruecklich 50/50/50.
3. `BEH-ibc-beetwanne` (Fasswulf): neuer IBC 1000 l HDPE, FDA ja, 229,94 EUR brutto, transparenter Innenbehaelter: PASST (Algenrisiko als Hinweis).
4. `PMP-pumpe-gross` (Green Aqua, Budapest): Eheim Universal 3400, 210,41 EUR, EU-Versand: PASST.
5. `ELE-kabelverschraubung-pg` (el12): **HTTP 403, nicht lesbar**; `check_links.py` hatte sie als OK. Die Zweitquelle Tameson ist eine US-Storefront (USD, nur Gewerbekunden, DE-Versand nicht angezeigt): Europa-Bezug nicht belegt.
6. `SON-spannverschluss-edelstahl` (schraubbar.de, Ganter GN 927.7): Hebel 1.4308, Achse 1.4305, nicht 1.4301 wie in der Zeile: **PASST NICHT** bei strenger Lesart (bei allgemeiner Edelstahl-Vorgabe verwendbar); Seite nennt keinen "Bock".
7. `TOP-blaehton` (Natursteinzentrum): Lecaton 8-16 mm, Big Bag: PASST; Gebindeangabe widerspruechlich (1 t gegen 1,5 m3 bei 350 kg/m3), vor Kauf klaeren.
8. `PRF-v2a-voll8x8` (stahl-shop24): 8x8, 1.4301, 6,12 EUR/m: PASST.
9. `SRB-satz-m10x60` (Schraubenking AT): M10x60, DIN 933, verzinkt, 8.8; Angebot ist nur Schraube im 10er-Los (2,76 EUR je 10), keine Mutter/Scheiben: PASST fuer die Schraube.
10. und 11. NFT-Rinne: siehe Punkt 2. Beide Seiten fuehren dieselbe Art.-Nr. 23644, "ohne Loch" und "mit Loch" lassen sich laut Seitentext nicht sicher unterscheiden; Golden Green Club weist die MwSt. nicht aus.

Zeilen mit zwei Angeboten (Punkt 3):
1. `SRB-satz-m6x16`: Hornbach (5,75 EUR je 100 Stk) und Schraubenking (0,92 EUR je 10 Stk) bestaetigen Mass und Werkstoff; die Zeile rechnet "je Satz" (Schraube + Mutter + 2 Scheiben) mit 0,13 und 0,07 EUR, Seitenpreise gelten nur fuer die Schraube: Einheit nicht vergleichbar. Zwei Haendler: ja.
2. `FIT-t-d50`: Bevo 50/50/50 PASST, Schwarte UNKLAR (reduziert). **Preisbasis:** Die Liste fuehrt Bevo 4,08 EUR als "netto"; die Seite nennt 3,43 EUR netto, 4,08 entspricht 3,43 x 1,19, also brutto mit deutscher MwSt. Gleiches bei `FIT-bogen90-d40`: Bevo 6,55 gegen 5,50 EUR netto (5,50 x 1,19).
3. `FIT-bogen90-d40`: Schwarte 3,01 EUR passt, Bevo passt: zwei Haendler (Baenninger, VDL).
4. `BEH-ibc-1000l`: Fasswulf PASST; Rekubik (299,99 EUR, "lebensmittelecht ja") ist derzeit **nicht bestellbar**; Faesser.de als dritte Quelle nicht geoeffnet.
5. `ELE-kabelverschraubung-pg`: siehe oben, eine Quelle nicht lesbar, eine ausserhalb Europas.
6. `MES-leck`: beide Seiten nicht lesbar (Shelly 429, Domadoo 403); beide sind dieselbe Marke (Hersteller und Wiederverkaeufer), also nicht unabhaengig im Sinn zweier Hersteller.
7. `BEH-drittbecken-klein` (Zeile: Beton, 920x920x1055): beide Angebote sind PE-Dosierbehaelter 500 l (ANDO 740 x 1230 mm, DENIOS ohne Masse): **PASST NICHT** (Werkstoff und Mass); in der Notiz als OFFEN (Ben) Mass und Werkstoff gefuehrt, im Angebot nicht als Ersatz gekennzeichnet.

## Nicht belegte oder nicht nachgemessene Behauptungen

1. Konfidenz "Q" in den Angeboten: je Angebot nur die Stichproben oben geoeffnet; 25 Seiten geoeffnet (4 davon nicht lesbar), die uebrigen Angebote nicht.
2. Lebensmitteleignung: kein Normbeleg (KTW, W270, EU 10/2011) in irgendeiner Zeile geprueft; offen, Entscheidung bei Ben.
3. Preise: nur Stichproben gegen die Seite (siehe oben); Bevo-Preisbasis netto/brutto nicht flaechig geprueft.
4. Browser-Screenshot der Einkaufsliste nur der obere Seitenteil; die NFT-Zeile per Seitentext gelesen, nicht per Bild.
5. Erreichbarkeit schwankt: `check_links.py` meldete 13 GESPERRT (vorher 32), el12 war in der Stichprobe 403 und gilt in der Messung als OK.

## Auflagen

1. Die Wortlaut-Regel aus Punkt 1 ("von Hand gelesen <Datum>: passt, weil ...") entweder einheitlich nachtragen oder im Blatt auf "Entscheidung je Zeile in der Gruppen-Notiz" lockern. Owner: Orchestrator.
2. NFT-Rinne in der Einkaufsliste: Bezeichnung steht noch "NFT-Rinnenprofil PVC-U 130x100", Kauf rechnet 154 m in 22 Stangen a 7000 mm, Preis 1.102,64 EUR aus 7,16 EUR/m. Echte Lieferlaenge 2,9 m (Segmente 1,25 m): Kaufmenge und Bezeichnung an Angebot und OFFEN-Grund angleichen oder die Zeile in der Anzeige als OFFEN kennzeichnen. Owner: Werkstatt (`bom.py`, nach Freigabe durch Ben fuer das Mass).
3. Schwarte-T-Stuecke d50 und d63 sind laut Seitentext reduzierte T-Stuecke; gleich grosse T-Stuecke (Bevo) als Hauptangebot oder Schwarte-Variante klaeren. Owner: Recherche Leitung.
4. Preisbasis der Bevo-Angebote: Bemerkung "netto" gegen den Listenpreis (brutto mit 19 %) vereinheitlichen; Schraubensaetze (Einheit "Satz") gegen den Seitenpreis je Schraube ueberpruefen. Owner: Recherche Leitung und Stahl.
5. Lebensmittel-Hinweis auch fuer Armaturen (ARM) und Stahlprofile in der Gruppen-Notiz ausdruecklich benennen; Entscheidung OFFEN (Ben) 1 steht weiter. Owner: Recherche Leitung/Stahl, Entscheidung Ben.
6. `stueckliste.json` meldet `drift: true` (gebaut mit `sc_sha256` 4aef..., aktuell 938f...): Liste nach dem letzten `.sc`-Stand neu erzeugen, bevor sie fuer die Ausfuell-Tabelle (W65) dient. Owner: Werkstatt.
7. Einzelmaengel: `SON-spannverschluss-edelstahl` (1.4308/1.4305 statt 1.4301) und `BEH-drittbecken-klein` (PE-Behaelter statt Beton) als Abweichung im Angebot kennzeichnen; `ELE-kabelverschraubung-pg` zweite Quelle mit Europa-Lieferung suchen; `BEH-ibc-1000l` Rekubik nicht bestellbar. Owner: Recherche.

Geprueft gegen: `python -X utf8 scripts/check_links.py` (Kopie 7d3fd5d), `python -X utf8 scripts/check_bom.py` (14/14, Exit 0), Python-Auswertung von `data/preis_pruefung_links.json`, `data/stueckliste.json`, `data/beschaffung/*.json` (Diff d23125f..7d3fd5d), `docs/session-notes/n-preis-pruef-*.md`, `docs/einkaufsliste.html` im Browser-Pane (Screenshot), 25 Produktseiten ueber Lese-Helfer (4 nicht lesbar).
Offen: Auflagen 1 bis 7 (Owner je Auflage genannt); nicht gemessen: Normbelege Lebensmitteleignung, Preise ausserhalb der Stichprobe, Bevo-Preisbasis flaechig.
