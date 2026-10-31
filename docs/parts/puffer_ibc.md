# Bauteilblatt T80 puffer_ibc (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/puffer_ibc.json` und `designs/components/puffer_ibc.sc`, nicht von Hand aendern)

**Funktion:** Puffertank der Puffer-Station (D46): hier wird gemessen und werden Naehrstoffe ausgeglichen. Nutzvolumen ca. 900 l bei Nenninhalt 1000 l. Zulauf und Ueberlauf liegen oben (Seitenstutzen), der Ablauf DN50 mit Kugelhahn unten; die Belueftung und der Sensorstutzen sitzen auf dem Blasendach niedrig (Oberkante z 1190), damit zwei gestapelte IBC unter 2,5 m bleiben.

**Datei:** `designs/components/puffer_ibc.sc` · **Teilenummer:** T80 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche am Boden (x Laenge 1200, y Breite 1000, z hoch); Vorderseite = -Y (Ablauf, Zulauf), Rueckseite = +Y (Ueberlauf)

**Anzahl (Instanzen):** 2 (Puffer-Station: 1 unten, 1 oben) (Quelle: D46 / docs/jobs/W28-puffer-ibc.md)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `ibc_l` | 1200 | mm | [E] Handelsmass Standard-IBC 1000 l: 1200 x 1000 x 1165 (Schuetz/Mauser-Datenblaetter, Messmass nicht recherchiert) |
| `ibc_w` | 1000 | mm | [E] Handelsmass IBC |
| `ibc_h` | 1165 | mm | [E] Handelsmass IBC (Oberkante Deckel) |
| `pal_h` | 150 | mm | [E] Palette 150 mm laut Jobblatt W28 |
| `deck_t` | 22 | mm | [A] Deckplatte der Kunststoffpalette |
| `runner_w` | 160 | mm | [A] Kufenbreite der Palette (3 Kufen laengs) |
| `rail` | 25 | mm | [A] Kaefigrahmen Rechteckrohr 25 x 25 x 1,5 (verzinkt) |
| `rail_wall` | 1.5 | mm | [A] Wand Kaefigrohr |
| `rod_d` | 8 | mm | [A] Gitterstab Durchmesser 8 (Kaefig) |
| `rod_pitch_v` | 200 | mm | [A] Teilung der senkrechten Staebe |
| `rod_pitch_h` | 100 | mm | [A] Teilung der waagerechten Staebe |
| `rod_z0` | 300 | mm | [A] unterster waagerechter Stab (laesst den Ablaufhahn frei) |
| `blase_l` | 1140 | mm | [A] Blase 1140 x 940 innerhalb des Kaefigs (Spiel 5 mm zu den Pfosten) |
| `blase_w` | 940 | mm | [A] Blasenbreite |
| `blase_h` | 995 | mm | [A] Blasenhoehe, von der Palette (z 150) bis 1145 |
| `blase_wall` | 2.5 | mm | [A] Wand PE-Blase (real 1,5-3) |
| `blase_r` | 60 | mm | [A] Eckenradius der Blase |
| `neck_od` | 225 | mm | [E] Einfuelloeffnung DN150 mit Gewindehals ca. D225 |
| `neck_id` | 150 | mm | [E] Einfuelloeffnung DN150 |
| `neck_h` | 15 | mm | [A] Halshoehe ueber der Blase |
| `neck_x` | -200 | mm | [A] Lage des Halses (x), y = 0 |
| `lid_d` | 235 | mm | [A] Schraubdeckel |
| `lid_t` | 5 | mm | [A] Deckelstaerke (Oberkante z 1165) |
| `stub_od` | 63 | mm | [E] PVC-U d63 = DN50 (Rohrnetz leitungsteile) |
| `stub_id` | 55 | mm | [A] Innendurchmesser Stutzen |
| `stub_len_side` | 75 | mm | [A] Seitenstutzen von der Blase bis zum Zapfenende |
| `stub_up` | 45 | mm | [A] Stutzen oben ab Blasendach (Oberkante z 1190 <= 1195, Stapelbedarf) |
| `vent_d` | 32 | mm | [A] Belueftung d32 |
| `port_x` | 300 | mm | [A] Lage der Seitenstutzen (x), zwischen den senkrechten Staeben |
| `zulauf_z` | 1100 | mm | [A] Zulauf oben (seitlich vorn) |
| `ueberlauf_z` | 1090 | mm | [A] Ueberlauf oben (seitlich hinten), ueber dem Nutzwasserstand |
| `ablauf_z` | 215 | mm | [A] Ablauf unten DN50 (vorn), ueber dem Kaefig-Bodenrahmen |
| `hahn_d` | 70 | mm | [A] Kugelhahn DN50 Gehaeuse |
| `hahn_l` | 70 | mm | [A] Kugelhahn Baulaenge |
| `nutz_l` | 900 | l | [E] Nutzvolumen ca. 900 l laut Jobblatt W28 (Nenninhalt 1000 l) |

Gesamt-Box (Messung): X -600.0 bis 600.0, Y -615.0 bis 545.0, Z 0.0 bis 1190.0 mm; Koerper: 77.

**Toleranzen / Spiel:** Blase 5 mm Spiel zu den Eckpfosten; Stutzen sitzen in den Gittermaschen (Abstand >= 3 mm zu den Staeben).

## Werkstoff und Gewicht

- Werkstoff: Stahl verzinkt (Kaefig), PE (Blase), HDPE (Palette), Dichte 7.85 g/cm3, Farbe #aeb4b8 ([A] Handels-IBC)
- Volumen (Messung, `solidcraft-cli eval`): 120713.3 cm3 · Masse leer (ohne Wasser): 69088 g (69.09 kg)
- Gefuellt/in Betrieb: Nutzwasser 900 l = 900 kg je IBC (im Modell als Wasserkoerper, nicht in der Leermasse); Leermasse siehe oben.

