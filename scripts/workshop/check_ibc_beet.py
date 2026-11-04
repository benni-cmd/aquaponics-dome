"""Vorpruefung IBC-Beet gegen die Scope-Card (docs/scope-cards.md) und R03: Aussenmass = layout.json, Wand, Medium EIN Koerper (Oberflaeche Z 400 absolut, Tiefe 300), Siebboden, Standrohr/Glocke/Medienschutz-Masse, Ports.
Aufruf: python scripts/workshop/check_ibc_beet.py [typ ...] [--no-interf]   (exit 1 bei FAIL; Interferenz je Typ etwa 80 s)
W40-BEET V3 (D77): Sperrboden ungelocht, Kerben, Lochblech-Medienschutz, Reinigungsschacht, Reduktion, Reduzierhuelsen."""
import sys, os, json, math, re, subprocess, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import sc

def n_interf(path):
    """Anzahl Interferenzen im Bauteil (inspect.interference, alle Koerperpaare); -1 bei Fehler."""
    t = tempfile.mkdtemp()
    js, out = os.path.join(t, "i.json"), os.path.join(t, "o.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 200}}]}, open(js, "w"))
    subprocess.run([sc.CLI, "run", js, "--in", path, "--results", "--json-out", out], capture_output=True)
    try:
        d = json.load(open(out, encoding="utf-8"))
    except Exception:
        return -1
    def find(o):
        if isinstance(o, dict):
            if "interferences" in o: return o["interferences"]
            for v in o.values():
                r = find(v)
                if r is not None: return r
        elif isinstance(o, list):
            for v in o:
                r = find(v)
                if r is not None: return r
    L = find(d)
    return -1 if L is None else len(L)

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
        if typ == "aussen_800":                                    # W17: Sollmass aus D29, im Layout noch nicht gesetzt (Montage M7): Anzahl = Aussenbeete (mit 'plants')
            ls = [b for b in lay if "plants" in b]
        else:
            ls = [b for b in lay if b["length"] == L and b["width"] == W and b["height"] == H]
        ck.eq(f"{typ} Anzahl laut layout.json" + (" (Aussenbeete, Mass erst nach M7)" if typ == "aussen_800" else ""), len(ls), T["anzahl"])
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
        if T.get("fase"):                                          # W26/D44: Medium-Grundflaeche = Rechteck - 4 Ecken (c^2/2) - Loch Medienschutz; Fase am Medium-Umriss parallel versetzt (c - d x (2 - sqrt 2))
            Wi_, Li_ = W - 2 * p["rim_w"] - 2 * p["wall"], L - 2 * p["rim_w"] - 2 * p["wall"]
            wm, lm = Wi_ - 2 * p["media_gap"], Li_ - 2 * p["media_gap"]
            cm = T["fase"] - (W - wm) / 2.0 * (2 - 2 ** 0.5)
            area = lm * wm - 2 * cm * cm - 3.141592653589793 * (p["guard_d"] / 2.0) ** 2 - 3.141592653589793 * (p["shaft_d"] / 2.0) ** 2
            ck.eq(f"{typ} Medium-Volumen (Liter) mit Eckenfase {T['fase']} (Medium-Fase {cm:.1f}) gegen Flaechenrechnung", B["Medium"]["volume_mm3"] / 1e6, area * p["media_depth"] / 1e6, 0.5)
        if T.get("fase"):                                          # Zulauf-Tropfrohr liegt vor der Eckenfase (gerade Stirnwand), sonst durchstoesst das Rohr die schraege Wand ohne Bohrung
            c_a = T["fase"] - ((W - (W - 2 * p["rim_w"])) / 2.0) * (2 - 2 ** 0.5)
            tr = B["Tropfrohr"]["bbox"]
            y_edge = (W - 2 * p["rim_w"]) / 2.0 - c_a                                  # Beginn der Fase an der Stirnwand (|y|)
            ck.eq(f"{typ} Zulauf-Tropfrohr: |y| {max(abs(tr['min'][1]), abs(tr['max'][1])):.0f} liegt vor dem Fasenbeginn {y_edge:.0f} (Rohr trifft die gerade Stirnwand)", 1 if max(abs(tr["min"][1]), abs(tr["max"][1])) <= y_edge - 10 else 0, 1)
        z0_abs = lay[0]["z0"] if typ.startswith("aussen") else lay[8]["z0"]
        tol_abs = 15 if typ.startswith("aussen") else 40            # innen: OBJ-Beete liegen z0 -209..-170 (Rand Z 440-479): Oberflaeche absolut 365-404
        ck.eq(f"{typ} Medium Oberflaeche absolut (z0 {z0_abs})", m["max"][2] + z0_abs, 400, tol_abs)      # R03: Z 400
        # --- W40-BEET V3 (D77): Sperrboden ungelocht, Kerben, Medienschutz, Reinigungsschacht, Reduktion, Reduzierhuelsen
        PI = math.pi
        Wi_, Li_ = W - 2 * p["rim_w"] - 2 * p["wall"], L - 2 * p["rim_w"] - 2 * p["wall"]
        wm_, lm_ = Wi_ - 2 * p["media_gap"], Li_ - 2 * p["media_gap"]
        if T.get("fase"):
            cm_ = T["fase"] - (W - wm_) / 2.0 * (2 - 2 ** 0.5)
            a_kontur = lm_ * wm_ - 2 * cm_ * cm_
        else:
            a_kontur = lm_ * wm_ - (4 - PI) * (p["corner_r"] - p["media_gap"]) ** 2
        sb = B["Siebboden"]
        ck.eq(f"{typ} Siebboden Dicke", sb["bbox"]["max"][2] - sb["bbox"]["min"][2], p["grid_t"], 0.01)
        ck.eq(f"{typ} Siebboden Volumen (Liter) = Flaeche x {p['grid_t']} mm minus Durchfuehrung d{p['bulkhead_d']} (ungelocht, kein Lochabzug)", sb["volume_mm3"] / 1e6, (a_kontur * p["grid_t"] - PI / 4 * p["bulkhead_d"] ** 2 * p["grid_t"]) / 1e6, 0.02)
        ck.eq(f"{typ} Medium-Volumen (Liter) gegen Flaechenrechnung (Loecher Schutz d{p['guard_d']} und Schacht d{p['shaft_d']})", B["Medium"]["volume_mm3"] / 1e6, (a_kontur - PI / 4 * p["guard_d"] ** 2 - PI / 4 * p["shaft_d"] ** 2) * p["media_depth"] / 1e6, 0.5)
        ck.eq(f"{typ} keine Siebloch-Koerper (Sperrboden)", 1 if not [k for k in B if k.startswith("Sieb_Loch")] else 0, 1)
        z_kerbe = p["bell_slot_z"] + p["bell_slot_h"]
        ck.eq(f"{typ} Kerben-Oberkante z {m['min'][2] + z_kerbe:.0f} (Plattenoberkante {m['min'][2]:.0f} + {z_kerbe}) hoechstens +12", 1 if z_kerbe <= 12 else 0, 1)
        a_sp_ = PI / 4 * (p["standpipe_d"] - 2 * p["standpipe_wall"]) ** 2
        ck.eq(f"{typ} Kerbenflaeche 4 x {p['bell_slot_w']} x {p['bell_slot_h']} = {4 * p['bell_slot_w'] * p['bell_slot_h']} mm2 >= Standrohrflaeche {a_sp_:.0f}", 1 if 4 * p["bell_slot_w"] * p["bell_slot_h"] >= a_sp_ else 0, 1)
        v_gl0 = PI / 4 * (p["bell_d"] ** 2 - (p["bell_d"] - 2 * p["bell_wall"]) ** 2) * p["bell_h"] + PI / 4 * (p["bell_d"] - 2 * p["bell_wall"]) ** 2 * p["bell_wall"]
        v_cut = 4 * p["bell_slot_w"] * p["bell_slot_h"] * p["bell_wall"] + p["air_hole"] ** 2 * p["bell_wall"]
        r_gl = (v_gl0 - B["Glocke"]["volume_mm3"]) / v_cut
        ck.eq(f"{typ} Glocke Volumen: 4 Kerben + Luftloch herausgeschnitten ({r_gl:.2f} x erwartet)", 1 if 0.85 <= r_gl <= 1.15 else 0, 1)
        # Medienschutz: V2A-Lochblech, 2 Ringe x 12 Schlitze 5 x 50 = 6000 mm2 >= 15 x Standrohr, Kappe lose obendrauf
        v_gd = PI / 4 * (p["guard_d"] ** 2 - (p["guard_d"] - 2 * p["guard_wall"]) ** 2) * p["guard_h"]
        v_sl = 2 * p["guard_slot_n"] * p["guard_slot_w"] * p["guard_slot_h"] * p["guard_wall"]
        r_gd = (v_gd - B["Medienschutz"]["volume_mm3"]) / v_sl
        ck.eq(f"{typ} Medienschutz Volumen: 2 x {int(p['guard_slot_n'])} Schlitze herausgeschnitten ({r_gd:.2f} x erwartet)", 1 if 0.9 <= r_gd <= 1.1 else 0, 1)
        a_sl = 2 * p["guard_slot_n"] * p["guard_slot_w"] * p["guard_slot_h"]
        ck.eq(f"{typ} Medienschutz Schlitzflaeche {a_sl:.0f} mm2 >= 15 x Standrohr", 1 if a_sl >= 15 * a_sp_ else 0, 1)
        ck.eq(f"{typ} Schutzkappe sitzt auf dem Medienschutz", B["Schutzkappe"]["bbox"]["min"][2], B["Medienschutz"]["bbox"]["max"][2], 0.01)
        # Reinigungsschacht d110, stehend auf dem Sperrboden, Oberkante 20 ueber Medium
        rs = B["Reinigungsschacht"]["bbox"]
        ck.eq(f"{typ} Reinigungsschacht D", rs["max"][0] - rs["min"][0], p["shaft_d"], 0.1)
        ck.eq(f"{typ} Reinigungsschacht steht auf dem Sperrboden", rs["min"][2], sb["bbox"]["max"][2], 0.01)
        ck.eq(f"{typ} Reinigungsschacht Oberkante ueber Medienoberflaeche", rs["max"][2] - m["max"][2], p["shaft_over"], 0.5)
        ck.eq(f"{typ} Reinigungsschacht Lage x = -Li/2 + 250", (rs["min"][0] + rs["max"][0]) / 2, -Li_ / 2 + 250, 0.5)
        ck.eq(f"{typ} Schachtkappe sitzt auf dem Schacht", B["Schachtkappe"]["bbox"]["min"][2], rs["max"][2], 0.01)
        # Reduktion d40 x d25 unter dem Port, Reduzierhuelsen 32/25 in Boden- und Plattenhuelse
        rd = B["Reduktion"]["bbox"]
        ck.eq(f"{typ} Reduktion Oberkante = Port z -30", rd["max"][2], -30, 0.1)
        ck.eq(f"{typ} Reduktion Bauhoehe", rd["max"][2] - rd["min"][2], p["reduktion_h"], 0.1)
        ck.eq(f"{typ} Reduktion groesster D (Uebergang)", rd["max"][0] - rd["min"][0], 46, 0.1)
        for nm in ("Bulkhead", "Plattenhuelse"):
            ck.eq(f"{typ} {nm} Flansch D", B[nm]["bbox"]["max"][0] - B[nm]["bbox"]["min"][0], p["bulkhead_flange"], 0.1)
        for nm in ("Reduzierhuelse_Boden", "Reduzierhuelse_Platte"):
            ck.eq(f"{typ} {nm} Aussen-D = Tankverbinder-Innen d{p['bulkhead_id']}", B[nm]["bbox"]["max"][0] - B[nm]["bbox"]["min"][0], p["bulkhead_id"], 0.1)
        ck.eq(f"{typ} Plattenhuelse: Flansch auf Plattenoberkante", B["Plattenhuelse"]["bbox"]["max"][2], sb["bbox"]["max"][2] + 4, 0.01)
        ck.eq(f"{typ} alle Koerper benannt (keine Body<n>)", 1 if not [k for k in B if re.match(r"Body[0-9]+", k)] else 0, 1)
        if "--no-interf" not in sys.argv:
            ck.eq(f"{typ} Interferenzen (inspect.interference)", n_interf(path), 0)
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
        ck.eq(f"{typ} Zulauf absolut (z0 {z0_abs})", (t["min"][2] + t["max"][2]) / 2 + z0_abs, 450, tol_abs + 10)
        # Nichts schwebt: jedes Teil der Wanne kollidiert nicht mit dem Medium (Medienschutz/Glocke stehen auf dem Siebboden)
        ck.eq(f"{typ} Glocke steht auf dem Siebboden", gl["min"][2], g["max"][2], 0.01)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith("--")] or ["aussen_933", "aussen_993", "aussen_800", "innen_933"]))
