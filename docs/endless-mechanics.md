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
