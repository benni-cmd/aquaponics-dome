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

# ---------------------------------------------------------------- Teil 2: Rohrschelle fuer Vierkant-Tischbein
LEG = 40.0                                    # Tischbein Rechteckrohr 40 x 40 x 3 (docs/parts/nft_tisch.md, leg_w)
SCH_SIZES = (32, 63)
SCH_T, SCH_W = 3.0, 20.0                      # Ringwand und Ringbreite wie lt_klemme (Ring 3, Breite 20)
SCH_PLATE_T, SCH_PLATE_HALF = 4.0, 37.0       # Rueckenplatte 74 x 20 x 4
SCH_BAND_T, SCH_SPIEL, SCH_TAB = 3.0, 0.5, 14.0   # Spannband 20 x 3, Spiel zum Bein 0,5, Lasche 14
SCH_SCREW_X = 30.0                            # Bandschrauben M6x16 bei x = +-30 durch Lasche und Platte (Kopf 11,6 mm ueber Ecken: 24,2 bis 35,8, frei vom Band bei 23,5)
SCH_STANDOFF = 14.0                           # Plattenvorderseite bis Rohroberflaeche: Platz fuer Mutter M6 (5,2) und Schraubenende (3,8) vor dem Rohr

def sch_geom(d):
    ro = d / 2 + SCH_T
    ypf = -d / 2 - SCH_STANDOFF               # Plattenvorderseite (Rohrseite)
    yf = ypf - SCH_PLATE_T                    # Plattenrueckseite = Anlageflaeche des Beins
    return dict(ro=ro, ypf=ypf, yf=yf, yb=yf - LEG, ear_z=ro + 7.0, leg_y=yf - LEG / 2)

