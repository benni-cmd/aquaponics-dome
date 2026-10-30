# W22 Haut nacharbeiten (Befunde aus W21, Entscheidung D37)
Ziel: Paneel liegt auf der Kappe auf (15 mm je Seite), Kappenzahl und alte Tuerlage in der Doku stimmen.
Eingaben: `docs/decisions.md` D37; `docs/workshop-log.md` (W21-Triage); `scripts/workshop/haut_paneel.py`, `check_haut.py`, `check_tuer.py`; `data/components/haut_paneel.json`, `haut_profil.json`.
Schritte:
1. `edge_inset` 15 -> 0 (Paneel bis Strebenachse, Kappe klemmt beide Kanten, Auflage 15 mm je Seite). check_haut und check_tuer muessen gruen bleiben (Tuerausschnitt, Kappenabstand, Interferenz 0); Blaetter und Herkunft (R11 widerspricht sich: Eintrag im Blatt) nachziehen.
2. Kappenzahl: 66 (64 ganze + 2 Reststuecke am Tuerfeld, je 1316 mm) als Zahl im Blatt `haut_profil` festhalten; Strebenzahl im Dom NICHT aendern (Montage).
3. Alte Tuerlage (Azimut 167, zwei Felder, Spitze 3150) in der Doku auf D36 korrigieren: `docs/components.md` (Z. 4, 25), `docs/model-description.md` (Z. 35), `docs/next-steps-workshop.md` (Z. 43). `docs/loop-log.md` nur Hinweis anhaengen, nicht umschreiben. NICHT anfassen: `designs/components/tuer.sc` (Montage ersetzt es durch tuer_komplett).
4. Offene Frage T40/T50 (Tuerausschnitt gehoert dem Paneel) im Blatt als Entscheidung D37 eintragen: Ausschnitt bleibt beim Paneel.
Ergebnis: check_haut/check_tuer gruen, Doku korrigiert, WIP-Commit je Schritt, Push, Zeile in `docs/workshop-state.md`.
Kein Pruefer-Lauf noetig (nur Parameter); Spezial: ein Render Paneel+Kappe im Schnitt per archive_render.py.
Danach: W23.
