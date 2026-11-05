# N-PREIS-PRUEF 1A Stahl: Notiz (05.11.2026)

**Problem:** Angebote in `data/beschaffung/stahl.json` waren tot, falsches Mass oder falscher Artikel (Beleg: NFT-Rinne mit Kabelkanal belegt).
**Intent:** Jede Zeile soll ein real bestellbares, passendes Teil tragen (D76 Europa, zwei Quellen).
**Goal:** Jede Stahl-Zeile der Stueckliste ist ersetzt, bestaetigt oder OFFEN mit Grund. Stand: 49 Eintraege bearbeitet (46 Stueckliste-Zeilen plus 3 Alt-Eintraege ausserhalb der Stueckliste): 12 bestaetigt, 18 ersetzt, 19 OFFEN. 9 Schraubensaetze (SRB-satz-*) neu angelegt.

Methode: Drei parallele Recherche-Agenten (Profile, Bleche/Winkel, Edelstahl/Alu/PP/Schrauben), Seiten per WebFetch geoeffnet, Konfiguratoren nur gelesen, nichts abgeschickt, nichts gekauft. Belegfall NFT-Rinne von mir selbst. Ergebnisse zusammengefuehrt, Kontrolle: jede Zeile hat Angebot oder 'OFFEN'-Grund; kein Kabelkanal in der NFT-Zeile.

## Ersetzt (18)

