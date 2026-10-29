# Scope-Cards der Bauteilklassen (Besitzer: Orchestrator; Stand 29.10.2026 04:00)

Format je Klasse: DRIN · DRAUSSEN · Anzahl je Eltern · Masse (Quelle) · Referenz · typische Fehlinterpretation · Pruefzahlen. Aenderungen nur mit Grund und Meldung an den Orchestrator. Regeln: `docs/review-protocol.md`.

## nft_rinne (EINE Rinne)
- **DRIN:** Profil 130 x 100 mm (Laenge parametrisch: 1304 / 1983 / 3232), gerippte Oberseite, **EINE Lochreihe** in der Mittellinie (Lochabstand `pitch`, Lochdurchmesser nach Netztopf 50 mm), Endkappen mit Zulauf-Stutzen an einem und Ablauf-Stutzen am anderen Ende (Wandstaerke Tuelle 3 mm, Ablauf mittig unten), Wandstaerke Profil.
- **DRAUSSEN:** Nachbarrinnen und **Versatz zwischen Rinnen (Zickzack)** = Tisch; Beine, Querstreben, Zulaufverteiler, Schlaeuche = Tisch; Netztopf, Salatkopf = eigene Klassen; Gefaelle als Einbaulage = Tisch.
- **Anzahl je Tisch:** 2 / 4 / 2 (OBJ, innen/mitte/aussen), aussen nach Beetbreite 3.
- **Masse (Quelle):** Breite 130, Tiefe ca. 100 (OBJ `hydro_tables`: 129 x 102), Abstand benachbarter Rinnen 262-288 (OBJ).
- **Referenz:** `reference/ref-6-grow-tables-detail.jpg`, Ausschnitt EINE Rinne mit Rahmen; Zickzack nur im Tisch-Ausschnitt.
- **Typische Fehlinterpretation:** zwei versetzte Lochreihen in einer Rinne (falsch: Zickzack entsteht durch Versatz benachbarter Rinnen).
- **Pruefzahlen:** Lochreihen je Rinne = 1; Lochzahl = Laenge / pitch (abgerundet); Rinnenbreite 130.
- **Ergaenzung 29.10. 04:20 (Werkstatt, bestaetigt):** Die Rinne liefert die Lochphase als Konfiguration A/B (shift = -pitch/4 bzw. +pitch/4, Phasenabstand = pitch/2, hier 125 mm bei pitch 250); der Zickzack selbst entsteht erst im Tisch, wenn benachbarte Rinnen abwechselnd Phase A und B bekommen. Konfigurationszeilen L/M/K (3232/1983/1304) je A und B, Masterdatei plus sechs Varianten. Zulauf-Tuelle am Stirnende (Schlauch ID 16), Ablaufstutzen d32 am anderen Ende; ref-6 zeigt Schlaeuche am Tischende, passt zum Stirnanschluss.

## nft_tisch (innen, mitte, aussen)
- **DRIN:** n Rinnen parallel (Abstand 262-288), **Versatz der Lochmuster benachbarter Rinnen um pitch/2 (Zickzack wie ref-6)**, 4 Beine mit Querstreben, Diagonalen, Fussplatten, Zulaufverteiler mit n Schlauchanschluessen (hellblau, ein Schlauch je Rinne wie ref-6), Sammelablauf, Gefaelle 1 cm/m, Rinnenhalter, Normschrauben.
- **DRAUSSEN:** Anordnung im Zehneck-Ring und Azimut (Layout/Integrator), Beete darunter, Pflanzen (eigene Klassen), Rohrnetz (Integrator, `system.json`).
- **Anzahl:** innen 10 (Apothem 1733 und 1995, Laenge 1304, 2 Rinnen), mitte 6 (4 Rinnen, Laenge 1983), aussen 8 (2-3 Rinnen, Laenge 3232).
- **Referenz:** ref-6 (Tischaufbau, Schlauchanschluesse), ref-4/ref-5 (Ring).
- **Pruefzahlen:** Versatz benachbarter Rinnen = pitch/2; Rinnenzahl und Abstand wie Ring; Hoehe Z laut `layout.json`.

