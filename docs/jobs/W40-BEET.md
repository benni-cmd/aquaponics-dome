# W40-BEET Beet-Bauteil `ibc_beet`: Beet leert sich ganz, Siphonschutz, Reinigungszugang, Reduktion, Europa-Bezug

Planer: Sonnet 5.5, 03.11.2026. Nur gelesen und gerechnet, kein Modell, keine Daten, nicht `data/roadmap.json` geändert. Mini-Plan: `docs/packages/w40-beet.md`. Grundlage: `docs/research/R51-beet-siphon-und-schutz.md` (ganz gelesen).

**Problem:** Die Glocke steht auf dem Siebboden; der Wasserraum darunter (aussen_800 485 l, innen 420 l, aussen_933 640 l) bleibt dauernd gefüllt (R51 Befund 5a), im Dunkeln entsteht Plörre. Dazu fehlen Siphonschutz mit passender Lochung (heute 12 Löcher 12 × 12 mm), Reinigungszugang und die Reduktion d40 × d25 (L03). **Intent:** Ben (03.11.2026, „bau beides, keinen Quatsch“): das Beet leert sich GANZ, nur Standardteile, alle Kaufteile mindestens in Europa bestellbar (D76), Selbstbau nur wenn super simpel. **Ziel in einem Satz:** Das Bauteil `ibc_beet` (aussen_800 und innen_933 Pflicht) hat einen ungelochten Sperrboden statt Siebboden (kein stehendes Wasser unter dem Medium), einen Siphon mit niedrigen Kerben (Rest höchstens 12 mm Film), einen Lochblech-Schutzkorb, einen stehenden Reinigungsschacht d110 und den Port für die Reduktion d40 × d25; Entleerzeit bleibt 4,3 bis 6,1 min; Bauteilblatt, Check und Interferenz grün.

## Aktualitätsprüfung (03.11.2026, Regel W44)
Ergebnis: **angepasst** (Plan gilt als freigegeben, Ben 03.11. „bau beides“).
- Roadmap `W40-BEET` (geplant, Reihenfolge 3,7, FREIGEGEBEN, um W57 und D76 erweitert) und `L03` (Lücke; Netz Version 3 angepasst, Bauteil bleibt d25) gelesen. Der Auftragstext der Roadmap nennt noch „Medienschutz-Löcher, Körnung mindestens 12 mm“: ersetzt durch R51 (Lochblech 5 mm deckt Korn ab 8 mm und ab 12 mm; Körnung ist nur noch Siebloch-Frage und entfällt mit dem Sperrboden, siehe unten).
- Decisions D56 bis D76: **D76** (Europa-Bezug) gilt für jede Teileliste unten; D75 (Subtank) und M10-S2V sind geparkt und berühren das Beet nicht; D73/D74 Verfahren. Kein Beschluss ändert das Beet-Bauteil außer W57/D76 aus der Roadmap.
- `git log --oneline -15` (HEAD 89f5a52): R50, R51, N-DETAIL-PILOT-Plan, D75/D76, Orchestrator-Stände; kein Commit an `scripts/workshop/ibc_beet.py`, `designs/components/ibc_beet*.sc`, `data/components/ibc_beet.json` oder `docs/parts/ibc_beet.md` (`git log` über diese Pfade war leer seit R51). Fremde unversionierte Änderungen: `designs/components/{becken_dritt,erdflaeche,fundamentring,haut_paneel_BBB,pool_zentral,schaltschrank,strebe_a,strebe_b,tuer,zulaufrohr,zweitbecken}.sc`, `viewer/extras.json`, `renders/section-61.png`: **nie anfassen**.
- Parallel laufend: N-DETAIL-PILOT (`data/parts/`, `data/katalog.json`, `scripts/workshop/tank.py`, `feinfilter.py`, `viewer/`) und R52: keine gemeinsame Datei mit dem Beet.
- **Messungen gegen den Auftragstext:** (1) Die Forderung „Siphon bis zum Wannenboden und Entleerzeit 4,3 bis 6,1 min“ lässt sich **nicht gleichzeitig** erfüllen, solange der Wasserraum wassergefüllt ist (Abschnitt Varianten, Rechnung). (2) Die Entleerzeit 4,3 bis 6,1 min stammt aus R45 (234 l für aussen_933); die Rechnung unten ergibt für den Zieltyp aussen_800 (195 l) 3,6 bis 5,1 min: Abweichung zu R45 kommt von der Annahme „Ablauf bis Schlitz-Unterkante“; die Werkstatt rechnet beide Fälle im Skript und meldet die Abweichung, ändert den Sollbereich nicht.

