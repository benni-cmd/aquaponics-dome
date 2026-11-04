# Start-Auftrag: Viewer N-STUECKLISTE Schritt 5b (Preis, Link, Menge in der Detailansicht)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Viewer. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Grundlage: `docs/jobs/N-STUECKLISTE.md` Punkt 5b (Zeile 47) und Pruefpunkt 7 (Zeile 77); Teiledaten aller 308 Komponenten in `data/parts/` (5a fertig, 5340b4b); `data/stueckliste.json`, `docs/einkaufsliste.html`.
2. Bauen: Teileliste und Infokarte der Detailansicht zeigen Menge, Stueckpreis, Bestell-Link und Gruppenpreis der Komponente (liest `stueckliste.json` nur bei Bedarf); Rueckverweis aus der Einkaufsliste auf die Detailansicht (Teil-ID als Sprungmarke).
3. Mit erledigen: Pilot-Auflagen A1 bis A3 aus `docs/jobs/pruefung/N-DETAIL-PILOT.md` (keine Register-Kuerzel oder Parameternamen in Anzeigetexten, "1 Teil" statt "1 Teile", "Schieber 1"); in der Ansicht Technisch Leitungen nach Leitungsart (Zulauf, Ruecklauf, Luft, Frischwasser, Kabel) statt Rohrgroesse, Leitungsart aus `data/leitungsnetz.json`/`data/leitungstrassen.json` ableiten (nur lesen) und in einer Viewer-Nebendatei ablegen; Nahansicht Tisch als Screenshot nachliefern.
4. Parallel laeuft `check_latte 69` (liest die Bauteile): kein Modellbau, nichts in `designs/`, `scripts/components/`, `gen_dome.py`; Viewer-Export nur am Muster in einer Kopie.
5. Messen nach Pruefpunkt 7 (Stichproben Tisch, Pumpe, Rohrbogen: Menge, Preis, Link gleich der Einkaufsliste), Screenshot gegen `..\..\docs\ui-standard.md`, Paket `docs/packages/n-stueckliste.md` nachfuehren. Commits nur per Pfad, Push, WIP alle 20 Minuten. Danach STOPP.
