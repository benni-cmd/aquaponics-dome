# Start-Auftrag: Montage N-MODELL-KOMPLETT Schritt 3 (Strebe Vierkant einbauen, Werkstoffe anwenden)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Montage, einzige Sitzung, die das Gesamtmodell baut. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen. Nachtmodus D82: vor dem Build freier RAM >= 10 GB.

1. Grundlage: `docs/jobs/N-MODELL-KOMPLETT.md` Schritt 3 und Fallen im Start-Hinweis (Rollwinkel aus `data/components/knoten_arme.json`, erst Muster von 5 Streben messen; `strut_r` in `gen_dome.py:250` durch Achshoehen-Parameter ersetzen, Basisring/Tuer/Fundament Differenz 0,0 mm). Strebe-Bauteile sind fertig (bdaccb4).
2. Werkstoffe: nach `gen_dome.py` `python -X utf8 scripts/workshop/default_werkstoffe.py --apply` (oder Zuordnung in `component_file`), Ziel: eingesetzte Komponenten mit `Default` = 0 ausser Ausnahmeliste.
3. Build `sh scripts/build.sh` (Runde 70), `check_walkways.py` PASS, `check_huelle.py` Exit 0, Viewer-Export `python viewer/export_model.py` Exit 0. `check_latte` NICHT selbst laufen lassen (laeuft spaeter je Variante in einer Kopie).
4. Nicht anfassen: `data/leitungsnetz.json`, `data/leitungstrassen.json`, `data/beschaffung/`, `scripts/bom.py` (andere Sitzungen). Paket `docs/packages/n-modell-komplett.md`, `docs/loop-state.md` Runde 70 nachfuehren. Commits nur per Pfad, je Teilschritt, Push, WIP alle 20 Minuten. Danach STOPP mit Kurzmeldung.
