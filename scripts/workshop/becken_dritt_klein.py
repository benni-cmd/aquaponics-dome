"""Drittbecken klein T14k (W34, R37 Befund 10, D66): Wanne Ø 920 (Ring 60) mit Hohlraum Ø 800 ab 120 mm Bodenstaerke, Wasserkoerper Ø 790 x 800, Rand 135 mm ueber dem Wasserspiegel; 0,4 m3.
KS: Ursprung Mitte der Beckenunterkante (Z 0); Einbau: Wasserspiegel Z 515 im Modellrahmen = Z 920 im Bauteil. Der Bestand becken_dritt.sc (gen_dome.py, Montage) bleibt unberuehrt.
W37-2 Teil 3: vier Anschluss-Stutzen K41 (Frischwasser d20, Muffe), K42 (Entnahme Biofilter d25, Muffe), K43 (Rueckfluss d25, Muffe), K49 (Luft, Schlauchtuelle ID16/AD20) als eigene Koerper
(Block auf der ebenen Rand-Oberkante + radialer Stutzen), Lage je Stutzen ueber winkel_k41/k42/k43/k49 (Vielfache von 90 Grad); die Wanne bleibt unveraendert.
Aufruf: python scripts/workshop/becken_dritt_klein.py [--render]"""

STUTZEN = (("K41", 20, "Muffe", "winkel_k41"), ("K42", 25, "Muffe", "winkel_k42"), ("K43", 25, "Muffe", "winkel_k43"), ("K49", 20, "Tuelle", "winkel_k49"))

def stutzen_ports(p):
    """[(name, (x,y,z), (dx,dy,dz), art, dn)] der Stutzen: Mitte der Oeffnungsebene am aeusseren Ende, Richtung radial nach aussen."""
    r_o = p["wasser_d"] / 2 + p["ring"]
    z = p["boden"] + p["wasser_tiefe"] + p["rand_ueber_wasser"] + p["stutzen_h"] / 2
    out = []
    for nm, d, art, key in STUTZEN:
        a = math.radians(p[key]); u = (round(math.cos(a), 6), round(math.sin(a), 6), 0)
        r = r_o + p["stutzen_len"]
        out.append((nm, (round(r * u[0], 3), round(r * u[1], 3), z), u, art, f"d{d}" if art == "Muffe" else "ID16"))
    return out
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import math
import sc
import leitung as L
import becken_soll as BS

def build():
    p, d = sc.load_params("becken_dritt_klein")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("material.create", name="Beton", density_g_cm3=2.4, color="#9a9a96")
    b.add("material.create", name="Wasser", density_g_cm3=1.0, color="#6fb6e8")
    root = "T14k_Drittbecken_klein"
    b.add("component.create", name=root, grounded=True)
    d_out = p["wasser_d"] + 2 * p["ring"]
    z_wasser = p["boden"] + p["wasser_tiefe"]                       # Wasserspiegel ueber der Unterkante (920)
    total = z_wasser + p["rand_ueber_wasser"]                       # Rand (1055)
    b.add("solid.cylinder", diameter=d_out, height=total, base=[0, 0, 0], axis=[0, 0, 1], operation="new", name="T14k_Wanne", body_name="T14k_Wanne")
    b.add("solid.cylinder", diameter=p["wasser_d"], height=total - p["boden"] + 1, base=[0, 0, p["boden"]], axis=[0, 0, 1], operation="cut", targets=["T14k_Wanne"], name="T14k_Hohlraum")
    b.add("material.assign", bodies=["T14k_Wanne"], material="Beton")
    b.add("solid.cylinder", diameter=p["wasser_d"] - p["wasser_spiel"], height=p["wasser_tiefe"], base=[0, 0, p["boden"]], axis=[0, 0, 1], operation="new", name="T14k_Wasser", body_name="Wasser")
    b.add("material.assign", bodies=["Wasser"], material="Wasser")
    b.add("material.create", name="Stutzen PVC", density_g_cm3=1.4, color="#8d9296")
    r_o = d_out / 2
    zb = total + p["stutzen_h"] / 2
    for nm, dd, art, key in STUTZEN:
        a = int(round(p[key])) % 360
        assert a % 90 == 0, "Stutzenwinkel nur Vielfache von 90 Grad (achsparallele Boeke)"
        ux, uy = round(math.cos(math.radians(a))), round(math.sin(math.radians(a)))
        rc = p["wasser_d"] / 2 + p["ring"] / 2
        bx, by = (p["stutzen_blk_r"], p["stutzen_blk_t"]) if ux else (p["stutzen_blk_t"], p["stutzen_blk_r"])
        body = "Stutzen_" + nm
        b.add("solid.box", length=bx, width=by, height=p["stutzen_h"], center=[rc * ux, rc * uy, zb], operation="new", name="R_" + body, body_name=body)
        od = L.od_f(dd) if art == "Muffe" else dd
        b.add("solid.cylinder", diameter=od, height=p["stutzen_len"] + 1, base=[(r_o - 1) * ux, (r_o - 1) * uy, zb], axis=[ux, uy, 0], operation="join", targets=[body], name=f"R_{body}_Rohr")
        if art == "Muffe":
            b.add("solid.cylinder", diameter=dd, height=L.DEPTH[dd] + 1, base=[(r_o + p["stutzen_len"] - L.DEPTH[dd]) * ux, (r_o + p["stutzen_len"] - L.DEPTH[dd]) * uy, zb], axis=[ux, uy, 0], operation="cut", targets=[body], name=f"R_{body}_Muffe")
        else:
            b.add("solid.cylinder", diameter=16, height=p["stutzen_len"] + 1, base=[(r_o + 1) * ux, (r_o + 1) * uy, zb], axis=[ux, uy, 0], operation="cut", targets=[body], name=f"R_{body}_Bohrung")
        b.add("material.assign", bodies=[body], material="Stutzen PVC")
    # U3 (D120): Ueberlauf-Tuelle d63 auf Wasserspiegelhoehe Richtung Anzuchtbecken (Weg e63), Azimut aus den Bauplaetzen von data/oasis-lage.json
    BS.ueberlauf_tuelle(b, p, "T14k_Wanne", 0, 0, z_wasser, BS.ue_azimut("feed", "nursery"), "T14k_Ueberlauf")
    b.add("component.metadata.set", component=root, part_number="T14k", description=d["beschreibung"], revision=d["revision"], properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "becken_dritt_klein.sc")
    sc.run(build().write("becken_dritt_klein"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], [(x["name"], round(x["volume_mm3"] / 1e6, 1), "l") for x in ev["bodies"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "becken_dritt_klein")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "becken_dritt_klein-01-schraeg.png"), [0, 0, 500], 0.7, 0.4, 2600, w=1000, h=700)
        sc.snapshot(out, os.path.join(rd, "becken_dritt_klein-02-schnitt.png"), [0, 0, 500], 0.0, 0.0, 2400, w=1000, h=700, section="y=0")
        sc.snapshot(out, os.path.join(rd, "becken_dritt_klein-03-stutzen.png"), [0, 0, 1000], 0.7, 0.55, 1900, w=1000, h=700)
