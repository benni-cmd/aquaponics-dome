# N-VERBINDER: Scherenknoten mit Lochplatte (W74)

**Problem:** Das Modell verbindet die 65 Streben mit Kugelknoten D100, Steckarm 23 x 23 und Querbolzen. Das echte Verbindungsstueck aus Chemnitz (Foto `reference/chemnitz/laschenknoten-foto.jpg`) ist ein Scherenknoten mit Lochplatte. R41 hat die Schere nicht erkannt.
**Intent:** Ben soll den echten Verbinder verstehen und pruefen koennen, bevor 26 Knoten und 130 Strebenenden umgebaut werden.
**Goal:** Der Bericht `docs/research/R56-scherenknoten.md` und der Prototyp `designs/components/knoten_schere_proto.sc` (eine Lochplatte und eine Schere im Rohrstueck, Nasen ausgefahren) liegen mit Skript, Render und Bauteilblatt gepusht vor. Das Gesamtmodell bleibt unveraendert.

## Plan
1. Quellen lesen: R41, R34, `docs/parts/knoten.md`, `docs/parts/strebe.md`, Foto mit vergroesserten Ausschnitten.
2. Rechnung `scripts/r56_scherenknoten.py` mit Selbsttest: Neigung, Rohrlaenge, Profile rund und vierkant, Einziehen der Nasen, Kraftweg, Masse.
3. Bericht R56: Funktion, Teile, Rund gegen Vierkant, Statik grob, Kauf- und Laserteile in Europa, Fragen an Ben.
4. Prototyp `scripts/components/knoten_schere_proto.py` -> `.sc`, Check, Render `renders/components/knoten_schere_proto/`, Bauteilblatt `docs/parts/knoten_schere_proto.md`.
5. Pfad-Commits und Push. KEIN Einbau ins Gesamtmodell und keine Serie bis Ben den Prototyp abnimmt.

## Dateien (keine Ueberschneidung mit parallelen Sitzungen)
`docs/research/R56-scherenknoten.md`, `scripts/r56_scherenknoten.py`, `scripts/components/knoten_schere_proto.py`, `designs/components/knoten_schere_proto.sc`, `renders/components/knoten_schere_proto/`, `docs/parts/knoten_schere_proto.md`, dieses Blatt, Wunschbuch-Zeile W74.

## Stand
05.11.2026: Plan angelegt. Rechnung Selbsttest 6/6. R56 geschrieben. Prototyp gebaut, Check 6/6, 5 Renders angesehen, Bauteilblatt `docs/parts/knoten_schere_proto.md`. Wartet auf Bens Abnahme (R56 Abschnitt 6, fuenf Fragen). Gesamtmodell unveraendert.

## DoD
- R56 enthaelt alle sechs Abschnitte des Auftrags mit [A]/[E]/[Q]-Kennzeichnung.
- Prototyp: Check-Skript besteht (Koerper geschlossen, Nasen ragen durch die Wand, keine Durchdringung Lasche/Rohr ausser in den Wandloechern).
- Render optisch geprueft (Bild angesehen).
- Gepusht; Gesamtmodell unveraendert (`git diff --stat` ohne `gen_dome.py`, `dome.sc`).
