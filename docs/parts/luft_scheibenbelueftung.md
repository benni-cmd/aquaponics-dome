# Bauteilblatt T88 luft_scheibenbelueftung (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/luft_scheibenbelueftung.json` und `designs/components/luft_scheibenbelueftung.sc`, nicht von Hand aendern)

**Funktion:** Gibt die Luft des Pool-Verteilers als feine Blasen ins Pool-Wasser ab: EPDM-Membran auf einem Tragteller, darunter ein Stuetzfuss mit Anschlussstutzen d25 nach unten. Vier Stueck im Pool, je einer an einem Abgang des Pool-Verteilers (K44). Parameter d (Standard 270) und pipe_d bilden die Luftstein-Variante fuer das Drittbecken (K49, d20) ohne eigenes Bauteil ab. Gilt in jeder Kreislaufvariante (E20)

**Datei:** `designs/components/luft_scheibenbelueftung.sc` · **Teilenummer:** T88 · **Revision:** A · **Bezugspunkt:** Port A (Ende des Anschlussstutzens, Mitte) im Ursprung; Oeffnung zeigt -Z (nach unten), Stutzen, Stuetzfuss, Tragteller und Membran stehen auf der Achse +Z

**Anzahl (Instanzen):** 4 Stueck im Pool (Pool-Verteiler 4-fach); 1 Luftstein-Variante im Drittbecken (K49) als Parameter (Quelle: Auftrag W37-3 Teil 3; Netz K44, K49)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `d` | 270 | mm | [A] Membran-Ø Handelsmass 215 bis 270 (Auftrag W37-3); Standard 270 (R53: JetFlex HD 270, Disque diffuseur 270) |
| `pipe_d` | 25 | mm | [A] Anschlussstutzen d25 (Pool-Verteiler d25, Auftrag W37-3); Variante Drittbecken K49: 20 |
| `stutzen_l` | 40 | mm | [A] Anschlussstutzen Laenge: Rohr steckt in die Muffe der Zuleitung (Tiefe 19) |
| `fuss_h` | 50 | mm | [A] Stuetzfuss: Hoehe von der Stutzenoberkante bis zum Tragteller |
| `teller_h` | 20 | mm | [A] Tragteller PP |
| `teller_rand` | 20 | mm | [A] Tragteller Ø = d minus 20 (Membranrand liegt ueber) |
| `membran_h` | 6 | mm | [A] EPDM-Membran, nicht geschlitzt modelliert (Schlitze nicht modelliert) |
| `luft_bohrung` | 16 | mm | [A] Luftkanal Ø 16 durch Stutzen und Stuetzfuss (Kanal im Tragteller nicht modelliert) |

Gesamt-Box (Messung): X -135.0 bis 135.0, Y -135.0 bis 135.0, Z 0.0 bis 116.0 mm; Koerper: 4.

**Toleranzen / Spiel:** Handelsmass-Platzhalter; Membran-Schlitze, Kanaele im Tragteller und Gewinde nicht modelliert; Stuetzfuss steht auf der Rohrleitung (Zuleitung kommt von unten, Bogen unter dem Fuss: Montage).

## Werkstoff und Gewicht

- Werkstoff: PP (Stutzen, Stuetzfuss, Tragteller), EPDM (Membran), Dichte 0.91 g/cm3, Farbe #e8e5d8 ([A] Handelsteil, Werkstoff nach Katalog offen)
- Volumen (Messung, `solidcraft-cli eval`): 1519.2 cm3 · Masse leer: 1465 g (1.46 kg)
- Gefuellt/in Betrieb: Luft fuehrend; EPDM-Membran schwimmt nicht, der Fuss muss beschwert werden (Montage)

## Querschnitt / Profil

Anschlussstutzen d25 x 40 mit Luftkanal Ø 16, Stuetzfuss Ø 70 x 50 mit Luftkanal Ø 16 (Kanal im Tragteller nicht modelliert), Tragteller Ø 250 x 20, EPDM-Membran Ø 270 x 6 (nicht geschlitzt modelliert); Gesamthoehe 116.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| A Luft-Anschluss (Zapfen) | PVC-U d25 (DN20), Zapfen, Aussen-Ø 25, Luftkanal Ø 16 | x 0, y 0, z 0 (Mitte der Stirnflaeche) | Oeffnung zeigt -Z (nach unten); Rohr d25 vom Pool-Verteiler wird aufgesteckt oder als Muffe ueber den Zapfen geklebt |

