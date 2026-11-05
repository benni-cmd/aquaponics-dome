# Work package: N-PREIS-PRUEF Einzelteilpruefung der Preisliste (W69)

**Problem:** Die Einkaufsliste enthaelt tote Links und unpassende Artikel, zum Beispiel einen Kabelkanal 110x60 statt der NFT-Rinne 130x100 (`data/beschaffung/stahl.json` `PRF-pvcu-rinne-130x100`).
**Intent:** Ben (W69, 05.11.2026) will, dass jede Zeile ein real bestellbares, zum Bauteil passendes Teil mit Bezug mindestens aus Europa (D76) ist, damit die Liste und die Ausfuell-Tabelle W65 belastbar sind.
**Goal:** `python -X utf8 scripts/check_links.py` meldet 0 FEHLER bei platzierten Hauptangeboten. Jeder VERDACHT und jedes GESPERRT ist von Hand belegt. Die NFT-Rinne ist kein Kabelkanal mehr. Der Pruefer hat 5 von 5 Pruefpunkten gemessen. Blatt: `docs/jobs/N-PREIS-PRUEF.md`

## Plan
1. [x] Planer: Link-Messlauf `scripts/check_links.py`, Tabelle `docs/preis-pruefung-links.md`, Auftragsblatt (05.11.2026)
2. [x] Fachrecherche 1A Stahl und Normteile (`data/beschaffung/stahl.json`, plus 8 SRB-Saetze)
3. [x] Fachrecherche 1B Leitung (`leitung.json`, plus 5 ARM/FIT)
4. [x] Fachrecherche 1C Behaelter, Pumpen (`behaelter.json`, plus 9 Aktivkohle/Luft)
5. [x] Fachrecherche 1D Mess und Elektrik (`mess_elektrik.json`, plus 2 Schrank)
6. [x] Fachrecherche 1E Huelle, Pflanze (`huelle_pflanze.json`)
7. [x] Werkstatt 2 (05.11.2026, Notiz `docs/session-notes/n-preis-pruef-werkstatt.md`): `bom.py`, `check_bom.py` mit Exit 0, `check_links.py` erneut, Screenshot der Seite
8. [ ] Pruefer 3: `docs/jobs/pruefung/N-PREIS-PRUEF.md`, 5 Pruefpunkte und 10 Stichproben

Reihenfolge: Schritte 2 bis 6 laufen parallel (D80, hoechstens 5 zugleich). Schritt 7 folgt nach allen fuenf, Schritt 8 zuletzt.

## Stand
05.11.2026, Planer (Opus 5.5). Aktualitaet **angepasst**: Die Strebe ist seit 1c966cd ein Vierkantrohr 30x30x3 und kann einen neuen Stahl-Artikel bringen. 24 Zeilen ohne Bezugsdatei sind den Gruppen zugeordnet.

Messlauf `python -X utf8 scripts/check_links.py` ueber 260 Zeilen, 172 davon mit Link, 289 Links, 212 URLs:
- 6 FEHLER
- 32 GESPERRT
- 127 VERDACHT
- 124 OK

Lebensmitteleignung ist bei 0 von 222 Zeilen mit Wasser- oder Pflanzenkontakt belegt. Kein Hauptangebot liegt ausserhalb Europas.

Platzierte Zeilen, deren Hauptangebot nicht OK ist:
- Stahl: 26
- Leitung: 25
- Behaelter: 11
- Mess und Elektrik: 10
- Huelle, Pflanze: 19

OFFEN (Ben):
1. Muss die Lebensmitteleignung per Hersteller belegt sein? Empfehlung: nur fuer Teile im Fischwasser.
2. Darf die Recherche ein marktuebliches Mass vorschlagen, zum Beispiel NFT-Kanal 100x50 statt 130x100? Empfehlung: ja, als Vorschlag in der Notiz.

