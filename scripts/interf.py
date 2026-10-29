"""Hilfsskript: listet Interferenzen (ohne Strebe-Strebe, Rohr/Tanks) gruppiert. Aufruf: python scripts/interf.py"""
import json, subprocess, tempfile, collections
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
t = tempfile.mkdtemp(); sc = t + "/i.json"
json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 150}}]}, open(sc, "w"))
subprocess.run([CLI, "run", sc, "--in", "designs/dome.sc", "--results", "--json-out", t + "/o.json"], capture_output=True)
d = json.load(open(t + "/o.json", encoding="utf-8"))
def find(o):
    if isinstance(o, dict):
        if "interferences" in o: return o["interferences"]
        for v in o.values():
            r = find(v)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v)
            if r is not None: return r
c = collections.Counter(); ex = {}
for i in find(d):
    a, b = i["a"], i["b"]
    if a.startswith("T1_") and b.startswith("T1_"): continue
    k = tuple(sorted((a.split("_")[0] + "_" + a.split("_")[1], b.split("_")[0] + "_" + b.split("_")[1]))); c[k] += 1; ex.setdefault(k, (a, b, round(i["volume_mm3"])))
for k, n in c.most_common(): print(n, ex[k])
