# Bauteilblatt T109 notluftpumpe (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/notluftpumpe.json` und `designs/components/notluftpumpe.sc`, nicht von Hand aendern)

**Funktion:** Haelt die Fische bei Ausfall der Wasserpumpen (und damit der Venturi-Belueffter) oder des Netzes am Leben: startet ueber die Steuerung am Notstrom (Batteriespeicher), blaest Luft ueber einen Luftstein in den Fischtank. Die Luftleitung steigt ueber den hoechsten Wasserspiegel (Rand 1200) und faellt dann zum Stein, ein Rueckschlagventil sitzt am Pumpenausgang: so laeuft kein Wasser in die Pumpe zurueck (Designprinzip 9). Pumpenzahl und Luftmenge offen wie in der Quelle (A24); Richtwert 55 l/min nach R55 (deckt rund 24 bis 49 Prozent des Spitzenbedarfs von 71 g O2/h, kein Ersatz fuer das Gebläse im Dauerbetrieb).

**Datei:** `designs/components/notluftpumpe.sc` · **Teilenummer:** T109 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche der Pumpe in X und Y, Z 0 = Standflaeche (Fussboden); Schlauch +X ueber den Rand (Z 1300) und senkrecht hinab; Luftstein bei Z -980 (Boden Fischtank -1000)

**Anzahl (Instanzen):** 1 (Notluftpumpe fuer den Fischtank) (Quelle: data/oasis-soll.json luftpumpe (anzahl 1))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `pumpe_l` | 330 | mm | [Q] Kerry Electronics KEA3600 (60 l/min, 35 W, 230 V), Hornbach-Seite am 10.11.2026 gelesen (Beschaffungslauf U2): L x B x H 33 x 23 x 32 cm; Kandidat, Fabrikat nicht entschieden |
| `pumpe_b` | 230 | mm | [Q] dieselbe Seite: Breite 23 cm |
| `pumpe_h` | 320 | mm | [Q] dieselbe Seite: Hoehe 32 cm (Standflaeche Z 0) |
| `tuelle_d` | 12 | mm | [A] Ausgangstuelle der Pumpe fuer Luftschlauch 9/12 |
| `tuelle_l` | 30 | mm | [A] Laenge der Tuelle ausserhalb des Gehaeuses |
| `tuelle_z` | 120 | mm | [A] Hoehe der Tuelle ueber der Standflaeche |
| `rv_d` | 18 | mm | [A] Rueckschlagventil Luft (Kunststoff), Aussen 18 |
| `rv_l` | 45 | mm | [A] Baulaenge Rueckschlagventil |
| `schlauch_d` | 12 | mm | [A] Luftschlauch 9/12 (Aussen 12) |
| `schleife_x` | 380 | mm | [A] Abstand der Steigleitung von der Pumpe (x) |
| `schleife_z` | 1300 | mm | [E] Rand des Fischtanks 1200 (data/oasis-soll.json fish) plus 100 mm: Luftleitung ueber dem hoechsten Wasserspiegel (Siphonbrecher, kein Wasser in die Pumpe) |
| `tank_x` | 760 | mm | [A] Abstand der Fallleitung in den Fischtank (x), die Schleife quert den Rand |
| `stein_d` | 40 | mm | [A] Luftstein Ø 40 (poroeses Sintermaterial) |
| `stein_l` | 100 | mm | [A] Luftstein 100 lang, steht senkrecht |
| `stein_ueber_boden` | 20 | mm | [A] Abstand des Luftsteins zum Boden des Fischtanks -1000 |
| `luft_l_min` | 55 |  | [A] Richtwert Notluft 55 l/min (R55 Tabelle), Quelle laesst Leistung und Luftmenge offen (A24) |

Gesamt-Box (Messung): X -165.0 bis 780.0, Y -115.0 bis 115.0, Z -980.0 bis 1306.0 mm; Koerper: 8.

**Toleranzen / Spiel:** Schlauch als ein Koerper (Knicke als Gehrung); Stein beruehrt den Schlauch (Stoss). Boden des Fischtanks und Rand liegen im Bauteil bei Z -1000 und Z 1200.

## Werkstoff und Gewicht

- Werkstoff: PS/PA (Pumpengehaeuse), PVC-P (Schlauch), PE (Luftstein), PP (Tuelle, Ventil), Dichte 1.05 g/cm3, Farbe #777777 ([A] Platzhalter; Werkstoffe je Fabrikat. Wasserkontakt hat nur der Luftstein (D85: Nachweis offen))
- Volumen (Messung, `solidcraft-cli eval`): 24866.9 cm3 · Masse leer: 26189 g (26.19 kg)

## Querschnitt / Profil

