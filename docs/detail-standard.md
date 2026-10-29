# Detail-Standard: Expertenniveau je Bauteil (verbindlich, 29.10.2026)

Ben erwartet maximale Detailtiefe und Expertenarbeit. Massstab: **Ein Handwerker oder Ingenieur koennte das Bauteil aus dem Modell bauen und bestellen.** Ein Bauteil gilt erst als "fertig", wenn es Stufe L3 erreicht hat und der Gauntlet-Kritiker plus Fachkritiker bestehen.

## Stufen

- **L1 Form:** richtige Masse, Lage, Anzahl (aus `layout.json`). Ohne Details.
- **L2 Detail:** alle sichtbaren Merkmale der Referenz (Profile, Raender, Beine, Rinnen, Kegel, Klappen), Farbe/Material.
- **L3 Konstruktion:** Bauteil ist baubar: Wandstaerken, Profile und Querschnitte, Verbindungen (Schrauben, Muffen, Klemmen mit Normbezeichnung), Anschluesse/Ports mit DN und Lage, Gefaelle, Spiel/Toleranz, Abstaende; keine Durchdringungen ausser gewollt; Werkstoff und Oberflaeche je Teil. Parameter in `params.json`.
- **L4 Fertigung/Montage:** Bauteilblatt komplett (siehe unten), Montagereihenfolge, Werkzeug, Stueckliste-Zeile mit Mengen, alternative lokale Fertigung (billig, einfach).

Alle Bauteile bis L3, die sichtbaren Hauptbauteile (Knoten, Beet, NFT-Rinne, Tank, Pool) bis L4, bevor die Gesamtansicht als abgeschlossen gilt.

## Bauteilblatt `docs/parts/<bauteil>.md` (aus `params.json` erzeugt, nicht von Hand)

Name und ID, Funktion, Anzahl (Instanzen laut `layout.json`), Masse und Toleranzen, Werkstoff und Wandstaerke, Querschnitt/Profil, Ports (Name, DN, Lage, Richtung), Verbindungen und Befestigungen (z. B. M10 A2 Schraube mit Mutter und Scheibe), Referenzbild und Ausschnitt, Abweichung zum OBJ (aus `check_fidelity`), Gewicht (aus Volumen und Dichte, gefuellt und leer), Montageschritte, offene Fragen.

## Erwartete Details je Bauteilklasse (Checkliste fuer Bauer und Kritiker)

1. **Strebe:** Rohr/Profil mit Wandstaerke, Laenge = Knotenabstand minus Knotenversatz (Streben A 3279 und B 3708 sind Knoten-zu-Knoten-Maße; die echte Teillaenge ist kuerzer), Bohrungen und Endkappen/Stopfen, Anschlusslaschen.
2. **Knoten (26 Stueck, 3 Typen: 5-, 6-, 4-wertig):** Naben (gewaehlte Variante), Armlaenge und -winkel je Strebenrichtung aus den Knotenvektoren, Schraubenbild, Mutter/Scheibe, Anker an den 10 Basisknoten (Bolzen, Ankerplatte, Betonpunkt im Boden).
3. **Haut:** dreieckige durchsichtige Felder (Folie/Glas/Polycarbonat) mit Rahmenleisten und Klemmprofil an den Streben; Tuerfeld ausgespart; Entlueftung/Klappe.
4. **Fundamentring:** flacher Betonring am Basis-Zehneck, Hoehe/Breite aus dem OBJ, Ankerpunkte; Erde als Boden (kein Betonboden), Bodenflaeche verdichtet.
5. **Beet (14, halbe IBC):** Wanne mit Wandstaerke und Rand, Kies/Blaehton-Schicht mit Tiefe, Ablauf-Fitting (Bulkhead), Standrohr/Glockensiphon, Zulauf-Tropfrohr, eingelassen laut OBJ.
6. **NFT-Rinne und Tisch:** Profil 130 x 100 mm mit Wandstaerke, gerippte Oberseite mit Topfoeffnungen im Rasterabstand, Endkappe mit Ablaufstutzen, Zulaufverteiler, Gefaelle 1 cm/m, Tisch mit Beinen, Querstreben, Fussplatten, Rinnenhalter; Schlauch-/Rohranschluss je Rinne.
7. **Tank (4, Vortex/Biofilter):** Zylinder + Kegel (Winkel 45-60 Grad), tangentialer Zulauf, Mittelrohr, Schlammventil an der Kegelspitze, Deckel/Oeffnung, Plattform mit Beinen und Diagonalverstrebung, Fussplatten, Fittings (PVC-Bulkhead mit Dichtung) an den OBJ-Positionen.
8. **Pool (und zweites Becken):** Wand (Wandstaerke), Rand, Boden, Bodenablauf, Skimmer/Ueberlauf, Belueftungsring, Luftschlauch, eingelassene Tiefe; Wasserflaeche als duenne durchsichtige Scheibe.
9. **Pumpe/Filtermodul:** Gehaeuse, Ein-/Auslass mit DN, Befestigung, Kabel; Leitungsverlauf zu den Ports.
10. **Rohre und Schlaeuche:** Aussendurchmesser/DN und Wandstaerke, Formstuecke als Bauteile (Bogen, T, Muffe, Kupplung, Ventil, Rueckschlagventil, Verteiler), Halter/Klemmen alle 0,5-1 m, Biegeradius, `routing: surface|buried`; Anschluss nur an Ports.
11. **Tuer:** Rahmen, Blatt, Scharniere, Griff, Schwelle, Glasfeld; Normmass 1000 x 2000.
12. **Schaltschrank:** Gehaeuse, Tuer, Schloss, Kabeleinfuehrungen, Standfuss.
13. **Pflanzen/Toepfe:** Netztopf (50 x 64 x 63) einheitlich, Salatkopf als EIN parametrisiertes Bauteil mit Groessenvarianten.

## Expertenpruefung (zusaetzlich zu Gauntlet und Zahlenchecks)

Ein getrennter Kritiker mit frischem Kontext prueft je Bauteil: (a) Ist es baubar (Wandstaerken, Verbindungen, Ports, Toleranzen)? (b) Stimmen Masse, Anzahl und Lage mit dem OBJ? (c) Sind alle sichtbaren Details der Referenz da? (d) Gibt es Durchdringungen, schwebende Teile, doppelte Koerper? (e) Ist es als Komponente mit Instanzen gebaut und aus `params.json` gesteuert? Er nennt hoechstens fuenf Luecken (gross/klein). Kein Bauteil gilt als L3, solange eine grosse Luecke offen ist.

## Reihenfolge nach sichtbarem Gewinn

NFT-Tisch mit Rinnen und Schlaeuchen (fehlt komplett) -> Tank mit Anschluessen und Plattform -> Pool mit Rand/Ablauf -> Beet mit Kies und Siphon -> Knoten -> Streben-Details -> Haut -> Rohrnetz aus dem Graphen -> Tuer, Schaltschrank, Fundamentring -> Pumpen/Filtermodule.
