# N-DETAIL-PILOT Detailansicht im Viewer, Pilot fuer Feinfilter und Absetzer

Planer: Sonnet 5.5, 03.11.2026. Nur gelesen und gemessen, kein Modell, keine Daten, nicht `data/roadmap.json`, nicht der Viewer geaendert. Mini-Plan: `docs/packages/n-detail-pilot.md`. Grosses Paket dahinter: `docs/packages/bauanleitung-teileliste-detailansicht.md` (B1 bis B5, wird hier nur fuer zwei Bauteile vorgezogen).

**Problem:** Ben kann die Funktion eines Bauteils im Viewer nicht beurteilen: er sieht nur die Huellform (Feinfilter 55 Koerper, Absetzer 33), nicht welches Teil was tut, woraus es ist und wie es zusammengesteckt ist. Teile-Datenmodell, benannte Einzelkoerper im Export und die Detailansicht fehlen (alle B1 bis B3 "noch nicht begonnen"). **Intent:** Ben (03.11.2026, Wunsch D56): "Dateiansicht/Detailansicht fertig machen, dann koennen wir Sachen wie die Filter, oder danach Subtanks, besser beurteilen mit ihrer Funktion." **Ziel in einem Satz:** Rechtsklick auf Feinfilter oder Absetzer im Viewer, Menue "Detailansicht", Explosionsdarstellung mit Schieber, Teileliste, Klick auf ein Teil zeigt eine Infokarte (was, Werkstoff, Funktion, Eigenschaften, Norm, Lebensmittelkontakt), "Zurueck" kehrt zum Gesamtmodell zurueck; das Detailmodell wird erst beim Klick geladen und der Hauptexport waechst nicht.

## Aktualitaetspruefung (03.11.2026, Regel W44)
Ergebnis: **angepasst** (Plan gilt als freigegeben, mit den Anpassungen unten).
- Roadmap: `N-DETAIL-PILOT` (geplant, Reihenfolge 3,78, "Planer (Blatt), dann Werkstatt + Viewer, dann Pruefer"), `N-DETAIL` (B2/B3, nach Zwischencheck), `N-KATALOG` (B4 + B1, nach Zwischencheck) und `V-MESS` (Viewer, vor Zwischencheck, Reihenfolge 10, schliesst L18 mit) gelesen. Der Pilot zieht von N-KATALOG und N-DETAIL nur das Noetige vor; beide bleiben bestehen und bauen auf dem Pilot-Muster auf.
- `docs/decisions.md`: D56 (Teileliste, Detailansicht, Grundsatz 6 "Koerperzahl = Teilezahl") und D65 (Messstellen als Teile und eigene Ebene, spaeter in der Detailansicht) gelten; D73/D74 sind Verfahren; **D75 (Subtank V4, 03.11.)** ist die Anpassung: der Feinfilterkasten wird mit M10-S2V durch einen Subtank ersetzt (der Siebkorb bleibt als eigenes Bauteil `siebkorb`, `docs/jobs/M10-S2V.md` Abschnitt Neue Bauteile). Der Pilot an `feinfilter` bleibt trotzdem sinnvoll: Ben will die Filterfunktion JETZT beurteilen, der Siebkorb-Teil der Teileliste wird 1:1 fuer `siebkorb` wiederverwendet, und das Muster ist der eigentliche Gewinn. M10-S2V ist geparkt (Roadmap), `designs/components/feinfilter.sc` bleibt bis dahin im Modell.
- `git log --oneline -15` (HEAD 57b01e0 "N-DETAIL-PILOT angelegt"): alle Commits sind Recherche R47c bis R49, Stationen-Artefakt, E21/D75, Roadmap-Stand; keiner aendert `viewer/`, `designs/components/feinfilter.sc`, `tank_klein.sc` oder `scripts/workshop/tank.py`/`feinfilter.py`. `git status`: `feinfilter.sc` und `tank_klein.sc` sind sauber (nicht unter den fremden Aenderungen). Fremde unversionierte Aenderungen liegen in `designs/components/{becken_dritt,erdflaeche,fundamentring,haut_paneel_BBB,pool_zentral,schaltschrank,strebe_a,strebe_b,tuer,zulaufrohr,zweitbecken}.sc`, `data/roadmap.json`, `viewer/extras.json` und `renders/section-61.png`: **nie committen, nie anfassen**.
- Parallel laufend (nur Recherche, schreiben nur `docs/research/`): R50 (Fein- und Vortexfilter, Standardgeraete) und R51 (Beet-Siphon). Kein Dateikonflikt; Ergebnisse fliessen spaeter ein (Abschnitt "Wie R50 und R51 einfliessen").
- **Gemessene Praezisierungen gegen den Auftragstext:** (1) `docs/ui-standard.md` liegt NICHT im Projekt, sondern im Workspace (`..\..\docs\ui-standard.md`, 7 Punkte, geschrieben fuer das Dashboard mit `HD.*`-Bausteinen); im Viewer gibt es diese Bausteine nicht, die Punkte gelten sinngemaess (Abschnitt Pruefung). (2) D56 Grundsatz 6 "Zahl Koerper = Zahl Teile" gilt nicht woertlich: Feinfilter hat 55 Koerper, aber nur etwa 20 Teile (4 Beine = ein Teil mit Menge 4). Die messbare Fassung lautet: **jeder Koerper des `.sc` steht in genau einer Teilezeile, und die Summe der Koerper je Zeile ist die Koerperzahl** (Abschnitt Datenformat). (3) Der Katalog heisst im Gross-Paket `data/katalog.json`; der Pilot schreibt genau diese Datei mit `"stand": "pilot"`, damit N-KATALOG sie nur erweitert und nichts umbenennt.

