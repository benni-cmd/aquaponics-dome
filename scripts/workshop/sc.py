"""Hilfsbibliothek der Komponenten-Werkstatt: Befehlsskript bauen, mit solidcraft-cli ausfuehren, rendern, messen.
Jede Komponente hat einen Generator scripts/workshop/<klasse>.py und Parameter in data/components/<klasse>.json."""
import json, os, subprocess, sys, tempfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
TMP = os.environ.get("WORKSHOP_TMP", tempfile.gettempdir())

def load_params(name):
    """data/components/<name>.json -> {param: wert}; Datei traegt je Parameter wert, einheit, herkunft."""
    d = json.load(open(os.path.join(ROOT, "data", "components", name + ".json"), encoding="utf-8"))
    return {k: v["wert"] for k, v in d["parameter"].items()}, d

class Build:
    def __init__(self):
        self.cmds = []
    def add(self, command, **params):
        self.cmds.append({"command": command, "params": params})
        return self
    def params_to_design(self, p, meta, unit_of):
        for k, v in p.items():
            u = unit_of.get(k, "")
            if u in ("mm", "deg"):
                self.add("parameters.add", name=k, expression=f"{v} {u}")
            elif u == "":
                self.add("parameters.add", name=k, expression=str(v), unit="")
    def write(self, name):
        path = os.path.join(TMP, f"ws-{name}.json")
        json.dump({"commands": self.cmds}, open(path, "w"))
        return path

def run(script, sc_out, extra=()):
    r = subprocess.run([CLI, "run", script, "--save", sc_out, "--quiet", *extra], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER run: " + r.stderr.strip() + r.stdout.strip())

def run_results(script):
    r = subprocess.run([CLI, "run", script, "--results"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER run: " + r.stderr.strip() + r.stdout.strip())
    return json.loads(r.stdout)

def evaluate(sc):
    r = subprocess.run([CLI, "eval", sc], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER eval: " + r.stderr.strip())
    return json.loads(r.stdout)

def snapshot(sc, out, target, yaw, pitch, dist, w=900, h=700, section=None, extra=()):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    cam = json.dumps({"target": target, "yaw": yaw, "pitch": pitch, "distance": dist})
    a = [CLI, "snapshot", sc, "--out", out, "--width", str(w), "--height", str(h), "--camera", cam, "--no-grid", "--no-axes", *extra]
    if section: a += ["--section", section]
    r = subprocess.run(a, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER snapshot: " + r.stderr.strip())

def bbox_all(ev):
    mn = [1e18]*3; mx = [-1e18]*3
    for b in ev["bodies"]:
        for i in range(3):
            mn[i] = min(mn[i], b["bbox"]["min"][i]); mx[i] = max(mx[i], b["bbox"]["max"][i])
    return mn, mx

def faces(sc_path, body):
    """model.faces eines Koerpers (Liste); Zylinderflaechen tragen 'cylinder': {axis, origin, radius}."""
    script = os.path.join(TMP, "ws-faces.json")
    json.dump({"commands": [{"command": "model.faces", "params": {"body": body}}]}, open(script, "w"))
    r = subprocess.run([CLI, "run", script, "--in", sc_path, "--results"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER faces: " + r.stderr.strip())
    return json.loads(r.stdout)[0]["faces"]

class Check:
    """Sammelt PASS/FAIL-Zeilen mit Ist und Soll; exit-Code 1 bei FAIL."""
    def __init__(self, name):
        self.name, self.rows = name, []
    def eq(self, label, ist, soll, tol=0.0):
        ok = abs(ist - soll) <= tol
        self.rows.append((label, ist, soll, ok))
        print(("PASS" if ok else "FAIL"), f"{self.name}: {label}: Ist {ist:g}, Soll {soll:g}" + (f" (+-{tol:g})" if tol else ""))
    def done(self):
        bad = [r for r in self.rows if not r[3]]
        print(f"== {self.name}: {len(self.rows) - len(bad)}/{len(self.rows)} PASS")
        return 0 if not bad else 1

def faces_multi(sc_path, bodies):
    """model.faces mehrerer Koerper in EINEM CLI-Lauf (grosse Designs werden nur einmal geladen): {name: [faces]}."""
    script = os.path.join(TMP, "ws-faces-multi.json")
    json.dump({"commands": [{"command": "model.faces", "params": {"body": b}} for b in bodies]}, open(script, "w"))
    r = subprocess.run([CLI, "run", script, "--in", sc_path, "--results"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER faces_multi: " + r.stderr.strip())
    return {x["body"]: x["faces"] for x in json.loads(r.stdout)}

def assign_part_materials(sc_path, material, pattern=r"Body\d+"):
    """Normteile aus parts.insert heissen 'Body<n>' und tragen die Standarddichte 1,29: Material nachtraeglich zuweisen (speichert die Datei neu)."""
    import re
    ev = evaluate(sc_path)
    names = [b["name"] for b in ev["bodies"] if re.fullmatch(pattern, b["name"])]
    if not names:
        return 0
    script = os.path.join(TMP, "ws-partmat.json")
    json.dump({"commands": [{"command": "material.assign", "params": {"bodies": names, "material": material}}]}, open(script, "w"))
    r = subprocess.run([CLI, "run", script, "--in", sc_path, "--save", sc_path, "--quiet"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER assign_part_materials: " + r.stderr.strip())
    return len(names)