Gehaeuse 330 x 230 x 320; Ausgangstuelle Ø 12 x 30 auf Z 120; Rueckschlagventil Ø 18 x 45; Luftschlauch Ø 12 als ein Koerper (Steigleitung bei x 380 bis Z 1300, waagerecht bis x 760, Fallleitung bis Z -880); Luftstein Ø 40 x 100 senkrecht (Z -980 bis -880).

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Strom (Steuerung) | Netz oder 12 V je Fabrikat | am Gehaeuse (nicht modelliert) | an die Steuerung am Notstrom |
| Luftstein | Ø 40 x 100 | x 760, y 0, z -980 bis -880 | steht auf dem Boden des Fischtanks (20 mm Abstand) |

## Verbindungen und Befestigungen

- Schlauch auf die Tuelle stecken und mit Schelle sichern
- Rueckschlagventil zwischen Tuelle und Schlauch
- Schlauch an der Fischtank-Wand fixieren (Klammern), Luftstein beschweren oder an den Schlauch binden

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Luftschlauch ueber dem hoechsten Wasserspiegel | Schleife bei Z 1300 | Q/E | Quelle luftpumpe_1.t3 'Luftleitung ueber dem hoechsten Wasserspiegel mit Rueckschlagventil'; Rand 1200 + 100 | mittel |
| Luftstein am Boden des Fischtanks | Z -980 bis -880 | Q | data/oasis-soll.json fish boden_ueber_fussboden_mm -1000; luftpumpe.t2 'Luftleitung zum Fischtank mit Luftstein' | hoch |
| Pumpe 60 l/min (Kandidat Kerry KEA3600) | Gehaeuse 330 x 230 x 320 | Q/A | Maße: Hornbach-Seite (Q, 10.11.2026); Luftmenge 60 l/min passt zum R55-Richtwert 55 l/min; Quelle laesst Leistung offen (A24); 230 V, Notstrom nur ueber Wechselrichter (12-V-Pumpe mit 60 l/min nicht gefunden) | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (luftpumpe: Notluftpumpe, Luftleitung zum Fischtank mit Luftstein, startet bei Ausfall A24; fish: Boden -1000, Rand 1200, Wsp 750); docs/research/R55-wasserquelle-venturi.md (Notluft 55 l/min Eintrag als Richtwert); docs/decisions.md D103
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Pumpe auf festem Platz im Dom aufstellen (trocken, ueber der Wasserlinie des Sumpfs)
2. Schlauch ueber den Rand des Fischtanks legen (Schleife ueber Z 1300) und zum Luftstein hinabfuehren
3. Luftstein auf den Boden stellen, Steuerung auf Notstrombetrieb pruefen

**Werkzeug:** Schlauchschelle, Seitenschneider, Kabelbinder

## Renders

- `renders/components/notluftpumpe/notluftpumpe-01-seite.png`
- `renders/components/notluftpumpe/notluftpumpe-02-pumpe.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_notluftpumpe.py

## Offene Fragen

- Pumpenfabrikat, Leistung und Luftmenge (Quelle A24 offen; 55 l/min ist Richtwert R55); Bezug Europa je Haendler siehe data/beschaffung/
- Lebensmitteleignung des Luftsteins (Wasserkontakt, D85) ohne Herstellernachweis; Rueckfall: Edelstahl- oder Keramikausstroemer
- Notstrom: der Kandidat Kerry KEA3600 laeuft mit 230 V (35 W); eine 12-V-Pumpe mit 60 l/min wurde nicht gefunden (Beschaffungslauf), Notbetrieb daher ueber Wechselrichter am Batteriespeicher oder 12-V-Pumpe mit weniger Luft (Oase AquaOxy 1000, rund 17 l/min); Auslegung des Batteriespeichers und Umschaltung gehoeren zur Steuerung
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: PMP-luftpumpe-notluft: Hornbach (Marktplatz-Verkaeufer AGABA) (DE), Konfidenz Q; Lebensmittel: nicht anwendbar (Luftseite, kein Wasserkontakt); Rueckfall: Notstrom 12 V: Oase AquaOxy 1000 (12 V DC, 15 W, 1000 l/h) mehrfach parallel [Q-Treffer, https://www.kaufland.de/product/61996491/], zusamme | ARM-luftstein-notluft: toom Baumarkt (DE), Konfidenz Q; Lebensmittel: offen (kein Herstellernachweis gefunden), Rueckfall: Hobby/Hailea nach Material und Konformitaet fragen; Aquaristik-Luftsteine sind fuer Fischwasser vorgesehen, das ist aber kein D85-Beleg; Rueckfall: Oase/FIAP Teichbelueftungs-Sets mit Ausstroemern (Conrad AT, FIAP Air active) als Kandidat [Q-Treffer, https://www.conrad.at/de/p/fiap-2951- | ARM-rueckschlagventil-luft: Kaufland (DE), Konfidenz Q-Treffer; Lebensmittel: nicht anwendbar (Luftseite); Rueckfall: Tameson-Seite 'Rueckschlagventile fuer Aquarien' als Quelle fuer Bauform [Q-Treffer, https://tameson.de/pages/ruckschlagventile-aquarien].
