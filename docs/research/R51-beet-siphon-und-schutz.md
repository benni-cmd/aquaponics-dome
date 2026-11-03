# R51 — Beet-Siphon und Siphon-Schutz (Standardteile, Schutzkorb, Reinigungszugang)

**Art:** Recherche, Rechnung und Spezifikation, KEIN Bau, kein Modell-Umbau. Auftrag Ben 03.11.2026 („vorbereitend die 100 % sicheren Teile, Standardgeräte suchen, Selbstbau nur wenn super simpel; z. B. ein Schutzgitter im Substratbeet, das den Siphon freihält“). Unabhängig von E20/E21 und vom Subtank; das Beetablauf-Niveau Z −100 bleibt wie vorgegeben (aber siehe Befund 2).
**Herkunftsmarken:** [Q] Quelle selbst gelesen · [E] eigene Rechnung (`scripts/r51_rechnung.py`, Aufruf `python -X utf8 -I scripts/r51_rechnung.py`) · [A] Annahme. „Kandidat“ = nur Suchausschnitt oder eine Quelle.

## Antwort zuerst (fünf Punkte)

1. **Der Siphon selbst ist schon ein Standardbau und „super simpel“: ja.** Standrohr d25, Glocke d75 mit Kappe, zwei gesägte Schlitze, alles PVC-U-Katalogteile. Ein fertiger Zukauf-Siphon bringt hier nichts: Die gefundenen Kits (US-Zoll, Standrohr 1″ ≈ ID 26,6 mm) sind für kleine Beete gebaut, kein Datenblatt nennt einen Durchsatz, und ein 1″-Standrohr entleert unser Beet in 2,9 bis 4,1 min statt 4,3 bis 6,1 min (das ist die in R45 verworfene Variante d32) [Q, E].
2. **L03 (d25 gegen d40) löst eine einzige gekaufte Reduktion:** PVC-U-Klebefitting „Reduktion kurz 40 × 25 mm“ unter dem Bulkhead (Katalogteil, z. B. Weinmann-Schanz 93 049 64 oder Georg Fischer D40AG-D25IG), dann Einzelabgang d40, Sammelleitung d50. Das Bauteil bleibt d25 (so schon R45).
3. **Der Schutz ist der Hebel, und hier ist Kaufen besser als Selbstbauen:** Ein Korb aus **Edelstahl-Lochblech 1,5 mm mit Rundloch 5 mm** (Standard-Tafelware „RV 5-8“) hält Korn ab 8 mm UND ab 12 mm zurück, hat 45× die Standrohr-Fläche offen und ist ziehbar. Damit hängt der Schutz nicht mehr an der Körnungsentscheidung (W40-Konflikt gelöst). Selbst bohren (168 Löcher je Schutz, 14 Schutze) ist **nicht** super simpel.
4. **Reinigungszugang (fehlt heute): ein Schacht d110 aus Rohrstück und Kappe durch den Siebboden bis über die Medienoberfläche** (super simpel: ja), plus das Ziehen des Standrohrs, das den Wasserraum in 11 bis 16 min leert [E].
5. **Zwei Befunde am Bestand, die du kennen musst:** (a) Die Glocke steht auf dem Siebboden, der Siphon leert deshalb nur das Medium; der **Wasserraum unter dem Sieb (420 bis 640 l je Beet, zusammen etwa 6,4 bis 7,8 m³) bleibt dauernd gefüllt**, anders als das Pitch-Register B08 sagt. (b) Der Beetablauf Z −100 liegt 92 mm **über** dem Rohrende des Bauteils (Z −192) und 57 mm über der Innenseite des Wannenbodens (Z −157).

---

## 1. Funktion des Glockensiphons im Flood-and-Drain-Beet

**Prinzip [Q UH BIO-10, Q Aquaponics411, Q Aquifarm]:** Zulauf füllt das Beet, bis der Wasserspiegel die Standrohrkante erreicht und in das Standrohr überläuft. Die Glocke (oben dicht, unten mit Schlitzen oder Zähnen) schließt das Standrohr gegen Luft ab; das überlaufende Wasser reißt die Luft aus dem Ablauf, das Standrohr läuft voll und saugt das Beet leer, schneller als der Zulauf nachfüllt. Sinkt der Spiegel auf die Lufteintrittsöffnung (Schlitzoberkante, Zähne, Schnorchel), strömt Luft ein, der Siphon reißt ab, das Beet füllt sich wieder.

