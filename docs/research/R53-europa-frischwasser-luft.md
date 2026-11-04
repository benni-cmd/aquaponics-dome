# R53: Europa-Bezug Frischwasser und Luft (D76, Teile aus W37-2 und W37-3)

**Auftrag:** Fachrecherche R53 (Sitzungsauftrag 04.11.2026) · **Bearbeitet:** 04.11.2026 · **Rolle:** Fachrecherche, nur lesen, im Netz suchen, rechnen, schreiben; Blätter, Modell, `data/`, `viewer/` unverändert.
**Problem:** Der Planer W37 fand für Frischwasser und Luft fast keine Kaufteile mit zwei europäischen Quellen (D76); ohne katalytische Kohle in Europa trägt der Chloramin-Fall nicht. **Intent:** W37-2 und W37-3 sollen mit belegten oder ehrlich als "nicht beschaffbar" markierten Teilen bauen. **Goal:** je Teil zwei unabhängige europäische Händler oder Hersteller mit Artikel und geöffneter Seite, oder ein begründetes "nicht beschaffbar" mit Ersatz.
**Herkunft:** [Q] Seite oder Datenblatt selbst geöffnet und gelesen · [Q-Treffer] nur Suchergebnis oder Zusammenfassung, nicht selbst gelesen · [E] eigene Rechnung · [A] Annahme. **Status:** *beschaffbar* = zwei unabhängige europäische Quellen mit [Q]; *eine Quelle* = eine; *nur UK* = nur Vereinigtes Königreich; *nicht belegt* = nichts Europäisches gefunden. Europa schließt UK ein wie in R52; ob UK reicht, ist Bens Entscheidung (R52 Abschnitt 4, weiter offen). Preise nur wo auf der Seite.
**Grenze der Methode:** WebFetch liefert PDFs nur als Binärdatei. Datenblätter habe ich lokal mit `pdftotext` gelesen; Kennlinien-Grafiken und Tabellen als Bild sind so nicht lesbar. Eine Kennlinie bei 26 kPa konnte ich deshalb für keine Pumpe belegen.

## 0. Antwort (sechs Punkte)

1. **Katalytische Kohle: nur UK, plus Herstellervertrieb auf Anfrage. Im EU-Festland kein Händler belegt.** Centaur 12x40 (Calgon Carbon, Steinkohle, nicht Kokos) ist bei Ecosoft (Belgien als Hauptsitz, UK-Shop in GBP) als CENT1240, 15 kg, geführt, derzeit nicht lieferbar [Q]. Haycarb RWAC (Kokos, Chloramin-Kapazität 150 mg/g) wird in Europa über Eurocarb (Bristol, UK) vertrieben; Händlerseite mit Artikel fand ich nicht [Q Broschüre]. Der Chloramin-Fall trägt damit nur, wenn Ben UK akzeptiert oder eine Anfrage bei Eurocarb oder Ecosoft Festland-Lieferung bestätigt.
2. **Durchflussbegrenzer 4 l/min: ein Fabrikat belegt, keine zweite Quelle.** Kobold KM-020A (G 3/4 außen, DN 20, Messing, 4 l/min als Festwert wählbar) [Q Datenblatt]. Das ist besser als "nicht beschaffbar" in W37-2: das Teil existiert; die Zuordnung zum Hersteller Kobold stammt aus Dateiname und Suche, nicht aus dem Datenblatt selbst.
3. **Probehahn: beschaffbar, aber mit G 1/4 statt d12.** Kemper 1870000600 und SYR 6705.10.050, beide DE, beide Datenblatt gelesen [Q]. Rotguss, nicht PVC.
4. **Pumpe 200 l/min bei 26 kPa: für keine Pumpe belegt.** Hiblow HP-200: 200 l/min nur bei 20 kPa, Arbeitsbereich bis 35,3 kPa, Kennlinie nur als Grafik [Q]. Secoh JDK-S-200: 200 l/min bei 20 kPa; Tabelle endet dort [Q]. Extrapolation auf 26 kPa grob 176 l/min [E, Vorbehalt]. Der Planwert 130 l/min bleibt tragbar, die Spitze 205 l/min mit einer Pumpe nicht.
5. **Luftleitung über Wasserspiegel plus Rückschlagventil: zweite Quelle nur teilweise.** Eine Anleitung (Pumpe unter Wasserspiegel braucht Rückschlagventil, Tropfschleife) habe ich gelesen [Q], Hersteller und Land nicht erkennbar; die Regel "über dem höchsten Wasserspiegel" bleibt [A].
6. **Standzeit der Kohle: Rechnung statt Quelle.** Aus der Kapazität 150 mg/g (Haycarb) folgt für den vorderen Behälter rechnerisch etwa 3,4 Jahre bei 2 mg/l Chloramin [E]. Das ist eine obere Grenze aus Labor-Kapazität; ein Praxis-Intervall belegt das nicht. Prüfintervall 6 bis 12 Monate nach Messung bleibt.