## Eingaben (nur diese; Zeilen selbst nachsehen)
- `docs/packages/bauanleitung-teileliste-detailansicht.md`: Tabelle B1 bis B5 (Zeilen 16 bis 28), Abhaengigkeiten (Zeile 30), offene Frage 3 Optik der Detailansicht (Zeile 39: erst Funktion, dann Politur).
- `designs/components/feinfilter.sc` und `tank_klein.sc` (ZIP-Dateien: `document.json` mit `materials` Koerper -> Werkstoff, `cache/model.json`); Koerperliste per `solidcraft-cli.exe eval <datei> --json-out <ausgabe>` (Felder `name`, `bbox`, `material`, `mass_g`, `volume_mm3`). Gemessen 03.11.: Feinfilter **55 Koerper**, alle benannt (`Bein_1`, `Korbgewebe`, `Spannhebel_1`, ...); Absetzer **33 Koerper**, davon **8 unbenannt** (`Body1` bis `Body8`: M8x30-Sechskantschrauben der Fussplatten, Material "Default", je 3 g, bbox z -24 bis 11).
- `scripts/workshop/feinfilter.py` (Funktionen `box`, `tube`, `sqtube`, `build` ab Zeile 74; 3 Zeilen mit `body_name=`, der Rest ueber diese Helfer), `scripts/workshop/tank.py` (`body_name=` ab Zeile 70; **Zeile 207**: `parts.insert family="hex_bolt" size="M8" length=30 name=f"Schraube_{i}_{int(hx)}"` ist der Feature-Name, der Koerper heisst trotzdem `Body<n>`), `scripts/workshop/sc.py` (`assign_part_materials` Zeile 95: bekannter Umgang mit `Body<n>`; `evaluate` Zeile 42; `Check` Zeile 73), `scripts/workshop/check_feinfilter.py` und `check_tank.py` (Vorbild fuer `check_parts.py`; `check_tank.py` Zeile 173 schliesst Namen mit Praefix `Schraube` bereits aus der Interferenzpruefung aus).
- `data/components/feinfilter.json` (Parameter mit Herkunft `[E]/[A]`, Siebflaeche 0,840 m2, Korb 560 x 370 x 400) und `data/components/tank.json` (`typen.klein`: R 336,5, H 1075, Wand 4, Leitrohr, Plattform 619); `docs/parts/feinfilter.md` (Funktion Zeile 3, Masse-Tabelle ab Zeile 14) und `docs/parts/tank.md` (Funktionstext Zeile 51 bis 57) als Textquelle fuer die Infokarten (nicht neu erfinden, abschreiben und Marke uebernehmen).
- `viewer/index.html` (494 Zeilen; Klick-Auswahl Zeile 356 bis 363 mit `hit.object.userData.def` = Definitionsname; Laden Zeile 370 bis 392 mit `loader.parse`; Infofeld `showInfo` Zeile 258; Farben `colorFor` Zeile 152; Schaltflaechen Zeile 69 bis 77; three.js 0.160 per importmap Zeile 56; **kein** `contextmenu` bisher), `viewer/export_model.py` (Zwischenspeicher `defs/.cache.json`, `MIN_DIAG = 150`, Aufruf `solidcraft-cli.exe eval` und `file.export format=obj bodies=[...]`; die OBJ-Datei traegt je Koerper eine Zeile `o <Name>`), `viewer/serve.py` (`translate_path` reicht `descriptions.json` und `system-specs.json` aus `data/` durch, Muster fuer `/parts/` und `/katalog.json`), `viewer/instances.json` (152 Definitionen, 272,5 MB OBJ, 4880 Instanzen; `defs/` gesamt 316,4 MB, Hauptexport-Ausgangswert fuer Pruefpunkt 2; Instanzen `Feinfilter:1/2`, `Tank_klein:1/2`).
- Zum Vergleich der Rechtslage: `docs/jobs/M10-S2V.md` Abschnitt Neue Bauteile (`siebkorb`, `subtank`, `tauchpumpe` entstehen als neue `.sc`; sie bekommen dasselbe Muster).