- `PRF-st-rr40x40x2.5`: Altes Angebot verwies auf die 40x40x3-Seite mit interpoliertem Preis = falsch. Beide Haendler geoeffnet; 2,5 mm existiert bei keinem. Ersatz-Angebote 40x40x3 mit zwei Quellen eingetragen; Mass-Entscheidung bei Ben.
- `PRF-st-rr40x60x3`: Altes stahlshop.de-Angebot zeigte auf die 40x40x3-Seite (falsches Mass) und wurde entfernt. Shop24 60x40x3 geoeffnet und bestaetigt; zweite Quelle Metallparadies-Konfigurator 60x40x3: 161,08/6 = 26,85 EUR/m verzinkt.
- `PRF-st-strebe30x30`: Altes stahlshop.de-Angebot zeigte auf die 40x40x3-Seite und wurde entfernt. 30x30x3 bei Shop24 geoeffnet (9,12 EUR) und bei Metallparadies per Konfigurator (92,23/6 = 15,37 EUR/m verzinkt); zwei Quellen.
- `WNK-wandlasche-30x30x3`: Kemper-Seite und Metallparadies-Konfigurator geoeffnet; zwei unabhaengige DE-Quellen fuer Ersatzmass, Modell nicht geaendert.
- `BLE-v2a-3mm-korbflansch`: Metallshopper-Snippetangebot (E, Konfigurator dynamisch) ersetzt durch drei geoeffnete Seiten: stahl-shop24 (Tafel, Q), Feld Maschinenbau und Edelstahl-Saegezentrum (Zuschnitt je m2 gerechnet, E). Alle DE; Feld liefert nur DE (DE ist EU, Regel D76 erfuellt).
- `PRF-alu-haut-profil`: OBI-Link 404 (entfernt). Hornbach und alu-verkauf.de geoeffnet; zwei unabhaengige DE-Quellen fuer U 20x20x1,5. Kappenprofil selbst nicht gesucht (Zeile ohne Mass).
- `PRF-alu-keilschiene`: OBI/Norhage/Wegner geprueft: Wegner Preis Q aber Masse unbelegt, Norhage Preis nur "ab 140 EUR" ohne Laengen/Preis je m lesbar (verworfen). U-Profil 25x25x2 mit zwei unabhaengigen DE-Haendlern als Naeherung; Zeile bleibt eine Mass-Entscheidung fuer Ben.
- `BLE-pp-blende-290x260`: S-Polytec-Preise 05.11. nicht lesbar (0,00 EUR) und deshalb ersetzt durch Technoplast + plastx24 (beide Preistabellen gelesen). Konfidenz E, da Zuschnitt-Aufpreis fehlt.
- `BLE-pp-tafel-693x463x7`: Zwei Preistabellen gelesen (Technoplast netto, plastx24 netto), auf brutto gerechnet. S-Polytec-Interpolation (6/8 mm Mittel) verworfen.
- `BLE-pp-tafel-502x345x5`: S-Polytec-Preise nicht lesbar; Technoplast + plastx24 gelesen. 5 mm ist marktueblich. Konfidenz E wegen fehlendem Zuschnitt-Aufschlag.
- `SRB-satz-m5x12`: NEUER Eintrag (nicht in stahl.json). Hornbach und Schraubenking, jeweils Schraube, Mutter und Scheibe einzeln geoeffnet; beide liefern nach DE. Hornbach 100er-Packungen brutto, Schraubenking Mengenstaffel bei 100 St.
- `SRB-satz-m6x16`: NEUER Eintrag (nicht in stahl.json). Hornbach und Schraubenking, jeweils Schraube, Mutter und Scheibe einzeln geoeffnet; beide liefern nach DE. Hornbach 100er-Packungen brutto, Schraubenking Mengenstaffel bei 100 St.
- `SRB-satz-m6x40`: NEUER Eintrag (nicht in stahl.json). Hornbach und Schraubenking, jeweils Schraube, Mutter und Scheibe einzeln geoeffnet; beide liefern nach DE. Hornbach 100er-Packungen brutto, Schraubenking Mengenstaffel bei 100 St.
- `SRB-satz-m8x30`: NEUER Eintrag (nicht in stahl.json). Hornbach und Schraubenking, jeweils Schraube, Mutter und Scheibe einzeln geoeffnet; beide liefern nach DE. Hornbach 100er-Packungen brutto, Schraubenking Mengenstaffel bei 100 St.
- `SRB-satz-m6x55`: NEUER Eintrag. Zwei Haendler, Preise fuer M6x60 als naechstgroessere Laenge; Modell nicht geaendert.
- `SRB-satz-m10x60`: NEUER Eintrag. Hornbach fuehrt M10x60 DIN 933 nur in Edelstahl A2 (25 St, 23,75 EUR), nicht verzinkt -> verworfen. Schraubenking Q (100er-Preis), Mister Agri E (Einzelstueck, Scheibe fremd).
- `SRB-m8x35`: Mister Agri (Scheibenpreis ANGENOMMEN) ersetzt durch Schraubenking (alle drei Teile gelesen, Q). Hornbach nur interpoliert (E).
- `PRF-pvcu-rinne-130x100`: Kabelkanaele (Hornbach 110x60, OBI 100x60) entfernt. Ersatz: echter NFT-Kanal Urban Hydro 100x50 mm, 290 cm, innen weiss, UPVC, bei GrowKing24 (8,41 EUR/m, 24,40 EUR inkl. MwSt je 290 cm) und Golden Green Club (7,16 EUR/m, 20,77 EUR je 290 cm), beide Seiten geoeffnet, Versand aus EU. Groesse 130x100 existiert nicht; naechster Kanal 100x80 (41,10 EUR/250 cm). Lebensmitteleignung nur als Herstellerwort.

## Bestaetigt (12)