## 1. Katalytische Aktivkohle gegen Chloramin (R45 Abschnitt 5, Zeile 286)

| Teil | Quelle 1 | Quelle 2 | Maß / Kennwert | Status |
|---|---|---|---|---|
| Katalytische Kohle 12x40, Schüttgut | **Ecosoft, Centaur 12x40, Art. CENT1240**, 15 kg, 384,45 £ netto, derzeit nicht lieferbar ("Request availability") [Q, `ecosoft.com/uk/product/centaurr-12x40-granular-activated-carbon`]. Länderwähler: DE, BE, NL, FR, ES, PL, IT, IE, UK; Hauptsitz laut Seite Belgien. Seite nennt Chloramin **nicht**, nur Schwefelwasserstoff; EN 12915, KIWA ATA, UK DWI | **Haycarb RWAC über Eurocarb (UK, Bristol)**: Broschüre gelesen [Q]; Kontakt `info@eurocarb.com`, +44 1179 820333; Gebinde 25 kg Sack, 12,5 kg Ventilsack, 500 kg Bigbag; Händler-Artikel und Preis nicht gefunden | Centaur: Iod 825 mg/g min, Asche 7 % max, Körnung 1 mm [Q Ecosoft]; Herstellerseite nennt Chloramin-Anwendung [Q, `calgoncarbon.com/products/centaur`]. Haycarb: Chloramin-Kapazität **150 mg/g** (Kokos Standard), 200 (Boosted), 450 (Holz); Katalytische Aktivität 20, 30, 35; Körnung 8x30, 12x40, 20x50 [Q Broschüre, Prüfmethode HC/STP/58] | **nur UK** (Ecosoft in GBP, Eurocarb Bristol); EU-Festland-Händler **nicht belegt** |
| Gegenprobe Kokos-Katalysator | Jacobi AquaSorb CX-MCA: Suche ergab nur US-Händler [Q-Treffer] | Lenntech (NL): Seite "Lenn Filtration" nennt Centaur als Kartuschen-Füllung, aber ohne Chloramin [Q-Treffer] | – | **nicht beschaffbar belegt** |
| Kartusche 10x35 mit katalytischer Kohle | GAPS Water Treatment (UK): Centaur 12x40 15 kg [Q-Treffer, Seite 429] | – | – | **nicht belegt** |

**Befund:** In Europa existiert die Kohle, aber ich fand keinen Festland-Händler mit Preis und Artikel. Ecosoft ist die belastbarste Spur, weil Hauptsitz Belgien und Länderwähler DE/NL/FR/PL; der Shop rechnet jedoch in GBP und nennt kein EU-Lager. Centaur ist **Steinkohle**, nicht Kokos; R45 und W37-2 planen "Kokosschale 12x40". Das Maß (12x40) bleibt gleich, die Kennwerte im Blatt müssen auf Centaur oder Haycarb zeigen, nicht auf ein Kokos-Fabrikat.
**Kontaktzeit (R45):** bleibt 10,5 min bei 2 x 21 l und 4 l/min [E, `python -X utf8 -I -c "print(42/4)"`]. Centaur-Datenblatt "typisch unter 7 min Kontaktzeit" stammt aus einer Suchzusammenfassung [Q-Treffer].
**Ersatz, wenn keine europäische Lieferung bestätigt wird:** (a) bei Chlor statt Chloramin genügt Standardkohle (Jacobi AquaSorb CS 12x40 oder Ecosoft; R45 und W37-2); (b) Chloramin-Fall nur mit UK-Bezug oder Eurocarb-Anfrage; (c) Zisterne bleibt "nicht bauen" (D69). Chemische Entchlorung statt Kohle ist hier **nicht** recherchiert.

