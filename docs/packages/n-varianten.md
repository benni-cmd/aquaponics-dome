# Paket: N-VARIANTEN — Kreislauf A+ und Ring B2 umschaltbar im ganzen Projekt (W70)

**Problem:** E20 (Wasserkreislauf) ist offen; das Projekt kennt nur einen Kreislauf, ein Vergleich ginge heute nur als Viewer-Bild, nicht in Einkaufsliste, Kennzahlen und Pruefungen.
**Intent:** Ben vergleicht beim Zwischencheck A+ (Empfehlung, Annahme D81) und die beste Wasserautobahn B2 (R47c) vollstaendig und schaltet mit einem Parameter.
**Goal:** `kreislauf_variante` (`a_plus` | `ring_b2`) erzeugt je Variante Modell, Einkaufsliste, Kennzahlen, Viewer-Export und Pruefergebnisse; A+ bleibt byte-gleich; Ring B2 ist mit Pegelschacht, Boostern, zwei Halbringen und 38 Abzweigen gebaut und geprueft.

Auftragsblatt mit Architektur, Netz-Delta, Pruefpunkten: `docs/jobs/N-VARIANTEN.md`.

## Plan
1. [x] V1a Werkstatt Skripte/Daten (05.11.2026, siehe Stand): `scripts/variante.py`, Schalter in `params.json`, Ausgabepfade in BOM, Einkaufsliste, Kennzahlen, Viewer-Export, `check_varianten.py`, Vergleichsseite.
2. V2 Werkstatt Bauteile (sofort, parallel): Pegelschacht, Ringstuetze, Entluefter, Ring-Abzweig; Booster = `pumpe_gross`.
3. VV Viewer-Schalter (nach V1a, parallel).
4. V1b Varianten-Weiche in `gen_dome.py`, `build.sh`, `leitungen.py`, Pruefskripten (EIN Slot der Modell-Kette); danach markiert die A+-Kette A+-only-Teile mit `varianten: ["a_plus"]`.
5. O1 Orchestrator: Netz-Delta K60..K75 in `data/leitungsnetz.json`.
6. R1/R2 Montage Ring B2 Linie 1 und 2 (nach M10-S7, vor CHECK).
7. Pruefer PV1 (nach V1a/V1b/VV), PV2 (nach R2); CHECK laeuft fuer beide Varianten.

## Stand
- 05.11.2026: Plan und Blatt geschrieben (Planer). Noch nichts gebaut. A+-Blaetter M10-S2N..S7 standen beim Schreiben nicht im Repo.
- 05.11.2026: **V2 Werkstatt Bauteile gebaut und gemessen.** `python -X utf8 scripts/workshop/check_ring_b2.py` 56/56 PASS; `python -X utf8 scripts/workshop/check_parts.py pegelschacht ringstuetze_d75 entluefter_d75 ring_abzweig_d40 ring_abzweig_d32` 5 x 22/22. Blatt `docs/parts/ring_b2.md`, Daten `data/components/ring_b2_teile.json`, Bilder `renders/components/ring_b2/`.
  - Pegelschacht `pegelschacht` (T94): Fass 60 l (62,2 l), Zulauf d50 im Deckel, 2 Saugstutzen d50, Schwimmer AUS 250 / EIN 340, Ueberdeckung 150 >= 134 mm. **Notueberlauf d63 statt d50** (d50 traegt bei 2 % nur 76 l/min, d63 141 l/min >= 110): Vorschlag an O1 fuer K67/K75.
  - Offen 4 beantwortet: Halbring 38,6 l > Reserve EIN bis Ueberlauf 8,6 l; Rest geht bei Booster-Stopp ueber den Notueberlauf in den Ruecklauf (kein Verlust). Rueckschlagventil hinter den Boostern entscheidet R1.
  - Ringstuetze `ringstuetze_d75` (T95): Parameter achse_h 2145, ausladung 250; Schelle tiefster Punkt 2101,5 >= 2100, nichts unter dem Rohr; Biegung 2,3/3,8 MPa, Kopf 1,16 mm.
  - Entluefter `entluefter_d75` (T96): T d75 + Nippel + Schnellentlueftungsventil 1 Zoll, Oberkante 215 ueber Achse.
  - Ring-Abzweig `ring_abzweig_d40` / `_d32` (T97): nur Bibliotheksteile (Volumen = Bibliotheks-.sc belegt), Abgang 362,4 / 350,4 unter der T-Achse.
  - Artikel stehen nicht in Katalog/Stueckliste (`ausnahme` in den Teiledaten): Aufnahme durch N-STUECKLISTE.

