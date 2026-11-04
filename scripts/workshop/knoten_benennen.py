"""W60 5a: benennt die Normteil-Koerper Body<n> der Knoten-Dateien um (ScheibeO_k, Schraube_k, ScheibeU_k, Mutter_k je Arm k; Reihenfolge der Einfuegung wie in knoten.py),
ohne die Geometrie neu zu bauen (body.rename auf der vorhandenen .sc, speichert dieselbe Datei). Danach die drei Repraesentanten knoten_6/5/4.sc als Kopie von n01/n02/n17 (waren byte-gleich).
Aufruf: python -X utf8 scripts/workshop/knoten_benennen.py        (idempotent: Dateien ohne Body<n> bleiben unveraendert)"""
import glob, json, os, re, shutil, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

D = os.path.join(sc.ROOT, "designs", "components")
REPR = {"knoten_6_n01": "knoten_6", "knoten_5_n02": "knoten_5", "knoten_4_n17": "knoten_4"}

def rename_file(path):
    ev = sc.evaluate(path)
    nums = sorted(int(b["name"][4:]) for b in ev["bodies"] if re.fullmatch(r"Body\d+", b["name"]))
    if not nums:
        return 0
    assert nums == list(range(1, len(nums) + 1)) and len(nums) % 4 == 0, (path, nums)
    cmds = []
    for k in range(1, len(nums) // 4 + 1):
        names = (f"ScheibeO_{k}", f"Schraube_{k}", f"ScheibeU_{k}", f"Mutter_{k}")
        for j, nm in enumerate(names):
            cmds.append({"command": "body.rename", "params": {"body": f"Body{4 * k - 3 + j}", "name": nm}})
    script = os.path.join(sc.TMP, "ws-knoten-rename.json")
    json.dump({"commands": cmds}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--save", path, "--quiet"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER rename " + path + ": " + r.stderr.strip() + r.stdout.strip())
    return len(nums)

if __name__ == "__main__":
    n_ges = 0
    for p in sorted(glob.glob(os.path.join(D, "knoten_?_n*.sc"))):
        n = rename_file(p)
        n_ges += n
        print(os.path.basename(p), "umbenannt:", n)
    for src, dst in REPR.items():
        shutil.copyfile(os.path.join(D, src + ".sc"), os.path.join(D, dst + ".sc"))
    print("Koerper umbenannt:", n_ges)
