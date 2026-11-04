# Preis-Pruefung: Link-Messlauf und Plausibilitaet (N-PREIS-PRUEF)

Erzeugt von `python -X utf8 scripts/check_links.py` aus `data/stueckliste.json`; Rohdaten `data/preis_pruefung_links.json`.
Nicht von Hand bearbeiten: neu erzeugen. Urteile: FEHLER (404/Netz/Weiterleitung auf Startseite, Suche, Kategorie), GESPERRT (Seite blockt Skripte, von Hand oeffnen), VERDACHT (Kennmass des Artikels fehlt auf der Seite oder steht nicht in Titel/URL, oder Bemerkung sagt ERSATZ), OK.

## Zahlen

- Zeilen der Stueckliste: 260; Zeilen mit mindestens einem Link: 172
- Links (Haupt- und Alternativangebote): 289; eindeutige URLs: 212
- FEHLER: 6
- GESPERRT: 32
- VERDACHT: 127
- OK: 124
- Zeilen ohne Link: 88
- Plausibilitaet: Lebensmittel OFFEN 222, belegt 0; Europa NEIN/unklar 0; Ersatz laut Bemerkung 19

| Bezugsdatei | FEHLER | GESPERRT | VERDACHT | OK |
|---|---|---|---|---|
| behaelter.json | 0 | 6 | 7 | 11 |
| huelle_pflanze.json | 4 | 8 | 7 | 10 |
| leitung.json | 0 | 0 | 43 | 80 |
| mess_elektrik.json | 1 | 17 | 9 | 4 |
| stahl.json | 1 | 1 | 61 | 19 |

## Links je Angebot

Rang 1 = Hauptangebot (Preis der Liste), 2+ = Alternativen.

