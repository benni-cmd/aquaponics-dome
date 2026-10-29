"""Vorpruefung Netztopf und Salatkopf (Scope-Card salatkopf/netztopf, layout.json pots): Netztopf 50 x 64 x 63, 8 Schlitze, PP; Salatkopf: Blattzahl, Breite 95-125, Hoehe 55-70, Hals im Topf, Konfigurationen S/M/L.
Aufruf: python scripts/workshop/check_pflanze.py   (exit 1 bei FAIL)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import sc

def main():
    ck = sc.Check("pflanze")
    pn, dn = sc.load_params("netztopf")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["pots"]
    pth = os.path.join(sc.ROOT, "designs", "components", "netztopf.sc")
    ev = sc.evaluate(pth)
    b = ev["bodies"][0]
    mn, mx = b["bbox"]["min"], b["bbox"]["max"]
    ck.eq("netztopf Hoehe (OBJ 63)", mx[2] - mn[2], 63, 0.1)
    ck.eq("netztopf Kragen-D (OBJ 64)", mx[0] - mn[0], 64, 0.1)
    ck.eq("netztopf Bezugspunkt Boden Z=0", mn[2], 0, 0.01)
    ck.eq("netztopf Schlitze (8)", (b["face_types"].get("plane", 0) - 4) / 4, pn["slot_count"], 0.01)
    ck.eq("netztopf Material PP", 1 if b["material"] == "PP" else 0, 1)
    ck.eq("netztopf Masse 14-20 g", 1 if 14 <= b["mass_g"] <= 20 else 0, 1)
    ck.eq("netztopf Anzahl 2160 laut layout.json", lay["total"], 2160)
    ck.eq("netztopf OBJ-Mass 50 x 64 x 63", 1 if sorted(lay["size_mm"]) == [50, 63, 64] or sorted(round(v) for v in lay["size_mm"]) == [50, 63, 64] else 0, 1)
    ps, ds = sc.load_params("salatkopf")
    pth = os.path.join(sc.ROOT, "designs", "components", "salatkopf.sc")
    ev = sc.evaluate(pth)
    n_leaves = sum(g["n"] for g in ds["blatt_gruppen"]["gruppen"])
    ck.eq("salatkopf Blaetter (Summe der Gruppen)", len([x for x in ev["bodies"] if x["name"].startswith("Blatt")]), n_leaves)
    mn, mx = sc.bbox_all(ev)
    ck.eq("salatkopf Breite M 95-125", 1 if 95 <= (mx[0] - mn[0]) <= 125 else 0, 1)
    ck.eq("salatkopf Hoehe ueber dem Topfrand M 50-70", 1 if 50 <= mx[2] <= 70 else 0, 1)
    ck.eq("salatkopf Hals im Topf (Z -25..0, D16 < Topf-Innen-D 47)", 1 if mn[2] >= -26 and ps["neck_d"] < 47 else 0, 1)
    ck.eq("salatkopf Wenige Flaechen (< 8 je Koerper)", 1 if max(x["faces"] for x in ev["bodies"]) < 8 else 0, 1)
    import subprocess
    script = os.path.join(sc.TMP, "ws-cfg.json")
    json.dump({"commands": [{"command": "config.table", "params": {}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", pth, "--results"], capture_output=True, text=True)
    rows = json.loads(r.stdout)[0].get("rows", []) if r.returncode == 0 else []
    names = {(x.get("name") if isinstance(x, dict) else x) for x in rows}
    ck.eq("salatkopf Konfigurationen S, M, L", 1 if {"S", "M", "L"} <= names else 0, 1)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
