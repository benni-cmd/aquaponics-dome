# R44: Sind Absetzer, Feinfilter und Biofilter bei 346 kg Fisch nötig, richtig groß, und wie viel Platz sparen kleinere Stufen?

**Priorität:** H · **Auftrag seit:** 01.11.2026 · **Bearbeitet:** 01.11.2026 · **Zielparameter:** keine geändert (der Bericht schlägt nur vor; Entscheidung Orchestrator mit Ben). Herkunft: Q Quelle, E eigene Rechnung, A Annahme; „Kandidat“ = weniger als zwei unabhängige Quellen.

## Kurzantwort (je Filter: nötig · Größe · Platz)

| Filter | Nötig? | Größe heute gegen Last 346 kg / 3,46 kg Futter/Tag | Platz (Grundfläche beide Linien) |
|---|---|---|---|
| **Absetzer** `tank_klein` ×2 | **Teilweise.** Eine mechanische Stufe ist nötig, weil ein Teil des Wassers über NFT läuft (Q FAO 589 Kap. 4.4.2, Q SRAC 454). Ein Swirl-Absetzer im Teilstrom ist dafür **nicht** belegt nötig. | Oberfläche und Verweilzeit sind reichlich (E), aber ein Swirl fängt nur ca. 23 % der Feststoffmasse (Q Davidson/Summerfelt 2005). | **0,91 m²** (E); entfällt im Kandidaten A. |
| **Feinfilter** `feinfilter` ×2 | **Ja für den NFT-Zweig, für die Beete nicht belegt.** Der FAO-Auslöser (>15 kg/m³ oder >50 g/m²/Tag) wird bei 346 kg **nicht mehr erreicht** (12,1 kg/m³, 45 g/m²/Tag, E). | Gewebe 100 µm fängt im Versuch nur 21 % der Schwebstoffe, 60 µm 48 % (Q Mortensen). Siebbelastung 8 m/h ist **unbelegt** (A). | **0,53 m²** (E, aktuelles Bauteil T55, nicht die 400 × 300 × 500 aus dem Auftrag). |
| **Biofilter** `tank_gross` ×2 | **Teilweise.** FAO: Beete sind „perfekte Biofilter“, ein eigener Biofilter nur für NFT/DWC; SRAC 454 mahnt, Aquaponik-Biofilter nahe an RAS-Regeln auszulegen. | 471 m² K1 decken den FAO-Fall 2,1-fach, den Messwert (0,215 g/m²/Tag) nur 0,78-fach (E). Die Hälfte (ein Tank) trägt nur zusammen mit den Beeten. | **1,73 m²** (E); ein Tank spart **0,87 m²**, beide **1,73 m²**. |
| **Beete** `ibc_beet` ×14 | Ja, sie tragen mit. Wie viel Nitrifikation sie wirklich leisten, ist **nicht gemessen** (nur Abstract-Werte aus Perlit/Kies, 14–110 g TAN/m³/Tag). | 8,2 m³ liegen nach FAO-Tabelle 7–9-fach über der Last, nach Messwerten 1,2–5-fach bei voller Wirksamkeit, 0,3–0,5-fach bei dem Simulator-Ansatz von 25 %. | kein Platzgewinn, schon gebaut |

**Gesamturteil:** Die vier Tanks plus zwei Siebe sind **für diese Last nicht übertrieben, aber zu viel hintereinander**. Zwei mechanische Stufen (Absetzer und Sieb) sind bei 1,04 kg Feststoff/Tag und niedriger Besatzdichte mehr, als zwei Quellen verlangen. Zwei Biofilter-Tanks sind gerade die Mitte der Raten-Spanne. Eine Biofilter-Größe von 0 % ist durch keine Quelle gedeckt. **Kandidat A** (Absetzer entfällt, Sieb bleibt als einzige Mechanikstufe, nur ein Biofilter-Tank) spart **1,77 m²** Grundfläche; **Kandidat B** (Absetzer bleibt, Sieb nur am NFT-Zweig, ein Biofilter-Tank) spart **1,40 m²**. Beide sind Kandidaten (Gründe unten), keine Freigabe.

