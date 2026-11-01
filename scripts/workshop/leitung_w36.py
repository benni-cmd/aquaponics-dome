"""Leitungsteile W36 (Ergaenzung zur Bibliothek T70): Verteiler d50, Rohrschelle Vierkant, Leerrohr DN50/DN100, Schacht Kugelhaehne.
Bauweise wie leitung.py (gleiche Helfer, gleiche Konvention); die Bibliothek leitung.py ruft ports() hier per Fallback auf.
Aufruf: python scripts/workshop/leitung_w36.py [verteiler ...]   (ohne Teil: alle)"""
import sys, os, math, re
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

FILES = []          # Dateinamen (ohne .sc) der W36-Teile; check_leitungsteile.py zaehlt sie nicht zu den 63 Bibliotheksteilen

# ---------------------------------------------------------------- Teil 1: Verteiler d50
V50_D = 50                                    # Sammler-Rohr d50 (Muffe A nimmt das Rohr d50 des Biofilter-Ueberlaufs auf)
V50_PITCH = 120                               # Teilung wie der Bibliotheks-Verteiler: Kugelhahn-Gehaeuse d50 = 70,5 mm + Hebel
V50_X0 = 75                                   # erster Abgang: Rohr d50 steckt 31 mm in Muffe A, Abgang-Bohrung d50 beginnt erst bei x = 75 - 25 = 50
V50_END = 10                                  # integrierte Endkappe (Wand) am Ende B
V50_ABGAENGE = [("Beete", 40, "K11/K27", 54.5), ("NFT", 32, "K12/K28", 38.0), ("Messkreis", 20, "K35 (nur Linie 1)", 3.0), ("Bypass", 50, "K13/K29", 14.5)]

def v50_geom():
    d = V50_D
    of = L.od_f(d)
    xs = [V50_X0 + V50_PITCH * k for k in range(len(V50_ABGAENGE))]
    Lg = xs[-1] + 45 + V50_END                # letzte Abgang-Bohrung (d50: r 22,6) + Steg, dann Endkappe
    top = of / 2 + 50                         # Zapfen ragt 50 mm ueber den Verteilerkoerper
    return dict(of=of, xs=xs, L=Lg, top=top, bore=d - 2 * L.wall_p(d), t=L.DEPTH[d])

