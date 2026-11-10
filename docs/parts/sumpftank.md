# Bauteilblatt T101 sumpftank (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/sumpftank.json` und `designs/components/sumpftank.sc`, nicht von Hand aendern)

**Funktion:** Sammelt die Ruecklaeufe der Linie (NFT und Flood-and-Drain der Anbauringe Aussen und Mitte, Ring-Ende, Notueberlauf Biofilter) durch Schwerkraft und haelt 850 l Soll-Inhalt (Pegel -250). Die Pumpe am Sumpf (tauchpumpe_modul auf dem Pumpensockel) hebt von hier 1,00 m in den Fischtank. Vier Pufferzonen am Ende (1 aufwaerts Kalk, 2 abwaerts Aktivkohle, 3 aufwaerts frei, 4 abwaerts frei) werden ueber den Pegelhub durchstroemt. Der Schwimmerschalter bei -110 meldet Hochstand. Die Grube liegt im Boden mit begehbarem Deckel und hat keinen Bodenablauf (Designprinzip 2: gepumpt wird von oben). Nach der Quelle A26 liegt der Boden des Fischtanks (-1000) tiefer als der Boden des Sumpfs (-500).

**Datei:** `designs/components/sumpftank.sc` · **Teilenummer:** T101 · **Revision:** A · **Bezugspunkt:** Mitte der Grube in X und Y; Z 0 = Fussboden (Deckel-Oberkante, Rand); Boden -500, Soll-Pegel -250, Hochstand -110 (Hoehen wie in der Quelle, Modell-Z = 400 + Z); Pufferzonen am +Y-Ende

**Anzahl (Instanzen):** 2 (Sumpftank 1 und 2, je eine Linie) (Quelle: data/oasis-soll.json sump_1, sump_2 (anzahl 2))

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `pit_w` | 1125 | mm | [Q] Quelle A22 / R61 Abschnitt 5: 90 Einheiten x 12,5 mm (Innenmass der Grube, Breite X) |
| `pit_l` | 2975 | mm | [Q] Quelle A22 / R61 Abschnitt 5: 238 Einheiten x 12,5 mm (Innenmass, Laenge Y; enthaelt die vier Pufferzonen) |
| `pit_d` | 500 | mm | [Q] data/oasis-soll.json sump_1: Boden -500 mm bis Rand 0 (Fussboden) |
| `liner_t` | 2 | mm | [A] EPDM-Teichfolie 1,5 bis 2 mm als fischvertraeglicher Belag der Betonwanne (Lebensmittelnachweis offen, Blatt Abschnitt Offene Fragen) |
| `wall_t` | 100 | mm | [A] Betonwanne, Wand und Boden je 100 mm (Statik und Erddruck offen, N-STATIK) |
| `deckel_t` | 40 | mm | [A] Gitterrost 30/10 verzinkt, 40 mm hoch; Oberkante des Deckels = Fussboden Z 0 (Quelle A18: Deckel auf Fussbodenhoehe) |
| `deckel_w` | 1229 | mm | [A] Deckelbreite = Wanne innen 1129 + 2 x 50 mm Auflage auf der Wannenwand |
| `deckel_seg` | 1026 | mm | [A] drei Platten je 1026 mm in Y (3 x 1026 = 3078 = Wanne innen 2979 + 2 x 49,5 mm Auflage); je Platte rund 35 kg als Gitterrost, einzeln abhebbar (Designprinzip 8); im Modell Vollplatte (396 kg), Masse im Modell daher zu hoch |
| `zone_l` | 212 | mm | [Q] Quelle A31 / D105: vier Pufferzonen zu je 17 Einheiten = 212,5 mm, auf 212 mm gerundet |
| `zone_n` | 4 |  | [Q] Quelle A31: vier Pufferzonen zu je 10 % der alten Laenge (Kalk, Aktivkohle, frei, frei) |
| `trenn_t` | 10 | mm | [A] Trennwand PP 10 mm (zaehlt nicht zur Zonenbreite 212; geht von der Hauptkammer ab) |
| `trenn_oeff` | 80 | mm | [A] Durchstroemoeffnung am Boden unter den Wanden 1 und 3 (Zone 1 aufwaerts, Zone 3 aufwaerts) |
| `trenn_oben` | -60 | mm | [A] Oberkante der bodenoffenen Trennwande (ueber dem Hochstand -110, unter dem Deckel -40) |
| `wehr_oben` | -290 | mm | [A] Oberkante der Ueberlaufwehre (Wand 2 und 4): 40 mm unter dem Soll-Pegel -250, dort faellt das Wasser in Zone 2 und Zone 4 abwaerts |
| `wsp` | -250 | mm | [Q] data/oasis-soll.json sump_1 wsp_ueber_fussboden_mm -250 (Soll-Pegel, 850 l) |
| `hochstand` | -110 | mm | [Q] data/oasis-soll.json sump_1 hochstand_ueber_fussboden_mm -110 (Schaltpunkt Schwimmerschalter, A20) |
| `sockel_s` | 400 | mm | [A] Pumpensockel PP 400 x 400 x 30 fuer tauchpumpe_modul (Pumpe Ø 230, Sockel gibt Standflaeche und Abstand zum Schlamm) |
| `sockel_h` | 30 | mm | [A] Sockelhoehe |
| `sockel_x` | 200 | mm | [A] Lage Pumpenplatz in der Hauptkammer (x) |
| `sockel_y` | -700 | mm | [A] Lage Pumpenplatz in der Hauptkammer (y) |
| `tuelle_d` | 32 | mm | [A] Schlauchtuelle ID25 (Aussen 32 mm, Bohrung 25 mm), D106: Sumpf-Zulaeufe Schlauch ID25 |
| `tuelle_id` | 25 | mm | [Q] D106: Zulauf-Schlauch ID25 |
| `tuelle_z` | -75 | mm | [A] Achse der Zulaufe oben: ueber dem Hochstand -110, unter dem Deckel -40 (freier Auslauf ueber dem Wasser) |
| `tuelle_l` | 142 | mm | [A] Tuelle von aussen durch Wand und Folie bis 40 mm in die Grube |
| `halter_z` | -80 | mm | [A] Mitte der Schwimmerhalter-Aufnahme (Z -120 bis -40, unter dem Deckel); sie umfasst den Hochstand -110 und die Kabelklemme des schwimmerschalter_hochstand (Z -75 bis -45) |
| `halter_y` | -444 | mm | [A] Lage der Aufnahme in der Hauptkammer (Mitte) |

