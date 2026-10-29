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
    pr, _ = sc.load_params("nft_rinne")
    ck.eq("netztopf Spiel im Rinnen-Topfloch (hole_d - rim_d = 2 mm)", pr["hole_d"] - pn["rim_d"], 2, 0.01)
    ps, ds = sc.load_params("salatkopf")
    pth = os.path.join(sc.ROOT, "designs", "components", "salatkopf.sc")
    ev = sc.evaluate(pth)
    n_leaves = ds["blatt_gruppen"]["verteilung"]["n"]
    ck.eq("salatkopf Blaetter (verteilung.n)", len([x for x in ev["bodies"] if x["name"].startswith("Blatt")]), n_leaves)
    mn, mx = sc.bbox_all(ev)
    wm = max(mx[0] - mn[0], mx[1] - mn[1])
    ck.eq("salatkopf Breite M 95-125", 1 if 95 <= wm <= 125 else 0, 1)
    lv = [x for x in ev["bodies"] if x["name"].startswith("Blatt")]
    ck.eq("salatkopf Blaetter nicht unter dem Topfrand (Z >= -1)", 1 if min(x["bbox"]["min"][2] for x in lv) >= -1.0 else 0, 1)
    ck.eq("salatkopf Hoehe ueber dem Topfrand M 50-70", 1 if 50 <= mx[2] <= 70 else 0, 1)
    inner_neck = pn["base_d"] + (pn["rim_d"] - pn["base_d"]) * (pn["cup_h"] - ps["neck_len"]) / pn["cup_h"] - 2 * pn["wall"]   # Innen-D des konischen Topfs in Halstiefe
    ck.eq(f"salatkopf Hals im Topf (Z -25..0, D16 < Topf-Innen-D in Halstiefe {inner_neck:.1f})", 1 if mn[2] >= -26 and ps["neck_d"] < inner_neck else 0, 1)
    ck.eq("salatkopf Flaechenbudget (<= 14 je Koerper, <= 1500 gesamt)", 1 if max(x["faces"] for x in ev["bodies"]) <= 14 and sum(x["faces"] for x in ev["bodies"]) <= 1500 else 0, 1)
    import subprocess
    script = os.path.join(sc.TMP, "ws-cfg.json")
    json.dump({"commands": [{"command": "config.table", "params": {}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", pth, "--results"], capture_output=True, text=True)
    rows = json.loads(r.stdout)[0].get("rows", []) if r.returncode == 0 else []
    names = {(x.get("name") if isinstance(x, dict) else x) for x in rows}
    ck.eq("salatkopf Konfigurationen S, M, L", 1 if {"S", "M", "L"} <= names else 0, 1)
    for row, f in (("S", 0.7), ("L", 1.3)):
        sp = os.path.join(sc.TMP, "ws-cfg-" + row + ".json")
        json.dump({"commands": [{"command": "config.activate", "params": {"row": row}}]}, open(sp, "w"))
        out = os.path.join(sc.TMP, "ws-cfg-" + row + ".sc")
        r = subprocess.run([sc.CLI, "run", sp, "--in", pth, "--save", out, "--quiet"], capture_output=True, text=True)
        if r.returncode == 0:
            e2 = sc.evaluate(out)
            m2, x2 = sc.bbox_all(e2)
            w2 = max(x2[0] - m2[0], x2[1] - m2[1])
            ck.eq(f"salatkopf Breite {row} = {f} x Breite M (+-6 %)", w2 / wm, f, 0.06 * f)
        else:
            ck.eq(f"salatkopf Konfiguration {row} laeuft", 0, 1)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