## Machbarkeit (Befund mit Datei und Zeilen)
- **Feinfilter: sofort exportierbar, nichts umzubenennen.** Alle 55 Koerper tragen Namen aus `feinfilter.py` (`box`/`tube`/`sqtube` setzen `body_name`); gemessen mit `solidcraft-cli.exe eval designs/components/feinfilter.sc`. 24 der 55 Koerper liegen unter `MIN_DIAG` 150 mm (Spannbeschlaege, Hebel, Stabe, Tuellen) und fehlen deshalb in `viewer/defs/feinfilter.obj` (31 Objekte, 2,1 MB): der **Detailexport muss `MIN_DIAG = 0` setzen**, nicht der Hauptexport.
- **Absetzer: 8 Koerper muessen umbenannt werden.** `scripts/workshop/tank.py:207` (`parts.insert`) erzeugt `Body1` bis `Body8`; das ist dasselbe Muster wie bei der Pumpe (`pumpe.py:49-51, 94`). Aufgabe der Werkstatt: nach dem Einfuegen umbenennen in `Schraube_<Fussplatte>_<x>` (gleiches Schema wie der Feature-Name im Code), entweder per Befehl `describe_command`/`list_commands` (ein Umbenennen-Befehl fuer Koerper ist zu pruefen) oder durch Erweiterung von `sc.assign_part_materials` um eine Namenszuweisung (Reihenfolge der Koerper = Reihenfolge der `parts.insert`-Aufrufe, per bbox gegen `legs` und `hx/hy` zu kontrollieren, nicht zu raten). Material von "Default" auf "Stahl verzinkt" setzen (gleiche Funktion). Die uebrigen 25 Koerper tragen Namen (`Tank`, `Deckel`, `Zulaufrohr`, `Leitrohr`, `Auslaufrohr`, `Schlammstutzen`, `Kugelhahn`, `Ablaufstutzen`, `Plattform`, `Bein_1..4`, `Fussplatte_1..4`, `Strebe_1..4`, `Diagonale_1..4`). `tank.py` baut auch `tank_gross` und `tank_gross_t3`: die Namensaenderung wirkt dort mit; Pilot baut nur `tank_klein` neu, `tank_gross*` zieht beim naechsten Tank-Lauf nach (kein Widerspruch, `check_tank.py` prueft alle drei).
- **Kein dome-Build noetig.** Der Detailexport liest die Bauteil-`.sc` direkt (wie `export_model.py`); `designs/dome.sc` und `viewer/instances.json` bleiben unberuehrt. Der naechste Montage-Build zieht die neuen Namen von selbst mit (die Schrauben sind unter `MIN_DIAG`, die Hauptdefinition aendert sich nicht).
- **Offen/Risiko:** (a) Tessellierung richtet sich nach der Koerpergroesse (Kommentar `export_model.py` Zeile 4): kleine Teile sind billig, aber 55 Koerper mit Stuetzrahmen koennen die Detail-OBJ groesser machen als 2,1 MB; Sollwert Pruefpunkt 3 (hoechstens 10 MB je Detail-OBJ) wird gemessen. (b) Umbenennen per Skript speichert die `.sc` neu: danach `check_tank.py` und `check_feinfilter.py` unveraendert gruen.

## Schritte (einzeln committbar; Rolle, Reihenfolge)
**Schritt 1, Werkstatt A (1 Sitzung, Sonnet): Daten.** Commits einzeln, je mit Pfad:
- 1a. `scripts/workshop/tank.py` (+ ggf. `sc.py`): Schrauben benennen und Material setzen; `tank_klein.sc` neu bauen (`check_tank.py` gruen, Koerperzahl 33 mit 0 Namen `Body<n>`); Commit `designs/components/tank_klein.sc` + Skripte (nur diese Pfade).
- 1b. `data/katalog.json` (`"stand": "pilot"`): nur Eintraege, die die zwei Bauteile brauchen: Werkstoffe (PP, PE, PVC-U, Edelstahl 1.4301, Edelstahl-Gewebe 100 Mikrometer, Stahl verzinkt, EPDM), Profile (Vierkantrohr 40x40x3), Rohre (PVC-U d25/d40/d50/d63/d110), Normteile (Sechskantschraube M8x30 ISO 4017, Kugelhahn PVC-U). Je Eintrag `id`, `name`, `norm`, `lebensmittelkontakt`, `pilot: true`, Quelle und Marke. Keine Preise, keine Lagerlaengen (das ist B4).
- 1c. `data/parts/feinfilter.json` (alle 55 Koerper in rund 20 Teilen) und `scripts/workshop/check_parts.py <komponente...>` (Pruefpunkt 1); Commit zusammen, damit der Check mitkommt.
- 1d. `data/parts/tank_klein.json` (33 Koerper in rund 14 Teilen); Commit.
- 1e. Bauteilblaetter `docs/parts/feinfilter.md` und `tank.md` werden von `partsheet.py` aus `data/components/*.json` erzeugt und sind hier **nicht** zu aendern; die Infokarten-Texte werden von dort abgeschrieben.

