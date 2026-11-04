"""W60 5a: Erklaertexte schwimmerventil_pool, becken_dritt_klein, becken_dritt, pool_zentral, zweitbecken, zulaufrohr (Format siehe texte_tank.py)."""
Z, ZM, XP, XM, YM, YP = [0, 0, 1], [0, 0, -1], [1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, 1, 0]

QUELLE_SV = "docs/parts/schwimmerventil_pool.md, data/components/schwimmerventil_pool.json; Handelsteil, Maße angenommen"
QUELLE_DK = "docs/parts/becken_dritt_klein.md, data/components/becken_dritt_klein.json, docs/research/R37 (Befund 10)"
QUELLE_BECKEN = "data/layout.json (Maße aus dem Referenzmodell), docs/research/R37; Eigenbau, Werkstoff im Modell nicht zugewiesen"

SV_GRUPPEN = [("ventil", "Ventil mit Schwimmer", "Gehäuse mit Wangen und Hebelarm mit Schwimmerkugel; der Übergang führt zur Leitung.",
               ["uebergang", "ventilgehaeuse", "wange_l", "wange_r", "hebelarm_mit_kugel"])]
SV = [
    (r"uebergang", "Übergang zur Leitung", "Der Übergang verbindet das Ventil mit der Frischwasserleitung.", ["PVC-Stutzen d32."], (YP, 150, None), "ventil", {"lm": "ja"}),
    (r"ventilgehaeuse", "Ventilgehäuse", "Das Gehäuse enthält den Sitz, den der Hebel öffnet und schließt.", ["PP-Gehäuse, 38 mm Durchmesser, 80 mm lang."], (Z, 150, None), "ventil", {"lm": "ja"}),
    (r"wange_[lr]", "Wange des Hebellagers", "Die Wangen halten den Drehpunkt des Hebelarms.", ["PP, 4 mm dick."], (XP, 80, "ventilgehaeuse"), "ventil", {"lm": "ja"}),
    (r"hebelarm_mit_kugel", "Hebelarm mit Schwimmerkugel", "Sinkt der Wasserspiegel, kippt die Kugel nach unten und öffnet das Ventil; steigt er, schließt es.",
     ["Hebel mit Kugel, rund 317 mm lang.", "Hält den Pegel im Pool auf der Soll-Höhe."], (YM, 200, "ventilgehaeuse"), "ventil", {"lm": "ja"}),
]

DK_GRUPPEN = [
    ("becken", "Wanne und Wasser", "Die Wanne fasst 0,4 m³ Wasser; sie wird in den Boden eingelassen.", ["t_wanne", "wasser"]),
    ("anschluss", "Anschlüsse", "Vier Stutzen verbinden das Becken mit den Leitungen.", ["stutzen_k"]),
]
DK = [
    (r"t_wanne", "Wanne des Drittbeckens", "Die Wanne ist das Quarantäne- und Notbecken für kranke Tiere oder Zuchttiere.", ["Rund 920 x 920 x 1055 mm.", "In den Boden eingelassen wie Pool und Zweitbecken."], None, "becken", {"lm": "ja"}),
    (r"wasser", "Wasserfüllung (nur Darstellung)", "Der Körper zeigt die Wasserfüllung von rund 0,4 m³; er ist kein Bauteil.", ["Reines Darstellungsvolumen."], None, "becken", {"lm": "ja"}),
    (r"stutzen_k", "Wanddurchführung", "Die Durchführungen leiten Wasser durch die Wand zum Biofilter und zur Belüftung.", ["PVC-Stutzen d63, vier Stück."], ("radial", 300, "t_wanne"), "anschluss", {"lm": "ja"}),
]

BECKEN_GRUPPEN = [("becken", "Becken und Wasser", "Das Becken mit der Wasserfüllung.", ["t_drittbecken", "t_wasser"])]
BECKEN_DRITT = [
    (r"t_drittbecken", "Drittbecken", "Das Drittbecken dient als Quarantäne- und Notbecken für Fische.", ["Außenmaß 1150 x 1150 x 1265 mm.", "Eigenbau oder Sonderanfertigung; Werkstoff im Modell nicht zugewiesen."], None, "becken", {}),
    (r"t_wasser", "Wasserfüllung (nur Darstellung)", "Der Körper zeigt die Wasserfüllung; er ist kein Bauteil.", ["Reines Darstellungsvolumen."], None, "becken", {}),
]

POOL_GRUPPEN = [("pool", "Pool und Wasser", "Das Becken mit der Wasserfüllung.", ["t_zentraltank", "t_wasser"]),
                ("anschluesse", "Wanddurchführungen", "Seitenablauf und Bodenablauf leiten das Wasser aus dem Pool.", ["t_stutzen_sa_ost_a", "t_stutzen_sa_west_b", "t_stutzen_ba_mitte"])]
POOL = [
    (r"t_zentraltank", "Zentralpool", "Der Zentralpool ist das Hauptbecken der Anlage, in dem die Fische leben.", ["Außenmaß rund 4190 x 4190 x 2475 mm.", "In den Boden eingelassen; Werkstoff im Modell nicht zugewiesen."], None, "pool", {}),
    (r"t_stutzen_sa_(ost_a|west_b)", "Seitenablauf-Durchführung", "Der Stutzen führt das Wasser seitlich aus dem Pool zum Filter.", ["PVC-Stutzen d63 durch die Poolwand."], ("radial", 400, "t_zentraltank"), "anschluesse", {"lm": "ja"}),
    (r"t_stutzen_ba_mitte", "Bodenablauf-Durchführung", "Der Stutzen leitet feststoffreiches Wasser aus der Poolmitte ab.", ["PVC-Stutzen d50 am Poolboden."], (ZM, 300, "t_zentraltank"), "anschluesse", {"lm": "ja"}),
    (r"t_wasser", "Wasserfüllung (nur Darstellung)", "Der Körper zeigt die Wasserfüllung; er ist kein Bauteil.", ["Reines Darstellungsvolumen."], None, "pool", {}),
]

ZWEIT_GRUPPEN = [("becken", "Becken und Wasser", "Das Becken mit der Wasserfüllung.", ["t_zweitbecken", "t_wasser"])]
ZWEIT = [
    (r"t_zweitbecken", "Zweitbecken", "Das Zweitbecken ergänzt den Pool als zweites Fischbecken im Boden.", ["Außenmaß rund 1867 x 1867 x 1135 mm.", "Eigenbau oder Sonderanfertigung; Werkstoff im Modell nicht zugewiesen."], None, "becken", {}),
    (r"t_wasser", "Wasserfüllung (nur Darstellung)", "Der Körper zeigt die Wasserfüllung; er ist kein Bauteil.", ["Reines Darstellungsvolumen."], None, "becken", {}),
]

ZULAUF_GRUPPEN = [("rohr", "Zulaufrohr", "Das lange Rohr führt Wasser zum Pool.", ["t_zulaufrohr"])]
ZULAUF = [
    (r"t_zulaufrohr", "Zulaufrohr zum Pool", "Das Rohr führt das Wasser zum Zentralpool.", ["PVC-U-Druckrohr d160.", "Länge aus dem Modell geschätzt (rund 4,4 m); Werkstoff im Modell nicht zugewiesen."], None, "rohr", {"lm": "offen"}),
]
