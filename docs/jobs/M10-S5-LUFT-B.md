# M10-S5-LUFT-B Technikbereich: Schaltschrank, Geblaese, Hauptverteiler, Aktivkohle und ihre Leitungen (Montage)

Planer: Opus 5.5, 05.11.2026 (Planer-Buendel M10 nach A+). Nur gelesen, kein Modell, keine Daten geaendert. Vorgaenger-Blatt: `docs/jobs/M10-S5-LUFT.md` (Teil A gebaut Runde 69, Teil B/C waren OFFEN E13/E20). Reihenfolge der Montage-Kette (`docs/packages/bis-zwischencheck.md` Plan 1): **LUFT-B -> M10-S2N -> M10-S3 -> M10-S4 -> M10-S5 -> M10-S6 -> M10-S7**, immer nur eine Montage-Sitzung zugleich.

**Problem:** Geblaese x2 (`geblaese_luft`), Hauptverteiler (`luftverteiler_6`), Aktivkohle-Station (`aktivkohle_station`) und Schrank-Einfuehrung (`schrank_einfuehrung`) sind gebaut, aber nicht im Dom; der Schaltschrank steht noch am alten Ort Az 0 (`scripts/gen_dome.py` Zeile 494 bis 497, D62). Die Kanten K39, K40, K41, K44 (Zuleitung), K45, K46, K49, K51 haben ein loses Ende.
**Intent:** D81 setzt E13 als Annahme (Schrank bei Az -85 / r 5750, Technik dort als verschiebbare Gruppe "vorlaeufig, E13") und E20 = A+ (kein Ring, K40 kommt aus der Station). Damit ist alles aus Teil B und Teil C baubar; Ben bestaetigt den Ort beim Zwischencheck.
**Ziel in einem Satz:** Eine verschiebbare Technikgruppe (Schrank, Einfuehrung, 2 Geblaese, Hauptverteiler, Aktivkohle-Station) steht bei Az -85, alle Luft- und Frischwasserkanten K39, K40, K41, K44, K45, K46, K49, K51 sind verlegt, `check_leitungen` 0 Verstoesse.

## Aktualitaetspruefung (05.11.2026, Regel W44)
Ergebnis: **angepasst** (Plan gilt als freigegeben).
1. D81 (05.11.): E13 Annahme Az -85 / r 5750, Teil B als verschiebbare Gruppe; E20 = A+ -> K40 Zulauf aus der Aktivkohle-Station (nicht aus einem Ring); E15 Chloramin -> Aktivkohle bleibt.
2. Teil C des alten Blatts loest sich auf: K40 baubar (A+); K45/K46 baubar (Biofilter bleiben wo gebaut, A+ aendert keine Hoehen); **K47/K48 "optional" (Netz) werden nicht gebaut** [A, Planer], Abgang am Hauptverteiler bekommt eine Kappe.
3. **Befund Ort:** r 5750 liegt INNERHALB des Fundamentrings: `schrank_fn` rechnet die Aussenkante als Apothem (6000 + 250) x cos 18 = 5944 mm (`gen_dome.py` Zeile 495). "Aussen am Fundamentring" (D81-Text) und r 5750 widersprechen sich. Annahme dieses Blatts: **innen an der Wand bei Az -85**, Rueckseite der Gruppe mit >= 110 mm Wandluft zur Haut/Plane (Regel Wandluft 110); r 5750 ist der Bezugspunkt der Schrankmitte und darf zur Kuppelmitte hin wandern, bis Wandluft und Gaenge passen. Besonderheit an den Orchestrator melden.
4. Teil A (Pool-Verteiler, 4 Scheiben, Schwimmerventil) bleibt unveraendert; die Muffe A des Pool-Verteilers zeigt nach Az 0, nicht zur Gruppe: die Trasse K44 holt die Richtung mit Boegen, Teil A wird nicht gedreht.
5. Subtank M10-S2V bleibt geparkt (Ben); dieses Blatt beruehrt ihn nicht.

## Eingaben (nur diese; Zeilen selbst nachsehen)
- `docs/jobs/M10-S5-LUFT.md` Abschnitte "Aufteilung" und "Schritte" Punkt 4; `docs/packages/m10-s5-luft.md` Port-Tabelle der Enden (Drittbecken K41/K42/K43/K49 gemessen, Zweitbecken K51 Annahme, Schwimmerventil K40 Port A, Pool-Verteiler K44 Port A).
- `data/leitungsnetz.json` (nur lesen): K39, K40, K41, K44 bis K52, Knoten `belueftung`, `aktivkohle`, `frischwasser`.
- `docs/parts/geblaese_luft.md`, `luftverteiler_6.md`, `aktivkohle_station.md`, `schrank_einfuehrung.md`, `schaltschrank` (Komponente `designs/components/schaltschrank.sc`): Ports, Ursprung, Masse.
- `scripts/gen_dome.py` `schrank_fn` (Zeile 494 bis 510), `place_instances`; `scripts/trassen_luft.py` (Muster Teil A), `scripts/leitungen.py`, `data/params.json` (cab_x 800, cab_y 500, cab_z 1200).