## Fünf wichtigste Befunde
1. **Die Auslegungslast ist veraltet.** `filter-konzept.md` rechnet mit 475 kg / 4,75 kg Futter. Seit D61 gelten 346 kg / 3,46 kg: TAN 130 statt 178 g/Tag, Besatz 12,1 statt 17 kg/m³, Futter 45 statt 62 g/m²/Tag (E). Damit entfällt die R28-Begründung für den Feinfilter („17 kg/m³ und 62 g/m² liegen über dem FAO-Auslöser“).
2. **Der FAO-Auslöser meint eine Notlösung, keine große Anlage.** FAO 589 Kap. 4.3.4 empfiehlt bei >15 kg/m³ **und/oder** >50 g/Tag je m² Bett einen zusätzlichen Fänger und beschreibt dafür einen Socken am Zulauf oder einen 3–5-l-Eimer im Beet. Die ganze FAO-Tabelle 8.1 endet bei 3 m³ Fischtank; unser Becken hat 28,5 m³ (E). Die Schwellen sind also Richtwerte aus dem Kleinbereich.
3. **Der NFT-Zweig braucht eine Mechanikstufe, unabhängig vom Auslöser.** FAO 4.4.2: „both types of filters need to be deliberately constructed: first, a physical trap … then a biological filter“. Bei uns gehen laut Netz ca. 38 von 110 l/min je Linie in NFT (E, `filter-konzept.md`).
4. **Die Biofilter-Rate bleibt der größte Unsicherheitsfaktor** (Faktor 2,65 zwischen FAO 0,57 und Messung 0,215 g TAN/m²/Tag). Zwei unabhängige Messungen aus Süßwasser-RAS liegen unter FAO (0,215 und 0,27); keine Messung liegt darüber.
5. **Messwerte für Substratbeete als Biofilter fehlen.** Gefunden wurden nur Abstract- und Zusammenfassungswerte (Perlit 19–80, Kies 14–110 g TAN/m³/Tag). Damit ist „Biofilter 0 %“ nicht belegbar, und „Biofilter 50 %“ hängt am Zufall der Annahmen (Szenariotabelle).

## Lastbasis (neu, D61)
| Größe | Wert | Herkunft |
|---|---|---|
| Fisch / Futter | 346 kg / 3,46 kg/Tag (Spanne 3,08–3,85) | `data/system-specs.json` (D61) |
| Fischwasser, Besatz | 28,5 m³ → **12,1 kg/m³** | E = 346 ÷ 28,5 |
| Futter je Pflanzfläche | 3460 g ÷ 77,0 m² = **45 g/m²/Tag** (nur Beete: 127 g/m², nur theoretisch, da NFT mitträgt) | E, `system-specs.json` |
| TAN | **130 g/Tag** bei 3,75 % Futter (104 bei 3 %, 173 bei 5 %); als N-Masse nach FAO-Rechnung 108 g | E nach Q FAO 589 App. 4: 200 g Futter → 7,5 g „ammonia“ (NH₃-Masse, Faktor 1,2) |
| Feststoffe | **1,04 kg/Tag** (0,30 kg je kg Futter) | E, Q Fort Valley State/SRAC-Folien (Suchzusammenfassung) |
| Kreislauf | 110 l/min je Linie, davon Beete 54,5, NFT 38, Rücklauf 17,5; Absetzer-Teilstrom 12,5 l/min je Linie | `filter-konzept.md`, `leitungsnetz.json` |

## Begründung

