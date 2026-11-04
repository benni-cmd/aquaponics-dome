# Pruefung N-DETAIL-W60 (Detailansicht aller Bauteile, Viewer-Neuerungen; Pruefer, 05.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md` und `docs/jobs/start/N-DETAIL-W60-pruefer.md`. Gegenstand: `docs/jobs/N-STUECKLISTE.md` Pruefpunkte 6 und 7 (Teiledaten 5a aller 308 Komponenten, Einkauf in der Detailansicht 70a6e7f) sowie `docs/packages/n-viewer-laden.md` (Ladeanzeige, Kleinteile-Schalter, robustes Laden) und `docs/packages/n-viewer-ansicht.md` (Visuell/Technisch). Die Selbstauskunft der Pakete zaehlt nicht als Beweis.

Vorgehen: Viewer auf eigenem Port 4433 (`python viewer/serve.py 4433`; `GET /api/state` meldet `busy: false`, kein Export gestartet, weil `viewer/instances.json` 13:32 neuer ist als `designs/dome.sc` 10:33). Gebaut, exportiert und geaendert habe ich nichts; im Repo liegt nur diese Datei. Parallel liefen `check_latte 69` und mein Gesamtlauf von `check_parts.py`, die Ladezeiten sind darum Obergrenzen.

## Urteil: PASS mit Auflagen (zwei Soll-Werte verfehlt: `check_parts` Exit 0 und Einkaufsdaten von Feinfilter/Absetzer)

Die Einkaufsanbindung stimmt bei allen sieben gemessenen Komponenten auf den Cent mit `data/stueckliste.json` ueberein, der Rueckverweis aus der Einkaufsliste funktioniert, Laden, Kleinteile, Visuell/Technisch und die Pilot-Auflagen A2 und A3 halten. Ein echter Fehler: bei den **zwei Pilot-Bauteilen Feinfilter und Absetzer** zeigt die Detailansicht "0,00 EUR, alle Teile ohne Preis", obwohl Preise vorhanden sind (Auflage A1). Dazu kommt: die in den Pilot-Auflagen versprochene Bereinigung der Anzeigetexte ist nur teilweise erreicht (Auflage A2).

## Messungen

