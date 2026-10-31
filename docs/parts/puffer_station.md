# Bauteilblatt T81 puffer_station (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/puffer_station.json` und `designs/components/puffer_station.sc`, nicht von Hand aendern)

**Funktion:** Puffer-Station (D46): Neben Pool und Becken werden hier Wasserwerte gemessen (pH, EC, Temperatur, O2) und Naehrstoffe/pH-Puffer ueber zwei Schlauchpumpen aus 20-l-Kanistern zudosiert. Zwei IBC stehen uebereinander (oben Zulauf und Messung, unten Vorrat), verbunden durch ein DN50-Rohr mit Kugelhahn vom Ablauf der oberen zum Zulauf der unteren IBC. Gesamtstapel der IBC samt Rahmen 2445 mm (<= 2,5 m).

**Datei:** `designs/components/puffer_station.sc` · **Teilenummer:** T81 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche der unteren IBC am Boden; X = Laenge der IBC (Messplatz -X, Dosierkonsole +X), Y: vorn -Y (Ablauf, Verbindungsrohr), hinten +Y (Ueberlauf, Plattform), Z hoch

**Anzahl (Instanzen):** 1 Station (Sektor 185,2 rechts der Tuer) (Quelle: D46; Platzierung Montage M8)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `sta_leg` | 60 | mm | [A] Stapelrahmen Rechteckrohr 60 x 60 x 3 verzinkt (Jobblatt W28: Rohre 60 x 60) |
| `sta_wall` | 3 | mm | [A] Wandstaerke Stapelrahmen |
| `sta_leg_x` | 640 | mm | [A] Beine ausserhalb des IBC-Kaefigs (Kaefig +-600, Bein 610..670, 10 mm Luft) |
| `sta_leg_y` | 540 | mm | [A] Beine ausserhalb des Kaefigs (+-500, Bein 510..570) |
| `sta_beam_z` | 1135 | mm | [A] Unterkante der Stirnbalken: Oberkante unterer Kaefig 1165 minus Kopfrahmen; Stirnbalken liegen ausserhalb des Kaefigs |
| `sta_xbeam_z` | 1195 | mm | [A] Unterkante Laengstraeger = Oberkante der Dachstutzen des unteren IBC (1190) + 5; Tragebene Palette der oberen IBC |
| `sta_z_up` | 1255 | mm | [R] Oberkante Laengstraeger = Unterkante Palette des oberen IBC; Stapelhoehe = 1255 + 1165 (+ Dachstutzen 25) = 2445 <= 2500 |
| `sta_foot` | 80 | mm | [A] Fussplatte 80 x 80 x 8 (Platte endet am Palettenrand x 600 / y 500: Kufen und Platten beruehren sich nur) |
| `sta_diag` | 30 | mm | [A] Diagonalrohr 30 x 30 x 2 an den Stirnseiten (ausserhalb der Beine) |
| `sta_stack_max` | 2500 | mm | [E] Jobblatt W28: Gesamtstapel <= 2,5 m (D46: AAB-Feld in 185,2 hat Spitze Z 2669 -> Abstand zu den Streben) |
| `pipe_y` | -660 | mm | [A] Verbindungsrohr DN50 (d63) vorn ausserhalb: y |
| `mess_x` | -1120 | mm | [A] Messplatz-Staender am -X-Ende der Station |
| `kon_x` | 1000 | mm | [A] Dosierkonsole am +X-Ende (Platten x 800..1200) |
| `plat_z` | 1500 | mm | [A] Wartungsplattform Oberkante 1506: Deckel der oberen IBC (z 2420) liegt 914 ueber dem Standplatz |
| `gel_h` | 900 | mm | [E] Gelaenderhoehe (Regel ab 1 m Absturzhoehe: 1000, hier 900 wegen Stapelgrenze 2,5 m; offen) |

Gesamt-Box (Messung): X -1220.0 bis 1200.0, Y -691.5 bis 1230.0, Z 0.0 bis 2445.0 mm; Koerper: 230.

**Toleranzen / Spiel:** Kaefig/Rahmen 10 mm Luft; Dachstutzen der unteren IBC (z 1190) 5 mm unter den Laengstraegern (1195).

## Werkstoff und Gewicht

- Werkstoff: Stahl verzinkt (Rahmen), IBC T80, Dichte 7.85 g/cm3, Farbe #aeb4b8 ([A])
- Volumen (Messung, `solidcraft-cli eval`): 315541.1 cm3 · Masse leer (ohne Wasser): 377712 g (377.71 kg)
- Gefuellt/in Betrieb: 2 x 900 kg Nutzwasser plus Leermassen; Rahmen traegt ca. 1000 kg (obere IBC gefuellt) auf 3 Laengstraegern [A, nicht gerechnet]

## Querschnitt / Profil

Stapelrahmen: 4 Beine 60 x 60 x 3 (x +-640, y +-540) mit Fussplatten 80 x 80 x 8, 2 Stirnbalken (z 1135-1195) und 3 Laengstraeger (z 1195-1255, y -420 / 0 / 420) unter den Kufen der oberen Palette; Diagonalen 30 x 30 x 2 an den Stirnseiten. Messplatz bei x -1120, Dosierkonsole bei x 1000, Plattform auf z 1500 mit Leiter an der Rueckseite.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf (obere IBC) | DN50 (d63) | x 300, y -545, z 2355 (1255 + 1100) | -Y |
| Ueberlauf (obere IBC) | DN50 (d63) | x 300, y 545, z 2345 | +Y |
| Ueberlauf (untere IBC) | DN50 (d63) | x 300, y 545, z 1090 | +Y |
| Ablauf unten (untere IBC, Kugelhahn) | DN50 (d63) | x 300, y -615, z 215 | -Y |
| Verbindung oben->unten | DN50 (d63) | von x 300, y -615, z 1470 ueber y -660 nach x 300, y -545, z 1100 | Platzhalter-Rohr im Modell |
| Belueftung/Sensorstutzen | d32 / DN50 | je IBC auf dem Dach (z 1190 bzw. 2445) | +Z |

