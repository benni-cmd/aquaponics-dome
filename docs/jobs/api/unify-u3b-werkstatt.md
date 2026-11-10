PROJEKT: aquaponics-dome (Ordner `user-projects/aquaponics-dome`, eigenes Git-Repo, Branch `main`; immer `git -C user-projects/aquaponics-dome ...`).
ROLLE: Werkstatt, Runde U3b des Pakets `docs/packages/n-unify-autobahn.md` (Empfehlung aus U3, Orchestrator 11.11.2026). Du läufst ohne Menschen im Dialog über das Agent-SDK. Fehlt eine Entscheidung, triff eine begründete Annahme (ANNAHME in `docs/decisions.md`, nächste freie D-Nummer) und mach weiter. Regel D117: so bauen wie in der Quelle; eigene Bedenken nur in `docs/packages/n-unify-bedenken.md` eintragen.

# Ziel
Die Substratbeete (Flood-and-Drain) bekommen den Aufbau aus Leons Annahme A21 als echte Geometrie, bevor U6 die Rückläufe anschließt: Abtropfgitter, Siphon durch das Gitter bis zum Boden, Vlies und Sieb darüber, Belüftung unten, seitlicher Auslass zum Rücklauf. In U2 steht das bisher nur in Daten und Blatt (`data/components/ibc_beet.json`, `docs/parts/ibc_beet.md`, D115).

# Lies zuerst
1. Paket `docs/packages/n-unify-autobahn.md` (Stand U2/U3, Offen), `docs/decisions.md` (D93 bis neueste), `docs/designprinzipien.md`.
2. Quelle: `docs/quellen/oasis-showcase-2026-11-10-nachtrag/flow-diagram.html` (A21, Flood-and-Drain, Flutstand 0,25 m, Siphon je Beet) und `data/oasis-soll.json` (Beete Außen 8, Mitte 6).
3. Bestehende Beet-Komponenten und Werkzeuge: `designs/components/ibc_beet*.sc`, `scripts/workshop/` (Beet-Skripte und `check_ibc_beet.py`), `data/components/ibc_beet.json`, `docs/parts/ibc_beet.md`, die U2/U3-Aufträge `docs/jobs/api/unify-u2-werkstatt.md` und `unify-u3-werkstatt.md` als Muster.

# Aufgaben
1. Geometrie der A21-Teile in den Beet-Komponenten bauen (alle Beet-Varianten, die im Modell vorkommen), Maße aus den Daten von U2; Siphon-Glocke und Standrohr so, dass der Flutstand 0,25 m über dem Beetboden der Quelle entspricht; seitlicher Auslass mit Anschlussstutzen für den Rücklauf (Nennweite aus `data/oasis-soll.json`, sonst Annahme).
2. `check_ibc_beet.py` um Prüfpunkte für die neue Geometrie erweitern (Flutstand, Gitterhöhe, Auslasslage, keine Durchdringung der Teile) und laufen lassen; Bilder in `renders/components/` neu erzeugen.
3. Nebenaufgabe aus U3 (Offen 2): Namenskollision zwischen `scripts/normteile_benennen.py` und `designs/components/winkelhalter.sc` bereinigen, ohne andere Komponenten zu verändern; Prüfbefehl angeben.
4. Gesamtmodell (`gen_dome.py`, `dome*.sc`, `data/params.json`) NICHT ändern; das macht die Montage.

# Regeln
- Pfad-Commits `git -C user-projects/aquaponics-dome commit -m "…" -- <pfade>`, neue Dateien vorher `add -N`; nach jedem Teilschritt committen und pushen; Commit-Nachricht endet mit `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Nichts deployen, nichts kaufen. `ANTHROPIC_API_KEY` nie ausgeben oder speichern. SolidCraft-CLI `C:\Program Files\SolidCraft\solidcraft-cli.exe`; lange Befehle im Hintergrund mit Log.

# Abschluss
Paket „Stand“ und Plan-Tabelle (Zeile U3b) mit Commits und Messwerten. Letzte Nachricht höchstens 8 Zeilen.