## 2. Durchflussbegrenzer 4 l/min (R45 Zeile 305)

| Teil | Quelle 1 | Quelle 2 | Maß / Kennwert | Status |
|---|---|---|---|---|
| Festwert-Begrenzer 4 l/min | **Kobold KM-020A**, Datenblatt "Flow limiter KM-...A" gelesen [Q, `cdn.shopify.com/.../kma_TDS.pdf`]: G 3/4 außen, DN 20, Messing CW614N vernickelt oder Edelstahl, Festwerte 1 bis 30 l/min, **4 l/min ist gelistet**; Toleranz ±15 % bis 2 l/min, ±10 % ab 3 l/min; Druck 2 bis 10 bar (Tabellenlayout verschoben, Zuordnung nicht sicher) | keine zweite unabhängige Quelle. Autoflow A127 3/4" (Thersane, FR): Titel nennt 0,085 [m3/h?], also rund 1,4 l/min, **nicht 4 l/min** [Q-Treffer] | Hersteller steht nicht auf dem Datenblatt (Dateiname `pi-ho_fbl-km_a_e`; Kobold per Suche zugeordnet [Q-Treffer]); Händler und Artikelnummer 4 l/min nicht gefunden | **eine Quelle** (Hersteller-Datenblatt) |

**Befund:** "Nicht beschaffbar" aus W37-2 ist zu streng: ein Festwert 4 l/min in G 3/4 existiert. Anschlussart ist Außengewinde G 3/4; die Station ist d25 PVC-Leitung, es braucht Gewinde-Übergänge (Katalogteile, [A]). Mindestdruck: Ohne ausreichend Differenzdruck regelt der Begrenzer nicht; bei Netzdruck erfüllt, mit Schwimmerventil und Behälter-Druckverlust vor dem Bau prüfen (R45 offener Punkt 4).

## 3. Probehahn "d12" (R45 Zeile 305)

| Teil | Quelle 1 | Quelle 2 | Maß / Kennwert | Status |
|---|---|---|---|---|
| Probenahmeventil | **Kemper (DE), Figur 187 00, Bestellnr. 1870000600** (G 1/4, DN 8) [Q Datenblatt gelesen] | **SYR (DE), 6705, Werks-Nr. 6705.10.050**, Anschluss ¼" mit Adapter auf ⅜", DN 10 [Q Katalogblatt gelesen] | Kemper: Rotguss entzinkungsfrei, PN 16, 90 °C, DVGW/KTW, Edelstahl-Auslaufbogen, H 125 mm, D 48 mm, 0,23 kg. SYR: Rotguss, 16 bar, 90 °C, Höhe 144 mm, Länge 86 mm | **beschaffbar** (zwei Hersteller, Händler nicht geprüft) |

**Befund:** Der Hahn hat Gewinde G 1/4 (Außen), **keinen** Rohr-Ø 12. "d12" im Blatt als Maß des Anschlusses lesen. Einbau über einen Abzweig mit G 1/4 Innengewinde; ein PVC-Klebe-Abzweig mit Innengewinde G 1/4 habe ich nicht belegt [A]. Der Hahn ist für Probenahme gebaut, nicht als Zapfstelle (Hersteller-Hinweis in Suchergebnis [Q-Treffer]); das passt zum wöchentlichen DPD-Test (R45 Betrieb).

## 4. Linear-Membranpumpe 200 l/min bei 26 kPa (R45 Zeile 250 bis 253)