| Urteil | Artikel | Rang | Haendler | HTTP | Grund | Seitentitel | URL |
|---|---|---|---|---|---|---|---|
| FEHLER | FOL-epdm-dichtband-zarge | 2 | Steinbach & Vollmann (stuv.de) | 0 | Netz: TimeoutError: The read operation timed out |  | https://stuv.de/api/de-DE/datasheet/V07800940 |
| FEHLER | FOL-epdm-tuerdichtung | 1 | wie FOL-epdm-dichtband-zarge ( | 0 | Netz: TimeoutError: The read operation timed out |  | https://stuv.de/api/de-DE/datasheet/V07700400 |
| FEHLER | FOL-pe-plane | 1 | AGRIplus UV5 200 um (stretchfo | 200 | Weiterleitung auf Startseite/Oberseite: https://www.stretchfolie.eu/ | Stretchfolie kaufen / nur bei Stretchfolien Profi ▷ stretchf | https://stretchfolie.eu |
| FEHLER | FOL-pe-plane | 3 | Lirsa Tristar (norhage.de) | 200 | Weiterleitung auf Startseite/Oberseite: https://norhage.de/ | Norhage – Gewächshaus- und Kunststoffzentrum – Norhage® | https://www.norhage.de |
| FEHLER | MES-par | 2 | gotogarden.com (Apogee SQ-520) | 402 | HTTP 402 | Store unavailable | https://gotogarden.com/products/apogee-instruments-sq-520-sonda-pro-mereni-parppfd |
| FEHLER | BLE-v2a-lochblech-medienschutz | 1 | Amazon.de (Verkaeufer Schloege | 404 | HTTP 404 |  | https://www.amazon.de/Edelstahl-Lochblech-Rv5-8-1-4301-500x1000mm/dp/B09MG6QWG8 |
| GESPERRT | BEH-fass-hdpe | 2 | Kanister-Vertrieb (Kaufland) | 403 | HTTP 403 |  | https://www.kaufland.de/product/564471148/ |
| GESPERRT | BEH-halter-box-gehaeuse | 1 | RS Components Deutschland (Spe | 403 | HTTP 403 | Access Denied | https://at.rs-online.com/web/p/universalgehause/5337385 |
| GESPERRT | BEH-halter-box-gehaeuse | 2 | RS Components Irland | 403 | HTTP 403 | Access Denied | https://ie.rs-online.com/web/p/products/5337739 |
| GESPERRT | BEH-kanister-hdpe | 1 | Kaufland-Verkaeufer (Leerkanis | 403 | HTTP 403 |  | https://www.kaufland.de/product/454580769/ |
| GESPERRT | BEH-messzelle-acryl | 3 | Bauhaus Oesterreich (Acrylglas | 403 | HTTP 403 |  | https://www.bauhaus.at/aluplatten-kunststoffplatten/acrylglas-nach-mass/p/29122352 |
| GESPERRT | PMP-dosierpumpe | 1 | ManoMano | 403 | HTTP 403 |  | https://www.manomano.de/p/12v-schlauchpumpe-fur-aquarien-labore-und-chemische-analysen-im-heimwerkerbereich-gruner-kopf-35-229357427 |
| GESPERRT | FOL-epdm-dichtung-630x440 | 1 | RS Components Deutschland, EPD | 403 | HTTP 403 | Access Denied | https://de.rs-online.com/web/p/gummimatten/5063214 |
| GESPERRT | SON-federdraht-d2 | 1 | eBay.de-Haendler 267458417642, | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/267458417642 |
| GESPERRT | SON-federdraht-d2 | 2 | eBay.de-Haendler, 304 Edelstah | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/388621401549 |
| GESPERRT | SON-knotenkugel-d100 | 1 | Kaufland.at, 20 Edelstahlkugel | 403 | HTTP 403 |  | https://www.kaufland.at/product/479387815/ |
| GESPERRT | SON-polycarbonat-paneel | 3 | Kaufland.at, 10er-Pack 8 mm, 7 | 403 | HTTP 403 |  | https://www.kaufland.at/product/523405227/ |
| GESPERRT | SON-tuerscharnier | 2 | Bauhaus (AT), Stabilit Anschwe | 403 | HTTP 403 |  | https://www.bauhaus.at/torbaender/c/10002806 |
| GESPERRT | TOP-biomedium | 1 | Wiltec, Unique Koi K1 Media 50 | 403 | HTTP 403 | 403 Forbidden | https://wiltec.de/en/unique-koi-k1-media-50l-4-paths-moving-bed-filtermedium-media-beads/7050058 |
| GESPERRT | TOP-blaehton | 1 | Baumarkt/Haendler 80-l-Sack (S | 403 | HTTP 403 |  | https://www.kaufland.de/product/533277187/ |
| GESPERRT | ELE-hutschiene-35 | 2 | RS Online DE (RS PRO gelocht,  | 403 | HTTP 403 | Access Denied | https://de.rs-online.com/web/p/din-schienen/2258315 |
| GESPERRT | ELE-kabelverschraubung-pg | 1 | RS Online DE (HellermannTyton  | 403 | HTTP 403 | Access Denied | https://de.rs-online.com/web/p/kabelverschraubungen/8188114 |
| GESPERRT | ELE-kabelverschraubung-pg | 2 | RS Online DE (Lapp SKINTOP M20 | 403 | HTTP 403 | Access Denied | https://de.rs-online.com/web/p/products/104010 |
| GESPERRT | MES-do-mini | 1 | DigiKey NL (Atlas ENV-20-DOX) | 403 | HTTP 403 |  | https://www.digikey.nl/en/products/detail/atlas-scientific/ENV-20-DOX/16003119 |
| GESPERRT | MES-druck-schalter | 1 | Kaufland AT (KOTARBAU BSK 2 1/ | 403 | HTTP 403 |  | https://www.kaufland.at/product/466406546/ |
| GESPERRT | MES-druck-schalter | 2 | eBay.de (einstellbarer Drucksc | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/397635686182 |
| GESPERRT | MES-ec | 1 | DigiKey FI (Atlas ENV-40-EC-K1 | 403 | HTTP 403 |  | https://www.digikey.fi/en/products/detail/atlas-scientific/ENV-40-EC-K1-0/16002997 |
| GESPERRT | MES-flow-12 | 2 | Farnell ES (DFRobot SEN0217, 1 | 403 | HTTP 403 |  | https://es.farnell.com/dfrobot/sen0217/sensor-flujo-agua-0-5-placa-arduino/dp/3517923 |
| GESPERRT | MES-flow-gross | 1 | ManoMano DE (Hall-Durchflussse | 403 | HTTP 403 |  | https://www.manomano.de/p/g3-4-1-30-l-min-hall-effekt-durchflusssensor-fur-wasser-zur-messung-und-steuerung-des-durchflusses-95793126 |
| GESPERRT | MES-flow-gross | 2 | eBay.de (DN32 Edelstahl Hall-T | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/317435429058 |
| GESPERRT | MES-leck | 1 | Homematic IP Wassersensor (ueb | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/156958983111 |
| GESPERRT | MES-level-druck | 2 | eBay.de (Tauchdrucksonde Edels | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/388519357627 |
| GESPERRT | MES-level-float | 2 | eBay.de Verkaeufer (PP-Schwimm | 403 | HTTP 403 | Error Page / eBay | https://www.ebay.de/itm/336049204033 |
| GESPERRT | MES-o2 | 1 | Annahme: wie MES-do-mini (Digi | 403 | HTTP 403 |  | https://www.digikey.nl/en/products/detail/atlas-scientific/ENV-20-DOX/16003119 |
| GESPERRT | MES-ph | 1 | RobotShop EU (Atlas ENV-40-pH, | 403 | HTTP 403 |  | https://eu.robotshop.com/de/products/atlas-scientific-ph-probe |
| GESPERRT | MES-strom-ct | 1 | Tinytronics (SCT013-030, 30 A  | 403 | HTTP 403 |  | https://www.tinytronics.nl/en/sensors/current-voltage/ac-current-sensor-sct013-030-30a |
| GESPERRT | MES-temp-ds | 2 | RobotShop EU (DFRobot DS18B20, | 403 | HTTP 403 |  | https://eu.robotshop.com/de/products/ds18b20-waterproof-digital-temperature-sensor |
| GESPERRT | BLE-v2a-lochblech-medienschutz | 2 | Eisen-Pfeiffer | 403 | HTTP 403 | 403 Forbidden | https://shop.eisen-pfeiffer.de/katalog/lochbleche-220327 |
| VERDACHT | BEH-fass-hdpe | 1 | billiger.de (Preisvergleich pl | 200 | Kennmass fehlt auf der Seite: 500 | plasteo 120 Liter Weithalsfass mit Deckel Blau💥Black Friday  | https://www.billiger.de/pricelist/4814918053-plasteo-120-liter-weithalsfass-mit-deckel-blau |
| VERDACHT | BEH-feinfilter-pp-630x440x610 | 1 | eBay.de-Haendler (Graf Mehrzwe | 200 | Kennmass fehlt auf der Seite: 440, 610, 630; Bemerkung: nicht belegt | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/1604249107 |
| VERDACHT | BEH-ibc-1000l | 2 | Hornbach | 200 | Kennmass fehlt auf der Seite: 1000 | IBC-Tank, Transportcontainer GRAF 1.000 l mit / HORNBACH | https://www.hornbach.de/p/ibc-tank-transportcontainer-graf-1-000-l-mit-un-kennzeichnung-geeignet-fuer-gefahrgueter-auf-kunststoff-palette/10230578/ |
| VERDACHT | BEH-messbecher-pp | 1 | barstuff.de | 200 | Kennmass fehlt auf der Seite: 160, 310 | Messbecher mit 100ml Skalierung, Polypropylen - 5 Liter | https://www.barstuff.de/messbecher-mit-100ml-skalierung-polypropylen-5-liter-12896 |
| VERDACHT | BEH-messbecher-pp | 2 | Bueromarkt-AG (Huenersdorff 93 | 200 | Kennmass fehlt auf der Seite: 160, 310 | Hünersdorff Messbecher 939000, aus Kunststoff, mit ml / Lite | https://www.bueromarkt-ag.de/messbecher_huenersdorff_939000_aus_kunststoff,p-939000.html |
| VERDACHT | BEH-messzelle-acryl | 2 | POLYVANTIS Shop (Plexiglas XT  | 200 | Kennmass fehlt auf der Seite: 260, 315 | POLYVANTIS Online-Shop für LEXAN(TM) & PLEXIGLAS(R) | https://www.polyvantis-shop.com/ |
| VERDACHT | BEH-tank-pe-673x1075 | 1 | tanksdirekt.de (Rotterdam Plas | 200 | Kennmass fehlt auf der Seite: 1075, 673 | Water Tank, 200 Litre, Conical versatile container, robust & | https://tanksdirekt.de/en/200-litre-conical-watertank |
| VERDACHT | FOL-epdm-dichtband-zarge | 1 | Fugendichtband24 (15x2 mm, 10  | 200 | Bemerkung: Ersatz | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/1258844086 |
| VERDACHT | FOL-epdm-schaumband | 1 | Fugendichtband24 / eBay-Haendl | 200 | Kennmass fehlt auf der Seite: 25; Bemerkung: Ersatz | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/1258844086 |
| VERDACHT | FOL-epdm-schaumband | 2 | Buerklin Elektronik, Essentra  | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | 10187890 / ESSENTRA COMPONENTS / Adhesive Tapes / Bürklin El | https://www.buerklin.com/en/p/essentra-components/adhesive-tapes/1200325001/14L2406/ |
| VERDACHT | GEW-v2a-100um | 1 | eBay.de-Haendler Edelstahl-Fil | 200 | Kennmass fehlt auf der Seite: 100 | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/1257460901 |
| VERDACHT | SON-tuerblatt-1000x2000 | 1 | Haendler laut wogibtswas.at: A | 200 | Kennmass fehlt auf der Seite: 1000, 2000; Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Gigaset A400 ➡️ Online-Angebote und Aktionen bis -67 % - wog | https://wogibtswas.at/ta/gigaset-a400 |
| VERDACHT | SON-tuerblatt-1000x2000 | 2 | vidaXL ueber Voelkner, Haustue | 200 | Kennmass fehlt auf der Seite: 1000, 2000, 40 | vidaXL Haustür Aluminium und PVC Anthrazit 100x200 cm / » Fr | https://www.voelkner.de/products/6935006/vidaXL-Haustuer-Aluminium-und-PVC-Anthrazit-100x200-cm.html |
| VERDACHT | TOP-blaehton | 2 | OSCAR.ehandel (eBay.de), Plagr | 200 | Kennmass fehlt auf der Seite: 16 | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/1646269961 |
| VERDACHT | ARM-bulkhead-d63 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63 | Bulkhead fitting PVC-U 40/50 mm x 1 3/4" glue socket/glue sp | https://www.bevo.com/en/bulkhead-fitting-pvc-u-10-bar-glue-socket-glue-spigot-x-male-thread-grey-0100541m |
| VERDACHT | ARM-bulkhead-pool | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63 | Bulkhead fitting PVC-U 40/50 mm x 1 3/4" glue socket/glue sp | https://www.bevo.com/en/bulkhead-fitting-pvc-u-10-bar-glue-socket-glue-spigot-x-male-thread-grey-0100541m |
| VERDACHT | ARM-kugelhahn-d110 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 110 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| VERDACHT | ARM-kugelhahn-d20 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| VERDACHT | ARM-kugelhahn-d40 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| VERDACHT | ARM-kugelhahn-d50 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| VERDACHT | ARM-kugelhahn-d63 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| VERDACHT | ARM-rsv-d20 | 1 | Schwarte-Shop | 200 | Kennmass fehlt auf der Seite: 20 | PVC Rückschlagventil günstig kaufen bei Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-rueckschlagventil-20-mm |
| VERDACHT | ARM-rsv-d25 | 1 | Schwarte-Shop | 200 | Kennmass fehlt auf der Seite: 25 | PVC Rückschlagventil günstig kaufen bei Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-rueckschlagventil-25-mm |
| VERDACHT | ARM-rsv-d40 | 1 | Schwarte-Shop | 200 | Kennmass fehlt auf der Seite: 40 | PVC Rückschlagventil günstig kaufen bei Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-rueckschlagventil-40-mm |
| VERDACHT | FIT-bogen45-d40 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Profec Long bend 45° PVC-U 90 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-90-mm-glue-socket-16bar-grey-type-made-from-tubing-0110231 |
| VERDACHT | FIT-bogen45-d50 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | Profec Long bend 45° PVC-U 90 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-90-mm-glue-socket-16bar-grey-type-made-from-tubing-0110231 |
| VERDACHT | FIT-bogen45-d63 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63 | Profec Long bend 45° PVC-U 90 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-90-mm-glue-socket-16bar-grey-type-made-from-tubing-0110231 |
| VERDACHT | FIT-bogen45-d75 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 75 | Profec Long bend 45° PVC-U 90 mm glue socket 16bar grey type | https://www.bevo.com/en/profec-long-bend-45-pvc-u-90-mm-glue-socket-16bar-grey-type-made-from-tubing-0110231 |
| VERDACHT | FIT-bogen90-d25 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | VDL Bend 90° PVC-U 50 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-50-mm-glue-socket-16bar-grey-7002573?fs=1 |
| VERDACHT | FIT-bogen90-d32 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 32 | VDL Bend 90° PVC-U 50 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-50-mm-glue-socket-16bar-grey-7002573?fs=1 |
| VERDACHT | FIT-bogen90-d40 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | VDL Bend 90° PVC-U 50 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-50-mm-glue-socket-16bar-grey-7002573?fs=1 |
| VERDACHT | FIT-kappe-d20 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | VDL Cap PVC-U 25 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-grey-7002810m |
| VERDACHT | FIT-kappe-d32 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 32 | VDL Cap PVC-U 25 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-grey-7002810m |
| VERDACHT | FIT-kappe-d50 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | VDL Cap PVC-U 25 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-grey-7002810m |
| VERDACHT | FIT-red-d40_d32 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 32, 40 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| VERDACHT | FIT-red-d50_d32 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 32, 50 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| VERDACHT | FIT-red-d50_d40 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40, 50 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| VERDACHT | FIT-red-d63_d50 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50, 63 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| VERDACHT | FIT-red-d75_d50 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50, 75 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| VERDACHT | FIT-red-d75_d63 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63, 75 | Reducer bush PVC-U 25 mm x 20 mm glue spigot x glue socket 1 | https://www.bevo.com/en/reducer-bush-pvc-u-25-mm-x-20-mm-glue-spigot-x-glue-socket-16bar-grey-0160733 |
| VERDACHT | FIT-t-d110 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 110 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | FIT-t-d20 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | FIT-t-d25 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | FIT-t-d32 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 32 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | FIT-t-d40 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | FIT-t-d50 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | FIT-t-d63 | 2 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| VERDACHT | ROH-leerrohr-dn100 | 1 | Hornbach | 200 | Kennmass fehlt auf der Seite: 100 | KG Rohr DN 110 1000 mm / HORNBACH | https://www.hornbach.de/p/kg-rohr-dn-110-1000-mm/267298/ |
| VERDACHT | ROH-pvcu-d20 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| VERDACHT | ROH-pvcu-d32 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 32 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| VERDACHT | ROH-pvcu-d40 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| VERDACHT | ROH-pvcu-d50 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| VERDACHT | ROH-pvcu-d63 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 63 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| VERDACHT | ROH-pvcu-d75 | 1 | Bevo | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 75 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| VERDACHT | SCH-rohrschelle-d110 | 1 | Schwarte-Shop | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 110 | Fischer Rohrschelle FRS 4" (108-116 mm), verzinkt - 20149 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-dn-100-4-108-116-mm |
| VERDACHT | SCH-rohrschelle-d50 | 1 | Schwarte-Shop | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 50 | Fischer Rohrschelle FRS 1 1/2" (48-54 mm), verzinkt - 20145 | https://www.schwarte-shop.de/fischer-zweischrauben-schellen-verzinkt-dn40-1-1-2-48-54-mm |
| VERDACHT | SCH-schlauchschelle-id16 | 1 | Schwarte-Shop | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 16 | ASW Schlauchschelle W4 Edelstahl 12-20 mm, Bandbreite 9 mm | https://www.schwarte-shop.de/schlauchschelle-edelstahl-w4-bandbreite-9mm-spannbereich-12-20-mm-1-2 |
| VERDACHT | ELE-schaltschrank-500x800x1200 | 1 | Proshop DE (Eldon Wandschrank  | 200 | Kennmass fehlt auf der Seite: 1200; Kennmass nicht in Titel/URL (nur im Seitentext): 500 | ELDON Wall mounted 800x400x300 / Günstig | https://www.proshop.de/Schaltkaesten-und-Schraenke/ELDON-Wall-mounted-800x400x300/2757478 |
| VERDACHT | ELE-schaltschrank-500x800x1200 | 2 | elektromax24 (Rittal AX Kompak | 200 | Kennmass fehlt auf der Seite: 500 | Rittal Kompakt-Schaltschrank 1türig 800x1200x400mm / elektro | https://www.elektromax24.de/rittal-kompakt-schaltschrank-1tuerig-800x1200x400mm |
| VERDACHT | MES-co2-scd41 | 1 | SOS electronic (Sensirion SCD4 | 200 | Kennmass fehlt auf der Seite: 39 | SCD41-D-R2 / SENSIRION Calibrated CO2 Sensor/ 347342 | https://www.soselectronic.com/en-us/products/sensirion/scd41-d-r2-347342 |
| VERDACHT | MES-flow-12 | 1 | Domoticx (YF-S201, G1/2, 1-30  | 200 | Kennmass fehlt auf der Seite: 39; Bemerkung: Ersatz | Water flow meter 1-30L/Min 1/2" DN15 kunststof 3-pin JST-SM  | https://domoticx.net/webshop/water-flow-meter-1-30lmin-12-dn15-kunststof-3-pin-jst-sm-yf-s201 |
| VERDACHT | MES-leck | 2 | eBay.de (Wassermelder Pad-Typ) | 200 | Kennmass fehlt auf der Seite: 39 | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/19070007052 |
| VERDACHT | MES-level-float | 1 | aquariumcomputer.com (GHL Nive | 200 | Kennmass fehlt auf der Seite: 39 | Niveau-Sensor, Schwimmer, Version 2 - GHL Advanced Technolog | https://www.aquariumcomputer.com/de/?p=87440 |
| VERDACHT | MES-par | 1 | shop-meeresaquaristik.de (Apog | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 39 | Apogee SQ-520 Quantum Sensor with USB output - Mrutzek Meere | https://www.shop-meeresaquaristik.de/Measurement-control-technology/PAR-measuring-devices-quantum-meters/Apogee-SQ-520-Quantum-Sensor-with-USB-output::18462.html |
| VERDACHT | MES-strom-ct | 2 | CDR (SCT-013-030) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 39 | SCT-013-030 inductive current sensor 0 - 30 A | https://en.cdr.pl/p6529,sct-013-030-inductive-current-sensor-0-30-a.html |
| VERDACHT | MES-temp-ds | 1 | Domoticx (DS18B20, Kabel 1-2 m | 200 | Kennmass fehlt auf der Seite: 39 | Temperatuur sensor digitaal 1-wire dallas waterdicht DS18B20 | https://domoticx.net/webshop/temperatuur-sensor-digitaal-1-wire-dallas-waterdicht-ds18b20-2m-kabel/ |
| VERDACHT | BLE-blech-st-3 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 700 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-blech-st-3 | 2 | stahl-shop24.de | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 700 | Stahl Blech 300x1500x3mm / 3 mm / 300x1500 mm / SBL128-5 | https://www.stahl-shop24.de/Stahl-Blech-300x1500x3mm |
| VERDACHT | BLE-blech-st-5 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 400, 840 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-blech-st-5 | 2 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 840; Kennmass nicht in Titel/URL (nur im Seitentext): 400 | Stahl Blech 200x1500x5mm / 5 mm / 200x1500 mm / SBL119-7 | https://www.stahl-shop24.de/Stahl-Blech-200x1500x5mm |
| VERDACHT | BLE-blech-st-6 | 1 | Metallparadies (metallparadies | 200 | Kennmass fehlt auf der Seite: 1360, 580 | Stahlblech 3 mm / Zuschnitt aus 3000 x 1500 / Metallparadies | https://www.metallparadies.de/stahlblech-3mm.html |
| VERDACHT | BLE-blech-st-6 | 2 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 1360, 580 | Stahl Blech 300x1500x6mm / 6 mm / 300x1500 mm / SBL128-8 | https://www.stahl-shop24.de/Stahl-Blech-300x1500x6mm |
| VERDACHT | BLE-fussplatte-100x100x6 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 100; Bemerkung: ERSATZ | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-100x100x6 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 100 | Stahlblech 6 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-6-mm-warmgewalzt-815795/ |
| VERDACHT | BLE-fussplatte-100x100x6 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 100 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-150x150x8 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 150 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-150x150x8 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass fehlt auf der Seite: 150 | Stahlblech 8 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-8-mm-warmgewalzt-750482/ |
| VERDACHT | BLE-fussplatte-150x150x8 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 150 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-200x200x8 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 200 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-200x200x8 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 200 | Stahlblech 8 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-8-mm-warmgewalzt-750482/ |
| VERDACHT | BLE-fussplatte-200x200x8 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 200 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-70x70x5 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 70 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-70x70x5 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass fehlt auf der Seite: 70 | Stahlblech 5 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-5-mm-warmgewalzt-540903/ |
| VERDACHT | BLE-fussplatte-70x70x5 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 70 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-80x80x6 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 80; Bemerkung: ERSATZ | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-80x80x6 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass fehlt auf der Seite: 80 | Stahlblech 6 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-6-mm-warmgewalzt-815795/ |
| VERDACHT | BLE-fussplatte-80x80x6 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 80 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-fussplatte-80x80x8 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 80 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-fussplatte-80x80x8 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass fehlt auf der Seite: 80 | Stahlblech 8 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-8-mm-warmgewalzt-750482/ |
| VERDACHT | BLE-fussplatte-80x80x8 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 80 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-platte-250x250x15 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 250; Kennmass nicht in Titel/URL (nur im Seitentext): 15 | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | BLE-platte-250x250x15 | 2 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass fehlt auf der Seite: 250; Kennmass nicht in Titel/URL (nur im Seitentext): 15 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | BLE-pp-blende-290x260 | 1 | S-Polytec | 200 | Kennmass fehlt auf der Seite: 260, 290 | Polypropylen PP-H in Grau 2x1 Meter - jetzt kaufen / S-Polyt | https://www.s-polytec.de/pp-h-polypropylen-platten-grau-2x1meter.html |
| VERDACHT | BLE-pp-blende-290x260 | 2 | Technoplast Kunststoffe | 200 | Kennmass fehlt auf der Seite: 260, 290 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| VERDACHT | BLE-pp-tafel-502x345x5 | 1 | S-Polytec | 200 | Kennmass fehlt auf der Seite: 345, 502 | Polypropylen PP-H in Grau 2x1 Meter - jetzt kaufen / S-Polyt | https://www.s-polytec.de/pp-h-polypropylen-platten-grau-2x1meter.html |
| VERDACHT | BLE-pp-tafel-502x345x5 | 2 | Technoplast Kunststoffe | 200 | Kennmass fehlt auf der Seite: 345, 502 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| VERDACHT | BLE-pp-tafel-693x463x7 | 1 | S-Polytec | 200 | Kennmass fehlt auf der Seite: 463, 693 | Polypropylen PP-H in Grau 2x1 Meter - jetzt kaufen / S-Polyt | https://www.s-polytec.de/pp-h-polypropylen-platten-grau-2x1meter.html |
| VERDACHT | BLE-pp-tafel-693x463x7 | 2 | Technoplast Kunststoffe | 200 | Kennmass fehlt auf der Seite: 463, 693 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| VERDACHT | BLE-v2a-3mm-korbflansch | 1 | Metallshopper | 200 | Kennmass fehlt auf der Seite: 414, 604 | Edelstahlblech K320 gebürstet 3 mm | https://metallshopper.de/Edelstahlblech-K320-gebuerstet-3-mm |
| VERDACHT | BLE-v2a-3mm-korbflansch | 2 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 414, 604 | Edelstahl Blech 500x800x3mm / 3 mm / 500x800 mm / VBL139-5 | https://www.stahl-shop24.de/Edelstahl-Blech-500x800x3mm |
| VERDACHT | PRF-alu-haut-profil | 1 | Hornbach | 200 | Bemerkung: ERSATZ | U-Profil Alu 20x20x1,5 mm, 2 m / HORNBACH | https://www.hornbach.de/p/u-profil-alu-20x20x1-5-mm-2-m/6368193/ |
| VERDACHT | PRF-alu-keilschiene | 1 | Wegner24 | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 15, 25; Bemerkung: ERSATZ | Klemmprofil, 2m Länge, 22,99 € | https://www.wegner24.eu/Klemmprofil_Netze_Planen |
| VERDACHT | PRF-alu-keilschiene | 2 | Norhage | 200 | Kennmass fehlt auf der Seite: 15, 25 | Aluminium Klemmprofil einfach für Gewächshausfolie silber –  | https://norhage.de/produkt/aluminium-klemmprofil-fuer-kunststofffolie-einzeln/ |
| VERDACHT | PRF-alu-klemmleiste | 1 | Hornbach | 200 | Bemerkung: ERSATZ | Flachstange Alu natur 30x2 mm, 2 m / HORNBACH | https://www.hornbach.de/p/flachstange-alu-natur-30x2-mm-2-m/757620/ |
| VERDACHT | PRF-pvcu-rinne-130x100 | 1 | Hornbach | 200 | Kennmass fehlt auf der Seite: 100, 130; Bemerkung: ERSATZ | ROTH LANGE Kabelkanal BxH 110 x 60 mm reinweiß 2 m / HORNBAC | https://www.hornbach.de/p/roth-lange-kabelkanal-bxh-110-x-60-mm-reinweiss-2-m/4685465/ |
| VERDACHT | PRF-pvcu-rinne-130x100 | 2 | OBI | 200 | Kennmass fehlt auf der Seite: 130 | EDO Kabelkanal 100x60 mm Weiß 2 m mit Klappdeckel zur Schrau | https://www.obi.de/p/2191181407035/edo-kabelkanal-100x60-mm-weiss-2-m-mit-klappdeckel-zur-schraubmontage |
| VERDACHT | PRF-st-rr25x25x2 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25 | Rechteckrohr + Quadratrohr bis 200 mm Breite S235JR | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr30x30x2 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | Rechteckrohr + Quadratrohr bis 200 mm Breite S235JR | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x40x2 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Rechteckrohr + Quadratrohr bis 200 mm Breite S235JR | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x40x2.5 | 1 | stahl-shop24.de | 200 | Bemerkung: Ersatz | Quadratrohr Feuerverzinkt 40x40x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-40x40x3mm-1000mm |
| VERDACHT | PRF-st-rr40x40x2.5 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 40 | Rechteckrohr + Quadratrohr bis 200 mm Breite S235JR | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rr40x60x3 | 2 | stahlshop.de (Krefeld) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 60 | verz. Vierkantstahlrohr 40 x 40 x 3,0 | https://stahlshop.de/verz-vierkantrohr-40-x-40-x-3-0-detail |
| VERDACHT | PRF-st-rr60x60x3 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 60 | Rechteckrohr + Quadratrohr bis 200 mm Breite S235JR | https://www.metallparadies.de/stahl-vierkantrohr.html |
| VERDACHT | PRF-st-rund20 | 1 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | Stabstahl Rundeisen bis 100 mm Durchmesser | https://www.metallparadies.de/stahl-vollmaterial-rundstahl.html |
| VERDACHT | PRF-st-rund20 | 3 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 20 | Stabstahl Rundeisen bis 100 mm Durchmesser | https://www.metallparadies.de/stahl-vollmaterial-rundstahl.html |
| VERDACHT | PRF-st-strebe30x30 | 2 | stahlshop.de (Krefeld) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | verz. Vierkantstahlrohr 40 x 40 x 3,0 | https://stahlshop.de/verz-vierkantrohr-40-x-40-x-3-0-detail |
| VERDACHT | SRB-halter-klein-12x10x20 | 2 | Hornbach | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 10, 12 | Reyher Sechskantschraube o. Schaft DIN 933 M6x20 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x20-mm-galv-verzinkt-100-stueck/10317037/ |
| VERDACHT | SRB-satz-m6x20 | 1 | Hornbach | 200 | Bemerkung: Ersatz | Reyher Sechskantschraube o. Schaft DIN 933 M6x20 mm galv. /  | https://www.hornbach.de/p/reyher-sechskantschraube-o-schaft-din-933-m6x20-mm-galv-verzinkt-100-stueck/10317037/ |
| VERDACHT | WNK-flach-14x3 | 1 | stahl-shop24.de | 200 | Kennmass fehlt auf der Seite: 14; Bemerkung: Ersatz | Flachstahl verzinkt 30x3mm 1000mm | https://www.stahl-shop24.de/Flachstahl-verzinkt-30x3mm-1000mm |
| VERDACHT | WNK-flach-14x3 | 2 | Metallparadies (metallparadies | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 14 | Flachstahl 20x3 mm bis 300x20 mm S235JR | https://www.metallparadies.de/stahl-flacheisen-s235jr-558.html |
| VERDACHT | WNK-pumpenkonsole | 1 | Hornbach | 200 | Bemerkung: Ersatz | Schwerlast-Winkelverbinder m. Sicke 90 x 90 x 65 mm, / HORNB | https://www.hornbach.de/p/schwerlast-winkelverbinder-m-sicke-90-x-90-x-65-mm-sendzimirverzinkt-1-stueck/738910/ |
| VERDACHT | WNK-rinnenhalter-25 | 1 | Metallshopper (Metaalshopper) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 25; Bemerkung: Ersatz | Stahl Winkelprofil warmgewalzt 30x30x3 mm | https://www.metallshopper.de/p/stahl-winkelprofil-warmgewalzt-30x30x3-mm-712809/ |
| VERDACHT | WNK-wandlasche-30x30x3 | 1 | Kemper GbR (kempergbr.de) | 200 | Kennmass fehlt auf der Seite: 30; Bemerkung: ERSATZ | Stahlplatten Zuschnitt nach Maß / Stahlbleche online kaufen | https://kempergbr.de/stahlplatte-zuschnitt-2-20mm-s235jr-stahlblech-blechplatte-blech-stahl::1.html |
| VERDACHT | WNK-wandlasche-30x30x3 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | Stahlblech 3 mm warmgewalzt | https://www.metallshopper.de/p/stahlblech-3-mm-warmgewalzt-894229/ |
| VERDACHT | WNK-wandlasche-30x30x3 | 3 | Stahlshop (stahlshop.de, Krefe | 200 | Kennmass nicht in Titel/URL (nur im Seitentext): 30 | Kopf- und Fußplatten | https://stahlshop.de/stahlplatten |
| VERDACHT | WNK-winkel-36x60x60 | 1 | Hornbach | 200 | Kennmass fehlt auf der Seite: 36; Bemerkung: Ersatz | Winkelverbinder 60 x 60 x 45 mm, sendzimirverzinkt, 1 Stück  | https://www.hornbach.de/p/winkelverbinder-60-x-60-x-45-mm-sendzimirverzinkt-1-stueck/3375551/ |
| VERDACHT | WNK-winkel-36x60x60 | 2 | Metallshopper (Metaalshopper) | 200 | Kennmass fehlt auf der Seite: 36 | Stahl Winkelprofil warmgewalzt 60x60x6 mm | https://www.metallshopper.de/p/stahl-winkelprofil-warmgewalzt-60x60x6-mm-384238/ |
| OK | BEH-ibc-1000l | 1 | Monopoel GmbH | 200 | HTTP 200 | IBC-Container, 1000 l, gebraucht / Monopoel GmbH | https://www.monopoel.de/catalog/container-1000-usage-p-525.html |
| OK | BEH-ibc-beetwanne | 1 | Monopoel GmbH | 200 | HTTP 200 | IBC-Container, 1000 l, gebraucht / Monopoel GmbH | https://www.monopoel.de/catalog/container-1000-usage-p-525.html |
| OK | BEH-ibc-beetwanne | 2 | Hornbach | 200 | HTTP 200 | IBC-Tank, Transportcontainer GRAF 1.000 l mit / HORNBACH | https://www.hornbach.de/p/ibc-tank-transportcontainer-graf-1-000-l-mit-un-kennzeichnung-geeignet-fuer-gefahrgueter-auf-kunststoff-palette/10230578/ |
| OK | BEH-kanister-hdpe | 2 | eBay.de-Haendler (Huenersdorff | 200 | HTTP 200 | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/14014263492 |
| OK | BEH-pool-zentral | 1 | Hornbach Oesterreich (Marimex  | 200 | HTTP 200 | Aufstellpool Stahlwandpool Marimex rund 457x107 cm inkl. / H | https://www.hornbach.at/p/aufstellpool-stahlwandpool-marimex-rund-457x107-cm-inkl-skimmer/12617697/ |
| OK | BEH-pool-zentral | 2 | Hornbach Oesterreich (Planet P | 200 | HTTP 200 | Aufstellpool Stahlwandpool-Set Planet Pool Vision-Pool / HOR | https://www.hornbach.at/p/aufstellpool-stahlwandpool-set-planet-pool-vision-pool-classic-rund-o-460x120-cm-inkl-kartuschenfilteranlage-leiter-weiss/7602701/ |
| OK | PMP-dosierpumpe | 2 | Funduino | 200 | HTTP 200 | Peristaltikpumpe 12 V, bis 150 ml/min / Funduino | https://funduino.com/es/products/peristaltikpumpe-dosierpumpe-12v-60-150ml |
| OK | PMP-pumpe-gross | 1 | Green Aqua (greenaqua.hu) | 200 | HTTP 200 | EHEIM Universal 3400 / Green Aqua | https://greenaqua.hu/en/eheim-universal-3400.html |
| OK | PMP-pumpe-gross | 2 | Hornbach Oesterreich | 200 | HTTP 200 | Universal-Pumpe EHEIM 3400 3-adriger Schukostecker mit 1,7 / | https://www.hornbach.at/p/universal-pumpe-eheim-3400-3-adriger-schukostecker-mit-1-7-m-kabel-80-w/8888958/ |
| OK | PMP-pumpe-klein | 1 | aquacomputer.de | 200 | HTTP 200 | Eheim 1250 / Eheim universal 1200 (Version Deutschland) Pump | https://shop.aquacomputer.de/Wasserkuehlung/Pumpen-Zub/Pumpen/Eheim-1250-Eheim-universal-1200-Version-Deutschland-Pumpe-1250219::1276.html |
| OK | PMP-pumpe-klein | 2 | Green Aqua (greenaqua.hu) | 200 | HTTP 200 | EHEIM Universal 1200 / Green Aqua | https://greenaqua.hu/en/eheim-universal-1200-pump-1250-828w-1200-lph.html |
| OK | FOL-pe-plane | 2 | Aquagart (auch OBI Marktplatz, | 200 | HTTP 200 | Aquagart 8m Gartenfolie Gewächshausfolie UV 5 Frühbeetfolie  | https://www.billiger.de/pricelist/4320529950-aquagart-8m-gartenfolie-gewaechshausfolie-uv-5-fruehbeetfolie-treibhausfolie-8m-breit |
| OK | SON-korbgriff-v2a | 1 | toolteam.com, Halder 24310.071 | 200 | HTTP 200 | HALDER Normalien Bügelgriff Ø 12 x 125 rostfreier Stahl 2431 | https://toolteam.com/en-GB/halder-normalien-buegelgriff-o-12-x-125-rostfreier-stahl-24310-0710-t-997832-4030618269892.html |
| OK | SON-korbgriff-v2a | 2 | Leschhorn, EO-20-160 Oval-Grif | 200 | HTTP 200 | Leschhorn EO-20-160-31 Oval-Edelstahl Bügelgriffe A 160, Mat | https://www.leschhorn.de/de/detail/0199737fd8cc73e9b26b275285143dc7 |
| OK | SON-polycarbonat-paneel | 2 | Voelkner (Sonnewelt, 10er-Pack | 200 | HTTP 200 | 10x Doppelstegplatten 8mm Zuschneidbar 121x60,5cm Polycarbon | https://www.voelkner.de/products/13260401/10x-Doppelstegplatten-8mm-Zuschneidbar-121x60-5cm-Polycarbonat-7-32m-UV-bestaendig-Klar-Hohlkammerplatten-Gewaechshaus-Platten-Stegplatten.html |
| OK | SON-spannverschluss-edelstahl | 1 | Leschhorn, Ganter GN 927.4 (Zi | 200 | HTTP 200 | Ganter 927.5-63-M6-35-A EDELSTAHL EXZENTERSPANNER, AUFLAGESC | https://www.leschhorn.de/de/detail/0199737dc29e7203bb609b5039ef8247 |
| OK | SON-spannverschluss-edelstahl | 2 | Leschhorn (Ganter GN 927.5 Ede | 200 | HTTP 200 | Ganter 927.7-101-M8-25-A Edelstahl Exzenterspanner mit Schra | https://www.leschhorn.de/de/detail/019973833f1e72bea1d0945048de1908 |
| OK | SON-tuerdruecker | 1 | eBay.de-Haendler, Hoppe Paris/ | 200 | HTTP 200 | Bitte entschuldigen Sie die Störung... | https://www.ebay.de/p/2254304591 |
| OK | SON-tuerdruecker | 2 | Hornbach (AT), Intersteel Tuer | 200 | HTTP 200 | Türdrücker und Rosetten kaufen / HORNBACH AT | https://www.hornbach.at/c/eisenwaren/beschlaege/tuerdruecker/tuerdruecker-rosetten/S2611/ |
| OK | SON-tuerscharnier | 1 | Hornbach (AT), verzinktes Tuer | 200 | HTTP 200 | Türbänder jetzt online kaufen / HORNBACH AT | https://www.hornbach.at/c/eisenwaren/beschlaege/tuerbaender/S31814/ |
| OK | TOP-biomedium | 2 | Absolute Koi (UK), Evolution A | 200 | HTTP 200 | Evolution Aqua K1 Media - Absolute Koi | https://absolute-koi.com/prod2430.html |
| OK | ARM-bulkhead-d40 | 1 | Bevo | 200 | HTTP 200 | Bulkhead fitting PVC-U 40/50 mm x 1 3/4" glue socket/glue sp | https://www.bevo.com/en/bulkhead-fitting-pvc-u-10-bar-glue-socket-glue-spigot-x-male-thread-grey-0100541m |
| OK | ARM-kugelhahn-d20 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 20 mm - 75319 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-20-mm |
| OK | ARM-kugelhahn-d25 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 25 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-25-mm-glue-socket-16bar-grey-type-dil-0100844 |
| OK | ARM-kugelhahn-d25 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 25 mm - 75320 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-25-mm |
| OK | ARM-kugelhahn-d32 | 1 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 32 mm glue socket 16bar grey type DIL | https://www.bevo.com/en/vdl-ball-valve-pvc-u-32-mm-glue-socket-16bar-grey-type-dil-0100845 |
| OK | ARM-kugelhahn-d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 32 mm - 75321 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-32-mm |
| OK | ARM-kugelhahn-d40 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 40 mm - 75322 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-40-mm |
| OK | ARM-kugelhahn-d40 | 3 | Bevo | 200 | HTTP 200 | VDL Ball valve PVC-U 40 mm glue socket 16bar DN32 grey type  | https://www.bevo.com/en/vdl-ball-valve-pvc-u-40-mm-glue-socket-16bar-dn32-grey-type-eil-7018363 |
| OK | ARM-kugelhahn-d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 50 mm - 75323 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-50-mm |
| OK | ARM-kugelhahn-d63 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kugelhahn 63 mm - 75324 | https://www.schwarte-shop.de/pvc-u-klebefitting-kugelhahn-63-mm |
| OK | FIT-bogen45-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 110 mm - 75030 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-110-mm |
| OK | FIT-bogen45-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 20 mm - 75022 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-20-mm |
| OK | FIT-bogen45-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 25 mm - 75023 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-25-mm |
| OK | FIT-bogen45-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 32 mm - 75024 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-32-mm |
| OK | FIT-bogen45-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 40 mm - 75025 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-40-mm |
| OK | FIT-bogen45-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 50 mm - 75026 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-50-mm |
| OK | FIT-bogen45-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 63 mm - 75027 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-63-mm |
| OK | FIT-bogen45-d75 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 45° 75 mm - 75028 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-45-75-mm |
| OK | FIT-bogen90-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 110 mm - 75020 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-110-mm |
| OK | FIT-bogen90-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 20 mm - 75012 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-20-mm |
| OK | FIT-bogen90-d20 | 2 | voelkner (Marktplatz-Anbieter  | 200 | HTTP 200 | PVC - U 90° Bogen 20 mm PN16 / » Freue dich auf voelkner | https://www.voelkner.de/products/12813981/PVC-U-90-Bogen-20-mm-PN16.html |
| OK | FIT-bogen90-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 25 mm - 75013 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-25-mm |
| OK | FIT-bogen90-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 32 mm - 75014 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-32-mm |
| OK | FIT-bogen90-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 40 mm - 75015 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-40-mm |
| OK | FIT-bogen90-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 50 mm - 75016 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-50-mm |
| OK | FIT-bogen90-d50 | 2 | Bevo | 200 | HTTP 200 | VDL Bend 90° PVC-U 50 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-bend-90-pvc-u-50-mm-glue-socket-16bar-grey-7002573?fs=1 |
| OK | FIT-bogen90-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 63 mm - 75017 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-63-mm |
| OK | FIT-bogen90-d75 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Winkel 90° 75 mm - 75018 | https://www.schwarte-shop.de/pvc-u-klebefitting-winkel-90-75-mm |
| OK | FIT-kappe-d16 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 16 mm - 75136 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-16-mm |
| OK | FIT-kappe-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 20 mm - 75137 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-20-mm |
| OK | FIT-kappe-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 25 mm - 75138 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-25-mm |
| OK | FIT-kappe-d25 | 2 | Bevo | 200 | HTTP 200 | VDL Cap PVC-U 25 mm glue socket 16bar grey | https://www.bevo.com/en/vdl-cap-pvc-u-grey-7002810m |
| OK | FIT-kappe-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Kappe 32 mm - 75139 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-kappe-32-mm |
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
| OK | FIT-red-d40_d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 40 mm (ø 32 mm) - 75212 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-40-mm-o-32-mm |
| OK | FIT-red-d50_d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 50 mm (ø 32 mm) - 75215 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-50-mm-o-32-mm |
| OK | FIT-red-d50_d40 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 50 mm (ø 40 mm) - 75216 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-50-mm-o-40-mm |
| OK | FIT-red-d63_d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 63 mm (ø 50 mm) - 75220 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-63-mm-o-50-mm |
| OK | FIT-red-d75_d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 75 mm (ø 50 mm) - 75223 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-75-mm-o-50-mm |
| OK | FIT-red-d75_d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Reduktion kurz 75 mm (ø 63 mm) - 75224 | https://www.schwarte-shop.de/pvc-u-klebefitting-reduktion-kurz-75-mm-o-63-mm |
| OK | FIT-stutzen-d16 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 16 mm x 3/8" - 75268 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-16-mm-x-3-8 |
| OK | FIT-stutzen-d20 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 20 mm x 1/2" - 75270 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-20-mm-x-1-2 |
| OK | FIT-stutzen-d32 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 32 mm x 3/4" - 75273 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-32-mm-x-3-4 |
| OK | FIT-stutzen-d40 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 40 mm x 1 1/4" - 75276 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-40-mm-x-1-1-4 |
| OK | FIT-stutzen-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Übergangsnippel 63 mm x 2" - 75280 | https://www.schwarte-shop.de/pvc-u-klebefitting-uebergangsnippel-63-mm-x-2 |
| OK | FIT-t-d110 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 110 mm - 75050 | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-110-mm |
| OK | FIT-t-d20 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 20 mm - 75042 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-20-mm |
| OK | FIT-t-d25 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 25 mm - 75043 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-25-mm |
| OK | FIT-t-d32 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 32 mm - 75044 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-32-mm |
| OK | FIT-t-d40 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 40 mm - 75045 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-40-mm |
| OK | FIT-t-d50 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 50 mm - 75046 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-50-mm |
| OK | FIT-t-d63 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 63 mm - 75047 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-63-mm |
| OK | FIT-t-d75 | 1 | Bevo | 200 | HTTP 200 | VDL T-piece 90° PVC-U 75 mm glue socket 16bar grey KIWA | https://www.bevo.com/en/vdl-t-piece-90-pvc-u-kiwa-glue-socket-grey-7002485m |
| OK | FIT-t-d75 | 2 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting T-Stück 75 mm - 75048 / Schwarte-Shop.de | https://www.schwarte-shop.de/pvc-u-klebefitting-t-stueck-75-mm |
| OK | FIT-verschraubung-d50 | 1 | Schwarte-Shop | 200 | HTTP 200 | PVC-U Klebefitting Rohrverschraubung 50 mm (2 1/4") - 75036 | https://www.schwarte-shop.de/pvc-u-klebefitting-rohrverschraubung-50-mm-2-1-4 |
| OK | FIT-verschraubung-d50 | 2 | voelkner (Marktplatz-Anbieter  | 200 | HTTP 200 | PVC - U Verschraubung Klebemuffe x Klebemuffe 50 mm / » Freu | https://www.voelkner.de/products/12814009/PVC-U-Verschraubung-Klebemuffe-x-Klebemuffe-50-mm.html |
| OK | ROH-pvcu-d110 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 110 mm x 6,6 mm glue socket x plain 16ba | https://www.bevo.com/en/pressure-pipe-pvc-u-110-mm-x-6-6-mm-glue-socket-x-plain-16bar-iso-pn16-grey-5m-0309233 |
| OK | ROH-pvcu-d160 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 160 mm x 4,7 mm glue socket x plain 7,5b | https://www.bevo.com/en/pressure-pipe-pvc-u-160-mm-x-4-7-mm-glue-socket-x-plain-7-5bar-grey-5m-0309003 |
| OK | ROH-pvcu-d25 | 1 | Bevo | 200 | HTTP 200 | Pressure pipe PVC-U 25 mm x 1,9 mm glue socket x plain 16bar | https://www.bevo.com/en/pressure-pipe-pvc-u-25-mm-x-1-9-mm-glue-socket-x-plain-16bar-iso-pn16-din-pn16-grey-5m-0329126 |
| OK | ROH-pvcu-d63 | 2 | Bosta (Bevo-Schwester) | 200 | HTTP 200 | Pressure pipe PVC-U 63 mm x 4,7 mm plain ISO-PN16 transparen | https://acc.bosta.com/en-ie/pressure-pipe-pvc-u-63-mm-x-4-7-mm-plain-iso-pn16-transparent-5m-0340030 |
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
| OK | MES-temperatur | 1 | Annahme: wie MES-temp-ds (DS18 | 200 | HTTP 200 | Temperatuur sensor digitaal 1-wire dallas waterdicht DS18B20 | https://domoticx.net/webshop/temperatuur-sensor-digitaal-1-wire-dallas-waterdicht-ds18b20-2m-kabel/ |
| OK | BLE-pp-siebboden-beet | 2 | S-Polytec | 200 | HTTP 200 | Polypropylen PP-H in Grau 2x1 Meter - jetzt kaufen / S-Polyt | https://www.s-polytec.de/pp-h-polypropylen-platten-grau-2x1meter.html |
| OK | BLE-pp-siebboden-beet | 3 | Technoplast Kunststoffe | 200 | HTTP 200 | PP-H hellgrau (Platten) - Technoplast Kunststoffe | https://www.technoplast-onlineshop.de/gruppe,mein_shop,de/Platten,plattenpp,43004,PP-H-hellgrau |
| OK | PRF-alu-haut-profil | 2 | OBI | 200 | HTTP 200 | Aluminium U Profil 20 mm x 20 mm x 2.000 mm Silber kaufen be | https://www.obi.de/p/8750010/u-profil-aluminium-20-mm-x-20-mm-x-2-000-mm-silber |
| OK | PRF-alu-klemmleiste | 2 | OBI | 200 | HTTP 200 | Arcansas Aluminium Flachstange Silber eloxiert 2 x 30 x 1000 | https://www.obi.de/profile/arcansas-flachstange-aluminium-silber-eloxiert-1-000-x-30-x-2-mm/p/4973244 |
| OK | PRF-st-rr25x25x2 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 25x25x2mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-25x25x2mm-1000mm |
| OK | PRF-st-rr30x30x2 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 30x30x2mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-30x30x2mm-1000mm |
| OK | PRF-st-rr40x40x2 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 40x40x2mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-40x40x2mm-1000mm |
| OK | PRF-st-rr40x40x3 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 40x40x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-40x40x3mm-1000mm |
| OK | PRF-st-rr40x40x3 | 2 | stahlshop.de (Krefeld) | 200 | HTTP 200 | verz. Vierkantstahlrohr 40 x 40 x 3,0 | https://stahlshop.de/verz-vierkantrohr-40-x-40-x-3-0-detail |
| OK | PRF-st-rr40x40x3 | 3 | metallparadies.de | 200 | HTTP 200 | Vierkantrohr 40x40x3,0 mm nach Wunschlänge kaufen | https://www.metallparadies.de/vierkantrohr-stahl-40x40x3-0-mm.html |
| OK | PRF-st-rr40x60x3 | 1 | stahl-shop24.de | 200 | HTTP 200 | Rechteckrohr Feuerverzinkt 60x40x3mm 1000mm | https://www.stahl-shop24.de/Rechteckrohr-Feuerverzinkt-60x40x3mm-1000mm |
| OK | PRF-st-rr60x60x3 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 60x60x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-60x60x3mm-1000mm |
| OK | PRF-st-rund20 | 2 | stahl-shop24.de | 200 | HTTP 200 | Rundstahl verzinkt 20mm 1000mm | https://www.stahl-shop24.de/Rundstahl-verzinkt-20mm-1000mm |
| OK | PRF-st-strebe30x30 | 1 | stahl-shop24.de | 200 | HTTP 200 | Quadratrohr Feuerverzinkt 30x30x3mm 1000mm | https://www.stahl-shop24.de/Quadratrohr-Feuerverzinkt-30x30x3mm-1000mm |
| OK | PRF-v2a-voll8x8 | 1 | stahl-shop24.de | 200 | HTTP 200 | Edelstahl Vierkant 8x8mm 1000mm / 1000 mm / 8x8 mm / VVK102- | https://www.stahl-shop24.de/Edelstahl-Vierkant-8x8mm-1000mm |
| OK | PRF-v2a-voll8x8 | 2 | Metallshopper (NL-Fertigung, . | 200 | HTTP 200 | Edelstahl vollmaterial vierkant 8 mm | https://metallshopper.de/Edelstahl-vollmaterial-vierkant-8-mm |
| OK | WNK-flach-3mm-diagonale | 2 | stahl-shop24.de | 200 | HTTP 200 | Flachstahl verzinkt 30x3mm 1000mm | https://www.stahl-shop24.de/Flachstahl-verzinkt-30x3mm-1000mm |
| OK | WNK-flach-3mm-diagonale | 3 | Metallparadies (metallparadies | 200 | HTTP 200 | Flachstahl 20x3 mm bis 300x20 mm S235JR | https://www.metallparadies.de/stahl-flacheisen-s235jr-558.html |
| OK | WNK-pumpenkonsole | 2 | Metallshopper (Metaalshopper) | 200 | HTTP 200 | Stahl Winkelprofil warmgewalzt 60x60x6 mm | https://www.metallshopper.de/p/stahl-winkelprofil-warmgewalzt-60x60x6-mm-384238/ |

## Plausibilitaet je Zeile

Lebensmittel: nur fuer Typen mit Wasser- oder Pflanzenkontakt (ROH, FIT, ARM, BEH, PMP, FOL, GEW, TOP, BLE, PRF, MES, SON); `belegt` = Bemerkung nennt Trinkwasser/Lebensmittel/KTW/W270/LFGB/1935/2004, sonst OFFEN. Europa nach Land des Hauptangebots (D76).

| Artikel | Bezeichnung | Datei | Mass | Einheit | Werkstoff | Lebensmittel | Europa | Konfidenz | Ersatz | Bedarf |
|---|---|---|---|---|---|---|---|---|---|---|
| ARM-durchflussbegrenzer-messing | Durchflussbegrenzer Messing [A] | - | - | Stk | Messing | OFFEN | - | - |  | 0.0 |
| ARM-probehahn-messing | Probierhahn Messing 1/2 Zoll [A] | - | - | Stk | Messing | OFFEN | - | - |  | 0.0 |
| ARM-schwimmerventil-pool | Schwimmerventil Pool (Gehaeuse, Wangen, Hebelarm m | - | - | Stk | PP | OFFEN | - | - |  | 0.0 |
| BEH-ak-kompositbehaelter-254x790 | Aktivkohle-Druckbehaelter Komposit 254x790 mm mit  | - | bbox_mm=[254, 254, 790] | Stk | Komposit | OFFEN | - | - |  | 0.0 |
| BEH-ak-sedimentfilter | Sedimentfilter-Set (Gehaeuse, Kopf, Patrone) [A] | - | - | Satz | PP | OFFEN | - | - |  | 0.0 |
| BLE-schrankboden-3x500x800 | Stahlblech 3 mm, Zuschnitt 800x500 (Schrankboden)  | - | - | Stk | Stahl | OFFEN | - | - |  | 0.0 |
| FIT-red-d32-d25 | PVC-U-Reduzierung d32 auf d25 | - | groesse=d32_d25 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-stutzen-d25 | PVC-U-Stutzen d25 (Klebe/Gewinde) | - | durchmesser_mm=25 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| PMP-geblaese-luft | Membrangeblaese Luft (Leistung offen, Bauteilblatt | - | bbox_mm=[180, 230, 240] | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-ak-konsole | Konsole Sedimentfilter (Stahl, Eigenbau) [A] | - | - | Stk | Stahl | OFFEN | - | - |  | 0.0 |
| SON-gummifuss-40 | Gummifuss 40x40x15 | - | - | Stk | Gummi | OFFEN | - | - |  | 0.0 |
| SON-luftverteiler-4 | Luftverteiler 4-fach (PVC, Eigenbau) [A] | - | bbox_mm=[48, 98, 470] | Stk | PVC | OFFEN | - | - |  | 0.0 |
| SON-luftverteiler-6 | Luftverteiler 6-fach (PVC, Eigenbau) [A] | - | bbox_mm=[48, 98, 710] | Stk | PVC | OFFEN | - | - |  | 0.0 |
| SON-scheibenbelueftung-270 | Scheibenbelueftung d270 (Tragteller, Stuetzfuss, E | - | - | Stk | PP/EPDM | OFFEN | - | - |  | 0.0 |
| SON-schrankwand-500x800 | Schrankwand 500x800 (Eigenbau, Werkstoff offen) [A | - | - | Stk | Stahl | OFFEN | - | - |  | 0.0 |
| SRB-satz-m10x60 | Schraubensatz M10x60 (Sechskantschraube DIN 933 +  | - | gewinde=M10, laenge_mm=60 | Satz | Stahl verzinkt | - | - | - |  | 130.0 |
| SRB-satz-m12x55 | Schraubensatz M12x55 (Sechskantschraube DIN 933 +  | - | gewinde=M12, laenge_mm=55 | Satz | Stahl verzinkt | - | - | - |  | 10.0 |
| SRB-satz-m16x300 | Schraubensatz M16x300 (Sechskantschraube DIN 933 + | - | gewinde=M16, laenge_mm=300 | Satz | Stahl verzinkt | - | - | - |  | 20.0 |
| SRB-satz-m5x12 | Schraubensatz M5x12 (Sechskantschraube DIN 933 + M | - | gewinde=M5, laenge_mm=12 | Satz | Stahl verzinkt | - | - | - |  | 304.0 |
| SRB-satz-m6x16 | Schraubensatz M6x16 (Sechskantschraube DIN 933 + M | - | gewinde=M6, laenge_mm=16 | Satz | Stahl verzinkt | - | - | - |  | 0.0 |
| SRB-satz-m6x40 | Schraubensatz M6x40 (Sechskantschraube DIN 933 + M | - | gewinde=M6, laenge_mm=40 | Satz | Stahl verzinkt | - | - | - |  | 112.0 |
| SRB-satz-m6x55 | Schraubensatz M6x55 (Sechskantschraube DIN 933 + M | - | gewinde=M6, laenge_mm=55 | Satz | Stahl verzinkt | - | - | - |  | 0.0 |
| SRB-satz-m8x30 | Schraubensatz M8x30 (Sechskantschraube DIN 933 + M | - | gewinde=M8, laenge_mm=30 | Satz | Stahl verzinkt | - | - | - |  | 184.0 |
| TOP-aktivkohle | Aktivkohle-Granulat (Behaelterfuellung) | - | - | m3 | Aktivkohle | OFFEN | - | - |  | 0.0 |
| BEH-becken-dritt | Drittbecken (Eigenbau/Sonderanfertigung, Masse aus | behaelter.json | bbox_mm=[1150, 1150, 1265] | Stk | - | OFFEN | - | - |  | 0.0 |
| BEH-drittbecken-klein | Drittbecken klein (Wanne 920x920x1055) | behaelter.json | bbox_mm=[920, 920, 1055] | Stk | Beton | OFFEN | - | - |  | 1.0 |
| BEH-fass-hdpe | HDPE-Fass 500 mm (Mischfass) | behaelter.json | - | Stk | HDPE blau | OFFEN | ja | Q-Treffer |  | 1.0 |
| BEH-feinfilter-pp-630x440x610 | Feinfilter-Behaelter PP 630x440x610 (Eigenbau/Kauf | behaelter.json | - | Stk | PP | OFFEN | ja | Q-Treffer | ERSATZ | 2.0 |
| BEH-halter-box-gehaeuse | Anschlussbox PS 200x150x100 mit Acryldeckel | behaelter.json | - | Stk | PS/Acryl | OFFEN | ja | Q-Treffer |  | 0.0 |
| BEH-ibc-1000l | IBC-Container 1000 l mit Gitterkaefig und Palette  | behaelter.json | volumen_l=1000 | Stk | PE/Stahl/HDPE | OFFEN | ja | Q |  | 0.0 |
| BEH-ibc-beetwanne | IBC-Beetwanne HDPE (aus IBC geschnitten, Laenge je | behaelter.json | bbox_mm=[637, 800, 2640] | Stk | HDPE weiss | OFFEN | ja | Q |  | 14.0 |
| BEH-kanister-hdpe | HDPE-Kanister (Dosiervorrat) | behaelter.json | - | Stk | HDPE | OFFEN | ja | Q-Treffer |  | 1.0 |
| BEH-messbecher-pp | Messbecher PP 160x310 | behaelter.json | - | Stk | PP | OFFEN | ja | Q |  | 0.0 |
| BEH-messzelle-acryl | Messzelle Acryl 315x315x260 | behaelter.json | - | Stk | Acryl klar | OFFEN | - | - |  | 1.0 |
| BEH-pool-zentral | Zentralpool (Eigenbau/Sonderanfertigung, Masse aus | behaelter.json | bbox_mm=[2475, 4190, 4190] | Stk | - | OFFEN | ja | Q |  | 1.0 |
| BEH-tank-pe-673-deckel | PE-Tankdeckel 673 mm | behaelter.json | - | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-tank-pe-673x1075 | PE-Tank 673 mm Durchm., 1075 mm hoch (Kegelboden/A | behaelter.json | bbox_mm=[673, 673, 1075] | Stk | PE | OFFEN | ja | Q |  | 2.0 |
| BEH-tank-pe-930-deckel | PE-Tankdeckel 930 mm | behaelter.json | - | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-tank-pe-930x1444 | PE-Tank 930 mm Durchm., 1444 mm hoch (Kegelboden/A | behaelter.json | bbox_mm=[930, 930, 1444] | Stk | PE | OFFEN | - | - |  | 2.0 |
| BEH-zweitbecken | Zweitbecken (Eigenbau/Sonderanfertigung, Masse aus | behaelter.json | bbox_mm=[1135, 1867, 1867] | Stk | - | OFFEN | - | - |  | 1.0 |
| PMP-dosierpumpe | Dosierpumpe (Schlauchpumpe) | behaelter.json | - | Stk | - | OFFEN | ja | Q-Treffer |  | 1.0 |
| PMP-pumpe-gross | Kreiselpumpe gross | behaelter.json | - | Stk | - | OFFEN | ja | Q |  | 4.0 |
| PMP-pumpe-klein | Kreiselpumpe klein | behaelter.json | - | Stk | - | OFFEN | ja | Q |  | 4.0 |
| FOL-epdm-dichtband-zarge | EPDM-Dichtband Zarge | huelle_pflanze.json | - | m | EPDM | OFFEN | ja | Q-Treffer | ERSATZ | 0.0 |
| FOL-epdm-dichtung-630x440 | EPDM-Flachdichtung 630x440x3 | huelle_pflanze.json | - | Stk | EPDM | OFFEN | ja | Q-Treffer |  | 2.0 |
| FOL-epdm-schaumband | EPDM-Schaumband 25x3 | huelle_pflanze.json | - | m | EPDM | OFFEN | ja | Q-Treffer | ERSATZ | 0.0 |
| FOL-epdm-tuerdichtung | EPDM-Tuerdichtung | huelle_pflanze.json | - | m | EPDM | OFFEN | ja | A | ERSATZ | 5.99 |
| FOL-pe-plane | PE-Planenbahn (Huelle, Zuschnitt je Feld, Flaeche  | huelle_pflanze.json | - | m2 | PE Folie | OFFEN | ja | Q |  | 1015.84 |
| GEW-v2a-100um | Edelstahl-Siebgewebe 100 um, 1.4301 (Siebkorb, Fla | huelle_pflanze.json | maschenweite_um=100 | m2 | Edelstahl 1.4301 | OFFEN | ja | E |  | 2.02 |
| SON-ankergabel-80x140 | Gabelkopf 80x140 (Fundamentanker, Stahl, Zuschnitt | huelle_pflanze.json | - | Stk | Stahl Anker | OFFEN | - | - |  | 20.0 |
| SON-ankerlasche | Ankerlasche am Knoten (Stahl, Zuschnitt) | huelle_pflanze.json | - | Stk | Stahl Knoten | OFFEN | - | - |  | 10.0 |
| SON-belueftungsgitter-460 | Belueftungsgitter 460x460 (PVC, Tankdeckel) | huelle_pflanze.json | - | Stk | PVC grau Tank | OFFEN | - | - |  | 2.0 |
| SON-federdraht-d2 | Federstahldraht d2 (Keilschiene) | huelle_pflanze.json | - | m | Federstahl | OFFEN | ja | A | ERSATZ | 0.0 |
| SON-halter-inline-d32-sensorblock | Sensorblock (halter_inline_d32, Eigenbau aus PVC-U | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d32-sieb | Sieb halter_inline_d32 (Edelstahl) | huelle_pflanze.json | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d32-vorfilter | Vorfilter (halter_inline_d32, Eigenbau aus PVC-U) | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d50-sensorblock | Sensorblock (halter_inline_d50, Eigenbau aus PVC-U | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d50-sieb | Sieb halter_inline_d50 (Edelstahl) | huelle_pflanze.json | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| SON-halter-inline-d50-vorfilter | Vorfilter (halter_inline_d50, Eigenbau aus PVC-U) | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-halter-zelle-zellkoerper | Zellkoerper (halter_zelle, Eigenbau aus PVC-U) | huelle_pflanze.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| SON-holz-stuetzrippe | Stuetzrippe Fichte (Tank-Auflage) | huelle_pflanze.json | - | Stk | Holz Fichte | OFFEN | - | - |  | 10.0 |
| SON-knotenarm-23x23x3 | Steckarm 23x23x3 am Knoten (Verbindungsstueck, N-S | huelle_pflanze.json | - | Stk | Stahl Knoten | OFFEN | - | - |  | 130.0 |
| SON-knotenkugel-d100 | Knotenkugel d100, Stahl (Verbindungsstueck, N-STAT | huelle_pflanze.json | - | Stk | Stahl Knoten | OFFEN | ja | Q-Treffer |  | 26.0 |
| SON-korbgriff-v2a | Korbgriff Edelstahl (Eigenbau) | huelle_pflanze.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | Q-Treffer |  | 4.0 |
| SON-pflanztisch-platte | Pflanztischplatte (Alt-Modell, nicht verbaut) | huelle_pflanze.json | - | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-plattform-619x619 | Tankplattform 619x619x73 (Stahl, Eigenbau) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 2.0 |
| SON-plattform-821x821 | Tankplattform 821x821x98 (Stahl, Eigenbau) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 2.0 |
| SON-polycarbonat-paneel | Polycarbonat-Paneel 8 mm (Zuschnitt je Feld) | huelle_pflanze.json | dicke_mm=8 | Stk | Polycarbonat | OFFEN | - | - |  | 0.0 |
| SON-pp-stuetze-60x60 | PP-Stuetze 60x60 (Beetboden, Hoehe je Beet) | huelle_pflanze.json | - | Stk | PP grau | OFFEN | - | - |  | 282.0 |
| SON-schacht-kugelhahn-d63 | Schacht fuer Kugelhahn (PE-HD) d63 | huelle_pflanze.json | groesse=d63 | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-sondenhalter-36 | Sondenhalter 36x36x40 (PVC, Eigenbau/Stuetze) | huelle_pflanze.json | - | Stk | Kanal PVC | OFFEN | - | - |  | 0.0 |
| SON-spannverschluss-edelstahl | Spannverschluss Edelstahl (Bock + Hebel) | huelle_pflanze.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | Q-Treffer |  | 8.0 |
| SON-strahlungsschutz-par | Strahlungsschutz PP weiss (Messmast) | huelle_pflanze.json | - | Stk | PP weiss | OFFEN | - | - |  | 0.0 |
| SON-tanksieb-stahl | Sieb am Tank (Stahl verzinkt, Zulauf/Auslauf) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 4.0 |
| SON-tauchklemme | Klemme Tauchrohr (Stahl, Eigenbau) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | - | - |  | 3.0 |
| SON-tuer-modellvariante | Tuer (Alt-Modell, nicht verbaut) T4_Pfosten_L | huelle_pflanze.json | - | Stk | - | OFFEN | - | - |  | 0.0 |
| SON-tuerblatt-1000x2000 | Tuerblatt Sandwich 1000x2000x40 | huelle_pflanze.json | - | Stk | Tuerblatt Sandwich | OFFEN | ja | Q-Treffer |  | 1.0 |
| SON-tuerdruecker | Tuerdruecker mit Rosette | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | ja | Q-Treffer |  | 2.0 |
| SON-tuerscharnier | Tuerscharnier (Zargenlasche, Blattlasche, Bolzen) | huelle_pflanze.json | - | Stk | Stahl verzinkt | OFFEN | ja | Q-Treffer |  | 3.0 |
| SON-zarge-aufsatzrahmen | Alu-Aufsatzrahmen Tuerzarge (Planenausschnitt) | huelle_pflanze.json | - | Stk | Aluminium Zarge | OFFEN | - | - |  | 0.0 |
| TOP-biomedium | Biomedium (Biofilter-Fuellkoerper) | huelle_pflanze.json | - | m3 | Kunststoff | OFFEN | ja | Q-Treffer |  | 1.29 |
| TOP-blaehton | Blaehton-Substrat 8-16 mm (Beetfuellung) | huelle_pflanze.json | - | m3 | Blaehton | OFFEN | ja | Q-Treffer |  | 7.52 |
| TOP-netztopf-64 | Netztopf PP 64 mm (Pflanzkorb, Stueckzahl aus Inst | huelle_pflanze.json | durchmesser_mm=64 | Stk | PP | OFFEN | - | - |  | 2222.0 |
| ARM-anbohrschelle | Anbohrschelle PVC-U (Messstelle) | leitung.json | - | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-bulkhead-d40 | PVC-U-Bulkhead d40 | leitung.json | durchmesser_mm=40 | Stk | PVC-U | OFFEN | ja | Q |  | 14.0 |
| ARM-bulkhead-d63 | PVC-U-Bulkhead d63 (Tank-/Behaelterdurchfuehrung) | leitung.json | durchmesser_mm=63 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| ARM-bulkhead-pool | Pool-Durchfuehrung d63 (Stutzen Pool-Wand) | leitung.json | durchmesser_mm=63 | Stk | PVC-U | OFFEN | ja | Q |  | 7.0 |
| ARM-kabeleinfuehrung-dn100 | Kabeleinfuehrung dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-kabeleinfuehrung-dn50 | Kabeleinfuehrung dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| ARM-kugelhahn-d110 | PVC-U-Kugelhahn d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-kugelhahn-d20 | PVC-U-Kugelhahn d20 | leitung.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-kugelhahn-d25 | PVC-U-Kugelhahn d25 | leitung.json | durchmesser_mm=25 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| ARM-kugelhahn-d32 | PVC-U-Kugelhahn d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-kugelhahn-d40 | PVC-U-Kugelhahn d40 | leitung.json | durchmesser_mm=40 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| ARM-kugelhahn-d50 | PVC-U-Kugelhahn d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| ARM-kugelhahn-d63 | PVC-U-Kugelhahn d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| ARM-rsv-d20 | PVC-U-Rueckschlagventil d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-rsv-d25 | PVC-U-Rueckschlagventil d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| ARM-rsv-d40 | PVC-U-Rueckschlagventil d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d110 | PVC-U-Bogen 45 Grad d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d20 | PVC-U-Bogen 45 Grad d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d25 | PVC-U-Bogen 45 Grad d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d32 | PVC-U-Bogen 45 Grad d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d40 | PVC-U-Bogen 45 Grad d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen45-d50 | PVC-U-Bogen 45 Grad d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 3.0 |
| FIT-bogen45-d63 | PVC-U-Bogen 45 Grad d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| FIT-bogen45-d75 | PVC-U-Bogen 45 Grad d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d110 | PVC-U-Bogen 90 Grad d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d20 | PVC-U-Bogen 90 Grad d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d25 | PVC-U-Bogen 90 Grad d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-bogen90-d32 | PVC-U-Bogen 90 Grad d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 8.0 |
| FIT-bogen90-d40 | PVC-U-Bogen 90 Grad d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 14.0 |
| FIT-bogen90-d50 | PVC-U-Bogen 90 Grad d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 19.0 |
| FIT-bogen90-d63 | PVC-U-Bogen 90 Grad d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 7.0 |
| FIT-bogen90-d75 | PVC-U-Bogen 90 Grad d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 8.0 |
| FIT-gewindenippel-edelstahl | Gewindenippel Edelstahl (Druckmessstelle) | leitung.json | - | Stk | Edelstahl | OFFEN | - | - |  | 0.0 |
| FIT-kappe-d16 | PVC-U-Kappe d16 | leitung.json | durchmesser_mm=16 | Stk | PVC-U | OFFEN | ja | Q |  | 42.0 |
| FIT-kappe-d20 | PVC-U-Kappe d20 | leitung.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | ja | Q |  | 5.0 |
| FIT-kappe-d25 | PVC-U-Endkappe d25 | leitung.json | durchmesser_mm=25 | Stk | PVC-U | OFFEN | ja | Q |  | 24.0 |
| FIT-kappe-d32 | PVC-U-Kappe d32 | leitung.json | durchmesser_mm=32 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-kappe-d50 | PVC-U-Kappe d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 24.0 |
| FIT-kupplung-d110 | PVC-U-Kupplung (Muffe) d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d20 | PVC-U-Kupplung (Muffe) d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d25 | PVC-U-Kupplung (Muffe) d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d32 | PVC-U-Kupplung (Muffe) d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d40 | PVC-U-Kupplung (Muffe) d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-kupplung-d50 | PVC-U-Kupplung (Muffe) d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 7.0 |
| FIT-kupplung-d63 | PVC-U-Kupplung (Muffe) d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-kupplung-d75 | PVC-U-Kupplung (Muffe) d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-leerrohr-bogen45-dn100 | Leerrohr-Bogen 45 Grad dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-bogen45-dn50 | Leerrohr-Bogen 45 Grad dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-bogen90-dn100 | Leerrohr-Bogen 90 Grad dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-bogen90-dn50 | Leerrohr-Bogen 90 Grad dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-red-dn100_dn50 | Leerrohr-Reduzierung dn100_dn50 | leitung.json | groesse=dn100_dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-t-dn100 | Leerrohr-T-Stueck dn100 | leitung.json | groesse=dn100 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-leerrohr-t-dn50 | Leerrohr-T-Stueck dn50 | leitung.json | groesse=dn50 | Stk | PVC-U | OFFEN | - | - |  | 0.0 |
| FIT-red-d110_d63 | PVC-U-Reduzierung d110_d63 | leitung.json | groesse=d110_d63 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d25_d20 | PVC-U-Reduzierung d25_d20 | leitung.json | groesse=d25_d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d32_d25 | PVC-U-Reduzierung d32_d25 | leitung.json | groesse=d32_d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d40_d20 | PVC-U-Reduzierung d40_d20 | leitung.json | groesse=d40_d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d40_d32 | PVC-U-Reduzierung d40_d32 | leitung.json | groesse=d40_d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-red-d50_d32 | PVC-U-Reduzierung d50_d32 | leitung.json | groesse=d50_d32 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-red-d50_d40 | PVC-U-Reduzierung d50_d40 | leitung.json | groesse=d50_d40 | Stk | PVC-U | OFFEN | ja | Q |  | 6.0 |
| FIT-red-d63_d50 | PVC-U-Reduzierung d63_d50 | leitung.json | groesse=d63_d50 | Stk | PVC-U | OFFEN | ja | Q |  | 8.0 |
| FIT-red-d75_d50 | PVC-U-Reduzierung d75_d50 | leitung.json | groesse=d75_d50 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-red-d75_d63 | PVC-U-Reduzierung d75_d63 | leitung.json | groesse=d75_d63 | Stk | PVC-U | OFFEN | ja | Q |  | 6.0 |
| FIT-reduktion-d16 | PVC-U-Reduktion/Huelse d16 | leitung.json | durchmesser_mm=16 | Stk | PVC-U | OFFEN | - | - |  | 28.0 |
| FIT-reduktion-d32 | PVC-U-Reduktion/Huelse d32 | leitung.json | durchmesser_mm=32 | Stk | PVC-U | OFFEN | - | - |  | 14.0 |
| FIT-reduktion-d50 | PVC-U-Reduktion/Huelse d50 | leitung.json | durchmesser_mm=50 | Stk | PVC-U | OFFEN | - | - |  | 14.0 |
| FIT-rinne-kappe-ablauf | Rinnen-Endkappe Ablauf 130x100 | leitung.json | - | Stk | PVC-U weiss | OFFEN | - | - |  | 76.0 |
| FIT-rinne-kappe-zulauf | Rinnen-Endkappe Zulauf 130x100 | leitung.json | - | Stk | PVC-U weiss | OFFEN | - | - |  | 76.0 |
| FIT-stutzen-d16 | PVC-U-Stutzen d16 (Klebe/Gewinde) | leitung.json | durchmesser_mm=16 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| FIT-stutzen-d20 | PVC-U-Stutzen d20 (Klebe/Gewinde) | leitung.json | durchmesser_mm=20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-stutzen-d32 | PVC-U-Stutzen d32 (Klebe/Gewinde) | leitung.json | durchmesser_mm=32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-stutzen-d40 | PVC-U-Stutzen d40 (Klebe/Gewinde) | leitung.json | durchmesser_mm=40 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| FIT-stutzen-d63 | PVC-U-Stutzen d63 (Klebe/Gewinde) | leitung.json | durchmesser_mm=63 | Stk | PVC-U | OFFEN | ja | Q |  | 2.0 |
| FIT-t-d110 | PVC-U-T-Stueck d110 | leitung.json | groesse=d110 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d20 | PVC-U-T-Stueck d20 | leitung.json | groesse=d20 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d25 | PVC-U-T-Stueck d25 | leitung.json | groesse=d25 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d32 | PVC-U-T-Stueck d32 | leitung.json | groesse=d32 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d40 | PVC-U-T-Stueck d40 | leitung.json | groesse=d40 | Stk | PVC-U | OFFEN | ja | Q |  | 0.0 |
| FIT-t-d50 | PVC-U-T-Stueck d50 | leitung.json | groesse=d50 | Stk | PVC-U | OFFEN | ja | Q |  | 3.0 |
| FIT-t-d63 | PVC-U-T-Stueck d63 | leitung.json | groesse=d63 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
| FIT-t-d75 | PVC-U-T-Stueck d75 | leitung.json | groesse=d75 | Stk | PVC-U | OFFEN | ja | Q |  | 4.0 |
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
| ROH-pvcu-d20 | PVC-U-Druckrohr d20 (Meterware) | leitung.json | durchmesser_mm=20 | m | PVC-U | OFFEN | ja | Q |  | 28.33 |
| ROH-pvcu-d25 | PVC-U-Druckrohr d25 (Meterware) | leitung.json | durchmesser_mm=25 | m | PVC-U | OFFEN | ja | Q |  | 8.63 |
| ROH-pvcu-d32 | PVC-U-Druckrohr d32 (Meterware) | leitung.json | durchmesser_mm=32 | m | PVC-U | OFFEN | ja | Q |  | 2.49 |
| ROH-pvcu-d40 | PVC-U-Druckrohr d40 (Meterware) | leitung.json | durchmesser_mm=40 | m | PVC-U | OFFEN | ja | Q |  | 12.53 |
| ROH-pvcu-d50 | PVC-U-Druckrohr d50 (Meterware) | leitung.json | durchmesser_mm=50 | m | PVC-U | OFFEN | ja | Q |  | 33.41 |
| ROH-pvcu-d63 | PVC-U-Druckrohr d63 (Meterware) | leitung.json | durchmesser_mm=63 | m | PVC-U | OFFEN | ja | Q |  | 7.78 |
| ROH-pvcu-d75 | PVC-U-Druckrohr d75 (Meterware) | leitung.json | durchmesser_mm=75 | m | PVC-U | OFFEN | ja | Q |  | 8.18 |
| SCH-rohrschelle-d110 | Rohrschelle (Klemme, Stahl) d110 | leitung.json | groesse=d110 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d20 | Rohrschelle (Klemme, Stahl) d20 | leitung.json | groesse=d20 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d25 | Rohrschelle (Klemme, Stahl) d25 | leitung.json | groesse=d25 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d32 | Rohrschelle (Klemme, Stahl) d32 | leitung.json | groesse=d32 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d40 | Rohrschelle (Klemme, Stahl) d40 | leitung.json | groesse=d40 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d50 | Rohrschelle (Klemme, Stahl) d50 | leitung.json | groesse=d50 | Stk | Stahl | - | ja | Q |  | 0.0 |
| SCH-rohrschelle-d63 | Rohrschelle d63 (Stahl verzinkt, Doppelschelle) | leitung.json | - | Stk | Stahl verzinkt | - | - | - |  | 4.0 |
| SCH-rohrschelle-vk-vk_d32 | Rohrschelle VK vk_d32 | leitung.json | groesse=vk_d32 | Stk | Stahl | - | - | - |  | 0.0 |
| SCH-rohrschelle-vk-vk_d63 | Rohrschelle VK vk_d63 | leitung.json | groesse=vk_d63 | Stk | Stahl | - | - | - |  | 0.0 |
| SCH-schlauch-id16 | Schlauch ID16 (Meterware) | leitung.json | nennweite=id16 | m | PVC/PE | - | - | - |  | 0.0 |
| SCH-schlauch-id25 | Schlauch ID25 (Meterware) | leitung.json | nennweite=id25 | m | PVC/PE | - | - | - |  | 0.0 |
| SCH-schlauch-rinne-id16 | Schlauch ID16, 110 mm Stueck (Rinne Zulauf) | leitung.json | - | Stk | PVC/PE | - | - | - |  | 76.0 |
| SCH-schlauchbogen90-id16 | Schlauchbogen 90 Grad id16 | leitung.json | groesse=id16 | Stk | Kunststoff | - | - | - |  | 0.0 |
| SCH-schlauchbogen90-id25 | Schlauchbogen 90 Grad id25 | leitung.json | groesse=id25 | Stk | Kunststoff | - | - | - |  | 0.0 |
| SCH-schlauchschelle-id16 | Schlauchschelle id16 | leitung.json | groesse=id16 | Stk | Kunststoff | - | ja | Q |  | 0.0 |
| SCH-schlauchschelle-id25 | Schlauchschelle id25 | leitung.json | groesse=id25 | Stk | Kunststoff | - | ja | Q |  | 0.0 |
| SCH-schlauchtuelle-d12 | Schlauchtuelle (PVC) | leitung.json | - | Stk | PVC | - | ja | Q |  | 0.0 |
| SCH-schlauchtuelle-d25 | Schlauchtuelle d25 (PVC) | leitung.json | - | Stk | PVC | - | ja | Q |  | 4.0 |
| ELE-hutschiene-35 | Hutschiene 35 mm | mess_elektrik.json | - | Stk | Stahl verzinkt | - | ja | Q-Treffer |  | 0.0 |
| ELE-kabelkanal-30x60 | Kabelkanal PVC 30x60 | mess_elektrik.json | - | m | PVC | - | ja | Q-Treffer |  | 0.0 |
| ELE-kabelverschraubung-pg | Kabelverschraubung PA (PG/M20) | mess_elektrik.json | - | Stk | PA schwarz | - | ja | Q-Treffer |  | 1.0 |
| ELE-schaltschrank-500x800x1200 | Schaltschrank 500x800x1200 mm (leer, Ausruestung o | mess_elektrik.json | - | Stk | - | - | ja | E |  | 1.0 |
| MES-co2-scd41 | Sonde co2_scd41 (Typ und Fabrikat offen: docs/rese | mess_elektrik.json | bbox_mm=[10, 17, 25] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-do-ind | Sonde do_ind (Typ und Fabrikat offen: docs/researc | mess_elektrik.json | bbox_mm=[25, 25, 170] | Stk | - | OFFEN | - | - |  | 1.0 |
| MES-do-mini | Sonde do_mini (Typ und Fabrikat offen: docs/resear | mess_elektrik.json | bbox_mm=[12, 12, 110] | Stk | - | OFFEN | ja | Q |  | 3.0 |
| MES-druck-schalter | Sonde druck_schalter (Typ und Fabrikat offen: docs | mess_elektrik.json | bbox_mm=[32, 32, 55] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-ec | Sonde EC (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | Q |  | 1.0 |
| MES-flow-12 | Sonde flow_12 (Typ und Fabrikat offen: docs/resear | mess_elektrik.json | bbox_mm=[40, 50, 80] | Stk | - | OFFEN | ja | Q-Treffer | ERSATZ | 0.0 |
| MES-flow-gross | Sonde flow_gross (Typ und Fabrikat offen: docs/res | mess_elektrik.json | bbox_mm=[40, 60, 100] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-leck | Sonde leck (Typ und Fabrikat offen: docs/research/ | mess_elektrik.json | bbox_mm=[6, 20, 50] | Stk | - | OFFEN | ja | Q-Treffer |  | 3.0 |
| MES-level-druck | Sonde level_druck (Typ und Fabrikat offen: docs/re | mess_elektrik.json | bbox_mm=[20, 20, 140] | Stk | - | OFFEN | - | - |  | 1.0 |
| MES-level-float | Sonde level_float (Typ und Fabrikat offen: docs/re | mess_elektrik.json | bbox_mm=[30, 30, 55] | Stk | - | OFFEN | ja | Q |  | 3.0 |
| MES-o2 | Sonde O2 (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | A |  | 0.0 |
| MES-par | Sonde par (Typ und Fabrikat offen: docs/research/R | mess_elektrik.json | bbox_mm=[30, 30, 37] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-ph | Sonde pH (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | Q |  | 3.0 |
| MES-strom-ct | Sonde strom_ct (Typ und Fabrikat offen: docs/resea | mess_elektrik.json | bbox_mm=[13, 30, 36] | Stk | - | OFFEN | ja | Q-Treffer |  | 0.0 |
| MES-temp-ds | Sonde temp_ds (Typ und Fabrikat offen: docs/resear | mess_elektrik.json | bbox_mm=[6, 6, 50] | Stk | - | OFFEN | ja | Q |  | 2.0 |
| MES-temperatur | Sonde Temperatur (Stationsmessplatz) | mess_elektrik.json | bbox_mm=[14, 14, 245] | Stk | - | OFFEN | ja | A |  | 0.0 |
| BLE-blech-st-3 | Stahlblech 3 mm verzinkt, Zuschnitt 700x700 | stahl.json | dicke_mm=3, zuschnitt_mm=[700, 700] | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 5.0 |
| BLE-blech-st-5 | Stahlblech 5 mm verzinkt, Zuschnitt 840x400 | stahl.json | dicke_mm=5, zuschnitt_mm=[840, 400] | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| BLE-blech-st-6 | Stahlblech 6 mm verzinkt, Zuschnitt 1360x580 | stahl.json | dicke_mm=6, zuschnitt_mm=[1360, 580] | Stk | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| BLE-fussplatte-100x100x6 | Fussplatte Stahl verzinkt 100x100x6 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E | ERSATZ | 16.0 |
| BLE-fussplatte-150x150x8 | Fussplatte Stahl verzinkt 150x150x8 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 0.0 |
| BLE-fussplatte-200x200x8 | Fussplatte Stahl verzinkt 200x200x8 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 0.0 |
| BLE-fussplatte-70x70x5 | Fussplatte Stahl verzinkt 70x70x5 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 76.0 |
| BLE-fussplatte-80x80x6 | Fussplatte Stahl verzinkt 80x80x6 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E | ERSATZ | 12.0 |
| BLE-fussplatte-80x80x8 | Fussplatte Stahl verzinkt 80x80x8 mm | stahl.json | - | Stk | Stahl verzinkt | OFFEN | ja | E |  | 0.0 |
| BLE-platte-250x250x15 | Ankerplatte 250x250x15 mm, Stahl | stahl.json | - | Stk | Stahl Anker | OFFEN | ja | E |  | 10.0 |
| BLE-pp-blende-290x260 | PP-Blende 290x260x3 (Messzelle) | stahl.json | - | Stk | PP schwarz | OFFEN | ja | E |  | 1.0 |
| BLE-pp-siebboden-beet | PP-Siebboden 8 mm (Zuschnitt je Beet) | stahl.json | dicke_mm=8 | Stk | PP grau | OFFEN | - | - |  | 14.0 |
| BLE-pp-tafel-502x345x5 | PP-Montagetafel 502x345x5 (Zuschnitt) | stahl.json | - | Stk | PP Tafel | OFFEN | ja | E |  | 4.0 |
| BLE-pp-tafel-693x463x7 | PP-Montagetafel 693x463x7 (Zuschnitt) | stahl.json | - | Stk | PP Tafel | OFFEN | ja | E |  | 4.0 |
| BLE-v2a-3mm-korbflansch | Edelstahlblech 3 mm 1.4301, Zuschnitt 604x414 (Kor | stahl.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | E |  | 2.0 |
| BLE-v2a-lochblech-medienschutz | Edelstahl-Lochblech 1,5 mm RV5-8, Medienschutz-Zyl | stahl.json | - | Stk | Edelstahl 1.4301 | OFFEN | ja | E |  | 14.0 |
| PRF-alu-haut-profil | Alu-Kappenprofil der Haut | stahl.json | - | m | Aluminium | OFFEN | ja | Q | ERSATZ | 0.0 |
| PRF-alu-keilschiene | Alu-Keilschiene (Kanal 25x15) | stahl.json | - | m | Aluminium | OFFEN | ja | Q | ERSATZ | 0.0 |
| PRF-alu-klemmleiste | Alu-Klemmleiste Zarge | stahl.json | - | m | Aluminium Zarge | OFFEN | ja | Q | ERSATZ | 0.0 |
| PRF-pvcu-rinne-130x100 | NFT-Rinnenprofil PVC-U 130x100 (Meterware, Lagerla | stahl.json | querschnitt_mm=[100, 130] | m | PVC-U weiss | OFFEN (Bemerkung verneint) | ja | Q | ERSATZ | 147.92 |
| PRF-st-rr25x25x2 | Vierkantrohr 25x25x2 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[25, 25], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-rr30x30x2 | Vierkantrohr 30x30x2 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[30, 30], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 24.88 |
| PRF-st-rr40x40x2 | Vierkantrohr 40x40x2 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-rr40x40x2.5 | Vierkantrohr 40x40x2.5 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | E | ERSATZ | 158.41 |
| PRF-st-rr40x40x3 | Vierkantrohr 40x40x3 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 40], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 10.67 |
| PRF-st-rr40x60x3 | Rechteckrohr 40x60x3 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[40, 60], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 40.44 |
| PRF-st-rr60x60x3 | Vierkantrohr 60x60x3 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[60, 60], norm_hinweis=Wa | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-rund20 | Rundstahl 20 mm, Stahl verzinkt | stahl.json | querschnitt_mm=[20, 20], norm_hinweis=Ru | m | Stahl verzinkt | OFFEN | ja | Q |  | 0.0 |
| PRF-st-strebe30x30 | Strebenprofil 30x30 (Kuppelstrebe, Profil und Wand | stahl.json | querschnitt_mm=[30, 30] | m | Stahl verzinkt | OFFEN | ja | Q |  | 209.08 |
| PRF-v2a-voll8x8 | Vierkant-/Flachstahl voll 8x8 mm, Edelstahl 1.4301 | stahl.json | querschnitt_mm=[8, 8], norm_hinweis=Voll | m | Edelstahl 1.4301 | OFFEN | ja | Q |  | 6.77 |
| SRB-halter-klein-12x10x20 | Kleinteil am Winkelhalter 12x10x20 (Schraube/Mutte | stahl.json | - | Stk | Stahl verzinkt | - | - | - |  | 456.0 |
| SRB-satz-m6x20 | Schraubensatz M6x20 (Sechskantschraube DIN 933 + M | stahl.json | gewinde=M6, laenge_mm=20 | Satz | Stahl verzinkt | - | ja | E | ERSATZ | 16.0 |
| WNK-flach-14x3 | Flachstahl 14x3 (Tuer-Anschlag) | stahl.json | - | m | Stahl verzinkt | - | ja | E | ERSATZ | 5.0 |
| WNK-flach-3mm-diagonale | Flachstahl 3 mm (Diagonalen, Breite aus Modell nic | stahl.json | dicke_mm=3 | Stk | Stahl verzinkt | - | - | - |  | 110.0 |
| WNK-pumpenkonsole | Pumpenkonsole/Standwinkel (Stahl, Zuschnitt) | stahl.json | - | Stk | Stahl Pumpe | - | ja | Q-Treffer | ERSATZ | 24.0 |
| WNK-rinnenhalter-25 | Rinnenhalter 25x25 (Stahl, Zuschnitt/Kleinteil) | stahl.json | - | Stk | Stahl verzinkt | - | ja | E | ERSATZ | 304.0 |
| WNK-wandlasche-30x30x3 | Wandlasche 30x30x3 | stahl.json | - | Stk | Stahl verzinkt | - | ja | E | ERSATZ | 0.0 |
| WNK-winkel-36x60x60 | Winkel 36x60x60 (Rinnen-Winkelhalter, Stahl) | stahl.json | - | Stk | Stahl verzinkt | - | ja | Q-Treffer | ERSATZ | 76.0 |
