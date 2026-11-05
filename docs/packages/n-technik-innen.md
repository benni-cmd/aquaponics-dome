# Work package: N-TECHNIK-INNEN Technikgruppe in die Kuppel, Rohrwege kurz

> Work artifact per `working-method.md`; angelegt vom Planer 05.11.2026, nachgefuehrt bei jedem Abschluss. Blatt: `docs/jobs/N-TECHNIK-INNEN.md`. Quelle: W72, D84 (Ben 05.11.).

**Problem:** Die Technikgruppe steht seit Runde 74 aussen vor dem Ring; die 9 Luft- und Frischwasserkanten sind zusammen 104,9 m lang.
**Intent:** Technik dort, wo sie arbeitet: kurze Wege, weniger Rohr und Graben, Wartung von innen.
**Goal:** Ein Technikturm (Station, 2 Geblaese, Verteiler) steht innen bei x 600 / y -4900, die Kanten sind zusammen hoechstens 85 m lang, die Gaenge bleiben PASS; der Schaltschrank-Ort ist Ben zur Entscheidung vorgelegt.

## Plan
1. [x] Planer: Aktualitaetspruefung, Platzsuche innen, Laengen und Druck vorher/nachher, Blatt mit 5 Pruefpunkten (05.11.2026; Rechenskript `scripts/n_technik_innen.py`)
2. [ ] Werkstatt Teil A: `technik_turm`, kompakte `aktivkohle_station`, Luftstutzen am Absetzerdeckel (K47/K48); darf sofort laufen
3. [ ] Montage Teil B: Turm setzen, Kanten neu routen, Build; nach der Abnahme von M10-S2N, vor M10-S3
4. [ ] Pruefer: Pruefpunkte 1 bis 5 des Blatts
5. [ ] Ben (Zwischencheck): Schaltschrank aussen lassen (V1) oder innen (V2, kostet das Verschieben von Absetzer 1 und Pumpe_klein:2)

## Stand (05.11.2026, Planer)
- **Platz innen** (`python -X utf8 scripts/n_technik_innen.py suche streng` / `... suche gang300`):
  - Mit den geltenden Gangregeln passt innen nur das Geblaese-Paar, und zwar nur im Tuerkeil.
  - Die Aktivkohle-Station (1,7 m) passt nirgends.
  - Bei 300 statt 500 mm Gang zur Stirnseite von Beet 4 passt genau ein Kasten 800 x 500 (Turm bis 2 m oder Schrank), nicht beides.
  - Die Huelle zieht in der Tuerfacette 0,191 mm je mm Hoehe nach innen; deshalb scheiterte Runde 74 innen.
- **Laengen** (`python -X utf8 scripts/n_technik_innen.py laengen`):
  - 9 Kanten: V0 104,9 m -> V1 77,4 m (-26 %).
  - Luft 57,3 -> 45,1 m, Frischwasser 47,6 -> 32,2 m.
  - K47/K48 dazu geschaetzt: 21,4 -> 15,3 m.
- **Leistung** (`python -X utf8 scripts/n_technik_innen.py druck`): Das Geblaese bleibt gleich (Pool-Strang 24,36 -> 24,35 kPa, 117 W -> 117 W). Der Druck kommt aus 2,17 m Wassertiefe, die Rohrreibung betraegt 64 bis 71 Pa. Frischwasser laeuft ohne Pumpe. Der Gewinn liegt im Material, nicht im Strom.
- **Schaltschrank:** innen hoechstens 284 mm Huellenluft in 1,2 m Hoehe (`... huelle`). Brandschutz-Abstand >= 500 mm, Unterlage A1 und IP54 sind Annahmen [A]; die Normen VDE 0100-705:2007-10 und VDE 0100-420:2022-06 sind benannt, Zahlen nicht gelesen.

## Definition of Done
Geprueft gegen:
1. `scripts/dome-script.json` (Instanzen nach Runde 74)
2. `data/leitungstrassen.json` (Trassen Runde 74)
3. `data/params.json`, `scripts/.compbox.json`
4. `docs/jobs/pruefung/M10-S5-LUFT-B.md`, `docs/leitungsordnung.md`, D62/D70/D72/D84, W72
5. `git log --oneline -15` (M10-S2N laeuft)

Offen:
1. Werkstatt Teil A (Turm, kompakte Station, Absetzer-Stutzen): Orchestrator startet die Sitzung (EMPFOHLEN als naechster Schritt)
2. Montage Teil B nach der Abnahme von M10-S2N: Orchestrator
3. Schaltschrank aussen (V1) oder innen (V2): DEINE ENTSCHEIDUNG, Ben, beim Zwischencheck
4. Brandschutz-Abstand und IP-Klasse mit zwei Quellen belegen: Recherche-Sitzung, Orchestrator
