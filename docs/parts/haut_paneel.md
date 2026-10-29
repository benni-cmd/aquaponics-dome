# Bauteilblatt T40 haut_paneel (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/haut_paneel.json` und `designs/components/haut_paneel.sc`, nicht von Hand aendern)

**Funktion:** Transparente Haut der Kuppel: dreieckiges Paneel (Polycarbonat-Doppelstegplatte 8 mm) je Kuppelfeld; haelt Wind und Regen ab und laesst Licht durch; Befestigung ueber das Randprofil T41 auf den Streben.

**Datei:** `designs/components/haut_paneel.sc` · **Teilenummer:** T40 · **Revision:** A · **Bezugspunkt:** Inkreismittelpunkt des Strebendreiecks (Achsen der drei Streben), Z = Aussennormale, Paneel von Z 0 (Innenseite) bis Z 8 (Aussenseite); X parallel zur ersten (Typ-)Kante P0P1

**Anzahl (Instanzen):** 40 Felder: 38 volle Paneele + 2 Paneele mit Tuerausschnitt (Tuerknoten 22, Azimut 167.2) (Quelle: data/layout.json dome: 65 Streben, 26 Knoten -> 40 Dreiecke (V - E + F = 1); Tuer bei Azimut 167 (docs/components.md) sitzt auf Basisknoten 22)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `panel_t` | 8 | mm | [A] Doppelstegplatte 8 mm (D35, R11: 6 mm ca. 80 % Lichtdurchlass, 16 mm 65 %) |
| `edge_inset` | 15 | mm | [A] R11: Paneele enden 15 mm vor der Strebenachse (halbe Kappenbreite 30/2) |
| `cap_w` | 30 | mm | [A] R11: Randprofil Aluminium-Kappe 30 mm breit |
| `cap_h` | 8 | mm | [A] R11: Randprofil 8 mm hoch |
| `opacity` | 0.35 |  | [A] R11/D35: Opazitaet ca. 0,35 im Viewer (transparent) |

| Typ | anzahl_felder | anzahl_voll | anzahl_mit_tuerausschnitt | kanten_nominal | kanten_gemessen_min | kanten_gemessen_max | basisfelder |
|---|---|---|---|---|---|---|---|
| AAB | 30 | 29 | 1 | [3279, 3279, 3708] | [3278.8, 3278.9, 3707.6] | [3279.6, 3279.8, 3708.9] | 5 |
| BBB | 10 | 9 | 1 | [3708, 3708, 3708] | [3707.6, 3707.9, 3708.0] | [3708.4, 3708.7, 3708.9] | 5 |

Gesamt-Box (Messung, Variante haut_paneel_AAB): X -1825.5 bis 1403.1, Y -961.9 bis 2049.6, Z 0.0 bis 8.0 mm; Koerper: 1.

**Toleranzen / Spiel:** Fuge zum Randprofil und Dehnung (Polycarbonat ca. 0,07 mm/m/K) nicht modelliert; Aussenflaeche eben (die Kuppelfelder sind plan, die Streben bilden die Kanten).

## Werkstoff und Gewicht

- Werkstoff: Polycarbonat-Doppelstegplatte 8 mm, Dichte 0.19 g/cm3, Farbe #bfe3f0 ([A] Doppelstegplatte 8 mm: Flaechengewicht ca. 1,5 kg/m2 (Herstellerrichtwert, nicht recherchiert) -> mittlere Dichte 1,5 kg/m2 / 8 mm = 0,19 g/cm3 als Vollkoerper (Naeherung fuer die Gewichtsangabe))
- Volumen (Messung, Variante haut_paneel_AAB, `solidcraft-cli eval`): 38891.2 cm3 · Masse leer: 7389 g (7.39 kg)
- Variante `haut_paneel_AAB`: 7.39 kg leer
- Variante `haut_paneel_BBB`: 8.80 kg leer

## Querschnitt / Profil

Ebenes Dreieck, 8 mm dick (Doppelstegplatte), Randabstand 15 mm vor der Strebenachse (Strebendreieck um den Inkreismittelpunkt mit Faktor (r - 15)/r verkleinert); Typ AAB = Strebenlaengen 3279 / 3279 / 3708 (30 Felder), Typ BBB = 3708 x 3 (10 Felder); Hohlkammern der Doppelstegplatte nicht modelliert (Vollkoerper).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| AAB Kante e0 (P0P1): Auflage auf Randprofil | Randkante 3229 mm, Strebe 3279 mm | Kantenmitte x -211, y -962, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt 15 mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen |
| AAB Kante e1 (P1P2): Auflage auf Randprofil | Randkante 3229 mm, Strebe 3279 mm | Kantenmitte x 821, y 544, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt 15 mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen |
| AAB Kante e2 (P2P0): Auflage auf Randprofil | Randkante 3651 mm, Strebe 3708 mm | Kantenmitte x -793, y 544, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt 15 mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen |
| BBB Kante e0 (P0P1): Auflage auf Randprofil | Randkante 3656 mm, Strebe 3708 mm | Kantenmitte x 0, y -1055, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt 15 mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen |
| BBB Kante e1 (P1P2): Auflage auf Randprofil | Randkante 3656 mm, Strebe 3708 mm | Kantenmitte x 914, y 528, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt 15 mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen |
| BBB Kante e2 (P2P0): Auflage auf Randprofil | Randkante 3656 mm, Strebe 3708 mm | Kantenmitte x -914, y 528, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt 15 mm vor der Strebenachse auf der Kappe T41 (Kappe 30 breit: 15 mm Auflage je Seite); Normale in der Plattenebene nach aussen |

