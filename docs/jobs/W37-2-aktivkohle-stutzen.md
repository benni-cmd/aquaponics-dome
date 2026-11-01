# W37-2 Aktivkohle-Gehaeuse mit Schwimmerventil und Becken-Stutzen Drittbecken (Werkstatt B, Sitzung 2 von 3)

Problem: Der Frischwasser-Filter (Knoten `aktivkohle`, Kanten K39 bis K43, K52) hat im Modell kein Bauteil, und das Drittbecken `becken_dritt_klein` hat keine Anschluss-Stutzen (L05, L09: K41, K42, K43, K49 haengen daran). Ohne beide ist S5 nicht baubar. Intent: S5 soll Frischwasser entchlort in Pool und Quarantaene fuehren und das Drittbecken anschliessen koennen; Handelsteile statt Eigenkonstruktion (L21). Ziel in einem Satz: Ein Bauteil `aktivkohle_station` (zwei Behaelter in Reihe, Sedimentvorfilter, Probehahn, Durchflussbegrenzer, Abzweige K41/K52) samt `schwimmerventil_pool` und eine Stutzen-Ergaenzung am Drittbecken, jeweils mit Ports, Blatt, Check und Bild.

## Aktualitaetspruefung (01.11.2026, Planer)
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

## Start-Hinweis fuer die Bau-Sitzung
1. W39 muss vorher gelaufen sein (Kappe, Kugelhahn-Reihe, PE-Uebergang d20, Schlauchschelle); fehlt etwas, Platzhalter und Vermerk.
2. `becken_dritt.sc` nie ueberschreiben (gen_dome.py erzeugt es); `becken_dritt_klein.sc` darf neu gebaut werden, Parameter `pool3_d_neu` 800 und `pool3_depth_neu` 920 bleiben.
3. Boolean mit duennem Zylindermantel scheitert: Stutzen als eigener Koerper oder auf Bloecke setzen.
4. Behaelter-Masse sind Handelsmass-Annahmen; Kontaktzeit, Standzeit und Kohle-Kapazitaet fehlen als Quelle (R45), im Blatt als [A] fuehren.
5. Limit: drei kleine Teile in einer Sitzung ist die Obergrenze; bei Kontext ueber 60 Prozent Stand in `docs/workshop-state.md` und stoppen.