## Eingaben (nur diese; Zeilen selbst nachsehen)
- `docs/research/R51-beet-siphon-und-schutz.md`: Abschnitt 3 (Schutz, Schacht), Abschnitt 5 (Modellier-Spezifikation T30e-1 bis T30e-7, Zeilen etwa 142 bis 157), Befunde am Bestand.
- `scripts/workshop/ibc_beet.py` (Zeilen etwa 70 bis 140: Siebboden mit `Sieb_Loch`-Muster und `Sieb_Standrohr`, Medium mit `Medium_Schutzloch`, Siphon-Block mit `tube`, Schlitze `SchlitzA/B`, `Luftloch`, `Medienschutz` mit `Schutzloch_*`), `scripts/workshop/check_ibc_beet.py` (Zeilen 47 bis 60: prüft Körper `Siebboden`, `Standrohr`, `Medienschutz` per Name und Maß).
- `data/components/ibc_beet.json` (Parameter `grid_*`, `guard_*`, `bell_slot_*`) und `docs/parts/ibc_beet.md` (wird von `partsheet.py` erzeugt, nicht von Hand ändern).
- `docs/research/R45-hydraulik-auslegung.md` Abschnitt 1 (Siphon-Auslegung, Zeilen 79 bis 116) und Abschnitt 3 (Beet-Sumpf 500 l: 1 Beet Spitze 25 l, 2 Beete 168 l, 3 Beete 405 l, Zeile 179).
- `data/leitungsnetz.json` Kanten K14 und K30 (Feld `hoehe`: „Beetablauf ca. Z −100 [A]“) und K11; `data/layout.json` `ibc_beds` (`z0`: aussen −162, innen −209 bis −173).

## Befund Z −100 (geklärt, Meldung an Montage und Orchestrator)
Das Netz (K14/K30 `hoehe`, R45 Abschnitt 3) rechnet „Beetablauf ca. Z −100 [A]“, das ist eine **Annahme**. Das Bauteil liegt tiefer: Wannenunterseite Z −162 (aussen) bzw. −209 bis −173 (innen), Rohrende des Bulkheads bei lokal z −30 = **abs −192 (aussen)**, innen −239 bis −203; Wanneninnenseite abs −157. Mit der Reduktion d40 × d25 (etwa 50 mm lang [A], Kaufmaß prüfen) und einem Bogen liegt die Achse des Einzelabgangs bei etwa **abs −260 (aussen) bis −290 (innen)**, am Ende des 0,5-m-Abgangs mit 2 % Gefälle 10 mm tiefer. **Der Beetablauf liegt also 160 bis 190 mm unter dem Netzwert.** Wirkung: Der Beet-Sumpf (Einlauf Sektorsammler bei 800 mm Tankhöhe, Tank 1,0 m eingegraben) muss seine Einlauf-Rohrsohle **unter** etwa Z −270 (aussen) bzw. −300 (innen) bekommen, sonst staut der Ablauf zurück und bremst den Siphon (R45 Zeile 192). Ob der Sumpf-Einlauf so tief liegt, ist aus den gelesenen Dateien nicht ableitbar: **OFFEN (Montage/Orchestrator)**: K14/K30 `hoehe` auf „Achse etwa −260 aussen, −290 innen“ setzen und die Sumpf-Einlaufhöhe gegenprüfen. Die Werkstatt ändert den Port nicht (Port bleibt z lokal −30), sondern meldet nur.

## Varianten für die vollständige Entleerung (Rechnung, Skript `scripts/w40_beet_rechnung.py` als Plan)
Randwerte: Medium 300 mm, Poren 40 %, Standrohrkante lokal z 527, Medium-Unterkante z 262 (innen 274), Siebboden z 254 bis 262, Wannenboden Innenseite z 5. Siphon d25 (ID 22,0), Druckhöhe 0,30/0,45/0,60 m, Formel `siphon_q` aus `scripts/r51_rechnung.py`. Flächen: aussen_800 1,95 m², innen 1,61 m², aussen_933 2,57 m².

