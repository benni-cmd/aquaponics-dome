# W18 Lochabstand NFT-Rinnen verringern (Ben 29.10. 22:00, D32, R16)
Ziel: mehr Topfloecher je Rinne: `pitch` von 250 auf 200 mm, als Parameter weiter einstellbar (150..250), Zickzack (pitch/2) bleibt.
Eingaben: `docs/research/R16.md`, `docs/parts/nft_rinne.md` (Parameter pitch, n_holes, shift), `data/components/nft_rinne.json`, `scripts/workshop/nft_rinne.py`, `nft_tisch.py`, `check_nft_fit.py`.
Ergebnis: Rinnenvarianten neu mit `pitch` 200 (n_holes = floor(Laenge/pitch), Randabstand >= 64), Tische neu eingebaut, `check_nft_fit` Gesamtzahl Topfloecher gegen Mindestzahl 459 (Soll jetzt ca. 580), Blatt-Nachtrag mit Herkunft (Q: Iowa State 203 mm, HortTechnology 150 mm; A fuer 200), ein Bild (Draufsicht Rinne mit Toepfen).
Pruefung: check_nft_rinne, check_nft_tisch, check_nft_fit PASS; Netztoepfe kollidieren nicht (Kragen 64 gegen Nachbarloch, Zickzack); Pflanzenzahl in `data/components/nft_tisch.json` aktualisieren, D20 (466/462) durch neue Zahl ersetzen.
Folge fuer die Montage: Rinnen-Pflanzen kommen aus `data/components/nft_tisch.json` (D20); nach W18 neue Zahl.
Reihenfolge: nach W17-Spec-Pruefer, vor Haut-Paneel. Nicht anfassen: dome.sc.
