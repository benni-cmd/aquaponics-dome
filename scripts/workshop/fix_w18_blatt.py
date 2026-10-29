"""W18 (D32, 29.10.): Lochabstand pitch 200 -- Blatt-Texte und Parameter-Herkunft in nft_rinne.json und nft_tisch.json; Zahlen aus tisch_geom/nft_rinne.json. Idempotent; VOR dem Bau-Start ausfuehren, nicht waehrend einer Kette.
Aufruf: python scripts/workshop/fix_w18_blatt.py"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

pt = TG.rinne_pitch()
p, d = load("nft_rinne")
P = d["parameter"]
nL, nM, nK = int(3232 // pt), int(1983 // pt), int(1304 // pt)
P["n_holes"]["wert"] = nL
P["n_holes"]["herkunft"] = f"[E] = floor(len_l / pitch): Master L {nL}, M {nM}, K {nK} (Pruefzahl Scope-Card: Lochzahl = Laenge/pitch abgerundet; Lochreihen = 1); die Tischreihen bekommen je Reihe eigene Zahl aus tisch_geom.hole_plan (Randabstand 64)"
P["shift"]["wert"] = -pt / 4
P["shift"]["herkunft"] = f"[E] Phase der Lochreihe: Variante A -pitch/4 = {-pt / 4:g}, Variante B +pitch/4 -> benachbarte Rinnen im Tisch um pitch/2 = {pt / 2:g} versetzt (Zickzack)"
bl = d["blatt"]
bl["querschnitt"] = bl["querschnitt"].replace("Teilung 250 (L 12, M 7, K 5 Loecher), Reihe um shift = +-62,5 verschoben", f"Teilung {pt:g} (Master L {nL}, M {nM}, K {nK} Loecher), Reihe um shift = +-{pt / 4:g} verschoben")
bl["offen"] = [x if not x.startswith("Lochabstand 250 ist unsere Auslegung") else f"Lochabstand {pt:g} (D32, Ben 29.10.) gestuetzt auf Iowa State 8 Zoll = 203 mm und HortTechnology 15 cm (R16); einstellbar 150..250; ref-6 gibt kein Mass" for x in bl["offen"]]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
p, d = load("nft_tisch")
cg = d["parameter"]["corner_gap"]
cg["herkunft"] = f"[A] W17: Abstand Rinnenende/Rohr zur Sektorgrenze 60 mm (vorher 100, D18); mit Lochabstand {pt:g} (W18/D32) ergibt das 586 Topfloecher (Soll ca. 580; mit 100 nur 542); Entscheidung beim Orchestrator/Ben"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("W18-Blatt-Parameter gepflegt, pitch", pt)