| Variante | Prinzip | Ablaufvolumen je Zyklus (800 / innen / 933) | Entleerzeit d25 (800 / 933) | Restwasser | Urteil |
|---|---|---|---|---|---|
| **V0 heute** | Glocke auf dem Siebboden | 195 / 161 / 257 l | 3,6 bis 5,1 / 4,7 bis 6,8 min | 497 / 429 / 656 l stehen dauernd | erfüllt W57 nicht |
| **V1 Schacht bis Wannenboden** | Standrohr und Glocke in einem Schacht d110 durch das Sieb bis 15 mm über den Boden (mit Reinigungsschacht kombiniert) | **649 / 555 / 857 l** | d25: 9,9 bis 12,4 / 13,1 bis 16,3 min; mit d40-Standrohr 3,4 bis 4,3 / 4,5 bis 5,6 min, aber Spitze 111 bis 158 l/min je Beet | alles leer | **verworfen:** ein Zyklus (649 l) sprengt den Beet-Sumpf (500 l brutto, R45 Zeile 179); d40 schafft die Zeit nur mit 111 bis 158 l/min, dann überlastet 1 Beet die Sammelleitung d50 (Grenze 3 × 54 l/min); Flutzeit mit 3,3 bis 8,3 l/min: 78 bis 197 min |
| V2a Gefälle/Mulde im Siebboden | Sieb bleibt gelocht, Mulde zum Ablauf | wie V1 (Wasserraum läuft mit) | wie V1 | Haftwasser | verworfen aus demselben Grund; Gefälle löst das Volumen nicht |
| V2b Wasserraum flach (Klötze 60 statt 249 mm, Medium 300 auf 490 mm) | Wasserraum verschwindet durch tieferes Medium | etwa 0,4 × 490 mm × Fläche = 383 l (800) | 7 bis 10 min | klein | verworfen: +0,5 m³ Blähton je Beet (rund 7 m³ für 14 Beete), Pflanzhöhe und Gewicht ändern sich |
| **V3 Sperrboden (gewählt)** | Siebboden **ohne Löcher**, ringsum abgedichtet, Wasserraum wird trockener Luftraum; Glocke steht wie heute auf dem Boden, Kerben statt hoher Schlitze | 195 / 161 / 257 l (**unverändert**) | 3,6 bis 5,1 / 4,7 bis 6,8 min (**unverändert**; Sollbereich R45 4,3 bis 6,1 min bleibt Maßstab) | **9,4 / 7,7 / 12,3 l** Film (12 mm Kerbenhöhe, Rechnung unten); Haftwasser im Korn bleibt | **gewählt**: Standardbauweise (Festboden-Beet, UH-CTAHR BIO-10), Ablaufvolumen und Zeiten unverändert, Sumpf unberührt, Beet wird 485 bis 640 kg leichter |

**Rechnung V3 (Plan für `scripts/w40_beet_rechnung.py`, nicht schreiben):** Film = Fläche × Kerbenhöhe × 0,4: aussen_800 1,95 m² × 12 mm × 0,4 = **9,4 l**, innen 7,7 l, aussen_933 12,3 l (Summe 8 × 800 + 6 innen = 121 l statt 6400 l stehendes Wasser). Flutstand bis Standrohrkante lokal z 527 (35 mm unter der Oberfläche z 562); Flutvolumen 195 l (800); Flutzeit 24 bis 59 min bei 8,3 bis 3,3 l/min (800), Zyklen 0,8 bis 1,8 je Stunde. **Ehrlich:** Die Entleerzeit 3,6 bis 5,1 min (800) liegt am unteren Ende von R45 4,3 bis 6,1 min, weil das Beet kleiner ist als aussen_933; das Skript rechnet auch aussen_933 und prüft, ob 4,7 bis 6,8 min (nicht 4,3 bis 6,1) aus der Wahl der Ablaufgrenze kommen. Das Anspringen bei 3,3 l/min ist nicht gerechnet, nur am Muster prüfbar.
**Folgen von V3:** (a) Der Wasserraum (6400 l im Zielstand) entfällt als Systemvolumen: das ändert die Wasserbilanz des Gesamtsystems und der Gewichte (Tischlast, Fundamente); **Meldung an Orchestrator**, Entscheidung Ben. (b) Die Luftkammer (249 mm) bleibt ungenutzt; Alternative „IBC kürzer schneiden“ ist ein Layout-Eingriff (Z-Höhen, Tische R35/R36), nicht Teil dieses Schrittes. (c) Die Dichtheit ist das neue Risiko: Dichtband am Rand (Spalt 2 mm), Durchführung am Standrohr, Muster mit 15 mm Wasser über 24 h. Leckwasser unter der Platte wäre wieder stehendes Wasser. (d) Optionale „Nachlaufbohrung“ d4 im Standrohr auf Plattenhöhe (rechnerisch etwa 0,5 l/min bei 0,26 m Druckhöhe, nimmt 15 bis 45 % des Zulaufs 3,3 bis 1,1 l/min weg): nur wenn der Film am Muster zu groß ist.

