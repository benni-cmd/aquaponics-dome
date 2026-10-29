# Loop-Checkpoint (aquaponics-dome)

- **Aktueller Schritt:** Runde 4 gebaut (alle T1-T11 vorhanden), Rohr T10 neu gelegt (Abstand >=340 mm zu allen Streben).
- **Naechster Schritt:** Runde 4 Screenshot pruefen; Tuer-Strebenstumpf entfernen; Bett 09 vor der Tuer klaeren; dann `designs/dome.step` exportieren, Paket nachfuehren.
- **Latte:** 1 erfuellt (5 Streben am Scheitel, 3V) · 2 erfuellt · 3 erfuellt · 4 erfuellt (10 Segmente, 2x4 Loecher) · 5 erfuellt (Verhaeltnis ~0,82 vs. Ref ~0,85, innerhalb 10 %) · 6 offen (Bett 09 steht vor der Tuer; Rohr-Strebe-Pruefung bestanden)
- **Offene Fehler:** Strebenstumpf neben Tuer; Bett 09 blockiert Tuerzugang.
- **Bauweise:** `scripts/build.sh <stufe> <runde>` erzeugt `designs/dome.sc` + `renders/round-NN.png` (Skript `scripts/gen_dome.py`, Parameter-Tabelle `P`).
