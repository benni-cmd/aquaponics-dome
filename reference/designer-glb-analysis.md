# Designer-Modell WorldEdenEraGreenhouseOnly (Philip, 20.03.2026): Maße und Verhältnisse

Quelle: `WorldEdenEra/GreenhouseOnlyExports/GLTF_003/WorldEdenEraGreenhouseOnly.glb` (285 MB, bleibt in Bens Downloads, nicht im Repo; `.blend` ist ohne Blender nicht lesbar, das GLB ist der gleiche Inhalt). Auswertung: `python scripts/glb_groups.py <glb> 0` (reines Python, liest Knotenbaum, Weltmatrizen, Accessor-Bounds). Einheit Meter, Y oben, Mittelpunkt Becken bei (0, 0). **Ben: optisch, technisch nicht korrekt, Wasserwege falsch** — nur für Maße und Verhältnisse. Maße sind Bounding-Boxen der Meshes (Wanddicken, Kippung nicht abgezogen).

| Bauteil | Designer-Modell | Unser Modell (Stand) | Bemerkung |
|---|---|---|---|
| Dach (GH_Roof) | 12,84 × 6,28 hoch × 12,75 | R 6000 (12 m), Höhe 6 m | gleiche Größenklasse, Dach inkl. Streben/Überstand |
| Fundament | 12,86 × 12,82, Höhe 0,63; Außenkante um Tür herum Zusatzplatte 0,93 × 1,35 | Fundamentring | Zusatzplatte = Türschwelle/Stufe |
| Hauptbecken (GHWaterPot) | Ø 4,06, Höhe 1,39 (Mitte 0,0) | Ø 3,89 (OBJ), Tiefe 2,2 (D26), zentriert (D35) | Designer 4 % größer, flacher dargestellt (oberirdischer Teil) |
| Kleine Töpfe/Tanks | Ø 1,88 × 1,27 bei (2,98, -0,40); Ø 1,03 × 1,13 bei (4,47, -0,61) | Tanks klein Ø 0,67 / groß Ø 0,93, Zweitbecken Ø 1,75 | Designer-Töpfe passen etwa zu Zweitbecken (1,75) und Tank-Gruppe |
| NFT lang | 8 Tische, Standhöhe 1,44, Rinnenebene Y 1,41, Länge je Tisch 2,1–3,7 (Bars) | Außenring 8 Tische, Rinnenhöhe Z 1300 | Anzahl und Höhe stimmen überein |
| NFT kurz | 6 Tische, Standhöhe 1,11, Rinnenebene Y 1,26 | Mittelring 6 Tische (Rinnenhöhe 1300) | Designer: Mittelring ca. 15 cm niedriger als Außenring |
| Innenring NFT | nicht vorhanden (nur 14 Tische) | 10 Innentische (Rinnenhöhe 840) | unser Innenring ist Zusatz aus OBJ/Bens Tabelle |
| NFT-Rinnen (Plane029) | 192 Teile lang (24 je Tisch), 120 kurz (20 je Tisch) | 68 Rinnen, 586 Töpfe | Designer-Zählung ist Gestaltung, Rinnenbild nicht übertragbar |
| Tür | 1,00 breit × 2,04 hoch, 0,52 tief, Mitte (6,04, -1,48) → Azimut 346° (Abstand 6,2 m) | Tür 1000 × 2000, Feld BBB bei 149,2° (D36) | OBJ-Tür lag bei 167°, das ist gegenüber 346,2° um 180° gedreht: gleiche Lage, Y-Spiegelung |
| Pflanzen | Kartoffel 69, Tomate 52, Erbse 32, Zwiebel 44, Karotte 22 (Einzelpflanzen-Modelle) | 2746 Töpfe, Artenmodelle zuletzt (D27) | Artenverhältnis des Designers als Orientierung für den Pflanzmix |
| Beete (GHPondsWater/BucketStand) | 6,8 × 6,7 Fläche, Höhe 0,5–0,9 | 14 IBC-Beete | Designer zeigt Flächen als Gruppen, keine Einzelbeete |
| Fische | 12 große + 6 kleine, Größe 0,2–0,55 m | 679 Fische (Auslegung D40) | nur Optik |

## Was daraus folgt (Vorschlag, nicht entschieden)
1. Die Tür liegt im Designer-Modell im selben Bereich wie im OBJ (167° gegenüber 346°, also 180° gedreht): bestätigt, dass die Tür nahe einem Basisknoten steht; D36 (mittig im Feld BBB 149,2) bleibt eine bewusste Abweichung zugunsten der Türbreite.
2. Mittelring niedriger als Außenring (Designer 1,26 gegen 1,41 m Rinnenebene): kann als Ergonomiepunkt geprüft werden; bei uns beide 1300 (Werkstatt).
3. Beckendurchmesser 4,06 gegen 3,89: Ben soll entscheiden, welcher Wert gilt; Becken bestimmt Wasservolumen (Pool 26,2 m³ bei 3,89).
4. Pflanzmix des Designers (Kartoffel ~35 %, Tomate ~27 %) liegt nahe an Bens Pflanzliste; für D40 (Fruchtgemüse-Anteil) nutzbar.

Geprüft gegen: GLB-Knotenbaum (820 Knoten, 320 Meshes), `data/layout.json`, D26, D35, D36, D40. Offen: Höhenbezug (Designer-Y 0 = Fundament-Unterkante, unser Z-0 = ?) nicht abgeglichen; Bildreferenzen aus `Ref/` (Unbenannt*.PNG, RefSheet.pur) nicht gesichtet.