## Verbindungen und Befestigungen

- Paneelkante liegt auf dem Randprofil T41 (Aluminium-Kappe 30 x 8) ueber der Strebe, 15 mm Auflage je Seite; Befestigung der Kappe auf der Strebe (Schrauben/Klemmung) und Dichtband nicht modelliert [A]
- Tuerfelder: die zwei Basisfelder am Tuerknoten brauchen einen Tuerausschnitt 1000 x 2000 (Zuschnitt = spaeterer Schritt, nicht modelliert)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Dreieckstypen AAB (30) und BBB (10), 40 Felder | 40 Felder | OBJ | layout.json dome.nodes_list + strut_len_mm: 65 Streben aus Knotenabstaenden, Dreiecke = Knotentripel (V - E + F = 1) | hoch |
| Strebenlaengen 3279 (A) / 3708 (B) | 3279 / 3708 mm | OBJ | layout.json dome.strut_len_mm; gemessene Knotenabstaende 3278,8-3279,8 / 3707,6-3708,9 | hoch |
| Doppelstegplatte 8 mm, transparent | 8 mm | A | docs/decisions.md D35, R11 (Domerama, Northern Homestead: Polycarbonat/Folie auf Kanalprofilen); 6 mm ca. 80 % Licht, 16 mm 65 % | niedrig |
| Rand 15 mm vor der Strebenachse | 15 mm | A | R11: halbe Kappenbreite 30/2 | niedrig |
| Dichte 0,19 g/cm3 | 0,19 g/cm3 | A | Flaechengewicht ca. 1,5 kg/m2 (Herstellerrichtwert, nicht recherchiert) / 8 mm | niedrig |
| Opazitaet 0,35 im Viewer | 0,35 | A | R11/D35 | niedrig |
| Tuer bei Azimut 167 (Basisknoten 22) beruehrt 2 Felder | 2 Felder | OBJ + E | docs/components.md (Tuer Azimut 167 im OBJ, 1000 x 2000); Basisknoten 22 hat Azimut 167,2: beide Basisfelder am Knoten (149,2 BBB und 185,2 AAB) beruehrt | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: data/layout.json dome (nodes_list, strut_len_mm, struts 65), docs/research/R11.md (Doppelstegplatte 8 mm, Paneele enden 15 mm vor der Strebenachse), docs/decisions.md D35
- Abweichung zum OBJ: keine OBJ-Vorgabe (das OBJ-Dom hat keine Haut); Dreiecksseiten aus den Strebenlaengen layout.json dome.strut_len_mm (3279 A / 3708 B, gemessene Knotenabstaende 3278,8-3279,8 bzw. 3707,6-3708,9).

## Montage (L4)

1. Randprofile T41 auf alle 65 Streben setzen und befestigen
2. Paneele je Feld auflegen (Typ AAB/BBB nach Feld, Lage aus den Knoten), Kanten auf die Kappen, Klemmleisten/Dichtband setzen
3. Tuerfelder mit Ausschnitt zuschneiden

**Werkzeug:** Akkuschrauber, Dichtband, Hebezeug/Helfer (ein Paneel bis ca. 9 kg)

## Stueckliste-Zeile

- T40 Haut-Paneel Typ AAB: 29 voll + 1 mit Tuerausschnitt = 30; Flaeche 4.86 m2, 7.4 kg
- T40 Haut-Paneel Typ BBB: 9 voll + 1 mit Tuerausschnitt = 10; Flaeche 5.79 m2, 8.8 kg
- Gesamtflaeche Haut ca. 204 m2 (40 Felder)

## Alternative lokale Fertigung

Doppelstegplatten 8 mm sind Baumarktware (Gewaechshausbau); Zuschnitt auf Dreiecke selbst oder per Zuschnittservice [A, nicht recherchiert]; Folie als billige Variante (R11).

## Renders

- `renders/components/haut_paneel/haut_paneel_AAB-01-draufsicht.png`
- `renders/components/haut_paneel/haut_paneel_BBB-01-draufsicht.png`

## Pruefung

- Gauntlet-Urteil: offen (kein Pruefer-Lauf, Wochenlimit)
- scripts/workshop/check_haut.py (27/27 PASS, Ergebnis renders/components/haut_paneel/check.txt): Felderzahl (Euler), Typen, Dicke 8, Flaeche gegen Heron-Rechnung, Randkanten, Randabstand 15 mm (Inkreisradius), Masse
- Bild renders/components/haut_paneel/haut_paneel_AAB-01-draufsicht.png (und BBB); kein Bild-Kritiker, kein Spec-Pruefer (Wochenlimit, W19 Auftrag)

## Offene Fragen

- Tuer: die zwei Basisfelder am Tuerknoten 22 (Azimut 167,2) tragen den Tuerausschnitt; Zuschnittform nicht modelliert; Lage der Tuer im Dom (Knoten statt Feldmitte) mit Montage/Orchestrator pruefen
- Hohlkammern, Dichtband, Klemmleisten, Lueftungsklappen nicht modelliert; Material/Preis/UV nicht recherchiert (R11 offen)
- Paneele sind eben; die Streben liegen auf der Kugel, die Felder sind plan (Pfeilhoehe zur Kugel bei 3,7 m Kante ca. 0,2 m): Aussenflaeche haengt an den Streben, Einbau durch die Montage
- Plattenlage: Inkreismittelpunkt des Strebendreiecks (Strebenachsen), nicht Schwerpunkt; Z 0 = Innenseite
