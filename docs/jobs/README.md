# Auftragsblaetter (Werkstatt) — der Orchestrator sagt konkret, was gebaut wird

Eine Werkstatt-Sitzung liest NUR: (1) ihr Auftragsblatt `docs/jobs/<ID>.md`, (2) `docs/cad-standard.md`, (3) `docs/detail-standard.md`.
Alles andere ist "bei Bedarf", mit Zeilenbereich oder Suchbegriff aus dem Auftragsblatt, nie ganz:
- `docs/provenance.md` erst beim Schreiben des Blatts; `docs/review-protocol.md` erst beim Kritiker-/Spec-Pruefer-Lauf; `docs/review-lessons.md` nur nach einem FAIL.
- NICHT lesen: `docs/parallel-work.md`, `docs/gauntlet.md`, `docs/endless-mechanics.md`, `docs/resume.md`, `docs/next-steps-workshop.md`, `docs/components.md` (ganz), `docs/scope-cards.md` (ganz), `docs/workshop-log.md` (ganz). Was daraus gebraucht wird, steht im Auftragsblatt.
- Zustand: `docs/workshop-state.md` (max. 8 Zeilen) nur beim Start; Regeln fuer Leeren/Wecken stehen im Prompt, nicht in Dateien.
Aufbau jedes Blatts: Ziel in einem Satz · Eingaben (Datei, Zeilen) · Ergebnis (Dateien) · Pruefung · nicht anfassen · danach.
Fehlt der Sitzung etwas, schreibt sie es als Mangel in `docs/session-notes/orchestrator.md`, statt zu suchen.
