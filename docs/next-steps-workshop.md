# Naechste Schritte Werkstatt (Rolle W) — rollender Plan, immer 3-5 definierte Schritte

Besitzer: Orchestrator (fuellt auf). Die Werkstatt liest diese Datei als Erstes, arbeitet den obersten Schritt ab, hakt ihn im Log ab und meldet dem Orchestrator, sobald nur noch 2 Schritte uebrig sind (oder fertig ist). Es darf nie ohne definierten naechsten Schritt dastehen. Je Schritt: Ziel · Eingaben/Quellen · Ergebnis (DoD) · Pruefung · Abhaengigkeit. Pruefung immer nach `docs/review-protocol.md` (Scope-Card, Kontextpaket, Vorpruefung, Bild-Kritiker + Spec-Pruefer, Triage) und Herkunftstabelle nach `docs/provenance.md`.

## Jetzt (laeuft)
**W1 Abschluss der Vorarbeit:** Netztopf, Salatkopf, NFT-Rinne durch Kritiker und Spec-Pruefer bringen, Bauteilblaetter vollstaendig (Herkunftstabelle), Fertigmeldung je Klasse an den Orchestrator. DoD: Vorpruefung PASS, Kritiker keine grosse Luecke in zwei Runden, Blatt vollstaendig.

## Naechste Schritte
**W2 NFT-Tisch (innen, mitte, aussen):** Ziel: je Ring eine Tisch-Komponente aus Rinnen-Instanzen.
- Eingaben: `docs/scope-cards.md` (nft_tisch), `docs/components.md` Abschnitt NFT-Ringe (innen 2 Rinnen Laenge 1304 Apothem 1733/1995; mitte 4 x 1983; aussen 3 x 3232, Abstand 262-288), ref-6, R06 falls fertig.
- Ergebnis: `designs/components/nft_tisch_{innen,mitte,aussen}.sc` mit Beinen (`frame.profile.insert`), Querstreben, Diagonalen, Fussplatten, Gefaelle 1 cm/m (0,573 Grad), **Zickzack = Versatz benachbarter Rinnen um pitch/2**, Zulaufverteiler mit einem Schlauchanschluss je Rinne, Sammelablauf, Ports benannt.
- Pruefung: Vorpruefung (Rinnenzahl, Abstand, Versatz pitch/2, Hoehe Z laut `layout.json`), Kritiker + Spec-Pruefer, Bauteilblatt.
- Abhaengigkeit: W1.

**W3 IBC-Beet (aussen, innen):** Ziel: Beet-Komponente nach R03.
- Eingaben: `docs/research/R03.md`, Scope-Card ibc_beet, layout.json (2953 x 933-993 x 637 bzw. 1865 x 933 x 649, Unterkante Z -160...-210).
- Ergebnis: Wanne (Wandstaerke 3-4 mm), Medium als EIN Koerper (Oberflaeche Z 400, Tiefe 300), Siebboden, Standrohr Ø25 x 220, Glocke Ø75 x 250 mit Schlitzen und Luftloch, Medienschutz Ø110 x 320, Ablauf-Bulkhead, Zulauf-Tropfrohr, Ports; Pflanzen NICHT enthalten (Instanzen aus Layout).
- Pruefung: Vorpruefung (Medienoberflaeche Z 400, Standrohrhoehe, Masse), Kritiker, Blatt.
- Abhaengigkeit: keine.

**W4 Tank klein (Vortex-Absetzer):** Ziel: Tank-Komponente mit Kegel.
- Eingaben: Scope-Card tank_klein, layout.json (Ø673, Hoehe 1075 inkl. Kegel, Plattform 706 x 707 x 73 auf Z 428, Beine 30 x 30 x 751, Fittings 30-40 an der Kegelspitze), R09 falls fertig.
- Ergebnis: Zylinder + Kegel (45-60 Grad), tangentialer Zulauf, Mittelrohr, Schlammventil, Deckel, Plattform, 4 Beine mit Diagonalen und Fussplatten, Fittings als Ports (Bulkhead mit Dichtung).
- Pruefung: Vorpruefung (Kegel vorhanden, Fitting an Kegelspitze), Kritiker, Blatt.

