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

Runde 6, Zweitkamera (`renders/round-06b-ref1.png`, Yaw 0,6 rad): Anordnung wie ref-1 links (Tanks innen, Betten-Ring, Rohr links). Abweichung: Kuppel flacher als im Bild (0,5 laut Ben statt ~0,6); Tuer liegt aus dieser Richtung hinten rechts, ref-1 zeigt sie links vorn (andere Blickrichtung). Beides nicht behoben (Ben-Mass geht vor).
| 7 | ref-5: wenige grosse Dreiecke, 5 am Scheitel, Basis-Zehneck. 3V gibt 157 Streben, 2V 63; 2V hat 10 Knoten auf Z=0 | Frequenz 3 -> 2, Basis-Zehneck-Kanten ergaenzt, keine Stauchung noetig, Sockel 0,4 m, Wasserscheibe T5_Wasser | 1-5,7,9,10,11; 12,13 teilweise |

Entscheidung Runde 7: 2V gewaehlt (Zaehlung an ref-5: ~5 Scheiteldreiecke + 10 + 10 Felder sichtbar; Bild passt zu 2V, nicht zu 3V). ref-6 von mir noch nicht angesehen, Punkt 12 stuetzt sich auf die Beschreibung der Hauptsitzung. Rohr-Strebe-Abstand nach 2V-Wechsel 252 mm (Achse zu Achse, > 195 mm noetig).
| 8 | ref-6: Reihen gestaffelt, Schlaeuche Tank-Tisch, mehr Substratwannen, dicker Tankrand | Reihenversatz 165 mm, 4 Substratwannen (126/198/234/342 Grad), 6 Schlaeuche r25, Tankwand 160 mm | 1-11; 12, 13 weitgehend |

Entscheidung Runde 8: 12 Tische nicht umgesetzt (10 Betten, Tuerplatz); keine Neigung/Rippen (nur Quader). ref-6 selbst angesehen: Reihen sind gestaffelt, Schlaeuche blau und flexibel zwischen Tischen/Tank.
