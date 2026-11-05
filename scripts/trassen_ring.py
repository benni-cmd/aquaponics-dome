"""N-AUTOBAHN-V2 Montage R1/R2 (docs/jobs/N-AUTOBAHN-V2.md Abschnitt 4): Lage aller Teile der Wasserautobahn (Variante ring_b2).
Koordinaten kommen aus den Instanzmatrizen von scripts/dome-script.json (A+-Bau, Tische/Tanks sind in beiden Varianten gleich) und aus den
Port-Tabellen der Werkstatt (data/components/autobahn_teile.json, scripts/workshop/autobahn_t.py, ring_b2.py, autobahn_s.py), nie von Hand.
Modellrahmen: Z absolut (= relativ + 400). Ring als Zehneck auf dem Mittelring (Apothem 3377, WA-T), Umlauf gegen den Uhrzeigersinn.

Ausgaben:
  tragwerk()            -> [(Klasse, Datei, [Matrizen], Assembly)] fuer gen_dome.ring_b2() (Joche, Stelzen, Ausleger, Schienen, Verbinder, Schellen,
                           Ring-Ecken, Podeste, Pegelschaechte, Booster, Abzweige, Entluefter, Fallleitungen)
  leitungen_eintraege() -> Trassen, T-Stuecke, R-Stuecke mit varianten ["ring_b2"] und quelle "trassen_ring" fuer data/leitungstrassen.json
Aufruf: python -X utf8 scripts/trassen_ring.py [--schreiben] [--bericht]
  --schreiben  ersetzt in data/leitungstrassen.json alle Eintraege mit quelle "trassen_ring" (fremde Eintraege bleiben stehen)
  --bericht    druckt Zaehlung und Geometrie-Pruefpunkte (R1/R2, Blatt Abschnitt 6)"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "workshop"))
import leitung as LT          # Bibliothek lt_* (Ports, Muffentiefen)
import autobahn_t as AT       # WA-T Tragwerk
import ring_b2 as RB          # V2 Bauteile (Pegelschacht, Abzweig, Entluefter)

COMP = os.path.join(ROOT, "designs", "components")
FZ = 400.0                                        # Innenboden absolut (params sock_h)
QUELLE = "trassen_ring"
V = ["ring_b2"]

# ------------------------------------------------------------------ Vektoren
def add(a, b, s=1.0): return tuple(a[i] + s * b[i] for i in range(len(a)))
def sub(a, b): return tuple(a[i] - b[i] for i in range(len(a)))
def mul(a, s): return tuple(v * s for v in a)
def dot(a, b): return sum(a[i] * b[i] for i in range(len(a)))
def nrm(a): return math.sqrt(dot(a, a))
def unit(a): n = nrm(a); return tuple(v / n for v in a)
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def h(deg): return (math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0.0)
def rot_z(v, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg)); return (v[0] * c - v[1] * s, v[0] * s + v[1] * c, v[2])
def rd(p, n=1): return [round(float(v), n) for v in p]
def az(p): return math.degrees(math.atan2(p[1], p[0]))
def mat(o, x, z):
    """3x4-Matrix (zeilenweise) mit lokaler X = x, Z = z (x wird orthogonalisiert), Ursprung o."""
    z = unit(z); x = unit(sub(x, mul(z, dot(x, z)))); y = cross(z, x)
    return [round(v, 9) for v in (x[0], y[0], z[0], o[0], x[1], y[1], z[1], o[1], x[2], y[2], z[2], o[2])]
def world(m, p): return tuple(m[4 * r] * p[0] + m[4 * r + 1] * p[1] + m[4 * r + 2] * p[2] + m[4 * r + 3] for r in range(3))
def wdir(m, d): return tuple(m[4 * r] * d[0] + m[4 * r + 1] * d[1] + m[4 * r + 2] * d[2] for r in range(3))

# ------------------------------------------------------------------ Bestand
def _bestand():
    cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json"), encoding="utf-8"))["commands"]
    return {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
MV = _bestand()
TEILE = json.load(open(os.path.join(ROOT, "data", "components", "autobahn_teile.json"), encoding="utf-8"))
TW = TEILE["tragwerk"]
Z = {k: v + FZ for k, v in TW["hoehenkette_rel"].items()}     # absolut: achse 2545, schiene_u 2612, schiene_o 2653, platte_o 2657, traeger_o 2697

# ------------------------------------------------------------------ Ring-Geometrie (Zehneck, Ecken an den Sektorgrenzen der Mitteltische)
EC = AT.ec_geom()                                  # Ring-Ecke PE R 1875, Port-Abstand 759,2 von der Ecke, Stich 96,5
AP = TW["ring"]["apothem"]; RE = TW["ring"]["eckradius"]; SEITE = TW["ring"]["seite"]
ECKEN_AZ = sorted(l["ecke_az"] for l in TW["lagen"])         # -161.7 ... 162.3 (Eckazimute aus WA-T lagen(), = Tisch-Azimut +- 18)
N = len(ECKEN_AZ)
VX = [(RE * math.cos(math.radians(a)), RE * math.sin(math.radians(a)), Z["achse"]) for a in ECKEN_AZ]
U = [unit(sub(VX[(k + 1) % N], VX[k])) for k in range(N)]     # Seite k: Ecke k -> Ecke k+1
NL = [(-u[1], u[0], 0.0) for u in U]                            # links der Laufrichtung = zur Mitte
def seite_pt(k, s): return add(VX[k], U[k], s)                  # Punkt auf Seite k im Abstand s ab Ecke k
L_GERADE = SEITE - 2 * EC["ecke_bis_port"]                      # 676 mm gerades Rohr je Seite zwischen zwei Ecken

def ecke_matrix(k):
    """Ring-Ecke k: Port A auf der einlaufenden Seite (k-1), lokale Z = Laufrichtung, lokale X = zur Mitte (Bogen in XZ)."""
    u_in = U[(k - 1) % N]; o = add(VX[k], u_in, -EC["ecke_bis_port"])
    return mat(o, (-u_in[1], u_in[0], 0.0), u_in)

def bogen_pt(k, s):
    """Punkt und Tangente auf dem Bogen der Ecke k; s = Bogenlaenge ab Scheitel (+ = Richtung Seite k, - = Richtung Seite k-1)."""
    u_in, u_out = U[(k - 1) % N], U[k]
    th = math.radians(36.0)
    bis = unit(add(mul(u_in, -1), u_out))                       # Winkelhalbierende zeigt in die Ecke hinein (zur Mitte)
    C = add(VX[k], bis, EC["R"] / math.cos(th / 2))             # Bogenmitte
    phi = s / EC["R"]
    r0 = mul(bis, -1)                                           # Scheitel: C - R * bis
    t0 = unit(add(u_in, u_out))
    p = add(C, add(mul(r0, EC["R"] * math.cos(phi)), mul(t0, EC["R"] * math.sin(phi))))
    t = unit(add(mul(t0, math.cos(phi)), mul(r0, -math.sin(phi))))
    return p, t

# Linien (Blatt 1.5): Eckazimute je Linie, Kupplungsseiten zwischen den Linien
def _ecke_idx(a): return min(range(N), key=lambda k: abs(((ECKEN_AZ[k] - a + 180) % 360) - 180))
LINIE_ECKEN = {1: [_ecke_idx(a) for a in (-53.7, -17.7, 18.3, 54.3, 90.3)], 2: [_ecke_idx(a) for a in (126.3, 162.3, -161.7, -125.7, -89.7)]}
def seite_linie(k):
    a, b = k, (k + 1) % N
    for l, ek in LINIE_ECKEN.items():
        if a in ek and b in ek: return l
    return 0                                                    # Kupplungsstrecke
KUPPLUNG = [k for k in range(N) if seite_linie(k) == 0]

# ------------------------------------------------------------------ Stuetzpunkte (R1a): 7 Joche, 3 Stelzen (Lage aus WA-T lagen)
ST = AT.stelze()[2]
def stuetzpunkte():
    out = []
    for l in TW["lagen"]:
        k = _ecke_idx(l["ecke_az"])
        if l["art"] == "joch":
            m = l["matrix_tisch"]
            jp = {p["name"].split(" (")[0]: p for p in TW["teile"][l["teil"]]["ports"]}
            aus = {}
            for seite in ("innen", "aussen"):
                if l["ausleger"].get(seite):
                    p = jp["Ausleger " + seite]
                    aus[seite] = (world(m, p["lage"]), wdir(m, p["richtung"]), l["ausleger_laenge"][seite])
            out.append(dict(k=k, art="joch", teil=l["teil"], matrix=m, ausleger=aus, schiene=world(m, jp["Schiene"]["lage"]), tisch=l["tisch"], bock=l["bock"]))
        else:
            innen_pf = l["pfosten"] == "innen"
            bis = unit((VX[k][0], VX[k][1], 0.0))                  # radial nach aussen
            o = (bis[0] * l["r_pfosten"], bis[1] * l["r_pfosten"], FZ)
            xl = bis if innen_pf else mul(bis, -1)                  # Kragarm +X zeigt zum Bogenscheitel
            m = mat(o, xl, (0, 0, 1))
            aus = {}
            for seite, lg in l["ausleger_laenge"].items():
                plus = (seite == "aussen") == innen_pf              # Aussen-Ausleger am Kragarm, wenn der Pfosten innen steht
                x = ST["x_plus"] if plus else ST["x_minus"]; d = (1.0, 0, 0) if plus else (-1.0, 0, 0)
                aus[seite] = (world(m, (x, 0.0, AT.Z["platte_o"] / 2 + AT.Z["traeger_o"] / 2)), wdir(m, d), lg)
            out.append(dict(k=k, art="stelze", teil="ringstuetze_d75_b", matrix=m, ausleger=aus, pfosten=l["pfosten"], r_pfosten=l["r_pfosten"],
                            schienenecke=world(m, (AT.RB_AUSLADUNG if hasattr(AT, "RB_AUSLADUNG") else RB.RS["ausladung"], 0, AT.Z["platte_o"])),
                            scheitel=world(m, (ST["x_scheitel"], 0, AT.Z["traeger_o"]))))
    return out

def ausleger_matrix(o, d):
    """Ausleger-KS: Flanschanlage x 0, Arm +X, Armmitte z 0."""
    return mat(o, d, (0, 0, 1))

# ------------------------------------------------------------------ Einspeisung (R1c): Lage am K10/K26-Ende (WA-T lage_podest), Booster daneben
TRASSEN = json.load(open(os.path.join(ROOT, "data", "leitungstrassen.json"), encoding="utf-8"))
def _trasse(tid): return [t for t in TRASSEN["trassen"] if t["id"] == tid][0]
PODEST_H = TW["teile"]["pegelschacht_podest"]["hoehe"]          # 820 rel
PS = RB.PS; PSP = {p[0].split(" (")[0]: p for p in RB.ps_ports()}
PG_SAUG = (196.0, 76.0, 120.0); PG_DRUCK = (90.0, 76.0, 255.0)  # pumpe_gross Ports (trassen_linie.PORTS)
EINSP = {1: dict(kante="K10", tank="Tank_gross:1", seite_tang=1), 2: dict(kante="K26", tank="Tank_gross_t3:1", seite_tang=-1)}
L_SAUG1, L_SAUG2 = 200.0, 330.0                                  # [A] Saugleitung: waagerecht ab Stutzen, dann senkrecht, dann waagerecht in den Booster

def einspeisung(l):
    """Lage Pegelschacht/Podest/Booster und Leitungspunkte der Linie l. Pegelschacht-KS: lokale X tangential (Saugstutzen +-30 Grad auf der +X-Seite)."""
    e = EINSP[l]; tr = _trasse(e["kante"]); p0, p1 = tr["pfad"][-2], tr["pfad"][-1]
    u = unit((p1[0] - p0[0], p1[1] - p0[1], 0.0))
    t50 = LT.DEPTH[50]; k90 = LT.ports("lt_bogen90_d50")[1][1][0]
    tip = add(tuple(p1), u, t50)                                 # K10-Rohrende (steckte in A+ im Verteiler, hier Stutzenspitze)
    corner = add(tip, u, k90 - t50)                              # Bogen 90 d50 direkt auf dem Rohrende
    zul = PSP["Zulauf"][1]                                       # (-100, 0, 575)
    xl = mul((-u[1], u[0], 0.0), e["seite_tang"])                # tangential, vom Tank-Sektor weg in den freien Teil (Seite je Linie)
    zxy = (corner[0], corner[1])
    c = (zxy[0] - xl[0] * zul[0], zxy[1] - xl[1] * zul[0], FZ)
    m_po = mat(c, xl, (0, 0, 1))
    m_ps = mat((c[0], c[1], FZ + PODEST_H), xl, (0, 0, 1))
    zulauf = world(m_ps, zul)
    k60 = [rd(tip), rd(corner), rd((corner[0], corner[1], zulauf[2]))]
    booster, saug, druck = [], [], []
    for tag in ("A", "B"):
        sp = PSP["Saug " + tag]; s0 = world(m_ps, sp[1]); d = unit(wdir(m_ps, sp[2]))
        a1 = add(s0, d, L_SAUG1); zs = FZ + PG_SAUG[2]
        a2 = (a1[0], a1[1], zs); tipb = add(a2, d, L_SAUG2)
        xb = mul(d, -1)                                          # Booster: Saugstutzen (+X lokal) zeigt zum Schacht
        yb = (-xb[1], xb[0], 0.0)
        ob = sub(tipb, add(mul(xb, PG_SAUG[0]), mul(yb, PG_SAUG[1])))
        ob = (ob[0], ob[1], FZ)
        mb = mat(ob, xb, (0, 0, 1)); booster.append(mb)
        saug.append(dict(tag=tag, pfad=[rd(s0), rd(a1), rd(a2), rd(tipb)]))
        druck.append(world(mb, PG_DRUCK))
    nu = world(m_ps, PSP["Notueberlauf"][1]); nd = unit(wdir(m_ps, PSP["Notueberlauf"][2]))
    return dict(u=u, xl=xl, m_po=m_po, m_ps=m_ps, k60=k60, zulauf=zulauf, booster=booster, saug=saug, druck=druck, nu=nu, nd=nd, tank=e["tank"])

# ------------------------------------------------------------------ Belegung der Ringseiten (R1b): Feed-T, Ring-Ende, Entleerung, Kupplungshahn, Schellen
T75 = LT.ports("lt_t_d75")[1][1][0]                              # 86,4 halbe T-Laenge
RED75_63 = LT.ports("lt_reduzierung_d75_d63")[1][1][2]           # 87,5
HAHN63 = LT.ports("lt_kugelhahn_d63")[1][1][2]                   # 125
def feed_s(l, ein, belegt=()):
    """Seite und Lage des Einspeise-T: auf der Geraden der Seite, die dem Steigrohr am naechsten liegt (mindestens 350 mm von belegten Stellen)."""
    best = None
    for k in range(N):
        if seite_linie(k) != l: continue
        p0 = add(VX[k], U[k], EC["ecke_bis_port"] + T75 + 40); p1 = add(VX[k], U[k], SEITE - EC["ecke_bis_port"] - T75 - 40)
        for i in range(41):
            s = EC["ecke_bis_port"] + T75 + 40 + (L_GERADE - 2 * T75 - 80) * i / 40
            if any(kb == k and abs(sb - s) < 350 for kb, sb in belegt): continue
            p = seite_pt(k, s); d = math.hypot(p[0] - ein["riser_xy"][0], p[1] - ein["riser_xy"][1])
            if best is None or d < best[0]: best = (d, k, s)
    return best[1], best[2]

def ring_ende_ecken():
    """Ende jeder Linie an den Kupplungsseiten: (linie, ecke, seite_auf_der_linie, s, art)."""
    out = []
    for k in KUPPLUNG:
        a, b = k, (k + 1) % N                                     # Kupplungsseite k zwischen Ecke a und b
        la = 1 if a in LINIE_ECKEN[1] else 2; lb = 1 if b in LINIE_ECKEN[1] else 2
        out.append((la, a, (a - 1) % N))                           # Linie la endet an Ecke a; ihre letzte eigene Seite ist a-1
        out.append((lb, b, b))                                     # Linie lb beginnt an Ecke b mit Seite b
    return out

def seiten_belegung(feeds):
    """Je Seite: Liste der In-Line-Teile [(s_mitte, art, info)] auf der Geraden; s ab Ecke k."""
    bel = {k: [] for k in range(N)}
    for l, (k, s) in feeds.items(): bel[k].append((s, "feed", dict(linie=l)))
    enden = ring_ende_ecken(); done = set()
    for l, ecke, k in enden:
        art = "ringende" if (l, "ringende") not in done else "entleerung"
        done.add((l, art))
        s = (SEITE - EC["ecke_bis_port"] - T75 - 30) if k == (ecke - 1) % N else (EC["ecke_bis_port"] + T75 + 30)
        bel[k].append((s, art, dict(linie=l, ecke=ecke)))
    for k in KUPPLUNG: bel[k].append((SEITE / 2, "kupplung", {}))
    return bel

def leitungen_eintraege():
    """Alle Trassen/T/R-Stuecke der Autobahn (ring_b2). Rueckgabe dict wie leitungstrassen.json (nur die Listen)."""
    tr, ts, rs, te = [], [], [], []
    base = dict(varianten=V, quelle=QUELLE)
    ein = {l: einspeisung(l) for l in (1, 2)}
    # ---- Einspeisung je Linie: K60 (Biofilter -> Schacht), Saug K61/K62, Druck -> Rueckschlagventil -> T -> Steigleitung K63, Notueberlauf K67
    for l, e in ein.items():
        kz = {1: dict(k60="K60", k61="K61", k62="K62", k63="K63", k67="K67"), 2: dict(k60="K68", k61="K69", k62="K70", k63="K71", k67="K75")}[l]
        tr.append(dict(id=f"RB{l}-K60", kante=kz["k60"], dn=50, farbe="dunkelblau", start="stutzen", ende="muffe", pfad=e["k60"], linie=l,
                       korridor=["KT", "KT"], notiz=f"Biofilter-Ueberlauf ({e['tank']}) frei fallend in den Pegelschacht: Bogen 90 d50 auf dem Ende von {EINSP[l]['kante']}, senkrecht in die Zulauf-Muffe im Fassdeckel (Z {e['zulauf'][2] - FZ:.0f} rel)", **base))
        for sg, kn in zip(e["saug"], (kz["k61"], kz["k62"])):
            tr.append(dict(id=f"RB{l}-{kn}", kante=kn, dn=50, farbe="dunkelblau", start="muffe", ende="stutzen", pfad=sg["pfad"], linie=l, korridor=["KT"] * 3,
                           notiz=f"Pegelschacht Saugstutzen {sg['tag']} -> waagerecht {L_SAUG1:g} -> senkrecht auf Saughoehe -> waagerecht {L_SAUG2:g} in den Saugstutzen Booster {l}{sg['tag'].lower()} (geflutet)", **base))
        # Druck: d40-Stutzen -> Kupplung -> Rohr d40 -> Reduziermuffe d50/d40 -> Rohr d50 -> Rueckschlagventil d50 (WA8) -> Rohr d50 -> Bogen -> T d63
        dA, dB = e["druck"]
        m = ((dA[0] + dB[0]) / 2, (dA[1] + dB[1]) / 2)
        lred = LT.ports("lt_reduzierung_d50_d40")[1][1][2]; lrsv = TEILE["wa_s"]["teile"]["lt_rueckschlagventil_d50"]["laenge"]
        zq1 = dA[2] + 120; za_red = zq1 + lred; zr_a = za_red + 60; zr_b = zr_a + lrsv
        zj = zr_b + 200
        tb = (m[0], m[1], zj); tbid = f"RB{l}-TB"
        for i, (dd, tag) in enumerate(((dA, "a"), (dB, "b"))):
            rid, vid = f"RB{l}-RED{tag}", f"RB{l}-RSV{tag}"
            tr.append(dict(id=f"RB{l}-D{tag}1", kante=kz["k63"], dn=40, farbe="dunkelblau", start="stutzen", ende="r:" + rid, pfad=[rd(dd), rd((dd[0], dd[1], zq1))], linie=l, korridor=["KT"],
                           notiz=f"Druckstutzen Booster {l}{tag} d40 -> Kupplung -> Reduziermuffe d50/d40", **base))
            rs.append(dict(id=rid, pos_a=rd((dd[0], dd[1], za_red)), dir=[0.0, 0.0, -1.0], d_gross=50, d_klein=40, linie=l, notiz="Reduziermuffe d50/d40 auf dem Booster-Druckrohr", **base))
            tr.append(dict(id=f"RB{l}-D{tag}2", kante=kz["k63"], dn=50, farbe="dunkelblau", start="r:" + rid, ende="r:" + vid, pfad=[rd((dd[0], dd[1], za_red)), rd((dd[0], dd[1], zr_a))], linie=l, korridor=["KT"],
                           notiz="Rohr d50 zum Rueckschlagventil", **base))
            rs.append(dict(id=vid, art="teil", datei="lt_rueckschlagventil_d50", pos_a=rd((dd[0], dd[1], zr_a)), dir=[0.0, 0.0, 1.0], d_gross=50, linie=l,
                           notiz=f"Rueckschlagventil d50 (WA8, GF 562) hinter Booster {l}{tag}", **base))
            tr.append(dict(id=f"RB{l}-D{tag}3", kante=kz["k63"], dn=50, farbe="dunkelblau", start="r:" + vid, ende="t:" + tbid,
                           pfad=[rd((dd[0], dd[1], zr_b)), rd((dd[0], dd[1], zj)), rd(tb)], linie=l, korridor=["KT", "KT"], notiz="Rueckschlagventil -> Bogen -> T d63 der Steigleitung", **base))
        # Steigleitung d63 (K63): T -> senkrecht auf Ringachse -> waagerecht parallel zur Seite -> senkrecht zur Seite in den Ring-T
        e["riser_xy"] = m
    feeds = {}
    belegt = [(k, s) for k, b in seiten_belegung({}).items() for s, _, _ in b]
    for l, e in ein.items():
        k, s = feed_s(l, e, belegt); feeds[l] = (k, s)
    bel = seiten_belegung(feeds)
    for l, e in ein.items():
        k, s = feeds[l]; p = seite_pt(k, s); nl = NL[k]
        m = e["riser_xy"]; za = Z["achse"]
        off = dot(sub((m[0], m[1], 0), (p[0], p[1], 0)), nl)       # Abstand Steigrohr zur Ringseite (+ = zur Mitte)
        q = add(p, nl, off)                                       # Punkt auf der Normalen des Ring-T auf Hoehe des Steigrohrs
        tbid = f"RB{l}-TB"; trid = f"RB{l}-TR"
        kz63 = "K63" if l == 1 else "K71"
        tr.append(dict(id=f"RB{l}-K63", kante=kz63, dn=63, farbe="dunkelblau", start="t:" + tbid, ende="t:" + trid,
                       pfad=[rd((m[0], m[1], e["druck"][0][2] + 0) if False else (m[0], m[1], 0)), rd((m[0], m[1], za)), rd((q[0], q[1], za)), rd(p)], linie=l, korridor=["KT", "KR", "KR"],
                       notiz=f"Steigleitung d63: T der Booster -> senkrecht auf Ringachse Z {za - FZ:.0f} rel -> parallel zur Ringseite -> senkrecht in den Einspeise-T d75", **base))
        tr[-1]["pfad"][0] = rd([t for t in tr if t["id"] == f"RB{l}-Da3"][0]["pfad"][-1])
        ts.append(dict(id=tbid, pos=tr[-1]["pfad"][0], d=63, ports=[dict(trasse=f"RB{l}-Da3", ende="ende", d=50), dict(trasse=f"RB{l}-Db3", ende="ende", d=50), dict(trasse=f"RB{l}-K63", ende="start", d=63)],
                       linie=l, notiz="T d63: zwei Booster-Druckleitungen d50 vereinigt, Abgang Steigleitung nach oben", **base))
        # Notueberlauf K67/K75: Stutzen -X -> waagerecht -> senkrecht auf Flur (offenes Ende ueber der Ruecklauf-Anbindung, Befund)
        nu, nd = e["nu"], e["nd"]; n1 = add(nu, nd, 200)
        tr.append(dict(id=f"RB{l}-K67", kante="K67" if l == 1 else "K75", dn=63, farbe="grau", start="muffe", ende="offen", pfad=[rd(nu), rd(n1), rd((n1[0], n1[1], FZ + 60))], linie=l, korridor=["KT", "KT"],
                       notiz="Notueberlauf d63 des Pegelschachts (Booster-Stillstand) -> senkrecht auf Flur; Anschluss an den Ruecklauf OFFEN (Montage R2c / Planer)", **base))
    # ---- Ring: je Seite die Gerade zwischen Port B der Ecke k und Port A der Ecke k+1, In-Line-Teile nach Belegung
    for k in range(N):
        s_a, s_b = EC["ecke_bis_port"], SEITE - EC["ecke_bis_port"]
        items = sorted(bel[k], key=lambda x: x[0])
        cur, cur_start = s_a, "offen"; n = 0; lin = seite_linie(k)
        def rohr(s0, start, s1, ende, note):
            nonlocal n
            n += 1
            tr.append(dict(id=f"RB-S{k}-{n}", kante="K76" if lin == 0 else ("K64" if lin == 1 else "K72"), dn=75, farbe="dunkelblau", start=start, ende=ende, halter=False,
                           pfad=[rd(seite_pt(k, s0)), rd(seite_pt(k, s1))], linie=lin, korridor=["KR"], notiz=note, **base))
        for s, art, info in items:
            if art in ("feed", "ringende", "entleerung"):
                tid = f"RB-T{k}-{art}"
                rohr(cur, cur_start, s, "t:" + tid, f"Ring d75 Seite {k} bis {art}-T")
                p = seite_pt(k, s)
                if art == "feed":
                    l = info["linie"]; branch = f"RB{l}-K63"; bd = 63
                    ts.append(dict(id=tid, pos=rd(p), d=75, ports=[dict(trasse=f"RB-S{k}-{n}", ende="ende", d=75), dict(trasse=f"RB-S{k}-{n + 1}", ende="start", d=75), dict(trasse=branch, ende="ende", d=63)],
                                   linie=l, notiz=f"Einspeise-T d75 der Linie {l} (Steigleitung d63 von der Seite)", **base))
                    for t_ in tr:
                        if t_["id"] == branch: t_["ende"] = "t:" + tid
                else:
                    l = info["linie"]; bid = f"RB-T{k}-{art}-ab"; hid = f"RB-H{k}-{art}"
                    zt = p[2] - T75 - 2 * LT.DEPTH[75] - RED75_63 - 60          # Hahn-Muffe A unter dem Abzweig
                    ts.append(dict(id=tid, pos=rd(p), d=75, ports=[dict(trasse=f"RB-S{k}-{n}", ende="ende", d=75), dict(trasse=f"RB-S{k}-{n + 1}", ende="start", d=75), dict(trasse=bid, ende="start", d=63)],
                                   linie=l, notiz=("Ring-Ende" if art == "ringende" else "Entleerung") + f" der Linie {l}: T d75, Abgang nach unten d63", **base))
                    tr.append(dict(id=bid, kante=("K66" if l == 1 else "K74") if art == "ringende" else None, dn=63, farbe="dunkelblau", start="t:" + tid, ende="r:" + hid,
                                   pfad=[rd(p), rd((p[0], p[1], zt))], linie=l, korridor=["KR"], halter=False, notiz="Abgang d63 zum Kugelhahn", **base))
                    rs.append(dict(id=hid, art="kugelhahn", pos_a=rd((p[0], p[1], zt)), dir=[0.0, 0.0, -1.0], d_gross=63, d_klein=63, linie=l,
                                   notiz=("Ring-Ende-Hahn d63 (Ueberschuss in den Ruecklauf, ersetzt K13/K29)" if art == "ringende" else "Entleerungshahn d63 (Ring leer, Frost)") + f" Linie {l}", **base))
                    tr.append(dict(id=hid + "-ab", kante=("K66" if l == 1 else "K74") if art == "ringende" else None, dn=63, farbe="grau", start="r:" + hid, ende="offen",
                                   pfad=[rd((p[0], p[1], zt - HAHN63)), rd((p[0], p[1], zt - HAHN63 - 150))], linie=l, korridor=["KR"], halter=False,
                                   notiz="Auslauf unter dem Hahn; Anschluss an den Ruecklauf OFFEN (R2c / Planer)", **base))
                cur, cur_start = s, "t:" + tid
            elif art == "kupplung":
                ra, h_, rb = f"RB-K{k}-RA", f"RB-K{k}-H", f"RB-K{k}-RB"
                lr = RED75_63; gap = 2 * LT.DEPTH[63] + 10
                s_h0 = s - HAHN63 / 2; s_h1 = s + HAHN63 / 2
                s_ra = s_h0 - gap - lr; s_rb = s_h1 + gap + lr
                rohr(cur, cur_start, s_ra, "r:" + ra, "Ring d75 bis Reduziermuffe der Kupplungsstrecke")
                rs.append(dict(id=ra, pos_a=rd(seite_pt(k, s_ra)), dir=rd(U[k], 6), d_gross=75, d_klein=63, linie=0, notiz="Reduziermuffe d75/d63 vor dem Kupplungshahn", **base))
                tr.append(dict(id=f"RB-K{k}-a", kante="K76", dn=63, farbe="dunkelblau", start="r:" + ra, ende="r:" + h_, pfad=[rd(seite_pt(k, s_ra + lr)), rd(seite_pt(k, s_h0))], linie=0, korridor=["KR"], halter=False, notiz="Rohrstueck d63", **base))
                rs.append(dict(id=h_, art="kugelhahn", pos_a=rd(seite_pt(k, s_h0)), dir=rd(U[k], 6), d_gross=63, d_klein=63, linie=0, normal="zu",
                               notiz="Kupplungshahn d63 zwischen den Linien (K76), im Betrieb geschlossen", **base))
                tr.append(dict(id=f"RB-K{k}-b", kante="K76", dn=63, farbe="dunkelblau", start="r:" + h_, ende="r:" + rb, pfad=[rd(seite_pt(k, s_h1)), rd(seite_pt(k, s_rb - lr))], linie=0, korridor=["KR"], halter=False, notiz="Rohrstueck d63", **base))
                rs.append(dict(id=rb, pos_a=rd(seite_pt(k, s_rb)), dir=rd(mul(U[k], -1), 6), d_gross=75, d_klein=63, linie=0, notiz="Reduziermuffe d63/d75 hinter dem Kupplungshahn", **base))
                cur, cur_start = s_rb, "r:" + rb
        rohr(cur, cur_start, s_b, "offen", f"Ring d75 Seite {k} bis Ecke {(k + 1) % N}")
    return dict(trassen=tr, t_stuecke=ts, r_stuecke=rs, teile=te), ein, feeds, bel

# ------------------------------------------------------------------ Schellen (R6 Ring <= 1000 mm): Scheitel jeder Ecke + je Seite auf der Geraden
def schellen(bel):
    out = []
    for k in range(N):
        sp = stp_by_k()[k]
        p, t = bogen_pt(k, 0.0)
        out.append(("lt_klemme_d75_stelze" if sp["art"] == "stelze" else "lt_klemme_d75_ecke", mat(p, t, (0, 0, 1)), k, "scheitel"))
    for k in range(N):
        frei = [EC["ecke_bis_port"] + 40, SEITE - EC["ecke_bis_port"] - 40]
        belegt = [(s - 115, s + 115) if a != "kupplung" else (s - 260, s + 260) for s, a, _ in bel[k]]
        cand = [SEITE / 2 + d for d in (0, -60, 60, -120, 120, -180, 180, -240, 240, -280, 280)]
        s = next(c for c in cand if frei[0] <= c <= frei[1] and all(not (a <= c <= b) for a, b in belegt))
        out.append(("lt_klemme_d75", mat(seite_pt(k, s), U[k], (0, 0, 1)), k, s))
    return out

_STP = None
def stp_by_k():
    global _STP
    if _STP is None: _STP = {s["k"]: s for s in stuetzpunkte()}
    return _STP

# ------------------------------------------------------------------ Tragwerk-Instanzen fuer gen_dome.ring_b2()
def comp(n): return os.path.join(COMP, n + ".sc")
def tragwerk(runde="r1"):
    out = []
    eint, ein, feeds, bel = leitungen_eintraege()
    sp = stuetzpunkte()
    jo = {}
    for s in sp:
        if s["art"] == "joch": jo.setdefault(s["teil"], []).append(s["matrix"])
    for t, ms in sorted(jo.items()): out.append((klasse(t), comp(t), ms, "09_Technik"))
    out.append(("Ringstuetze_d75_B", comp("ringstuetze_d75_b"), [s["matrix"] for s in sp if s["art"] == "stelze"], "09_Technik"))
    sch = [mat((seite_pt(k, (SEITE - TW["teile"]["montageschiene_41_2179"]["parameter"]["laenge"]) / 2)[0], seite_pt(k, (SEITE - TW["teile"]["montageschiene_41_2179"]["parameter"]["laenge"]) / 2)[1], Z["schiene_u"]), U[k], (0, 0, 1)) for k in range(N)]
    out.append(("Montageschiene_41_2179", comp("montageschiene_41_2179"), sch, "09_Technik"))
    out.append(("Schienenverbinder_36", comp("schienenverbinder_36"), [mat((VX[k][0], VX[k][1], Z["schiene_o"]), U[(k - 1) % N], (0, 0, 1)) for k in range(N)], "09_Technik"))
    kl = {}
    for f, m, k, s in schellen(bel): kl.setdefault(f, []).append(m)
    for f, ms in sorted(kl.items()): out.append((klasse(f), comp(f), ms, "08_Leitungen"))
    out.append(("Ring_Ecke_d75", comp("ring_ecke_d75"), [ecke_matrix(k) for k in range(N)], "08_Leitungen"))
    out.append(("Pegelschacht_Podest", comp("pegelschacht_podest"), [ein[l]["m_po"] for l in (1, 2)], "09_Technik"))
    out.append(("Pegelschacht", comp("pegelschacht"), [ein[l]["m_ps"] for l in (1, 2)], "09_Technik"))
    out.append(("Booster_gross", comp("pumpe_gross"), [m for l in (1, 2) for m in ein[l]["booster"]], "09_Technik"))
    out.append(("Entluefter_d75", comp("entluefter_d75"), entluefter(), "08_Leitungen"))
    if runde in ("r2",):
        au = {}
        for s in sp:
            for seite, (o, d, lg) in s["ausleger"].items(): au.setdefault(lg, []).append(ausleger_matrix(o, d))
        for lg, ms in sorted(au.items()): out.append((f"Ausleger_Schlauch_{lg}", comp(f"ausleger_schlauch_{lg}"), ms, "09_Technik"))
    return out

def entluefter():
    """Je Linie ein Entluefter d75 am Linien-Ende (Bogen der End-Ecke, 450 mm hinter dem Bogenanfang: dort liegt das Rohr seitlich neben der Schiene)."""
    ms = []
    for l, ecke, k in ring_ende_ecken():
        if (l, ecke) not in ENTL: continue
        sgn = -1 if k == (ecke - 1) % N else 1
        p, t = bogen_pt(ecke, sgn * (EC["bogen_l"] / 2 - 450))
        ms.append(mat(p, t, (0, 0, 1)))
    return ms
ENTL = set()
def _entl_init():
    seen = set()
    for l, ecke, k in ring_ende_ecken():
        if l not in seen: ENTL.add((l, ecke)); seen.add(l)
_entl_init()

def klasse(fname): return "_".join(x if x[:1] == "d" and x[1:2].isdigit() else x.capitalize() for x in fname.split("_"))

# ------------------------------------------------------------------ Schreiben und Bericht
def schreiben():
    eint = leitungen_eintraege()[0]
    p = os.path.join(ROOT, "data", "leitungstrassen.json")
    doc = json.load(open(p, encoding="utf-8"))
    for key in ("trassen", "t_stuecke", "r_stuecke", "teile"):
        doc[key] = [e for e in doc.get(key, []) if e.get("quelle") != QUELLE] + eint[key]
    json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("geschrieben:", {k: len(v) for k, v in eint.items()})

def bericht():
    eint, ein, feeds, bel = leitungen_eintraege()
    sp = stuetzpunkte()
    print("Ring: Apothem %.0f, Eckradius %.1f, Seite %.1f, Gerade je Seite %.1f mm" % (AP, RE, SEITE, L_GERADE))
    print("Linie 1 Ecken", [ECKEN_AZ[k] for k in LINIE_ECKEN[1]], "| Linie 2", [ECKEN_AZ[k] for k in LINIE_ECKEN[2]], "| Kupplungsseiten", [(ECKEN_AZ[k], ECKEN_AZ[(k + 1) % N]) for k in KUPPLUNG])
    print("Stuetzpunkte: %d Joche, %d Stelzen; Ausleger %d" % (sum(s["art"] == "joch" for s in sp), sum(s["art"] == "stelze" for s in sp), sum(len(s["ausleger"]) for s in sp)))
    for l in (1, 2):
        e = ein[l]; c = world(e["m_po"], (0, 0, 0))
        print("Einspeisung Linie %d: Pegelschacht r %.0f az %.1f, Zulauf Z %.0f rel, Feed-T Seite %d s %.0f" % (l, math.hypot(c[0], c[1]), az(c), e["zulauf"][2] - FZ, feeds[l][0], feeds[l][1]))
    kl = schellen(bel)
    print("Schellen:", len(kl))
    print({k: len(v) for k, v in eint.items()})

if __name__ == "__main__":
    if "--schreiben" in sys.argv: schreiben()
    if "--bericht" in sys.argv or len(sys.argv) == 1: bericht()
