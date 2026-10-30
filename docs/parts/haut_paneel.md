# Bauteilblatt T40 haut_paneel (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/haut_paneel.json` und `designs/components/haut_paneel.sc`, nicht von Hand aendern)

**Funktion:** Transparente Haut der Kuppel: dreieckiges Paneel (Polycarbonat-Doppelstegplatte 8 mm) je Kuppelfeld; haelt Wind und Regen ab und laesst Licht durch; Befestigung ueber das Randprofil T41 auf den Streben.

**Datei:** `designs/components/haut_paneel.sc` · **Teilenummer:** T40 · **Revision:** A · **Bezugspunkt:** Inkreismittelpunkt des Strebendreiecks (Achsen der drei Streben), Z = Aussennormale, Paneel von Z 0 (Innenseite) bis Z 8 (Aussenseite); X parallel zur ersten (Typ-)Kante P0P1

**Anzahl (Instanzen):** 40 Felder: 39 volle Paneele + 1 Paneel mit Tuerausschnitt (Basisfeld BBB 149.2) (Quelle: data/layout.json dome: 65 Streben, 26 Knoten -> 40 Dreiecke (V - E + F = 1); Tuerfeld nach D36 (docs/decisions.md))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `panel_t` | 8 | mm | [A] Doppelstegplatte 8 mm (D35, R11: 6 mm ca. 80 % Lichtdurchlass, 16 mm 65 %) |
| `edge_inset` | 0 | mm | [A] D37 (30.10.): Paneel reicht bis zur Strebenachse, die Kappe T41 (30 breit) klemmt beide Nachbarkanten mit 15 mm Auflage je Seite; vorher 15 (buendig an der Kappenkante, Auflage 0, Befund Pruefer W19; R11 widerspricht sich: 'Paneele enden 15 mm vor der Achse' gegen 'Randprofil haelt die Paneelkanten') |
| `cap_w` | 30 | mm | [A] R11: Randprofil Aluminium-Kappe 30 mm breit |
| `cap_h` | 8 | mm | [A] R11: Randprofil 8 mm hoch |
| `opacity` | 0.35 |  | [A] R11/D35: Opazitaet ca. 0,35 im Viewer (transparent) |

| Typ | anzahl_felder | anzahl_voll | anzahl_mit_tuerausschnitt | kanten_nominal | kanten_gemessen_min | kanten_gemessen_max | basisfelder |
|---|---|---|---|---|---|---|---|
| AAB | 30 | 30 | 0 | [3279, 3279, 3708] | [3278.8, 3278.9, 3707.6] | [3279.6, 3279.8, 3708.9] | 5 |
| BBB | 10 | 9 | 1 | [3708, 3708, 3708] | [3707.6, 3707.9, 3708.0] | [3708.4, 3708.7, 3708.9] | 5 |

Gesamt-Box (Messung, Variante haut_paneel_AAB): X -1854.0 bis 1425.0, Y -976.9 bis 2081.5, Z 0.0 bis 8.0 mm; Koerper: 1.

**Toleranzen / Spiel:** Fuge zum Randprofil und Dehnung (Polycarbonat ca. 0,07 mm/m/K) nicht modelliert; Aussenflaeche eben (die Kuppelfelder sind plan, die Streben bilden die Kanten).

## Werkstoff und Gewicht

- Werkstoff: Polycarbonat-Doppelstegplatte 8 mm, Dichte 0.19 g/cm3, Farbe #bfe3f0 ([A] Doppelstegplatte 8 mm: Flaechengewicht ca. 1,5 kg/m2 (Herstellerrichtwert, nicht recherchiert) -> mittlere Dichte 1,5 kg/m2 / 8 mm = 0,19 g/cm3 als Vollkoerper (Naeherung fuer die Gewichtsangabe))
- Volumen (Messung, Variante haut_paneel_AAB, `solidcraft-cli eval`): 40113.7 cm3 · Masse leer: 7622 g (7.62 kg)
- Variante `haut_paneel_AAB`: 7.62 kg leer
- Variante `haut_paneel_BBB`: 9.05 kg leer
- Variante `haut_paneel_BBB_tuer`: 5.67 kg leer

## Querschnitt / Profil

