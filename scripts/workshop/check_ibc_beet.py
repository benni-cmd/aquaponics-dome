"""Vorpruefung IBC-Beet gegen die Scope-Card (docs/scope-cards.md) und R03: Aussenmass = layout.json, Wand, Medium EIN Koerper (Oberflaeche Z 400 absolut, Tiefe 300), Standrohr/Glocke-Masse, Ports.
M-BEET-TAUSCH-fix (D79): Abstand Siphon-Achse zu jedem Netztopf, alle vier Typen.
U3b (D132 bis D135): A21-Aufbau (Gitter, Vlies, Sieb, Glocke bis zum Boden, Seitenauslass, Belueftung unten, Nichts unter dem Flur, keine Interferenz).
Aufruf: python scripts/workshop/check_ibc_beet.py [typ ...] [--no-interf]   (exit 1 bei FAIL; Interferenz je Typ etwa 80 s)
Stand U3b: Sperrboden, Medienschutz, Plattenhuelse und Reduktion unter dem Boden entfallen (D133, D134)."""
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
    LAY = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
    lay = LAY["ibc_beds"]
    soll = {b["id"]: b for b in json.load(open(os.path.join(sc.ROOT, "data", "oasis-soll.json"), encoding="utf-8"))["bauteile"]}   # U3 (D122): Soll der Quelle, Wanne steht auf dem Flur
    z0_soll = LAY["oasis"]["ibc_beds_z0"]                    # 0 = Unterkante Wanne auf dem Flur (A+: layout.json ibc_beds z0 -162 bis -209)
    SOLL_ID = {"aussen_800": "fd_aussen", "innen_933": "fd_mitte"}          # Typen, die im Soll vorkommen (aussen_933/993 sind unbenutzte Altfassungen)
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
            ls = [b for b in lay if b["length"] == L and b["width"] == W]     # Hoehe ignoriert: layout.json traegt die A+-Hoehen (U3: Wanne 420 / 460)
        ck.eq(f"{typ} Anzahl laut layout.json" + (" (Aussenbeete, Mass erst nach M7)" if typ == "aussen_800" else ""), len(ls), T["anzahl"])
        w = B["Wanne"]["bbox"]
        ck.eq(f"{typ} Wanne Laenge", w["max"][0] - w["min"][0], L, 0.5)
        ck.eq(f"{typ} Wanne Breite", w["max"][1] - w["min"][1], W, 0.5)
        ck.eq(f"{typ} Wanne Hoehe", w["max"][2] - w["min"][2], H, 0.5)
        # Medium: genau EIN Koerper, Oberflaeche und Tiefe
        med = [k for k in B if k.startswith("Medium")]
        ck.eq(f"{typ} Medium Koerperzahl", len(med), 1)
        m = B["Medium"]["bbox"]
        ck.eq(f"{typ} Medium Oberflaeche lokal = Beetboden {p['a21_boden']} + Medientiefe {p['media_depth']} (U3, D122)", m["max"][2], p["a21_boden"] + p["media_depth"], 0.5)
        ck.eq(f"{typ} Medium Unterkante = Soll-Beetboden {p['a21_boden']} (data/oasis-soll.json boden_ueber_fussboden_mm)", m["min"][2], p["a21_boden"], 0.5)
        ck.eq(f"{typ} Medium Tiefe", m["max"][2] - m["min"][2], p["media_depth"], 0.5)
        if T.get("fase"):                                          # W26/D44: Zulauf-Tropfrohr liegt vor der Eckenfase (gerade Stirnwand), sonst durchstoesst das Rohr die schraege Wand ohne Bohrung
            c_a = T["fase"] - ((W - (W - 2 * p["rim_w"])) / 2.0) * (2 - 2 ** 0.5)
            tr = B["Tropfrohr"]["bbox"]
            y_edge = (W - 2 * p["rim_w"]) / 2.0 - c_a                                  # Beginn der Fase an der Stirnwand (|y|)
            ck.eq(f"{typ} Zulauf-Tropfrohr: |y| {max(abs(tr['min'][1]), abs(tr['max'][1])):.0f} liegt vor dem Fasenbeginn {y_edge:.0f} (Rohr trifft die gerade Stirnwand)", 1 if max(abs(tr["min"][1]), abs(tr["max"][1])) <= y_edge - 10 else 0, 1)
        z0_abs = z0_soll                                           # U3: Wanne auf dem Flur (A+ -162 bis -209 siehe docs/decisions.md D122)
        if typ in SOLL_ID:                                         # Soll der Quelle (fd_aussen / fd_mitte): Beetboden 70, Rand 460 / 420, Flutstand 250 ueber dem Flur
            S = soll[SOLL_ID[typ]]["hoehen"]
            ck.eq(f"{typ} Wannen-Oberkante absolut = Soll-Rand {S['rand_ueber_fussboden_mm']} (data/oasis-soll.json {SOLL_ID[typ]})", w["max"][2] + z0_abs, S["rand_ueber_fussboden_mm"], 0.5)
            ck.eq(f"{typ} Beetboden absolut = Soll {S['boden_ueber_fussboden_mm']}", m["min"][2] + z0_abs, S["boden_ueber_fussboden_mm"], 0.5)
            ck.eq(f"{typ} Flutstand (Standrohr-Oberkante) absolut = Soll {S['wsp_ueber_fussboden_mm']}", B["Standrohr"]["bbox"]["max"][2] + z0_abs, S["wsp_ueber_fussboden_mm"], 0.5)
            ck.eq(f"{typ} Medium liegt ueber dem Flutstand nicht unter ihm (Oberflaeche {m['max'][2] + z0_abs:.0f} >= Flutstand {S['wsp_ueber_fussboden_mm']})", 1 if m["max"][2] + z0_abs >= S["wsp_ueber_fussboden_mm"] else 0, 1)
        # --- U3b: A21-Aufbau (D132 bis D135). Alle Soll-Zahlen unabhaengig aus den Parametern gerechnet, nicht aus dem Generator.
        PI = math.pi
        Wi_, Li_ = W - 2 * p["rim_w"] - 2 * p["wall"], L - 2 * p["rim_w"] - 2 * p["wall"]
        wm_, lm_ = Wi_ - 2 * p["media_gap"], Li_ - 2 * p["media_gap"]
        hole_d = p["bell_d"] + 4
        if T.get("fase"):
            cm_ = T["fase"] - (W - wm_) / 2.0 * (2 - 2 ** 0.5)
            a_kontur = lm_ * wm_ - 2 * cm_ * cm_
        else:
            a_kontur = lm_ * wm_ - (4 - PI) * (p["corner_r"] - p["media_gap"]) ** 2
        ck.eq(f"{typ} Medium-Volumen (Liter) gegen Flaechenrechnung (Loecher Glocke d{hole_d} und Schacht d{p['shaft_d']})", B["Medium"]["volume_mm3"] / 1e6, (a_kontur - PI / 4 * hole_d ** 2 - PI / 4 * p["shaft_d"] ** 2) * p["media_depth"] / 1e6, 0.5)
        # Stapel von unten: Gitter, Vlies, Sieb, Medium (Sieb ueber dem Vlies, D132)
        gi, vl, sb = B["Abtropfgitter"]["bbox"], B["Vlies"]["bbox"], B["Sieb"]["bbox"]
        z_g0 = p["a21_boden"] - p["a21_sieb_t"] - p["a21_vlies_t"] - p["a21_gitter_h"]
        ck.eq(f"{typ} Abtropfgitter Hoehe = a21_gitter_h", gi["max"][2] - gi["min"][2], p["a21_gitter_h"], 0.01)
        ck.eq(f"{typ} Abtropfgitter Unterkante {z_g0:.0f} = Beetboden {p['a21_boden']} - Sieb - Vlies - Gitterhoehe", gi["min"][2], z_g0, 0.01)
        ck.eq(f"{typ} Vlies liegt auf dem Gitter (Unterkante = Gitter-Oberkante)", vl["min"][2], gi["max"][2], 0.01)
        ck.eq(f"{typ} Vlies Dicke = a21_vlies_t", vl["max"][2] - vl["min"][2], p["a21_vlies_t"], 0.01)
        ck.eq(f"{typ} Sieb liegt auf dem Vlies (Unterkante = Vlies-Oberkante)", sb["min"][2], vl["max"][2], 0.01)
        ck.eq(f"{typ} Sieb Dicke = a21_sieb_t", sb["max"][2] - sb["min"][2], p["a21_sieb_t"], 0.01)
        ck.eq(f"{typ} Medium liegt auf dem Sieb (Unterkante = Sieb-Oberkante)", m["min"][2], sb["max"][2], 0.01)
        g_in = p["a21_gitter_rand"] - p["media_gap"]
        a_gi = (lm_ - 2 * g_in) * (wm_ - 2 * g_in)
        offen = 1 - B["Abtropfgitter"]["volume_mm3"] / (a_gi * p["a21_gitter_h"])
        ck.eq(f"{typ} Abtropfgitter freie Flaeche {offen * 100:.0f} % (real Maschen 20 x 20 = 64 %), mindestens 60 %", 1 if offen >= 0.60 else 0, 1)
        ck.eq(f"{typ} Gitter zur Innenwand: Abstand {p['a21_gitter_rand']} mm (Platz fuer den Flansch)", (w["max"][0] - w["min"][0]) / 2 - p["rim_w"] - p["wall"] - gi["max"][0], p["a21_gitter_rand"], 0.6)
        # Stuetzen tragen das Gitter: Oberkante = Gitter-Unterkante; Zahl hoechstens 3 x nx, davon fehlen die im Weg von Siphon und Auslass
        stz = [k for k in B if k == "Stuetze" or re.fullmatch(r"Stuetze \(\d+\)", k)]
        nx_ = int(p["post_nx"]) if L > 2500 else 5
        ck.eq(f"{typ} Stuetzen: Zahl {len(stz)} liegt zwischen 3 x {nx_} - 4 und 3 x {nx_}", 1 if 3 * nx_ - 4 <= len(stz) <= 3 * nx_ else 0, 1)
        ck.eq(f"{typ} Stuetzen Oberkante = Gitter-Unterkante", max(B[k]["bbox"]["max"][2] for k in stz), gi["min"][2], 0.01)
        ck.eq(f"{typ} Stuetzen stehen auf dem Wannenboden (Unterkante {p['floor_t']})", min(B[k]["bbox"]["min"][2] for k in stz), p["floor_t"], 0.01)
        # Reinigungsschacht d110, stehend auf dem Sieb, Oberkante 20 ueber Medium
        rs = B["Reinigungsschacht"]["bbox"]
        ck.eq(f"{typ} Reinigungsschacht D", rs["max"][0] - rs["min"][0], p["shaft_d"], 0.1)
        ck.eq(f"{typ} Reinigungsschacht steht auf dem Sieb", rs["min"][2], sb["max"][2], 0.01)
        ck.eq(f"{typ} Reinigungsschacht Oberkante ueber Medienoberflaeche", rs["max"][2] - m["max"][2], p["shaft_over"], 0.5)
        # M-BEET-TAUSCH 0c: Schacht und Siphon auf einer Zellmitte des Netztopf-Rasters; Soll hier unabhaengig aus params.json (pot_pitch, pot_margin) gerechnet, nicht aus dem Generator
        prm = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8")); pitch, mar = prm["pot_pitch"]["value"], prm["pot_margin"]["value"]
        nu_, nv_ = int((L - 2 * mar) // pitch) + 1, int((W - 2 * mar) // pitch) + 1
        grid = [((i - (nu_ - 1) / 2) * pitch, (j - (nv_ - 1) / 2) * pitch) for i in range(nu_) for j in range(nv_)]
        sx_, sy_ = (rs["min"][0] + rs["max"][0]) / 2, (rs["min"][1] + rs["max"][1]) / 2
        dmin = min(math.hypot(sx_ - u, sy_ - v) for u, v in grid)
        ck.eq(f"{typ} Reinigungsschacht in der Naehe der alten Lage -Li/2 + 250 (hoechstens ein Rasterschritt {pitch})", 1 if abs(sx_ - (-Li_ / 2 + 250)) <= pitch else 0, 1)
        ck.eq(f"{typ} Abstand Schachtachse zu jedem Netztopf des Rasters {dmin:.1f} mm >= 87 (Schachtradius 55 + Kragenradius 32; Raster {nu_} x {nv_}, {len(grid)} Toepfe)", 1 if dmin >= 87 else 0, 1)
        gl = B["Glocke"]["bbox"]
        px_, py_ = (gl["min"][0] + gl["max"][0]) / 2, (gl["min"][1] + gl["max"][1]) / 2
        dmin_g = min(math.hypot(px_ - u, py_ - v) for u, v in grid)
        ck.eq(f"{typ} Abstand Siphon-Achse zu jedem Netztopf des Rasters {dmin_g:.1f} mm >= {hole_d / 2 + 32:.1f} (Loch d{hole_d} im Medium + Kragenradius 32; Achse x {px_:.1f}, y {py_:.1f})", 1 if dmin_g >= hole_d / 2 + 32 else 0, 1)
        ck.eq(f"{typ} Siphon-Achse in der Naehe der alten Lage Li/2 - 200 (hoechstens ein Rasterschritt {pitch})", 1 if abs(px_ - (Li_ / 2 - 200)) <= pitch else 0, 1)
        s_ = B["Standrohr"]["bbox"]
        sx2_, sy2_ = (s_["min"][0] + s_["max"][0]) / 2, (s_["min"][1] + s_["max"][1]) / 2
        ck.eq(f"{typ} Standrohr in der Achse der Glocke (Versatz {math.hypot(sx2_ - px_, sy2_ - py_):.2f} mm)", math.hypot(sx2_ - px_, sy2_ - py_), 0, 0.1)
        ck.eq(f"{typ} Schachtkappe sitzt auf dem Schacht", B["Schachtkappe"]["bbox"]["min"][2], rs["max"][2], 0.01)
        # --- Siphon bis ganz nach unten (D133): Glocke steht auf dem Wannenboden, Kerben und Luftloch liegen unter dem Gitter
        z_b0 = p["floor_t"] + p["a21_standrohr_unten"]
        ck.eq(f"{typ} Glocke steht auf dem Wannenboden (Unterkante {z_b0:g} = Boden + a21_standrohr_unten)", gl["min"][2], z_b0, 0.01)
        ck.eq(f"{typ} Glocke geht durch das Gitter (Unterkante {gl['min'][2]:.0f} unter Gitter-Unterkante {gi['min'][2]:.0f}, Oberkante {gl['max'][2]:.0f} ueber dem Sieb {sb['max'][2]:.0f})", 1 if gl["min"][2] < gi["min"][2] and gl["max"][2] > sb["max"][2] else 0, 1)
        ck.eq(f"{typ} Glocke D", gl["max"][0] - gl["min"][0], p["bell_d"], 0.1)
        ck.eq(f"{typ} Glocke Hoehe", gl["max"][2] - gl["min"][2], p["bell_h"], 0.1)
        ck.eq(f"{typ} Kerben-Oberkante {z_b0 + p['bell_slot_z'] + p['bell_slot_h']:g} liegt unter der Gitter-Unterkante {gi['min'][2]:g}", 1 if z_b0 + p["bell_slot_z"] + p["bell_slot_h"] < gi["min"][2] else 0, 1)
        ck.eq(f"{typ} Luftloch-Oberkante {p['a21_luftloch_z'] + p['air_hole'] / 2:g} liegt unter der Gitter-Unterkante {gi['min'][2]:g}", 1 if p["a21_luftloch_z"] + p["air_hole"] / 2 < gi["min"][2] else 0, 1)
        a_sp_ = PI / 4 * (p["standpipe_d"] - 2 * p["standpipe_wall"]) ** 2
        ck.eq(f"{typ} Kerbenflaeche 3 x {p['bell_slot_w']} x {p['bell_slot_h']} = {3 * p['bell_slot_w'] * p['bell_slot_h']} mm2 >= Standrohrflaeche {a_sp_:.0f}", 1 if 3 * p["bell_slot_w"] * p["bell_slot_h"] >= a_sp_ else 0, 1)
        v_gl0 = PI / 4 * (p["bell_d"] ** 2 - (p["bell_d"] - 2 * p["bell_wall"]) ** 2) * p["bell_h"] + PI / 4 * (p["bell_d"] - 2 * p["bell_wall"]) ** 2 * p["bell_wall"]
        v_cut = 3 * p["bell_slot_w"] * p["bell_slot_h"] * p["bell_wall"] + p["air_hole"] ** 2 * p["bell_wall"] + PI / 4 * (p["standpipe_d"] + 2) ** 2 * p["bell_wall"]
        r_gl = (v_gl0 - B["Glocke"]["volume_mm3"]) / v_cut
        ck.eq(f"{typ} Glocke Volumen: 3 Kerben + Luftloch + Auslassloch d{p['standpipe_d'] + 2} herausgeschnitten ({r_gl:.2f} x erwartet)", 1 if 0.85 <= r_gl <= 1.15 else 0, 1)
        # Standrohr, Flutstand (Standrohr-Oberkante) und Luft unter der Glockendecke
        ck.eq(f"{typ} Standrohr Hoehe ueber Medienunterkante", s_["max"][2] - m["min"][2], p["standpipe_over"], 0.5)
        ck.eq(f"{typ} Standrohr D", s_["max"][0] - s_["min"][0], p["standpipe_d"], 0.1)
        ck.eq(f"{typ} Standrohr unter Glockendecke (Luft >= 20)", 1 if gl["max"][2] - s_["max"][2] >= 20 else 0, 1)
        # --- Seitlicher Auslass (D134): Winkel unter der Glocke, Rohr d25 durch die +X-Stirnwand, Tankverbinder, Schlauchtuelle ID25
        wi_, ar, bh, tl, rh_ = B["Auslasswinkel"]["bbox"], B["Auslassrohr"]["bbox"], B["Bulkhead"]["bbox"], B["Schlauchtuelle"]["bbox"], B["Reduzierhuelse_Auslass"]["bbox"]
        ck.eq(f"{typ} Auslassachse: Rohr-Mitte z = a21_auslass_z", (ar["min"][2] + ar["max"][2]) / 2, p["a21_auslass_z"], 0.01)
        ck.eq(f"{typ} Auslassrohr D", ar["max"][2] - ar["min"][2], p["standpipe_d"], 0.1)
        ck.eq(f"{typ} Auslassrohr bleibt unter dem Gitter (Rohr-Oberkante {ar['max'][2]:.1f} <= Gitter-Unterkante {gi['min'][2]:.0f} - 1)", 1 if ar["max"][2] <= gi["min"][2] - 1 else 0, 1)
        ck.eq(f"{typ} Auslasswinkel sitzt unter der Glocke (Winkelachse x {wi_['min'][0] + p['a21_winkel_d'] / 2:.1f} = Glockenachse {px_:.1f})", wi_["min"][0] + p["a21_winkel_d"] / 2, px_, 0.1)
        ck.eq(f"{typ} Auslasswinkel liegt innerhalb der Glocke (Ende {wi_['max'][0] - px_:.1f} mm von der Achse < Glocken-Innenradius {p['bell_d'] / 2 - p['bell_wall']:.1f})", 1 if wi_["max"][0] - px_ < p["bell_d"] / 2 - p["bell_wall"] else 0, 1)
        ck.eq(f"{typ} Standrohr steckt im Winkel (Standrohr-Unterkante {s_['min'][2]:.0f} ueber der Rohrachse {p['a21_auslass_z']})", 1 if s_["min"][2] > p["a21_auslass_z"] else 0, 1)
        ck.eq(f"{typ} Auslass seitlich: Tankverbinder durch die +X-Stirnwand (Flansch innen bei x {bh['min'][0]:.1f} = Innenwand {Li_ / 2:.1f} - 4)", bh["min"][0], Li_ / 2 - 4, 0.1)
        ck.eq(f"{typ} Tankverbinder-Flansch D", bh["max"][2] - bh["min"][2], p["bulkhead_flange"], 0.1)
        ck.eq(f"{typ} Tankverbinder-Flansch ueber dem Wannenboden (Unterkante {bh['min'][2]:.1f} > {p['floor_t']})", 1 if bh["min"][2] > p["floor_t"] else 0, 1)
        ck.eq(f"{typ} Reduzierhuelse Aussen-D = Tankverbinder-Innen d{p['bulkhead_id']}", rh_["max"][1] - rh_["min"][1], p["bulkhead_id"], 0.1)
        ck.eq(f"{typ} Schlauchtuelle: Widerhaken-D 28 fuer Schlauch ID25 (Nennweite aus D106, Quelle nennt keine)", tl["max"][1] - tl["min"][1], 28, 0.1)
        ck.eq(f"{typ} Schlauchtuelle liegt auf der Auslassachse (z {(tl['min'][2] + tl['max'][2]) / 2:.2f})", (tl["min"][2] + tl["max"][2]) / 2, p["a21_auslass_z"], 0.01)
        ck.eq(f"{typ} Schlauchtuelle beginnt am Ende des Tankverbinders (x {tl['min'][0]:.1f})", tl["min"][0], bh["max"][0], 0.01)
        ck.eq(f"{typ} Schlauchtuelle Laenge", tl["max"][0] - tl["min"][0], p["a21_tuelle_l"], 0.1)
        ueber = tl["max"][0] - L / 2
        ck.eq(f"{typ} Auslass ragt {ueber:.0f} mm ueber den Randwulst (hoechstens 40; Beetabstand 60, W17)", 1 if ueber <= 40 else 0, 1)
        ck.eq(f"{typ} Auslass-Anschluss nahe der Mitte der Stirnwand (|y| {abs((tl['min'][1] + tl['max'][1]) / 2):.0f} <= 80, gerade Wandstrecke)", 1 if abs((tl["min"][1] + tl["max"][1]) / 2) <= 80 else 0, 1)
        zmin = min(x["bbox"]["min"][2] for x in ev["bodies"])
        ck.eq(f"{typ} Nichts unter der Wannenunterkante (kleinstes z aller Koerper {zmin:.1f}; Bedenken B9: kein Teil im Fussboden)", 1 if zmin >= -0.001 else 0, 1)
        # --- Belueftung unten (D135)
        ab, ls_ = B["Ausstroemer"]["bbox"], B["Luftschlauch"]["bbox"]
        ck.eq(f"{typ} Ausstroemer D", ab["max"][2] - ab["min"][2], p["a21_ausstroemer_d"], 0.1)
        ck.eq(f"{typ} Ausstroemer Laenge", ab["max"][0] - ab["min"][0], p["a21_ausstroemer_l"], 0.1)
        ck.eq(f"{typ} Ausstroemer liegt unten (Unterkante {ab['min'][2]:.1f} >= Boden {p['floor_t']}, Oberkante {ab['max'][2]:.1f} < Gitter-Unterkante {gi['min'][2]:.0f})", 1 if ab["min"][2] >= p["floor_t"] and ab["max"][2] < gi["min"][2] else 0, 1)
        ck.eq(f"{typ} Luftschlauch D = a21_belueftung_d", ls_["max"][2] - ls_["min"][2], p["a21_belueftung_d"], 0.1)
        ck.eq(f"{typ} Luftschlauch kommt durch die -X-Stirnwand (Ende x {ls_['min'][0]:.0f} ausserhalb der Wand bei {w['min'][0] + p['rim_w']:.0f})", 1 if ls_["min"][0] < w["min"][0] + p["rim_w"] - 20 else 0, 1)
        ck.eq(f"{typ} Luftschlauch endet am Ausstroemer (x {ls_['max'][0]:.1f})", ls_["max"][0], ab["min"][0], 0.01)
        # --- Zulauf durch die Stirnwand
        t = B["Tropfrohr"]["bbox"]
        ck.eq(f"{typ} Zulaufport ausserhalb der Wanne (x < -L/2)", 1 if t["min"][0] < w["min"][0] + 10 else 0, 1)
        ck.eq(f"{typ} Zulaufhoehe lokal", (t["min"][2] + t["max"][2]) / 2, H - p["inflow_below_rim"], 0.5)
        if typ in SOLL_ID:
            ck.eq(f"{typ} Zulauf absolut = Soll-Rand minus {p['inflow_below_rim']} (z0 {z0_abs})", (t["min"][2] + t["max"][2]) / 2 + z0_abs, soll[SOLL_ID[typ]]["hoehen"]["rand_ueber_fussboden_mm"] - p["inflow_below_rim"], 0.5)
        ck.eq(f"{typ} alle Koerper benannt (keine Body<n>)", 1 if not [k for k in B if re.match(r"Body[0-9]+", k)] else 0, 1)
        if "--no-interf" not in sys.argv:
            ck.eq(f"{typ} Interferenzen (inspect.interference)", n_interf(path), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main([a for a in sys.argv[1:] if not a.startswith("--")] or ["aussen_933", "aussen_993", "aussen_800", "innen_933"]))
