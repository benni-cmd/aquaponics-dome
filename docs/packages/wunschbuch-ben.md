# Wunschbuch: alles, was Ben gewuenscht oder vorgegeben hat (Orchestrator, Stand 31.10.2026 17:30)

**Problem:** Ben gibt ueber viele Nachrichten Wuensche und Vorgaben; einzeln gehen sie in langen Sitzungen verloren. Ben (31.10.): "behalte die gesamte restliche Dokumentation vollstaendig und im Blick und vergiss nichts, was ich dir in Nachrichten gegeben habe; das muss alles nacheinander abgearbeitet werden."
**Intent:** Eine einzige, nachpruefbare Liste jedes Wunschs mit Quelle (Nachricht Nr. in Bens Verlauf dieser Sitzung, Datum), Status und Platz in der Abarbeitung. Der Orchestrator liest sie bei jedem Wiederanlauf und fuehrt sie bei jeder Abnahme nach.
**Goal:** Kein Wunsch ohne Zeile; jede offene Zeile hat einen Auftrag in `docs/packages/reihenfolge-offene-wuensche.md` oder `docs/packages/bauanleitung-teileliste-detailansicht.md`.
**Herkunft der Liste:** automatisch aus dem Sitzungsprotokoll gezogen (alle Nachrichten Bens ab 28.10.2026 20:17, 202 nach Filter, danach von Hand gelesen), nicht aus der Erinnerung. Befehl: `python -I ben_msgs.py` (Scratchpad der Orchestrator-Sitzung), Quelle `~/.claude/projects/C--Users-benkn-Claude-keel-harness/b929343a-3fc8-48fb-98d8-33a811bb78fe.jsonl`.
**Statuscodes:** ERLEDIGT (im Repo belegt) · LAEUFT · GEPLANT (Auftrag/Zeile vorhanden) · DAUERHAFT (Regel, gilt immer) · PRUEFEN (Stand nicht sicher belegt) · ENTSCHEIDUNG (wartet auf Ben).

