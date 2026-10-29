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
cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
pre = lambda p: [b for n, b in B.items() if n.startswith(p)]
ext = lambda bs, i: (min(b["bbox"]["min"][i] for b in bs), max(b["bbox"]["max"][i] for b in bs))
res = []
def chk(name, ist, soll, ok): res.append({"check": name, "ist": ist, "soll": soll, "pass": bool(ok)})

t1 = pre("T1_"); sock_top = B["T3_Sockel"]["bbox"]["max"][2]
z0, z1 = ext(t1, 2); x0, x1 = ext(t1, 0)
h = z1 - sock_top - 75 - 45; w = x1 - x0 - 90
chk("L5/7 Kuppelhoehe [mm]", round(h), 6000, abs(h - 6000) / 6000 < 0.03)
chk("L5/7 Kuppelbreite [mm]", round(w), 12000, abs(w - 12000) / 12000 < 0.03)
chk("L5/7 Hoehe/Breite", round(h / w, 3), 0.5, abs(h / w - 0.5) / 0.5 < 0.03)
# Knotenvalenz aus Strebenenden
ends = {}
for c in cmds:
    p = c["params"]
    if c["command"] == "solid.cylinder" and str(p.get("name", "")).startswith("T1_"):
        b = p["base"]; u = p["axis"]; L = p["height"]
        for pt in (tuple(round(b[i] + u[i]*25) for i in range(3)), tuple(round(b[i] + u[i]*(L-25)) for i in range(3))):
            ends[pt] = ends.get(pt, 0) + 1
apex = max(ends, key=lambda k: k[2]); apex_n = ends[apex]
base_nodes = [k for k in ends if abs(k[2] - (sock_top + P['strut_r'] + 30)) < 5]
chk("L1/10 Streben am Scheitel", apex_n, 5, apex_n == 5)
chk("L10 Basisknoten (Zehneck)", len(base_nodes), 10, len(base_nodes) == 10)
chk("L10 Strebenzahl 2V (60 + 10 Basis - Tuer)", len(t1), "55-63", 55 <= len(t1) <= 63)
s = B["T3_Sockel"]; ue = (s["bbox"]["max"][0] - s["bbox"]["min"][0] - 12000) / 2
chk("L2/9/11 Sockel Seiten (Flaechen = 10 + 2)", s["faces"], 12, s["faces"] == 12)
chk("L9/11 Sockel Ueberstand [mm]", round(ue), "<= 300", ue <= 300)
chk("L11 Sockelhoehe [mm]", round(s["bbox"]["max"][2] - s["bbox"]["min"][2]), "300-500", 300 <= s["bbox"]["max"][2] - s["bbox"]["min"][2] <= 500)
beds = pre("T9_") + pre("T8_")
chk("OBJ Substratbeete T9 (14 IBC-Wannen)", len(pre("T9_")), 14, len(pre("T9_")) == 14)
chk("L12 Schlaeuche (1 je Tank)", len(pre("T10_Schlauch")), ">= 4", len(pre("T10_Schlauch")) >= 4)
d = B["T4_Tuer"]["bbox"]; dh = d["max"][2] - d["min"][2]
dw = math.hypot(d["max"][0] - d["min"][0], d["max"][1] - d["min"][1])
chk("Tuer Hoehe [mm]", round(dh), 2000, abs(dh - 2000) < 20)
chk("Tuer Breite (Rahmen) [mm]", round(P["door_w"]), 1000, abs(P["door_w"] - 1000) < 20)
# Zugang: kleinster seitlicher Abstand Tuer-Bett (Mittelpunkte der Bett-/Tuerboxen, Naeherung ueber bbox-Abstand)
def gap(a, b):
    return math.hypot(*[max(0, max(a["min"][i] - b["max"][i], b["min"][i] - a["max"][i])) for i in range(2)])
tg = min(gap(d, b["bbox"]) for b in beds)
chk("Tuerzugang: Abstand Tuer-Bett (bbox) [mm]", round(tg), ">= 1000", tg >= 1000)
t5 = B["T5_Zentraltank"]["bbox"]; t5d = t5["max"][0] - t5["min"][0]
chk("OBJ Tanks T7 (4 Tanks, kein Mitteltank)", (len(pre("T7_Tank_")), len(pre("T6_"))), (4, 0), (len(pre("T7_Tank_")), len(pre("T6_"))) == (4, 0))
t5 = B["T5_Zentraltank"]["bbox"]; t5c = ((t5["max"][0] + t5["min"][0]) / 2, (t5["max"][1] + t5["min"][1]) / 2)
chk("OBJ Pool zentriert (Abstand Mitte [mm])", round(math.hypot(*t5c)), "< 50", math.hypot(*t5c) < 50)
wb = B["T5_Wasser"]["bbox"]; wd = wb["max"][0] - wb["min"][0]
chk("OBJ Wasserscheibe D [mm]", round(wd), 3890, abs(wd - 3890) < 20)
chk("L13 Tankwand [mm]", round(P["wall"]), ">= 150", P["wall"] >= 150)
chk("L13 Wasserscheibe T5_Wasser", len(pre("T5_Wasser")), 1, len(pre("T5_Wasser")) == 1)
chk("L6 Teilenamen T1,T3-T5,T7-T11 vorhanden (T2 Haut = Phase 2, T6 laut OBJ entfallen)", sorted({n.split("_")[0] for n in B}, key=lambda x: int(x[1:])), "T1,T3..T11", {n.split("_")[0] for n in B} >= {f"T{i}" for i in (1, 3, 4, 5, 7, 8, 9, 10, 11)})
# Interferenz (T1-T1, Rohr durch Haut/Struts-Bereich und Schlaeuche an Tanks erlaubt)
sc = os.path.join(tmp, "i.json"); json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 150}}]}, open(sc, "w"))
rr = run_json(["run", sc, "--in", dome, "--results"])
inter = find(rr, "interferences") or []
bad = []
for it in inter:
    a, b = it["a"], it["b"]
    if a.startswith("T1_") and b.startswith("T1_"): continue
    if {a.split("_")[0], b.split("_")[0]} & {"T10"} and ({a.split("_")[0], b.split("_")[0]} <= {"T10", "T1", "T5", "T7"}): continue
    bad.append((a, b, round(it.get("volume_mm3", it.get("volume", 0)))))
chk("L6 Kollisionen (ohne Strebenknoten, Rohr/Schlauch)", len(bad), 0, len(bad) == 0)
res.append({"info": "Kollisionen", "pairs": bad[:20]})
passed = sum(1 for r in res if r.get("pass")); total = sum(1 for r in res if "pass" in r)
for r in res:
    if "pass" in r: print(("PASS" if r["pass"] else "FAIL"), r["check"], "| Ist:", r["ist"], "| Soll:", r["soll"])
print(f"SCORE {passed}/{total} = {100*passed/total:.0f}%")
sys.exit(0 if passed == total else 1)