**Schritt 2, Viewer-Sitzung (1 Sitzung, ggf. 2; Sonnet, Aufwand hoch fuer die UI):**
- 2a (parallel zu 1b bis 1d moeglich, eigene Dateien): `viewer/export_detail.py <komponente>`: liest `data/parts/<komponente>.json` (Feld `datei` = `.sc`-Pfad), Koerperliste per `eval`, exportiert **alle** Koerper mit `file.export format=obj` nach `viewer/detail/<komponente>.obj` (Zwischenspeicher nach Aenderungszeit wie `export_model.py`) und schreibt `viewer/detail/<komponente>.json` (je Koerper `name`, `material`, `farbe`, `masse_g`, `bbox`). Farben: Werkstoff -> Farbe aus einer festen Tabelle im Skript (aus `document.json` `materials`). Bricht mit Fehler ab, wenn Koerpernamen im `.sc` fehlen oder in `data/parts` doppelt/zu viel sind. `export_model.py` und der Auto-Export in `serve.py` bleiben **unveraendert** (Detail wird per Hand oder per Befehl neu gebaut, nicht bei jedem Speichern); `serve.py` bekommt nur zwei Durchreichen in `translate_path`: `/parts/<name>.json` -> `data/parts/` und `/katalog.json` -> `data/katalog.json`.
- 2b (braucht 1c, Feinfilter-Daten): `viewer/index.html`: Rechtsklick-Menue, Detailszene, Schieber, Teileliste, Infokarte, Zurueck (Abschnitt UI). Zuerst mit Feinfilter, dann mit tank_klein (nach 1d).
- 2c: Bilder und Pruefpunkte 2 bis 4 selbst durchlaufen, bevor der Pruefer kommt (Screenshot ist Pflicht, `working-method.md`).

**Schritt 3, Pruefer (1 Sitzung, nach `docs/jobs/vorlagen/pruefung.md`, nie die Bau-Sitzung):** Pruefpunkte unten selbst ausfuehren, Befund in `docs/jobs/pruefung/N-DETAIL-PILOT.md`.

**Was parallel laeuft und was nicht:**
- Parallel: 1b bis 1d (Werkstatt, Dateien `data/`, `scripts/workshop/`, `designs/components/tank_klein.sc`) mit 2a (Viewer, Dateien `viewer/export_detail.py`, `viewer/serve.py`); R50 und R51 (nur `docs/research/`); W37 (Werkstatt B, andere Bauteile; Pilot fasst `sc.py` nur an, wenn der Umbenennen-Befehl fehlt, dann W37 vorher fragen/nachziehen lassen, sonst keine Ueberschneidung).
- Nicht parallel: 2b nach 1c (echte Daten), tank_klein-Test nach 1d. **`V-MESS` (ebenfalls `viewer/index.html`) und `N-DETAIL` duerfen nicht gleichzeitig mit 2b laufen:** erst Pilot, dann V-MESS (Reihenfolge 10 gegen 3,78 passt). Ein dome-Build der Montage darf laufen, er beruehrt `viewer/defs/` und `instances.json`, nicht `viewer/detail/`.
- `data/descriptions.json` bleibt **unveraendert** (das alte Infofeld `showInfo` zeigt weiter die Gesamtbeschreibung; die Infokarte der Detailansicht liest nur `data/parts/*.json`). So gibt es keine Kollision mit Orchestrator, W37 oder Specs-Seiten.

