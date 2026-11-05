"""Pruefung WA-T Tragwerk der Wasserautobahn (autobahn_t.py): Koerper, Ports (Stirnflaechen), Interferenz 0 (gegen echte Bestandsgeometrie), Hoehenkette, Statik, Gefaelle K10.
Aufruf: python -X utf8 scripts/workshop/check_autobahn_t.py [joch|ausleger|stelze|schiene|klemme|verbinder|ecke|podest]   (exit 1 bei FAIL)
Statik [E] mit E = 210000 MPa, Grenze Biegespannung 160 MPa (S235/S250GD, Teilsicherheit ~1,5), Kopfverschiebung L/300, Durchbiegung Ausleger 10 mm, Schiene L/200."""
import sys, os, math, json, hashlib
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import ring_b2 as R
import autobahn_t as A
import check_lt_w36 as C

D = A.DC; E = 210000.0; G = 9.81; SIG = 160.0
# Lasten [A, Rechenwerte]: Schlauch voll je m (Spiralschlauch, Wand + Wasser), Fallstrecke unter dem Sattel, Ring PE-100 d75 SDR17 voll
Q_SCHLAUCH = {"id25": (0.35 + math.pi / 4 * 0.025 ** 2 * 1000), "id16": (0.20 + math.pi / 4 * 0.016 ** 2 * 1000)}     # kg/m
FALL_M = 1.3                                                    # m frei haengender Schlauch je Abnehmer bis zum Kugelhahn [A]
PE = A.ec_geom()
Q_RING = (math.pi / 4 * (0.075 ** 2 - (PE["di"] / 1000) ** 2) * 960 + math.pi / 4 * (PE["di"] / 1000) ** 2 * 1000)    # kg/m
I_SCHIENE = 5.81e4; W_SCHIENE = 2.84e3; KG_SCHIENE = 2.53   # [Q] MUEPRO MPR 41/41/2,5 Datenblatt 33665 (fischer FUS 41/2,5: 6,0 cm4 / 2,85 cm3) -> kleinerer Wert
ABZWEIG_KG = 1.18 + 2 * 0.5                                     # T97 d40 (Blatt ring_b2) + 2 Schlauchanfaenge [A]
GANG = {"A": (2195.0, 2795.0), "B": (3959.0, 4492.0)}           # [E] Radialbaender: Innentisch-Pfosten-Fussplatte 1864+331 / Mitte-Portal 3377 -+ 582 / Aussen-Portal 5074 - 582

def rohr_I(s, w): return (s ** 4 - (s - 2 * w) ** 4) / 12

def port_faces(ck, tag, path, bodies, ports):
    fs = [f for v in sc.faces_multi(path, bodies).values() for f in v]
    planes = [(f["plane_normal"], f["centroid"]) for f in fs if f.get("plane_normal")]
    for name, pos, dr, art, dn in ports:
        hit = any(sum(n[i] * dr[i] for i in range(3)) > 0.999 and abs(sum((c[i] - pos[i]) * dr[i] for i in range(3))) < 0.6 and math.dist(c, pos) < 60 for n, c in planes)
        ck.eq(f"{tag} Port {name} ({art}, {dn}): Stirnflaeche bei {tuple(round(v, 1) for v in pos)}", 1 if hit else 0, 1)

def interf(ck, tag, path, extra=(), own=None, label=""):
    bad, res = C.interference(path, list(extra))
    if own is not None:
        bad = [i for i in bad if (i.get("a") in own) != (i.get("b") in own) or (i.get("a") in own and i.get("b") in own)]
    ck.eq(f"{tag} Interferenz 0 {label}({res.get('checked', '?')} Koerper)", len(bad), 0)
    for i in bad[:12]:
        print("   Ueberlappung:", i.get("a"), i.get("b"), round(i.get("volume_mm3", 0), 1))

def own_cmds(build):
    """Befehle eines Teils zum Einfuegen in eine fremde Datei (ohne Parameter, Komponente, Metadaten)."""
    return [c for c in build.cmds if c["command"] in ("solid.cylinder", "solid.box", "material.create", "material.assign", "sketch.create", "sketch.line", "sketch.finish", "solid.extrude")]