### Frage 1 – Absetzer: braucht es einen eigenen Feststoffabscheider? Reicht eine Stufe?
- **Mechanik ist nötig, aber nicht unbedingt als Swirl im Teilstrom.** FAO 589 (Kap. 4.3.4, 4.4.2, 8.1.3): Beete sind Netz- und Biofilter zugleich; NFT/DWC brauchen eine eigene mechanische Stufe; Klärer können „bis zu 60 %“ der entfernbaren Feststoffe fassen [Q FAO, Volltext gelesen]. SRAC 454: Das UVI-System nutzt einen Klärer (ca. 50 % der Feststoffe) **und** Netzfilter-Tanks (die übrigen 50 %), weil „clarification as the sole method“ große Mengen in die Hydroponik schickt [Q SRAC 454, Volltext]. Dieselbe SRAC-Quelle sagt aber auch: Bei **wenig Fisch im Verhältnis zur Pflanzfläche** kann Feststoffabscheidung entbehrlich sein, weil Mineralisation die Nährstoffe liefert; die Wahl hängt an der Futterlast, in zweiter Linie an der Pflanzfläche [Q SRAC 454].
- **Swirl gegen Sieb:** Im 150-m³-Becken fing der Swirl 37,1 % der Schwebstoffe (23 % der Tagesmasse), der Radial-Flow-Absetzer 77,9 % (48 %), ein Mikrosieb im Vollstrom zusätzlich 40–45 % der Tagesmasse; die Autoren nennen das Sieb im Vollstrom „critical“ [Q Davidson/Summerfelt 2005 über Global Seafood Advocate, gelesen; Original ungelesen]. FarmHub/Goddek Kap. 7.4: Klärer sind das übliche Gerät, aber die abgetrennte Menge ist „rather low“, Trommel- oder Scheibenfilter sind wirksamer [Q Goddek u. a. 2019, gelesen].
- **Reicht eine Stufe?** Nach den Quellen: **ja bei dieser Last, als Kandidat.** Gründe: FAO (Fänger im Beet genügt, wenn der Auslöser nicht erreicht ist) und SRAC (geringe Last gegen Pflanzfläche) stützen den Verzicht auf zwei Stufen, aber beide sind qualitativ und gelten für kleinere Anlagen oder UVI-Raftsysteme. Welche Stufe: ein Sieb im Hauptstrom fängt nach Davidson (40–45 %) etwa doppelt so viel Masse wie ein Swirl (23 %); der Swirl hat dafür die Vorteile, dass er nichts zerkleinert und kein Gewebe reinigen muss (Mortensen/NMBU: Siebe zerbrechen Partikel). Der Kandidat A lässt daher den Absetzer entfallen. Kandidat B behält ihn und kürzt das Sieb auf den NFT-Zweig.
- **Dimension des Absetzers (Gegenprobe):** 267 l, 12,5 l/min, Oberflächenbelastung 2,1 m/h gegen 11,2 m/h der Prüfanlage (E). FAO empfiehlt „one-sixth“ des Fischtanks (4,75 m³) oder 10–30 % (2,85–8,55 m³) für das Klärgefäß im Vollstrom; unser Absetzer hat 0,534 m³ = 1,9 % (E). Der Vergleich ist schief, weil FAO vom Vollstrom ausgeht und Teilstrom (Dual-Drain) nicht behandelt.

### Frage 2 – Feinfilter: nötig, Siebbelastung, Maschenweite, Alternativen
- **Auslöser nicht erreicht.** 12,1 kg/m³ < 15 kg/m³ und 45 g/m² < 50 g/m² (E, Q FAO 4.3.4). Das ist der FAO-Maßstab für Beete; der NFT-Zweig braucht unabhängig davon eine Stufe (FAO 4.4.2).
- **Maschenweite belegt nur gegen RAS-Messungen:** 30/60/100 µm → 99/48/21 % der Schwebstoffe [Q Mortensen (Hydrotech, Aal-RAS), über R30 und die Suche bestätigt: 60 µm = 48 %]. T55 verwendet 100 µm (21 %). Ein Mikrosieb im Vollstrom nahm 40–45 % der Tagesmasse (Davidson). Für Gewebe unter ~30 µm gilt: Partikel brechen, Feinstanteil steigt [Q Goddek Kap. 3: <30 µm sind „Fine solids“, durch Sieben nicht mehr fassbar; Q NMBU, Suchzusammenfassung].
- **Siebbelastung: nicht belegt.** Es wurde keine Quelle für m³/h je m² Gewebe in dieser Größe gefunden (Herstellerangaben nur als Gesamtleistung: 15–25 m³/h bei 60-µm-Trommeln, Suchzusammenfassung). T55 rechnet mit 8 m/h [A], R30 hatte 1,6 m/h; das ist Faktor 5 ohne Beleg. Bei 110 l/min = 6,6 m³/h gäbe 8 m/h 0,83 m², 4 m/h 1,65 m², 2 m/h 3,3 m² Gewebe (E).
- **Alternativen und Platz** (Quelle nur für FAO und UVI): Socke/Beutel am Zulauf oder 3–5-l-Eimer im Beet, täglich gespült [Q FAO 4.3.4]; Netzfilter-Tank mit Obstnetz, UVI 2 × 185 gal (0,70 m³) je Klärer in Reihe, 1–2× pro Woche gespült [Q SRAC 454]; Trommelfilter 60 µm, 15–25 m³/h je Gerät [Q Herstellerlisten, Suchzusammenfassung, Maße nicht gelesen]; Fleece/Vlies: **keine Quelle gelesen**. Eine Trommel für 6,6 m³/h wäre das kleinste Handelsgerät; Maße unbelegt.
- **Hauptstrom oder Teilstrom?** Davidson: den gesamten Umlauf über ein Mikrosieb führen (Vollstrom). FAO/UVI: Vollstrom durch Klärer und Netzfilter. Für NFT genügt ein Sieb am NFT-Zweig (38 l/min je Linie, bei 8 m/h 0,29 m², E), das ist Kandidat B.