## Änderungen am Bauteil (nach Variante V3)
1. `Siebboden` (PP 8 mm): `Sieb_Loch`-Muster **entfernen**; `Sieb_Standrohr` wird zur Durchführung d36 für die Plattenhülse (Bulkhead D36 + Flansch D50, zweite Hülse neben der am Wannenboden); Körpername bleibt `Siebboden` (Check, descriptions, Viewer bleiben unverändert; Hinweis im Blatt „ungelocht, Sperrboden“). Parameter `grid_hole/nx/ny` entfallen aus `data/components/ibc_beet.json`.
2. Glocke: 2 Schlitze 10 × 40 bei +15 **ersetzen** durch 4 Kerben 10 × 12 am Fuß (z 262 bis 274), Fläche 480 mm² ≥ Standrohrfläche 380 mm²; Luftloch 10 × 10 bei +50 bleibt. Glockenhöhe 295 und Standrohrkante z 527 bleiben.
3. Medienschutz S-A (R51 T30e-4) ersetzt `Medienschutz`: Rohr d110 × 1,5 V2A, h 320, Modell vereinfacht 2 Ringe × 12 Schlitze 5 × 50 (z 272 bis 322 und 342 bis 392; 6000 mm² = 15,8 × Standrohr), lose Kappe d110; Körpername `Medienschutz` und Außen-Ø 110 bleiben (Check).
4. Reinigungsschacht T30e-5, **geändert gegenüber R51**: Rohr d110 × 3 **stehend auf dem Sperrboden** (kein Loch in der Platte, keine zweite Dichtstelle), Oberkante 20 mm über der Medienoberfläche (z 582), Kappe d110, Lage x = −Li/2 + 250, y = 0; Medium-Ausschnitt d110; 2 Kerben 30 × 30 am Fuß lassen Wasser und Schlamm vom Plattenfilm in den Schacht, dort absaugbar (Saugschlauch d ≤ 75).
5. Reduktion d40 × d25 (T30e-3): neues Kaufteil unter dem Bulkhead, im Modell als Körper `Reduktion` (d25-Muffe oben, d40-Stutzen unten, 50 mm [A] bis Kaufmaß geprüft); Port bleibt z −30.
6. Parameter: `bell_slot_h` 40 auf 12, `bell_slot_z` 15 auf 0, neue `shaft_d` 110, `guard_*` anpassen. Bauteilblatt per `partsheet.py` neu erzeugen (Text „Wasserraum 485 l“ muss weg, ebenso Gefüllt-Gewicht: Wasser nur Porenwasser).

## Teileliste mit Beschaffbarkeit in Europa (D76)
Marke: [Q] Seite/Ausschnitt dieser Sitzung gelesen (nur Katalogzeile, kein Datenblatt, Preise nicht geprüft), [R51] aus R51 übernommen. „Artikel“ = Händlerbezeichnung, vor der Bestellung gegen Maß und PN prüfen.

