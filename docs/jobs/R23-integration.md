# R23 Empfehlung in Kennzahlen, Beschreibungen und Konzept uebernehmen
Ziel: Viewer-Uebersicht und Bauteilbeschreibungen zeigen die geprueften Auslegungswerte, Bens Tabellenwerte stehen daneben.
Eingaben: `docs/research/aquaponik-empfehlung.md` (Abschnitt 2 und 3), `aquaponik-werte.md`; D38 in `docs/decisions.md`.
Aendern: `scripts/system_specs.py` (Biomasse 350 kg statt 1839 x 0,7; Futter 3,5 kg/Tag; TAN 3,75 %; NFT 1 l/min; PUMP_EFF 0,25; Substratflaeche 27,3 m2; Konsistenzzeilen gegen 45 g/m2; Filter Faustregel und FAO-Tabelle; O2 aus Biomasse; Heizung als eigene Zeile; Tabellenwert Ben jeweils als zweiter Wert), `data/system-specs.json` (Ausgabe), `data/descriptions.json` (Gruppen pumpe, tank, ibc_beet, nft: Hauptkreislauf = 4 pumpe_gross, Absetzer-Teilstrom = 4 pumpe_klein), `docs/system-concept.md`, `docs/hydraulics.md`.
Nicht anfassen: `viewer/index.html`, `designs/`, `dome.sc`, Komponentenblaetter (Werkstatt W24).
Wenn die Viewer-Felder neue Schluessel brauchen (z. B. heizung): in `system-specs.json` ergaenzen und im Ergebnis melden, der Orchestrator passt den Viewer an.
Ergebnis: `python scripts/system_specs.py` laeuft, Zahlen mit Q/E/A-Herkunft, WIP-Commit mit Pfad, Push, Kurzmeldung mit den neuen Kennzahlen und offenen Fragen an Ben.
