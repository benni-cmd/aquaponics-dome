# Bauteilblatt T70-SCH-KH63-TS / -TW: tiefer Ventilschacht fuer Kugelhahn d63

Generator `scripts/workshop/schacht_tief.py`, Pruefung `scripts/workshop/check_schacht_tief.py`, Daten `data/components/lt_schacht_tief.json`, Teiledaten `data/parts/lt_schacht_kugelhahn_d63_tief_*.json`.
Grundlage: `lt_schacht_kugelhahn_d63` (`docs/parts/leitungsteile.md`, Abschnitt Schacht; gleiche Wand 8, Boden 15, Deckel 30, PE-HD und EPDM). [Q] Quelle im Repo · [E] eigene Rechnung/Messung · [A] Annahme.

**Mini-Plan.** Problem: Der Bestands-Schacht passt nur fuer eine waagerechte Rohrachse 160 mm unter Flur. KH1/KH2 sitzen senkrecht, Port A 424 mm unter Flur; die Stamm-Haehne laegen waagerecht 186 mm unter Flur (`docs/jobs/M10-S2N.md` Aktualitaetspruefung Punkt 5). Intent: M10-S2N kann Schaechte mit Deckel an KH1/KH2 und an den Stamm-Haehnen setzen (R47 M2). Goal: zwei Bauformen mit Parametern Achstiefe und Rohrrichtung, Deckel buendig mit dem Innenboden (Z 400 absolut), Interferenz 0 gegen Hahn und Rohre in beiden Hebelstellungen, Abstand zu allen Bestandstrassen am Einbauort gemessen.

## Zwei Bauformen aus einem Generator

| Datei | fuer | Rohrrichtung | Tiefe |
|---|---|---|---|
| `lt_schacht_kugelhahn_d63_tief_senkrecht` | KH1 (K56, Linie 1), KH2 (K57, Linie 2) | senkrecht, Rohr d63 unten durch den Boden; Heber d75 (K01/K17 mit T5/T13) quer durch | Hahnmitte 486,4, Port A 423,9 unter Flur [E aus `r_stuecke` KH1/KH2 Z -23,9] |
| `lt_schacht_kugelhahn_d63_tief_waagerecht` | Stamm-Hahn je Linie (M3) | waagerecht durch zwei Wanddurchfuehrungen | Rohrachse 186 unter Flur [E aus Stamm Z 214] |

Pruefpunkt 5 in M10-S2N zaehlt "Instanzen `lt_schacht_kugelhahn_d63_tief`": beide Dateien tragen diesen Namen als Praefix (2 x senkrecht + 2 x waagerecht = 4).

## Masse

| Merkmal | senkrecht | waagerecht |
|---|---|---|
| Innen laengs X x quer Y | 188 x 400 | 240 x 400 |
| Aussen (Wanne) | 204 x 416, Hoehe 551,4 | 256 x 416, Hoehe 321 |
| Gesamttiefe Deckel-Oberkante bis Boden aussen | 581,4 | 351 |
| Versatz Schachtmitte gegen Hahnmitte (x, y) | -8, +35 | 0, 0 |
| Boden innen unter Hahnmitte | 80 (17,5 unter der Stutzen-Unterkante) | 150 |
| Durchfuehrungen | Boden d85 + EPDM-Ring innen 73 (Formstueck d63 72,15 passt); 2 x Wand d100 bei 250 unter Flur + EPDM-Ring innen 86 (Formstueck d75 84,75 passt) | 2 x Wand d70 + EPDM-Manschette innen 63 |
| Deckel | 208 x 420 x 30, 2 Griffmulden | 260 x 420 x 30, 2 Griffmulden |
| Masse [E, `check_schacht_tief.py`] | 8,44 kg (Wanne 5,93, Deckel 2,40) | 7,56 kg (Wanne 4,51, Deckel 3,03) |

Warum schmal laengs X (senkrecht): Links liegt der Bogen des Hebers K17 (Tangente 114 mm vor der Hahnachse), rechts der Abgang K21 am T12 (107,6 mm). Ein 400er-Schacht durchstiesse beide. Quer (Y) bleibt 400 fuer Hand und Hebel; Y ist um 35 mm zum Hebel hin verschoben, damit der T6-Arm (Linie 1, -185 mm) draussen bleibt.

Warum 240 laengs (waagerecht): Die laengste freie Gerade bei Z 214 auf Linie 2 ist K22-T Segment 1 mit 263 mm (Formstuecke abgezogen); 256 + 2 x 3 Dichtung = 262 passt.

## Ports (Bauteil-KS, mm; Ursprung = Hahnmitte, Z hoch)

| Bauform | Port | Lage x, y, z | Richtung | Art |
|---|---|---|---|---|
| senkrecht | Hahn Port A (oben) | 0, 0, 62,5 | +Z | Lage Kugelhahn d63 |
| senkrecht | Bodendurchfuehrung | 0, 0, -95 | -Z | Durchfuehrung DN50 (d63) |
| senkrecht | Querdurchfuehrung A / B | -110 / 94, 0, 236,4 | -X / +X | Durchfuehrung DN65 (d75) |
| senkrecht | Deckel | -8, 35, 486,4 | +Z | Oeffnung, Flur |
| waagerecht | Durchfuehrung A / B | -128 / 128, 0, 0 | -X / +X | Durchfuehrung DN50 (d63) |
| waagerecht | Deckel | 0, 0, 186 | +Z | Oeffnung, Flur |

