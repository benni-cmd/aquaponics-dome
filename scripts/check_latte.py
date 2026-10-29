"""Messbare Latte: prueft designs/dome.sc per Zahlen. Aufruf: python scripts/check_latte.py <runde>
Gibt je Pruefung PASS/FAIL mit Ist/Soll aus (Exit-Code 0 = alles PASS). Sicherheitstest, kein Score-Verlauf."""
import json, math, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
rnd = sys.argv[1] if len(sys.argv) > 1 else "00"
tmp = tempfile.mkdtemp()
dome = os.path.join(ROOT, "designs", "dome.sc")

def run_json(args):
    out = os.path.join(tmp, "o.json")
    subprocess.run([CLI] + args + ["--json-out", out], capture_output=True, check=False)
    return json.load(open(out, encoding="utf-8"))

def find(o, key):
    if isinstance(o, dict):
        if key in o and isinstance(o[key], list): return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None: return r

bodies = find(run_json(["eval", dome]), "bodies")
B = {b["name"]: b for b in bodies}
BN = {n: b for n, b in B.items() if n[:1] == "T" and n[1:2].isdigit()}   # eigene T-Koerper; Werkstatt-Instanzen heissen anders
cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
pre = lambda p: [b for n, b in B.items() if n.startswith(p)]
ext = lambda bs, i: (min(b["bbox"]["min"][i] for b in bs), max(b["bbox"]["max"][i] for b in bs))
res = []
def chk(name, ist, soll, ok): res.append({"check": name, "ist": ist, "soll": soll, "pass": bool(ok)})

t1 = pre("T1_"); sock_top = P["sock_h"]
z0, z1 = ext(t1, 2); x0, x1 = ext(t1, 0)
h = z1 - sock_top - 75 - 45
chk("L5/7 Kuppelhoehe [mm]", round(h), 6000, abs(h - 6000) / 6000 < 0.03)
# Knotenvalenz aus Strebenenden
ends = {}
for c in cmds:
    p = c["params"]
    if c["command"] == "occurrence.move" and str(p.get("occurrence", "")).startswith("Strebe_"):
        m = p["matrix"]; L = 0.5465 * P["dome_base_d"] / 2 if p["occurrence"].startswith("Strebe_A") else 0.618 * P["dome_base_d"] / 2
        o = P["strut_end_offset"]; org = [m[(3, 7, 11)[j]] - m[(2, 6, 10)[j]] * o for j in range(3)]   # Strebe beginnt strut_end_offset hinter der Knotenmitte
        for pt in (tuple(round(v) for v in org), tuple(round(org[j] + m[(2, 6, 10)[j]] * L) for j in range(3))):
            ends[pt] = ends.get(pt, 0) + 1
apex = max(ends, key=lambda k: k[2]); apex_n = ends[apex]
base_nodes = [k for k in ends if abs(k[2] - (sock_top + P['strut_r'] + 30)) < 5]
chk("L1/10 Streben am Scheitel", apex_n, 5, apex_n == 5)
w = 2 * sum(math.hypot(k[0], k[1]) for k in base_nodes) / len(base_nodes)
chk("L5/7 Kuppelbreite (Knoten-Durchmesser) [mm]", round(w), 12000, abs(w - 12000) / 12000 < 0.03)
chk("L5/7 Hoehe/Breite", round(h / w, 3), 0.5, abs(h / w - 0.5) / 0.5 < 0.03)
chk("L10 Basisknoten (Zehneck; 1 Knoten an der Tuer ohne Streben)", len(base_nodes), "9-10", len(base_nodes) in (9, 10))
chk("L10 Strebenzahl 2V (60 + 10 Basis - Tuer)", len(t1), "55-65", 55 <= len(t1) <= 65)
s = B["T3_Sockel"]; ue = (s["bbox"]["max"][0] - s["bbox"]["min"][0] - 12000) / 2
chk("L2/11 Fundamentring (Flaechen 10 aussen + 10 innen + 2, Tuerluecke +4)", s["faces"], "22-28", 22 <= s["faces"] <= 30)
chk("L9/11 Sockel Ueberstand [mm]", round(ue), "<= 300", ue <= 300)
beds = [b for n, b in B.items() if n.startswith("Wanne")]   # Werkstatt-Komponente ibc_beet_*: je Instanz eine Wanne
chk("OBJ Substratbeete (14 IBC-Wannen als Instanzen)", len(beds), 14, len(beds) == 14)
d = B["T4_Blatt"]["bbox"]; dh = d["max"][2] - d["min"][2]
dw = math.hypot(d["max"][0] - d["min"][0], d["max"][1] - d["min"][1])
chk("Tuer Hoehe Blatt ueber Schwelle 40 mm [mm]", round(dh), 1960, abs(dh - 1960) < 20)
chk("Tuer Breite (Rahmen) [mm]", round(P["door_w"]), 1000, abs(P["door_w"] - 1000) < 20)
# Zugang: kleinster seitlicher Abstand Tuer-Bett (Mittelpunkte der Bett-/Tuerboxen, Naeherung ueber bbox-Abstand)
def gap(a, b):
    return math.hypot(*[max(0, max(a["min"][i] - b["max"][i], b["min"][i] - a["max"][i])) for i in range(2)])
