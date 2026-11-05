# Bauteilblatt T93 schlammfass (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/schlammfass.json` und `designs/components/schlammfass.sc`, nicht von Hand aendern)

**Funktion:** Nimmt den Schlamm auf, den der Absetzer alle 2 bis 3 Tage ueber den Federrueckzug-Kugelhahn und K07/K23 ablaesst (20 bis 40 l je Spuelung). Der Schlamm setzt sich ab; einmal pro Woche wird Klarwasser abgehoben (zurueck in den Pool) und Dickschlamm zum Wurmkompost gebracht. Kein Reaktor, kein Auslass.

**Datei:** `designs/components/schlammfass.sc` · **Teilenummer:** T93 · **Revision:** A · **Bezugspunkt:** Mitte Fassboden aussen (Z 0), Z hoch; Luftbohrung +X, Entlueftung -X. Einbau: Fassboden flur-relativ -880 auf 70 mm Sandbett (Grubensohle -950), Fassoberkante Flur 0

**Anzahl (Instanzen):** 2 (je Linie: schlammfass_1, schlammfass_2) (Quelle: data/leitungsnetz.json Knoten schlammfass_1/2; Standort 0,7-0,8 m neben dem Kegelspitzen-Hahn setzt die Montage (M10 S5))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `fass_d` | 580 | mm | [A] docs/research/R45-hydraulik-auslegung.md Abschnitt 0: Spannringfass PE 200-220 l, Oe 0,58-0,60 m (Handelsmass, nicht gegengeprueft) |
| `fass_h` | 880 | mm | [A] docs/research/R45-hydraulik-auslegung.md Abschnitt 0: H 0,88-0,92 m inklusive Deckel |
| `fass_wall` | 4 | mm | [A] Wandstaerke PE-Fass (kein Datenblatt gelesen) |
| `fass_floor` | 5 | mm | [A] |
| `deckel_t` | 15 | mm | [A] Deckel mit Spannring |
| `ring_b` | 10 | mm | [A] Spannring radial |
| `ring_h` | 35 | mm | [A] Spannring hoch |
| `stutzen_d` | 40 | mm | [E] docs/research/R45-hydraulik-auslegung.md Abschnitt 0: Deckel mit Stutzen d40 Mitte; K07/K23 d40 (Netz V3) |
| `luft_d` | 8 | mm | [E] docs/research/R45-hydraulik-auslegung.md Abschnitt 0: Bohrung Oe 8 fuer Luftschlauch (Luftstein optional, Frage 4) |
| `luft_x` | 150 | mm | [A] Lage Luftbohrung |
| `entl_d` | 20 | mm | [E] docs/research/R45-hydraulik-auslegung.md Abschnitt 0: Entlueftung Oe 20 |
| `entl_x` | -150 | mm | [A] Lage Entlueftung |
| `grube_d` | 800 | mm | [E] docs/research/R45-hydraulik-auslegung.md Abschnitt 0 Bauteil-Skizze: Grube Oe 0,8 m (baut die Montage) |
| `grube_t` | 950 | mm | [E] docs/research/R45-hydraulik-auslegung.md Abschnitt 0: Tiefe etwa 0,95 m; Fassoberkante etwa Flur 0 bis +20 bei 70 mm Sandbett |

Gesamt-Box (Messung): X -300.0 bis 300.0, Y -300.0 bis 300.0, Z -0.0 bis 920.0 mm; Koerper: 5.

**Toleranzen / Spiel:** Grube Oe 800 laesst 100 mm Ringspalt um das Fass (Verfuellung); Fassoberkante Flur 0, Stutzen-Muffe bis Flur +40.

## Werkstoff und Gewicht

- Werkstoff: PE (Fass, Deckel), Stahl verzinkt (Spannring), PVC-U (Stutzen), Dichte 0.95 g/cm3, Farbe #2a4f8f ([A])
- Volumen (Messung, `solidcraft-cli eval`): 12165.6 cm3 · Masse leer: 16054 g (16.05 kg)
- Gefuellt/in Betrieb: Bis 105 l Schlammwasser ca. 105 kg, voll ca. 220 kg [E, Dichte 1]; Entleerung von Hand (Heber/Tauchpumpe, Eimer)

## Querschnitt / Profil

Fass Oe 580 x 865 (Wand 4, Boden 5) mit Deckel Oe 580 x 15 und Spannring 600 x 35; Einlaufstutzen d40 (Muffe) in der Deckelmitte, Bohrung Oe 8 bei x +150, Entlueftungsstutzen Oe 20 bei x -150.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Einlauf Schlamm (K07 Linie 1 / K23 Linie 2, vom Federrueckzug-Kugelhahn des Absetzers) | Muffe d40, Mitte Deckel | x 0, y 0, z 920 | +Z |
| Luftschlauch (optional Luftstein) | Bohrung Oe 8 im Deckel | x 150, y 0, z 880 | +Z |
| Entlueftung | Stutzen Oe 20 innen | x -150, y 0, z 900 | +Z |

