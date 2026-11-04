# Work package: N-STUECKLISTE Einkaufsliste nach Typ (buendelt N-KATALOG, N-STUECKLISTE, N-BESCHAFFUNG)

**Problem:** Es gibt keine gemeinsame Liste aller Kaufteile der Kuppel: Mengen stehen im Modell (4880 Instanzen, 152 Definitionen), Teile in 25 Komponentenmodellen, Quellen nur fuer 14 Teile in R52, Preise und Links fehlen ganz; der Mini-Katalog (`data/katalog.json`, pilot) kennt 17 Eintraege.
**Intent:** Ben (W59, 04.11.2026): jedes Einzelteil nach Typ indexiert in EINER Einkaufsliste mit groben Stueck- und Gesamtpreisen und Bestell-Link mit Lieferung nach Deutschland; Zahlen aus einem festen Skript (W45), Bezug mindestens Europa (D76).
**Goal:** `python -X utf8 scripts/bom.py` erzeugt `data/stueckliste.json` und `docs/einkaufsliste.html`; Summen gleich Modellzaehlung (`scripts/check_bom.py` Exit 0); jede Zeile mit Preis, Datum, Quelle, Land, Link oder mit benanntem OFFEN-Grund. Blatt: `docs/jobs/N-STUECKLISTE.md`

## Plan
1. [x] Werkstatt 1a: Typ-Index und Artikelliste aus allen Komponenten-`.sc` (Preise leer), sofort committen (04.11.2026, `scripts/bom_artikel.py`, `data/katalog.json`)
2. [x] Werkstatt 1b: `data/bom_regeln.json`, unbenannte Koerper (`Body<n>`) benennen (04.11.2026, a83f21a; Benennung per Regel in der Stueckliste, `.sc` unveraendert)
3. [x] Werkstatt 1c: `scripts/bom.py` (Zaehlung, Zuschnitt 1D) und `scripts/check_bom.py` (04.11.2026, check_bom 13 von 13 PASS)
4. [x] Werkstatt 1d: `data/stueckliste.json`, `docs/stueckliste.md` (04.11.2026)
5. [ ] Recherche 2A Stahl und Normteile (`data/beschaffung/stahl.json`)
6. [ ] Recherche 2B Wasserleitung, L21 (`data/beschaffung/leitung.json`; E20-abhaengig: OFFEN (E20))
7. [ ] Recherche 2C Behaelter, Becken, Pumpen (`data/beschaffung/behaelter.json`; Subtank: OFFEN (Subtank))
8. [ ] Recherche 2D Messtechnik und Elektrik (`data/beschaffung/mess_elektrik.json`)
9. [ ] Recherche 2E Huelle, Toepfe, Substrat, Gewebe (`data/beschaffung/huelle_pflanze.json`)
10. [x] Zusammenfuehrung und Seite `docs/einkaufsliste.html`, Screenshot-Abnahme (04.11.2026; Desktop und 390 px im Browser-Pane)
11. [ ] Pruefer: `docs/jobs/pruefung/N-STUECKLISTE.md` nach fuenf Pruefpunkten
11b. [x] Seite interaktiv, Gruppieren/Sortieren, Desktop-Verknuepfung (04.11.2026; lnk nach Bens ausdruecklichem Wunsch W59 angelegt: Desktop, Datei Einkaufsliste Kuppel.lnk)
11c. [ ] W60: Teiledaten fuer alle Bauteile in 5 Gruppen (Werkstatt, parallel nach 1b), dann Viewer-Anbindung Preis/Link, Pruefer (Pruefpunkte 6 und 7 im Blatt)
12. [ ] Orchestrator: Roadmap nachfuehren (N-KATALOG, N-STUECKLISTE, N-BESCHAFFUNG gebuendelt, N-BOM-PARAM bleibt)

Reihenfolge: 1a vor 2A bis 2E (Artikelliste); 2A bis 2E parallel; 10 nach 1d und 2A bis 2E; 11 zuletzt. Eine Sitzung = ein Schritt (D74).

