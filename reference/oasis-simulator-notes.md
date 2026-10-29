# Notizen zum Oasis-Simulator-Prototyp (Kontext, nicht verifiziert)

Quelle: https://showcase-oasis-simulator.vercel.app/ui-prototype/ (Bens Hinweis 29.10.2026: ein Rechner, Richtigkeit unbekannt, nur Kontext). Gelesen per Seitenabruf; Diagramme, Formeln, Katalogwerte und Ergebnisse werden per JavaScript geladen und waren nicht sichtbar.

Sichtbare Angaben (alle als Kontext, NICHT als Wahrheit; Bens Angaben und das OBJ gehen vor):
- Projektname "Project Oasis V12", Simulator fuer ein aquaponisches Dom-System mit Dashboard, Kausalgraph, Formel-Explorer, Simulation (30 bis 360 Tage), Jahreszeiten.
- Eingaben: Personen (Standard 10), Fischarten Nil-Tilapia und Karpfen, Lebendfutter Daphnien und Schwarze Soldatenfliege (BSF), Dom-Durchmesser **11 m** (Ben: 12 m, Ben gilt), Fischtank **27,8 m3**, Besatzdichte 15 kg/m3 (ergibt rund 417 kg Fisch, abgeleitet), PV-Leistung kWp, Zisterne (Regenwasser), Dom-Ausbau in Ringen und Modulen.
- Biofilter "K1" mit Medienauswahl: Micro (MBBR) SSA 1150, Sinterglas 1050, Keramikringe 2000, Bio Balls 400, Lavagestein 290 (SSA = spezifische Oberflaeche, Einheit nicht erklaert).
- Kataloge: Pflanzen (10 Naehrstoffe), Fische/Lebendfutter, Hardware-Preise, Biologie/Physik, Pumpen, Anbausysteme, Filter/Substrat, Bakterienkinetik.
- Hinweis auf Gesamtbild: Fisch (inkl. Lebendfutter) + Biofilter + Pflanzen + Energie/Wasser (PV, Zisterne), Dom in Ringen.

Folgen fuer das Modell (zur spaeteren Pruefung, nicht jetzt):
- Fischtank 27,8 m3 bei 3,89 m Durchmesser = Wassertiefe etwa 2,3 m. Das OBJ zeigt nur eine Wasserflaeche bei Z 515. Offen, ob der Pool tief eingelassen ist; fuer das Modell vorerst Wasserspiegel und Rand wie im OBJ, Tiefe als Parameter `pool_depth`.
- Moegliche Zusatzbauteile aus dem Rechner: Zisterne/Regenwassertank, PV, Lebendfutter-Module (Daphnien, BSF). Nur aufnehmen, wenn das OBJ oder die Bilder sie zeigen.
- Dom-Ausbau "in Ringen": passt zum Ring-Layout (Aussenringe, Innenringe) der Beete.
