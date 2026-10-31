# M10 Schlaeuche, Rohre und Kabel verlegen (Ben 31.10., D50) — NACH R28 (Netzliste) und W30 (Stands)
Problem: Es sind noch keine Rohre, Schlaeuche und Kabel verlegt. Ben: komplett, logisch und stimmig; danach Kollisionspruefung, dann Pause und Zwischencheck.
Ziel: Alle Leitungen laut `data/leitungsnetz.json` (R28) im Modell: Wasser (Rohr DN 50/63/32, Schlauch 20 fuer den Tisch-Zulauf), Luft (Belueftungsleitungen), Strom (Kabeltrassen vom Schaltschrank), ohne Kollision, Laufwege >= 500 mm frei (Rohre unter Flur oder an Wand/Beinen, nicht quer ueber Laufwege), Gefaelle, Anschluesse an die Ports der Bauteile.
Pflicht VOR dem Bau: Plan im Paket `docs/packages/m10-leitungen.md` (Problem-Intent-Goal, Reihenfolge, Trassenregeln: Ringsammler, Abgaenge je Sektor, Hoehenlagen, Befestigung). WIP-Commit, dem Orchestrator melden, vom Orchestrator gegenlesen lassen, erst dann bauen.
Eingaben: `data/leitungsnetz.json`, `docs/filter-konzept.md`, `docs/parts/leitungsteile.md` (Bibliothek aus W10: Rohr, Bogen, T, Kugelhahn, Kupplung, Schlauch, Klemme, Verteiler mit Ports), `docs/hydraulics.md` (Abschnitt Leitungen), `scripts/check_hydraulics.py` (falls vorhanden), D38, D46, D50.
Schritte:
1. Plan.
2. Hauptkreislauf Pool -> Absetzer -> Biofilter -> Puffer -> Pumpen -> Verteiler.
3. Verteilung Beete/NFT je Linie und Rueckfluss.
4. Belueftung, Drittbecken, Zweitbecken.
5. Kabel (Trassen).
6. check_walkways, EIN check_latte mit Leitungen, Draufsicht und Seitenansicht in den Bildverlauf. Je Schritt WIP-Commit.
Nicht anfassen: Werkstatt-Komponenten; fehlt ein Leitungsteil, melden (Werkstatt-Notiz) statt selbst bauen.
Danach PAUSE: Zwischencheck mit Ben; `docs/model-description.md` und `docs/integration-board.md` pflegen.
