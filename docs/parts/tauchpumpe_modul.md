# Bauteilblatt T110 tauchpumpe_modul (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/tauchpumpe_modul.json` und `designs/components/tauchpumpe_modul.sc`, nicht von Hand aendern)

**Funktion:** Hebt Wasser von unten nach oben: Pumpstelle 1 saugt im Fischtank und hebt 1,15 m (Wsp 750 zu Vortex 1900), Pumpstelle 2 saugt im Sumpf und hebt 1,00 m (Wsp -250 zu 750) durch den Venturi-Belueffter in den Fischtank. Das Rueckschlagventil in der Druckleitung haelt die Leitung bei Stillstand gefuellt (A14). Typ bleibt Kandidat (R59/D92). Die Rechnung der Foerderleistung im Check zeigt: Pumpstelle 1 trifft 110 l/min nur nach den optimistischen Kennlinienformen, Pumpstelle 2 mit Venturi nicht; Nachweis offen.

**Datei:** `designs/components/tauchpumpe_modul.sc` · **Teilenummer:** T110 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche (Unterkante Ansaugkorb) in X und Y, Z 0 = Boden des Beckens; Druckleitung d50 senkrecht nach oben (Port bei Z 389), Kabel +X

**Anzahl (Instanzen):** 4 (2 Pumpstelle 1 im Fischtank, 2 Pumpstelle 2 im Sumpf) (Quelle: docs/decisions.md D102; data/oasis-soll.json filterpumpe_1/_2, hauptpumpe_1/_2)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `geh_l` | 340 | mm | [Q] oase-teichbau.de/oase-aquamax-eco-premium-8000 (Seite am 10.11.2026 gelesen, Beschaffungslauf): Masse L x B x H 340 x 280 x 165 mm, Ansaugbereich eingeschlossen; die Zeichnung der Quelle zeigt die Pumpe als Kreis Ø 275 (Lage-Probe U1) |
| `geh_b` | 280 | mm | [Q] dieselbe Seite: Breite 280 mm |
| `geh_h` | 165 | mm | [Q] dieselbe Seite: Hoehe 165 mm (Standflaeche Z 0 bis Gehaeuse-Oberkante) |
| `stutzen_l` | 70 | mm | [A] Druckstutzen Ø 50 (Schlauchtuelle auf Klebeadapter) 70 hoch, 31 mm davon im Rueckschlagventil |
| `rv_d` | 63 | mm | [A] Rueckschlagventil PVC-U d50 (Klappe oder Kugel), Gehaeuse Ø 63 x 110 |
| `rv_l` | 110 | mm | [A] Baulaenge Rueckschlagventil mit Muffe d50 oben und unten |
| `kabel_d` | 9 | mm | [A] Netzkabel Ø 9 |
| `kabel_l` | 400 | mm | [A] Kabelstueck im Modell (Ausschnitt) |
| `qmax_l_min` | 133.3 |  | [E] 8000 l/h aus R59 (Herstellerangabe Eco Premium 8000) |
| `hmax_m` | 4.1 |  | [A] R59: 4,1 m, Zuordnung der Hmax-Spalte im Handbuch unsicher |
| `tiefe_max_mm` | 4000 | mm | [Q] R59: wasserdicht bis 4 m (Handbuch der Baureihe) |

Gesamt-Box (Messung): X -170.0 bis 570.5, Y -140.0 bis 140.0, Z 0.0 bis 314.0 mm; Koerper: 4.

**Toleranzen / Spiel:** Platzhalterkoerper; Pumpeninneres nicht modelliert; Stutzen steckt 31 mm im Ventil (Beruehrung).

## Werkstoff und Gewicht

- Werkstoff: Kunststoffgehaeuse (Pumpe), PP (Korb, Stutzen), PVC-U (Rueckschlagventil), Dichte 1.5 g/cm3, Farbe #3a5f9a ([A] Platzhalterkoerper; Gehaeusewerkstoff und Lebensmittelnachweis der Teichpumpe nicht belegt (R59, D85))
- Volumen (Messung, `solidcraft-cli eval`): 16042.2 cm3 · Masse leer: 23957 g (23.96 kg)

## Querschnitt / Profil