## Datenformat-Vorschlag `data/parts/<komponente>.json` (Komponente = Definitionsname im Viewer: `feinfilter`, `tank_klein`)
Kopf:
```json
{
  "komponente": "feinfilter",
  "datei": "designs/components/feinfilter.sc",
  "teilenummer": "T55",
  "stand": "pilot",
  "titel": "Feinfilter (Hauptstrom, Siebkorb 100 Mikrometer)",
  "kurz": "Der Behaelter nimmt das Wasser einer Linie auf. Es laeuft durch den Siebkorb, der Schwebstoffe ab 100 Mikrometer zurueckhaelt.",
  "koerperzahl": 55,
  "gruppen": [{"id": "siebkorb", "name": "Siebkorb", "teile": ["korbgewebe", "korbflansch", "korbstab", "korbrahmen", "korbgriff"]}],
  "teile": [ ... ]
}
```
Felder je Teil (B1, erweitert um die Pflicht aus D56 Grundsatz 6 und die Explosion):
`id` (kurz, eindeutig) · `name` (deutsch, ein Satz taugt als Ueberschrift) · `koerper` (Liste der Koerpernamen im `.sc`, Pflicht, jeder Name im ganzen File genau einmal) · `menge` (= Laenge von `koerper`, wird geprueft) · `typ` (`profil`, `platte`, `rohr`, `normteil`, `sonderteil`) · `werkstoff` (Katalog-ID) · `masse_mm` (Text oder Objekt, aus den Parametern von `data/components/<komponente>.json`, mit Parametername) · `funktion` (ein bis zwei Saetze, ausformuliert) · `eigenschaften` (Liste kurzer Saetze, je Zahl mit Einheit) · `norm` (Katalog-ID oder Text, `null` wenn keine) · `lebensmittelkontakt` (`ja` / `nein` / `offen`) · `konfidenz` (`belegt` / `gerechnet` / `angenommen`, Wort statt nur Farbe, entspricht `[B]/[E]/[A]` im Repo) · `quelle` (Datei oder Blatt, aus dem der Wert stammt) · `explosion`.
`explosion` (aus den Daten, nicht aus dem Viewer): `{"richtung": [x,y,z] | "radial", "abstand_mm": Zahl, "folgt": "<teil-id>" (optional)}`.
- Achsen wie im Bauteil (Z oben, Ursprung Mitte Standflaeche). Verschiebung eines Koerpers bei Schieberstand s (0 bis 1) = normierte Richtung x abstand_mm x s; `folgt`: die Verschiebung des genannten Teils wird zuerst addiert, damit z. B. die Spannverschluesse mit dem Deckel nach oben wandern und dann weiter nach aussen. Reihenfolge: ausbaubar zuerst, wie man es von Hand abbaut (Siebkorb nach oben, dann Deckel, dann Dichtung).
- `"radial"` = Richtung vom Koerpermittelpunkt der Bauteil-Achse (x=0, y=0) nach aussen in der XY-Ebene, vom Viewer aus der bbox des Koerpers gerechnet; fuer vier gleiche Teile (Beine, Fussplatten, Schrauben).
- Fehlt `explosion`, bleibt das Teil in Ruhe (z. B. der Behaelter als Bezugsteil).

Beispiel Feinfilter-Siebkorb (Werte aus `data/components/feinfilter.json` und `docs/parts/feinfilter.md`; Normverweise und Lebensmittelkontakt sind `[A]` bis R31/B6 sie belegt):
```json
{
  "id": "korbgewebe",
  "name": "Siebgewebe des Korbs",
  "koerper": ["Korbgewebe"],
  "menge": 1,
  "typ": "sonderteil",
  "werkstoff": "edelstahl_gewebe_100um",
  "masse_mm": "560 x 370 x 400 (Parameter basket_l, basket_w, basket_d)",
  "funktion": "Das Gewebe haelt Schwebstoffe ab 100 Mikrometer zurueck; das Wasser tritt durch Boden und Seitenwaende in die Ablaufkammer, der Schmutz bleibt im Korb.",
  "eigenschaften": ["Benetzte Siebflaeche 0,840 m2 bei Soll 0,825 m2 (Strom 110 l/min, Siebbelastung 7,86 m/h).", "Maschenweite 100 Mikrometer; im Versuch von Mortensen hielt das Gewebe 21 Prozent der Schwebstoffe zurueck (R30).", "Im Modell eine 1-mm-Huelle mit Ersatzdichte 0,55 g/cm3, damit die Masse zum echten Gewebe (0,5 kg/m2) passt."],
  "norm": "Drahtgewebe nach DIN ISO 9044 (Maschenweite 100 Mikrometer) [A]",
  "lebensmittelkontakt": "ja",
  "konfidenz": "gerechnet",
  "quelle": "data/components/feinfilter.json (basket_*, mesh_*), docs/parts/feinfilter.md, docs/research/R30.md",
  "explosion": {"richtung": [0, 0, 1], "abstand_mm": 700}
},
{
  "id": "korbstab",
  "name": "Stuetzstab des Korbrahmens",
  "koerper": ["Korbstab_1", "Korbstab_2", "Korbstab_3", "Korbstab_4"],
  "menge": 4,
  "typ": "profil",
  "werkstoff": "edelstahl_1_4301",
  "masse_mm": "Flachstab 8 x 8 (Parameter rod)",
  "funktion": "Die vier Staebe halten das weiche Gewebe in Form, damit der Korb beim Herausheben nicht einknickt.",
  "eigenschaften": ["Edelstahl 1.4301, Querschnitt 8 x 8 mm."],
  "norm": "Werkstoff 1.4301 nach EN 10088-2 [A]",
  "lebensmittelkontakt": "ja",
  "konfidenz": "angenommen",
  "quelle": "data/components/feinfilter.json (rod: [A])",
  "explosion": {"richtung": [0, 0, 1], "abstand_mm": 700, "folgt": null}
}
```
Anmerkung zum Pruefsatz: Menge, `koerper` und Koerperzahl im Kopf stimmen nur zusammen, wenn **jeder** `.sc`-Koerper in genau einem Teil steht (55 / 33); Teile mit Menge 4 (Bein, Fussplatte, Spannverschluss mit Bock und Hebel, Schraube) tragen alle vier Namen.
Wie die Gruppierung aussieht (Vorschlag, die Werkstatt prueft gegen die Koerperliste, ob eine andere Aufteilung natuerlicher ist): **Feinfilter** Standrahmen (Bein 4, Fussplatte 4, Ring 4, Stege), Behaelter, Siebkorb (Flansch, Gewebe, Staebe 4, Rahmen 4, Griffe 2), Deckel (Deckel, Deckelgriff, Dichtung), Spannverschluss (Bock 4, Hebel 4), Einlaufrohr, Auslauf (Rohr, Flansch innen, Mutter aussen), Ablass (Stutzen, Kugelhahn, Hebel, Tuelle), Spuelanschluss (Stutzen, Kugelhahn, Hebel, Tuelle, Spritzrohr). **Absetzer** Tank, Deckel, Zulaufrohr, Leitrohr, Auslaufrohr, Schlammablass (Stutzen, Kugelhahn, Ablaufstutzen), Plattform, Bein 4, Fussplatte 4, Schraube 8, Strebe 4, Diagonale 4. Die Gruppen steuern nur die Klappgruppen der Teileliste und gemeinsame Explosionsschritte.

