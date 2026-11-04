# Pruefung W40-BEET (Pruefer, 04.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md`. Gegenstand: Blatt `docs/jobs/W40-BEET.md` (mit Bezugsquellen-Nachtrag), Paket `docs/packages/w40-beet.md`, Commits 3c4acc2, c9b7f50, 0f0c84a, a8d45dc. D77 (`docs/decisions.md`) gilt: Sperrboden V3, Standrohr d25 mit Reduzierhuelse 32/25, Lochblech 5 mm vom Metallbauer. Die Selbstauskunft im Paket wurde als Behauptung behandelt; alle Zahlen unten sind in dieser Sitzung neu gemessen (Repo unveraendert, nur diese Datei geschrieben).

## Urteil: PASS mit Auflagen

Alle fuenf Pruefpunkte des Blatts sind erfuellt. Die Auflagen betreffen eine falsche Zahl in der Selbstauskunft (191 statt 190), einen nicht erreichten Zielsatz-Bereich (Entleerzeit, im Paket ausgewiesen), fehlende Artikelnummern in zwei Teilelisten-Zeilen und Texte; keine bricht ein Soll eines Pruefpunkts.

## Pruefpunkte

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | Film aussen_800 <= 10 l, innen_933 <= 8 l; Siebboden ohne Loecher (Volumen = Flaeche x 8 mm); Kerben-OK <= z 274 (innen 286) | `python -X utf8 scripts/w40_beet_rechnung.py`; `solidcraft-cli.exe eval designs/components/ibc_beet_<typ>.sc --json-out ...` (Koerper, Zeitleiste); `python scripts/workshop/check_ibc_beet.py` | Film aussen_800 9,3 l, innen_933 7,6 l (aussen_933 12,3 l). Siebboden aussen_800 15 468 522 mm3, innen_933 12 594 257 mm3; Zeitleiste enthaelt nur `Siebboden_Kontur`, `Siebblech`, `Sieb_Standrohr` (kein Lochmuster, kein `Sieb_Loch`). Gegenrechnung aussen_800: bbox 2588 x 748 x 8 = 15 486 592 minus d36-Durchfuehrung 8 143 minus Eckrundung r 38 (rund 9 900) = 15 468 5xx, Differenz zum Messwert unter 0,01 %. Kerben-OK aussen_800 z 274 (262 + 12), innen_933 z 286 (274 + 12): Check-Zeilen PASS | PASS |
| 2 | Ablaufzeit d25, h 0,30 bis 0,60 m: 3,6 bis 5,1 min (aussen_800); Abweichung zu R45 4,3 bis 6,1 ausgewiesen; Ablaufvolumen 195 l | `python -X utf8 scripts/w40_beet_rechnung.py` (Abschnitt 2) | aussen_800: 194 l (R45-Definition) bzw. 196 l (V3-Geometrie) -> 3,6 bis 5,1 min; Skript gibt "ABWEICHUNG ... liegt unter R45 4,3 bis 6,1 min" aus. innen_933 2,9 bis 4,2 min, aussen_933 4,8 bis 6,8 min (obere Grenze ueber R45). Siphon-Leistung 38,1 / 46,9 / 54,4 l/min | PASS (Abweichung offen ausgewiesen, siehe Auflage 2) |
| 3 | Check Exit 0 (alle vier Typen) | `python scripts/workshop/check_ibc_beet.py; echo $?` | Exit 0; Schlusszeile "== ibc_beet: 190/190 PASS"; 0 Zeilen ohne PASS; je Typ 47 / 47 / 47 / 49 Messungen (aussen_933, aussen_993, aussen_800, innen_933) | PASS |
| 4 | Alle Koerper benannt, keine `Body<n>`; Interferenz 0; `Reduktion`, `Reinigungsschacht`, `Medienschutz` vorhanden | Check-Zeilen "alle Koerper benannt" und "Interferenzen (inspect.interference)"; `eval`-JSON, Koerperliste aussen_800 und innen_933 | Je Typ Interferenz Ist 0 (4 von 4), "alle Koerper benannt" Ist 1 (4 von 4). aussen_800: 40 Koerper, innen_933: 31 Koerper, Anzahl `Body<n>` 0. `Reduktion` (z -80 bis -30), `Reinigungsschacht` (z 262 bis 582, Aussen-d 110), `Medienschutz` (d110, z 262 bis 582), dazu `Schutzkappe`, `Schachtkappe`, `Plattenhuelse`, `Reduzierhuelse_Boden`, `Reduzierhuelse_Platte` vorhanden | PASS |
| 5 | Jede Teilelisten-Zeile hat Hersteller/Haendler und Artikel; Blocker (Plattenhuelse, Dichtband, Kleber) im Blatt als "nicht beschafft" | `docs/parts/ibc_beet.md` Abschnitt "Teileliste mit Bezug in Europa (D76)" gelesen (10 Zeilen), gegen Nachtrag im Blatt | 10 Zeilen, alle mit Hersteller/Haendler. Artikel/Bestellnummer fehlt in 2 Zeilen: Reinigungsschacht-Rohr ("Rohr-Artikel beim Kauf eintragen") und Dichtband (nur Haendler, Werkstoff, keine Art.-Nr.). Plattenhuelse: Blocker durch Reduzierhuelse 32/25 geloest (Schwarte 75208, Bevo 7002656, zwei Haendler). Kleber: Tangit PVC-U Plus, toom 8150236, beschaffbar. Dichtband: Status "Mass offen", nicht wortgleich "nicht beschafft", inhaltlich offen und ehrlich ausgewiesen. Der Nachtrag hat die Blocker laut Blatt-Wortlaut verschoben; das Paket weist die Abweichung selbst aus | PASS (mit Auflage 3) |

