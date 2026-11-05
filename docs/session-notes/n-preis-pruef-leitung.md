# N-PREIS-PRUEF Gruppe 1B Leitung (`data/beschaffung/leitung.json`), Stand 05.11.2026

Problem: Bevo-Alternativen verlinkten die Familien-Standardseite (zum Beispiel T-Stueck 75 mm) statt der Variante mit dem benoetigten Durchmesser. Ziel: jede Zeile ersetzt, bestaetigt oder OFFEN mit Grund.

## Ersetzt (Bevo-Variantenseite mit passendem Durchmesser, Preis nachgemessen)
Bevo bietet je Familie eine Variantentabelle; der Titel der Familienseite zeigt nur die Standardgroesse. Je Zeile gelesen: Variantenseite, Netto-Preis (je Stueck bzw. je 5-m-Stange), Lager "European central warehouse". Der alte Preis stimmte bei allen Zeilen ausser Bulkhead d63 und Pool mit der richtigen Variante ueberein; nur der Link war falsch.
1. T-Stueck d20, d25, d32, d40, d50, d63, d75, d110 (16 bar KIWA): Varianten 7002487, 7002488, 7002489, 7002491, 7002493, 7002495, 7002497, 7002499.
2. Bogen 90 d25, d32, d40, d50: 7002570 bis 7002573. Bogen 45 d40, d50, d63, d75: 0110227 bis 0110230.
3. Kappe d20, d25, d32, d50: 7002812, 7002813, 7002814, 7002816.
4. Reduzierung d40_d32, d50_d32, d50_d40, d63_d50, d75_d50, d75_d63: 0160740, 0160743, 0160744, 0160748, 0160751, 0160752.
5. Kugelhahn d20, d40, d50, d63, d110 (Typ DIL): 0100843, 0100846, 0100847, 0100848, 7003055.
6. Druckrohr d20, d32, d40, d50, d63, d75 (PN16): 0329121, 0329133, 0329141, 0309229, 0309159, 7018027.
7. Bulkhead d40: 40/50 mm (0100543). **Bulkhead d63 und Pool: Preis korrigiert** von 40,45 auf 49,02 EUR brutto (Variante 63/75 mm, 7026182, 41,19 EUR netto, 3 Stk Lager); vorher war die Variante 40/50 bzw. ein falscher Preis hinterlegt.

## Bestaetigt (von Hand gelesen 05.11.: passt, weil ...)
1. `SCH-rohrschelle-d50`: Spannbereich 48-54 mm passt zu Rohr-AD 50 mm. `SCH-rohrschelle-d110`: 108-116 mm passt zu AD 110 mm.
2. `ROH-leerrohr-dn100`: Hornbach KG-Rohr DN110 (AD 110) als Kabelschutz-Naeherung, weiter NAEHERUNG.
3. Bereits OK gemessene Schwarte-Zeilen (57) unveraendert; Seitentitel nennt das Mass.
4. `FIT-kappe-d16`: zweites Angebot Bevo 16 mm (7002811) ergaenzt, aber nur 250er-Packung 282,50 EUR netto: Preisvergleich, nicht einzeln kaufbar.

## OFFEN mit Grund (Eintrag in `luecke`)
1. `ARM-rsv-d20/d25/d40` (nicht platziert): Schwarte-Links fuehren auf leere Kategorie, Angebote entfernt. Bevo fuehrt Rueckschlagventile (0111211/0111212/0111214: 135,79 / 158,47 / 258,27 EUR netto je Stk), nur eine Quelle und auffaellig teuer.
2. Alle `ROH-pvcu-*`: zweite Quelle fehlt. Schwarte hat keine Meterware; Pimtas-1-m-Rohr bei santechnikos-centras.lt liegt hinter einer Cloudflare-Bot-Pruefung (nicht umgangen); Bosta ist Bevo-Schwester, nicht unabhaengig.
3. Zeilen mit nur einem Angebot (zum Beispiel Bogen 90 d63/d75, Kupplung d40/d50, Stutzen d16/d40/d63, Schlauchtuelle d25): Hauptangebot geprueft, zweite Quelle nicht gefunden.
4. Zeilen ohne Angebot (zum Beispiel `ROH-pvcu-d16`, `FIT-reduktion-d16/d32/d50`, `SCH-rohrschelle-d63`, `FIT-verteiler-d25-nft`, `SCH-schlauch-rinne-id16`): nicht in dieser Sitzung gefunden. Bevo-Suche ist JavaScript-gesteuert, Websuche lieferte keine zwei lesbaren Quellen.
5. `FIT-rinne-kappe-zulauf/ablauf`: haengen an der NFT-Rinne 130x100 (Gruppe Stahl).
6. `SCH-schlauchschelle-id16`: Schelle 12-20 mm, Schlauch-AD bei ID16 vermutlich groesser.
7. Nicht platzierte Zeilen ohne Link (Leerrohr-Fittinge, Verteiler, Schlauchbogen, Anbohrschelle u. a.): nicht bearbeitet (Grenze Kontext/Reihenfolge).
8. Lebensmitteleignung: bei den Zeilen im Fischwasser (Rohre, Fittings) nicht per Hersteller belegt (nur KIWA-Hinweis im Titel der Bevo-T-Stuecke): OFFEN (Quelle): Eignung nicht angegeben. Nichts deshalb ersetzt (Blatt OFFEN (Ben) 1).

## OFFEN (Ben)
Keine neue Massabweichung in Gruppe 1B gefunden.

## Auflagen aus der Pruefung (101277e), Nachtrag 05.11.2026
1. **Auflage 3, T-Stuecke:** Von Hand gelesen 05.11.: Schwarte-T-Stuecke sind laut Seitentext "T-Stueck 90 Grad reduziert" (Baenninger). Gemessen ueber alle acht Zeilen (`FIT-t-d20` bis `d110`), nicht nur d50/d63. Bevo-Varianten (gleich grosses T, KIWA, 16 bar) sind jetzt Hauptangebot, Schwarte bleibt als Preisvergleich mit Warnhinweis. Zweite gleichwertige Quelle: OFFEN (Quelle).
2. **Auflage 4, Preisbasis:** Jedes Bevo-Angebot (48) traegt jetzt "preis_eur = brutto = netto x 1,19"; Bevo-Seiten zeigen netto und brutto (Beispiel T d50: 3,43 netto, 4,15 brutto laut Seite). Die Schraubensaetze gehoeren zur Gruppe Stahl.
3. **Auflage 5, Lebensmitteleignung:** OFFEN (Quelle): Eignung nicht angegeben fuer alle Teile im Fischwasser dieser Gruppe: Rohre (ROH), Fittings (FIT), Armaturen (ARM: Kugelhaehne, Bulkheads, Rueckschlagventile). Hinweis: Bevo-T-Stuecke tragen KIWA im Titel (Trinkwasser-Pruefzeichen); das ist kein Beleg fuer die Armaturen. Entscheidung OFFEN (Ben) 1 steht weiter, nichts deshalb ersetzt.
