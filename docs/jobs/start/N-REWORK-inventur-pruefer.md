# Start-Auftrag: Pruefer N-REWORK Maengel-Inventur im Viewer (W71)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Pruefer, nur lesen, messen, Screenshots; schreibt nur `docs/model-maengel.md` und `renders/maengel/`. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Anlass (Ben 05.11., drei Viewer-Bilder): Absetzer/Vortex-Tank hat Durchbrueche in der Wand ohne Rohr (man sieht das Erdreich), Rohrleitungen laufen wirr und unrealistisch in Bogenketten, grosse Teile der Wasserversorgung fehlen.
2. Viewer eigener Port (`python viewer/serve.py <port>`, kein Export), Modell Runde 70. Je Bauteilgruppe (Filter/Becken/Tanks, Leitungen, Beete/Tische, Technik, Huelle) systematisch pruefen und mit Screenshot belegen: Durchbrueche/Stutzen ohne Anschluss, Rohrenden ins Leere, Rohre durch Bauteile, schwebende Teile, Bogenketten (mehr als 3 Boegen ohne Grund), kreuzende Leitungen im Gang, fehlende Halter, fehlende Verbindungen laut `data/leitungsnetz.json` (Kante ohne gebautes Rohr). Zusaetzlich per Skript: Ports der Bauteile (`docs/parts/*.md`, `data/components/*.json`) gegen gebaute Rohrenden (Abstand > 20 mm = offen).
3. Ergebnis `docs/model-maengel.md`: Tabelle je Mangel (ID, Bauteil, Art, Ort x/y/z, Bild, Vorschlag, Zustaendig Werkstatt/Montage/Planer), sortiert nach Schwere; Zusammenfassung, welche Maengel die A+-Kette (M10-S2N bis S7) ohnehin schliesst und welche eigene Fixes brauchen.
4. Kein Modellbau, kein Export, keine schweren CAD-Laeufe (Nachtmodus D82). Commit nur dieser Dateien per Pfad, Push. Danach STOPP mit Kurzmeldung.
