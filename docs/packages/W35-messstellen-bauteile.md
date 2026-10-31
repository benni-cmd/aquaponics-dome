# Paket W35 — Messstellen-Bauteile: Halter und Sonden-Platzhalter (Werkstatt, Auftrag docs/jobs/W35-messstellen-bauteile.md, R39, D65)

## PIG
- **Problem:** R39 plant 67 Messstellen (22 Pflicht, 45 Zusatz) in `data/messstellen.json`, im Modell gibt es dafuer keine Bauteile. Ohne Halter und Sonden fehlen sie in Stueckliste, Viewer und Leitungsplan; die Montage kann sie nicht setzen.
- **Intent:** Standard vor Sonderloesung: handelsuebliche Rohre d20/d32/d40/d63, Kugelhahn, Klemmen, IP65-Gehaeuse; je Sondentyp ein schlichter Platzhalter in Hersteller-Farbe und -Mass, damit die Montage jede Messstelle mit einem Bauteil besetzen kann.
- **Goal:** Die acht Halter H_TAUCH, H_BERUHIG, H_ZELLE, H_INLINE, H_HAHN, H_DRUCK, H_MAST, H_BOX als Komponenten `halter_*.sc` mit Ports; die 14 Sondentypen als `sonde_*.sc` (je ein Koerper, Kabelport); Blatt `docs/parts/messstellen.md` (Q/E/A, Preis aus R39, Kalibrierintervall, Lebensmittelkontakt); `data/descriptions.json` (Gruppen `^halter_`, `^sonde_`); `scripts/workshop/check_messstellen.py` gruen; Zahl der Koerper je Komponente = Zahl der Teile-Zeilen im Blatt (Roadmap B1); ein Render mit Figur als Massstab.

## Plan (ein WIP-Commit je Schritt)
1. Spezifikation und Generator `scripts/workshop/messstellen.py` (alle Halter und Sonden aus einer Tabelle); Halter H_TAUCH, H_BERUHIG, H_ZELLE bauen, Check.
2. H_INLINE (d32 und d50), H_HAHN, H_DRUCK, H_MAST, H_BOX bauen, Check.
3. 14 Sonden-Platzhalter mit Kabelport, Check.
4. Blatt `docs/parts/messstellen.md`, `data/descriptions.json`, Render mit Figur 1,80 m, Stand und Log.

## Annahmen und Luecken
- `data/messstellen.json` enthaelt keine Abmessungen der Sonden (nur Name, Technik, Preis, Kabelart, Adern). Die Hersteller-Datenblaetter sind nicht gelesen: **alle Sondenmasse sind Annahme [A]**, gerundet; Farbe nach Hersteller-Erscheinung geschaetzt. Das wird im Blatt je Zeile ausgewiesen und in `docs/workshop-state.md` gemeldet.
- H_INLINE kommt als zwei Groessen: d32 (flow_12 an K12/K28 und kleinere Leitungen) und d50 (flow_gross an K10/K26, Soll 110 l/min); die Rohrdurchmesser je Kante stehen nur in `leitungsnetz.json` (nicht anfassen), d40/d25-Kanten nehmen d32 bzw. d50 mit Reduzierung (offen).
- Ports an Rohren sind Anlagen (Anbohrschelle, Stutzen); die Rohrmuffen der Bibliothek T70 werden nicht nachgebaut.

## Stand
Geplant, noch nichts gebaut.

## DoD
Alle 8 Halter und 14 Sonden gebaut, Check gruen (Zahlen im Stand), Blatt und descriptions nachgefuehrt, Render im Bildverlauf, WIP-Commits gepusht, `docs/workshop-state.md` und `docs/workshop-log.md` nachgefuehrt.