**Auslegung für unser Beet (aussen_933 mit Maßen aus `ibc_beet.md`):**

| Größe | Wert | Herkunft |
|---|---|---|
| Fläche innen | 2,57 m² (2905 × 885); aussen_800: 1,95 m²; innen_933: 1,61 m² | [E] |
| Ablaufvolumen (Standrohrkante z 527 bis Schlitz-Unterkante z 277, Porosität 40 %) | 257 l (R45: 234 l); aussen_800 195 l; innen 161 l | [E] gegen [Q R45] |
| Siphon-Durchsatz d25 (ID 22,0), Druckhöhe 0,30 / 0,45 / 0,60 m | 38 / 47 / 54 l/min | [E] wie R45 nachgerechnet |
| **Entleerzeit** | 4,3 bis 6,1 min (234 l) | [E] |
| Zulauf je Beet (Tropfrohr 200–500 l/h) | 3,3 bis 8,3 l/min | [Q ibc_beet.md, R03] |
| **Flutzeit** bis zur Standrohrkante | 28 bis 71 min (234 l) | [E] |
| Zyklen je Stunde | etwa 0,8 bis 1,8 (K11 rechnet 2/h bei 7,8 l/min: 30 min Flutung) | [E] |
| Verhältnis Siphon zu Zulauf | 4,6 bis 16,5 | [E] |

**Hinweis zur Beauftragung:** „Flutungs-/Entleerzeit 4 bis 6 min“ ist die **Entleerzeit**. Die Flutzeit liegt bei 28 bis 71 min; die „5–8 min Spitze je Flutung“ in K11 meint den Ablauf. Das ändert nichts an den Netzwerten (54,5 l/min Mittel = 7 × 234 l × 2/h).

**Verhältnisse im Bauteil [E]:** Ringraum zwischen Standrohr und Glocke 3248 mm² (8,5 × Standrohr-Fläche 380 mm²); Glockenschlitze 800 mm² (2,1 ×); Luftloch 100 mm². Glocke zu Standrohr 3 : 1 liegt im Bereich der Tabelle bei [Q Aquifarm] (Standrohr 1″ → Glocke 2–3″, Schutz 4–6″); die 2 : 1 aus [Q UH BIO-10] ist dort die Faustregel für kleine Beete. Schutz zu Glocke: heute 110 : 75 = 1,47; UH empfiehlt etwa 2 (Hand und Schnorchel müssen Platz haben), Aquifarm nennt für 3″-Glocke 4–6″, also 100–150 mm: d110 ist die untere Grenze.

**Fehlerarten und Gegenmittel** (Aquaponics411 und Aquifarm sind unabhängige Quellen und decken sich; GoGreen nur als Suchausschnitt):

| Fehler | Ursache | Maßnahme in unserem Beet |
|---|---|---|
| Trickle / Siphon startet nicht | Zulauf zu klein, Glocke undicht (Kappe, Bohrung), Ablauf-Leitung fängt Luft, Medium verdeckt die Glocken-Öffnungen | Kappe verkleben; Schutz hält Medium weg; am Muster mit 3,3 und 8,3 l/min testen (**kein Beleg für eine Mindest-Zulaufmenge gefunden**) |
| Dauerlauf (Siphon reißt nicht ab) | Zulauf zu hoch, Öffnungen zu tief oder untergetaucht, Glocke am Boden abgedichtet, Wurzeln versperren den Lufteintritt, Rückstau im Ablauf | Zulauf ≤ 1/4 des Siphons (heute 1/4,6 bis 1/16); Schlitze statt Zähne; Einzelabgang d40 muss frei auslaufen (R45: kein Rückstau, Sammler mit Gefälle und Lüftung) |
| Verstopfung | Medium, Wurzeln, Schlamm, Biofilm/Algen über den Öffnungen oder im Standrohr | Schutzkorb (Abschnitt 3); Pflanzen-Freihaltezone; Wartungsplan unten |
| Unregelmäßige Zyklen | mehrere Beete gleichzeitig, Luftpolster, Ablauf getaucht | höchstens 3 Beete gleichzeitig (R45) |