## UI-Skizze (in Worten) und Pruefung nach `docs/ui-standard.md`
- **Einstieg:** Rechtsklick auf eine Feinfilter- oder Absetzer-Instanz (die vorhandene Klickauswahl trifft `hit.object.userData.def`): Menue mit einer Zeile "Detailansicht" an der Mausposition; fuer Bauteile ohne `data/parts/<def>.json` steht dort grau "Detailansicht (noch keine Teiledaten)". Zusaetzlich eine Schaltflaeche "Detailansicht" im Infofeld, sobald eine Instanz ausgewaehlt ist (fuer Touch und fuer den Fall, dass ein Browser das Kontextmenue abfaengt). Im FPV-Modus aus.
- **Detailszene:** Erst jetzt werden `viewer/detail/<def>.obj`, `.json` und `/parts/<def>.json` geladen (Pruefpunkt 3). Das Gesamtmodell wird ausgeblendet, das Detailmodell steht im Bauteilkoordinatensystem, die Kamera fliegt auf dessen bbox und merkt sich die vorige Kamera. Farben je Werkstoff aus `detail/<def>.json`.
- **Explosions-Schieber** (Bereich, Beschriftung "Zusammengebaut" links, "Auseinander" rechts, Standard 0, einmal "Animieren" als Textschaltflaeche); die Verschiebung kommt nur aus `explosion` der Teile (Formel oben).
- **Teileliste** in der linken Spalte (dort, wo sonst der Baum steht): je Gruppe aufklappbar, je Zeile Name, Menge und Werkstoff in Worten; Hover auf Zeile hebt die Koerper des Teils im Modell hervor, Klick waehlt das Teil (und umgekehrt: Klick auf einen Koerper im Modell waehlt die Zeile).
- **Infokarte** rechts im bestehenden Infofeld: Titel (Teilname), Satz "Was es ist" (Typ, Menge), Funktion als Satz, Werkstoff, Masse (aus Modell: Summe `mass_g`), Eigenschaften als kurze Saetze, Norm, Lebensmittelkontakt als Wort (Ja/Nein/Offen) und Konfidenz als Wort (belegt/gerechnet/angenommen), Quelle als Satz.
- **Zurueck:** Textschaltflaeche "Zurueck zum Gesamtmodell" oben in der Detailszene (und Esc); Hauptmodell und Kamera wie vorher, Detailgeometrie wird freigegeben (`dispose`).
- **Pruefung nach den 7 Punkten:** (1) Saetze statt Fragmente: Funktion und Eigenschaften sind ausgeschriebene Saetze (`check_parts.py` meldet Eigenschaften ohne Verb/Einheit nicht, das prueft der Mensch am Screenshot). (2) Ein Vokabular: Infokarte benutzt die vorhandenen Klassen des Viewers (`.k`, `.badge`, `.note`, `.src`) und mischt keine neuen. (3) Status als Wort: Konfidenz und Lebensmittelkontakt als Wort mit Marke, nie Farbe allein. (4) Etablierte Bausteine: bestehendes Infofeld und Baum-Stil wiederverwenden. (5) Kein Unicode-Symbol statt Icon (kein Pfeil/Kreuz als Zurueck oder Schliessen; Text oder SVG). (6) Keine verbotenen Woerter (Brett, Posten, Rubrik, Marke, Kennung, ...; `Marke` darum im UI nicht benutzen, "Kennzeichnung" sagen). (7) **Screenshot im Browser ist Pflicht** (`mcp__Claude_Browser__*`, Bilder nur an Stellen, die ein Pruefpunkt nennt): Feinfilter zusammengebaut, gesprengt (Schieber 1), Infokarte des Siebkorbs; Absetzer gesprengt. Die Punkte sind fuer das Dashboard geschrieben und im Viewer sinngemaess [A] uebertragen; der Pruefer bewertet die Optik gegen diese sieben Punkte.
- **Umfang bewusst klein (Frage 3 im Gross-Paket: erst Funktion, dann Politur):** keine Beschriftungslinien, keine Animationspolitur, keine Schnittansicht, keine Stuecklisten-Summen, kein Bauanleitungsschritt.

