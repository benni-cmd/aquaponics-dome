# Endlos-Mechanik: wie das Gesamtkonstrukt weiterlaeuft (Stand 29.10.2026, 03:55)

Ziel (Ben): Das ganze Konstrukt (Integrator, Werkstatt, Orchestrator, Viewer, Recherche, Gauntlet) arbeitet endlos weiter, auch nach Limit-Abbruechen, bis Ben "stopp" sagt oder eine neue Phase nennt.

## Bausteine und woran sie haengen

| Baustein | Laeuft in | Neustart-Mechanik | Haelt, wenn ... | Schwachstelle |
|---|---|---|---|---|
| Integrator (Rolle I) | Sitzung "Kuppel mit Aquaponik in SolidCraft bauen" | (1) Orchestrator-Anstoss alle 30 min (Cron, nur solange Hauptsitzung offen); (2) dauerhafter Auftrag `dome-loop-hourly-fallback` (:41); (3) Einmalauftrag `dome-loop-restart-0715` | App offen | Wachter sieht nur Commits und ListAgents |
| Werkstatt (Rolle W) | Sitzung "Komponenten-Werkstatt Innenraum (Kuppel)" | wie oben, Rolle waehlt der Auftrag nach Alter des letzten Commits | App offen | gleiches Limit, pausiert zuerst bei Engpass |
| Orchestrator (Rolle O) | Hauptsitzung "Solidcraft GitHub installation" + (neu) dritte Rolle im dauerhaften Auftrag | Cron `25687a4a` (Hauptsitzung); dauerhafter Auftrag uebernimmt Rolle O, wenn nichts in den Orchestrator-Pfaden committet wurde | App offen; Zustand in `docs/orchestrator-state.md` | Kontext der Hauptsitzung (bei ca. 63 %); Cron nur in der Hauptsitzung |
| Viewer-Server | Hintergrundprozess der Hauptsitzung | Cron prueft `http://localhost:4410/api/state`, startet neu | Hauptsitzung offen oder Rolle O startet ihn | stirbt mit der Sitzung, Rolle O startet ihn |
| Gauntlet-Kritiker | Unter-Agenten der Bau-Sitzungen | je Meilenstein, ein Agent zur Zeit | Limit frei | verbraucht Limit |
| Recherche | Orchestrator (Aufträge R03, R06, R09, R11) | je Anstossrunde ein Auftrag | Limit frei | gemeinsames Limit |

## Stopp und Wiederaufnahme

Nur Bens ausdrueckliches "stopp" (oder eine neue Phase) beendet das Konstrukt, und zwar als **sauberer Stopp** nach `docs/clean-stop.md` (Sitzungen sichern, Automatik aus, alles gepusht, Gesamtzusammenfassung). Wiederaufnahme: `docs/resume.md`.

## Wachter-Regeln (verhindern Doppelarbeit)

1. Rolle waehlen: Alter des letzten Commits je Rollenpfad (Integrator: `designs/dome.sc scripts data/params.json docs/loop-state.md viewer`; Werkstatt: `designs/components docs/parts docs/workshop-state.md docs/workshop-log.md data/components renders/components`; Orchestrator: `docs/integration-board.md docs/research docs/research-queue.md docs/decisions.md docs/orchestrator-state.md`).
2. Eine Rolle nur uebernehmen, wenn ihr letzter Commit aelter als 20 Minuten ist UND `ListAgents` die zugehoerige Sitzung nicht als `busy` fuehrt (Sitzungsnamen: Integrator "Kuppel mit Aquaponik in SolidCraft bauen", Werkstatt "Komponenten-Werkstatt Innenraum (Kuppel)", Orchestrator "Solidcraft GitHub installation").
3. STOPP: Enthaelt `docs/loop-state.md` die Zeile "STOPP von Ben" oder nennt Ben eine neue Phase, beendet jeder Lauf sich.

## Was nach dem letzten Bauteil kommt (Endlos heisst: nie fertig)