## Verbindungen und Befestigungen

- Stapelrahmen auf Fussplatten am Boden verankert (Duebel/Ankerplatten nicht modelliert) [A]; Laengstraeger auf den Stirnbalken geschweisst; Paletten stehen auf den Laengstraegern (Kufen y -420/0/420 liegen auf), gegen Verrutschen mit Spanngurt/Winkel (nicht modelliert) [A]
- Messplatz und Dosierkonsole stehen frei auf Fussplatten (Duebel nicht modelliert)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| 2 IBC uebereinander | 2 x T80 | E | D46 (Ben 31.10.), Jobblatt W28 | hoch |
| Stapelrahmen 4 Beine 60 x 60 x 3, Stirnbalken, 3 Laengstraeger | 60 mm | A | Jobblatt: verzinkte Rohre 60 x 60; Lagen aus der Stapelhoehe gerechnet | mittel |
| Stapelhoehe 2445 mm (IBC 2 x 1165 + Rahmen 90) | <= 2500 | R | check_puffer station: hoechster Koerper der IBC-Instanzen minus Boden | hoch |
| Verbindungsrohr DN50 oben->unten | d63 | A | Jobblatt: Verbindung DN50 mit Kugelhahn (Hahn im IBC T80); Rohr Platzhalter fuer leitungsteile | niedrig |
| Messplatz: 4 Sonden, Messbecher, Kabelkanal | D14/D160 | A | Jobblatt W28; Sondenmasse Annahme | niedrig |
| Dosierkonsole: 2 Schlauchpumpen 140 x 120 x 100, 2 Kanister 20 l (250 x 300 x 280) | 20 l | A | Jobblatt W28 (Kanister 20 l); Pumpenmasse Annahme | niedrig |
| Wartungsplattform 1360 x 610, Leiter, Gelaender 900 | z 1506 | A | Jobblatt W28; Hoehe so, dass der Deckel der oberen IBC erreichbar ist | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/jobs/W28-puffer-ibc.md und D46 (Ben 31.10.): Stapelhoehe <= 2,5 m, Messplatz, Dosierkonsole; Masse Annahme A
- Abweichung zum OBJ: keine OBJ-Vorgabe; Konzept der Werkstatt nach Jobblatt W28.

## Montage (L4)

1. Fussplatten setzen, Stapelrahmen aufstellen und verschweissen/verschrauben
2. Untere IBC einschieben (Lage: Ablauf nach vorn), Laengstraeger auflegen, obere IBC mit Stapler/Kran aufsetzen
3. Verbindungsrohr DN50 mit Kugelhahn, Ueberlaeufe und Belueftung anschliessen; Messplatz, Dosierkonsole, Plattform und Leiter aufstellen

**Werkzeug:** Stapler/Kran, Schweissgeraet oder Schraubensatz, Wasserwaage, Rohrschneider

## Stueckliste-Zeile

- T81 Puffer-Station: 2 x T80 Puffer-IBC, Stapelrahmen (4 Beine, 2 Stirnbalken, 3 Laengstraeger, 2 Diagonalen), Verbindungsrohr, Messplatz, Dosierkonsole, Wartungsplattform mit Leiter

## Alternative lokale Fertigung

Rahmen aus handelsueblichem Stahlrohr 60 x 60 verschweisst; Messplatz-Staender, Konsole und Plattform als Schlosserarbeit [A].

## Renders

- `renders/components/puffer_station/puffer_station-01-schraeg.png`
- `renders/components/puffer_station/puffer_station-02-seite.png`

## Pruefung

- Gauntlet-Urteil: offen (kein Pruefer-Lauf ohne Auftrag; gemeinsamer Lauf mit W25 am Ende)
- scripts/workshop/check_puffer.py station (27/27 PASS): Stapel auf z 1255, Stapelhoehe 2445 <= 2500, Gesamthoehe inkl. Plattform <= 2500, Rahmen 10 mm ausserhalb des Kaefigs, Traeger unter den Kufen, Verbindungsrohr, Sonden im Becher, Kanister >= 20 l, Deckel 914 ueber der Plattform, Interferenz 0; Spec-/Bild-Pruefer: gemeinsamer Lauf steht aus

## Offene Fragen

- Statik Stapelrahmen und Plattform nicht gerechnet (1000 kg auf 3 Traegern 60 x 60 x 3 ueber 1340 mm: grobe Abschaetzung ok, Nachweis offen)
- Geländerhoehe 900 statt 1000 wegen Stapelgrenze 2,5 m (Absturzhoehe der Plattform 1,5 m)
- Verbindungsrohr, Ablaufhahn und Anschluesse sind Platzhalter fuer die Bibliothek leitungsteile (T70); Verlegung und Ueberlaufleitung: Montage M8
- Sondenfabrikate, Pumpenfabrikat, Dosierleitungen (Schlaeuche Pumpe -> Sensorstutzen) nicht modelliert; Rolle/Volumen/Strom: Fachrecherche R27
- Messbecher/Durchflusszelle nur als Becher; Probenahme-Hahn fehlt
