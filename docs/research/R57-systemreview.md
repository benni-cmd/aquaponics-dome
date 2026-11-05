# R57: Systemreview — so viele Teile wie nötig, so wenige wie möglich (W75, W76, W79, W82)

**Rolle:** Planer und Fachkritiker, nur lesen und rechnen; Modell, `data/leitungsnetz.json`, Roadmap unverändert. **Bearbeitet:** 05.11.2026. **Paket:** `docs/packages/n-minimal.md`.
**Herkunft:** [Q] Datei oder Quelle gelesen · [E] eigene Rechnung (Befehl daneben; Skript `python -X utf8 scripts/r57_rechnung.py <abschnitt>`) · [A] Annahme. Eine Recherche-Aussage gilt erst mit zwei unabhängigen Quellen (Abschnitt 7).
**Problem:** Die Anlage A+ hat viele Bauteile, die nur eine Höhenlücke überbrücken. Der Pool-Spiegel (Z +515 über Flur) liegt höher als die Beetabläufe (Z −100). Deshalb braucht es Beet-Sümpfe mit Reservepumpen, einen Heber in eine Filtergrube, einen Notbypass mit Schächten, einen Absetzer-Teilstrom mit Kleinpumpen und Schlammfässer in Gruben. Gebaut liegen 151,2 m Leitung unter Flur, geplant kommen 78,9 m Gräben dazu.
**Intent:** Schlank und natürlich: Schwerkraft statt Pumpen, wenig graben, kurze Wege, Technik innen, Schlamm draußen, dazu Sensorik und Ausgleich (W76).
**Goal:** Tabelle behalten / vereinfachen / streichen je Bauteil- und Leitungsgruppe mit Kostenwirkung, eine Empfehlung für Ben und Leon, Leitungsordnung v2.

## 0. Antwort (fünf Punkte)

1. **Ein Hebel löst fast alles: Der Pool wird der tiefste Punkt des Kreislaufs.** Wird der Ruhepegel um 665 mm abgesenkt (Z +515 auf Z −150) und stehen die Beete auf dem Flur statt eingelassen, dann fließt jedes Beet, jede NFT-Rinne und jeder Überlauf frei in den Pool zurück. Dann bleibt eine einzige Pumpstufe: Tauchpumpen im Pool heben über einen Schlauch in den Siebkorb auf dem Biofilter [E, `r57_rechnung.py pegel`].
2. **Entfallen würden:**
   - Beet-Sümpfe mit 4 Teichpumpen, 6 Schwimmern und 2 Rückschlagventilen
   - Heber K01/K17 samt zwei Poolwand-Durchführungen unter Wasser
   - Filtergruben, Filter-Stamm, Notbypass und 4 Kugelhahn-Schächte
   - Absetzerkreis mit 4 Kleinpumpen und Schlammfass-Gruben

   Die Stückzahl dieser Gruppen sinkt von 40 auf 10, die belegten Teilekosten um rund 3800 €, der Dauerstrom der Pumpen von 429 auf 328 W und der Aushub ohne Poolgrube von 43,7 auf 2,0 m³ [E, `r57_rechnung.py kosten | pumpen | aushub`].
3. **Zwei belegte Gegenregeln (Abschnitt 7):** FAO 589 und Hallam empfehlen, den Pegel im Fischbecken konstant zu halten und die Pumpe in einen eigenen Sumpf zu setzen. Bregnballe und Sindilariu belegen, dass eine Pumpe vor dem Sieb den Kot zerkleinert. Das Zielbild S widerspricht beidem. Es entspricht dem Bumina-Aufbau in FAO 589 (Becken pumpt in einen Kopfbehälter mit Filter, Rücklauf frei), dafür gibt es aber nur diese eine Quelle. Deshalb gilt S nur mit zwei Bedingungen:
   - Pegel-tief-Abschaltung der Pumpen als Pflicht, damit ein Leck den Pool nicht leer pumpt
   - Siebleistung im ersten Betriebsmonat messen; als Rückfall wird ein Vortex nachgerüstet