### Frage 3 – Biofilter: Mindestfläche, Beete, Szenarien
- **Mindestfläche** (TAN 130 g/Tag; E = TAN ÷ Rate):

| Rate (g TAN/m²/Tag) | Quelle | Fläche | K1-Volumen bei 500 m²/m³ | Heute (471 m²) |
|---|---|---|---|---|
| 0,57 | FAO 589 App. 4 „conservative“ (Q, Volltext) | 228 m² | 0,46 m³ | **2,07-fach** |
| 0,27 | Suhr & Pedersen 2010, Schwebebett Forellen-RAS, 850 m²/m³ (Q Abstract, Temperatur unbekannt) | 481 m² | 0,96 m³ | 0,98-fach |
| 0,25 bei 30 °C → 0,215 bei 28 °C | Kinyage & Pedersen 2016, θ = 1,079 (Q Abstract, Kurzzeitwert) | 605 m² | 1,21 m³ | **0,78-fach** |
| 1,06 | Simulator-Annahme (A) | 123 m² | 0,25 m³ | 3,8-fach |

  Als Gegenprobe über das Volumen: Losordo/DeLong „350 g TAN/m³/Tag, konservativ“ (Q, gelesen) → 130 g ÷ 350 = 0,37 m³; 0,94 m³ tragen 329 g = 2,5-fach.
  SRAC 454 warnt, die „standard equations“ gälten für Aquaponik nicht unbedingt (Pflanzenwurzeln, Aufnahme), empfiehlt aber, die Biofilter „fairly close to the recommendations for recirculating systems“ zu bemessen [Q SRAC 454] – das spricht für die untere Raten-Hälfte (0,2–0,6).
- **Beete als Biofilter:** FAO-Tabelle (SSA 200–400, 3,0–6 g Futter/l/Tag, auf 0,57 gerechnet) → 8,2 m³ für 24,6–31 kg Futter/Tag; „the grow beds themselves are perfect biofilters“ [Q FAO]. Gemessen (nur Abstract): Perlit-Biofilter in Aquaponik 19 / 31 / 80 g TAN/m³/Tag bei pH 6 / 7 / 8 [Q Tyson u. a. 2008]; Kies-Biofilter für Aquakultur 14–110, Mittel 41 g TAN/m³/Tag [Q Bachelorarbeit UPLB, Suchzusammenfassung, niedrig]. Daraus: 8,2 m³ tragen 156–656 g bei voller Wirksamkeit (1,2–5-fach), aber nur 39–64 g (0,3–0,5-fach) mit dem Simulator-Ansatz von 25 % wirksamem Volumen [E, A]. Goddek Kap. 7: Beete können in kleinen und Hobby-Anlagen Biofilter sein, verstopfen aber leicht und sind für größere kommerzielle Systeme „nicht geeignet“; ein einfacher Biofilter im Nebenstrom erhöhte die mögliche Futtermenge um etwa 25 % [Q Goddek u. a. 2019, Kap. 7.4, Knaus & Palm 2017 dort zitiert].
- **Szenarien** (Kapazität gegen TAN 130 g/Tag; E; P = pessimistisch: K1 0,215, Beete 19 g/m³/Tag × 25 %; M = mittel: K1 0,27, Beete 31 × 25 %; O = optimistisch: K1 0,57, Beete 41 × 100 %):

