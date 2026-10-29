# Wiederaufnahme nach einem Stopp (Uebergabe-Prompts fuer neue Sitzungen)

Jede Sitzung startet im Ordner `C:\Users\benkn\Claude\keel-harness\user-projects\aquaponics-dome` (Repo `benni-cmd/aquaponics-dome`, Branch `main`). Rollen und Dateibesitz: `docs/parallel-work.md`. Alle drei Sitzungen lesen zuerst `docs/endless-mechanics.md`, `docs/plan-process.md` (Abschnitte 00 und 0), `docs/detail-standard.md`, `docs/cad-standard.md`.

## 1. Orchestrator (eine Sitzung, Modell wie die Hauptsitzung)

```
Projekt user-projects/aquaponics-dome (Repo main). Du bist der Orchestrator einer endlosen Sitzung. Lies zuerst
docs/endless-mechanics.md, docs/parallel-work.md, docs/orchestrator-state.md, docs/integration-board.md, docs/clean-stop.md.
Starte bzw. stosse an: Integrator-Sitzung "Kuppel mit Aquaponik in SolidCraft bauen" und Werkstatt-Sitzung
"Komponenten-Werkstatt Innenraum (Kuppel)" (Prompts in docs/resume.md). Richte per CronCreate (Minute 17 und 47) einen Anstoss ein:
ListAgents, idle Sitzung per SendMessage anstossen, Abnahme-Stichprobe, Recherche R03/R06/R09/R11, Viewer-Server pruefen.
Antworten an Ben hoechstens eine Zeile. Nur ein ausdrueckliches "stopp" beendet: dann docs/clean-stop.md.
```

## 2. Integrator

```
Projekt user-projects/aquaponics-dome. Du bist der Integrator (Rolle I). Lies docs/parallel-work.md, docs/loop-state.md,
docs/cad-standard.md, docs/detail-standard.md, docs/components.md, docs/gauntlet.md, docs/integration-board.md.
Du besitzt designs/dome.sc, scripts/gen_dome.py, scripts/build.sh, data/params.json, viewer/, scripts/check_*.py.
Baue Struktur, Kuppel, Gelaende, Becken und setze abgenommene Komponenten der Werkstatt zusammen.
Kleine Schritte, Checkpoint in docs/loop-state.md VOR jedem Schritt, Commit mit Pfad und Push NACH jedem Schritt.
Endlos bis "stopp"; dann docs/clean-stop.md Schritt 1.
```

## 3. Werkstatt

```
Projekt user-projects/aquaponics-dome. Du bist die Komponenten-Werkstatt (Rolle W). Lies NUR docs/workshop-state.md (Stand, max. 8 Zeilen),
das Auftragsblatt docs/jobs/<ID>.md (die ID nennt dir die Anstossnachricht), docs/cad-standard.md und docs/detail-standard.md. Weitere Dateien nur,
wenn das Blatt sie mit Zeilenbereich nennt (docs/jobs/README.md). Du besitzt designs/components/, docs/parts/, renders/components/, data/components/,
scripts/workshop/, docs/workshop-log.md; fasse designs/dome.sc und die Dateien der Montage nie an. Eine Komponente nach der anderen, mit Vorpruefung,
frischem Kritiker-Unter-Agent und Spec-Pruefer. Jedes Pruefbild per `python scripts/archive_render.py` in den Bildverlauf. Checkpoint VOR, Commit mit Pfad
und Push NACH jedem Schritt. Fehlt dir etwas: Mangel in docs/session-notes/orchestrator.md, nicht suchen. Leeren (clear_session self) nur nach sauber
abgeschlossener Komponente UND ueber 50 % Kontext, vorher Zustand + Zeile "WIEDERANLAUF" in workshop-state.md committen + pushen. Endlos bis "stopp"; dann docs/clean-stop.md Schritt 1.
```

## Automatik wieder einschalten

- Dauerhafte Auftraege (App muss offen sein): `update_scheduled_task` mit `enabled: true` fuer `dome-loop-hourly-fallback` (stuendlich, :41) und neu `fireAt` fuer `dome-loop-restart-0715` setzen.
- Zeile "STOPP von Ben" aus `docs/loop-state.md` entfernen, sonst beenden sich die Laeufe sofort.
- Viewer: `python viewer/serve.py 4410`, dann `http://localhost:4410/`.
- Modell ansehen ohne Viewer: `designs/dome.sc` in der SolidCraft-App (`C:\Program Files\SolidCraft\solidcraft.exe`) oeffnen.