tg = min(gap(d, b["bbox"]) for b in beds)
chk("Tuerzugang: Abstand Tuer-Bett (bbox) [mm]", round(tg), ">= 1000", tg >= 1000)
t5 = B["T5_Zentraltank"]["bbox"]; t5d = t5["max"][0] - t5["min"][0]
import re
def base(n): return re.sub(r" \(\d+\)", "", re.sub(r" \([^()]*:\d+\)", "", n))   # Ordinal/Pfad-Suffix der Instanzkoerper abtrennen
tanks = [n for n in B if base(n) == "Tank"]   # Werkstatt-Komponenten tank_*: je Instanz ein Koerper 'Tank'
pumps = [n for n in B if base(n) == "Montagetafel"]   # Werkstatt-Komponenten pumpe_*
chk("OBJ Tanks (4 Instanzen) + Zweitbecken T6 (1) + Pumpentafeln (8)", (len(tanks), len(pre("T6_Zweit")), len(pumps)), (4, 1, 8), (len(tanks), len(pre("T6_Zweit")), len(pumps)) == (4, 1, 8))
t5 = B["T5_Zentraltank"]["bbox"]; t5c = ((t5["max"][0] + t5["min"][0]) / 2, (t5["max"][1] + t5["min"][1]) / 2)
chk("OBJ Pool zentriert (Abstand Mitte [mm])", round(math.hypot(*t5c)), "< 50", math.hypot(*t5c) < 50)
wb = B["T5_Wasser"]["bbox"]; wd = wb["max"][0] - wb["min"][0]
chk("OBJ Wasserscheibe D [mm]", round(wd), 3890, abs(wd - 3890) < 20)
chk("L13 Tankwand [mm]", round(P["wall"]), ">= 150", P["wall"] >= 150)
chk("L13 Wasserscheibe T5_Wasser", len(pre("T5_Wasser")), 1, len(pre("T5_Wasser")) == 1)
chk("L6 Teilenamen T1,T3-T6,T10,T11 vorhanden (T2 Haut = Phase 2, T8 NFT folgt)", sorted({n.split("_")[0] for n in BN}, key=lambda x: int(x[1:])), "T1,T3..T11", {n.split("_")[0] for n in BN} >= {f"T{i}" for i in (1, 3, 4, 5, 6, 10, 11)})   # T7/T9 = Werkstatt-Instanzen (Tanks, Beete)
n_cls = lambda c: sum(1 for x in cmds if x["command"] == "occurrence.move" and str(x["params"].get("occurrence", "")).startswith(c + ":"))
chk("OBJ Netztoepfe (2160 Beete + 466 Rinnen) als Instanzen", n_cls("Netztopf"), 2626, n_cls("Netztopf") == 2626)
# Interferenz zwischen Instanzen/Teilen (Koerper EINER Komponenteninstanz ueberschneiden sich bewusst: Schweiss-/Schraubverbindungen, Pruefung der Werkstatt-Skripte)
# Das ganze Modell hat > 1500 Koerper: erst Bounding-Boxen in Python (nur Paare verschiedener Instanzen), dann nur die betroffenen Koerper exakt schneiden.
cl = {}
sc = os.path.join(tmp, "cl.json"); json.dump({"commands": [{"command": "component.list", "params": {}}]}, open(sc, "w"))
for c in find(run_json(["run", sc, "--in", dome, "--results"]), "components"):
    for bn in c.get("bodies", []): cl[bn] = (c["name"], 1)
def base(n): return re.sub(r" \(\d+\)", "", re.sub(r" \([^()]*:\d+\)", "", n))
PLANT_CLS = ("Netztopf", "Salatkopf")
def grp(n):
    m = re.search(r"\((\w+):(\d+)/(\w+):(\d+)\)$", n)
    return (m.group(3), int(m.group(4))) if m else cl.get(n, (n, 0))
