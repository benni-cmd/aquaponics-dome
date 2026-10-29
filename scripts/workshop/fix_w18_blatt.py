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

# --- Netztopf: Gesamtzahl der Rinnen-Toepfe (W18: 586 statt 556)
cnt = {"innen": 10, "mitte": 6, "aussen": 8}
pj, dj = load("nft_tisch")
Pj = {k: v["wert"] for k, v in dj["parameter"].items()}
per = {t: sum(r["n_holes"] for r in TG.geometry(t, Pj, dj["typen"][t])["rows"]) for t in cnt}
nft = sum(per[t] * cnt[t] for t in cnt)
pn, dn = load("netztopf")
txt = json.dumps(dn, ensure_ascii=False)
new_r = f"Rinnen {nft} (Tische innen 10 x {per['innen']}, Mitte 6 x {per['mitte']}, aussen 8 x {per['aussen']}; pitch {pt:g}, W18)"
for old in ("Rinnen 556 (20 Rinnen K x 5 Loecher + 24 Rinnen M x 7 + 24 Rinnen L x 12; Auslegung E)", "Rinnen 556 (E)", "Rinnen (556)", "Rinnen 556"):
    if old in txt:
        txt = txt.replace(old, new_r if old.endswith("Auslegung E)") else (f"Rinnen {nft} (E)" if old == "Rinnen 556 (E)" else f"Rinnen {nft}"))
txt = txt.replace("2160 (Beete) + 556 (Rinnen)", f"2160 (Beete) + {nft} (Rinnen)").replace("= 2716", f"= {2160 + nft}").replace("2716", str(2160 + nft)).replace("556", str(nft))
dn = json.loads(txt)
dn["blatt"]["offen"] = [x for x in dn["blatt"]["offen"] if not x.startswith("W18:")] + [f"W18: Rinnen-Topfloecher {nft} laut docs/parts/nft_tisch.md (pitch {pt:g}, corner_gap 60); Beete 2160 nur bis zur Umstellung auf aussen_800 (Raster Aussenbeet 800 x 2640: Layout/Integrator)"]
json.dump(dn, open(pn, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("netztopf.json: Rinnen", nft, "gesamt", 2160 + nft)
