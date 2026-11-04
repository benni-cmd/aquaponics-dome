"""Fundamentanker T61 (10 Stueck an den Basisknoten): Betonpunkt im Erdreich, Ankerplatte, 2 Verbundanker M16, Gabellaschen mit Querbolzen M12 zur Ankerlasche des Knotens.
Bezugspunkt: Knotenmitte des Basisknotens (X radial, Y tangential, Z oben). Aufruf: python scripts/workshop/fundamentanker.py [--render]"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("fundamentanker")
    b = sc.Build()
    for k, v in p.items():
        b.add("parameters.add", name=k, expression=f"{v} mm")
    b.add("material.create", name="Beton C25", density_g_cm3=2.4, color="#9a9a96")
    b.add("material.create", name="Stahl Anker", density_g_cm3=7.85, color=d["werkstoff"]["farbe"], pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    root = "T61_Fundamentanker"
    b.add("component.create", name=root, grounded=True)
    z_top = p["lug_hole_z"] - p["clevis_below_hole"]                  # Oberkante Ankerplatte
    z_pl0 = z_top - p["plate_t"]                                      # Unterkante Ankerplatte = Oberkante Beton
    off = p["anchor_off"]
    pos = ((off, off), (-off, -off))
    # --- Betonpunkt
    b.add("component.create", name="T61a_Betonpunkt")
    b.add("solid.box", length=p["block_x"], width=p["block_y"], height=p["block_z"], center=[0, 0, z_pl0 - p["block_z"] / 2], operation="new", name="Block_R", body_name="Betonpunkt")
    for k, (x, y) in enumerate(pos, 1):
        b.add("solid.cylinder", diameter=p["anchor_hole"], height=p["anchor_len"], base=[x, y, z_pl0 - p["anchor_len"]], operation="cut", targets=["Betonpunkt"], name=f"Bohrloch_{k}")
    b.add("material.assign", bodies=["Betonpunkt"], material="Beton C25")
    # --- Ankerplatte mit Loechern
    b.add("component.activate", component=root)
    b.add("component.create", name="T61b_Ankerplatte")
    b.add("solid.box", length=p["plate_s"], width=p["plate_s"], height=p["plate_t"], center=[0, 0, z_pl0 + p["plate_t"] / 2], operation="new", name="Platte_R", body_name="Ankerplatte")
    for k, (x, y) in enumerate(pos, 1):
        b.add("solid.cylinder", diameter=p["anchor_hole"], height=p["plate_t"] + 2, base=[x, y, z_pl0 - 1], operation="cut", targets=["Ankerplatte"], name=f"Plattenloch_{k}")
    b.add("material.assign", bodies=["Ankerplatte"], material="Stahl Anker")
    # --- Gabellaschen (zwei Platten, Spalt = Knotenlasche + Spiel), Loch D14 auf der Hoehe der Knotenlasche
    b.add("component.activate", component=root)
    b.add("component.create", name="T61c_Gabel")
    gap = p["lug_t"] + p["lug_clear"]
    zc = z_top + p["clevis_h"] / 2
    for sg, nm in ((1, "GabelAussen"), (-1, "GabelInnen")):
        b.add("solid.box", length=p["clevis_w"], width=p["clevis_t"], height=p["clevis_h"], center=[0, sg * (gap / 2 + p["clevis_t"] / 2), zc], operation="new", name=nm + "_R", body_name=nm)
        b.add("solid.cylinder", diameter=p["bolt_hole"], height=p["clevis_t"] + 2, base=[0, sg * (gap / 2 - 1), p["lug_hole_z"]], axis=[0, sg, 0], operation="cut", targets=[nm], name="Lasche_Loch_" + nm)
        b.add("material.assign", bodies=[nm], material="Stahl Anker")
    # --- Normteile: Verbundanker M16x300 mit Scheibe (Kopf oben), Querbolzen M12x50 mit 2 Scheiben und Mutter
    b.add("component.activate", component=root)
    b.add("component.create", name="T61d_Normteile")
    for k, (x, y) in enumerate(pos, 1):
        b.add("parts.insert", family="washer", size="M16", point=[x, y, z_top], direction=[0, 0, 1], name=f"ScheibeA_{k}")
        b.add("parts.insert", family="hex_bolt", size="M16", length=p["anchor_len"], point=[x, y, z_top + 3], direction=[0, 0, 1], name=f"Anker_{k}")
    yo = gap / 2 + p["clevis_t"]
    b.add("parts.insert", family="washer", size="M12", point=[0, yo, p["lug_hole_z"]], direction=[0, 1, 0], name="ScheibeQ_O")
    b.add("parts.insert", family="hex_bolt", size="M12", length=p["bolt_len"], point=[0, yo + p["washer_t"], p["lug_hole_z"]], direction=[0, 1, 0], name="Querbolzen")
    b.add("parts.insert", family="washer", size="M12", point=[0, -yo, p["lug_hole_z"]], direction=[0, -1, 0], name="ScheibeQ_U")
    b.add("parts.insert", family="hex_nut", size="M12", point=[0, -yo - p["washer_t"], p["lug_hole_z"]], direction=[0, -1, 0], name="MutterQ")
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T61", d["beschreibung"]), ("T61a_Betonpunkt", "T61a", "Betonpunkt 400x400x600 mit Bohrloechern"), ("T61b_Ankerplatte", "T61b", "Ankerplatte 250x250x15"), ("T61c_Gabel", "T61c", "Gabellaschen fuer die Knotenlasche"), ("T61d_Normteile", "T61d", "Verbundanker M16 und Querbolzen M12")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, dict(z_top=z_top, z_pl0=z_pl0)


def name_normteile(out):
    """parts.insert-Koerper heissen 'Body<n>': in Einfuegereihenfolge (wie die Feature-Namen im build) benennen, sonst bleibt der Name nur in der Stueckliste."""
    import re, json, subprocess
    ev = sc.evaluate(out)
    bodies = sorted((int(re.fullmatch(r"Body(\d+)", b["name"]).group(1)), b["name"]) for b in ev["bodies"] if re.fullmatch(r"Body\d+", b["name"]))
    ziel = ["ScheibeA_1", "Anker_1", "ScheibeA_2", "Anker_2", "ScheibeQ_O", "Querbolzen", "ScheibeQ_U", "MutterQ"]
    if len(bodies) != len(ziel):
        return 0
    cmds = [{"command": "body.rename", "params": {"body": alt, "name": neu}} for (_, alt), neu in zip(bodies, ziel)]
    script = os.path.join(sc.TMP, "ws-anker-names.json")
    json.dump({"commands": cmds}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", out, "--save", out, "--quiet"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("FEHLER name_normteile: " + r.stderr.strip() + r.stdout.strip())
    return len(cmds)

if __name__ == "__main__":
    b, info = build()
    out = os.path.join(sc.ROOT, "designs", "components", "fundamentanker.sc")
    sc.run(b.write("fundamentanker"), out)
    sc.assign_part_materials(out, "Stahl Anker")                       # Normteile (Body<n>) auf Stahl
    name_normteile(out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], round(x["mass_g"] / 1000, 2), "kg", [round(v) for v in x["bbox"]["min"]], [round(v) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        r = os.path.join(sc.ROOT, "renders", "components", "fundamentanker")
        os.makedirs(r, exist_ok=True)
        for n, (t, yaw, pitch, dist) in {"01-iso": ([0, 0, -400], 0.7, 0.4, 1800), "02-gabel": ([0, 0, -160], 0.6, 0.3, 450), "03-schnitt": ([0, 0, -400], 0.0, 0.0, 1800)}.items():
            sc.snapshot(out, os.path.join(r, f"fundamentanker-{n}.png"), t, yaw, pitch, dist, w=1000, h=700, section="XZ" if n == "03-schnitt" else None)