**W5 Tank gross (Biofilter):** wie W4 mit Ø930, Hoehe 1444, Plattform 977 x 976 x 98 auf Z 570, Beine 40 x 40 x 1008; Biofilter-Einbauten als Platzhalter (Biomedium-Korb als EIN Koerper), Belueftungsanschluss.

## Reserve (rueckt nach, wenn ein Schritt fertig ist)
W6 Pumpe/Filtermodul (OBJ-Module 502 x 345, 384 x 419, Platte 693 x 463) · W7 Salatkopf-Varianten S/M/L fuer Beet und Rinne feinern · W8 Haut-Paneel (R11, falls fertig).

## Auffuellung 29.10. 08:25 (Orchestrator) — W1-W6 gebaut/abgenommen, ab hier arbeiten
**W7 Abschluss Netztopf und Salatkopf:** Netztopf-Spec-Pruefer, Salatkopf-Kritiker Runde 3 (Kontextpaket), Fertigmeldung. Salatkopf sieht aus wie gestapelte Scheiben, ref-4/ref-6 zeigen buschige Salatkoepfe: Form feinern (mehr Blaetter, Falten), wenige Facetten halten (Export!). Pruefung: Vorpruefung, Bild-Kritiker (Ausschnitt ref-6 NUR Salatkopf), Blatt. Abhaengigkeit: keine.
**W8 Knoten 4/5/6 (R02, Scope-Card `knoten_*`):** isoliert bauen: Platten/Huelsen, Normschrauben M10, Armrichtungen aus `layout.json`; drei Komponenten, Konfigurationen je Knoten moeglich. Ergebnis: `designs/components/knoten_{4,5,6}.sc`, Vorpruefung (Armzahl, Winkel), Blatt mit Herkunft, Kritiker + Spec-Pruefer. Abhaengigkeit: Scope-Card (steht).
**W9 Fundamentanker (Scope-Card `fundamentanker`):** Ankerplatte, Bolzen, Betonpunkt; ein Bauteil. Pruefung wie oben.
**W10 Leitungsteile-Bibliothek (Scope-Card `rohr...verteiler`):** Rohr (DN 25/32/50/110), Bogen 90/45, T-Stueck, Kugelhahn, Kupplung, Schlauchstueck, Klemme/Halter, Verteiler als Komponenten mit Ports; die Montage verlegt sie (M5). Ergebnis: je Teil Datei + Sammelblatt `docs/parts/leitungsteile.md` mit Herkunft; Vorpruefung (DN, Ports, Biegeradius).
**W11 Reserve:** Winkelhalter am Beinkopf der NFT-Tische (L4), Beine/Plattform des Tanks klaeren (Beine ueber Plattform: Zweck im OBJ pruefen), Haut-Paneel (R11 steht aus).
Hinweis: Die Montage-Sitzung laeuft derzeit nicht; Komponenten-DEFINITIONEN (isoliert) fuer Knoten, Anker und Leitungsteile liegen deshalb vorerst bei der Werkstatt, die Platzierung in `dome.sc` bleibt bei der Montage.

