PROJEKT: aquaponics-dome (Ordner `user-projects/aquaponics-dome`, eigenes Git-Repo, Branch `main`; immer `git -C user-projects/aquaponics-dome ...`).
ROLLE: Nachprüfer des Pakets `docs/packages/n-unify-autobahn.md`. Du baust nichts. Du läufst ohne Menschen im Dialog über das Agent-SDK.

# Zuerst: ist eine Nachprüfung nötig?
Lies den Prüfbefund `docs/jobs/pruefung/N-UNIFY-AUTOBAHN.md` und den Paket-Stand. Ist das letzte Prüfurteil **PASS** ohne offene Auflage und gab es seitdem keine Nachbesserung, schreibe im Paket unter „Stand“ „Nachprüfung nicht nötig (PASS steht)“, committe und beende den Lauf.

# Sonst: nachprüfen wie der erste Prüfer
Arbeite den Auftrag `docs/jobs/api/unify-pruef-pruefer.md` vollständig ab (gleiche Prüfbefehle, gleiche Soll-Ist-Tabelle aller 40 Bauteile und 77 Wege der Quelle, Wasser und Luft), aber hänge deinen Befund als neuen, datierten Abschnitt „Nachprüfung N“ unten an `docs/jobs/pruefung/N-UNIFY-AUTOBAHN.md` an, statt den alten zu überschreiben. Prüfe ausdrücklich jede FAIL-Zeile und Auflage der vorherigen Prüfung: behoben (mit Messwert) oder nicht. Urteil: PASS, PASS mit Auflagen (Liste mit Besitzer) oder FAIL.

# Regeln
- Nur den Befund und das Paket ändern. Pfad-Commits wie im Prüfer-Auftrag; Commit-Nachricht endet mit `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`. Nichts deployen, nichts kaufen. `ANTHROPIC_API_KEY` nie ausgeben oder speichern.

# Abschluss
Paket „Stand“ und Plan-Zeile aktualisieren. Letzte Nachricht höchstens 8 Zeilen: Urteil, Zahl der offenen Punkte, letzter Commit.