4. **Der Preis:** 7,9 m³ weniger Poolwasser. Der Besatz steigt dadurch von 12,1 auf 16,8 kg/m³ (FAO-Grenze 20, R44). Der Flutbetrieb lässt den Pegel um 39 bis 79 mm schwanken. Die Hauptpumpen brauchen 2,28 statt 2,0 m Förderhöhe. Die schon modellierten Saug- und Absetzerstrecken müssen zurückgebaut werden. Das Streichen des Absetzers öffnet D71 neu (Ben: „bei heute bleiben“) [E, Q D71].
5. **Leitungsordnung v2:** Rechtwinklig und starr bleibt nur, was gebündelt, verteilt oder unter Druck steht. Rückläufe, Luft, Frischwasser, Schlamm und der Pumpendruck aus dem Pool werden frei geführte Schläuche, mit stetigem Gefälle, ohne Hochpunkt und mit Zugang. Unter Flur liegt nur noch, was einen Gang quert oder in den Pool mündet. Schon in A+ fielen so 105,9 m Luft- und Frischwasserleitung aus dem Graben [E, `r57_rechnung.py vergraben`; `docs/leitungsordnung.md`].
6. **Empfehlung: Zielbild S mit den zwei Bedingungen beschließen und die Montage-Kette ab M10-S3 darauf umplanen, nicht A+ weiterbauen.** Die lehrbuchtreue Alternative ist Variante T aus R49: Pool konstant, Sieb vor den Pumpen im Sumpf, Beete laufen in den Sumpf. Sie kostet aber Sumpfgruben, behält den Heber und halbiert den Durchsatz durch den Pool (55,5 statt 110 l/min je Linie), außer man fährt 50 % mehr Pumpenstrom. Der Rückfall ohne Topologiewechsel ist A+ nach Ordnung v2 (124 m statt 230 m unter Flur, alle Pumpstufen bleiben).

## 1. Zielbild S in einem Bild (je Linie, zwei gleiche Linien nach D67)

```
Pool (tiefster Punkt, Ruhepegel Z -150, Rand Z 650)
  └─ 2 Tauchpumpen am Poolboden (Ansaugkorb) ── Druckschlauch über den Rand ──► Siebkorb 100 µm oben im Biofilter
                                                                                   │
Biofilter (K1-Schwebebett, belüftet, Spiegel Z 1600) ──► Verteiler mit allen Hähnen (Wasserstation, W82)
  ├─► 7 Beete auf dem Flur (Glockensiphon) ── Schlauch, Gefälle ≥ 1 % ──► Pool (freier Fall)
  ├─► 12 NFT-Tische ── Sektorsammler ── Halbring an der Wandkrone ──► Pool (freier Fall 0,8 m)
  ├─► Überlauf (heute K13) ──► Pool
  └─► Messkreis 3 l/min ──► Messzelle ──► Pool
Schlamm: Siebkorb-Spülwanne und Biofilter-Kegelboden ── Schlauch ── Durchführung Fundamentring ──► Fass über dem Boden draußen
Luft: 2 Gebläse am Technikturm ── Schläuche frei geführt ──► Scheiben im Pool, Biofilter, Becken
Frischwasser: Hausleitung ── Schwimmerventil auf Tiefpegel ──► Pool (R55: ohne Dauer-Kohle bei Chlor)
```
Rechenwerte: `python -X utf8 scripts/r57_rechnung.py pegel` (Pegelgrenzen je Beet Z −148 / −123 / −98, gewählt −150), `... pumpen` (H 2,28 m = Auslauf Z 1750 [A] minus tiefster Pegel Z −229 plus 0,30 m Reibung [A]).

## 2. Review je Gruppe: behalten / vereinfachen / streichen

Kosten: kleinster belegter Preis in `data/beschaffung/*.json` (Stand 04./05.11.), Menge aus den Trassen der Variante A+ oder der genannten Quelle; Befehl `python -X utf8 scripts/r57_rechnung.py kosten`. „ohne Preis“ heißt: kein Preis belegt, nicht in der Summe.