## Stand
04.11.2026, Planer (Sonnet 5.5): Blatt geschrieben, Aktualitaet **angepasst** (B1 liegt nur fuer 2 von 25 Komponenten vor, deshalb Namensregeln statt voller B1; D69 durch W59 auf grobe Preise erweitert; E20 und Subtank als OFFEN-Status gefuehrt). Messung unbenannter Koerper: `nft_tisch_mitte.sc` 40 von 124; Messung ueber alle Komponenten folgt in 1a. OFFEN (Ben): Preise brutto oder netto (Empfehlung brutto); UK als Europa; Pflanzgut/Fisch/Beton/Aushub in die Liste (Empfehlung nein).

04.11.2026, Nachtraege eingearbeitet: W59 (interaktive Seite, Sortieren, Gruppieren mit Gruppenpreis, Desktop-Verknuepfung) als Paket 3b; W60 (Detailansicht aller Bauteile, verknuepft mit Einkaufsliste) als Paket 5 mit gemeinsamem Datenmodell `data/parts` + `artikel_id`; Pruefpunkte 6 und 7. Zusatz: 6 bis 7 Sitzungen. Empfehlung: Einkaufsliste zuerst, W60 danach.

04.11.2026, Werkstatt 1a gebaut: `data/katalog.json` traegt zusaetzlich `typen` (17 Kuerzel), `artikel` (239 Zeilen, Preise leer, Status OFFEN (Quelle)), `artikel_ausnahmen`, `artikel_ungeklaert` (0), `artikel_stempel`. Messung: 301 `.sc` per `solidcraft-cli eval` (`python -X utf8 scripts/bom_artikel.py --messen`, rund 15 min) -> 2349 Koerper, Cache `data/bom_koerper.json`. Stempel: instances `built` 2026-11-04 01:33:42, sc_sha256 38162d73c8f590cb, `ibc_beet*` 41f3f1c81fe299e5 (W40-BEET-Stand). Typen: FIT 73, SON 31, BLE 17, BEH 16, MES 16, ARM 16, SCH 18, PRF 14, ROH 12, TOP 3, SRB 4, WNK 6, ELE 4, PMP 3, FOL 5, GEW 1 (`python -c` ueber `katalog.json` `artikel`). 112 von 239 Artikeln kommen nur in Komponenten ohne Instanz im Modellstand vor (`ohne_instanz_im_modell`), z. B. Haut, Keilschiene, Halter, Dosierstation. Ausgenommen (Entscheidung 04.11.): Salat 98 Koerper, Massfigur 43, Wasserkoerper 7, Beton 2, Aushub 1. Unbenannte Koerper (`Body<n>`) sind den Artikeln `SRB-*` und `BLE-platte-30x30x3` mit Hinweis `unbenannt` zugeordnet (Zahl nach Namensregeln folgt in 1b).
Bekannte Naeherungen fuer 1b/2A: Profilwand aus Modellmasse gerechnet [E] (z. B. 40x40: Wand 2,5 und 3 mm gemischt, vereinheitlichen); Strebenprofil als Platzhalterkoerper (Laenge aus Bbox, Profil 30x30 laut strut_cutting); Diagonalen als Flachstahl 3 mm ohne Breite; IBC-Gebinde als ein Artikel; Rohr-Laengen aus Bbox (L-Stuecke ungenau); Kugelhahn-Nennweite je Bauteil angenommen [A].