| Teil | Quelle 1 | Quelle 2 | Maß / Kennwert | Status |
|---|---|---|---|---|
| Hiblow HP-200 | **Hiblow FRANCE S.A.S. und SPAIN S.L.**, Katalog 2015 "HP-100/120/150/200" gelesen [Q, `siurbliai.lt` PDF, Tel. FR +33-1-61-37-09-15, ES +34-91-669-3953]: Spannung AC 100/120/230 V, 200 l/min bei **20,0 kPa Nennpunkt**, 210 W (50 Hz) und 250 W (60 Hz), 46 und 48 dBA, **Druckbereich 5,0 bis 35,3 kPa**; Kennlinie nur als Grafik | Händler: Koi-Spezialist eBay.de 539 € [Q-Treffer]; Sibo/Fluidra Benelux (NL) führt "original Hiblow", Art. SC424 Membransatz (Pumpe nicht gezeigt) [Q] | **Wert bei 26 kPa nicht lesbar** (Kennlinie liegt als Vektorgrafik; Tabelle fehlt). Gewicht im Katalog nicht eindeutig (8,5 und 9 kg) | Hersteller-Niederlassungen FR/ES belegt; Händler-Artikel **eine Quelle** (nicht geöffnet); Kennlinie **offen** |
| Secoh JDK-S-200 | **BIBUS** (Ukraine-Seite) [Q]: 290/270/245/220/200 l/min bei 0/50/100/150/200 mbar, 180 W bei 200 mbar, 230 V, 46 dB(A), 10,0 kg, 240 x 180 x 230,5 mm | **tanks.ie (IE, Kingspan Parts, SKU 0022090)** [Q]: 372,70 € netto, 115 W, 44 dB(A), EU-Stecker, Lieferzeit 3 bis 5 Tage. **BIBUS NL** [Q]: 200 l/min, 170 W, 48 dB, 20 kPa | Werte widersprechen sich (180/170/115 W; 46/48/44 dB): Messbedingung nicht genannt. Tabelle **endet bei 200 mbar** | **beschaffbar** als Gerät (BIBUS, tanks.ie), Kennlinie bei 26 kPa **nicht belegt** |
| Medo/Nitto, Thomas, Oase, Heissner | Suche ohne Treffer für ein 200-l/min-Linearmodell [Q-Treffer: Nitto-Kohki-Katalog listet Vakuumpumpen, kein LA-200] | – | – | **nicht belegt** (Thomas/Oase/Heissner nicht einzeln geprüft) |

**Rechnung:** Aus der Secoh-Tabelle folgt je 50 mbar rund minus 20 bis 25 l/min im Bereich 150 bis 200 mbar. Linear auf 260 mbar fortgeschrieben: 200 minus 20 x (260 minus 200) / 50 = 176 l/min [E, `python -X utf8 -I -c "print(200-20*(260-200)/50)"`]. **Vorbehalt:** reine Fortschreibung; die wirkliche Kennlinie kann steiler fallen. Für die HP-200 gibt es keine Tabelle, nur die Obergrenze 35,3 kPa; ein ähnliches Verhalten ist [A].
**Folge für R45 Empfehlung 3 und 4:** 130 l/min (Planwert) liegen unter 176, eine Pumpe trägt den Planwert. Die Spitze 205 l/min trägt eine Pumpe **nicht**. Wenn beide Pumpen parallel laufen (Spitze), fällt N+1 weg. Das ist eine Auslegungsfrage für Ben und die Planung, keine Beschaffungsfrage.

## 5. Zweite Quelle: Luftleitung über Wasserspiegel plus Rückschlagventil (R45 Zeile 256)

| Teil | Quelle 1 | Quelle 2 | Maß / Kennwert | Status |
|---|---|---|---|---|
| Regel Schleife und Rückschlagventil | Anleitung "Setting up an Air Pump with a Check Valve" gelesen [Q, `cdn.shopify.com/.../Check_Valve_Installation.pdf`, Stand 10.11.2021, Hersteller und Land nicht genannt]: Pumpe über dem Wasserspiegel nach Möglichkeit; **liegt die Pumpe unter dem Wasserspiegel, ist ein Rückschlagventil nötig**; Zeichnung zeigt Rückschlagventil und **Tropfschleife** | EP 0919524 A1 "Sicherheitsventil für Belüfter": Rückschlagventil in der Luftleitung zwischen Membranbelüfter und Druckluftquelle schließt bei Ausfall [Q-Treffer, Seite 404]; aquifarm.com (Ventil über dem höchstmöglichen Wasserspiegel) [Q-Treffer, Seite 403] | Quelle 1 deckt Rückschlagventil und Schleife für **Aquarium-Pumpen**; die Höhenregel "Z > 515 plus Reserve" ist so nicht belegt | **Regel bleibt [A]**; zweite Quelle teilweise, europäische Herkunft unbelegt |
| Rückschlagventil für Luft, Öffnungsdruck | Bänninger Art. 75328/75326/75325 (schwarte-shop, aus W37-3 übernommen, nicht neu geöffnet): Seite nennt Wasser, nicht Luft | – | Öffnungsdruck für Luft bei 130 l/min fehlt | **offen**; Ersatz: Luftschlauch-Rückschlagventile (Tetra CV4 u. a.) für kleine Leitung, für d40 keine belegt |

