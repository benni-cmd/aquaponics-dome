"""W60 5a, Gruppe Becken/Tanks/Filter/Pumpen/Puffer: Erklaertexte Tank (tank_gross, tank_gross_t3) und Pumpenmodule.
Eintrag: (Muster der Teil-ID, Anzeigename, Funktion, Eigenschaften, Explosion|None, Gruppe, Zusatzfelder)
Explosion: (richtung, abstand_mm, folgt|None). Reihenfolge zaehlt: erster Treffer gilt."""

Z, ZM, XP, YM, YP = [0, 0, 1], [0, 0, -1], [1, 0, 0], [0, -1, 0], [0, 1, 0]

QUELLE_TANK = "docs/parts/tank.md, data/components/tank.json (typen.gross), docs/research/R09.md; Maße im Modell, Rohr- und Wandmaße angenommen"

TANK_GRUPPEN = [
    ("tank", "Tank und Deckel", "Der Behälter mit Kegelboden, der das Schwebebett und das Wasser fasst.", ["tank", "deckel"]),
    ("fuellung", "Schwebebett und Belüftung", "Lose Biomedium-Träger, die von unten belüftet und durch zwei Siebe im Tank gehalten werden.",
     ["biomedium", "belueftungsgitter", "belueftungsrohr", "zulaufsieb", "auslaufsieb"]),
    ("anschluesse", "Zulauf, Überlauf und Schlammablass", "Wasser kommt tangential herein, läuft oben seitlich über; Schlamm wird an der Kegelspitze abgelassen.",
     ["zulaufrohr", "ueberlauf", "schlammstutzen", "kugelhahn", "ablaufstutzen"]),
    ("gestell", "Plattform und Gestell", "Die Plattform trägt den gefüllten Tank auf vier Beinen; Rippen stützen den Kegel.",
     ["plattform", "stuetzrippe", "bein", "fussplatte", "strebe", "diagonale", "schraube_m8x30"]),
]

