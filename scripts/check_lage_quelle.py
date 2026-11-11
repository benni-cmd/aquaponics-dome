"""N-UNIFY-AUTOBAHN L1: Ueberlagerungs-Pruefung Modell-Draufsicht gegen die Quell-Draufsicht (Leons Oasis-Showcase, D117).

Aufruf (Projektordner):
  python -I -X utf8 scripts/check_lage_quelle.py            misst, druckt die Tabelle, schreibt renders/lage-quelle-vs-modell.png, Exit 0 (alles innerhalb) / 1
  python -I -X utf8 scripts/check_lage_quelle.py --md       zusaetzlich die Tabelle als Markdown (fuer das Paket)
  python -I -X utf8 scripts/check_lage_quelle.py --ohne-bild  ohne PNG

Soll: data/oasis-draufsicht.json (Erzeuger scripts/oasis_draufsicht.py, direkt aus der SVG `#mainSvg`).
Ist:  viewer/instances.json (Matrix je Instanz, Feld `built` nennt den Stand) + viewer/detail/<definition>.json (Koerper-Boxen, nur lesen).
      Fehlt die Detaildatei (z. B. Komponenten aus U2), gilt der Ursprung der Instanz als Mitte des Fussabdrucks (Bezugspunkt steht in
      data/components/<name>.json: "Mitte der Standflaeche") und das Mass aus den Parametern dieser Datei, sonst entfaellt der Massvergleich.

Regeln (Grenzen aus dem Auftrag L1):
  Mittelpunkt: Abstand Ist - Soll hoechstens 150 mm.
  Mass: Durchmesser bzw. Rechteckkanten innerhalb 5 % (nur wo Soll und Ist ein Mass haben; Symbole der Quelle, A16, werden nur nach Lage verglichen).
  Drehung (Rechtecke): hoechstens 5 Grad (modulo 180).
  Vorbau: Ist-Mitte ausserhalb r 6000, Soll-Mitte innerhalb -> Verstoss.
  Anbauringe: mittlerer Radius der Segment-Mitten je Ring hoechstens 150 mm vom Bogenradius der Quelle; Stueckzahl gleich; kein Segment in der Oeffnung
  (120 Grad um Az -72, Tuer-Achse).
Vergleichsmass bei Becken: Aussenkontur des gebauten Koerpers (Huelle); das Wasser-/Innenmass steht daneben (ANNAHME D151).
"""
import itertools
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLL = os.path.join(ROOT, "data", "oasis-draufsicht.json")
INST = os.path.join(ROOT, "viewer", "instances.json")
DETAIL = os.path.join(ROOT, "viewer", "detail")
COMP = os.path.join(ROOT, "data", "components")
BILD = os.path.join(ROOT, "renders", "lage-quelle-vs-modell.png")

TOL_MITTE, TOL_MASS, TOL_DREH, KUPPEL_R = 150.0, 0.05, 5.0, 6000.0


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


S = load(SOLL)
I = load(INST)
INSTANCES = I["instances"]
_DET = {}


def detail(defn):
    if defn not in _DET:
        p = os.path.join(DETAIL, defn + ".json")
        _DET[defn] = load(p)["koerper"] if os.path.exists(p) else None
    return _DET[defn]


def comp_par(name, key):
    p = os.path.join(COMP, name + ".json")
    if not os.path.exists(p):
        return None
    v = load(p).get("parameter", {}).get(key)
    return v["wert"] if v else None


def xy(m, u, v):
    return (m[0] * u + m[1] * v + m[3], m[4] * u + m[5] * v + m[7])


def yaw(m):
    return math.degrees(math.atan2(m[4], m[0]))


def az(x, y):
    return math.degrees(math.atan2(y, x))


def az_norm(a):
    return (a + 180.0) % 360.0 - 180.0


