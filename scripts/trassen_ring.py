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
def _bestand(datei="dome-script-ring_b2.json"):
    """U6: Lage aus dem Bauskript der Variante ring_b2 (Beete auf dem Flur, Technik am Bauplatz der Lage-Probe; Tische wie A+)."""
    cmds = json.load(open(os.path.join(ROOT, "scripts", datei), encoding="utf-8"))["commands"]
    return {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
MV = _bestand()
MV_APLUS = _bestand("dome-script.json")
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
        sp = dot(sub((ein["riser_xy"][0], ein["riser_xy"][1], VX[k][2]), VX[k]), U[k])           # U6: Fusspunkt des Lots (gerade Einspeisung ohne Versatz), wenn frei
        lo, hi = EC["ecke_bis_port"] + T75 + 40, SEITE - EC["ecke_bis_port"] - T75 - 40
        if lo <= sp <= hi and not any(kb == k and abs(sb - sp) < 350 for kb, sb in belegt):
            d = math.hypot(*(sub(seite_pt(k, sp), (ein["riser_xy"][0], ein["riser_xy"][1], VX[k][2]))[:2]))
            if d < best[0] + 1.0: best = (d - 1.0, k, sp)
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

# ------------------------------------------------------------------ U6 Einspeisung (Quelle e25/e26): Ueberlauf-Stutzen d63 des Biofilters (Lage aus dem A+-Stutzen R_UEB/R_UEB2, mit dem Tank gedreht)
L_EIN = 250.0                                                     # [A] waagerechtes Stueck ab Stutzen, dann Bogen 90 nach unten
def _inv_world(m, p):
    q = sub(p, (m[3], m[7], m[11])); return tuple(m[r] * q[0] + m[4 + r] * q[1] + m[8 + r] * q[2] for r in range(3))
def _inv_dir(m, d): return tuple(m[r] * d[0] + m[4 + r] * d[1] + m[8 + r] * d[2] for r in range(3))
def einspeisung_u6(l):
    tank = {1: "Tank_gross:1", 2: "Tank_gross_t3:1"}[l]; rid = {1: "R_UEB", 2: "R_UEB2"}[l]
    r = [x for x in TRASSEN["r_stuecke"] if x["id"] == rid][0]
    ma, mb = MV_APLUS[tank], MV[tank]
    p0 = world(mb, _inv_world(ma, tuple(r["pos_a"]))); u = unit(wdir(mb, _inv_dir(ma, tuple(r["dir"]))))
    p1 = add(p0, u, L_EIN)
    return dict(p0=p0, u=u, p1=p1, tank=tank, riser_xy=(p1[0], p1[1]))

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
    ein = {l: einspeisung_u6(l) for l in (1, 2)}
    # ---- U6 (D93, Quelle e25/e26): Ueberlauf d63 des Biofilters -> waagerecht aus dem Tank -> senkrecht auf die Ringachse -> in den Einspeise-T d75.
    #      Pegelschacht, Booster, Rueckschlagventile und Notueberlauf des Schachts (V2: K60 bis K67, K68 bis K75) entfallen (D101).
    feeds = {}
    belegt = [(k, s) for k, b in seiten_belegung({}).items() for s, _, _ in b]
    for l, e in ein.items():
        k, s = feed_s(l, e, belegt); feeds[l] = (k, s)
    bel = seiten_belegung(feeds)
    for l, e in ein.items():
        k, s = feeds[l]; p = seite_pt(k, s); nl = NL[k]; za = Z["achse"]
        sp = dot(sub((e["p1"][0], e["p1"][1], VX[k][2]), VX[k]), U[k])
        if abs(s - sp) < 30.0:                                           # Fusspunkt knapp ausserhalb des freien Bereichs: Fallrohr um (s - sp) entlang der Seite versetzen (Knick < 7 Grad am Stutzen-Bogen? nein: nur der waagerechte Ast dreht < 0,5 Grad)
            e["p1"] = add(e["p1"], U[k], s - sp); e["riser_xy"] = (e["p1"][0], e["p1"][1])
        m = e["riser_xy"]
        off = dot(sub((m[0], m[1], 0), (p[0], p[1], 0)), nl)
        q = add(p, nl, off)
        pfad = [rd(e["p0"]), rd(e["p1"]), rd((m[0], m[1], za))]
        if math.hypot(q[0] - m[0], q[1] - m[1]) > 1.0: pfad.append(rd((q[0], q[1], za)))
        pfad.append(rd(p))
        kz = "K63" if l == 1 else "K71"
        tr.append(dict(id=f"RB{l}-K63", kante=kz, soll_weg="e25" if l == 1 else "e26", dn=63, farbe="dunkelblau", start="offen", ende="t:RB-T%d-feed" % k,
                       pfad=pfad, linie=l, korridor=["KT"] * (len(pfad) - 1),
                       notiz=f"Einspeisung d63 (Quelle e25/e26): Ueberlauf {e['tank']} auf Z {e['p0'][2] - FZ:.0f} rel -> waagerecht {L_EIN:g} -> senkrecht auf die Ringachse Z {za - FZ:.0f} rel -> in den Einspeise-T d75 (Schwerkraft, Gefaelle {e['p0'][2] - za:.0f} mm)", **base))
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
                    if art == "ringende": tr[-1]["soll_weg"] = "e31" if l == 1 else "e32"
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
                tr.append(dict(id=f"RB-K{k}-a", kante="K76", soll_weg=["e27", "e30"], dn=63, farbe="dunkelblau", start="r:" + ra, ende="r:" + h_, pfad=[rd(seite_pt(k, s_ra + lr)), rd(seite_pt(k, s_h0))], linie=0, korridor=["KR"], halter=False, notiz="Rohrstueck d63", **base))
                rs.append(dict(id=h_, art="kugelhahn", pos_a=rd(seite_pt(k, s_h0)), dir=rd(U[k], 6), d_gross=63, d_klein=63, linie=0, normal="offen", soll_weg=["e27", "e28", "e29", "e30"],
                               notiz="Kupplungshahn d63 zwischen den Linien (K76), im Betrieb OFFEN (Quelle A29, U6); schliessen nur zur Wartung einer Linie", **base))
                tr.append(dict(id=f"RB-K{k}-b", kante="K76", soll_weg=["e28", "e29"], dn=63, farbe="dunkelblau", start="r:" + h_, ende="r:" + rb, pfad=[rd(seite_pt(k, s_h1)), rd(seite_pt(k, s_rb - lr))], linie=0, korridor=["KR"], halter=False, notiz="Rohrstueck d63", **base))
                rs.append(dict(id=rb, pos_a=rd(seite_pt(k, s_rb)), dir=rd(mul(U[k], -1), 6), d_gross=75, d_klein=63, linie=0, notiz="Reduziermuffe d63/d75 hinter dem Kupplungshahn", **base))
                cur, cur_start = s_rb, "r:" + rb
        rohr(cur, cur_start, s_b, "offen", f"Ring d75 Seite {k} bis Ecke {(k + 1) % N}")
    for t in tr:                                                   # U6: Hoehenband (Ring 1550 liegt im Band WH 0..2100 rel) und Bezug zur Quelle (Bauteil oder Weg)
        t.setdefault("band", "WH")
        if "soll_weg" not in t: t["soll_bauteil"] = "kupplungshahn" if t.get("linie") == 0 else ("ring_1" if t.get("linie") == 1 else "ring_2")
        if t["id"].startswith("RB-K") and t["dn"] == 63: t["dn_abweichung"] = "Kupplungsstrecke d63 mit Kugelhahn d63 im Ring d75 (Quelle e27 bis e30: 'd63 (Kugelhahn), Ring d75')"
        if t["id"].endswith("-K63"): t["anschluss"] = [ein[t["linie"]]["tank"]]                  # beginnt am Ueberlauf-Stutzen des Biofilters
    return dict(trassen=tr, t_stuecke=ts, r_stuecke=rs, teile=te), ein, feeds, bel

# ------------------------------------------------------------------ Schellen (R6 Ring <= 1000 mm): Scheitel jeder Ecke + je Seite auf der Geraden
def _s_schelle():
    """Lage der Eck-Schelle je Ecke (Bogenlaenge ab Scheitel): im Scheitel; haengt an der Ecke ein Mitte-Abnehmer, sitzt dort der Beet-Abzweig, die Schelle rueckt zur Seite davor."""
    mit = {_ecke_idx(math.degrees(math.atan2(m[7], m[3])) - 18.0) for n, m in MV.items() if n.split(":")[0] in ("Tisch_mitte", "Beet_innen_933")}
    return {k: (-(T75 + 5.0 + 25.0) if k in mit else 0.0) for k in range(N)}
S_SCHELLE = _s_schelle()

def schellen(bel):
    out = []
    for k in range(N):
        sp = stp_by_k()[k]
        p, t = bogen_pt(k, S_SCHELLE[k]) if sp["art"] == "joch" else bogen_pt(k, 0.0)
        out.append(("lt_klemme_d75_stelze" if sp["art"] == "stelze" else "lt_klemme_d75_ecke", mat(p, t, (0, 0, 1)), k, "scheitel"))
    for k in range(N):                                                    # je Seite zwei Schellen an der Schiene (Gerade 609..1585 ab Ecke): Laufabstand Scheitel-Schelle zu Schelle <= 1000
        t0 = EC["tangente"] + 20; t1 = SEITE - EC["tangente"] - 20
        belegt = [(s - 115, s + 115) if a != "kupplung" else (s - 260, s + 260) for s, a, _ in bel[k]]
        for ziel in (EC["tangente"] + 250, SEITE - EC["tangente"] - 250):
            cand = sorted((ziel + d for d in range(-230, 231, 5)), key=lambda c: abs(c - ziel))
            s = next(c for c in cand if t0 <= c <= t1 and all(not (a <= c <= b) for a, b in belegt))
            belegt.append((s - 40, s + 40))
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
    # U6 (D101): Pegelschacht samt Podest und Booster entfallen; die Einspeisung ist der Ueberlauf d63 des Biofilters (Trasse RB<l>-K63)
    out.append(("Entluefter_d75", comp("entluefter_d75"), entluefter(), "08_Leitungen"))
    if runde in ("r2",):
        au = {}
        for s in sp:
            for seite, (o, d, lg) in s["ausleger"].items(): au.setdefault(lg, []).append(ausleger_matrix(o, d))
        for lg, ms in sorted(au.items()): out.append((f"Ausleger_Schlauch_{lg}", comp(f"ausleger_schlauch_{lg}"), ms, "09_Technik"))
        fl = fallleitungen()
        for dk in (40, 32):
            out.append((f"Ring_Abzweig_d{dk}", comp(f"ring_abzweig_d{dk}"), [f["m_t"] for f in fl if f["dk"] == dk], "08_Leitungen"))
        out.append(("Ring_B2_Schlauchwege", comp(SCHLAUCH_DATEI), [[1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]], "08_Leitungen"))
    return out

# ================================================================== R2: 38 Abzweige und Schlauch-Fallleitungen
import autobahn_s as AS
SCHLAUCH_DATEI = "ring_b2_schlauchwege"   # neuer Name: alte 622-MB-Definition ring_b2_schlaeuche blieb im Viewer gesperrt
ZONE = {"Tisch_innen": ("innen", "tisch"), "Tisch_mitte": ("mitte", "tisch"), "Tisch_aussen": ("aussen", "tisch"), "Beet_innen_933": ("mitte", "beet"), "Beet_aussen_800": ("aussen", "beet")}
PORT = {"Tisch_innen": ((-449.0, 256.0, 1306.0), "t"), "Tisch_mitte": ((-823.0, 520.0, 963.0), "t"), "Tisch_aussen": ((-1349.0, 497.0, 1121.0), "t"),
        "Beet_innen_933": ((-973.0, -298.0, 395.0), "b"), "Beet_aussen_800": ((-1360.0, -326.0, 435.0), "b")}   # U6: gemessen an viewer/detail/nft_tisch_*.json (Verteiler-Mitte, U3: +230/-120/+30) und ibc_beet_*.json (Tropfrohr, U3b: Rand - 25)
LINIE1_SEKT = (0, 36, 72, 108); LINIE2_SEKT = (144, 180, -144, -108); INNEN_EXTRA = {1: -36, 2: -72}   # wie scripts/n_autobahn_rechnung.py (Blatt 1.5)
Y_CLIP = [v for k, v in TW["teile"].items() if k.startswith("ausleger_schlauch_")][0]["ports"][1]["lage"][1]   # 42,5 seitlich der Armachse (gleich fuer alle Laengen)
T_HALB = T75 + 5.0                                                       # T-Laenge/2 + Luft
def _sekt(a): a = round(a); a = (a + 180) % 360 - 180; return 180 if a == -180 else a

def abnehmer():
    out = []
    for n, m in sorted(MV.items()):
        cls = n.split(":")[0]
        if cls not in ZONE: continue
        zone, art = ZONE[cls]; a = _sekt(math.degrees(math.atan2(m[7], m[3])))
        l = 1 if (a in LINIE1_SEKT or (zone == "innen" and a == INNEN_EXTRA[1])) else 2 if (a in LINIE2_SEKT or (zone == "innen" and a == INNEN_EXTRA[2])) else 0
        if not l: continue
        k = _ecke_idx(math.degrees(math.atan2(m[7], m[3])) - 18.0)
        pl, typ = PORT[cls]
        if typ == "t": d_o = unit(wdir(m, (math.tan(math.radians(18.0)), 1.0, 0.0)))   # Oeffnung +Y, 18 Grad geneigt (Sektorgrenze)
        else: d_o = unit(wdir(m, (-1.0, 0.0, 0.0)))
        out.append(dict(name=n, cls=cls, zone=zone, art=art, linie=l, k=k, port=world(m, pl), d_o=(d_o[0], d_o[1], 0.0), idd=25 if art == "beet" else 19, dk=40 if art == "beet" else 32))
    return out

def ring_pt(k, s):
    """Ringachse bei Ecke k, s = Lauflaenge ab Scheitel (+ Richtung Seite k); jenseits des Bogens auf der Geraden."""
    hb = EC["bogen_l"] / 2
    if abs(s) <= hb: return bogen_pt(k, s)
    p, t = bogen_pt(k, math.copysign(hb, s)); return add(p, t, s - math.copysign(hb, s)), t

def _s_lateral(k, o, x, lam):
    """s auf dem Ring der Ecke k, an dem der Abstand zur Linie (o, Richtung senkrecht x) entlang x gleich lam ist (Bisektion)."""
    f = lambda s: dot(sub(ring_pt(k, s)[0], o), x) - lam
    lo, hi = -1300.0, 1300.0
    if f(lo) > f(hi): lo, hi = hi, lo
    for _ in range(60):
        mid = (lo + hi) / 2
        if f(mid) < 0: lo = mid
        else: hi = mid
    return (lo + hi) / 2

def _jog_min(idd): return 2 * AS.hose_R(idd) * math.tan(math.radians(22.5)) / math.sqrt(2) + 2.0

_FL = None
def fallleitungen():
    """Je Abnehmer: Lage des Abzweigs (Matrix m_t), Ausleger-Zuordnung und Schlauchweg (Weltpunkte). Platzierung je Ecke ohne Ueberlappung der T-Stuecke,
    ohne Scheitel-Schelle und Entluefter; Schlauch auf dem Ausleger in der Clip-Linie (seitlicher 45-Grad-Versatz, wenn der Abzweig daneben sitzt)."""
    global _FL
    if _FL is not None: return _FL
    ab = abnehmer(); stp = stp_by_k(); out = []
    sperr = {}
    for k in range(N): sperr[k] = [(S_SCHELLE[k] - 15.0, S_SCHELLE[k] + 15.0)]          # Scheitel-Schelle ring_b 30
    _, _, _, bel = leitungen_eintraege()
    hb = EC["bogen_l"] / 2; tg = EC["tangente"]
    def _sperr_seite(k, d, halb):                                             # Lage auf Seite k (ab Ecke k) in die Lauflaenge beider Ecken umrechnen
        sperr[k].append((d - tg + hb - halb, d - tg + hb + halb)); k2 = (k + 1) % N; d2 = SEITE - d
        sperr[k2].append((-(d2 - tg + hb) - halb, -(d2 - tg + hb) + halb))
    for f, m, k, sl in schellen(bel):
        if sl != "scheitel": _sperr_seite(k, sl, 15.0 + 5.0)
    for k in range(N):
        for sl, art, _ in bel[k]: _sperr_seite(k, sl, (T75 + 10.0) if art != "kupplung" else 260.0)
    for m in entluefter():
        p = (m[3], m[7], m[11]); k = min(range(N), key=lambda i: math.dist(p, bogen_pt(i, 0)[0]))
        s = min((x for x in range(-700, 701, 2)), key=lambda x: math.dist(ring_pt(k, x)[0], p)); sperr[k].append((s - 2 * T_HALB, s + 2 * T_HALB))
    for k in range(N):
        sp = stp[k]; belegt = list(sperr[k]); liste = [a for a in ab if a["k"] == k]
        # Clip-Seite: Tisch links (+y), Beet rechts (-y); allein auf dem Ausleger: links
        for a in liste:
            if a["zone"] == "mitte": a["seite"] = None; continue
            seite = a["zone"]; o, d, lg = sp["ausleger"][seite]
            a["ausleger"] = dict(o=o, d=d, lg=lg, seite=seite, m=ausleger_matrix(o, d))
            yv = (-d[1], d[0], 0.0); allein = sum(1 for b in liste if b["zone"] == a["zone"]) == 1
            a["y_clip"] = Y_CLIP if (a["art"] == "tisch" or allein) else -Y_CLIP; a["yv"] = yv
        for a in sorted(liste, key=lambda a: (a["zone"] == "mitte", a["art"])):
            if a["zone"] == "mitte":
                tgt = [0.0]; xref = None
            else:
                au = a["ausleger"]; s0 = _s_lateral(k, au["o"], a["yv"], a["y_clip"]); tgt = [s0]
            jm = _jog_min(a["idd"])
            cand = sorted({round(t + d_, 1) for t in tgt for d_ in [0.0] + [sg * (jm + 5 * i) for i in range(0, 120) for sg in (1, -1)]}, key=lambda s: abs(s - tgt[0]))
            if a["zone"] == "mitte": cand = [0.0] + [5.0 * i for i in range(1, 220)] if a["art"] == "beet" else [5.0 * i for i in range(1, 220)]
            s = next(c for c in cand if all(c + T_HALB <= b0 or c - T_HALB >= b1 for b0, b1 in belegt) and abs(c) < 1100)
            belegt.append((s - T_HALB, s + T_HALB)); a["s"] = s
            p, t = ring_pt(k, s)
            if a["zone"] == "mitte":
                a["m_t"] = mat(p, t, (0, 0, 1)); a["abgang"] = add(p, (0, 0, -1), AS.abz_len(a["dk"])); a["u0"] = (0.0, 0.0, -1.0)
            else:
                dd = a["ausleger"]["d"]; a["m_t"] = mat(p, t, mul(dd, -1)); a["abgang"] = add(p, dd, AS.abz_len(a["dk"])); a["u0"] = dd
                a["lam"] = dot(sub(p, a["ausleger"]["o"]), a["yv"]) - a["y_clip"]
            out.append(a)
    for a in out: a["weg"] = schlauch_weg(a)
    _FL = out
    return out

Z_ARM = AT.Z["platte_o"] / 2 + AT.Z["traeger_o"] / 2 + FZ            # 2677 abs
WINKEL_H = 45.0                                                     # [A] Winkeltuelle 90 Grad d25 (PVC-U): Achse Port bis Schlauchende senkrecht
def _fall_xy(a):
    """Fall-Linie (x, y, 0) eines Ausleger-Abnehmers: Endbuegel-Port 'Fall'."""
    au = a["ausleger"]; f = world(au["m"], (au["lg"] + AT.AU["biege_r"], a["y_clip"], 0.0)); return (f[0], f[1], 0.0)
def schlauch_weg(a, winkel=None):
    """Weltpunkte des Schlauchs (s1 bis Regelhahn, Zwischenschlauch, s3 bis Anschluss) und Lage von Hahn, Kupplung, Endstueck (Masse aus autobahn_s)."""
    idd, Rb = a["idd"], AS.hose_R(a["idd"]); tl = AS.FT["tuelle"][idd]; kr = AS.FT["kragen"]
    u0 = a["u0"]; A0 = a["abgang"]
    la = AS.FT["anschl_l"][a["art"]]; E = add(a["port"], a["d_o"], la); zE = a["port"][2]
    # W88: Port oeffnet vom Fall weg (Innentisch: Verteiler-Oeffnung zeigt zum Pool) -> Winkeltuelle 90 Grad nach oben am Port, Schlauch kommt von oben;
    # dafuer liegen Regelhahn und Kupplung so hoch, dass zwei 90-Grad-Boegen (Tangente Rb) zwischen Kupplung und Winkel passen.
    E_up = (E[0], E[1], zE + WINKEL_H)
    z_h = AS.FT["z_hahn"][a["art"]] + FZ; hl = AS.FT["hahn_lb"][idd]
    k_d = AS.SK[idd]; stapel = hl / 2 + (2 * tl + 20) + (k_d["dose_l"] + k_d["st_l"])          # z_h bis Kupplungs-Unterkante
    fxy = (a["abgang"][0], a["abgang"][1], 0.0) if a["zone"] == "mitte" else _fall_xy(a)
    if winkel is None: winkel = dot(a["d_o"], sub(fxy, (E[0], E[1], 0.0))) < 0   # Port zeigt vom Fall weg
    if winkel: z_h = max(z_h, E_up[2] + 2 * Rb + 10 + stapel)
    if a["zone"] == "mitte": z_h = min(z_h, A0[2] - kr - tl - hl / 2 - 10)    # U6 (D139): Ring 1550, der Hahn sitzt unter dem Abgang (Schlauch faellt, steigt nie)
    else: z_h = min(z_h, Z_ARM - Rb - 10 - tl - hl / 2)                       # U6 (D139): Hahn unter dem Ausleger (Arm auf 1682 rel), sonst stiege der Schlauch
    z_ht = z_h + hl / 2; z_hb = z_ht - hl
    if a["zone"] == "mitte":                                                 # Fall senkrecht unter dem Abzweig (Beet: in der Fuge auf der Sektorgrenze)
        D = (A0[0], A0[1]); s1 = [add(A0, u0, kr), (D[0], D[1], z_ht)]
    else:
        au = a["ausleger"]; d = au["d"]; yv = a["yv"]; up = (0.0, 0.0, 1.0)
        x1 = kr + tl + Rb * math.tan(math.pi / 8) + 5; dz = Z_ARM - A0[2]
        P1 = add(A0, d, x1)
        fall = world(au["m"], (au["lg"] + AT.AU["biege_r"], a["y_clip"], 0.0))       # Fall-Linie am Endbuegel (WA-T Port 'Fall')
        D = (fall[0], fall[1]); lam = a["lam"]
        def _s1(quer):
            """quer False: seitlicher Versatz als 45-Grad-Diagonale (braucht |lam| entlang des Arms); quer True (W88, kurze Innen-Ausleger):
            Versatz rechtwinklig mit zwei 90-Grad-Boegen (braucht nur 2 x Rb entlang des Arms)."""
            P = add(A0, d, (kr + tl + Rb + 5) if quer else x1); pts = [add(A0, u0, kr), P]   # seitlicher Versatz zuerst auf Ring-Achshoehe, dann Anstieg in der Clip-Linie
            if abs(lam) > 0.5:
                if quer: P = add(P, yv, -lam); pts.append(P); P = add(P, d, Rb + Rb * math.tan(math.pi / 8) + 5)
                else: P = add(add(P, d, abs(lam)), yv, -lam); pts.append(P); P = add(P, d, 2 * Rb * math.tan(math.pi / 8) + 5)
                pts.append(P)
            pts.append(add(add(P, d, dz), up, dz))
            return pts + [fall, (D[0], D[1], z_ht)]
        s1 = _s1(False)
        try: AS.hose_layout([list(p) for p in s1], Rb)
        except ValueError: s1 = _s1(True)
    z_kt = z_hb - (2 * tl + 20); z_kb = z_kt - (k_d["dose_l"] + k_d["st_l"])
    s3 = None
    if winkel:                                                               # W88: ueber dem Tisch zum Port, dann von oben in die Winkeltuelle (Halter je <= 400 mm, R6)
        zm = E_up[2] + Rb + 5
        for cand in ([(D[0], D[1], z_kb), (D[0], D[1], zm), (E_up[0], E_up[1], zm), E_up],                        # waagerecht ueber dem Abnehmer
                     [(D[0], D[1], z_kb), (D[0], D[1], z_kb - 40), (E_up[0], E_up[1], E_up[2] + 40), E_up]):       # Fall fast ueber dem Port: schraeges S
            if math.hypot(D[0] - E_up[0], D[1] - E_up[1]) < 1.0: cand = [(D[0], D[1], z_kb), E_up]
            try: AS.hose_layout([list(p) for p in cand], Rb); s3 = cand; break
            except ValueError: continue
    for Lc in ([] if (s3 or winkel) else (Rb + 40, 2 * Rb)):                # nur kurzer Anlauf; laengere Umwege waren die Schlaufen in der Luft (W88)
        C = add(E, a["d_o"], Lc); C = (C[0], C[1], zE)
        cand = [(D[0], D[1], z_kb), (D[0], D[1], zE), C, (E[0], E[1], zE)]
        if math.hypot(C[0] - D[0], C[1] - D[1]) < 1.0: cand = [cand[0], cand[1], cand[3]]
        try: AS.hose_layout(cand, Rb); s3 = cand; break
        except ValueError: continue
    if s3 is None and not winkel: return schlauch_weg(a, winkel=True)        # W88: statt Schlaufe in der Luft (frueher Rueckfall) Winkeltuelle von oben
    befund = None
    if s3 is None:                                                           # U6 (D139): Ring auf 1550; zwischen Kupplung und Anschluss fehlt Hoehe oder Abstand fuer zwei Boegen mit Rb
        s3 = [(D[0], D[1], z_kb), E_up]; befund = "schraeg: gerader Schlauch von der Kupplung zur Winkeltuelle, Biegeradius an beiden Enden nicht eingehalten (D139)"
    if s3 is None: raise SystemExit("%s: kein Schlauchweg unten" % a["name"])
    return dict(Rb=Rb, ad=AS.HOSE[idd]["ad"], tl=tl, kr=kr, s1=s1, z_ht=z_ht, z_hb=z_hb, z_kt=z_kt, z_kb=z_kb, D=D, s2=[(D[0], D[1], z_hb), (D[0], D[1], z_kt)], s3=s3, E=E, la=la, winkel=winkel, E_up=E_up, befund=befund)

def prisma(b, nm, d, p0, u, ln, mat_=None):
    """Achtkant-Prisma (Darstellung [A]): Durchmesser d ueber Ecken, Achse u ab p0, Laenge ln. Wenige Dreiecke im OBJ (Zylinder mit Bohrung: Tausende)."""
    u = unit(u); x = unit(cross(u, (0.0, 0.0, 1.0)) if abs(u[2]) < 0.9 else cross(u, (1.0, 0.0, 0.0))); y = cross(u, x)
    r = d / 2.0; pts = [[round(r * math.cos(math.radians(22.5 + 45 * i)), 3), round(r * math.sin(math.radians(22.5 + 45 * i)), 3)] for i in range(8)]
    b.add("sketch.create", plane={"origin": [round(v, 3) for v in p0], "x_dir": [round(v, 9) for v in x], "y_dir": [round(v, 9) for v in y]}, name=nm + "_sk")
    b.add("sketch.line", points=pts, closed=True); b.add("sketch.finish")
    b.add("solid.extrude", distance=round(ln, 3), operation="new", name=nm, body_name=nm)
    return nm

def hose_einfach(b, prefix, pts, R, ad, idd):
    """Darstellungs-Schlauch [A]: Weg wie AS.hose_layout (gleiche Laenge), je Gerade ein Achtkant-Prisma, Bogen aus 4 Sehnen (je 2 mm verlaengert)."""
    segs = AS.hose_layout([list(p) for p in pts], R); names = []
    for n, sg in enumerate(segs, 1):
        stuecke = []
        if sg[0] == "G": stuecke.append((tuple(sg[1]), tuple(sg[2])))
        else:
            _, A, Bp, C, k, u_in, th = sg; prev = tuple(A)
            for j in range(1, 5):
                q = tuple(add(C, AS.rot(list(sub(A, C)), k, th * j / 4))); stuecke.append((prev, q)); prev = q
        for j, (p0, p1) in enumerate(stuecke):
            u = unit(sub(p1, p0)); names.append(prisma(b, f"{prefix}_{n}_{j}", ad, sub(p0, mul(u, 1.0)), u, math.dist(p0, p1) + 2.0))
    b.add("material.assign", bodies=names, material="SCH schwarz")
    return segs, AS.hose_length(segs, R), names

def halter_s3(w, raster=400.0, breite=20.0):
    """Halter-Lagen (je ein kurzes Stueck entlang der Achse) auf den waagerechten Geraden von s3 nach AS.hose_layout: Abstand <= raster (R6 Schlauch),
    gezaehlt ab Bogenende; Geraden kuerzer als raster bekommen keinen Halter (liegen zwischen zwei Boegen am Port bzw. an der Kupplung)."""
    out = []
    for sg in AS.hose_layout([list(p) for p in w["s3"]], w["Rb"]):
        if sg[0] != "G": continue
        p0, p1 = tuple(sg[1]), tuple(sg[2]); L = math.dist(p0, p1)
        if abs(p1[2] - p0[2]) > 0.05 * L or L <= raster: continue
        n = math.ceil(L / raster) - 1; u = unit(sub(p1, p0))
        for k in range(1, n + 1):
            c = add(p0, u, L * k / (n + 1)); out.append((add(c, u, -breite / 2), add(c, u, breite / 2)))
    return out

def schlauch_bauen(out_sc=None):
    """Eine Komponente mit allen 38 Fallleitungen in Weltlage (Instanz im Ursprung), Darstellungsgeometrie [A]: Tuelle, Schlauch, Regelhahn, Zwischenschlauch,
    Schnellkupplung, Schlauch, Endstueck als Achtkant-Prismen ohne Bohrung (Masse aus autobahn_s; Wege und Laengen wie in fallleitungen())."""
    import sc
    b = sc.Build(); nm = "R2_Ring_B2_Schlaeuche"
    AS.mats(b, ["SCH schwarz", "LT pp", "LT pvc", "LT v2a", "LT hahn"]); b.add("component.create", name=nm, grounded=True)
    laengen = []
    for i, a in enumerate(fallleitungen(), 1):
        w = a["weg"]; idd, dk, tl, kr = a["idd"], a["dk"], w["tl"], w["kr"]; u0 = a["u0"]; A0 = a["abgang"]; pre = f"F{i:02d}"
        tu = prisma(b, pre + "_Tuelle_oben", LT.od_f(dk), add(A0, u0, -LT.DEPTH[dk]), u0, LT.DEPTH[dk] + kr + tl)
        b.add("material.assign", bodies=[tu], material="LT pvc")
        _, l1, _ = hose_einfach(b, pre + "_S1", w["s1"], w["Rb"], w["ad"], idd)
        D = w["D"]; dn = (0.0, 0.0, -1.0); zt, zb = w["z_ht"], w["z_hb"]
        hn = prisma(b, pre + "_Regelhahn", AS.FT["hahn_ob"][idd], (D[0], D[1], zt + tl), dn, AS.FT["hahn_lb"][idd] + 2 * tl)
        b.add("solid.box", length=10, width=AS.FT["hebel"], height=12, center=[D[0], D[1] + AS.FT["hahn_ob"][idd] / 2 + AS.FT["hebel"] / 2 - 2, (zt + zb) / 2], operation="new", name=pre + "_Hebel", body_name=pre + "_Hebel")
        b.add("material.assign", bodies=[hn, pre + "_Hebel"], material="LT hahn")
        _, l2, _ = hose_einfach(b, pre + "_S2", w["s2"], w["Rb"], w["ad"], idd)
        k_ = AS.SK[idd]; z0 = w["z_kt"] + k_["tl"]
        kd = prisma(b, pre + "_Kupplung_Dose", k_["dose_d"], (D[0], D[1], z0 - k_["tl"]), dn, k_["tl"] + k_["dose_l"])
        ks = prisma(b, pre + "_Kupplung_Stecker", k_["st_d"], (D[0], D[1], z0 - k_["tl"] - k_["dose_l"]), dn, k_["st_l"] + k_["tl"])
        b.add("material.assign", bodies=[kd, ks], material="LT v2a")
        _, l3, _ = hose_einfach(b, pre + "_S3", w["s3"], w["Rb"], w["ad"], idd)
        ed = mul(a["d_o"], -1); an = prisma(b, pre + "_Anschluss", AS.FT["anschl_od"][a["art"]], sub(w["E"], mul(ed, tl)), ed, tl + w["la"])
        b.add("material.assign", bodies=[an], material="LT pvc" if a["art"] == "tisch" else "LT pp")
        if w.get("winkel"):                                                  # W88: Winkeltuelle 90 Grad nach oben am Port
            wk = prisma(b, pre + "_Winkel", AS.FT["anschl_od"][a["art"]], sub(w["E"], (0.0, 0.0, AS.FT["anschl_od"][a["art"]] / 2)), (0.0, 0.0, 1.0), WINKEL_H + AS.FT["anschl_od"][a["art"]] / 2 + tl)
            b.add("material.assign", bodies=[wk], material="LT pvc")
        hl_ = []                                                             # W88/R6: Schlauchhalter auf waagerechten Strecken unten (s3) je <= 400 mm
        for i_, (p0, p1) in enumerate(halter_s3(w)):
            hl_.append(prisma(b, f"{pre}_Halter_{i_ + 1}", w["ad"] + 10, p0, sub(p1, p0), math.dist(p0, p1)))
        if hl_: b.add("material.assign", bodies=hl_, material="LT pp")
        laengen.append((a["name"], l1 + l2 + l3))
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="R2-SCHLAEUCHE", revision="A", properties={"Werkstoff": "Schlauch REHAU RAUAQUA T-Flex ID19/ID25 schwarz (D85), Tuellen PVC-U/PP, Regelhahn PVC-U, Kupplung Edelstahl"},
          description="Montage R2 Ring B2: 38 Schlauch-Fallleitungen in Weltlage (trassen_ring.py); Darstellungsgeometrie [A]: Achtkant-Prismen ohne Bohrung (Werkstatt-Teile mit Bohrung WA5/WA6 ergeben 17 MB OBJ je Fallleitung); je Abnehmer Tuelle -> Schlauch (Ausleger + freier Fall) -> Regelhahn -> Schnellkupplung -> Endstueck am Tisch-Zulaufverteiler bzw. Tropfrohr")
    out_sc = out_sc or comp(SCHLAUCH_DATEI)
    sc.run(b.write("ring_b2_schlaeuche"), out_sc)
    return laengen