- `PRF-st-rr40x40x3`: Alle drei URLs geoeffnet; Mass 40x40x3 passt. Altes metallparadies-Angebot (78,90 EUR/Stange, Spanne unklar) durch Konfigurator-Wert ersetzt: 121,41 EUR/6 m = 20,23 EUR/m verzinkt. Preis stahlshop.de bleibt E (Gewicht/m nicht eindeutig).
- `PRF-st-rr40x40x2`: Shop24-Seite geoeffnet, Preis 9,04 EUR bestaetigt; metallparadies-Konfigurator reproduziert 92,37 EUR/6 m = 15,40 EUR/m verzinkt. Zeile nicht platziert (Bedarf 0).
- `PRF-st-rr30x30x2`: Beide Quellen geoeffnet, Preise reproduziert. Modell-Lagerlaenge 6500 mm, marktueblich 6000 mm (Ben-Hinweis, kein Eingriff).
- `PRF-st-rr60x60x3`: Beide Quellen geoeffnet, Preise reproduziert. Zeile nicht platziert (Bedarf 0).
- `PRF-st-rr25x25x2`: Beide Quellen geoeffnet, Preise reproduziert. Zeile nicht platziert (Bedarf 0).
- `PRF-st-rund20`: Beide Seiten geoeffnet; 20 mm passt. Metallparadies-Meterpreis 14,70 gilt nur fuer Abholung 6 m, Versandlaenge max 3 m (15,42 EUR/m). Roh-Angebot 8,18 passt nicht zu 'verzinkt' und wurde entfernt. Zeile nicht platziert.
- `PRF-v2a-voll8x8`: stahl-shop24 und Metallshopper geoeffnet; Artikel passt (8x8 Vollmaterial 1.4301/304, Preis je m). Zwei unabhaengige Haendler, stahl-shop24 DE-Sitz, Preis Q. Voss (Login-Preis) nicht erneut geprueft.
- `PRF-alu-klemmleiste`: OBI-Link 404 (entfernt). Hornbach und alu-verkauf.de geoeffnet, zwei unabhaengige DE-Quellen, Mass 30x2 Flachstange Alu passt zur Zeile (Zarge/Klemmleiste Flachprofil).
- `SRB-knoten-klein`: Hornbach bestaetigt (Preis M6x20 6,50/100 05.11.), zweite Quelle Schraubenking ergaenzt (Q). Zeile ohne Mass: M6x20 bleibt Annahme [A].
- `SRB-halter-klein-12x10x20`: Wie SRB-knoten-klein: Hornbach bestaetigt, Schraubenking als zweite Quelle. Bedarf 456 St: bei Schraubenking Mengenstaffel guenstiger, hier 100er-Preis angesetzt.
- `SRB-pumpe-klein`: Hornbach bestaetigt (M8x20 9,25/100). Mister Agri-Angebot (Scheibe ANGENOMMEN, E) ersetzt durch Schraubenking (Q). Zeile ohne Mass: M8x20 bleibt Annahme [A].
- `SRB-satz-m6x20`: Zeile bisher ohne Angebot in stahl.json: Hornbach und Schraubenking, je Schraube/Mutter/Scheibe einzeln geoeffnet; beide liefern nach DE.

## OFFEN mit Grund (19)

