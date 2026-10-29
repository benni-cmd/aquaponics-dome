# Integrations-Board (Besitzer: Orchestrator; Stand 29.10.2026 03:35)

Status je Bauteilklasse: `offen` · `in Arbeit` · `L2` · `L3` · `abgenommen` (Orchestrator hat Stichprobe gemacht) · `eingebaut` (Integrator hat es im Dom verknuepft).
Zustaendig: I = Integrator, W = Werkstatt. Quelle der Anzahl: `data/layout.json`.

| Klasse | Anzahl | Zustaendig | Status | Datei | Letzte Meldung |
|---|---|---|---|---|---|
| Salatkopf | ca. 2716 (D17) | W | L3 gebaut, Bauteilblatt/Kritiker offen | `designs/components/salatkopf.sc` | 03:50 Orchestrator: Bauteilblatt und Gauntlet fehlen |
| Netztopf | ca. 2716 (D17) | W | L3 gebaut, Bauteilblatt/Kritiker offen | `designs/components/netztopf.sc` | 03:50 Orchestrator: Bauteilblatt und Gauntlet fehlen |
| NFT-Rinne (3 Laengen, Phase A/B) | je Tisch 2-4 | W | abgenommen | `designs/components/nft_rinne.sc` (+6 Varianten) | 04:20 Orchestrator: Stichprobe ok (eine Lochreihe, 93/93 PASS selbst gemessen, Blatt mit Herkunft); Montage darf verknuepfen |
| NFT-Tisch innen (10), Mitte (6), aussen (8) | 24 | W | abgenommen Rev. B (W16, 18:35), W17 und W18 (Lochabstand 200, 586 Toepfe, 22:40) gebaut, nur check nachgemessen, Spec-Pruefer offen: check_nft_fit 36/36 selbst nachgemessen, Pruefer-Befunde eingearbeitet, Blatt; Montage darf Rev. B einsetzen (Rinnen-Pflanzen 466 aus data/components/nft_tisch.json, D20) | `designs/components/nft_tisch_{innen,mitte,aussen}.sc` | 07:35 Orchestrator: Render innen ok (2 Rinnen versetzt, 2 Boecke mit Diagonalen, Verteiler, Sammelrohr), Blatt nach Spec-Pruefer, Triage im Log; Montage darf verknuepfen; offen laut Log: Winkelhalter (L4), Schlaeuche weich = Montage |
| IBC-Beet aussen (8), innen (6) | 14 | W | abgenommen | `designs/components/ibc_beet_*.sc` | 07:35 Werkstatt: Vorpruefung 66/66, Blatt, Kontextpaket (Commit 09e3406); Orchestrator: Stichprobe steht aus |
| Tank klein (Vortex) | 2 | W | abgenommen (08:25, check_tank 60/60, Schnitt ok) | `designs/components/tank_klein.sc` | - |
| Tank gross (Biofilter) | 2 | W | abgenommen (08:25, check_tank 60/60) | `designs/components/tank_gross.sc` | - |
| Pumpe (4 Tafeln; Kassetten = Tank-Stuetzrippen, D16) | 4 | W | L3 gebaut (check_pumpe 37/37), Spec-Pruefer laeuft | `designs/components/pumpe.sc` | - |
| Strebe A / B | 30 / 35 | I | in Arbeit | `designs/components/strebe_*.sc` | - |
| Knoten 4/5/6-wertig (Kugel mit Steckarmen, D15) | 10 / 6 / 10 | W | gebaut (26 Dateien, 135/135), Spec-Pruefer laeuft | `designs/components/knoten_*.sc` | - |
| Tuer komplett | 1 | I | offen | `designs/components/tuer_komplett.sc` | - |
| Fundamentanker (Werkstatt), Fundamentring, Erdflaeche | 10 / 1 / 1 | W/I | Anker gebaut (15/15), Blatt/Pruefer folgen | | - |
| Pool, zweites Becken | 2 | I | in Arbeit | | - |
| Haut | siehe Gitter | I | offen | | - |
| Rohrnetz (aus `system.json`) | - | I (nach W) | offen | | - |