## ibc_beet (aussen, innen)
- **DRIN:** Wanne (halbe IBC, Wandstaerke 3-4 mm), Medium (EIN Koerper, Oberflaeche Z 400, Tiefe 300 mm), Siebboden, Standrohr Ø25 x 220, Glocke Ø75 x 250, Medienschutz Ø110 x 320, Ablauf-Fitting im Beetboden, Zulaufrohr quer (Z 450). Quelle R03.
- **DRAUSSEN:** Pflanzen (Topf + Salatkopf als Instanzen aus `layout.json`, 288 je Aussenbeet), NFT-Tische darueber, Rohrnetz.
- **Anzahl:** 8 aussen (2953 x 933-993 x 637), 6 innen (1865 x 933 x 649); eingelassen (Unterkante Z -160...-210).
- **Fehlinterpretation:** Pflanzen als Teil der Wanne bauen; Medium als Einzelkoerner.

## tank_klein (Vortex-Absetzer) / tank_gross (Biofilter)
- **DRIN:** Zylinder + Kegel (Winkel 45-60 Grad), tangentialer Zulauf, Mittelrohr (Leitrohr), Schlammventil an der Kegelspitze (Bulkhead), Deckel/Oeffnung, Plattform mit 4 Beinen, Diagonalen, Fussplatten.
- **DRAUSSEN:** Rohrnetz und Schlaeuche (Integrator), Pumpe/Filtermodul (eigene Klasse), Wasserfuellung.
- **Anzahl:** klein 2 (Ø673, Hoehe 1075 inkl. Kegel; Plattform 706 x 707 x 73 auf Z 428, Beine 30 x 30 x 751), gross 2 (Ø930, Hoehe 1444; Plattform 977 x 976 x 98 auf Z 570, Beine 40 x 40 x 1008). Azimute 123/213 und 108/229 (OBJ, Rotation `layout_rot`).
- **Fehlinterpretation:** Tank als reiner Zylinder ohne Kegel; Fittings am Rand statt an der Kegelspitze.

## pumpe (Pumpe/Filtermodul)
- **DRIN:** Gehaeuse, Ein-/Auslass mit DN, Befestigung/Fuss, Kabel mit Stecker.
- **DRAUSSEN:** Rohre und Schlaeuche, Tank, Elektrik/Schaltschrank.
- **Anzahl und Lage:** je Tank mehrere Module (OBJ `tanks[].modules`: 502 x 345, 384 x 419, Platten 693 x 463); Rolle ist Annahme.

## salatkopf, netztopf
- **salatkopf DRIN:** EIN Bauteil, wenige Facetten, Varianten S/M/L; **DRAUSSEN:** Topf, Beet, Anzahl/Platzierung. **netztopf DRIN:** 50 x 64 x 63, Kragen; **DRAUSSEN:** Rinne/Beet, Pflanze.

## knoten_4 / knoten_5 / knoten_6 (Kuppelknoten, R02) — Werkstatt baut isoliert, Montage platziert
- **DRIN:** Nabe fuer 4/5/6 Streben als zwei Knotenplatten (oben/unten, Dicke `hub_plate_t` 6 mm A) mit Armen in den Strebenrichtungen aus den Knotenvektoren in `layout.json` (`dome.nodes_list`, Strebenrichtungen per Nachbarknoten), Stecklaenge `hub_insert` 80 mm, Normschrauben M10 (`parts.insert`) mit Mutter und Scheibe je Strebe, Schraubenbild, Bezugspunkt = Knotenmitte; Wertigkeit 4 (10 Stueck, Basis), 5 (6 Stueck, Apex und Ring 2), 6 (10 Stueck).
- **DRAUSSEN:** Strebe (Komponente strebe_a/b), Haut, Fundamentanker, Tuerknoten-Sonderanschluss (Montage).
- **Masse/Quelle:** Anzahl und Wertigkeit OBJ (26 Knoten: 10 vierwertig, 6 fuenfwertig, 10 sechswertig); Bauart R02 (Platten/Huelsen, kein Flachdruecken); Strebenteillaenge = Knoten-zu-Knoten minus 2 x `strut_end_offset` (120 mm A).
- **Typische Fehlinterpretation:** Armwinkel gleich fuer alle Knoten (jeder Knoten hat eigene Richtungen); Streben als Teil des Knotens.
- **Pruefzahlen:** Armzahl = Wertigkeit, Armwinkel aus Vektoren (Toleranz 0,5 Grad), Schrauben je Strebe >= 1, Gewicht.

