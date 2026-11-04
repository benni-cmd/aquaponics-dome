"""Luftverteiler und Scheibenbelueftung (W37-3, Teil 2 und 3): Hauptverteiler 6-fach `luftverteiler_6` (T86), Pool-Verteiler 4-fach `luftverteiler_4` (T87),
EPDM-Scheibenbelueftungsteil `luft_scheibenbelueftung` (T88). Bauweise der Verteiler wie `lt_verteiler_d50` (W36): Sammler d40 als Formstueck (Aussen od_f), Abgaenge als Zapfen, Teilung 120,
Muffe A d40 am Einlauf, Ende B geschlossen. Rohre und Ventile (Kugelhahn, Rueckschlagventil aus Bibliothek/W39) stecken ueber Zapfen und Muffen und sind nicht Teil dieser Datei.
KS Verteiler: Port A (Mitte der Muffenoeffnung) im Ursprung, Sammlerachse +X, Abgaenge nach +Z. KS Scheibe: Port A (Ende des Anschlussstutzens) im Ursprung, Stutzen nach +Z.
Aufruf: python -X utf8 scripts/workshop/luft_verteiler.py [luftverteiler_6|luftverteiler_4|luft_scheibenbelueftung ...] [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

SAMMLER_D = 40                    # Sammler d40 (Netz K44, R45 Abschnitt 4)
TOP = 50                          # Zapfen ragt 50 ueber den Sammlerkoerper (wie lt_verteiler_d50)
KLASSEN = ("luftverteiler_6", "luftverteiler_4")
MATS = (("LV PVC", 1.4, "#3d6f9e"), ("LV PP", 0.91, "#e8e5d8"), ("LV EPDM", 1.15, "#1f2023"))

def v_geom(p, abgaenge):
    of = L.od_f(SAMMLER_D)
    xs = [p["x0"] + p["pitch"] * k for k in range(len(abgaenge))]
    last_r = max(a[1] for a in abgaenge[-1:]) / 2
    Lg = xs[-1] + 25 + p["end_cap"]                               # letzte Abgangsbohrung (Radius <= 20) plus Steg, dann Endkappe
    return dict(of=of, xs=xs, L=Lg, top=of / 2 + TOP, bore=SAMMLER_D - 2 * L.wall_p(SAMMLER_D), t=L.DEPTH[SAMMLER_D])

def abgang_d(ds):
    """Aussen-Ø des Zapfens: ein Abgang mit dem Durchmesser des Sammlers braucht im Kernel ~60 s je Schnitt (W37-2): 0,25 mm duenner, Bohrung 0,2 mm kleiner."""
    return ds - 0.25 if ds >= SAMMLER_D else ds

def abgang_bohrung(ds):
    return ds - 2 * L.wall_p(ds) - (0.2 if ds >= SAMMLER_D else 0.0)

def build_verteiler(name):
    p, d = sc.load_params(name)
    ab = d["abgaenge"]                                           # [[Name, DN, Kante, l_min, Herkunft], ...]
    g = v_geom(p, ab)
    t, of = g["t"], g["of"]
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in MATS:
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = d["teilenummer"] + "_" + name
    b.add("component.create", name=root, grounded=True)
    b.add("solid.cylinder", diameter=of, height=g["L"], base=[0, 0, 0], axis=[1, 0, 0], operation="new", name="Sammler_R", body_name="Verteiler")
    for k, (a, x) in enumerate(zip(ab, g["xs"]), 1):
        b.add("solid.cylinder", diameter=abgang_d(a[1]), height=g["top"], base=[x, 0, 0], axis=[0, 0, 1], operation="join", targets=["Verteiler"], name=f"Abgang_{k}")
    b.add("solid.cylinder", diameter=SAMMLER_D, height=t + 1, base=[-1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name="Muffe_A")
    b.add("solid.cylinder", diameter=g["bore"], height=g["L"] - p["end_cap"] - t + 1, base=[t - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name="Sammlerbohrung")
    for k, (a, x) in enumerate(zip(ab, g["xs"]), 1):
        b.add("solid.cylinder", diameter=abgang_bohrung(a[1]), height=g["top"] + 2, base=[x, 0, 0], axis=[0, 0, 1], operation="cut", targets=["Verteiler"], name=f"Abgangsbohrung_{k}")
    b.add("material.assign", bodies=["Verteiler"], material="LV PVC")
    b.add("component.metadata.set", component=root, part_number=d["teilenummer"], description=d["beschreibung"], revision="A", properties={"Werkstoff": "PVC-U"})
    return b, g

# ---------------------------------------------------------------- Scheibenbelueftung
def s_geom(p):
    d = p["d"]
    fuss_d = max(40.0, round(0.26 * d))
    z0 = p["stutzen_l"]; z1 = z0 + p["fuss_h"]; z2 = z1 + p["teller_h"]; z3 = z2 + p["membran_h"]
    return dict(fuss_d=fuss_d, z0=z0, z1=z1, z2=z2, z3=z3, teller_d=d - p["teller_rand"], bohr=p["luft_bohrung"])

def build_scheibe():
    name = "luft_scheibenbelueftung"
    p, d = sc.load_params(name)
    g = s_geom(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in MATS:
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = d["teilenummer"] + "_" + name
    b.add("component.create", name=root, grounded=True)
    b.add("solid.cylinder", diameter=p["pipe_d"], height=g["z0"], base=[0, 0, 0], operation="new", name="R_Stutzen", body_name="Stutzen")
    b.add("solid.cylinder", diameter=g["bohr"], height=g["z0"] + 2, base=[0, 0, -1], operation="cut", targets=["Stutzen"], name="Stutzenbohrung")
    b.add("solid.cylinder", diameter=g["fuss_d"], height=p["fuss_h"], base=[0, 0, g["z0"]], operation="new", name="R_Fuss", body_name="Stuetzfuss")
    b.add("solid.cylinder", diameter=g["bohr"], height=p["fuss_h"] + 2, base=[0, 0, g["z0"] - 1], operation="cut", targets=["Stuetzfuss"], name="Fussbohrung")
    b.add("solid.cylinder", diameter=g["teller_d"], height=p["teller_h"], base=[0, 0, g["z1"]], operation="new", name="R_Teller", body_name="Tragteller")
    b.add("solid.cylinder", diameter=p["d"], height=p["membran_h"], base=[0, 0, g["z2"]], operation="new", name="R_Membran", body_name="Membran")
    b.add("material.assign", bodies=["Stutzen", "Stuetzfuss", "Tragteller"], material="LV PP")
    b.add("material.assign", bodies=["Membran"], material="LV EPDM")
    b.add("component.metadata.set", component=root, part_number=d["teilenummer"], description=d["beschreibung"], revision="A", properties={"Werkstoff": "PP / EPDM"})
    return b, g

def main():
    want = [a for a in sys.argv[1:] if not a.startswith("--")]
    todo = want or ["luftverteiler_6", "luftverteiler_4", "luft_scheibenbelueftung"]
    for name in todo:
        out = os.path.join(sc.ROOT, "designs", "components", name + ".sc")
        b, g = build_scheibe() if name == "luft_scheibenbelueftung" else build_verteiler(name)
        sc.run(b.write(name), out)
        ev = sc.evaluate(out)
        mn, mx = sc.bbox_all(ev)
        print(name, "Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx], "Masse g", round(ev["total"]["mass_g"]))
        if "--render" in sys.argv:
            rd = os.path.join(sc.ROOT, "renders", "components", name)
            os.makedirs(rd, exist_ok=True)
            if name == "luft_scheibenbelueftung":
                sc.snapshot(out, os.path.join(rd, name + "-01-schraeg.png"), [0, 0, 60], 0.7, 0.45, 650, w=1000, h=700)
                sc.snapshot(out, os.path.join(rd, name + "-02-schnitt.png"), [0, 0, 50], 3.14159, 0.0, 480, w=1000, h=700, section="XZ")
            else:
                cx = g["L"] / 2
                dist = g["L"] * 1.6
                sc.snapshot(out, os.path.join(rd, name + "-01-schraeg.png"), [cx, 0, 20], 0.6, 0.5, dist, w=1100, h=720)
                sc.snapshot(out, os.path.join(rd, name + "-02-oben.png"), [cx, 0, 20], 0.0, 1.5, dist, w=1100, h=720)
                sc.snapshot(out, os.path.join(rd, name + "-03-schnitt.png"), [cx, 0, 20], 0.0, 0.0, dist, w=1100, h=720, section="y=0")

if __name__ == "__main__":
    main()