Sind alle Klassen im Board `eingebaut` und alle Checks PASS: (1) Foto-Latte (ControlNet-Render gegen ref-4), (2) Detailstufe um eine Stufe anheben (L3 -> L4), (3) Gesamtansicht-Gauntlet mit schaerferem Blick (Kameras ref-4, ref-5, ref-6), (4) neue Phase nur durch Ben (Statik, Biologie, Elektrik, Betrieb).

## Bekannte Ausfallarten und Gegenmassnahmen

| Ausfall | Folge | Gegenmassnahme |
|---|---|---|
| 5-Stunden-Limit voll | beide Bau-Sitzungen enden mit Fehler | Checkpoints, naechster Anstoss/Auftrag macht weiter; ab 90 % wird die Werkstatt nicht angestossen |
| Wochenlimit voll (heute 53 %, Reset 30.10. 02:59) | alles steht bis zum Reset | `docs/orchestrator-state.md` nennt den Stand, Aufträge laufen danach selbst weiter |
| Hauptsitzung beendet/App geschlossen | Cron und Viewer weg | dauerhafter Auftrag uebernimmt Rolle O, App muss offen sein |
| Kontext der Hauptsitzung voll | Verdichtung | Zustand in `orchestrator-state.md`, `plan-process.md`, Board |
| Zwei Sitzungen in gleicher Rolle | doppelte Commits | Wachter mit Commit-Alter und ListAgents |
| Berechtigungs-Ablehnung (Auto-Modus) | Aktion fehlt | nicht umgehen, im Checkpoint vermerken, weiter mit anderem |
| Teures Bauteil ohne Commit > 20 min | Wachter koennte Doppelstart ausloesen | ListAgents-Pruefung (busy) verhindert es |

## Kontext-Hygiene (Ben, 29.10. 12:35) — Werkstatt und Montage halten ihren Kontext unter 50-60 %
Messwert beim Beschluss: Werkstatt 92 % (917k von 1M Token, davon 835k Nachrichten), Montage 11 %. Jeder weitere Zug liest den ganzen Kontext neu: das kostet Limit.
Regel nach jedem sinnvollen groesseren Schritt (ein Bauteil oder eine Klasse fertig, Commit + Push erledigt):
1. Eigenen Kontext messen (get_usage, session "self"). Unter 50 %: weiterarbeiten.
2. Ab 50 %: Zwischenstand in die eigene Zustandsdatei schreiben (Werkstatt docs/workshop-state.md, Montage docs/loop-state.md): erledigter Schritt, naechster Schritt aus dem Plan, offene Punkte, laufende Messwerte. Committen + pushen.
3. Dann `clear_session` mit session_id "self" als letzte Aktion des Zuges. Danach ist der Kontext leer; der Zustand liegt im Repo.
4. Nach dem Leeren startet der naechste Anstoss (Orchestrator oder stuendlicher Auffang) die Sitzung wieder: erst docs/resume.md (eigener Abschnitt), dann die Zustandsdatei, dann den obersten Schritt des eigenen Next-Steps-Plans.
Der Orchestrator darf eine Sitzung, die er gestartet hat und die idle ist, selbst leeren (clear_session mit ihrer ID), wenn sie ueber 60 % liegt und ihr Zustand committet ist.

