# Bauteilblatt T87 luftverteiler_4 (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/luftverteiler_4.json` und `designs/components/luftverteiler_4.sc`, nicht von Hand aendern)

**Funktion:** Pool-Verteiler am Becken: nimmt die Pool-Luft (K44, Planwert 130 l/min, Spitze 205) in einer Muffe d40 auf und gibt sie ueber vier Zapfen d25 (je 33 l/min) an vier Scheibenbelueftungsteile weiter. Formstueck-Verteiler nach dem Muster lt_verteiler_d50 (W36). Gilt in jeder Kreislaufvariante (E20)

**Datei:** `designs/components/luftverteiler_4.sc` · **Teilenummer:** T87 · **Revision:** A · **Bezugspunkt:** Port A (Mitte der Muffenoeffnung d40, Einlauf) im Ursprung; Sammlerachse +X (Muffe oeffnet nach -X), Abgaenge zeigen nach +Z (Zapfen-Ende 74 ueber der Achse), Ende B bei X = Laenge geschlossen

**Anzahl (Instanzen):** 1 Pool-Verteiler am Becken (Quelle: R45 Abschnitt 4 Empfehlung 4 und 5; Netz Version 3)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `pipe_d` | 40 | mm | [E] Netz K44: Hauptleitung d40 (R45 Abschnitt 4: d40 bei 200 l/min 3,2 m/s, Innen-Ø 36,2) |
| `pitch` | 120 | mm | [A] Teilung wie lt_verteiler_d50 (Kugelhahn-Gehaeuse d25 = 43,25 plus Hebel; Ventil d40 = 60 mm) |
| `x0` | 75 | mm | [A] erster Abgang: Muffe A d40 (Tiefe 26) plus Abgangsbohrung d40 (Radius 18,1) plus Steg |
| `end_cap` | 10 | mm | [A] integrierte Endkappe (Wand) am Ende B wie lt_verteiler_d50 |

Gesamt-Box (Messung): X -0.0 bis 470.0, Y -24.0 bis 24.0, Z -24.0 bis 74.0 mm; Koerper: 1.

**Toleranzen / Spiel:** Kein Abgang hat den Durchmesser des Sammlers; keine Kernel-Korrektur noetig.

## Werkstoff und Gewicht

- Werkstoff: PVC-U (Formstueck, Sammler und Zapfen aus einem Koerper), Dichte 1.4 g/cm3, Farbe #3d6f9e ([A] wie lt_verteiler_d50 (W36))
- Volumen (Messung, `solidcraft-cli eval`): 389.3 cm3 · Masse leer: 545 g (0.55 kg)
- Gefuellt/in Betrieb: Luft fuehrend, keine Fuellmasse; Masse leer siehe Messung

## Querschnitt / Profil

Sammler Aussen 48 (Formstueck d40: 40 + 2 x 4), Innen-Ø 36.2 (Wand 1,9), Muffe A d40 Tiefe 26; Zapfen Aussen-Ø = d (Pool-Abgang 39,75), Zapfenende 74 ueber der Achse; Teilung 120, Laenge 470, Ende B mit 10 mm Endkappe geschlossen.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| A Einlauf (Muffe) | PVC-U d40 (DN32), Klebemuffe, Einstecktiefe 26 | x 0, y 0, z 0 (Mitte der Oeffnung) | Oeffnung zeigt -X; Rohr d40 vom Hauptverteiler (K44, Pool-Leitung) |
| Abgang 1 Scheibe 1 (K44 (Teil)) | PVC-U d25 (DN20), Zapfen, Aussen-Ø 25, Bohrung 21.4 | x 75, y 0, z 74 | zeigt +Z; Rohr oder Ventil wird aufgeklebt (Zapfen steckt in die Muffe) |
| Abgang 2 Scheibe 2 (K44 (Teil)) | PVC-U d25 (DN20), Zapfen, Aussen-Ø 25, Bohrung 21.4 | x 195, y 0, z 74 | zeigt +Z; Rohr oder Ventil wird aufgeklebt (Zapfen steckt in die Muffe) |
| Abgang 3 Scheibe 3 (K44 (Teil)) | PVC-U d25 (DN20), Zapfen, Aussen-Ø 25, Bohrung 21.4 | x 315, y 0, z 74 | zeigt +Z; Rohr oder Ventil wird aufgeklebt (Zapfen steckt in die Muffe) |
| Abgang 4 Scheibe 4 (K44 (Teil)) | PVC-U d25 (DN20), Zapfen, Aussen-Ø 25, Bohrung 21.4 | x 435, y 0, z 74 | zeigt +Z; Rohr oder Ventil wird aufgeklebt (Zapfen steckt in die Muffe) |

## Verbindungen und Befestigungen