- 05.11.2026: **V1a Werkstatt Skripte/Daten gebaut und gemessen** (kein Bau, kein `gen_dome.py`, kein `designs/dome.sc`).
  - Neu: `scripts/variante.py` (Schalter `--variante`/`KREISLAUF_VARIANTE`/`params.json`, `gilt`, `filtere`, `pfad`), `scripts/check_varianten.py`, `scripts/bom_vergleich.py` -> `docs/varianten-vergleich.md`. `data/params.json`: Eintrag `kreislauf_variante` (Standard `a_plus`).
  - Schalter eingebaut in `bom.py`, `bom_artikel.py` (Pfad der Instanzen), `bom_seite.py`, `check_bom.py`, `check_netz.py` (Filter `varianten` an Knoten und Kanten), `system_specs.py` (Block `kreislauf`, Datei je Variante), `viewer/export_model.py` und `viewer/export_ansicht.py` (Ausgabe nach `viewer/varianten/ring_b2/`, `defs/` gemeinsam).
  - P1 (A+ unveraendert), Messung vom 05.11.2026:
    1. `python -X utf8 scripts/check_varianten.py --a-plus-gleich`: 11 PASS, 1 OFFEN (Ring B2 noch nicht gebaut), 0 FAIL, Exit 0. `bom.py` ohne Schalter und mit `--variante a_plus` erzeugen in einer Kopie `stueckliste.json`, `stueckliste.md` und `einkaufsliste.html` byte-gleich.
    2. `data/system-specs.json`: alle Schluessel ausser dem neuen Block `kreislauf` gleich dem Stand `HEAD` (Vergleich per `python -c`, `a == old` nach `pop('kreislauf')`).
    3. `viewer/export_ansicht.py`: altes Skript (`git show HEAD:...`) und neues Skript auf denselben Eingaben, `sha256sum` der `ansicht.json` gleich (cccb1ffc55...).
    4. `python -X utf8 scripts/check_bom.py`: Exit 0, 14 von 14 PASS. `check_netz.py` und `check_netz.py --variante ring_b2`: bestanden.
  - Grenzen: (a) `viewer/export_model.py` ist nur auf Syntax und Pfade geprueft, nicht gelaufen (voller Export macht die naechste Montage; Ring B2 hat noch kein `dome-script-ring_b2.json`). (b) `data/stueckliste.json` der Kopie weicht vom Repo nur im Modellstempel ab, weil eine parallele Sitzung eine `.sc` ergaenzt hat. (c) Die Einkaufsliste von Ring B2 traegt kein sichtbares Variantenetikett (Vorlage `bom_seite_vorlage.html` bleibt fuer A+ byte-gleich); nur das Feld `kopf.variante` steht in `stueckliste-ring_b2.json`. (d) Die gemessenen Kennzahlen (Rohrlaenge, Wasser in Rohren) sind in beiden Varianten gleich, bis V1b die Trassen mit `varianten` markiert.

05.11.2026, Viewer VV (Schalter Kreislauf A+ / Ring B2, `viewer/index.html`, `viewer/serve.py`): Auswahl "Kreislauf: A+ | Ring B2" im linken Menue, gespiegelt in der Adresse (`?variante=ring_b2`) und im `localStorage` (`viewer.variante`); sichtbares Etikett oben in der Bildmitte und im Tab-Titel. Beim Wechsel liest `load()` `instances.json`, `extras.json` und `ansicht.json` aus dem Variantenordner (`viewer/varianten/ring_b2/`), die Definitionen (`defs/`) bleiben gemeinsam. `serve.py` beobachtet beide Modelle (`designs/dome.sc`, `designs/dome-ring_b2.sc`), exportiert die geaenderte Variante mit `export_model.py --variante <v>` (nie zwei Exporte zugleich), liefert `/api/state`, `/system-specs.json` und `/stueckliste.json` je Variante (Pfade aus `scripts/variante.py`). Ist die Variante noch nicht exportiert, steht die Meldung mit dem Exportbefehl da, das bisherige Modell bleibt und Schalter und Etikett kehren zur gezeigten Variante zurueck.
- Probe nur mit vorhandenem Export (Scratchpad-Kopie mit Junctions auf `viewer/defs` und `data/parts`, Ring-B2-Ordner aus dem A+-Export abgeleitet ohne die zwei Absetzer): A+ 4914 Instanzen, 164 Definitionen; Wechsel auf Ring B2: 4912 Instanzen, 163 Definitionen, Kennzahlen mit anderem Stand, 0 neue Abrufe aus `defs/` (164 vor, 164 nach), Adresse `?variante=ring_b2`, Rueckwechsel ebenso; Ordner entfernt: Meldung "noch nicht exportiert" und Rueckkehr zu A+. Screenshots mit Etikett "Kreislauf: Ring B2" und "Kreislauf: A+".
- Nicht gemessen: ein echter Ring-B2-Export (V1b steht aus), Kennzahlen-Datei `data/system-specs-ring_b2.json` und `data/stueckliste-ring_b2.json` der echten Variante.

## DoD
1. P1 bis P5 aus `docs/jobs/N-VARIANTEN.md` Abschnitt 5 von fremden Pruefern als PASS belegt (`docs/jobs/pruefung/N-VARIANTEN-1.md`, `-2.md`).
2. Viewer-Screenshot beider Varianten im echten Browser.
3. `docs/varianten-vergleich.md` mit Mehr/Weniger (Artikel, Kosten, Kennzahlen) fuer den Zwischencheck-Bericht.
4. Jeder Schritt mit Pfad-Commit und Push.