- `WNK-flach-14x3`: Shop24 und Metallparadies geoeffnet; 14x3 gibt es bei beiden nicht. 15x3 nur eine Quelle (Metallparadies), WebSearch nach weiterem Shop ohne verwertbaren Treffer, daher OFFEN. Das alte Shop24-Angebot rechnete proportional und war kein Kaufartikel.
- `WNK-flach-3mm-diagonale`: Beide Seiten geoeffnet und Preise fuer 30x3 bestaetigt, aber die Zeile hat keine Breite und keine Stueck-Laenge; ohne diese Masse ist kein Stueckpreis seriös herleitbar. Zwei Quellen existieren fuer den Platzhalter 30x3 verzinkt.
- `BLE-blech-st-3`: Metallparadies-Konfigurator und stahl-shop24-Seite geoeffnet; zwei unabhaengige DE-Haendler bestaetigen roh S235JR 3 mm, Preis passt (35,96 EUR). Werkstoff verzinkt nicht kaufbar, daher Ben-Entscheidung.
- `BLE-blech-st-5`: Metallparadies-Konfigurator (5 mm) und stahl-shop24 geoeffnet, beide roh, Preise bestaetigt.
- `BLE-blech-st-6`: Metallparadies-Konfigurator (6 mm) und stahl-shop24 geoeffnet; beide roh, Preis bestaetigt. Metallparadies deutlich guenstiger als Raster-Hochrechnung.
- `BLE-fussplatte-70x70x5`: Metallparadies-Konfigurator, stahlshop.de und Kemper-Seite geoeffnet; Mass kaufbar, Werkstoff roh, Preise bestaetigt (3,54-3,96 EUR). Metallshopper (NL) nicht neu gerechnet, Bearbeitungsgebuehr 9,79 ohne Label (je Bestellung oder je Stk unklar).
- `BLE-fussplatte-80x80x6`: Metallparadies-Konfigurator und stahlshop.de geoeffnet; zwei unabhaengige DE-Haendler fuer exakt 80x80x6 roh, Preise 3,84/4,96 EUR.
- `BLE-fussplatte-80x80x8`: Drei DE-Haendler geoeffnet, Mass kaufbar roh, Spanne 1,36-6,18 EUR.
- `BLE-fussplatte-100x100x6`: Metallparadies-Konfigurator und stahlshop.de geoeffnet; zwei unabhaengige DE-Quellen fuer exakt 100x100x6 roh.
- `BLE-fussplatte-150x150x8`: Drei DE-Haendler, Mass kaufbar roh; Spanne 4,79-11,23 EUR.
- `BLE-fussplatte-200x200x8`: Drei DE-Haendler, Mass kaufbar roh; Spanne 8,52-16,73 EUR.
- `BLE-platte-250x250x15`: Drei DE-Haendler geoeffnet, Mass kaufbar; grosse Preisspanne 32-71 EUR (Metallparadies teuer). Zeile verlangt nicht ausdruecklich verzinkt.
- `WNK-winkel-36x60x60`: Metallparadies, Metallshopper, Hornbach geoeffnet. 36 mm Schenkelhoehe nicht kaufbar; Ersatzmasse zeigen Preisbereich 0,80-7,37 EUR.
- `WNK-rinnenhalter-25`: Metallparadies-Konfigurator geoeffnet; zweite Quelle nur fuer Nachbarprofil, daher keine ersetzt-Zusage. Bei 304 Stk lohnt Sammelanfrage beim Haendler.
- `WNK-pumpenkonsole`: Metallparadies-Konfigurator geoeffnet; Konsolenmass unbekannt, daher nur Richtpreise.
- `BLE-v2a-lochblech-medienschutz`: Geoeffnet: Amazon (503), Eisen-Pfeiffer (403), ehorst (kein Preis), Feld (Preis gelesen), bestell-dein-lochblech (ausverkauft), online-bleche, zuschnittprofi. Zweite unabhaengige Preisquelle fehlt, daher OFFEN; Feld-Angebot als E belassen.
- `BLE-pp-siebboden-beet`: Technoplast, plastx24, S-Polytec geoeffnet; PP-Suche nach gelochten Platten fand nur RS PRO 2-mm-Siebplatten (3 mm Loch). Plattenmaterial zweifach belegt, Siebboden selbst OFFEN.
- `SRB-satz-m12x55`: Geoeffnet: Hornbach (Suche, Seiten 1-2), Schraubenking, Mister Agri, Fabory (404). Keine zweite Quelle mit Preis fuer die Schraube; zur Not M12x60 (Schraubenking) pruefen.
- `SRB-satz-m16x300`: Geoeffnet: Hornbach, Schraubenking, Mister Agri; Websuche fand nur ehorst (Login), SFS (CH), Fabory (404). Modell nicht geaendert.

## OFFEN (Ben)
(Auszug aus den `luecke`-Feldern; Modell unveraendert)

