"""Rinnenvarianten je Reihe (W16): nft_rinne_<typ>_r<k>.sc aus der Master-Datei nft_rinne.sc (Parameter len_l, n_holes, shift; Phase a/b = Zickzack), Laengen aus tisch_geom.geometry.
Aufruf: python scripts/workshop/rinnen_reihen.py [typ ...]"""
import json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def main(typs):
    p, d = sc.load_params("nft_tisch")
    master = os.path.join(sc.ROOT, "designs", "components", "nft_rinne.sc")
    for typ in typs:
        G = TG.geometry(typ, p, d["typen"][typ])
        for r in G["rows"]:
            f = f"nft_rinne_{typ}_r{r['k'] + 1}.sc"
            script = os.path.join(sc.TMP, f"rr-{typ}-{r['k']}.json")
            json.dump({"commands": [{"command": "parameters.change", "params": {"changes": {"len_l": f"{r['L']} mm", "n_holes": str(r["n_holes"]), "shift": f"{r['shift']} mm"}}}]}, open(script, "w"))
            out = os.path.join(sc.ROOT, "designs", "components", f)
            res = subprocess.run([sc.CLI, "run", script, "--in", master, "--save", out, "--quiet"], capture_output=True, text=True)
            if res.returncode != 0:
                sys.exit("FEHLER " + f + ": " + res.stderr + res.stdout)
            ev = sc.evaluate(out)
            pr = [b for b in ev["bodies"] if b["name"] == "Rinnenprofil"][0]
            print(f, "Laenge", round(pr["bbox"]["max"][0] - pr["bbox"]["min"][0], 1), "Soll", r["L"], "Flaechen", pr["faces"])

if __name__ == "__main__":
    main([a for a in sys.argv[1:]] or ["innen", "mitte", "aussen"])