04.11.2026, Werkstatt 1b bis 1d gebaut (Messbefehle: `python -X utf8 scripts/check_bom.py`, `python -X utf8 scripts/bom.py`):
- Benennung: 740 unbenannte Koerper, alle per Gestalt-Regel (`scripts/bom_benennung.py`, Daten `data/bom_regeln.json` `benennung`) als Schraube, Mutter oder Scheibe benannt, 0 ungeklaert. Mutter und Scheibe zaehlen im Schraubensatz (Schraube + Mutter + 2 Scheiben, Einheit Satz, IDs `SRB-satz-<gewinde>x<laenge>`). Die `.sc` bleiben unveraendert: Abweichung vom Blatt (dort: Benennung im Werkstatt-Skript je Komponente), Grund: 45 Komponenten aus rund 20 Skripten, Rebuild-Risiko, andere Sitzungen bauen parallel; die Regel wirkt auch nach jedem Rebuild.
- Neu mitgezaehlt: 7 Komponenten aus W37-2/W37-3 (`classify_w37` in `scripts/bom_artikel.py`, Annahmen mit [A] und Hinweis `w37_annahme`), Nachmessung per `bom_artikel.py --ergaenzen`; Katalog jetzt 260 Artikel, 0 ungeklaert.
- Ausgabe: 260 Zeilen, Summe der platzierten Zeilen mit Preis 28.510,25 EUR brutto; 37 platzierte Zeilen ohne Preis (benannter Grund je Zeile); `data/stueckliste.json` erzeugt in zwei Laeufen identisch (sha256 636750845d9e).
- Befund (Entscheidung noetig): 130 von 260 Zeilen stehen nur in Komponenten OHNE Instanz im Modell (`viewer/instances.json`), darunter Huelle (Haut, Tuer, Keilschiene), Messtechnik, Puffer-Station, Aktivkohle. Sie zaehlen Menge 0 und nicht in die Summe; je 1 Stueck gerechnet waeren es weitere 2.279,02 EUR (36 Zeilen, ohne lt_-Bibliothek). Davon 105 Komponenten lt_* sind ungenutzte Bibliotheksvarianten.
- Befund fuer Recherche 2A: Preise unter `SRB-m8x35`, `SRB-knoten-klein`, `SRB-pumpe-klein`, `BLE-platte-30x30x3` haben keinen Katalogartikel mehr (Schrauben jetzt je Gewinde und Laenge). `SRB-satz-m6x20` erbt den Preis ueber `preis_alias`; neu zu bepreisen: `SRB-satz-m5x12`, `m6x16`, `m6x40`, `m6x55`, `m8x30`, `m10x60`, `m12x55`, `m16x300`.
- Nicht Teil von 1b bis 1d, offen: Geruestdateien `data/parts/<komp>.json` fuer alle Komponenten (W60, Blatt Paket 5), Seite `docs/einkaufsliste.html` (Paket 3).

04.11.2026, Werkstatt Paket 3 und 3b: `scripts/bom_seite.py` + `scripts/bom_seite_vorlage.html` erzeugen `docs/einkaufsliste.html` (eine Datei, offline, wird von `bom.py` mitgeschrieben); `scripts/open_einkaufsliste.bat`, `scripts/make_shortcut.ps1`. Gemessen im Browser: Summe Seite = Summe Datei 28.510,25 EUR; Summe der 8 Gruppenpreise 28.510,25; Preis absteigend erste Zeile 2.607,00 = Maximum, aufsteigend 1,08 = Minimum; 16 von 16 Typen mit Sprungpunkt; Zaehler Preis fehlt 37 = 37; externe Requests 0; schmale Breite 390 px ohne waagerechtes Scrollen. Anzeige-Entscheidung: nicht platzierte Komponenten sind standardmaessig ausgeblendet (Haken zeigt sie), nicht in der Summe. Seite zeigt Drift-Hinweis, wenn sich die `.sc` seit der Messung geaendert haben (aktuell ja: W40-BEET).

## DoD
Dateien aus dem Blatt vorhanden; `check_bom.py` gruen; fuenf Pruefpunkte vom Pruefer gemessen; Seite per Screenshot geprueft; Entscheidungen der Offen-Liste in `docs/decisions.md`; Wunschbuch W59 nachgefuehrt; Commit und Push je Teilschritt.