TANK = [
    (r"tank", "Tankkörper mit Kegelboden", "Der Tank ist der Biofilter: In ihm schwebt das Biomedium im Wasser, Bakterien auf den Trägern bauen Ammonium zu Nitrat ab.",
     ["Zylinder über Kegel, Außendurchmesser 930 mm, Höhe 1444 mm.", "PE, gerollter Randwulst, Revisionsöffnung im Deckel.",
      "Maße aus dem Layout; Wanddicke und Fassungsvermögen sind angenommen."], None, "tank", {}),
    (r"deckel", "Deckel", "Der Deckel schließt den Tank oben ab, hält das Belüftungsrohr und lässt sich für Wartung abnehmen.",
     ["PE-Platte 6 mm, bündig mit dem Randwulst.", "Durchführung für das Belüftungsrohr."], (Z, 350, None), "tank", {}),
    (r"zulaufrohr", "Zulaufrohr, tangential", "Das Rohr führt das Wasser tangential an die Innenwand; so entsteht eine Drehströmung, die das Biomedium in Bewegung hält.",
     ["PVC-U-Rohr d63, 260 mm lang, Achse parallel zur Y-Achse.", "Berührt die Innenwand tangential."], (YM, 250, None), "anschluesse", {}),
    (r"ueberlauf", "Überlaufstutzen", "Der Stutzen lässt das Wasser oben seitlich aus dem Tank ablaufen und hält so den Wasserstand konstant.",
     ["PVC-U-Stutzen d63 (DN50), 100 mm unter dem Rand.", "Das Auslaufsieb davor hält das Biomedium im Tank."], (XP, 250, None), "anschluesse", {}),
    (r"biomedium", "Biomedium (Schwebebett)", "Die losen Kunststoffträger bieten Bakterien viel Oberfläche; sie schweben im belüfteten Wasser und scheuern sich gegenseitig sauber.",
     ["Schüttung als Hüllkörper modelliert, etwa 470 Liter.", "Füllgrad rund zwei Drittel des Tankvolumens; Fabrikat offen."], (Z, 1100, None), "fuellung", {"lm": "ja"}),
    (r"belueftungsgitter", "Belüftungsgitter am Konus", "Das Gitter am Kegel verteilt die Luft feinblasig im Tank und hält das Biomedium dadurch in Schwebe.",
     ["PVC-Gitter 460 x 460 mm, 20 mm hoch.", "Luftzufuhr über das Belüftungsrohr von oben."], (Z, 500, None), "fuellung", {}),
    (r"belueftungsrohr", "Belüftungsrohr", "Das Rohr bringt die Druckluft vom Deckel zum Gitter am Kegelboden.",
     ["PVC-U-Rohr d16, 1269 mm lang.", "Luftanschluss im Deckel."], (Z, 700, None), "fuellung", {}),
    (r"zulaufsieb", "Zulaufsieb", "Das Sieb am Zulauf fängt grobe Teile ab, bevor sie ins Schwebebett gelangen.",
     ["Stahlsieb 63 mm Durchmesser, 4 mm dick.", "Sitzt im Zulaufrohr."], (YM, 400, "zulaufrohr"), "fuellung", {}),
    (r"auslaufsieb", "Auslaufsieb", "Das Sieb vor dem Überlauf hält das Biomedium im Tank zurück.",
     ["Stahlsieb als Korb vor dem Überlaufstutzen, 110 x 110 mm.", "Muss regelmäßig gereinigt werden."], (XP, 400, "ueberlauf"), "fuellung", {}),
    (r"schlammstutzen", "Schlammstutzen an der Kegelspitze", "Der Stutzen sitzt an der tiefsten Stelle und sammelt den abgesetzten Schlamm.",
     ["PVC-U-Stutzen d16."], (ZM, 80, None), "anschluesse", {}),
    (r"kugelhahn", "Kugelhahn des Schlammablasses", "Der Hahn sperrt den Schlammablass; zum Ablassen wird er geöffnet.",
     ["PVC-U-Kugelhahn d50 mit Verschraubung.", "Im Modell eine Ersatzform; Fabrikat offen."], (ZM, 160, None), "anschluesse", {"katalog": "kugelhahn_pvc_u"}),
    (r"ablaufstutzen", "Ablaufstutzen", "Der Stutzen führt den abgelassenen Schlamm weiter in die Entleerleitung.",
     ["PVC-U-Stutzen d40."], (ZM, 240, None), "anschluesse", {}),
    (r"plattform", "Plattform mit Kegelsitz", "Die Plattform trägt den gefüllten Tank; der Kegel sitzt in einer Aussparung und die Last verteilt sich auf die Rippen.",
     ["Stahlplattform 821 x 821 mm, 98 mm hoch.", "Kegelsitz mit 2 mm Spiel."], (ZM, 150, None), "gestell", {}),
    (r"stuetzrippe", "Stützrippe aus Holz", "Die Rippen stützen den Kegel von unten gegen die Plattform ab.",
     ["Fichtenholz, fünf Rippen radial unter dem Kegel.", "Holz im Außenbereich: Schutzanstrich nötig."], ("radial", 60, "plattform"), "gestell", {"lm": "nein"}),
    (r"bein", "Standbein", "Die vier Beine tragen Plattform und Tank und stehen auf Fußplatten.",
     ["Vierkantrohr 40 x 40 x 2,5 mm, rund 1002 mm lang, verzinkt."], (ZM, 400, "plattform"), "gestell", {}),
    (r"fussplatte", "Fußplatte", "Die Fußplatte verteilt die Last des Beins auf den Boden und nimmt die Schrauben auf.",
     ["Stahlplatte 100 x 100 x 6 mm, verzinkt."], (ZM, 100, "bein"), "gestell", {}),
    (r"strebe", "Querstrebe zwischen den Beinen", "Die Streben verbinden die Beine und steifen das Gestell gegen Kippen.",
     ["Vierkantrohr 40 x 40 x 2,5 mm, 741 mm lang."], ("radial", 100, "bein"), "gestell", {}),
    (r"diagonale", "Diagonale", "Die Diagonalen halten das Gestell rechtwinklig und nehmen seitliche Kräfte auf.",
     ["Flachstahl 3 mm, rund 733 mm lang."], ("radial", 180, "bein"), "gestell", {}),
    (r"schraube_m8x30", "Schraube M8 x 30 an der Fußplatte", "Die Schrauben halten die Fußplatten am Untergrund.",
     ["Sechskantschraube M8 x 30, verzinkt.", "Im Modell ohne Mutter und Scheibe."], (Z, 150, "fussplatte"), "gestell", {}),
]