def schelle(d):
    g = sch_geom(d)
    ro, yf, yb = g["ro"], g["yf"], g["yb"]
    b = sc.Build(); nm = f"T70_Schelle_VK40_d{d}"
    L.setup(b, nm, d, {"bein": LEG, "ringbreite": SCH_W, "bandbreite": SCH_W})
    ez = g["ear_z"]
    for half, ys in (("vorn", 1), ("hinten", -1)):
        body = f"Halbschale_{half}"
        b.add("solid.cylinder", diameter=2 * ro, height=SCH_W, base=[-SCH_W / 2, 0, 0], axis=[1, 0, 0], operation="new", name=f"Ring_{half}", body_name=body)
        b.add("solid.cylinder", diameter=d, height=SCH_W + 2, base=[-SCH_W / 2 - 1, 0, 0], axis=[1, 0, 0], operation="cut", targets=[body], name=f"Bohrung_{half}")
        b.add("solid.box", length=SCH_W + 2, width=ro + 2, height=2 * ro + 2, center=[0, -ys * (ro + 2) / 2, 0], operation="cut", targets=[body], name=f"Schnitt_{half}")      # andere Haelfte weg
        for sz in (-1, 1):
            b.add("solid.box", length=SCH_W, width=4.0, height=14.0 + 1, center=[0, ys * 2.0, sz * (ro + 7 - 0.5)], operation="join", targets=[body], name=f"Ohr_{half}_{sz}")
        for sz in (-1, 1):
            b.add("solid.cylinder", diameter=6.4, height=9.0, base=[0, -4.5, sz * ez], axis=[0, 1, 0], operation="cut", targets=[body], name=f"Ohrloch_{half}_{sz}")
    # Rueckenplatte mit Steg (gehoert zur hinteren Halbschale); der Steg haelt die Platte 14 mm vom Rohr ab, 1 mm Ueberlappung mit Ring und Platte
    ypf = g["ypf"]
    b.add("solid.box", length=SCH_W, width=(-ro + 1) - (ypf - 1), height=SCH_W, center=[0, ((ypf - 1) + (-ro + 1)) / 2, 0], operation="join", targets=["Halbschale_hinten"], name="Steg")
    b.add("solid.box", length=2 * SCH_PLATE_HALF, width=SCH_PLATE_T, height=SCH_W, center=[0, (yf + ypf) / 2, 0], operation="join", targets=["Halbschale_hinten"], name="Platte")
    for sx in (-1, 1):
        b.add("solid.cylinder", diameter=6.4, height=SCH_PLATE_T + 2, base=[sx * SCH_SCREW_X, yf - 1, 0], axis=[0, 1, 0], operation="cut", targets=["Halbschale_hinten"], name=f"Plattenloch_{sx}")
    b.add("material.assign", bodies=["Halbschale_vorn", "Halbschale_hinten"], material="LT stahl")
    # Spannband um das Bein (U-Form, Spiel 0,5): Ruecken, zwei Seiten, zwei Laschen auf der Plattenrueckseite
    sp, bt = SCH_SPIEL, SCH_BAND_T
    xs_in = LEG / 2 + sp
    b.add("solid.box", length=2 * (xs_in + bt), width=bt, height=SCH_W, center=[0, yb - sp - bt / 2, 0], operation="new", name="Band_Ruecken", body_name="Spannband")
    for sx in (-1, 1):
        ymid = ((yb - sp - bt) + yf) / 2
        b.add("solid.box", length=bt, width=yf - (yb - sp - bt), height=SCH_W, center=[sx * (xs_in + bt / 2), ymid, 0], operation="join", targets=["Spannband"], name=f"Band_Seite_{sx}")
        b.add("solid.box", length=SCH_TAB, width=bt, height=SCH_W, center=[sx * (xs_in + bt - 1 + SCH_TAB / 2), yf - bt / 2, 0], operation="join", targets=["Spannband"], name=f"Band_Lasche_{sx}")
        b.add("solid.cylinder", diameter=6.4, height=bt + 2, base=[sx * SCH_SCREW_X, yf - bt - 1, 0], axis=[0, 1, 0], operation="cut", targets=["Spannband"], name=f"Laschenloch_{sx}")
    b.add("material.assign", bodies=["Spannband"], material="LT stahl")
    # Normteile: Ringschrauben M6x16 (Kopf vorn, Mutter hinten), Bandschrauben M6x16 (Kopf auf der Lasche, Mutter vor der Platte)
    for sz in (-1, 1):
        b.add("parts.insert", family="hex_bolt", size="M6", length=16, point=[0, 4.0, sz * ez], direction=[0, 1, 0], name=f"Ringschraube_{sz}")      # point = Kopfauflage, Kopf liegt in Richtung direction, Schaft entgegen
        b.add("parts.insert", family="hex_nut", size="M6", point=[0, -4.0, sz * ez], direction=[0, -1, 0], name=f"Ringmutter_{sz}")
    for sx in (-1, 1):
        b.add("parts.insert", family="hex_bolt", size="M6", length=16, point=[sx * SCH_SCREW_X, yf - bt, 0], direction=[0, -1, 0], name=f"Bandschraube_{sx}")
        b.add("parts.insert", family="hex_nut", size="M6", point=[sx * SCH_SCREW_X, yf + SCH_PLATE_T, 0], direction=[0, 1, 0], name=f"Bandmutter_{sx}")
    L.meta(b, nm, f"T70-SVK-{d}", f"Rohrschelle fuer Rohr d{d} an Vierkant-Tischbein 40x40: 2 Halbschalen mit 2 Schrauben M6x16, Rueckenplatte, Spannband 20x3 um das Bein mit 2 Schrauben M6x16")
    return b, nm, g

for _d in SCH_SIZES:
    FILES.append(f"lt_schelle_vk_d{_d}")

