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
