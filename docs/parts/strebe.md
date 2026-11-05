# Bauteilblatt: Kuppelstrebe A und B (T1)

Generator: `scripts/components/strebe.py` -> `designs/components/strebe_a.sc`, `strebe_b.sc`. Teiledaten: `data/parts/strebe_a.json`, `strebe_b.json`.

## Form (D91, 05.11.2026)
- Rundrohr `strut_d` x `strut_wall` = 42,4 x 2,6 mm, EN 10255 verzinkt (Parameter in `data/params.json`; muss gleich `tube_d`/`tube_t` des Scherenknotens `data/components/knoten_schere.json` sein, sonst bricht das Skript ab). Vorher Vierkant 30 x 30 x 3 (Kugelknoten mit Steckarm).
- Laenge = Rohrmund bis Rohrmund der zwei Scheren, gemessen in der Montage-Lage (`scripts/knoten_montage.py` `rohrlaengen`): Mitte der Spanne je Typ.
  - A: Spanne 3075,5 bis 3078,7 mm, gebaut 3077,1 mm (30 Stueck). Die Spanne kommt von der einheitlichen 6-Loch-Platte (D91): an den 5-wertigen Knoten dreht jeder Arm bis 24 Grad um seine Plattenschraube, der Rohrmund wandert bis 15 mm. Alle A-Streben beruehren einen 5-wertigen Knoten.
  - B: 3503,8 mm (34 Stueck), Spanne 0,0 mm.
  - Nennmass ohne Plattendrehung (Werkstatt `knoten_schere.json` `geometrie.rohr_mm`): A 3075,3 / B 3503,5.
- Je Ende zwei Gegenloecher D15 (`wall_hole`), 46 mm hinter dem Rohrmund (`b_pivot_to_nose` 58 - `pivot_out` 12), je auf der Mittelebene einer Lasche (x = -/+ 4 mm bei `link_t` 8).
- Rahmen: Ursprung Rohrmund am Anfang, Achse +Z, X = Kuppel aussen (Laschennormale), Y = Nasenrichtung. Anfang: Lasche 1 nach +Y, Lasche 2 nach -Y; Ende umgekehrt.
- Ein Koerper je Datei (`T1_Strebe_A`, `T1_Strebe_B`), Werkstoff `Stahl verzinkt` (7,85 g/cm3).

## Einbau (Montage)
`gen_dome.py` `place_struts` setzt jede Strebe mittig zwischen die Rohrmuender ihrer zwei Scherenarme (`scripts/knoten_montage.py`). Spalt Rohrende zu Rohrmund je Ende: A hoechstens 0,8 mm, B 0,0 mm. Die Nase (10 x 8 mm, Diagonale 12,8) passt mit 1,1 mm Spiel in D15; Pruefung `python -X utf8 scripts/check_verbinder_montage.py`.

## Profil aendern (N-STATIK)
`strut_d`/`strut_wall` in `data/params.json` UND `tube_d`/`tube_t` in `data/components/knoten_schere.json` gleich aendern, dann `python -X utf8 scripts/workshop/knoten_schere.py` und `python -X utf8 scripts/components/strebe.py` (liest `scripts/.segs.json` aus dem letzten `gen_dome.py`-Lauf).

## Messwerte 05.11.2026
Befehl: `solidcraft-cli.exe eval designs/components/strebe_<x>.sc`

| | bbox mm | Volumen mm3 | Masse kg | closed | Material |
|---|---|---|---|---|---|
| A | 42,4 x 42,4 x 3077,1 | 998 041 | 7,835 | wahr | Stahl verzinkt |
| B | 42,4 x 42,4 x 3503,8 | 1 136 694 | 8,923 | wahr | Stahl verzinkt |

`python -X utf8 scripts/workshop/check_parts.py strebe_a strebe_b`: 22/22 je Teil.

## Offen
- Katalog-Artikel: `data/katalog.json` fuehrt noch `PRF-st-strebe30x30`; Rundrohr 42,4 x 2,6 (Haendler in R56 Abschnitt 5) traegt die Stuecklisten-Kette nach.
- Bekommen die 5-wertigen Knoten eine 5-Loch-Platte (Werkstatt-Befund N-VERBINDER), entfaellt die A-Spanne: alle A 3075,3 mm.
