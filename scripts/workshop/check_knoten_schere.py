"""Pruefung Scherenknoten (Blatt docs/jobs/N-VERBINDER.md, Pruefpunkte 1 bis 4).
1. Platte, Arm A, Arm B: alle Koerper geschlossen; Nasen reichen Rohraussenradius + nose_out (+-0,05); Rohrachse durch den Knotenpunkt (<= 0,01 mm).
2. Probe-Knoten n01 (6-wertig) und n02 (5-wertig, Pflicht seit Pruefer-Auflage a1ed36b), je Plattenpaar + Arm-Instanzen, gedreht wie in data/components/knoten_schere.json) im Scratchpad:
   inspect.interference 0 Durchdringungen ueber 0,1 mm3 (Schraube/Mutter/Scheibe im eigenen Arm ausgenommen: Gewinde- und Auflageberuehrung).
3. Knotentabelle: 26 Knoten, Armzahl = Wertigkeit aus data/layout.json (10 x 4, 6 x 5, 10 x 6), 130 Arme, A 60 / B 70.
4. Groesster Achsversatz nach Drehung um die Plattenschraube: gemeldet; Soll <= 5 mm, sonst BEFUND (kein FAIL, Blatt: melden statt umbauen).
Aufruf: python -X utf8 scripts/workshop/check_knoten_schere.py [--probe-dir DIR] [--knoten n01,n02]   (Exit 0 = alle PASS)"""
import json, math, os, re, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sc
import knoten_schere as ks

NORMTEIL = ("Platte_ScheibeO", "Platte_Schraube", "Platte_ScheibeU", "Platte_Mutter", "Dreh_ScheibeO", "Dreh_Schraube", "Dreh_ScheibeU", "Dreh_Mutter")


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def probe_script(knoten, out_dir):
    """Befehlsskript: Platte + je Arm eine verknuepfte Instanz, gedreht um die Plattennormale (Loch) und um die Plattenschraube (Abweichung)."""
    tab = {r["knoten"]: r for r in ks.DOC["knoten"]}[knoten]
    b = sc.Build()
    b.add("component.create", name=f"Probe_{knoten}")
    b.add("component.insert_design", path="designs/components/knoten_schere_platte.sc", name="Platte")
    rc = ks.P["bolt_circle_r"]
    for a in tab["arme"]:
        nm = f"Arm{a['arm']}_{a['typ']}"
        b.add("component.insert_design", path=f"designs/components/knoten_schere_arm_{a['typ'].lower()}.sc", name=nm)
        ang = a["drehwinkel_loch_grad"]
        if abs(ang) > 1e-9:
            b.add("occurrence.move", occurrence=f"{nm}:1", axis=[0, 0, 1], angle=f"{ang:.5f} deg", origin=[0, 0, 0], space="world")
        d = a["drehung_um_plattenschraube_grad"]
        if abs(d) > 1e-6:
            hx, hy = rc * math.cos(math.radians(ang)), rc * math.sin(math.radians(ang))
            b.add("occurrence.move", occurrence=f"{nm}:1", axis=[0, 0, 1], angle=f"{d:.5f} deg", origin=[round(hx, 5), round(hy, 5), 0], space="world")
    path = os.path.join(out_dir, f"knoten_schere_probe_{knoten}.sc")
    sc.run(b.write(f"knoten-schere-probe-{knoten}"), path)
    return path, tab


def interference(path):
    script = os.path.join(sc.TMP, "ws-schere-probe-int.json")
    json.dump({"commands": [{"command": "inspect.interference", "params": {}}]}, open(script, "w"))
    r = subprocess.run([sc.CLI, "run", script, "--in", path, "--results"], capture_output=True, text=True)
    if r.returncode:
        sys.exit("FEHLER interference: " + (r.stderr + r.stdout)[-400:])
    return json.loads(r.stdout)[0]


