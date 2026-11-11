# Bauteilblatt Ring B2: Pegelschacht T94, Ringstuetze d75 T95, Entluefter d75 T96, Ring-Abzweig d40/d32 T97

Auftrag: `docs/jobs/N-VARIANTEN.md` Abschnitt 4, Schritt V2 (Werkstatt Bauteile). Generator `scripts/workshop/ring_b2.py`, Pruefung `scripts/workshop/check_ring_b2.py`, Daten `data/components/ring_b2_teile.json`, Teiledaten `data/parts/<komp>.json` (aus `scripts/workshop/parts_ring_b2.py`). Bilder `renders/components/ring_b2/<komp>.png`.
Booster = vorhandenes Bauteil `pumpe_gross` (Blatt 2.2), kein neues Teil. [Q] Quelle im Repo · [E] eigene Rechnung/Messung · [A] Annahme.

**Mini-Plan.** Problem: Ring B2 braucht vier Bauteile, die es nicht gibt. Intent: R1/R2 koennen den Ring montieren, ohne in der Montage Teile zu erfinden. Goal: je Bauteil `.sc` mit Port-Tabelle, Check (Ports, Interferenz 0, Fachrechnung), Teiledaten und Bild; Ring-Abzweig nur aus Bibliotheksteilen.

## 1 Pegelschacht `pegelschacht` (T94)

Fass PE-HD 60 l zwischen Biofilter-Ueberlauf (K10/K26) und den zwei Boostern; entkoppelt Zulauf und Pumpen (Blatt 2.3).

| Merkmal | Wert |
|---|---|
| Fass | aussen 400 x 520, Wand 4, Boden 5; Nenninhalt 62,2 l [E] (Handelsgroesse 60 l [A]) |
| Deckel | d410 x 15 mit Zulauf, Schwimmerstange, Kabelverschraubung M20, Entlueftung d20 |
| Zulauf K10/K26 | Stutzen d50 durch den Deckel, Unterkante 490 ueber Fassboden: freier Einlauf ueber dem Notueberlauf (476) |
| Saugstutzen A/B | 2 x Tankdurchfuehrung d50 radial bei +-30 Grad, Achse 100 ueber Fassboden (geflutet) |
| Notueberlauf K67/K75 | Tankdurchfuehrung **d63** radial -X, Achse 440, Sohle 411,5 |
| Schwimmerschalter | Stange d16, Ringschwimmer AUS bei 250, EIN bei 340 |
| Volumen [E] | AUS bis EIN 10,9 l; EIN bis Ueberlauf 8,6 l; Boden bis Ueberlauf 49,1 l |
| Masse leer | 5,76 kg [E] |

**Abweichung vom Netz-Vorschlag:** Notueberlauf d63 statt d50. Grund: Steht der Booster, muss der ganze Zulauf (110 l/min) ueber den Notueberlauf. Bei 2 % Gefaelle traegt d50 voll nur 76 l/min, d63 141 l/min [E, Manning n 0,009, `check_ring_b2.py`]. Das Netz-Delta (Blatt 2.6, Kanten K67/K75) nannte d50 als Vorschlag [A]; die Werkstatt bestaetigt d63.
**Offen 4 aus dem Blatt (Pegelschacht gegen Nachlauf des Rings):** Ein Halbring d75 x 10,7 m haelt 38,6 l [E]; zwischen EIN und Ueberlauf sind 8,6 l Platz. Laeuft der Halbring bei Booster-Stopp zurueck, gehen rund 30 l ueber den Notueberlauf in den Ruecklauf, also in den Pool: kein Wasserverlust, nur ein Schwall. Wer das vermeiden will, setzt ein Rueckschlagventil hinter jeden Booster (Montage-Entscheidung R1).

**Ports** (KS: Mitte Fassboden aussen, Z hoch):