Ebenes Dreieck, 8 mm dick (Doppelstegplatte), Paneel reicht bis zur Strebenachse (edge_inset 0, D37; die Paneelform ist das Strebendreieck), die Kappe T41 klemmt beide Kanten, Auflage 15 mm je Seite; Typ AAB = Strebenlaengen 3279 / 3279 / 3708 (30 Felder), Typ BBB = 3708 x 3 (10 Felder); Hohlkammern der Doppelstegplatte nicht modelliert (Vollkoerper).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| AAB Kante e0 (P0P1): Auflage auf dem Randprofil | Randkante 3279 mm, Strebe 3279 mm | Kantenmitte x -214, y -977, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt auf der Strebenachse (edge_inset 0) und mit 15 mm Auflage auf der Kappe T41 (30 breit, klemmt beide Nachbarkanten; Klemmung/Schrauben/Dichtband nicht modelliert); Normale in der Plattenebene nach aussen |
| AAB Kante e1 (P1P2): Auflage auf dem Randprofil | Randkante 3279 mm, Strebe 3279 mm | Kantenmitte x 834, y 552, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt auf der Strebenachse (edge_inset 0) und mit 15 mm Auflage auf der Kappe T41 (30 breit, klemmt beide Nachbarkanten; Klemmung/Schrauben/Dichtband nicht modelliert); Normale in der Plattenebene nach aussen |
| AAB Kante e2 (P2P0): Auflage auf dem Randprofil | Randkante 3708 mm, Strebe 3708 mm | Kantenmitte x -806, y 552, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt auf der Strebenachse (edge_inset 0) und mit 15 mm Auflage auf der Kappe T41 (30 breit, klemmt beide Nachbarkanten; Klemmung/Schrauben/Dichtband nicht modelliert); Normale in der Plattenebene nach aussen |
| BBB Kante e0 (P0P1): Auflage auf dem Randprofil | Randkante 3708 mm, Strebe 3708 mm | Kantenmitte x 0, y -1070, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt auf der Strebenachse (edge_inset 0) und mit 15 mm Auflage auf der Kappe T41 (30 breit, klemmt beide Nachbarkanten; Klemmung/Schrauben/Dichtband nicht modelliert); Normale in der Plattenebene nach aussen |
| BBB Kante e1 (P1P2): Auflage auf dem Randprofil | Randkante 3708 mm, Strebe 3708 mm | Kantenmitte x 927, y 535, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt auf der Strebenachse (edge_inset 0) und mit 15 mm Auflage auf der Kappe T41 (30 breit, klemmt beide Nachbarkanten; Klemmung/Schrauben/Dichtband nicht modelliert); Normale in der Plattenebene nach aussen |
| BBB Kante e2 (P2P0): Auflage auf dem Randprofil | Randkante 3708 mm, Strebe 3708 mm | Kantenmitte x -927, y 535, z 0..8 (Bezug = Inkreismittelpunkt) | Kante liegt auf der Strebenachse (edge_inset 0) und mit 15 mm Auflage auf der Kappe T41 (30 breit, klemmt beide Nachbarkanten; Klemmung/Schrauben/Dichtband nicht modelliert); Normale in der Plattenebene nach aussen |

## Verbindungen und Befestigungen

- Paneelkante reicht bis zur Strebenachse und liegt mit 15 mm Auflage je Seite auf dem Randprofil T41 (Aluminium-Kappe 30 x 8 ueber der Strebe), die Kappe klemmt beide Nachbarkanten (D37; R11 widerspricht sich: 'Paneele enden 15 mm vor der Achse' gegen 'Randprofil haelt die Paneelkanten'); Befestigung der Kappe auf der Strebe, Klemmung und Dichtband nicht modelliert [A]
- Tuerfeld (D36): das Basisfeld BBB 149,2 bekommt das Paneel haut_paneel_BBB_tuer mit Ausschnitt = Zarge (1076 x 2068, in der Feldebene) ab der Basiskante; Zarge siehe docs/parts/tuer_komplett.md

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Dreieckstypen AAB (30) und BBB (10), 40 Felder | 40 Felder | OBJ | layout.json dome.nodes_list + strut_len_mm: 65 Streben aus Knotenabstaenden, Dreiecke = Knotentripel (V - E + F = 1) | hoch |
| Strebenlaengen 3279 (A) / 3708 (B) | 3279 / 3708 mm | OBJ | layout.json dome.strut_len_mm; gemessene Knotenabstaende 3278,8-3279,8 / 3707,6-3708,9 | hoch |
| Doppelstegplatte 8 mm, transparent | 8 mm | A | docs/decisions.md D35, R11 (Domerama, Northern Homestead: Polycarbonat/Folie auf Kanalprofilen); 6 mm ca. 80 % Licht, 16 mm 65 % | niedrig |
| Paneel bis zur Strebenachse (edge_inset 0), Auflage 15 mm je Seite auf der Kappe | 0 / 15 mm | A | D37 (Werkstatt W21, Befund B1): Kappe klemmt beide Kanten; R11 widerspricht sich (Paneele enden 15 mm vor der Achse gegen Randprofil haelt die Paneelkanten) | niedrig |
| Dichte 0,19 g/cm3 | 0,19 g/cm3 | A | Flaechengewicht ca. 1,5 kg/m2 (Herstellerrichtwert, nicht recherchiert) / 8 mm | niedrig |
| Opazitaet 0,35 im Viewer | 0,35 | A | R11/D35 | niedrig |
| Tuerfeld BBB 149,2 (D36) | 1 Feld | E | D36 (30.10.): Tuer mittig im Basisfeld BBB 149,2 statt auf Knoten 22 (OBJ Azimut 167 beruehrte zwei Felder); Ausschnitt = Zarge Aussenmass (tuer_komplett.json) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: data/layout.json dome (nodes_list, strut_len_mm, struts 65), docs/research/R11.md (Doppelstegplatte 8 mm, Paneel bis zur Strebenachse, Kappe klemmt beide Kanten mit 15 mm Auflage je Seite: D37), docs/decisions.md D35
- Abweichung zum OBJ: keine OBJ-Vorgabe (das OBJ-Dom hat keine Haut); Dreiecksseiten aus den Strebenlaengen layout.json dome.strut_len_mm (3279 A / 3708 B, gemessene Knotenabstaende 3278,8-3279,8 bzw. 3707,6-3708,9).