| Nr | Gruppe | Funktion im Kreislauf | Urteil | Begründung | Kostenwirkung (belegt) | Wartung und Rückbau |
|---|---|---|---|---|---|---|
| G1 | Pool, Pegel | Fischwasser, Wärmespeicher, Sammelpunkt | **vereinfachen:** Ruhepegel Z −150 statt +515 | Höhenkette Biofilter > Beete/NFT > Pool schließt sich ohne zweite Pumpstufe [E pegel] | 0 € (Becken bleibt) | Freibord 800 mm; bei Stromausfall steigt der Pool um höchstens 276 mm und läuft nicht über [E pegel] |
| G2 | Heber K01/K17, 2 Durchführungen in der Poolwand | Seitenablauf Pool → Feinfilter, voll laufend | **streichen** | im Zielbild saugen die Pumpen im Pool; zwei Wanddurchführungen unter Wasser (Leckstelle) fallen weg | −235 € Rohr d75 (5,3 m), −98 € Durchführungen | kein Heber-Luftsack mehr (R47b 6.2: Einzelpfad ohne Erkennung) |
| G3 | Absetzerkreis: Bodenablauf K03/K19, 4 Kleinpumpen, 2 Absetzer, K04/K05/K20/K21, Revisionsstutzen | Teilstrom 12,5 l/min je Linie durch Wirbelabscheider | **streichen** (öffnet D71) | Ein Swirl fängt rund 23 % der Feststoffmasse, ein Sieb im Vollstrom 40 bis 45 % (Davidson/Summerfelt, R44/R45). Die Tauchpumpe am Poolboden nimmt die Bodenfracht im Vollstrom mit. Gegenrede, belegt: Die Pumpe vor dem Sieb zerkleinert Partikel (Bregnballe 2015, Sindilariu 2009); um wie viel, ist nicht gelesen. Rückfall: Absetzer als Vollstrom-Vortex vor dem Sieb nachrüsten (Teich-Vortex 4 bis 40 m³/h, R50 3.2), wenn der Korb öfter als einmal am Tag voll ist | −384 € Pumpen, −774 € Rohr d50/d32 (34,6 m); Tanks ohne Preis | entfällt: 30,5 m Strecke unter Flur mit 0,13 m/s (R47b: Absetzgefahr) |
| G4 | Schlammfass in der Grube, K07/K23 | Schlamm lagern, Klarwasser von Hand zurück | **streichen, ersetzen durch Schlamm draußen über dem Boden** (W79) | Schlamm fließt per Schlauch aus Siebkorb-Spülwanne und Biofilter-Kegelboden durch den Fundamentring in ein Fass draußen; der Kreislauf bleibt innen. Das Fass ist ein Kurzzeitlager: höchstens eine Woche, dann auf Kompost oder Wurmkiste. Belegt ist: Schlamm ohne Luft bildet Schwefelwasserstoff und Ammoniak (FAO 589, KSU); wer länger lagern oder mineralisieren will, braucht einen belüfteten Behälter mit 5 bis 10 % des Systemvolumens (KSU), hier 1,5 bis 3 m³. Das Wasser (20 bis 40 l je Spülung, R45) taugt draußen als Gießwasser | −150 € Fässer, −59 € Hähne, −48 € Rohr; neu +198 € (2 Fässer 220 l lebensmittelecht, Einzelquelle) und +110 € Schlauch 32 mm | Fass von außen leeren, keine Grube, kein Eimer durch die Halle; Frost unbelegt: Schlauch läuft nach jeder Spülung leer (Gefälle R11) [A] |
| G5 | Feinfilter: PP-Kasten in der Grube (2) | Schutzsieb 100 µm im Hauptstrom (R50) | **vereinfachen:** nur der Edelstahl-Siebkorb, hängend oben im Biofilter | Funktion bleibt (Schutzsieb, R50 Punkt 2); Kasten, Grube und 85-mm-Reserveproblem entfallen | Kasten ohne Preis; Grube 0,8 m³ Aushub weniger | Korb ziehen über Flur ohne Grube; Platzmaß im Deckel Ø 930 [A, Werkstatt prüft] |
| G6 | Filter-Stamm und Zweig K02/K06/K18/K22 mit Stamm-Hähnen | Feinfilter → Saugseite Pumpen | **streichen** | ohne Saugseite keine Stammleitung | −194 € Rohr d50 (8,2 m) | entfällt: Einzelpfad je Linie (R47b) |
| G7 | Notbypass K56/K57, Kugelhähne d63, 4 Schächte | Umgeht den verstopften Korb | **streichen** | Antwort auf W79: Der tiefe Schacht gibt es nur, weil Bypass- und Stamm-Hahn 186 bis 424 mm unter Flur liegen (M10-S2N). Ohne Saugseite gibt es keinen Bypass; läuft der Korb über, fällt das Wasser in den Biofilter | −150 € Rohr d63 (4,6 m), −316 € Hähne, −180 € Schächte | kein ungetesteter Totast mehr (R47b 6.2) |
| G8 | Hauptpumpen 4 (2 je Linie) | einzige Hebestufe | **behalten, als Tauchpumpen im Pool** | Zahl gleich; Kennlinie muss 55 l/min bei 2,28 m schaffen. Die heutige Eheim 3400 liefert rechnerisch schon bei 2,0 m nur 38 l/min | 0 € Mehrzahl; neue Kennlinie ohne Preis; +344 € Schlauch 40 mm lebensmittelecht (24 m) | Pumpe am Seil ziehen statt Leitung trennen; kein Rückschlagventil; Pegel-tief-Schalter schaltet ab (FAO 589: Wasserverlust ist eine der häufigsten Katastrophen) |
| G9 | Biofilter 2 (K1, belüftet) | Nitrifikation, Höhenquelle der Schwerkraft | **behalten** (D55) | trägt den Siebkorb; Kegelboden-Ablass wird Schlammweg | 0 € | wie heute |
| G10 | Verteiler, K11/K12/K13 | teilt den Strom auf Beete, NFT, Überlauf | **behalten, als Wasserstation je Linie** (W82) | Der Verteiler ist physikalisch der einzige Ort, an dem sich jeder Strom einer Linie teilt. Dort sitzen alle Hähne beschriftet nebeneinander. Eine einzige Station für beide Linien senkt den Druckkopf zum NFT-Tisch auf 398 mm, unter das Soll von 500 mm (Abschnitt 2a) [E] | 0 € | ein Ort je Linie für alle Hähne; Strom (Schrank) getrennt |
| G11 | Beete 14 mit Glockensiphon | Pflanzen, Medienfilter, Nitrifikation | **behalten, auf den Flur stellen statt einlassen** | Ablauf steigt von Z −100 auf +62. Der Beetrand liegt dann bei Z 637 statt 475, also bessere Arbeitshöhe. Die Kopffreiheit über den Außenbeeten sinkt von 1343 auf 1181 mm, das reicht für das Blattgemüse nach D61. Kompostwürmer im Medium als natürliche Verwertung (Abschnitt 7) | 0 €; 5,3 m³ Aushub weniger | Beet ohne Grube tauschbar |
| G12 | Beet-Rücklauf K14/K30 | Siphonwasser zurück | **vereinfachen:** Schlauch oder Rohr frei auf dem Flur entlang der Beetfüße (Art C), nur die Einmündung am Pool flach unter Flur | 58,9 m Graben (R49) werden 46,5 m oberirdisch plus 2 × 3 m flacher Kanal [A]. HT- oder KG-Rohr wäre billiger (2 bis 4 €/m), ist aber nur als Abwasserrohr ausgewiesen und scheidet nach D85 aus | −1394 € Rohr d50, +702 € Schlauch 50 mm | ausspülbar am Tiefpunkt (Ordnung v2, Zugang) |
| G13 | Beet-Sumpf 2 × 500 l, 4 Teichpumpen, 6 Schwimmer, 2 Rückschlagventile, K58/K59 | hebt Beetwasser über den Pool-Spiegel | **streichen** | nur wegen der Höhenlücke nötig (R49 Abschn. 3); im Zielbild läuft das Beet frei in den Pool | −882 € Pumpen, −269 € Schwimmer, −123 € Rohr; Tanks und Ventile ohne Preis; −108 W | keine Flutsperre mehr nötig (R45: Pflicht wegen Überlaufgefahr) |
| G14 | NFT 24 Tische, K12/K15, Halbringe K16/K32 | Pflanzen, Rücklauf | **behalten** | läuft heute schon frei; Fallhöhe am Pool steigt von etwa 0,15 auf 0,8 m, gratis Sauerstoff (R55: 10 bis 15 % des Bedarfs bei 0,5 m, Einzelquelle) [E] | 0 € | wie heute |
| G15 | Zweitbecken, K33/K34 | Aufzucht | **behalten** | sein Überlauf in den Pool fällt jetzt 665 mm tiefer, der eigene Pegel bleibt | 0 € | wie heute |
| G16 | Drittbecken mit eigenem Biofilter und Luft | Quarantäne (45 Tage, FAO 589) | **behalten** | eigenes Wasser ist der Zweck | 0 € | wie heute |
| G17 | Messzelle, Stammlösung, Eisen, Dosierpumpen | Ausgleich pH, Eisen; Messung | **behalten** | das ist der „Ausgleich“ aus W76 | 0 € | wie heute; Messkreis als Schlauch |
| G18 | Frischwasser, Aktivkohle-Station T83 | Nachspeisung | **vereinfachen** (R55): Hausleitung, ein Kohleblock nur bei Chloramin; Schwimmerventil auf den Tiefpegel des Flutbetriebs gestellt | Station mit 2 Behältern, Begrenzer, Probehahn, 4 Hähnen wird ein Block oder entfällt; Leitungen als Schlauch über Flur | Einsparung in R55 | Ben klärt beim Versorger Chlor/Chloramin (E15) |
| G19 | Belüftung: 2 Gebläse, Verteiler, K44 bis K51 | Sauerstoff unabhängig von den Pumpen | **behalten; Leitungen als Schlauch über Flur** (66,8 m aus dem Graben) | Venturi ist kein Ersatz (R54, R55); K47/K48 entfallen mit dem Absetzer; zweites Gebläse gegen Akku-Notluft prüfen (R55, Förderkurve offen) | Leitung billiger als Rohr [A]; K47/K48 entfallen | Luftausfall bleibt der harte Termin: 0,8 bis 1,2 h (R45) |
| G20 | Sensorik | Erkennen statt Sichtkontrolle | **vereinfachen und ergänzen:** 2 Pool-Pegelschalter und 1 Durchflusswächter je Linie statt 6 Sumpfschwimmer; Messzelle bleibt | ein Pegel für die ganze Anlage, weil alles im Pool endet | +105 € | Alarm in Minuten (R47b M5) |
| G21 | Schaltschrank | Strom, Steuerung | **behalten, als Kasten innen** (D87) | Der Platz wird frei, wo Absetzer und Kleinpumpe standen; genau diese Teile musste N-TECHNIK-INNEN für den Schrank innen verschieben | 0 € | Brandschutzabstand offen (N-TECHNIK-INNEN) |
| G22 | Rückschlagventile, Schwimmerventile, Bypässe | Sicherungen | **ausdünnen:** 2 Sumpf-Rückschlagventile und Notbypass weg; Luft-Rückschlagventil (R53) und Schwimmerventil Frischwasser bleiben; Überlauf am Verteiler bleibt | jede verbleibende Sicherung hat eine Funktion, die sonst niemand übernimmt | in G7, G13 enthalten | – |
| G23 | Zwei Linien | Ausfallsicherheit | **behalten** (D67) | Ausfall einer Linie halbiert nur | 0 € | – |

