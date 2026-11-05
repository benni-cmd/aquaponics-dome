"""Bilder des Scherenknotens fuer Bens Abnahme -> renders/components/knoten_schere/.
01-03: Probe-Knoten n01 (1 Platte + 6 Arm-Instanzen wie in data/components/knoten_schere.json) aus drei Richtungen;
04-05: Explosionsbild (Platte, 2 Laschen, Schrauben, Rohr auseinandergezogen; Verschiebungen = EXPLODE, dieselben wie die Viewer-Detailansicht);
06: Nasen-Detail (Rohr durchsichtig); 07: Arm A und Arm B seitlich (Knick 15,9 gegen 18,0 Grad).
Probe- und Explosionsdateien entstehen im Arbeitsordner WORKSHOP_TMP (nicht im Repo).
Aufruf: python -X utf8 scripts/workshop/knoten_schere.py --render"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sc
import knoten_schere as ks

OUT = os.path.join(sc.ROOT, "renders", "components", "knoten_schere")


def explode_vectors():
    """Verschiebung je Koerper im Explosionsbild (mm, Bauteilrahmen des Arms B: Strebe +X, Platte oben)."""
    g = ks.Geo("B")
    n, u = g.nrm, g.u
    m = lambda v, s: [round(x * s, 3) for x in v]
    return {"Lochplatte": [0, 0, 170], "Platte_ScheibeO": [0, 0, 225], "Platte_Schraube": [0, 0, 285],
            "Lasche_2": [0, 70, 45], "Lasche_1": [0, -70, -30],
            "Platte_ScheibeU": [0, 0, -70], "Platte_Mutter": [0, 0, -110],
            "Dreh_ScheibeO": m(n, 45), "Dreh_Schraube": m(n, 90), "Dreh_ScheibeU": m(n, -50), "Dreh_Mutter": m(n, -85),
            "Rohrstueck": m(u, 230)}


def main():
    import check_knoten_schere as ck
    tmp = sc.TMP
    probe, _ = ck.probe_script("n01", tmp)
    b, _ = ks.design("detail", explode=explode_vectors())
    expl = os.path.join(tmp, "knoten_schere_explosion.sc")
    sc.run(b.write("knoten-schere-explosion"), expl)
    glass = ["--body", "Rohrstueck:opacity=0.25"]
    shots = [  # name, Datei, Ziel, yaw, pitch, Abstand, extra
        ("01-knoten-n01-iso", probe, [0, 0, -40], 0.6, 0.6, 720, []),
        ("02-knoten-n01-draufsicht", probe, [0, 0, -40], 0.0, 1.5607, 680, []),
        ("03-knoten-n01-seite", probe, [0, 0, -50], 0.0, 0.05, 720, []),
        ("04-explosion-iso", expl, [170, 0, 30], 0.55, 0.7, 700, []),
        ("05-explosion-draufsicht", expl, [210, 0, 0], 0.0, 1.5607, 640, []),
        ("06-nase-detail", ks.OUT["B"], [round(x, 2) for x in ks.Geo("B").pt(ks.Geo("B").s_nose)], 0.45, 0.35, 200, glass),
        ("07-arm-b-seite", ks.OUT["B"], [110, 0, -40], 0.0, 0.0, 320, glass),
        ("08-arm-a-seite", ks.OUT["A"], [110, 0, -40], 0.0, 0.0, 320, glass)]
    nur = sys.argv[sys.argv.index("--nur") + 1].split(",") if "--nur" in sys.argv else None
    for nm, f, tgt, yaw, pitch, dist, extra in shots:
        if nur and nm[:2] not in nur:
            continue
        p = os.path.join(OUT, f"knoten_schere-{nm}.png")
        sc.snapshot(f, p, tgt, yaw, pitch, dist, w=1400, h=900, extra=extra)
        print(p)


if __name__ == "__main__":
    main()
