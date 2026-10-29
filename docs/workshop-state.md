# Werkstatt-Checkpoint (Rolle W, max. 8 Zeilen)
- Jetzt (29.10. ~04:25): NFT-Rinne gebaut (`nft_rinne.sc`, Profil + 2 Endkappen, 3 Laengen ueber Parameter len_l/n_holes); Kritiker Salatkopf laeuft (1 Agent zur Zeit).
- Naechster Schritt: NFT-Tisch (frame.member fuer Beine/Querstreben, Fussplatten, Rinnen geneigt 0,573 Grad) -> Gauntlet Rinne -> IBC-Beet -> Tank klein/gross -> Pumpe.
- Status: netztopf L3 (Gauntlet offen) · salatkopf L2/L3 (Kritiker Runde 1 laeuft) · nft_rinne L3 gebaut (Gauntlet offen) · nft_tisch offen · ibc_beet offen · tank offen · pumpe offen
- Arbeitsweise: Generator `scripts/workshop/<klasse>.py` (Parameter aus `data/components/<klasse>.json`) -> `solidcraft-cli run` -> `designs/components/<klasse>.sc`; Python: `C:\Users\benkn\AppData\Local\Programs\Python\Python312\python` (PYTHONIOENCODING=utf-8). Neue Dateien vor Commit mit `git add -N`.
- Nach Abbruch: `git status`, letzter Commit, dann hier fortsetzen. Befunde: `docs/workshop-log.md`.
