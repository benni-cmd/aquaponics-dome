# W37-2 Aktivkohle-Gehaeuse mit Schwimmerventil und Becken-Stutzen Drittbecken (Werkstatt B, Sitzung 2 von 3)

Problem: Der Frischwasser-Filter (Knoten `aktivkohle`, Kanten K39 bis K43, K52) hat im Modell kein Bauteil, und das Drittbecken `becken_dritt_klein` hat keine Anschluss-Stutzen (L05, L09: K41, K42, K43, K49 haengen daran). Ohne beide ist S5 nicht baubar. Intent: S5 soll Frischwasser entchlort in Pool und Quarantaene fuehren und das Drittbecken anschliessen koennen; Handelsteile statt Eigenkonstruktion (L21). Ziel in einem Satz: Ein Bauteil `aktivkohle_station` (zwei Behaelter in Reihe, Sedimentvorfilter, Probehahn, Durchflussbegrenzer, Abzweige K41/K52) samt `schwimmerventil_pool` und eine Stutzen-Ergaenzung am Drittbecken, jeweils mit Ports, Blatt, Check und Bild.

## Aktualitaetspruefung (04.11.2026, Planer, Regel W44) — gilt zuerst
Ergebnis: **angepasst** (Plan gilt als freigegeben, nur fuer den variantenunabhaengigen Teil). Mini-Plan: `docs/packages/w37-2-3-frischwasser-luft.md`. Geprueft gegen: `git log --since=2026-11-01`, `docs/decisions.md` D70 bis D77, `docs/research/R47-wasserkreislauf-neu.md` (Definition A/B/C), `docs/research/R52-europa-bezug.md`, `data/leitungsnetz.json` Version 3 (K39 bis K43, K52).
- **Rahmen Ben 04.11.:** Die Kreislaufvariante E20 (A+, A, B, C) entscheidet Ben erst am 05.11. Dieses Blatt plant nur, was in JEDER Variante gleich bleibt; Abhaengiges steht als "OFFEN (E20)".
- **Variantenbefund je Teil:**
  | Teil | Befund | Grund |
  |---|---|---|
  | 1 `aktivkohle_station` | **unabhaengig** | Frischwasser kommt von aussen und wird vor jedem Kreislauf entchlort (D66); Behaelter, Vorfilter, Ports K39/K40/K41/K52 gleich in A+, A, B, C |
  | 2 `schwimmerventil_pool` | **Bauteil unabhaengig, Zulauf OFFEN (E20)** | Das Ventil am Pool (Z 515) gilt in jeder Variante. In Variante B speist der Ring (d90, Z 2100/2245) auch das "Becken-Frischwasser" (R47 Definition B); ob K40 dann aus dem Ring statt aus der Filterstation kommt, ist **OFFEN (E20)**. Nicht planen, nur den Hinweis behalten: die Filterstation bleibt davor |
  | 3 Stutzen Drittbecken | **unabhaengig** | Quarantaene mit eigenem Biofilter (K42/K43) und eigener Luft (K49) haengt nicht am Hauptkreislauf |
