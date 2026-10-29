# Verfeinerungsschleife

| Runde | Abweichungen (Zahlen) | Fixes | Latte erfuellt |
|---|---|---|---|
| 1 | Tuer massiv (Volumen 108 Mio mm3 statt Rahmen) | Innenrechteck von y=30 -> Rahmen | 1,2,5 |
| 2 | Mitteltank von Fasstank verdeckt | T6 (300,-1550), Fass-Tanks auf Ring r<=2100 | 1,2,3,5 |
| 3 | Fasstanks r~2000-2300 kollidieren mit Betten (innen 2150); Rohr schneidet Strebe 145 (Abstand 16 mm) | Betten r=2850, T5 D2400, T6 D1200, Rohr von links | 1-5 |
| 4 | Rohr kollidierte mit Fasstank 1 | Fasstank 1 -> (-1900,200); Rohr A=(-4078,429,2200) | 1-5 |

Entscheidungen: Streben als getrennte Koerper T1_Strebe_nnn (kein Boolean, schneller, 157 Stueck); 8 Streben im Tuerbereich entfallen; Skript statt Einzelaufrufe (CLI `run`, gleiche Engine). Hoehe 4,2 m statt 3,5 m (5/8-Kuppel, an Referenz kalibriert).
| 5 | Bett 09 versperrt Tuer (Tuer ±450 mm, Bett ±750 mm); Strebenstumpf neben Tuer | Tuer 550 mm tangential verschoben (door_off), Bett 09 auf 700 mm gekuerzt und 400 mm von der Tuer weg; Stumpf entfaellt mit der Tuerverschiebung | 1-6 |

Abbruch nach Runde 5: alle sechs Latte-Punkte erfuellt. Einschraenkung Punkt 6: Durchdringungen nur per Rohr-Strebe-Abstand und Geometrierechnung geprueft, nicht per Boolean-Test aller Paare.
| 6 | Ben: Basis 12 m, Hoehe 6 m (Quelle 1); Normtuer 1,0x2,0 m (Quelle 2); Menschenmasse (Quelle 3) | P komplett neu; Kuppel in Z gestaucht (Verhaeltnis 0,503); Tanks/Betten/Rohr/Schrank neu; Rohr per Abstandssuche (>=520 mm zu Streben) von links; Bett 09 1,2 m, Tuer +1,1 m versetzt | 1-9 (8 mit Einschraenkung) |

Entscheidungen Runde 6: 3V beibehalten (Strebenlaenge ~2,3 m, Bildanmutung passt); Stabradius 45 mm; Rangfolge der Massquellen im Paket. Zwei-Kamera-Vergleich (ref-1 links) noch offen.
