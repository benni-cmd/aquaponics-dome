# N-PREIS-PRUEF: Einzelteilpruefung der Preisliste (W69)

**Problem:** Die Einkaufsliste (`docs/einkaufsliste.html`, `data/stueckliste.json`) enthaelt tote Links und Artikel, die nicht zum Bauteil passen. Beleg: Die NFT-Rinne `PRF-pvcu-rinne-130x100` ist mit Kabelkanaelen 110x60 und 100x60 belegt (`data/beschaffung/stahl.json` Zeile 1095 bis 1121).
**Intent:** Jede Zeile soll ein real bestellbares, zum Bauteil passendes Teil sein, damit die Liste und die spaetere Ausfuell-Tabelle (W65) belastbar sind.
**Ziel in einem Satz:** Nach Recherche, Werkstatt und Pruefer meldet `python -X utf8 scripts/check_links.py` fuer jedes Hauptangebot einer platzierten Zeile OK oder einen von Hand belegten Grund, und jede andere Zeile traegt einen benannten OFFEN-Grund.

## Aktualitaetspruefung (05.11.2026, Planer)
Ergebnis: **angepasst**.
1. Roadmap `N-PREIS-PRUEF` (status geplant, reihenfolge 3.94, vor W65): gilt.
2. `docs/decisions.md` D76 (mindestens Europa) und D80 (bis 5 Sitzungen zugleich): gelten, keine neue Entscheidung zur Preisliste.
3. `git log`: Commit 1c966cd stellt die Strebe auf Vierkantrohr 30x30x3 um (N-MODELL-KOMPLETT Schritt 2). Die Strebe kann dadurch einen neuen Stahl-Artikel bekommen, sobald die `.sc` neu gebaut und `bom.py` neu gelaufen ist. Die Sitzung Stahl prueft diesen Artikel mit, wenn er bei ihrem Start in `data/stueckliste.json` steht.
4. Gegen den Start-Auftrag angepasst: Der Start-Auftrag nennt 172 Zeilen mit Link. Gemessen sind 172 Zeilen mit mindestens einem Link, davon 166 mit Link im Hauptangebot. 24 Zeilen ohne Bezugsdatei (`quelle_preis` leer) werden unten einer Gruppe zugeordnet.

## Messlauf (vom Planer gelaufen)
Befehl: `python -X utf8 scripts/check_links.py` (Standardbibliothek, 8 parallele Abrufe, etwa 1 min). Das Skript schreibt `docs/preis-pruefung-links.md` (Tabelle) und `data/preis_pruefung_links.json` (Rohdaten).
Urteile:
- **FEHLER:** HTTP-Fehler, Netzfehler oder Weiterleitung auf Startseite, Suche oder Kategorie.
- **GESPERRT:** HTTP 401, 403 oder 429. Die Seite blockt Skripte und muss von Hand geoeffnet werden (Kaufland, eBay, RS, DigiKey, ManoMano, RobotShop).
- **VERDACHT:** Ein Kennmass der Bezeichnung fehlt in Titel oder URL der Seite, oder die Bemerkung des Angebots sagt selbst ERSATZ.
- **OK:** sonst.

Messung vom 05.11.2026 ueber 260 Zeilen, 289 Links und 212 eindeutige URLs: 6 FEHLER, 32 GESPERRT, 127 VERDACHT, 124 OK.

Hauptangebote je Gruppe (Rang 1). Gezaehlt nach Zeilen, Messung per `python -c` ueber `data/preis_pruefung_links.json`:

| Gruppe, Datei | Zeilen | platziert | ohne Link | FEHLER | GESPERRT | VERDACHT | OK | platziert und nicht OK |
|---|---|---|---|---|---|---|---|---|
| A Stahl und Normteile, `stahl.json` | 38 (+8 SRB ohne Datei) | 25 (+6) | 3 (+8) | 1 | 0 | 26 | 8 | 20 (+6) |
| B Leitung, `leitung.json` | 119 (+4 ARM/FIT ohne Datei) | 51 | 33 (+4) | 0 | 0 | 29 | 57 | 25 |
| C Behaelter, Pumpen, `behaelter.json` | 19 (+10 ohne Datei) | 15 | 7 (+10) | 0 | 3 | 4 | 5 | 11 |
| D Mess und Elektrik, `mess_elektrik.json` | 20 (+2 ohne Datei) | 10 | 2 (+2) | 0 | 9 | 6 | 3 | 10 |
| E Huelle, Pflanze, `huelle_pflanze.json` | 40 | 23 | 25 | 2 | 5 | 4 | 4 | 19 |

