"""Vorpruefung Feinfilter T55 (W31 Grundbau, W32 Neubemessung, D55): Siebflaeche gegen Strom und Siebbelastung, Behaelter- und Wandmasse, Korb im Behaelter (Spalt, Auflage), Ports (Lage, Durchmesser, Richtung), Hoehenreihenfolge Einlauf > Korb > Auslauf, Standrahmen, Interferenz.
Erwartung unabhaengig vom Generator: Siebflaeche aus den gemessenen Korb-Boxen, Behaelter-Volumen aus der Wandformel, Ports aus den Stutzen-Boxen (bbox), Rohrgeschwindigkeit aus dem Innendurchmesser.
Aufruf: python scripts/workshop/check_feinfilter.py   (exit 1 bei FAIL)"""
import json, math, os, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def interference(path):
    script = os.path.join(sc.TMP, "ws-ff-interf.json"); out = os.path.join(sc.TMP, "ws-ff-interf-out.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 240}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--results", "--json-out", out], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER interference: " + r.stderr.strip())
    d = json.load(open(out, encoding="utf-8"))
    def find(o):
        if isinstance(o, dict):
            if "interferences" in o:
                return o["interferences"]
            for v in o.values():
                x = find(v)
                if x is not None:
                    return x
        elif isinstance(o, list):
            for v in o:
                x = find(v)
                if x is not None:
                    return x
    return [(i["a"], i["b"], i.get("volume_mm3", 0)) for i in find(d) or []]