**Summe der Gruppen mit Preis:** heute 6039 €, Zielbild S 2242 €, also 3797 € weniger. Darin fehlen 4 Artikel ohne belegten Preis, die alle entfallen (Absetzer-Tanks, Sumpf-Tanks, Feinfilter-Kästen, Rückschlagventile d40); die Einsparung ist damit eher größer. Nicht enthalten sind die Mehrkosten der stärkeren Tauchpumpe [E, `r57_rechnung.py kosten`]. Stückzahl dieser Gruppen ohne Meterware: 40 → 10.

## 2a. Wasserstation (W82): ja, eine je Linie am Biofilter, keine zentrale

**Empfehlung: zwei Wasserstationen, je eine pro Linie direkt am Biofilter, dazu der Stromschrank als getrennter Ort.** Eine einzige zentrale Station für beide Linien verwerfe ich aus physikalischen Gründen.

| Variante | Wasserwege | Urteil |
|---|---|---|
| **je Linie am Biofilter** | Der Verteiler sitzt unter dem Biofilter-Auslauf, dem einzigen Punkt, an dem sich der Strom einer Linie teilt. An einem Ort liegen: Siebkorb, alle Abgangshähne zu Beeten und Tischen, Überlauf, Messkreis-Abgang, Schlammhahn, Durchflusswächter. Druckkopf zum NFT-Tisch 510 mm (Soll ≥ 500 mm, Netz K12) [Q R49 2.1] | **empfohlen**; beschriftet und auf einer Tafel, siehe unten |
| zentral für beide Linien | Die Biofilter stehen 4,9 m auseinander. Eine Station in der Mitte verlängert jede Linie um 2,4 m d50 bei 1,14 m/s. Der Verlust beträgt 112 mm, der Druckkopf zum NFT-Tisch sinkt auf 398 mm, also unter das Soll von 500 mm. Die NFT-Tische laufen dann nicht mehr frei, nötig wäre ein höherer Biofilter oder eine Pumpe [E, `python -X utf8 scripts/r57_rechnung.py station`] | **verworfen** |
| verteilt (heute, Hähne an Beet und Tisch) | jeder Hahn an seinem Abnehmer; kurze Wege, aber 38 Stellen im ganzen Dom | **nicht nötig**; nur Feinregelung am Beet bleibt möglich |

