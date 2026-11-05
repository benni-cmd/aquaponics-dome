"""Bauteile Strebe A und B der 2V-Kuppel als Rundrohr (D91, R56): Rohr strut_d x strut_wall (42,4 x 2,6, EN 10255 verzinkt).
Laenge = Rohrmund bis Rohrmund der beiden Scherenknoten, gemessen in der Montage-Lage (scripts/knoten_montage.py rohrlaengen, aus
scripts/.segs.json): Mitte der Spanne je Typ. Nennmass ohne Plattendrehung (knoten_schere.json geometrie.rohr_mm) A 3075,3 / B 3503,5;
die 6-Loch-Platte (D91) verschiebt an den 5-wertigen Knoten die Rohrmuender, A streut 3075,5 bis 3078,7.
Je Rohrende zwei Gegenloecher wall_hole (D 13) fuer die Nasen der Schere, 46 mm hinter dem Rohrmund (b_pivot_to_nose - pivot_out),
je auf der Mittelebene ihrer Lasche (x = -+ link_t/2).
Rahmen: Ursprung = Rohrmund am Anfang, Achse +Z, X = Laschennormale (Kuppel aussen), Y = Z x X (Nasenrichtung).
Lage der Nasen (gen_dome.py place_struts, scripts/knoten_montage.py): Anfang Lasche 1 (x -t/2) nach +Y, Lasche 2 (x +t/2) nach -Y;
Ende umgekehrt (der Arm am anderen Knoten schaut in Gegenrichtung).
Profil und Wand kommen nur aus data/params.json (strut_d, strut_wall); N-STATIK aendert dort, das Skript bleibt.
Aufruf: python -X utf8 scripts/components/strebe.py [--out <ordner>]   (Standard: designs/components)"""
import json, os, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
MAT, DENS, COL = "Stahl verzinkt", 7.85, "#b9c0c8"   # Katalog data/katalog.json stahl_verzinkt (sc_material 'Stahl verzinkt', 7,85 g/cm3)
P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
KS = json.load(open(os.path.join(ROOT, "data", "components", "knoten_schere.json"), encoding="utf-8"))
KP = {k: v["wert"] for k, v in KS["parameter"].items()}
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "designs", "components")
os.makedirs(out, exist_ok=True)
d, w = P["strut_d"], P["strut_wall"]
if abs(d - KP["tube_d"]) > 1e-6 or abs(w - KP["tube_t"]) > 1e-6:
    sys.exit(f"Strebe {d} x {w} passt nicht zum Scherenknoten-Rohr {KP['tube_d']} x {KP['tube_t']} (data/components/knoten_schere.json)")
t, hole = KP["link_t"], KP["wall_hole"]
s_hole = KP["b_pivot_to_nose"] - KP["pivot_out"]       # Gegenloch hinter dem Rohrmund (46 mm)
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import knoten_montage as KM
LEN = KM.rohrlaengen(json.load(open(os.path.join(ROOT, "scripts", ".segs.json"))), P["door_az"] - 167)
for key in ("a", "b"):
    L = LEN[key.upper()][0]; nm = f"T1_Strebe_{key.upper()}"
    cmds = [{"command": "parameters.add", "params": {"name": "strut_d", "expression": f"{d} mm"}},
            {"command": "parameters.add", "params": {"name": "strut_wall", "expression": f"{w} mm"}},
            {"command": "material.create", "params": {"name": MAT, "density_g_cm3": DENS, "color": COL, "pbr": {"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5}}},
            {"command": "solid.cylinder", "params": {"diameter": d, "height": L, "base": [0, 0, 0], "axis": [0, 0, 1], "operation": "new", "name": nm, "body_name": nm}},
            {"command": "solid.cylinder", "params": {"diameter": round(d - 2 * w, 4), "height": L + 2, "base": [0, 0, -1], "axis": [0, 0, 1], "operation": "cut", "targets": [nm], "name": f"{nm}_Innen"}}]
    # Bohrzylinder 14 mm ab 12 mm Achsabstand (ganz durch die Wand; kuerzer liefert bei 3 m Rohr einen fehlerhaften Boolean, gemessen 05.11.)
    # (z, x, Richtung y): Anfang Lasche 1 +Y, Lasche 2 -Y; Ende Lasche 1 -Y, Lasche 2 +Y
    for j, (z, x, sy) in enumerate(((s_hole, -t / 2, 1), (s_hole, t / 2, -1), (L - s_hole, -t / 2, -1), (L - s_hole, t / 2, 1)), 1):
        cmds.append({"command": "solid.cylinder", "params": {"diameter": hole, "height": w + 11.4, "base": [round(x, 4), round(sy * (d / 2 - w - 6.6), 4), round(z, 4)],
                                                               "axis": [0, sy, 0], "operation": "cut", "targets": [nm], "name": f"{nm}_Gegenloch_{j}"}})
    cmds.append({"command": "material.assign", "params": {"bodies": [nm], "material": MAT}})
    tmp = os.path.join(out, f"_strebe_{key}.json"); json.dump({"commands": cmds}, open(tmp, "w"))
    subprocess.run([CLI, "run", tmp, "--save", os.path.join(out, f"strebe_{key}.sc"), "--quiet"], check=True); os.remove(tmp)
    print(f"strebe_{key}.sc L={L} (Spanne {LEN[key.upper()][1]:.1f} .. {LEN[key.upper()][2]:.1f}) Rund {d} x {w}, 4 Gegenloecher D{hole:g} bei {s_hole:g} mm vom Rohrmund")