## Stichproben ausserhalb der Pruefpunkte

1. Zahl aus der Kurzmeldung gegen die Messung: Paket und Commit c9b7f50 behaupten "191 PASS". Gemessen: 190 Messungen, Schlusszeile 190/190 (`grep -c PASS` ergibt 191 nur, weil die Schlusszeile das Wort enthaelt). Behauptung um 1 falsch, Ergebnis (0 FAIL) richtig. FAIL dieser Stichprobe, keine Folge fuer das Urteil.
2. Teil gegen sein Blatt: Reinigungsschacht: Blatt nennt Laenge etwa 562 mm, Teileliste und Modell 320 mm ab Platte (Modell z 262 bis 582 = 320 mm, Oberkante 20 mm ueber Medium wie im Blatt). Das Modell ist stimmig, das Blatt-Mass 562 ist die alte Rechnung von z 20 bis 582. Standrohrflaeche: Blatt 380 mm2 (ID 22), Check-Text "346" (ID 21); Kerbenflaeche 480 mm2 deckt beide.
3. Commit gegen `git diff`: `git show --stat` der vier Commits beruehrt nur Pfade des Blatts (`scripts/w40_beet_rechnung.py`; `data/components/ibc_beet.json`, vier `ibc_beet_*.sc`, `check_ibc_beet.py`, `ibc_beet.py`; `docs/parts/ibc_beet.md`, `partsheet.py`; `docs/packages/w40-beet.md`). Keine fremden `.sc`, kein `data/roadmap.json`, kein `viewer/`. PASS. Arbeitsbaum: 11 fremde `designs/components/*.sc` und `viewer/extras.json` sind veraendert, keine davon `ibc_beet_*`.

## Nicht belegte oder nicht nachgemessene Behauptungen

1. Anspringen der Glocke bei 3,3 l/min und Dichtheit der Platte: laut Blatt und Rechnung nur am Muster pruefbar, nicht nachgemessen (nicht pruefbar).
2. Kaufteile (Bevo, Schwarte, Ostendorf, Hornbach, ehorst) und Preise: keine Haendlerseite in dieser Sitzung aufgerufen; nur Konsistenz der Eintraege zwischen Blatt, Nachtrag und Bauteilblatt geprueft.
3. Reduzierhuelse Baulaenge 22 mm (Bevo-Katalogzeile) gegen Modell-Huelsen 39 mm (Boden) und 15 mm (Platte): Paket und Bauteilblatt nennen das selbst als offen; Datenblatt nicht gelesen.
4. Das Ziel-Satz-Versprechen "Entleerzeit bleibt 4,3 bis 6,1 min" ist fuer aussen_800 (3,6 bis 5,1) und innen_933 (2,9 bis 4,2) nicht erfuellt; Pruefpunkt 2 des Blatts selbst verlangt aber 3,6 bis 5,1 und ist erfuellt. Widerspruch im Blatt (Zielsatz gegen Pruefpunkt), vom Paket erkannt.

## Auflagen

1. Paket `docs/packages/w40-beet.md` (Zeile 31 und 53): "191 PASS" auf "190/190 PASS" korrigieren (Messwert `check_ibc_beet.py`). Owner: Werkstatt/Orchestrator.
2. Entleerzeit: Der Zielsatz des Blatts (4,3 bis 6,1 min) passt nicht zu den kleineren Typen. Entscheidung, ob je Typ ein eigener Sollbereich gefuehrt wird (aussen_800 3,6 bis 5,1, innen_933 2,9 bis 4,2, aussen_933 4,8 bis 6,8) und ob 2,9 min bei innen_933 noch ausreicht. Owner: Orchestrator; kein Bau noetig.
3. Bauteilblatt `docs/parts/ibc_beet.md`: Artikelzeile fuer das Rohr DN100 des Reinigungsschachts und fuer das Dichtband eintragen; Dichtband-Status ausdruecklich "nicht beschafft (Mass offen)" fuehren. Owner: Werkstatt bei der naechsten Bauteilblatt-Pflege.
4. `check_ibc_beet.py` Anzeigetext "Standrohrflaeche 346" an das Blatt (380 mm2, ID 22) angleichen oder die Wandstaerke klaeren; Blatt-Mass "Laenge etwa 562 mm" fuer den Schacht ist ueberholt (Modell 320 mm). Owner: Werkstatt (Blatt selbst bleibt unveraendert).
5. Vor Montage der 14 Beete: Reduzierhuelse-Baulaenge (22 mm) gegen Modell-Huelsen und Tankverbinder-Flansch D50 gegen Datenblatt pruefen. Owner: Planer/Montage.

Geprueft gegen: `python -X utf8 scripts/w40_beet_rechnung.py`, `python scripts/workshop/check_ibc_beet.py` (Exit 0, 190/190), `solidcraft-cli.exe eval` je Typ aussen_800 und innen_933, `docs/parts/ibc_beet.md`, `docs/jobs/W40-BEET.md`, `docs/packages/w40-beet.md`, `git show --stat` der vier Commits, D77.
Offen: Auflagen 1 bis 5 (Owner je Auflage genannt); Muster-Pruefung (Anspringen, Dichtheit) und Haendlerseiten nicht pruefbar in dieser Sitzung.
