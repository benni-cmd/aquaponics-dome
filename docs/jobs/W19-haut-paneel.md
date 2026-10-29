# W19 Haut-Paneel (Kuppelhaut) — klein anfangen (D35, R11)
Ziel: Komponenten fuer die dreieckigen Haut-Paneele der Kuppel samt Randprofil, nur die Komponenten (Einbau macht die Montage).
Eingaben: `docs/research/R11.md`, `data/layout.json` (dome: nodes_list, struts, strut_len_mm), `docs/jobs/README.md`, Standards. Keine weiteren Dateien.
Schritte (jeder fuer sich committen): (1) Dreieckstypen aus Knoten und Streben bestimmen (A/B-Kombinationen, Anzahl je Typ, Tuerfeld erkennen) und in `data/components/haut_paneel.json` ablegen; (2) EIN Paneel pro Typ als `haut_paneel_<typ>.sc`: Dreieck, Dicke 8, Rand 15 mm Abstand zur Strebenachse, Ports an den drei Kanten; (3) Randprofil `haut_profil.sc` (Aluminium-Kappe 30 x 8, Laengen 3279/3708) als Komponente; (4) Vorpruefung (Flaeche, Dicke, Kantenlaengen), ein Bild, Blatt mit Herkunft (E/A), kein Spec-Pruefer bis das Limit es erlaubt.
Nicht anfassen: dome.sc. Danach: Fertigmeldung in `docs/session-notes/orchestrator.md`.
