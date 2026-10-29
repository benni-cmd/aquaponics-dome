# Werkstatt-Checkpoint (Rolle W, max. 8 Zeilen)
- Jetzt (29.10. ~04:00): Schritt 1 Netztopf gebaut (`designs/components/netztopf.sc`), Render ok; als naechstes Salatkopf.
- Naechster Schritt: Salatkopf (EIN Bauteil, wenige Facetten, Varianten S/M/L) -> Gauntlet -> NFT-Rinne -> NFT-Tisch x3 -> IBC-Beet -> Tank klein/gross -> Pumpe.
- Status: netztopf L3 gebaut (Gauntlet offen) · salatkopf offen · nft_rinne offen · nft_tisch offen · ibc_beet offen · tank offen · pumpe offen
- Arbeitsweise: Generator `scripts/workshop/<klasse>.py` (Parameter aus `data/components/<klasse>.json`) -> `solidcraft-cli run` -> `designs/components/<klasse>.sc`; Python: `C:\Users\benkn\AppData\Local\Programs\Python\Python312\python` (PYTHONIOENCODING=utf-8).
- Nach Abbruch: `git status`, letzter Commit, dann hier fortsetzen. Befunde: `docs/workshop-log.md`.