**Befund:** Eine praktische Regel gibt es (Schleife plus Ventil bei Pumpe unter Wasser). Für die Auslegung der Station gilt: Sicherheit durch **Schleife über dem Spiegel** als Hauptschutz, Ventil als zweite Sperre, nicht umgekehrt [A]. Der Ventil-Durchlass bei 130 l/min (Druckverlust, Öffnungsdruck) ist unbelegt und verändert den Gegendruck (R45: 24 bis 26 kPa).

## 6. Standzeit der katalytischen Kohle (R45 Zeile 312)

**Gefunden:** Haycarb nennt **Chloramin-Kapazität in mg/g** (150, 200, 450; Prüfmethode HC/STP/58) mit dem Hinweis "höhere Kapazität, längere Filterlebensdauer" [Q Broschüre]. Eine Standzeit in Monaten steht nicht darin.
**Rechnung** (`python -X utf8 -I -c`, Eingaben: 27,5 lb/ft³ gleich 0,441 kg/l aus der Handelsangabe Centaur 12x40 [Q-Treffer]; Bett 21 l gleich 9,3 kg Kohle je Behälter; Last 0,552 m³/Tag nach D77; Formel: Masse x Kapazität / (0,552 m³/Tag x Konzentration)):

| Chloramin im Zulauf | Last | Kapazität 150 mg/g | Kapazität 200 mg/g |
|---|---|---|---|
| 1 mg/l | 0,55 g/Tag | 2514 Tage, 6,9 Jahre | 3352 Tage, 9,2 Jahre |
| 2 mg/l | 1,10 g/Tag | 1257 Tage, 3,4 Jahre | 1676 Tage, 4,6 Jahre |
| 4 mg/l | 2,21 g/Tag | 628 Tage, 1,7 Jahre | 838 Tage, 2,3 Jahre |

**Aussage:** Obergrenze rein nach Kapazität, nur vorderer Behälter, ohne Sicherheitsfaktor. Vorsicht: (1) Testbedingungen von HC/STP/58 unbekannt (Konzentration, Kontaktzeit); (2) bei katalytischer Kohle begrenzt oft die abnehmende **katalytische Aktivität** die Standzeit, nicht die Masse; (3) eine Händlerangabe nennt "6 bis 12 Monate" für einen Kohleblock ohne Wasserchemie, ein Reef-Blog behauptet Ausfall bei weniger als 1 % der Nennlebensdauer ohne Methode [Q-Treffer, beides nur Hinweise]. **Folge:** R45-Betrieb bleibt: DPD-Test wöchentlich hinter Behälter 1, Prüfintervall 6 bis 12 Monate [A]; die Rechnung dient nur als Plausibilität ("Jahre, nicht Wochen"), nicht als Wechselplan. Verbindliche Kapazität beim Lieferanten (Eurocarb oder Ecosoft) erfragen.

## 7. Folgen für W37-2 und W37-3 (nur Liste; Blätter nicht geändert)

**W37-2 `docs/jobs/W37-2-aktivkohle-stutzen.md`, Abschnitt "Europa-Teileliste" (Zeilen 21 bis 33):**
1. Zeile "Katalytische Kokoskohle 12x40" (Zeile 29): Status "nicht beschaffbar belegt" ersetzen durch "nur UK (Ecosoft CENT1240, Eurocarb/Haycarb RWAC); EU-Festland offen"; "Kokos" streichen, Centaur ist Steinkohle.
2. Zeile "Durchflussbegrenzer 4 l/min" (Zeile 27): "nicht beschaffbar" ersetzen durch "eine Quelle (Kobold KM-020A, G 3/4 außen, 4 l/min)"; Pruefpunkt 6 (Soll >= 2 mal "nicht beschaffbar" in `docs/parts/aktivkohle_station.md`) neu zählen: statt 2 bleibt höchstens die Kohle, falls Festland-Lieferung nicht bestätigt wird.
3. Zeile "Probehahn d12" (Zeile 31): "offen" ersetzen durch "beschaffbar: Kemper 1870000600 und SYR 6705.10.050, G 1/4 statt d12, Rotguss"; Port-Beschriftung `Probehahn d12` prüfen.
4. Offener Punkt "Standzeit" (Zeile 18, 90): Rechnung aus Abschnitt 6 als [E] einführen, Prüfintervall bleibt [A].
5. Bauentscheidung (Zeile 33) bleibt: Maße Platzhalter [A]; Ben-Aufgabe E15 (Chlor oder Chloramin) bleibt.