Gehaeuse 340 x 280 x 165 (Z 0 bis 165, Maße laut Hersteller-Shop); Druckstutzen Ø 50 x 70 (Z 165 bis 235); Rueckschlagventil Ø 63 x 110 mit Muffe d50 unten (nimmt den Stutzen) und oben (Z 204 bis 314); Kabel Ø 9 x 400 seitlich bei Z 80.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Druckleitung (Muffe d50) | PVC-U d50, Tiefe 31 | x 0, y 0, z 314 | Oeffnung zeigt +Z; Rohr d50 nach oben (D106) |
| Strom | Netzkabel Ø 9 | x 170 bis 570, z 80 | an die Steuerung (nicht modelliert) |

## Verbindungen und Befestigungen

- Druckleitung d50 in die Muffe oben kleben
- Pumpe steht auf Sockel oder Boden, Kabel zum Schaltschrank

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Eco Premium 8000 als Kandidat | Körper Ø 230 x 190, Korb Ø 275 | A | R59 Empfehlung (bedingt); Kennlinie nur aus Qmax/Hmax gerechnet, Nachweis offen | niedrig |
| Rueckschlagventil in der Druckleitung | d50 PVC-U | Q | A14, filterpumpe_1.t3 und hauptpumpe_1.t2 | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (filterpumpe_1: Rueckschlagventil in der Druckleitung A14; hauptpumpe_1; Zeichnung Pumpe Radius 137,5 mm); docs/research/R59-tauchpumpe.md (Eco Premium 8000: 8000 l/h, Hmax 4,1 m [A], 65 W, Eintauchtiefe 4 m); docs/decisions.md D92, D102, D106
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Pumpe auf den Boden (Fischtank) oder den Pumpensockel (Sumpf) stellen
2. Rueckschlagventil in die Druckleitung d50, Rohr nach oben fuehren
3. Kabel ueber den Rand zum Schaltschrank; Probelauf mit Pegelkontrolle

**Werkzeug:** Rohrschneider, PVC-Kleber

## Renders

- `renders/components/tauchpumpe_modul/tauchpumpe_modul-01-schraeg.png`
- `renders/components/tauchpumpe_modul/tauchpumpe_modul-02-schnitt.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_tauchpumpe_modul.py

## Offene Fragen

- Foerderleistung: Kennlinie nur aus Qmax/Hmax gerechnet (R59), Herstellerkennlinie und zweite Quelle fehlen; Pumpstelle 2 mit Venturi nach der Rechnung nicht belegt
- Lebensmittel- und Fischvertraeglichkeit der Teichpumpe (D85) nicht belegt; Rueckfall Aquaforte EC-10000 (R59)
- Handelssituation: der Hersteller-Shop (oase-teichbau.de, 10.11.2026) fuehrt den Eco Premium 8000 als nicht lieferbar und verweist auf den Eco Premium 9000, dessen Daten nicht gelesen sind; Eintauchtiefe 4 m steht nur im Handbuch der Baureihe (R59), Leistung auf der Seite widerspruechlich (65 W gegen 15 bis 60 W)
- Anzahl und Leistung wie in der Quelle offen (A3)
- Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: PMP-tauchpumpe-oase-8000: oase-teichbau.de (Oase Shop) (DE), Konfidenz Q; Lebensmittel: offen (kein Herstellernachweis gefunden), Rueckfall: Oase-Support nach Werkstoffliste und Konformitaet (EU 1935/2004, KTW) fragen; Pumpe ist bei Oase ausgelaufen, also Nachfolger 9000 mit Datenblatt und Nachweis pruefen; Rueckfall: Oase AquaMax Eco Premium 9000 (Nachfolger laut oase-teichbau.de [Q], Daten ungelesen) oder Aquaforte EC-10000 (129 EUR Hornbach DE, R59 Ruec | ARM-rueckschlagventil-d50: toom Baumarkt (mediPOOL) (DE), Konfidenz Q; Lebensmittel: offen (kein Herstellernachweis KTW/UBA gelesen), Rueckfall: FIP/MCM VR oder Georg Fischer 561 mit Herstellerzertifikat anfragen; Rueckfall: MCM-Systeme/FIP PVC-U Schraegsitz-Rueckschlagventil [Q-Treffer, https://mcm-systeme.de/mediafiles/PDF/FIP/vr_pvc-u_schraegsitz-rueckschlagve
