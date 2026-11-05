"""Leitungsteile W71 (N-REWORK B, Mangel M02): Ruecklauf-Sammler d110 fuer die Netz-Knoten ruecklauf_1/ruecklauf_2.
Bauweise wie leitung_w36.verteiler_d50 (Formstueck-Koerper, Bohrungen, ein Koerper); Konvention docs/parts/leitungsteile.md: Port A im Ursprung.
Schwerkraft-Sammler: Zulaeufe oben als Klebemuffen (Rohrende steckt direkt hinein), Auslauf A als Muffe d110 zum Pool, Ende geschlossen,
Teilstrom zum Zweitbecken als Zapfen d50 nach unten (K33, nur Linie 1; Linie 2 verschliesst ihn mit lt_kappe_d50). Gefaelle >= 1 % setzt die Montage.
leitung.py, leitung_w36/w37/w39.py bleiben unveraendert; ports() hier liefert die W71-Ports und fragt sonst leitung_w37.ports().
Aufruf: python -X utf8 scripts/workshop/leitung_w71.py [--out <ordner>] [--json]"""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w37 as W37

FILES = ["lt_sammler_d110"]              # check_leitungsteile.py zaehlt sie nicht zu den 63 Bibliotheksteilen
S_D = 110                                # Sammler d110 (K16/K32 DN100)
S_PITCH = 120                            # Teilung wie Verteiler d50
S_X0 = 120                               # erster Anschluss: Muffe A (Tiefe 61) + Radius Abgang d50 (25) + Luft
S_END = 10                               # integrierte Endkappe
S_SHOULDER = 5                           # Anschlag unter jeder Zulauf-Muffe (Rohr stoesst dort an)
S_STUB = 50                              # Zapfen-Ueberstand Abgang Zweitbecken unter dem Koerper
# (Name, d, Kanten Linie 1 / Linie 2, Soll l/min Linie 1, Linie 2, Art, Lage) in Reihenfolge vom Auslauf A aus
S_ANSCHL = [("Zweitbecken", 50, "K33 (nur Linie 1)", 5.0, 0.0, "Zapfen", "unten"),
            ("NFT", 63, "K15/K31", 38.0, 38.0, "Muffe", "oben"),
            ("Bypass", 50, "K13/K29", 14.5, 17.5, "Muffe", "oben"),
            ("Beet-Sumpf", 40, "K58/K59", 54.5, 54.5, "Muffe", "oben")]
S_KANTE_A = ("K16/K32", 102.0, 110.0)    # Auslauf zum Pool: Linie 1 (107 Zulauf minus 5 Zweitbecken), Linie 2

def geom():
    d = S_D
    of = L.od_f(d)
    xs = [S_X0 + S_PITCH * k for k in range(len(S_ANSCHL))]
    last = S_ANSCHL[-1][1]
    Lg = xs[-1] + L.od_f(last) / 2 + 16 + S_END          # letzte Muffe + Steg + Endkappe
    tops = {ds: of / 2 + S_SHOULDER + L.DEPTH[ds] for _, ds, *_ in S_ANSCHL}
    return dict(of=of, xs=xs, L=Lg, bore=d - 2 * L.wall_p(d), t=L.DEPTH[d], tops=tops, bottom=-(of / 2 + S_STUB))