## Stand Schritt 2 Werkstatt (05.11.2026)
Vorher = Messlauf des Planers vom 05.11.2026 (Stand vor 1A bis 1E, Sektion Stand oben). Nachher = Lauf der Werkstatt nach 1A bis 1E.

| Messwert | vorher | nachher | Befehl |
|---|---|---|---|
| Zeilen in der Stueckliste | 260 | 273 | `python -X utf8 scripts/bom.py` |
| davon nicht platziert | 124 | 137 | gleich |
| Zeilen ohne Preis | 43 | 43 | gleich |
| Summe Einkaufsliste | 26767.12 EUR (erster bom-Lauf, schon mit den Recherche-Dateien, noch altes Modell) | 26870.92 EUR | gleich |
| `check_bom.py` | nicht gemessen | Exit 0, 14 von 14 PASS | `python -X utf8 scripts/check_bom.py; echo $?` |
| Links FEHLER | 6 | 0 | `python -X utf8 scripts/check_links.py` |
| Links GESPERRT | 32 | 13 | gleich |
| Links VERDACHT | 127 | 87 | gleich |
| Links OK | 124 | 189 | gleich |
| platzierte Hauptangebote nicht OK | 91 | 26 (22 VERDACHT, 4 GESPERRT, 0 FEHLER) | `python -c` ueber `data/preis_pruefung_links.json` `link_liste`, `rang == "1"`, platziert nach `data/stueckliste.json` |

Die Summe stieg um 103.80 EUR, weil die Recherche Angebote ersetzt hat und neue Zeilen (273 statt 260) dazukamen; die Zeilen sind nicht platziert oder ohne Preis, die Summe ist deshalb kein sauberer Vorher/Nachher-Vergleich.

### check_bom.py: Ursache und Behebung
Erster Lauf nach `bom.py`: Exit 1, 3 FAIL.
1. Ursache A (Pruefungen 2, 5, 8): Der Messcache `data/bom_koerper.json` stammte vom 04.11. 05:29. Fuenf `lt_rohr_d25_*`-Komponenten fehlten, `strebe_a` trug noch die Masse des Vollprofils (24747.9 g statt 7729.4 g Vierkantrohr 30x30x3). Behebung: 73 seit dem Cache geaenderte Komponenten neu gemessen (`bom_artikel.messen(nur)`, 31 min, 0 Fehler), keine Skriptaenderung.
2. Ursache B (Pruefungen 6, 10): Die neu gemessenen Komponenten brachten Koerper ohne Regel. Behebung, nur diese Luecken:
   - `data/bom_regeln.json`: `schlammfass` in Gruppe "Becken und Tanks", `beet_sumpf` in "Tische und Beete".
   - `scripts/bom_artikel.py` `classify`: Regeln fuer `beet_sumpf` (Schachtaufsatz, Tankverbinder d50, Pumpen, Rueckschlagventile d40, Durchfuehrung, Schwimmerstange, Schwimmer, Entlueftung, Kabelverschraubung) und `schlammfass` (Fass).
   - `scripts/bom_artikel.py` `zuordnen`: die seit W60 5a benannten Normteile (`Scheibe*`, `Mutter*`, `Anker_n`, `Querbolzen`) laufen wieder durch die Gestalt-Erkennung, wie vorher als `Body<n>`.
Annahmen [A] sind im Artikeltext markiert; Preise fehlen (OFFEN) bis die Recherche die neuen Artikel anlegt.

## DoD
1. Die Pruefpunkte 1 bis 5 aus dem Blatt stehen auf PASS (Befund `docs/jobs/pruefung/N-PREIS-PRUEF.md`).
2. `check_bom.py` liefert Exit 0.
3. Die Seite ist per Screenshot geprueft.
4. Die beiden Entscheidungen aus OFFEN (Ben) stehen in `docs/decisions.md`.
5. W69 im Wunschbuch ist nachgefuehrt.
6. Jeder Teilschritt ist committet und gepusht.
