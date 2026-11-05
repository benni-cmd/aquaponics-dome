"""Pruefung Montage N-AUTOBAHN-V2 (docs/jobs/N-AUTOBAHN-V2.md Abschnitt 4 und 6) auf dem Bau-Skript scripts/dome-script-ring_b2.json und den Trassen:
Zaehlung (Blatt 6 Punkt 3), Hoehen (Ring und Schlauch im Gang >= Z 2100 rel), Halterabstaende (Ring <= 1000, Schlauch <= 400, freier Fall <= 1500),
Stuetzpunkte ausserhalb der Gangbaender, Schlauchlaengen, Abweichung Schlauchende zum Port. Rein geometrisch, kein CAD-Lauf (Interferenz: scripts/interf_ring_b2.py).
Aufruf: python -X utf8 scripts/check_autobahn_montage.py [r1|r2]   (Exit 1 bei FAIL)"""
import json, math, os, sys
from collections import Counter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "workshop"))
import variante, trassen_ring as TR, autobahn_s as AS, leitungen as LTG

RUNDE = "r2" if "r2" in sys.argv else "r1"
cmds = json.load(open(variante.pfad("dome_script", "ring_b2"), encoding="utf-8"))["commands"]
occ = [c["params"]["occurrence"] for c in cmds if c["command"] == "occurrence.move"]
cnt = Counter(o.split(":")[0] for o in occ)
doc = LTG.laden_variante("ring_b2")
rs = [r for r in doc["r_stuecke"] if r.get("quelle") == "trassen_ring"]
FZ = TR.FZ; GANG = {"A": (2195.0, 2795.0), "B": (3959.0, 4492.0)}   # Radialbaender wie scripts/workshop/check_autobahn_t.py GANG [E]
res = []
def chk(name, ist, soll, ok):
    res.append(ok); print(("PASS" if ok else "FAIL"), name, "| Ist:", ist, "| Soll:", soll)

# ---- R1: Zaehlung
chk("Joche (Portal_Joch_Mitte_A + _B)", cnt["Portal_Joch_Mitte_A"] + cnt["Portal_Joch_Mitte_B"], 7, cnt["Portal_Joch_Mitte_A"] + cnt["Portal_Joch_Mitte_B"] == 7)
chk("Stelzen (Ringstuetze_d75_B)", cnt["Ringstuetze_d75_B"], 3, cnt["Ringstuetze_d75_B"] == 3)
chk("Montageschienen 41 / Schienenverbinder 36", (cnt["Montageschiene_41_2179"], cnt["Schienenverbinder_36"]), (10, 10), cnt["Montageschiene_41_2179"] == 10 and cnt["Schienenverbinder_36"] == 10)
chk("Ring-Ecken d75 36 Grad", cnt["Ring_Ecke_d75"], 10, cnt["Ring_Ecke_d75"] == 10)
nkl = cnt["Lt_Klemme_d75"] + cnt["Lt_Klemme_d75_Ecke"] + cnt["Lt_Klemme_d75_Stelze"]
chk("Ring-Schellen d75", nkl, "30 (10 Ecken + 2 je Seite; Blatt schaetzte 22)", nkl == 30)
chk("Pegelschaechte auf Podest", (cnt["Pegelschacht"], cnt["Pegelschacht_Podest"]), (2, 2), cnt["Pegelschacht"] == 2 and cnt["Pegelschacht_Podest"] == 2)
chk("Booster (pumpe_gross)", cnt["Booster_gross"], 4, cnt["Booster_gross"] == 4)
chk("Rueckschlagventile d50", sum(1 for r in rs if r.get("datei") == "lt_rueckschlagventil_d50"), 4, sum(1 for r in rs if r.get("datei") == "lt_rueckschlagventil_d50") == 4)
chk("Entluefter d75", cnt["Entluefter_d75"], 2, cnt["Entluefter_d75"] == 2)
hk = Counter(("kupplung" if "-K" in r["id"] and r["id"].endswith("-H") else "ringende" if "ringende" in r["id"] else "entleerung" if "entleerung" in r["id"] else "?") for r in rs if r.get("art") == "kugelhahn")
chk("Kugelhaehne d63 (Kupplung / Ring-Ende / Entleerung)", (hk["kupplung"], hk["ringende"], hk["entleerung"]), (2, 2, 2), (hk["kupplung"], hk["ringende"], hk["entleerung"]) == (2, 2, 2))

