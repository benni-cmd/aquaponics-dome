# Nachtkette N-UNIFY-AUTOBAHN (Ben 11.11.2026: „bis zum Ziel komplett fertig, ohne Unterbrechungen, morgen früh Ergebnis; keinen localhost starten, am Ende alles sauber beenden“)

Jede Runde läuft in einer eigenen Sitzung. Alle Sitzungen starten gleichzeitig und **warten**, bis die Plan-Zeile ihres
Vorgängers im Paket `docs/packages/n-unify-autobahn.md` auf `**erledigt**` oder `**teilweise**` steht. Erst dann arbeiten sie.

| Runde | Wartet auf Plan-Zeile | Auftrag (`docs/jobs/api/`) | Setzt am Ende Plan-Zeile |
|---|---|---|---|
| U7 Montage | U6 | `unify-u7-montage.md` | U7 |
| U8 Daten | U7 | `unify-u8-daten.md` | U8 |
| U9 Montage | U8 | `unify-u9-montage.md` | U9 |
| U10 Viewer | U9 | `unify-u10-viewer.md` | U10 |
| Prüfer | U10 | `unify-pruef-pruefer.md` | P-Prüf |
| F1 Nachbesserung | P-Prüf | `unify-fix-nachbesserung.md` | F1 |
| N1 Nachprüfung + Abschluss | F1 | `unify-nachpruef.md` | N1 |

## Regeln für jede Sitzung
1. **Warten ohne Token zu verbrauchen:** als erstes im Hintergrund (Bash `run_in_background`, Arbeitsordner = Projektordner):
   `until grep -qE '^\| <VORGÄNGER> \|.*\*\*(erledigt|teilweise)' docs/packages/n-unify-autobahn.md; do sleep 120; done; echo START`
   und dann den Zug beenden. Weiter erst, wenn diese Hintergrundaufgabe gemeldet hat.
2. Dann den Auftrag vollständig abarbeiten. „Läuft über das Agent-SDK“ heißt: keine Rückfragen an Ben, fehlende Entscheidungen als ANNAHME in `docs/decisions.md`. D117: bauen wie in Leons Quelle, Bedenken nur in `docs/packages/n-unify-bedenken.md`.
3. **RAM (D137):** schwere SolidCraft-Läufe nur einzeln und nur unter 80 % RAM starten, keinen zweiten Python-Prozess daneben; `scripts/ram_guard.ps1` kann Prozesse ab 90 % beenden; dann Schritt sparsamer wiederholen. Nach jedem Teilschritt commit + push (Pfad-Commits; bei abgelehntem Push `git fetch` und erneut pushen).
4. **Kette nie abreißen lassen:** Gelingt die Runde nicht ganz, trotzdem die eigene Plan-Zeile auf `**teilweise** (Grund, was offen ist)` setzen, committen und pushen. Nur dieses Wort startet die nächste Runde.
5. Keinen dauerhaften localhost; ein lokaler Server nur kurz für eine Prüfung und danach beenden. Nichts deployen, nichts kaufen.
6. **N1 zusätzlich (Abschluss):** nach der Nachprüfung alle verbliebenen SolidCraft-/Python-/Server-Prozesse dieser Kette beenden, einen Ergebnisbericht `docs/berichte/unify-ergebnis-2026-11-11.md` schreiben (Ziel erreicht ja/nein gegen Paket-DoD, Prüfurteil, Bilder aus `renders/`, offene Punkte, Bedenkenliste B1 ff. zur Entscheidung, Kosten), committen, pushen und die Plan-Zeile N1 setzen.
