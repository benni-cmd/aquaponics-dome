# Start-Auftrag: Werkstatt check_latte nach Runde 69 (Filter nach Umbenennung, Teil-A-Treffer)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Werkstatt (nur Pruefskript und Befund). Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Befund Montage Runde 69 (`docs/loop-state.md` Abschnitt M10-S5-LUFT Teil A, `renders/check_latte-69.txt`): 669 KOLL statt 115. Davon 509 durch den Filter `scripts/check_latte.py:205/249` ("T1_Strebe" x `knoten_`), der nach der Umbenennung der Knoten-Normteile (ScheibeO_k, Schraube_k, ScheibeU_k, Mutter_k; Commit cd60551) nicht mehr greift; 45 aus Teil A (Wasserkoerper, Steckverbindungen); 115 Altbestand Leitungen.
2. Filter reparieren, sodass er die umbenannten Knoten-Koerper wieder als M2b-offen (Bohrungen fehlen) fuehrt; nichts breiter ausnehmen als vorher. Gegenprobe: Liste der 509 Zeilen vorher, nachher 0 davon als KOLL, Zahl M2b-offen entsprechend hoeher.
3. Die 45 Teil-A-Treffer einzeln bewerten: gewollter Kontakt (Rohr steckt in Muffe, Scheibe liegt im Wasserkoerper) bekommt eine eng benannte Ausnahme mit Kommentar; echte Ueberschneidung bleibt KOLL und geht als Befund an die Montage (Datei `docs/jobs/pruefung/` nicht anfassen, Befund ins Paket `docs/packages/m10-s5-luft.md`).
4. Neu laufen lassen: `python scripts/check_latte.py 69` (ca. 67 min, Hintergrund). Soll: KOLL = 115 Altbestand plus echte Teil-A-Treffer (Zahl nennen). Nicht anfassen: `gen_dome.py`, `designs/`, `scripts/components/`, `viewer/`; waehrend des Laufs aendert niemand die Bauteile.
5. Commits nur per Pfad (`scripts/check_latte.py`, `renders/check_latte-69.txt`, Paket, loop-state), Push, WIP alle 20 Minuten. Danach STOPP.