- **D75 (Subtank, Bau geparkt) und R47/R47B-Waechter:** beruehren Frischwasser und Drittbecken nicht; Waechter (Durchfluss je Linie, Hoch-Schwimmer) sind kein Auftrag hier.
- **D77 (Beet Sperrboden):** Das Systemvolumen sinkt um rund 6400 l; die mittlere Nachspeisung (2 Prozent je Tag) sinkt von 0,68 auf etwa 0,55 m3/Tag [E, `python -X utf8 -c "print(0.68*(34-6.4)/34)"` = 0,552; 34 m3 aus 0,68 / 0,02]. Der Durchflussbegrenzer (4 l/min) und die Spitze (10 l/min) bleiben; die Auslegung der Station aendert sich nicht.
- **D76 (Kaufteile mindestens Europa):** neu im Blatt, Abschnitt "Europa-Teileliste" unten. **Befund:** katalytische Kokoskohle gegen Chloramin ist in Europa nicht belegt beschaffbar (nur US-Shops); nicht katalytische Kohle (Jacobi AquaSorb CS 12x40, Ecosoft) hilft nur gegen Chlor. Das trifft E15 (Chlor oder Chloramin, Ben): bei Chloramin im Leitungswasser faellt der "beide Behaelter"-Plan auf die Kohlebeschaffung zurueck. Zisterne bleibt "nicht bauen".
- **R52:** deckt nur Kugelhaehne d40/d63/d75 und die Bulkhead-Reihe von Bevo (darunter 20/25 x 3/4 Zoll, Art. 7026181) ab; das gilt fuer die Stutzen des Drittbeckens.
- **R45 Zeile 312:** Wechselintervall und Kapazitaet der Kohle sind weiter ohne Quelle, bleiben **OFFEN** (Hersteller erfragen).
- **Parallel:** Werkstatt W40-BEET baut `ibc_beet*`; keine gemeinsame Datei mit diesem Blatt. `designs/components/becken_dritt.sc` bleibt fremd und veraendert (`git status`), nicht committen.