**Was in die Station je Linie gehört:**
1. Siebkorb im Biofilter-Deckel
2. Verteilerbalken mit einem beschrifteten Kugelhahn je Abgang (7 Beete, 12 Tische, Überlauf, Messkreis)
3. Durchflusswächter der Linie
4. Schlammhahn am Biofilter-Kegelboden mit Abgang des Schlammschlauchs
5. Schild mit Fließbild der Linie

Strom (Pumpen, Gebläse, Sensoren) läuft im Schaltschrank-Kasten (D87) zusammen. So gibt es einen Ort für Strom und zwei gleiche Orte für Wasser. Die Station ist kein neues Bauteil, sondern eine Anordnung am vorhandenen Biofilter; die Werkstatt braucht nur eine Hahntafel. Gilt sinngemäß auch für A+.

## 3. Natürliche Kreisläufe und Ausgleich (W76)

1. **Selbstregelnde Wasserbilanz:** Im Zielbild endet jeder Weg im Pool. Fällt eine Pumpe, ein Siphon oder der Strom aus, läuft alles dorthin zurück. Kein Behälter kann überlaufen, eine Flutsperre ist nicht nötig, und ein Schwimmerventil hält den Stand [E pegel].
2. **Nährstoffkette:** Fischkot und Ammonium gehen über den Siebkorb (grob) in den Biofilter (Nitrifikation), von dort in Beete und NFT (Nitrat-Aufnahme) und zurück. Die Beete sind zugleich Medienfilter und Nitrifizierer (R44).
3. **Würmer im Beet, Schlamm im Garten:** Kompostwürmer im Medium bauen Kot ab und mindern Verstopfung (FAO 589, Hallam; belegt, qualitativ). Allein filtern können die Beete die Last aber nicht: Nach beiden Faustregeln (50 g Futter oder 5 kg Fisch je m²) bräuchte es etwa 69 m² Medienbett, die 14 Beete haben rund 30 m² [E: 14 × 0,80 × 2,64 m]. Siebkorb und Biofilter bleiben deshalb. Der abgetrennte Schlamm geht als Dünger und Gießwasser nach draußen (Wurmkiste 1,25 bis 2,5 m² nach R45).
4. **Freier Fall belüftet gratis:** Die Einläufe fallen 0,8 m statt etwa 0,15 m tief [E]; R55 rechnet bei 0,5 m 10 bis 15 % des Sauerstoffbedarfs (Einzelquelle). Das Gebläse bleibt die Grundlast.
5. **Sensorik und Ausgleich:**
   - Messzelle mit pH, EC, O₂ und Temperatur
   - Dosierung von Base und Eisen
   - Pool-Pegel tief und hoch
   - Durchfluss je Linie mit Alarm