def hull(points):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def body_info(i, body):
    """(Mitte x, y, lokale Kantenlaenge u, v) eines benannten Koerpers der Instanz; None wenn Detail oder Koerper fehlt."""
    ks = detail(i["d"])
    if not ks:
        return None
    ks = [k for k in ks if k["name"] == body]
    if not ks:
        return None
    lo = [min(k["bbox"]["min"][a] for k in ks) for a in range(3)]
    hi = [max(k["bbox"]["max"][a] for k in ks) for a in range(3)]
    cx, cy = xy(i["m"], (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2)
    return cx, cy, hi[0] - lo[0], hi[1] - lo[1]


def inst_hull(i):
    ks = detail(i["d"])
    if not ks:
        return None
    pts = []
    for k in ks:
        lo, hi = k["bbox"]["min"], k["bbox"]["max"]
        for u in (lo[0], hi[0]):
            for v in (lo[1], hi[1]):
                pts.append(xy(i["m"], u, v))
    return hull(pts)


def centroid(h):
    return sum(p[0] for p in h) / len(h), sum(p[1] for p in h) / len(h)


# Zuordnung Soll-Teil -> Modell: (Definitionen, Gruppe (gemeinsame Zuordnung), Koerper fuer das Mass, Zusatzkoerper Innenmass, Art, Ersatzmass)
SPEC = {
    "fish": (("pool_zentral",), "fish", "T5_Zentraltank", "T5_Wasser", "kreis", None),
    "nursery": (("zweitbecken",), "nursery", "T6_Zweitbecken", "T6_Wasser", "kreis", None),
    "feed": (("becken_dritt_klein",), "feed", "T14k_Wanne", "Wasser", "kreis", None),
    "vortex_1": (("tank_klein",), "vortex", "Tank", None, "kreis", None), "vortex_2": (("tank_klein",), "vortex", "Tank", None, "kreis", None),
    "bio_1": (("tank_gross", "tank_gross_t3"), "bio", "Tank", None, "kreis", None), "bio_2": (("tank_gross", "tank_gross_t3"), "bio", "Tank", None, "kreis", None),
    "sludge_1": (("schlamm_sammelbehaelter",), "sludge", None, None, "kreis", ("schlamm_sammelbehaelter", "aussen_d")),
    "sludge_2": (("schlamm_sammelbehaelter",), "sludge", None, None, "kreis", ("schlamm_sammelbehaelter", "aussen_d")),
    "sump_1": (("sumpftank", "sumpftank_spiegel"), "sump", "Sumpf_Folie", None, "rechteck", None), "sump_2": (("sumpftank", "sumpftank_spiegel"), "sump", "Sumpf_Folie", None, "rechteck", None),   # L2 (D152): Sumpf 2 gespiegelt
    "permakultur": (("permakultur_modul",), "perma", None, None, "rechteck", ("permakultur_modul", ("kompost_l", "kompost_b"))),
    "filterpumpe_1": (("tauchpumpe_modul",), "pumpen", None, None, "punkt", None), "filterpumpe_2": (("tauchpumpe_modul",), "pumpen", None, None, "punkt", None),
    "hauptpumpe_1": (("tauchpumpe_modul",), "pumpen", None, None, "punkt", None), "hauptpumpe_2": (("tauchpumpe_modul",), "pumpen", None, None, "punkt", None),
    "venturi_1": (("venturi_belueffter",), "venturi", None, None, "punkt", None), "venturi_2": (("venturi_belueffter",), "venturi", None, None, "punkt", None),
    "schwimmer_1": (("schwimmerschalter_hochstand",), "schwimmer", None, None, "punkt", None), "schwimmer_2": (("schwimmerschalter_hochstand",), "schwimmer", None, None, "punkt", None),
    "nachspeise": (("nachspeise_ventil",), "nachspeise", None, None, "punkt", None),
    "luftpumpe": (("notluftpumpe",), "notluft", None, None, "punkt", None),
    "luftpumpe_1": (("geblaese_luft",), "geblaese", None, None, "punkt", None), "luftpumpe_2": (("geblaese_luft",), "geblaese", None, None, "punkt", None),
    "rain": (("regentank_5m3",), "regen", None, None, "punkt", None),
    "control": (("schaltschrank",), "schrank", "T11_Schaltschrank", None, "punkt", None),
}


def sx(i):
    return i["m"][3], i["m"][7]


def zuordnen():
    """Instanzen -> Soll-IDs einer Gruppe nach kleinster Gesamtentfernung (wie check_oasis_soll.assign)."""
    gruppen = {}
    for sid, sp in SPEC.items():
        gruppen.setdefault(sp[1], []).append(sid)
    erg = {}
    for g, ids in gruppen.items():
        defs = SPEC[ids[0]][0]
        insts = [i for i in INSTANCES if i["d"] in defs]
        if g == "pumpen":
            pass
        if len(insts) < len(ids):
            for k, sid in enumerate(ids):
                erg[sid] = insts[k] if k < len(insts) else None
            continue
        best = None
        for perm in itertools.permutations(range(len(insts)), len(ids)):
            d = sum(math.hypot(sx(insts[k])[0] - S["teile"][s]["x_mm"], sx(insts[k])[1] - S["teile"][s]["y_mm"]) for k, s in zip(perm, ids))
            if best is None or d < best[0]:
                best = (d, perm)
        for k, s in zip(best[1], ids):
            erg[s] = insts[k]
    return erg


def messen():
    zu = zuordnen()
    zeilen = []
    for sid, sp in SPEC.items():
        so = S["teile"][sid]
        i = zu.get(sid)
        z = {"id": sid, "name": so["name"], "art": so["art"], "soll": so, "ist": None, "fehler": [], "info": [], "in_umfang": so["im_umfang"]}
        zeilen.append(z)
        if i is None:
            z["fehler"].append("FEHLT: keine Instanz von %s im Export" % "/".join(sp[0]))
            continue
        defs, grp, body, body_innen, art, ersatz = sp
        bi = body_info(i, body) if body else None
        ist = {"definition": i["d"], "name": i.get("n", "")}
        if bi:
            cx, cy, u, v = bi
            ist.update(x=cx, y=cy, quelle="Koerper %s aus viewer/detail/%s.json" % (body, i["d"]))
            if art == "kreis":
                ist["durchmesser"] = max(u, v)
            else:
                ist.update(breite=u, hoehe=v, drehung=yaw(i["m"]))
            if body_innen:
                bj = body_info(i, body_innen)
                if bj:
                    ist["innenmass"] = max(bj[2], bj[3])
        else:
            cx, cy = sx(i)
            ist.update(x=cx, y=cy, quelle="Ursprung der Instanz (Bezugspunkt = Mitte der Standflaeche, data/components/%s.json)" % i["d"])
            if ersatz:
                comp, key = ersatz
                if art == "kreis":
                    ist["durchmesser"] = comp_par(comp, key)
                else:
                    ist.update(breite=comp_par(comp, key[0]), hoehe=comp_par(comp, key[1]), drehung=yaw(i["m"]))
                ist["quelle"] += "; Mass aus Parameter %s" % (key,)
        z["ist"] = ist
        z["dx"], z["dy"] = ist["x"] - so["x_mm"], ist["y"] - so["y_mm"]
        z["abw_mitte"] = math.hypot(z["dx"], z["dy"])
        if z["abw_mitte"] > TOL_MITTE:
            z["fehler"].append("Mitte %.0f mm daneben (Grenze %.0f)" % (z["abw_mitte"], TOL_MITTE))
        # Mass
        if art == "kreis" and ist.get("durchmesser") and so["art"] == "kreis" and sid not in ("filterpumpe_1", "filterpumpe_2", "hauptpumpe_1", "hauptpumpe_2"):
            p = (ist["durchmesser"] - so["durchmesser_mm"]) / so["durchmesser_mm"]
            z["abw_mass_pct"] = 100 * p
            if abs(p) > TOL_MASS:
                z["fehler"].append("Durchmesser %.0f statt %.0f mm (%+.1f %%, Grenze 5 %%)" % (ist["durchmesser"], so["durchmesser_mm"], 100 * p))
            if ist.get("innenmass"):
                z["info"].append("Innen/Wasser %.0f mm (%+.1f %%)" % (ist["innenmass"], 100 * (ist["innenmass"] - so["durchmesser_mm"]) / so["durchmesser_mm"]))
        elif art == "rechteck" and ist.get("breite") and so["art"] == "rechteck" and sid in ("sump_1", "sump_2", "permakultur"):
            pb, ph = (ist["breite"] - so["breite_mm"]) / so["breite_mm"], (ist["hoehe"] - so["hoehe_mm"]) / so["hoehe_mm"]
            z["abw_mass_pct"] = 100 * max(abs(pb), abs(ph)) * (1 if max(abs(pb), abs(ph)) == abs(pb) and pb >= 0 or max(abs(pb), abs(ph)) == abs(ph) and ph >= 0 else -1)
            if abs(pb) > TOL_MASS or abs(ph) > TOL_MASS:
                z["fehler"].append("Rechteck %.0f x %.0f statt %.0f x %.0f mm" % (ist["breite"], ist["hoehe"], so["breite_mm"], so["hoehe_mm"]))
            dr = abs(((ist["drehung"] - so["drehung_grad"] + 90) % 180) - 90)
            z["abw_drehung"] = dr
            if dr > TOL_DREH:
                z["fehler"].append("Drehung %.0f Grad statt %.0f (Grenze %.0f)" % (ist["drehung"] % 180, so["drehung_grad"] % 180, TOL_DREH))
        else:
            z["info"].append("Mass nicht verglichen (Symbol der Quelle oder kein Fussabdruck im Export)")
        # Vorbau
        rist = math.hypot(ist["x"], ist["y"])
        z["r_ist"] = rist
        if rist > KUPPEL_R and not so["ausserhalb_kuppel"]:
            z["fehler"].append("steht ausserhalb der Kuppel (r %.0f), in der Quelle innen (r %.0f)" % (rist, so["r_mm"]))
        if so["ausserhalb_kuppel"]:
            z["info"].append("Quelle selbst: ausserhalb der Kuppel (Platzhalter, r %.0f)" % so["r_mm"])
    return zeilen


RING_DEF = {"nft_aussen": ("nft_tisch_aussen", None), "nft_mitte": ("nft_tisch_mitte", None), "nft_innen": ("nft_tisch_innen", None),
            "fd_aussen": ("ibc_beet_aussen_800", "Wanne"), "fd_mitte": ("ibc_beet_innen_933", "Wanne")}


def ringe_messen():
    erg = []
    for rid, rg in S["ringe"].items():
        defn, body = RING_DEF[rid]
        insts = [i for i in INSTANCES if i["d"] == defn]
        z = {"id": rid, "soll": rg, "n_ist": len(insts), "fehler": [], "segmente": [], "hulls": []}
        rr = []
        for i in insts:
            h = inst_hull(i)
            if body:
                b = body_info(i, body)
                cx, cy = b[0], b[1]
            else:
                cx, cy = centroid(h) if h else sx(i)
            rr.append(math.hypot(cx, cy))
            z["segmente"].append({"x": cx, "y": cy, "r": math.hypot(cx, cy), "az": az(cx, cy)})
            if h:
                z["hulls"].append(h)
        z["r_ist"] = sum(rr) / len(rr) if rr else None
        z["r_min"], z["r_max"] = (min(rr), max(rr)) if rr else (None, None)
        z["abw_radius"] = z["r_ist"] - rg["radius_mm"] if rr else None
        if len(insts) != rg["stueckzahl"]:
            z["fehler"].append("Stueckzahl %d statt %d" % (len(insts), rg["stueckzahl"]))
        if rr and abs(z["abw_radius"]) > TOL_MITTE:
            z["fehler"].append("Radius %.0f statt %.0f mm (%+.0f, Grenze %.0f)" % (z["r_ist"], rg["radius_mm"], z["abw_radius"], TOL_MITTE))
        inop = [s for s in z["segmente"] if abs(az_norm(s["az"] - rg["oeffnung_mitte_az_grad"])) < rg["oeffnung_grad"] / 2]
        z["in_oeffnung"] = len(inop)
        if inop:
            z["fehler"].append("%d Segment(e) in der Oeffnung (Az %.0f +- %.0f): Ist hat den Ring voll umlaufend" % (len(inop), rg["oeffnung_mitte_az_grad"], rg["oeffnung_grad"] / 2))
        erg.append(z)
    return erg


def tabelle(zeilen, ringe):
    out = []
    out.append("| Teil | Soll Mitte x/y (mm) | Ist Mitte x/y (mm) | Abweichung Mitte | Soll Mass | Ist Mass | Abweichung Mass | Urteil |")
    out.append("|---|---|---|---|---|---|---|---|")
    for z in zeilen:
        so, ist = z["soll"], z["ist"]
        sm = ("Ø %.0f" % so["durchmesser_mm"]) if so["art"] == "kreis" else ("%.0f x %.0f" % (so["breite_mm"], so["hoehe_mm"]) if so["art"] == "rechteck" else "Symbol")
        if ist is None:
            out.append("| %s | %.0f / %.0f | FEHLT | - | %s | - | - | FAIL |" % (z["id"], so["x_mm"], so["y_mm"], sm))
            continue
        im = ("Ø %.0f" % ist["durchmesser"]) if ist.get("durchmesser") and so["art"] == "kreis" else ("%.0f x %.0f" % (ist["breite"], ist["hoehe"]) if ist.get("breite") else "-")
        am = ("%+.1f %%" % z["abw_mass_pct"]) if "abw_mass_pct" in z else "-"
        out.append("| %s | %.0f / %.0f | %.0f / %.0f | %.0f mm | %s | %s | %s | %s |" % (z["id"], so["x_mm"], so["y_mm"], ist["x"], ist["y"], z["abw_mitte"], sm, im, am,
                                                                                           "FAIL" if z["fehler"] else "OK"))
    out.append("")
    out.append("| Ring | Soll Radius (mm) | Ist mittlerer Radius (min-max) | Abweichung | Soll Stueck | Ist Stueck | in der Oeffnung | Urteil |")
    out.append("|---|---|---|---|---|---|---|---|")
    for z in ringe:
        rg = z["soll"]
        out.append("| %s | %.1f | %s | %s | %d | %d | %d | %s |" % (z["id"], rg["radius_mm"], ("%.0f (%.0f-%.0f)" % (z["r_ist"], z["r_min"], z["r_max"])) if z["r_ist"] else "-",
                                                                 ("%+.0f" % z["abw_radius"]) if z["r_ist"] else "-", rg["stueckzahl"], z["n_ist"], z["in_oeffnung"], "FAIL" if z["fehler"] else "OK"))
    return out


# ---------------------------------------------------------------- Bild
def bild(zeilen, ringe, pfad):
    from PIL import Image, ImageDraw, ImageFont
    W = H = 2200
    R = 9300.0
    k = (W / 2 - 40) / R

    def P(x, y):
        return (W / 2 + x * k, H / 2 - y * k)
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 22)
        fb = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 30)
        fs = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    except OSError:
        f = fb = fs = ImageFont.load_default()
    SC, MC, ERR = (30, 90, 200), (235, 120, 20), (200, 20, 20)

    def kreis(cx, cy, r, col, w=3, n=180):
        pts = [P(cx + r * math.cos(2 * math.pi * t / n), cy + r * math.sin(2 * math.pi * t / n)) for t in range(n + 1)]
        d.line(pts, fill=col, width=w)

    def rect(cx, cy, b, h, yaw_deg, col, w=3):
        c, s = math.cos(math.radians(yaw_deg)), math.sin(math.radians(yaw_deg))
        pts = [P(cx + c * u - s * v, cy + s * u + c * v) for u, v in ((-b / 2, -h / 2), (b / 2, -h / 2), (b / 2, h / 2), (-b / 2, h / 2), (-b / 2, -h / 2))]
        d.line(pts, fill=col, width=w)

    def kreuz(x, y, col, r=9, w=3):
        a = P(x, y)
        d.line([(a[0] - r, a[1] - r), (a[0] + r, a[1] + r)], fill=col, width=w)
        d.line([(a[0] - r, a[1] + r), (a[0] + r, a[1] - r)], fill=col, width=w)

    kreis(0, 0, KUPPEL_R, (170, 170, 170), 3)
    for a in range(10):
        pass
    # Zehneck-Innenkante (Apothem wie check_walkways_voll) und Tuer-Achse
    ap = KUPPEL_R * math.cos(math.radians(18))
    ecken = [(KUPPEL_R * math.cos(math.radians(18 + 36 * t)), KUPPEL_R * math.sin(math.radians(18 + 36 * t))) for t in range(11)]
    d.line([P(*e) for e in ecken], fill=(215, 215, 215), width=2)
    ta = math.radians(-72)
    d.line([P(0, 0), P(KUPPEL_R * math.cos(ta), KUPPEL_R * math.sin(ta))], fill=(150, 150, 150), width=2)
    d.text(P(KUPPEL_R * math.cos(ta) * 0.97 + 150, KUPPEL_R * math.sin(ta) * 0.97), "Tuer Az -72", fill=(110, 110, 110), font=fs)
    # Anbauringe: Soll als Bogen, Ist als Segment-Huellen
    for z in ringe:
        rg = z["soll"]
        a0 = rg["oeffnung_mitte_az_grad"] + rg["oeffnung_grad"] / 2
        a1 = rg["oeffnung_mitte_az_grad"] - rg["oeffnung_grad"] / 2 + 360
        pts = [P(rg["radius_mm"] * math.cos(math.radians(a0 + (a1 - a0) * t / 200)), rg["radius_mm"] * math.sin(math.radians(a0 + (a1 - a0) * t / 200))) for t in range(201)]
        d.line(pts, fill=SC, width=5 if rg["art"] == "nft" else 3)
        for h in z["hulls"]:
            d.line([P(*p) for p in h + [h[0]]], fill=MC, width=2)
        for s in z["segmente"]:
            kreuz(s["x"], s["y"], MC, 5, 2)
        la = rg["oeffnung_mitte_az_grad"] + rg["oeffnung_grad"] / 2 + 6 + (0 if rg["art"] == "nft" else 4)
        d.text(P(rg["radius_mm"] * math.cos(math.radians(a0 + 8)), rg["radius_mm"] * math.sin(math.radians(a0 + 8))), z["id"], fill=SC, font=fs)
    # Teile
    for z in zeilen:
        so, ist = z["soll"], z["ist"]
        if not ("x_mm" in so):
            continue
        if so["art"] == "kreis":
            kreis(so["x_mm"], so["y_mm"], so["radius_mm"], SC, 4)
        elif so["art"] == "rechteck":
            rect(so["x_mm"], so["y_mm"], so["breite_mm"], so["hoehe_mm"], so["drehung_grad"], SC, 4)
        else:
            kreuz(so["x_mm"], so["y_mm"], SC, 10, 4)
        if ist:
            if so["art"] == "kreis" and ist.get("durchmesser") and z["id"] not in ("filterpumpe_1", "filterpumpe_2", "hauptpumpe_1", "hauptpumpe_2"):
                kreis(ist["x"], ist["y"], ist["durchmesser"] / 2, MC, 4)
            elif so["art"] == "rechteck" and ist.get("breite"):
                rect(ist["x"], ist["y"], ist["breite"], ist["hoehe"], ist["drehung"], MC, 4)
            else:
                kreuz(ist["x"], ist["y"], MC, 10, 4)
            if z["abw_mitte"] > 1:
                a, b = P(so["x_mm"], so["y_mm"]), P(ist["x"], ist["y"])
                d.line([a, b], fill=ERR if z["abw_mitte"] > TOL_MITTE else (60, 160, 60), width=2)
                mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
                d.text((mx + 4, my - 12), "%s %.0f" % (z["id"], z["abw_mitte"]), fill=ERR if z["abw_mitte"] > TOL_MITTE else (60, 160, 60), font=fs)
        else:
            d.text(P(so["x_mm"], so["y_mm"]), z["id"] + " FEHLT", fill=ERR, font=fs)
    # Kopf
    nfail = sum(1 for z in zeilen if z["fehler"]) + sum(1 for z in ringe if z["fehler"])
    d.text((30, 20), "Quelle (blau) gegen Modell (orange), Draufsicht, Norden oben", fill=(0, 0, 0), font=fb)
    d.text((30, 62), "Beschriftung: Teil und Mittelpunkt-Abweichung in mm (rot > 150 mm). Modellstand %s. Teile mit Verstoss: %d von %d." % (I["built"], nfail, len(zeilen) + len(ringe)), fill=(0, 0, 0), font=f)
    d.line([(30, 110), (90, 110)], fill=SC, width=5)
    d.text((100, 98), "Quelle (SVG #mainSvg, gedreht 18 Grad)", fill=SC, font=f)
    d.line([(520, 110), (580, 110)], fill=MC, width=5)
    d.text((590, 98), "Modell (viewer/instances.json + detail)", fill=MC, font=f)
    d.text((30, H - 40), "Massstab: Rahmen = %.0f m; Kuppel r 6000 (grau)" % (2 * R / 1000), fill=(90, 90, 90), font=fs)
    os.makedirs(os.path.dirname(pfad), exist_ok=True)
    im.save(pfad, optimize=True)


