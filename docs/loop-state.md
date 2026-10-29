# Loop-Checkpoint (aquaponics-dome)

- **Aktueller Schritt:** Runde 9 fertig (Hoehe/Breite per Zahlen 0,50 belegt; Tischring dichter, r=4,5 m).
- **Naechster Schritt:** optional Rundung/Rippen/Neigung; Farben; Haut T2 (Phase 2). Limit 5h ~90 %.
- **Latte:** 1-11 erfuellt; 12, 13 weitgehend (siehe Paket)
- **Offene Fehler:** keine bekannten.
- **Bauweise:** `scripts/build.sh <stufe> <runde>` erzeugt `designs/dome.sc` + `renders/round-NN.png` (Skript `scripts/gen_dome.py`, Parameter-Tabelle `P`).

## Checkpoint vor dem naechsten Schritt (Limit ~90 %)
- **Jetzt kommt:** Schlussschritt ComfyUI: `renders/round-09.png` -> `renders/photoreal-01.png` (denoise 0.45), dann 2-3 Varianten. Entscheidung: Latte 12/13 gelten mit dokumentierten Abweichungen (Neigung, Rippen, Rand-Rundung, Farben, 12 Tische) als abgenommen; nach dem Schritt ComfyUI beenden.
- **Nach Abbruch:** `git status`, letzten Commit pruefen; ComfyUI-Prozess pruefen/beenden; fehlende photoreal-Dateien erneut erzeugen.

## Checkpoint (Limit ~91 %): Loop v2
- Photoreal-Versuch 1 (`renders/photoreal-01.png`, denoise 0,45) ist schwach (img2img verformt Details); ComfyUI beendet. Schlussschritt wird nach Loop v2 wiederholt.
- **Jetzt kommt:** Loop v2 Schritt 1: `scripts/check_latte.py` (messbare Latte, `renders/score.json`). Dann Kameras cam_ref4/5/1, `scripts/compare.py`, Rundenablauf v2.
- **Loop v2 Schritt 1 fertig:** `scripts/check_latte.py` laeuft (Score Runde 9: 22/23 = 96 %, FAIL: 32 Kollisionen). **Jetzt kommt:** Kollisionen auflisten und die groesste beheben; dann cam_ref4/5/1 + `compare.py`.
