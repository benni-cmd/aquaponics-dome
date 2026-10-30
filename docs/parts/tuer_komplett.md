# Bauteilblatt T50 tuer_komplett (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/tuer_komplett.json` und `designs/components/tuer_komplett.sc`, nicht von Hand aendern)

**Funktion:** Eingang der Kuppel: rechteckige Zarge aus Rohr 30 x 30 x 2 (Schwelle, 2 Pfosten, Sturz) in der Ebene des Basisfeldes BBB 149,2 (D36) mit Normtuerblatt 1000 x 2000 x 40, nach aussen oeffnend, 3 Aufschraubbaendern, Druecker, Anschlag und Dichtung.

**Datei:** `designs/components/tuer_komplett.sc` · **Teilenummer:** T50 · **Revision:** B · **Bezugspunkt:** Feld-KS: Ursprung Mitte der Basiskante (Knoten 24 -> 22) auf Z 0 = Basisknotenhoehe, X tangential (24 -> 22), Y hangaufwaerts in der Feldebene zur Spitze (Knoten 6), Z Feldnormale nach aussen; Zarge liegt in der Feldebene (um ca. 10,8 Grad zur Senkrechten geneigt)

**Anzahl (Instanzen):** 1 (Feld BBB 149,2) (Quelle: docs/decisions.md D36)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `blatt_w` | 1000 | mm | [A] Normtuer 1000 x 2000 (docs/components.md, Auftrag W20) |
| `blatt_h` | 2000 | mm | [A] Normtuer 1000 x 2000 |
| `blatt_t` | 40 | mm | [A] Tuerblatt 40 mm (Auftrag W20) |
| `spiel` | 8 | mm | [A] Spiel Blatt zu Zarge je Seite und oben (Normtuer-Praxis 5-10 mm) |
| `rohr` | 30 | mm | [A] Zarge aus Rechteckrohr 30 x 30 x 2 wie die Streben (Auftrag W20 Schritt 2) |
| `rohr_wand` | 2 | mm | [A] Wandstaerke Zargenrohr 2 mm |
| `schwelle_h` | 30 | mm | [A] Schwelle = Rohr 30 x 30 (ebenerdig, Blatt liegt auf der Schwelle auf, R13 Befund 8: kein Mass belegt) |

Gesamt-Box (Messung): X -549.0 bis 538.0, Y -0.0 bis 2068.0, Z -55.0 bis 73.0 mm; Koerper: 26.

**Toleranzen / Spiel:** Spiel Blatt zu Zarge 8 mm je Seite, oben 6, unten 2 (gemessen); Zarge passt ins Feld: Feldbreite in Sturzhoehe 1320 mm gegen Zarge 1076, Reserve 122 mm je Seite (>= 100).

## Werkstoff und Gewicht

- Werkstoff: Stahl verzinkt (Zarge, Beschlaege), Tuerblatt Sandwich, EPDM (Dichtung), Dichte 7.85 g/cm3, Farbe #aeb4b8 ([A] Zarge Rechteckrohr 30 x 30 x 2 verzinkt; Tuerblatt Sandwich 0,31 g/cm3 (ca. 25 kg fuer 1 x 2 x 0,04 m, Normtuer-Richtwert, nicht recherchiert); EPDM 1,1 g/cm3)
- Volumen (Messung, `solidcraft-cli eval`): 81790.0 cm3 · Masse leer: 38651 g (38.65 kg)

## Querschnitt / Profil

Zarge Aussenbreite 1076 x Hoehe 2068 (in der Feldebene gemessen, Neigung der Feldebene 10.8 Grad zur Senkrechten, senkrechte Hoehe 2031), Lichte 1016 x 2008; Blatt 1000 x 2000 x 40 mit Spiel 8 seitlich / 6 oben / 2 unten; Anschlag Flachstahl 14 x 3 innen, Dichtung EPDM 6 x 1; Beschlaege: 3 Aufschraubbaender links (Lasche 48 x 90 x 4, Bolzen D10), Druecker rechts auf 1 m (Rosette D50, Hebel 130).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Anschluss Sturz links / rechts an die schraege Strebe (Knoten 24-6 / 22-6) | Flachstahl-Lasche 30 x 4, Schrauben M6 [A, nicht modelliert] | Sturzende x +-538, y' 2053, z' 0; Strebenachse bei x +-669 (Luecke 131 mm je Seite) | Sturz liegt in der Feldebene, Strebe verlaeuft schraeg nach oben; die Lasche ueberbrueckt die Luecke |
| Anschluss Pfosten / Schwelle an den Boden | Ankerplatten 70 x 70 x 5 mit M8 [A, nicht modelliert] | Schwellenenden x +-538, y' 0..30 | Zarge steht auf dem Fundament/Boden; Tuer ist hoch beanspruchte Zone (R13: zusaetzliche Bodenverankerung) |
| Basisstrebe zwischen den Pfosten entfaellt | Strebe 3708 (Knoten 24-22) | Basiskante y' 0, x +-1854; verbleibende Reststrecke je Seite 1316 mm | die Schwelle ersetzt die Basisstrebe zwischen den Pfosten (R13); im Dom entfaellt die Strebe (Montage) |
| Tuerausschnitt im Paneel BBB | haut_paneel_BBB_tuer.sc | Rechteck 1076 x 2068 ab der Basiskante, mittig | Paneel liegt aussen an der Zarge; Ausschnitt = Zarge-Aussenmass |

## Verbindungen und Befestigungen