| # | Soll | Befehl | Messwert | Urteil |
|---|---|---|---|---|
| 1 | `check_parts.py` ueber alle Komponenten Exit 0 | `python -X utf8 scripts/workshop/check_parts.py` (ohne Argument) | Gesamtlauf ueber alle 308 Komponenten in zwei Teilen (erste 40 in einem Lauf, die uebrigen 268 in vier parallelen Teillaeufen, Befehl `python -X utf8 scripts/workshop/check_parts.py <Komponenten>`; alle 308 Namen aus `data/parts` kamen vor): 306 Komponenten alle Pruefungen PASS (je 21 bis 22), **2 FAIL**: `strebe_a` und `strebe_b`, Pruefung "Koerper, deren .sc-Material nicht zum Werkstoff der Zeile passt: Ist 1, Soll 0" (`T1_Strebe_A`/`T1_Strebe_B` tragen Material `Default`, die Zeile `stahl_verzinkt`). Exit 1 in zwei der vier Teillaeufen. Das Paket fuehrt beide als offen (fremde, nicht committete Aenderungen an den `.sc`), also bekannt; das Soll "Exit 0" ist trotzdem nicht erreicht. Teile mit Marker `geruest: true` insgesamt 84 (`python -I` ueber `data/parts`) | FAIL (2 von 308) |
| 2 | Fehlende `artikel_id`-Verweise 0 | `python -I` ueber `data/parts/*.json`, `data/stueckliste.json`, `data/katalog.json` | 308 Dateien, 1069 Teile, 941 mit `artikel_id`; davon nicht in `stueckliste.json`: 0; nicht im Katalog (298 Artikel-IDs): 0 | PASS |
| 3 | Stichprobe mindestens 5 Bauteile: Menge, Preis, Link gegen `data/stueckliste.json` und `docs/einkaufsliste.html` (nicht Tisch, Pumpe, Rohrbogen der Bau-Sitzung) | Browser-Pane, `#detail=<komponente>`, `document.getElementById('detailpanel').innerText`, Erwartung per `python -I` aus `data/parts` und `data/stueckliste.json` | Sieben Komponenten: `tank_gross` (931,32 EUR, 10 Teile ohne Preis), `knoten_6_n01` (5,35), `lt_kugelhahn_d63` (79,02; 2 Bauteile = 158,04), `sonde_ph` (94,59; 3 Bauteile = 283,77), `puffer_klein` (353,82), `pumpe_klein` (103,86; 4 Bauteile = 415,44), `luftverteiler_4` (0,00; kein Preis): alle 7 Summen gleich der Erwartung. Je Teil Menge und Stueckpreis bei `tank_gross`, `knoten_6_n01`, `sonde_ph`, `puffer_klein` (23 Zeilen), `pumpe_klein` (6 Zeilen): jede Zeile gleich. Infokarte "Einkauf" des Kugelhahn-Gehaeuses (echter Klick): Menge 1 Stueck, 79,02 EUR, Bevo (NL), Stand 2026-11-04, Link gleich dem `url` der JSON. Einkaufsliste (`docs/einkaufsliste.html`): Zeile `PRF-st-strebe30x30` steht in der Seite, 331 Rueckverweise | PASS (Ausnahme A1) |
| 4 | Rueckverweis aus der Einkaufsliste | `document.querySelectorAll('a')` auf der Seite; Link mit Host 4433 im Viewer | 331 Links `http://localhost:4410/#detail=<komponente>&teil=<teil>` (alle auf einem Host); Probe `#detail=tank_gross&teil=plattform` im frisch geladenen Viewer: Detailansicht oeffnet nach Ende des Ladens (Wartezeit rund 28 s), Teil `plattform` ist gewaehlt, Infokarte zeigt Einkauf. Die Links zeigen fest auf Port 4410; der Viewer lief dort zur Pruefzeit nicht (`Get-NetTCPConnection`: nur 4433). Vor dem Laden der Seite reagiert der Sprung nicht | PASS (Hinweis H1) |
| 5 | Laden mit und ohne Kleinteile, Zeit, Fehlerzeilen 0, Tuer zeigt Klinke | Browser-Pane Port 4433; `window.viewerStand()`; Seite `Fertig:`-Zeile; Haken "Kleinteile unter 15 cm zeigen"; FPV | Ohne Kleinteile: "Fertig: 164 Definitionen, 256,0 MB, 18 s", 0 Fehlerzeilen. Mit Haken (echter Klick): "Kleinteile, Schritt 3 von 3: fertig" nach 10,4 s, 198,9 MB, 0 Fehlerzeilen; `tuer_komplett` 12 Koerper + 15 Kleinteile; Screenshot der Tuer in FPV: Klinke rechts, Scharniere links sichtbar. Das Paket nennt 12,7 s statt 18 s (mein Lauf mit zwei parallelen Pruefskripten) | PASS |
| 6 | Umschalten Visuell/Technisch | Klick auf "Technisch"/"Visuell"; `window.ansichtStand()`; Legende | Visuell: 685 Koerper sichtbar (ohne Kleinteile), 30 Farben; Technisch (mit Kleinteilen): 1607 Koerper, 1578 sichtbar, 29 Menschfiguren ausgeblendet (1607 minus 29), 13 Farben, Legende "Bauteilgruppen" mit 8 Gruppen und "Leitungen (nach Leitungsart)": Zulauf, Luft, Kabel, Hinweis "Menschfiguren sind ausgeblendet"; `localStorage` `viewer.ansicht` = technisch, merkt die Wahl; Screenshot Technisch gegen `ui-standard.md` gesehen | PASS |
| 7 | Pilot-Auflagen A2 und A3 (Singular, Kamera) | Kopfzeile `luftverteiler_4`; Schieber mit echtem Ziehen, `window.detailState().cam` vorher/nachher | "1 Teil, 1 Koerper" (Singular); Feinfilter Kamera vor dem Ziehen 1319/-2110/1591, nach Schieber 1 2681/-4370/3198, gesprengtes Modell passt vollstaendig ins Bild (Screenshot) | PASS |
| 8 | Modellklick waehlt die Zeile | echter Klick im Modell, Feinfilter gesprengt | Klick auf den Korb: `sel` = `korbgewebe`, Zeile "Siebgewebe des Korbs" markiert | PASS |