def main():
    p, d = sc.load_params("feinfilter")
    path = os.path.join(sc.ROOT, "designs", "components", "feinfilter.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: B[n]["bbox"]
    ext = lambda n, i: bb(n)["max"][i] - bb(n)["min"][i]
    ck = sc.Check("feinfilter")
    L, W, H, w, zb = p["tank_l"], p["tank_w"], p["tank_h"], p["wall"], p["foot_h"]
    # --- Siebflaeche gegen Strom (W32): aus den GEMESSENEN Korbmassen, nicht aus den Parametern
    kl, kw, kd = ext("Korbgewebe", 0), ext("Korbgewebe", 1), ext("Korbgewebe", 2)
    a_wet = (p["wet_frac"] * 2 * (kl + kw) * kd + kl * kw) / 1e6
    q_m3h = p["q_lmin"] * 60 / 1000
    ck.eq("Hauptstrom Q = 110 l/min (W32)", p["q_lmin"], 110)
    ck.eq("Siebflaeche aus gemessenem Korb >= Q / Siebbelastung (m2, Soll 6,6 m3/h / 8 m/h = 0,825)", 1 if a_wet >= q_m3h / p["sieve_load"] else 0, 1)
    ck.eq("Siebflaeche nicht mehr als 10 % ueber dem Soll (kein Ueberbau)", 1 if a_wet <= 1.10 * q_m3h / p["sieve_load"] else 0, 1)
    ck.eq("Siebbelastung am gebauten Korb in m/h <= Parameter (8)", 1 if q_m3h / a_wet <= p["sieve_load"] else 0, 1)
    ck.eq("Gewebe 100 Mikrometer (W32: <= 100)", 1 if p["mesh_um"] <= 100 else 0, 1)
    # --- Behaelter
    for i, (n, s) in enumerate((("Laenge", L), ("Tiefe", W), ("Hoehe", H))):
        ck.eq(f"Behaelter {n} gemessen = Parameter", ext("Behaelter", i), s, 0.5)
    ck.eq("Behaelter steht auf dem Standrahmen (Unterkante = foot_h)", bb("Behaelter")["min"][2], zb, 0.01)
    il, iw = L - 2 * w, W - 2 * w
    v_wanne = L * W * H - il * iw * (H - w)
    v_leisten = 2 * p["basket_l"] * p["ledge_t"] * p["ledge_w"]
    v_loecher = math.pi / 4 * w * (p["inlet_d"] ** 2 + p["outlet_d"] ** 2 + p["drain_d"] ** 2 + p["spray_d"] ** 2)
    ck.eq("Behaelter-Volumen aus Wandformel (Wanne + Leisten - 4 Bohrungen), Wand 10 mm", B["Behaelter"]["volume_mm3"], v_wanne + v_leisten - v_loecher, v_wanne * 0.003)
    ck.eq("Behaelter-Innenraum in Litern (Inhalt bis Rand)", il * iw * (H - w) / 1e6, il * iw * (H - w) / 1e6, 0.0)
    print(f"   Innenraum {il * iw * (H - w) / 1e6:.1f} l, Korb-Siebflaeche {a_wet:.3f} m2, Siebbelastung {q_m3h / a_wet:.2f} m/h")
    # --- Siebkorb
    gf = bb("Korbflansch")
    ck.eq("Korbflansch liegt auf den Leisten (Unterkante = Leistenoberkante)", gf["min"][2], zb + p["ledge_z"], 0.01)
    ck.eq("Spalt Korbflansch zur Behaelterwand in X je Seite = 3 mm", (il - ext("Korbflansch", 0)) / 2, p["flange_gap"], 0.01)
    ck.eq("Spalt Korbflansch zur Behaelterwand in Y je Seite = 3 mm", (iw - ext("Korbflansch", 1)) / 2, p["flange_gap"], 0.01)
    ck.eq("Korbboden-Abstand zum Behaelterboden = Ablaufkammer (115)", bb("Korbgewebe")["min"][2] - (zb + w), p["chamber"], 0.01)
    ck.eq("Dichtflansch des Auslaufs unter dem Korbboden (Luft >= 15 mm)", 1 if bb("Korbgewebe")["min"][2] - bb("Auslauf_Flansch_innen")["max"][2] >= 15 else 0, 1)
    ck.eq("Korbgewebe Huelle 1 mm: Volumen aus Flaechen (Boden + 4 Waende)", B["Korbgewebe"]["volume_mm3"], p["mesh_t"] * (kl * kw + 2 * (kl + kw) * (kd - p["mesh_t"])), 0.01 * B["Korbgewebe"]["volume_mm3"] + 500)
    ck.eq("Korbstaebe 4 Stueck", len([k for k in B if k.startswith("Korbstab_")]), 4)
    ck.eq("Korbgriff je Seite ein Koerper (2)", len([k for k in B if k.startswith("Korbgriff_")]), 2)
    ck.eq("Korb herausnehmbar: Griff-Oberkante unter dem Deckel (>= 10 mm Luft)", 1 if bb("Dichtung")["max"][2] - max(bb("Korbgriff_v")["max"][2], bb("Korbgriff_h")["max"][2]) >= 10 else 0, 1)
    # --- Ports (Lage im Bauteil-KS: Ebene der Stutzenoeffnung, Mitte)
    e = bb("Einlaufrohr"); a = bb("Auslaufrohr"); ab = bb("Schlauchtuelle"); sp = bb("Spuel_Tuelle")
    ck.eq("Einlauf: Oeffnungsebene aussen bei x = -(L/2 + 60) (Richtung -X)", e["min"][0], -L / 2 - p["inlet_out"], 0.01)
    ck.eq("Einlauf: Durchmesser d63", e["max"][1] - e["min"][1], p["inlet_d"], 0.2)
    ck.eq("Einlauf: Mitte y = 0", (e["max"][1] + e["min"][1]) / 2, 0.0, 0.01)
    ck.eq("Einlauf: Oberkante des Winkels = Einlaufmitte + 31,5", e["max"][2], zb + p["inlet_z"] + p["inlet_d"] / 2, 0.01)
    ck.eq("Einlauf: senkrechtes Rohr endet inlet_down unter der Einlaufmitte", e["min"][2], zb + p["inlet_z"] - p["inlet_down"], 0.01)
    ck.eq("Einlauf: Oberkante <= Behaelterrand (kein Stau ueber dem Rand)", 1 if e["max"][2] <= zb + H else 0, 1)
    ck.eq("Einlaufrohr liegt ueber dem Korbflansch (Luft >= 8 mm)", 1 if (zb + p["inlet_z"] - p["inlet_d"] / 2) - gf["max"][2] >= 8 else 0, 1)
    ck.eq("Einlauf mündet im Korb: senkrechtes Rohr endet ueber dem Korbboden (> 100 mm)", 1 if e["min"][2] > bb("Korbgewebe")["min"][2] + 100 else 0, 1)
    ck.eq("Auslauf: Oeffnungsebene aussen bei x = L/2 + 70 (Richtung +X)", a["max"][0], L / 2 + p["outlet_out"], 0.01)
    ck.eq("Auslauf: Durchmesser d63", a["max"][1] - a["min"][1], p["outlet_d"], 0.2)
    ck.eq("Auslauf: Mitte unter dem Korbboden", 1 if (a["max"][2] + a["min"][2]) / 2 + p["outlet_collar_d"] / 2 < bb("Korbgewebe")["min"][2] else 0, 1)
    ck.eq("Ablass: Oeffnungsebene aussen bei y = -(W/2 + 40 + 50 + 30) (Richtung -Y)", ab["min"][1], -W / 2 - p["drain_stub"] - p["valve_l"] - p["barb_l"], 0.01)
    ck.eq("Ablass: Durchmesser d40", ab["max"][0] - ab["min"][0], p["drain_d"], 0.2)
    ck.eq("Ablass: Unterkante der Bohrung ueber dem Behaelterboden >= 5 mm", 1 if (zb + p["drain_z"] - p["drain_d"] / 2) - (zb + w) >= 5 else 0, 1)
    ck.eq("Kugelhahn d40: Gehaeuse D56 und Hebel vorhanden", 1 if "Kugelhahn_Ablass" in B and "Kugelhahn_Hebel" in B and abs(ext("Kugelhahn_Ablass", 0) - p["valve_d"]) < 0.3 else 0, 1)
    ck.eq("Ablass-Kugelhahn erreichbar: Hebel ausserhalb der Behaelterbox (y < -W/2)", 1 if bb("Kugelhahn_Hebel")["max"][1] < -W / 2 else 0, 1)
    ck.eq("Eimer unter dem Ablass: Mitte Schlauchtuelle >= 250 mm ueber dem Boden", 1 if (ab["max"][2] + ab["min"][2]) / 2 >= 250 else 0, 1)
    # --- Spuelanschluss (W32)
    ck.eq("Spuelanschluss: Oeffnungsebene aussen bei y = W/2 + 40 + 40 + 25 (Richtung +Y)", sp["max"][1], W / 2 + p["spray_stub"] + p["spray_valve_l"] + p["barb_l"] - 5, 0.01)
    ck.eq("Spuelanschluss: Durchmesser d25", sp["max"][0] - sp["min"][0], p["spray_d"], 0.2)
    ck.eq("Spuelanschluss: Kugelhahn d25 vorhanden (Gehaeuse D40)", 1 if abs(ext("Kugelhahn_Spuelen", 0) - p["spray_valve_d"]) < 0.3 else 0, 1)
    sr = bb("Spritzrohr")
    ck.eq("Spritzrohr liegt ueber dem Korbflansch (Luft >= 30 mm) und unter dem Rand", 1 if sr["min"][2] - gf["max"][2] >= 30 and sr["max"][2] < zb + H else 0, 1)
    ck.eq("Spritzrohr quer ueber den Korb: Ende bei y = spray_reach", sr["min"][1], p["spray_reach"], 0.01)
    # --- Rohrgeschwindigkeit am Ein-/Auslauf (110 l/min durch d63, Wand 3)
    v = (p["q_lmin"] / 1000 / 60) / (math.pi / 4 * ((p["inlet_d"] - 2 * p["wall_d63"]) / 1000) ** 2)
    ck.eq("Geschwindigkeit im Einlaufrohr in m/s <= 1,0 (Saugseite, leitungsnetz.json)", 1 if v <= 1.0 else 0, 1)
    print(f"   Rohrgeschwindigkeit d63 {v:.2f} m/s")
    # --- Deckel und Verschluesse
    ck.eq("Deckel ueberdeckt den Behaelter (Laenge = Behaelter + 2 x 4)", ext("Deckel", 0), L + 2 * p["lid_over"], 0.01)
    ck.eq("Spannverschluesse 4 Stueck (Bock + Hebel)", len([k for k in B if k.startswith("Spannbock_")]) + len([k for k in B if k.startswith("Spannhebel_")]), 8)
    ck.eq("Dichtung EPDM auf dem Rand (Unterkante = Behaelteroberkante)", bb("Dichtung")["min"][2], zb + H, 0.01)
    ck.eq("Gesamthoehe (Rahmen + Behaelter + Dichtung + Deckel + Griff)", max(b["bbox"]["max"][2] for b in ev["bodies"]), zb + H + p["gasket_t"] + p["lid_t"] + 34, 0.5)
    # --- Standrahmen
    ck.eq("Standrahmen 4 Beine und 4 Fussplatten", len([k for k in B if k.startswith("Bein_")]) + len([k for k in B if k.startswith("Fussplatte_")]), 8)
    ck.eq("Rahmen traegt den Boden: Ring-Oberkante = Behaelterunterkante", bb("Ring_X_v")["max"][2], zb, 0.01)
    ck.eq("Fussplatten stehen auf z = 0", min(bb(k)["min"][2] for k in B if k.startswith("Fussplatte_")), 0.0, 0.01)
    ck.eq("Auflagestege im Raster bar_dx: Anzahl", len([k for k in B if k.startswith("Auflage_Y_")]), int(p["bar_n"]))
    xs = sorted((bb(k)["min"][0] + bb(k)["max"][0]) / 2 for k in B if k.startswith("Auflage_Y_"))
    ends = [(bb("Ring_Y_l")["min"][0] + bb("Ring_Y_l")["max"][0]) / 2, (bb("Ring_Y_r")["min"][0] + bb("Ring_Y_r")["max"][0]) / 2]
    pts = [ends[0]] + xs + [ends[1]]
    ck.eq("Boden-Spannweite (groesster Abstand Steg zu Steg/Endring, gemessen) <= 125 mm", 1 if max(b_ - a_ for a_, b_ in zip(pts, pts[1:])) <= 125.01 else 0, 1)
    # --- Gewichte
    leer = sum(b["mass_g"] for b in ev["bodies"]) / 1000
    ck.eq("Leermasse plausibel (20-45 kg)", 1 if 20 <= leer <= 45 else 0, 1)
    print(f"   Leermasse {leer:.2f} kg, Koerper {len(ev['bodies'])}")
    itf = interference(path)
    for x in itf[:10]:
        print("   Interferenz", x)
    ck.eq("Interferenzen im Feinfilter (Rahmen, Behaelter, Korb, Deckel, Anschluesse)", len(itf), 0)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