## Kontext-Zuschnitt (Ben, 29.10. 12:40) — Arbeitssitzungen sehen nur ihre Aufgabe, der Orchestrator den Ueberblick
Grundsatz: Der Ueberblick lebt im Orchestrator (Board, Plaene, Entscheidungen, Abnahme) und im Repo. Werkstatt und Montage arbeiten je Auftrag mit einem engen Kontextpaket, nicht mit der Gesamtgeschichte.
- **Werkstatt: eine Komponente = ein Kontext.** Gebaut wird eine Klasse (z. B. Pumpe, Tuer) bis zur Fertigmeldung (Vorpruefung, Kritiker, Blatt, Commit + Push). Danach IMMER `clear_session` self, unabhaengig vom Fuellstand. Neuer Kontext = Zustandsdatei `docs/workshop-state.md` (nur Stand, naechster Schritt) + Scope-Card der naechsten Klasse + `docs/cad-standard.md` + `docs/detail-standard.md` + `docs/provenance.md` + die in der Scope-Card genannten Eingaben. NICHT lesen: workshop-log.md als Ganzes (nur die letzten 40 Zeilen), orchestrator-state.md, fremde Bauteilblaetter.
- **Montage: ein Schritt M<n> = ein Kontext.** Nach jedem erledigten Schritt `clear_session` self; neuer Kontext = `docs/loop-state.md` + der Schritt aus `docs/next-steps-montage.md` + `data/layout.json` (nur benoetigte Teile) + Board-Zeile der betroffenen Klassen.
- **Orchestrator** liest die Fertigmeldungen und Blaetter, setzt das Board, schreibt die Auftraege (Scope-Card, Eingaben, Pruefung) so, dass die Arbeitssitzung nichts anderes braucht. Fehlt ihr etwas, steht das als Mangel im Auftrag, nicht als Sucharbeit der Sitzung.
- Anstoss nach dem Leeren (SendMessage): "Neuer Kontext: docs/resume.md Abschnitt Werkstatt (bzw. Montage), dann Zustandsdatei, dann Schritt <ID> aus deinem Plan."

## Bildverlauf (Ben, 29.10. 12:50) — alle Pruefbilder an EINEM Ort
Jedes Bild, das eine Sitzung als Pruefung erzeugt (Render, Schnitt, Kritiker-Bild, Nahaufnahme), wird zusaetzlich in `renders/history/` abgelegt, damit der Verlauf spaeter nachvollziehbar ist und Ben zwischendurch bewerten kann.
- Ablage per Befehl: `python scripts/archive_render.py <bild.png> --role werkstatt|montage --subject <klasse oder gesamt> --note "<kurz, z. B. Kritiker Runde 2>"` (mehrere Bilder moeglich). Das Skript benennt `YYYYMMDD-HHMMSS_<rolle>_<bauteil>_<name>`, vermerkt den Commit, ueberspringt identische Bilder und baut `renders/history/index.html` (Galerie, neueste zuerst, Filter Bauteil/Rolle) und `index.json` neu.
- Das Original bleibt am bisherigen Ort (Dokumente verweisen darauf); der Verlauf ist die Kopie. Zeitpunkt: direkt nach dem Render, vor dem Commit des Schritts; die Bilder gehoeren in denselben Commit (`git add renders/history`).
- Ansicht: http://localhost:4410/history/ (Link "Bildverlauf" im Viewer) oder `renders/history/index.html`.
- Bestand: 130 bisherige Bilder am 29.10. 12:48 einsortiert (`--backfill`).

## KORREKTUR 29.10. 13:00 (Ben) — NICHT leeren, komprimieren lassen
Die Regeln "clear_session self" in den Abschnitten Kontext-Hygiene und Kontext-Zuschnitt sind AUFGEHOBEN. Grund: Leeren loescht die Gespraechsgeschichte; eine geleerte Sitzung ist danach ein leerer Prozess, den der Orchestrator wegen der Sitzungspost-Sperre (Owner-Entscheid 27.08.) nicht mehr anstossen kann, die Endlosschleife reisst. Komprimieren behaelt eine Zusammenfassung und laeuft weiter.
Neue Regel: Sitzungen leeren sich NIE selbst. Der Kontext bleibt klein, weil jede Sitzung nur ihre Komponente bzw. ihren Schritt liest (Zustandsdatei, Scope-Card, Standards, Log nur letzte 40 Zeilen); wird er trotzdem gross, komprimiert das System automatisch (bei 97 %), und der Zustand liegt ohnehin im Repo (Zustandsdatei nach jedem Schritt committen). Manuelles Komprimieren (/compact) kann nur Ben in der jeweiligen Sitzung ausloesen.