## Schritte (je Schritt ein Pfad-Commit)
1. **Parameter:** `data/params.json` neu `technik_az` = -85 und `technik_r` = 5750 (origin A, Quelle "D81 Annahme E13, vorlaeufig"); `schrank_fn` auf diese Parameter umstellen (Schrank innen an der Wand, Front zur Kuppelmitte).
2. **Gruppe setzen:** Komponente `09_Technik_E13` (Name enthaelt "E13") mit Schrank, `schrank_einfuehrung` (unten am Schrank), `geblaese_luft` x2 nebeneinander auf Konsole/Boden, `luftverteiler_6`, `aktivkohle_station` wandnah. Alle Lagen relativ zu einem Gruppen-Ursprung, damit eine einzige Translation/Drehung die Gruppe verschiebt (Ben kann E13 aendern).
3. **Luft:** `scripts/trassen_luft.py` erweitern: K44-Haupt (Hauptverteiler -> Pool-Verteiler Port A, d40, unterflur U-Band, Steigrohr an der Poolwand), K45/K46 (d25 -> Biofilter-Deckel Ø16, `Tank_gross:1` und `Tank_gross_t3:1`), K49 (d20 -> Drittbecken Tuelle ID16), K51 (d20 -> Zweitbecken). Rueckschlagventile `lt_rueckschlagventil_d25/d20` am Geblaese-Ausgang je Strang (Luft darf bei Stromausfall nicht Wasser ziehen). Abgaenge fuer K47/K48 mit Kappe.
4. **Frischwasser:** K39 (Hausanschluss als Ende "aussen", Durchfuehrung Fundament, -> Station, Zaehler-Halter MS50 H_INLINE), K40 (Station -> Schwimmerventil Port A, d25), K41 (Station -> Drittbecken K41 Muffe d20), K52 als Zapfhahn d25 an der Station (Netz: "von Hand, kein Dauerfluss", keine Leitung).
5. **Zweitbecken-Stutzen K51** (und Frischwasser, falls im Netz) in `gen_dome.py` am Beckenrand zur Kuppelmitte (Annahme der Port-Tabelle), wie die Drittbecken-Stutzen gebaut.
6. Build `sh scripts/build.sh 5 <naechste Runde>`, Pruefungen, Bild, `docs/loop-state.md` Abschnitt "M10-S5-LUFT-B", Paket `docs/packages/m10-s5-luft.md` nachfuehren (Plan Punkt 4 und 5 abhaken).

## Nicht anfassen
Teil A (Pool-Verteiler, Scheiben, Schwimmerventil, K44-S1..S4); `data/leitungsnetz.json`, `data/roadmap.json`, `data/katalog.json`, `data/beschaffung/`; Bauteil-Dateien `designs/components/*.sc` (fehlt etwas: Werkstatt-Notiz); Kabel (M10-S6); Wasser-Hauptkreislauf; M10-S2V.

## Dateiliste (darf schreiben)
`data/params.json` (nur `technik_az`, `technik_r`), `scripts/gen_dome.py`, `scripts/trassen_luft.py`, `scripts/leitungen.py` (nur falls noetig), `data/leitungstrassen.json`, `designs/dome.sc`, `scripts/dome-script.json`, neue `designs/components/lt_rohr_d*_L*.sc` (vom Werkzeug erzeugt), `docs/loop-state.md`, `docs/packages/m10-s5-luft.md`, `renders/`.

## Ergebnis
Technikgruppe "vorlaeufig, E13" im Dom, acht Kanten verlegt, Port-Tabelle der Gruppe im Paket, Kurzmeldung mit Lage der Gruppe (Az, r, Wandluft) und Befund innen/aussen.

## Pruefpunkte (fremd messbar)
1. Gruppe: genau 1 Instanz je `schaltschrank`, `schrank_einfuehrung`, `luftverteiler_6`, `aktivkohle_station` und 2 Instanzen `geblaese_luft`, alle unter einer Komponente mit "E13" im Namen; Schwerpunkt der Gruppe Az -85 +- 5 Grad (aus `scripts/dome-script.json`, Instanzmatrizen). Soll 1/1/1/1/2.
2. Kanten: `data/leitungstrassen.json` enthaelt Trassen fuer K39, K40, K41, K44 (Zuleitung), K45, K46, K49, K51 (Soll 8 Kanten, `python -X utf8 -c` ueber das Feld `kante`); keine Trasse fuer K47/K48.
3. `python -X utf8 scripts/check_leitungen.py`: EINGABE/KOLL/BAND/GANG/GEFAELLE 0 Verstoesse (dokumentierte dn-Abweichungen erlaubt).
4. `python -X utf8 scripts/check_walkways.py` PASS mit A >= 700, B >= 600, Wandluft >= 110, Tuer-Gang >= 3177 (gleich Runde 69).
5. `git hash-object` von `data/leitungsnetz.json` und `data/roadmap.json` gleich dem Stand vor der Sitzung; Teil-A-Instanzen (`Luftverteiler_4`, 4 `Luft_Scheibenbelueftung`, `Schwimmerventil_Pool`) mit unveraenderten Matrizen.

## Start-Hinweis fuer die Montage-Sitzung
1. Startet erst, wenn die Montage "Strebe + Werkstoffe" committet ist (eine Montage zugleich, D80).
2. Befund r 5750 innerhalb des Fundamentrings zuerst nachmessen (Haut-Innenkante bei Az -85); Gruppe innen, Wandluft >= 110.
3. Falle W37-3: `component.insert_design` kennt nur `translate`; drehen per `occurrence.move ... matrix=[12 Zahlen]`.
4. Falle Runde 69: der Viewer-Export kann unter paralleler CLI-Last scheitern; einmal wiederholen, dann melden.
5. Limit: ein Paket; Stand in `docs/loop-state.md`, Meldung hoechstens sechs Zeilen, dann STOPP.