def box_cmd(nm, x0, x1, y0, y1, z0, z1):
    return {"command": "solid.box", "params": {"length": x1 - x0, "width": y1 - y0, "height": z1 - z0, "center": [(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2], "operation": "new", "name": nm, "body_name": nm}}

def cyl_cmd(nm, d, h, base, axis):
    return {"command": "solid.cylinder", "params": {"diameter": d, "height": h, "base": base, "axis": axis, "operation": "new", "name": nm, "body_name": nm}}

# =========================================================================== WA1 Joch
def check_joch(ck):
    for s in ("a", "b"):
        tag = f"joch_{s}"; path = os.path.join(D, f"portal_joch_mitte_{s}.sc"); ev = sc.evaluate(path); g = A.jo_geom(s)
        bb = {b["name"]: b for b in ev["bodies"]}
        soll = 2 + 2 + 4 + 8 + 8 + 1 + 2 + 1      # Verlaengerungen, Kappen, Distanzbleche, Klemmplatten, Schrauben, Querriegel, Stirnplatten, Ausgleichsplatte
        ck.eq(f"{tag} Koerperzahl = {soll}", len(bb), soll)
        port_faces(ck, tag, path, ["Ausgleichsplatte", "Stirnplatte_innen", "Stirnplatte_aussen"], A.jo_ports(s))
        top = max(b["bbox"]["max"][2] for b in bb.values())
        ck.eq(f"{tag} Oberkante {top:.0f} <= Korridor KR {A.Z['kr_oben']:g}", 1 if top <= A.Z["kr_oben"] + 1e-6 else 0, 1)
        tief = [n for n, b in bb.items() if b["bbox"]["min"][2] < A.Z["gang_frei"] and max(abs(b["bbox"]["min"][1]), abs(b["bbox"]["max"][1])) > 582.0]
        ck.eq(f"{tag} kein Teil unter Z 2100 ausserhalb des Portalrands |y| <= 582 (Gang frei): {tief}", len(tief), 0)
        # Interferenz gegen den echten Mitteltisch (Tisch-.sc geladen, Joch-Befehle eingefuegt) + Innenbeet als Quader + Testkoerper Ring, Schiene, Ausleger
        b, nm, _ = A.joch(s)
        beet = sc.evaluate(os.path.join(D, "ibc_beet_innen_933.sc")); mn, mx = sc.bbox_all(beet)
        dz = 230 - 400                                                     # hoechstes Innenbeet (Beet_innen_933:4, z 230 abs) relativ zum Tisch (z 400 abs)
        extra = own_cmds(b) + [box_cmd("Test_Beet_innen", mn[0], mx[0], mn[1], mx[1], mn[2] + dz, mx[2] + dz),
                               cyl_cmd("Test_Ring_d75", 75, A.SEITE, [-A.SEITE / 2, 0, A.Z["achse"]], [1, 0, 0]),
                               box_cmd("Test_Schiene", -A.SEITE / 2, A.SEITE / 2, -20.5, 20.5, A.Z["schiene_u"], A.Z["schiene_o"]),
                               box_cmd("Test_Ausleger_innen", g["xe"] - 50, g["xe"] + 50, g["y_flansch"], g["y_flansch"] + 300, A.Z["platte_o"], A.Z["traeger_o"]),
                               box_cmd("Test_Ausleger_aussen", g["xe"] - 50, g["xe"] + 50, -g["y_flansch"] - 300, -g["y_flansch"], A.Z["platte_o"], A.Z["traeger_o"])]
        mine = set(bb)
        tests = {"Test_Beet_innen", "Test_Ring_d75", "Test_Schiene", "Test_Ausleger_innen", "Test_Ausleger_aussen"}
        bad, res = C.interference(os.path.join(D, "nft_tisch_mitte.sc"), extra)
        bad = [i for i in bad if (i.get("a") in mine or i.get("b") in mine) and not ({i.get("a"), i.get("b")} <= mine)]
        bad = [i for i in bad if not (i.get("a") in tests and i.get("b") in tests)]
        ck.eq(f"{tag} Interferenz 0 gegen nft_tisch_mitte (echte Geometrie), Innenbeet, Ring d75, Schiene, Ausleger ({res.get('checked', '?')} Koerper)", len(bad), 0)
        for i in bad[:12]: print("   Ueberlappung:", i.get("a"), i.get("b"), round(i.get("volume_mm3", 0), 1))
        own_bad, _ = C.interference(path)
        ck.eq(f"{tag} Interferenz 0 innerhalb des Jochs", len(own_bad), 0)
        for i in own_bad[:12]: print("   Ueberlappung:", i.get("a"), i.get("b"), round(i.get("volume_mm3", 0), 1))
    # Statik (Joch b ist der haeufige Fall; a gleich gebaut): Ausleger innen 1 Tisch-Schlauch, aussen 1 Tisch + 1 Beet; Ring voll je Ecke
    Ma_i, Fa_i = ausleger_last(A.AUSL["joch_innen"], ["id16"]); Ma_a, Fa_a = ausleger_last(A.AUSL["joch_aussen"], ["id16", "id25"])
    hebel = A.jo_geom("b")["y_flansch"] - 546.5
    M_net = abs((Ma_a + Fa_a * hebel / 1000) - (Ma_i + Fa_i * hebel / 1000))
    F_v = Fa_i + Fa_a + (Q_RING + KG_SCHIENE) * G * A.SEITE / 1000 + ABZWEIG_KG * G
    I = rohr_I(40, 3); Lk = A.Z["platte_o"] - JO_KLEMME_OBEN()
    d_y = M_net * 1000 / 2 * Lk ** 2 / (2 * E * I)                # Rahmen in der y-z-Ebene: Restmoment je Stiel, Stiel ab oberer Klemme eingespannt
    H = 50.0; d_x = (H / 2) * Lk ** 3 / (3 * E * I)                # Querlast 50 N [A] (Zug am Schlauch, Anstossen) tangential, zwei Stiele
    sig = max(M_net * 1000 / 2, H / 2 * Lk) / (I / 20)
    ck.eq(f"joch Kopfverschiebung radial {d_y:.2f} mm (Restmoment Ausleger {M_net:.1f} Nm) <= L/300 = {Lk / 300:.1f} (L = {Lk:.0f} ab oberer Klemme)", 1 if d_y <= Lk / 300 else 0, 1)
    ck.eq(f"joch Kopfverschiebung tangential {d_x:.2f} mm bei 50 N Querlast <= L/300 = {Lk / 300:.1f}", 1 if d_x <= Lk / 300 else 0, 1)
    ck.eq(f"joch Biegespannung Stiel {sig:.1f} MPa <= {SIG:g}", 1 if sig <= SIG else 0, 1)
    mu, fv = 0.15, 5000.0                                            # Reibbeiwert verzinkt [A], Vorspannkraft M8 8.8 handfest 5 kN [A, Tabellenwert ~16 kN bei Anzug nach VDI 2230]
    F_r = 2 * 2 * 2 * fv * mu                                      # 2 Klemmen x 2 Schrauben x 2 Reibflaechen je Stiel
    ck.eq(f"joch Klemmen tragen {F_r / 1000:.1f} kN je Stiel >= 3 x Last {F_v / 2:.0f} N (Reibschluss, kein Schweissen am Tisch)", 1 if F_r >= 3 * F_v / 2 else 0, 1)
    M_kipp = H * A.Z["traeger_o"] / 1000; print(f"INFO joch: Kippmoment aus 50 N am Kopf {M_kipp:.0f} Nm auf den Tisch (Bock: 2 Fussplatten mit je 2 M8, Abstand 1093 -> Zug {M_kipp / 1.093 / 2:.0f} N je Seite); Vertikallast je Joch {F_v:.0f} N")

def JO_KLEMME_OBEN(): return A.JO["klemm_z"][1][1]

def ausleger_last(lg, schlaeuche):
    """Moment am Flansch [Nm] und Querkraft [N]: Eigengewicht 40x40x3, Halter/Endbuegel aus dem Modell, Schlaeuche liegend + frei haengend am Ende."""
    q_arm = (40 ** 2 - 34 ** 2) * 7.85e-3                      # kg/m
    m_end = 1.2                                                 # Endbuegel + Halter [E grob aus dem Modell, siehe check_ausleger]
    q_s = sum(Q_SCHLAUCH[s] for s in schlaeuche); f_end = sum(Q_SCHLAUCH[s] * FALL_M for s in schlaeuche) + m_end
    l = lg / 1000
    M = (q_arm + q_s) * G * l ** 2 / 2 + f_end * G * l
    F = (q_arm + q_s) * G * l + f_end * G
    return M, F

# =========================================================================== WA2 Ausleger
def check_ausleger(ck):
    combos = {A.AUSL["joch_innen"]: ["id16"], A.AUSL["joch_aussen"]: ["id16", "id25"], A.AUSL["stelze_aussen_pfosten_aussen"]: ["id16", "id25"]}
    for lg, sl in sorted(combos.items()):
        tag = f"ausleger {lg:.0f}"; fn = f"ausleger_schlauch_{lg:.0f}"; path = os.path.join(D, fn + ".sc"); ev = sc.evaluate(path); g = A.au_geom(lg)
        bb = {b["name"]: b for b in ev["bodies"]}
        ck.eq(f"{tag} Koerper = Flansch, Arm, Endbuegel + {len(g['xs'])} Halterpaare", len(bb), 3 + 2 * len(g["xs"]))
        stellen = [A.AU["flansch_t"]] + g["xs"] + [lg]
        luecke = max(b_ - a_ for a_, b_ in zip(stellen, stellen[1:]))
        ck.eq(f"{tag} Halterabstand max {luecke:.0f} mm <= 400 (Leitungsordnung R6 Schlauch)", 1 if luecke <= 400 + 1e-6 else 0, 1)
        port_faces(ck, tag, path, ["Flansch"], A.au_ports(lg)[:1])
        clips = [f for f in sc.faces(path, f"Halter_1_l") if f.get("cylinder") and abs(f["cylinder"]["radius"] - A.AU["schlauch_ad_max"] / 2) < 0.01]
        ck.eq(f"{tag} Schlauchclip Bohrung AD {A.AU['schlauch_ad_max']:g} auf der Schlauchachse y {g['yh']:.1f}", 1 if clips and abs(clips[0]["cylinder"]["origin"][1] - g["yh"]) < 0.01 else 0, 1)
        sat = [f for f in sc.faces(path, "Endbuegel") if f.get("cylinder") and abs(f["cylinder"]["radius"] - g["rs"]) < 0.01]
        ck.eq(f"{tag} Sattelradius unter dem Schlauch {g['rs']:.1f} = Biegeradius {A.AU['biege_r']:g} - AD/2 (R14: >= 6 x AD {A.AU['schlauch_ad_max']:g} = {6 * A.AU['schlauch_ad_max']:g})", 1 if sat and A.AU["biege_r"] >= 6 * A.AU["schlauch_ad_max"] else 0, 1)
        interf(ck, tag, path, [cyl_cmd("Test_Schlauch_l", A.AU["schlauch_ad_max"] - 0.5, lg - 20, [10, g["yh"], 0], [1, 0, 0]), cyl_cmd("Test_Schlauch_r", A.AU["schlauch_ad_max"] - 0.5, lg - 20, [10, -g["yh"], 0], [1, 0, 0])], label="mit 2 Testschlaeuchen ")
        M, F = ausleger_last(lg, sl); I = rohr_I(40, 3)
        sig = M * 1000 / (I / 20)
        l = lg; q_arm = (40 ** 2 - 34 ** 2) * 7.85e-3; q = (q_arm + sum(Q_SCHLAUCH[s] for s in sl)) * G / 1000; P = (sum(Q_SCHLAUCH[s] * FALL_M for s in sl) + 1.2) * G
        w = q * l ** 4 / (8 * E * I) + P * l ** 3 / (3 * E * I)
        ck.eq(f"{tag} Biegespannung am Flansch {sig:.1f} MPa <= {SIG:g} (Moment {M:.0f} Nm, {'+'.join(sl)})", 1 if sig <= SIG else 0, 1)
        ck.eq(f"{tag} Durchbiegung Ende {w:.2f} mm <= 10 (ohne Kopfband)", 1 if w <= 10 else 0, 1)
        bolt = M / 0.020 / 2                                    # 2 Schrauben M10, Hebel 20 mm (halbe Flanschhoehe) [E konservativ]
        ck.eq(f"{tag} Zug je Flanschschraube M10 {bolt / 1000:.1f} kN <= 15 kN (8.8, Ft,Rd ~ 41 kN / 2,7)", 1 if bolt <= 15000 else 0, 1)
        low_arm = A.Z["platte_o"]
        low_sat = (A.Z["platte_o"] + A.Z["traeger_o"]) / 2 - A.AU["biege_r"]
        print(f"INFO {tag}: Arm-Unterkante Z {low_arm:g} rel (>= 2100 ueber dem Gang); Sattel bis Z {low_sat:.0f} rel nur am Ende ueber dem Abnehmer; Masse {ev['total']['mass_g'] / 1000:.2f} kg")
    # Gangquerung: Sattel (freier Fall) liegt radial jenseits der Gangbaender, je Lage aus autobahn_t.lagen()
    st = A.stelze()[2]; r_scheitel = A.R_ECKE - PE["stich"]; y0 = A.jo_geom("b")["y_flansch"]
    faelle = [("joch innen", A.AP_MITTE - y0, -1, A.AUSL["joch_innen"]), ("joch aussen", A.AP_MITTE + y0, 1, A.AUSL["joch_aussen"]),
              ("stelze Pfosten innen, innen", r_scheitel - (st["x_scheitel"] - st["x_minus"]), -1, A.AUSL["stelze_innen_pfosten_innen"]),
              ("stelze Pfosten aussen, innen", r_scheitel - (st["x_plus"] - st["x_scheitel"]), -1, A.AUSL["stelze_innen_pfosten_aussen"]),
              ("stelze Pfosten aussen, aussen", r_scheitel + (st["x_scheitel"] - st["x_minus"]), 1, A.AUSL["stelze_aussen_pfosten_aussen"])]
    for nm_, r0, sgn, lg in faelle:
        r_ende = r0 + sgn * lg; sat = sorted((r_ende, r_ende + sgn * (A.AU["biege_r"] + 5)))
        # W88/FIX-a: Der Sattel darf ueber dem Gang beginnen, solange die Schlauch-Unterkante dort >= Z 2100 rel bleibt; der senkrechte Fall liegt ausserhalb.
        z_arm = (A.Z["platte_o"] + A.Z["traeger_o"]) / 2; Rb = A.AU["biege_r"]; ad2 = A.AU["schlauch_ad_max"] / 2
        r_fall = r_ende + sgn * Rb; z_min_gang = None
        for g0, g1 in GANG.values():
            for i in range(0, 211):
                r = r_ende + sgn * Rb * i / 210
                if g0 <= r <= g1:
                    dx = Rb * i / 210; zu = z_arm - (Rb - math.sqrt(max(0.0, Rb * Rb - dx * dx))) - ad2
                    z_min_gang = zu if z_min_gang is None else min(z_min_gang, zu)
        fall_frei = all(not (g0 - ad2 - 50 <= r_fall <= g1 + ad2 + 50) for g0, g1 in GANG.values())
        frei = fall_frei and (z_min_gang is None or z_min_gang >= 2100)
        ck.eq(f"ausleger {nm_} ({lg:.0f}): Flansch r {r0:.0f}, Fallachse r {r_fall:.0f} ausserhalb Gang A {GANG['A'][0]:.0f}..{GANG['A'][1]:.0f} und B {GANG['B'][0]:.0f}..{GANG['B'][1]:.0f} (+ AD/2 + 50); "
              f"Schlauch-Unterkante im Sattel ueber dem Gang {'-' if z_min_gang is None else round(z_min_gang)} >= 2100 rel", 1 if frei else 0, 1)

# =========================================================================== WA2b Stelze Rev. B
def check_stelze(ck):
    path = os.path.join(D, "ringstuetze_d75_b.sc"); ev = sc.evaluate(path); bb = {b["name"]: b for b in ev["bodies"]}; b, nm, g = A.stelze()
    soll = {"Fussplatte", "Anker_1", "Anker_2", "Anker_3", "Anker_4", "Pfosten", "Kragarm", "Gegenarm", "Stirnplatte_plus", "Stirnplatte_minus"}
    ck.eq("stelze_b Koerper = Sollliste (10)", len(set(bb) ^ soll), 0)
    ports = A.st_ports()
    port_faces(ck, "stelze_b", path, ["Kragarm", "Stirnplatte_plus", "Stirnplatte_minus", "Fussplatte"], [ports[0], ports[2], ports[3], ports[4]])
    hole = [f for f in sc.faces(path, "Kragarm") if f.get("cylinder") and abs(f["cylinder"]["radius"] - (A.KL["stummel_d"] + 1) / 2) < 0.01]
    ck.eq(f"stelze_b Bohrung M8 im Kragarm ueber dem Bogenscheitel x {g['x_scheitel']:.1f}", 1 if hole and abs(hole[0]["cylinder"]["origin"][0] - g["x_scheitel"]) < 0.01 else 0, 1)
    top = max(x["bbox"]["max"][2] for x in bb.values())
    ck.eq(f"stelze_b Oberkante {top:.0f} <= KR {A.Z['kr_oben']:g}", 1 if top <= A.Z["kr_oben"] else 0, 1)
    # Testkoerper: Schienen beider Ringseiten (vereinfacht als eine Schiene entlang Y an x 250), Verbinder-Platte, Ring am Scheitel, Scheitel-Schelle
    extra = [box_cmd("Test_Schiene", R.RS["ausladung"] - 20.5, R.RS["ausladung"] + 20.5, -600, 600, A.Z["schiene_u"], A.Z["schiene_o"]),
             box_cmd("Test_Verbinder", R.RS["ausladung"] - 20.5, g["x_scheitel"] + 25, -20, 20, A.Z["schiene_o"], A.Z["platte_o"]),
             cyl_cmd("Test_Ring_d75", 75, 400, [g["x_scheitel"], -200, A.Z["achse"]], [0, 1, 0])]
    interf(ck, "stelze_b", path, extra, label="mit Schiene, Verbinder, Ring am Scheitel ")
    # Statik je Aufstellung: Moment am Fuss = Ring am Scheitel (x_scheitel) + Ausleger an den Stirnplatten; Pfosten-Lage wie autobahn_t.lagen()
    F_ring = (Q_RING + KG_SCHIENE) * G * A.SEITE / 1000 + ABZWEIG_KG * G
    def am(lg, sl, x):
        M_, F_ = ausleger_last(lg, sl); return M_ + F_ * abs(x) / 1000
    faelle = {"Pfosten innen, nur Innen-Ausleger am Gegenarm (-89,7 / -53,7)": F_ring * g["x_scheitel"] / 1000 - am(A.AUSL["stelze_innen_pfosten_innen"], ["id16"], g["x_minus"]),
              "Pfosten innen, Innen-Schlauch leer": F_ring * g["x_scheitel"] / 1000 - am(A.AUSL["stelze_innen_pfosten_innen"], [], g["x_minus"]),
              "Pfosten aussen, Innen- und Aussen-Ausleger (-17,7)": F_ring * g["x_scheitel"] / 1000 + am(A.AUSL["stelze_innen_pfosten_aussen"], ["id16"], g["x_plus"]) - am(A.AUSL["stelze_aussen_pfosten_aussen"], ["id16", "id25"], g["x_minus"]),
              "Pfosten aussen, Aussen-Schlaeuche leer": F_ring * g["x_scheitel"] / 1000 + am(A.AUSL["stelze_innen_pfosten_aussen"], ["id16"], g["x_plus"]) - am(A.AUSL["stelze_aussen_pfosten_aussen"], [], g["x_minus"])}
    Ip = rohr_I(R.RS["pfosten_b"], R.RS["pfosten_w"]); Lp = A.Z["traeger_o"]
    for k, M in faelle.items():
        M = abs(M); d = M * 1000 * Lp ** 2 / (2 * E * Ip); sig = M * 1000 / (Ip / (R.RS["pfosten_b"] / 2))
        zug = M / (R.RS["anker_abstand"] / 1000) / 2 - (ev["total"]["mass_g"] / 1000 * G) / 4
        ck.eq(f"stelze_b {k}: Kopfverschiebung {d:.2f} mm <= L/300 = {Lp / 300:.1f} (Moment am Fuss {M:.0f} Nm, Spannung {sig:.1f} MPa, Ankerzug {max(zug, 0):.0f} N)", 1 if d <= Lp / 300 and sig <= SIG and zug <= 3000 else 0, 1)
    print(f"INFO stelze_b: Masse {ev['total']['mass_g'] / 1000:.2f} kg; Scheitel x {g['x_scheitel']:.1f}, Stirnplatten x {g['x_plus']:.1f} / {g['x_minus']:.1f}")

# =========================================================================== WA3 Schiene, Klemmen, Verbinder
def stuetz_positionen():
    """Stuetzpunkte entlang des Ringumfangs (Bogenlaenge ab Ecke -89,7 gegen den Uhrzeigersinn): Joch im Abstand abstand_ecke vor/nach der Ecke, Stelze an der Ecke."""
    lag = A.lagen(); s0 = lag[0]["ecke_az"]; out = []
    for l in lag:
        k = round(((l["ecke_az"] - s0) % 360) / 36.0); s = k * A.SEITE
        if l["art"] == "joch":
            s += -l["abstand_ecke"] if l["bock"] == "b" else l["abstand_ecke"]
        out.append(s % (10 * A.SEITE))
    return sorted(out)

def check_schiene(ck):
    q = A.sch_querschnitt(); lg = A.SCH["laenge"]; path = os.path.join(D, f"montageschiene_41_{lg:.0f}.sc"); ev = sc.evaluate(path)
    bbx = ev["bodies"][0]["bbox"]
    ck.eq(f"schiene Laenge {lg:g} (Seite {A.SEITE:.1f} - Gehrungsluft)", bbx["max"][0] - bbx["min"][0], lg, 0.05)
    ck.eq("schiene Querschnitt 41 x 41", (bbx["max"][1] - bbx["min"][1]) + (bbx["max"][2] - bbx["min"][2]), 82.0, 0.05)
    ck.eq(f"schiene Masse Modell {ev['total']['mass_g'] / lg:.2f} kg/m = Datenblatt {KG_SCHIENE} kg/m (+-10 %)", ev["total"]["mass_g"] / lg, KG_SCHIENE, 0.253)
    print(f"INFO schiene: Iy Modell (Rechtecke, ohne Lochung/Radien) {q['I'] / 1e4:.2f} cm4; Rechnung nutzt Datenblatt {I_SCHIENE / 1e4:.2f} cm4 (MUEPRO), fischer 6,0 cm4")
    pos = stuetz_positionen(); U = 10 * A.SEITE
    spans = [((pos[(i + 1) % len(pos)] - pos[i]) % U) for i in range(len(pos))]
    Lm = max(spans); q_ = (Q_RING + KG_SCHIENE) * G / 1000; P = ABZWEIG_KG * G + 2 * Q_SCHLAUCH["id25"] * G * 1.5
    w = 5 * q_ * Lm ** 4 / (384 * E * I_SCHIENE) + P * Lm ** 3 / (48 * E * I_SCHIENE)
    M = q_ * Lm ** 2 / 8 + P * Lm / 4; sig = M / W_SCHIENE
    ck.eq(f"schiene Stuetzpunkte im Ring = 10 (7 Joche, 3 Stelzen)", len(pos), 10)
    ck.eq(f"schiene groesste Spannweite {Lm:.0f} mm: Durchbiegung {w:.2f} mm <= L/200 = {Lm / 200:.1f} (Ring voll {Q_RING:.2f} kg/m + Schiene, Einzellast Ecke {P:.0f} N, Einfeldtraeger)", 1 if w <= Lm / 200 else 0, 1)
    ck.eq(f"schiene Biegespannung {sig:.1f} MPa <= {SIG:g}", 1 if sig <= SIG else 0, 1)
    print("INFO schiene: Spannweiten " + ", ".join(f"{s:.0f}" for s in spans))
    # Schellen: an beiden Tangentenpunkten jeder Ecke (Schiene) + Scheitel (Verbinder-Lasche bzw. Stelzen-Kragarm)
    t = PE["tangente"]; mitte = A.SEITE - 2 * t
    ck.eq(f"schiene Schellenabstand max {max(t, mitte):.0f} mm <= 1000 (R6 d75): Scheitel -> Tangentenpunkt {t:.0f}, Tangentenpunkt -> Tangentenpunkt {mitte:.0f}", 1 if max(t, mitte) <= 1000 else 0, 1)
    print(f"INFO schiene: Schellen je Ring 30 (20 an den Tangentenpunkten auf der Schiene, 10 am Scheitel: 7 Verbinder-Laschen + 3 Stelzen-Kragarme)")

def check_klemme(ck):
    for art in A.KL_ART:
        fn = "lt_klemme_d75" if art == "schiene" else f"lt_klemme_d75_{art}"; tag = fn; path = os.path.join(D, fn + ".sc"); ev = sc.evaluate(path); g = A.kl_geom(art)
        bb = {b["name"]: b for b in ev["bodies"]}
        ck.eq(f"{tag} Koerper = Schelle, Einlage, Stummel, Mutter (4)", len(set(bb) ^ {"Rohrschelle", "Schelleneinlage", "Gewindestummel", "Schienenmutter"}), 0)
        low = min(b["bbox"]["min"][2] for b in bb.values()) + A.Z["achse"]
        ck.eq(f"{tag} tiefster Punkt {low:.1f} rel >= 2100 (Gang unter dem Ring frei)", 1 if low >= A.Z["gang_frei"] else 0, 1)
        hit = [f["cylinder"] for f in sc.faces(path, "Schelleneinlage") if f.get("cylinder") and abs(f["cylinder"]["radius"] - 37.5) < 0.01]
        ck.eq(f"{tag} Einlage umschliesst d75 auf der Rohrachse", 1 if hit and abs(hit[0]["origin"][2]) < 0.01 and abs(abs(hit[0]["axis"][0]) - 1) < 1e-6 else 0, 1)
        mu = bb["Schienenmutter"]["bbox"]
        ck.eq(f"{tag} Mutter liegt auf ihrer Auflage z {g['z_mutter0'] + A.Z['achse']:.1f} rel", mu["min"][2], g["z_mutter0"], 0.01)
        test = [cyl_cmd("Test_Rohr_d75", 75, 300, [-150, 0, 0], [1, 0, 0])]
        if art == "schiene":
            # Schiene mit Schlitz: Lippen als zwei Quader unter der Mutter, Schlitz frei fuer den Stummel
            test += [box_cmd("Test_Lippe_l", -100, 100, -20.5, -11, g["z_su"], g["z_su"] + A.SCH["t"]), box_cmd("Test_Lippe_r", -100, 100, 11, 20.5, g["z_su"], g["z_su"] + A.SCH["t"])]
        else:
            test += [box_cmd("Test_Auflage", -30, 30, -20, 20, g["z_mutter0"] - 4, g["z_mutter0"]) if art == "ecke" else box_cmd("Test_Kragarm_unten", -30, 30, -20, 20, g["z_mutter0"] - 40, g["z_mutter0"] - 37)]
        interf(ck, tag, path, test, own={"Rohrschelle", "Schelleneinlage", "Schienenmutter"}, label="mit Testrohr und Auflage (Stummel durch Bohrung/Schlitz ausgenommen) ")

def check_verbinder(ck):
    path = os.path.join(D, "schienenverbinder_36.sc"); ev = sc.evaluate(path); sl = A.sv_lasche()
    ck.eq("verbinder ein Koerper", len(ev["bodies"]), 1)
    bbz = ev["bodies"][0]["bbox"]
    ck.eq("verbinder Dicke 4 (Ausgleich Schiene 2253 -> Traeger 2257)", bbz["max"][2] - bbz["min"][2], A.Z["platte_o"] - A.Z["schiene_o"], 0.01)
    holes = list({(round(f["cylinder"]["origin"][0], 2), round(f["cylinder"]["origin"][1], 2)): f["cylinder"] for f in sc.faces(path, "Schienenverbinder")
                  if f.get("cylinder") and abs(f["cylinder"]["radius"] - A.SV["loch_d"] / 2) < 0.01}.values())     # Zylinderflaechen sind je Bohrung geteilt -> nach Achse zaehlen
    sch = [h for h in holes if math.hypot(h["origin"][0] - sl["scheitel"][0], h["origin"][1] - sl["scheitel"][1]) < 0.01]
    ck.eq(f"verbinder Bohrung ueber dem Bogenscheitel (Stich {sl['stich']:.1f} mm auf der Winkelhalbierenden)", len(sch), 1)
    ck.eq("verbinder 4 Bohrungen M8 in den Schenkeln + 1 Scheitel", len(holes), 5)

# =========================================================================== WA4 Ring-Ecke
def check_ecke(ck):
    path = os.path.join(D, "ring_ecke_d75.sc"); ev = sc.evaluate(path); g = A.ec_geom()
    ck.eq("ecke ein Koerper (PE-100 Rohr gebogen)", len(ev["bodies"]), 1)
    ck.eq(f"ecke Biegeradius {g['R']:.0f} >= 25 x d = {25 * 75} (PE100+ Association SDR17 25 x DN; Firat und Ostendorf 20 x d -> strengerer Wert)", 1 if g["R"] >= 25 * 75 else 0, 1)
    port_faces(ck, "ecke", path, ["Ring_Ecke"], A.ec_ports())
    v_soll = math.pi / 4 * (75 ** 2 - g["di"] ** 2) * g["achs_l"]
    ck.eq(f"ecke Volumen = Ringflaeche x Achslaenge {g['achs_l']:.0f} (Bogen ohne Querschnittsverlust)", ev["bodies"][0]["volume_mm3"], v_soll, v_soll * 0.005)
    ck.eq(f"ecke Tangenten 2 x {g['tangente']:.0f} < Seite {A.SEITE:.0f}: Gerade zwischen zwei Boegen {A.SEITE - 2 * g['tangente']:.0f} mm >= 300 (Platz fuer Abzweig und Schelle)", 1 if A.SEITE - 2 * g["tangente"] >= 300 else 0, 1)
    interf(ck, "ecke", path, [cyl_cmd("Test_Rohr_A", 75, 300, [0, 0, -300], [0, 0, 1])], own={"Ring_Ecke"}, label="mit Anschlussrohr ")
    print(f"INFO ecke: Stich (Scheitel innen vor der Polygonecke) {g['stich']:.1f} mm, Bogenlaenge {g['bogen_l']:.0f}, Wand SDR17 {g['wand']} mm")

# =========================================================================== WA7 Podest
def shift_cmds(build, dz, skip_mat=()):
    out = []
    for c in build.cmds:
        if c["command"] not in ("solid.cylinder", "solid.box", "material.create", "material.assign"):
            continue
        if c["command"] == "material.create" and c["params"]["name"] in skip_mat:
            continue
        pr = dict(c["params"])
        for k in ("base", "center"):
            if k in pr: pr[k] = [pr[k][0], pr[k][1], pr[k][2] + dz]
        out.append({"command": c["command"], "params": pr})
    return out

def check_podest(ck):
    path = os.path.join(D, "pegelschacht_podest.sc"); ev = sc.evaluate(path); g = A.po_geom(); ph = A.podest_h()
    bb = {b["name"]: b for b in ev["bodies"]}
    ck.eq("podest Koerper = 4 Fuesse, 4 Beine, 8 Rahmenrohre, Deckplatte, Haltering (18)", len(bb), 18)
    ck.eq(f"podest Deckplatte oben = Fassboden Z {g['h']:g}", bb["Deckplatte"]["bbox"]["max"][2], g["h"], 0.01)
    port_faces(ck, "podest", path, ["Deckplatte", "Fuss_1"], [A.po_ports()[0]])
    drop = A.K10["achse"] - (g["h"] + ph["zport"] + ph["stueck"] + ph["bogen"])
    gef = drop / A.K10["laenge_max"]
    ck.eq(f"podest K10-Gefaelle {gef * 100:.2f} % >= 1 % auf {A.K10['laenge_max']:g} mm (Achse {A.K10['achse']:g} -> Bogen 90 d50 {ph['bogen']:g} -> Rohrstueck {ph['stueck']:g} -> Zulauf-Muffe {g['h'] + ph['zport']:g})", 1 if gef >= 0.01 - 1e-9 else 0, 1)
    pb = R.pegelschacht()[0]
    extra = shift_cmds(pb, g["h"], skip_mat=())
    interf(ck, "podest", path, extra, label="mit Pegelschacht T94 auf der Deckplatte ")
    # Kippen: Fass voll (bis Ueberlauf) + Podest, Horizontallast 10 % [A] am Fassschwerpunkt
    m = R.ps_geom()["vol_bis_ueberlauf_l"] + 5.8 + ev["total"]["mass_g"] / 1000
    z_s = g["h"] + 250; M_k = 0.1 * m * G * z_s / 1000; M_s = m * G * (A.PO["b"] / 2) / 1000
    ck.eq(f"podest Standsicherheit ohne Anker {M_s / M_k:.1f} >= 1,5 (Fass voll {m:.0f} kg, 10 % Horizontallast in Z {z_s:.0f})", 1 if M_s / M_k >= 1.5 else 0, 1)
    sig = m * G / 4 / ((40 ** 2 - 34 ** 2))
    ck.eq(f"podest Druck je Bein {sig:.2f} MPa <= {SIG:g} (Knicken bei L {g['h']:.0f} unkritisch: Schlankheit {g['h'] / math.sqrt(rohr_I(40, 3) / (40 ** 2 - 34 ** 2)):.0f})", 1 if sig <= SIG else 0, 1)
    p_ab = 4 * 55 / 60000 * 1000 * G * ((A.Z["achse"] + 45) - (g["h"] + R.PS["pegel_ein"])) / 1000 / 0.25 + 0
    print(f"INFO podest: Hoehe {g['h']:g} statt Planer-Annahme 950 (K10 passt nicht in den Fassdeckel bei 950: Bogen + Rohrstueck brauchen {ph['bogen'] + ph['stueck']:g} mm). "
          f"Pegel EIN Z {g['h'] + R.PS['pegel_ein']:g}; Booster-Foerderhoehe geodaetisch bis Hochpunkt 2190 = {2190 - g['h'] - R.PS['pegel_ein']:.0f} mm")
    lage_podest(ck, g)

def lage_podest(ck, g):
    """Vorschlag fuer Montage R1c: Pegelschacht an der Stelle des A+-Verteilers (K10-Ende) gegen Gang A und Nachbarn pruefen (Bounding-Boxen, Welt)."""
    cmds = json.load(open(os.path.join(sc.ROOT, "scripts", "dome-script.json"), encoding="utf-8"))["commands"]
    mats = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
    tr = json.load(open(os.path.join(sc.ROOT, "data", "leitungstrassen.json"), encoding="utf-8"))
    tr = tr["trassen"] if isinstance(tr, dict) else tr
    out = []
    for kid, tank in (("K10", "Tank_gross:1"), ("K26", "Tank_gross_t3:1")):
        p = [t for t in tr if t.get("id") == kid][0]["pfad"]; a, e = p[0], p[-1]
        dx, dy = e[0] - a[0], e[1] - a[1]; n = math.hypot(dx, dy); u = (dx / n, dy / n)
        zu = (e[0] + u[0] * 91, e[1] + u[1] * 91)                         # Zulauf-Muffe senkrecht unter dem Bogen
        c = (zu[0] + u[0] * 100, zu[1] + u[1] * 100)                      # Fassmitte: Zulauf liegt bei x -100 im Schacht-KS
        r = math.hypot(*c); r_in, r_out = r - 250, r + 250                  # Fass + Stutzen r 250
        ov = {k: max(0.0, min(r_out, b_[1]) - max(r_in, b_[0])) for k, b_ in GANG.items()}
        out.append((kid, c, r, ov))
        print(f"BEFUND podest Lage {kid} (Platz des A+-Verteilers, K10/K26-Ende): Fassmitte x {c[0]:.0f} y {c[1]:.0f} (r {r:.0f}), Schacht mit Stutzen r {r_in:.0f}..{r_out:.0f}; "
              f"Ueberdeckung Gang A {ov['A']:.0f} mm, Gang B {ov['B']:.0f} mm -> Montage R1c fuehrt K10/K26 seitlich am Biofilter vorbei (bis {A.K10['laenge_max']:g} mm bei 1 %); nicht zaehlend, Lage ist Montage-Sache")

def main():
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or ["joch", "ausleger", "stelze", "schiene", "klemme", "verbinder", "ecke", "podest"]
    ck = sc.Check("autobahn_t")
    for w in want:
        globals()["check_" + w](ck)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
