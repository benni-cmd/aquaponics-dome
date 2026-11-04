# Work package: N-STUECKLISTE Einkaufsliste nach Typ (buendelt N-KATALOG, N-STUECKLISTE, N-BESCHAFFUNG)

**Problem:** Es gibt keine gemeinsame Liste aller Kaufteile der Kuppel: Mengen stehen im Modell (4880 Instanzen, 152 Definitionen), Teile in 25 Komponentenmodellen, Quellen nur fuer 14 Teile in R52, Preise und Links fehlen ganz; der Mini-Katalog (`data/katalog.json`, pilot) kennt 17 Eintraege.
**Intent:** Ben (W59, 04.11.2026): jedes Einzelteil nach Typ indexiert in EINER Einkaufsliste mit groben Stueck- und Gesamtpreisen und Bestell-Link mit Lieferung nach Deutschland; Zahlen aus einem festen Skript (W45), Bezug mindestens Europa (D76).
**Goal:** `python -X utf8 scripts/bom.py` erzeugt `data/stueckliste.json` und `docs/einkaufsliste.html`; Summen gleich Modellzaehlung (`scripts/check_bom.py` Exit 0); jede Zeile mit Preis, Datum, Quelle, Land, Link oder mit benanntem OFFEN-Grund. Blatt: `docs/jobs/N-STUECKLISTE.md`

## Plan
1. [ ] Werkstatt 1a: Typ-Index und Artikelliste aus allen Komponenten-`.sc` (Preise leer), sofort committen
2. [ ] Werkstatt 1b: `data/bom_regeln.json`, unbenannte Koerper (`Body<n>`) benennen
3. [ ] Werkstatt 1c: `scripts/bom.py` (Zaehlung, Zuschnitt 1D) und `scripts/check_bom.py`
4. [ ] Werkstatt 1d: `data/stueckliste.json`, `docs/stueckliste.md`
5. [ ] Recherche 2A Stahl und Normteile (`data/beschaffung/stahl.json`)
6. [ ] Recherche 2B Wasserleitung, L21 (`data/beschaffung/leitung.json`; E20-abhaengig: OFFEN (E20))
7. [ ] Recherche 2C Behaelter, Becken, Pumpen (`data/beschaffung/behaelter.json`; Subtank: OFFEN (Subtank))
8. [ ] Recherche 2D Messtechnik und Elektrik (`data/beschaffung/mess_elektrik.json`)
9. [ ] Recherche 2E Huelle, Toepfe, Substrat, Gewebe (`data/beschaffung/huelle_pflanze.json`)
10. [ ] Zusammenfuehrung und Seite `docs/einkaufsliste.html`, Screenshot-Abnahme
11. [ ] Pruefer: `docs/jobs/pruefung/N-STUECKLISTE.md` nach fuenf Pruefpunkten
11b. [ ] Seite interaktiv, Gruppieren/Sortieren, Desktop-Verknuepfung (W59-Nachtrag; Verknuepfung auf Bens Desktop nur nach seinem Ja)
11c. [ ] W60: Teiledaten fuer alle Bauteile in 5 Gruppen (Werkstatt, parallel nach 1b), dann Viewer-Anbindung Preis/Link, Pruefer (Pruefpunkte 6 und 7 im Blatt)
12. [ ] Orchestrator: Roadmap nachfuehren (N-KATALOG, N-STUECKLISTE, N-BESCHAFFUNG gebuendelt, N-BOM-PARAM bleibt)

Reihenfolge: 1a vor 2A bis 2E (Artikelliste); 2A bis 2E parallel; 10 nach 1d und 2A bis 2E; 11 zuletzt. Eine Sitzung = ein Schritt (D74).

## Stand
04.11.2026, Planer (Sonnet 5.5): Blatt geschrieben, Aktualitaet **angepasst** (B1 liegt nur fuer 2 von 25 Komponenten vor, deshalb Namensregeln statt voller B1; D69 durch W59 auf grobe Preise erweitert; E20 und Subtank als OFFEN-Status gefuehrt). Messung unbenannter Koerper: `nft_tisch_mitte.sc` 40 von 124; Messung ueber alle Komponenten folgt in 1a. OFFEN (Ben): Preise brutto oder netto (Empfehlung brutto); UK als Europa; Pflanzgut/Fisch/Beton/Aushub in die Liste (Empfehlung nein).

04.11.2026, Nachtraege eingearbeitet: W59 (interaktive Seite, Sortieren, Gruppieren mit Gruppenpreis, Desktop-Verknuepfung) als Paket 3b; W60 (Detailansicht aller Bauteile, verknuepft mit Einkaufsliste) als Paket 5 mit gemeinsamem Datenmodell `data/parts` + `artikel_id`; Pruefpunkte 6 und 7. Zusatz: 6 bis 7 Sitzungen. Empfehlung: Einkaufsliste zuerst, W60 danach.

## DoD
Dateien aus dem Blatt vorhanden; `check_bom.py` gruen; fuenf Pruefpunkte vom Pruefer gemessen; Seite per Screenshot geprueft; Entscheidungen der Offen-Liste in `docs/decisions.md`; Wunschbuch W59 nachgefuehrt; Commit und Push je Teilschritt.
