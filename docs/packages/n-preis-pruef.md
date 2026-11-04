# Work package: N-PREIS-PRUEF Einzelteilpruefung der Preisliste (W69)

**Problem:** Die Einkaufsliste enthaelt tote Links und unpassende Artikel, zum Beispiel einen Kabelkanal 110x60 statt der NFT-Rinne 130x100 (`data/beschaffung/stahl.json` `PRF-pvcu-rinne-130x100`).
**Intent:** Ben (W69, 05.11.2026) will, dass jede Zeile ein real bestellbares, zum Bauteil passendes Teil mit Bezug mindestens aus Europa (D76) ist, damit die Liste und die Ausfuell-Tabelle W65 belastbar sind.
**Goal:** `python -X utf8 scripts/check_links.py` meldet 0 FEHLER bei platzierten Hauptangeboten. Jeder VERDACHT und jedes GESPERRT ist von Hand belegt. Die NFT-Rinne ist kein Kabelkanal mehr. Der Pruefer hat 5 von 5 Pruefpunkten gemessen. Blatt: `docs/jobs/N-PREIS-PRUEF.md`

## Plan
1. [x] Planer: Link-Messlauf `scripts/check_links.py`, Tabelle `docs/preis-pruefung-links.md`, Auftragsblatt (05.11.2026)
2. [ ] Fachrecherche 1A Stahl und Normteile (`data/beschaffung/stahl.json`, plus 8 SRB-Saetze)
3. [ ] Fachrecherche 1B Leitung (`leitung.json`, plus 5 ARM/FIT)
4. [ ] Fachrecherche 1C Behaelter, Pumpen (`behaelter.json`, plus 9 Aktivkohle/Luft)
5. [ ] Fachrecherche 1D Mess und Elektrik (`mess_elektrik.json`, plus 2 Schrank)
6. [ ] Fachrecherche 1E Huelle, Pflanze (`huelle_pflanze.json`)
7. [ ] Werkstatt 2: `bom.py`, `check_bom.py` mit Exit 0, `check_links.py` erneut, Screenshot der Seite
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

## DoD
1. Die Pruefpunkte 1 bis 5 aus dem Blatt stehen auf PASS (Befund `docs/jobs/pruefung/N-PREIS-PRUEF.md`).
2. `check_bom.py` liefert Exit 0.
3. Die Seite ist per Screenshot geprueft.
4. Die beiden Entscheidungen aus OFFEN (Ben) stehen in `docs/decisions.md`.
5. W69 im Wunschbuch ist nachgefuehrt.
6. Jeder Teilschritt ist committet und gepusht.