## Auffuellung 29.10. 12:20 (Orchestrator) — W8-W10 erledigt, offen: W7, W11, ab hier W12-W15
Reihenfolge: W7 · W12 · W13 · W14 · W15 · W11. Limit ist zurueckgesetzt (5h 14 %); kleine Schritte, Checkpoint vor jedem, Commit mit Pfad + Push nach jedem.
**W12 Pumpe und Knoten/Anker Abschluss:** Pumpe-Spec-Pruefer (Herkunftstabelle, Blatt) und Salatkopf/Netztopf-Blaetter nachziehen, Fertigmeldung an Orchestrator. Pruefung: Vorpruefung, Spec-Pruefer, Triage im Log. Abhaengigkeit: keine.
**W13 Strebe A/B als Komponenten (isoliert):** Ziel: `strebe_a.sc` (30 Stk.) und `strebe_b.sc` (35 Stk.) als Rohr 30x30 mit Laenge laut layout.json (0,5465 R / 0,618 R), Steckenden fuer Knotenkugel-Arme (D15), Ports an beiden Enden. Eingaben: layout.json, R02, Scope-Card knoten_*. Ergebnis: Dateien, Vorpruefung (Laenge, Profil, Ports), Blatt mit Herkunft E/A. Abhaengigkeit: keine.
**W14 Tuer komplett (isoliert):** Ziel: `tuer_komplett.sc` als Komponente (Rahmen, Blatt, Scharniere, Schwelle) im Basisfeld BBB 149,2 (Apex Z 3140, D36), Breite 1353 mm in 2 m Hoehe (erledigt als W20: tuer_komplett.sc) (siehe docs/components.md, Tuer-Recherche); vorhandenes `tuer.sc` pruefen und nur bei Mangel ersetzen. Pruefung: Vorpruefung (Mass in Dreieck), Bild-Kritiker (ref-4), Blatt. Abhaengigkeit: keine.
**W15 Pool und zweites Becken (isoliert):** Ziel: Komponenten `pool.sc` (Ø3890, Gesamttiefe 2340, Wasserspiegel Z 515, Rand Z 650 laut D08) und `zweitbecken.sc` pruefen/feinern (Wandstaerke, Rand, Einlauf/Ablauf-Ports, eingelassener Teil sichtbar im Schnitt). Pruefung: Vorpruefung (Masse D08), Schnitt-Render, Blatt. Abhaengigkeit: keine.

## KORREKTUR 29.10. 13:55 (Orchestrator): W13-W15 gestrichen, Auftraege jetzt als Blaetter
W13 Strebe, W14 Tuer, W15 Pool/Zweitbecken liegen bei der Montage (Zwischenbauteile; `strebe_a/b`, `tuer`, `pool_zentral`, `zweitbecken` stammen aus gen_dome.py bzw. components/strebe.py): die Auffuellung von 12:20 war eine Dublette. Werkstatt-Reihenfolge ab jetzt: W10-Abschluss, W12 Pumpe, W7 Salatkopf, W11 Winkelhalter. Jeder Auftrag steht als Blatt in `docs/jobs/` (Lesen: nur Blatt + cad-standard + detail-standard).

REIHENFOLGE 13:45: W10 fertig, W12 Pumpe (laeuft), dann **W16 NFT-Tische Passung** (docs/jobs/W16-nft-tisch-passung.md, D18), danach W7, W11.

REIHENFOLGE 19:55: W11 (laeuft) -> **W17 Radialbudget** (docs/jobs/W17-radialbudget.md, D28) -> Haut-Paneel nach R11. Pflanzenartmodelle (7 Arten laut R15) hinten angestellt (D27).

REIHENFOLGE 22:05: nach dem Neustart: W17-Spec-Pruefer -> **W18 Lochabstand 200 mm** (docs/jobs/W18-lochabstand.md, D32, R16) -> Haut-Paneel R11.

REIHENFOLGE 30.10. 11:30: **W20 Tuer komplett** (docs/jobs/W20-tuer-komplett.md, D36) -> W21 Pruefer W19 (docs/jobs/W21-pruefer-w19.md) -> weitere Auftraege nach Fachrecherche (Pumpen/Hauptkreislauf).

