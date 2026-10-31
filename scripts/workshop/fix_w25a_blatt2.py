"""Triage-Nachtrag Spec-Pruefer W25a/W26/W25 (31.10.): Aussentisch-Ports/Stueckliste auf 4 Rinnen, Widersprueche und alte Zahlen als aktuelle Aussage in nft_tisch/netztopf/nft_rinne/salatkopf/pumpe. Idempotent.
Aufruf: python scripts/workshop/fix_w25a_blatt2.py (danach partsheet.py je Klasse)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

def rep(pth, d, pairs):
    txt = json.dumps(d, ensure_ascii=False)
    for a, b in pairs:
        txt = txt.replace(a, b)
    json.dump(json.loads(txt), open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

p, d = load("nft_tisch")
P = {k: v["wert"] for k, v in d["parameter"].items()}
G = TG.geometry("aussen", P, d["typen"]["aussen"])
t18 = TG.T18
y1 = G["ymid"] + G["Wt"] / 2 + 60                                    # +Y-Ende von Verteiler und Sammelrohr (Tisch-KS)
hdr_len = round((G["Wt"] + 120) / 0.951057)                           # (Wt + 2 x 60) / cos 18 Grad
x_z = -((G["apc"] - y1) * t18 - G["gap"]) + 12.5 / 0.951057           # Zulaufverteiler, Achse am +Y-Ende
x_s = ((G["apc"] - y1) * t18 - G["gap"]) - 25 / 0.951057              # Sammelrohr
xs_row = [G["rows"][0]["xc"] - r["L"] / 2 - 99 for r in G["rows"]]
lmin = min(r["L"] for r in G["rows"])
foot = G["xb"]
lengs = round(G["xb"][1] - G["xb"][0] - P["leg_w"])                  # Laengsstrebe zwischen den Beinen (nft_tisch.py: xb-Abstand minus leg_w)
def fmt(v): return f"{round(v)}"
pairs = [
 ("x -1376, y 413, z 1391 (Achse laeuft schraeg", f"x {fmt(x_z)}, y {fmt(y1)}, z 1391 (Achse laeuft schraeg"),
 ("x 1363, y 413, z 1299 (Achse dx/dy", f"x {fmt(x_s)}, y {fmt(y1)}, z 1299 (Achse dx/dy"),
 ("aussen: Verteiler-Stutzen je Rinne (n=3)", "aussen: Verteiler-Stutzen je Rinne (n=4)"),
 ("x -1547, -1454, -1360 (Stutzenspitze je Reihe), y = Rinnenmitte, z ca. 1391", "x " + ", ".join(fmt(x) for x in xs_row) + " (Stutzenspitze je Reihe), y = Rinnenmitte (-288 / -68 / 152 / 372), z ca. 1391"),
 ("x -1011 / y -480; x -1011 / y 480; x 1101 / y -480; x 1101 / y 480", f"x {fmt(foot[0] - 20 + 0)} / y -480; x {fmt(foot[0])} / y 480; x {fmt(foot[1])} / y -480; x {fmt(foot[1])} / y 480"),
 ("Laengsstreben 40x40x3 x 2: Laenge 2072", f"Laengsstreben 40x40x3 x 2: Laenge {lengs}"),
 ("Verteiler d25 schraeg: Laenge 869; Sammelrohr d50 schraeg: Laenge 869", f"Verteiler d25 schraeg: Laenge {hdr_len}; Sammelrohr d50 schraeg: Laenge {hdr_len}"),
 ("Standard bleibt aussen (3 Rinnen) bis Ben/Orchestrator entscheidet", "seit D43 Standard (die 3-Rinnen-Fassung steht als aussen3)"),
 ("= Standard aussen (3 Reihen, Abstand 288: y = -288); keine Reihe weiter aussen als im Standard", "= aussen3 (3 Reihen, Abstand 288: y = -288); keine Reihe weiter aussen als in aussen3"),
 ("2612-2986 (aussen)", "2558-2986 (aussen, 4 Reihen)"),
]
# Doppelte Ersetzung der Fussplatten-x verhindern: Fusspunkt = Fussplattenmitte der Bein-x (xb)
pairs[4] = ("x -1011 / y -480; x -1011 / y 480; x 1101 / y -480; x 1101 / y 480", f"x {fmt(foot[0])} / y -480; x {fmt(foot[0])} / y 480; x {fmt(foot[1])} / y -480; x {fmt(foot[1])} / y 480")
dd = json.loads(json.dumps(d))
for row in dd["herkunft_tabelle"]:
    if row[0].startswith("NFT-Topfloecher gesamt 570"):
        row[0], row[1] = row[0].replace("570", "674 (aussen3: 570)"), "674"
    if row[1] == "2/4/3":
        row[1] = "2/4/4"
    if row[0].startswith("Rinnenabstand 262 / 263 / 288"):
        row[0], row[1] = "Rinnenabstand 262 / 263 / 220 (aussen: D43, vorher 288)", "262 / 263 / 220 mm"
json.dump(dd, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
p, d = load("nft_tisch"); rep(p, d, pairs)
pth, dd = load("netztopf")
rep(pth, dd, [("Beete 2160 (OBJ) + Rinnen 570 (E) = 2730", "Beete 2160 (OBJ) + Rinnen 674 (E) = 2834"), ("W18: Rinnen-Topfloecher 570 laut", "W18/D43: Rinnen-Topfloecher 674 (aussen 4 Rinnen; 570 mit 3) laut"), ("Gesamtzahl 2730 = 2160 (Beete) + 570 (Rinnen)", "Gesamtzahl 2834 = 2160 (Beete) + 674 (Rinnen)"), ('"2730"', '"2834"')])
pth, dd = load("nft_rinne"); rep(pth, dd, [("Rinnen je Tisch 2 / 4 / 3 (aussen 3: Annahme, OBJ 2)", "Rinnen je Tisch 2 / 4 / 4 (aussen 4: D43, vorher Annahme 3, OBJ 2)")])
pth, dd = load("salatkopf"); rep(pth, dd, [("Budget bei 2730 Instanzen", "Budget bei 2834 Instanzen")])
# Pumpenblatt: Widersprueche 3b, 3c, 3d, 3e
pth, dd = load("pumpe")
q = dd["typen"]["pumpe_klein"]
q["foerderstrom_l_min"] = "12-13 je Tank (zwei Pumpen je Tank: eine in Betrieb und eine Reserve, oder je ca. 6,5 parallel; offen)"
dd["typen"]["pumpe_gross"]["rolle"] = "Hauptkreislauf (je Linie 2 Pumpen parallel, vorlaeufig D38)"
dd["typen"]["pumpe_klein"]["rolle"] = "Absetzer-Teilstrom (vorlaeufig D38)"
tab = []
for row in dd["herkunft_tabelle"]:
    if "12" in row[0] and "30" in row[0] and "l/min" in row[0]:
        row = ["Foerderstrom Hauptkreislauf gross 55-60 l/min je Pumpe, Absetzer klein 12-13 l/min je Tank", "55-60 / 12-13 l/min", "E", "D38 / aquaponik-empfehlung.md (vorher Modellwerte 12 / 30 l/min, hydraulics.md 2.3)", "mittel"]
    tab.append(row)
dd["herkunft_tabelle"] = tab
bl = dd["blatt"]
bl["funktion"] = bl["funktion"].replace("ENTSCHEIDUNG D38 30.10. fuer die Pumpen", "vorlaeufige ENTSCHEIDUNG D38 30.10. fuer die Pumpen").replace("pumpe_klein (4 Stueck, Tanktafeln 1/4) = ABSETZER-TEILSTROM, 12-13 l/min je Pumpe [E]", "pumpe_klein (4 Stueck, Tanktafeln 1/4) = ABSETZER-TEILSTROM, 12-13 l/min je Tank (zwei Pumpen je Tank, Aufteilung offen) [E]").replace("Pflanzenstrom = Hauptkreislauf - Beete", "NFT-Strom = Hauptkreislauf - Beete")
bl["offen"] = [x for x in bl["offen"] if not x.startswith("NFT-Durchfluss R06")] + ["nft_tisch.json rechnet die Verteilerschlaeuche noch mit 0,5 l/min je Rinne (R06); das Pumpenblatt (D38) ergibt 1,5-1,7 l/min je Rinne bei 76 Rinnen: Schlauch ID 16 reicht, Verteilerquerschnitt und Rinnenueberlauf (Rinnen-Tuelle) bei dieser Menge ungeprueft (Hydraulik)", "Empfehlung rechnet Pflanzenstrom = Beete + NFT (177-245 l/min); die 230-320 W gelten fuer 245 l/min; Reserve-Paar nicht festgelegt (4 Pumpen voll belegt)"]
json.dump(dd, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("ok", fmt(x_z), fmt(x_s), y1, hdr_len, lengs, [fmt(x) for x in xs_row], [fmt(f) for f in foot])