| Biofilter | K1-Fläche | P | M | O | bei 20 °C (alle × 0,54) P / M / O |
|---|---|---|---|---|---|
| **100 %** (heute, 2 Tanks) | 471 m² | **1,08** | 1,47 | 4,65 | 0,58 / 0,79 / 2,5 |
| **50 %** (ein Tank oder je halb gefüllt) | 235 m² | 0,69 | **0,98** | 3,6 | 0,37 / 0,53 / 1,95 |
| **0 %** (nur Beete) | 0 | 0,30 | 0,49 | 2,6 | 0,16 / 0,26 / 1,4 |

  Zahlen sind Deckungsfaktoren (Kapazität ÷ 130 g). Unter 1 heißt: reicht nicht. Bei 5 % TAN (173 g) sinken alle Werte um 25 %.
  - **100 %** reicht in allen drei Fällen bei 28 °C, knapp im pessimistischen.
  - **50 %** reicht nur, wenn die Beete mehr als das Simulator-Viertel tun (M gerade, P nicht).
  - **0 %** reicht nur, wenn die Beete praktisch voll wirken (O); die Quellen belegen das nicht (E: bei 109 l/min Beetstrom und 1,5 mg/l TAN im Pool müssten die Beete je Durchlauf mindestens 55 % des TAN entfernen).
- **Winter und Anlauf:** Die Kuppel wird geheizt (`system-specs.json`, Heizlast); der Faktor 0,54 bei 20 °C gilt nur bei Heizungsausfall (E aus θ = 1,079; FAO: unter 17 °C sinkt die Bakterienleistung, unter 10 °C um 50 % und mehr [Q FAO 2.3.3]). Tilapia fressen unter 17 °C nicht mehr [Q FAO]; die Last sinkt dann mit. Anlauf: Cycling dauert 3–6 Wochen [Q FAO 8.2.2]; die Kinyage-Dauerversuche zeigten niedrigere Raten als die Kurzzeitversuche. Das schrittweise Besetzen (D61) ist die tragende Maßnahme, kein Biofilter-Volumen.

### Frage 4 – Gesamtsystem: übertrieben oder passend?
- **FAO Tab. 8.1:** Absetzer plus Biofilter zusammen 10–30 % des Fischtankvolumens (Q); wir haben 1,94 m³ = 6,8 %, mit den Sieben (2 × 0,163 m³) 2,27 m³ = 8,0 % (E). Das liegt unter der FAO-Spanne, die aber bis 3 m³ Fischtank gilt.
- **UVI (SRAC 454):** vier Fischtanks 31,2 m³, zwei Klärer 7,6 m³ + vier Netzfilter-Tanks 2,8 m³ + Entgasung 0,7 m³, kein Biofilter, 379 l/min im Vollstrom. Die Mechanik ist damit 33 % des Fischvolumens oder, bei 13–21 kg Futter/Tag (E: 214 m² Raft × 60–100 g), 0,5–0,8 m³ je kg Tagesfutter; wir haben 0,86 m³ Mechanik (Absetzer + Siebe) für 3,46 kg = 0,25 m³/kg. **Unser Mechanikteil ist je kg Futter kleiner als UVI, dafür läuft er im Teilstrom**; er ist also nicht überdimensioniert.
- **Kein belegtes Auslegungsverfahren für die Kombination Absetzer + Sieb + Biofilter + Beete.** Die Quellen behandeln jede Stufe einzeln (FAO, Losordo/DeLong) oder große RAS (Davidson). Eine zweite unabhängige Gesamtquelle (Timmons & Ebeling, Wilson Lennard) war nicht abrufbar.

### Frage 5 – Platzersparnis
Grundfläche als Hüllquadrat des größten Maßes; Höhe aus den Bauteildaten (E). Ø673 bzw. Ø930 liegen über der Plattform (619² bzw. 821²).

