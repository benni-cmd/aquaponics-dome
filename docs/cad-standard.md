# CAD-Konstruktionsstandard (Fusion-360/SolidCraft-Praxis, verbindlich ab 29.10.2026)

Ben: ALLE Bauteile sind Komponenten; lose Einzelkoerper sind Anfaengerfehler. Arbeite wie ein erfahrener Fusion-360-/SolidCraft-Konstrukteur: Top-Down-Design, parametrisch, Baugruppenstruktur, Normteile, Stueckliste aus dem Modell. Dieser Standard geht `docs/detail-standard.md` voraus: erst die Struktur, dann die Details.

## 1. Baugruppenstruktur (Browser-Baum)

Wurzel `Kuppel_Aquaponik` enthaelt NUR Baugruppen und Komponenten, keine losen Koerper:
- `01_Layout` (Skelett: Referenzgeometrie und Parameter: Ringe, Sektoren, Achsen, Hoehenebenen, Azimute; alle Platzierungen leiten sich davon ab)
- `02_Gelaende` (Erdflaeche mit Aussparungen, Fundamentring, Fundamentanker)
- `03_Kuppel` (Streben A/B, Knoten 4/5/6-wertig, Haut, Tuer, Schrauben)
- `04_Wasserbecken` (Pool, zweites Becken, Wasserflaechen)
- `05_Beete` (Aussenbeet, Innenbeet, Kies, Siphon)
- `06_NFT` (Ring innen, Mitte, aussen: Tisch-Baugruppen mit Rinnen, Beinen, Verteilern)
- `07_Tanks` (Vortex klein, Biofilter gross, Plattform, Beine, Fittings)
- `08_Leitungen` (Rohre, Schlaeuche, Formstuecke, Ventile, Klemmen)
- `09_Technik` (Pumpen, Filtermodule, Schaltschrank)
- `10_Pflanzen` (Salatkopf, Topf, Pflanzen je Variante)

## 2. Komponenten-Regeln

1. **Eine Definition je Bauteilklasse** in `designs/components/<klasse>.sc`, im Dom per `component.insert_design` verknuepft; Instanzen per `occurrence.copy` oder `solid.pattern.*` (Parameter `components`). Aenderung der Datei, `component.update_links`: alle Instanzen folgen.
2. **Geschachtelte Baugruppen:** zusammengesetzte Teile sind Baugruppen aus Unterkomponenten (z. B. `NFT_Tisch` = Rinne x n + Bein x 4 + Querstrebe + Endkappe + Verteiler); die Baugruppe ist selbst verknuepft und wird instanziert.
3. **Kein Koerper im Wurzelknoten.** Pruefung: `component.list` zeigt in der Wurzel nur Komponenten; `component.copies` listet unverknuepfte Duplikate (muss leer sein).
4. **Position durch Layout, nicht durch Zahlen:** Instanzen werden nach `data/layout.json` (Ring, Sektor, Azimut, Radius, Z, yaw) platziert; Bauteil-Ursprung liegt am funktionalen Bezugspunkt (z. B. Mitte der Standflaeche), damit Platzierung ein Punkt plus Winkel ist.
5. **Parametrik:** zentrale Parameter (`parameters.add`, Quelle `data/params.json`), Skizzen voll bestimmt (Bemassung und Constraints), Features verweisen auf Parameter, keine Zahlen im Feature. Parametrisch aenderbare Varianten statt Kopien (z. B. Rinne mit Laengenparameter).
6. **Normteile:** Schrauben, Muttern, Scheiben, Stifte ueber `parts.insert` (z. B. M10 A2); Profile ueber `frame.profile.insert`; keine selbstgebauten Zylinder fuer Normteile.
7. **Verbindungen:** wo Teile gelenkig oder lagegebunden sind, Joints/Rigid-Gruppen statt freier Koordinaten (`component.unlock` nur bei Bedarf); grundgelegte Referenz (`grounded`) fuer das Layout.
8. **Benennung und Metadaten:** `<Nummer>_<Klasse>_<Variante>`; `component.metadata.set` mit part_number, description, revision, Werkstoff, Gewicht; ein Bauteilblatt `docs/parts/<klasse>.md` entsteht daraus.
9. **Material/Aussehen** je Komponente (gemeinsam fuer alle Instanzen), nicht je Koerperkopie; Wasserflaechen transparent.
10. **Tesselierung:** SolidCraft meshed jeden Koerper nach seiner Groesse; kleine gekruemmte Koerper wenige Facetten (Salatkopf aus wenigen Flaechen), sonst werden Exporte riesig.
11. **Stueckliste:** `assembly.bom` (levels: flat) ist die Quelle fuer `docs/bom.md`; Mengen = Instanzzahlen, muessen mit `layout.json` uebereinstimmen.

## 3. Reihenfolge der Umstellung (jetzt, vor weiterem Detail)

1. `01_Layout` aus `layout.json`/`params.json` erzeugen (Skelett-Komponente).
2. Pro Bauteilklasse eine Datei in `designs/components/` anlegen (Salatkopf, Strebe A/B, Knoten, Rinne, NFT-Tisch innen/mitte/aussen, Beet aussen/innen, Tank klein/gross, Pool, Zweitbecken, Plattform, Pumpe, Schaltschrank, Tuer, Fundamentanker, Erdflaeche) und im Dom verknuepfen.
3. Dom-Skript so umbauen, dass es nur noch verknuepft und platziert (Tabelle aus `layout.json`); die alten losen Koerper entfallen.
4. Neuen Test `scripts/check_components.py` anlegen: Wurzel ohne lose Koerper, jedes Bauteil eine verknuepfte Komponente, Instanzzahl je Klasse = `layout.json`, keine unverknuepften Kopien (`component.copies` leer), Stueckliste = Layout. Ergebnis in `renders/summary.json`.
5. Danach Detailstufen L2/L3/L4 je Komponente nach `docs/detail-standard.md`, im Gauntlet.
Ausnahme erlaubt nur mit Begruendung in `docs/decisions.md`, wenn SolidCraft im Headless-Lauf etwas nicht kann (zuerst ausprobieren, nicht annehmen); der Befund kommt nach `docs/solidcraft-components.md`.