def probe_one(c, knoten, out_dir):
    path, row = probe_script(knoten, out_dir)
    pev = sc.evaluate(path)
    c.eq(f"Probe {knoten}: Koerper (2 Platten + {len(row['arme'])} x 11)", len(pev["bodies"]), 2 + 11 * len(row["arme"]))
    res = interference(path)
    pairs = res.get("interferences", res.get("pairs", []))
    unchecked = res.get("unchecked", [])

    def owner(p):
        return p.get("occurrence") or p.get("path") or ""
    bad, ignored = [], 0
    for p in pairs:
        vol = p.get("volume_mm3", p.get("volume", 0)) or 0
        a, b2 = p.get("a", p.get("body_a", "")), p.get("b", p.get("body_b", ""))
        an, bn = (a.get("name", "") if isinstance(a, dict) else str(a)), (b2.get("name", "") if isinstance(b2, dict) else str(b2))
        arm = lambda nm: (re.search(r"\((\d+)\)$", nm) or [None, "1"])[1]   # Instanz-Suffix "(n)" = gleicher Arm
        same = arm(an) == arm(bn)
        if vol <= 0.1:
            continue
        if same and (an.split("/")[-1] in NORMTEIL or bn.split("/")[-1] in NORMTEIL):
            ignored += 1
            continue
        bad.append((an, bn, round(vol, 3)))
    print(f"interference {knoten}: {len(pairs)} Paare gemeldet, {ignored} Normteil-Beruehrungen im eigenen Arm ausgenommen, ungeprueft {len(unchecked)}")
    for p in pairs[:8]:
        print("  Paar:", json.dumps(p, ensure_ascii=False)[:220])
    for x in bad[:12]:
        print("  Durchdringung:", x)
    if not pairs:
        print("  Rohantwort:", json.dumps(res)[:400])
    c.eq(f"Probe {knoten}: Durchdringungen > 0,1 mm3", len(bad), 0)
    c.eq(f"Probe {knoten}: ungepruefte Paare", len(unchecked), 0)