- `PRF-st-rr40x40x2.5`: OFFEN (Ben): Mass Wand 2,5 mm bei 40x40 nicht marktueblich (Shop24 und Metallparadies fuehren 2,0/3,0); 3,0 mm als kaufbarer Ersatz, Modell nicht geaendert. Lagerlaenge im Modell 6500 mm, marktueblich 6000 mm.
- `PRF-st-strebe30x30`: OFFEN (Ben): Mass Wand/Profil der Kuppelstrebe laut Zeile offen (N-STATIK V1/V2c); 30x30x3 als Annahme. Modell-Lagerlaenge 7000 mm, marktueblich max 6000 mm.
- `WNK-flach-14x3`: OFFEN (Ben): Mass 14x3 nicht marktueblich; 15x3 verzinkt nur bei Metallparadies gefunden (zweite Quelle fehlt, Suche ohne Treffer), 30x3 bei beiden Haendlern kaufbar. Modell nicht geaendert.
- `WNK-flach-3mm-diagonale`: OFFEN (Ben): Mass Breite und Zuschnittlaenge der 3-mm-Diagonale nicht aus Modell ableitbar; Zeile in Stk, Angebote je m (30x3 nur Platzhalter).
- `BLE-blech-st-3`: OFFEN (Ben): roh statt verzinkt - Zeile verlangt verzinkt, Marktstandard fuer Zuschnitt 3 mm ist roh S235JR; verzinkte Zuschnitte nur bis 4 mm (Metallparadies). Verzinken-Mehrpreis nur grob belegt (hausjournal.net: Feuerverzinken ab ca. 0,50-0,70 EUR/kg, Schleuderverzinken Kleinteile/Privat ab 1,50 EUR/kg; 700x700x3 = 11,5 kg => ca. 6-8 EUR zzgl. Grundpreis, konfidenz A, nur eine Quelle).
- `BLE-blech-st-5`: OFFEN (Ben): roh statt verzinkt - verzinkt als Zuschnitt nur bis 4 mm lieferbar, 5 mm nur roh S235JR. Mehrpreis Verzinken siehe BLE-blech-st-3 (ca. 0,5-0,7 EUR/kg, 13,2 kg Blech => ca. 7-9 EUR, nur eine Quelle). Bedarf 0.
- `BLE-blech-st-6`: OFFEN (Ben): roh statt verzinkt - 6 mm nur roh. Mehrpreis Verzinken ca. 0,5-0,7 EUR/kg (37 kg => ca. 19-26 EUR, nur eine Quelle hausjournal.net). Bedarf 0.
- `BLE-fussplatte-70x70x5`: OFFEN (Ben): roh statt verzinkt - alle drei Haendler liefern Zuschnitt nur roh; verzinkte Platten 5 mm als Zuschnitt nicht gefunden (Metallparadies verzinkt nur bis 4 mm). Mehrpreis Verzinken: 0,192 kg x 0,5-1,5 EUR/kg = ca. 0,10-0,29 EUR/Stk plus Grundpreis der Verzinkerei (hausjournal.net, nur eine Quelle, 'Privat: ab 1,50 EUR/kg Schleuderverzinken'); Wirtschaftlichkeit eher als Sammelauftrag 76 Stk.
- `BLE-fussplatte-80x80x6`: OFFEN (Ben): roh statt verzinkt - Marktstandard roh; Kemper fuehrt 6 mm nicht (Dicken 5/8), daher 6 mm nur bei Metallparadies/Stahlshop. Mehrpreis Verzinken siehe Fussplatte 70x70x5 (nur grob belegt).
- `BLE-fussplatte-80x80x8`: OFFEN (Ben): roh statt verzinkt. Bedarf 0.
- `BLE-fussplatte-100x100x6`: OFFEN (Ben): roh statt verzinkt. Kemper fuehrt 6 mm nicht (nur 5/8 mm).
- `BLE-fussplatte-150x150x8`: OFFEN (Ben): roh statt verzinkt. Bedarf 0.
- `BLE-fussplatte-200x200x8`: OFFEN (Ben): roh statt verzinkt. Bedarf 0.
- `BLE-platte-250x250x15`: OFFEN (Ben): Ankerplatte roh - Zeile nennt Werkstoff 'Stahl Anker' ohne Verzinkung; roh S235JR 250x250x15 ist marktueblich, Verzinken optional.
- `WNK-winkel-36x60x60`: OFFEN (Ben): Mass 36x60x60 nicht marktueblich (kein Normwinkel); naechstes Standardprofil 60x60x6 (Zuschnitt min 40/50 mm, roh). Verzinkt nur als duenner Verbinder (Hornbach 2,5 mm). Funktion (Rinnenhalter, Belastung) klaeren.
- `WNK-wandlasche-30x30x3`: OFFEN (Ben): Mass 30x30x3 nicht kaufbar (Mindestmass Kemper 40x40, Metallparadies 50x50, Stahlshop min. 5 mm Dicke); Ersatz roh 40x40x3 oder 50x50x3. Bedarf 0.
- `WNK-rinnenhalter-25`: OFFEN (Ben): Mass/Form 'Rinnenhalter 25' undefiniert (Winkel 25x25x3 oder flache Lasche 25x25?); Zuschnitt mind. 50 mm (Metallparadies) bzw. 40 mm; verzinkt nicht erhaeltlich. Zweites Angebot ist anderes Profil (30x30x3).
- `WNK-pumpenkonsole`: OFFEN (Ben): Mass der Pumpenkonsole/Standwinkel nicht definiert (Zeile ohne Masse); Preisnaeherung ueber 60x60x6-Winkel, roh.
- `PRF-v2a-voll8x8`: OFFEN (Ben): Mass Lagerlaenge 7000 mm im Modell; Handel liefert Stuecke 0,5-3 m (stahl-shop24 bis 2 m, Metallshopper bis 3 m). Preis je m unveraendert, Verschnitt/Saegeschnitt/Stangenzahl neu rechnen.
- `PRF-alu-haut-profil`: OFFEN (Ben): Zeile heisst "Kappenprofil der Haut" (Mass leer, nicht platziert, Bedarf 0); belegt ist nur ein U-Profil 20x20x1,5 mm als Platzhalter.
- `PRF-alu-keilschiene`: OFFEN (Ben): Mass Kanal 25x15 nicht marktueblich/nicht gefunden (U-Profile 25x25x2, 20x20, 15x22 u. a.); Zeile "Keilschiene" (Kanal fuer Keil/Klemmung) hat kein Handels-Standardprofil. Modell nicht geaendert.
- `BLE-pp-blende-290x260`: OFFEN (Ben): Farbe schwarz nicht gefunden (grau/hellgrau belegt); schwarzes PP 3 mm nur als eBay-Treffer ohne Beleg.
- `BLE-pp-tafel-693x463x7`: OFFEN (Ben): Mass Dicke 7 mm nicht marktueblich (6 oder 8 mm); Preise fuer 8 mm. Modell nicht geaendert.
- `SRB-satz-m6x55`: OFFEN (Ben): Mass M6x55 nicht im Handel gefunden (nur M6x50 und M6x60; ISO 4017 kennt 55, Hornbach 9,45 EUR/100 fuer M6x50); Preise gelten fuer M6x60.
- `SRB-satz-m16x300`: OFFEN (Ben): Mass M16x300 als DIN 933 (Vollgewinde) nicht marktueblich (Handel fuehrt M16 DIN 933 nur bis ca. 120-260 mm, SFS M16x260); lange Schrauben dieser Art sind ueblicherweise DIN 931 (Teilgewinde). OFFEN (Quelle): kein M16x300-Preis gelesen; Hornbach fuehrt nur DIN 931 M10/M12 bis 140, Schraubenking/Mister Agri keine M16x300-Seite. Nuss M16: Hornbach 32,25 EUR/100, Schraubenking 11,16 EUR/100; Scheibe 17 mm Hornbach 11,90 EUR/100, Schraubenking 5,64 EUR/100.

