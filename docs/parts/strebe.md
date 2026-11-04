# Bauteilblatt: Kuppelstrebe A und B (T1)

Generator: `scripts/components/strebe.py` -> `designs/components/strebe_a.sc`, `strebe_b.sc`. Teiledaten: `data/parts/strebe_a.json`, `strebe_b.json`.

## Form
- Hohles Vierkantrohr `strut_profile` x `strut_profile` x `strut_wall` = 30 x 30 x 3 mm (Parameter in `data/params.json`, Herkunft [A] Knotenblatt `data/components/knoten.json`; Wand 3 mm entschieden 05.11.2026 bis N-STATIK).
- Laenge = Knoten-Knoten-Abstand minus 2 x `strut_end_offset` (120): A 3279 - 240 = 3039 mm (30 Stueck), B 3708 - 240 = 3468 mm (34 Stueck).
- Ursprung Strebenanfang, Achse +Z, Rohrflaechen parallel zu X und Y. Die Drehlage im Gesamtmodell setzt die Montage (`gen_dome.py` `place_struts`, N-MODELL-KOMPLETT Schritt 3) aus `data/components/knoten_arme.json`.
- Ein Koerper je Datei (`T1_Strebe_A`, `T1_Strebe_B`), Werkstoff `Stahl verzinkt` (Katalog `stahl_verzinkt`, 7,85 g/cm3).
- Keine eigene Aufnahme: der Steckarm 23 x 23 steckt 80 mm im durchgehenden Innenmass 24 x 24 (0,5 mm Luft je Seite). `strut_pocket` (runde Aufnahme D34 des Rundstabs) ist nicht mehr benutzt.

## Profil aendern (N-STATIK)
Nur `strut_profile` und `strut_wall` in `data/params.json` aendern, dann `python -X utf8 scripts/components/strebe.py`. Achtung: der Knoten-Steckarm (`data/components/knoten.json`, 23,0) muss zum neuen Innenmass passen (Innenmass - 1,0).

## Messwerte 05.11.2026
Befehl: `solidcraft-cli.exe eval <strebe_x.sc> --json-out <datei>`

| | bbox mm | Volumen mm3 | Masse kg | closed | Material |
|---|---|---|---|---|---|
| A | 30 x 30 x 3039 | 984 636 | 7,729 | wahr | Stahl verzinkt |
| B | 30 x 30 x 3468 | 1 123 632 | 8,821 | wahr | Stahl verzinkt |

Soll laut Blatt: 7,73 / 8,82 kg (+-1 %), Querschnitt 324 mm2. Passung: CAD-Probe Steckarm 23 x 23 x 3, 80 mm tief an beiden Enden, `inspect.interference`: 0 Interferenzen (2 Paare geprueft); Gegenprobe Steckarm 25 x 25: 2 Interferenzen je 3920 mm3. `check_parts.py strebe_a strebe_b`: 22/22 je Teil, Exit 0.

## Folgen fuer die Montage (Schritt 3)
- `strut_r` (45) bleibt in `data/params.json`: `gen_dome.py:250`, `check_latte.py:75`, `place_m8.py:11` und `check_huelle.py:144` rechnen damit (Basisringhoehe, Folienabstand). Die Montage entkoppelt das.
- Rohr-Aussenkante liegt 15 statt 45 mm von der Achse: der Folienabstand in `check_huelle.py` (45 + 3 + 15 < 64) wird groesser, nicht kleiner.