## Verbindungen und Befestigungen

- Port A: Rohr d25 vom Abgang des Pool-Verteilers (luftverteiler_4)
- Fuss auf dem Beckenboden: Befestigung (Gewicht, Auftrieb) nicht modelliert (Montage)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Membran-Ø 270 | 270 (Parameter d, 215 bis 270) | A | Auftrag W37-3 Teil 3; R53 (JetFlex HD 270, Disque diffuseur 270) [Q-Treffer] | niedrig |
| Anschluss d25 nach unten | Zapfen Ø 25, Kanal Ø 16 | A | Auftrag W37-3 Teil 3 (d25 senkrecht nach unten) | mittel |
| Stuetzfuss, Tragteller, Membran-Dicke | Ø 70 x 50, Ø 250 x 20, 6 mm | A | Annahme, Handelsmass nicht gelesen | niedrig |
| Luftstein-Variante Drittbecken | d 100, pipe_d 20 | A | Netz K49 (d20, 2 l/min) | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: reference/ref-6-grow-tables-detail.jpg
- Quelle der Masse: docs/research/R45-hydraulik-auslegung.md Abschnitt 4; docs/research/R53-europa-frischwasser-luft.md (Jaeger JetFlex HD 270 [Q-Treffer], Disque diffuseur 270 EPDM Ref. DD-0270-EPDM-HCS [Q]); data/leitungsnetz.json K44, K49
- Abweichung zum OBJ: Kein OBJ-Bestand.

## Montage (L4)

1. Scheibe auf dem Beckenboden am vorgesehenen Platz absetzen (Abstand der vier Scheiben mindestens 270 mm; Verteilung im Pool Montage)
2. Rohr d25 vom Abgang des Pool-Verteilers an Port A anschliessen
3. Luft einschalten, Blasenbild pruefen; Fuss gegen Auftrieb beschweren

**Werkzeug:** Rohrschneider, Klebstoff PVC

## Stueckliste-Zeile

- 4 Scheibenbelueftungsteile EPDM 270 mit Anschluss d25 (Pool); 1 Luftstein klein (Variante d 100, pipe_d 20) im Drittbecken (K49)
- 4 Beschwerungen oder Halter (Montage)

## Teileliste mit Bezug in Europa (D76)

Marke: [Q] Seite/Ausschnitt gelesen (nur Katalogzeile, Preise nicht geprueft), [R51] aus R51 uebernommen, [A] Annahme. Artikel vor der Bestellung gegen Mass und PN pruefen.

| Teil | Mass | Europaeische Quelle (Hersteller/Haendler, Artikel) | Status |
|---|---|---|---|
| Scheibenbelueftung 270 EPDM, Anschluss 3/4 Zoll bzw. d25 (Klebe/Gewinde) | Membran Ø 270 | Jaeger JetFlex HD 270 (DE) [Q-Treffer R53]; Disque diffuseur 270 EPDM, Ref. DD-0270-EPDM-HCS (FR) [Q R53]; Datenblatt Jaeger nicht lesbar | beschaffbar (schwach): zwei Herkuenfte, je eine Quelle; Datenblatt und Anschluss ungeprueft |

## Alternative lokale Fertigung

Handelsteil (Teichbelueftung, EPDM-Scheibe 215 bis 270 mm).

## Renders

- `renders/components/luft_scheibenbelueftung/luft_scheibenbelueftung-01-schraeg.png`
- `renders/components/luft_scheibenbelueftung/luft_scheibenbelueftung-02-schnitt.png`

## Pruefung

- Gauntlet-Urteil: Pruefer-Lauf: PASS, Befund in docs/jobs/pruefung/W37-2-W37-3.md.
- scripts/workshop/check_luft_verteiler.py luft_scheibenbelueftung (Ergebnis renders/components/luft_scheibenbelueftung/check.txt): vier Koerper, Stutzen-, Fuss-, Teller- und Membran-Maße, Stapelhoehe 116, Port A, Volumen Membran und Stutzen gegen Rechnung, Interferenz 0

## Offene Fragen

- Hersteller-Maß und Kennlinie (Druckverlust, Luftmenge je Scheibe) OFFEN, Katalog N-BESCHAFFUNG (W47)
- Biofilter-Rohr- und Plattenbelueftungsteile: nur Platzhalter-Hinweis (Menge nach Traegerhersteller, K1), nicht modelliert
- Anschluss d25 vs. 3/4 Zoll Gewinde der Handelsscheibe: Uebergang offen