Gesamt-Box (Messung): X -664.5 bis 664.5, Y -1589.5 bis 1589.5, Z -602.0 bis 2.0 mm; Koerper: 19.

**Toleranzen / Spiel:** Wasserkoerper 1125 x 2975 bis -250 abzueglich Trennwand, Wehre und Sockel: 823 l (Soll 850 l, -3,1 Prozent). Trennwaende und Folie ohne Spiel (Beruehrung, keine Durchdringung).

## Werkstoff und Gewicht

- Werkstoff: Beton C25 (Wanne), EPDM (Belag), PP (Trennwaende), Stahl verzinkt (Gitterrost), Dichte 2.4 g/cm3, Farbe #9a9a96 ([A] Selbstbau der Grube (Designprinzip 7: nur Sumpf-Grube und Podeste); Werkstoffe je Teil in data/parts/sumpftank.json)
- Volumen (Messung, `solidcraft-cli eval`): 1003877.3 cm3 · Masse leer (ohne Wasser): 3188620 g (3188.62 kg)
- Gefuellt/in Betrieb: Wasser bis Soll-Pegel 823 l = 823 kg zusaetzlich; Deckel im Modell Vollplatte (396 kg je Platte, real Gitterrost rund 35 kg), daher Modellmasse zu hoch

## Querschnitt / Profil

Betonwanne aussen 1329 x 3179, Wand und Boden 100, Oberkante -40; EPDM-Folie 2 mm innen (lichte Grube 1125 x 2975, Boden -500); Hauptkammer 2087 mm lang mit Pumpensockel und Zulaeufen, dann vier Trennwaende PP 10 mm und vier Zonen zu 212 mm; Wand 1 und 3 bodenoffen 80 mm (Strom aufwaerts), Wand 2 und 4 als Ueberlaufwehr bis -290 (Strom abwaerts); Deckel 3 Gitterrost-Platten 1229 x 1026 x 40, Oberkante 0.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Zulauf 1 bis 3 (Schlauchtuelle ID25) | PP-Tuelle Aussen 32, Bohrung 25, D106 | x -664,5 bis -522,5, y -1100 / -700 / -300, z -75 | waagerecht von der -X-Wand in die Grube; Schlauch ID25 aus Fallleitung oder Ruecklauf, freier Auslauf ueber dem Hochstand |
| Pumpenplatz (tauchpumpe_modul) | Sockel 400 x 400 x 30 | x 200, y -700, z -500 bis -470 | Pumpe steht auf dem Sockel; Druckleitung d50 nach oben durch eine Deckelfuge |
| Aufnahme Schwimmerschalter | Halter PP 60 x 40 x 80 | x 532,5, y -444, z -120 bis -40 | Klemmpunkt des Schwimmerschalters auf dem Hochstand -110 |

## Verbindungen und Befestigungen

