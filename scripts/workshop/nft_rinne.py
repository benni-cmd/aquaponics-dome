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
    for s in (-1, 1):
        b.add("solid.box", length="len_l", width="rib_w", height="rib_h", center=[0, s*p["rib_y"], hb + rh/2], operation="join", targets=["Rinnenprofil"], name="Rippe" + ("L" if s < 0 else "R"))
    b.add("solid.cylinder", diameter="hole_d", height="wall + 2", base=["-(n_holes-1)*pitch/2", 0, hb - w - 1], operation="cut", targets=["Rinnenprofil"], name="Topfloch1")
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
    for nm, pn, ds in (("T20_NFT_Rinne", "T20", d["beschreibung"]), ("T20a_Profil", "T20a", "Rinnenprofil 130x100x2,5 mit Rippen und Topfoeffnungen"),
                       ("T20b_Endkappe_Zulauf", "T20b", "Endkappe Zulauf mit Tuelle 16 mm"), ("T20c_Endkappe_Ablauf", "T20c", "Endkappe Ablauf mit Stutzen DN32")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

if __name__ == "__main__":
    b = build()
    script = b.write("nft_rinne")
    out = os.path.join(sc.ROOT, "designs", "components", "nft_rinne.sc")
    sc.run(script, out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], round(x["volume_mm3"], 1), "mm3", round(x["mass_g"], 1), "g", x["faces"], "F", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        sc.snapshot(out, os.path.join(sc.ROOT, "renders", "components", "nft_rinne", "nft_rinne-01.png"), [0, 0, 50], 0.7, 0.45, 5200, w=1000, h=500)