**Wartung [Q Aquifarm, übertragen]:** wöchentlich einige Zyklen beobachten (langsamer Start, unvollständiger Ablauf); monatlich Schutz auf Wurzeln, verschobenes Medium, verstopfte Öffnungen prüfen; alle paar Monate Glocke ziehen (Schleim, Wurzeln, Schnecken) und Standrohr innen prüfen; je Jahreszeit den Auslauf. Für 14 Beete heißt das 14 Handgriffe im Monat: **der Schutz muss ohne Werkzeug ziehbar sein** (Abschnitt 3).

---

## 2. Standardsiphons kaufen

Gefunden wurden nur Kits für Hobby-Aquaponik; **kein Anbieter nennt einen Durchsatz in l/min oder gal/min** (geprüft: The Aquaponic Source, Desert Aquaponics, Practical Aquaponics, Go Green; Perth Aquaponics und Ofera waren nicht lesbar).

| # | Hersteller / Modell | Maße (Standrohr / Glocke / Schutz) | Bauhöhe | Material, Anschluss | Durchsatz | Preis (grob) | Quelle |
|---|---|---|---|---|---|---|---|
| 1 | The Aquaponic Source, **AquaParts 12in Bell Siphon with Media Guard** (CMFAS108; auch bei Go Green Aquaponics) | Siphon 2″ × 12″, Schutz 4″ × 12″, Standrohr nicht genannt | für 12″ Medium (nicht über 13″; unter 11″ Standrohr kürzen) | Material nicht genannt („handcrafted in Colorado“); Bulkhead nicht sicher enthalten, 3/4″ FPT separat | nicht genannt | etwa 36 USD | [Q theaquaponicsource.com](https://www.theaquaponicsource.com/shop/plumbing-parts-kits/bell-siphons/aquaparts-bell-siphon-and-media-guard/); Maße bestätigt im Suchausschnitt von [Go Green](https://gogreenaquaponics.com/products/aquaparts-12-bell-siphon-with-media-guard) |
| 2 | Desert Aquaponics, **Auto Bell Siphon for 100+ Gallon Systems** | Standrohr 1″, Glocke 2″ mit Kappe und Schnorchel, Schutz 4″ dünnwandig, auf Medienoberfläche + 2″ zugeschnitten | Wasserstand wählbar 5–12″ | PVC; Adapterpaar mit O-Ringen, 2 Bögen 90°, Rohrstücke 7″ und 4″ | nicht genannt | 24–28 USD | [Q desertaquaponics.org](https://desertaquaponics.org/store/bell-siphon-large) |
| 3 | Practical Aquaponics (AU), **Autosiphon (Bell Siphon) Kit** AP-ASA | vormontiert: Standrohr, Glocke, Außengehäuse (Steinschutz) mit Schraubdeckel; Maße nicht genannt | nicht genannt | Ablauf-Fittings und Rohr enthalten; Material nicht genannt | nicht genannt (Abgleich mit dem Zulauf nötig) | 99,90 AUD (eine Fundstelle 170) | [Q aquaponics.net.au](https://www.aquaponics.net.au/shop/products/38.php) |
| 4 | Perth Aquaponics, Bell Auto Siphon Kit | für Beete bis 200 l und 200 mm Tiefe | 200 mm Medium | nicht lesbar | nicht lesbar | – | Kandidat ([perthaquaponics.com.au](https://perthaquaponics.com.au/Bell_Siphon), Seite nicht abrufbar) |
| 5 | Ofera (AT), Bell Siphon for Aquaponics Kit | nicht lesbar | – | – | – | – | Kandidat, der einzige gefundene EU-Händler ([ofera.at](https://ofera.at/en-us/products/bell-siphon-aquaponics-kit), Seite nicht abrufbar); **vor einer Bestellung Datenblatt anfordern** |

Nicht geeignet: das SeaHawk „Flood & Drain Fittings Kit“ (13/19-mm-Schlauchtüllen, Überlauf mit Sieb) ist ein Standrohr-Überlauf **ohne** Siphon [Q aquagardening.com.au], und der „Locked-in Media Guard“ von Go Green ist laut Händlerangabe für Dauerfluss-Systeme und nicht mit Glockensiphons gedacht (Suchausschnitt, Kandidat).

**Passt eines zu d25 / d40 / d50?** Nein, nicht ohne Anpassung. Zwei Gründe:
1. **Maßsystem:** US-Zoll (NPS) hat andere Außendurchmesser als EN 1452: Schedule-40-Rohr 3/4″ hat 26,7 mm, 1″ 33,4 mm, unser d25 hat 25 mm und d32 hat 32 mm; die Steckverbindungen passen nicht aufeinander [A, bekannte Normmaße]. Ein 1″-Kit wäre zudem ein Schritt größer als unser Standrohr (R45 Variante B: Entleerzeit 2,4–3,4 min, Spitze 70–100 l/min je Beet, „kein Gewinn“); mit gleichem Modell: ID 26,6 mm → 57–82 l/min, ID 20,9 mm (3/4″) → 34–49 l/min [E].
2. **Beetgröße:** Die Kits zielen auf Beete mit etwa 300 mm Medium und IBC-Größe [A, aus der Produktbeschreibung]; ob sie 47–54 l/min sicher auslegen, belegt kein Datenblatt.

**Lösung L03 (Vorschlag, Netz-Anpassung ist schon in Version 3):**

| Strecke | Teil | Beschaffung |
|---|---|---|
| Standrohr im Beet | PVC-U d25 × 1,5 (ID 22,0), in Bulkhead D36 | Standard (R45: Bevo-Händlerblatt, Engineering Toolbox) |
| Übergang unter dem Bulkhead | **PVC-U Klebefitting Reduktion kurz d40 × d25** (Klebestutzen d40, Klebemuffe d25) | Standard: [Weinmann-Schanz 93 049 64](https://weinmann-schanz.de/de/de/Installation/Rohrsysteme/Klebefittinge-aus-PVC-U/PVC-U-Klebfittings/PVC-U-Klebefitting-Reduktion-kurz/PVC-U-Klebefitting-Reduktion-kurz-40-x-25-mm-mit-Klebstutzen-u-Klebmuffe-sid313937.html), Georg Fischer „TP PVC-U Reduzierung D40AG-D25IG“ ([Vanmarcke](https://blue.vanmarcke.com/de_CH/p/20020205)) [Q, beide nur Katalogseite gelesen, PN und Preis nicht geprüft] |
| Einzelabgang | PVC-U d40 × 1,9, ≤ 0,5 m, Gefälle ≥ 2 % | Standard (R45) |
| Sammelleitung K14/K30 | PVC-U d50 × 2,4 mit Gefälle | Standard (R45) |

Das ersetzt die „zwei Stück Reduzierung d40/d32 + d32/d25“ aus R45 durch **ein** Teil. Das Bauteil bleibt d25; kein Eingriff am Siphon.

---

## 3. Siphon-Schutz und Reinigungszugang

**Zweck des Schutzes [Q UH BIO-10, Q Aquifarm, Q AquaParts-Seite]:** ein poröses Rohr um Standrohr und Glocke, das Medium und Wurzeln fernhält, Wasser durchlässt und die Glocke ohne Medienausbau zugänglich macht. Er ist laut UH „nicht notwendig für die Funktion“, aber für die Wartung „well worth“. UH: etwa doppelter Glockendurchmesser, etwas länger als die Glocke. Aquifarm: Öffnungen größer als der Standrohr-Querschnitt, abnehmbar, Platz für Hand und Werkzeug, Öffnung gegen Korn bemessen (keine Maßangabe). Händler: Schutz drehen oder ziehen, um Wurzeln abzuschneiden (Herstellerangabe, unbelegt).

**Befund zum heutigen Schutz [E]:** 12 Durchbrüche 12 × 12 mm in drei Ringen (z 40/120/200) = 1728 mm² (4,5 × Standrohr). Im letzten Ablaufabschnitt (Spiegel unter etwa z 46) strömt das Wasser nur durch den untersten Ring: 4 Löcher = 576 mm² (1,5 ×), Anströmung 1,45 m/s bei 50 l/min. Das drosselt wahrscheinlich das Ende des Ablaufs und hält Körner ab 8 mm nicht zurück.

**Lochgröße gegen Korn (Konflikt W40-BEET gelöst) [E, Regel: Öffnung ≤ 0,75 × kleinstes Korn, Annahme]:**

| Medium | Handelsware | Öffnung höchstens |
|---|---|---|
| Blähton 8–16 mm (Standard im Handel, 5–80 l-Säcke, Hornbach, Plagron u. a. [Q Suchtreffer]) | ja | **6 mm** |
| Korn ab 12 mm (R47/W40-Vorgabe) | **Blähton 10–20 / 12–20 nicht gefunden**; Lavagranulat 16–32 mm (Hornbach, 500-l-Big-Bag) und Kies sind erhältlich [Q Suchtreffer] | 9 mm |

Folgerungen: (1) **Öffnung 5 mm deckt beide Fälle ab**, damit ist der Schutz von der Körnungswahl entkoppelt. (2) R47 „Korn 12–20 mm“ ist als Blähton nicht Handelsware; wenn Ben Blähton will, ist 8–16 mm der Kauf und dann gilt 6 mm Öffnung auch für den **Siebboden** (heute real D8 gegen Korn ab 8: Korn setzt sich in die Löcher). (3) Das Modell bildet die Löcher bewusst vereinfacht ab (quadratische Durchbrüche, Rechenzeit).

**Varianten des Schutzes:**

| Variante | Beschaffung | Offene Fläche | Urteil |
|---|---|---|---|
| **S-A: Korb aus Edelstahl-Lochblech** 1,5 mm, 1.4301, Rundloch 5 mm / Teilung 8 mm (RV 5-8, Lochanteil 35 %), Zuschnitt 366 × 340 mm, zum Zylinder d110 gerollt, Naht überlappt und vernietet | Tafelware 1000 × 2000 mm ([ehorst.de](https://www.ehorst.de/Lochblech-Edelstahl-1-4301-RV-5-8-1-50-1000-2000-mm-beids-K240-Folie-DIN24041-1003438.html), Tafel 10 Zuschnitte [E]); Rollen beim Metallbauer oder per Hand bei dünnerem Blech [A, nicht belegt] | unten 140 mm: 17 160 mm² = 45 × Standrohr | **empfohlen**; korrosionsfest, wurzelfest, ziehbar, 0,96 kg |
| S-B: PVC-U-Rohr d110 selbst gebohrt (6 Zeilen × 28 Löcher d6) | Rohr Standard (KG/HT DN100 hat 110 mm Außen-Ø) | 4750 mm² = 12,5 × | **nicht super simpel**: 168 Löcher je Schutz, 14 Schutze = 2352 Löcher (Zeit nach [A] 30–45 min je Stück mit Ständerbohrmaschine und Schablone, 7–10 h); nur sinnvoll für ein Muster |
| S-C: PVC-U-Rohr mit gesägten Schlitzen 6 × 60 mm, 20 am Umfang | Selbstbau | 7200 mm² = 18,9 × | machbar, aber Schlitzbreite 6 mm lässt Korn 8 mm nur knapp stehen; Brucharbeit am Stegrand [A] |
| S-D: Kunststoff-Siebrohr Ø110 (Teich-/Koi-Zubehör) | Händlertreffer ohne Lochmaß (eBay, 30–48 EUR) | unbekannt | Kandidat, Lochmaß vor Kauf prüfen |
| S-E: Ansaugsieb DN100 (verzinkt, Maschen 4–6 mm) | Händler (aquatechnika) | – | **nein**: verzinkter Stahl im Fischwasser (Zink ist Fischgift [A]) |
| S-F: Brunnenfilterrohr PVC-U (DIN 4925, Schlitz fein) | Standard | Dränrohr 1,2 mm Schlitz: ≥ 80 cm²/m | **nein**: zu feine Schlitze, verwachsen mit Biofilm; Schutz soll Korn halten, nicht filtern [A] |
| S-G: 3D-Druck (Printables „Aquaponics syphon media guard“) | Selbstbau | – | nur Kandidat, Seite nicht lesbar |

**Reinigungszugang zum Wasserraum unter dem Siebboden (fehlt heute):**
- **Reinigungsschacht** (neu): PVC-U-Rohr d110 × 3 senkrecht durch den Siebboden, Unterkante 15 mm über der Wannen-Innenseite, Oberkante 20 mm über der Medienoberfläche, oben Kappe d110 (lose oder Schraubverschluss). Hand, Saugschlauch d ≤ 75 oder Spülschlauch passen hinein. Standardteile: Rohr plus Kappe. Lage: Stirnende gegenüber dem Siphon, x = −Li/2 + 250 [A] (freie Lücke zwischen den Stützklötzen: Abstand 150 mm zum ersten, 192 mm (aussen_800) bzw. 236 mm (aussen_933) zum zweiten, Platzbedarf je Klotz 85 mm [E]).
- **Standrohr ziehen** (R47-Vorschlag: Steckverbindung unter dem Boden): leert den Wasserraum durch die Bulkhead-Bohrung D36 in 11 bis 16 min (Cd 0,6, fallender Spiegel, [E]) und spült Schlamm mit. Das ist die einzige Entleerung des Wasserraums und kostet kein neues Teil.
- **Pflanzen-Freihaltezone** Ø 250 mm um die Siphonachse, in der der Integrator keinen Netztopf setzt [A]: so wachsen keine Wurzeln durch die Schutzöffnungen.

**Ist Selbstbau „super simpel“?**

| Teil | Antwort | Begründung |
|---|---|---|
| Standrohr + Glocke + Kappe | **ja** | 3 Rohrstücke sägen, 1 Kappe kleben, 2 Schlitze sägen, 1 Loch bohren [Q UH BIO-10 beschreibt denselben Weg]; was bleibt, ist das Einstellen am Muster |
| Schutz gebohrt | **nein** | 168 Löcher je Stück, 14 Stück |
| Schutz aus Lochblech | **bedingt ja** | Lochung ist Kaufware; Rollen und Nieten sind Handarbeit (10 Zuschnitte je Tafel) |
| Reinigungsschacht | **ja** | Rohrstück + Kappe |
| Reduktion d40 × d25 | Kaufteil | Katalog |

---

## 4. Bewertung: Kaufteil, Selbstbau, heutiges Bauteil

| Teil | Kaufteil | Selbstbau | Heutiges Bauteil | Empfehlung |
|---|---|---|---|---|
| Gesamtsiphon (Kit) | US-Zoll, kein Durchsatzbeleg, 1″ zu groß, EU-Händler nicht lesbar; Funktion: mittel; Risiko: Maßsystem | – | d25/d75 passt zu R45 (38–54 l/min), Funktion belegt nur durch Rechnung | **behalten**; kein Kit kaufen |
| Standrohr + Glocke | Katalog-PVC | gesägt | wie Selbstbau | **behalten**; am Muster tunen (Schlitze, Luftloch, Zulauf 3,3 und 8,3 l/min) |
| Medienschutz | Lochblech-Zuschnitt (Halbzeug) | Bohren aufwendig | 12 Löcher 12 × 12: hält Korn 8–12 nicht, drosselt das Ablaufende (Befund) | **kaufen** (S-A, Lochblech 5 mm); Modell bis dahin als „Platzhalter“ |
| Reduktion d40 × d25 | Katalog | – | fehlt (Port d25, Netz d40) | **kaufen** (löst L03) |
| Reinigungsschacht | Rohr + Kappe | trivial | fehlt | **selbst bauen** (aus Standardteilen) |
| Siebboden-Lochung | – | – | real D8 (Modell D12) gegen Korn 8–16 | auf **D6** ändern, wenn Blähton 8–16 gewählt wird |

**Risiken, die offen bleiben:** Anspringverhalten bei 3,3 l/min Zulauf (kein Beleg, nur Muster klärt es); Lochblech-Korb verwächst mit Wurzeln (Gegenmittel Freihaltezone und monatliches Ziehen, [Q Aquifarm] Monatsprüfung); Edelstahl 1.4301 im Gewächshaus-Wasser mit Dünger: Lochkorrosion nicht belegt untersucht [A].

---

## 5. Modellier-Spezifikation (nur Spezifikation, kein Bau)

**Bezug:** Bauteil-KS `ibc_beet` (Z = 0 Wannenunterseite, X längs, Y quer), Maße aussen_800 / [innen_933]. Absolut (aussen): Wannenunterseite Z −162, Siebboden-Oberkante Z 100, Standrohrkante Z 365, Medienoberfläche Z 400. **Höhe über dem Beetablauf Z −100** (festgelegt): Siebboden-OK +200, Standrohrkante +465, Medienoberfläche +500, Wannen-Innenseite −57 (siehe Befund 2). Siphon bei x = Li/2 − 200 (aussen_800: 1096, innen: 708), y = 0.

| Nr. | Teil | Maße | Lage (z lokal / Höhe über Siebboden-OK 262 [274]) | Öffnungen | Gewicht | Beschaffung |
|---|---|---|---|---|---|---|
| T30e-1 | **Standrohr** (behalten) | PVC-U d25 × 2 (real 1,5), Länge 557 [569] | z −30 bis 527 [539]; Kante +265 | – | 0,11 kg | Standard |
| T30e-2 | **Glocke** (behalten) | PVC-U d75 × 3, h 295, Deckel 3, innen bündig | z 262 bis 557 [274–569]; steht auf Siebboden | 2 Schlitze 10 × 40 bei +15…+55 (±X); Luftloch 10 × 10 bei +50 (−Y) | 0,30 kg | Standard (Kappe d75) |
| T30e-3 | **Reduktion** (neu) | PVC-U Reduktion kurz d40 × d25, Länge etwa 50 mm [A] | Port bei z −30 (abs −192); Klebemuffe d25 oben, Klebestutzen d40 unten | – | etwa 0,05 kg [A] | Standard |
| T30e-4 | **Medienschutz S-A** (ersetzt `guard`) | Rohr d110 (Innen 107) × 1,5, h 320, V2A; Deckel Kappe d110 PVC-U, lose | z 262 bis 582 [274–594]; lose auf Siebboden; Oberkante +20 über Medium | real: Rundloch d5, Teilung 8 versetzt, alle Zeilen (35 %); **Modellvereinfachung:** 2 Ringe × 12 Schlitze 5 × 50 bei z 272–322 und 342–392 (6000 mm² = 15,8 × Standrohr) | 0,96 kg + Deckel 0,15 | Halbzeug kaufen, Rollen/Nieten Selbstbau |
| T30e-4b | Medienschutz S-B (Variante, PVC-U gebohrt) | d110 × 3, h 320 | wie oben | 168 Löcher d6 in 6 Zeilen (z 272–332) | 0,43 kg | Selbstbau (nicht super simpel) |
| T30e-5 | **Reinigungsschacht** (neu) | PVC-U d110 × 3, Länge 562; Kappe d110 (15 mm hoch) | x = −Li/2 + 250 (aussen_800: −1046), y = 0; z 20 bis 582 [594], Kappe bis 597 [609]; im Siebboden Ausschnitt d114, im Medium Ausschnitt d110 | 2 Kerben 30 × 30 am Fuß; oben offen unter der Kappe | 0,94 kg | Standard (Rohr + Kappe), Selbstbau trivial |
| T30e-6 | **Siebboden-Lochung** (Änderung, nur bei Blähton 8–16) | PP 8 mm, Loch d6 statt d8 | z 254 bis 262 | Raster wie heute | wie heute | Selbstbau/Lieferant |
| T30e-7 | **Freihaltezone** (Hinweis an Integrator) | Kreis Ø 250 um (x_sp, 0) und um den Schacht | Medienoberfläche | kein Netztopf | – | – |

**Wasserstände in der Spezifikation:** Standrohrkante z 527 (35 mm unter der Medienoberfläche z 562, aussen_800/933); Luftlochmitte z 312; Siphon reißt ab bei z 277…317 [E]; höchster Wasserstand im Betrieb z 527 = Schacht-Oberkante minus 55.

**Prüfpunkte für die Werkstatt:** Schutz-Innenraum muss Glocke frei lassen (Ringspalt 16 mm), Schacht steht zwischen zwei Stützklötzen, kein Teil schneidet den Siebboden-Raster der Stützen (Y = 0-Reihe), Medium-Ausschnitte für Schutz und Schacht je d110.

---

## Befunde am Bestand (nicht von mir geändert, Meldung an den Orchestrator)

1. **Wasserraum bleibt gefüllt [E aus `scripts/workshop/ibc_beet.py` Zeile 45/111, am Modell nicht gemessen].** Die Glockenunterkante liegt auf z_m0 (Siebboden-Oberkante), die Schlitze 15 bis 55 mm darüber; der Siphon reißt dort ab. Das entspricht R45 (234 l Ablauf), **nicht** der Aussage „leert bis zur Bodenplatte … nichts steht“ (R47 Abschnitt 4, Pitch B08). Stehendes Wasser unter dem Sieb: aussen_933 640 l, aussen_800 485 l, innen 420 l; Summe Zielstand 8 × 485 + 6 × 420 = 6400 l (alter Stand 7772 l). Folgen: Schlamm- und Sauerstoffrisiko im Dunkeln, Reinigungszugang wird Pflicht; ein bis zum Boden reichender Siphon würde das Ablaufvolumen auf etwa 870 l (aussen_933, 3,7 ×; Ablaufzeit 16 bis 23 min) steigern und den Beet-Sumpf (500 l) sprengen. Entscheidung nötig: akzeptieren (mit Schacht), Wasserraum flacher machen (Klötze niedriger), oder Siphonauslegung ändern.
2. **Z −100 [A] (K14) gegen Bauteil-Port:** Rohrende des Bulkheads liegt bei z −30 = abs −192, die Innenseite des Wannenbodens bei abs −157. Ein Beetablauf auf Z −100 läge **über** dem Wannenboden. Netz (K14/K30) und Port müssen abgeglichen werden (Montage/Orchestrator).
3. **Pitch B08** („Siphon leert bis zum Boden“) ist so nicht belegt; Wortlaut nach Befund 1 prüfen.
4. **W40-BEET** ist mit R51 entscheidungsreif: Medienschutz S-A (Öffnung 5 mm), Reinigungsschacht T30e-5, Körnung Blähton 8–16 (Handelsware) mit Siebloch d6 **oder** Korn ab 12 mm (Sonderware, Lava/Kies) mit Öffnung bis 9 mm.

---

**Geprüft gegen:** `docs/parts/ibc_beet.md`, `scripts/workshop/ibc_beet.py`, Roadmap W40-BEET und L03, R45 (Abschnitt 1 und 3), R47 (Abschnitt 4), `data/leitungsnetz.json` K11/K14/K30/K58, `data/layout.json` (z0), Quellen: UH-CTAHR BIO-10 (Volltext gelesen), Aquaponics411, Aquifarm (Zusammenfassung, Seite selbst nicht abrufbar), The Aquaponic Source, Desert Aquaponics, Practical Aquaponics, SeaHawk, Weinmann-Schanz/Vanmarcke (nur Katalogseiten), ehorst.de (Suchausschnitt), Hornbach/Plagron (Suchausschnitt); Rechnung `scripts/r51_rechnung.py`.
**Offen:** (ICH) Muster- und Prüfplan für Anspringverhalten bei 3,3 l/min Zulauf, Lochblech-Zuschnitt beim Metallbauer anfragen, Ofera-/Perth-Datenblatt nachholen; (DEINE ENTSCHEIDUNG) Wasserraum bleibt gefüllt akzeptieren oder ändern, Körnung Blähton 8–16 oder ab 12 mm; (DEINE HANDLUNG) keine.
