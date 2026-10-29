# Verfeinerungsschleife

| Runde | Abweichungen (Zahlen) | Fixes | Latte erfuellt |
|---|---|---|---|
| 1 | Tuer massiv (Volumen 108 Mio mm3 statt Rahmen) | Innenrechteck von y=30 -> Rahmen | 1,2,5 |
| 2 | Mitteltank von Fasstank verdeckt | T6 (300,-1550), Fass-Tanks auf Ring r<=2100 | 1,2,3,5 |
| 3 | Fasstanks r~2000-2300 kollidieren mit Betten (innen 2150); Rohr schneidet Strebe 145 (Abstand 16 mm) | Betten r=2850, T5 D2400, T6 D1200, Rohr von links | 1-5 |
| 4 | Rohr kollidierte mit Fasstank 1 | Fasstank 1 -> (-1900,200); Rohr A=(-4078,429,2200) | 1-5 |

Entscheidungen: Streben als getrennte Koerper T1_Strebe_nnn (kein Boolean, schneller, 157 Stueck); 8 Streben im Tuerbereich entfallen; Skript statt Einzelaufrufe (CLI `run`, gleiche Engine). Hoehe 4,2 m statt 3,5 m (5/8-Kuppel, an Referenz kalibriert).