def sammler():
    g = geom(); d, of, t = S_D, g["of"], g["t"]
    b = sc.Build(); nm = "T70_Sammler_d110"
    L.setup(b, nm, d, {"laenge": round(g["L"], 1), "anzahl_anschluesse": len(S_ANSCHL), "teilung": S_PITCH})
    b.add("solid.cylinder", diameter=of, height=g["L"], base=[0, 0, 0], axis=[1, 0, 0], operation="new", name="Sammler_R", body_name="Sammler")
    for k, ((fn, ds, kante, q1, q2, art, lage), x) in enumerate(zip(S_ANSCHL, g["xs"]), 1):
        if lage == "oben":     # Muffen-Stutzen: Aussen wie Formstueck d, von der Achse bis Oberkante
            b.add("solid.cylinder", diameter=L.od_f(ds), height=g["tops"][ds], base=[x, 0, 0], axis=[0, 0, 1], operation="join", targets=["Sammler"], name=f"Stutzen_{k}_{fn}")
        else:                  # Zapfen d nach unten
            b.add("solid.cylinder", diameter=ds, height=-g["bottom"], base=[x, 0, g["bottom"]], axis=[0, 0, 1], operation="join", targets=["Sammler"], name=f"Zapfen_{k}_{fn}")
    b.add("solid.cylinder", diameter=d, height=t + 1, base=[-1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Sammler"], name="Muffe_A")
    b.add("solid.cylinder", diameter=g["bore"], height=g["L"] - S_END - t + 1, base=[t - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Sammler"], name="Sammlerbohrung")
    for k, ((fn, ds, kante, q1, q2, art, lage), x) in enumerate(zip(S_ANSCHL, g["xs"]), 1):
        di = ds - 2 * L.wall_p(ds)
        if lage == "oben":
            top = g["tops"][ds]
            b.add("solid.cylinder", diameter=ds, height=L.DEPTH[ds] + 1, base=[x, 0, top - L.DEPTH[ds]], axis=[0, 0, 1], operation="cut", targets=["Sammler"], name=f"Muffe_{k}_{fn}")
            b.add("solid.cylinder", diameter=di, height=top - L.DEPTH[ds] + 1, base=[x, 0, 0], axis=[0, 0, 1], operation="cut", targets=["Sammler"], name=f"Bohrung_{k}_{fn}")
        else:
            b.add("solid.cylinder", diameter=di, height=-g["bottom"] + 2, base=[x, 0, g["bottom"] - 1], axis=[0, 0, 1], operation="cut", targets=["Sammler"], name=f"Bohrung_{k}_{fn}")
    b.add("material.assign", bodies=["Sammler"], material="LT pvc")
    L.meta(b, nm, "T70-S-110-4", f"Ruecklauf-Sammler d110 (Schwerkraft): Auslauf A Muffe d110, Zulaeufe oben Muffe d63 (NFT), d50 (Bypass), d40 (Beet-Sumpf), Abgang unten Zapfen d50 (Zweitbecken), Ende geschlossen")
    return b, nm, g

def ports(fname):
    if fname == "lt_sammler_d110":
        g = geom()
        out = [("A Auslauf", (0.0, 0.0, 0.0), (-1.0, 0.0, 0.0), "Muffe", L.DN[S_D])]
        for k, ((fn, ds, kante, q1, q2, art, lage), x) in enumerate(zip(S_ANSCHL, g["xs"]), 1):
            if lage == "oben":
                out.append((f"Zulauf {k} {fn}", (float(x), 0.0, round(g["tops"][ds], 3)), (0.0, 0.0, 1.0), art, L.DN[ds]))
            else:
                out.append((f"Abgang {k} {fn}", (float(x), 0.0, round(g["bottom"], 3)), (0.0, 0.0, -1.0), art, L.DN[ds]))
        return out
    return W37.ports(fname)

def json_entry():
    g = geom()
    return {"lt_sammler_d110": {
        "teilenummer": "T70-S-110-4", "komponente": "T70_Sammler_d110", "werkstoff": "PVC-U", "farbe": "grau (Ruecklauf)", "netz_knoten": ["ruecklauf_1", "ruecklauf_2"],
        "sammler": {"d": S_D, "wand": L.wall_p(S_D), "innen_d": round(g["bore"], 1), "formstueck_aussen": g["of"], "laenge": round(g["L"], 2), "muffentiefe_A": g["t"], "ende": "geschlossen (integrierte Kappe 10 mm)"},
        "teilung": S_PITCH, "gefaelle": ">= 1 % zum Auslauf A (setzt die Montage)",
        "anschluesse": [{"nr": k, "name": fn, "d": ds, "dn": L.DN[ds], "x": x, "lage": lage, "art": art, "kanten": kante, "soll_l_min": {"linie_1": q1, "linie_2": q2}}
                        for k, ((fn, ds, kante, q1, q2, art, lage), x) in enumerate(zip(S_ANSCHL, g["xs"]), 1)],
        "auslauf": {"kanten": S_KANTE_A[0], "soll_l_min": {"linie_1": S_KANTE_A[1], "linie_2": S_KANTE_A[2]}},
        "linie_2": "Abgang Zweitbecken mit lt_kappe_d50 verschliessen",
        "ports": [{"name": n, "lage": list(p), "richtung": list(dr), "art": a, "dn": dn} for n, p, dr, a, dn in ports("lt_sammler_d110")]}}

def write_json():
    p = os.path.join(sc.ROOT, "data", "components", "leitungsteile.json")
    raw = open(p, "rb").read().decode("utf-8")
    d = json.loads(raw)
    d.setdefault("w71_teile", {}).update(json_entry())
    txt = json.dumps(d, indent=1, ensure_ascii=False)
    if "\r\n" in raw:
        txt = txt.replace("\n", "\r\n")
    open(p, "w", encoding="utf-8", newline="").write(txt)

if __name__ == "__main__":
    if "--json" in sys.argv:
        write_json(); sys.exit(0)
    out_dir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(sc.ROOT, "designs", "components")
    b, nm, g = sammler()
    out = os.path.join(out_dir, "lt_sammler_d110.sc")
    sc.run(b.write("lt_sammler_d110"), out)
    print("lt_sammler_d110", out, {k: (round(v, 2) if isinstance(v, float) else v) for k, v in g.items()})