**Einbau senkrecht:** Schacht-X = Richtung K01-m (Linie 1) bzw. K17-m (Linie 2), also vom Steigrohr K01/K17 weg; Schacht-Y = Z x X. Kugelhahn `lt_kugelhahn_d63`: Hahn-Z nach Welt -Z (Port A oben), Hahn +X (Spindel) nach Schacht +Y. Ursprung auf die Hahnmitte KH1 (2587,9 / 630,9 / -86,4) bzw. KH2 (-1245,9 / -2294,8 / -86,4) absolut.
**Einbau waagerecht:** Schacht-X = Rohrachse, Hahn-Z = Rohrachse, Spindel nach Welt +Z, Ursprung = Hahnmitte.

## Pruefung

`python -X utf8 scripts/workshop/check_schacht_tief.py --render` → **46/46 PASS**, Befunde Einbauort 1.
Geprueft: Koerperzahl, Aussenmasse, Wannen- und Deckelvolumen gegen Rechnung (Toleranz 0,2 %), Deckel buendig mit Flur, Deckel auf der Wand, Durchfuehrungen und Dichtungsbohrungen, Tiefe Port A 423,9 (Soll 424) und Querleitung 250 unter Flur, Boden unter Stutzen und Hebel, Tiefleitung K56-b/K57-b unter dem Schachtboden, Oeffnung >= Hebel + 200, Greiftiefe bis Hebeloberkante (senkrecht 431, waagerecht 103; Grenze 600 [A]), Interferenz 0 gegen Hahn d63, T d75, Rohre d75/d63 und Tiefleitung in Richtung KH1 und KH2, je Hebel offen und zu; Abstand zu allen Trassen und T-Stueck-Armen aus `data/leitungstrassen.json` an KH1 und KH2 >= 10 mm.
Bilder (Schnitt y = 0 mit Hahn und Rohren): `renders/components/leitungsteile/lt_schacht_kugelhahn_d63_tief_senkrecht.png`, `..._waagerecht.png`.

## Befund an die Montage (M10-S2N, Stamm-Haehne)

1. M3 legt die Stamm-Haehne auf K06-T-b / K22-T-b. Dort ist keine Gerade lang genug: frei 148 / 124 mm (Linie 1) und 117 / 68 mm (Linie 2) gegen Bedarf 262 mm [E, `check_schacht_tief.py waagerecht`, Formstueck-Anteile abgezogen].
2. Linie 1 passt auf K06-T (vor dem Bypass-T T6): bester Platz Hahnmitte 3626,0 / 458,2 / 214,0, Segment K06-T[2], Rohrrichtung (-0,866, 0,5), 99,5 mm Luft zur naechsten Leitung. Folge: Der Hahn sperrt dann den Filterauslauf, nicht die Pumpen-Saugseite; bei geschlossenem Hahn versorgt der Bypass K56 die Pumpen.
3. Linie 2 hat keinen Platz: K22-T[1] ist lang genug, aber K18 laeuft 68 mm neben K22-T; die Schachtwand (Y +-208) liegt 25 mm im Rohr K18.
4. Optionen fuer S2N: (a) Linie 2 Stamm-Hahn oberirdisch oder an anderer Stelle, (b) Trasse K18/K22-T neben dem Hahn auseinanderziehen (>= 245 mm Achsabstand), (c) ein Doppelschacht mit Durchfuehrung fuer K18 (neues Werkstatt-Teil). Entscheidung liegt bei der Montage/dem Orchestrator.

## Herkunft

| Merkmal | Wert | Herkunft | Konfidenz |
|---|---|---|---|
| KH1/KH2 Port A Z -23,9, T5/T13 Z 150, Stamm Z 214, Flur Z 400 | mm absolut | Q `data/leitungstrassen.json` (`r_stuecke`, `t_stuecke`, Trassen) | hoch |
| Hahn d63 L 125, Gehaeuse 84,15, Hebel 110 | mm | E aus `leitung.kugelhahn(63)` | niedrig (Bauform der Bibliothek) |
| Wand 8, Boden 15, Deckel 30, PE-HD 0,95, EPDM 1,1 | | A wie `lt_schacht_kugelhahn_d63` | niedrig |
| Ringraumdichtung d100/d86 und d85/d73 | mm | A: Handelsteil "Ringraumdichtung" nicht abgerufen | niedrig |
| Greiftiefe 600 | mm | A: Armlaenge Schulter bis Fingerspitze etwa 650, nicht abgerufen | niedrig |
| Mindestluft zu fremder Leitung 10 | mm | A | mittel |

**Montage (L4):** Graben bis 10 cm unter Schachtboden, Sandbett; Wanne einsetzen und ausrichten; senkrecht: Rohr d63 von unten durch die Bodendichtung, Heber d75 durch die Querdichtungen; Hahn kleben; Wanne verfuellen; Deckel buendig. Werkzeug wie Bestands-Schacht.

**Offene Fragen:** (1) Entwaesserung des Schachtbodens fehlt wie beim Bestand. (2) Bogenlage K17/K01 aus der Montage (R 90 angenommen); weicht sie ab, Querdurchfuehrung A neu pruefen. (3) Linie 2 Stamm-Hahn (Befund oben).