| Teil | Maß | Europäische Quelle (Hersteller/Händler, Artikel) | Status |
|---|---|---|---|
| Reduktion kurz 40 × 25 | PVC-U Klebefitting mit Klebstutzen und Klebmuffe | Weinmann-Schanz (DE) „PVC-U Klebefitting Reduktion kurz 40 × 25 mm mit Klebstutzen u. Klebmuffe“, Bestell-Nr. 93 049 64 [R51]; Georg Fischer (CH) „TP PVC-U Reduzierung D40AG-D25IG“ über Vanmarcke (BE) [R51] | beschaffbar (Maß der Bauhöhe noch aus Datenblatt) |
| Standrohr d25 × 1,5 | PVC-U Druckrohr PN10, ISO 4422 | Bevo (NL/BE) „Druckrohr PVC-U 25 mm × 1,5 mm Klebemuffe × glatt 10 bar ISO-PN10 grau 5 m“, Art. 0309025 [R51/R45] | beschaffbar |
| Glocke d75 | PVC-U Rohr d75 (2,9 oder 3,6 mm) plus Klebekappe d75, Länge 295 mm sägen | Rohr: Bevo „Druckrohr PVC-U 75 mm × 2,9 mm Klebemuffe × glatt 8 bar grau 5 m“ Art. 7027594 bzw. × 3,6 mm Art. 0309175 [Q]; Kappe: Bevo „Kappe PVC-U 75 mm Klebemuffe 16 bar grau“ Art. 0160592 [Q], Klebefitting-Kappen auch bei Schwarte (DE) | beschaffbar; Modell rechnet Wand 3 mm: auf 2,9 oder 3,6 mm abstimmen |
| Schutzkorb Lochblech | Edelstahl 1.4301, 1,5 mm, Rundloch 5 mm, Teilung 8, Zuschnitt 366 × 340 mm | ehorst.de (DE) „Lochblech Edelstahl 1.4301 RV 5-8 1,50 1000 × 2000 mm DIN 24041“, Art. 1003438 [R51]; Zuschnitt und Rollen beim Metallbauer anfragen | beschaffbar als Tafelware; **Rollen/Zuschnitt: Anfrage OFFEN (Ben)** |
| Kappe Schutzkorb d110 (lose) | PVC-U/PP Muffenstopfen DN110 | Ostendorf (DE) „KG Muffenstopfen DN/OD 110“ 220620 und „HT-Safe M Muffenstopfen PP D110 grau“ (über Vanmarcke) [Q]; Bauhaus/Hornbach KG-/HT-Muffenstopfen DN110 (Hornbach Art. 267389/267185) [Q] | beschaffbar |
| Reinigungsschacht d110 + Kappe | KG/HT-Rohr DN100 (Außen-Ø 110) × 3, Länge etwa 562 mm, Muffenstopfen DN110 | Rohr: Ostendorf/Wavin/Funke KG- oder HT-Rohr DN100 (Baumarkt-/Baustoffhandel) [Q nur Stopfen gesehen]; Kappe wie oben | beschaffbar; Rohr-Artikel beim Kauf eintragen |
| Hülse in der Platte (Siebboden-Durchführung) | Bulkhead D36 mit Flansch D50 im Modell [A] | Georg Fischer/VDL: „VDL Tankverbinder PVC-U 32 mm × 1″ Klebemuffe × Außengewinde 10 bar grau“ (Bevo 7018227) [Q], Koi-Breeder „PVC-U tank bushing“ [Q] | **Maßproblem:** Standard-Tankverbinder hat Klebemuffe d32, das Standrohr ist d25: es braucht eine Reduzierhülse 32/25 oder ein d32-Standrohr (Entleerzeit schneller, R45 Variante B). **OFFEN (Ben)**; bis dahin Blocker für die Plattenhülse |
| Hülse im Wannenboden (heute) | wie oben | wie oben | gleiches Maßproblem, bisher Annahme [A] in R45 |
| Dichtband Plattenrand | EPDM-Moosgummi selbstklebend 10 × 10 | nicht gesucht (Baumarkt-/Technikhandel, Normware) | **nicht nachgewiesen**: vor Bau Quelle eintragen, sonst Blocker |
| Kleber PVC-U | Klebstoff nach DIN EN 14814 | nicht gesucht | **nicht nachgewiesen** (Normware, z. B. Weinmann-Schanz Sortiment) |

Selbstbau, alles super simpel: Standrohr, Glocke und Schacht sägen, Kappe kleben, 4 Kerben sägen; **nicht** simpel: Schutzkorb rollen und nieten (Metallbauer) und die Plattenabdichtung (Muster entscheidet).

## Bezugsquellen-Nachtrag (Orchestrator, 04.11.2026)
Suche dieser Sitzung (Websuche, nur Katalog- und Datenblattausschnitte, Preise nicht geprüft). In die Teileliste des Bauteilblatts übernehmen.