# ---- R1: Hoehe und Halter des Rings
EC = TR.EC; ach = TR.Z["achse"]
chk("Ring-Unterkante (Achse - 37,5) / Schellen-Unterkante [rel]", (round(ach - 37.5 - FZ, 1), round(ach - 43.5 - FZ, 1)), ">= 2100", ach - 43.5 - FZ >= 2100 - 1e-6)
# Schellen-Lage als Laufmeter auf dem Ring (Ecke k: Scheitel bei k*SEITE + Korrektur Bogen)
eint, ein, feeds, bel = TR.leitungen_eintraege()
per = TR.N * (TR.SEITE - 2 * EC["tangente"]) + TR.N * EC["bogen_l"]
def lauf_ecke(k, s): return k * (TR.SEITE - 2 * EC["tangente"] + EC["bogen_l"]) + s
def lauf_seite(k, s): return k * (TR.SEITE - 2 * EC["tangente"] + EC["bogen_l"]) + EC["bogen_l"] / 2 + (s - EC["tangente"])
pos = []
for f, m, k, s in TR.schellen(bel):
    pos.append(lauf_ecke(k, TR.S_SCHELLE[k] if TR.stp_by_k()[k]["art"] == "joch" else 0.0) if s == "scheitel" else lauf_seite(k, s))
pos = sorted(p % per for p in pos); gaps = [(pos[(i + 1) % len(pos)] - pos[i]) % per for i in range(len(pos))]
chk("Ring: groesster Schellenabstand entlang der Achse [mm] (Leitungsordnung R6 d75)", round(max(gaps)), "<= 1000", max(gaps) <= 1000)
# Stuetzpunkte im Gang?
inn = []
for s in TR.stuetzpunkte():
    if s["art"] != "stelze": continue
    r = s["r_pfosten"]; ov = {g: max(0.0, min(r + 100, b) - max(r - 100, a)) for g, (a, b) in GANG.items()}
    inn.append((round(TR.ECKEN_AZ[s["k"]], 1), round(r), ov))
chk("Stelzen-Fussplatte (r +-100) ausserhalb Gang A/B [mm Ueberdeckung]", inn, "0 je Gang", all(v == 0 for _, _, ov in inn for v in ov.values()))
for l in (1, 2):
    c = TR.world(ein[l]["m_po"], (0, 0, 0)); r = math.hypot(c[0], c[1]); ov = {g: round(max(0.0, min(r + 250, b) - max(r - 250, a))) for g, (a, b) in GANG.items()}
    chk(f"Pegelschacht Linie {l} (Fass mit Stutzen r +-250) ausserhalb Gang A/B [mm Ueberdeckung]", (round(r), ov), "0 je Gang", all(v == 0 for v in ov.values()))

