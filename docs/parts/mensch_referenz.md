# Bauteilblatt T90 mensch_referenz (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/mensch_referenz.json` und `designs/components/mensch_referenz.sc`, nicht von Hand aendern)

**Funktion:** Groessenreferenz im Modell (D47): zwei Figuren 1,80 m, die so aussehen, als arbeiteten sie gerade an der Anlage; wichtig ist die Groesse (Laufwege, Tischhoehen, Stapelhoehe lassen sich daran ablesen). Typ messen an der Puffer-Station, Typ arbeiten im Laufweg B zwischen Mittel- und Aussenring.

**Datei:** `designs/components/mensch_referenz.sc` · **Teilenummer:** T90 · **Revision:** A · **Bezugspunkt:** Fussmitte am Boden (Z 0), Blickrichtung +Y, X seitlich (rechte Hand +X); Hoehe aufrecht 1800

**Anzahl (Instanzen):** 2 Instanzen: messen (Puffer-Station) und arbeiten (Laufweg B zwischen Mittel- und Aussenring) (Quelle: D47; Platzierung Montage M9)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `height` | 1800 | mm | [E] Ben 31.10./D47: 1,80 m; Gesamthoehe aufrecht exakt 1800 (Parameter, Standard 1800) |
| `lean` | 0 | deg | [A] Oberkoerperneigung nach vorn um die Huefte; aufrecht 0, messen 10, arbeiten 20 (typen) |
| `k_head` | 0.13 |  | [E] Drillis/Contini: Kopfhoehe 0,13 H (Scheitel bis Kinn) |
| `k_shoulder` | 0.818 |  | [E] Drillis/Contini: Schulterhoehe 0,818 H |
| `k_elbow` | 0.63 |  | [E] Drillis/Contini: Ellbogenhoehe 0,63 H |
| `k_hip` | 0.53 |  | [E] Drillis/Contini: Huefthoehe 0,53 H |
| `k_knee` | 0.285 |  | [E] Drillis/Contini: Kniehoehe 0,285 H |
| `k_sw` | 0.259 |  | [E] Drillis/Contini: Schulterbreite 0,259 H = 466 mm |
| `k_fw` | 0.055 |  | [E] Drillis/Contini: Fussbreite 0,055 H |
| `k_fl` | 0.152 |  | [E] Drillis/Contini: Fusslaenge 0,152 H |
| `k_ankle` | 0.044 |  | [A] Knoechelhoehe 0,044 H (Anteil der Fussbreite/Hoehe) |
| `rho` | 0.87 |  | [A] Ersatzdichte 0,87 g/cm3, damit die stilisierte Silhouette (Zylinder, Kasten) ca. 80 kg ergibt (echter Koerper 1,01-1,07 bei 75-80 kg; die Figur ist voluminoeser) |

| Typ | lean | beschreibung | hand_r | hand_l |
|---|---|---|---|---|
| aufrecht | 0 | steht aufrecht, Arme hängen (Pruefkoerper fuer Hoehe 1800 und Schulterbreite 466) |  |  |
| messen | 10 | Oberkoerper 10 Grad vorgebeugt, rechter Arm vorgestreckt auf Brusthoehe (zur Dosierkonsole/Sonde), linke Hand haelt ein Messgeraet | [0.1, 0.3, 0.69] | [-0.1, 0.19, 0.64] |
| arbeiten | 20 | Oberkoerper 20 Grad vorgebeugt, beide Arme nach vorn auf ca. 1,2-1,3 m (Pflanzen/Ernten am NFT-Tisch) | [0.1, 0.27, 0.69] | [-0.1, 0.27, 0.69] |

Gesamt-Box (Messung): X -233.1 bis 233.1, Y -115.0 bis 203.6, Z 0.0 bis 1800.0 mm; Koerper: 14.

**Toleranzen / Spiel:** Hoehe 1800 +-2, Schulterbreite 466 +-10, Hand-Ziele +-30 mm (IK-Naeherung).

## Werkstoff und Gewicht

- Werkstoff: Koerper (Ersatzdichte 0,87 g/cm3), Dichte 0.87 g/cm3, Farbe #2f5fa8 ([A] Mensch ca. 1,0; Farben als Hinweis: Kleidung blau, Weste orange, Kopf/Haende hautfarben)
- Volumen (Messung, `solidcraft-cli eval`): 91900.0 cm3 · Masse leer: 79953 g (79.95 kg)
- Variante `mensch_referenz_messen`: 80.25 kg leer
- Variante `mensch_referenz_arbeiten`: 79.95 kg leer

