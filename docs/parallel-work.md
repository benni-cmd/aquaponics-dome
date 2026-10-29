# Parallele Arbeit: Integrator, Komponenten-Werkstatt, Orchestrator (ab 29.10.2026, 03:35)

Ziel: Bauteile werden parallel und unabhaengig verfeinert, das Gesamtmodell bleibt sauber und wird nur an einer Stelle zusammengesetzt; jedes Bauteil geht durch den Gauntlet, bevor es ins Modell kommt.

## AENDERUNG 29.10.2026 04:15 (Ben): Neue Aufteilung
- Die erste Sitzung ("Kuppel mit Aquaponik in SolidCraft bauen", Rolle Integrator) wird sauber beendet. An ihre Stelle tritt die Sitzung **"Montage und Layout (Kuppel)" (Rolle M)**: Layout und Anordnung der Komponenten, Zwischenbauteile (Streben, Knoten, Anker, Tuer, Haut, Rohre, Schlaeuche, Verteiler, Ventile, Klemmen), Wasserweg-Graph, Zusammenbau, Gesamtchecks, Viewer. Plan: `docs/next-steps-montage.md`.
- Die **Werkstatt** (Rolle W) baut die grossen Funktionsbauteile: NFT-Tische, Beete, Tanks, Pumpen/Filter, Pflanzen. Plan: `docs/next-steps-workshop.md`.
- **Rollender Plan:** Fuer W und M liegt immer ein ausdefinierter Plan fuer die naechsten 3-5 Schritte vor (je Schritt Ziel, Eingaben, Ergebnis, Pruefung, Abhaengigkeit). Der Orchestrator fuellt auf, sobald ein Schritt fertig ist oder eine Sitzung meldet, dass nur noch 2 Schritte uebrig sind. Eine Sitzung ohne definierten Schritt meldet das sofort.
- Wo unten "Integrator" steht, ist ab der neuen Sitzung "Montage" (Rolle M) gemeint.

## Rollen

| Rolle | Wer | Besitzt (nur hier schreiben) | Aufgabe |
|---|---|---|---|
| **Orchestrator** | Hauptsitzung "Solidcraft GitHub installation" | `docs/integration-board.md`, `docs/research/*`, `docs/research-queue.md`, `docs/decisions.md`, Plan-Dokumente | Aufgaben verteilen, Recherche, Stichproben am Render, Abnahme-Status setzen, Limit beobachten |
| **Integrator** | Sitzung "Kuppel mit Aquaponik in SolidCraft bauen" | `designs/dome.sc`, `scripts/gen_dome.py`, `scripts/build.sh`, `data/params.json`, `data/layout.json`-Verbraucher, `viewer/`, `scripts/check_*.py` | Baugruppenstruktur (cad-standard), Layout, Kuppel (Streben, Knoten, Tuer, Anker, Haut), Gelaende, Becken, Zusammenbau der abgenommenen Komponenten per `component.insert_design`/`update_links`, Gesamtchecks |
| **Werkstatt** | Sitzung "Komponenten-Werkstatt Innenraum" | `designs/components/<ihre Klassen>.sc`, `docs/parts/<klasse>.md`, `renders/components/<klasse>/`, `data/components/<klasse>.json` (eigene Parameter), `docs/workshop-log.md` | Bauteile Salatkopf, Netztopf, NFT-Rinne, NFT-Tisch (3 Ringe), IBC-Beet (Kies, Siphon), Tank (Vortex/Biofilter mit Kegel, Plattform, Fittings), Pumpe/Filtermodul isoliert bis L3/L4 (`docs/detail-standard.md`) |

Keine Sitzung schreibt in Dateien einer anderen Rolle. Aenderungswuensche an fremde Dateien gehen per `SendMessage` an den Besitzer.

## Regeln gegen Konflikte (gleiches Arbeitsverzeichnis)

1. Commit immer mit Pfad: `git -C <repo> commit -m ... -- <eigene Pfade>`; nie `add -A`, nie `commit -a`. Push danach; bei Ablehnung `git pull --rebase` und erneut pushen.
2. Jede Komponente ist eine eigene `.sc`-Datei, damit nichts kollidiert; SolidCraft-Befehle nur auf die eigene Datei.
3. Die Werkstatt aendert nie `designs/dome.sc`; sie liefert Komponenten, der Integrator verknuepft sie.
4. Eigene Parameter der Werkstatt stehen in `data/components/<klasse>.json` (Wert, Einheit, Herkunft), der Integrator uebernimmt sie in `data/params.json`.
5. Fertigmeldung der Werkstatt je Komponente per `SendMessage` an den Orchestrator mit: Datei, Bauteilblatt, Nahaufnahme-Render, Ergebnis der Pruefungen, Kritiker-Urteil.

## Abnahme-Ablauf je Komponente (Gauntlet)

Entwurf (Werkstatt) -> Werkstatt-Gauntlet (Bauer + getrennter Kritiker mit frischem Kontext, `docs/gauntlet.md`; bis 4 Runden, Zahlen aus `layout.json` und `components.md`) -> Meldung an Orchestrator -> Stichprobe des Orchestrators (Nahaufnahme gegen Referenzausschnitt ansehen, Pruefzahlen lesen) -> Status `abgenommen` im Board -> Integrator verknuepft, setzt Instanzen nach Layout, laeuft Gesamtchecks -> Gesamtansicht-Gauntlet mit `cam_ref4`.
Zwischenstufen im Board: `offen`, `in Arbeit`, `L2`, `L3`, `abgenommen`, `eingebaut`.

## Limit

Das Limit ist gemeinsam; zwei Bau-Sitzungen verbrauchen es schneller, bringen es aber nicht mehr (Stand 03:33: 5-Stunden-Limit 35 %, Wochenlimit 53 %). Beide arbeiten in kleinen Schritten mit Checkpoint vor jedem Schritt und Commit nach jedem Schritt. Ist das Fenster voll, pausieren beide, die geplanten Neustarts (07:15 und stuendlich) setzen aus den Checkpoints fort: Integrator `docs/loop-state.md`, Werkstatt `docs/workshop-state.md`. Sinkt das Limit unter 10 %, pausiert die Werkstatt zuerst (Orchestrator-Entscheidung).