## Nicht anfassen
`data/roadmap.json`, `data/leitungsnetz.json`, `data/descriptions.json`; `designs/dome.sc`; `viewer/export_model.py` und die Auto-Export-Schleife in `viewer/serve.py` (nur zwei `translate_path`-Zeilen ergaenzen); alle fremden unversionierten Dateien (Liste oben); `designs/components/*.sc` ausser `tank_klein.sc` (Schritt 1a); `docs/parts/*.md` (erzeugt); `scripts/gen_dome.py`, Netzliste, Trassen; M10-S2V-Dateien; Recherche-Ergebnisse R50/R51 (nur lesen, wenn fertig).

## Wie R50 und R51 einfliessen (ohne dass der Pilot wartet)
- Der Pilot schreibt Werte nur aus dem, was im Repo steht (`data/components/*.json`, `docs/parts/*.md`, R30) und markiert jeden Wert mit `konfidenz`. R50 (`docs/research/R50-fein-und-vortexfilter.md`, Standardgeraete) liefert spaeter Handelsteile, Kennzahlen und Normverweise; sie kommen **in dieselben Felder** (`werkstoff`, `norm`, `eigenschaften`, `quelle`) plus ein optionales Feld `handelsteil` (`{"hersteller": ..., "typ": ..., "quelle": ..., "stand": "Datum"}`), das der Pilot leer laesst. Ein Folgeschritt `N-DETAIL-R50` (Werkstatt, klein, nach R50 und dem Pruefer) aendert nur `data/parts/feinfilter.json`, `tank_klein.json` und `data/katalog.json`, nie den Viewer. Gilt das Schema unveraendert, ist der Viewer nicht beteiligt (Pruefpunkt: Viewer-Code nennt keine Komponentennamen).
- R51 (Beet-Siphon) und der Subtank (M10-S2V: `subtank`, `siebkorb`, `tauchpumpe`) bekommen **je eine neue `data/parts/<komponente>.json`** nach demselben Schema, sobald das jeweilige `.sc` existiert; der Siebkorb-Teil wird aus `feinfilter.json` kopiert (Gruppe `siebkorb` ist dafuer eigene Gruppe). Pumpe (`pumpe_klein`, `pumpe_gross`, auch dort `Body<n>`) folgt gleich: erst Koerper benennen, dann Parts. Das ist der Kern von N-KATALOG/N-DETAIL: der Viewer-Code aus dem Pilot muss dafuer **nicht** angefasst werden.

## Ergebnis
Dateien nach Schritt 1/2: `data/katalog.json` (Stand Pilot), `data/parts/feinfilter.json`, `data/parts/tank_klein.json`, `scripts/workshop/check_parts.py`, geaenderte `scripts/workshop/tank.py` (+ ggf. `sc.py`), `designs/components/tank_klein.sc`, `viewer/export_detail.py`, `viewer/serve.py` (2 Zeilen), `viewer/index.html` (Detailansicht), `viewer/detail/*.obj|json` (erzeugt; **nicht committen**, in der Pruefung nachbauen), Bilder unter `renders/` nur zur Abnahme (**nicht committen**), `docs/packages/n-detail-pilot.md` nachgefuehrt. Mit den Dateien aus Schritt 1 und 2 ist das Muster fuer Subtank, Siphon und Pumpen in je einer kleinen Werkstatt-Sitzung (nur Daten) nachbaubar.