## 4. Rechnung im Überblick (heute A+ gegen Zielbild S)

| Größe | heute (A+) | Zielbild S | Befehl |
|---|---|---|---|
| Leitung unter Flur, gebaut | 151,2 m | – | `r57_rechnung.py vergraben` |
| geplante Gräben A+ (K14, K58/59, K11) | 78,9 m | – | dito, Werte R49 Abschn. 4 |
| unter Flur gesamt | 230,1 m | 18,0 m [A: 2 × 3 m Pool-Einmündung, 10 Querungen × 1,2 m] | dito |
| davon Luft und Frischwasser (A+) | 105,9 m | 0 (Schlauch über Flur, Querungen enthalten) | dito |
| Aushub ohne Poolgrube | 43,7 m³ | 2,0 m³ | `r57_rechnung.py aushub` |
| Pumpen gesamt (inkl. Reserve) | 12 | 4 | `r57_rechnung.py pumpen` |
| Dauerstrom Pumpen | 429 W = 10,3 kWh/Tag | 328 W = 7,9 kWh/Tag | dito (Wirkungsgrad 25 %) |
| Fischwasser, Besatz | 28,5 m³, 12,1 kg/m³ | 20,6 m³, 16,8 kg/m³ | `r57_rechnung.py pegel` |
| Wärmespeicher Wasser | 40,4 kWh/K | 31,2 kWh/K | dito |
| Pegelschwankung im Pool | 0 | 39 mm (1 Beet je Linie), 79 mm (2 Beete je Linie) | dito |
| Belegte Teilekosten der Gruppen G2 bis G13, G20 | 6039 € | 2242 € | `r57_rechnung.py kosten` |

Zwischenvariante **A+ nach Ordnung v2** (Topologie bleibt, nur Luft und Frischwasser oberirdisch): 45,3 m gebaut plus 78,9 m geplant = 124,2 m unter Flur; alle 12 Pumpen und alle Gruben bleiben [E, `r57_rechnung.py vergraben`].

## 5. Risiken und was sie kosten

| Nr | Risiko | Wirkung | Gegenmaßnahme |
|---|---|---|---|
| K1 | Besatz 16,8 kg/m³ näher an der FAO-Grenze 20 | weniger Puffer bei Störung | Besatz schrittweise erhöhen (D61 sagt das schon); Grenze bleibt eingehalten |
| K2 | Pegelschwankung 39 bis 79 mm (alle 14 Beete gleichzeitig: 276 mm) | widerspricht der belegten Regel „Fischbecken konstant“ (FAO 589, Hallam); eine zulässige Schwankung nennt keine Quelle | Flutungen staffeln (höchstens 2 Beete je Linie, Steuerung wie heute); Pumpe am Boden mit 2 m Überdeckung; Schwimmerventil auf den tiefen Stand |
| K3 | Pumpe vor dem Sieb zerkleinert Kot (belegt: Bregnballe 2015, Sindilariu 2009) | mehr Feinanteil geht an Biofilter, Beete und NFT; Maß nicht gelesen | langsam laufende Teichpumpe mit grobem Ansaugkorb; Korb- und Trübungsmessung im ersten Monat; Rückfall Vortex vor dem Sieb (G3) |
| K7 | Leck auf der Druckseite oder in einem Beet pumpt den Pool leer | Fischverlust (FAO 589 nennt Wasserverlust eine der häufigsten Katastrophen) | Pegel-tief-Schalter schaltet die Pumpen ab, bevor mehr als der Flutstand fehlt; Alarm; das ist Bedingung 1 von S |
| K4 | Pumpenkennlinie (H 2,28 m bei 55 l/min) | stärkere Pumpe, eventuell mehr Strom als gerechnet | besteht schon heute (Eheim rechnerisch 38 l/min bei 2,0 m); Pumpenwahl als eigener Schritt |
| K5 | Rückbau im Modell | Heber, Filtergruben, Absetzerkreis, Bypass, Schächte (M10-S2N Runde 75) werden entfernt; M10-S2V (Subtank, geparkt) entfällt | Montage-Kette neu planen (Planer), bevor M10-S3 baut; im Feld ist nichts gebaut |
| K6 | D71 wieder geöffnet (Absetzer) | Ben hatte „bei heute bleiben“ gesagt; R44 Kandidat A blieb ein Kandidat | Rückfall Vortex vor dem Sieb als Nachrüstung; Entscheidung Ben |

## 6. Leitungsordnung v2 (Kurzfassung, Volltext `docs/leitungsordnung.md`)