PUMPE_GRUPPEN = [
    ("tafel", "Montagetafel und Konsole", "Die Tafel trägt die Pumpe; Winkel halten sie senkrecht und die Konsole nimmt die Pumpe auf.",
     ["montagetafel", "standwinkel_l", "standwinkel_r", "konsole", "pumpensockel"]),
    ("pumpe", "Pumpe", "Motor und Pumpenkopf mit Saug- und Druckstutzen sowie Stromanschluss.",
     ["motor", "pumpenkopf", "saugstutzen", "druckstutzen", "kabel", "stecker"]),
    ("befestigung", "Schrauben", "Die Schrauben halten die Konsole an der Tafel.", ["schraube_m6x20", "mutter_m6"]),
]

QUELLE_PUMPE = "docs/parts/pumpe.md, data/components/pumpe.json, docs/research/R47 (Pumpenauslegung); Fabrikat offen"

PUMPE = [
    (r"montagetafel", "Montagetafel", "Die Tafel trägt die ganze Pumpeneinheit senkrecht und lässt sich als Modul versetzen.",
     ["PP-Platte, stehend auf zwei Standwinkeln.", "Maße entsprechen dem Layout."], None, "tafel", {}),
    (r"standwinkel_[lr]", "Standwinkel", "Der Winkel stellt die Tafel aufrecht und leitet das Gewicht in den Boden.",
     ["Stahlwinkel 50 x 100 x 5 mm, hinten an der Tafel."], (ZM, 120, "montagetafel"), "tafel", {}),
    (r"konsole", "Pumpenkonsole", "Die Konsole trägt die Pumpe vor der Tafel und hält sie auf Höhe der Achse.",
     ["Stahlwinkel 5 mm, an der Tafel verschraubt."], (YP, 200, "montagetafel"), "tafel", {}),
    (r"pumpensockel", "Pumpensockel", "Der Sockel hebt den Motor an und gibt dem Pumpenkopf Luft zur Konsole.",
     ["Stahlsockel 11 mm hoch."], (Z, 100, "konsole"), "tafel", {}),
    (r"motor", "Pumpenmotor", "Der Motor treibt das Laufrad im Pumpenkopf an.",
     ["Zylindrische Hüllform; reale Pumpen wiegen mehr.", "230 V Wechselstrom."], (YP, 300, "konsole"), "pumpe", {"lm": "nein"}),
    (r"pumpenkopf", "Pumpenkopf", "Im Pumpenkopf fördert das Laufrad das Wasser vom Saug- zum Druckstutzen.",
     ["Kunststoffgehäuse, Saugstutzen axial, Druckstutzen nach oben."], (XP, 250, "motor"), "pumpe", {"lm": "ja"}),
    (r"saugstutzen", "Saugstutzen", "Über den Stutzen saugt die Pumpe Wasser an.",
     ["PVC-U-Stutzen, Öffnung zeigt nach +X."], (XP, 350, "pumpenkopf"), "pumpe", {"lm": "ja"}),
    (r"druckstutzen", "Druckstutzen", "Über den Stutzen drückt die Pumpe das Wasser in die Leitung.",
     ["PVC-U-Stutzen, Öffnung zeigt nach oben."], (Z, 250, "pumpenkopf"), "pumpe", {"lm": "ja"}),
    (r"kabel", "Anschlusskabel", "Das Kabel führt den Strom vom Stecker zum Motor.",
     ["Kabel 3 x 1,5 mm², im Modell 150 mm, real 1,5 bis 3 m."], ([-1, 0, 0], 250, "motor"), "pumpe", {"lm": "nein"}),
    (r"stecker", "Schutzkontaktstecker", "Der Stecker verbindet die Pumpe mit der Steckdose.",
     ["230 V Schutzkontaktstecker."], ([-1, 0, 0], 350, "kabel"), "pumpe", {"lm": "nein"}),
    (r"schraube_m6x20", "Schraube M6 x 20", "Die Schrauben halten die Konsole an der Tafel.",
     ["Sechskantschraube M6 x 20 nach ISO 4017, je Konsole zwei."], (YP, 120, "konsole"), "befestigung", {}),
    (r"mutter_m6", "Mutter M6", "Die Mutter sichert die Schraube auf der Rückseite der Tafel.",
     ["Sechskantmutter M6 nach ISO 4032.", "Im Schraubensatz enthalten."], (YM, 120, "montagetafel"), "befestigung", {}),
]
