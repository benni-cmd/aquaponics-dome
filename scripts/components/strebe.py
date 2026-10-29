"""Bauteile Strebe A (Laenge 0,5465 R) und Strebe B (0,618 R) der 2V-Kuppel (layout.json: 3279 / 3708 mm). Ursprung = Strebenanfang, Achse +Z.
Aufruf: python scripts/components/strebe.py   -> schreibt designs/components/strebe_a.sc und strebe_b.sc"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"))).items()}
R = P["dome_base_d"] / 2
for key, f in (("a", 0.5465), ("b", 0.6180)):
    L = round(R * f, 1); nm = f"T1_Strebe_{key.upper()}"
    cmds = [{"command": "solid.cylinder", "params": {"radius": P["strut_r"], "height": L, "base": [0, 0, 0], "axis": [0, 0, 1], "operation": "new", "name": nm, "body_name": nm}},
            {"command": "appearance.assign", "params": {"bodies": [nm], "color": "#b9c0c8"}}]
    tmp = os.path.join(ROOT, "scripts", f"_strebe_{key}.json"); json.dump({"commands": cmds}, open(tmp, "w"))
    subprocess.run([CLI, "run", tmp, "--save", os.path.join(ROOT, "designs", "components", f"strebe_{key}.sc"), "--quiet"], check=True); os.remove(tmp)
    print(f"strebe_{key}.sc L={L}")