- Sechs Leitungsarten statt eines Rohrtyps:
  - A Druck starr
  - B Druckschlauch
  - C Schwerkraft frei
  - D Luft
  - E Heber/Siphon
  - F Leerrohr/Kanal
- Neue messbare Regeln:
  - R11: Gefälle in jedem Teilstück mindestens 1 %, ab d75 0,5 %
  - R12: kein Hochpunkt; ein Siphon nur mit Kennzeichen
  - R13: unter Flur nur mit Grund und höchstens 3 m bis zum Zugang
  - R14: Schlauchradius mindestens 6 × d (Herstellerwerte 260 bis 270 mm bei 40 bis 51 mm)
  - R6: Schlauchschellen höchstens 400 mm auseinander, oder der Schlauch liegt auf
- Prüfskript angepasst: Schlauch-Trassen gehen nicht mehr in `leitungen.bauen()`. Mit `--nur-v2` werden nur Trassen mit Feld `art` geprüft.
- Bestand unverändert gemessen: `python -X utf8 scripts/check_leitungsordnung.py` meldet dieselben 11 Verstöße wie vorher (R4 1, R5 4, R8 5, R9 1) und R11 bis R14 je 0.
- Testlauf mit sieben Prüftrassen (Scratchpad `v2-test.json`): R11 2, R12 2, R13 1, R14 1, R6 2. Die gute Trasse T1 besteht.

## 7. Quellen und Belegstand der neuen Aussagen

Recherche am 05.11.2026, Volltext und Zitate im Sitzungs-Scratchpad (`r57-quellen.md`); hier die Aussagen mit Belegstand. „belegt“ = zwei unabhängige, geöffnete Quellen.

