# Arbeitspaket: N-MINIMAL — Systemreview und Leitungsordnung v2

> Arbeitsartefakt nach `working-method.md`. Angelegt vom Planer/Fachkritiker am 05.11.2026, nachgefuehrt bei jedem Abschluss. Quelle: Wuensche W75, W76, W79 (`docs/packages/wunschbuch-ben.md`), Entscheidungen D84 bis D87 (`docs/decisions.md`). Rolle: nur lesen und rechnen, am Modell wird nichts gebaut.

**Problem:** Die Anlage hat viele Bauteile, die nur wegen Hoehenluecken noetig sind: Beet-Sumpf mit Reservepumpe, Heber und Filtergrube, Notbypass mit Schacht, Schlammfass in der Grube und rund 30 m vergrabenes Rohr (heute gebaut) plus 79 m geplante Graeben. Dazu ist die Leitungsordnung v1 starr rechtwinklig.
**Intent:** Ben und Leon wollen ein schlankes, natuerliches System: so viele Teile wie noetig, so wenige wie moeglich, so guenstig wie moeglich, wenig graben, Schwerkraft nutzen, Technik innen, Schlauch-Ruecklaeufe frei gefuehrt.
**Goal:** `docs/research/R57-systemreview.md` (Tabelle behalten / vereinfachen / streichen je Gruppe, Kostenwirkung, Befehl oder Quelle neben jeder Zahl), `docs/leitungsordnung.md` v2 mit messbarem `scripts/check_leitungsordnung.py` und die Entscheidungsseite `docs/berichte/systemreview.html` sind gepusht.

## Plan
1. [x] Bestand lesen: W75/W76/W79, D84 bis D87, Netzliste, Inventar, Maengel, Hydraulik, R44/R45/R47/R49/R50/R51/R53/R54, Technik innen, Pruefskript (Basis 11 Verstoesse)
2. [x] Quellenrecherche mit zwei Quellen je Aussage (R57 Abschnitt 7; zwei belegte Gegenregeln gefunden: Fischbecken konstant, Sieb vor der Pumpe)
3. [x] Rechenskript `scripts/r57_rechnung.py`: vergraben, aushub, pegel, pumpen, kosten
4. [x] R57-Bericht mit Gruppentabelle G1 bis G23
5. [x] Leitungsordnung v2 und Pruefskript (Arten A bis F, R11 bis R14, `--nur-v2`; Schlauch-Trassen ausserhalb von `leitungen.bauen()`)
6. [x] Entscheidungsseite `docs/berichte/systemreview.html`, Sichtpruefung im Browser (Desktop und 375 px), Commit und Push

## Stand
05.11.2026 — Abgeschlossen bis zur Entscheidung von Ben und Leon.
- Empfehlung: Zielbild S (Pool als tiefster Punkt, Ruhepegel Z -150, Beete auf dem Flur, eine Pumpstufe) mit zwei Bedingungen: Pegel-tief-Abschaltung der Pumpen; Siebmessung im ersten Betriebsmonat mit Vortex-Rueckfall.
- Zahlen (`python -X utf8 scripts/r57_rechnung.py`): unter Flur 230 -> 18 m, Aushub 43,7 -> 2,0 m3, Pumpen 12 -> 4, Dauerstrom 429 -> 328 W, belegte Teilekosten 6039 -> 2242 EUR, Besatz 12,1 -> 16,8 kg/m3.
- Pruefskript: Bestand unveraendert 11 Verstoesse (R4 1, R5 4, R8 5, R9 1), R11 bis R14 je 0; sieben Testtrassen loesen R6 2, R11 2, R12 2, R13 1, R14 1 aus.

- 05.11.2026 Nachtrag D88 (Ben: Zielbild S, Pool gleich gross und 665 mm tiefer eingelassen): neu gerechnet mit `python -X utf8 scripts/r57_rechnung.py pegel | aushub`. Fischwasser 28,5 m3 und Besatz 12,1 kg/m3 bleiben, Beckenboden Z -2350, Aushub 9,9 m3 (7,9 m3 davon tiefere Poolgrube), Freibord 150 mm bei Rand Z 0 reicht im Stoerfall nicht (+276 mm), Empfehlung Aufkantung 150 mm (Freibord 300), freier Fall 0,30 bis 0,35 m, Halbring auf der Aufkantung (KW in der Leitungsordnung angepasst).

## Definition of Done
Geprueft gegen:
1. `python -X utf8 scripts/r57_rechnung.py` (alle Abschnitte)
2. `python -X utf8 scripts/check_leitungsordnung.py` (Bestand) und `--trassen <Scratchpad v2-test.json> --nur-v2`
3. Browser-Sichtpruefung der Seite (Desktop, 375 px, kein seitlicher Bildlauf)
4. Quellen R57 Abschnitt 7

Offen:
1. Entschieden (D88): Zielbild S mit eingelassenem Pool gleicher Groesse. Offen: Aufkantung 150 mm oder Ruhepegel Z -300 als Freibord-Loesung: DEINE ENTSCHEIDUNG (Ben); Grundwasser und Auftrieb der tieferen Grube: Statik
2. Nach Ja: Netzliste v4, Roadmap, Neuplanung M10-S3 bis S7, M10-S2V schliessen: Orchestrator
3. Werkstatt: Schlauch-Baustein, Siebkorb-Aufnahme im Biofilter, Leerrohr-Querung, Schlamm-Durchfuehrung: Orchestrator startet nach Ja
4. Pumpenwahl Tauchpumpe 55 l/min bei 2,3 m (besteht auch fuer A+): Recherche-Sitzung