| Teil | Quelle 1 | Quelle 2 | Status |
|---|---|---|---|
| Reduzierhülse 32 × 25 (Tankverbinder-Muffe d32 auf Standrohr d25) | Schwarte (DE) „PVC-U Klebefitting Reduktion kurz 32 mm × 25 mm“, Art. 75208, Stutzen 32, Muffe 25, 16 bar | Bevo (NL/BE) „VDL reducer bush PVC-U 32 mm × 25 mm glue spigot × glue socket 16 bar grey“, Art. 7002656, Länge 22 mm | beschaffbar (zwei unabhängige Händler); Baulänge 22 mm aus Bevo-Katalogzeile, Datenblatt nicht gelesen |
| Kleber PVC-U | Henkel Tangit PVC-U Plus, Technisches Merkblatt (datasheets.tdx.henkel.com): erfüllt DIN EN 14814, für EN 1452, Trinkwasserkontakt | Baumarkt-Handel: toom „Rohrklebstoff PVC-U Plus 125 g“ (Art. 8150236), Kaufland/ewm-sales Tangit PVC-U 125 g | beschaffbar |
| Dichtband Plattenrand | Graf-Dichtungen (DE) Moosgummi Vierkant 10 × 10 mm (Z0701): laut Datenblatt zum Einnuten, **nicht** selbstklebend; selbstklebend erst 10 × 20 mm | Steinbach & Vollmann (stuv.de, DE) EPDM-Zellkautschuk geschlossenzellig, selbstklebend, wasserdicht laut Datenblatt; Maße 10 × 3 bis 15 × 2 mm auch bei Marktplatz-Händlern | **Maß 10 × 10 selbstklebend nicht nachgewiesen.** Werkstoff (EPDM-Zellkautschuk, geschlossenzellig) beschaffbar. Werkstatt führt im Bauteilblatt: „EPDM-Zellkautschuk geschlossenzellig, selbstklebend; Maß vor Bau festlegen (Spalt 2 mm: z. B. 10 × 3 mm verpresst oder 10 × 20 Graf)“, Status „Maß offen“ |

## Schritte (einzeln committbar; Rolle)
**Schritt 1, Werkstatt (1 Sitzung, Sonnet):**
- 1a. `scripts/w40_beet_rechnung.py` schreiben und laufen lassen (Plan oben); Ausgabe ins Paket. Commit `scripts/w40_beet_rechnung.py`.
- 1b. `data/components/ibc_beet.json` (Parameter) und `scripts/workshop/ibc_beet.py` ändern (Punkte 1 bis 6), vier Typen bauen (`python scripts/workshop/ibc_beet.py` ohne Argument), `check_ibc_beet.py` anpassen und grün. Commit `scripts/workshop/ibc_beet.py`, `check_ibc_beet.py`, `data/components/ibc_beet.json`, `designs/components/ibc_beet_*.sc`.
- 1c. Bauteilblatt `docs/parts/ibc_beet.md` per `partsheet.py` neu erzeugen; Interferenzprüfung und alle Körper benannt. Commit `docs/parts/ibc_beet.md`.
**Schritt 2, Prüfer (frische Sitzung, nach `docs/jobs/vorlagen/pruefung.md`, nie die Bau-Sitzung):** Prüfpunkte selbst messen, Befund `docs/jobs/pruefung/W40-BEET.md`.
**Schritt 3, danach (nicht hier):** Montage baut die 14 Beete im Dom neu (Roadmap-Vermerk); Netz K14/K30 `hoehe` und Sumpf-Einlauf angleichen.
**Parallel erlaubt:** Pilot N-DETAIL-PILOT (andere Dateien), R52, alle Recherchen. **Nicht parallel:** ein zweiter Schreiber an `ibc_beet.py`, `check_ibc_beet.py`, `data/components/ibc_beet.json`; ein dome-Build der Montage (er liest `ibc_beet_*.sc`).

## Nicht anfassen
Fremde Dateien (Liste oben), `data/roadmap.json`, `data/leitungsnetz.json` (Meldung nur), Port-Lage z −30, Wannenmaße, Standrohrkante z 527, Zulauf-Tropfrohr, `viewer/`, `data/parts/`, `data/katalog.json`, `scripts/workshop/tank.py`, `feinfilter.py`.

## Ergebnis
`designs/components/ibc_beet_{aussen_933,aussen_993,aussen_800,innen_933}.sc` (neu), Skripte, Parameter, Bauteilblatt, Rechenskript; Prüfer-Befund.