### Europa-Teileliste (D76, Recherche 04.11.2026; [Q] Seite geoeffnet, [Q-Treffer] nur Suchergebnis; keine Preise)
| Teil | Hersteller, Artikel | Land | Quellen | Status |
|---|---|---|---|---|
| Kompositbehaelter 10x35 mit Kopf | PWG-Vessel 10x35, Clack-Handrueckspuelkopf 1", 38,3 l, Q-1035-A9 (GAPS) [Q-Treffer] | UK | 1 Quelle | **nur UK, eine Quelle**; Bypass nicht genannt; EU-Festland offen |
| Sedimentgehaeuse 10" | Gehaeuse EKO 3/4" Messing, Art. 32420234 (wasserfilter-berlin); Ecosoft INL-FPV34ECO-3/4 [Q-Treffer] | DE, BE (unsicher) | 2 | beschaffbar (schwach, nicht geoeffnet) |
| Patrone PP 20 um, 10" | ALFILTRA Filterkerze PP 20 um [Q-Treffer] | DE | 1 | nur eine Quelle |
| Durchflussbegrenzer 4 l/min | kein Festwert 3/4" gefunden; Kemper FG 68499001 (Set 4/10/20 l/min) [Q-Treffer] | DE | – | **nicht beschaffbar** als Festwert; Ersatz Blende oder Nadelventil plus Durchflussmesser, im Modell Platzhalter-Koerper |
| Schwimmerventil 3/4" | R+M Suttner Art. 701403, Kunststoff, max. 22 l/min [Q]; Pegler Yorkshire 3/4" Messing (RS Art. 0197867) [Q-Treffer] | DE; UK-Marke | 2 | beschaffbar (Spitze 10 l/min erfuellt); Schliessdruck mit Drossel offen |
| Katalytische Kokoskohle 12x40 | Jacobi AquaSorb CX-MCA: nur US-Shops; EU-Distribution (Lenntech NL, Endler) nicht bestaetigt [Q-Treffer] | EU-Hersteller (SE), Haendler offen | – | **nicht beschaffbar belegt**; AquaSorb CS 12x40 (Ecosoft) nur Chlor [Q] |
| Kugelhahn d25, d20 | bevo Profec Safe 600 Art. 0112135 (d25); Safe 525 Art. 0112140 (d20); GF Typ 546 via RS [Q-Treffer] | DE, NL | 1 bis 2 | beschaffbar (nicht geoeffnet) |
| Probehahn d12 | nicht gefunden | – | – | **offen** |
| Tankdurchfuehrung d25 | Bevo VDL Bulkhead 7026181 (20/25 x 3/4") [Q, R52]; Koi-Breeder via Galaxus CH (Art. 14774829) [Q-Treffer] | NL; CH | 1 EU-Quelle | nur eine EU-Quelle |
**Entscheidung fuer den Bau:** alle Masse bleiben Handelsmass-Platzhalter [A] mit Vermerk "Katalog offen, N-BESCHAFFUNG (W47)"; kein Fabrikat wird als gewaehlt eingetragen. **DEINE HANDLUNG (Ben):** E15 (Chlor oder Chloramin) beim Versorger klaeren; Jacobi EU, Lenntech oder Endler nach CX-MCA fragen.

## Aktualitaetspruefung (01.11.2026, Planer; ueberholt durch den Abschnitt oben)
Ergebnis: **angepasst** (Plan gilt als freigegeben).
- Roadmap L05, L09, W37 gueltig. Knoten `aktivkohle` (Netz Version 3) hat `bauteil: null`, Status "Auslegung R45, Fabrikat offen"; Kanten K39/K40 d25 mit 4 l/min begrenzt, K41 d20 2 l/min, K52 d25 ohne Dauerfluss.
- D69: **Standort und Versorger-Anruf sind keine offenen Fragen mehr**; Aktivkohle ist Standard (D66). Die Chlor-/Chloramin-Frage (E15) bleibt bei Ben (DEINE HANDLUNG), betrifft hier nur, ob der zweite Behaelter noetig ist: **beide Behaelter bauen** (Auslegung auf den ungünstigeren Fall Chloramin), der zweite laesst sich per Parameter `behaelter` (1 oder 2) weglassen.
- Zisterne als Alternative (R45 Abschnitt 5): **nicht bauen**, nur im Blatt erwaehnen.
- Zweitbecken-Stutzen entstehen in `scripts/gen_dome.py` (Montage S5) und gehoeren nicht hierher.
- Schwimmerventil-Fabrikat und Schliessdruck mit Drossel sind offen (R45 Frage 5 Nr. 4): als Platzhalter mit [A] bauen.

## Eingaben (nur diese)
- `docs/research/R45-hydraulik-auslegung.md` Abschnitt 5 (Zeilen 280 bis 329) und aus Abschnitt 4 (Zeile 258 bis 266) nur die Zeile K49 (Luft Drittbecken).
- `data/leitungsnetz.json` per Python: Knoten `aktivkohle`, `drittbecken`; Kanten K39, K40, K41, K42, K43, K49, K52.
- `docs/parts/becken_dritt_klein.md` (ganz, 60 Zeilen) und `scripts/workshop/becken_dritt_klein.py`, `check_becken_dritt_klein.py` (Bauweise; die Datei `designs/components/becken_dritt_klein.sc` wird erweitert, nicht `becken_dritt.sc`, das gen_dome.py erzeugt).
- Bibliothek: `docs/parts/leitungsteile.md` Konvention (Zeilen 7 bis 30); `scripts/workshop/leitung.py` (`kugelhahn`, `rohr`, `reduzierung`, `save`); Muster Station: `scripts/workshop/puffer_station.py`.

## Teile
### Teil 1 `aktivkohle_station`
Mini-Plan zuerst im Blatt. Maße aus R45 Abschnitt 5 (Belegstand je Zeile):
| Merkmal | Wert | Beleg |
|---|---|---|
| Kohle | katalytische Kohle (Kokosschale) 12 x 40 mesh; je Behaelter etwa 21 l Bett; 2 Behaelter in Reihe; Kontaktzeit 10,5 min bei 4 l/min | gerechnet (`scripts/r45_kohle.py`), Handels-Eckwerte [Q] aus Haendler-/Verbandsmaterial, keine Fachartikel |
| Behaelter | Kompositbehaelter 10 x 35 Zoll, Ø 254 x 889 mm (Handelsmass, Fabrikat offen), stehend, Kopf mit Bypass-/Absperrhahn | Annahme [A] |
| Vorfilter | Sedimentfilter 20 µm, Gehaeuse 10 Zoll (Handelsmass) | Annahme [A] |
| Verbindung | Leitung d25 (K39/K40); Probehahn d12 zwischen Behaelter 1 und 2; Durchflussbegrenzer 4 l/min hinter Behaelter 2 | R45 |
| Abzweige | K41 (d20, Quarantaene 2 l/min) und K52 (d25, Stammloesung von Hand) **nach** dem Filter | R45 |
| Aufstellung | frostfrei, Regalboden oder wandnah, Behaelter stehend 0,9 m hoch; Standort ist Montage | R45 |
Ports: Eingang d25 (K39), Ausgang d25 (K40), Abzweig d20 (K41), Abzweig d25 (K52), Probehahn d12; alle im Bibliotheksformat, Hahn und Begrenzer als Teile aus der Bibliothek (Kugelhahn d25/d20) oder Platzhalter-Koerper. Stueckliste aus Handelsteilen (L21): 2 Kompositbehaelter 10x35, 1 Sedimentgehaeuse 10", 2 Kopf-Bypasshaehne, 1 Probehahn d12, 1 Durchflussbegrenzer 4 l/min, Verrohrung d25. Prueft ausdruecklich: keine Vorratsflaeche, kein Eigenbau-Behaelter.

### Teil 2 `schwimmerventil_pool` (Handelsteil, klein)
Schwimmerventil am Pool (K40) mit Drossel; Maße Platzhalter, Schliessdruck und Fabrikat offen (R45 Frage 5 Nr. 4). Ein Port d25 (Muffe/Gewinde-Uebergang), Ventilkoerper und Schwimmerkugel mit Hebelarm als Hoehe-Parameter (Spiegelhoehe Z 515 ueber `water_z`, Wert aus `layout.json` nur lesen). Nur ein Kurzteil, kein eigener Check ausser Masse, Port, Interferenz 0.

### Teil 3 Becken-Stutzen Drittbecken (Erweiterung `becken_dritt_klein`)
Stutzen am Wannenrand/Ring des Drittbeckens fuer: K41 Frischwasser-Zulauf d20 (Muffe aussen), K42 Umlauf zum Biofilter d25 (Entnahme) und K43 Rueckfluss d25, K49 Luftschlauch d20 (Luft: Notstrom, gehoert zum Gebläse in W37-3, hier nur der Stutzen). Ueberlauf/Ablauf des Wechselwassers ist laut Netz Montage und bleibt aus. Stutzen als **eigene Koerper** auf ebenen Flaechen oder Bloecken (nicht als Boolean in den duennen Ringmantel: "implausible result volume", `docs/workshop-state.md` GELERNT), Lage fuer K42/K43 mit Biofilter-Seite nach Azimut-Vorgabe der Montage offen lassen und als Parameter `stutzen_winkel` (Standard: ein Stutzen je 90 Grad, Ablesbar im Blatt). `becken_dritt_klein.json` und Blatt werden **nachgefuehrt** (neuer Abschnitt "Stutzen"), die vorhandene Wanne bleibt unveraendert (Pruefpunkt 4). Die Zweitbecken-Stutzen sind explizit nicht Teil.

### Gemeinsame Ergebnisse
Je Teil: `designs/components/<name>.sc` bzw. erweiterte `becken_dritt_klein.sc`, Check (Masse, Ports, Interferenz 0), Blatt-Abschnitt, `data/components/*.json`, `data/descriptions.json` (vor `^puffer` einsortieren; Namen `aktivkohle_*` und `schwimmerventil_*` kollidieren mit keinem bestehenden Muster, vorab `grep -n '"match"' data/descriptions.json` pruefen), Bild per `scripts/archive_render.py --role werkstatt`, Zeile in `docs/workshop-state.md`. Je Teil ein Commit, dazwischen push.

## Nicht anfassen
`designs/components/becken_dritt.sc` (gen_dome.py), `scripts/gen_dome.py`, `scripts/leitungen.py`, `data/leitungsnetz.json`, `data/roadmap.json`, `docs/research/R45-hydraulik-auslegung.md`, `data/params.json` (die Verknuepfung `pool3_d`/`pool3_depth` setzt die Montage), die fremden Dateien aus `docs/workshop-state.md`. Nichts zu Sumpf, Schlammfass, Luft, Schaltschrank.

## Ergebnis
`aktivkohle_station.sc`, `schwimmerventil_pool.sc`, erweiterte `becken_dritt_klein.sc` mit Stutzen samt Generatoren, Checks, Blaettern, JSON, descriptions, Bildern. Kurzmeldung: je Teil eine Zeile (Masse, Ports, offene Fragen); Hinweis an den Orchestrator: Chlor-/Chloramin-Frage E15 (DEINE HANDLUNG Ben), Zisterne nicht gebaut.

## Pruefpunkte (fuer den Pruefer)
1. Check der drei Teile PASS (Aufruf im Blatt-Abschnitt "Pruefung"; Soll: keine FAIL-Zeile).
2. Bettvolumen: 2 x etwa 21 l je Behaelter im Blatt gegen Rechnung (`python -X utf8 scripts/r45_kohle.py`, Soll: 20 l bei 5 min und 40 l bei 10 min Kontaktzeit; die Auslegung 2 x 21 l erfuellt 10,5 min bei 4 l/min).
3. Port-Tabelle `aktivkohle_station`: Eingang d25 (K39), Ausgang d25 (K40), Abzweig d20 (K41), Abzweig d25 (K52), Probehahn d12; jede Kante im Blatt genannt (`grep -c "K4[01]\|K52\|K39" docs/parts/aktivkohle_station.md`, Soll >= 4).
4. Drittbecken: Wannenkoerper unveraendert, Gesamt-Box wie im Bestand (X -460 bis 460, Y -460 bis 460, Z 0 bis 1055) plus Stutzen; neue Stutzen mit Ports K41 d20, K42 d25, K43 d25, K49 d20; Interferenz 0 gegen die Ringwand.
5. Herkunftstabelle trennt belegt, gerechnet, Annahme; kein erfundenes Fabrikat (Behaelter, Begrenzer, Schwimmerventil nur als Handelsmass mit Vermerk "Katalog offen, N-BESCHAFFUNG").
6. Europa-Teileliste (D76) im Bauteilblatt `docs/parts/aktivkohle_station.md`: jede Zeile mit Hersteller, Artikel, Land, Status; kein Teil als "beschaffbar" mit nur US-Quelle; katalytische Kohle und Begrenzer als "nicht beschaffbar" gefuehrt (`grep -c "nicht beschaffbar" docs/parts/aktivkohle_station.md`, Soll >= 2).
7. Variantenbefund: `schwimmerventil_pool` enthaelt den Vermerk "Zulauf OFFEN (E20)" (Variante B, Ring); `aktivkohle_station` und Drittbecken-Stutzen enthalten keinen E20-Bezug (`grep -c "OFFEN (E20)" docs/parts/schwimmerventil_pool.md`, Soll >= 1).

## Start-Hinweis fuer die Bau-Sitzung
1. W39 muss vorher gelaufen sein (Kappe, Kugelhahn-Reihe, PE-Uebergang d20, Schlauchschelle); fehlt etwas, Platzhalter und Vermerk.
2. `becken_dritt.sc` nie ueberschreiben (gen_dome.py erzeugt es); `becken_dritt_klein.sc` darf neu gebaut werden, Parameter `pool3_d_neu` 800 und `pool3_depth_neu` 920 bleiben.
3. Boolean mit duennem Zylindermantel scheitert: Stutzen als eigener Koerper oder auf Bloecke setzen.
4. Behaelter-Masse sind Handelsmass-Annahmen; Kontaktzeit, Standzeit und Kohle-Kapazitaet fehlen als Quelle (R45), im Blatt als [A] fuehren.
5. Limit: drei kleine Teile in einer Sitzung ist die Obergrenze; bei Kontext ueber 60 Prozent Stand in `docs/workshop-state.md` und stoppen.

## Nachtrag Pruefpunkt 6 (Orchestrator, 04.11.2026, Pruefer-Auflage A1)
Das Soll von Pruefpunkt 6 ist durch R53 ueberholt. Neues Soll: Kohle "nicht beschaffbar (EU-Festland)" (nur UK), Durchflussbegrenzer "eine Quelle" (Kobold KM-020A); zweite EU-Quelle fuer den Begrenzer und Kohle vom Festland (Eurocarb, Ecosoft DE/BE) bleiben offen (Auflage A2, N-BESCHAFFUNG).
