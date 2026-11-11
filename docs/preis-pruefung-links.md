# Preis-Pruefung: Link-Messlauf und Plausibilitaet (N-PREIS-PRUEF)

Erzeugt von `python -X utf8 scripts/check_links.py` aus `data/stueckliste.json`; Rohdaten `data/preis_pruefung_links.json`.
Nicht von Hand bearbeiten: neu erzeugen. Urteile: FEHLER (404/Netz/Weiterleitung auf Startseite, Suche, Kategorie), GESPERRT (Seite blockt Skripte, von Hand oeffnen), VERDACHT (Kennmass des Artikels fehlt auf der Seite oder steht nicht in Titel/URL, oder Bemerkung sagt ERSATZ), OK.

## Zahlen

- Zeilen der Stueckliste: 345; Zeilen mit mindestens einem Link: 175
- Links (Haupt- und Alternativangebote): 300; eindeutige URLs: 254
- GESPERRT: 27
- VERDACHT: 90
- OK: 183
- Zeilen ohne Link: 170
- Plausibilitaet: Lebensmittel OFFEN 284, belegt 8; Europa NEIN/unklar 0; Ersatz laut Bemerkung 11

| Bezugsdatei | FEHLER | GESPERRT | VERDACHT | OK |
|---|---|---|---|---|
| behaelter.json | 0 | 6 | 10 | 13 |
| huelle_pflanze.json | 0 | 2 | 3 | 15 |
| leitung.json | 0 | 0 | 5 | 116 |
| mess_elektrik.json | 0 | 13 | 7 | 5 |
| stahl.json | 0 | 3 | 61 | 30 |
| u2_wasserkreislauf.json | 0 | 2 | 2 | 2 |
| u8_unify.json | 0 | 1 | 2 | 2 |

## Links je Angebot

Rang 1 = Hauptangebot (Preis der Liste), 2+ = Alternativen.