def ports(fname, L_rohr=1000):
    """Ports der W36-Teile, Format wie leitung.ports(): [(name, (x,y,z), (dx,dy,dz), art, dn)]."""
    m = re.match(r"lt_schelle_vk_d(\d+)$", fname)
    if m:
        d = int(m.group(1)); g = sch_geom(d)
        return [("Rohrachse", (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), "Aufnahme", L.DN[d]),
                ("Bein", (0.0, round(g["leg_y"], 2), 0.0), (0.0, 0.0, 1.0), "Aufnahme", "Vierkant 40x40")]
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
    for d in SCH_SIZES:
        g = sch_geom(d)
        out[f"lt_schelle_vk_d{d}"] = {"teilenummer": f"T70-SVK-{d}", "komponente": f"T70_Schelle_VK40_d{d}", "werkstoff": "Stahl verzinkt (Ring, Platte, Band), Schrauben M6x16 ISO 4017 und Muttern M6",
            "rohr_d": d, "bein": "Rechteckrohr 40x40x3", "ring": {"innen_d": d, "aussen_d": 2 * g["ro"], "wand": SCH_T, "breite": SCH_W}, "platte": {"breite": 2 * SCH_PLATE_HALF, "dicke": SCH_PLATE_T, "abstand_zum_rohr": SCH_STANDOFF},
            "spannband": {"breite": SCH_W, "dicke": SCH_BAND_T, "spiel": SCH_SPIEL, "lasche": SCH_TAB}, "bolzenbild": {"ring_z": g["ear_z"], "band_x": SCH_SCREW_X}, "anlageflaeche_y": g["yf"], "beinachse_y": g["leg_y"],
            "ports": [{"name": n, "lage": list(p), "richtung": list(dr), "art": a, "dn": dn} for n, p, dr, a, dn in ports(f"lt_schelle_vk_d{d}")]}
    return out

def write_json():
    import json
    p = os.path.join(sc.ROOT, "data", "components", "leitungsteile.json")
    d = json.load(open(p, encoding="utf-8"))
    d.setdefault("w36_teile", {}).update(json_entries())
    txt = json.dumps(d, indent=1, ensure_ascii=False).replace("\n", "\r\n")
    open(p, "w", encoding="utf-8", newline="").write(txt)

DESCRIPTIONS = [
    {"match": "^lt_schelle_vk_", "titel": "Rohrschelle für Vierkant-Tischbein", "was": "Hält ein Rohr (d32 oder d63) waagerecht am senkrechten Vierkant-Bein 40 × 40 des Tischs; die Fuß-Klemme der Bibliothek passt nicht an ein Bein.",
     "status": "gebaut, 30/30 Prüfungen mit Interferenz 0 gegen Bein und Rohr",
     "ablauf": ["Zwei Halbschalen mit je zwei Schrauben M6 umfassen das Rohr.", "Eine Rückenplatte mit Steg liegt am Bein; ein Spannband um das Bein zieht die Platte mit zwei Schrauben M6 fest.", "Der Steg hält die Platte 14 mm vom Rohr entfernt, damit Muttern und Schraubenenden Platz haben."],
     "aufbau": [{"t": "Blechteile", "p": ["Halbschalen (Ring 3 mm, Breite 20) mit Ohren", "Rückenplatte 74 × 20 × 4 mit Steg", "Spannband 20 × 3 um das Bein, Spiel 0,5 mm"]}, {"t": "Normteile", "p": ["4 Schrauben M6 × 16 mit 4 Muttern"]}],
     "masse": {"Gewicht": "d32 270 g, d63 315 g (Stahl)", "Bein": "Rechteckrohr 40 × 40 × 3"}, "grenzen": "Befestigung nur an Tischbeinen, nie an Streben (Plan M10 Regel 7).", "quelle": "docs/parts/leitungsteile.md (Ergänzung W36)"},
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
    jobs = [("verteiler", "lt_verteiler_d50", verteiler_d50)]
    jobs += [("schelle", f"lt_schelle_vk_d{d}", (lambda d=d: schelle(d))) for d in SCH_SIZES]
    for key, fname, fn in jobs:
        if want and key not in want:
            continue
        res = fn()
        out = L.save(res[0], res[1], fname)
        if key == "schelle":
            sc.assign_part_materials(out, "LT stahl")                  # Normteile (Body<n>) tragen sonst die Standarddichte 1,29
        print(fname, res[2])
