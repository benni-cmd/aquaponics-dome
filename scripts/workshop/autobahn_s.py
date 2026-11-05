"""Werkstatt WA-S (docs/jobs/N-AUTOBAHN-V2.md Abschnitt 3): Schlauchteile der Wasserautobahn (Ring B2).
WA5 Schlauch-Fallleitung (fuenf Typen je Abnehmer-Zone), WA6 Schnellkupplung ID16/ID25, WA8 Rueckschlagventil d50,
WA9 Ruecklauf-Rinne am Tischbein, Bodenrinne mit Rost, Schlauch d50. Dazu der Schlauch-Baustein hose_path() (Polylinie mit
Biegeradius, Leitungsordnung v2 R14), den die Montage R2 (trassen_ring.py) fuer Fall- und Ruecklauf-Schlaeuche benutzt.
Z-Werte in Kommentaren relativ zum Innenboden (absolut = relativ + 400); Teile-KS siehe docs/parts/autobahn.md Abschnitt WA-S.
Aufruf: python -X utf8 scripts/workshop/autobahn_s.py [teil ...] [--json] [--render]
        Teile: kupplung rsv fall rinne bodenrinne schlauch50   (ohne Teil: alle)"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import sc
import leitung as L
import ring_b2 as R
import n_autobahn_rechnung as NR

DC = os.path.join(sc.ROOT, "designs", "components")
RENDER_DIR = os.path.join(sc.ROOT, "renders", "components", "autobahn")
MAT = {"SCH schwarz": (1.25, "#1c1c1c"),      # Schlauch PVC/EPDM schwarz, lichtdicht (D85, Leitungsordnung Art B/C)
       "LT pp": (0.91, "#3d6b9c"),            # PP blau (Kupplung, Regelhahn)
       "LT pvc": (1.4, "#8d9296"), "LT hahn": (1.4, "#2a5da8"), "LT stahl": (7.85, "#aeb4b8"), "LT epdm": (1.1, "#1a1a1a"),
       "RIN pp": (0.91, "#5a5f63"), "RIN v2a": (7.9, "#c9cdd0")}

def mats(b, names):
    for n in names:
        dens, col = MAT[n]
        b.add("material.create", name=n, density_g_cm3=dens, color=col)

# ------------------------------------------------------------------ Vektor-Helfer
def add(a, c): return [a[i] + c[i] for i in range(3)]
def sub(a, c): return [a[i] - c[i] for i in range(3)]
def mul(a, s): return [a[i] * s for i in range(3)]
def dot(a, c): return sum(a[i] * c[i] for i in range(3))
def cross(a, c): return [a[1] * c[2] - a[2] * c[1], a[2] * c[0] - a[0] * c[2], a[0] * c[1] - a[1] * c[0]]
def norm(a):
    n = math.sqrt(dot(a, a)); return [x / n for x in a]
def rot(v, k, ang):
    """Rodrigues: v um Einheitsachse k um ang (rad) drehen."""
    c, s = math.cos(ang), math.sin(ang)
    kv = cross(k, v); kd = dot(k, v)
    return [v[i] * c + kv[i] * s + k[i] * kd * (1 - c) for i in range(3)]
def r4(v): return [round(x, 9) for x in v]

def cyl_ax(b, nm, d, p0, u, ln, op="new", body=None, targets=None):
    kw = dict(diameter=d, height=ln, base=r4(p0), axis=r4(u), operation=op, name=nm)
    if op == "new":
        kw["body_name"] = body or nm
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)

def bx(b, nm, lx, wy, hz, c, op="new", body=None, targets=None):
    kw = dict(length=lx, width=wy, height=hz, center=r4(c), operation=op, name=nm)
    if op == "new":
        kw["body_name"] = body or nm
    else:
        kw["targets"] = targets
    b.add("solid.box", **kw)

# ------------------------------------------------------------------ Schlauch-Baustein (Leitungsordnung v2: Arten B, C, D; R14)
def hose_layout(pts, R):
    """Polylinie pts mit Ausrundung R an jeder inneren Ecke -> Segmente [('G', p0, p1) | ('B', A, B, C, k, u_in, th)].
    Fehler, wenn die Geraden fuer die Tangenten nicht reichen (R14: genug Gerade beidseits)."""
    segs, cur = [], list(pts[0])
    for i in range(1, len(pts) - 1):
        u_in = norm(sub(pts[i], pts[i - 1])); u_out = norm(sub(pts[i + 1], pts[i]))
        th = math.acos(max(-1.0, min(1.0, dot(u_in, u_out))))
        if th < 1e-6:
            continue
        t = R * math.tan(th / 2)
        A = sub(pts[i], mul(u_in, t)); B = add(pts[i], mul(u_out, t))
        if dot(sub(A, cur), u_in) < -1e-6:
            raise ValueError(f"Ecke {i}: Tangente {t:.1f} laenger als die Gerade davor")
        if math.dist(cur, A) > 1e-6:
            segs.append(("G", cur, A))
        w = norm(sub(u_out, mul(u_in, dot(u_out, u_in))))
        C = add(A, mul(w, R)); k = norm(cross(u_in, u_out))
        segs.append(("B", A, B, C, k, u_in, th))
        cur = B
    if dot(sub(pts[-1], cur), norm(sub(pts[-1], pts[-2]))) < -1e-6:
        raise ValueError("letzte Gerade kuerzer als die Tangente")
    if math.dist(cur, pts[-1]) > 1e-6:
        segs.append(("G", cur, list(pts[-1])))
    return segs

def hose_length(segs, R):
    return sum(math.dist(s[1], s[2]) if s[0] == "G" else R * s[6] for s in segs)

def hose_path(b, prefix, pts, R, ad, idd, mat="SCH schwarz"):
    """Schlauch als Koerperfolge <prefix>_G<n> (Gerade) und <prefix>_B<n> (Bogen R); Bohrung idd. Rueckgabe: Segmente, Laenge, Koerpernamen."""
    segs = hose_layout(pts, R); names = []
    for n, s in enumerate(segs, 1):
        if s[0] == "G":
            p0, p1 = s[1], s[2]; u = norm(sub(p1, p0)); ln = math.dist(p0, p1); nm = f"{prefix}_G{n}"
            cyl_ax(b, nm + "_R", ad, p0, u, ln, body=nm)
            cyl_ax(b, nm + "_Bohrung", idd, sub(p0, u), u, ln + 2, op="cut", targets=[nm])
        else:
            _, A, B, C, k, u_in, th = s; nm = f"{prefix}_B{n}"
            w = norm(sub(C, A))                                   # Sketch-Ebene: Normale u_in, x = w, y = u_in x w
            b.add("sketch.create", plane={"origin": r4(A), "x_dir": r4(w), "y_dir": r4(cross(u_in, w))}, name=nm + "_S")
            b.add("sketch.circle.center", center=[0, 0], radius=ad / 2)
            b.add("sketch.finish")
            b.add("solid.revolve", axis={"origin": r4(C), "dir": r4(k)}, angle=f"{math.degrees(th):.6f} deg", operation="new", body_name=nm, name=nm + "_Rev")
            # Bohrung: Werkzeug 1 Grad vor und nach dem Bogen (keine deckungsgleichen Stirnflaechen), dann combine cut
            d1 = math.radians(1.0)
            A1 = add(C, rot(sub(A, C), k, -d1)); n1 = rot(u_in, k, -d1); w1 = norm(sub(C, A1))
            b.add("sketch.create", plane={"origin": r4(A1), "x_dir": r4(w1), "y_dir": r4(cross(n1, w1))}, name=nm + "_SB")
            b.add("sketch.circle.center", center=[0, 0], radius=idd / 2)
            b.add("sketch.finish")
            b.add("solid.revolve", axis={"origin": r4(C), "dir": r4(k)}, angle=f"{math.degrees(th + 2 * d1):.6f} deg", operation="new", body_name=nm + "_W", name=nm + "_RevB")
            b.add("solid.combine", target=nm, tools=[nm + "_W"], operation="cut")
        names.append(nm)
    b.add("material.assign", bodies=names, material=mat)
    return segs, hose_length(segs, R), names

# ------------------------------------------------------------------ Schlauch-Masse (Recherche WA-S, docs/parts/autobahn.md; [A] bis belegt)
HOSE = {16: dict(ad=24.0, r_hersteller=110.0), 25: dict(ad=33.0, r_hersteller=150.0), 50: dict(ad=60.0, r_hersteller=270.0)}
def hose_R(idd):
    """Biegeradius nach R14: >= 6 x Aussendurchmesser und >= Herstellerwert; auf 5 mm aufgerundet."""
    h = HOSE[idd]; return 5 * math.ceil(max(6 * h["ad"], h["r_hersteller"]) / 5)

# ------------------------------------------------------------------ WA6 Schnellkupplung ID16 / ID25 (Kupplungsdose + Stecker mit Schlauchtuellen, PP)
SK = {16: dict(tl=30.0, rib=1.0, dose_d=36.0, dose_l=45.0, nase_d=22.0, nase_l=25.0, st_d=30.0, st_l=20.0, bore=11.0),
      25: dict(tl=40.0, rib=1.5, dose_d=50.0, dose_l=60.0, nase_d=32.0, nase_l=32.0, st_d=42.0, st_l=25.0, bore=19.0)}

def sk_len(idd):
    k = SK[idd]; return 2 * k["tl"] + k["dose_l"] + k["st_l"]

def add_kupplung(b, prefix, p0, u, idd, wulst=True):
    """Kupplung gekuppelt entlang u ab p0 (Ende Tuelle Dose = Port A): Tuelle | Dose | Stecker | Tuelle. Koerper <prefix>_Dose, <prefix>_Stecker."""
    k = SK[idd]; tl = k["tl"]
    nd, ns = prefix + "_Dose", prefix + "_Stecker"
    cyl_ax(b, nd + "_Tuelle", idd, p0, u, tl, body=nd)
    if wulst:                                          # Haltewulst nur am Einzelteil; in der Baugruppe steckt die Tuelle im Schlauch (Schlauch dehnt sich, nicht modelliert)
        cyl_ax(b, nd + "_Wulst", idd + 2 * k["rib"], add(p0, mul(u, 4)), u, 4, op="join", targets=[nd])
    cyl_ax(b, nd + "_Koerper", k["dose_d"], add(p0, mul(u, tl)), u, k["dose_l"], op="join", targets=[nd])
    cyl_ax(b, nd + "_Aufnahme", k["nase_d"], add(p0, mul(u, tl + k["dose_l"] - k["nase_l"])), u, k["nase_l"] + 1, op="cut", targets=[nd])
    cyl_ax(b, nd + "_Bohrung", k["bore"], sub(p0, u), u, tl + k["dose_l"] + 2, op="cut", targets=[nd])
    z1 = tl + k["dose_l"]
    cyl_ax(b, ns + "_Nase", k["nase_d"], add(p0, mul(u, z1 - k["nase_l"])), u, k["nase_l"], body=ns)
    cyl_ax(b, ns + "_Koerper", k["st_d"], add(p0, mul(u, z1)), u, k["st_l"], op="join", targets=[ns])
    cyl_ax(b, ns + "_Tuelle", idd, add(p0, mul(u, z1 + k["st_l"])), u, tl, op="join", targets=[ns])
    if wulst:
        cyl_ax(b, ns + "_Wulst", idd + 2 * k["rib"], add(p0, mul(u, z1 + k["st_l"] + tl - 8)), u, 4, op="join", targets=[ns])
    cyl_ax(b, ns + "_Bohrung", k["bore"], add(p0, mul(u, z1 - k["nase_l"] - 1)), u, k["nase_l"] + k["st_l"] + tl + 2, op="cut", targets=[ns])
    b.add("material.assign", bodies=[nd, ns], material="LT pp")
    return [nd, ns], add(p0, mul(u, sk_len(idd)))

def kupplung(idd):
    b = sc.Build(); nm = f"WA6_Schnellkupplung_ID{idd}"
    mats(b, ["LT pp"]); b.add("component.create", name=nm, grounded=True)
    for kk, v in SK[idd].items():
        b.add("parameters.add", name=kk, expression=f"{v} mm")
    add_kupplung(b, "Kupplung", [0, 0, 0], [0, 0, 1], idd)
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=f"WA6-{idd}", revision="A", properties={"Werkstoff": "PP lebensmittelecht (EU 10/2011), Dichtung EPDM/NBR lebensmittelecht"},
          description=f"Schnellkupplung fuer Schlauch ID{idd}: Kupplungsdose und Stecker mit Schlauchtuellen, gekuppelt {sk_len(idd):g} lang; Abnehmer ohne Werkzeug abtrennbar")
    return b, nm

def kupplung_ports(idd):
    return [("A (Tuelle Dose, Zulauf)", (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), "Schlauchtuelle", f"ID{idd}"),
            ("B (Tuelle Stecker, Abgang)", (0.0, 0.0, sk_len(idd)), (0.0, 0.0, 1.0), "Schlauchtuelle", f"ID{idd}")]

# ------------------------------------------------------------------ WA8 Rueckschlagventil d50 (Kugel-Rueckschlagventil PVC-U, Klebemuffen)
RSV = dict(d=50, L=172.0, ob=92.0, kugel_d=56.0)     # Baulaenge und Gehaeuse: Recherche WA-S (Herstellerblatt), bis dahin [A]

def rsv_geom():
    p = RSV; d = p["d"]; dp = L.DEPTH[d]
    return dict(dp=dp, of=L.od_f(d), wi=d - 2 * L.wall_p(d), lb=p["L"] - 2 * dp)

def rueckschlagventil_d50():
    p, g = RSV, rsv_geom(); d = p["d"]
    b = sc.Build(); nm = "WA8_Rueckschlagventil_d50_A-B"
    mats(b, ["LT hahn"]); b.add("component.create", name=nm, grounded=True)
    for kk in ("L", "ob"):
        b.add("parameters.add", name=kk, expression=f"{p[kk]} mm")
    cyl_ax(b, "Stutzen_A", g["of"], [0, 0, 0], [0, 0, 1], g["dp"], body="Rueckschlagventil")
    cyl_ax(b, "Gehaeuse", p["ob"], [0, 0, g["dp"]], [0, 0, 1], g["lb"], op="join", targets=["Rueckschlagventil"])
    cyl_ax(b, "Stutzen_B", g["of"], [0, 0, p["L"] - g["dp"]], [0, 0, 1], g["dp"], op="join", targets=["Rueckschlagventil"])
    cyl_ax(b, "Muffe_A", d, [0, 0, -1], [0, 0, 1], g["dp"] + 1, op="cut", targets=["Rueckschlagventil"])
    cyl_ax(b, "Muffe_B", d, [0, 0, p["L"] - g["dp"]], [0, 0, 1], g["dp"] + 1, op="cut", targets=["Rueckschlagventil"])
    cyl_ax(b, "Kugelraum", p["kugel_d"] + 4, [0, 0, g["dp"] + 10], [0, 0, 1], g["lb"] - 20, op="cut", targets=["Rueckschlagventil"])
    cyl_ax(b, "Durchgang", g["wi"], [0, 0, -1], [0, 0, 1], p["L"] + 2, op="cut", targets=["Rueckschlagventil"])
    b.add("material.assign", bodies=["Rueckschlagventil"], material="LT hahn")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="WA8", revision="A", properties={"Werkstoff": "PVC-U, Dichtung EPDM (Trinkwasser), Kugel PVC/PE"},
          description=f"Kugel-Rueckschlagventil PVC-U d50 (DN40), Klebemuffen, Baulaenge {p['L']:g}, Gehaeuse {p['ob']:g}; Durchfluss nur A nach B (+Z); hinter jedem Booster, Einbau waagerecht oder senkrecht aufwaerts")
    return b, nm

def rsv_ports():
    return [("A (Zulauf, Booster)", (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), "Muffe", L.DN[50]), ("B (Abgang, Steigleitung)", (0.0, 0.0, RSV["L"]), (0.0, 0.0, 1.0), "Muffe", L.DN[50])]

# ------------------------------------------------------------------ WA5 Schlauch-Fallleitung
# KS: Ursprung = Abgang des Ring-Abzweigs (Stirnflaeche Muffe B des Kugelhahns, ring_b2 T97). +X = radial zum Abnehmer (innen oder aussen,
# die Montage dreht), Z hoch. Typ 'fall' (Mittelzone): Abzweig wie T97 nach unten, Schlauch faellt senkrecht. Typ 'ausleger': Abzweig um die
# Ringachse 90 Grad gedreht, Abgang waagerecht radial auf Ring-Achshoehe; Schlauch liegt auf dem Ausleger bis zu dessen Ende, faellt dann frei.
Z_ACHSE = NR.Z_RING_ACHSE                    # 2145 rel
Z_UK = NR.Z_RING_UK                          # 2100 rel
R_ECKE = NR.AP["mitte"] / math.cos(NR.HALB)  # 3446
R_INLET = {z: NR.AP[z] / math.cos(NR.HALB) for z in NR.AP}
FT = dict(kragen=10.0, tuelle={16: 35.0, 25: 45.0}, wulst=1.0,          # Tuelle oben: Klebezapfen d32/d40 in Muffe B des Hahns, Kragen, Schlauchtuelle
          hahn_lb={16: 60.0, 25: 75.0}, hahn_ob={16: 40.0, 25: 52.0}, hebel=90.0,      # Regelhahn PP mit zwei Tuellen (Kugelhahn fuer Schlauch)
          anschl_l={"tisch": 40.0, "beet": 45.0}, anschl_od={"tisch": 33.0, "beet": 34.0},  # Endstueck: Tuelle + Klebemuffe d25 (Tisch) bzw. Klemmverbinder d20 PE (Beet)
          z_hahn={"tisch": 1500.0, "beet": 1150.0})                                    # Regelhahn-Mitte rel (Greifhoehe [A])
TYPES = {
    "id16_mitte":  dict(art="tisch", zone="mitte",  idd=16, dk=32, mode="fall"),
    "id16_innen":  dict(art="tisch", zone="innen",  idd=16, dk=32, mode="ausleger"),
    "id16_aussen": dict(art="tisch", zone="aussen", idd=16, dk=32, mode="ausleger"),
    "id25_mitte":  dict(art="beet",  zone="mitte",  idd=25, dk=40, mode="fall"),
    "id25_aussen": dict(art="beet",  zone="aussen", idd=25, dk=40, mode="ausleger"),
}
ANSCHLUSS = {"tisch": ("Muffe d25 (Zulaufverteiler T22)", 25), "beet": ("Klemmverbinder PE d20 (Tropfrohr T30)", 20)}

def abz_len(dk):
    return -R.ab_kette(dk)[-1][4]                     # T-Achse bis Abgang: 362,375 (d40) / 350,375 (d32)

def rechnung_len(t):
    """Laenge je Abnehmer nach n_autobahn_rechnung.py Abschnitt 3: waagerecht + (Ring-Achse - Ziel) + Schlaufe."""
    T = TYPES[t]; horiz = abs(R_INLET[T["zone"]] - R_ECKE)
    z_ziel = NR.Z_BEET_ZULAUF if T["art"] == "beet" else NR.Z_TISCH_ZULAUF
    return horiz + (Z_ACHSE - z_ziel) + NR.SCHLAUFE, horiz, z_ziel

def fall_geom(t):
    """Lage aller Glieder im Teile-KS; Endstueck so lang, dass 300 mm Schlaufe ueber dem kuerzesten Weg bleiben (Bogenverkuerzung ausgeglichen)."""
    T = TYPES[t]; idd, dk, art = T["idd"], T["dk"], T["art"]
    soll, horiz, z_ziel = rechnung_len(t)
    al = abz_len(dk); Rb = hose_R(idd); ad = HOSE[idd]["ad"]; tl = FT["tuelle"][idd]
    fall = T["mode"] == "fall"
    z0 = Z_ACHSE - (al if fall else 0.0)                 # Ursprung rel
    x_v = 0.0 if fall else horiz - al                    # x der senkrechten Fallstrecke (Auslegerende bzw. unter dem Abzweig)
    zl = lambda zr: zr - z0                              # rel -> lokal
    u0 = [0.0, 0.0, -1.0] if fall else [1.0, 0.0, 0.0]
    kr = FT["kragen"]
    tuelle_ende = mul(u0, kr)                            # Schlauch 1 beginnt am Kragen und deckt die Tuelle
    hb, hl = FT["hahn_ob"][idd], FT["hahn_lb"][idd]
    z_h_top = zl(FT["z_hahn"][art]) + hl / 2; z_h_bot = z_h_top - hl
    s1 = [tuelle_ende, [x_v, 0.0, z_h_top]] if fall else [tuelle_ende, [x_v, 0.0, 0.0], [x_v, 0.0, z_h_top]]
    z_k_top = z_h_bot - (2 * tl + 20)                    # Zwischenschlauch Hahn -> Kupplung deckt beide Tuellen + 20
    z_k_bot = z_k_top - (SK[idd]["dose_l"] + SK[idd]["st_l"])
    # Kupplung: Tuellen ragen in die Schlaeuche; Koerper von z_k_top bis z_k_bot
    end_dir = [0.0, 1.0, 0.0]                            # waagerechter Anschluss entlang +Y (Port Tisch/Beet waagerecht, Montage dreht um Z)
    zz = zl(z_ziel); la = FT["anschl_l"][art]
    base = abs(z_k_bot - zz) + Rb                        # kuerzester Weg Kupplung -> Port ohne Schlaufe (Ecke + Tangente)
    # Wegsumme bis zur Ecke unten; Schlaufe: Endstueck waagerecht = SCHLAUFE + Bogenverkuerzungen
    n_b = 1 if fall else 2
    loss = n_b * Rb * (2 - math.pi / 2)
    a = NR.SCHLAUFE + loss                               # Ecke unten bis Port (inkl. Endstueck la)
    corner = [x_v, 0.0, zz]
    port = add(corner, mul(end_dir, a))
    s3 = [[x_v, 0.0, z_k_bot - tl * 0 ], corner, sub(port, mul(end_dir, la))]
    s3[0] = [x_v, 0.0, z_k_bot]
    g = dict(T=T, idd=idd, dk=dk, art=art, soll=soll, horiz=horiz, z_ziel=z_ziel, al=al, Rb=Rb, ad=ad, tl=tl, z0=z0, x_v=x_v, u0=u0,
             s1=s1, z_h_top=z_h_top, z_h_bot=z_h_bot, z_k_top=z_k_top, z_k_bot=z_k_bot, s2=[[x_v, 0.0, z_h_bot], [x_v, 0.0, z_k_top]], s3=s3,
             port=port, end_dir=end_dir, la=la, a=a, loss=loss, fall=fall, ring_achse=[0.0, 0.0, al] if fall else [-al, 0.0, 0.0])
    return g

def fallleitung(t):
    g = fall_geom(t); idd, art = g["idd"], g["art"]
    b = sc.Build(); nm = f"WA5_Schlauch_Fall_{t}"
    mats(b, ["SCH schwarz", "LT pp", "LT pvc"]); b.add("component.create", name=nm, grounded=True)
    for kk in ("horiz", "z_ziel", "Rb", "a"):
        b.add("parameters.add", name=kk, expression=f"{round(g[kk], 3)} mm")
    u0, dk, tl, kr = g["u0"], g["dk"], g["tl"], FT["kragen"]
    # Tuelle oben (PVC-U): Klebezapfen d32/d40 steckt in Muffe B des Abzweig-Hahns (hinter dem Ursprung), Kragen, Schlauchtuelle
    cyl_ax(b, "Tuelle_oben_Zapfen", dk, mul(u0, -L.DEPTH[dk]), u0, L.DEPTH[dk], body="Tuelle_oben")
    cyl_ax(b, "Tuelle_oben_Kragen", L.od_f(dk), [0, 0, 0], u0, kr, op="join", targets=["Tuelle_oben"])
    cyl_ax(b, "Tuelle_oben_Tuelle", idd, mul(u0, kr), u0, tl, op="join", targets=["Tuelle_oben"])
    cyl_ax(b, "Tuelle_oben_Bohrung", idd - 5, mul(u0, -L.DEPTH[dk] - 1), u0, L.DEPTH[dk] + kr + tl + 2, op="cut", targets=["Tuelle_oben"])
    b.add("material.assign", bodies=["Tuelle_oben"], material="LT pvc")
    # Schlauch 1: Ausleger (waagerecht) + Bogen + freier Fall bis Regelhahn
    _, l1, n1 = hose_path(b, "Schlauch_1", g["s1"], g["Rb"], g["ad"], idd)
    # Regelhahn (PP, Kugelhahn mit zwei Schlauchtuellen), Hebel +Y
    xv = g["x_v"]; zt, zb = g["z_h_top"], g["z_h_bot"]; dn = [0, 0, -1]
    cyl_ax(b, "Hahn_Tuelle_oben", idd, [xv, 0, zt + tl], dn, tl, body="Regelhahn")
    cyl_ax(b, "Hahn_Gehaeuse", FT["hahn_ob"][idd], [xv, 0, zt], dn, FT["hahn_lb"][idd], op="join", targets=["Regelhahn"])
    cyl_ax(b, "Hahn_Tuelle_unten", idd, [xv, 0, zb], dn, tl, op="join", targets=["Regelhahn"])
    bx(b, "Hahn_Hebel", 10, FT["hebel"], 12, [xv, FT["hahn_ob"][idd] / 2 + FT["hebel"] / 2 - 2, (zt + zb) / 2], op="join", targets=["Regelhahn"])
    cyl_ax(b, "Hahn_Bohrung", idd - 5, [xv, 0, zt + tl + 1], dn, FT["hahn_lb"][idd] + 2 * tl + 2, op="cut", targets=["Regelhahn"])
    b.add("material.assign", bodies=["Regelhahn"], material="LT pp")
    # Zwischenschlauch und Schnellkupplung
    _, l2, n2 = hose_path(b, "Schlauch_2", g["s2"], g["Rb"], g["ad"], idd)
    kb, _ = add_kupplung(b, "Kupplung", [xv, 0, g["z_k_top"] + tl], dn, idd, wulst=False)
    # Schlauch 3: freier Fall bis Ziel-Hoehe, Bogen, waagerecht zum Anschluss
    _, l3, n3 = hose_path(b, "Schlauch_3", [[xv, 0, g["z_k_bot"]]] + g["s3"][1:], g["Rb"], g["ad"], idd)
    # Endstueck: Tuelle + Kragen + Muffe (Tisch d25) bzw. Klemmverbinder d20 (Beet), Port an der Stirnflaeche
    ed, la = g["end_dir"], g["la"]; p_e0 = sub(g["port"], mul(ed, la)); dz_a = ANSCHLUSS[art][1]
    cyl_ax(b, "Anschluss_Tuelle", idd, sub(p_e0, mul(ed, tl)), ed, tl, body="Anschluss")
    cyl_ax(b, "Anschluss_Koerper", FT["anschl_od"][art], p_e0, ed, la, op="join", targets=["Anschluss"])
    cyl_ax(b, "Anschluss_Muffe", dz_a, add(p_e0, mul(ed, la - 22)), ed, 23, op="cut", targets=["Anschluss"])
    cyl_ax(b, "Anschluss_Bohrung", idd - 5, sub(p_e0, mul(ed, tl + 1)), ed, tl + la + 2, op="cut", targets=["Anschluss"])
    b.add("material.assign", bodies=["Anschluss"], material="LT pvc" if art == "tisch" else "LT pp")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=f"WA5-{t}", revision="A",
          properties={"Werkstoff": "Schlauch lebensmittelecht schwarz (lichtdicht, UV-fest), Tuellen PVC-U/PP, Regelhahn und Kupplung PP lebensmittelecht"},
          description=f"Schlauch-Fallleitung {t}: Tuelle d{dk} -> Schlauch ID{idd} ({'Ausleger + freier Fall' if not g['fall'] else 'freier Fall'}) -> Regelhahn auf Z {FT['z_hahn'][art]:g} rel -> Schnellkupplung -> {ANSCHLUSS[art][0]}; Biegeradius {g['Rb']:g}")
    g.update(hose_names=n1 + n2 + n3, hose_len=[l1, l2, l3])
    return b, nm, g

def fall_ports(t):
    g = fall_geom(t); u0 = g["u0"]
    return [("Oben (Muffe B Abzweig-Hahn)", (0.0, 0.0, 0.0), tuple(mul(u0, -1)), "Klebezapfen", f"d{g['dk']}"),
            ("Unten (Abnehmer)", tuple(round(v, 3) for v in g["port"]), tuple(g["end_dir"]), "Muffe" if g["art"] == "tisch" else "Klemmverbinder", f"d{ANSCHLUSS[g['art']][1]}")]

# ------------------------------------------------------------------ WA9 Ruecklauf: Schlauch d50, Tragrinne am Tischbein, Bodenrinne mit Rost
S50_L = 1000.0
def schlauch50():
    h = HOSE[50]; b = sc.Build(); nm = "WA9_Schlauch_d50"
    mats(b, ["SCH schwarz"]); b.add("component.create", name=nm, grounded=True)
    b.add("parameters.add", name="laenge", expression=f"{S50_L} mm")
    cyl_ax(b, "S_R", h["ad"], [0, 0, 0], [1, 0, 0], S50_L, body="Schlauch")
    cyl_ax(b, "Bohrung", 50, [-1, 0, 0], [1, 0, 0], S50_L + 2, op="cut", targets=["Schlauch"])
    b.add("material.assign", bodies=["Schlauch"], material="SCH schwarz")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="WA9-S50", revision="A", properties={"Werkstoff": "PVC-Spiralschlauch glatt innen, lebensmittelecht (EU 10/2011), schwarz/lichtdicht"},
          description=f"Ruecklauf-Schlauch ID50 / AD{h['ad']:g} (Art C), Meterware; Stueck {S50_L:g} als Muster; Biegeradius {hose_R(50):g}")
    return b, nm

# Tragrinne: Kabelrinne 100 breit (innen), Seitenhoehe 60, Blech 1,5 [A bis Recherche]; zwei Konsolen mit Langloch am Tischbein 40x40
RR = dict(L=2000.0, b_innen=100.0, h=60.0, t=1.5, kons_abstand=1600.0, kons_platte=(5.0, 80.0, 160.0), langloch=60.0, arm_l=150.0, arm_b=40.0, arm_t=4.0,
          bein=40.0, stuetz_max=1500.0)

def rr_geom():
    p = RR; bo = p["b_innen"] + 2 * p["t"]
    z_rinne = 0.0                                          # Rinnenboden unten bei z 0 (KS: Rinnenmitte unten), Rinne entlang X
    return dict(bo=bo, z_arm_top=z_rinne, xs=[-p["kons_abstand"] / 2, p["kons_abstand"] / 2],
                y_bein=-(bo / 2 + 10 + p["bein"] / 2))       # Tischbein-Achse 10 mm neben der Rinne

def ruecklauf_rinne():
    p, g = RR, rr_geom(); b = sc.Build(); nm = "WA9_Ruecklauf_Rinne"
    mats(b, ["RIN v2a", "LT stahl"]); b.add("component.create", name=nm, grounded=True)
    for kk in ("L", "b_innen", "h", "t", "kons_abstand", "langloch"):
        b.add("parameters.add", name=kk, expression=f"{p[kk]} mm")
    bo = g["bo"]
    bx(b, "Rinne_R", p["L"], bo, p["h"], [0, 0, p["h"] / 2], body="Rinne")
    bx(b, "Rinne_Innen", p["L"] + 2, p["b_innen"], p["h"], [0, 0, p["t"] + p["h"] / 2], op="cut", targets=["Rinne"])
    b.add("material.assign", bodies=["Rinne"], material="RIN v2a")
    kt, kw, kh = p["kons_platte"]
    for i, x in enumerate(g["xs"], 1):
        k = f"Konsole_{i}"
        yb = g["y_bein"]; yp = yb + p["bein"] / 2 + kt / 2      # Klemmplatte liegt an der Beinflaeche zur Rinne
        # Arm (Flachstahl 40 x 4) unter der Rinne, von der Klemmplatte bis unter die Rinnen-Aussenkante
        bx(b, k + "_Arm", p["arm_b"], (bo / 2 + 5) - (yp + kt / 2) + bo / 2 + 5, p["arm_t"], [x, ((yp + kt / 2) + (bo / 2 + 5)) / 2, -p["arm_t"] / 2], body=k)
        bx(b, k + "_Platte", kw, kt, kh, [x, yp, -kh / 2 + 20], op="join", targets=[k])
        bx(b, k + "_Langloch", 10, kt + 2, p["langloch"], [x, yp, -kh / 2 + 20], op="cut", targets=[k])
    b.add("material.assign", bodies=["Konsole_1", "Konsole_2"], material="LT stahl")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="WA9-RR", revision="A", properties={"Werkstoff": "Kabelrinne Edelstahl/verzinkt, Konsolen Stahl verzinkt"},
          description=f"Ruecklauf-Tragrinne {p['b_innen']:g} x {p['h']:g}, Element {p['L']:g}, zwei Konsolen mit Langloch {p['langloch']:g} am Tischbein 40x40 (Gefaelle einstellbar); Schlauch d50 liegt auf (R6 aufliegend)")
    return b, nm

# Bodenrinne mit Gitterrost, buendig im Boden (Rost-Oberkante = Innenboden z 0), Laenge = Gangbreite + 2 x 300
BR = dict(b_innen=100.0, h_innen=150.0, wand=10.0, boden=12.0, rost_t=20.0, falz=8.0, rost_spalt=2.0, gang={"A": 600.0, "B": 500.0}, ueber=300.0)

def br_len(gang): return BR["gang"][gang] + 2 * BR["ueber"]

def bodenrinne(gang):
    p = BR; Lr = br_len(gang); b = sc.Build(); nm = f"WA9_Bodenrinne_Rost_Gang{gang}"
    mats(b, ["RIN pp", "LT stahl"]); b.add("component.create", name=nm, grounded=True)
    for kk in ("b_innen", "h_innen", "rost_t"):
        b.add("parameters.add", name=kk, expression=f"{p[kk]} mm")
    b.add("parameters.add", name="laenge", expression=f"{Lr} mm")
    bo = p["b_innen"] + 2 * p["wand"]; ht = p["h_innen"] + p["boden"]
    bx(b, "Koerper_R", Lr, bo, ht, [0, 0, -ht / 2], body="Rinnenkoerper")
    bx(b, "Koerper_Innen", Lr + 2, p["b_innen"], p["h_innen"], [0, 0, -p["h_innen"] / 2], op="cut", targets=["Rinnenkoerper"])
    bx(b, "Koerper_Falz", Lr + 2, p["b_innen"] + 2 * p["falz"], p["rost_t"], [0, 0, -p["rost_t"] / 2], op="cut", targets=["Rinnenkoerper"])
    bw = p["b_innen"] + 2 * p["falz"] - 2 * p["rost_spalt"]
    bx(b, "Rost_R", Lr - 2 * p["rost_spalt"], bw, p["rost_t"], [0, 0, -p["rost_t"] / 2], body="Gitterrost")
    n_sl = int((Lr - 40) // 30)
    for i in range(n_sl):                                   # Maschen als Querschlitze 20 x (b - 20)
        bx(b, f"Rost_Masche_{i + 1}", 20, bw - 20, p["rost_t"] + 2, [-(Lr - 40) / 2 + 15 + i * 30, 0, -p["rost_t"] / 2], op="cut", targets=["Gitterrost"])
    b.add("material.assign", bodies=["Rinnenkoerper"], material="RIN pp")
    b.add("material.assign", bodies=["Gitterrost"], material="LT stahl")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=f"WA9-BR-{gang}", revision="A", properties={"Werkstoff": "Rinnenkoerper PP/PE, Gitterrost Stahl verzinkt oder Edelstahl, Klasse A15/B125"},
          description=f"Bodenrinne NW{p['b_innen']:g} mit Gitterrost fuer Gang {gang} ({p['gang'][gang]:g} mm), Laenge {Lr:g}, Rost buendig mit dem Innenboden; Schlauch d50 liegt mit Gefaelle darin (offen, begehbar statt vergraben)")
    return b, nm

# ------------------------------------------------------------------ Register, Speichern, Teiledaten, Bilder
def jobs():
    out = [("kupplung", f"lt_schnellkupplung_id{i}", (lambda i=i: kupplung(i))) for i in (16, 25)]
    out.append(("rsv", "lt_rueckschlagventil_d50", rueckschlagventil_d50))
    out += [("fall", f"schlauch_fall_{t}", (lambda t=t: fallleitung(t))) for t in TYPES]
    out.append(("rinne", "ruecklauf_rinne", ruecklauf_rinne))
    out += [("bodenrinne", f"bodenrinne_rost_gang{gg.lower()}", (lambda gg=gg: bodenrinne(gg))) for gg in ("A", "B")]
    out.append(("schlauch50", "lt_schlauch_d50", schlauch50))
    return out

RENDER = {"lt_schnellkupplung_id16": dict(yaw=0.8, pitch=0.3, zoom=1.8, section="XZ"), "lt_schnellkupplung_id25": dict(yaw=0.8, pitch=0.3, zoom=1.8, section="XZ"),
          "lt_rueckschlagventil_d50": dict(yaw=0.8, pitch=0.2, zoom=1.8, section="XZ"), "ruecklauf_rinne": dict(yaw=0.6, pitch=0.35, zoom=0.9),
          "bodenrinne_rost_ganga": dict(yaw=0.6, pitch=0.6, zoom=1.0), "bodenrinne_rost_gangb": dict(yaw=0.6, pitch=0.6, zoom=1.0), "lt_schlauch_d50": dict(yaw=0.6, pitch=0.3, zoom=1.0)}

def render(fname, yaw=0.9, pitch=0.25, zoom=1.0, section=None):
    path = os.path.join(DC, fname + ".sc")
    mn, mx = sc.bbox_all(sc.evaluate(path))
    tgt = [(a + c) / 2 for a, c in zip(mn, mx)]
    out = os.path.join(RENDER_DIR, fname + ".png")
    sc.snapshot(path, out, tgt, yaw, pitch, math.dist(mn, mx) * zoom * 1.4, w=900, h=900, section=section)
    return out

def pr(v): return [round(float(x), 3) for x in v]

def json_entries():
    E = {}
    def ent(fname, **kw):
        E[fname] = kw
    for i in (16, 25):
        ent(f"lt_schnellkupplung_id{i}", teil="WA6", teilenummer=f"WA6-{i}", schlauch_id=i, laenge_gekuppelt=sk_len(i), masse=SK[i],
            werkstoff="PP lebensmittelecht, Dichtung EPDM/NBR lebensmittelecht (D85)", ports=[dict(name=n, lage=pr(p), richtung=pr(d), art=a, dn=dn) for n, p, d, a, dn in kupplung_ports(i)],
            stueckzahl=38 if i == 16 else 0, bemerkung="ID16: 24 Tische; ID25: 14 Beete (zusammen 38 Abnehmer, Blatt 2.4)" if i == 16 else "14 Beete")
    E["lt_schnellkupplung_id16"]["stueckzahl"] = 24; E["lt_schnellkupplung_id25"]["stueckzahl"] = 14
    ent("lt_rueckschlagventil_d50", teil="WA8", teilenummer="WA8", d=50, laenge=RSV["L"], gehaeuse_aussen_d=RSV["ob"], muffentiefe=L.DEPTH[50], stueckzahl=4,
        werkstoff="PVC-U, Dichtung EPDM Trinkwasser (D85)", einbaulage="waagerecht oder senkrecht aufwaerts", ports=[dict(name=n, lage=pr(p), richtung=pr(d), art=a, dn=dn) for n, p, d, a, dn in rsv_ports()])
    for t in TYPES:
        g = fall_geom(t)
        ent(f"schlauch_fall_{t}", teil="WA5", typ=t, art=g["art"], zone=g["T"]["zone"], schlauch_id=g["idd"], schlauch_ad=g["ad"], biegeradius=g["Rb"], abzweig=f"ring_abzweig_d{g['dk']}",
            abzweig_lage="nach unten (wie T97)" if g["fall"] else "um die Ringachse 90 Grad gedreht, Abgang waagerecht radial",
            ursprung_z_rel=round(g["z0"], 3), regelhahn_z_rel=FT["z_hahn"][g["art"]], ziel_z_rel=g["z_ziel"], waagerecht_ab_ringachse=round(g["horiz"], 1),
            laenge_rechnung=round(g["soll"], 1), endstueck_waagerecht=round(g["a"], 1),
            ports=[dict(name=n, lage=pr(p), richtung=pr(d), art=a, dn=dn) for n, p, d, a, dn in fall_ports(t)], pfad_schlauch_1=[pr(p) for p in g["s1"]], pfad_schlauch_3=[pr(p) for p in g["s3"]])
    ent("ruecklauf_rinne", teil="WA9", element_laenge=RR["L"], breite_innen=RR["b_innen"], hoehe=RR["h"], konsolen_abstand=RR["kons_abstand"], langloch=RR["langloch"],
        gefaelle_max_pct=round(RR["langloch"] / RR["kons_abstand"] * 100, 2), werkstoff="Kabelrinne Edelstahl 1.4301 oder verzinkt; Wasserkontakt nur ueber den Schlauch")
    for gg in ("A", "B"):
        ent(f"bodenrinne_rost_gang{gg.lower()}", teil="WA9", gang=gg, gangbreite=BR["gang"][gg], laenge=br_len(gg), breite_innen=BR["b_innen"], tiefe_innen=BR["h_innen"], rost_dicke=BR["rost_t"],
            stueckzahl=4 if gg == "A" else 2, werkstoff="PP/PE-Rinne, Rost verzinkt/Edelstahl; Wasserkontakt nur ueber den Schlauch")
    ent("lt_schlauch_d50", teil="WA9", schlauch_id=50, schlauch_ad=HOSE[50]["ad"], biegeradius=hose_R(50), meterware_m=53.2, werkstoff="PVC-Spiralschlauch glatt innen lebensmittelecht, schwarz")
    return E

def write_json():
    p = os.path.join(sc.ROOT, "data", "components", "autobahn_teile.json")
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {"beschreibung": "Teiledaten N-AUTOBAHN-V2 (Werkstatt WA-T und WA-S, je ein Abschnitt)"}
    d["wa_s"] = dict(quelle="scripts/workshop/autobahn_s.py --json", blatt="docs/jobs/N-AUTOBAHN-V2.md Abschnitt 3", teileblatt="docs/parts/autobahn.md Abschnitt WA-S",
                     schlauch={str(k): dict(ad=v["ad"], r_hersteller=v["r_hersteller"], biegeradius=hose_R(k)) for k, v in HOSE.items()}, teile=json_entries())
    open(p, "w", encoding="utf-8").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    return p

if __name__ == "__main__":
    want = set(a for a in sys.argv[1:] if not a.startswith("--"))
    if "--json" in sys.argv:
        print(write_json()); sys.exit(0)
    for key, fname, fn in jobs():
        if want and key not in want:
            continue
        if "--render" in sys.argv:
            print(render(fname, **RENDER.get(fname, {}))); continue
        res = fn()
        sc.run(res[0].write(fname), os.path.join(DC, fname + ".sc"))
        print(fname)