## OFFEN (Quelle)

- `BLE-v2a-lochblech-medienschutz`: OFFEN (Quelle): nur EINE gelesene Quelle mit Preis (Feld Maschinenbau). Amazon-Link 404/503 (nicht erreichbar), Eisen-Pfeiffer 403 (nicht oeffnbar), ehorst Preis nur nach Login, bestell-dein-lochblech.de (Rv5-8 1,5 mm, kostenloser Zuschnitt) ausverkauft und Preis nicht auf 110x320 zuordenbar (12,14 EUR bei 485,60 EUR/m2, Groesse unklar), online-bleche.de Preis/m2 unplausibel (3.800 EUR/m2), zuschnittprofi Staerke nicht ausgewiesen. Zusatz: Randloch-Hinweis pruefen (Rollenform/Abwicklung).
- `BLE-pp-siebboden-beet`: OFFEN (Quelle): gelochte PP-Platte 8 mm (Siebboden) nicht gefunden; Lochung/Zuschnitt je Beet nicht bepreisbar, Stk-Preis braucht Zuschnittmass (Katalog masse leer). Preise oben nur Plattenmaterial je m2. Fischwasser-Eignung: Herstellerbeleg zur Lebensmitteleignung offen.
- `SRB-satz-m12x55`: OFFEN (Quelle): M12x55 DIN 933 verzinkt: kein EU-Preis gelesen. Hornbach fuehrt DIN 933 nur bis M12x30 verzinkt (sonst DIN 931 M12x80+), Schraubenking nur M12x60 (P001142), Fabory-Seite 404, SFS (CH, nicht EU) nennt CHF 34/100 nur im Suchsnippet, Mister Agri keine M12x55-Seite. Nuss/Scheibe M12 belegt: Hornbach Mutter 13,35 und Scheibe 13 mm 8,30 EUR je 100, Schraubenking Mutter 5,88 und Scheibe 3,84 EUR je 100.
- `SRB-satz-m16x300`: OFFEN (Ben): Mass M16x300 als DIN 933 (Vollgewinde) nicht marktueblich (Handel fuehrt M16 DIN 933 nur bis ca. 120-260 mm, SFS M16x260); lange Schrauben dieser Art sind ueblicherweise DIN 931 (Teilgewinde). OFFEN (Quelle): kein M16x300-Preis gelesen; Hornbach fuehrt nur DIN 931 M10/M12 bis 140, Schraubenking/Mister Agri keine M16x300-Seite. Nuss M16: Hornbach 32,25 EUR/100, Schraubenking 11,16 EUR/100; Scheibe 17 mm Hornbach 11,90 EUR/100, Schraubenking 5,64 EUR/100.