- Betonwanne in die Grube setzen, Wanne innen mit EPDM-Folie auskleiden und an der Oberkante fassen
- Trennwaende PP stehen lose zwischen den Folienflanken (Nuten oder Winkelleisten, im Modell Beruehrung)
- Deckelplatten liegen lose auf den Wannenwaenden (50 mm Auflage), mit Sicherung gegen Abheben (Designprinzip 9)
- Zulauftuellen durch Bohrungen von Wand und Folie, Dichtung mit Wanddurchfuehrung (im Modell Passsitz)

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Grube 1125 x 2975 x 500 | Innenmasse | Q | A22, R61 Abschnitt 5: 1125 x 2975 mm = 3,35 m2, 1680 l bei 0,50 m | hoch |
| Soll-Pegel -250 mm | Wasserkoerper bis -250 | Q | data/oasis-soll.json sump_1; Modell 823 l statt 850 l (Platz der Trennwaende und des Sockels) | hoch |
| Pufferzonen 4 x 212 mm | Zonen am +Y-Ende | Q/A | A31, D105; Fluss auf und ab (1 auf, 2 ab, 3 auf, 4 ab) als Annahme D112: passiver Austausch ueber Pegelhub | mittel |
| Betonwanne 100 mm, EPDM-Belag | Wanne 1329 x 3179 | A | Selbstbau der Grube; Wandstaerken Annahme, Statik N-STATIK | niedrig |
| Deckel Gitterrost 40 mm, 3 Platten | Oberkante Z 0 | A | A18: Deckel auf Fussbodenhoehe, begehbar; Tragklasse offen | niedrig |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (Bauteil sump_1: boden -500, rand 0, wsp -250, hochstand -110, 1680 l bei 0,50 m, Quelle A22, A31); docs/research/R61-oasis-wasserkreislauf.md Abschnitt 2 Nr. 6 und Abschnitt 5 Nr. 1 (Sumpf 90 x 238 Einheiten x 12,5 mm = 1125 x 2975 mm); docs/decisions.md D105 (Pufferzonen 17 Einheiten = 212 mm), D106 (Zulaeufe Schlauch ID25)
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Grube ausheben (Innenmass 1129 x 2979 plus Wandstaerken, Tiefe 602 mm unter Fussboden), Sauberkeitsschicht und Betonwanne setzen
2. Folie einlegen und an der Oberkante fassen, Trennwaende und Pumpensockel stellen, Schwimmerhalter an die +X-Seite montieren
3. Zulauftuellen einsetzen, Deckelplatten auflegen und sichern, Zonenschilder anbringen (1 Kalk, 2 Aktivkohle, 3 frei, 4 frei)

**Werkzeug:** Bagger oder Spaten, Wasserwaage, Betonmischer oder Fertigteil, Lochsaege 32 mm

## Renders

- `renders/components/sumpftank/sumpftank-01-schraeg.png`
- `renders/components/sumpftank/sumpftank-02-laengsschnitt.png`
- `renders/components/sumpftank/sumpftank-03-zonen.png`
- `renders/components/sumpftank/sumpftank-04-querschnitt.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_sumpftank.py (Messwerte siehe Paket n-unify-autobahn Abschnitt U2)

## Offene Fragen

- Pufferzonen-Durchstroemung: Quelle nennt nur Auf-und-ab-Fluss und Fuellung als Einstellung; Modell setzt passiven Austausch ueber den Pegelhub (ANNAHME D112), ein Zwangsstrom durch die Zonen ist nicht belegt
- Betonwanne und EPDM-Folie: Lebensmittel- und Fischvertraeglichkeit je Hersteller offen (D85); Rueckfall: PE-Erdtank als Fertigteil
- Deckel: Tragklasse des Gitterrosts (begehbar) und Sicherung gegen Abheben offen; Statik N-STATIK
- Wasserdruck bei hohem Grundwasser (Auftrieb der leeren Wanne) nicht gerechnet
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: MAT-epdm-teichfolie: Teichbedarf24 (TeichVision EPDM Pro 1,5 mm) (DE), Konfidenz Q-Treffer; Lebensmittel: offen (kein Herstellernachweis zu Fisch/Trinkwasser gefunden), Rueckfall: Datenblatt der Teichfolie & Teichfilter TM GmbH als Text lesen und Fisch-/Trinkwasserangabe oder WRc-/KTW-Pruefung beim Hersteller erfragen; Rueckfall: Oase EPDM-Folie 'fisch- und pflanzenvertraeglich nach WRc' (Oase-Katalog 2017, https://www.oase-livingwater.com/fileadmin/pageflip/61146_PK_ | MAT-gitterrost-deckel: kein Angebot in Europa gefunden; Lebensmittel: nicht verlangt/offen (Zinkueberzug am Wasser nicht belegt), Rueckfall: Gitterrost nur als Abdeckung ueber Wasser, nicht eintauchend, oder Edelstahl-/GFK-Rost; Rueckfall: Seppeler Pressroste Lager (Hersteller, Lagerprogramm) [Q-Treffer, https://www.seppeler.de/fileadmin/user_upload/Gitterroste/Gitterroste/Lage