## A. Modell, Standard und Technik
| Nr | Wunsch (Kurzform, Bens Sinn) | Quelle | Status | Wo |
|---|---|---|---|---|
| W01 | Kuppel mit Aquaponik-System nachbauen, Teile sauber erkennen, in Schleifen verfeinern | #12 29.10. | ERLEDIGT bis Zwischencheck (Loop aus) | `designs/dome.sc`, D-Liste |
| W02 | Grundflaeche genau 12 m Durchmesser als Massstab, Hoehe entsprechend | #21 | ERLEDIGT | layout.json, Radius 6000 |
| W03 | Genormte deutsche Tuer | #22 | ERLEDIGT | `tuer_komplett`, D36 |
| W04 | Wiederkehrende Elemente als EINE Definition, viele Instanzen; Aenderung einer Komponente aendert alle Klone | #32, #41 | DAUERHAFT, erfuellt | Komponenten + Instanzen |
| W05 | Expertenstandard in allen Bereichen; maximale Detailtiefe; statisch, biologisch, technisch sinnvoll | #45, #50, #51 | DAUERHAFT | Arbeitsregel; Statik siehe W32/B9b |
| W06 | Phase "reines Modell": Fischart, Standort, Betrieb, Preise ruhen, bis Ben etwas anderes sagt | #48 | DAUERHAFT | Standort/Folie bleiben ENTSCHEIDUNG |
| W07 | Technisch logisch: wo Wasser fliesst, Filter, Pumpen, Verteiler, Schlaeuche | #37, #41 | GEPLANT (M10) | Reihenfolge Zeile 9 |
| W08 | Kuppel ohne festen Boden, Skelett im Boden verankert, Rohre liegen auf der Erde oder sind erkennbar vergraben | #49 | GEPLANT (in M10-Plan aufnehmen) | M10 |
| W09 | Verbindungsstuecke der Streben: einfachste, billigste, mit lokalen Ressourcen baubare Loesung (NGO, entfernte Regionen) | #37 | ERLEDIGT als Knotenkugel D100 mit Steckarmen und Querbolzen; Alternative Laschenknoten (Foto Chemnitz, #272) wird verglichen | D59, R41 |
| W10 | Bauplan mit Farben, Materialien, Schlaeuche schoen liegend, schoene Renders | #41 | GEPLANT (nach Zwischencheck: Farben/Material/Render, ComfyUI-Schlussschritt) | Roadmap B10 / Render |
| W11 | Filterarten einzeln verstehen und modellieren (Helix, Sediment, Vortex, Biofilter), Simulator pruefen | #41, #224, #230 | ERLEDIGT | R28, R30, D53, D55, `docs/filter-konzept.md` |
| W12 | Staender unter den Filtern kleiner | #224 | ERLEDIGT | W30 (Plattform klein 619, gross 821) |
| W13 | NFT: nur EINE Lochreihe je Rinne; aussen 4 Rohre; mehr Pflanzen | #60, #35, #201 | ERLEDIGT | W24, D43 (674 Toepfe) |
| W14 | NFT-Tische ohne Kollision, passend zu den Beeten, Beete notfalls schmaler | #123, #160 | ERLEDIGT bis check_latte | D24, D25, D30, W33; check_latte steht aus (G) |
| W15 | Standardbauteile (Pumpen usw.) online als fertige Modelle suchen | #126 | ERLEDIGT | R14 (Gewinn klein) |
| W16 | Pflanzenzahl mindestens wie Bens Tabelle (609: Substrat >= 152, NFT >= 459), eher mehr | #159 | ERLEDIGT (Modell 674 Rinnen + 960 + 588 Beet-Toepfe) | system-specs, D52 |
| W17 | Pflanzenarten-Modelle zuletzt, Bauteile/Technik/Schlaeuche haben Vorrang | #159 | DAUERHAFT (zurueckgestellt) | nach Zwischencheck |
| W18 | Alles erreichbar, Laufwege nicht zu eng; NFT/Beete notfalls schmaler, nur praeziser platzieren | #160, #235 | LAEUFT (Karte Knie ok, Kopfscheibe 2 rote Engstellen Becken/Wand) | D54, D62, Montage |
| W19 | Wachsende Beschreibung des Modells: was beruecksichtigt ist, was wir lernen, wie praezise | #161 | LAEUFT | `docs/model-description.md` (B14) |
| W20 | Lochabstand verringern, mehr Toepfe | #173, #178 | ERLEDIGT | W18 (200 mm) |
| W21 | Bauteilbeschreibungen mit Funktion, Neigung usw.; Kuppel-Specs bei keiner Auswahl; Strom, Pumpenleistung, Filterumsatz rechnerisch stimmig | #187-#189 | ERLEDIGT, laufend nachfuehren | `data/descriptions.json`, `system-specs.json` (B14) |
| W22 | Nicht blind Tabelle/Simulator uebernehmen, eigene wissenschaftliche Recherche, Fischbesatz zur Tankgroesse; Fachrecherche-Sitzung | #191-#193 | ERLEDIGT / laufend | R17-R39 |
| W23 | Huelle ist eine Plane, keine Paneele | #201 | ERLEDIGT | D39, 40 Felder (Montage, Build 53) |
| W24 | Fisch 450-500 kg (mehr Pflanzen: 4 Rohre aussen, Suesskartoffeln dichter) | #201, #202 | **ENTSCHEIDUNG**: R36 ergibt bei Weg 1 nur 346 kg (308-385); ich habe D61 so gesetzt. Ben soll bestaetigen, dass 346 reicht, oder mehr Pflanzflaeche/Weg 2b will | R36, D61 |
| W25 | Designer-Modell (.blend) als Massreferenz nutzen | #205 | ERLEDIGT | `reference/designer-glb-analysis.md` |
| W26 | Drittes (kleineres) Becken platzieren | #213 | ERLEDIGT / angepasst | D46, D48, D49, D66 (0,4 m3) |
| W27 | Puffertanks (2 IBC gestapelt) mit Messung und Naehrstoffausgleich, rechts neben der Tuer; Dosierkonsole | #213, #214 | ERSETZT durch kleinen Puffer im Dom (Bens Frage 31.10.): W34 LAEUFT | D46, D66 |
| W28 | Menschenfigur 1,80 m an der Station und an der Gegenseite zwischen Mittel- und Aussenring, wenn moeglich arbeitend | #216 | ERLEDIGT | M9, W29 |
| W29 | FPV-Knopf, UI weg, 1,80 m Person, Tuer ausgeblendet = fehlt auch im FPV | #219, #220 | ERLEDIGT (Hoehe 400+1680, `walk_z` Export e5fae0d) | V01 |
| W30 | Danach komplette Schlaeuche/Rohre/Kabel logisch verlegen, Kollisionspruefung, dann Pause und Zwischencheck | #224 | GEPLANT | Reihenfolge Zeilen 9, 10 |
| W31 | Tischhoehe der NFT-Tische begruenden; zu hoch? | #243, #245 | ERLEDIGT (1000 mm) | R35, W33, D60 |
| W32 | Roadmap: Bauanleitung mit Teileliste und Funktionserklaerung; Detailansicht per Rechtsklick mit Explosion jedes Einzelteils; Teileliste; Klick auf Teil = Erklaerung; Standardprofile/Meterware, minimaler Verschnitt; Schrauben/Winkel einheitlich; lebensmittelechte Werkstoffe/Zertifizierung DE; Becken/Beete kaufen oder selbst bauen; Streben moeglichst einheitliche Laenge | #239 | GEPLANT (nach Zwischencheck) | B1-B10 (+ B11-B15) |
| W33 | Plane muss transparent sein | #265 | ERLEDIGT im Viewer (dedad6a); CAD-Render zeigt Referenzflaeche | D63, B15 |
| W34 | Puffer vielleicht nur 100-l-Faesser oder kleine transparente Optionen, alles in der Kuppel | #265 | R37 ERLEDIGT, W34 LAEUFT | D66 |
| W35 | Plane im Bauplan mit moeglichst simplem Schnitt- und Nahtmuster | #266 | LAEUFT (R38) | D64, B11 |
| W36 | Wichtige Kreislaufwerte an mehreren kritischen Stellen messen, Recherche, ins Modell | #267 | LAEUFT (R39), danach W35-Bauteile | D65, B12 |
| W37 | Aufgaben in alle offenen Wuensche einreihen; Roadmap vollstaendig; nichts vergessen | #267, #271, #273 | ERLEDIGT / dauerhaft | dieses Buch, Reihenfolge-Paket |
| W38 | Chemnitz-Verbindungsstueck (Foto) und Bericht des NGO-Forschers verstehen und einordnen | #272 | GEPLANT (R41) | D68, `reference/chemnitz/` |
| W39 | Viewer: Gruppen mit Zahl, ein-/ausblendbar, Hover-/Klick-Leuchten durch andere Koerper | #174, #188 | ERLEDIGT; Hover-Bug (#188) PRUEFEN | Viewer |
| W40 | ComfyUI-Workflow fuer photoreale Renders einrichten und nutzen | #4-#11, #28 | BELEGT 01.11. (R43): ComfyUI laeuft, nur ein Test; Umsetzung nach Zwischencheck (Roadmap N-RENDER) | dome-build.md |