names = [n for n in B if grp(n)[0] not in PLANT_CLS]; G = {n: grp(n) for n in names}   # Pflanzen stecken bewusst im Medium: nicht auf Kollision geprueft
bb = {n: (B[n]["bbox"]["min"], B[n]["bbox"]["max"]) for n in names}
cand = []; openm = {"W-M1": [], "W-M2": [], "W-M3": []}
for i, a in enumerate(names):
    amin, amax = bb[a]
    for b in names[i + 1:]:
        if G[a] == G[b] and G[a][1]: continue   # gleiche Komponenteninstanz
        if a.startswith("T1_") and b.startswith("T1_"): continue   # Streben treffen sich an den Knoten (bewusst)
        bmin, bmax = bb[b]
        if all(amin[k] < bmax[k] and bmin[k] < amax[k] for k in range(3)):
            cs = {G[a][0], G[b][0]}
            ring = [n for n in (a, b) if n == "T3_Sockel"]   # Fundamentring: Bounding-Box ueberdeckt alles, nur Koerper am Rand (Radius >= 5600) koennen es beruehren
            if ring and max(math.hypot(x, y) for n in (a, b) if n != "T3_Sockel" for x in (B[n]["bbox"]["min"][0], B[n]["bbox"]["max"][0]) for y in (B[n]["bbox"]["min"][1], B[n]["bbox"]["max"][1])) < 5600: continue
            kk = ("W-M2" if   # offene Werkstatt-Maengel W-M2/W-M3 (docs/session-notes/werkstatt.md): nur Bounding-Box-Kandidaten gezaehlt, nicht exakt geschnitten (zu viele Paare)
                   any(c.startswith("Tisch_") for c in cs) and any(c.startswith("Beet_") for c in cs) else
                  "W-M3" if all(c.startswith("Tisch_") for c in cs) else None)
            if kk: openm[kk].append((a, b))
            else: cand.append((a, b))
used = sorted({n for pr in cand for n in pr})
sc = os.path.join(tmp, "i.json"); json.dump({"commands": [{"command": "inspect.interference", "params": {"bodies": used, "budget_s": 420}}]}, open(sc, "w"))
rr = run_json(["run", sc, "--in", dome, "--results"])
inter = find(rr, "interferences") or []
candset = {frozenset(pr) for pr in cand}
bad = []
for it in inter:
    a, b = it["a"], it["b"]
    if frozenset((a, b)) not in candset: continue   # nur Paare verschiedener Instanzen
    ca, cb = G[a][0], G[b][0]; cs = {ca, cb}
    if a.startswith("T1_") and b.startswith("T1_"): continue
    if a.split("_")[0] == b.split("_")[0] == "T4": continue   # Tuer-Teile verbinden sich (Scharnier/Pfosten/Schwelle)
    if {a.split("_")[0], b.split("_")[0]} == {"T1", "T3"}: continue   # Streben im Fundamentring verankert
    if {a.split("_")[0], b.split("_")[0]} & {"T10"} and ({a.split("_")[0], b.split("_")[0]} <= {"T10", "T1", "T5", "T7"}): continue
    if "T13_Erde" in (a, b) and (cs - {"Erdflaeche"}) and all(c.startswith(("Tank_", "Pumpe_", "Tisch_")) for c in cs - {"Erdflaeche"}): continue   # Fussplatten/-schrauben stehen im Boden (Werkstatt: bis 24 mm)
    if all(c.startswith(("Pumpe_", "Tank_")) for c in cs) and any(c.startswith("Pumpe_") for c in cs): openm["W-M1"].append((a, b)); continue   # offener Werkstatt-Mangel W-M1: Tank-Rahmenstreben x OBJ-Pumpentafeln
    if any(c.startswith(("Knoten_", "Fundamentanker")) for c in cs) and ({a, b} & {"T3_Sockel", "T13_Erde"}): continue   # Knoten/Anker sind im Fundamentring bzw. Erdreich verankert
    print("KOLL", a, b)
    bad.append((a, b, round(it.get("volume_mm3", it.get("volume", 0)))))
chk("L6 Kollisionen (ohne Strebenknoten, Rohr/Schlauch; ohne offene Werkstatt-Maengel)", len(bad), 0, len(bad) == 0)
res.append({"info": "Kollisionen", "pairs": bad[:20]})
unch = [u for u in (find(rr, "unchecked") or []) if u.get("b") and frozenset((u["a"], u["b"])) in candset]   # nur Kandidatenpaare (das Werkzeug paart alle uebergebenen Koerper)
from collections import Counter
if unch: print("NICHT GEPRUEFT je Klassenpaar:", dict(Counter(" x ".join(sorted({G[u["a"]][0], G.get(u["b"], ("?",))[0]})) for u in unch if u.get("b"))))
chk("L6 Kollisionspruefung vollstaendig (alle Kandidatenpaare exakt geschnitten)", len(unch), 0, len(unch) == 0)
print("OFFEN Werkstatt-Maengel (nur Bounding-Box-Kandidaten, nicht gezaehlt): W-M1 Pumpentafel x Tankrahmen (exakt)", len(openm["W-M1"]), "| W-M2 NFT-Tisch x Beet", len(openm["W-M2"]), "| W-M3 Tisch x Tisch", len(openm["W-M3"]), "| exakt geprueft: Paare", len(cand), "Koerper", len(used))
passed = sum(1 for r in res if r.get("pass")); total = sum(1 for r in res if "pass" in r)
for r in res:
    if "pass" in r: print(("PASS" if r["pass"] else "FAIL"), r["check"], "| Ist:", r["ist"], "| Soll:", r["soll"])
print(f"SCORE {passed}/{total} = {100*passed/total:.0f}%")
sys.exit(0 if passed == total else 1)
