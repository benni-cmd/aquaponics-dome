# R49 — Einfachstes natuerliches System (Schwerkraft, Siphon), Beet-Rueckfuehrung, Vergrabungs-Audit

**Art:** Recherche und Variantenrechnung, KEIN Bau, kein Modell-Umbau. Frage Ben 03.11.2026 (zu E20/E21).

## Problem
Ben will ein moeglichst simples, wartungsarmes, ueberschaubares und effizientes System mit natuerlichen Prinzipien (Schwerkraft, Siphon). Offen: Ob der Biofilter hoeher gesetzt werden sollte, ob wirklich alles vergraben sein muss und ob das Siphon-Wasser der Beete in einem Kreisschlauch ohne Pumpe zurueckgefuehrt werden kann. Heute braucht die Beet-Rueckfuehrung eine zweite Pumpstufe (Beetablauf Z -100 liegt 615 mm unter dem Pool-Spiegel 515).

## Intent
Eine belegte Antwort auf Bens drei Fragen mit gemessenen Zahlen je Konzept und eine Empfehlung fuer E20/E21.

## Goal
`docs/research/R49-einfachstes-natuerliches-system.md` mit Kriterien (Pumpen, Pumpstufen, Foerderhoehe, Dauerstrom, vergrabene Meter, Meter ueber Kopf, Einzelpfade, Teilearten, Umbau), Konzepten (A+ mit V4, Biofilter hoeher in Stufen, Ring auf Tischhoehe, Tiefsumpf), Beet-Rueckfuehrung (Schwerkraft-Sammelring, zentrale Hebestelle, Luftheber, Pegelkreislauf), Vergrabungs-Audit je Abschnitt und Rangfolge; Rechnung als `scripts/r49_rechnung.py`.

## Stand (03.11.2026, Fachrecherche)
- **Fertig:** Bericht und Rechenskript; Modell, `gen_dome.py`, `data/*`, Netzliste und Roadmap unveraendert.
- **Ergebnis:** (1) Biofilter hoeher vereinfacht nichts: Schwerkraft-Zulauf laeuft heute (Kopf 600/950 mm); Ring ueber dem Gang braucht +717 bis +807 mm (+95 bis +104 W); Ring auf Tischhoehe 0 mm, erreicht Beete nicht; tiefer hoechstens 70 bis 100 mm. (2) Schwerkraft-Rueckfuehrung der Beete verlangt Beete 0,8 bis 0,95 m hoeher (Ablauf Z 715 bis 845): Aussenbeete ueberschreiten die Kuppel, 16,9 t; Sammelring aendert nichts an der Hoehe. (3) Luftheber fuer die Beete scheitert (Eintauchen 44 bis 50 %, 140 bis 320 l/min Luft je Linie); fuer den Absetzer-Teilstrom Kandidat (84 %, 6 bis 26 l/min). (4) Vergraben: 30,3 m auf 12,7 m (V4 + K05 direkt), 2,4 m ohne Absetzerkreis; Heber und K14 als Bodenkanal mit Rost. (5) Rang 1 A+ + V4 + K05 direkt + Kanal; Rang 2 Tiefsumpf T (eine Pumpstufe, 436 W) nur nach Fachpruefung des halbierten Pool-Durchsatzes.
- **Abweichungen gefunden:** Bodenablauf real Z -1975 (nicht -1685); Beet-Tropfrohr Z 450 im Bauteilblatt gegen 650 in R47; R48 V4 "23,2 m" enthaelt den Notbypass (ohne 20,0 m).
- **Grenzen der Belege:** Luftheber-Grenzen ein Volltext (Global Seafood), zwei Suchausschnitte; Pool-Durchsatz/TAN-Modell ohne Fachquelle; Teilearten und kuenftige Graeben [A].
- **Offen:** E21 Entscheidung Ben (V4 ja/nein; Kanal fuer K14); Fachfrage Pool-Durchsatz fuer T (ICH); Absetzer-Luftheber am Muster (DEINE HANDLUNG); Gangkarte fuer Kanal und K11 (Planer nach Freigabe).
