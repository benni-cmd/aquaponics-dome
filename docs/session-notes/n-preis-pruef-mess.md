# N-PREIS-PRUEF Gruppe 1D Mess und Elektrik (05.11.2026)

Bezugsdatei: `data/beschaffung/mess_elektrik.json` (22 Zeilen, davon 10 platziert). Gelesen im Browser-Pane ohne Klick; nichts gekauft, nirgends angemeldet.

## Grenze der Lesbarkeit
Von Hand lesbar waren: DigiKey (FI, NL, DE), Atlas Scientific, Galaxus, Shelly, Domadoo, el12, Tameson, Domoticx, GHL, eBay-Produktseite. **Nicht lesbar** (Bot-Pruefung, nicht umgangen): RobotShop EU, RS Online, teils eBay-Artikel, Kaufland, ManoMano, Tinytronics. Diese Zeilen tragen OFFEN.

## Ersetzt
1. `ELE-kabelverschraubung-pg`: RS-Angebote (403) ersetzt durch el12 HAUPA 250086 (4,85 EUR je 10 Stk, PL) und DigiKey DE TE Entrelec EP-SGL-M20-BL-C (0,89 EUR brutto je Stk, 79 auf Lager, EUR). Beide im Pane gelesen, M20 PA IP68. Auflage 7: Tameson (US-Storefront, USD, Europa-Lieferung nicht belegt) entfernt. Auflage 5: Kabelverschraubungen liegen an Gehaeusen im Trockenen, kein Fischwasserkontakt, Eignung nicht noetig (Werkstoff Polyamid benannt).
2. `MES-leck`: eBay SEBSON GS153 ist ein Einzelwarnmelder ohne Signalausgang, passt nicht. Ersatz Shelly Flood Gen4 mit Leck-Sensorkabel: Shelly Europe 34,90 EUR, Domadoo FR 35,28 EUR (beide gelesen).
3. `MES-level-druck`: eBay-Angebot beendet und 0-2 m statt 0-1 m. Kein Ersatz, siehe OFFEN.
4. `MES-flow-gross`: ManoMano (30 l/min) und eBay-China deckt/erfuellt D76 nicht. Entfernt, siehe OFFEN.
5. Entfernt ohne Ersatz: elektromax24-Rittal (404 laut Auflage A3), Eldon (zu klein), gotogarden (HTTP 402), eBay-Schwimmer CN.

## Bestaetigt (von Hand gelesen 05.11.)
1. `MES-do-mini`: DigiKey NL ENV-20-DOX, 285,72 EUR brutto, 11 auf Lager, Active. Passt (Atlas Mini-DO).
2. `MES-temp-ds`: Domoticx DS18B20 waterdicht RVS, 4,07 EUR, 43 auf Lager. Kabel Titel 2 m, Text 100 cm.
3. `MES-level-float`: GHL PL-1889, 44,90 EUR, sofort lieferbar, vertikale Montage, Mini-DIN.
4. `MES-schaltschrank` Nachbargroesse: Galaxus Rittal AX 1281.000 469,97 EUR (siehe OFFEN Ben).
5. `MES-temperatur` (Annahme, gleiche Seite wie temp-ds) und `MES-o2` (Annahme wie do-mini).
6. Nur per Linkpruefung bestaetigt (Titel passt, Preis nicht gelesen): `ELE-kabelkanal-30x60`, `ELE-hutschiene-35`, `MES-co2-scd41` (die VERDACHT-Meldung "39" ist ein Filterartefakt).

## OFFEN mit Grund (Quelle)
1. `MES-ph` (platziert): RobotShop EU nicht lesbar, DigiKey ENV-40-PH gelesen: "no longer available". Zweite EU-Quelle fehlt. Offer bleibt als Q-Treffer.
2. `MES-do-ind` (platziert): kein EU-Haendler fuer ENV-50-DO; Atlas direkt nur US.
3. `MES-level-druck` (platziert): kein EU-Angebot 0-1 mH2O mit Preis gelesen. Kandidat RS AT 2726968 (gesperrt), Tecson TDS-52xxx, Barksdale, Aplisens nur Datenblatt.
4. `MES-flow-gross`: kein EU-Angebot DN32 bis 120 l/min.
5. `MES-druck-schalter`, `MES-strom-ct` (Tinytronics), `ELE-hutschiene-35` (RS), `MES-co2-scd41` (zweites Angebot): gesperrt oder nicht geoeffnet.
6. `BLE-schrankboden-3x500x800`, `SON-schrankwand-500x800`: Eigenbau-Zuschnitt, nicht platziert, kein Angebot angelegt (Zuschnitt-Shop gehoert zur Gruppe Stahl).
7. `MES-ph`, `MES-level-float`, `MES-temp-ds`, `MES-do-mini`, `MES-ec`, `ELE-schaltschrank`: zweite unabhaengige EU-Quelle fehlt oder nicht lesbar.

## OFFEN (Ben)
1. `MES-ec`: DigiKey-Seite widerspricht sich (Beschreibung K 0.1, Artikel und Datenblatt K 1.0). R39 plant K 0,1; in EU nur K 1.0 (Bestand 0). Atlas nennt fuer K 0.1 0,07-50.000 uS/cm; Entscheidung K 1.0 ja/nein.
2. `ELE-schaltschrank`: Mass. 500x800x1200 gibt es nicht; Vorschlag Rittal AX 800x1200x400 (469,97 EUR). Modell aendert sich nicht.
3. `MES-flow-12`: Hobby-Sensor YF-S201 statt Atlas, Dauerbetrieb im Fischwasser nicht belegt.
4. `MES-par`: SQ-520 (USB) statt SQ-500 (analog).
5. `MES-temperatur`, `MES-o2`: Sondentyp der Station.
6. `MES-leck` und `MES-level-float`: Schnittstelle (Shelly WLAN/Zigbee, GHL Mini-DIN) zum Messknoten.

## Lebensmitteleignung
Mess- und Elektrikteile haben keinen Fischwasser-Bauteilkontakt ausser Sondengehaeusen; kein Herstellerbeleg gesucht (Vorlaeufige Entscheidung (a)).
