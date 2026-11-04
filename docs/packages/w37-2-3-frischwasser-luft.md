# Work package: W37-2/W37-3 Frischwasser und Luft (Planer, gebuendelt)

> Work artifact per `working-method.md`: lebt im Repo seines Projekts. Angelegt beim Planen
> (Planer, 04.11.2026), nachgefuehrt bei jedem Abschluss. Bau-Sitzungen folgen erst nach der
> Werkstatt W40-BEET (nur eine schreibende Bau-Sitzung gleichzeitig).

**Problem:** Frischwasser-Filter (Aktivkohle mit Schwimmerventil), Stutzen am Drittbecken, Geblaese N+1, Luftverteiler, Scheibenbelueftung und Schrank-Einfuehrung fehlen im Modell (Luecken L05, L06, L08, L09). Die Blaetter vom 01.11. sind durch D75, D76, D77, R47/R47B, R52 und Bens Rahmen vom 04.11. (E20 erst am 05.11.) nicht mehr aktuell.
**Intent:** Nur das vorbereiten, was in JEDER Kreislaufvariante (E20: A+, A, B, C) gleich bleibt (Frischwasser, Belueftung), und jedes Kaufteil von Anfang an mit mindestens einer europaeischen Bezugsquelle fuehren (D76).
**Goal:** Zwei Blaetter (`docs/jobs/W37-2-aktivkohle-stutzen.md`, `docs/jobs/W37-3-luft-schaltschrank.md`) mit frischer Aktualitaetspruefung (04.11., W44), Europa-Teileliste mit Hersteller und Artikel, Pruefpunkten und "OFFEN (E20)"-Markierung; eine Bau-Sitzung kann ohne Rueckfrage starten.

## Plan

1. [x] Bestand lesen: beide Blaetter, Vorlage `planung.md`, D66 bis D77, R47/R47B-Notizen, R52, Netz Version 3 (K39 bis K52), W39-Pruefbericht
2. [x] Variantenpruefung je Teil (siehe Stand): unabhaengig / abhaengig / OFFEN
3. [x] Europa-Recherche der neuen Kaufteile (zwei Recherche-Agenten, Websuche) und Abgleich mit R52
4. [x] Blatt W37-2 nachfuehren (Aktualitaetspruefung neu, Europa-Teileliste, Pruefpunkte, OFFEN-Marken)
5. [x] Blatt W37-3 nachfuehren (dito)
6. [x] Pfad-Commit und Push (nur Blaetter und dieses Paket)
7. [x] Bau W37-2 Teil 1 `aktivkohle_station` (T83): Generator, Check 40/40 PASS, Blatt, Bilder (Werkstatt, 04.11.2026)
8. [x] Bau W37-2 Teil 2 `schwimmerventil_pool` (T84): Check 15/15 PASS, Blatt, Bild; Zulauf "OFFEN (E20)" vermerkt
9. [x] Bau W37-2 Teil 3 Stutzen Drittbecken (`becken_dritt_klein` erweitert): Check 40/40 PASS, Wanne unveraendert (231314 cm3), Blatt nachgefuehrt
10. [ ] Bau W37-3 Belueftung (naechste Werkstatt-Sitzung), Pruefer W37-2/W37-3

## Status

04.11.2026 — Aktualitaetspruefung durchgefuehrt, Ergebnis **angepasst** (Plan gilt als freigegeben). Beleg: `git log --since=2026-11-01` (178 Commits), `docs/decisions.md` D75 bis D77, `docs/research/R47-wasserkreislauf-neu.md` Abschnitt Definition A/B/C, `docs/research/R52-europa-bezug.md`, `data/leitungsnetz.json` Version 3.

04.11.2026 (spaeter) — beide Blaetter nachgefuehrt (Aktualitaetspruefung neu, Variantenbefund, Europa-Teileliste, Pruefpunkte 6 und 7). Recherche: zwei Agenten, viele Treffer nur [Q-Treffer], daher kaum "beschaffbar" mit zwei Quellen.

04.11.2026 (Werkstatt, Bau W37-2) — drei Teile gebaut und gesichert (Commits d719bff, f79371e und Abschluss-Commit): `aktivkohle_station` (43 Koerper, 2 x 21 l Bett = 10,5 min bei 4 l/min, 5 Ports, check_aktivkohle_station 40/40), `schwimmerventil_pool` (5 Koerper, check 15/15), Drittbecken-Stutzen K41/K42/K43/K49 (6 Koerper, check 40/40). Befund Kernel: T-Stuecke mit gleichen Durchmessern von Lauf und Abgang brauchten 60 s je Schnitt (Bau 209 s); Abgang 0,25 mm duenner und Abgangsbohrung 0,2 mm kleiner: 10 s. Europa (R53): Kohle nur UK, Behaelter mit Kopf nur UK, Begrenzer eine Quelle (Kobold KM-020A), Probehahn G 1/4 beschaffbar; Kohle und Begrenzer im Blatt nach R53 geführt (Begrenzer nicht mehr 'nicht beschaffbar'; Pruefpunkt 6 zaehlt 2 Treffer, einer davon ein Zitat der alten Fuehrung).

## Definition of Done

Geprueft gegen: beide Blaetter enthalten Abschnitt "Aktualitaetspruefung (04.11.2026, W44)", Europa-Teileliste, ergaenzte Pruefpunkte; `git diff HEAD --stat` zeigt nur Blaetter und dieses Paket
Offen: Bau W37-3 (Werkstatt), Pruefer W37-2/W37-3; E20 (Ben 05.11.); E13 (Schaltschrank-Standort); E15 (Chlor/Chloramin, Ben) mit Folge: katalytische Kohle in Europa nicht belegt; Kennlinie Luftpumpe bei 26 kPa; Rueckschlagventil-Regel ohne zweite Quelle; Kohle-Standzeit; Durchflussbegrenzer 4 l/min und Probehahn d12 nicht beschaffbar/gefunden