## B. Arbeitsweise, Sitzungen, Limit (alles DAUERHAFT, soweit nicht anders vermerkt)
| Nr | Regel | Quelle | Stand |
|---|---|---|---|
| P01 | Orchestrator behaelt den Ueberblick, Werkstatt/Montage nur begrenzten Kontext; Subsessions bekommen konkrete Auftraege und lesen wenig | #105-#118, #206, #229 | umgesetzt (Jobblaetter) |
| P02 | Kontext unter 50-70 %; Werkstatt erst nach sauber abgeschlossener Komponente leeren, Montage weicher | #105, #113 | umgesetzt |
| P03 | Leere Sitzungen darf der Orchestrator selbst neu anstossen; vorher pruefen, ob sie arbeitet; Weck-Nachrichten (Praefix, <= 300 Zeichen) im sessionpost-guard | #115-#117 | umgesetzt, Guard-Ausnahme gebaut |
| P04 | Bilder der Pruefungen in einem Ordner sammeln, Entwicklung sichtbar | #108 | umgesetzt (`renders/history/`) |
| P05 | Limit: nicht bei 95 % aufhoeren, aber vorsichtiger; immer zwischenspeichern; nichts abbrechen; bei knappem Wochenlimit nur eine Sitzung; bei Reset sofort weiter | #28, #166, #170, #177, #178, #227, #257, #260 | umgesetzt |
| P06 | Fragen der Subsessions logisch selbst beantworten, Ben nicht unnoetig fragen | #180, #184 | umgesetzt (Pruefung 31.10., D67) |
| P07 | Entscheidungen wie empfohlen treffen und weitermachen | #211 | umgesetzt |
| P08 | Zwischenstand-Zeile bei abgeschlossenen Schritten; gegliederte Stand-Aufzaehlung mit Besitzern beibehalten | #224, #230 | umgesetzt (Memory) |
| P09 | Dokumentation pflegen, regelmaessig zwischenspeichern | #224 | umgesetzt (laufend, B14) |
| P10 | Viewer auf Zuruf starten | #185, #204, #212, #234 | Server Port 4410 |
| P11 | Loops aus | #195 | umgesetzt |
| P12 | Nichts vergessen: dieses Buch bei jeder Abnahme nachfuehren | #273 | dauerhaft |