## Hinweise
- Nicht in der aktuellen Stueckliste, in `stahl.json` unveraendert gelassen: `BLE-platte-30x30x3`, `SRB-knoten-klein`, `SRB-m8x35`, `SRB-pumpe-klein`.
- Von Hand gelesen 05.11.2026: PRF-st-rr40x40x3, 40x40x2, 30x30x2, 60x60x3, 25x25x2, rund20 (Block 1), je mit Seitenbeleg in der `bemerkung`.
- Lebensmitteleignung: Beleg nur als Haendler-/Herstellerwort (NFT-Kanal, PP-Platten); kein Normbeleg gefunden. Gilt laut vorlaeufiger Entscheidung als 'OFFEN (Quelle): Eignung nicht angegeben'.
- Das Modell wurde nicht geaendert. Massvorschlaege (NFT 100x50, Rohr 40x40x3 statt 2,5, Winkel 60x60x6) stehen oben als OFFEN (Ben).

## Auflagen aus dem Pruefer-Befund (101277e), Stand 05.11.2026

1. **Auflage 2 (NFT-Zeile):** Im Angebot ergaenzt: Lieferlaenge 2,9 m, 154 m Bedarf = 54 Stueck a 2,9 m. OFFEN (Ben): Bezeichnung 'PVC-U 130x100' und Kauf 22 Stangen a 7 m in der Stueckliste passen nicht zum Angebot; Anpassung in `bom.py`/Katalog (Werkstatt) erst nach der Massentscheidung.
2. **Auflage 4 (Schraubensaetze):** Alle Satz-Angebote gegen die Einzelpreise der Seiten (je 100 St) nachgerechnet. Die Preise waren auf 2 Stellen gerundet (Abweichung bis 8 %, zum Beispiel M5x12 Hornbach 0,12 statt 0,1165). Jetzt steht der Satzpreis mit 4 Stellen aus der Rechnung in der `bemerkung`. Preisbasis: Hornbach brutto DE; Schraubenking inkl. 20 % AT-USt (DE-Brutto etwa plus/minus 1 %, nicht umgerechnet); Mister Agri inkl. NL-USt. Es gibt in der Stahl-Datei keine Bevo-Angebote.
3. **Auflage 5 (Lebensmittel-Hinweis):** Stahlprofile, Bleche, Schrauben (verzinkter Stahl, Edelstahl 1.4301, Alu) tragen in dieser Datei keinen Eignungsbeleg. Nach der vorlaeufigen Entscheidung (a) genuegt fuer Teile ausserhalb des Fischwassers die Werkstoffangabe. OFFEN (Quelle): Eignung nicht angegeben fuer die Teile mit Wasserkontakt: NFT-Kanal (UPVC, nur Haendlerwort 'ungiftig'), PP-Platten und PP-Siebboden (nur Haendleraussage S-Polytec), Edelstahl-Lochblech Medienschutz. Entscheidung OFFEN (Ben) 1 steht weiter.
4. **Auflage 7, Spannverschluss:** `SON-spannverschluss-edelstahl` liegt in `huelle_pflanze.json`, nicht in `stahl.json`; Gruppe 1E, nicht angefasst.