Typische Befunde:
1. Die NFT-Rinne ist mit Kabelkanaelen belegt (VERDACHT, Bemerkung ERSATZ).
2. Alternativangebote bei Bevo zeigen oft auf einen anderen Durchmesser, zum Beispiel `ARM-kugelhahn-d20` auf einen 32-mm-Kugelhahn, `FIT-t-d20` auf ein 75-mm-T-Stueck und `ROH-pvcu-d75` auf ein 25-mm-Rohr.
3. Einige Links zeigen auf Kategorieseiten statt auf Artikel (stahlshop.de/stahlplatten, metallparadies, polyvantis-shop.com).
4. Zwei Folien-Links zeigen auf die Startseite (`FOL-pe-plane`, stretchfolie.eu und norhage.de). Das Lochblech bei Amazon liefert 404.
5. Lebensmitteleignung ist bei 0 von 222 Zeilen mit Wasser- oder Pflanzenkontakt belegt. Europa-Bezug fehlt bei 0 Hauptangeboten.

Grenze des Messlaufs: VERDACHT ist ein Filter, kein Urteil. Konfigurierbare Shopseiten (metallparadies, stahl-shop24 mit Zuschnitt) nennen das Mass oft erst nach der Auswahl. OK heisst nur, dass die Seite erreichbar ist und das Mass nennt. Ob der Artikel funktional passt, prueft erst die Fachrecherche.

## Eingaben
1. `docs/preis-pruefung-links.md`: Abschnitt "Links je Angebot" (gefiltert auf die eigene Bezugsdatei) und Abschnitt "Plausibilitaet je Zeile" (Mass, Einheit, Werkstoff, Lebensmittel, Europa, Ersatz).
2. `data/preis_pruefung_links.json`: `link_liste[]` mit `urteil`, `grund`, `titel` und `ziel`; `plausi[]` je Zeile.
3. `data/stueckliste.json` `zeilen[]`: `artikel_id`, `bezeichnung`, `masse`, `einheit`, `werkstoff`, `bedarf`, `nicht_platziert`, `verwendung`. Nur per Python lesen, die Datei ist 534 kB gross.
4. Die eigene Bezugsdatei `data/beschaffung/<gruppe>.json`. `leitung.json` traegt `artikel` als Liste mit `id`, die anderen vier Dateien als Objekt mit der Artikel-ID als Schluessel.
5. Bei Bedarf Funktion und Mass des Bauteils aus `data/parts/<komponente>.json`, gesucht ueber `verwendung[].komponente`.
6. Regeln: D76 in `docs/decisions.md` (mindestens Europa), zwei unabhaengige Quellen (Arbeitsregel), `docs/arbeitsweise-sitzungen.md` Abschnitt 4 (Kontext- und Limitgrenzen).

## Gruppenzuordnung der 24 Zeilen ohne Bezugsdatei
Diese Zeilen haben kein `quelle_preis`. Die jeweilige Sitzung legt sie in ihrer Datei neu an; `bom.py` liest alle `data/beschaffung/*.json`.
- **A Stahl:** `SRB-satz-m5x12`, `SRB-satz-m6x16`, `SRB-satz-m6x40`, `SRB-satz-m6x55`, `SRB-satz-m8x30`, `SRB-satz-m10x60`, `SRB-satz-m12x55`, `SRB-satz-m16x300`. Davon sind 6 platziert.
- **B Leitung:** `ARM-durchflussbegrenzer-messing`, `ARM-probehahn-messing`, `ARM-schwimmerventil-pool`, `FIT-red-d32-d25`, `FIT-stutzen-d25`.
- **C Behaelter, Pumpen:** `BEH-ak-kompositbehaelter-254x790`, `BEH-ak-sedimentfilter`, `TOP-aktivkohle`, `PMP-geblaese-luft`, `SON-ak-konsole`, `SON-gummifuss-40`, `SON-luftverteiler-4`, `SON-luftverteiler-6`, `SON-scheibenbelueftung-270`.
- **D Mess und Elektrik:** `BLE-schrankboden-3x500x800`, `SON-schrankwand-500x800`.

## Schritte
Schritte 1A bis 1E laufen parallel als je eine Sitzung (D80: hoechstens 5 zugleich). Schritt 2 startet erst nach allen fuenf, Schritt 3 danach. Jeder Schritt ist einzeln committbar.