| Urteil | Artikel | Rang | Haendler | HTTP | Grund | Seitentitel | URL |
|---|---|---|---|---|---|---|---|
| GESPERRT | BEH-ak-sedimentfilter | 1 | WilTec (NW-BRK01 20"-Set, 5 um | 403 | HTTP 403 | 403 Forbidden | https://www.wiltec.de/en/nw-brk01-1-stage-water-filter-20inch-508mm-5-sediment-filter-connectors-1inch-25.4mm/50881 |
| GESPERRT | BEH-halter-box-gehaeuse | 1 | RS Components Deutschland (RS  | 403 | HTTP 403 | Access Denied | https://de.rs-online.com/web/p/universalgehause/1972014 |
| GESPERRT | BEH-ibc-1000l | 1 | Fasswulf (Arthur Wulf Fasshand | 429 | HTTP 429 | Too many requests | https://www.fasswulf.de/products/1000-l-ibc-container-neu-kunststoff-palette-225-50-fda-un |
| GESPERRT | BEH-ibc-beetwanne | 1 | Fasswulf (Arthur Wulf Fasshand | 429 | HTTP 429 | Too many requests | https://www.fasswulf.de/products/1000-l-ibc-container-neu-kunststoff-palette-225-50-fda-un |
| GESPERRT | PMP-geblaese-luft | 1 | tanks.ie (Secoh JDK-S-200) | 429 | HTTP 429 | Too many requests | https://www.tanks.ie/secoh-jdk-s-200-single-series-blower/p21263 |
| GESPERRT | PMP-teichpumpe-5300 | 2 | Galaxus.de (Marktplatz) | 403 | HTTP 403 |  | https://www.galaxus.de/en/s4/product/oase-eco-classic-5500-fountain-garden-pond-6185872 |
| GESPERRT | FOL-pe-plane | 1 | Aquagart UV5 4x20 m (billiger. | 403 | HTTP 403 |  | https://www.billiger.de/pricelist/4320529954-aquagart-20m-gartenfolie-gewaechshausfolie-uv-5-fruehbeetfolie-treibhausfolie-4m-breit |
| GESPERRT | FOL-pe-plane | 3 | haga-welt.de, UV5-Folie 4 m br | 429 | HTTP 429 | Too many requests | https://haga-welt.de/en/products/uv5-film-in-various-widths-film-tunnel-greenhouse-film-hothouse-film |
| GESPERRT | ELE-hutschiene-35 | 2 | RS Online DE (RS PRO gelocht,  | 403 | HTTP 403 | Access Denied | https://de.rs-online.com/web/p/din-schienen/2258315 |
| GESPERRT | ELE-kabelverschraubung-pg | 1 | DigiKey DE (TE Entrelec EP-SGL | 403 | HTTP 403 |  | https://www.digikey.de/de/products/detail/te-connectivity-entrelec/EP-SGL-M20-BL-C/16686595 |
| GESPERRT | ELE-schaltschrank-500x800x1200 | 1 | Galaxus.de (Rittal AX 1281.000 | 403 | HTTP 403 |  | https://www.galaxus.de/en/s4/product/rittal-ax-1281000-switch-cabinet-800-x-1200-x-400-sheet-steel-light-grey-ral-7035-1pce-electrical-en-23688527 |
| GESPERRT | MES-do-mini | 1 | DigiKey NL (Atlas ENV-20-DOX) | 403 | HTTP 403 |  | https://www.digikey.nl/en/products/detail/atlas-scientific/ENV-20-DOX/16003119 |
| GESPERRT | MES-druck-schalter | 1 | Kaufland AT (KOTARBAU BSK 2 1/ | 403 | HTTP 403 |  | https://www.kaufland.at/product/466406546/ |
| GESPERRT | MES-druck-schalter | 2 | eBay.de (einstellbarer Drucksc | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/397635686182 |
| GESPERRT | MES-ec | 1 | DigiKey FI (Atlas ENV-40-EC-K1 | 403 | HTTP 403 |  | https://www.digikey.fi/en/products/detail/atlas-scientific/ENV-40-EC-K1-0/16002997 |
| GESPERRT | MES-flow-12 | 2 | Farnell ES (DFRobot SEN0217, 1 | 403 | HTTP 403 |  | https://es.farnell.com/dfrobot/sen0217/sensor-flujo-agua-0-5-placa-arduino/dp/3517923 |
| GESPERRT | MES-leck | 1 | Shelly Europe (Shelly Flood Ge | 429 | HTTP 429 | Too many requests | https://www.shelly.com/de/products/leak-sensor-cable |
| GESPERRT | MES-o2 | 1 | Annahme: wie MES-do-mini (Digi | 403 | HTTP 403 |  | https://www.digikey.nl/en/products/detail/atlas-scientific/ENV-20-DOX/16003119 |
| GESPERRT | MES-ph | 1 | RobotShop EU (Atlas ENV-40-pH, | 403 | HTTP 403 |  | https://eu.robotshop.com/de/products/atlas-scientific-ph-probe |
| GESPERRT | MES-strom-ct | 1 | Tinytronics (SCT013-030, 30 A  | 403 | HTTP 403 |  | https://www.tinytronics.nl/en/sensors/current-voltage/ac-current-sensor-sct013-030-30a |
| GESPERRT | MES-temp-ds | 2 | RobotShop EU (DFRobot DS18B20, | 403 | HTTP 403 |  | https://eu.robotshop.com/de/products/ds18b20-waterproof-digital-temperature-sensor |
| GESPERRT | PRF-alu-haut-profil | 1 | alu-verkauf.de (Hildesheim) | 429 | HTTP 429 | Too many requests | https://alu-verkauf.de/en/products/aluminium-profile-u-profile |
| GESPERRT | PRF-alu-keilschiene | 1 | alu-verkauf.de (Hildesheim) | 429 | HTTP 429 | Too many requests | https://alu-verkauf.de/en/products/aluminium-profile-u-profile |
| GESPERRT | PRF-alu-klemmleiste | 1 | alu-verkauf.de (Hildesheim) | 429 | HTTP 429 | Too many requests | https://alu-verkauf.de/en/products/aluminium-profile-flach |
| GESPERRT | MAT-epdm-teichfolie | 2 | dachfolien.de (FiFox EPDM Dach | 429 | HTTP 429 | Too many requests | https://dachfolien.de/en/collections/fifox/products/fifox-epdm-dachfolie-pro-1-5-mm |
| GESPERRT | PMP-tauchpumpe-oase-8000 | 2 | guenstiger.de (Preisvergleich, | 403 | HTTP 403 |  | https://www.guenstiger.de/Produkt/Oase/Aquamax_Eco_Premium_8000.html |
| GESPERRT | SCH-schlauch-luft-d8 | 1 | eBay AquaNova (Silikonschlauch | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/p/1656628645 |
| VERDACHT | BEH-drittbecken-klein | 1 | DENIOS | 200 | Kennmass fehlt auf der Seite: 1055, 920; Bemerkung: ERSATZ | Lager- und Dosierbehälter aus Polyethylen (PE), 500 Liter Vo | https://www.denios.de/lager-und-dosierbehaelter-aus-polyethylen-pe-500-liter-volumen-natur-transparent-136937/136937 |
| VERDACHT | BEH-drittbecken-klein | 2 | ANDO Technik GmbH (PE-Behaelte | 200 | Kennmass fehlt auf der Seite: 1055, 920 | PE Dosierbehälter 500l anschlussfertig als Vorlagebehälter z | https://ando-technik.com/pe-dosierbehaelter--500l-weiss-h-1230mm--d-740m.html |
| VERDACHT | BEH-fass-hdpe | 1 | Rekubik GmbH | 200 | Kennmass fehlt auf der Seite: 500 | 120 L Weithalsfass Kunststoffdeckelfass mit Spannring, Blau, | https://www.rekubik.de/kanister-faesser/faesser/120-l-weithalsfass-kunststoffdeckelfass-mit-spannring-blau-un-zulassung |
| VERDACHT | BEH-fass-hdpe | 2 | richter & hess Verpackungen | 200 | Kennmass fehlt auf der Seite: 500 | 120 Liter Kunststoff Deckelfass blau UN Zulassung lebensmitt | https://shop.richter-hess.de/standarddeckelfass-120-l-aus-kunststoff-105d120rbxs.html |
| VERDACHT | BEH-ibc-1000l | 3 | Faesser.de (Gerhard van Well G | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 1000 | Lebensmittelechte IBC-Container - Qualität & Sicherheit | https://www.faesser.de/IBC-Container/Lebensmittel/ |
| VERDACHT | BEH-messbecher-pp | 1 | barstuff.de | 200 | Kennmass fehlt auf der Seite: 160, 310 | Messbecher mit 100ml Skalierung, Polypropylen - 5 Liter | https://www.barstuff.de/messbecher-mit-100ml-skalierung-polypropylen-5-liter-12896 |
| VERDACHT | BEH-messbecher-pp | 2 | Bueromarkt-AG (Huenersdorff 93 | 200 | Kennmass fehlt auf der Seite: 160, 310 | Hünersdorff Messbecher 939000, aus Kunststoff, mit ml / Lite | https://www.bueromarkt-ag.de/messbecher_huenersdorff_939000_aus_kunststoff,p-939000.html |
| VERDACHT | BEH-messzelle-acryl | 2 | Hornbach Deutschland (Acrylgla | 200 | Kennmass fehlt auf der Seite: 260, 315 | acrylplatten kaufen bei HORNBACH | https://www.hornbach.de/s/acrylplatten |
| VERDACHT | BEH-tank-pe-580x865 | 1 | Rekubik GmbH | 200 | Kennmass fehlt auf der Seite: 865; Kennmass nicht in Titel/URL (nur im Seitentext): 580 | 220 L Weithalsfass Kunststoffdeckelfass mit Spannring, Blau, | https://www.rekubik.de/kanister-faesser/faesser/220-l-weithalsfass-kunststoffdeckelfass-mit-spannring-blau-un-zulassung |
| VERDACHT | PMP-teichpumpe-5300 | 1 | OBI.de | 200 | Kennmass fehlt auf der Seite: 5300 | Oase Teichpumpe AquaMax Eco Classic 5500 l/h 60 W kaufen bei | https://www.obi.de/p/1358613/oase-filter-und-bachlaufpumpe-aquamax-eco-classic-5500 |
| VERDACHT | FOL-epdm-dichtung-630x440 | 1 | diconfa.de, EPDM-Matte nach Ma | 200 | Kennmass fehlt auf der Seite: 440, 630 | diconfa EPDM Rubber Mat UV Stable | https://diconfa.de/en/epdm-rubber-mat-made-to-measure/ |
| VERDACHT | FOL-epdm-schaumband | 1 | Buerklin Elektronik, Essentra  | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | 10187890 / ESSENTRA COMPONENTS / Adhesive Tapes / Bürklin El | https://www.buerklin.com/en/p/essentra-components/adhesive-tapes/1200325001/14L2406/ |
| VERDACHT | SON-tuerblatt-1000x2000 | 1 | garagenonline.eu, Nebeneingang | 200 | Kennmass fehlt auf der Seite: 1000, 2000 | Nebeneingangstür Stahl nach Maß / 40 mm gedämmt | https://www.garagenonline.eu/onlineshop/nebeneingangsturen/nebeneingangstur-stahl-nach-mass-aus-iso-40-sektionaltor-sandwichpaneelen |
| VERDACHT | FIT-bogen90-d75 | 1 | Schwarte-Shop | 200 | Bemerkung: NICHT belegt | PVC-U Klebefitting Winkel 90° 75 mm - 75018 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-75-mm |
| VERDACHT | ROH-leerrohr-dn100 | 1 | Hornbach | 200 | Kennmass fehlt auf der Seite: 100 | KG Rohr DN 110 1000 mm / HORNBACH | https://www.hornbach.de/p/kg-rohr-dn-110-1000-mm/267298/ |
| VERDACHT | SCH-rohrschelle-d110 | 1 | Schwarte-Shop | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 110 | Fischer Rohrschelle FRS 4" (108-116 mm), verzinkt - 20149 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-dn-100-4-108-116-mm |
| VERDACHT | SCH-rohrschelle-d50 | 1 | Schwarte-Shop | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | Fischer Rohrschelle FRS 1 1/2" (48-54 mm), verzinkt - 20145 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-dn40-1-1-2-48-54-mm |
| VERDACHT | SCH-schlauchschelle-id16 | 1 | Schwarte-Shop | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 16 | ASW Schlauchschelle W4 Edelstahl 12-20 mm, Bandbreite 9 mm | https://www.schwarte-shop.de/schlauchschelle-edelstahl-w4-bandbreite-9mm-spannbereich-12-20-mm-1-2 |
| VERDACHT | MES-co2-scd41 | 1 | SOS electronic (Sensirion SCD4 | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 39 | SCD41-D-R2 / SENSIRION Calibrated CO2 Sensor/ 347342 | https://www.soselectronic.com/en-us/products/sensirion/scd41-d-r2-347342 |
| VERDACHT | MES-flow-12 | 1 | Domoticx (YF-S201, G1/2, 1-30  | 200 | Kennmass fehlt auf der Seite: 39; Bemerkung: Ersatz | Water flow meter 1-30L/Min 1/2" DN15 kunststof 3-pin JST-SM  | https://domoticx.net/webshop/water-flow-meter-1-30lmin-12-dn15-kunststof-3-pin-jst-sm-yf-s201 |
| VERDACHT | MES-leck | 2 | Domadoo (Shelly Flood Gen4, RE | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 39 | Shelly Flood 4: Wassersensor WiFi, Bluetooth, Zigbee, Matter | https://www.domadoo.fr/de/smart-home-produkte/8387-shelly-wassersensor-wifi-bluetooth-zigbee-matter-gen4-flood-4-3800238071714.html?domid=8 |
| VERDACHT | MES-level-float | 1 | aquariumcomputer.com (GHL Nive | 200 | Kennmass fehlt auf der Seite: 39 | Niveau-Sensor, Schwimmer, Version 2 - GHL Advanced Technolog | https://www.aquariumcomputer.com/de/?p=87440 |
| VERDACHT | MES-par | 1 | shop-meeresaquaristik.de (Apog | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 39 | Apogee SQ-520 Quantum Sensor with USB output - Mrutzek Meere | https://www.shop-meeresaquaristik.de/Measurement-control-technology/PAR-measuring-devices-quantum-meters/Apogee-SQ-520-Quantum-Sensor-with-USB-output::18462.html |
| VERDACHT | MES-strom-ct | 2 | CDR (SCT-013-030) | 200 | Kennmass fehlt auf der Seite: 39 | SCT-013-030 inductive current sensor 0 - 30 A | https://en.cdr.pl/p6529,sct-013-030-inductive-current-sensor-0-30-a.html |
| VERDACHT | MES-temp-ds | 1 | Domoticx (DS18B20, Kabel 1-2 m | 200 | Kennmass fehlt auf der Seite: 39 | Temperatuur sensor digitaal 1-wire dallas waterdicht DS18B20 | https://domoticx.net/webshop/temperatuur-sensor-digitaal-1-wire-dallas-waterdicht-ds18b20-2m-kabel/ |
| VERDACHT | BLE-blech-st-3 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 700; Bemerkung: NICHT 3 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-blech-st-3 | 2 | stahl-shop24.de | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 700 | Stahl Blech 300x1500x3mm / 3 mm / 300x1500 mm / SBL128-5 | https://www.stahl-shop24.de/Stahl-Blech-300x1500x3mm |
| VERDACHT | BLE-blech-st-5 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 400, 840 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-blech-st-5 | 2 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 840; Kennmass nicht in Titel/URL (nur im Seitentext): 400 | Stahl Blech 200x1500x5mm / 5 mm / 200x1500 mm / SBL119-7 | https://www.stahl-shop24.de/Stahl-Blech-200x1500x5mm |
| VERDACHT | BLE-blech-st-6 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 100 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-blech-st-6 | 2 | stahl-shop24.de | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 100 | Stahl Blech 300x1500x6mm / 6 mm / 300x1500 mm / SBL128-8 | https://www.stahl-shop24.de/Stahl-Blech-300x1500x6mm |
| VERDACHT | BLE-fussplatte-100x100x6 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 100 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-fussplatte-100x100x6 | 2 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 100 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-150x150x8 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 150 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-150x150x8 | 2 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 150 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-fussplatte-150x150x8 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 150 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-200x200x8 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 200 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-200x200x8 | 2 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 200 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-fussplatte-200x200x8 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 200 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-70x70x5 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 70 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-70x70x5 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 70 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-fussplatte-70x70x5 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 70 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-80x80x6 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 80 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-fussplatte-80x80x6 | 2 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 80 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-80x80x8 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 80 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-80x80x8 | 2 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 80 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-fussplatte-80x80x8 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 80 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-platte-250x250x15 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 250; Kennmass nicht in Titel/URL (nur im Seitentext): 15 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-platte-250x250x15 | 2 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 250; Kennmass nicht in Titel/URL (nur im Seitentext): 15 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-platte-250x250x15 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass fehlt auf der Seite: 250; Kennmass nicht in Titel/URL (nur im Seitentext): 15 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-pp-blende-290x260 | 1 | Technoplast Kunststoffe | 200 | Kennmass fehlt auf der Seite: 260, 290 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| VERDACHT | BLE-pp-blende-290x260 | 2 | plastx24 | 200 | Kennmass fehlt auf der Seite: 260, 290 | PP Zuschnitte online kaufen / PlastX24 | https://www.plastx24.de/pp/pp/ |
| VERDACHT | BLE-pp-tafel-502x345x5 | 1 | Technoplast Kunststoffe | 200 | Kennmass fehlt auf der Seite: 345, 502 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| VERDACHT | BLE-pp-tafel-502x345x5 | 2 | plastx24 | 200 | Kennmass fehlt auf der Seite: 345, 502 | PP Zuschnitte online kaufen / PlastX24 | https://www.plastx24.de/pp/pp/ |
| VERDACHT | BLE-pp-tafel-693x463x7 | 1 | Technoplast Kunststoffe | 200 | Kennmass fehlt auf der Seite: 463, 693 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| VERDACHT | BLE-pp-tafel-693x463x7 | 2 | plastx24 | 200 | Kennmass fehlt auf der Seite: 463, 693 | PP Zuschnitte online kaufen / PlastX24 | https://www.plastx24.de/pp/pp/ |
| VERDACHT | BLE-v2a-3mm-korbflansch | 1 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 414, 604 | Edelstahl Blech 500x800x3mm / 3 mm / 500x800 mm / VBL139-5 | https://www.stahl-shop24.de/Edelstahl-Blech-500x800x3mm |
| VERDACHT | BLE-v2a-3mm-korbflansch | 2 | Feld Maschinenbau (feld-eitorf | 200 | Kennmass fehlt auf der Seite: 414, 604 | Edelstahlblech gebürstet, V2A, Stärke 3,0 mm / Online bestel | https://www.feld-eitorf.de/edelstahlblech-gebuerstet-staerke-3-0-mm |
| VERDACHT | BLE-v2a-3mm-korbflansch | 3 | Edelstahl-Saegezentrum | 200 | Kennmass fehlt auf der Seite: 414, 604 | Edelstahlblech 0,3 - 3mm Blech Platte V2A 1.4301 2B Zuschnit | https://www.edelstahl-saegezentrum.de/bleche/edelstahlblech-0-3-3mm-blech-platte-v2a-1-4301-2b-zuschnitt-groesse-nach-wahl_197_8070 |
| VERDACHT | PRF-alu-keilschiene | 2 | Hornbach | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 15, 25 | Alu U Profil kaufen bei HORNBACH | https://www.hornbach.de/s/Alu%20U%20Profil |
| VERDACHT | PRF-alu-keilschiene | 3 | Wegner24 | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 15, 25 | Klemmprofil, 2m Länge, 22,99 € | https://www.wegner24.eu/Klemmprofil_Netze_Planen |
| VERDACHT | PRF-pvcu-rinne-130x100 | 1 | Golden Green Club | 200 | Kennmass fehlt auf der Seite: 130; Bemerkung: nicht 7 | Urban Hydro NFT Rinne 100x50 mm - mit Loch, 1-lagig, innen w | https://goldengreenclub.de/produkt/urban-hydro-nft-rinne-100x50-mm-mit-loch-1-lagig-innen-weiss-290-cm/ |
| VERDACHT | PRF-pvcu-rinne-130x100 | 2 | GrowKing24 | 200 | Kennmass fehlt auf der Seite: 130 | Urban Hydro NFT Rinne 100x50 mm - ohne Loch, 1-lagig, innen  | https://growking24.com/urban-hydro-nft-rinne-100x50-mm-ohne-loch-1-lagig-innen-weiss-290-cm/ |
| VERDACHT | PRF-st-rr25x25x2 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr30x30x2 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x40x2 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x40x2.5 | 1 | stahl-shop24.de | 200 | Bemerkung: Ersatz | Quadratrohr Feuerverzinkt 40x40x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-40x40x3mm-1000mm |
| VERDACHT | PRF-st-rr40x40x2.5 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x40x3 | 3 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x60x3 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40, 60 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr60x60x3 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 60 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rund20 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | Stabstahl Rundeisen bis 100 mm Durchmesser | https://www.metallparadies.de/stahl-vollmaterial-rundstahl.html |
| VERDACHT | PRF-st-strebe30x30 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | Vierkantrohr Stahl nach Maß / Quadratrohr & Rechteckrohr | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | SRB-halter-klein-12x10x20 | 2 | Hornbach | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 10, 12 | Reyher Sechskantschraube o. Schaft DIN 933 M6x20 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x20-mm-galv-verzinkt-100-stueck/10317037/ |
| VERDACHT | SRB-halter-klein-12x10x20 | 3 | Schraubenking (schraubenking.a | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 10, 12 | M6 x 20mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M6-x-20mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P001095 |
| VERDACHT | SRB-satz-m6x55 | 1 | Schraubenking (schraubenking.a | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 55; Bemerkung: ERSATZ | M6 x 60mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M6-x-60mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P000266 |
| VERDACHT | SRB-satz-m6x55 | 2 | Hornbach | 200 | Kennmass fehlt auf der Seite: 55 | Reyher Sechskantschraube o. Schaft DIN 933 M6x60 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x60-mm-galv-verzinkt-100-stueck/10316892/ |
| VERDACHT | WNK-flach-14x3 | 1 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 14; Bemerkung: Ersatz | Flachstahl verzinkt 30x3mm 1000mm | https://www.stahl-shop24.de/Flachstahl-verzinkt-30x3mm-1000mm |
| VERDACHT | WNK-flach-14x3 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 14 | Flachstahl 20x3 mm bis 300x20 mm S235JR | https://www.metallparadies.de/stahl-flacheisen-s235jr-558.html |
| VERDACHT | WNK-rinnenhalter-25 | 1 | Metallparadies (metallparadies | 200 | Bemerkung: ERSATZ | Winkelstahl 25x25x3 mm / Jetzt kaufen | https://www.metallparadies.de/winkelstahl-25x25x3-mm.html |
| VERDACHT | WNK-rinnenhalter-25 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | Stahl Winkelprofil warmgewalzt 30x30x3 mm | https://www.metallshopper.de/p/stahl-winkelprofil-warmgewalzt-30x30x3-mm-712809/ |
| VERDACHT | WNK-wandlasche-30x30x3 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 30; Bemerkung: ERSATZ | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | WNK-wandlasche-30x30x3 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | WNK-winkel-36x60x60 | 1 | Hornbach | 200 | Kennmass fehlt auf der Seite: 36 | Winkelverbinder 60 x 60 x 45 mm, sendzimirverzinkt, 1 Stück  | https://www.hornbach.de/p/winkelverbinder-60-x-60-x-45-mm-sendzimirverzinkt-1-stueck/3375551/ |
| VERDACHT | WNK-winkel-36x60x60 | 2 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 36; Kennmass nicht in Titel/URL (nur im Seitentext): 60 | Winkelstahl 25x25x3 mm / Jetzt kaufen | https://www.metallparadies.de/winkelstahl-25x25x3-mm.html |
| VERDACHT | WNK-winkel-36x60x60 | 3 | Metallshopper (Metaalshopper) | 200 | Kennmass fehlt auf der Seite: 36 | Stahl Winkelprofil warmgewalzt 60x60x6 mm | https://www.metallshopper.de/p/stahl-winkelprofil-warmgewalzt-60x60x6-mm-384238/ |
| VERDACHT | BEH-schlammbehaelter-350 | 1 | OBI (Graf Universal-Kunststoff | 200 | Kennmass fehlt auf der Seite: 350, 600, 900 | Graf Universal-Kunststofffass Oval 300 l kaufen bei OBI | https://www.obi.at/p/1104751/graf-universal-kunststofffass-oval-300-l |
| VERDACHT | PMP-tauchpumpe-oase-8000 | 1 | Neyses Gartenteiche GmbH ueber | 200 | Kennmass fehlt auf der Seite: 8000 | Oase AquaMax Eco Premium 9000 / HORNBACH | https://www.hornbach.de/p/oase-aquamax-eco-premium-9000/12714146/ |
| VERDACHT | ARM-schnellkupplung-id19 | 1 | Westfalia | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 19 | Messing-Schnellkupplung 3/4 Zoll mit Edelstahlkugeln / Westf | https://www.westfalia.de/shop/boni-33032-messing-stecksystem-3-4-zoll-schnellkupplung-ohne-wasserstop-3025 |
| VERDACHT | ARM-schnellkupplung-id19 | 2 | Reimo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 19 | Schnellkupplung 3/4" mit Schlauchtülle / Wasseranlage Instal | https://www.reimo.com/camping-shop/wasser-sanitaer-campingtoilette/wasseranlage-installation/14407/schnellkupplung-3/4-mit-schlauchtuelle |
| OK | BEH-ak-sedimentfilter | 2 | Alfiltra GmbH (Gehaeuse 10" DN | 200 | HTTP 200 | Filtergehäuse 10 x 2,5 DN25 / Filtergehäuse / Alfiltra | https://www.alfiltra.de/water-filter/filtergehaeuse-fch-tr-9-3-4-x-2-5-san |
| OK | BEH-ibc-1000l | 2 | Rekubik GmbH (Werit, schwarz) | 200 | HTTP 200 | 1000 l IBC Container schwarz DN150/50 / REKUBIK | https://www.rekubik.de/ibc-container/neue-ibc/1000l-ibc-container-schwarz-auf-pe-palette-neu |
| OK | BEH-ibc-beetwanne | 2 | Rekubik GmbH (Werit, schwarz) | 200 | HTTP 200 | 1000 l IBC Container schwarz DN150/50 / REKUBIK | https://www.rekubik.de/ibc-container/neue-ibc/1000l-ibc-container-schwarz-auf-pe-palette-neu |
| OK | BEH-kanister-hdpe | 1 | richter & hess Verpackungen | 200 | HTTP 200 | Kunststoff Kanister 20 Liter kaufen bei richter & heß VERPAC | https://shop.richter-hess.de/kanister-20-l-aus-kunststoff-106est20n980-61xova.html |
| OK | BEH-kanister-hdpe | 2 | subolab | 200 | HTTP 200 | subolab. 20 L UN-Kanister HDPE natur ND61 – rechteckig, 950  | https://www.subolab.de/20-liter-un-kanister-aus-hdpe-natur-rechteckig-nd61-950-g/ |
| OK | PMP-pumpe-gross | 1 | Green Aqua (greenaqua.hu) | 200 | HTTP 200 | EHEIM Universal 3400 / Green Aqua | https://greenaqua.hu/en/eheim-universal-3400.html |
| OK | PMP-pumpe-gross | 2 | shop-meeresaquaristik.de | 200 | HTTP 200 | Eheim Universalpumpe 3400 / 1262 (1262210) - Eheim - Mrutzek | https://www.shop-meeresaquaristik.de/Pumpen/Foerderpumpen/Eheim/Eheim-Foerderpumpen/Eheim-Universalpumpe-3400-1262-1262210::17.html |
| OK | PMP-pumpe-gross | 3 | aquaristikshop.com | 200 | HTTP 200 | EHEIM Universal Pump 3400 (1262) | https://www.aquaristikshop.com/aquaristic/EHEIM-Universal-Pump-1262/126221/ |
| OK | PMP-pumpe-gross | 4 | Hornbach Oesterreich | 200 | HTTP 200 | Universal-Pumpe EHEIM 3400 3-adriger Schukostecker mit 1,7 / | https://www.hornbach.at/p/universal-pumpe-eheim-3400-3-adriger-schukostecker-mit-1-7-m-kabel-80-w/8888958/ |
| OK | PMP-pumpe-klein | 1 | aquacomputer.de | 200 | HTTP 200 | Eheim 1250 / Eheim universal 1200 (Version Deutschland) Pump | https://shop.aquacomputer.de/Wasserkuehlung/Pumpen-Zub/Pumpen/Eheim-1250-Eheim-universal-1200-Version-Deutschland-Pumpe-1250219::1276.html |
| OK | PMP-pumpe-klein | 2 | Green Aqua (greenaqua.hu) | 200 | HTTP 200 | EHEIM Universal 1200 / Green Aqua | https://greenaqua.hu/en/eheim-universal-1200-pump-1250-828w-1200-lph.html |
| OK | TOP-aktivkohle | 2 | Ecosoft (Jacobi AquaSorb CS 12 | 200 | HTTP 200 | Aktivkohle Jacobi AquaSorb СS 12x40 25 kg, AQUASORB_CS_12X40 | https://www.ecosoft.com/de-de/product-ecosoft/fm-ss1240 |
| OK | TOP-aktivkohle | 3 | silica-gel.it (Kokosnuss-GAC 1 | 200 | HTTP 200 | Granular Activated Carbon (Coconut) / In Stock / Small & Lar | https://www.silica-gel.it/en/activated-charcoal/4721-granular-activated-carbon-coconut.html |
| OK | FOL-epdm-tuerdichtung | 1 | graf-dichtungen.de, Klebedicht | 200 | HTTP 200 |  | https://www.graf-dichtungen.de/pdfdatasheet/59544667a10f4f4aa2186a236edc010c |
| OK | FOL-pe-plane | 2 | gekaho-shop.de, Gewaechshausfo | 200 | HTTP 200 | Gewächshausfolien UV 4 Standard - Meterware | https://gekaho-shop.de/gewaechshausfolien/hochbeet-folie/gewaechshausfolien-uv-4-standardfolie |
| OK | SON-korbgriff-v2a | 1 | profishop.de, Ganter GN 425-NI | 200 | HTTP 200 | Ganter Edelstahl-Bügelgriffe (GN 425-NI-12-160-GS) VE: 10 St | https://www.profishop.de/p/ganter-edelstahl-buegelgriffe-gn-425-ni-12-160-gs-ve-10-stueck-425-ni-12-160-gs |
| OK | SON-korbgriff-v2a | 2 | leschhorn.de, EO-20-160-36 Ova | 200 | HTTP 200 | Leschhorn EO-20-160-36 Oval-Edelstahl Bügelgriffe A 160, Mat | https://www.leschhorn.de/de/detail/0199737fd8ce728b87dbedb4bded8b0c |
| OK | SON-polycarbonat-paneel | 2 | polycarbonatstore.de, Doppelst | 200 | HTTP 200 | SUNLITE® Doppelstegplatte 8 mm klar | https://polycarbonatstore.de/product/doppelstegplatte-8-mm-klar/ |
| OK | SON-polycarbonat-paneel | 3 | stegplattenguru.de, MARLON ST  | 200 | HTTP 200 | Doppelstegplatten 8 mm farblos – Polycarbonat | https://stegplattenguru.de/polycarbonat-doppelstegplatte-hohlkammerplatte-8-mm-farblos/ |
| OK | SON-polycarbonat-paneel | 4 | stegplatten-fachmarkt.de, Steg | 200 | HTTP 200 | Stegplatten 8 mm, Doppelstegplatten 8 mm | https://www.stegplatten-fachmarkt.de/stegplatten-aus-polycarbonat/stegplatten-8-mm/transparent-klar/stegplatten-8-mm-transparent-klar-2100-mm-breit.html |
| OK | SON-spannverschluss-edelstahl | 1 | schraubbar.de, Ganter GN 927.7 | 200 | HTTP 200 | schraubbar.de / GN 927.7 Edelstahl-Exzenterspanner mit Schra | https://www.schraubbar.de/de/edelstahl-exzenterspanner-mit-schraube-59555.html |
| OK | SON-tuerdruecker | 1 | mein-tuergriff.de, Wechsel-Dru | 200 | HTTP 200 | Türdrücker U-Form Rosette Edelstahl Türgriff Wechsel-Drücker | https://www.mein-tuergriff.de/tuerdruecker-u-form-rosette-edelstahl-tuergriff-wechsel-drueckergarnitur-138-1070-wg_163_1124/ |
| OK | SON-tuerdruecker | 2 | habefa.de, Wechselgarnitur Ede | 200 | HTTP 200 | Rosettengarnitur aus Edelstahl für Objekttüren, Drücker/Drüc | https://www.habefa.de/shop/artikel/drueckergarnitur-aus-edelstahl-mit-rosette-fuer-objekttueren_4309.html |
| OK | SON-tuerscharnier | 1 | der-technikprofi.de, Hettich T | 200 | HTTP 200 | HETTICH Türband rechts, 80 x 45mm, Stahl verzinkt, 10 Stück, | https://www.der-technikprofi.de/Tuerband-80-x-45mm-DIN-Rechts-verzinkt |
| OK | SON-tuerscharnier | 2 | hornbach.de, Scharnier verzink | 200 | HTTP 200 | Scharnier verzinkt 80x45 mm / HORNBACH | https://www.hornbach.de/p/scharnier-verzinkt-80x45-mm/6826260/ |
| OK | TOP-blaehton | 1 | natursteinzentrum-rm.de, Lecat | 200 | HTTP 200 | Lecaton Blähton 8–16 mm – Hydrokultur Substrat kaufen | https://www.natursteinzentrum-rm.de/Lecaton-8-16-mm-im-Big-Bag/Lvton8-16-1-5 |
| OK | TOP-blaehton | 2 | kiesdirekt.de, Keramsit 8-16 m | 200 | HTTP 200 | Blähton 8-16 mm Keramsit online kaufen / Kies Direkt | https://www.kiesdirekt.de/p/blaehton-8-16-mm-keramsit-1073.asp |
| OK | TOP-blaehton | 3 | kiesundco.de, Hamann Blaehton  | 200 | HTTP 200 | Hamann Blähton 8-16 mm 800 l / Kiesundco | https://www.kiesundco.de/hamann-blaeaehton-8-16-mm-800-l |
| OK | ARM-bulkhead-d63 | 1 | Bevo | 200 | HTTP 200 | Bulkhead fitting PVC-U 63/75 mm x 2 1/2" glue socket/glue sp | https://www.bevo.com/en/bulkhead-fitting-pvc-u-63-75-mm-x-2-1-2-glue-socket-glue-spigot-x-male-thread-10bar-grey-7026182 |
| OK | ARM-bulkhead-pool | 1 | Bevo | 200 | HTTP 200 | Bulkhead fitting PVC-U 63/75 mm x 2 1/2" glue socket/glue sp | https://www.bevo.com/en/bulkhead-fitting-pvc-u-63-75-mm-x-2-1-2-glue-socket-glue-spigot-x-male-thread-10bar-grey-7026182 |
| OK | ARM-kugelhahn-d110 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 110 mm glue socket 10bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-110-mm-glue-socket-10bar-grey-type-dil-7003055 |
| OK | ARM-kugelhahn-d20 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 20 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-20-mm-glue-socket-16bar-grey-type-dil-0100843 |
| OK | ARM-kugelhahn-d20 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 20 mm - 75319 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-20-mm |
| OK | ARM-kugelhahn-d25 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 25 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-25-mm-glue-socket-16bar-grey-type-dil-0100844 |
| OK | ARM-kugelhahn-d25 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 25 mm - 75320 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-25-mm |
| OK | ARM-kugelhahn-d32 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| OK | ARM-kugelhahn-d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 32 mm - 75321 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-32-mm |
| OK | ARM-kugelhahn-d40 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 40 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-40-mm-glue-socket-16bar-grey-type-dil-0100846 |
| OK | ARM-kugelhahn-d40 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 40 mm - 75322 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-40-mm |
| OK | ARM-kugelhahn-d40 | 3 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 40 mm glue socket 16bar DN32 grey type  | https://www.bevo.com/en/vdl-ball-valve-pvc-u-40-mm-glue-socket-16bar-dn32-grey-type-eil-7018363 |
| OK | ARM-kugelhahn-d50 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 50 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-50-mm-glue-socket-16bar-grey-type-dil-0100847 |
| OK | ARM-kugelhahn-d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 50 mm - 75323 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-50-mm |
| OK | ARM-kugelhahn-d63 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 63 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-63-mm-glue-socket-16bar-grey-type-dil-0100848 |
| OK | ARM-kugelhahn-d63 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 63 mm - 75324 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-63-mm |
| OK | FIT-bogen45-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 110 mm - 75030 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-110-mm |
| OK | FIT-bogen45-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 20 mm - 75022 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-20-mm |
| OK | FIT-bogen45-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 25 mm - 75023 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-25-mm |
| OK | FIT-bogen45-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 32 mm - 75024 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-32-mm |
| OK | FIT-bogen45-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 40 mm - 75025 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-40-mm |
| OK | FIT-bogen45-d40 | 2 | Bevo | 200 | HTTP 200 | Profec Long bend 45° PVC-U 40 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-40-mm-glue-socket-16bar-grey-type-made-from-tubing-0110227 |
| OK | FIT-bogen45-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 50 mm - 75026 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-50-mm |
| OK | FIT-bogen45-d50 | 2 | Bevo | 200 | HTTP 200 | Profec Long bend 45° PVC-U 50 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-50-mm-glue-socket-16bar-grey-type-made-from-tubing-0110228 |
| OK | FIT-bogen45-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 63 mm - 75027 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-63-mm |
| OK | FIT-bogen45-d63 | 2 | Bevo | 200 | HTTP 200 | Profec Long bend 45° PVC-U 63 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-63-mm-glue-socket-16bar-grey-type-made-from-tubing-0110229 |
| OK | FIT-bogen45-d75 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 75 mm - 75028 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-75-mm |
| OK | FIT-bogen45-d75 | 2 | Bevo | 200 | HTTP 200 | Profec Long bend 45° PVC-U 75 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-75-mm-glue-socket-16bar-grey-type-made-from-tubing-0110230 |
| OK | FIT-bogen90-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 110 mm - 75020 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-110-mm |
| OK | FIT-bogen90-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 20 mm - 75012 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-20-mm |
| OK | FIT-bogen90-d20 | 2 | voelkner (Marktplatz-Anbieter  | 200 | HTTP 200 | PVC - U 90° Bogen 20 mm PN16 / » Freue dich auf voelkner | https://www.voelkner.de/products/12813981/PVC-U-90-Bogen-20-mm-PN16.html |
| OK | FIT-bogen90-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 25 mm - 75013 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-25-mm |
| OK | FIT-bogen90-d25 | 2 | Bevo | 200 | HTTP 200 | VDL Bend 90° PVC-U 25 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-25-mm-glue-socket-16bar-grey-7002570 |
| OK | FIT-bogen90-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 32 mm - 75014 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-32-mm |
| OK | FIT-bogen90-d32 | 2 | Bevo | 200 | HTTP 200 | VDL Bend 90° PVC-U 32 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-32-mm-glue-socket-16bar-grey-7002571 |
| OK | FIT-bogen90-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 40 mm - 75015 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-40-mm |
| OK | FIT-bogen90-d40 | 2 | Bevo | 200 | HTTP 200 | VDL Bend 90° PVC-U 40 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-40-mm-glue-socket-16bar-grey-7002572 |
| OK | FIT-bogen90-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 50 mm - 75016 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-50-mm |
| OK | FIT-bogen90-d50 | 2 | Bevo | 200 | HTTP 200 | VDL Bend 90° PVC-U 50 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-50-mm-glue-socket-16bar-grey-7002573 |
| OK | FIT-bogen90-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 63 mm - 75017 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-63-mm |
| OK | FIT-bogen90-d75 | 2 | Bevo | 200 | HTTP 200 | Profec Long bend 90° PVC-U 75 mm glue socket 16bar grey | https://www.bevo.com/en/profec-long-bend-90-pvc-u-75-mm-glue-socket-16bar-grey-0110183 |
| OK | FIT-kappe-d16 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 16 mm - 75136 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-16-mm |
| OK | FIT-kappe-d16 | 2 | Bevo | 200 | HTTP 200 | VDL Cap PVC-U 16 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-16-mm-glue-socket-16bar-grey-7002811 |
| OK | FIT-kappe-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 20 mm - 75137 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-20-mm |
| OK | FIT-kappe-d20 | 2 | Bevo | 200 | HTTP 200 | VDL Cap PVC-U 20 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-20-mm-glue-socket-16bar-grey-7002812 |
| OK | FIT-kappe-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 25 mm - 75138 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-25-mm |
| OK | FIT-kappe-d25 | 2 | Bevo | 200 | HTTP 200 | VDL Cap PVC-U 25 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-25-mm-glue-socket-16bar-grey-7002813 |
| OK | FIT-kappe-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 32 mm - 75139 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-32-mm |
| OK | FIT-kappe-d32 | 2 | Bevo | 200 | HTTP 200 | VDL Cap PVC-U 32 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-32-mm-glue-socket-16bar-grey-7002814 |
| OK | FIT-kappe-d50 | 1 | Bevo | 200 | HTTP 200 | VDL Cap PVC-U 50 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-50-mm-glue-socket-16bar-grey-7002816 |
| OK | FIT-kappe-d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 50 mm - 75141 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-50-mm |
| OK | FIT-kupplung-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 110 mm - 75115 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-110-mm |
| OK | FIT-kupplung-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 20 mm - 75107 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-20-mm |
| OK | FIT-kupplung-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 25 mm - 75108 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-25-mm |
| OK | FIT-kupplung-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 32 mm - 75109 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-32-mm |
| OK | FIT-kupplung-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 40 mm - 75110 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-40-mm |
| OK | FIT-kupplung-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 50 mm - 75111 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-50-mm |
| OK | FIT-kupplung-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 63 mm - 75112 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-63-mm |
| OK | FIT-kupplung-d75 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Muffe 75 mm - 75113 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-muffe-75-mm |
| OK | FIT-red-d110_d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 110 mm (ø 63 mm) - 75230 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-110-mm-o-63-mm |
| OK | FIT-red-d25_d20 | 1 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| OK | FIT-red-d25_d20 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 25 mm (ø 20 mm) - 75205 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-25-mm-o-20-mm |
| OK | FIT-red-d32_d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 32 mm (ø 25 mm) - 75208 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-32-mm-o-25-mm |
| OK | FIT-red-d40_d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 40 mm (ø 20 mm) - 75210 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-40-mm-o-20-mm |
| OK | FIT-red-d40_d32 | 1 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 40 mm x 32 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-40-mm-x-32-mm-glue-spigot-x-glue-socket-16bar-grey-0160740 |
| OK | FIT-red-d40_d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 40 mm (ø 32 mm) - 75212 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-40-mm-o-32-mm |
| OK | FIT-red-d50_d32 | 1 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 50 mm x 32 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-50-mm-x-32-mm-glue-spigot-x-glue-socket-16bar-grey-0160743 |
| OK | FIT-red-d50_d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 50 mm (ø 32 mm) - 75215 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-50-mm-o-32-mm |
| OK | FIT-red-d50_d40 | 1 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 50 mm x 40 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-50-mm-x-40-mm-glue-spigot-x-glue-socket-16bar-grey-0160744 |
| OK | FIT-red-d50_d40 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 50 mm (ø 40 mm) - 75216 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-50-mm-o-40-mm |
| OK | FIT-red-d63_d50 | 1 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 63 mm x 50 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-63-mm-x-50-mm-glue-spigot-x-glue-socket-16bar-grey-0160748 |
| OK | FIT-red-d63_d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 63 mm (ø 50 mm) - 75220 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-63-mm-o-50-mm |
| OK | FIT-red-d75_d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 75 mm (ø 50 mm) - 75223 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-75-mm-o-50-mm |
| OK | FIT-red-d75_d50 | 2 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 75 mm x 50 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-75-mm-x-50-mm-glue-spigot-x-glue-socket-16bar-grey-0160751 |
| OK | FIT-red-d75_d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 75 mm (ø 63 mm) - 75224 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-75-mm-o-63-mm |
| OK | FIT-red-d75_d63 | 2 | Bevo | 200 | HTTP 200 | Reducer bush PVC-U 75 mm x 63 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-75-mm-x-63-mm-glue-spigot-x-glue-socket-16bar-grey-0160752 |
| OK | FIT-stutzen-d16 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 16 mm x 3/8" - 75268 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-16-mm-x-3-8 |
| OK | FIT-stutzen-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 20 mm x 1/2" - 75270 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-20-mm-x-1-2 |
| OK | FIT-stutzen-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 32 mm x 3/4" - 75273 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-32-mm-x-3-4 |
| OK | FIT-stutzen-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 40 mm x 1 1/4" - 75276 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-40-mm-x-1-1-4 |
| OK | FIT-stutzen-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 63 mm x 2" - 75280 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-63-mm-x-2 |
| OK | FIT-t-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 110 mm - 75050 | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-110-mm |
| OK | FIT-t-d110 | 2 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 110 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-110-mm-glue-socket-16bar-grey-kiwa-7002499 |
| OK | FIT-t-d20 | 1 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 20 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-20-mm-glue-socket-16bar-grey-kiwa-7002487 |
| OK | FIT-t-d20 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 20 mm - 75042 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-20-mm |
| OK | FIT-t-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 25 mm - 75043 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-25-mm |
| OK | FIT-t-d25 | 2 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 25 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-25-mm-glue-socket-16bar-grey-kiwa-7002488 |
| OK | FIT-t-d32 | 1 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 32 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-32-mm-glue-socket-16bar-grey-kiwa-7002489 |
| OK | FIT-t-d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 32 mm - 75044 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-32-mm |
| OK | FIT-t-d40 | 1 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 40 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-40-mm-glue-socket-16bar-grey-kiwa-7002491 |
| OK | FIT-t-d40 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 40 mm - 75045 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-40-mm |
| OK | FIT-t-d50 | 1 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 50 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-50-mm-glue-socket-16bar-grey-kiwa-7002493 |
| OK | FIT-t-d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 50 mm - 75046 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-50-mm |
| OK | FIT-t-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 63 mm - 75047 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-63-mm |
| OK | FIT-t-d63 | 2 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 63 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-63-mm-glue-socket-16bar-grey-kiwa-7002495 |
| OK | FIT-t-d75 | 1 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-75-mm-glue-socket-16bar-grey-kiwa-7002497 |
| OK | FIT-t-d75 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 75 mm - 75048 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-75-mm |
| OK | FIT-verschraubung-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Rohrverschraubung 50 mm (2 1/4") - 75036 | https://www.schwarte-shop.de/pvc-u-klebefitting-rohrverschraubung-50-mm-2-1-4 |
| OK | FIT-verschraubung-d50 | 2 | voelkner (Marktplatz-Anbieter  | 200 | HTTP 200 | PVC - U Verschraubung Klebemuffe x Klebemuffe 50 mm / » Freu | https://www.voelkner.de/products/12814009/PVC-U-Verschraubung-Klebemuffe-x-Klebemuffe-50-mm.html |
| OK | ROH-pvcu-d110 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 110 mm x 6,6 mm glue socket x plain 16ba | https://www.bevo.com/en/pressure-pipe-pvc-u-110-mm-x-6-6-mm-glue-socket-x-plain-16bar-iso-pn16-grey-5m-0309233 |
| OK | ROH-pvcu-d160 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 160 mm x 4,7 mm glue socket x plain 7,5b | https://www.bevo.com/en/pressure-pipe-pvc-u-160-mm-x-4-7-mm-glue-socket-x-plain-7-5bar-grey-5m-0309003 |
| OK | ROH-pvcu-d20 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 20 mm x 1,5 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-20-mm-x-1-5-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329121 |
| OK | ROH-pvcu-d25 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| OK | ROH-pvcu-d32 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 32 mm x 2,4 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-32-mm-x-2-4-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329133 |
| OK | ROH-pvcu-d40 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 40 mm x 3,0 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-40-mm-x-3-0-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329141 |
| OK | ROH-pvcu-d50 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 50 mm x 3,7 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-50-mm-x-3-7-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0309229 |
| OK | ROH-pvcu-d63 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 63 mm x 4,7 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-63-mm-x-4-7-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0309159 |
| OK | ROH-pvcu-d63 | 2 | Bosta (Bevo-Schwester) | 200 | HTTP 200 | Pressure pipe PVC-U 63 mm x 4,7 mm plain ISO-PN16 transparen | https://acc.bosta.com/en-ie/pressure-pipe-pvc-u-63-mm-x-4-7-mm-plain-iso-pn16-transparent-5m-0340030 |
| OK | ROH-pvcu-d75 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 75 mm x 5,6 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-75-mm-x-5-6-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-7018027 |
| OK | SCH-rohrschelle-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | Fischer Rohrschelle FRS 1/2" (20-24 mm), verzinkt - 20013 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-1-2-20-24-mm |
| OK | SCH-rohrschelle-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | Fischer Rohrschelle FRS 3/4" (25-30 mm), verzinkt - 20014 | https://www.schwarte-shop.de/zweischrauben-schellen-verzinkt-3-4-25-30-mm |
| OK | SCH-rohrschelle-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | Fischer Rohrschelle FRS 1" (32-37 mm), verzinkt - 20015 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-1-32-37-mm |
| OK | SCH-rohrschelle-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | Fischer Rohrschelle FRS 1 1/4" (40-45 mm), verzinkt - 20144 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-dn32-1-1-4-40-45-mm |
| OK | SCH-schlauchschelle-id25 | 1 | Schwarte-Shop | 200 | HTTP 200 | ASW Schlauchschelle W4 Edelstahl 16-25 mm, Bandbreite 9 mm | https://www.schwarte-shop.de/schlauchschelle-edelstahl-w4-bandbreite-9mm-spannbereich-16-25-mm-3-4 |
| OK | SCH-schlauchtuelle-d12 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Druckschlauchtülle 12 mm - 75147 | https://www.schwarte-shop.de/pvc-u-klebefitting-druckschlauchtuelle-12-mm |
| OK | SCH-schlauchtuelle-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Druckschlauchtülle 25 mm - 75150 | https://www.schwarte-shop.de/pvc-u-klebefitting-druckschlauchtuelle-25-mm |
| OK | ELE-hutschiene-35 | 1 | elektromax24 (OBO 2069 2M, gel | 200 | HTTP 200 | OBO Hutschiene gelocht 2000x35x7,5 St GTP 2069 2M GTPL / ele | https://www.elektromax24.de/2m-obo-2069-2m-gtpl-hutschiene-gelocht-2000x35x7-5-st-gtp |
| OK | ELE-kabelkanal-30x60 | 1 | zaehlerschrank24 (Hager LF3006 | 200 | HTTP 200 | ᐅ Hager Kabelkanal /30x60mm /verkehrsweiß kaufen | https://www.zaehlerschrank24.de/hager-kabelkanal-lf3006009016-pvc-30x60-mm-verkehrsweiss.html |
| OK | ELE-kabelkanal-30x60 | 2 | el12.com (Hager LF3006009016) | 200 | HTTP 200 | PVC wiring trunking 30x60mm white / el12 | https://el12.com/en/running-cables-and-wires/pvc-kabelkanal-30x60mm-weiss-lf3006009016,i428060 |
| OK | ELE-kabelverschraubung-pg | 2 | el12 (HAUPA 250086, M20 IP68 s | 200 | HTTP 200 | Gland M 20 metric IP 68 black 10 pcs / el12 | https://el12.com/en/switchboards-and-enclosures/gland-m-20-metric-ip-68-black-10-pcs-250086,i207068 |
| OK | MES-temperatur | 1 | Annahme: wie MES-temp-ds (DS18 | 200 | HTTP 200 | Temperatuur sensor digitaal 1-wire dallas waterdicht DS18B20 | https://domoticx.net/webshop/temperatuur-sensor-digitaal-1-wire-dallas-waterdicht-ds18b20-2m-kabel/ |
| OK | PRF-alu-haut-profil | 2 | Hornbach | 200 | HTTP 200 | U-Profil Alu 20x20x1,5 mm, 2 m / HORNBACH | https://www.hornbach.de/p/u-profil-alu-20x20x1-5-mm-2-m/6368193/ |
| OK | PRF-alu-klemmleiste | 2 | Hornbach | 200 | HTTP 200 | Flachstange Alu natur 30x2 mm, 2 m / HORNBACH | https://www.hornbach.de/p/flachstange-alu-natur-30x2-mm-2-m/757620/ |
| OK | PRF-st-rr25x25x2 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 25x25x2mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-25x25x2mm-1000mm |
| OK | PRF-st-rr30x30x2 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 30x30x2mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-30x30x2mm-1000mm |
| OK | PRF-st-rr40x40x2 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 40x40x2mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-40x40x2mm-1000mm |
| OK | PRF-st-rr40x40x3 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 40x40x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-40x40x3mm-1000mm |
| OK | PRF-st-rr40x40x3 | 2 | stahlshop.de (Krefeld) | 200 | HTTP 200 | verz. Vierkantstahlrohr 40 x 40 x 3,0 | https://stahlshop.de/verz-vierkantrohr-40-x-40-x-3-0-detail |
| OK | PRF-st-rr40x60x3 | 1 | stahl-shop24.de | 200 | HTTP 200 | Rechteckrohr Feuerverzinkt 60x40x3mm 1000mm | https://www.stahl-shop24.de/Rechteckrohr-Feuerverzinkt-60x40x3mm-1000mm |
| OK | PRF-st-rr60x60x3 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 60x60x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-60x60x3mm-1000mm |
| OK | PRF-st-rund20 | 1 | stahl-shop24.de | 200 | HTTP 200 | Rundstahl verzinkt 20mm 1000mm | https://www.stahl-shop24.de/Rundstahl-verzinkt-20mm-1000mm |
| OK | PRF-st-strebe30x30 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 30x30x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-30x30x3mm-1000mm |
| OK | PRF-v2a-voll8x8 | 1 | stahl-shop24.de | 200 | HTTP 200 | Edelstahl Vierkant 8x8mm 1000mm / 1000 mm / 8x8 mm / VVK102- | https://www.stahl-shop24.de/Edelstahl-Vierkant-8x8mm-1000mm |
| OK | PRF-v2a-voll8x8 | 2 | Metallshopper (NL-Fertigung, . | 200 | HTTP 200 | Edelstahl vollmaterial vierkant 8 mm | https://metallshopper.de/Edelstahl-vollmaterial-vierkant-8-mm |
| OK | SRB-satz-m10x60 | 1 | Schraubenking (schraubenking.a | 200 | HTTP 200 | M10 x 60mm Sechskantschrauben DIN 933 Vollgewinde Stahl verz | https://www.schraubenking.at/M10-x-60mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P000274 |
| OK | SRB-satz-m10x60 | 2 | Mister Agri | 200 | HTTP 200 | Zeskantbout M10x60 DIN 933 Verzinkt Staal 8.8 / Mister Agri | https://www.misteragri.com/it/51073987-zeskantbout-m10x60-din-933-verzinkt-staal-8-8 |
| OK | SRB-satz-m5x12 | 1 | Schraubenking (schraubenking.a | 200 | HTTP 200 | M5 x 12mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M5-x-12mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P003196 |
| OK | SRB-satz-m5x12 | 2 | Hornbach | 200 | HTTP 200 | Reyher Sechskantschraube o. Schaft DIN 933 M5x12 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m5x12-mm-galv-verzinkt-100-stueck/10316540/ |
| OK | SRB-satz-m6x16 | 1 | Schraubenking (schraubenking.a | 200 | HTTP 200 | M6 x 16mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M6-x-16mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P001093 |
| OK | SRB-satz-m6x16 | 2 | Hornbach | 200 | HTTP 200 | Reyher Sechskantschraube o. Schaft DIN 933 M6x16 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x16-mm-galv-verzinkt-100-stueck/10317081/ |
| OK | SRB-satz-m6x20 | 1 | Schraubenking (schraubenking.a | 200 | HTTP 200 | M6 x 20mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M6-x-20mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P001095 |
| OK | SRB-satz-m6x20 | 2 | Hornbach | 200 | HTTP 200 | Reyher Sechskantschraube o. Schaft DIN 933 M6x20 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x20-mm-galv-verzinkt-100-stueck/10317037/ |
| OK | SRB-satz-m6x40 | 1 | Schraubenking (schraubenking.a | 200 | HTTP 200 | M6 x 40mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M6-x-40mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P001100 |
| OK | SRB-satz-m6x40 | 2 | Hornbach | 200 | HTTP 200 | Reyher Sechskantschraube o. Schaft DIN 933 M6x40 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x40-mm-galv-verzinkt-100-stueck/10316704/ |
| OK | SRB-satz-m8x30 | 1 | Schraubenking (schraubenking.a | 200 | HTTP 200 | M8 x 30mm Sechskantschrauben DIN 933 Vollgewinde Stahl verzi | https://www.schraubenking.at/M8-x-30mm-Sechskantschrauben-DIN933-Vollgewinde-Stahl-verzinkt-FKL88-P001112 |
| OK | SRB-satz-m8x30 | 2 | Hornbach | 200 | HTTP 200 | Reyher Sechskantschraube o. Schaft DIN 933 M8x30 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m8x30-mm-galv-verzinkt-100-stueck/10316631/ |
| OK | WNK-flach-3mm-diagonale | 2 | stahl-shop24.de | 200 | HTTP 200 | Flachstahl verzinkt 30x3mm 1000mm | https://www.stahl-shop24.de/Flachstahl-verzinkt-30x3mm-1000mm |
| OK | WNK-flach-3mm-diagonale | 3 | Metallparadies (metallparadies | 200 | HTTP 200 | Flachstahl 20x3 mm bis 300x20 mm S235JR | https://www.metallparadies.de/stahl-flacheisen-s235jr-558.html |
| OK | WNK-pumpenkonsole | 1 | Hornbach | 200 | HTTP 200 | Schwerlast-Winkelverbinder m. Sicke 90 x 90 x 65 mm, / HORNB | https://www.hornbach.de/p/schwerlast-winkelverbinder-m-sicke-90-x-90-x-65-mm-sendzimirverzinkt-1-stueck/738910/ |
| OK | WNK-pumpenkonsole | 2 | Metallparadies (metallparadies | 200 | HTTP 200 | Winkelstahl 25x25x3 mm / Jetzt kaufen | https://www.metallparadies.de/winkelstahl-25x25x3-mm.html |
| OK | WNK-pumpenkonsole | 3 | Metallshopper (Metaalshopper) | 200 | HTTP 200 | Stahl Winkelprofil warmgewalzt 60x60x6 mm | https://www.metallshopper.de/p/stahl-winkelprofil-warmgewalzt-60x60x6-mm-384238/ |
| OK | MAT-epdm-teichfolie | 1 | Teichbedarf24 (TeichVision EPD | 200 | HTTP 200 | TeichVision EPDM pond liner Pro 1.5 mm - durable &amp; extra | https://teichbedarf24.de/en/products/epdm-teichfolie-teichvision-pro-1-5-mm |
| OK | PMP-luftpumpe-notluft | 1 | Hornbach (Marktplatz-Verkaeufe | 200 | HTTP 200 | Kerry Electronics Teichbelüfter 3600 L/H stufenlos / HORNBAC | https://www.hornbach.de/p/kerry-electronics-teichbeluefter-3600-l-h-stufenlos-regulierbar-35-watt-sauerstoffpumpe-fuer-teich-membranpumpe-60-l-min-teichbelueftung-luftpumpe-teich-beluefterpumpe-fuer-gartenteiche-teichbelueftungspumpe/12771855/ |
| OK | SCH-schlauch-id19 | 1 | OBI (obi.at, Fitt Glasklarschl | 200 | HTTP 200 | Fitt Glasklarschlauch Ø 19 mm Transparent kaufen bei OBI | https://www.obi.at/p/2573764/fitt-glasklarschlauch-19-mm-transparent |
| OK | SCH-schlauch-luft-d12 | 1 | OBI (JBL Aquarium-Schlauch gra | 200 | HTTP 200 | JBL Aquarienschlauch 9/12 mm Meterware kaufen bei OBI | https://www.obi.de/p/8485427/jbl-aquarium-schlauch-grau-9-12-mm-meterware |

## Plausibilitaet je Zeile

Lebensmittel: nur fuer Typen mit Wasser- oder Pflanzenkontakt (ROH, FIT, ARM, BEH, PMP, FOL, GEW, TOP, BLE, PRF, MES, SON); `belegt` = Bemerkung nennt Trinkwasser/Lebensmittel/KTW/W270/LFGB/1935/2004, sonst OFFEN. Europa nach Land des Hauptangebots (D76).

| Artikel | Bezeichnung | Datei | Mass | Einheit | Werkstoff | Lebensmittel | Europa | Konfidenz | Ersatz | Bedarf |
|---|---|---|---|---|---|---|---|---|---|---|
| ARM-bulkhead-d50 | PVC-U-Bulkhead d50 (Tankverbinder, Tankdurchfuehru | - | durchmesser_mm=50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-kugelhahn-feder_d40 | PVC-U-Kugelhahn feder_d40 | - | groesse=feder_d40 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-rsv-d50 | PVC-U-Rueckschlagventil d50 | - | groesse=d50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-schwimmerventil-pool | Schwimmerventil Pool (Gehaeuse, Wangen, Hebelarm m | - | - | Stk | PP | OFFEN | - | - |  | 0.0 |
| BEH-biofilter-dritt-fass | Biofilter-Fass PE mit Lochplatte (Altbestand-Dritt | - | - | Stk | PE | OFFEN | - | - |  | 0.0 |
| BEH-pegelschacht-fass | Pegelschacht PE-HD-Fass mit Deckel (Altbestand, en | - | - | Stk | PE-HD | OFFEN | - | - |  | 0.0 |
| ELE-kabelverschraubung-m25 | Kabelverschraubung M25 (PA) | - | - | Stk | PA | - | - | - |  | 0.0 |
| FIT-sammler-d110 | Sammelleitung (Sammler) d110 | - | groesse=d110 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FOL-epdm-schelleneinlage-d75 | EPDM-Schelleneinlage d75 | - | - | Stk | EPDM | OFFEN | - | - |  | 0.0 |
| MAT-gitterrost-112x1096 | Gitterrost verzinkt 1096x112x20 mm (Rinnenabdeckun | - | - | Stk | Stahl verzinkt | - | - | - |  | 0.0 |
| MAT-gitterrost-112x1196 | Gitterrost verzinkt 1196x112x20 mm (Rinnenabdeckun | - | - | Stk | Stahl verzinkt | - | - | - |  | 0.0 |
| MES-schwimmerschalter | Schwimmerschalter (Niveau AUS/EIN/ALARM, Fabrikat  | - | - | Stk | - | OFFEN | - | - |  | 0.0 |
| PRF-st-rr35x600x0.5 | Rechteckrohr 35x600x0.5 mm, Stahl verzinkt | - | querschnitt_mm=[35, 600], norm_hinweis=W | m | Stahl verzinkt | OFFEN | - | - |  | 0.0 |
| PRF-st-rr42x109x1 | Rechteckrohr 42x109x1 mm, Stahl verzinkt | - | querschnitt_mm=[42, 109], norm_hinweis=W | m | Stahl verzinkt | OFFEN | - | - |  | 0.0 |
| PRF-st-rr42x118x1 | Rechteckrohr 42x118x1 mm, Stahl verzinkt | - | querschnitt_mm=[42, 118], norm_hinweis=W | m | Stahl verzinkt | OFFEN | - | - |  | 0.0 |
| SCH-schlauch-d50 | Schlauch D50 (Meterware) | - | nennweite=d50 | m | PVC/PE | - | - | - |  | 0.0 |
| SON-bodenrinne-pp-1100 | Bodenrinne PP 120x162x1100 (Laufgang-Entwaesserung | - | - | Stk | PP | OFFEN | - | - |  | 0.0 |
| SON-bodenrinne-pp-1200 | Bodenrinne PP 120x162x1200 (Laufgang-Entwaesserung | - | - | Stk | PP | OFFEN | - | - |  | 0.0 |
| SON-ruecklaufrinne-v2a-2000 | Ruecklaufrinne Edelstahl 55x103x2000 (Altbestand)  | - | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| SON-stahlteil-60x416x416 | Stahlteil 60x416x416 mm (Eigenbau/Zuschnitt, Stahl | - | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 0.0 |
| SON-stahlteil-80x118x160 | Stahlteil 80x118x160 mm (Eigenbau/Zuschnitt, Stahl | - | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 0.0 |
| SRB-gewindestange-m17x110 | Gewindestange M17x110, verzinkt | - | - | Stk | Stahl verzinkt | - | - | - |  | 0.0 |
| BEH-ak-kompositbehaelter-254x790 | Aktivkohle-Druckbehaelter Komposit 254x790 mm mit  | behaelter.json | bbox_mm=[254, 254, 790] | Stk | Komposit | OFFEN | - | - |  | 2.0 |
| BEH-ak-sedimentfilter | Sedimentfilter-Set (Gehaeuse, Kopf, Patrone) [A] | behaelter.json | - | Satz | PP | OFFEN | ja | Q |  | 1.0 |
| BEH-becken-dritt | Drittbecken (Eigenbau/Sonderanfertigung, Masse aus | behaelter.json | bbox_mm=[1150, 1150, 1265] | Stk | - | OFFEN | - | - |  | 0.0 |
| BEH-drittbecken-klein | Drittbecken klein (Wanne 920x920x1055) | behaelter.json | bbox_mm=[1000, 1120, 1120] | Stk | Beton | belegt | ja | E | ERSATZ | 1.0 |
| BEH-fass-hdpe | HDPE-Fass 500 mm (Mischfass) | behaelter.json | - | Stk | HDPE blau | belegt | ja | Q |  | 1.0 |
| BEH-feinfilter-pp-630x440x610 | Feinfilter-Behaelter PP 630x440x610 (Eigenbau/Kauf | behaelter.json | - | Stk | PP | OFFEN | - | - |  | 0.0 |
| BEH-halter-box-gehaeuse | Anschlussbox PS 200x150x100 mit Acryldeckel | behaelter.json | - | Stk | PS/Acryl | OFFEN | ja | Q |  | 0.0 |
| BEH-ibc-1000l | IBC-Container 1000 l mit Gitterkaefig und Palette  | behaelter.json | volumen_l=1000 | Stk | PE/Stahl/HDPE | belegt | ja | Q |  | 0.0 |
| BEH-ibc-beetwanne | IBC-Beetwanne HDPE (aus IBC geschnitten, Laenge je | behaelter.json | bbox_mm=[460, 800, 2640] | Stk | HDPE weiss | belegt | ja | Q |  | 14.0 |
| BEH-kanister-hdpe | HDPE-Kanister (Dosiervorrat) | behaelter.json | - | Stk | HDPE | belegt | ja | E |  | 1.0 |
| BEH-messbecher-pp | Messbecher PP 160x310 | behaelter.json | - | Stk | PP | OFFEN | ja | Q |  | 0.0 |
| BEH-messzelle-acryl | Messzelle Acryl 315x315x260 | behaelter.json | - | Stk | Acryl klar | OFFEN | - | - |  | 1.0 |
| BEH-pe-schachtaufsatz-600x200 | PE-Schachtaufsatz (Dom) Oe 600 x 200 mm fuer Tank  | behaelter.json | bbox_mm=[200, 600, 600] | Stk | PE | OFFEN | - | - |  | 0.0 |
| BEH-pool-zentral | Zentralpool (Eigenbau/Sonderanfertigung, Masse aus | behaelter.json | bbox_mm=[2475, 4190, 4190] | Stk | - | OFFEN | - | - |  | 1.0 |
| BEH-tank-pe-580-deckel | PE-Tankdeckel 580 mm | behaelter.json | - | Stk | PE | OFFEN | - | - |  | 0.0 |
| BEH-tank-pe-580x865 | PE-Tank 580 mm Durchm., 865 mm hoch (Kegelboden/Ab | behaelter.json | bbox_mm=[580, 580, 865] | Stk | PE | belegt | ja | Q |  | 0.0 |
| BEH-tank-pe-673-deckel | PE-Tankdeckel 673 mm | behaelter.json | - | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-tank-pe-673x1075 | PE-Tank 673 mm Durchm., 1075 mm hoch (Kegelboden/A | behaelter.json | bbox_mm=[673, 673, 1075] | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-tank-pe-700-deckel | PE-Tankdeckel 700 mm | behaelter.json | - | Stk | PE | OFFEN | - | - |  | 0.0 |
| BEH-tank-pe-800x1000 | PE-Tank 800 mm Durchm., 1000 mm hoch (Kegelboden/A | behaelter.json | bbox_mm=[800, 800, 1000] | Stk | PE | OFFEN | - | - |  | 0.0 |
| BEH-tank-pe-930-deckel | PE-Tankdeckel 930 mm | behaelter.json | - | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-tank-pe-930x1444 | PE-Tank 930 mm Durchm., 1444 mm hoch (Kegelboden/A | behaelter.json | bbox_mm=[930, 930, 1444] | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-zweitbecken | Zweitbecken (Eigenbau/Sonderanfertigung, Masse aus | behaelter.json | bbox_mm=[1135, 1867, 1867] | Stk | - | OFFEN | - | - |  | 1.0 |
| PMP-dosierpumpe | Dosierpumpe (Schlauchpumpe) | behaelter.json | - | Stk | - | OFFEN | - | - |  | 1.0 |
| PMP-geblaese-luft | Membrangeblaese Luft (Leistung offen, Bauteilblatt | behaelter.json | bbox_mm=[180, 230, 240] | Stk | - | OFFEN | ja | E |  | 2.0 |
| PMP-pumpe-gross | Kreiselpumpe gross | behaelter.json | - | Stk | - | OFFEN | ja | Q |  | 0.0 |
| PMP-pumpe-klein | Kreiselpumpe klein | behaelter.json | - | Stk | - | OFFEN | ja | Q |  | 0.0 |
| PMP-teichpumpe-5300 | Teichpumpe 5300 l/h, 60 W, Hmax 2,8 m (Beet-Sumpf, | behaelter.json | - | Stk | - | OFFEN | ja | Q |  | 0.0 |
| SON-ak-konsole | Konsole Sedimentfilter (Stahl, Eigenbau) [A] | behaelter.json | - | Stk | Stahl | OFFEN | - | - |  | 1.0 |
| SON-gummifuss-40 | Gummifuss 40x40x15 | behaelter.json | - | Stk | Gummi | OFFEN | - | - |  | 8.0 |
| SON-luftverteiler-4 | Luftverteiler 4-fach (PVC, Eigenbau) [A] | behaelter.json | bbox_mm=[48, 98, 470] | Stk | PVC | OFFEN | - | - |  | 2.0 |
| SON-luftverteiler-6 | Luftverteiler 6-fach (PVC, Eigenbau) [A] | behaelter.json | bbox_mm=[48, 98, 710] | Stk | PVC | OFFEN | - | - |  | 0.0 |
| SON-scheibenbelueftung-270 | Scheibenbelueftung d270 (Tragteller, Stuetzfuss, E | behaelter.json | - | Stk | PP/EPDM | OFFEN | - | - |  | 4.0 |
| TOP-aktivkohle | Aktivkohle-Granulat (Behaelterfuellung) | behaelter.json | - | m3 | Aktivkohle | OFFEN | - | - |  | 0.04 |
| FOL-epdm-dichtband-zarge | EPDM-Dichtband Zarge | huelle_pflanze.json | - | m | EPDM | OFFEN | - | - |  | 0.0 |
| FOL-epdm-dichtung-630x440 | EPDM-Flachdichtung 630x440x3 | huelle_pflanze.json | - | Stk | EPDM | OFFEN | ja | Q |  | 0.0 |
| FOL-epdm-schaumband | EPDM-Schaumband 25x3 | huelle_pflanze.json | - | m | EPDM | OFFEN | ja | Q-Treffer |  | 0.0 |
| FOL-epdm-tuerdichtung | EPDM-Tuerdichtung | huelle_pflanze.json | - | m | EPDM | OFFEN | ja | Q |  | 5.99 |
| FOL-pe-plane | PE-Planenbahn (Huelle, Zuschnitt je Feld, Flaeche  | huelle_pflanze.json | - | m2 | PE Folie | OFFEN | ja | Q |  | 1015.84 |
| GEW-v2a-100um | Edelstahl-Siebgewebe 100 um, 1.4301 (Siebkorb, Fla | huelle_pflanze.json | maschenweite_um=100 | m2 | Edelstahl 1.4301 | OFFEN | - | - |  | 0.0 |
| SON-ankergabel-80x140 | Gabelkopf 80x140 (Fundamentanker, Stahl, Zuschnitt | huelle_pflanze.json | - | Stk | Stahl Anker | OFFEN | - | - |  | 20.0 |
| SON-ankerlasche | Ankerlasche am Knoten (Stahl, Zuschnitt) | huelle_pflanze.json | - | Stk | Stahl Knoten | OFFEN | - | - |  | 0.0 |
| SON-belueftungsgitter-460 | Belueftungsgitter 460x460 (PVC, Tankdeckel) | huelle_pflanze.json | - | Stk | PVC grau Tank | OFFEN | - | - |  | 2.0 |
| SON-federdraht-d2 | Federstahldraht d2 (Keilschiene) | huelle_pflanze.json | - | m | Federstahl | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d32-sensorblock | Sensorblock (halter_inline_d32, Eigenbau aus PVC-U | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d32-sieb | Sieb halter_inline_d32 (Edelstahl) | huelle_pflanze.json | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d32-vorfilter | Vorfilter (halter_inline_d32, Eigenbau aus PVC-U) | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d50-sensorblock | Sensorblock (halter_inline_d50, Eigenbau aus PVC-U | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d50-sieb | Sieb halter_inline_d50 (Edelstahl) | huelle_pflanze.json | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d50-vorfilter | Vorfilter (halter_inline_d50, Eigenbau aus PVC-U) | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-zelle-zellkoerper | Zellkoerper (halter_zelle, Eigenbau aus PVC-U) | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-holz-stuetzrippe | Stuetzrippe Fichte (Tank-Auflage) | huelle_pflanze.json | - | Stk | Holz Fichte | OFFEN | - | - |  | 10.0 |
| SON-knotenarm-23x23x3 | Steckarm 23x23x3 am Knoten (Verbindungsstueck, N-S | huelle_pflanze.json | - | Stk | Stahl Knoten | OFFEN | - | - |  | 0.0 |
| SON-knotenkugel-d100 | Knotenkugel d100, Stahl (Verbindungsstueck, N-STAT | huelle_pflanze.json | - | Stk | Stahl Knoten | OFFEN | - | - |  | 0.0 |
| SON-korbgriff-v2a | Korbgriff Edelstahl (Eigenbau) | huelle_pflanze.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | Q |  | 0.0 |
| SON-pflanztisch-platte | Pflanztischplatte (Alt-Modell, nicht verbaut) | huelle_pflanze.json | - | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-plattform-619x619 | Tankplattform 619x619x73 (Stahl, Eigenbau) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 2.0 |
| SON-plattform-821x821 | Tankplattform 821x821x98 (Stahl, Eigenbau) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 2.0 |
| SON-polycarbonat-paneel | Polycarbonat-Paneel 8 mm (Zuschnitt je Feld) | huelle_pflanze.json | dicke_mm=8 | Stk | Polycarbonat | OFFEN | - | - |  | 0.0 |
| SON-pp-stuetze-60x60 | PP-Stuetze 60x60 (Beetboden, Hoehe je Beet) | huelle_pflanze.json | - | Stk | PP grau | OFFEN | - | - |  | 274.0 |
| SON-schacht-kugelhahn-d63 | Schacht fuer Kugelhahn (PE-HD) d63 | huelle_pflanze.json | groesse=d63 | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-sondenhalter-36 | Sondenhalter 36x36x40 (PVC, Eigenbau/Stuetze) | huelle_pflanze.json | - | Stk | Kanal PVC | OFFEN | - | - |  | 0.0 |
| SON-spannverschluss-edelstahl | Spannverschluss Edelstahl (Bock + Hebel) | huelle_pflanze.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | Q |  | 0.0 |
| SON-strahlungsschutz-par | Strahlungsschutz PP weiss (Messmast) | huelle_pflanze.json | - | Stk | PP weiss | OFFEN | - | - |  | 0.0 |
| SON-tanksieb-stahl | Sieb am Tank (Stahl verzinkt, Zulauf/Auslauf) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 4.0 |
| SON-tauchklemme | Klemme Tauchrohr (Stahl, Eigenbau) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 3.0 |
| SON-tuer-modellvariante | Tuer (Alt-Modell, nicht verbaut) T4_Pfosten_L | huelle_pflanze.json | - | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-tuerblatt-1000x2000 | Tuerblatt Sandwich 1000x2000x40 | huelle_pflanze.json | - | Stk | Tuerblatt Sandwich | OFFEN | ja | Q |  | 1.0 |
| SON-tuerdruecker | Tuerdruecker mit Rosette | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 2.0 |
| SON-tuerscharnier | Tuerscharnier (Zargenlasche, Blattlasche, Bolzen) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 3.0 |
| SON-zarge-aufsatzrahmen | Alu-Aufsatzrahmen Tuerzarge (Planenausschnitt) | huelle_pflanze.json | - | Stk | Aluminium Zarge | OFFEN | - | - |  | 0.0 |
| TOP-biomedium | Biomedium (Biofilter-Fuellkoerper) | huelle_pflanze.json | - | m3 | Kunststoff | OFFEN | - | - |  | 1.29 |
| TOP-blaehton | Blaehton-Substrat 8-16 mm (Beetfuellung) | huelle_pflanze.json | - | m3 | Blaehton | OFFEN | ja | Q |  | 7.52 |
| TOP-netztopf-64 | Netztopf PP 64 mm (Pflanzkorb, Stueckzahl aus Inst | huelle_pflanze.json | durchmesser_mm=64 | Stk | PP | OFFEN | - | - |  | 2222.0 |
| ARM-anbohrschelle | Anbohrschelle PVC-U (Messstelle) | leitung.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-bulkhead-d63 | PVC-U-Bulkhead d63 (Tank-/Behaelterdurchfuehrung) | leitung.json | durchmesser_mm=63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-bulkhead-pool | Pool-Durchfuehrung d63 (Stutzen Pool-Wand) | leitung.json | durchmesser_mm=63 | Stk | PVC-U | OFFEN | ja | Q |  | 8.0 |
| ARM-kabeleinfuehrung-dn100 | Kabeleinfuehrung dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 1.0 |
| ARM-kabeleinfuehrung-dn50 | Kabeleinfuehrung dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 1.0 |
| ARM-kugelhahn-d110 | PVC-U-Kugelhahn d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-kugelhahn-d20 | PVC-U-Kugelhahn d20 | leitung.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | ja | Q |  | 1.0 |
| ARM-kugelhahn-d25 | PVC-U-Kugelhahn d25 | leitung.json | durchmesser_mm=25 | Stk | PVC-U | OFFEN | ja | Q |  | 42.0 |
| ARM-kugelhahn-d32 | PVC-U-Kugelhahn d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 24.0 |
| ARM-kugelhahn-d40 | PVC-U-Kugelhahn d40 | leitung.json | durchmesser_mm=40 | Stk | PVC-U | OFFEN | ja | Q |  | 18.0 |
| ARM-kugelhahn-d50 | PVC-U-Kugelhahn d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| ARM-kugelhahn-d63 | PVC-U-Kugelhahn d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 6.0 |
| ARM-rsv-d20 | PVC-U-Rueckschlagventil d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | - | - |  | 2.0 |
| ARM-rsv-d25 | PVC-U-Rueckschlagventil d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-rsv-d40 | PVC-U-Rueckschlagventil d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-bogen45-d110 | PVC-U-Bogen 45 Grad d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d20 | PVC-U-Bogen 45 Grad d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d25 | PVC-U-Bogen 45 Grad d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d32 | PVC-U-Bogen 45 Grad d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d40 | PVC-U-Bogen 45 Grad d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d50 | PVC-U-Bogen 45 Grad d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d63 | PVC-U-Bogen 45 Grad d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d75 | PVC-U-Bogen 45 Grad d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d110 | PVC-U-Bogen 90 Grad d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d20 | PVC-U-Bogen 90 Grad d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 26.0 |
| FIT-bogen90-d25 | PVC-U-Bogen 90 Grad d25 (Beet-Auslass) | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 26.0 |
| FIT-bogen90-d32 | PVC-U-Bogen 90 Grad d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d40 | PVC-U-Bogen 90 Grad d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d50 | PVC-U-Bogen 90 Grad d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 16.0 |
| FIT-bogen90-d63 | PVC-U-Bogen 90 Grad d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 11.0 |
| FIT-bogen90-d75 | PVC-U-Bogen 90 Grad d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q | ERSATZ | 0.0 |
| FIT-gewindenippel-edelstahl | Gewindenippel Edelstahl (Druckmessstelle) | leitung.json | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| FIT-kappe-d16 | PVC-U-Kappe d16 | leitung.json | durchmesser_mm=16 | Stk | PVC-U | OFFEN | ja | Q |  | 28.0 |
| FIT-kappe-d20 | PVC-U-Kappe d20 | leitung.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | ja | Q |  | 5.0 |
| FIT-kappe-d25 | PVC-U-Endkappe d25 | leitung.json | durchmesser_mm=25 | Stk | PVC-U | OFFEN | ja | Q |  | 24.0 |
| FIT-kappe-d32 | PVC-U-Kappe d32 | leitung.json | durchmesser_mm=32 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-kappe-d50 | PVC-U-Kappe d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 24.0 |
| FIT-kupplung-d110 | PVC-U-Kupplung (Muffe) d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d20 | PVC-U-Kupplung (Muffe) d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d25 | PVC-U-Kupplung (Muffe) d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 1.0 |
| FIT-kupplung-d32 | PVC-U-Kupplung (Muffe) d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d40 | PVC-U-Kupplung (Muffe) d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d50 | PVC-U-Kupplung (Muffe) d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d63 | PVC-U-Kupplung (Muffe) d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d75 | PVC-U-Kupplung (Muffe) d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-leerrohr-bogen45-dn100 | Leerrohr-Bogen 45 Grad dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-bogen45-dn50 | Leerrohr-Bogen 45 Grad dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-bogen90-dn100 | Leerrohr-Bogen 90 Grad dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 1.0 |
| FIT-leerrohr-bogen90-dn50 | Leerrohr-Bogen 90 Grad dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 1.0 |
| FIT-leerrohr-red-dn100_dn50 | Leerrohr-Reduzierung dn100_dn50 | leitung.json | groesse=dn100_dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-t-dn100 | Leerrohr-T-Stueck dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-t-dn50 | Leerrohr-T-Stueck dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-red-d110_d63 | PVC-U-Reduzierung d110_d63 | leitung.json | groesse=d110_d63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d25_d20 | PVC-U-Reduzierung d25_d20 | leitung.json | groesse=d25_d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d32_d25 | PVC-U-Reduzierung d32_d25 | leitung.json | groesse=d32_d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d40_d20 | PVC-U-Reduzierung d40_d20 | leitung.json | groesse=d40_d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d40_d32 | PVC-U-Reduzierung d40_d32 | leitung.json | groesse=d40_d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d50_d32 | PVC-U-Reduzierung d50_d32 | leitung.json | groesse=d50_d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d50_d40 | PVC-U-Reduzierung d50_d40 | leitung.json | groesse=d50_d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d63_d50 | PVC-U-Reduzierung d63_d50 | leitung.json | groesse=d63_d50 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d75_d50 | PVC-U-Reduzierung d75_d50 | leitung.json | groesse=d75_d50 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d75_d63 | PVC-U-Reduzierung d75_d63 | leitung.json | groesse=d75_d63 | Stk | PVC-U | OFFEN | ja | Q |  | 10.0 |
| FIT-rinne-kappe-ablauf | Rinnen-Endkappe Ablauf 130x100 | leitung.json | - | Stk | PVC-U weiss | OFFEN | - | - |  | 76.0 |
| FIT-rinne-kappe-zulauf | Rinnen-Endkappe Zulauf 130x100 | leitung.json | - | Stk | PVC-U weiss | OFFEN | - | - |  | 76.0 |
| FIT-stutzen-d16 | PVC-U-Stutzen d16 (Klebe/Gewinde) | leitung.json | durchmesser_mm=16 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| FIT-stutzen-d20 | PVC-U-Stutzen d20 (Klebe/Gewinde) | leitung.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| FIT-stutzen-d32 | PVC-U-Stutzen d32 (Klebe/Gewinde) | leitung.json | durchmesser_mm=32 | Stk | PVC-U | OFFEN | ja | Q |  | 9.0 |
| FIT-stutzen-d40 | PVC-U-Stutzen d40 (Klebe/Gewinde) | leitung.json | durchmesser_mm=40 | Stk | PVC-U | OFFEN | ja | Q |  | 6.0 |
| FIT-stutzen-d63 | PVC-U-Stutzen d63 (Klebe/Gewinde) | leitung.json | durchmesser_mm=63 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-t-d110 | PVC-U-T-Stueck d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d20 | PVC-U-T-Stueck d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d25 | PVC-U-T-Stueck d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 3.0 |
| FIT-t-d32 | PVC-U-T-Stueck d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d40 | PVC-U-T-Stueck d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d50 | PVC-U-T-Stueck d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d63 | PVC-U-T-Stueck d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d75 | PVC-U-T-Stueck d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 46.0 |
| FIT-uebergang-pe-pvc-pe_pvc_d20 | Uebergang PE auf PVC-U pe_pvc_d20 | leitung.json | groesse=pe_pvc_d20 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-verschraubung-d50 | PVC-U-Verschraubung (Rohrverbinder) | leitung.json | - | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-verschraubung-d75 | PVC-U-Verschraubung (Rohrverbinder) | leitung.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-verteiler-d25-nft | NFT-Verteiler d25 (Zulauf je Rinne, Laenge je Tisc | leitung.json | - | Stk | PVC blau | OFFEN | - | - |  | 24.0 |
| FIT-verteiler-d32_n2 | PVC-U-Verteiler d32_n2 | leitung.json | groesse=d32_n2 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-verteiler-d32_n3 | PVC-U-Verteiler d32_n3 | leitung.json | groesse=d32_n3 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-verteiler-d32_n4 | PVC-U-Verteiler d32_n4 | leitung.json | groesse=d32_n4 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-verteiler-d50 | PVC-U-Verteiler d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ROH-leerrohr-dn100 | Leerrohr DN100 (Kabelschutz, Meterware) | leitung.json | nennweite=dn100 | m | PVC/PP | OFFEN | ja | Q |  | 0.0 |
| ROH-leerrohr-dn50 | Leerrohr DN50 (Kabelschutz, Meterware) | leitung.json | nennweite=dn50 | m | PVC/PP | OFFEN | - | - |  | 0.0 |
| ROH-pvcu-d110 | PVC-U-Druckrohr d110 (Meterware) | leitung.json | durchmesser_mm=110 | m | PVC-U | OFFEN | ja | Q |  | 6.29 |
| ROH-pvcu-d16 | PVC-U-Druckrohr d16 (Meterware) | leitung.json | durchmesser_mm=16 | m | PVC-U | OFFEN | - | - |  | 2.54 |
| ROH-pvcu-d160 | PVC-U-Druckrohr d160 (Zulaufrohr, Meterware, Laeng | leitung.json | durchmesser_mm=160 | m | PVC-U | OFFEN | ja | Q |  | 4.4 |
| ROH-pvcu-d20 | PVC-U-Druckrohr d20 (Meterware) | leitung.json | durchmesser_mm=20 | m | PVC-U | OFFEN | ja | Q |  | 99.96 |
| ROH-pvcu-d25 | PVC-U-Druckrohr d25 (Meterware) | leitung.json | durchmesser_mm=25 | m | PVC-U | OFFEN | ja | Q |  | 38.13 |
| ROH-pvcu-d32 | PVC-U-Druckrohr d32 (Meterware) | leitung.json | durchmesser_mm=32 | m | PVC-U | OFFEN | ja | Q |  | 1.3 |
| ROH-pvcu-d40 | PVC-U-Druckrohr d40 (Meterware) | leitung.json | durchmesser_mm=40 | m | PVC-U | OFFEN | ja | Q |  | 3.87 |
| ROH-pvcu-d50 | PVC-U-Druckrohr d50 (Meterware) | leitung.json | durchmesser_mm=50 | m | PVC-U | OFFEN | ja | Q |  | 64.19 |
| ROH-pvcu-d63 | PVC-U-Druckrohr d63 (Meterware) | leitung.json | durchmesser_mm=63 | m | PVC-U | OFFEN | ja | Q |  | 30.23 |
| ROH-pvcu-d75 | PVC-U-Druckrohr d75 (Meterware) | leitung.json | durchmesser_mm=75 | m | PVC-U | OFFEN | ja | Q |  | 13.59 |
| SCH-rohrschelle-d110 | Rohrschelle (Klemme, Stahl) d110 | leitung.json | groesse=d110 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d20 | Rohrschelle (Klemme, Stahl) d20 | leitung.json | groesse=d20 | Stk | Stahl | - | ja | Q |  | 66.0 |
| SCH-rohrschelle-d25 | Rohrschelle (Klemme, Stahl) d25 | leitung.json | groesse=d25 | Stk | Stahl | - | ja | Q |  | 25.0 |
| SCH-rohrschelle-d32 | Rohrschelle (Klemme, Stahl) d32 | leitung.json | groesse=d32 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d40 | Rohrschelle (Klemme, Stahl) d40 | leitung.json | groesse=d40 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d50 | Rohrschelle (Klemme, Stahl) d50 | leitung.json | groesse=d50 | Stk | Stahl | - | ja | Q |  | 49.0 |
| SCH-rohrschelle-d63 | Rohrschelle d63 (Stahl verzinkt, Doppelschelle) | leitung.json | - | Stk | Stahl verzinkt | - | - | - |  | 30.0 |
| SCH-rohrschelle-vk-vk_d32 | Rohrschelle VK vk_d32 | leitung.json | groesse=vk_d32 | Stk | Stahl | - | - | - |  | 0.0 |
| SCH-rohrschelle-vk-vk_d63 | Rohrschelle VK vk_d63 | leitung.json | groesse=vk_d63 | Stk | Stahl | - | - | - |  | 0.0 |
| SCH-schlauch-id16 | Schlauch ID16 (Meterware) | leitung.json | nennweite=id16 | m | PVC/PE | - | - | - |  | 0.0 |
| SCH-schlauch-id25 | Schlauch ID25 (Meterware) | leitung.json | nennweite=id25 | m | PVC/PE | - | - | - |  | 321.93 |
| SCH-schlauch-rinne-id16 | Schlauch ID16, 110 mm Stueck (Rinne Zulauf) | leitung.json | - | Stk | PVC/PE | - | - | - |  | 76.0 |
| SCH-schlauchbogen90-id16 | Schlauchbogen 90 Grad id16 | leitung.json | groesse=id16 | Stk | Kunststoff | - | - | - |  | 0.0 |
| SCH-schlauchbogen90-id25 | Schlauchbogen 90 Grad id25 | leitung.json | groesse=id25 | Stk | Kunststoff | - | - | - |  | 0.0 |
| SCH-schlauchschelle-id16 | Schlauchschelle id16 | leitung.json | groesse=id16 | Stk | Kunststoff | - | ja | Q |  | 0.0 |
| SCH-schlauchschelle-id25 | Schlauchschelle id25 | leitung.json | groesse=id25 | Stk | Kunststoff | - | ja | Q |  | 0.0 |
| SCH-schlauchtuelle-d12 | Schlauchtuelle (PVC) | leitung.json | - | Stk | PVC | - | ja | Q |  | 15.0 |
| SCH-schlauchtuelle-d25 | Schlauchtuelle d25 (PVC) | leitung.json | - | Stk | PVC | - | ja | Q |  | 38.0 |
| BLE-schrankboden-3x500x800 | Stahlblech 3 mm, Zuschnitt 800x500 (Schrankboden)  | mess_elektrik.json | - | Stk | Stahl | OFFEN | - | - |  | 1.0 |
| ELE-hutschiene-35 | Hutschiene 35 mm | mess_elektrik.json | - | Stk | Stahl verzinkt | - | ja | Q-Treffer |  | 0.0 |
| ELE-kabelkanal-30x60 | Kabelkanal PVC 30x60 | mess_elektrik.json | - | m | PVC | - | ja | Q-Treffer |  | 0.0 |
| ELE-kabelverschraubung-pg | Kabelverschraubung PA (PG/M20) | mess_elektrik.json | - | Stk | PA schwarz | - | ja | Q |  | 1.0 |
| ELE-schaltschrank-500x800x1200 | Schaltschrank 500x800x1200 mm (leer, Ausruestung o | mess_elektrik.json | - | Stk | - | - | ja | Q |  | 1.0 |
| MES-co2-scd41 | Sonde co2_scd41 (Typ und Fabrikat offen: docs/rese | mess_elektrik.json | bbox_mm=[10, 17, 25] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-do-ind | Sonde do_ind (Typ und Fabrikat offen: docs/researc | mess_elektrik.json | bbox_mm=[25, 25, 170] | Stk | - | OFFEN | - | - |  | 1.0 |
| MES-do-mini | Sonde do_mini (Typ und Fabrikat offen: docs/resear | mess_elektrik.json | bbox_mm=[12, 12, 110] | Stk | - | OFFEN | ja | Q |  | 3.0 |
| MES-druck-schalter | Sonde druck_schalter (Typ und Fabrikat offen: docs | mess_elektrik.json | bbox_mm=[32, 32, 55] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-ec | Sonde EC (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | Q |  | 1.0 |
| MES-flow-12 | Sonde flow_12 (Typ und Fabrikat offen: docs/resear | mess_elektrik.json | bbox_mm=[40, 50, 80] | Stk | - | OFFEN | ja | Q-Treffer | ERSATZ | 0.0 |
| MES-flow-gross | Sonde flow_gross (Typ und Fabrikat offen: docs/res | mess_elektrik.json | bbox_mm=[40, 60, 100] | Stk | - | OFFEN | - | - |  | 0.0 |
| MES-leck | Sonde leck (Typ und Fabrikat offen: docs/research/ | mess_elektrik.json | bbox_mm=[6, 20, 50] | Stk | - | OFFEN | ja | Q |  | 3.0 |
| MES-level-druck | Sonde level_druck (Typ und Fabrikat offen: docs/re | mess_elektrik.json | bbox_mm=[20, 20, 140] | Stk | - | OFFEN | - | - |  | 1.0 |
| MES-level-float | Sonde level_float (Typ und Fabrikat offen: docs/re | mess_elektrik.json | bbox_mm=[30, 30, 55] | Stk | - | OFFEN | ja | Q |  | 3.0 |
| MES-o2 | Sonde O2 (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | A |  | 0.0 |
| MES-par | Sonde par (Typ und Fabrikat offen: docs/research/R | mess_elektrik.json | bbox_mm=[30, 30, 37] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-ph | Sonde pH (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | Q-Treffer |  | 3.0 |
| MES-strom-ct | Sonde strom_ct (Typ und Fabrikat offen: docs/resea | mess_elektrik.json | bbox_mm=[13, 30, 36] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-temp-ds | Sonde temp_ds (Typ und Fabrikat offen: docs/resear | mess_elektrik.json | bbox_mm=[6, 6, 50] | Stk | - | OFFEN | ja | Q |  | 2.0 |
| MES-temperatur | Sonde Temperatur (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | A |  | 0.0 |
| SON-schrankwand-500x800 | Schrankwand 500x800 (Eigenbau, Werkstoff offen) [A | mess_elektrik.json | - | Stk | Stahl | OFFEN | - | - |  | 1.0 |
| BLE-blech-st-3 | Stahlblech 3 mm verzinkt, Zuschnitt 700x700 | stahl.json | dicke_mm=3, zuschnitt_mm=[700, 700] | Stk | Stahl verzinkt | OFFEN | ja | Q | ERSATZ | 5.0 |
| BLE-blech-st-5 | Stahlblech 5 mm verzinkt, Zuschnitt 840x400 | stahl.json | dicke_mm=5, zuschnitt_mm=[840, 400] | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| BLE-blech-st-6 | Stahlblech 6 mm verzinkt, Zuschnitt 100x100 | stahl.json | dicke_mm=6, zuschnitt_mm=[100, 100] | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 56.0 |
| BLE-fussplatte-100x100x6 | Fussplatte Stahl verzinkt 100x100x6 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 32.0 |
| BLE-fussplatte-150x150x8 | Fussplatte Stahl verzinkt 150x150x8 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 0.0 |
| BLE-fussplatte-200x200x8 | Fussplatte Stahl verzinkt 200x200x8 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 0.0 |
| BLE-fussplatte-70x70x5 | Fussplatte Stahl verzinkt 70x70x5 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 76.0 |
| BLE-fussplatte-80x80x6 | Fussplatte Stahl verzinkt 80x80x6 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 4.0 |
| BLE-fussplatte-80x80x8 | Fussplatte Stahl verzinkt 80x80x8 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 0.0 |
| BLE-platte-250x250x15 | Ankerplatte 250x250x15 mm, Stahl | stahl.json | - | Stk | Stahl Anker | OFFEN | ja | E |  | 10.0 |
| BLE-pp-blende-290x260 | PP-Blende 290x260x3 (Messzelle) | stahl.json | - | Stk | PP schwarz | OFFEN | ja | E |  | 1.0 |
| BLE-pp-tafel-502x345x5 | PP-Montagetafel 502x345x5 (Zuschnitt) | stahl.json | - | Stk | PP Tafel | OFFEN | ja | E |  | 0.0 |
| BLE-pp-tafel-693x463x7 | PP-Montagetafel 693x463x7 (Zuschnitt) | stahl.json | - | Stk | PP Tafel | OFFEN | ja | E |  | 0.0 |
| BLE-v2a-3mm-korbflansch | Edelstahlblech 3 mm 1.4301, Zuschnitt 604x414 (Kor | stahl.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | Q |  | 0.0 |
| PRF-alu-haut-profil | Alu-Kappenprofil der Haut | stahl.json | - | m | Aluminium | OFFEN | ja | Q | ERSATZ | 0.0 |
| PRF-alu-keilschiene | Alu-Keilschiene (Kanal 25x15) | stahl.json | - | m | Aluminium | OFFEN | ja | Q |  | 0.0 |
| PRF-alu-klemmleiste | Alu-Klemmleiste Zarge | stahl.json | - | m | Aluminium Zarge | OFFEN | ja | Q |  | 0.0 |
| PRF-pvcu-rinne-130x100 | NFT-Rinnenprofil PVC-U 130x100 (Meterware, Lagerla | stahl.json | querschnitt_mm=[100, 130] | m | PVC-U weiss | OFFEN | ja | Q | ERSATZ | 147.92 |
| PRF-st-rr25x25x2 | Vierkantrohr 25x25x2 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[25, 25], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-rr30x30x2 | Vierkantrohr 30x30x2 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[30, 30], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 24.88 |
| PRF-st-rr40x40x2 | Vierkantrohr 40x40x2 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-rr40x40x2.5 | Vierkantrohr 40x40x2.5 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q | ERSATZ | 161.89 |
| PRF-st-rr40x40x3 | Vierkantrohr 40x40x3 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 40.8 |
| PRF-st-rr40x60x3 | Rechteckrohr 40x60x3 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 60], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 29.6 |
| PRF-st-rr60x60x3 | Vierkantrohr 60x60x3 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[60, 60], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-rund20 | Rundstahl 20 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[20, 20], norm_hinweis=Ru | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-strebe30x30 | Strebenprofil 30x30 (Kuppelstrebe, Profil und Wand | stahl.json | querschnitt_mm=[30, 30] | m | Stahl verzinkt | OFFEN | ja | Q |  | 211.45 |
| PRF-v2a-voll8x8 | Vierkant-/Flachstahl voll 8x8 mm, Edelstahl 1.4301 | stahl.json | querschnitt_mm=[8, 8], norm_hinweis=Voll | m | Edelstahl 1.4301 | OFFEN | ja | Q |  | 0.0 |
| SRB-halter-klein-12x10x20 | Kleinteil am Winkelhalter 12x10x20 (Schraube/Mutte | stahl.json | - | Stk | Stahl verzinkt | - | - | - |  | 456.0 |
| SRB-satz-m10x60 | Schraubensatz M10x60 (Sechskantschraube DIN 933 +  | stahl.json | gewinde=M10, laenge_mm=60 | Satz | Stahl verzinkt | - | ja | Q |  | 128.0 |
| SRB-satz-m12x55 | Schraubensatz M12x55 (Sechskantschraube DIN 933 +  | stahl.json | gewinde=M12, laenge_mm=55 | Satz | Stahl verzinkt | - | - | - |  | 10.0 |
| SRB-satz-m16x300 | Schraubensatz M16x300 (Sechskantschraube DIN 933 + | stahl.json | gewinde=M16, laenge_mm=300 | Satz | Stahl verzinkt | - | - | - |  | 20.0 |
| SRB-satz-m5x12 | Schraubensatz M5x12 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M5, laenge_mm=12 | Satz | Stahl verzinkt | - | ja | Q |  | 304.0 |
| SRB-satz-m6x16 | Schraubensatz M6x16 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M6, laenge_mm=16 | Satz | Stahl verzinkt | - | ja | Q |  | 0.0 |
| SRB-satz-m6x20 | Schraubensatz M6x20 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M6, laenge_mm=20 | Satz | Stahl verzinkt | - | ja | Q |  | 0.0 |
| SRB-satz-m6x40 | Schraubensatz M6x40 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M6, laenge_mm=40 | Satz | Stahl verzinkt | - | ja | Q |  | 112.0 |
| SRB-satz-m6x55 | Schraubensatz M6x55 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M6, laenge_mm=55 | Satz | Stahl verzinkt | - | ja | Q | ERSATZ | 0.0 |
| SRB-satz-m8x30 | Schraubensatz M8x30 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M8, laenge_mm=30 | Satz | Stahl verzinkt | - | ja | Q |  | 312.0 |
| WNK-flach-14x3 | Flachstahl 14x3 (Tuer-Anschlag) | stahl.json | - | m | Stahl verzinkt | - | ja | Q | ERSATZ | 5.0 |
| WNK-flach-3mm-diagonale | Flachstahl 3 mm (Diagonalen, Breite aus Modell nic | stahl.json | dicke_mm=3 | Stk | Stahl verzinkt | - | - | - |  | 110.0 |
| WNK-pumpenkonsole | Pumpenkonsole/Standwinkel (Stahl, Zuschnitt) | stahl.json | - | Stk | Stahl Pumpe | - | ja | A |  | 0.0 |
| WNK-rinnenhalter-25 | Rinnenhalter 25x25 (Stahl, Zuschnitt/Kleinteil) | stahl.json | - | Stk | Stahl verzinkt | - | ja | Q | ERSATZ | 304.0 |
| WNK-wandlasche-30x30x3 | Wandlasche 30x30x3 | stahl.json | - | Stk | Stahl verzinkt | - | ja | E | ERSATZ | 0.0 |
| WNK-winkel-36x60x60 | Winkel 36x60x60 (Rinnen-Winkelhalter, Stahl) | stahl.json | - | Stk | Stahl verzinkt | - | ja | Q |  | 76.0 |
| ARM-luftstein-notluft | Luftausstroemer (Luftstein) | u2_wasserkreislauf.json | - | Stk | PE | OFFEN | - | - |  | 1.0 |
| ARM-rueckschlagventil-d50 | PVC-U-Rueckschlagventil d50 (Klebemuffe) | u2_wasserkreislauf.json | groesse=d50 | Stk | PVC-U | OFFEN | - | - |  | 4.0 |
| ARM-rueckschlagventil-luft | Rueckschlagventil Luft (Schlauch) | u2_wasserkreislauf.json | - | Stk | PP | OFFEN | - | - |  | 3.0 |
| ARM-schwimmerschalter-hochstand | Schwimmerschalter Hochstand (Fabrikat offen) [A] | u2_wasserkreislauf.json | - | Stk | - | OFFEN | - | - |  | 2.0 |
| ARM-schwimmerventil-nachspeise | Schwimmerventil 3/4 Zoll (Nachspeisung, Gehaeuse,  | u2_wasserkreislauf.json | - | Stk | PP | OFFEN | - | - |  | 2.0 |
| ARM-venturi-mazzei-1583 | Venturi-Injektor | u2_wasserkreislauf.json | - | Stk | PP | OFFEN | - | - |  | 2.0 |
| BEH-regentank-5000 | Regenwassertank 5000 l, stehend, oberirdisch (PE) | u2_wasserkreislauf.json | volumen_l=5000 | Stk | PE | OFFEN | - | - |  | 1.0 |
| BEH-schlammbehaelter-350 | Schlamm-Sammelbehaelter PE rund 350 l mit Deckel ( | u2_wasserkreislauf.json | volumen_l=350 | Stk | PE | belegt | ja | Q-Treffer |  | 2.0 |
| MAT-epdm-teichfolie | EPDM-Teichfolie 1,5 mm (Grubenauskleidung, Flaeche | u2_wasserkreislauf.json | - | m2 | EPDM | - | ja | Q-Treffer |  | 14.32 |
| MAT-gitterrost-deckel | Begehbarer Gitterrost 30/10 feuerverzinkt 1229 x 1 | u2_wasserkreislauf.json | bbox_mm=[40, 1026, 1229] | Stk | Stahl verzinkt | - | - | - |  | 6.0 |
| PMP-luftpumpe-notluft | Notluftpumpe (Membranpumpe, Akku/Netz) [A] | u2_wasserkreislauf.json | bbox_mm=[230, 320, 330] | Stk | - | OFFEN | ja | Q |  | 1.0 |
| PMP-tauchpumpe-oase-8000 | Tauchpumpe (Klasse Oase AquaMax Eco Premium 8000,  | u2_wasserkreislauf.json | bbox_mm=[165, 280, 340] | Stk | - | OFFEN | ja | Q |  | 4.0 |
| ARM-bulkhead-d20 | PVC-U-Bulkhead d20 | u8_unify.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | - | - |  | 14.0 |
| ARM-durchflussbegrenzer-messing | Durchflussbegrenzer Messing [A] | u8_unify.json | - | Stk | Messing | OFFEN | - | - |  | 1.0 |
| ARM-entlueftungsventil-messing | Be-/Entlueftungsventil Messing (Rohrleitung, 1 1/2 | u8_unify.json | - | Stk | Messing | OFFEN | - | - |  | 2.0 |
| ARM-probehahn-messing | Probierhahn Messing 1/2 Zoll [A] | u8_unify.json | - | Stk | Messing | OFFEN | - | - |  | 1.0 |
| ARM-schnellkupplung-id19 | Schnellkupplung id19 | u8_unify.json | groesse=id19 | Stk | PVC-U | belegt | ja | Q |  | 26.0 |
| ARM-schnellkupplung-id25 | Schnellkupplung id25 | u8_unify.json | groesse=id25 | Stk | PVC-U | OFFEN | - | - |  | 12.0 |
| BEH-futterzuchtkiste-pe | Futterzuchtkiste PE 350x525x800 (Permakultur-Modul | u8_unify.json | bbox_mm=[350, 525, 800] | Stk | PE | OFFEN | - | - |  | 1.0 |
| BLE-blech-st-10 | Stahlblech 10 mm verzinkt, Zuschnitt 200x200 | u8_unify.json | dicke_mm=10, zuschnitt_mm=[200, 200] | Stk | Stahl verzinkt | OFFEN | - | - |  | 3.0 |
| BLE-blech-st-4 | Stahlblech 4 mm verzinkt, Zuschnitt 40x40 | u8_unify.json | dicke_mm=4, zuschnitt_mm=[40, 40] | Stk | Stahl verzinkt | OFFEN | - | - |  | 31.0 |
| BLE-blech-st-8 | Stahlblech 8 mm verzinkt, Zuschnitt 100x40 | u8_unify.json | dicke_mm=8, zuschnitt_mm=[100, 40] | Stk | Stahl verzinkt | OFFEN | - | - |  | 66.0 |
| BLE-laser-lochplatte-110x110x8 | Laserteil Lochplatte 110x110x8 mm, Stahl (Knoten S | u8_unify.json | - | Stk | Stahl Laserteil | OFFEN | - | - |  | 52.0 |
| BLE-pp-abtropfgitter-beet | PP-Abtropfgitter 25 mm (Stegrost, Zuschnitt je Bee | u8_unify.json | dicke_mm=25 | Stk | PP grau | OFFEN | - | - |  | 14.0 |
| BLE-pp-platte10-210x1125 | PP-Platte 10 mm, Zuschnitt 1125x210 (Trennwand, Pu | u8_unify.json | - | Stk | PP weiss | OFFEN | - | - |  | 4.0 |
| BLE-pp-platte10-360x1125 | PP-Platte 10 mm, Zuschnitt 1125x360 (Trennwand, Pu | u8_unify.json | - | Stk | PP weiss | OFFEN | - | - |  | 4.0 |
| BLE-pp-platte30-400x400 | PP-Platte 30 mm, Zuschnitt 400x400 (Pumpensockel) | u8_unify.json | - | Stk | PP grau | OFFEN | - | - |  | 2.0 |
| FIT-entlueftung-d32 | Entlueftung d32 (PVC-U, mit Insektengitter-Kappe)  | u8_unify.json | durchmesser_mm=32 | Stk | PVC-U | OFFEN | - | - |  | 2.0 |
| FIT-red-d32-d25 | PVC-U-Reduzierung d32 auf d25 | u8_unify.json | groesse=d32_d25 | Stk | PVC-U | OFFEN | - | - |  | 1.0 |
| FIT-red-d50-d32 | PVC-U-Reduzierung d50 auf d32 | u8_unify.json | groesse=d50_d32 | Stk | PVC-U | OFFEN | - | - |  | 24.0 |
| FIT-red-d50-d40 | PVC-U-Reduzierung d50 auf d40 | u8_unify.json | groesse=d50_d40 | Stk | PVC-U | OFFEN | - | - |  | 14.0 |
| FIT-red-d75-d50 | PVC-U-Reduzierung d75 auf d50 | u8_unify.json | groesse=d75_d50 | Stk | PVC-U | OFFEN | - | - |  | 38.0 |
| FIT-reduktion-d20 | PVC-U-Reduktion/Huelse d20 | u8_unify.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | - | - |  | 14.0 |
| FIT-ring-ecke-d75 | Ring-Ecke d75 (PE100, Segmentbogen/Formteil fuer d | u8_unify.json | durchmesser_mm=75 | Stk | PE100 | OFFEN | - | - |  | 10.0 |
| FIT-schlauchanschluss-abzweig | Schlauchanschluss am Abzweig (Gewinde/Klebe auf Sc | u8_unify.json | - | Stk | PVC/PP | OFFEN | - | - |  | 38.0 |
| FIT-schlauchwinkel-90 | Schlauch-Winkelstueck 90 Grad (PVC, Tuelle-Tuelle) | u8_unify.json | - | Stk | PVC | OFFEN | - | - |  | 31.0 |
| FIT-stutzen-d25 | PVC-U-Stutzen d25 (Klebe/Gewinde) | u8_unify.json | durchmesser_mm=25 | Stk | PVC-U | OFFEN | - | - |  | 4.0 |
| FIT-stutzen-d50 | PVC-U-Stutzen d50 (Klebe/Gewinde) | u8_unify.json | durchmesser_mm=50 | Stk | PVC-U | OFFEN | - | - |  | 6.0 |
| FIT-stutzen-d75 | PVC-U-Stutzen d75 (Klebe/Gewinde) | u8_unify.json | durchmesser_mm=75 | Stk | PVC-U | OFFEN | - | - |  | 1.0 |
| FIT-uebergangsnippel-d75-d40 | PVC-U-Uebergangsnippel d75 auf d40 | u8_unify.json | - | Stk | PVC-U | OFFEN | - | - |  | 2.0 |
| GEW-sieb-v2a-2mm | Edelstahl-Siebgewebe 2 mm (Beetsieb, Flaeche aus M | u8_unify.json | maschenweite_mm=2 | m2 | Edelstahl 1.4301 | OFFEN | - | - |  | 25.07 |
| GEW-vlies-pp | PP-Vlies (Beetboden, Flaeche aus Modell) | u8_unify.json | - | m2 | PP Vlies | OFFEN | - | - |  | 25.07 |
| PRF-st-rr20x40x2.5 | Rechteckrohr 20x40x2.5 mm, Stahl verzinkt | u8_unify.json | querschnitt_mm=[20, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | - | - |  | 10.84 |
| PRF-st-rr41x41x2 | Vierkantrohr 41x41x2 mm, Stahl verzinkt | u8_unify.json | querschnitt_mm=[41, 41], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | - | - |  | 21.79 |
| PRF-st-rr50x50x3 | Vierkantrohr 50x50x3 mm, Stahl verzinkt | u8_unify.json | querschnitt_mm=[50, 50], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | - | - |  | 5.08 |
| PRF-st-voll40x40 | Vierkant-/Flachstahl voll 40x40 mm, Stahl verzinkt | u8_unify.json | querschnitt_mm=[40, 40], norm_hinweis=Vo | m | Stahl verzinkt | OFFEN | - | - |  | 30.04 |
| PRF-st-voll6x100 | Vierkant-/Flachstahl voll 6x100 mm, Stahl verzinkt | u8_unify.json | querschnitt_mm=[6, 100], norm_hinweis=Vo | m | Stahl verzinkt | OFFEN | - | - |  | 3.2 |
| SCH-rohrschelle-d75 | Rohrschelle (Klemme, Stahl) d75 | u8_unify.json | groesse=d75 | Stk | Stahl | - | - | - |  | 20.0 |
| SCH-rohrschelle-d75_ecke | Rohrschelle (Klemme, Stahl) d75_ecke | u8_unify.json | groesse=d75_ecke | Stk | Stahl | - | - | - |  | 7.0 |
| SCH-rohrschelle-d75_stelze | Rohrschelle (Klemme, Stahl) d75_stelze | u8_unify.json | groesse=d75_stelze | Stk | Stahl | - | - | - |  | 3.0 |
| SCH-schlauch-id19 | Schlauch ID19 (Meterware, Laenge aus Modellmasse) | u8_unify.json | nennweite=id19 | m | PVC/PE | - | ja | Q-Treffer |  | 861.08 |
| SCH-schlauch-luft-d12 | Luftschlauch d12 (Meterware) | u8_unify.json | durchmesser_mm=12 | m | PVC | - | ja | Q-Treffer |  | 3.88 |
| SCH-schlauch-luft-d8 | Luftschlauch d8 (Meterware) | u8_unify.json | durchmesser_mm=8 | m | PVC | - | ja | Q-Treffer |  | 2.02 |
| SON-ausstroemer-stab-600 | Ausstroemer-Stab PP 16x600 (Beet-Belueftung) [A] | u8_unify.json | - | Stk | PP weiss | OFFEN | - | - |  | 14.0 |
| SON-laser-lasche-30x34x123 | Laserteil Lasche 30x34x123 mm, Stahl (Knoten Scher | u8_unify.json | - | Stk | Stahl Laserteil | OFFEN | - | - |  | 60.0 |
| SON-laser-lasche-30x34x125 | Laserteil Lasche 30x34x125 mm, Stahl (Knoten Scher | u8_unify.json | - | Stk | Stahl Laserteil | OFFEN | - | - |  | 60.0 |
| SON-laser-lasche-34x35x122 | Laserteil Lasche 34x35x122 mm, Stahl (Knoten Scher | u8_unify.json | - | Stk | Stahl Laserteil | OFFEN | - | - |  | 68.0 |
| SON-laser-lasche-34x36x124 | Laserteil Lasche 34x36x124 mm, Stahl (Knoten Scher | u8_unify.json | - | Stk | Stahl Laserteil | OFFEN | - | - |  | 68.0 |
| SON-luftfilter-ansaug | Ansaug-Luftfilter fuer den Venturi (PP) [A] | u8_unify.json | - | Stk | PP weiss | OFFEN | - | - |  | 2.0 |
| SON-permakultur-kompostbox | Kompostbox Fichte 525x600x1500 mit Deckel (Permaku | u8_unify.json | - | Stk | Holz Fichte | OFFEN | - | - |  | 1.0 |
| SON-pp-schwimmerhalter | Schwimmerhalter PP 40x60x80 (Eigenbau) | u8_unify.json | - | Stk | PP grau | OFFEN | - | - |  | 2.0 |
| SON-pp-zonenschild | Zonenschild PP 2x40x100 (Beschriftung Pufferzone) | u8_unify.json | - | Stk | PP weiss | OFFEN | - | - |  | 8.0 |
| SON-schlauchhalter-pp | Schlauchhalter PP (Clip) [A] | u8_unify.json | - | Stk | PP | OFFEN | - | - |  | 27.0 |
| SON-stahlteil-134x192x230 | Stahlteil 134x192x230 mm (Eigenbau/Zuschnitt, Stah | u8_unify.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 18.0 |
| SON-stahlteil-20x40x42 | Stahlteil 20x40x42 mm (Eigenbau/Zuschnitt, Stahl v | u8_unify.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 74.0 |
| SON-stahlteil-35x40x40 | Stahlteil 35x40x40 mm (Eigenbau/Zuschnitt, Stahl v | u8_unify.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 3.0 |
| SRB-gewindestange-m17x120 | Gewindestange M17x120, verzinkt | u8_unify.json | - | Stk | Stahl verzinkt | - | - | - |  | 12.0 |
| SRB-satz-m8x65 | Schraubensatz M8x65 (Sechskantschraube + Mutter +  | u8_unify.json | gewinde=M8 | Satz | Stahl verzinkt | - | - | - |  | 56.0 |
