# Start-Auftrag: Werkstatt N-MODELL-KOMPLETT Schritt 2 (Strebe Vierkant 30x30x3)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Werkstatt. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Grundlage: `docs/jobs/N-MODELL-KOMPLETT.md` Schritt 2 und Pruefpunkt 1, Falle Rollwinkel und Falle `strut_r` im Start-Hinweis. Entschieden: Wand 3 mm, Profil austauschbar per Parameter (N-STATIK darf aendern).
2. Bauen: `scripts/components/strebe.py` baut ein hohles Vierkantrohr (Parameter `strut_profile` 30, `strut_wall` 3 in `data/params.json`, `strut_r` NICHT loeschen), Koerper benannt, Werkstoff Katalogname Stahl verzinkt; Bauteilblatt und `data/parts/strebe_a.json`, `strebe_b.json` nachziehen; Passung Steckarm 23x23 im Innenmass 24 per CAD-Probe, Interferenz 0.
3. Parallel laeuft `check_latte 69` (liest `designs/components/*.sc`): bis der Orchestrator "check_latte fertig" meldet, die neuen `.sc` nur in einer Scratchpad-Kopie erzeugen und messen; `scripts/components/strebe.py`, `data/params.json`, Blatt und Teiledaten duerfen committet werden. Danach `strebe_a.sc`/`strebe_b.sc` im Repo schreiben und committen. Kein `gen_dome.py`, kein `build.sh`, kein `viewer/` (Einbau macht die Montage).
4. Messen: `solidcraft-cli.exe eval` je Strebe: 1 Koerper, bbox 30 x 30 x 3039 bzw. 3468, Masse 7,73 bzw. 8,82 kg (+-1 %), hohl, Material nicht Default; `check_parts.py strebe_a strebe_b` Exit 0. Paket `docs/packages/n-modell-komplett.md` nachfuehren. Commits nur per Pfad, Push, WIP alle 20 Minuten. Danach STOPP.
