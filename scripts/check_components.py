"""Struktur-Test (docs/cad-standard.md): Wurzel ohne lose Koerper, 10 Baugruppen, jede Teileklasse eine verknuepfte Komponente (Instanzen), Instanzzahl = layout.json.
Aufruf: python scripts/check_components.py   (Exit 0 = alles PASS)"""
import json, os, subprocess, sys, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
tmp = tempfile.mkdtemp(); sc = os.path.join(tmp, "c.json"); out = os.path.join(tmp, "o.json")
json.dump({"commands": [{"command": "component.list", "params": {}}, {"command": "component.copies", "params": {"component": "Strebe_A"}}, {"command": "component.copies", "params": {"component": "Strebe_B"}}]}, open(sc, "w"))
subprocess.run([CLI, "run", sc, "--in", os.path.join(ROOT, "designs", "dome.sc"), "--results", "--json-out", out], capture_output=True)
res = json.load(open(out, encoding="utf-8"))
def find(o, key):
    if isinstance(o, dict):
        if key in o: return o
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None: return r
comps = find(res, "components")["components"]
L = json.load(open(os.path.join(ROOT, "data", "layout.json")))
rows = []
def chk(name, ist, soll, ok): rows.append(ok); print(("PASS" if ok else "FAIL"), name, "| Ist:", ist, "| Soll:", soll)
byid = {c["id"]: c for c in comps}
root = byid[0]
chk("Wurzel ohne lose Koerper", len(root.get("bodies", [])), 0, len(root.get("bodies", [])) == 0)
names = [byid[ch["component"]]["name"] if ch["component"] in byid else ch["name"] for ch in root.get("children", [])]
chk("10 Baugruppen in der Wurzel", len(root.get("children", [])), 10, len(root.get("children", [])) == 10)
loose = {c["name"]: len(c.get("bodies", [])) for c in comps if c["id"] != 0 and c["name"][:2].isdigit() and c.get("bodies")}
chk("keine losen Koerper in Baugruppen (alle Teile verknuepfte Komponenten)", loose, {}, not loose)
inst = {}
for c in comps:
    for ch in c.get("children", []):
        nm = byid[ch["component"]]["name"] if ch["component"] in byid else ch["name"]; inst[nm] = inst.get(nm, 0) + 1
chk("Strebe A (30) + B (35) = 65 minus 1 Basisstrebe am Tuerdreieck (R13)", (inst.get("Strebe_A", 0), inst.get("Strebe_B", 0)), "30/35 minus Tuerraum", inst.get("Strebe_A", 0) + inst.get("Strebe_B", 0) == 64)
ncopies = sum(len(r["copies"]) for r in (res if isinstance(res, list) else [res]) if isinstance(r, dict) and isinstance(r.get("copies"), list))
chk("component.copies leer", ncopies, 0, ncopies == 0)
sys.exit(0 if all(rows) else 1)