## Verbindungen und Befestigungen

- Deckel mit Spannring (Schnellverschluss) auf dem Fass; Dichtung nicht modelliert [A]
- Einlaufstutzen d40 in den Deckel eingeklebt oder per Tankverbinder [A]; K07/K23 steckt mit dem Fallrohr in die Muffe

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Fass 220 l, Oe 580 x 880 | Oe 580 x 880 | Annahme (Handelsmass) | docs/research/R45-hydraulik-auslegung.md Abschnitt 0 Bauteil-Skizze (Oe 0,58-0,60, H 0,88-0,92); nicht gegengeprueft | mittel |
| Fassung 105 l/Woche plus Reserve | 220 l nominal | gerechnet | docs/research/R45-hydraulik-auslegung.md Abschnitt 0 Zahlen: 70-105 l je Linie und Woche (Spanne 47-140) | mittel |
| Stutzen d40 Mitte Deckel | d40 | belegt (Netz) / gerechnet | data/leitungsnetz.json V3 K07/K23 dn 40; R45 Einlauf | hoch |
| Luftbohrung Oe 8, Entlueftung Oe 20 | Oe 8 / Oe 20 | gerechnet (R45-Skizze) | docs/research/R45-hydraulik-auslegung.md Abschnitt 0 Entlueftung/Luft | mittel |
| Grube Oe 800, Tiefe 950 | 800 / 950 | gerechnet (R45-Skizze) | docs/research/R45-hydraulik-auslegung.md Abschnitt 0 Bauteil-Skizze; Kollision mit eingegrabenen Rohren prueft die Montage (Frage 0 Nr. 5) | mittel |
| Wand 4, Boden 5, Deckel 15, Spannring 10 x 35 | mm | Annahme | kein Datenblatt gelesen | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R45-hydraulik-auslegung.md Abschnitt 0 (Bauteil-Skizze, Zahlen), data/leitungsnetz.json Version 3 (K07/K23, Knoten schlammfass_1/2)
- Abweichung zum OBJ: Keine OBJ-Vorgabe; Bauteil nach R45 Abschnitt 0 (Bauteil-Skizze).

## Montage (L4)

1. Grube Oe 0,8 m, Tiefe 0,95 m neben dem Absetzer (0,7-0,8 m Mitte zu Mitte vom Kegelspitzen-Hahn), Sandbett 70 mm
2. Fass einsetzen, Oberkante auf Flur 0 ausrichten, Ringspalt verfuellen
3. Deckel mit Stutzen aufsetzen, Spannring schliessen; K07/K23 (d40, 5 % Gefaelle, Bogen 90, Fallrohr 0,1 m) in die Muffe stecken

**Werkzeug:** Spaten, Wasserwaage, Lochsaege, PVC-Kleber

## Stueckliste-Zeile

- T93 Schlammfass je Linie: 1 Spannringfass PE 220 l mit Deckel und Spannring, 1 Einlaufstutzen d40 (Tankverbinder oder Klebemuffe), 1 Entlueftungsstutzen Oe 20; Federrueckzug-Kugelhahn d40 am Absetzer siehe lt_kugelhahn_feder_d40

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Spannringfass PE 220 l | Oe 580 x 880 | offen (Fasshandel in DE/EU) | offen [A] |
| Tankverbinder/Stutzen d40 | Klebemuffe | offen (N-BESCHAFFUNG) | offen [A] |

## Alternative lokale Fertigung

Gebrauchtes Lebensmittel-Spannringfass (gereinigt) aus dem regionalen Fasshandel.

## Renders

- `renders/components/schlammfass/schlammfass-01-schraeg.png`
- `renders/components/schlammfass/schlammfass-02-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Pruefpunkte fuer den Pruefer im Blatt W37-1).
- scripts/workshop/check_schlammfass.py (Ergebnis renders/components/schlammfass/check.txt): Fassmass, Volumen 200-220 l (+-5 %) aus Oe und H und aus dem Modell, Stutzen d40 Mitte Deckel, Bohrungen, Ports, Gruben-Parameter, Interferenz 0

## Offene Fragen

- Fassfabrikat und Mass im Handel nicht gegengeprueft [A]
- Kollision der Grube mit eingegrabenen Rohren: Montage mit check_leitungen.py (R45 Frage 0 Nr. 5)
- Luftstein/Luftmenge optional, Menge offen (R45 Frage 4)
- Schlammkonzentration im Betrieb messen (R45 Frage 0 Nr. 1)
- M10-S2V (Subtank, GEPARKT) beruehrt die Schlammfuehrung; bei Freigabe pruefen