REIHENFOLGE 30.10. 13:10: W20/W21 fertig (check_haut 28/28, check_tuer 30/30). Jetzt **W22 Haut nacharbeiten** (docs/jobs/W22-haut-nacharbeit.md, D37) -> **W23 Spec-Pruefer W17+W18** (docs/jobs/W23-spec-pruefer-w17-w18.md) -> W24 Pumpen-Blatt (nach Fachrecherche-Integration, D38).
REIHENFOLGE 30.10. 14:00: nach W23 -> **W24 Aussentisch 4 Rinnen** (docs/jobs/W24-aussentisch-4-rinnen.md, Ben-Idee) -> W25 Pumpen-Blatt (D38). Haut-Paneel ruht (D39: Huelle ist eine Plane); Plane-Bauteile erst nach R24.
REIHENFOLGE 30.10. 14:30: W24 fertig (aussen4, 674 Toepfe, D43). Jetzt **W25a**: aussen4 als Standard in nft_tisch.json setzen (Parameter, Blaetter, Topfzahl 674, nft_pots-Quelle fuer Montage), dann **W25 Pumpen-Blatt** (D38). Pruefer nur EIN Lauf fuer nft_tisch aussen4 gemeinsam mit W25 (Limit sparen).
REIHENFOLGE 30.10. 15:00 (nach Reset): **W25a** aussen4 als Standard (D43) -> **W26 Innenbeet-Ecken anfasen** (W-M4, D44: Fase 120 mm in ibc_beet innen, Rueckfall Laenge 1790; Beet x Beet >= 0 pruefen, Topfraster/Topfzahl neu) -> **W25 Pumpen-Blatt** (D38). Montage uebernimmt danach: extract_nft_pots, build, check_latte, dann M3 Tuer.
REIHENFOLGE 31.10. 00:30: Limit neu (5h 8 %, Woche 14 %). Reihenfolge unveraendert: W25a (aussen4 Standard, D43) -> W26 (Innenbeet-Ecken anfasen, D44) -> W25 (Pumpen-Blatt, D38). Pruefer EIN gemeinsamer Lauf am Ende. Huelle (Plane) erst danach: W27 huelle_folie/keilschiene nach R24 (Orchestrator schreibt das Blatt).
REIHENFOLGE 31.10. 01:10 (D46): W25a -> W26 -> **W28 Puffer-Station** (docs/jobs/W28-puffer-ibc.md) -> W25 Pumpen-Blatt -> W27 Huelle. Montage platziert danach per M8.
REIHENFOLGE 31.10. 01:40 (Ben: IBC und Dosierkonsole sofort sichtbar machen): aktuellen Schritt (W25a) fertig, DANN **W28 Puffer-Station** (docs/jobs/W28-puffer-ibc.md), dann W26 Innenbeet-Fase, dann W25 Pumpen-Blatt, W27 Huelle. Platz geprueft (Orchestrator): Sektor 185,2 frei, Stapel Aussenkante r <= ca. 5150 (Wand neigt 10,8 Grad, 100 mm Abstand), Innenkante ca. 4150, Tank 4 (213 Grad) und Tank 1 (123 Grad) sind >= 2 m entfernt.
REIHENFOLGE 31.10. 02:40: nach W28 -> **W29 Mensch-Referenz** (docs/jobs/W29-mensch-referenz.md, D47) -> W27 Huelle (Plane).
REIHENFOLGE 31.10. 04:00 (D50): W30 Tank-Staende verkleinern (docs/jobs/W30-tank-staende.md), dann W27 Huelle. Danach Pause fuer den Zwischencheck.
REIHENFOLGE 31.10. 05:00 (D51): W30 fertig (f40d967). Jetzt W31 Feinfilter (docs/jobs/W31-feinfilter.md), dann W27 Huelle. Immer nur EINE Sitzung gleichzeitig.
REIHENFOLGE 31.10. 14:00 (D55): W32 Biofilter K1 und Feinfilter im Hauptstrom (docs/jobs/W32-biofilter-feinfilter.md).
REIHENFOLGE 31.10. 16:30 (D60): W33 Tischhoehe 1000 (docs/jobs/W33-tischhoehe-1000.md). Danach Fachrecherche R36 (docs/jobs/R36-beete-unter-tischen.md), dann Montage (Innenbeete D52, Neubau, Laufwegkarte D54, Leitungsplan).
