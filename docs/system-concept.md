# Systemkonzept: passt die Rechnung zusammen? (30.10.2026, Ben: "rechnerisch muss alles zusammenpassen")
Rechnung: `python scripts/system_specs.py` -> `data/system-specs.json` (Viewer zeigt sie, wenn nichts ausgewaehlt ist). Herkunft je Zahl: Q Quelle (Bens Tabelle R15, `docs/hydraulics.md`), E eigene Rechnung aus Modellmassen, A Annahme. Keine fachliche Freigabe.

## Ergebnis auf einen Blick
- **Wasser** ca. 34 m³ (Pool 26,2 · zweites Becken 2,4 · Tanks 1,9 · Beete 3,3 · NFT 0,1 · Rohre 0,2). Bens Tabelle nennt 25 m³ Systemwasser, die Zisterne (5 m³) liegt ausserhalb des Modells.
- **Pflanzen** 2746 Toepfe (2160 Beete + 586 NFT) gegen mindestens 609 laut Tabelle: erfuellt.
- **Futter** 10,7 kg/Tag (Tabelle: 321 kg/Monat) bei 1839 Tilapia a 0,7 kg = 1287 kg, 45 kg/m³ Beckenwasser, Ammonium-Anfall ca. 345 g/Tag [A Faustregel 35 % Protein x 9,2 %].
- **Hauptkreislauf** Bedarf 143 l/min (NFT 68 Rinnen x 0,5 l/min = 34, Beete bei 2 Flutzyklen je Stunde ca. 109) = 8,6 m³/h, je Linie 72 l/min bei 2,0 m Foerderhoehe: hydraulisch 23 W, elektrisch ca. 67 W je Pumpe (Wirkungsgrad 35 % [A]). Umwaelzung des Gesamtwassers alle ca. 4 h.
- **Strom** ca. 351 W (Pumpen 2 x 67, Belueftung ca. 177 W aus 4,3 kg O2/Tag bei 1 kg O2/kWh [A], Steuerung 40 W) = 8,4 kWh/Tag = ca. 253 kWh/Monat, ohne Heizung. Bens Tabelle rechnet 219 EUR/Monat Strom, das ist deutlich mehr (Heizung nicht modelliert).
- **Filter** Absetzer klein 267 l, Verweilzeit 22 min bei 12 l/min (Auslegung 30 min); Biofilter gross 702 l mit 0,26 m³ Medium je Tank: 0,52 m³ Medium decken ca. 1 kg Futter/Tag (0,5 l Medium je g, Bioballs); die 8,2 m³ Substrat decken ca. 8,2 kg/Tag (1 l je g, Kies). Zusammen 9,2 von 10,7 kg/Tag (86 %).

## Was nicht zusammenpasst (offene Konzeptentscheidungen, nicht erfunden, fuer Ben)
1. **Pumpen:** Die Modellpumpen (12 und 30 l/min) sind die Verweilzeit-Auslegung der Tanks, nicht der Hauptkreislauf. Der Kreislauf braucht ca. 72 l/min je Linie. Entweder Hauptpumpen 72 l/min und der Vortex-Absetzer als Teilstrom (12 l/min je Linie behandelt nur etwa 8 % des Wassers je Stunde) oder der Absetzer im Hauptstrom (dann waere das Tankvolumen mit 267 l zu klein fuer 30 min).
2. **Pflanzflaeche gegen Futter:** 80 m² Pflanzflaeche (Substrat 38 + NFT 42) tragen bei 40-50 g/m²/Tag nur 3,2-4,0 kg Futter, die Tabelle plant 10,7 kg. Entweder ca. 700 Fische (38 %) oder mehr Flaeche oder mehr Fruchtgemuese (50-80 g/m²).
3. **Pool 26 m³:** Bei Tiefe 2,2 m (D26) ist `docs/hydraulics.md` 2.4 ("Pool ca. 6 m³") veraltet.
4. **Besatzdichte** 45 kg/m³ liegt unter dem Tabellenbereich 60-150: eher locker besetzt, unkritisch.

## Naechste Schritte
Ben entscheidet 1 und 2; danach `data/system.json` und `scripts/check_hydraulics.py` auf diese Zahlen stellen (M4). Pumpen- und Filterbeschreibungen im Viewer zeigen die gerechneten Werte.