| Bauteil | Maß je Stück | Grundfläche je Stück | Höhe | Bauraum je Stück | beide Linien |
|---|---|---|---|---|---|
| Absetzer | Ø673, Plattform 619² | 0,45 m² | 1,25 m | 0,57 m³ | **0,91 m², 1,13 m³** |
| Biofilter | Ø930, Plattform 821² | 0,87 m² | 1,67 m | 1,45 m³ | **1,73 m², 2,89 m³** |
| Feinfilter T55 Rev B | 620 × 430 (Behälter), Standhöhe 0,86 m | 0,27 m² | 0,86 m | 0,23 m³ | **0,53 m², 0,46 m³** |
| **Summe heute** | | | | | **3,17 m²** |

| Variante | Grundfläche gespart | Bauraum gespart | Quellenlage |
|---|---|---|---|
| Biofilter 50 % (ein Tank statt zwei) | 0,87 m² | 1,45 m³ | Kandidat (M-Fall gerade ausreichend) |
| Biofilter 0 % | 1,73 m² | 2,89 m³ | nicht gestützt |
| Absetzer entfällt | 0,91 m² | 1,13 m³ | Kandidat |
| Sieb entfällt (nur Absetzer) | 0,53 m² | 0,46 m³ | nicht gestützt, NFT braucht Stufe |
| **Kandidat A** = Absetzer weg + ein Biofilter | **1,77 m²** | 2,58 m³ | Kandidat |
| **Kandidat B** = Sieb nur am NFT-Zweig (Beutel/Eimer-Größe, A) + ein Biofilter, Absetzer bleibt | **1,40 m²** | 1,91 m³ (Sieb ersetzt, 0,53 m² entfallen) | Kandidat |

Pumpentafeln, Beine und Laufwege sind nicht eingerechnet. Ein einziger Biofilter für beide Linien braucht eine Hydraulikprüfung (Verweilzeit sinkt von 6,4 auf 3,2 min bei 220 l/min; `tank_gross` hat 702 l).

## Widerspruchstabelle
| Aussage A | Aussage B | mögliche Ursache | gewählte Seite |
|---|---|---|---|
| R28/R30: FAO-Auslöser erreicht (17 kg/m³, 62 g/m²) | neue Last: 12,1 kg/m³, 45 g/m² | D61 senkt 475 → 346 kg | neue Last |
| FAO: Klärer fassen „bis 60 %“, SRAC: 50 % | Davidson: Swirl 23 % der Masse (37 % TSS) | Radial-/Zylinderklärer gegen Swirl, Messbasis | Davidson (konservativ, Swirl) |
| FAO Klärer 1/6 bis 10–30 % des Fischtanks (Vollstrom) | Modell 1,9 % im Teilstrom | Dual-Drain nicht von FAO behandelt, FAO ≤ 3 m³ | offen, nicht als Fehler gewertet |
| FAO Biofilter-Rate 0,57 (NH₃-Masse) | Kinyage 0,215, Suhr 0,27 (Messung, N-Masse, Kurzzeit/Forelle) | Basis NH₃ gegen N, Temperatur, Medium | bis zur Klärung beide ausweisen |
| FAO: Beete sind „perfekte Biofilter“, 8,2 m³ tragen 25–31 kg Futter | Goddek: Beete verstopfen, nicht für größere Systeme; Messwerte tragen nur 3–24 kg | Auslegungsrate gegen Messung, Maßstab | Messung, Beete nur als Reserve |
| SRAC 454: Biofilter nahe RAS-Regeln | FAO: Beete ersetzen den Biofilter | verschiedene Systeme (Raft/Kleinanlage) | beide als Spanne, kein Biofilter 0 % |
| Auftrag: Feinfilter 400 × 300 × 500, 1,6 m/h | Bauteil T55: 620 × 430 × 610, 8 m/h [A] (Hauptstrom) | W31 → W32/D55 | T55 (aktuell) |
| Mortensen 100 µm = 21 % | Davidson Mikrosieb 40–45 % der Tagesmasse | Maschenweite, Anlage, Messgröße | beide, Maschenweite entscheidet |
| TAN 3,75 % (NH₃-Masse bei FAO) | N-Masse 3,1 % | Faktor 1,2 NH₃/N | 130 g beibehalten (konservativ), Basis markiert |