## Querschnitt / Profil

Kaefig: Rahmen 25 x 25 x 1,5 (Boden z 150-175, Kopf z 1140-1165), 4 Eckpfosten, senkrechte Staebe D8 alle 200, waagerechte alle 100 ab z 300; Blase 1140 x 940 x 995 Wand 2,5 auf der Palette; Palette 150: Deckplatte 22 und 3 Kufen 160 breit.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf oben | DN50 (d63) | x 300, y -470..-545, z 1100 | -Y (Zapfenende) |
| Ueberlauf oben | DN50 (d63) | x 300, y 470..545, z 1090 | +Y |
| Ablauf unten (Kugelhahn) | DN50 (d63) | x 300, y -575..-615, z 215 | -Y |
| Belueftung | d32 | x -420, y -300, z 1145..1190 | +Z |
| Sensorstutzen | DN50 (d63) | x -420, y 300, z 1145..1190 | +Z |
| Einfuelloeffnung | DN150 | x -200, y 0, z 1145..1165 (Deckel) | +Z |

## Verbindungen und Befestigungen

- Blase steht auf der Palette (Kontakt), Kaefig umschliesst die Blase; Stutzen sind mit der Blase verschweisst/verschraubt (nicht im Detail modelliert); Ablauf: Schraubstutzen S60 x 6 mit Kugelhahn (Platzhalter fuer lt_kugelhahn).

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| IBC 1200 x 1000 x 1165 | 1200/1000/1165 mm | E | Handelsmass Standard-IBC 1000 l (Hersteller-Datenblaetter, nicht geprueft) | mittel |
| Palette 150 mm | 150 mm | E | Jobblatt W28 (Palette 150 mm); Kufen/Deckplatte Annahme | mittel |
| Stahlgitterkaefig (Rahmen 25 x 25 x 1,5, Staebe D8) | 25/8 mm | A | Aufbau typisch; Staebe und Teilung geschaetzt | niedrig |
| PE-Blase 1140 x 940, Wand 2,5 | 2,5 mm | A | Wand real 1,5-3; Inhalt innen ca. 1000 l gerechnet (check_puffer) | mittel |
| Einfuelloeffnung DN150 mit Deckel | D150/D225 | E | Handelsmass der IBC (Gewindehals ca. D225) | mittel |
| Ablauf DN50 mit Kugelhahn unten vorn | d63 | E | Handelsmass; Lage Annahme (z 215 ueber dem Bodenrahmen) | mittel |
| Zulauf/Ueberlauf DN50 seitlich oben, Belueftung d32, Sensorstutzen d63 oben | d63/d32 | A | D46/W28: Zulauf oben, Ueberlauf oben; seitlich statt Deckel wegen der Stapelhoehe <= 2,5 m (check_puffer) | niedrig |
| Nutzvolumen 900 l (Wasserkoerper) | 900 l | E | Jobblatt W28 | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/jobs/W28-puffer-ibc.md und D46 (Ben 31.10.): IBC 1200 x 1000 x 1165; Wandstaerken und Kaefig Annahme A nach Handelsmassen
- Abweichung zum OBJ: keine OBJ-Vorgabe (IBC-Puffer neu, D46); Handelsmass.

## Montage (L4)

1. IBC auf tragfaehigem Untergrund aufstellen (Station: Stapelrahmen T81), Ablaufhahn schliessen
2. Stutzen mit den Rohren der Montage (leitungsteile) verbinden, Belueftung nicht verschliessen
3. Sonden in den Sensorstutzen; Ueberlauf gefaellig abfuehren

**Werkzeug:** Schluessel, Rohrschneider, PVC-Kleber

## Stueckliste-Zeile

- T80 Puffer-IBC 1000 l, Kaefig verzinkt: 2 Stueck in der Puffer-Station (T81)

## Alternative lokale Fertigung

Gebrauchte IBC (Lebensmittel, 1000 l) sind guenstig verfuegbar [A]; Palette aus HDPE oder Stahl.

## Renders

- `renders/components/puffer_ibc/puffer_ibc-01-schraeg.png`
- `renders/components/puffer_ibc/puffer_ibc-02-seite.png`

## Pruefung

- Gauntlet-Urteil: offen (kein Pruefer-Lauf ohne Auftrag; gemeinsamer Lauf mit W25 am Ende)
- scripts/workshop/check_puffer.py ibc (17/17 PASS): Handelsmass 1200 x 1000 x 1165, Palette 150, 50 Gitterstaebe, Nutzvolumen 900 l (Wasserkoerper), Blasen-Innenvolumen 1048 l, Ueberlauf ueber dem Nutzstand, Portlagen und Zapfenenden, Dachstutzen <= 1195, Interferenz 0; Spec-/Bild-Pruefer: gemeinsamer Lauf mit W25 steht aus

## Offene Fragen

- Kaefig/Blase/Palette sind Annahme A nach Handelsmassen; Hersteller offen (Nenngewicht leer ca. 60 kg real, gegen Messung)
- Stutzenlagen (Seitenstutzen statt Deckelstutzen) sind eine Entscheidung dieser Werkstatt wegen Stapelhoehe; Orchestrator/Ben bestaetigen
- Ablaufhahn/Anschluesse sind Platzhalter fuer die Bibliothek leitungsteile (T70)
- Palette als Vollkoerper mit Ersatzdichte 0,2 g/cm3 modelliert (reale Hohlkufen/Rippen: Palettenmasse ca. 20 kg [A]), nicht als HDPE-Dichte 0,95; Masse leer der IBC ca. 70 kg gegen Handelsware 55-70 kg [A]