## Prüfpunkte (fremd nachmessbar)
1. **Restwasser:** `python -X utf8 scripts/w40_beet_rechnung.py` gibt für aussen_800 höchstens 10 l und für innen_933 höchstens 8 l Film aus; im Modell: Siebboden ohne Löcher (`solidcraft-cli.exe eval designs/components/ibc_beet_aussen_800.sc`: Körper `Siebboden` Volumen = Fläche × 8 mm, kein Lochabzug) und Kerben-Oberkante höchstens z 274 (innen 286).
2. **Entleerzeit:** Skript meldet für d25 und h 0,30 bis 0,60 m eine Ablaufzeit 3,6 bis 5,1 min (aussen_800) und weist die Abweichung zu R45 4,3 bis 6,1 min aus; Ablaufvolumen 195 l.
3. **Check:** `python scripts/workshop/check_ibc_beet.py` Exit 0 (alle vier Typen).
4. **Körper:** alle Körper benannt, keine `Body<n>`; Interferenz 0 (Schacht, Schutzkorb, Glocke, Stützen, Medium); `Reduktion`, `Reinigungsschacht` und `Medienschutz` vorhanden.
5. **Europa-Bezug:** jede Zeile der Teileliste im Bauteilblatt hat Hersteller/Händler und Artikel; Blocker (Plattenhülse, Dichtband, Kleber) stehen im Blatt als „nicht beschafft“.

## Offene Entscheidungen
- **ENTSCHIEDEN (Ben, 04.11.2026, D77):** V3 Sperrboden bestätigt (Wasserraum entfällt, 6400 l Systemvolumen weg).
- **ENTSCHIEDEN (Ben, 04.11.2026, D77):** Schutzkorb aus Lochblech 5 mm, Zuschnitt und Rollen beim Metallbauer (Anfrage: Ben); im Modell und Bauteilblatt so führen. Ursprüngliche Frage: Schutzkorb kaufen und rollen lassen (Lochblech 5 mm, Metallbauer) oder gebohrtes PVC-Rohr als Muster; Körnung nach V3 nur noch Wahl, Blähton 8–16 reicht (Schutz 5 mm), Mindestkörnung 12 mm nicht mehr nötig.
- **ENTSCHIEDEN (Ben, 04.11.2026, D77):** Standrohr bleibt d25 mit Reduzierhülse 32/25 im Tankverbinder (Kaufteil Reduzierhülse in die Teileliste, Quelle in Europa suchen). Ursprüngliche Frage: Standrohr bleibt d25 (mit Reduzierhülse 32/25 im Tankverbinder) oder wechselt auf d32 (Zeiten 2,6 bis 3,8 min, Spitze 68 bis 97 l/min).
- **OFFEN (Montage/Orchestrator):** K14/K30 Höhe und Sumpf-Einlauf, Systemwasserbilanz ohne Wasserräume.

## Start-Hinweis für die Werkstatt-Sitzung (fünf Zeilen)
1. Lies nur dieses Blatt, `docs/cad-standard.md`, `docs/detail-standard.md`; R51 Abschnitt 5 nur Zeilen 142 bis 157.
2. Fallen: Körpername `Siebboden` bleibt (Check, Viewer); Box-statt-Zylinder-Schnitte (Rechenzeit, Kommentar im Skript); `Medium_Schutzloch` und neuer Schacht-Ausschnitt je d110.
3. Typen aussen_800 und innen_933 sind Pflicht, 933/993 mitbauen (gleiches Skript), aber nicht im Dom.
4. Committe nur mit `git -C … commit -m … -- <Pfade>`, nie fremde `.sc`; Rechenskript zuerst, dann Bau.
5. Limit (D74): Lauf etwa 600 Nachrichten; weiche Grenze 40 % (etwa 750 Nachrichten): kein neues Paket; harte Grenze 50 %: Stand ins Paket schreiben und stoppen.

**Geprüft gegen:** `docs/jobs/vorlagen/planung.md`, `docs/arbeitsweise-sitzungen.md` Abschnitt 4, R51 (ganz), `scripts/workshop/ibc_beet.py` (ganz), `docs/parts/ibc_beet.md`, Roadmap `W40-BEET`/`L03`, R45 (Zeilen 79 bis 116, 169 bis 192), `data/leitungsnetz.json` K11/K14/K30, D75/D76, Pitch B08/B12, `git log --oneline -15`, Rechnung `calc.py` im Scratchpad (nach `scripts/r51_rechnung.py`), Websuche Bevo/Ostendorf/VDL (nur Suchausschnitte). **Offen:** Anspringen bei 3,3 l/min und Dichtheit der Platte nur am Muster; Datenblätter der Kaufteile; Dichtband und Kleber nicht gesucht.