- Zarge geschweisst (MAG) und verzinkt [A]; Anschluss an die Streben ueber Laschen mit M6 (nicht modelliert)
- Aufschraubbaender: Zargenlasche auf dem linken Pfosten, Blattlasche auf dem Blatt, Bolzen D10 dazwischen; Schrauben der Baender nicht modelliert
- Anschlag Flachstahl 14 x 3 innen auf Pfosten und Sturz geklebt/genietet [A], Dichtung EPDM darauf

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Tuer mittig im Basisfeld BBB 149,2 | Azimut 149,2 | OBJ + E | D36: Spitze Z 3140, 1353 mm breit in 2 m (R13); Feld aus layout.json dome.nodes_list (Knoten 24, 22, 6) | mittel |
| Normtuer 1000 x 2000 x 40 | 1000 x 2000 x 40 | OBJ + A | docs/components.md Tuer 1000 x 2000 (OBJ-Normtuer), Dicke 40 Annahme | mittel |
| Zarge Rohr 30 x 30 x 2, Schwelle 30 | 30 x 30 x 2 | A | Auftrag W20 (Rohr wie die Streben); R13 Befund 8: kein belastbares Mass fuer Sturz/Schwelle | niedrig |
| Spiel 8 seitlich, 6 oben, 2 unten | 8 / 6 / 2 mm | A | Normtuer-Praxis 5-10 mm | niedrig |
| Zarge in der Feldebene, Neigung 10,8 Grad | 10.8 Grad | E | aus den Knoten 24, 22, 6 (layout.json); R13 Befund 2: die Tuer steht nicht senkrecht | mittel |
| Blatt oeffnet nach aussen, Anschlag innen | nach aussen | A | R13 Befund 7 (Shelter Dome: oeffnet nach aussen) | niedrig |
| 3 Aufschraubbaender, Druecker auf 1 m, Dichtung EPDM | 3 + 1 + 1 | A | Standard-Tuerbeschlag; Beschlagmasse Annahme | niedrig |
| Tuerblatt 0,31 g/cm3 (25 kg) | 0,31 g/cm3 | A | Sandwich-Tuerblatt 1 x 2 x 0,04 m ca. 25 kg (Richtwert, nicht recherchiert) | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R13.md, docs/decisions.md D36, data/layout.json dome.nodes_list (Knoten 24, 22, 6), data/components/haut_paneel.json felder
- Abweichung zum OBJ: keine OBJ-Vorgabe fuer die Tuer ausser Normmass 1000 x 2000 und Azimut 167 (OBJ); D36 legt die Tuer mittig in das Basisfeld BBB 149,2 (Azimut 149,2) statt auf den Basisknoten 22.

## Montage (L4)

1. Zarge in die Feldebene stellen (Schwelle am Boden, Pfosten parallel zu den Hangkanten ausrichten), Sturz-Laschen an die schraegen Streben schrauben, Basisstrebe zwischen den Pfosten entfernen
2. Anschlag und Dichtung innen setzen, Blatt mit den 3 Baendern einhaengen (oeffnet nach aussen), Druecker montieren
3. Paneel BBB_tuer auflegen (Ausschnitt an der Zarge), Seitenfelder neben der Tuer sind Teil des Paneels

**Werkzeug:** Schweissgeraet, Akkuschrauber, Wasserwaage, Bohrmaschine

## Stueckliste-Zeile

- T50 Tuer komplett: Zarge Rohr 30 x 30 x 2 (Schwelle 1076, 2 Pfosten 2008, Sturz 1076) 10.3 kg; Tuerblatt 1000 x 2000 x 40 24.8 kg; 3 Aufschraubbaender; Druecker (Rosette D50 + Hebel) innen/aussen; Anschlag 3 Leisten; Dichtung EPDM 3 Streifen; gesamt 38.7 kg (1 Stueck)

## Alternative lokale Fertigung

Normtuer 1000 x 2000 (Stahl-/Holzsandwich) ist Baumarktware; Zarge selbst geschweisst oder aus Systemprofil; Beschlaege Standard [A, nicht recherchiert].

## Renders

- `renders/components/tuer_komplett/tuer_komplett-01-zarge.png`

## Pruefung

- Gauntlet-Urteil: offen (kein Pruefer-Lauf, Auftrag W20)
- scripts/workshop/check_tuer.py (25/25 PASS, Ergebnis renders/components/tuer_komplett/check.txt): Lichte, Spiel, Zarge im Feld (Reserve), Neigung und Feldtyp aus den Knoten, Beschlaege, Interferenz 0, Paneelausschnitt gegen numerische Rechnung
- Bilder renders/components/tuer_komplett/ und renders/components/haut_paneel/haut_paneel_BBB_tuer-01-draufsicht.png; kein Spec-Pruefer, kein Bild-Kritiker (Auftrag W20)

## Offene Fragen

- Zarge in der Feldebene (Neigung 10,8 Grad) ist Annahme A (R13 nennt auch rechteckigen senkrechten Rahmen mit verlaengerten Streben); senkrechter Rahmen braucht Tiefe bis 603 mm am Oberkante, Entscheidung Orchestrator/Ben
- Anschlag-Laschen an die Streben, Bodenanker, Schrauben der Baender, Schloss/Schliessblech nicht modelliert; Statik (Schnee/Wind auf Sturz, R13 Befund 8) nicht gerechnet
- Oeffnungsrichtung nach aussen (Shelter Dome, R13) und Windfang offen (Ben: wohin soll die Tuer)
- Platzhalter designs/components/tuer.sc (Integrator, alter Stand) ist durch tuer_komplett.sc zu ersetzen (Montage)
- Zweites Becken muss auf die Tuerachse 149,2 gedreht werden (D36, Montage)