## C. Offene Entscheidungen fuer Ben (alle ENTSCHEIDUNG, keine blockiert den naechsten Schritt)
1. W24: Fischmenge 346 kg (R36, D61) akzeptieren oder 450-500 kg verlangen (dann mehr Pflanzflaeche, Weg 2b oder mehr Rinnen)?
2. Technikvorbau entfaellt (D66); Puffer klein im Dom (0,16 m3) bestaetigen; Frischwasser: Aktivkohle oder Zisterne (Versorger fragen: Chlor/Chloramin).
3. Drittbecken 0,4 m3 (Oe 0,8 m) bestaetigen.
4. Standort, Folienart (Plane), Beschaffungsregion.
5. V1 (zwei Strebenlaengen) oder V2c; Verbindungsstueck: Knotenkugel (heute) oder Laschenknoten (nach R41).
6. Weg 2b fuer Fruchtgemuese in den Beeten (nur falls gewuenscht).

## Nachtrag 31.10. 17:50 (D69)
| Nr | Wunsch | Quelle | Status | Wo |
|---|---|---|---|---|
| W41 | Vorerst keine Ertragsrechnungen, keine konkreten Wasser-/Stromkosten, Standort irrelevant, keine Verschattungs- oder aehnlichen Rechnungen | #274 31.10. | DAUERHAFT (bis Ben es aendert) | D69; Entscheidungen "Standort" und "Wasserversorger" entfallen |
| W42 | Folienart: in den Quellen suchen, sonst UV-bestaendige Gewaechshausfolie, moeglichst lange haltbar, noetige Zertifizierungen, guenstig; Lieferform klaeren; pruefen, ob das Schnittmuster damit umsetzbar ist; reale standardisierte Teile im Bauplan | #274 | LAEUFT (R42) | D69, B11 |
| W43 | Verbindungsstuecke (Knoten): moeglichst viele Standardmasse (Flachstahl, Schrauben, Rohr) verwenden; Geruestdicke (Strebenprofil) aus Recherche oder eigener Rechnung bestimmen, Verbindungsstuecke muessen dazu passen; genaue Masse legt der Orchestrator selbst fest | Ben 01.11.2026 | OFFEN: Profilwahl braucht Statik (Roadmap N-STATIK), Orientierung 40x40x3 oder 50x50x3 statt 30x30x2 | R41, R34, D59 |
| W44 | Vor jedem Roadmap-Schritt pruefen, ob die Aufgabe noch aktuell ist oder sich durch vorherige Schritte geaendert hat (Regel); danach gilt der Plan grundsaetzlich als freigegeben | Ben 01.11.2026 | DAUERHAFT (Regel in docs/jobs/README.md und orchestrator-state.md) | M10-PLAN |
| W45 | Teileliste, Meterware, Bestellmengen und Schnittmuster sollen NICHT bei jeder Aenderung von einer KI neu gemacht werden, sondern von einem fest programmierten Skript aus dem 3D-Modell kommen; Aenderungen am Modell sieht man direkt in der Teileliste. Spaeter, einen Schritt danach: Parameter in der Teileliste einstellen, sodass sich Teile, Bestellmengen und Schnittmuster sofort anpassen | Ben 01.11.2026 | GEPLANT (Roadmap N-STUECKLISTE als Skript, danach N-BOM-PARAM); Machbarkeit siehe B5/B16 | B1, B4, B5, B16 |
| W46 | Dunstwasser (Kondensat und Verdunstung) wieder einfangen; verschiedene Vorschlaege von mir, moeglichst durch die Bauweise der Kuppel | Ben 01.11.2026 | OFFEN: Recherche R46 in der Roadmap (nach dem Zwischencheck, vor N-PLANE), danach Entscheidung E17 | R46, E17, L20 |
| W47 | Sauberer Beschaffbarkeits-Nachweis: fuer ALLE Bauteile und Komponenten (Schrauben, Muttern, Schellen, Verteiler bis Wassertank, Filter, Plane) belegen, dass sie gekauft oder realistisch selbst gebaut werden koennen, auch als Kombination aus Kaufteilen; bis dahin wird so weitergebaut | Ben 01.11.2026 | OFFEN: Roadmap N-BESCHAFFUNG (nach dem Zwischencheck), Ausloeser Stichprobe L21 | N-BESCHAFFUNG, L21 |
| W48 | Besonderheiten des Projekts und des Modells (z. B. Wasser ohne Pumpe durch Heber und Siphon) immer irgendwo vermerken, damit man Projekt und Modell pitchen kann | Ben 01.11.2026 | DAUERHAFT: Register docs/pitch-besonderheiten.md, Roadmap PITCH-REGISTER | PITCH-REGISTER |
| W49 | Neue Sitzungsarten als Standard: Planungssitzung (Auftragsblatt) und Pruefsitzung (Gegenleser), damit der Orchestrator den Ueberblick behaelt und die Bau-Sitzungen besser arbeiten | Ben 01.11.2026 | DAUERHAFT: Vorlagen docs/jobs/vorlagen, Regel in docs/jobs/README.md, Roadmap SITZUNGSARTEN | SITZUNGSARTEN |
| W50 | Arbeitsweise dokumentieren (welche Subsessions, welche Regeln) und die Regeln so anpassen, dass Tokens und Kontext noch besser gespart werden (Themen bestehenden Sitzungen zuordnen, solange der Kontext nicht zu voll ist) | Ben 01.11.2026 | ERLEDIGT: docs/arbeitsweise-sitzungen.md, D73, D74, docs/jobs/kosten.md; Schwellen werden aus den Messwerten nachgeschaerft | SITZUNGSARTEN |
| W51 | Leitungssystem und Wasserkreislauf neu denken: in Bauform und Verteilart weiterdenken, moeglichst wenige Teile, Filter/Pumpen/Subtanks nah am Kreislauf (weniger Umleitung), Schwerkraft beachten und NUTZEN, haengende Verteil-"Wasserautobahn" (ein Leitungsring ueber den Zonenringen, Verteiler zu Subtanks und NFT, Regler direkt an den Elementen), Ring ueber dem mittleren Ring auf einfachen Stelzen; Flood-and-Drain fuer Substratbeete mit Abstandshalter oder Sieb am Boden gegen Vergammeln, Siphon nicht verstopfend; erst Machbarkeitsbericht und Einschaetzung, dann umsetzen | Ben 02.11.2026 | OFFEN: Recherche R47 laeuft, danach Entscheidung E20 | R47, E20 |
| W52 | Wartbarkeit und Ausfallsicherheit: ein verstopftes VERGRABENES Rohr legt die Anlage still, die Kreislaeufe kippen und alles kann sterben; oberirdische Leitungen sind einfacher zu warten; bitte nochmal abwaegen | Ben 02.11.2026 | OFFEN: Recherche R47B laeuft, danach E20 | R47B, E20 |
| W53 | Mitgruender-Rueckfrage zum Wasserkreislauf: Wasser muss nur einmal hochgepumpt werden; der Fluss soll EINHEITLICH bleiben (alles durch die Biofilter, ein Pool, gesamtheitlicher Naehrstoffkreislauf als Sicherheitsmechanismus, kein einzelnes Ableiten der Biofilter); Foerderhoehe 2 bis 4 m ist normal | Ben/Mitgruender 02.11.2026 | OFFEN: Recherche R47c laeuft, danach E20 | R47C, E20 |
| W54 | Filterreihenfolge und Hoehenprofil pruefen: (a) Vortex (Absetzer) ueber den Biofilter setzen, Pumpe in den Subtank (Sumpf) verlegen, damit besser wartbar; (b) ist ein Feinfilter VOR dem Vortex sinnvoll, oder gleich in den Vortex, dann Ueberlauf in den Biofilter; (c) Feinfilter eventuell in den Subtank | Ben 03.11.2026 | OFFEN: Recherche R48, danach Entscheidung E21 (zusammen mit E20) | R48, E21 |
| W55 | Einfachstes naturnahes System (Schwerkraft, Siphon): Biofilter hoeher oder kleine Anpassungen, simpel, wartungsarm, ueberschaubar, effizient; Pruefung ob wirklich alles vergraben sein muss; Beet-Rueckfuehrung nach dem Siphon per Schlauch im Kreis; Profilbilder der Wasserautobahn auf fehlende Komponenten pruefen | Ben 03.11.2026 | OFFEN: Recherche R49 laeuft (Sitzung local_b0d89204-1bb0-41d9-9f86-467634539b73); Profilbild Bild 2 im Stationen-Artefakt ERLEDIGT (v5, fehlende Komponenten ergaenzt) | R49, E20, E21 |
| W56 | Detailansicht im Viewer jetzt fertig machen (vorgezogen), damit Filter und danach Subtanks nach Funktion beurteilt werden koennen; Standardgeraete finden und im Modell nachbauen, kaufen wenn moeglich, Selbstbau nur wenn super simpel; Siphons an den Substratbeeten mit Schutzgitter als sichere Vorarbeit | Ben 03.11.2026 | OFFEN: Planer N-DETAIL-PILOT laeuft, R50 (Filter, Standardgeraete) und R51 (Beet-Siphon) laufen | N-DETAIL-PILOT, R50, R51, D56 |
| W57 | Substratbeete muessen sich wirklich GANZ leeren, sonst bildet sich stehendes Wasser und Ploerre; Siphon-Ansaugung bis zum Boden des Wasserraums (R51 Befund: heute bleibt der Wasserraum unter dem Sieb gefuellt) | Ben 03.11.2026 | OFFEN: Planer W40-BEET plant die Aenderung am Beet-Bauteil | W40-BEET, R51, B08 |
| W58 | Alle Kaufteile muessen mindestens in Europa bestellbar sein (D76); Bau der Detailansicht und der Beet-Teile freigegeben ("bau grundsaetzlich, keinen Quatsch"), Planer zuerst, auf Limit achten | Ben 03.11.2026 | IN ARBEIT: Planer W40-BEET, Werkstatt N-DETAIL-PILOT, R52 Europa-Check | D76, W40-BEET, N-DETAIL-PILOT, R52 |
| W59 | Alle Einzelteile nach Typ indexieren (Metallprofile der Tische, Winkel, Rohre usw.), jede Komponente landet indexiert in einer Einkaufsliste mit groben Stueck- und Gesamtpreisen und, wenn gefunden, Bestell-Link mit Lieferung nach Deutschland | Ben 04.11.2026 | IN ARBEIT: Planer N-STUECKLISTE gestartet (buendelt N-KATALOG, N-STUECKLISTE, N-BESCHAFFUNG) | N-KATALOG, N-STUECKLISTE, N-BESCHAFFUNG, D76 |