## Fachliches Gegenlesen der Leitungsteile

Gelesen: `lt_bogen90_d50`, `lt_t_d63`, `lt_reduzierung_d63_d50`, `lt_kupplung_d50`, `lt_rohr_d50_L1211`, `lt_kugelhahn_d63`, `lt_klemme_d32` (jede `funktion`, `eigenschaften`, `norm`). Befund: fachlich richtig, soweit pruefbar.

1. PVC-U-Druckrohr d50, Wand 3,7 mm bei PN16: passt zu SDR 13,6 (50 / 13,6 = 3,68 mm). Klebeverbindung mit PVC-U-Kleber nach DIN EN 14814: richtig benannte Norm fuer Kleber in Thermoplastrohrsystemen. EN 1452-3 fuer Formstuecke: richtig (Teil 3). Kugelhahn EN ISO 16135 fuer Hahn aus Thermoplast: richtig.
2. Kugelhahn: Hebel quer zur Leitung = geschlossen, laengs = offen, 90 Grad Drehweg: richtig. Rohrklemme: Stahlband nach EN 10346, Sechskantschraube ISO 4017: richtig. Der Hinweis, das Rohr werde nicht eingeklemmt, damit die Laengsausdehnung bleibt: fachlich sinnvoll.
3. Zwei Schwaechen: (a) "DIN 8062 / EN 1452" nennt mit DIN 8062 eine zurueckgezogene Norm vor der heutigen; (b) PN16 ist am Rohr "Richtwert [A]" angegeben, der Hersteller-Wert gehoert nach `data/beschaffung` (R52/R54 offen). Alle Normverweise tragen "[A]" und das Wort "angenommen".

## Anzeigetexte (Stichprobe)

29 Infokarten in 14 Komponenten gelesen (3 Teile je Komponente, gleichmaessig verteilt; Messung: JavaScript im Browser ueber `#detailpanel` und `#info`; die Zeile "Quelle:" ausgenommen, weil sie Dateipfade absichtlich nennt):

1. Register-Kuerzel im Fliesstext ausserhalb der Quellzeile: `R42` 2 Karten (Norm "[Q: R42]"), `W43` 2 Karten ("N-STATIK W43 offen"), `data/beschaffung` 3 Karten ("kein Eintrag in data/beschaffung"); der Marker `[A]` steht in 27 von 29 Karten (Norm- und Eigenschaftszeilen). Parameternamen mit Unterstrich: 0 ausserhalb der Quellzeile (Pilot-Auflage A1 dort erfuellt).
2. ASCII-Schreibung: "Einkaufsartikel"-Zeile `Artikel` mit "Stueck", "Huelle", "Flaeche", "Verbindungsstueck" in 3 Karten (zum Beispiel "PVC-U-T-Stueck d50" neben dem Titel "PVC-U-T-Stück d50"); "Einzelkoerper" in der Masse-Zeile in 25 von 29 Karten.
3. Dezimalpunkt statt Dezimalkomma ("Masse 312.6 g, Einzelkoerper 84.1 x 84.1 x 125.0 mm") in 25 von 29 Karten.

## Auflagen