## Pruefpunkte (fuer die fremde Pruef-Sitzung nachmessbar)
1. **Koerper vollstaendig zugeordnet:** `python -X utf8 scripts/workshop/check_parts.py feinfilter tank_klein` endet mit Exit-Code 0; Ausgabe nennt 55 Koerper (feinfilter) und 33 Koerper (tank_klein), jeder Koerpername aus `solidcraft-cli.exe eval` genau einmal in `koerper`, `menge` gleich Laenge von `koerper`, kein Name der Form `Body<Zahl>`, alle Pflichtfelder (`name`, `werkstoff`, `funktion`, `eigenschaften`, `norm`, `lebensmittelkontakt`, `konfidenz`, `quelle`) gefuellt.
2. **Hauptexport waechst nicht:** Summe der Dateigroessen `viewer/defs/*.obj` nach dem Pilot gleich 316,4 MB +- 1 % (Messung: `python -c "import os;print(sum(os.path.getsize('viewer/defs/'+f) for f in os.listdir('viewer/defs'))/1e6)"`), `viewer/instances.json` weiter 152 Definitionen und 4880 Instanzen; die Detaildateien liegen nur in `viewer/detail/`, jede `.obj` hoechstens 10 MB.
3. **Detailmodell laedt erst beim Klick:** im Browser (`read_network_requests`, Filter `detail`) bis zum Klick auf "Detailansicht" kein Request auf `detail/` oder `/parts/`; danach genau je eine `.obj`, `.json` und `/parts/<def>.json`; `grep -c "^o " viewer/detail/feinfilter.obj` = 55, bei `tank_klein` = 33.
4. **Funktion und Optik (Screenshot gegen `docs/ui-standard.md`):** bei Schieber 0 gleicht die Bounding-Box der Detailgruppe der bbox der `.sc`-Koerper (+-1 mm, per `javascript_tool`); bei Schieber 1 ist der Siebkorb ueber dem Deckel und die Koerper der Teile mit `folgt` stehen ueber ihrem Bezugsteil; Klick auf die Zeile "Siebgewebe" zeigt Werkstoff, Funktion, Norm, Lebensmittelkontakt als Worte; "Zurueck" stellt Gesamtmodell und Kamera wieder her (Kamera-Position gleich +-1 mm). Mindestens vier Screenshots (Feinfilter zusammen/gesprengt/Infokarte, Absetzer gesprengt), vom Pruefer mit dem Read-Werkzeug angesehen und gegen die sieben Punkte bewertet.
5. **Muster wiederverwendbar:** `grep -nE "feinfilter|tank_klein" viewer/index.html` trifft keinen Komponentennamen (alles ueber `data/parts/<def>.json`); eine dritte Datei `data/parts/<neu>.json` im gleichen Schema laesst sich ohne Aenderung am Viewer laden (Probe: kopierte Mini-Datei mit einem Koerper, danach wieder loeschen).

## Kosten und Sitzungen (Schaetzung nach `docs/jobs/kosten.md`)
Werkstatt A: 1 Sitzung (etwa 300 bis 450 Nachrichten; wird sie zu lang, Schritt 1d als zweite). Viewer: 1 bis 2 Sitzungen (UI-Teil etwa 400 bis 600 Nachrichten; 2a kann die Werkstatt-Wartezeit ausfuellen). Pruefer: 1 Sitzung (etwa 100 Nachrichten). Gesamt **3 bis 4 Bau-/Pruefsitzungen**, kein dome-Build.

## Offen
- OFFEN (Ben): Soll die Detailansicht im Pilot ausser Feinfilter und Absetzer auch den Biofilter (`tank_gross`, selber Generator, selbe Namensaenderung) bekommen? Vorschlag: nein, erst nach dem Pilot-Test (Frage 3 im Gross-Paket: erst Funktion, dann Politur).
- OFFEN (Ben): Normverweise und Lebensmittelkontakt sind `angenommen`, bis R31/B6 und R50 sie belegen; Ben muss vor einer Bauentscheidung nicht darauf warten, die Infokarte zeigt das Wort "angenommen".
- Montage/Orchestrator (kein Ben): `V-MESS` hinter den Pilot stellen (gleiche Datei `viewer/index.html`); L18 (Export 212 MB, Ziel 40 MB) bleibt bei V-MESS, der Pilot erhoeht nichts.

## Start-Hinweis fuer die Bau-Sitzungen
1. Werkstatt: zuerst `solidcraft-cli.exe eval` je Bauteil und die Koerpernamen lesen (55 / 33); `tank.py:207` ist die einzige Umbenennung; `tank_gross*` nicht anfassen; nie Fremdes committen (Liste oben), Commits nur mit Pfad.
2. Viewer: `export_model.py` und `serve.py` (ausser 2 Durchreichen) nicht aendern; Detail-OBJ mit `MIN_DIAG = 0`; kein Komponentenname im JS; `viewer/detail/` und `viewer/extras.json` nie committen.
3. Falle: `parts.insert`-Koerper heissen `Body<n>` und tragen Material "Default"; nach jedem Neubau `check_tank.py`/`check_feinfilter.py` laufen lassen (Interferenzpruefung kennt das Praefix `Schraube`).
4. Screenshot im Browser gegen `..\..\docs\ui-standard.md` ist Pflicht; ein fehlgeschlagener Screenshot ist ein Blocker. Texte der Infokarte aus `docs/parts/*.md` abschreiben, jede Zahl mit Herkunft.
5. Limit: weiche Grenze 40 Prozent Kontext, harte 50 Prozent (D74); Stand vor dem Stoppen in `docs/packages/n-detail-pilot.md` Abschnitt Status schreiben.
