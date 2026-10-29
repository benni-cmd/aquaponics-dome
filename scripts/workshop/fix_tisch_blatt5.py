"""Blatt nft_tisch nach W11 (29.10.): Winkelhalter T23 am Beinkopf (Funktion, Verbindungen, Stueckliste, Montage, Herkunft, Pruefung, offene Fragen). Idempotent; nach fix_tisch_blatt4.py, vor partsheet.py.
Aufruf: python scripts/workshop/fix_tisch_blatt5.py [pruefzeile-check-nft-tisch]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
p = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(p, encoding="utf-8"))
bl = d["blatt"]
MARK = "Winkelhalter T23"
if MARK not in bl["funktion"]:
    bl["funktion"] += " Rev. B + W11: je Bein ein Winkelhalter T23 (Eckwinkel 36 x 60 x 60 x 4) zwischen Beininnenflaeche und Holmunterkante."
def add_once(lst, text, key=MARK):
    if not any(key in x for x in lst):
        lst.append(text)
add_once(bl["verbindungen"], "Winkelhalter T23 (W11): je Bein ein Eckwinkel 36 x 60 x 60 x 4 an der Beininnenflaeche (2 x M6x50 mit Mutter durch das Bein) und unter Holm/Kragarm (2 x M6x16 in Blindnietmuttern M6, nicht modelliert); Schenkel am Bein 60 mm (z -60..0), unter dem Holm 60 mm (y 0..60); Bein mit y < 0 nach +Y, Bein mit y > 0 um 180 Grad gedreht")
add_once(bl["stueckliste"], "Je Bein ein Winkelhalter T23 (36 x 60 x 60 x 4, S235 verzinkt, 2 x M6x50 + Mutter, 2 x M6x16): innen 2, mitte 4, aussen 4 je Tisch; gesamt 76 (innen 10 x 2, mitte 6 x 4, aussen 8 x 4), Blatt docs/parts/winkelhalter.md")
bl["montage"] = [x for x in bl["montage"] if MARK not in x]
for i, x in enumerate(bl["montage"]):
    if x.startswith("Bock am Boden ausrichten"):
        bl["montage"].insert(i + 1, "Winkelhalter T23 je Bein an die Holmunterkante schrauben (Blindnietmuttern M6) und am Bein verschrauben (M6x50, Winkel nach innen zum Holm hin), vor dem Auflegen der Rinnen")
        break
bl["offen"] = [x.replace("; Kopfplatten/Winkelhalter an den Beinkoepfen (W11) nicht modelliert", "") for x in bl["offen"]]
for i, x in enumerate(bl["offen"]):
    if x.startswith("Innen: Pfosten stehen ausserhalb des Beckenrands"):
        bl["offen"][i] = x.replace("ein Stuetzwinkel am Pfosten ist wegen der Beckenwand nicht moeglich (Annahme A)", "ein tiefer Stuetzwinkel am Pfosten ist wegen der Beckenwand nicht moeglich (Annahme A); der Winkelhalter T23 sitzt am Pfostenkopf (Z 721-781) ueber dem Beckenrand Z 650")
add_once(bl["offen"], "Winkelhalter T23: Statik (Kippmoment, Lochwandung der Rechteckrohre ohne Huelse), Blindnietmuttern/Scheiben nicht modelliert, siehe docs/parts/winkelhalter.md")
rows = d["herkunft_tabelle"]
if not any("Winkelhalter" in r[0] for r in rows):
    rows.append(["Winkelhalter T23 je Bein (Eckwinkel am Beinkopf)", "76 gesamt", "A + E", "Job W11 / Scope-Card winkelhalter; Beinzahl 2/4/4 je Tisch aus tisch_geom.py, Tischzahl 10/6/8 aus layout.json; Ausfuehrung Annahme A", "niedrig"])
if len(sys.argv) > 1:
    bl["pruefung"] = [x for x in bl["pruefung"] if "check_nft_tisch.py" not in x] + [sys.argv[1]]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("nft_tisch.json gepflegt")
