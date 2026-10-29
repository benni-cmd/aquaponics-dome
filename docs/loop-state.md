# Checkpoint Montage (M1 Start, 29.10.2026, Sitzung neu gestartet)
## Stand
- Docs gelesen. dome.sc (Stand 04:45): Layout, 64 Streben, Fundamentring, Erdflaeche, Pools, Schrank, Zulaufrohr, Tuer. check_components: 4 PASS, 1 FAIL (lose Koerper 05_Beete 14, 07_Tanks 20, 10_Pflanzen 240).
- Board: abgenommen NFT-Rinne, NFT-Tisch, IBC-Beet, Tank klein/gross; L3: Knoten, Anker, Pumpe, Salatkopf, Netztopf.
## Plan M1 in Teilschritten (je Commit+Push)
1. IBC-Beete (14 Instanzen, Varianten aussen_933/aussen_993/innen_933; Ursprung = Mitte Wannenunterseite, z = sock_z + z0, yaw = yaw + ROT) in gen_dome.py t9.
2. Tanks (4) + Pumpen, 3. NFT-Tische (24, aus Ringen), 4. Netztopf/Salatkopf (2716), 5. Knoten/Anker.
## Regel vom Orchestrator
- Kontext messen nach grossem Schritt; ab 50 % Zustand sichern, dann clear_session("self") als letzte Aktion.
