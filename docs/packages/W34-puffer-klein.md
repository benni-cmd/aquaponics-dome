# Paket W34 — Kleiner Puffer im Dom und kleineres Drittbecken (Werkstatt, Auftrag docs/jobs/W34-puffer-klein.md, R37, D66)

## PIG
- **Problem:** Die Puffer-Station T81 (2 IBC uebereinander, 2420 x 1920 x 2445 mm, 4,65 m2) passt nicht in den Dom (Laufwegkarte, D62). Pflicht im Dom sind laut R37 nur vier Dinge mit 0,16 m3 / ca. 0,4 m2: Messzelle 20 l, Stammloesungsfass 120 l (Base), Eisenchelat-Kanister 20 l, entchlortes Nachfuellwasser (Quelle). Das Drittbecken (Innen 1030 x 1130, 1,04 m2 mit Ring) ist fuer eine Quarantaene zu gross.
- **Intent:** Platz im Dom freigeben (Option A der R37), ohne die alte Station zu loeschen (Variante bleibt bis Bens Entscheidung).
- **Goal:** (1) Komponente `puffer_klein` (Fass 120 l opak, Messzelle 20 l Acryl abdeckbar mit 4 Sondenhalter-Stutzen d25, Kanister 20 l, 2 Schlauchpumpen, Stand), Grundflaeche <= 0,7 x 0,7 m, Hoehe < 1,3 m, Ports wie die Station, Blatt `docs/parts/puffer_klein.md`, Check ohne Interferenz; (2) Drittbecken 0,4 m3 (Wasser Ø 800 x 800 mm, Ring 60 mm); (3) Render mit Figur 1,80 m.

## Plan (ein WIP-Commit je Schritt)
1. `data/components/puffer_klein.json`, `scripts/workshop/puffer_klein.py`, `check_puffer_klein.py`: bauen und pruefen (Masse, Ports, Interferenz 0).
2. Blatt `docs/parts/puffer_klein.md` (partsheet) und `data/descriptions.json` (Gruppe `^puffer_klein`, vor `^puffer` einsortiert: `find` nimmt den ersten Treffer).
3. Drittbecken klein: Parameter, Bau, Check, Blatt `docs/parts/becken_dritt.md`.
4. Render mit Figur 1,80 m, archiviert; `docs/workshop-state.md` und `docs/workshop-log.md`.

## Abweichung vom Blatt (Grund)
`designs/components/becken_dritt.sc` wird von `scripts/gen_dome.py` (`pool_fn`, Parameter `pool3_d`/`pool3_depth` in `data/params.json`) erzeugt und hat gerade ungesicherte Aenderungen der Montage im Arbeitsbaum. Ich ueberschreibe sie nicht: Die Werkstatt baut `becken_dritt_klein.sc` als eigene Komponente (neue Datei, eigener Generator). Die Montage setzt danach `pool3_d` 800 und `pool3_depth` 800 oder verknuepft die neue Komponente.

## Stand
31.10.: puffer_klein T82 gebaut (32 Koerper, 700 x 700 x 1203, 43,8 kg), check_puffer_klein 51/51; becken_dritt_klein T14k gebaut (402 l, 0,66 m2), check 13/13; Blaetter `docs/parts/puffer_klein.md` und `becken_dritt_klein.md`, descriptions `^puffer_klein` vor `^puffer`; Bilder `renders/components/puffer_klein/puffer_klein-04-massstab.png` (Figur 1,80 m), `-01-schraeg`, `-03-schnitt` archiviert. Alte puffer_station/puffer_ibc unveraendert. Offen: Montage setzt pool3_d 800 / pool3_depth 920 oder verknuepft T14k; Sondenliste R39; Statik; Lichtschutz Messzelle.

## DoD
puffer_klein gebaut und Check gruen (Zahlen im Stand), Blaetter und descriptions nachgefuehrt, Drittbecken klein gebaut und geprueft, Render im Bildverlauf, WIP-Commits gepusht, workshop-state und workshop-log nachgefuehrt.