if RUNDE == "r2":
    fl = TR.fallleitungen()
    nz = Counter((a["linie"], a["art"]) for a in fl)
    chk("Fallleitungen je Linie (Beete, Tische)", [(l, nz[(l, "beet")], nz[(l, "tisch")]) for l in (1, 2)], "je Linie 7 Beete, 12 Tische", all(nz[(l, "beet")] == 7 and nz[(l, "tisch")] == 12 for l in (1, 2)))
    chk("Ausleger", sum(v for k, v in cnt.items() if k.startswith("Ausleger_Schlauch")), 18, sum(v for k, v in cnt.items() if k.startswith("Ausleger_Schlauch")) == 18)
    chk("Abzweige d40 / d32", (cnt["Ring_Abzweig_d40"], cnt["Ring_Abzweig_d32"]), (14, 24), (cnt["Ring_Abzweig_d40"], cnt["Ring_Abzweig_d32"]) == (14, 24))
    # Schlauch im Gang: tiefster Punkt der Schlauchachse - AD/2, ueber Gangband A/B, ohne die senkrechten Fallstrecken ueber dem Abnehmer
    tief, frei, laengen, miss, jenseits = [], [], [], [], []
    for a in fl:
        w = a["weg"]; ad = w["ad"]
        pts = []
        for seg in (w["s1"],):
            for i in range(len(seg) - 1):
                p0, p1 = seg[i], seg[i + 1]
                for t in range(0, 11): pts.append(tuple(p0[j] + (p1[j] - p0[j]) * t / 10 for j in range(3)))
        for p in pts:
            r = math.hypot(p[0], p[1])
            for g, (lo, hi) in GANG.items():
                if lo <= r <= hi: tief.append((round(p[2] - ad / 2 - FZ), a["name"], g))
        L = sum(AS.hose_length(AS.hose_layout([list(p) for p in s], w["Rb"]), w["Rb"]) for s in (w["s1"], w["s2"], w["s3"]))
        laengen.append((a["idd"], L))
        # freie Spannen: Ausleger-Typen -> Tuelle bis erster Clip (Weg entlang s1), Clip-Raster (WA-T <= 400), Fall Sattel -> Regelhahn; Mitte -> Fall Abzweig -> Regelhahn
        if a["zone"] == "mitte":
            frei.append(("fall", a["name"], a["abgang"][2] - w["z_ht"], 1500.0))
        else:
            au = a["ausleger"]; x_clip1 = TR.TW["teile"]["ausleger_schlauch_%d" % au["lg"]]["ports"][1]["lage"][0]
            c1 = TR.world(au["m"], (x_clip1, a["y_clip"], 0.0))
            s1 = w["s1"]; acc = 0.0; best = None
            for i in range(len(s1) - 1):
                p0, p1 = s1[i], s1[i + 1]; sl = math.dist(p0, p1)
                for t in range(0, 101):
                    q = tuple(p0[j] + (p1[j] - p0[j]) * t / 100 for j in range(3))
                    if best is None or math.dist(q, c1) < best[0]: best = (math.dist(q, c1), acc + sl * t / 100)
                acc += sl
            frei.append(("auf", a["name"], best[1], 400.0)); frei.append(("clip", a["name"], round(best[0], 1), 5.0))
            frei.append(("fall", a["name"], TR.Z_ARM - w["z_ht"], 1500.0))
        miss.append((a["name"], round(math.dist(w["s3"][-1], w["E_up"] if w.get("winkel") else w["E"]), 1)))
        # W88: kein Schlauchstueck jenseits des Ports (keine Schlaufe ueber dem Pool bzw. hinter dem Abnehmer), gemessen entlang der Port-Richtung d_o
        # Soll: hoechstens bis zur Fall-Linie oder einen kurzen Anlauf (Rb + 45) hinter den Port; mehr ist ein Umweg (Schlaufe), wie W88 ihn zeigte
        ax = lambda q: TR.dot(TR.sub((q[0], q[1], 0.0), (w["E"][0], w["E"][1], 0.0)), a["d_o"])
        jenseits.append((round(max(ax(q) for q in w["s3"]) - max(ax(w["s3"][0]), 0.0) - (w["Rb"] + 45), 1), a["name"]))
    tmin = min(tief) if tief else (None,)
    chk("Schlauch-Unterkante ueber Gang A/B [rel] (tiefster Punkt)", tmin[:3], ">= 2100", (not tief) or tmin[0] >= 2100)
    for art, soll in (("auf", 400.0), ("fall", 1500.0)):
        worst = max((f for f in frei if f[0] == art), key=lambda f: f[2] - f[3])
        n_over = sum(1 for f in frei if f[0] == art and f[2] > f[3])
        chk(f"Schlauch frei {'vom Abzweig bis zum ersten Ausleger-Clip' if art == 'auf' else 'im letzten Fall bis zum Regelhahn'} [mm] (R6 / Blatt 2.6.3)", f"max {worst[2]:.0f} ({worst[1]}), {n_over} ueber Soll", f"<= {soll:.0f}", n_over == 0)
    cl = [f for f in frei if f[0] == "clip"]; ncl = sum(1 for f in cl if f[2] > 5.0)
    chk("Schlauch liegt im Clip (Abstand Schlauchachse zum ersten Clip-Port)", f"max {max(f[2] for f in cl):.0f} mm, {ncl} von {len(cl)} > 5 mm", "<= 5 mm", ncl == 0)
    genutzt, gesamt = 0, 0
    for a in fl:
        if a["zone"] == "mitte": continue
        au = a["ausleger"]; s1 = a["weg"]["s1"]
        for pt in TR.TW["teile"]["ausleger_schlauch_%d" % au["lg"]]["ports"][1:-2:2]:
            c = TR.world(au["m"], (pt["lage"][0], a["y_clip"], 0.0)); gesamt += 1
            dmin = min(math.dist(tuple(s1[i][j] + (s1[i + 1][j] - s1[i][j]) * t / 200 for j in range(3)), c) for i in range(len(s1) - 1) for t in range(201))
            genutzt += dmin <= 5.0
    print(f"INFO Clips: Schlauch liegt in {genutzt} von {gesamt} Clip-Plaetzen der Ausleger (Rest: Versatz und Anstieg vor dem Arm)")
    s19 = sum(L for i, L in laengen if i == 19) / 1000; s25 = sum(L for i, L in laengen if i == 25) / 1000
    print(f"INFO Schlauchmeter aus den Wegen: ID19 {s19:.1f} m (Rechnung ID16 60,8), ID25 {s25:.1f} m (Rechnung 38,6); je Abnehmer {min(L for _, L in laengen):.0f} bis {max(L for _, L in laengen):.0f} mm")
    chk("Schlauchende = Endstueck am Port (Abstand) [mm]", max(m for _, m in miss), "<= 1", max(m for _, m in miss) <= 1.0)
    js = max(jenseits)
    chk("W88: kein Umweg unten (Schlauch reicht hoechstens bis Fall-Linie bzw. Anlauf Rb + 45 hinter den Port) [mm Ueberschuss entlang Port-Richtung]", js, "<= 0", js[0] <= 0.5)
    nh = sum(len(TR.halter_s3(a["weg"])) for a in fl); nw = sum(1 for a in fl if a["weg"].get("winkel"))
    lmax = max((math.dist(sg[1], sg[2]), a["name"]) for a in fl for sg in AS.hose_layout([list(p) for p in a["weg"]["s3"]], a["weg"]["Rb"]) if sg[0] == "G" and abs(sg[2][2] - sg[1][2]) <= 0.05 * math.dist(sg[1], sg[2]))
    print(f"INFO W88: {nh} Schlauchhalter auf waagerechten Strecken unten, {nw} Winkeltuellen am Port (Port zeigt vom Fall weg oder Fall fast ueber dem Port); laengste waagerechte Gerade {lmax[0]:.0f} mm ({lmax[1]})")

    # ---- N-AUTOBAHN-FIX P2/P3 (docs/jobs/N-AUTOBAHN-FIX.md Abschnitt 5): Abstand zur Kuppelhaut, Fallachsen aussen hinter Gang B
    # Huelle = konvexe Facetten aus den Strebenachsen (scripts/.segs.json, schreibt gen_dome.py; nach D91 Rundrohr 42,4: Rohr-Innenseite = Achse - 21,2;
    # an 5-wertigen Knoten liegt die Achse bis 15,9 mm neben dem Knotenpunkt, Pruefung N-VERBINDER) -> Normalabstand je Pruefpunkt = min ueber die Facetten.
    segs = json.load(open(os.path.join(HERE, ".segs.json"), encoding="utf-8"))
    key = lambda p: tuple(round(v) for v in p)
    nb = {}
    for A, B in segs:
        nb.setdefault(key(A), set()).add(key(B)); nb.setdefault(key(B), set()).add(key(A))
    tri = {tuple(sorted((a, b, c))) for a in nb for b in nb[a] for c in nb[b] if c in nb[a] and len({a, b, c}) == 3}
    zs = [p[2] for p in nb]; C0 = (0.0, 0.0, (min(zs) + max(zs)) / 2)
    facets = []
    for a, b, c in tri:
        n = TR.cross(TR.sub(b, a), TR.sub(c, a)); n = TR.unit(n)
        m = tuple((a[i] + b[i] + c[i]) / 3 for i in range(3))
        if TR.dot(n, TR.sub(m, C0)) < 0: n = TR.mul(n, -1)                       # Normale nach aussen (weg vom Kuppel-Innenpunkt C0)
        facets.append((n, TR.dot(n, a)))
    R_ROHR = 42.4 / 2
    def haut(p): return min(d - TR.dot(n, p) for n, d in facets) - R_ROHR      # > 0: innen, Abstand zur Rohr-Innenseite
    au_pts = []
    for a in fl:
        if a["zone"] == "mitte": continue
        au = a["ausleger"]; lg = au["lg"]
        for x in [i * (lg + TR.AT.AU["biege_r"]) / 20 for i in range(21)]:
            for y in (-62.0, 62.0):
                for z in (-20.0, 20.0): au_pts.append((haut(TR.world(au["m"], (x, y, z))), "Ausleger %d (%s)" % (lg, a["name"])))
    hs_pts = []
    for a in fl:
        w = a["weg"]
        for seg in (w["s1"], w["s2"], w["s3"]):
            for i in range(len(seg) - 1):
                for t in range(11):
                    q = tuple(seg[i][j] + (seg[i + 1][j] - seg[i][j]) * t / 10 for j in range(3)); hs_pts.append((haut(q) - w["ad"] / 2, a["name"]))
    ma, mh = min(au_pts), min(hs_pts)
    chk("Kuppelhaut: kleinster Normalabstand Ausleger (Huelle +-62 / +-20) zur Rohr-Innenseite der Facetten [mm] (FIX P2)", (round(ma[0]), ma[1]), ">= 100", ma[0] >= 100)
    chk("Kuppelhaut: kleinster Normalabstand Schlauch (Achse + AD/2) zur Rohr-Innenseite der Facetten [mm] (FIX P2)", (round(mh[0]), mh[1]), ">= 100", mh[0] >= 100)
    fa = [(round(math.hypot(*a["weg"]["D"])), a["name"]) for a in fl if a["zone"] == "aussen"]
    chk("Fallachse aussen (senkrechter Fall nach dem Sattel) hinter Gang B [r mm] (FIX P3)", min(fa), ">= 4560", min(fa)[0] >= 4560)

print(f"\n{sum(res)} PASS, {len(res) - sum(res)} FAIL von {len(res)} ({RUNDE})")
sys.exit(0 if all(res) else 1)
