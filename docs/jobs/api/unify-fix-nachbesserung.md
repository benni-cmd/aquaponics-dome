PROJEKT: aquaponics-dome (Ordner `user-projects/aquaponics-dome`, eigenes Git-Repo, Branch `main`; immer `git -C user-projects/aquaponics-dome ...`).
ROLLE: Nachbesserung (Bau) des Pakets `docs/packages/n-unify-autobahn.md`, nach einem Prüfer-Lauf. Du läufst ohne Menschen im Dialog über das Agent-SDK. Fehlt eine Entscheidung, triff eine begründete Annahme (ANNAHME in `docs/decisions.md`, nächste freie D-Nummer) und mach weiter.

# Zuerst: ist überhaupt etwas zu tun?
Lies den neuesten Prüfbefund `docs/jobs/pruefung/N-UNIFY-AUTOBAHN.md` (bei mehreren Prüfungen den untersten Abschnitt). Steht dort das Urteil **PASS** ohne offene Auflage, dann ändere nichts, schreibe im Paket unter „Stand“ eine Zeile „Nachbesserung nicht nötig (Prüfer PASS)“, committe und beende den Lauf sofort. Gibt es keinen Prüfbefund, beende den Lauf ebenso mit dieser Feststellung.

# Sonst: Abweichungen zur Quelle beheben
Ziel ist der Zustand aus dem Paket (Goal und DoD): jedes Wasser- und Luft-Bauteil und jeder Weg der Quelle (`data/oasis-soll.json`, Quelle `docs/quellen/oasis-showcase-2026-11-10/` und `-nachtrag/`) an Lage und Höhe der Quelle gebaut (Wasserspiegel ±50 mm, Stufen 0 bis 5 exakt), eine einzige Variante, Listen und Beschreibungen vollständig, keine neue Kollision.
1. Lies `docs/designprinzipien.md`, `docs/decisions.md` (D93 bis D107 und später), `docs/jobs/N-UNIFY-AUTOBAHN.md` (Prüfbefehle je Runde) und den Prüfbefund.
2. Arbeite jede FAIL-Zeile und jede Auflage des Befunds ab, in der Reihenfolge Werkstatt → Montage → Daten → Viewer, mit denselben Werkzeugen und Regeln wie die Runden U2 bis U10 (`docs/jobs/api/unify-u*.md` zeigen Dateien, Befehle und Prüfwerte).
3. Danach die betroffenen Prüfbefehle erneut laufen lassen (mindestens `python -I -X utf8 scripts/check_oasis_soll.py --teil alle`, Gesamtbau `sh scripts/build.sh`, bei Geometrieänderung `check_latte` in einer Kopie). Messwerte ins Paket.
4. Was du nicht beheben kannst, steht mit Grund und Besitzer im Paket unter „Offen“.

# Regeln
- Pfad-Commits `git -C user-projects/aquaponics-dome commit -m "…" -- <pfade>`, neue Dateien vorher `add -N`; nach jedem Teilschritt committen und pushen. Commit-Nachricht endet mit `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Nichts deployen, nichts kaufen, keine Anmeldungen. `ANTHROPIC_API_KEY` nie ausgeben oder speichern.
- SolidCraft: installierte CLI `C:\Program Files\SolidCraft\solidcraft-cli.exe`. Lange Befehle (über 2 Minuten) im Hintergrund mit Log-Datei, Log mit kurzen Befehlen prüfen. `check_latte` nur in einer Kopie.
- Den Prüfbefund selbst nicht ändern: Er gehört dem Prüfer.

# Abschluss
Paket „Stand“: was behoben ist (Commits, Messwerte), was offen bleibt. Letzte Nachricht höchstens 10 Zeilen: behobene Punkte, offene Punkte, letzter Commit.