SOLL_FALL = {(1, "tisch", "aussen"): "e39", (1, "tisch", "mitte"): "e40", (1, "tisch", "innen"): "e41", (1, "beet", "aussen"): "e42", (1, "beet", "mitte"): "e43",
             (2, "tisch", "aussen"): "e44", (2, "tisch", "mitte"): "e45", (2, "tisch", "innen"): "e46", (2, "beet", "aussen"): "e47", (2, "beet", "mitte"): "e48"}
SOLL_ABZ = {(1, "tisch"): "e35", (1, "beet"): "e36", (2, "tisch"): "e37", (2, "beet"): "e38"}
def schlauch_soll_wege():
    """U6: Soll-Wege der Abfahrten (e35 bis e38, Ring-Abzweig) und Fallleitungen (e39 bis e48, Schlauch) mit Stueckzahl im Modell (Komponente ring_b2_schlauchwege)."""
    out = {}
    for a in fallleitungen():
        for w in (SOLL_ABZ[(a["linie"], a["art"])], SOLL_FALL[(a["linie"], a["art"], a["zone"])]):
            out[w] = out.get(w, 0) + 1
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
    json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(p, "a").write("\n")
    print("geschrieben:", {k: len(v) for k, v in eint.items()})

def bericht():
    eint, ein, feeds, bel = leitungen_eintraege()
    sp = stuetzpunkte()
    print("Ring: Apothem %.0f, Eckradius %.1f, Seite %.1f, Gerade je Seite %.1f mm" % (AP, RE, SEITE, L_GERADE))
    print("Linie 1 Ecken", [ECKEN_AZ[k] for k in LINIE_ECKEN[1]], "| Linie 2", [ECKEN_AZ[k] for k in LINIE_ECKEN[2]], "| Kupplungsseiten", [(ECKEN_AZ[k], ECKEN_AZ[(k + 1) % N]) for k in KUPPLUNG])
    print("Stuetzpunkte: %d Joche, %d Stelzen; Ausleger %d" % (sum(s["art"] == "joch" for s in sp), sum(s["art"] == "stelze" for s in sp), sum(len(s["ausleger"]) for s in sp)))
    for l in (1, 2):
        e = ein[l]; c = e["p0"]
        print("Einspeisung Linie %d: Ueberlauf %s r %.0f az %.1f Z %.0f rel, Feed-T Seite %d s %.0f" % (l, e["tank"], math.hypot(c[0], c[1]), az(c), c[2] - FZ, feeds[l][0], feeds[l][1]))
    kl = schellen(bel)
    print("Schellen:", len(kl))
    print({k: len(v) for k, v in eint.items()})

def bericht_r2():
    fl = fallleitungen()
    from collections import Counter
    print("Fallleitungen:", len(fl), Counter((a["zone"], a["art"]) for a in fl), "je Linie", Counter((a["linie"], a["art"]) for a in fl))
    for a in fl:
        w = a["weg"]
        try: L = "%5.0f" % sum(AS.hose_length(AS.hose_layout([list(p) for p in s], w["Rb"]), w["Rb"]) for s in (w["s1"], w["s2"], w["s3"]))
        except ValueError as e: L = "FEHLER " + str(e)
        print("  %-18s Ecke %6.1f s %7.1f lam %6.1f ID%d L %s" % (a["name"], ECKEN_AZ[a["k"]], a["s"], a.get("lam", 0.0), a["idd"], L))

if __name__ == "__main__":
    if "--r2" in sys.argv: bericht_r2()
    if "--schlauch-bauen" in sys.argv: print(schlauch_bauen())
    if "--schreiben" in sys.argv: schreiben()
    if "--bericht" in sys.argv or len(sys.argv) == 1: bericht()