**1A bis 1E Fachrecherche je Gruppe** (Rolle Recherche; schreibt NUR die eigene Datei `data/beschaffung/<gruppe>.json` und die Notiz `docs/session-notes/n-preis-pruef-<gruppe>.md`):
1. Reihenfolge innerhalb der Gruppe:
   1. platzierte Zeilen mit FEHLER
   2. platzierte Zeilen mit VERDACHT
   3. platzierte Zeilen mit GESPERRT
   4. platzierte Zeilen ohne Link
   5. Alternativangebote mit FEHLER oder VERDACHT
   6. nicht platzierte Zeilen, nur wenn Kontext uebrig ist (Grenze 40 Prozent)
2. Je Zeile die Seite oeffnen (WebFetch, bei 403 Browser-Pane nur lesen) und Funktion, Mass, Einheit, Werkstoff, Lebensmittel- oder Trinkwassereignung bei Wasser- oder Pflanzenkontakt sowie Europa-Bezug gegen die Zeile pruefen.
3. Passt das Angebot, `konfidenz` auf `Q` setzen und `stand` auf das Datum. Gelesene Fakten in die `bemerkung`.
4. Passt es nicht, ein Ersatzangebot mit **zwei unabhaengigen Quellen** suchen: zwei Haendler oder Haendler plus Herstellerdatenblatt, je Seite geoeffnet. Mindestens eine Quelle muss in Europa liefern (D76). Das alte Angebot faellt weg; der Grund steht in der Notiz.
5. Ohne zwei Quellen `angebote` leer lassen und `luecke` auf "OFFEN (Quelle): <Grund>" setzen, zum Beispiel "kein NFT-Profil 130x100 in EU gefunden, naechstes 100x50".
6. Weicht das Mass des Kaufteils vom Modell ab (zum Beispiel NFT-Rinne 130x100 gegen marktuebliches 100x50), NICHT das Modell aendern. Die Abweichung kommt als "OFFEN (Ben): Mass" in die Notiz.
7. Fallen fuer einzelne Gruppen:
   - **A:** NFT-Rinne ist der Belegfall fuer Ben. Echte NFT-Kanaele (lebensmittelechtes PVC/ABS) suchen, keine Kabelkanaele. SRB-Saetze sind Normteile DIN 933/934/125, verzinkt.
   - **B:** Bevo-Alternativen mit falschem Durchmesser auf die richtige Variante setzen; die Bevo-Seite traegt die Nennweite im Titel.
   - **C:** IBC und Faesser mit Lebensmittelvorgeschichte belegen.
   - **D:** 9 von 10 platzierten Hauptangeboten sind GESPERRT und muessen von Hand gelesen werden.
   - **E:** `FOL-pe-plane` hat zwei Startseiten-Links; das Lochblech bei Amazon liefert 404.

**2 Werkstatt** (eine Sitzung, nach 1A bis 1E):
1. Ausfuehren:
   1. `python -X utf8 scripts/bom.py`
   2. `python -X utf8 scripts/check_bom.py`, Exit 0
   3. `python -X utf8 scripts/check_links.py`
2. `docs/preis-pruefung-links.md` und `data/preis_pruefung_links.json` neu erzeugt committen, ebenso `data/stueckliste.json` und `docs/einkaufsliste.html`.
3. Liefert der zweite Lauf neue FEHLER oder VERDACHT bei platzierten Hauptangeboten, gehen diese als Liste je Gruppe in die Notiz `docs/session-notes/n-preis-pruef-werkstatt.md`. Die Werkstatt recherchiert nicht selbst.
4. Seite `docs/einkaufsliste.html` per Screenshot im Browser-Pane pruefen: Summe, Zaehler "Preis fehlt", NFT-Rinne-Zeile.

**3 Pruefer** (fremde Sitzung, Vorlage `docs/jobs/vorlagen/pruefung.md`; schreibt `docs/jobs/pruefung/N-PREIS-PRUEF.md`):
1. Pruefpunkte unten nachmessen.
2. Eigene Stichproben: je Gruppe zwei zufaellige platzierte Zeilen mit OK selbst oeffnen und Funktion, Mass und Werkstoff gegen die Zeile pruefen, also 10 Zeilen. Dazu die NFT-Rinne.

## Nicht anfassen
1. Modell (`.sc`, `scripts/components/`), `viewer/`, `data/parts/`, `data/roadmap.json`.
2. Die Beschaffungsdatei einer anderen Gruppe.
3. `scripts/bom*.py` und `scripts/check_links.py`. Mangel am Skript als Notiz an den Orchestrator.
4. Fremde, nicht committete Dateien im Arbeitsbaum (heute `renders/check_latte-69.txt` und `viewer/detail/`).
5. Nichts kaufen, nirgends anmelden, keine Formulare, keine Cookie-Zustimmung ausser "nur notwendige".