## fundamentanker (10 Stueck an den Basisknoten)
- **DRIN:** Ankerplatte mit 2 Bolzen, Betonpunkt (Block im Erdreich, Mass A), Anschlusslaschen zum Basisknoten, Normschrauben.
- **DRAUSSEN:** Knoten, Strebe, Fundamentring (Montage), Erde.
- **Masse/Quelle:** Anzahl OBJ (10 Basisknoten); Block 400 x 400 x 600 mm A; Verankerung wie Ben: Skelett im Boden verankert.

## rohr / bogen / t_stueck / ventil / kupplung / schlauch / klemme / verteiler (Leitungsteile, Bibliothek)
- **DRIN:** je Teil Geometrie und Ports (Name, DN, Lage): Rohrstueck (DN parametrisch 25/32/50/110, Laenge parametrisch, Wandstaerke), Bogen 90 und 45 Grad, T-Stueck, Kugelhahn, Kupplung, Schlauchstueck (ID 16/25, Laenge, Biegeradius >= 5 x Aussendurchmesser, Farbe nach Funktion), Rohrklemme/Halter (fuer Boden und Beine), Verteiler mit n Anschluessen. Kuppelungen als Normteil (`parts.insert`), Farben nach `docs/hydraulics.md` Abschnitt 5.
- **DRAUSSEN:** Verlegung und Weg (aus `data/system.json`, Montage), welcher Port womit verbunden ist, `routing surface/buried`.
- **Masse/Quelle:** DN aus Fittings im OBJ (30-56 mm) und Bauteilblaettern (Rinne Stutzen d32, Tuelle ID 16, Tankzulauf DN50, Beet Standrohr/Ablauf); Normmasse PVC-U; Annahme A.
- **Fehlinterpretation:** Rohrverlauf im Bauteil modellieren; jedes Rohr als Einzelkoerper statt Komponente.

## REVISION 29.10. 08:40 (Orchestrator, Entscheidung D15): knoten_4/5/6
Abweichung der Werkstatt akzeptiert: **Knotenkugel Ø100 mit 4/5/6 Steckarmen** (Rechteckrohr, 80 mm in die Strebe gesteckt) und **Querbolzen M10** je Strebe statt "zwei Knotenplatten oben/unten". Grund (nachgerechnet aus `layout.json`): die Strebenrichtungen sind um asin(L/2R) = 15,9 Grad (Strebe A) bzw. 18,0 Grad (Strebe B) gegen die Tangentialebene geneigt; Arme zwischen flachen Platten wuerden die Platten durchdringen. R02 nennt Huelsen- und Sternnaben als Bauart, passt. Ergaenzung: Ankerlasche 60 x 10 x 150 mm, Loch Ø14, nur am vierwertigen Basisknoten (Schnittstelle zum Fundamentanker). 26 Einzelknoten-Dateien (Armrichtungen je Knoten aus den Nachbarknoten), Repraesentanten knoten_4/5/6. Pruefzahlen wie bisher (Armzahl = Wertigkeit, Armwinkel aus Vektoren).

## netztopf / salatkopf (Format nachgetragen, 08:40)
- **netztopf DRIN:** Korpus 50 x 64 x 63 mm mit Kragen (Ø64, Dicke 3,5 mm), Schlitze/Loecher fuer Wurzeln, Sitz im Topfloch (Rinne: Loch Ø52, Beet: Loch im Medium). **DRAUSSEN:** Loch, Rinne, Beet, Pflanze.
- **salatkopf DRIN:** EIN Kopf als Bauteil, wenige Facetten (Export!), Hals, Groessen S/M/L als Konfigurationen, Ursprung = Kragenoberkante des Netztopfs. **DRAUSSEN:** Netztopf, Platzierung, Instanzvariation (Layout).
- **Anzahl:** Netztopf gesamt ca. 2716 = 2160 (Beete, OBJ) + 556 (Rinnen: 20 Rinnen x 5 + 24 x 7 + 24 x 12, Annahme 3 Aussenrinnen je Tisch, E); Salatkopf gleiche Zahl (ein Kopf je Topf), Board-Angabe "ca. 240+" war veraltet.
- **Pruefzahlen:** Topfkragen liegt auf der Deckelflaeche, Kopf sitzt auf dem Kragen (Abstand Mitte Kopf zu Lochmitte 0).

