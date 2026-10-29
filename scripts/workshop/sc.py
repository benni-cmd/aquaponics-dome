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
                self.add("parameters.add", name=k, expression=str(v))
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
