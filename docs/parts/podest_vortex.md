# Bauteilblatt T102 podest_vortex (erzeugt von `scripts/workshop/partsheet.py` aus `data/components/podest_vortex.json` und `designs/components/podest_vortex.sc`, nicht von Hand aendern)

**Funktion:** Hebt tank_klein (Vortex 1 und 2) um 577 mm, damit der Ueberlauf auf dem Soll-Wasserspiegel 1900 liegt und das Wasser danach per Schwerkraft weiterlaeuft (Designprinzip 1). Reiner Stahlrahmen aus Normprofil, kein eigener Kreislaufteil.

**Datei:** `designs/components/podest_vortex.sc` · **Teilenummer:** T102 · **Revision:** A · **Bezugspunkt:** Mitte der Standflaeche in X und Y, Z 0 = Boden (Fussplatten-Unterkante); Auflage fuer tank_klein auf Z = podest_vortex_h (Oberkante Kopfrahmen)

**Anzahl (Instanzen):** Vortex 1 und 2: je 1 Podest je Tank (Quelle: data/oasis-soll.json (vortex_1/_2, bio_1/_2); D100)

## Masse und Parameter

| Parameter | Wert | Einheit | Herkunft |
|---|---|---|---|
| `podest_vortex_h` | 577 | mm | [E] Soll-Wasserspiegel Vortex 1900 (data/oasis-soll.json vortex_1) minus Tankoberkante 1323 (tank_klein, R61 Abschnitt 6 Nr. 3) = 577; mindestens, D100; U4/U5 setzen den Wert aus data/oasis-lage.json |
| `span` | 720 | mm | [A] Aussenmass des Rahmens = Plattform 619 + 2 x 50 mm Ueberstand (Annahme Lage-Probe U1, Paket Abschnitt Grenzen), auf 720 gerundet |

Gesamt-Box (Messung): X -390.0 bis 390.0, Y -390.0 bis 390.0, Z 0.0 bis 577.0 mm; Koerper: 24.

**Toleranzen / Spiel:** Rahmenstuecke stossen auf Stoss an die Stuetzen (Beruehrung, keine Durchdringung); Hoehe ueber den Parameter einstellbar.

## Werkstoff und Gewicht

- Werkstoff: Stahl, feuerverzinkt (Vierkantrohr 40 x 40 x 3, Blech 6 mm), Dichte 7.85 g/cm3, Farbe #b8bcc2 ([A] Normprofil aus dem Katalog (vierkantrohr_40x40x3), Selbstbau durch Schweissen oder Verschrauben (Designprinzip 7: Podeste sind Selbstbau))
- Volumen (Messung, `solidcraft-cli eval`): 12566.4 cm3 · Masse leer: 98646 g (98.65 kg)

## Querschnitt / Profil

Vierkantrohr 40 x 40 x 3; Fussplatten 100 x 100 x 6; Stuetzen von Z 6 bis 577; Fussrahmen (Z 6 bis 46) und Kopfrahmen (Z 537 bis 577) zwischen den Stuetzen; 8 Knotenbleche 6 x 100 x 100 aussen an den X-Seiten.

## Ports (Anschluesse)

| Name | DN / Mass | Lage (Bauteil-KS) | Richtung |
|---|---|---|---|
| Auflage Tank | tank_klein Plattform 619 x 619 | Z = 577 | Tank steht mittig auf dem Kopfrahmen |

## Verbindungen und Befestigungen

- Rahmen verschweisst oder verschraubt (Normprofil, Selbstbau)
- Fussplatten mit Fussbodenankern (Loecher im Modell nicht gebohrt)
- Tank mit Tankplattform auf dem Kopfrahmen verschraubt

## Herkunft (docs/provenance.md)

| Merkmal | Wert | Herkunft | Bezug (Datei, Ausschnitt) | Konfidenz |
|---|---|---|---|---|
| Hoehe 577 mm | Parameter podest_vortex_h | E | [E] Soll-Wasserspiegel Vortex 1900 (data/oasis-soll.json vortex_1) minus Tankoberkante 1323 (tank_klein, R61 Abschnitt 6 Nr. 3) = 577; mindestens, D100 | mittel |
| Standflaeche 720 x 720 | tank_klein Plattform 619 + Ueberstand | A | data/components/tank.json plat_l; Ueberstand 50 mm aus der Lage-Probe U1 | niedrig |
| Vierkantrohr 40 x 40 x 3 | Stuetzen und Rahmen | A | data/katalog.json vierkantrohr_40x40x3; Tragfaehigkeit gerechnet im Check, Statik N-STATIK offen | mittel |

## Referenz und Abweichung zum OBJ

- Referenzbild: kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json
- Quelle der Masse: data/oasis-soll.json (Vortex 1 und 2: Wasserspiegel 1900 ueber Fussboden); docs/research/R61-oasis-wasserkreislauf.md Abschnitt 4 (O2, O10) und 6 Nr. 3; docs/decisions.md D100; data/components/tank.json (plat_l 619)
- Abweichung zum OBJ: Kein OBJ-Bestand (Bauteil ist neu nach der Quelle).

## Montage (L4)

1. Fussplatten setzen, Stuetzen und Fussrahmen verschweissen/verschrauben, Kopfrahmen aufsetzen und ausrichten
2. Knotenbleche anschweissen, Rahmen auf Fussboden dueblen
3. tank_klein aufsetzen und mit dem Kopfrahmen verbinden

**Werkzeug:** Winkelschleifer, Schweissgeraet oder Schrauben M8, Wasserwaage

## Renders

- `renders/components/podest_vortex/podest_vortex-01-schraeg.png`
- `renders/components/podest_vortex/podest_vortex-02-seite.png`

## Pruefung

- Gauntlet-Urteil: offen (Pruefer P-Pruef)
- python -X utf8 scripts/workshop/check_podest_vortex.py

## Offene Fragen

- Statik (Kippsicherheit, Horizontallast, Fussbodenanker) ist Sache von N-STATIK; der Check rechnet nur Stuetzendruck und Knicken
- Verzinkung und Werkstoff-Lebensmittelnachweis nicht noetig (kein Wasserkontakt)