## Querschnitt / Profil

Rumpf 466 x 230 (Huefte bis Schulter), Kopf als Kugel D190 mit Kinn/Hals (234 hoch), Oberarm D80, Unterarm D65 samt Hand, Oberschenkel D150, Unterschenkel D100, Fuss 99 x 274 x 80. Wenige Flaechen (< 800), Teile > 150 mm.

## Verbindungen und Befestigungen

- Koerperteile als getrennte Koerper (Gelenke Kugeln nicht modelliert); Posen starr, keine Joints.

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Koerperhoehe H | 1800 mm | E | Ben 31.10./D47 | hoch |
| Kopf 0,13 H, Schulterhoehe 0,818 H, Ellbogen 0,63 H, Huefte 0,53 H, Knie 0,285 H | 234/1472/1134/954/513 mm | E | Drillis/Contini (Anteile der Koerperhoehe, Jobblatt W29) | mittel |
| Schulterbreite 0,259 H | 466 mm | E | Drillis/Contini; Rumpf 466 breit, Arme innerhalb der Rumpfbreite | mittel |
| Fussbreite 0,055 H, Fusslaenge 0,152 H | 99 x 274 mm | E | Drillis/Contini | mittel |
| Querschnitte der Gliedmassen und des Rumpfes (Rumpftiefe 230, Oberschenkel D 150, Unterschenkel D 100, Oberarm D 80, Unterarm D 65) | 50-230 mm | A | Annahme fuer eine einfache Silhouette; nicht anthropometrisch genau | niedrig |
| Posen: Neigungen 10 / 20 Grad, Handziele | 10/20 deg | A | Jobblatt W29: messen Brusthoehe, arbeiten 1,2-1,3 m | niedrig |
| Koerperdichte 0,87 g/cm3 (Ersatzdichte, Masse ca. 80 kg) | 0,87 | A | stilisierte Koerper sind voluminoeser als ein Mensch (Rumpf 466 x 230 Kasten) | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/jobs/W29-mensch-referenz.md, D47 (Ben 31.10.); Proportionen Drillis/Contini (Anteile der Koerperhoehe H)
- Abweichung zum OBJ: keine OBJ-Vorgabe; Referenz fuer die Groesse, kein Bauteil der Anlage.

## Montage (L4)

1. Platzierung durch die Montage (M9): Fusspunkt auf den Boden, Blickrichtung +Y auf die Arbeitsstelle drehen

**Werkzeug:** keines (Referenzfigur)

## Stueckliste-Zeile

- T90 Mensch-Referenz 1,80 m: 2 Instanzen (messen, arbeiten); keine Beschaffung

## Alternative lokale Fertigung

nicht zutreffend (Darstellung).

## Renders

- `renders/components/mensch_referenz/mensch_referenz-massstab.png`
- `renders/components/mensch_referenz/mensch_referenz_arbeiten-schraeg.png`
- `renders/components/mensch_referenz/mensch_referenz_arbeiten-seite.png`
- `renders/components/mensch_referenz/mensch_referenz_aufrecht-schraeg.png`
- `renders/components/mensch_referenz/mensch_referenz_aufrecht-seite.png`
- `renders/components/mensch_referenz/mensch_referenz_messen-schraeg.png`
- `renders/components/mensch_referenz/mensch_referenz_messen-seite.png`

## Pruefung

- Gauntlet-Urteil: kein Pruefer-Lauf (Jobblatt: Selbstcheck genuegt)
- scripts/workshop/check_mensch.py (33/33 PASS, Selbstcheck): Hoehe 1800, Schulterbreite 466, Schulter-/Huefte-/Knie-/Ellbogenhoehe nach Drillis/Contini aus den Koerper-Boxen, Fuss 99 x 274, Masse 80 kg, Flaechen < 800 je Figur, alle Teile > 150 mm, Neigung 10/20 Grad aus der Rumpf-Box, Haende am Ziel (+-60), Messgeraet in der linken Hand; Bild renders/components/mensch_referenz/mensch_referenz-massstab.png mit Massstab

## Offene Fragen

- Proportionen Drillis/Contini sind Mittelwerte (Maenner, 1,80 m = P75-P90); Frauen/Kleinere nicht modelliert
- Querschnitte und Posen Annahme A; Hand/Fingerform nicht modelliert; Farben als Hinweis (Kleidung blau, Weste orange, Haut), im Modell nur Materialien je Teil
- Kein Spec-/Bild-Pruefer (Limit); Selbstcheck check_mensch.py
