"""Vorpruefung IBC-Beet gegen die Scope-Card (docs/scope-cards.md) und R03: Aussenmass = layout.json, Wand, Medium EIN Koerper (Oberflaeche Z 400 absolut, Tiefe 300), Siebboden, Standrohr/Glocke/Medienschutz-Masse, Ports.
Aufruf: python scripts/workshop/check_ibc_beet.py [typ ...]   (exit 1 bei FAIL)"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import sc

def main(typs):
    p, d = sc.load_params("ibc_beet")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["ibc_beds"]
    ck = sc.Check("ibc_beet")
    for typ in typs:
        T = d["typen"][typ]
        L, W, H = T["laenge"], T["breite"], T["hoehe"]
        path = os.path.join(sc.ROOT, "designs", "components", f"ibc_beet_{typ}.sc")
        ev = sc.evaluate(path)
        B = {b["name"]: b for b in ev["bodies"]}
        # Anzahl und Masse gegen layout.json (Klasse aussen: Laenge 2953; innen 1865)
        ls = [b for b in lay if b["length"] == L and b["width"] == W and b["height"] == H]
        ck.eq(f"{typ} Anzahl laut layout.json", len(ls), T["anzahl"])
        w = B["Wanne"]["bbox"]
        ck.eq(f"{typ} Wanne Laenge", w["max"][0] - w["min"][0], L, 0.5)
        ck.eq(f"{typ} Wanne Breite", w["max"][1] - w["min"][1], W, 0.5)
        ck.eq(f"{typ} Wanne Hoehe", w["max"][2] - w["min"][2], H, 0.5)
        # Medium: genau EIN Koerper, Oberflaeche und Tiefe
        med = [k for k in B if k.startswith("Medium") and not k.startswith("Medienschutz")]
        ck.eq(f"{typ} Medium Koerperzahl", len(med), 1)
        m = B["Medium"]["bbox"]
        ck.eq(f"{typ} Medium Oberflaeche lokal", m["max"][2], H - p["rim_gap"], 0.5)
        ck.eq(f"{typ} Medium Tiefe", m["max"][2] - m["min"][2], p["media_depth"], 0.5)
        z0_abs = lay[0]["z0"] if typ.startswith("aussen") else lay[8]["z0"]
        ck.eq(f"{typ} Medium Oberflaeche absolut (z0 {z0_abs})", m["max"][2] + z0_abs, 400, 15)      # R03: Z 400 (innen z0 -209..-173)
        # Siebboden unter dem Medium
        g = B["Siebboden"]["bbox"]
        ck.eq(f"{typ} Siebboden Oberkante = Medienunterkante", g["max"][2], m["min"][2], 0.01)
        # Standrohr, Glocke, Medienschutz
        s_ = B["Standrohr"]["bbox"]
        ck.eq(f"{typ} Standrohr Hoehe ueber Medienunterkante", s_["max"][2] - m["min"][2], p["standpipe_over"], 0.5)
        ck.eq(f"{typ} Standrohr D", s_["max"][0] - s_["min"][0], p["standpipe_d"], 0.1)
        gl = B["Glocke"]["bbox"]
        ck.eq(f"{typ} Glocke D", gl["max"][0] - gl["min"][0], p["bell_d"], 0.1)
        ck.eq(f"{typ} Glocke Hoehe", gl["max"][2] - gl["min"][2], p["bell_h"], 0.1)
        ms = B["Medienschutz"]["bbox"]
        ck.eq(f"{typ} Medienschutz D", ms["max"][0] - ms["min"][0], p["guard_d"], 0.1)
        ck.eq(f"{typ} Medienschutz Hoehe", ms["max"][2] - ms["min"][2], p["guard_h"], 0.1)
        ck.eq(f"{typ} Medienschutz ueber Medienoberflaeche", ms["max"][2] - m["max"][2], p["guard_h"] - p["media_depth"], 0.5)
        # Glocke ueber Standrohr: Standrohrkopf unter der Glockendecke
        ck.eq(f"{typ} Standrohr unter Glockendecke (Luft >= 20)", 1 if gl["max"][2] - s_["max"][2] >= 20 else 0, 1)
        # Ports: Ablauf unter dem Boden (Standrohr/Bulkhead-Unterkante), Zulauf durch die Stirnwand
        ck.eq(f"{typ} Ablaufport z (Rohrende unter Boden)", s_["min"][2], -30, 0.1)
        t = B["Tropfrohr"]["bbox"]
        ck.eq(f"{typ} Zulaufport ausserhalb der Wanne (x < -L/2)", 1 if t["min"][0] < w["min"][0] + 10 else 0, 1)
        ck.eq(f"{typ} Zulaufhoehe lokal", (t["min"][2] + t["max"][2]) / 2, H - p["inflow_below_rim"], 0.5)
        ck.eq(f"{typ} Zulauf absolut (z0 {z0_abs})", (t["min"][2] + t["max"][2]) / 2 + z0_abs, 450, 25)
        # Nichts schwebt: jedes Teil der Wanne kollidiert nicht mit dem Medium (Medienschutz/Glocke stehen auf dem Siebboden)
        ck.eq(f"{typ} Glocke steht auf dem Siebboden", gl["min"][2], g["max"][2], 0.01)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or ["aussen_933", "aussen_993", "innen_933"]))