1. **A1, Feinfilter und Absetzer ohne Einkaufsdaten (Fehler):** `data/parts/feinfilter.json` und `data/parts/tank_klein.json` tragen `artikel_id` (29 und 14 Teile), aber kein `artikel_menge_je_instanz`; die Detailansicht zeigt darum "anteilig 0,00 EUR; 29 Teile haben noch keinen Preis" (Feinfilter) bzw. "0,00 EUR; 14 Teile" (Absetzer) und keine Menge in der Teileliste. Gemessen: `python -I` ueber alle 308 Dateien: genau diese zwei haben Teile mit `artikel_id` ohne Menge. Tatsaechlich haben mehrere Artikel Preise (zum Beispiel `BEH-tank-pe-673x1075` 354,62 EUR, `ROH-pvcu-d110` 79,83 EUR im Absetzer). Gerade die beiden Bauteile des Pilots sind damit die einzigen, die den Zweck "Preis in der Detailansicht" verfehlen. Aufgabe: die zwei Dateien mit `parts_geruest.py` oder von Hand um `artikel_menge_je_instanz` und `artikel_einheit` ergaenzen. Ausserdem "0,00 EUR" bei fehlenden Preisen durch "kein Preis" ersetzen (gilt auch fuer `luftverteiler_4`, "kosten anteilig 0,00 EUR").
2. **A2, Anzeigetexte nicht ganz bereinigt:** siehe Abschnitt Anzeigetexte: Register-Kuerzel (R42, W43), Pfad `data/beschaffung`, Marker `[A]` in 27 von 29 Karten, ASCII-Schreibung in Artikelzeilen und "Einzelkoerper", Dezimalpunkt in 25 von 29. Die Filterregel `klartext` im Viewer kennt diese Faelle nicht (Daten sind unveraendert, der Filter nur im Viewer). Vorschlag: `[A]` und "Einzelkoerper"/Dezimalpunkt in den Filter, die Katalog-Bezeichnungen (`artikel` in `data/katalog.json`) mit Umlauten schreiben.
3. **A3, "2 Teile haben noch keinen Preis" bei Spindel und Hebel:** beim `lt_kugelhahn_d63` sind Spindel und Hebel im Gehaeusepreis des Hahns enthalten; der Text meldet sie trotzdem als ohne Preis und der Preis-Satz wirkt, als fehle Geld. Teile mit Artikel-Verweis auf denselben Hahn nicht als fehlend zaehlen.
4. **A4, Teile in Stand `geruest`:** 19 Dateien tragen noch `stand: geruest` und 84 Teile den Marker `geruest: true` (erdflaeche, fundamentanker, fundamentring, haut_paneel_*, huelle_folie_*, keilschiene, mensch_referenz (3), strebe_a, strebe_b, tuer, tuer_komplett, tuer_zarge_planenausschnitt). Die Texte der geprueften Huelle-Karten sind gefuellt (Folie: Norm EN 13206, Stand 'belegt'); fuer die Menschfiguren (43 Teile) ist das gewollt. Fuer die uebrigen die Marker nachziehen oder den offenen Grund (Katalog-Werkstoff, Streben-Profil) im Paket als Offen fuehren.
5. **A5, `check_parts.py` nicht Exit 0:** `strebe_a` und `strebe_b` tragen im `.sc` das Material `Default`, die Teiledaten `stahl_verzinkt`. Entweder das Material im `.sc` setzen (Werkstatt, Strebenmodell ist laut Paket Platzhalter bis N-STATIK) oder die Zeile auf `unbestimmt_modell` stellen, dann ist der Gesamtlauf gruen.
6. **A6, Anzeige "Modell gespeichert - -":** In der Kopfzeile des Bedienfelds steht "Modell gespeichert - - Viewer 13:32:32"; das Feld ist leer, wenn der Server ohne Export startet. Hinweis, kein Fehler.

## Hinweise

- H1: Die 331 Rueckverweise tragen fest `http://localhost:4410/`. Wer den Viewer auf einem anderen Port betreibt, landet im Leeren. Kein Fehler, aber im Paket vermerken.
- Hover auf eine Zeile (gelbe Hervorhebung im Modell) wurde nicht nachgemessen.
- Robustes Laden (Wiederholung fehlgeschlagener Dateien, Hinweis "Export laeuft") nicht nachgestellt, weil dafuer ein Export oder ein Entfernen von Dateien noetig waere; `check_latte 69` lief parallel.

## Nicht belegt oder nicht nachgemessen

1. Hover-Hervorhebung, Wiederholung beim Laden, Ladeanzeige mit Schwelle (Selbstauskunft des Pakets).
2. Ladezeit 12,7 s des Pakets (gemessen 18 s unter Last).
3. Jeder Katalog-Preis gegen die Haendlerseite (siehe `N-STUECKLISTE.md`-Befund).

Geprueft gegen: `check_parts.py` ueber 308 Komponenten, `python -I` ueber `data/parts`, `data/stueckliste.json`, `data/katalog.json`; Browser-Pane Port 4433 (Detailansicht von 14 Komponenten, 29 Infokarten, Visuell/Technisch, Kleinteile, FPV-Tuer, Modellklick, Schieber), `docs/einkaufsliste.html` (331 Rueckverweise).
Offen: A1 bis A6 (Werkstatt oder Viewer, Orchestrator); Hover und robustes Laden nicht nachgemessen.