## Montage (L4)

1. Randprofile T41 auf alle 65 Streben setzen und befestigen
2. Paneele je Feld auflegen (Typ AAB/BBB nach Feld, Lage aus den Knoten), Kanten auf die Kappen, Klemmleisten/Dichtband setzen
3. Tuerfeld BBB 149,2: Paneel BBB_tuer auflegen (Ausschnitt an der Zarge)

**Werkzeug:** Akkuschrauber, Dichtband, Hebezeug/Helfer (ein Paneel bis ca. 9 kg)

## Stueckliste-Zeile

- T40 Haut-Paneel Typ AAB: 30 voll + 0 mit Tuerausschnitt = 30; Flaeche 5.01 m2, 7.6 kg
- T40 Haut-Paneel Typ BBB: 9 voll + 1 mit Tuerausschnitt = 10; Flaeche 5.95 m2, 9.0 kg
- Gesamtflaeche Haut ca. 207.7 m2 (39 volle Paneele + Tuerpaneel mit Ausschnitt 3.73 m2)

## Alternative lokale Fertigung

Doppelstegplatten 8 mm sind Baumarktware (Gewaechshausbau); Zuschnitt auf Dreiecke selbst oder per Zuschnittservice [A, nicht recherchiert]; Folie als billige Variante (R11).

## Renders

- `renders/components/haut_paneel/haut_paneel_AAB-01-draufsicht.png`
- `renders/components/haut_paneel/haut_paneel_BBB-01-draufsicht.png`
- `renders/components/haut_paneel/haut_paneel_BBB_tuer-01-draufsicht.png`

## Pruefung

- Gauntlet-Urteil: offen (kein Pruefer-Lauf, Wochenlimit)
- scripts/workshop/check_haut.py (29/29 PASS, Ergebnis renders/components/haut_paneel/check.txt): Felderzahl (Euler), Typen, Dicke 8, Flaeche gegen Heron-Rechnung, Randkanten, Randabstand 0 (Inkreisradius), Auflage 15 mm auf der Kappe, Masse
- Bild renders/components/haut_paneel/haut_paneel_AAB-01-draufsicht.png (und BBB); kein Bild-Kritiker, kein Spec-Pruefer (Wochenlimit, W19 Auftrag)

## Offene Fragen

- Tuer (D36): nur das Basisfeld BBB 149,2 traegt den Tuerausschnitt (haut_paneel_BBB_tuer.sc); Zargenlage in der Feldebene Annahme A (siehe tuer_komplett)
- Hohlkammern, Dichtband, Klemmleisten, Lueftungsklappen nicht modelliert; Material/Preis/UV nicht recherchiert (R11 offen)
- Paneele sind eben; die Streben liegen auf der Kugel, die Felder sind plan (Pfeilhoehe zur Kugel (Umkreis des Feldes gegen R 6000) ca. 0,34 m (AAB) bzw. 0,40 m (BBB)): Aussenflaeche haengt an den Streben, Einbau durch die Montage
- Plattenlage: Inkreismittelpunkt des Strebendreiecks (Strebenachsen), nicht Schwerpunkt; Z 0 = Innenseite
- edge_inset 0 (D37): Paneel bis zur Strebenachse, Kappe klemmt; Auflage 15 mm je Seite = cap_w/2 (haut_profil.json) - edge_inset, check_haut prueft die Auflage; Klemmung/Schrauben nicht modelliert
- Zustaendigkeit (D37): der Tuerausschnitt bleibt beim Paneel T40 (haut_paneel.py liest nur das Zargenmass aus tuer_komplett.json)