| Port | Lage x, y, z | Richtung | Art |
|---|---|---|---|
| Zulauf (K10/K26) | -100, 0, 575 | +Z | Muffe d50 (DN40) |
| Saug A (K61/K69) | 216,5, 125, 100 | (0,866, 0,5, 0) | Muffe d50 (DN40) |
| Saug B (K62/K70) | 216,5, -125, 100 | (0,866, -0,5, 0) | Muffe d50 (DN40) |
| Notueberlauf (K67/K75) | -250, 0, 440 | -X | Muffe d63 (DN50) |
| Kabel Schwimmer | 100, 120, 555 | +Z | Kabelverschraubung M20 |
| Entlueftung | 0, -120, 535 | +Z | Bohrung d20 |

**Pruefung:** Koerperliste (10), Fassmasse, Nenninhalt, 6 Ports, Interferenz 0, Ueberdeckung Saugstutzen bei AUS 150 mm >= S = D(1 + 2,3 Fr) = 134 mm (55 l/min je Booster, v 0,57 m/s) [Formel A: Mindestueberdeckung nach Hydraulic-Institute-Ansatz, nicht abgerufen], Pegelreihenfolge, Schwimmer auf Pegel, freier Einlauf, Notueberlauf-Leistung, Schaltpuffer >= 10 l.

## 2 Ringstuetze d75 `ringstuetze_d75` (T95)

Bodenstuetze mit Kragarm; das Rohr haengt in einer Schelle, darunter bleibt der Gang frei (Blatt 2.4).

| Merkmal | Wert |
|---|---|
| Parameter | `achse_h` 2145 (Rohrachse ueber Innenboden), `ausladung` 250 (Pfostenachse bis Rohrachse); Varianten per `ringstuetze(dict(RS, achse_h=..., ausladung=...))` |
| Fussplatte | 200 x 200 x 10, 4 Anker M10 (Achsabstand 150) |
| Pfosten | Quadratrohr 50 x 50 x 3, Hoehe bis 2297 |
| Kragarm | Quadratrohr 40 x 40 x 3, von der Pfostenflaeche bis 310 |
| Haenger | Gewindestange M10, je eine Mutter unter und ueber dem Arm |
| Schelle | Stahl, Ring 3 + EPDM-Einlage 3, Breite 30; tiefster Punkt 2101,5 >= 2100 |
| Masse | 14,90 kg [E] |

**Statik [E, Check]:** Feldlast d75 voll Wasser bei Stuetzabstand 1,65 m = 77 N; Moment 19,2 Nm; Biegespannung Pfosten 2,3 MPa, Kragarm 3,8 MPa (Grenze 100 MPa); Kopfverschiebung 1,16 mm (Grenze L/300 = 7,7 mm); Ankerzug 64 N je Seite. Stuetzen je Halbring: 10,7 / 1,65 -> 7. Statik von Pfosten-Fuss und Boden prueft N-STATIK (Blatt Offen 3).

**Ports:** Rohrachse (Ring d75) bei 250, 0, 2145, Rohr entlang Y (Aufnahme DN65); Fuss bei 0, 0, 0, -Z (Auflage + 4 Anker M10).

**Pruefung:** Koerperliste (10), Einlage-Bohrung d75 auf der Rohrachse, Fussplatte auf z 0, tiefster Punkt >= 2100, nichts unter dem Rohr, Interferenz 0 inkl. Testrohr d75 (1,65 m), Biegespannung, Kopfverschiebung.

## 3 Entluefter d75 `entluefter_d75` (T96)

Am Hochpunkt jedes Halbrings (Blatt 2.4). T d75 mit Abgang d25, Uebergangsnippel d25 auf 1 Zoll, Schnellentlueftungsventil 1 Zoll (Messing, Schwimmer).

| Merkmal | Wert |
|---|---|
| Lauf | wie `lt_t_d75`: 2 x 86,375, Klebemuffen d75, Durchgang 67,8 (kein Querschnittsverlust) |
| Abgang | Stutzen d40 aussen, Muffe d25, 82,4 ueber der Achse |
| Ventil | d52 x 100 + Kappe d30 x 15, Luftaustritt d4; Oberkante 215 ueber der Rohrachse (Ring-Achse 2145 -> 2360 ueber Innenboden) |
| Masse | 1,46 kg [E] |

