# Auftragsblaetter (Werkstatt) — der Orchestrator sagt konkret, was gebaut wird

**Orchestrator-Regel (Ben 01.11.2026):** Aktualitaetspruefung vor jedem Roadmap-Start (Ben 01.11.2026): Bevor ein Schritt der Roadmap beauftragt wird, prueft der Orchestrator, ob Blatt und Aufgabe noch aktuell sind oder ob vorherige Schritte, Entscheidungen oder Befunde sie veraendert haben (Eingaben, Annahmen, Reihenfolge, erledigte oder entfallene Teile). Ergebnis steht als Abschnitt "Aktualitaetspruefung" im Auftragsblatt und geht dem alten Text vor; der Auftrag nennt die ersetzten Eingaben. Ist die Aufgabe hinfaellig oder wesentlich geaendert, geht sie zuerst zu Ben.

Eine Werkstatt-Sitzung liest NUR: (1) ihr Auftragsblatt `docs/jobs/<ID>.md`, (2) `docs/cad-standard.md`, (3) `docs/detail-standard.md`.
Alles andere ist "bei Bedarf", mit Zeilenbereich oder Suchbegriff aus dem Auftragsblatt, nie ganz:
- `docs/provenance.md` erst beim Schreiben des Blatts; `docs/review-protocol.md` erst beim Kritiker-/Spec-Pruefer-Lauf; `docs/review-lessons.md` nur nach einem FAIL.
- NICHT lesen: `docs/parallel-work.md`, `docs/gauntlet.md`, `docs/endless-mechanics.md`, `docs/resume.md`, `docs/next-steps-workshop.md`, `docs/components.md` (ganz), `docs/scope-cards.md` (ganz), `docs/workshop-log.md` (ganz). Was daraus gebraucht wird, steht im Auftragsblatt.
- Zustand: `docs/workshop-state.md` (max. 8 Zeilen) nur beim Start; Regeln fuer Leeren/Wecken stehen im Prompt, nicht in Dateien.
Aufbau jedes Blatts: Ziel in einem Satz · Eingaben (Datei, Zeilen) · Ergebnis (Dateien) · Pruefung · nicht anfassen · danach.
Fehlt der Sitzung etwas, schreibt sie es als Mangel in `docs/session-notes/orchestrator.md`, statt zu suchen.
Besonderheiten: Faellt einer Sitzung eine ungewoehnliche Loesung oder ein Vorteil auf, meldet sie in der Kurzmeldung eine Zeile "Besonderheit: ..."; der Orchestrator traegt sie in `docs/pitch-besonderheiten.md` ein (Wunsch W48).

## Sitzungsarten Planer und Pruefer (Standard seit 01.11.2026, Ben E18)
Ablauf je Schritt: Orchestrator -> **Planer** (schreibt `docs/jobs/<ID>.md` mit Aktualitaetspruefung und Pruefpunkten) -> Orchestrator liest nur Blatt und Kurzmeldung und gibt frei -> **Bau-Sitzung** (Montage, Werkstatt, Recherche) -> **Pruefer** (misst nach, `docs/jobs/pruefung/<ID>.md`) -> Orchestrator -> Ben.
Vorlagen: `docs/jobs/vorlagen/planung.md` und `docs/jobs/vorlagen/pruefung.md`; der Start-Prompt des Orchestrators enthaelt nur die feste Kopfzeile (Projekt, cd, keine AskUserQuestion) plus Schritt-ID und drei bis fuenf Zeilen Brief.
Nicht noetig fuer kleine Orchestrator-Arbeiten (Netzliste, Roadmap) und Wiederanlauf eines schon geplanten Schritts. Eine Sitzung gleichzeitig schreibt; Planer und Pruefer lesen nur und schreiben je eine eigene Datei.
Sitzungsstart ohne Kontext-Frage (Ben 01.11.2026): Vor jedem `start_session` setzt der Orchestrator die Marke per `node -e "require('fs').writeFileSync(require('os').tmpdir()+'/keel-subsession-marker.json', JSON.stringify({bis: Date.now()+600000}))"` (gilt 10 Minuten); der Hook `.claude/project-context.js` bleibt dann stumm. Zusaetzlich beginnt jeder Start-Prompt mit "PROJEKT: <name>".
Aenderung 01.11.2026 spaet: Die Kontext-Frage entscheidet jetzt der Hook bei der ERSTEN Nachricht: beginnt der Start-Prompt mit "PROJEKT: <name>", bleibt er stumm, die Marke ist nur noch Rueckfall (Beleg steht aus, bis eine echte Subsession ohne Marke gestartet wurde).

## Kontext- und Limitregeln fuer ALLE Sitzungen (Ben 01.11.2026)
1. Eine Sitzung = ein Arbeitspaket (eine Schritt-ID oder ein Buendel mit denselben Eingaben). Ein neues Thema bekommt eine NEUE Sitzung, auch wenn eine untaetige Sitzung derselben Rolle existiert; eine bestehende Sitzung wird nur fuer den Wiederanlauf desselben Pakets genutzt (Limit, Build).
2. Planer und Pruefer arbeiten je Schritt (PLAN-<ID>, PRUEF-<ID>), nie mehrere Schritte nacheinander in einer Sitzung; ein Planer darf mehrere Blaetter schreiben, wenn sie zum selben Buendel gehoeren und dieselben Eingaben teilen (Pilot W37/W39).
3. Nur die im Blatt genannten Eingaben lesen; grosse Dateien mit Grep oder Offset und Limit; keine Ordner durchsuchen; Bilder nur, wenn ein Pruefpunkt sie nennt.
4. Ergebnisse stehen in Dateien, die Chat-Meldung hat hoechstens sechs Zeilen; nach der Meldung STOPP, keine Folgeaufgaben.
5. Ab etwa 60 Prozent Kontextfuellung nach dem letzten Commit den Stand ins Blatt oder in den Zustand schreiben und stoppen; die Fortsetzung macht eine neue Sitzung (Wiederanlauf).
6. Modell und Aufwand: Planer und Pruefer Sonnet mit Aufwand medium; Bau-Sitzungen mit Geometrie high.
7. Orchestrator: liest Blatt, Befund und Kurzmeldung, nicht die Recherche-Volltexte; ein Thema, das mehr als wenige Aufrufe braucht, geht in eine neue Sitzung, nicht in die Orchestrator-Sitzung.
