"""NFT-Rinne T20 (Baugruppe aus Profil + 2 Endkappen). Aufruf: python scripts/workshop/nft_rinne.py [--render]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("nft_rinne")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("material.create", name="PVC-U weiss", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"])
    b.add("component.create", name="T20_NFT_Rinne", grounded=True)
    # --- Profil mit Rippen und Topfoeffnungen
    b.add("component.create", name="T20a_Profil")
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [0, 1, 0], "y_dir": [0, 0, 1]}, name="Querschnitt")
    W, H, w, rh = p["ch_w"], p["ch_h"], p["wall"], p["rib_h"]
    hb = H - rh                                  # Hoehe des Rohrkoerpers ohne Rippen
    b.add("sketch.rectangle.two_point", p0=[-W/2, 0], p1=[W/2, hb])
    b.add("sketch.rectangle.two_point", p0=[-W/2 + w, w], p1=[W/2 - w, hb - w])
    b.add("sketch.finish")
    b.add("solid.extrude", distance="len_l", direction="symmetric", name="Profil", body_name="Rinnenprofil")
    # vier Rippen auf der Oberseite (innen y1, aussen y2), enden rib_end vor den Kappen
    for nm in ("RippeI", "RippeA"):
        yk = "rib_y1" if nm == "RippeI" else "rib_y2"
        for sgn in (-1, 1):
            b.add("solid.box", length="len_l - 2*rib_end", width="rib_w", height="rib_h", center=[0, f"{sgn}*{yk}", hb + rh/2], operation="join", targets=["Rinnenprofil"], name=nm + ("L" if sgn < 0 else "R"))
    # EINE Lochreihe in der Mittellinie, n_holes Loecher, Teilung pitch, um shift verschoben
    b.add("solid.cylinder", diameter="hole_d", height="wall + 2", base=["-(n_holes-1)*pitch/2 + shift", 0, hb - w - 1], operation="cut", targets=["Rinnenprofil"], name="Topfloch1")
    b.add("solid.pattern.rectangular", features=["Topfloch1"], dir1=[1, 0, 0], count1="n_holes", spacing1="pitch")
    b.add("material.assign", bodies=["Rinnenprofil"], material="PVC-U weiss")
    # --- Endkappen: Platte + Zapfen + Stutzen mit Bohrung
    for name, sx, od, idd, ln, zz, tag in (("T20b_Endkappe_Zulauf", -1, "inlet_od", "inlet_id", "inlet_len", "inlet_z", "Zulauf"),
                                           ("T20c_Endkappe_Ablauf", 1, "drain_od", "drain_id", "drain_len", "drain_z", "Ablauf")):
        b.add("component.activate", component="T20_NFT_Rinne")
        b.add("component.create", name=name)
        xc = f"{sx}*len_l/2"
        b.add("solid.box", length="cap_t", width="ch_w", height="ch_h", center=[f"{xc} + {sx}*cap_t/2", 0, H/2], operation="new", name="Platte" + tag, body_name="Kappe" + tag)
        b.add("solid.box", length="plug_len", width="ch_w - 2*wall - 2*fit", height=f"{hb} - 2*wall - 2*fit", center=[f"{xc} - {sx}*plug_len/2", 0, hb/2],
              operation="join", targets=["Kappe" + tag], name="Zapfen" + tag)
        b.add("solid.box", length="plug_len + 1", width="ch_w - 2*wall - 2*fit - 8", height=f"{hb} - 2*wall - 2*fit - 8", center=[f"{xc} - {sx}*(plug_len + 1)/2 - {sx}*0.01", 0, hb/2],
              operation="cut", targets=["Kappe" + tag], name="Tasche" + tag)
        b.add("solid.cylinder", diameter=od, height=f"{ln} + cap_t", base=[xc, 0, zz], axis=[sx, 0, 0], operation="join", targets=["Kappe" + tag], name="Stutzen" + tag)
        b.add("solid.cylinder", diameter=idd, height=f"{ln} + cap_t + plug_len + 2", base=[f"{xc} - {sx}*plug_len - {sx}", 0, zz], axis=[sx, 0, 0], operation="cut", targets=["Kappe" + tag], name="Bohrung" + tag)
        b.add("material.assign", bodies=["Kappe" + tag], material="PVC-U weiss")
        b.add("appearance.assign", bodies=["Kappe" + tag], color="#d6d8dc")
    b.add("component.activate", component="T20_NFT_Rinne")
    b.add("config.configure", params=["len_l", "n_holes", "shift"])      # L aussen, M Mitte, K innen; Phase A/B = Zickzack-Versatz im Tisch
    b.add("config.row", name="L_A")
    for row, ln, n, sh in (("L_B", 3232, 12, 62.5), ("M_A", 1983, 7, -62.5), ("M_B", 1983, 7, 62.5), ("K_A", 1304, 5, -62.5), ("K_B", 1304, 5, 62.5)):
        b.add("config.row", name=row, **{"from": "L_A"}, values={"param:len_l": f"{ln} mm", "param:n_holes": str(n), "param:shift": f"{sh} mm"})
    b.add("config.activate", row="L_A")
    for nm, pn, ds in (("T20_NFT_Rinne", "T20", d["beschreibung"]), ("T20a_Profil", "T20a", "Rinnenprofil 130x100x2,5 mit Rippen und Topfoeffnungen"),
                       ("T20b_Endkappe_Zulauf", "T20b", "Endkappe Zulauf mit Tuelle 16 mm"), ("T20c_Endkappe_Ablauf", "T20c", "Endkappe Ablauf mit Stutzen DN32")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

def render(out, p):
    """Testaufbau (nur Render): Rinne + 3 Netztoepfe + 3 Salatkoepfe in den ersten Topfloechern; Kameras fuellen das Bild."""
    items = [("component.create", {"name": "Test", "grounded": True}),
             ("component.insert_design", {"path": "designs/components/nft_rinne.sc", "name": "R1"})]
    x0 = -(p["n_holes"] - 1) * p["pitch"] / 2 + p["shift"]
    zp = p["ch_h"] - p["rib_h"] - 59.5
    for nm, path, dz in (("P", "netztopf", 0), ("S", "salatkopf", 63)):
        items.append(("component.insert_design", {"path": f"designs/components/{path}.sc", "name": f"{nm}1", "translate": [x0, 0, zp + dz]}))
        for k in (1, 2):
            items.append(("occurrence.copy", {"component": f"{nm}1", "translate": [k * p["pitch"], 0, 0]}))
    b = sc.Build()
    for c, q in items:
        b.add(c, **q)
    tmp = os.path.join(sc.TMP, "nft_rinne_test.sc")
    sc.run(b.write("nft_rinne_test"), tmp)
    r = os.path.join(sc.ROOT, "renders", "components", "nft_rinne")
    L = p["len_l"]
    views = {"02-zulauf-ende": ([-L/2 + 150, 0, 60], 0.9, 0.45, 750), "03-ablauf-ende": ([L/2 - 150, 0, 60], -2.3, 0.45, 750),
             "04-oberseite-toepfe": ([x0 + p["pitch"], 0, 95], 0.35, 1.0, 600), "05-ueberblick": ([0, 0, 50], 0.7, 0.3, 4300)}
    for n, (t, yaw, pitch, dist) in views.items():
        sc.snapshot(tmp, os.path.join(r, f"nft_rinne-{n}.png"), t, yaw, pitch, dist, w=1000, h=650)
    sc.snapshot(tmp, os.path.join(r, "nft_rinne-06-schnitt-zulauf.png"), [-L/2 + 200, 0, 55], 3.14159, 0.0, 520, w=1000, h=520, section="XZ")
    sc.snapshot(tmp, os.path.join(r, "nft_rinne-07-querschnitt.png"), [x0 + p["pitch"] + 80, 0, 50], 1.5708, 0.0, 420, w=800, h=600, section="YZ,flip")

if __name__ == "__main__" and "--render-only" not in sys.argv:
    b = build()
    script = b.write("nft_rinne")
    out = os.path.join(sc.ROOT, "designs", "components", "nft_rinne.sc")
    sc.run(script, out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], round(x["volume_mm3"], 1), "mm3", round(x["mass_g"], 1), "g", x["faces"], "F", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        render(out, sc.load_params("nft_rinne")[0])
if __name__ == "__main__" and "--render-only" in sys.argv:
    render(os.path.join(sc.ROOT, "designs", "components", "nft_rinne.sc"), sc.load_params("nft_rinne")[0])

def make_variants():
    """Je Laenge (L aussen, M Mitte, K innen) und Phase (A/B = Zickzack) eine Datei aus der Master-Datei: Konfigurationszeile aktivieren, speichern."""
    import subprocess, json as _j
    master = os.path.join(sc.ROOT, "designs", "components", "nft_rinne.sc")
    for row in ("L_A", "L_B", "M_A", "M_B", "K_A", "K_B"):
        f = "nft_rinne_" + row.lower() + ".sc"
        script = os.path.join(sc.TMP, f"cfg-{row}.json")
        _j.dump({"commands": [{"command": "config.activate", "params": {"row": row}}]}, open(script, "w"))
        r = subprocess.run([sc.CLI, "run", script, "--in", master, "--save", os.path.join(sc.ROOT, "designs", "components", f), "--quiet"], capture_output=True, text=True)
        if r.returncode != 0:
            sys.exit("FEHLER Variante " + row + ": " + r.stderr)
        ev = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f))
        pr = [b for b in ev["bodies"] if b["name"] == "Rinnenprofil"][0]
        print("Variante", row, "->", f, "Laenge", round(pr["bbox"]["max"][0] - pr["bbox"]["min"][0]), "Flaechen", pr["faces"])

if __name__ == "__main__" and "--variants" in sys.argv:
    make_variants()