def main():
    zeilen, ringe = messen(), ringe_messen()
    tab = tabelle(zeilen, ringe)
    if "--md" in sys.argv:
        print("\n".join(tab))
        print()
    print("Modellstand: %s (%d Instanzen). Grenzen: Mitte %.0f mm, Mass %.0f %%, Drehung %.0f Grad." % (I["built"], len(INSTANCES), TOL_MITTE, 100 * TOL_MASS, TOL_DREH))
    bad = 0
    for z in zeilen + ringe:
        if z["fehler"]:
            bad += 1
            print("FAIL %-13s %s" % (z["id"], "; ".join(z["fehler"])))
        for t in z.get("info", []):
            if "--verbose" in sys.argv:
                print("     %-13s %s" % (z["id"], t))
    n = len(zeilen) + len(ringe)
    umf = [z for z in zeilen if z["in_umfang"]]
    print("Teile mit Verstoss: %d von %d (davon im Umfang: %d von %d); Mitte ueber 150 mm: %d; Mass ueber 5 %%: %d; ausserhalb der Kuppel, in der Quelle innen: %d" % (
        bad, n, sum(1 for z in umf if z["fehler"]), len(umf), sum(1 for z in zeilen if z.get("abw_mitte", 0) > TOL_MITTE),
        sum(1 for z in zeilen if abs(z.get("abw_mass_pct", 0)) > 100 * TOL_MASS), sum(1 for z in zeilen if any("ausserhalb der Kuppel (r" in e for e in z["fehler"]))))
    if "--ohne-bild" not in sys.argv:
        bild(zeilen, ringe, BILD)
        print("Bild:", os.path.relpath(BILD, ROOT))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
