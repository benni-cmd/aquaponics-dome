# Checkpoint Montage (M1.1 fertig, 29.10.2026)
## Stand
- IBC-Beete: 14 Instanzen (Beet_aussen_933 x5, aussen_993 x3, innen_933 x6) in 05_Beete per gen_dome.py `place_instances`; Erdtaschen auf echte Wannenmasse, 200 mm tiefer (Bulkhead). Build: `sh scripts/build.sh 4 22`.
- check_components: nur FAIL 07_Tanks 20 lose Koerper. check_latte 18/19: 8 Kollisionen Beet/Strebe_B und Beet/Sockel (beds 2,3,4: OBJ-Wannen ragen in Kuppelrand; Layout-Frage, nicht gefixt).
- 10_Pflanzen: alte Kugeln entfernt, bis Netztopf/Salatkopf als Instanzen kommen leer.
## Naechste Teilschritte M1
2. Tanks (4: klein 2, gross 2 inkl. tank_gross_t3?) + Pumpen als Instanzen (07_Tanks, 09_Technik). 3. NFT-Tische (24 aus Ringen, nft_tisch_*). 4. Netztopf/Salatkopf (2716). 5. Knoten/Anker (M2).
## Regeln vom Orchestrator
- Ein Schritt = ein enger Lesekontext; nach jedem Schritt Zustand sichern, NICHT leeren (System komprimiert, docs/endless-mechanics.md KORREKTUR). Render zusaetzlich mit scripts/archive_render.py ablegen (renders/history mit committen).