**W37-3 `docs/jobs/W37-3-luft-schaltschrank.md`, Abschnitt "Europa-Teileliste" (Zeilen 23 bis 36):**
1. Zeile "Luftpumpe 200 l/min" (Zeile 26): "nur UK" ersetzen durch HP-200 mit Hersteller-Niederlassungen FR/ES [Q] und Händler-Artikel auf Anfrage; Secoh JDK-S-200 über BIBUS und tanks.ie (IE, 372,70 € netto, SKU 0022090) als **beschaffbar** führen.
2. "Kennlinie bei 26 kPa" bleibt **offen**; stattdessen im Blatt die Rechnung 176 l/min bei 26 kPa als [E] mit Vorbehalt ergänzen; Aussage "Planwert 130 l/min trägt, Spitze 205 l/min nur mit zwei Pumpen".
3. Zeile "Rückschlagventil" (Zeile 30) und Regel R45 Zeile 256: zweite Quelle Abschnitt 5 eintragen; "Luft nicht freigegeben" bleibt, Tropfschleife und Ventil als Doppelschutz.
4. Pruefpunkt 5 (Zeile 83): "Kennlinie bei 26 kPa als OFFEN" bleibt gültig.
5. D76-Status der Pumpenklasse: weder UK noch EU-Händler trägt "beschaffbar" mit Kennlinie; gültig ist "beschaffbar als Gerät, Kennlinie offen".

## 8. Offen (Besitzer)

1. **DEINE ENTSCHEIDUNG (Ben):** gilt das Vereinigte Königreich als "Europa" für Kohle (Ecosoft GBP, Eurocarb)? Ohne Ja bleibt der Chloramin-Fall ohne belegten Bezug (R52 Abschnitt 4, gleiche Frage).
2. **DEINE HANDLUNG (Ben):** E15 (Chlor oder Chloramin) beim Versorger klären; bei Chlor entfällt das Kohle-Problem.
3. **DEINE HANDLUNG (Ben oder N-BESCHAFFUNG):** Anfrage an Eurocarb (`info@eurocarb.com`) und Ecosoft (Länderseite DE/BE): Lieferung EU-Festland, Preis, Chloramin-Kapazität, Standzeit; Anfrage an BIBUS (Secoh) und Hiblow France (+33-1-61-37-09-15) nach Förderleistung bei 26 kPa (Kennlinie als Zahlentabelle).
4. **ICH, nicht erledigt:** zweite europäische Quelle für Kobold KM-020A (Händler-Artikel 4 l/min); Thomas, Oase, Heissner einzeln prüfen; Katalog-Tabellen und Kennlinien in Bild-PDFs lesen (braucht Bildansicht der PDF-Seite, die mir hier fehlte).
5. **ICH, entschieden und ausgeführt:** Blätter W37-2/W37-3 **nicht** geändert (Auftrag); die Planer-Sitzung übernimmt Abschnitt 7.

**Geprüft gegen:** Ecosoft Seite CENT1240 (geöffnet), Calgon-Carbon-Seite Centaur (geöffnet), Haycarb-Broschüre (`pdftotext`), Hiblow-Katalog FR/ES (`pdftotext`), BIBUS-Ukraine- und BIBUS-NL-Seite (geöffnet), tanks.ie (geöffnet), Kemper-Datenblatt und SYR-Katalogblatt (`pdftotext`), Kobold-Datenblatt (`pdftotext`), Anleitung Rückschlagventil (`pdftotext`), Sibo-Seite (geöffnet) · Rechnungen: `python -X utf8 -I` (Bett, Standzeit, Extrapolation) · `docs/jobs/W37-2-aktivkohle-stutzen.md`, `docs/jobs/W37-3-luft-schaltschrank.md`, `docs/research/R45-hydraulik-auslegung.md` Abschnitte 4 und 5, `docs/research/R52-europa-bezug.md`.
