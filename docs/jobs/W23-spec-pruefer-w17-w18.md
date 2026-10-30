# W23 Ein gemeinsamer Spec-Pruefer fuer W17 und W18 (NFT-Tische)
Ziel: Die offenen Pruefungen der NFT-Tische (Radialbudget D28, Lochabstand 200 D32/D33) in EINEM Lauf nachholen.
Eingaben: `docs/jobs/W17-radialbudget.md`, `W18-lochabstand.md`; Blaetter nft_tisch/nft_rinne; `scripts/workshop/check_nft_fit.py` (40/40); D18, D28, D29, D32-D34.
Vorgehen: ein frischer Unter-Agent (general-purpose, sonnet) prueft Blaetter gegen Zahlen und Modell (Topfzahl 586, Footprint >= 95 mm, Tischbreiten, Rinnenzahl 68, Hoehe 1,3 m, Laufweg-Budget); du triagierst im `docs/workshop-log.md` und behebst nur echte Befunde in Werkstatt-Dateien.
Nicht anfassen: dome.sc, Layout/Platzierung (Montage).
Ergebnis: Befundliste + Triage, Blaetter korrigiert, WIP-Commit, Push, Fertigmeldung.
Danach: Pumpen-Blatt (W24) nach Rueckmeldung des Orchestrators (Fachrecherche-Integration).
