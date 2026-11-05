# N-PREIS-PRUEF 1E: Hülle und Pflanzbereich (`data/beschaffung/huelle_pflanze.json`)

Stand 05.11.2026. Gruppe E, 40 Zeilen. Gelesen heißt: Seite per WebFetch geöffnet. Suchtreffer sind als solche gekennzeichnet. Nichts gekauft, nirgends angemeldet.

**Problem:** Links der Gruppe E zeigten auf Startseiten, 404, falsche Artikel oder gesperrte Seiten.
**Intent:** Jede Zeile ein bestellbares, passendes Teil (D76: mindestens Europa, zwei unabhängige Quellen).
**Ziel:** Jede der 40 Zeilen ist ersetzt, bestätigt oder OFFEN mit Grund (Feld `luecke`).

## Ersetzt (zwei oder mehr gelesene Quellen)
1. `FOL-pe-plane`: Startseiten-Links stretchfolie.eu und norhage.de entfernt. Neu: gekaho-shop.de (200 my, UV4), haga-welt.de (150 um, UV5), Aquagart über billiger.de. Kein Angebot mit 200 um und UV5 zugleich, daher trotzdem OFFEN (Quelle) und OFFEN (Ben): Mass.
2. `TOP-blaehton`: drei DE-Händler (natursteinzentrum-rm.de, kiesdirekt.de, kiesundco.de), 314 bis 528 EUR/m3. Richtwert 424 EUR/m3 statt 330.
3. `SON-polycarbonat-paneel`: drei DE-Händler, 14,72 bis 17,95 EUR/m2 (Voelkner ausverkauft).

## Bestätigt
1. `SON-tuerscharnier`: der-technikprofi.de liefert, Hornbach nur Abholung.
2. `SON-tuerdruecker`: mein-tuergriff.de und habefa.de. Preis je Wechselgarnitur (1 Satz).

## OFFEN mit Grund (Quelle)
1. `TOP-biomedium`: kein EU-Händler mit lieferbarem K1 je m3. Wiltec 404, Absolute Koi UK.
2. `TOP-netztopf-64`: kein 64-mm-Topf. 2-Zoll-Töpfe belegt, kein Staffelpreis.
3. `GEW-v2a-100um`: 100 um in 1.4301 belegt (laborsieb.de, rotec-berlin.de), Preis nur auf Anfrage.
4. `SON-pp-stuetze-60x60`: kein PP-Vierkant. plastx24.de Rundstab d60 27,00 EUR netto je m.
5. `FOL-epdm-tuerdichtung`: nur Graf-Datenblatt (1,64 EUR/m), zweite Quelle fehlt.
6. `FOL-epdm-schaumband`: nur Bürklin (Suchtreffer, 403). Ahlsell SE ohne Preis.
7. `FOL-epdm-dichtband-zarge`: Maß nicht festgelegt, keine Produktseite.
8. `FOL-epdm-dichtung-630x440`: nur diconfa.de (4,23 EUR/Stk), zweite Quelle fehlt.
9. `SON-tuerblatt-1000x2000`: nur garagenonline.eu (Komplettür ab 749 EUR). Einzelblatt Domoferm nur Suchtreffer.
10. `SON-spannverschluss-edelstahl`: schraubbar.de und elesa-ganter.at gelesen, Güte A2 nicht belegt (1.4308/1.4305).
11. `SON-federdraht-d2`: kein Preis auf geöffneter Seite.
12. `SON-korbgriff-v2a`: Ganter 12/160 bei profishop.de, Güte 1.4301 nicht belegt, Halder (125 mm) entfernt.
13. `SON-knotenkugel-d100`: nur Hohlkugeln (fenau.eu 5,37 EUR, edelstahl-handel.com 4,35 EUR). Nicht als Angebot eingetragen, weil sie sonst den Preis der Vollkugel überschreiben würden.
14. `SON-belueftungsgitter-460`: kein Kunststoffgitter 460x460.
15. `SON-schacht-kugelhahn-d63`: nicht recherchiert, Bedarf im Modell 0.
16. 18 Eigenbau-Zeilen (Halter, Siebe, Plattformen, Knotenarm, Ankerlasche, Tauchklemme u.a.): kein Kaufteil, Preis angenommen (A).
17. `SON-pflanztisch-platte`, `SON-tuer-modellvariante`: Altmodell, Bedarf 0, entfallen.

## OFFEN (Ben)
1. Folie: 150 um (UV5) statt 200 um akzeptabel?
2. Netztopf: 2 Zoll (ca. 50 mm) statt 64 mm.
3. Knotenkugel: Hohlkugel statt Vollkugel (4 kg), hängt an N-STATIK W43.
4. Tür: Komplettür statt Blatt, Scharnier und Drücker?
5. Lüftungsgitter: Metall 450x450 statt Kunststoff 460x460?
6. Dichtband Zarge: Maß festlegen.

## Hinweise
1. Das Lochblech mit dem Amazon-404 (`BLE-v2a-lochblech-medienschutz`) liegt in `stahl.json`, nicht in dieser Gruppe. Nicht angefasst.
2. Lecaton-Seite nennt "1 Tonne" bei 1,5 m3. Beim Händler klären.
3. Lebensmitteleignung: bei Blähton, Netztopf, Folie auf keiner gelesenen Seite belegt. Nach vorläufiger Entscheidung nichts ersetzt, nur Befund.
4. Zwei Quellen mit lieferbarem DE-Händler gelten als erfüllt. Zeilen mit einer Quelle tragen das Angebot weiter, `luecke` benennt die fehlende zweite.
5. Die Preise stammen von drei Teil-Recherchen. Seiten wurden vom jeweiligen Rechercheur gelesen, ich habe sie nicht erneut geöffnet.
