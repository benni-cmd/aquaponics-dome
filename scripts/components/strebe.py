"""Bauteile Strebe A (Laenge 0,5465 R) und Strebe B (0,618 R) der 2V-Kuppel (layout.json: 3279 / 3708 mm Knoten-Knoten).
Hohles Vierkantrohr strut_profile x strut_profile x strut_wall (30 x 30 x 3, Knotenblatt), Werkstoff 'Stahl verzinkt' (Katalog stahl_verzinkt).
Ursprung = Strebenanfang, Achse +Z, Rohrflaechen parallel zu X und Y (Rollwinkel setzt die Montage, gen_dome.py place_struts).
Der Steckarm des Knotens (23 x 23) steckt 80 mm im durchgehenden Innenmass (strut_profile - 2 x strut_wall = 24); keine eigene Aufnahme mehr.
Profil und Wand kommen nur aus data/params.json: N-STATIK aendert dort (z. B. 40/4), das Skript bleibt.
Aufruf: python -X utf8 scripts/components/strebe.py [--out <ordner>]   (Standard: designs/components)"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
MAT, DENS, COL = "Stahl verzinkt", 7.85, "#b9c0c8"   # Katalog data/katalog.json stahl_verzinkt (sc_material 'Stahl verzinkt', 7,85 g/cm3)
P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "designs", "components")
os.makedirs(out, exist_ok=True)
R = P["dome_base_d"] / 2
a, w = P["strut_profile"], P["strut_wall"]; i = a - 2 * w
if i <= 0: sys.exit(f"strut_wall {w} zu dick fuer strut_profile {a}")
for key, f in (("a", 0.5465), ("b", 0.6180)):
    L = round(R * f - 2 * P["strut_end_offset"], 1); nm = f"T1_Strebe_{key.upper()}"   # Knoten-Knoten-Abstand minus 2 x Endversatz; Ursprung = Strebenanfang (120 mm hinter der Knotenmitte)
    cmds = [{"command": "parameters.add", "params": {"name": "strut_profile", "expression": f"{a} mm"}},
            {"command": "parameters.add", "params": {"name": "strut_wall", "expression": f"{w} mm"}},
            {"command": "material.create", "params": {"name": MAT, "density_g_cm3": DENS, "color": COL, "pbr": {"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5}}},
            {"command": "solid.box", "params": {"length": a, "width": a, "height": L, "center": [0, 0, L / 2], "operation": "new", "name": nm, "body_name": nm}},
            {"command": "solid.box", "params": {"length": i, "width": i, "height": L + 2, "center": [0, 0, L / 2], "operation": "cut", "targets": [nm], "name": f"{nm}_Innen"}},
            {"command": "material.assign", "params": {"bodies": [nm], "material": MAT}}]
    tmp = os.path.join(out, f"_strebe_{key}.json"); json.dump({"commands": cmds}, open(tmp, "w"))
    subprocess.run([CLI, "run", tmp, "--save", os.path.join(out, f"strebe_{key}.sc"), "--quiet"], check=True); os.remove(tmp)
    print(f"strebe_{key}.sc L={L} Profil {a}x{a}x{w} Innen {i}")