## Ergebnis
- `data/beschaffung/{stahl,leitung,behaelter,mess_elektrik,huelle_pflanze}.json` korrigiert.
- Fuenf Notizen `docs/session-notes/n-preis-pruef-<gruppe>.md` mit den Listen "ersetzt", "bestaetigt", "OFFEN mit Grund" und "OFFEN (Ben)".
- `data/stueckliste.json`, `docs/einkaufsliste.html`, `docs/preis-pruefung-links.md`, `data/preis_pruefung_links.json` neu erzeugt.
- Befund `docs/jobs/pruefung/N-PREIS-PRUEF.md`.

## Pruefpunkte (fremd nachmessbar)
1. `python -X utf8 scripts/check_links.py`: Platzierte Zeilen mit Hauptangebot FEHLER = 0. Platzierte Zeilen mit Hauptangebot VERDACHT oder GESPERRT haben je eine Zeile in der Gruppen-Notiz mit "von Hand gelesen <Datum>: passt, weil ...". Messung per `python -c` ueber `data/preis_pruefung_links.json` `link_liste`, `rang == "1"`.
2. `PRF-pvcu-rinne-130x100`: Kein Angebot mit "Kabelkanal" in `data/beschaffung/stahl.json`. Entweder zwei NFT-Kanal-Angebote mit Europa-Bezug oder `luecke` "OFFEN (Quelle)". Messung: `python -c` ueber `stahl.json`.
3. Jedes neue oder ersetzte Angebot hat zwei unabhaengige Quellen, entweder als zwei `angebote` verschiedener Haendler oder als Haendler plus Datenblatt in der `bemerkung`. Messung: Diff `git diff <Start-Commit>..HEAD -- data/beschaffung/` gegen die Notizen, Stichprobe 10 Zeilen.
4. Wasser- und Pflanzenkontakt: Spalte "Lebensmittel" in `docs/preis-pruefung-links.md` ist fuer platzierte Zeilen der Typen ROH, FIT, ARM, BEH, PRF, FOL, TOP `belegt` oder in der Notiz als "OFFEN (Quelle): Eignung nicht angegeben" benannt. Sollwert: kein platziertes Teil mit Wasserkontakt ohne einen der beiden Eintraege.
5. `python -X utf8 scripts/check_bom.py` mit Exit 0. `docs/einkaufsliste.html` zeigt dieselbe Summe wie `data/stueckliste.json` (Screenshot).

## OFFEN (Ben)
1. **Lebensmitteleignung:** Muss sie fuer alle Teile mit Wasser- oder Pflanzenkontakt per Hersteller belegt sein (Trinkwasser-Zulassung, KTW/W270 oder EU 1935/2004), oder reicht "Werkstoff PVC-U/PE/PP ohne Weichmacher"? Empfehlung: Beleg nur fuer Teile im Fischwasser (Becken, Rohre, Rinnen, Folie), Werkstoffangabe fuer den Rest. Bis zur Entscheidung tragen die Sitzungen den Befund ein und ersetzen nichts nur wegen fehlenden Belegs.
2. **Massabweichung Kaufteil gegen Modell:** Darf die Recherche ein marktuebliches Mass vorschlagen (zum Beispiel NFT-Kanal 100x50 statt 130x100), das spaeter das Modell aendert? Empfehlung: ja, als Vorschlag in der Notiz. Das Modell aendert nur ein eigener Schritt.

## Start-Hinweis fuer die Bau-Sitzungen
1. Erst `docs/preis-pruefung-links.md` nach der eigenen Datei filtern (`grep "<gruppe>.json"`), nicht ganz lesen.
2. eBay, Kaufland, RS, DigiKey, ManoMano und RobotShop antworten Skripten mit 403. Diese Seiten mit dem Browser-Pane lesen, nichts anklicken ausser "nur notwendige Cookies".
3. VERDACHT ist ein Filter. Konfigurierbare Zuschnitt-Shops nennen das Mass erst nach der Auswahl; dort den Konfigurator lesen, nicht abschicken.
4. Parallel arbeitende Sitzungen schreiben nie dieselbe Datei. `bom.py` laeuft nur in Schritt 2, nicht in 1A bis 1E.
5. Limit: Fuenf Recherchen zugleich sind teuer. Ab 85 Prozent Planlimit startet der Orchestrator hoechstens 2 (D80). Jede Sitzung committet nach jeweils etwa 10 Zeilen.