## Quellen (gelesen, nicht nur Suchtreffer)
| # | Titel / URL | Art | Abruf | Qualität | Unabhängig von |
|---|---|---|---|---|---|
| 1 | Somerville u. a. (2014), FAO Technical Paper 589 – [fao.org PDF](https://www.fao.org/3/i4021e/i4021e.pdf) | FAO, **Volltext** (288 S., Kap. 2.3.3, 4.3.4, 4.4.2, 8.1.3, 8.2.2, Tab. 8.1, App. 4) | 01.11.2026 | hoch | 2 teilweise (FAO nutzt UVI) |
| 2 | Rakocy, Masser, Losordo (2006), SRAC 454 – [pods.okstate.edu](https://pods.okstate.edu/fact-sheets/SRAC-454pod.pdf) | Extension, **Volltext** | 01.11.2026 | hoch | 1 teilweise |
| 3 | Davidson & Summerfelt (2005) über [Global Seafood Advocate](https://www.globalseafood.org/advocate/settler-evaluation-radial-flow-vs-tangential-flow/) | Fachartikel-**Zusammenfassung**, Original ungelesen | 01.11.2026 | mittel | 1, 2 |
| 4 | Losordo & DeLong (2015) [Estimating biofilter size for RAS](https://www.globalseafood.org/advocate/estimating-biofilter-size-for-ras-systems/) | Fachartikel, gelesen | 01.11.2026 | mittel-hoch | 2 (gleiche Autoren wie SRAC) |
| 5 | Goddek u. a. (2019), *Aquaponics Food Production Systems*, Kap. 7.4 über [FarmHub](https://learn.farmhub.ag/resources/aquaponics-food-production-systems/7-coupled-aquaponics-systems/7-4-aquaculture-unit/) und Kap. 3 [Springer PDF](https://link.springer.com/content/pdf/10.1007/978-3-030-15943-6_3.pdf) | Buchkapitel (Kap. 3 Volltext, Kap. 7.4 Webseite) | 01.11.2026 | mittel-hoch | 1–4 |
| 6 | Kinyage & Pedersen (2016), Aquacultural Eng. 75 – [DTU Orbit](https://orbit.dtu.dk/en/publications/impact-of-temperature-on-ammonium-and-nitrite-removal-rates-in-ra/) | Peer-Review, **nur Abstract** | 01.11.2026 | mittel | alle |
| 7 | Suhr & Pedersen (2010), Aquacultural Eng. 42 – [Eintrag](https://dissem.in/p/34351719/nitrification-in-moving-bed-and-fixed-bed-biofilters-treating-effluent-water-from-a-large-commercial-outdoor-rainbow-trout-ras) | Peer-Review, **nur Abstract** (Suchzusammenfassung: 231 g N/m³/Tag, 0,27 g/m²/Tag) | 01.11.2026 | mittel-niedrig | alle |
| 8 | Tyson u. a. (2008), Perlit-Biofilter – [AGRIS](https://agris.fao.org/search/en/records/65dfb69e63b8185d9cae3f3a) | Peer-Review, **nur Abstract** | 01.11.2026 | mittel-niedrig | alle |
| 9 | Mortensen (2000), Drum filter efficiency – [Global Seafood Advocate](https://www.globalseafood.org/advocate/drum-filter-efficiency-as-particle-separator-in-a-recirculated-system/) | Fachartikel (R30 gelesen), 60 µm = 48 % über Suche bestätigt | 01.11.2026 | mittel | alle |
| 10 | Review „Filters and media used in aquaponic system filtration“ (2024) – [SciELO](https://new.scielo.br/j/bip/a/9RKDyMDSNXWN9GRQnSjv3mr/?lang=en) | Review, Webseite gelesen; nennt keine Raten und keine Auslegungsgrößen | 01.11.2026 | mittel | alle |
| 11 | Bachelorarbeit UPLB, Kies-/Holzkohle-Biofilter – [Eintrag](https://www.ukdr.uplb.edu.ph/etd-undergrad/167) | **Suchzusammenfassung**, 14–110 g TAN/m³/Tag | 01.11.2026 | niedrig | alle |
| 12 | Lennard & Leonard (2006), Aquaculture Int. 14 – [Springer](https://link.springer.com/doi/10.1007/s10499-006-9053-2) | Abstract (Kies- gegen Raft gegen NFT: NFT ca. 20 % schlechtere Nitratentnahme), kein Filterwert | 01.11.2026 | mittel | alle |

Nicht abrufbar oder nicht gefunden: Timmons & Ebeling (Buch), Wilson Lennard „Solids filtration“ (aquaponic.com.au lieferte HTML statt PDF), Rusten u. a. (2006), Herstellerdatenblätter zu Trommel-, Fleece- und Beutelfiltern, Sieb-Belastungswerte je m².

## Konfidenz und Lücken
- **Hoch:** Lastbasis neu (Rechnung), FAO-Schwellen und -Tabelle (Volltext), UVI-Aufbau und Aufteilung 50/50 (Volltext), FAO-Bedarf einer Stufe für NFT.
- **Mittel:** Swirl-Wirkung (eine Anlage, 150 m³), Biofilter-Rate (zwei Messungen unter FAO, beide Abstract), Platzzahlen (Bauteildaten aus `data/components`, ohne Pumpentafeln).
- **Niedrig / unbelegt:** Substratbeete als Biofilter (nur Abstracts und eine Bachelorarbeit), Siebbelastung je m², Platzbedarf von Trommel/Fleece, Wirksamkeit unseres Absetzers im Teilstrom, Einfluss von Pflanzenaufnahme auf TAN (SRAC: nicht untersucht).
- **Nicht beantwortet:** Wie viel Prozent des Beetvolumens wirklich nitrifizieren (`f_beete_eff`), ob ein Tank für zwei Linien hydraulisch geht.
- **Keine Ertrags-, Kosten- oder Standortrechnung** (D69).

## Folge (Vorschläge, nichts geändert)
1. **Entscheidung Ben (Orchestrator vorbereiten):** Kandidat A, B oder Status quo. A spart 1,77 m², B 1,40 m²; beide setzen einen Biofilter-Tank voraus. Biofilter 0 % entfällt.
2. `docs/filter-konzept.md` Art 2: Begründung „17 kg/m³ und 62 g/m²“ auf 12,1 kg/m³ und 45 g/m² aktualisieren; die Ampel „Feinfilter fehlt“ neu bewerten.
3. Vor jedem Umbau messen, nicht rechnen: Nitrifikationsleistung der Beete (TAN-Differenz Beetzu- und -ablauf im Betrieb), Schlammmasse aus Absetzer und Sieb nach einer Woche, Maschenweite 60 gegen 100 µm im Probebetrieb.
4. Offen für Hydraulik: ein Biofilter für zwei Linien; Siebbelastung 8 m/h belegen oder ändern.

## Recherche-Kritiker
01.11.2026: (1) Davidson/Summerfelt, Kinyage, Suhr, Tyson nur als Zusammenfassung oder Abstract; (2) Timmons/Ebeling und Lennard-Volltexte nicht erreicht; (3) keine Messung zu Beeten im Süßwasser-Aquaponikbetrieb mit Kies/Blähton; (4) Trommelfilter-Maße nicht gelesen; (5) FAO- und SRAC-Aussagen sind nicht voneinander unabhängig (FAO stützt sich auf UVI). Behebung: Folgesitzung mit Buchzugang oder Herstellerangeboten.

Geprüft gegen: FAO 589 (Volltext), SRAC 454 (Volltext), Goddek-Kap. 3, `docs/filter-konzept.md`, `data/system-specs.json`, R19, R21, R27, `docs/parts/feinfilter.md`, `data/components/tank.json`, D38, D55, D61 · Offen: Entscheidung Ben (Kandidat A/B), Siebbelastung, Beete-Nitrifikation messen (Besitzer DEINE ENTSCHEIDUNG und ICH in einer Folgesitzung), Hydraulik bei einem Biofilter (ICH)