def main():
    c = sc.Check("knoten_schere")
    # --- 1. Einzelteile
    ev = {w: sc.evaluate(ks.OUT[w]) for w in ("platte", "A", "B")}
    for w, e in ev.items():
        n = len(e["bodies"])
        c.eq(f"{w}: alle Koerper geschlossen ({n})", sum(1 for x in e["bodies"] if x.get("closed")), n)
    c.eq("platte: 2 Koerper (Plattenpaar oben/unten, W83)", len(ev["platte"]["bodies"]), 2)
    pl = {x["name"]: x for x in ev["platte"]["bodies"]}
    c.eq("platte: obere und untere Platte gleich (Volumendifferenz mm3)", round(abs(pl["Lochplatte"].get("volume_mm3", pl["Lochplatte"].get("mass_g", 0)) - pl["Lochplatte_unten"].get("volume_mm3", pl["Lochplatte_unten"].get("mass_g", 0))), 3), 0.0, 0.01)
    for typ in "AB":
        g = ks.Geo(typ)
        bodies = {x["name"]: x for x in ev[typ]["bodies"]}
        c.eq(f"Arm {typ}: 11 Koerper (2 Laschen, Rohr, 8 Normteile)", len(bodies), 11)
        for nm in ("Lasche_1", "Lasche_2"):
            bb = bodies[nm]["bbox"]
            reach = max(abs(bb["min"][1]), abs(bb["max"][1]))
            c.eq(f"Arm {typ} {nm}: Nasenspitze = Rohraussenradius + {ks.P['nose_out']:g} mm (|Y| max, mm)", round(reach, 3), ks.P["tube_d"] / 2 + ks.P["nose_out"], 0.05)
        # Rohrachse aus der Zylinderflaeche des Rohrs gemessen (nicht aus den Bauparametern)
        cyl = [f["cylinder"] for f in sc.faces(ks.OUT[typ], "Rohrstueck") if f.get("cylinder") and abs(f["cylinder"]["radius"] - ks.P["tube_d"] / 2) < 0.01]
        ax, org = ks.unit(cyl[0]["axis"]), cyl[0]["origin"]
        cr = ks.cross(org, ax)
        c.eq(f"Arm {typ}: Rohrachse durch den Knotenpunkt (Abstand mm, gemessen)", round(math.sqrt(ks.dot(cr, cr)), 4), 0.0, 0.01)
        c.eq(f"Arm {typ}: Neigung der Rohrachse gegen die Platte (Grad)", round(math.degrees(math.asin(abs(ax[2]))), 3), round(g.deg, 3), 0.01)
        # Platte in Arm-Datei und Plattendatei auf gleicher Hoehe: Unterkante Lasche 2 = Plattenunterkante
        top = [f for f in sc.faces(ks.OUT[typ], "Lasche_2") if f.get("plane_normal") and f["plane_normal"][2] > 0.9999]
        top = max(top, key=lambda f: f["area"])                  # Oberseite des flachen Stuecks (Augenbereich)
        c.eq(f"Arm {typ}: Oberseite Lasche 2 (Auge) = Plattenunterkante (z mm, Flaeche gemessen)", round(top["centroid"][2], 3),
             round(pl["Lochplatte"]["bbox"]["min"][2], 3), 0.01)
        bot = [f for f in sc.faces(ks.OUT[typ], "Lasche_1") if f.get("plane_normal") and f["plane_normal"][2] < -0.9999]
        bot = max(bot, key=lambda f: f["area"])                  # Unterseite des flachen Stuecks (Augenbereich)
        c.eq(f"Arm {typ}: Unterseite Lasche 1 (Auge) = Oberkante untere Platte (z mm, Flaeche gemessen)", round(bot["centroid"][2], 3),
             round(pl["Lochplatte_unten"]["bbox"]["max"][2], 3), 0.01)
    # --- 3. Knotentabelle gegen layout.json
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    vl = [nd["valence"] for nd in lay["nodes_list"]]
    tab = ks.DOC["knoten"]
    c.eq("Tabelle: 26 Knoten (layout.json nodes_list)", len(tab), len(vl))
    c.eq("Tabelle: Knotenlage = layout.json (Abweichungen > 1 mm)", sum(1 for i, r in enumerate(tab) if math.dist(r["ursprung"], [lay["nodes_list"][i][k] for k in "xyz"]) > 1), 0)
    c.eq("Tabelle: Armzahl je Knoten = Wertigkeit layout.json (Abweichungen)", sum(1 for i, r in enumerate(tab) if len(r["arme"]) != vl[i]), 0)
    for v, soll in ((4, lay["node_valence"]["4"]), (5, lay["node_valence"]["5"]), (6, lay["node_valence"]["6"])):
        c.eq(f"Tabelle: {v}-wertige Knoten", sum(1 for r in tab if len(r["arme"]) == v), soll)
    c.eq("Tabelle: Arme gesamt", sum(len(r["arme"]) for r in tab), 130)
    c.eq("Tabelle: Enden Typ A", sum(1 for r in tab for a in r["arme"] if a["typ"] == "A"), 60)
    c.eq("Tabelle: Enden Typ B", sum(1 for r in tab for a in r["arme"] if a["typ"] == "B"), 70)
    c.eq("Tabelle: je Knoten jedes Loch hoechstens einmal belegt (Doppelbelegungen)", sum(len(r["arme"]) - len({a["loch"] for a in r["arme"]}) for r in tab), 0)
    # --- 2. Probe-Knoten
    out_dir = arg("--probe-dir", sc.TMP)
    for knoten in arg("--knoten", "n01,n02").split(","):        # Pflicht: 6-wertig n01 und 5-wertig n02 (Pruefer-Auflage 5, a1ed36b)
        probe_one(c, knoten, out_dir)
    # --- 4. Achsversatz (Befund, kein FAIL)
    au = ks.DOC["auswertung"]
    print(f"BEFUND-MESSUNG Achsversatz: groesster {au['groesster_achsversatz_mm']} mm bei {au['bei_knoten']} (Drehung {au['groesste_drehung_grad']} Grad); "
          + "; ".join(f"{v}-wertig {d['groesster_achsversatz_mm']} mm / {d['groesste_drehung_grad']} Grad" for v, d in au["je_wertigkeit"].items())
          + f"; Soll <= {au['soll_achsversatz_mm']} mm -> " + ("eingehalten" if au["groesster_achsversatz_mm"] <= au["soll_achsversatz_mm"] else "BEFUND: Lochbild je Knotentyp pruefen (Ben)"))
    return c.done()


if __name__ == "__main__":
    sys.exit(main())