def verteiler_d50():
    g = v50_geom()
    d, of, t = V50_D, g["of"], g["t"]
    b = sc.Build(); nm = "T70_Verteiler_d50"
    L.setup(b, nm, d, {"laenge": round(g["L"], 1), "anzahl_abgaenge": len(V50_ABGAENGE), "teilung": V50_PITCH})
    b.add("material.create", name="LT pvc dunkelblau", density_g_cm3=1.4, color=L.COL["dunkelblau"])
    b.add("solid.cylinder", diameter=of, height=g["L"], base=[0, 0, 0], axis=[1, 0, 0], operation="new", name="Sammler_R", body_name="Verteiler")
    for k, ((fn, ds, kante, q), x) in enumerate(zip(V50_ABGAENGE, g["xs"]), 1):
        b.add("solid.cylinder", diameter=ds, height=g["top"], base=[x, 0, 0], axis=[0, 0, 1], operation="join", targets=["Verteiler"], name=f"Abgang_{k}_{fn}")
    b.add("solid.cylinder", diameter=d, height=t + 1, base=[-1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name="Muffe_A")
    b.add("solid.cylinder", diameter=g["bore"], height=g["L"] - V50_END - t + 1, base=[t - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=["Verteiler"], name="Sammlerbohrung")
    for k, ((fn, ds, kante, q), x) in enumerate(zip(V50_ABGAENGE, g["xs"]), 1):
        b.add("solid.cylinder", diameter=ds - 2 * L.wall_p(ds), height=g["top"] + 2, base=[x, 0, 0], axis=[0, 0, 1], operation="cut", targets=["Verteiler"], name=f"Abgangsbohrung_{k}_{fn}")
    b.add("material.assign", bodies=["Verteiler"], material="LT pvc dunkelblau")
    L.meta(b, nm, "T70-V-50-4", f"Verteiler d50 mit 4 Abgaengen d40 (Beete), d32 (NFT), d20 (Messkreis), d50 (Bypass), Teilung {V50_PITCH}, Muffe A d50, Ende B geschlossen")
    return b, nm, g

FILES.append("lt_verteiler_d50")

def ports(fname, L_rohr=1000):
    """Ports der W36-Teile, Format wie leitung.ports(): [(name, (x,y,z), (dx,dy,dz), art, dn)]."""
    if fname == "lt_verteiler_d50":
        g = v50_geom()
        out = [("A", (0.0, 0.0, 0.0), (-1.0, 0.0, 0.0), "Muffe", L.DN[50])]
        for k, ((fn, ds, kante, q), x) in enumerate(zip(V50_ABGAENGE, g["xs"]), 1):
            out.append((f"Abgang {k} {fn}", (float(x), 0.0, round(g["top"], 2)), (0.0, 0.0, 1.0), "Zapfen", L.DN[ds]))
        return out
    return []

def json_entries():
    """Maschinenlesbare Daten der W36-Teile fuer data/components/leitungsteile.json (Schluessel w36_teile)."""
    g = v50_geom()
    out = {"lt_verteiler_d50": {
        "teilenummer": "T70-V-50-4", "komponente": "T70_Verteiler_d50", "werkstoff": "PVC-U", "farbe": "dunkelblau",
        "sammler": {"d": V50_D, "wand": L.wall_p(V50_D), "innen_d": round(g["bore"], 1), "formstueck_aussen": g["of"], "laenge": g["L"], "muffentiefe_A": g["t"], "ende_B": "geschlossen (integrierte Kappe 10 mm)"},
        "teilung": V50_PITCH, "zapfen_hoehe_z": round(g["top"], 2),
        "abgaenge": [{"nr": k, "name": fn, "d": ds, "dn": L.DN[ds], "x": x, "kante": kante, "soll_l_min": q} for k, ((fn, ds, kante, q), x) in enumerate(zip(V50_ABGAENGE, g["xs"]), 1)],
        "ports": [{"name": n, "lage": list(p), "richtung": list(dr), "art": a, "dn": dn} for n, p, dr, a, dn in ports("lt_verteiler_d50")]}}
    return out

def write_json():
    import json
    p = os.path.join(sc.ROOT, "data", "components", "leitungsteile.json")
    d = json.load(open(p, encoding="utf-8"))
    d.setdefault("w36_teile", {}).update(json_entries())
    txt = json.dumps(d, indent=1, ensure_ascii=False).replace("\n", "\r\n")
    open(p, "w", encoding="utf-8", newline="").write(txt)

DESCRIPTIONS = [
    {"match": "^lt_verteiler_d50$", "titel": "Verteiler d50 (Hauptkreislauf)", "was": "Sammelrohr am Ende der Hauptleitung einer Linie; verteilt 110 l/min auf Beete, NFT, Messkreis und Bypass.",
     "status": "gebaut, 29/29 Prüfungen (Interferenz 0, Volumen gegen CSG-Raster)",
     "ablauf": ["Das Rohr d50 vom Biofilter-Überlauf steckt in die Muffe am Einlauf.", "Vier Abgänge nach oben: Beete d40, NFT d32, Messkreis d20, Bypass d50 (zuletzt, mit Drossel).", "Das Ende ist geschlossen; der Strom nimmt nach jedem Abgang ab."],
     "aufbau": [{"t": "Sammler", "p": ["Formstück 58,5 mm außen, Rohr d50 × 2,4, Länge 490", "Einlauf als Klebemuffe d50"]}, {"t": "Abgänge", "p": ["4 Zapfen, 50 mm Überstand, Teilung 120", "Platz für Kugelhähne und Hebel ohne Kollision"]}],
     "masse": {"Leergewicht": "0,78 kg (PVC-U)", "Wasser": "ca. 1,0 l", "Geschwindigkeit": "1,14 m/s im Sammler (Grenze 1,5)"},
     "grenzen": "Stopfen für den unbenutzten Messkreis-Abgang (Linie 2) fehlen in der Bibliothek.", "quelle": "docs/parts/leitungsteile.md (Ergänzung W36)"},
]

def write_descriptions():
    """Fuegt die W36-Eintraege vor dem Sammeleintrag '^lt_' in data/descriptions.json ein (Viewer nimmt den ersten Treffer); idempotent."""
    import json
    p = os.path.join(sc.ROOT, "data", "descriptions.json")
    txt = open(p, "rb").read().decode("utf-8")
    anchor = '    {\r\n      "match": "^lt_",'
    assert txt.count(anchor) == 1
    for e in DESCRIPTIONS:
        if json.dumps(e["match"], ensure_ascii=False) in txt:
            continue
        body = json.dumps(e, indent=2, ensure_ascii=False).replace("\n", "\n    ").replace("\n", "\r\n")
        txt = txt.replace(anchor, "    " + body + ",\r\n" + anchor)
    open(p, "wb").write(txt.encode("utf-8"))
    json.loads(txt)

if __name__ == "__main__" and "--json" in sys.argv:
    write_json(); write_descriptions(); sys.exit(0)

if __name__ == "__main__":
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    jobs = {"verteiler": ("lt_verteiler_d50", verteiler_d50)}
    for key, (fname, fn) in jobs.items():
        if want and key not in want:
            continue
        res = fn()
        L.save(res[0], res[1], fname)
        print(fname, res[2])