**Ports:** A -86,375, 0, 0 (-X, Muffe DN65); B 86,375, 0, 0 (+X, Muffe DN65); Luftaustritt 0, 0, 215 (+Z). Abgang nach oben einbauen.
**Pruefung:** Koerperliste (3), Lauflaenge = `lt_t_d75`, Ports, Durchgang d67,8, Interferenz 0 mit Testrohren d75 in beiden Muffen.

## 4 Ring-Abzweig `ring_abzweig_d40` / `ring_abzweig_d32` (T97)

Nur Bibliotheksteile, Geometrie unveraendert aus `scripts/workshop/leitung.py` (verschoben und gespiegelt): `lt_t_d75` -> Rohrstueck d75 -> `lt_reduzierung_d75_d50` -> Rohrstueck d50 -> `lt_reduzierung_d50_d40` (bzw. `_d32`) -> Rohrstueck d40 (d32) -> `lt_kugelhahn_d40` (d32) als Regler. Rohrstueck = 2 x Muffentiefe + 10 mm Spalt. Abgang nach unten (-Z).

| Merkmal | d40 (Beet) | d32 (Tisch) |
|---|---|---|
| T-Achse bis Abgang | 362,4 | 350,4 |
| Strom je Abnehmer | 7,8 l/min (54,5 / 7), v 0,13 m/s | 3,2 l/min (38 / 12), v 0,08 m/s |
| Masse | 1,18 kg | 1,14 kg |

**Ports:** A (Ring) -86,375, 0, 0 (-X, Muffe DN65); B (Ring) 86,375, 0, 0 (+X, Muffe DN65); Abgang 0, 0, -362,375 (d40, DN32) bzw. 0, 0, -350,375 (d32, DN25), Richtung -Z, Muffe B des Hahns (Fallleitung steckt dort).
**Pruefung:** Koerperliste (9), Volumen von T, beiden Reduziermuffen und Hahn = Volumen der Bibliotheks-`.sc` (Beleg "kein neues Teil"), Rohrstueck-Laengen, Ports, Interferenz 0. Die Spindel des Bibliotheks-Kugelhahns steckt bauartbedingt in Gehaeuse und Hebel (`leitung.kugelhahn`); diese zwei Ueberlappungen je Hahn zaehlt der Check nicht und meldet sie als INFO.
**Fuer die Montage:** Die Kette kann statt der Datei auch aus den Bibliotheksteilen gesetzt werden; Lagen stehen in `data/components/ring_b2_teile.json` (`kette`, je Teil z oben/unten).

## Herkunft (alle Texte, Normen, Bezug [A]; Masse aus dem Modell [E])

| Merkmal | Herkunft | Konfidenz |
|---|---|---|
| Fass 60 l aussen 400 x 520 | A: Weithalsfass-Handelsgroesse, nicht abgerufen | niedrig |
| Booster 55 l/min, Zulauf 110 l/min, Abnehmer 7 Beete / 12 Tische je Linie, NFT 38 l/min, Beete 54,5 l/min | Q `docs/jobs/N-VARIANTEN.md` 2.1 bis 2.4, `leitung_w36.py` V50_ABGAENGE | mittel |
| Ring Achse 2145, Unterkante 2100, Stuetzabstand 1,65 m | Q Blatt 2.1, 2.4 (R47 Abschnitt 1) | mittel |
| Profile 50x50x3, 40x40x3, Platte 200x10, Anker M10 | A | niedrig |
| Schnellentlueftungsventil 1 Zoll Messing | A: uebliche Bauart, kein Datenblatt | niedrig |
| Bezug aller Kaufteile | A: in der EU bestellbar (D76), Haendler nicht abgerufen; Artikel nicht in Katalog/Stueckliste (`ausnahme`, Aufnahme durch N-STUECKLISTE) | niedrig |

**Offene Fragen:** (1) Rueckschlagventil hinter den Boostern (Schwall in den Ruecklauf) entscheidet R1. (2) Fabrikat Schwimmerschalter und Entlueftungsventil offen. (3) Ringstuetzen-Statik am Fuss und im Boden: N-STATIK. (4) Entleerungs-Kugelhahn am Tiefpunkt und Ueberschuss-Kugelhahn am Ring-Ende sind Bibliotheksteile (`lt_kugelhahn_d50`), kein eigenes Teil.