| Aussage | Quellen | Belegstand | Folge im Review |
|---|---|---|---|
| Fischbecken-Pegel konstant halten, Pumpe in einen eigenen tiefsten Sumpf (CHIFT-PIST/CHOP) | FAO 589 Kap. 4.2.6 S. 52–53 (https://openknowledge.fao.org/3/i4021e/i4021e.pdf); Hallam, „C.H.O.P. Aquaponics operating system“ (https://blog.aquaponics.net.au/chop-system/c-h-o-p-aquaponics-operating-system.htm) | belegt | S widerspricht; Bedingung 1, Risiko K2/K7, Alternative T genannt |
| Fischbecken pumpt in Kopfbehälter mit Filter, Rücklauf frei durch Pflanzen (Bumina) | FAO 589 Kap. 9.4.3 S. 153–154 | Einzelquelle | S entspricht diesem Aufbau |
| Wasser nur einmal heben | FAO 589/Hallam (CHOP); Bregnballe 2015 S. 71 (https://openknowledge.fao.org/3/i4626e/i4626e.pdf) | belegt | stützt S und T gleichermaßen |
| Zulässige Pegelschwankung im Fischbecken | – | nicht gefunden | K2 bleibt Annahme |
| Pumpe vor dem Sieb zerkleinert Partikel; Sieb vor die Pumpe | Bregnballe 2015 S. 71; Sindilariu, Brinker, Reiter 2009, Aquacultural Engineering (Abstract über AGRIS) | belegt (qualitativ), Zahlen nicht gelesen | Risiko K3, Bedingung 2 |
| Pumpgespeiste Filter sind in Teich und Kleinanlage üblich | FAO 589 S. 53, 153–154; Toppy.nl „Filter koivijver“ | belegt | S ist handelsübliche Praxis, nicht Neuland |
| Medienbeet filtert mechanisch und biologisch, mineralisiert | FAO 589 S. 58; Hallam, „Rules-of-Thumb“ | belegt | G11 |
| Kompostwürmer bauen Kot ab, mindern Verstopfung | FAO 589 S. 60, 141–142; Hallam „Rules-of-Thumb“; ergänzend Mishra 2003 (Sandfilter) | belegt (qualitativ) | G11, Abschnitt 3 |
| Beet allein filtert bis etwa 50 g Futter bzw. 5 kg Fisch je m² Bett | FAO 589 S. 58–59; Hallam | belegt | 69 m² nötig, 30 m² vorhanden: Sieb und Biofilter bleiben |
| Schlamm ohne Luft bildet H₂S/Ammoniak; Mineralisierung belüftet, 5–10 % Systemvolumen | FAO 589 S. 47; Kentucky State University, „Turning Fish Waste into Plant Nutrients“ | belegt | G4: Fass nur Kurzzeitlager |
| Schlamm direkt auf Boden, Kompost oder Feld | FAO 589 S. 47; Bregnballe 2015 S. 72–73; KSU | belegt | G4 |
| Frost bei Schlammbehältern draußen | – | nicht gefunden | G4 [A] |
| Gefälle unbelüfteter kleiner Leitungen etwa 1 cm/m, Sammelleitung 0,5 cm/m | SBZ Monteur 06/2016 nach DIN 1986-100; FAO 589 S. 65 (NFT) | belegt (zwei Anwendungen) | R11 |
| Abfließendes Wasser zieht das 10- bis 35-fache an Luft mit | SBZ Monteur 06/2016 | Einzelquelle | Art C beginnt offen (belüftet) |
| Halterabstand für Schläuche, Durchhang | – | nicht gefunden | R6 400 mm bleibt [A] |
| Biegeradius Spiralschlauch: 32 mm 95–200 mm, 40 mm 260 mm, 51 mm 270 mm | esska.de Datenblatt; ehorst.de Tricoflex Spirabel | belegt (produktabhängig) | R14 auf 6 × d |
| Leitungen lebensmitteltauglich und lichtdicht | FAO 589 S. 53 | Einzelquelle | Ordnung v2: Schlauch schwarz oder lichtdicht |
| Spiralschlauch lebensmittelecht: 32 mm ab 6,86 €/m, 40 mm ab 14,32 €/m, 50 mm 15,10 €/m | asdec-life.de, esska.de, imkado.de (je zwei Händler bei 32 und 40 mm) | belegt (32, 40), 50 mm zwei Händler, einer nur 51 mm | `r57_rechnung.py kosten` |
| HT DN50 2,05–2,56 €/m, KG DN110 3,85 €/m; keine Trinkwasser-/Lebensmittelangabe | Hornbach.de, eBay obadis; crassus/Ostendorf | Preis HT belegt, KG Einzelquelle; Eignung: als Abwasserrohr ausgewiesen | scheidet nach D85 aus |
| Fass 220 l lebensmittelecht 99 € | fermetech.eu (EE) | Einzelquelle; Fass mit Hahn, UV und Lebensmittelangabe zugleich nicht gefunden | G4 |

Nicht verwertbar (geöffnet, gescheitert): McMillan 2003 und Davidson/Summerfelt (Paywall), Eco Films (404), Minnesota-Wurmstudie (403).

## 8. Was nicht geprüft ist

1. Gangkarte mit Leerrohr-Querungen und Schlauchwegen (`check_walkways.py` am Modell): erst nach Montage.
2. Statik der Beete auf dem Flur (Boden trägt heute die Beete eingelassen): Lastfall unverändert, Unterbau offen [A].
3. Ob der Siebkorb in den Biofilter-Deckel Ø 930 passt: Werkstatt.
4. Wärme: weniger Wasser speichert 23 % weniger Wärme (Standort offen, D69).
5. Kosten von Absetzer-, Sumpf- und Filterkästen, die entfallen: kein Preis belegt; die Einsparung ist damit eher größer.

## 9. Folgen und nächste Schritte

1. **DEINE ENTSCHEIDUNG (Ben, mit Leon):** Zielbild S mit den zwei Bedingungen (Pegel-tief-Abschaltung, Siebmessung mit Vortex-Rückfall) ja, Variante T (Sumpf, lehrbuchtreu) oder Rückfall A+ nach v2. Darin stecken für S drei Teilfragen:
   - Pegel Z −150
   - Absetzer streichen (D71 neu)
   - Beete auf dem Flur
2. Bei Ja (Orchestrator): Netzliste v4 (Kanten K01 bis K07, K17 bis K23, K56 bis K59 streichen, Pumpen in den Pool) und Roadmap umbauen. Ein Planer schreibt M10-S3 bis S7 auf das Zielbild und die Ordnung v2 neu. M10-S2V wird geschlossen.
3. Werkstatt vor der ersten v2-Montage: Schlauch-Baustein (Polylinie mit Radius, Schelle, Tülle), Siebkorb-Aufnahme im Biofilter-Deckel, Leerrohr-Querung mit Zugang, Schlamm-Durchführung im Fundamentring.
4. Pumpenwahl: Tauchpumpe 55 l/min bei 2,3 m, lebensmittelecht, Europa (D76), als Recherche-Schritt.
5. Bei Nein: A+ nach Ordnung v2 umverlegen (Luft und Frischwasser oberirdisch), alles andere bleibt.

Geprüft gegen:
1. `data/leitungstrassen.json` (Variante A+ über `scripts/leitungen.laden_variante()`), `data/leitungsnetz.json`, `data/system-specs.json`, `data/params.json`, `data/beschaffung/*.json`
2. `docs/research/R44`, `R45`, `R47` (mit R47b/c), `R49`, `R50`, `R51`, `R53`, `R54`, `R55`; `docs/model-maengel.md`, `docs/hydraulics.md`, `docs/system-concept.md`, `docs/packages/n-technik-innen.md`, `docs/decisions.md` D26, D55, D61, D67, D71, D72, D75, D77, D81, D84 bis D87
3. Befehle: `python -X utf8 scripts/r57_rechnung.py` (alle Abschnitte, einschließlich `station`), `python -X utf8 scripts/check_leitungsordnung.py` (Bestand und Testtrassen)

Offen: siehe Abschnitt 8 und 9.