- Strom Abgang 1: 33 l/min im Innen-Ø 21.4 = 1.53 m/s [E]
- Strom Abgang 2: 33 l/min im Innen-Ø 21.4 = 1.53 m/s [E]
- Strom Abgang 3: 33 l/min im Innen-Ø 21.4 = 1.53 m/s [E]
- Strom Abgang 4: 33 l/min im Innen-Ø 21.4 = 1.53 m/s [E]
- Summe der Abgangsstroeme 4 x 33 = 132 l/min gegen Planwert 130 l/min (Abweichung 1.5 Prozent, unter 2 Prozent) [E]
- Sammler Innen-Ø 36.2: 130 l/min = 2.11 m/s; Spitze 205 l/min = 3.32 m/s (R45: d40 bei 200 l/min 3,2 m/s)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Hauptleitung d40 / Sammler | d40, Innen-Ø 36,2 | E | Netz K44 (R45 Abschnitt 4): d40 bei 200 l/min 3,2 m/s | hoch |
| Abgaenge | 4 Zapfen: d25 (K44 (Teil)), d25 (K44 (Teil)), d25 (K44 (Teil)), d25 (K44 (Teil)) | A | Netz K44 bis K51 (Hauptverteiler); Pool-Verteiler 4 Abgaenge d25 aus dem Auftrag W37-3 [A] | mittel |
| Teilung 120, Zapfenueberstand 50, Endkappe 10 | wie lt_verteiler_d50 | A | docs/parts/leitungsteile.md Verteiler d50 (W36) | mittel |
| Strom je Abgang | 4 x 33 = 132 l/min | E/A | R45 Abschnitt 4; Netz K49 2 l/min; Zweitbecken 5 [A] | mittel |
| Handelsteile (T, Reduzierung, Hahn, Rueckschlagventil) | Europa-Teileliste im Blatt | Q-Treffer | R52, R53, Auftrag W37-3 Europa-Teileliste | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R45-hydraulik-auslegung.md Abschnitt 4 (Zeilen 225 bis 279); data/leitungsnetz.json Version 3 K44 bis K51 (nur gelesen); docs/parts/leitungsteile.md Verteiler d50 (W36); scripts/workshop/leitung.py (od_f, wall_p, DEPTH)
- Abweichung zum OBJ: Kein OBJ-Bestand (Luftverteiler fehlte, L06).

## Montage (L4)

1. Pool-Verteiler am Beckenrand befestigen (Befestigung Montage); Rohr d40 (K44) in Muffe A kleben
2. Jeden Abgang d25 mit einem Rohr zu je einem Scheibenbelueftungsteil verbinden; die Scheiben (Ø 270) brauchen mehr Abstand als die Teilung 120: die Rohre fuehren auseinander
3. Luft einschalten und das Blasenbild kontrollieren

**Werkzeug:** Rohrschneider, Klebstoff PVC, Entgrater

## Stueckliste-Zeile

- Sammler d40 aus Handelsteilen (L21): 4 T-Stuecke 40x25x40, Rohrstuecke d40 zwischen den T-Stuecken, 1 Endkappe d40
- Je Abgang ein Rohr d25 zu einem Scheibenbelueftungsteil (luft_scheibenbelueftung, 4 Stueck); Einzelabsperrung je Scheibe nicht im Auftrag (Montage/Planer)

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| T-Stueck 40x25x40 (4 Stueck), Reduzierung 40x25 | PVC-U Klebemuffen (Teilung 120, T-Stueck 40 ist 100 lang) | Bevo Profec (NL); schwarte-shop (DE); Weinmann-Schanz (DE) Art. 93 049 64 Reduktion 40 x 25 [Q-Treffer R52, Seite beim Abruf 404]; Vanmarcke GF 40 x 25 (BE) [Q R52] | beschaffbar (zwei Quellen fuer 40 x 25 nach R52); 40 x 20 nur ueber Reduzierungen aus der Bibliothek, Artikel offen |
| Endkappe d40 | PVC-U Klebekappe | Katalog offen, N-BESCHAFFUNG (W47); W39 baute nur Kappen d20 und d50 | offen |

## Alternative lokale Fertigung

Handelsteile (T-Stuecke, Reduzierungen, Kappe) aus dem Katalog; Eigenbau aus Rohr d40 mit Anbohrung und aufgeschweissten Abgaengen nur als Notloesung.

## Renders

- `renders/components/luftverteiler_4/luftverteiler_4-01-schraeg.png`
- `renders/components/luftverteiler_4/luftverteiler_4-02-oben.png`
- `renders/components/luftverteiler_4/luftverteiler_4-03-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Kein Pruefer-Lauf (Auftrag W37-3: Selbstcheck; gebuendelter Pruefer W37-2/W37-3 folgt).
- scripts/workshop/check_luft_verteiler.py luftverteiler_4 (Ergebnis renders/components/luftverteiler_4/check.txt): Koerper, Aussen-Ø, Laenge, Muffe A, Abgaenge (Zahl, Ø, Bohrung, Port-Stirnflaechen) und Strom je Abgang, Summe 132 gegen 130, Geschwindigkeit im Sammler, Interferenz 0

## Offene Fragen

- Menge je Scheibe 33 l/min ist Annahme (130 geteilt durch 4); Kennlinie der Scheibe (Druckverlust, Blasenbild) OFFEN
- Befestigung am Beckenrand und Wegfuehrung der vier Rohre: Montage
- Einzelabsperrung je Scheibe: nicht im Auftrag
- Rueckschlagventil im Zulauf: bei Pumpenstillstand sperrt das Ventil der Geblaese-Baugruppe (Schleife ueber dem Spiegel); Luft nicht freigegeben (Seite nennt Wasser, PN16), Oeffnungsdruck bei 130 l/min ungeprueft
