"""Pruefung Kleiner Puffer T82 (W34, R37 Option A): Anzahl der Teile, Grundflaeche und Hoehe, Fass (Mass, Masse, Fuellmarke 120 l, Spiel), Messzelle (Innenvolumen 20 l, Verweilzeit, Stutzen), Kanister 20 l,
Pumpen, Auffangrand, Ports (Lage und Richtung gegen die Spitzen der gebauten Koerper), Interferenz 0.
Erwartungen aus den Parametern (puffer_klein.json) und den Quellen (R37), die Port-Lagen aus dem Blatt-Eintrag `blatt.ports`, nicht aus dem Generator.
Aufruf: python scripts/workshop/check_puffer_klein.py   (exit 1 bei FAIL)"""
import json, math, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def interference(path):
    script = os.path.join(sc.TMP, "ws-pk-interf.json")
    out = os.path.join(sc.TMP, "ws-pk-interf-out.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {"budget_s": 200}}]}, open(script, "w"))
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
    return find(d) or []

def xyz(s):
    return {k: float(v) for k, v in re.findall(r"([xyz]) (-?\d+)", s)}

def main():
    p, d = sc.load_params("puffer_klein")
    path = os.path.join(sc.ROOT, "designs", "components", "puffer_klein.sc")
    ev = sc.evaluate(path)
    B = {b["name"]: b for b in ev["bodies"]}
    bb = lambda n: B[n]["bbox"]
    ck = sc.Check("puffer_klein")
    ext = lambda n, i: (bb(n)["min"][i], bb(n)["max"][i])
    # --- Teile
    cnt = lambda pre: len([k for k in B if k.startswith(pre)])
    ck.eq("Pfosten", cnt("Pfosten_"), 4)
    ck.eq("Fussplatten", cnt("Fussplatte_"), 4)
    ck.eq("Riegel (5 oben, 3 unten)", cnt("Riegel_"), 8)
    ck.eq("Auffangrand-Teile", cnt("Auffangrand_"), 4)
    ck.eq("Koerper gesamt (Stand 21 + Fass 3 + Zelle 3 + Kanister 2 + Pumpen 2 + Kabel 1)", len(B), 32)
    mn, mx = sc.bbox_all(ev)
    ck.eq("Grundflaeche X <= 700 (Auftrag: max 0,7 x 0,7 m)", 1 if mx[0] - mn[0] <= p["stand_w"] + 0.1 else 0, 1)
    ck.eq("Grundflaeche Y <= 700", 1 if mx[1] - mn[1] <= p["stand_w"] + 0.1 else 0, 1)
    ck.eq(f"Hoehe gesamt {mx[2]:.0f} < 1300 (Auftrag)", 1 if mx[2] < p["hoehe_max"] and mn[2] >= -0.1 else 0, 1)
    # --- Fass
    fx = ext("Fass", 0)
    ck.eq("Fass Durchmesser (bbox x) = 500", fx[1] - fx[0], p["fass_d"], 0.2)
    ck.eq("Fass Hoehe mit Deckel = 800 (Deckelplatte ohne Einfuellstutzen)", ext("Fass_Deckel", 2)[1] - p["einf_h"] - ext("Fass", 2)[0], p["fass_h"], 0.2)
    ck.eq("Fass steht auf dem Boden (z 0)", ext("Fass", 2)[0], 0, 0.1)
    fm = sum(B[k]["mass_g"] for k in ("Fass", "Fass_Deckel", "Fass_Entnahmestutzen")) / 1000
    ck.eq(f"Fass-Masse {fm:.1f} kg (R37: ca. 6 kg)", fm, 6.0, 1.5)
    r_o = p["fass_d"] / 2
    cav = (math.pi * r_o ** 2 * (p["fass_h"] - p["fass_lid_t"]) - B["Fass"]["volume_mm3"]) / 1e6          # Hohlraum bis zum Deckel (Loch fuer den Stutzen vernachlaessigt)
    ck.eq(f"Fass Hohlraum {cav:.0f} l >= 120 (Nennvolumen)", 1 if cav >= p["fass_nenn_l"] else 0, 1)
    r_i = r_o - p["fass_wall"]
    zmark = p["fass_floor"] + p["fass_nenn_l"] * 1e6 / (math.pi * r_i ** 2)
    ck.eq(f"Fuellmarke 120 l bei Z {zmark:.0f} liegt unter dem Deckel ({p['fass_h'] - p['fass_lid_t']}) (Rechnung aus Innenradius)", 1 if zmark < p["fass_h"] - p["fass_lid_t"] else 0, 1)
    # Spiel zu den Pfosten, Deckelluft unter dem Regalboden
    ck.eq("Fass-Spiel zum Pfosten (Fass Aussenkante 250, Pfosten Innenkante) >= 40", min(ext("Pfosten_pp", 0)[0] - fx[1], -(ext("Pfosten_mp", 0)[1]) - (-fx[0])), 45, 0.2)
    top_f = ext("Fass_Deckel", 2)[1]
    ck.eq(f"Luft Fass-Einfuellstutzen {top_f:.0f} bis Regalboden-Unterkante {ext('Regalboden', 2)[0]:.0f} >= 50", 1 if ext("Regalboden", 2)[0] - top_f >= 50 else 0, 1)
    # --- Messzelle
    ox, oy = ext("Messzelle_Deckel", 0), ext("Messzelle_Deckel", 1)
    oh = ext("Messzelle", 2)[1] - ext("Messzelle", 2)[0]
    inner = ((ox[1] - ox[0]) * (oy[1] - oy[0]) * oh - B["Messzelle"]["volume_mm3"]) / 1e6
    ck.eq(f"Messzelle Innenvolumen {inner:.1f} l = 20 (R37 Befund 1; aus Aussenmass minus Volumen)", inner, 20.0, 0.3)
    ck.eq("Messzelle Wand 5 mm (Aussen 290 - Innen 280)", ((ox[1] - ox[0]) - p["zelle_ix"]) / 2, p["zelle_wall"], 0.1)
    z_abl_u = p["regal_z"] + p["zelle_wall"] + p["zelle_ablauf_z"] - p["stu_od"] / 2
    v_stand = p["zelle_ix"] * p["zelle_iy"] * (z_abl_u - p["regal_z"] - p["zelle_wall"]) / 1e6
    ck.eq(f"Verweilzeit im Messkreis 3 l/min bis Ablauf-Unterkante {v_stand:.1f} l = {v_stand / 3:.1f} min >= 5,5 (R37: 6,7 min bei voller Zelle)", 1 if v_stand / 3 >= 5.5 else 0, 1)
    ck.eq("Ablaufstutzen unter dem Zelldeckel (Oberkante < Innenhoehe)", 1 if p["zelle_ablauf_z"] + p["stu_od"] / 2 < p["zelle_ih"] else 0, 1)
    ck.eq("Sondenstutzen im Deckel: 4 Stueck d25", len({(round(f["cylinder"]["origin"][0], 1), round(f["cylinder"]["origin"][1], 1)) for f in sc.faces_multi(path, ["Messzelle_Deckel"])["Messzelle_Deckel"] if f.get("cylinder") and abs(f["cylinder"]["radius"] - p["halter_od"] / 2) < 0.1 and abs(abs(f["cylinder"]["axis"][2]) - 1) < 0.02}), 4)
    ck.eq("Blende liegt an der Vorderseite der Zelle (y-Abstand 0)", abs(ext("Blende", 1)[1] - ext("Messzelle_Deckel", 1)[0]), 0, 0.1)
    # --- Kanister
    kb = bb("Kanister")
    kv = ((kb["max"][0] - kb["min"][0]) * (kb["max"][1] - kb["min"][1]) * (kb["max"][2] - kb["min"][2]) - B["Kanister"]["volume_mm3"]) / 1e6
    ck.eq(f"Kanister Innenvolumen {kv:.1f} l = 20 (R37: Eisenchelat-Kanister 20 l)", kv, 20.0, 0.3)
    km = (B["Kanister"]["mass_g"] + B["Kanister_Schraubdeckel"]["mass_g"]) / 1000
    ck.eq(f"Kanister leer {km:.2f} kg (HDPE, Wand 3 mm: 1-1,5 kg)", 1 if 0.8 <= km <= 1.8 else 0, 1)
    # --- Regalboden und Auffangrand
    ck.eq("Regalboden liegt auf den oberen Riegeln (Unterkante = Riegel-Oberkante)", abs(ext("Regalboden", 2)[0] - ext("Riegel_oben_quer", 2)[1]), 0, 0.1)
    ck.eq("Regalboden Oberkante z 898", ext("Regalboden", 2)[1], p["regal_z"], 0.1)
    rim_in = min(ext("Auffangrand_r", 0)[0], -ext("Auffangrand_l", 0)[1], ext("Auffangrand_h", 1)[0], -ext("Auffangrand_v", 1)[1])
    inside = all(abs(v) <= rim_in + 0.1 for n in ("Messzelle", "Messzelle_Deckel", "Kanister", "Pumpe_Base", "Pumpe_Eisen") for v in (*ext(n, 0), *ext(n, 1)))
    ck.eq(f"Zelle, Kanister, Pumpen (inkl. Stutzen) liegen innerhalb des Auffangrands (innen {rim_in:.0f})", 1 if inside else 0, 1)
    # --- Ports gegen die gebauten Koerper (Spitze in Richtung, Mitte quer)
    ports = {x[0]: (xyz(x[2]), x[3]) for x in d["blatt"]["ports"]}
    def pt(prefix):
        k = [n for n in ports if n.startswith(prefix)]
        assert len(k) >= 1, prefix
        return ports[k[0]]
    P, dr = pt("Messkreis Zulauf")
    ck.eq("Port Messkreis Zulauf: Spitze x", ext("Messzelle", 0)[0], P["x"], 0.2)
    ck.eq("Port Messkreis Zulauf: Richtung -X", 0 if dr == "-X" else 1, 0)
    ck.eq("Port Messkreis Zulauf: y-Mitte der Zelle", sum(ext("Messzelle_Deckel", 1)) / 2, P["y"], 0.2)
    P, dr = pt("Ablauf Messzelle")
    ck.eq("Port Ablauf Messzelle: Spitze y (+Y)", ext("Messzelle", 1)[1], P["y"], 0.2)
    P, dr = pt("Entnahme")
    ck.eq("Port Entnahme: Spitze x (+X)", ext("Fass_Entnahmestutzen", 0)[1], P["x"], 0.2)
    ck.eq("Port Entnahme: z-Mitte", sum(ext("Fass_Entnahmestutzen", 2)) / 2, P["z"], 0.2)
    P, dr = pt("Frischwasser")
    ck.eq("Port Frischwasser: Spitze z (+Z)", ext("Fass_Deckel", 2)[1], P["z"], 0.2)
    for k in range(1, 5):
        P, dr = pt(f"Sondenstutzen {k}")
        ck.eq(f"Port Sondenstutzen {k}: Spitze z", ext("Messzelle_Deckel", 2)[1], P["z"], 0.2)
    hx = sorted((round(f["cylinder"]["origin"][0], 1), round(f["cylinder"]["origin"][1], 1)) for f in sc.faces_multi(path, ["Messzelle_Deckel"])["Messzelle_Deckel"] if f.get("cylinder") and abs(f["cylinder"]["radius"] - p["halter_od"] / 2) < 0.1)
    pp = sorted((P["x"], P["y"]) for P in (pt(f"Sondenstutzen {k}")[0] for k in range(1, 5)))
    ck.eq("Sondenstutzen x/y gegen Blatt (max. Abweichung mm)", max(abs(a[0] - b[0]) + abs(a[1] - b[1]) for a, b in zip(sorted(set(hx)), pp)) if len(set(hx)) == 4 else 99, 0, 1.0)
    for nm, body in (("Base", "Pumpe_Base"), ("Eisen", "Pumpe_Eisen")):
        P, dr = pt(f"Saug {nm}")
        ck.eq(f"Port Saug {nm}: Spitze y (+Y)", ext(body, 1)[1], P["y"], 0.2)
        ck.eq(f"Port Saug {nm}: x-Mitte", sum(ext(body, 0)) / 2, P["x"], 0.2)
        P, dr = pt(f"Dosierleitung {nm}")
        ck.eq(f"Port Dosierleitung {nm}: Spitze y (-Y)", ext(body, 1)[0], P["y"], 0.2)
        ck.eq(f"Port Dosierleitung {nm}: z-Mitte", sum(ext(body, 2)) / 2, P["z"], 0.2)
    P, dr = pt("Kabel")
    ck.eq("Port Kabel: Spitze y (+Y)", ext("Kabelverschraubung", 1)[1], P["y"], 0.2)
    ck.eq("Kabelverschraubung sitzt am hinteren oberen Riegel (Anlage y)", abs(ext("Kabelverschraubung", 1)[0] - ext("Riegel_oben_x2", 1)[1]), 0, 0.1)
    ck.eq("Ports im Blatt: 2 + 4 + 2 + 4 + 1", len(ports), 13)
    # --- Interferenz
    inter = [i for i in interference(path) if i.get("volume_mm3", 0) > 1.0]
    ck.eq("Interferenzen (Volumen > 1 mm3)", len(inter), 0)
    for i in inter[:8]:
        print("   Interferenz", i["a"], i["b"], round(i.get("volume_mm3", 0), 1), "mm3")
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
