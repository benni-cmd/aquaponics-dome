# Bauteilblatt: Prototyp Scherenknoten (W74, R56) — NICHT im Gesamtmodell

**Funktion:** Verbindet ein Strebenrohr mit der Lochplatte des Knotens. Zwei gekreuzte Laschen mit Drehpunktschraube stecken im Rohr; geschlossen (Augen deckungsgleich, mit der Plattenschraube auf dem Lochkreis verschraubt) stehen ihre Nasen durch zwei gegenueberliegende Wandloecher 3 mm nach aussen. Offen (Augen etwa 6,5 Grad je Seite auseinander) ziehen die Nasen ein, das Rohr laesst sich aufschieben. Zustand im Modell: geschlossen, Nasen ausgefahren.

**Datei:** `designs/components/knoten_schere_proto.sc` · **Generator:** `scripts/components/knoten_schere_proto.py` (Bau + Check; `--render` fuer Bilder; `--check` nur pruefen) · **Bericht:** `docs/research/R56-scherenknoten.md` · **Status:** Prototyp zur Abnahme durch Ben; keine Serie, kein Einbau.

**Bezugspunkt:** Knotenpunkt = Ursprung; Z = Kuppelnormale (aussen); Lochplatte in der Tangentialebene, Oberkante Z -25,47; Strebe in +X, um 18,0 Grad nach innen geneigt (Strebe B, asin(3708/12000)). Die Rohrachse geht durch den Knotenpunkt (Check 0,000 mm).

## Masse und Parameter (alle [A] aus dem Foto ohne Massstab, R56 Abschnitt 2)
| Teil | Mass |
|---|---|
| Lochplatte | D 110 x 8, 6 Loecher D 11 auf Lochkreis r 37, Mittelbohrung D 20 |
| Lasche (2 Stueck) | 20 x 5, Auge bis Drehpunkt 50 mm, Drehpunkt bis Nase 58 mm, Nase 10 mm breit, Knick 18,0 Grad bei r 63 (8 mm ausserhalb der Platte) |
| Rohrstueck | Rund 42,4 x 2,6, Laenge 250 (Probestueck), Rohrende 12 mm hinter dem Drehpunkt, 102,2 mm vom Knotenpunkt |
| Wandloecher | 2 x D 13, 46 mm hinter dem Rohrende, gegenueber; je um 2,5 mm zur Laschenmitte versetzt |
| Schrauben | Platte M10 x 35 mit 2 Scheiben und Mutter; Drehpunkt M8 x 25 mit 2 Scheiben und Mutter (Bibliothek `parts.insert`) |

## Werkstoff und Gewicht (Messung `solidcraft-cli eval`)
Laserteile `Stahl Laserteil` S235, Rohr `Stahl verzinkt`, Schrauben `Stahl Schraube`, je 7,85 g/cm3.
Lochplatte 541 g · Lasche 96 und 97 g · Rohrstueck 250 mm 632 g · Schrauben, Scheiben, Muttern zusammen 75 g.

## Pruefung
`python -X utf8 scripts/components/knoten_schere_proto.py` → 6/6 PASS (05.11.2026):
1. 12 Koerper (Platte, 2 Laschen, Rohr, 8 Normteile), alle geschlossen.
2. Beide Nasen reichen 24,2 mm von der Achse = Rohraussenradius 21,2 + 3.
3. Rohrachse durch den Knotenpunkt: 0,000 mm.
4. `inspect.interference` Laschen, Rohr, Platte: 0 Durchdringungen. Alle Koerper: einzig Drehpunktschraube/Mutter 0,01 mm3 (Gewindeberuehrung).

## Renders (angesehen 05.11.2026)
- `renders/components/knoten_schere_proto/knoten_schere_proto-01-iso.png`
- `renders/components/knoten_schere_proto/knoten_schere_proto-02-iso-rohr-durchsichtig.png`
- `renders/components/knoten_schere_proto/knoten_schere_proto-03-draufsicht-durchsichtig.png` (Nasen links und rechts durch die Wand)
- `renders/components/knoten_schere_proto/knoten_schere_proto-04-seite.png` (Knick der Laschen, Achse durch den Knotenpunkt)
- `renders/components/knoten_schere_proto/knoten_schere_proto-05-nase-detail.png`

## Offen (fuer Ben, siehe R56 Abschnitt 6)
1. Lesart der Funktion bestaetigen.
2. Rohr 42,4 x 2,6 rund statt 30 x 30 x 3.
3. Laschendicke 8 statt 5 mm (Knick ist der Engpass, R56 Abschnitt 4).
4. Der geoeffnete Zustand ist nicht modelliert.
