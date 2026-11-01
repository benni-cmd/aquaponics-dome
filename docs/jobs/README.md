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