## winkelhalter (Beinkopf-Winkel der NFT-Tische, W11, Werkstatt 29.10.)
- **DRIN:** EIN Stahlwinkel 36 x 60 x 60 x 4 mm (Flansch senkrecht am Bein, Flansch waagerecht unter dem Querholm bzw. Kragarm), je 2 Loecher D6,6 je Flansch, Normteile M6 (2 x M6x55 + Mutter durch das Bein, 2 x M6x16 in den Holm); Ursprung = Ecke Beininnenflaeche / Holmunterkante, Mitte der Winkelbreite. Holm/Kragarm ist ueber diesen Winkel am Bein geschraubt (nicht geschweisst).
- **DRAUSSEN:** Bein, Holm, Kragarm, Rinnenhalter, Diagonalen (Klasse nft_tisch); Platzierung je Bein (Tisch); Statik.
- **Anzahl:** je Bein einer = innen 2, mitte 4, aussen 4 je Tisch; gesamt 10 x 2 + 6 x 4 + 8 x 4 = 76 (Tische innen 10, mitte 6, aussen 8 laut docs/components.md: Zehneck-Sockel, 8 Aussen-, 6 Innenbeete).
- **Masse/Quelle:** Annahme A (Baumarkt-Eckwinkel 60 x 60 x 4, Breite 36); Bein 40 x 40 x 3 und Holm 40 x 60 x 3 aus nft_tisch.
- **Referenz:** keine sichtbar (ref-6 zeigt die Beinkoepfe nicht aufgeloest); Ausfuehrung Annahme A.
- **Typische Fehlinterpretation:** Winkel als Teil von Bein oder Holm modellieren (gehoert zur eigenen Klasse); Schrauben/Mutter in die Diagonalen- und Laengsdiagonalenschrauben legen (Spec-Pruefer W11 fand das bei z -20 / -45).
- **Pruefzahlen:** Winkelzahl = Beinzahl; Winkel beruehrt Bein-Innenflaeche (Abstand 0) und Holmunterkante (Oberkante = Unterkante Holm/Kragarm); Schenkel 60, Breite 36, Masse 126,8 g; inspect.interference ohne Treffer ausser Bein/Holm/Kragarm (Rohrloecher nicht modelliert).


## Nachtrag W17/W18 (Werkstatt, 29.10. ~23:00)
Stand der Parameter nach W17/W18/D32-D34; aeltere Zeilen oben (Laengen 1304/1983/3232, pitch 250, 125 mm, 2716/556, Beet 2953 x 933-993, Gefaelle 1 cm/m) gelten nicht mehr.
- **nft_rinne:** `pitch` 200 mm (einstellbar 150..250), Zickzack = pitch/2 = 100, Phase +-50; Master-Konfigurationen L/M/K 16/9/6 Loecher; Lochzahl je Tischreihe bestimmt der Tisch (hole_plan: n <= floor(L/pitch), Phasenzwang, Randabstand 64).
- **nft_tisch:** Rinnenlaenge je Reihe (innen 758/928, Mitte 1505-2018, aussen 2676-3051), 2 / 4 / 3 Rinnen, Tischmitte ap_c innen 1864, Mitte 3277, aussen 4973, `corner_gap` 60 (D34), Portalrand = Beet + 115 (Fussplatte 70, leg_clearance 45), Gefaelle 1,5 %, Winkelhalter je Bein; NFT-Topfloecher gesamt 586 (innen 10 x 7, Mitte 6 x 30, aussen 8 x 42; D33).
- **ibc_beet:** Aussenbeet `aussen_800` = 800 x 2640 x 637 (D29), Innenbeet 933 x 1865 x 649; Pflanzraster im Aussenbeet rechnet die Montage (M7).
- **netztopf:** Gesamtzahl 2160 (Beete, altes Raster) + 586 (Rinnen) = 2746 ist Sache des Integrators/Layouts, nicht der Klasse.
