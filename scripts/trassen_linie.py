"""M10-S2: Trassenliste data/leitungstrassen.json je Linie (Linie 1 = Ost, Linie 2 = West), abgeleitet aus Instanzmatrizen und Port-Tabellen. Nachfolger von trassen_s2a.py.
Aufruf: python -X utf8 scripts/trassen_linie.py <linie>      (schreibt die Trassen dieser Linie in data/leitungstrassen.json, Trassen der anderen Linie bleiben stehen; druckt die Koordinaten)
Die Koordinaten kommen NICHT von Hand, sondern aus den Instanzmatrizen (scripts/dome-script.json) mal den Port-Tabellen der Bauteilblaetter (PORTS unten, je mit Quelle).
Zuordnung der Netz-Etiketten zu Modell-Instanzen: LINIEN (docs/leitungsnetz-umhaengen.md); die Netz-Kanten je Linie stehen in data/leitungsnetz.json (nur gelesen).
Z absolut (Flur 400). Das Skript ist die Ableitung, die Liste ihr Ergebnis: Aenderungen an Lage oder Hoehe gehen hier (und in data/params.json, lt_*) hinein.
Bogenmasse (Schenkel k = Abstand Kreuzungspunkt - Muffenebene, Radius R = k - t) aus scripts/workshop/leitung.ports()."""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import leitung as LT

P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
MV = {c["params"]["occurrence"]: c["params"]["matrix"] for c in json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"] if c["command"] == "occurrence.move"}
OUT = os.path.join(ROOT, "data", "leitungstrassen.json")

# Port-Tabellen (Bauteil-KS): (x, y, z), Richtung der Oeffnung nach aussen, Aussen-d
PORTS = {
    "feinfilter":   {"ein": ((-375, 0, 816), (-1, 0, 0), 63), "aus": ((385, 0, 310), (1, 0, 0), 63)},      # docs/parts/feinfilter.md Zeilen 104/105
    "pumpe_gross":  {"saug": ((196, 76, 120), (1, 0, 0), 50), "druck": ((90, 76, 255), (0, 0, 1), 40)},    # docs/parts/pumpe.md Port-Tabelle
    "pumpe_klein":  {"saug": ((176, 64, 120), (1, 0, 0), 40), "druck": ((75, 64, 245), (0, 0, 1), 32)},
    "tank_klein":   {"zulauf": ((282.5, -351, 997), (0, -1, 0), 50), "auslauf": ((442, 0, 1147), (1, 0, 0), 50)},   # docs/parts/tank.md Ports
    "tank_gross":   {"zulauf": ((403.5, -395, 1420), (0, -1, 0), 63), "ueberlauf": ((570, 0, 1570), (1, 0, 0), 63)},
}
# Etiketten je Linie: Netz-Knoten -> Modell-Instanz (docs/leitungsnetz-umhaengen.md); Linie 2 folgt in S2c
LINIEN = {
    1: {"name": "Ost", "filter": "Feinfilter:1", "pool_sa": "SA_Ost_A", "pumpe_gross": ("Pumpe_gross:1", "Pumpe_gross:2"), "tank_gross": "Tank_gross:1",
        "absetzer": "Tank_klein:2", "pumpe_klein": ("Pumpe_klein:3", "Pumpe_klein:4")},
    2: {"name": "West", "filter": "Feinfilter:2", "pool_sa": "SA_West_B", "pumpe_gross": ("Pumpe_gross:3", "Pumpe_gross:4"), "tank_gross": "Tank_gross_t3:1",
        "absetzer": "Tank_klein:1", "pumpe_klein": ("Pumpe_klein:1", "Pumpe_klein:2")},
}

def world(m, p): return tuple(m[4 * r] * p[0] + m[4 * r + 1] * p[1] + m[4 * r + 2] * p[2] + m[4 * r + 3] for r in range(3))
def wdir(m, d): return tuple(m[4 * r] * d[0] + m[4 * r + 1] * d[1] + m[4 * r + 2] * d[2] for r in range(3))
def h(deg): return (math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0.0)
def add(a, b, s=1.0): return tuple(a[i] + s * b[i] for i in range(3))
def sub(a, b): return tuple(a[i] - b[i] for i in range(3))
def dot(a, b): return sum(a[i] * b[i] for i in range(3))
def unit(a): n = math.sqrt(dot(a, a)); return tuple(v / n for v in a)
def rd(p): return [round(v, 1) for v in p]
def ang(v): return math.degrees(math.atan2(v[1], v[0]))

def k90(d): return LT.ports("lt_bogen90_d%d" % d)[1][1][0]          # Schenkel Bogen 90
def r90(d): return k90(d) - LT.DEPTH[d]                              # Abstand Stutzenspitze -> Kreuzungspunkt bei direkt aufgestecktem Bogen
def r45(d):                                                          # dasselbe fuer den Bogen 45 (Schenkel wie leitungen.tangent)
    B = LT.ports("lt_bogen45_d%d" % d)[1]
    return B[1][2] - B[1][0] / B[2][0] * B[2][2] - LT.DEPTH[d]
def lred(dg, dk): return LT.ports("lt_reduzierung_d%d_d%d" % (dg, dk))[1][1][2]
def ta(d): return -LT.ports("lt_t_d%d" % d)[0][1][0]                 # Arm des T-Stuecks (Mitte -> Muffenebene)

HD = 75   # E14 (01.11.2026): Heber K01/K17 durchgehend d75; die Stutzen von Pool und Feinfilter bleiben d63

def port(inst, klasse, name):
    """Weltpunkt der Stutzenspitze, Richtung nach aussen, Aussen-d eines Bauteil-Ports."""
    p, o, d = PORTS[klasse][name]; m = MV[inst]
    return world(m, p), unit(wdir(m, o)), d

def stutzen_red(tip, o, d_stutzen, d_rohr):
    """Reduziermuffe auf einem Stutzen d_stutzen fuer ein Rohr d_rohr (d_rohr < d_stutzen): Muffenebene A liegt t hinter der Spitze, B um die Muffenlaenge weiter aussen.
    Gibt (r_stueck ohne id, Trassenpunkt auf Ebene B) zurueck."""
    pa = add(tip, o, -LT.DEPTH[d_stutzen]); pb = add(pa, o, lred(d_stutzen, d_rohr))
    return {"pos_a": rd(pa), "dir": [round(v, 6) for v in o], "d_gross": d_stutzen, "d_klein": d_rohr, "auf_stutzen": True}, pb   # auf_stutzen: Ausnahme 2 der Leitungsordnung

def heber_red(tip, o):
    """Reduziermuffe d75/d63 auf einem Stutzen d63 (M10-S2R): die kleine Seite B (Muffe d63) steckt t63 hinter der Spitze auf dem Stutzen, die grosse Seite A (Muffe d75) schaut nach aussen.
    Gibt (r_stueck ohne id, Trassenpunkt auf Ebene A) zurueck; pos_a = Ebene A, dir von A nach B (zum Bauteil hin)."""
    pb = add(tip, o, -LT.DEPTH[63]); pa = add(pb, o, lred(HD, 63))
    return {"pos_a": rd(pa), "dir": [round(-v, 6) for v in o], "d_gross": HD, "d_klein": 63, "auf_stutzen": True}, pa

def s_alt(neu, kid, g0, gh, s):
    """Lage eines T auf der Grabenstrecke: die Parameter lt_*_s sind von der alten d63-Ecke gemessen (Runde 65); die d75-Ecke sitzt weiter aussen, das T bleibt deshalb an seinem Ort (Abstand von der neuen Ecke gekuerzt)."""
    return s - dot(sub(g0, neu["g0_alt"][kid]), gh)

def schreiben(doc, linie, neu):
    """Mischt die Trassen der Linie in die bestehende Liste (Trassen der anderen Linie bleiben); S2a-Eintraege ohne Feld linie gelten als Linie 1."""
    alt = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"z_bezug": "absolut", "regeln": {}, "trassen": []}
    gehoert = lambda e: e.get("linie", 1) == linie
    for key in ("trassen", "t_stuecke", "r_stuecke", "teile", "gruben"):
        doc[key] = [e for e in alt.get(key, []) if not gehoert(e)] + neu.get(key, [])
        for e in neu.get(key, []): e["linie"] = linie
    if not doc["r_stuecke"]: del doc["r_stuecke"]
    return doc

def pool_filter(L, neu, kid):
    """K01 (Linie 1) / K17 (Linie 2): Pool-Seitenablauf (Stutzen d63) -> Feinfilter-Einlauf (Stutzen d63), unterflur im Heber, Rohr d75 (M10-S2R, E14):
    je Stutzen Reduziermuffe d75/d63, Rohrstueck (Muffenebene auf Muffenebene) und Bogen d75; die Achshoehen (740 / Graben / 720) bleiben, die Senkrechten rutschen waagerecht nach aussen."""
    ein, ein_o, _ = port(L["filter"], "feinfilter", "ein")
    sa = [p for p in L["G"].pool_ports(P["sock_h"]) if p["name"] == L["pool_sa"]][0]
    tip_pool, u = sa["ende"], sa["axis"]
    zu = P["lt_k01_z_u"]
    rp, ap = heber_red(tip_pool, u); rf, af = heber_red(ein, ein_o)
    neu["r_stuecke"] += [dict(id="R_%s_P" % kid, **rp), dict(id="R_%s_F" % kid, **rf)]
    neu.setdefault("g0_alt", {})[kid] = (*add(tip_pool, u, r90(63))[:2], zu)    # Ecke der d63-Verlegung (Runde 65): Bezug der T-Lagen auf der Grabenstrecke
    K = k90(HD)                                                             # Schenkel Bogen d75: Bogen-Muffe stoesst an Ebene A (Rohrstueck 2 t dazwischen)
    v1 = add(ap, u, K)
    c_in = add(af, ein_o, K)
    pf = [ap, v1, (v1[0], v1[1], zu), (c_in[0], c_in[1], zu), c_in, af]
    neu["trassen"].append({"id": kid, "kante": kid, "dn": HD, "farbe": "dunkelblau", "start": "r:R_%s_P" % kid, "ende": "r:R_%s_F" % kid, "heber": True,
        "dn_abweichung": "E14 (01.11.2026): Heber durchgehend d75 gebaut, Netz-Kante %s fuehrt noch d63 (Netzliste gehoert dem Orchestrator)" % kid,
        "baender": ["W", "W", "U", "W", "W"], "anschluss": ["Zentralpool", L["filter"]], "pfad": [rd(p) for p in pf],
        "notiz": "Seitenablauf Z 740 (Pool-Stutzen %s d63, Az %.1f) -> Reduziermuffe d75/d63 -> Bogen runter -> Graben Z %g (Heber d75, Rohr oben %.1f unter Spiegel 915) -> Bogen hoch -> Reduziermuffe d75/d63 auf den Einlauf Z %.0f (Stutzenspitze x %.1f y %.1f)" % (L["pool_sa"], ang(u), zu, 915 - (zu + HD / 2), ein[2], ein[0], ein[1])})

def linie1_s2a(L, neu):
    """K01 Pool -> Feinfilter-Einlauf (unterflur, Heber), Stamm K06-T Filterauslauf -> T, K06/K02 T -> Pumpen-Saugstutzen (M10-S2a, unveraendert)."""
    aus, aus_o, _ = port(L["filter"], "feinfilter", "aus")
    pump = {i: port(L["pumpe_gross"][i - 1], "pumpe_gross", "saug") for i in (1, 2)}
    R63 = r90(63)
    pool_filter(L, neu, "K01")
    # ---------------- K06-Stamm: Feinfilter-Auslauf (d63) -> T d63/d50/d50 (Z gleich Auslauf), 90 + 45 + 45 + 90 Grad
    z = aus[2]
    v1 = add(aus, aus_o, R63); a0 = ang(aus_o)
    h2 = a0 - 90                       # nach 90 Grad rechts: Westsuedwest
    h3 = h2 - 45                       # 45 Grad rechts: Westnordwest
    h4 = h3 + 45                       # 45 Grad links: zurueck auf h2
    h5 = h4 + 90                       # 90 Grad links: Abstieg nach Sued (= Richtung des Auslaufs)
    v2 = add(v1, h(h2), P["lt_k06_s2"])
    v4 = (P["lt_k06_v4_x"], P["lt_k06_v4_y"], z)
    # v2 + l3*h(h3) + l4*h(h4) = v4 (zwei Gleichungen, zwei Unbekannte)
    a1, a2, b1, b2 = math.cos(math.radians(h3)), math.sin(math.radians(h3)), math.cos(math.radians(h4)), math.sin(math.radians(h4))
    dx, dy = v4[0] - v2[0], v4[1] - v2[1]; det = a1 * b2 - a2 * b1
    l3, l4 = (dx * b2 - dy * b1) / det, (a1 * dy - a2 * dx) / det
    v3 = add(v2, h(h3), l3)
    # T0 auf der Halbgeraden v4 + s*h(h5) bei y = lt_k06_t_y
    s5 = (P["lt_k06_t_y"] - v4[1]) / h(h5)[1]; t0 = add(v4, h(h5), s5)
    pf = [aus, v1, v2, v3, v4, t0]
    neu["trassen"].append({"id": "K06-T", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T1", "band": "U", "anschluss": [L["filter"]],
        "pfad": [rd(p) for p in pf], "notiz": "Stamm d63 zwischen Filterauslauf und T (gehoert zu K02 und K06: Netz fuehrt dort d50, T-Stueck d63/d50/d50 laut Netz-Bemerkung K06); Winkel %.0f/%.0f/%.0f/%.0f Grad im 15-Grad-Gitter des Filters; Laengen v2-v3 %.0f, v3-v4 %.0f, v4-T %.0f" % (h2, h3, h4, h5, l3, l4, s5)})
    # ---------------- Abgaenge d50 vom T zu den Pumpen: je Riser (unterflur -> Saugstutzenhoehe) und Zulauf in den Stutzen
    # Pumpe_gross:1 (Sued) geradeaus (h5), Pumpe_gross:2 (Nord) links 90 Grad (h5 + 90, Richtung Ost)
    for kid, pi, dirdeg in (("K06", 1, h5), ("K02", 2, h5 + 90)):
        tip, o, _ = pump[pi]; dv = h(dirdeg)
        s = (tip[1] - t0[1]) / dv[1]; r = add(t0, dv, s)                      # Fusspunkt des Risers: Strahl vom T bei y der Saugstutzenachse
        r = (r[0], tip[1], z); up = (r[0], tip[1], tip[2])
        neu["trassen"].append({"id": kid, "kante": kid, "dn": 50, "farbe": "dunkelblau", "start": "t:T1", "ende": "stutzen", "baender": ["U", "W", "W"],
            "anschluss": [L["pumpe_gross"][pi - 1]] + ([L["tank_gross"]] if kid == "K02" else []), "pfad": [rd(t0), rd(r), rd(up), rd(tip)],
            "notiz": "T -> Fuss des Risers (Z %.0f) -> Riser auf Saugstutzenhoehe Z %.0f -> Zulauf in den Saugstutzen %s (Stutzenspitze x %.1f y %.1f, Oeffnung -X)" % (z, tip[2], L["pumpe_gross"][pi - 1], tip[0], tip[1])})
    neu["t_stuecke"].append({"id": "T1", "pos": rd(t0), "d": 63, "ports": [{"trasse": "K06-T", "ende": "ende", "d": 63}, {"trasse": "K06", "ende": "start", "d": 50}, {"trasse": "K02", "ende": "start", "d": 50}],
                         "notiz": "T d63 aus lt_t_d63 + je Ausgang Rohrstueck d63 (2 t) + Reduziermuffe d63/d50 (die Muffen eines T und einer Reduziermuffe passen nicht Muffe auf Muffe)"})

def linie1_biofilter(L, neu):
    """K08/K09 Pumpen-Druckstutzen d40 -> T d50 (Z des Biofilter-Zulaufs) -> Stamm d50 -> Reduziermuffe d63/d50 auf den Zulauf-Stutzen; K10 Ueberlauf d63 -> Reduziermuffe -> Rohr d50 bis zum offenen Verteilerplatz (M10-S2b)."""
    tg = L["tank_gross"]; p8, p9 = (port(L["pumpe_gross"][i], "pumpe_gross", "druck") for i in (0, 1))
    zt, zo, _ = port(tg, "tank_gross", "zulauf"); ut, uo, _ = port(tg, "tank_gross", "ueberlauf")
    zh = zt[2]; R40 = r90(40); up = (0.0, 0.0, 1.0)
    hp = (-zo[1], zo[0], 0.0)                                              # waagerecht, senkrecht zur Zulauf-Achse (Richtung Westnordwest)
    # K09 (Pumpe 2 steht unter der Plattform): hoch -> unter der Plattform in Zulauf-Richtung hinaus -> Steigrohr -> waagerecht zum T
    c1 = add(p9[0], up, R40); c2 = add(c1, zo, P["lt_k09_aus"]); c3 = (c2[0], c2[1], zh)
    u = dot(sub(zt, c3), hp); t2 = add(c3, hp, u)                           # T: Schnitt der K09-Waagerechten mit der Zulauf-Achse
    # K08 (Pumpe 1): hoch -> nach Westen -> an der Plattform vorbei nach Norden -> Steigrohr -> waagerecht von Westen zum T
    xw = P["lt_k08_west_x"]; W = (xw - t2[0]) / hp[0]; cy = t2[1] + W * hp[1]
    k8 = [p8[0], add(p8[0], up, R40), (xw, p8[0][1], p8[0][2] + R40), (xw, cy, p8[0][2] + R40), (xw, cy, zh), t2]
    k9 = [p9[0], c1, c2, c3, t2]
    # Reduziermuffe d63/d50 auf dem Zulauf-Stutzen, Stamm d50 vom T bis zur Muffenebene B
    rz, pb = stutzen_red(zt, zo, 63, 50)
    neu["r_stuecke"].append(dict(id="R_ZUL", **rz))
    neu["trassen"] += [
        {"id": "K08", "kante": "K08", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T2", "baender": ["W", "W", "W", "W", "WH"], "anschluss": [L["pumpe_gross"][0]],
         "pfad": [rd(p) for p in k8], "notiz": "Druckstutzen %s (Z %.0f) -> hoch auf Z %.0f -> %.0f mm nach Westen (x %g, an der Plattform vorbei) -> %.0f mm nach Norden -> Steigrohr auf Zulaufhoehe Z %.0f -> %.0f mm zum T d50 an der Zulauf-Achse" % (L["pumpe_gross"][0], p8[0][2], p8[0][2] + R40, p8[0][0] - xw, xw, cy - p8[0][1], zh, math.dist(k8[4], t2))},
        {"id": "K09", "kante": "K09", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T2", "baender": ["W", "W", "W", "WH"], "anschluss": [L["pumpe_gross"][1], tg],
         "pfad": [rd(p) for p in k9], "notiz": "Druckstutzen %s (Z %.0f) -> hoch auf Z %.0f -> %g mm unter der Plattform nach aussen -> Steigrohr auf Zulaufhoehe Z %.0f -> %.0f mm zum T d50" % (L["pumpe_gross"][1], p9[0][2], p9[0][2] + R40, P["lt_k09_aus"], zh, math.dist(c3, t2))},
        {"id": "K08-K09-Stamm", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T2", "ende": "r:R_ZUL", "band": "WH", "anschluss": [tg], "pfad": [rd(t2), rd(pb)],
         "notiz": "vereinigte Druckleitung d50 (Netz K08/K09: vereinigt vor dem Tank zu d50) vom T bis zur Reduziermuffe d63/d50 auf dem Zulauf-Stutzen d63 des Biofilters (Z %.0f)" % zh}]
    neu["t_stuecke"].append({"id": "T2", "pos": rd(t2), "d": 50, "ports": [{"trasse": "K08", "ende": "ende", "d": 40}, {"trasse": "K09", "ende": "ende", "d": 40}, {"trasse": "K08-K09-Stamm", "ende": "start", "d": 50}],
                             "notiz": "T d50 mit zwei Eingaengen d40 (Rohrstueck d50 + Reduziermuffe d50/d40) und einem Ausgang d50"})
    # K10: Ueberlauf-Stutzen d63 -> Reduziermuffe d63/d50 -> Rohr d50, offenes Ende am Verteilerplatz
    ru, pbu = stutzen_red(ut, uo, 63, 50)
    neu["r_stuecke"].append(dict(id="R_UEB", **ru))
    ende = add(pbu, uo, P["lt_k10_len"])
    neu["trassen"].append({"id": "K10", "kante": "K10", "dn": 50, "farbe": "dunkelblau", "start": "r:R_UEB", "ende": "offen", "band": "WH", "anschluss": [tg], "pfad": [rd(pbu), rd(ende)],
        "notiz": "Ueberlauf-Stutzen d63 (Z %.0f = 1570 relativ) -> Reduziermuffe d63/d50 -> %g mm Rohr d50 nach aussen; das offene Ende (x %.0f y %.0f) ist der Verteiler-Eingang (Verteilerplatz, Verteiler d50 in S3)" % (ut[2], P["lt_k10_len"], ende[0], ende[1])})

def linie1_absetzer(L, neu):
    """Absetzerkreis (M10-S2b): K03 Pool-Bodenablauf d50 -> T d50 (Teilung Linie 1/2) -> Pumpe_klein-Saugstutzen (d50 -> d40), K04 Druckstutzen d32 -> Absetzer-Zulauf (d50 -> d32),
    K05 Absetzer-Auslass d50 -> T auf K01 am Feinfilter-Einlauf (K01 wird dort in K01 und K01-b geteilt). Das Linie-2-Zweigstueck endet offen hinter dem T."""
    G = L["G"]; ab = L["absetzer"]; pk = L["pumpe_klein"][0]; up = (0.0, 0.0, 1.0)
    ba = [p for p in G.pool_ports(P["sock_h"]) if p["name"] == "BA_Mitte"][0]; tipb = tuple(ba["ende"])
    saug, so, _ = port(pk, "pumpe_klein", "saug"); druck, _, _ = port(pk, "pumpe_klein", "druck")
    R50, R32 = r90(50), r90(32)
    # ---- K03: Bodenablauf-Stutzen (Z -1575, Oeffnung nach unten) -> Bogen -> unter dem Pool nach Sueden -> T d50 (Teilung) -> nach Osten -> Steigrohr auf Saughoehe -> Reduziermuffe d50/d40 -> Stutzen
    xr = P["lt_k03_riser_x"]; s = (xr - saug[0]) / so[0]; c4 = add(saug, so, s)               # Punkt der Saugachse bei x = xr
    c1 = add(tipb, (0.0, 0.0, -1.0), R50); zt = c1[2]
    t3 = (tipb[0], c4[1], zt); c3 = (xr, c4[1], zt)
    lr = lred(50, 40); pos_a = add(saug, so, lr + 120.0); pos_b = add(saug, so, 120.0)         # Reduziermuffe 120 mm vor dem Saugstutzen
    din = tuple(-v for v in so)
    stumpf = add(t3, (0.0, -1.0, 0.0), P["lt_l2_stub"])
    neu["r_stuecke"].append({"id": "R_K03", "pos_a": rd(pos_a), "dir": [round(v, 6) for v in din], "d_gross": 50, "d_klein": 40})
    neu["trassen"] += [
        {"id": "K03-Tief", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T3", "baender": ["UT", "UT"], "anschluss": ["Zentralpool"], "pfad": [rd(tipb), rd(c1), rd(t3)],
         "notiz": "Bodenablauf-Stutzen d50 (Pool-Mitte, Z %.0f) -> Bogen -> %.0f mm unter dem Pool nach Sueden (Z %.0f, unter der Pool-Bodenplatte Z -1425) bis zum T d50 (Teilung auf Linie 1 und 2)" % (tipb[2], math.dist(c1, t3), zt)},
        {"id": "K03-Steig", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T3", "ende": "r:R_K03", "baender": ["UT", "UT", "W"], "anschluss": [], "pfad": [rd(t3), rd(c3), rd(c4), rd(pos_a)],
         "notiz": "T-Ost-Ausgang -> %.0f mm nach Osten unter dem Pool hinaus (x %g) -> Steigrohr auf die Saughoehe Z %.0f -> zur Reduziermuffe d50/d40" % (math.dist(t3, c3), xr, c4[2])},
        {"id": "K03", "kante": "K03", "dn": 40, "farbe": "dunkelblau", "start": "r:R_K03", "ende": "stutzen", "band": "W", "anschluss": [pk, ab], "pfad": [rd(pos_b), rd(saug)],
         "notiz": "Reduziermuffe d50/d40 -> Saugstutzen %s (d40, Z %.0f)" % (pk, saug[2])},
        {"id": "K03-K19-Stumpf", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T3", "ende": "offen", "band": "UT", "anschluss": ["Zentralpool"], "pfad": [rd(t3), rd(stumpf)],
         "notiz": "Linie-2-Zweig (Netz K19) nur bis zur Abzweigung: %g mm Rohr d50 nach Sueden, offenes Ende; die Fortsetzung zu Pumpe_klein:1 baut S2c" % P["lt_l2_stub"]}]
    neu["t_stuecke"].append({"id": "T3", "pos": rd(t3), "d": 50, "ports": [{"trasse": "K03-Tief", "ende": "ende", "d": 50}, {"trasse": "K03-Steig", "ende": "start", "d": 50}, {"trasse": "K03-K19-Stumpf", "ende": "start", "d": 50}],
                             "notiz": "T d50: Teilung des gemeinsamen Pool-Bodenablaufs auf Linie 1 (Ost) und Linie 2 (West)"})
    # ---- K04: Druckstutzen d32 -> hoch -> unter der Absetzer-Plattform nach aussen (Bauteil -Y) -> Steigrohr -> an der Tankwand entlang -> Reduziermuffe d50/d32 am tangentialen Zulauf
    m = MV[ab]; zul, zo, _ = port(ab, "tank_klein", "zulauf")
    loc = lambda p: (m[0] * (p[0] - m[3]) + m[4] * (p[1] - m[7]), m[1] * (p[0] - m[3]) + m[5] * (p[1] - m[7]))
    wl = lambda x, y, z: (m[0] * x + m[1] * y + m[3], m[4] * x + m[5] * y + m[7], z)
    rk, pb = stutzen_red(zul, zo, 50, 32); neu["r_stuecke"].append(dict(id="R_K04", **rk))
    xd = loc(druck)[0]; xz = loc(zul)[0]; ky = -P["lt_k04_y"]; z1 = druck[2] + R32
    k4 = [druck, (druck[0], druck[1], z1), wl(xd, ky, z1), wl(xd, ky, zul[2]), wl(xz, ky, zul[2]), pb]
    neu["trassen"].append({"id": "K04", "kante": "K04", "dn": 32, "farbe": "dunkelblau", "start": "stutzen", "ende": "r:R_K04", "baender": ["W", "W", "WH", "WH", "WH"], "anschluss": [pk, ab], "pfad": [rd(p) for p in k4],
        "notiz": "Druckstutzen %s (d32, Z %.0f) -> hoch auf Z %.0f -> %.0f mm unter der Plattform nach aussen -> Steigrohr auf Zulaufhoehe Z %.0f -> %.0f mm an der Tankwand entlang -> Reduziermuffe d50/d32 auf dem tangentialen Zulauf-Stutzen" % (pk, druck[2], z1, math.dist(k4[1], k4[2]), zul[2], math.dist(k4[3], k4[4]))})
    # ---- K05: Auslauf-Stutzen d50 -> Bogen -> Fallrohr -> Unterflur mit Gefaelle -> senkrecht auf die K01-Grabenstrecke, dort T d75 (Zweig d50)
    k01 = [t for t in neu["trassen"] if t["id"] == "K01"][0]; neu["trassen"].remove(k01)
    f = [tuple(p) for p in k01["pfad"]]; g0, g1 = f[2], f[3]; zu = g0[2]
    gh = unit((g1[0] - g0[0], g1[1] - g0[1], 0.0)); ph = (-gh[1], gh[0], 0.0)
    aus, ao, _ = port(ab, "tank_klein", "auslauf"); l1 = R50 + P["lt_k05_vor"]; a1 = add(aus, ao, l1); a1 = (a1[0], a1[1], a1[2] - P["lt_k05_pct"] / 100.0 * l1)   # schon das Stutzenstueck faellt (Schwerkraft)
    rel = (a1[0] - g0[0], a1[1] - g0[1], 0.0); sT = s_alt(neu, "K01", g0, gh, P["lt_k05_s"]); la = sT - dot(rel, gh); lb = -dot(rel, ph); pct = P["lt_k05_pct"] / 100.0
    t4 = add(g0, gh, sT); z3 = zu + pct * lb; z2 = z3 + pct * la
    c2 = (a1[0], a1[1], z2); c3 = (a1[0] + la * gh[0], a1[1] + la * gh[1], z3)
    k5 = [aus, a1, c2, c3, t4]
    if la < 0 or lb < 0: raise SystemExit("K05: T liegt hinter dem Fallrohr (la %.0f, lb %.0f)" % (la, lb))
    neu["trassen"].append({"id": "K05", "kante": "K05", "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T4", "baender": ["WH", "U", "U", "U"], "gefaelle_pct": 1.0, "anschluss": [ab], "pfad": [rd(p) for p in k5],
        "notiz": "Auslauf-Stutzen %s (d50, Z %.0f) -> Bogen -> Fallrohr auf Z %.0f -> %.0f mm unterflur nach ENE (Gefaelle %.1f %%) -> %.0f mm senkrecht auf die K01-Grabenstrecke zum T d75 (Zweig d50, Z %.0f)" % (ab, aus[2], z2, la, P["lt_k05_pct"], lb, zu)})
    kc = dict(k01); kc["id"] = "K01"; kc["pfad"] = [rd(p) for p in f[:3]] + [rd(t4)]; kc["baender"] = ["W", "W", "U"]; kc["ende"] = "t:T4"
    kc["notiz"] = k01["notiz"] + " Hier bis zum T d75 des Absetzer-Zulaufs K05 (Teil 1)."
    kd = dict(k01); kd["id"] = "K01-b"; kd["pfad"] = [rd(t4)] + [rd(p) for p in f[3:]]; kd["baender"] = ["U", "W", "W"]; kd["start"] = "t:T4"
    kd["notiz"] = "K01 (Teil 2): vom T d75 des Absetzer-Zulaufs K05 bis zum Feinfilter-Einlauf (Heber, Graben Z %g)." % zu
    neu["trassen"] += [kc, kd]
    neu["t_stuecke"].append({"id": "T4", "pos": rd(t4), "d": HD, "ports": [{"trasse": "K01", "ende": "ende", "d": HD}, {"trasse": "K01-b", "ende": "start", "d": HD}, {"trasse": "K05", "ende": "ende", "d": 50}],
                             "notiz": "T d75 im Einlauf der K01 (Netz K05: T-Stueck mit Seitenablauf); Zweig d50 mit Rohrstueck d75 + Reduziermuffe d75/d50"})

IDS1 = {"pf": "K01", "pf_m": "K01-m", "st": "K06-T", "st_b": "K06-T-b", "abs": "K05", "t4": "T4", "t1": "T1", "t5": "T5", "t6": "T6", "kh": "KH1", "kante": "K56", "a": "K56-a", "b": "K56-b"}

def bypass(L, neu, I, spar, leg):
    """Notbypass (K56 Linie 1, K57 Linie 2; M10-S2b/S2c): T d63 auf der Pool-Filter-Leitung (Grabenstrecke) -> Kugelhahn d63 (senkrecht nach unten) -> Tiefleitung unter Leitung und Filter-Stamm -> senkrecht hoch zu einem T d63 im Stamm hinter dem Filterauslauf.
    Die Pool-Filter-Leitung I["pf"] und der Stamm I["st"] werden an den T-Stuecken geteilt (pf / pf_m / Rest, st / st_b); spar = Parametername der T-Lage auf der Grabenstrecke, leg = Index des Stammschenkels (q[leg] -> q[leg + 1]), auf dem das T im Stamm sitzt."""
    tr = {t["id"]: t for t in neu["trassen"]}; ts = {t["id"]: t for t in neu["t_stuecke"]}
    pf, pf_m, st, st_b, kante = I["pf"], I["pf_m"], I["st"], I["st_b"], I["kante"]
    t4n, t1n, t5n, t6n, khn = I["t4"], I["t1"], I["t5"], I["t6"], I["kh"]
    k01, kt = tr[pf], tr[st]
    f = [tuple(p) for p in k01["pfad"]]; g0, g1 = f[2], f[3]; zu = g0[2]
    gh = unit((g1[0] - g0[0], g1[1] - g0[1], 0.0))
    t5 = add(g0, gh, s_alt(neu, pf, g0, gh, P[spar]))
    q = [tuple(p) for p in kt["pfad"]]; v3, v4 = q[leg], q[leg + 1]; uu = unit(sub(v3, v4))
    al = dot(sub(t5, v4), uu); t6 = add(v4, uu, al)
    dh = int(k01["dn"]); a63 = ta(63); lkh = LT.ports("lt_kugelhahn_d63")[1][1][2]
    abz = ta(dh) + (lred(dh, 63) if dh != 63 else 0.0)                      # Abgang des Bypass-T auf der Heberleitung (d75: Arm + Reduziermuffe d75/d63; Rohrstueck 2 t dazwischen)
    if not (a63 + 120 < al < math.dist(v3, v4) - a63 - 120): raise SystemExit("%s: T im Stamm liegt zu nah an einem Knick (%.0f von %.0f)" % (kante, al, math.dist(v3, v4)))
    down = (0.0, 0.0, -1.0)
    pa = (t5[0], t5[1], zu - abz); pb = add(pa, down, lkh)                  # Kugelhahn: Muffenebene A direkt am Ausgang des T (Rohrstueck d63 2 t), B darunter
    zc = pb[2] - P["lt_k56_tief"]; ca = (t5[0], t5[1], zc); cb = (t6[0], t6[1], zc)
    neu["r_stuecke"].append({"id": khn, "art": "kugelhahn", "pos_a": rd(pa), "dir": list(down), "d_gross": 63, "d_klein": 63,
                             "notiz": "Kugelhahn d63 %s (Normalbetrieb zu, Stoerfall auf); Handrad nicht erreichbar im Graben: Schacht mit Deckel in S6" % kante})
    # Pool-Filter-Leitung teilen: pf (Pool -> T5), pf_m (T5 -> T4)
    kc = dict(k01); kc["pfad"] = [rd(p) for p in f[:3]] + [rd(t5)]; kc["ende"] = "t:" + t5n; kc["baender"] = ["W", "W", "U"]
    km = dict(k01); km["id"] = pf_m; km["pfad"] = [rd(t5), k01["pfad"][3]]; km["start"] = "t:" + t5n; km["ende"] = "t:" + t4n; km["baender"] = ["U"]
    km["notiz"] = "%s (Teil 2): vom T d75 des Notbypasses %s bis zum T d75 des Absetzer-Zulaufs %s (Heber, Graben Z %g)." % (pf, kante, I["abs"], zu)
    neu["trassen"][neu["trassen"].index(k01)] = kc; neu["trassen"].insert(neu["trassen"].index(kc) + 1, km)
    for p in ts[t4n]["ports"]:
        if p["trasse"] == pf: p["trasse"] = pf_m
    # Stamm teilen: st (Filter -> T6), st_b (T6 -> T1)
    k6 = dict(kt); k6["pfad"] = [rd(p) for p in q[:leg + 1]] + [rd(t6)]; k6["ende"] = "t:" + t6n
    kb = dict(kt); kb["id"] = st_b; kb["pfad"] = [rd(t6)] + [rd(p) for p in q[leg + 1:]]; kb["start"] = "t:" + t6n
    kb["notiz"] = "%s (Teil 2): vom T d63 des Notbypasses %s bis zum T d63/d50/d50 (%s) vor den Pumpen." % (st, kante, t1n)
    neu["trassen"][neu["trassen"].index(kt)] = k6; neu["trassen"].insert(neu["trassen"].index(k6) + 1, kb)
    for p in ts[t1n]["ports"]:
        if p["trasse"] == st: p["trasse"] = st_b
    neu["trassen"] += [
        {"id": I["a"], "kante": kante, "dn": 63, "farbe": "dunkelblau", "start": "t:" + t5n, "ende": "r:" + khn, "band": "UT", "anschluss": [], "pfad": [rd(t5), rd(pa)],
         "notiz": "Abzweig vom T d75 auf %s senkrecht nach unten bis zum Kugelhahn" % pf},
        {"id": I["b"], "kante": kante, "dn": 63, "farbe": "dunkelblau", "start": "r:" + khn, "ende": "t:" + t6n, "band": "UT", "anschluss": [], "pfad": [rd(pb), rd(ca), rd(cb), rd(t6)],
         "notiz": "Kugelhahn -> %g mm abwaerts -> %.0f mm Tiefleitung (Z %.0f) unter %s und Stamm %s -> senkrecht hoch zum T d63 im Stamm hinter dem Filterauslauf (Netz %s: Anschluss an die Saugleitung hinter dem Filterauslauf)" % (P["lt_k56_tief"], math.dist(ca, cb), zc, pf, st, kante)}]
    neu["t_stuecke"] += [
        {"id": t5n, "pos": rd(t5), "d": dh, "ports": [{"trasse": pf, "ende": "ende", "d": dh}, {"trasse": pf_m, "ende": "start", "d": dh}, {"trasse": I["a"], "ende": "start", "d": 63}],
         "notiz": "T d%d auf %s, Zweig d63 senkrecht nach unten (Notbypass %s)%s" % (dh, pf, kante, "" if dh == 63 else ": Rohrstueck d%d + Reduziermuffe d%d/d63" % (dh, dh))},
        {"id": t6n, "pos": rd(t6), "d": 63, "ports": [{"trasse": st, "ende": "ende", "d": 63}, {"trasse": st_b, "ende": "start", "d": 63}, {"trasse": I["b"], "ende": "ende", "d": 63}],
         "notiz": "T d63 im Filter-Stamm, Zweig senkrecht nach unten (Notbypass %s)" % kante}]

def linie1_bypass(L, neu):
    bypass(L, neu, IDS1, "lt_k56_s", 3)

IDS2 = {"pf": "K17", "pf_m": "K17-m", "st": "K22-T", "st_b": "K22-T-b", "abs": "K21", "t4": "T12", "t1": "T11", "t5": "T13", "t6": "T14", "kh": "KH2", "kante": "K57", "a": "K57-a", "b": "K57-b"}

def axis_hit(c, hdeg, tip, o):
    """Strahl c + s * h(hdeg) schneidet die waagerechte Achse des Stutzens (Spitze tip, Oeffnung o): Fusspunkt und Strahllaenge s."""
    hh = h(hdeg); den = hh[0] * o[1] - hh[1] * o[0]
    s = ((tip[0] - c[0]) * o[1] - (tip[1] - c[1]) * o[0]) / den
    if s <= 0: raise SystemExit("Zweig trifft die Saugachse nicht (s %.0f)" % s)
    return add(c, hh, s), s

def linie2_s2a(L, neu):
    """K17 Pool -> Feinfilter West B (Heber), Stamm K22-T Filterauslauf -> T d63/d50/d50 (Bogen 45, 45, 90), K22 T -> Pumpe_gross:3 (geradeaus), K18 T -> Pumpe_gross:4 (M10-S2c).
    Auslauf liegt 24 mm neben der Saugachse von Pumpe 4, aber der Filterkasten steht vor beiden Saugachsen: das T sitzt oestlich des Filters (Suche ueber T-Lagen, siehe lt_k22_*)."""
    aus, aus_o, _ = port(L["filter"], "feinfilter", "aus")
    pump = [port(L["pumpe_gross"][i], "pumpe_gross", "saug") for i in (0, 1)]
    pool_filter(L, neu, "K17")
    z = aus[2]
    h0 = ang(aus_o); hs1, hs2, hr = h0 + 45, h0 + 90, h0 + 180
    v1 = add(aus, aus_o, r45(63))                                           # erster Bogen ist ein 45-Grad-Bogen, direkt auf den Auslaufstutzen gesteckt
    p2 = add(v1, h(hs1), P["lt_k22_l1"])
    tt = (P["lt_k22_t_x"], P["lt_k22_t_y"], z)
    ha, hb = h(hs2), h(hr)
    det = ha[0] * hb[1] - ha[1] * hb[0]; dx, dy = tt[0] - p2[0], tt[1] - p2[1]
    l2, l3 = (dx * hb[1] - dy * hb[0]) / det, (ha[0] * dy - ha[1] * dx) / det        # p2 + l2 * h(hs2) + l3 * h(hr) = T
    p3 = add(p2, ha, l2)
    neu["trassen"].append({"id": "K22-T", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T11", "band": "U", "anschluss": [L["filter"]],
        "pfad": [rd(p) for p in (aus, v1, p2, p3, tt)], "notiz": "Stamm d63 zwischen Filterauslauf und T (gehoert zu K18 und K22: Netz fuehrt dort d50, T-Stueck d63/d50/d50 laut Netz-Bemerkung K22); Richtungen %.0f / %.0f / %.0f / %.0f Grad, Schenkel %g / %.0f / %.0f mm, um den Filterkasten herum nach Osten" % (h0, hs1, hs2, hr, P["lt_k22_l1"], l2, l3)})
    # K22: T geradeaus (Richtung hr) auf die Saugachse von Pumpe_gross:3, Riser, Zulauf in den Stutzen
    tip, o, _ = pump[0]; fp, s = axis_hit(tt, hr, tip, o)
    r = (fp[0], fp[1], z); up = (fp[0], fp[1], tip[2])
    neu["trassen"].append({"id": "K22", "kante": "K22", "dn": 50, "farbe": "dunkelblau", "start": "t:T11", "ende": "stutzen", "baender": ["U", "W", "W"], "anschluss": [L["pumpe_gross"][0], L["tank_gross"]], "pfad": [rd(tt), rd(r), rd(up), rd(tip)],
        "notiz": "T geradeaus %.0f mm (Richtung %.0f Grad) -> Riser auf Saugstutzenhoehe Z %.0f -> %.0f mm Zulauf in den Saugstutzen %s (Stutzenspitze x %.1f y %.1f)" % (s, hr, tip[2], math.dist(up, tip), L["pumpe_gross"][0], tip[0], tip[1])})
    # K18: T nach links (hr + 90), Schenkel lt_k18_l0, 45 Grad zur Saugachse von Pumpe_gross:4, Riser, Zulauf
    tip, o, _ = pump[1]; c = add(tt, h(hr + 90), P["lt_k18_l0"]); fp, s = axis_hit(c, hr + 135, tip, o)
    r = (fp[0], fp[1], z); up = (fp[0], fp[1], tip[2])
    neu["trassen"].append({"id": "K18", "kante": "K18", "dn": 50, "farbe": "dunkelblau", "start": "t:T11", "ende": "stutzen", "baender": ["U", "U", "W", "W"], "anschluss": [L["pumpe_gross"][1], L["tank_gross"]], "pfad": [rd(tt), rd(c), rd(r), rd(up), rd(tip)],
        "notiz": "T nach links %g mm (Richtung %.0f Grad) -> 45 Grad weiter %.0f mm bis zur Saugachse -> Riser auf Z %.0f -> %.0f mm Zulauf in den Saugstutzen %s (Stutzenspitze x %.1f y %.1f)" % (P["lt_k18_l0"], hr + 90, s, tip[2], math.dist(up, tip), L["pumpe_gross"][1], tip[0], tip[1])})
    neu["t_stuecke"].append({"id": "T11", "pos": rd(tt), "d": 63, "ports": [{"trasse": "K22-T", "ende": "ende", "d": 63}, {"trasse": "K22", "ende": "start", "d": 50}, {"trasse": "K18", "ende": "start", "d": 50}],
                             "notiz": "T d63 aus lt_t_d63 + je Ausgang Rohrstueck d63 (2 t) + Reduziermuffe d63/d50"})

def linie2_biofilter(L, neu):
    """K25 Pumpe_gross:4 (steht unter dem Zulauf-Stutzen) -> hoch -> unter der Plattform hinaus -> Steigrohr auf der Stutzenachse -> zurueck auf der Achse zum T d50; K24 Pumpe_gross:3 -> hoch -> nach Norden hinaus -> Steigrohr -> um den Tank herum
    ueber dem Filter -> von der Seite zum T; T d50 -> Stamm d50 -> Reduziermuffe d63/d50 auf den Zulauf-Stutzen; K26 Ueberlauf d63 -> Reduziermuffe -> Rohr d50, offenes Ende am Verteilerplatz (M10-S2c)."""
    tg = L["tank_gross"]; p3, p4 = (port(L["pumpe_gross"][i], "pumpe_gross", "druck") for i in (0, 1))
    zt, zo, _ = port(tg, "tank_gross", "zulauf"); ut, uo, _ = port(tg, "tank_gross", "ueberlauf")
    zh = zt[2]; R40 = r90(40); up = (0.0, 0.0, 1.0)
    un = (zo[1], -zo[0], 0.0)                                                # waagerecht senkrecht zur Zulauf-Achse, zeigt zur Pumpe-3-Seite
    t2 = add(zt, zo, P["lt_k25_s"]); pc = add(zt, zo, P["lt_k25_sc"])
    c1 = add(p4[0], up, R40); k25 = [p4[0], c1, (pc[0], pc[1], c1[2]), (pc[0], pc[1], zh), t2]
    d1 = add(p3[0], up, R40); n2 = add(p3[0], un, P["lt_k24_n"]); c3 = (n2[0], n2[1], zh)
    l3 = dot(sub(t2, c3), zo); c4 = add(c3, zo, l3)
    if l3 <= 0: raise SystemExit("K24: Querschenkel hat keine Laenge (%.0f)" % l3)
    k24 = [p3[0], d1, (n2[0], n2[1], d1[2]), c3, c4, t2]
    rz, pb = stutzen_red(zt, zo, 63, 50)
    neu["r_stuecke"].append(dict(id="R_ZUL2", **rz))
    neu["trassen"] += [
        {"id": "K24", "kante": "K24", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T15", "baender": ["W", "W", "WH", "WH", "WH"], "anschluss": [L["pumpe_gross"][0], tg],
         "pfad": [rd(p) for p in k24], "notiz": "Druckstutzen %s (Z %.0f) -> hoch auf Z %.0f -> %g mm nach Norden unter der Plattform hinaus -> Steigrohr auf Zulaufhoehe Z %.0f -> %.0f mm nach WSW um den Tank (ueber dem Filter) -> %.0f mm von der Seite zum T d50 auf der Zulauf-Achse" % (L["pumpe_gross"][0], p3[0][2], d1[2], P["lt_k24_n"], zh, l3, math.dist(c4, t2))},
        {"id": "K25", "kante": "K25", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T15", "baender": ["W", "W", "WH", "WH"], "anschluss": [L["pumpe_gross"][1], tg],
         "pfad": [rd(p) for p in k25], "notiz": "Druckstutzen %s (Z %.0f, unter dem Zulauf-Stutzen) -> hoch auf Z %.0f -> %.0f mm unter der Plattform hinaus -> Steigrohr bei %g mm vor der Zulaufspitze auf der Achse -> Z %.0f -> %.0f mm auf der Achse zurueck zum T d50" % (L["pumpe_gross"][1], p4[0][2], c1[2], math.dist(k25[1], k25[2]), P["lt_k25_sc"], zh, math.dist(k25[3], t2))},
        {"id": "K24-K25-Stamm", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T15", "ende": "r:R_ZUL2", "band": "WH", "anschluss": [tg], "pfad": [rd(t2), rd(pb)],
         "notiz": "vereinigte Druckleitung d50 (Netz K24/K25: vereinigt vor dem Tank zu d50) vom T auf der Zulauf-Achse bis zur Reduziermuffe d63/d50 auf dem Zulauf-Stutzen d63 des Biofilters (Z %.0f)" % zh}]
    neu["t_stuecke"].append({"id": "T15", "pos": rd(t2), "d": 50, "ports": [{"trasse": "K25", "ende": "ende", "d": 40}, {"trasse": "K24-K25-Stamm", "ende": "start", "d": 50}, {"trasse": "K24", "ende": "ende", "d": 40}],
                             "notiz": "T d50: Gerade = K25 und Stamm auf der Zulauf-Achse, Abzweig = K24; Eingaenge d40 mit Rohrstueck d50 + Reduziermuffe d50/d40"})
    ru, pbu = stutzen_red(ut, uo, 63, 50)
    neu["r_stuecke"].append(dict(id="R_UEB2", **ru))
    ende = add(pbu, uo, P["lt_k10_len"])
    neu["trassen"].append({"id": "K26", "kante": "K26", "dn": 50, "farbe": "dunkelblau", "start": "r:R_UEB2", "ende": "offen", "band": "WH", "anschluss": [tg], "pfad": [rd(pbu), rd(ende)],
        "notiz": "Ueberlauf-Stutzen d63 (Z %.0f = 1570 relativ) -> Reduziermuffe d63/d50 -> %g mm Rohr d50 nach aussen; das offene Ende (x %.0f y %.0f) ist der Verteiler-Eingang (Verteilerplatz Linie 2, Verteiler d50 in S3)" % (ut[2], P["lt_k10_len"], ende[0], ende[1])})

def linie2_absetzer(L, neu, alt):
    """Absetzerkreis Linie 2 (M10-S2c): K19 ab dem offenen Linie-2-Stumpf des Bodenablaufs (Linie 1, S2b) unter dem Pool nach Sueden, 45 Grad, Steigrohr auf der Saugachse von Pumpe_klein:1 -> Reduziermuffe d50/d40 -> Saugstutzen;
    K20 Druckstutzen d32 -> Absetzer-Zulauf (Tank_klein:1, wie K04); K21 Absetzer-Auslass d50 mit Gefaelle -> Fallrohr -> unterflur nach Norden und Westen -> T d63 auf K17."""
    ab = L["absetzer"]; pk = L["pumpe_klein"][0]
    st = [t for t in alt.get("trassen", []) if t["id"] == "K03-K19-Stumpf"]
    if not st: raise SystemExit("Linie 1 fehlt: erst trassen_linie.py 1 laufen lassen (Stumpf K03-K19-Stumpf)")
    stumpf = tuple(st[0]["pfad"][-1])
    saug, so, _ = port(pk, "pumpe_klein", "saug"); druck, _, _ = port(pk, "pumpe_klein", "druck")
    R50, R32 = r90(50), r90(32)
    # ---- K19: Stumpf (Z -1635, Richtung Sued) -> Ecke 45 Grad -> Fusspunkt unter der Saugachse -> Steigrohr -> Saugachse -> Reduziermuffe d50/d40
    zt = stumpf[2]; c4 = add(saug, so, P["lt_k19_foot"]); c3 = (c4[0], c4[1], zt)
    pa_ = (stumpf[0], c3[1] + abs(c3[0] - stumpf[0]), zt)
    lr = lred(50, 40); pos_a = add(saug, so, lr + 120.0); pos_b = add(saug, so, 120.0)
    din = tuple(-v for v in so)
    neu["r_stuecke"].append({"id": "R_K19", "pos_a": rd(pos_a), "dir": [round(v, 6) for v in din], "d_gross": 50, "d_klein": 40})
    neu["trassen"] += [
        {"id": "K19-Tief", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "r:R_K19", "baender": ["UT", "UT", "UT", "W"], "anschluss": [pk, ab], "pfad": [rd(p) for p in (stumpf, pa_, c3, c4, pos_a)],
         "notiz": "ab dem Linie-2-Stumpf (Kupplung auf dem offenen Ende, Z %.0f): %.0f mm nach Sueden unter dem Pool -> 45 Grad -> %.0f mm -> Steigrohr bei %g mm vor dem Saugstutzen auf Saughoehe Z %.0f -> zur Reduziermuffe d50/d40" % (zt, math.dist(stumpf, pa_), math.dist(pa_, c3), P["lt_k19_foot"], c4[2])},
        {"id": "K19", "kante": "K19", "dn": 40, "farbe": "dunkelblau", "start": "r:R_K19", "ende": "stutzen", "band": "W", "anschluss": [pk, ab], "pfad": [rd(pos_b), rd(saug)],
         "notiz": "Reduziermuffe d50/d40 -> Saugstutzen %s (d40, Z %.0f)" % (pk, saug[2])}]
    # ---- K20: wie K04 (lt_k04_y)
    m = MV[ab]; zul, zo, _ = port(ab, "tank_klein", "zulauf")
    loc = lambda p: (m[0] * (p[0] - m[3]) + m[4] * (p[1] - m[7]), m[1] * (p[0] - m[3]) + m[5] * (p[1] - m[7]))
    wl = lambda x, y, z: (m[0] * x + m[1] * y + m[3], m[4] * x + m[5] * y + m[7], z)
    rk, pb = stutzen_red(zul, zo, 50, 32); neu["r_stuecke"].append(dict(id="R_K20", **rk))
    xd = loc(druck)[0]; xz = loc(zul)[0]; ky = -P["lt_k04_y"]; z1 = druck[2] + R32
    k20 = [druck, (druck[0], druck[1], z1), wl(xd, ky, z1), wl(xd, ky, zul[2]), wl(xz, ky, zul[2]), pb]
    neu["trassen"].append({"id": "K20", "kante": "K20", "dn": 32, "farbe": "dunkelblau", "start": "stutzen", "ende": "r:R_K20", "baender": ["W", "W", "WH", "WH", "WH"], "anschluss": [pk, ab], "pfad": [rd(p) for p in k20],
        "notiz": "Druckstutzen %s (d32, Z %.0f) -> hoch auf Z %.0f -> %.0f mm zur Plattform hinaus -> Steigrohr auf Zulaufhoehe Z %.0f -> %.0f mm an der Tankwand entlang -> Reduziermuffe d50/d32 auf dem Zulauf-Stutzen" % (pk, druck[2], z1, math.dist(k20[1], k20[2]), zul[2], math.dist(k20[3], k20[4]))})
    # ---- K21: Auslauf-Stutzen d50 -> Bogen -> Fallrohr -> Norden -> Westen -> 45 Grad senkrecht auf die K17-Grabenstrecke, T d75 (Zweig d50); Gefaelle nach hinten gerechnet
    k17 = [t for t in neu["trassen"] if t["id"] == "K17"][0]; neu["trassen"].remove(k17)
    f = [tuple(p) for p in k17["pfad"]]; g0, g1 = f[2], f[3]; zu = g0[2]
    gh = unit((g1[0] - g0[0], g1[1] - g0[1], 0.0)); ph = (-gh[1], gh[0], 0.0)
    t4 = add(g0, gh, s_alt(neu, "K17", g0, gh, P["lt_k21_s"]))
    aus, ao, _ = port(ab, "tank_klein", "auslauf"); pct = P["lt_k05_pct"] / 100.0; l1 = R50 + P["lt_k05_vor"]; lb = P["lt_k21_lb"]
    a1 = add(aus, ao, l1); a1 = (a1[0], a1[1], a1[2] - pct * l1)
    side = 1.0 if dot(sub(a1, t4), ph) > 0 else -1.0
    cw = add(t4, ph, side * lb)
    # M10-S2R: der Graben K17 liegt mit den d75-Ecken nicht mehr auf 225 Grad; der Querschenkel cw -> T steht senkrecht auf ihm (Richtung th3), davor ein 45-Grad-Knick (Lauf th2, moeglichst nach Westen),
    # davor 90 Grad (Lauf th1, moeglichst nach Norden): die beiden Laeufe sind um den Grabenwinkel gedreht statt achsparallel, die Knicke bleiben 45 und 90 Grad
    th3 = ang(sub(t4, cw)); wd = lambda a: abs((a - 180.0 + 180.0) % 360.0 - 180.0)
    th2 = min((th3 + 45.0, th3 - 45.0), key=wd); th1 = min((th2 + 90.0, th2 - 90.0), key=lambda a: abs((a - 90.0 + 180.0) % 360.0 - 180.0))
    d1, d2 = h(th1), h(th2); det = d1[0] * d2[1] - d1[1] * d2[0]; rx, ry = cw[0] - a1[0], cw[1] - a1[1]
    ln, lw = (rx * d2[1] - ry * d2[0]) / det, (d1[0] * ry - d1[1] * rx) / det     # a1 + ln * d1 + lw * d2 = cw
    if ln <= 0 or lw <= 0: raise SystemExit("K21: Nord-/Westschenkel haben keine Laenge (%.0f / %.0f)" % (ln, lw))
    c1, c2 = add(a1, d1, ln), cw
    z4 = zu + pct * lb; z3 = z4 + pct * lw; z2 = z3 + pct * ln
    k21 = [aus, a1, (a1[0], a1[1], z2), (c1[0], c1[1], z3), (cw[0], cw[1], z4), t4]
    neu["trassen"].append({"id": "K21", "kante": "K21", "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T12", "baender": ["WH", "U", "U", "U", "U"], "gefaelle_pct": 1.0, "anschluss": [ab], "pfad": [rd(p) for p in k21],
        "notiz": "Auslauf-Stutzen %s (d50, Z %.0f) -> Bogen -> Fallrohr auf Z %.0f -> %.0f mm nach Norden (Richtung %.1f Grad, Gefaelle %.1f %%) -> %.0f mm nach Westen (Richtung %.1f Grad) -> %.0f mm unter 45 Grad senkrecht auf die K17-Grabenstrecke zum T d75 (Zweig d50, Z %.0f)" % (ab, aus[2], z2, ln, th1, P["lt_k05_pct"], lw, th2, lb, zu)})
    kc = dict(k17); kc["id"] = "K17"; kc["pfad"] = [rd(p) for p in f[:3]] + [rd(t4)]; kc["baender"] = ["W", "W", "U"]; kc["ende"] = "t:T12"
    kc["notiz"] = k17["notiz"] + " Hier bis zum T d75 des Absetzer-Zulaufs K21 (Teil 1)."
    kd = dict(k17); kd["id"] = "K17-b"; kd["pfad"] = [rd(t4)] + [rd(p) for p in f[3:]]; kd["baender"] = ["U", "W", "W"]; kd["start"] = "t:T12"
    kd["notiz"] = "K17 (Teil 2): vom T d75 des Absetzer-Zulaufs K21 bis zum Feinfilter-Einlauf (Heber, Graben Z %g)." % zu
    neu["trassen"] += [kc, kd]
    neu["t_stuecke"].append({"id": "T12", "pos": rd(t4), "d": HD, "ports": [{"trasse": "K17", "ende": "ende", "d": HD}, {"trasse": "K17-b", "ende": "start", "d": HD}, {"trasse": "K21", "ende": "ende", "d": 50}],
                             "notiz": "T d75 im Einlauf der K17 (Netz K21: T-Stueck mit Seitenablauf); Zweig d50 mit Rohrstueck d75 + Reduziermuffe d75/d50"})

def linie2_bypass(L, neu):
    bypass(L, neu, IDS2, "lt_k57_s", 2)

# ======================================================================================================================
# M10-UMBAU (05.11.2026, docs/leitungsordnung.md): Linie 1 im Welt-Rahmen. Waagerechte Rohre nur in X oder Y, sonst lotrecht; schraege Bauteil-Ports
# (Feinfilter, Tank-Zulauf/-Ueberlauf, Absetzer) bekommen hoechstens 300 mm in Port-Richtung (Ausnahme 2), dann einen 90-Grad-Bogen lotrecht:
# der Steiger entkoppelt das Azimut, der naechste 90-Grad-Bogen geht in eine Weltachse (Etage nach R3). Der Heber K01 bleibt unveraendert (Ausnahme 1);
# K05 und der Bypass K56 schliessen lotrecht von unten an seine T-Stuecke an. Lagen und Hoehen der Lagen-Konstanten unten: Montage M10-UMBAU [A].
U1 = {"z_stamm": 14.0,            # Grabensohle Stamm K06-T (Rohrachse): Filterauslauf Z 214 minus Etage 200 (2 Boegen d63 + Rohrstueck)
      "x_steig": 3000.0,          # x der Pumpen-Saugsteiger K06/K02 (186 mm vor den Saugstutzen, ausserhalb der Standwinkel)
      "x_t6": 3550.0,             # T6 (Bypass-Anschluss) auf der Stamm-Strecke y = Filter-Etage
      "z_druck": 900.0,           # K08/K09 waagerecht ueber der Pumpen-Montagetafel (Oberkante Z 863)
      "x_k08": 2770.0,            # K08 laeuft westlich am Biofilter-Tank vorbei (Tank-Radius 465, Bein bei x 2915; Grobkasten check_leitungen)
      "l_zul": 150.0,             # Stamm zum Tank-Zulauf: Laenge in Port-Richtung vor dem Bogen
      "l_ueb": 100.0,             # K10 Ueberlauf: Laenge in Port-Richtung bis zum Verteiler-Platz (M10-UMBAU Schritt 6)
      "z_k04": 780.0,             # K04 waagerecht ueber der Montagetafel der kleinen Pumpe (Oberkante Z 745)
      "l_k04": 150.0,             # K04: Laenge in Port-Richtung vor dem Zulauf-Stutzen
      "z_k05": -40.0,             # K05 Grabenstrecke am Fallrohr (danach 1,5 % Gefaelle bis unter T4)
      "x_k05": 3260.0}            # K05 Nordlauf: >= 250 mm Achsabstand zum Stamm (x 3000) und Platz fuer den Schacht an KH1 (x 2588)

def baender_auto(pfad, fz=400.0):
    """Hoehenband je Teilstueck fuer check_leitungen.py (BANDS, Z relativ zum Flur): Steiger 'W' (kein Bandtest), sonst U / UT / W / WH nach der mittleren Hoehe."""
    out = []
    for a, b in zip(pfad[:-1], pfad[1:]):
        if math.hypot(a[0] - b[0], a[1] - b[1]) < 20.0: out.append("W" if max(a[2], b[2]) > fz else "U"); continue
        z = (a[2] + b[2]) / 2 - fz
        out.append("UT" if z < -400 else "U" if z < -50 else "W" if z <= 1000 else "WH")
    return out

def linie1_ordnung(L, neu):
    G = L["G"]; up = (0.0, 0.0, 1.0); z0 = U1["z_stamm"]; xs = U1["x_steig"]
    pool_filter(L, neu, "K01")
    k01 = neu["trassen"][-1]; f = [tuple(p) for p in k01["pfad"]]; g0, g1 = f[2], f[3]; zu = g0[2]
    gh = unit((g1[0] - g0[0], g1[1] - g0[1], 0.0))
    t5 = add(g0, gh, s_alt(neu, "K01", g0, gh, P["lt_k56_s"])); t4 = add(g0, gh, s_alt(neu, "K01", g0, gh, P["lt_k05_s"]))
    # ---------------- Heber teilen: K01 (Pool -> T5), K01-m (T5 -> T4), K01-b (T4 -> Filter); Pfad und Formstuecke wie Runde 70
    neu["trassen"].remove(k01)
    for nid, pf, st, en, bd in (("K01", f[:3] + [t5], k01["start"], "t:T5", ["W", "W", "U"]), ("K01-m", [t5, t4], "t:T5", "t:T4", ["U"]), ("K01-b", [t4] + f[3:], "t:T4", k01["ende"], ["U", "W", "W"])):
        e = dict(k01); e.update(id=nid, pfad=[rd(p) for p in pf], start=st, ende=en, baender=bd, korridor=["KS" if abs(pf[i][2] - pf[i + 1][2]) > 1 and math.hypot(pf[i][0] - pf[i + 1][0], pf[i][1] - pf[i + 1][1]) < 1 else ("KG" if pf[i][2] < 400 else "KH") for i in range(len(pf) - 1)])
        neu["trassen"].append(e)
    # ---------------- Stamm K06-T: Filterauslauf -> Bogen auf dem Stutzen lotrecht -> Grabensohle z0 -> -X (T6) -> -Y (T1)
    aus, ao, _ = port(L["filter"], "feinfilter", "aus")
    p1 = add(aus, ao, r90(63)); p2 = (p1[0], p1[1], z0); ys = p2[1]
    t6 = (U1["x_t6"], ys, z0); c = (xs, ys, z0)
    sg, so, _ = port(L["pumpe_gross"][0], "pumpe_gross", "saug"); s2, _, _ = port(L["pumpe_gross"][1], "pumpe_gross", "saug")
    t1 = (xs, s2[1], z0)
    neu["trassen"] += [
        {"id": "K06-T", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T6", "korridor": ["KG", "KS", "KG"], "anschluss": [L["filter"]], "pfad": [rd(p) for p in (aus, p1, p2, t6)],
         "notiz": "Filterauslauf (Az %.0f) -> Bogen d63 direkt auf dem Stutzen lotrecht -> Etage auf Z %g -> nach -X zum T6 (Bypass)" % (ang(ao), z0)},
        {"id": "K06-T-b", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "t:T6", "ende": "t:T1", "korridor": ["KG", "KG"], "anschluss": [], "pfad": [rd(p) for p in (t6, c, t1)],
         "notiz": "T6 -> -X bis x %g -> -Y zum T1 (Abgaenge K06 geradeaus, K02 lotrecht)" % xs}]
    for kid, tip, a0, kor in (("K06", sg, t1, ["KG", "KS", "KH"]), ("K02", s2, t1, ["KS", "KH"])):
        pf = [a0, (xs, tip[1], z0), (xs, tip[1], tip[2]), tip] if kid == "K06" else [a0, (xs, tip[1], tip[2]), tip]
        neu["trassen"].append({"id": kid, "kante": kid, "dn": 50, "farbe": "dunkelblau", "start": "t:T1", "ende": "stutzen", "korridor": kor, "anschluss": [L["pumpe_gross"][0]] if kid == "K06" else [L["pumpe_gross"][1], L["tank_gross"]], "pfad": [rd(p) for p in pf],
            "notiz": "T1 -> Steiger bei x %g auf Saughoehe Z %.0f -> waagerecht +X in den Saugstutzen" % (xs, tip[2])})
    neu["t_stuecke"].append({"id": "T1", "pos": rd(t1), "d": 63, "ports": [{"trasse": "K06-T-b", "ende": "ende", "d": 63}, {"trasse": "K06", "ende": "start", "d": 50}, {"trasse": "K02", "ende": "start", "d": 50}],
                             "notiz": "T d63, K06 geradeaus (-Y), K02 lotrecht nach oben; je Abgang Rohrstueck d63 + Reduziermuffe d63/d50"})
    # ---------------- Bypass K56: T5 (Heber) -> Kugelhahn KH1 lotrecht -> Tiefleitung +X, -Y -> lotrecht hoch in T6
    a63 = ta(63); lkh = LT.ports("lt_kugelhahn_d63")[1][1][2]; abz = ta(HD) + lred(HD, 63)
    pa = (t5[0], t5[1], zu - abz); pb = add(pa, (0.0, 0.0, -1.0), lkh); zc = pb[2] - P["lt_k56_tief"]
    neu["r_stuecke"].append({"id": "KH1", "art": "kugelhahn", "pos_a": rd(pa), "dir": [0.0, 0.0, -1.0], "d_gross": 63, "d_klein": 63,
                             "notiz": "Kugelhahn d63 K56 (Normalbetrieb zu, Stoerfall auf); Schacht in S2N/S6"})
    yk = ys - 200.0   # Tiefleitung 200 mm suedlich des Stamms: eigener Graben (unter dem Stamm fielen die Grabenflaechen zusammen, Erdflaechen-Schnitt ohne Ergebnis, Build 71)
    k56 = [pb, (t5[0], t5[1], zc), (t5[0], yk, zc), (t6[0], yk, zc), (t6[0], yk, z0), t6]   # -Y unter dem Stamm durch, +X, lotrecht hoch, +Y waagerecht in T6
    neu["trassen"] += [
        {"id": "K56-a", "kante": "K56", "dn": 63, "farbe": "dunkelblau", "start": "t:T5", "ende": "r:KH1", "korridor": ["KS"], "anschluss": [], "pfad": [rd(t5), rd(pa)], "notiz": "Abzweig vom T d75 auf K01 lotrecht nach unten bis zum Kugelhahn"},
        {"id": "K56-b", "kante": "K56", "dn": 63, "farbe": "dunkelblau", "start": "r:KH1", "ende": "t:T6", "korridor": ["KS", "KG", "KG", "KS", "KG"], "anschluss": [], "pfad": [rd(p) for p in k56],
         "notiz": "Kugelhahn -> Tiefleitung Z %.0f -Y unter dem Stamm durch, +X bis x %g -> lotrecht auf Z %g -> 200 mm +Y in T6" % (zc, t6[0], z0)}]
    neu["t_stuecke"] += [
        {"id": "T5", "pos": rd(t5), "d": HD, "ports": [{"trasse": "K01", "ende": "ende", "d": HD}, {"trasse": "K01-m", "ende": "start", "d": HD}, {"trasse": "K56-a", "ende": "start", "d": 63}],
         "notiz": "T d75 auf K01, Zweig d63 lotrecht nach unten (Notbypass K56): Rohrstueck d75 + Reduziermuffe d75/d63"},
        {"id": "T6", "pos": rd(t6), "d": 63, "ports": [{"trasse": "K06-T", "ende": "ende", "d": 63}, {"trasse": "K06-T-b", "ende": "start", "d": 63}, {"trasse": "K56-b", "ende": "ende", "d": 63}],
         "notiz": "T d63 im Filter-Stamm, Zweig waagerecht nach Sueden (Notbypass K56)"}]
    # ---------------- Biofilter: K08/K09 Druckstutzen -> Z z_druck -> T2 neben dem Tank; Stamm lotrecht zur Zulaufhoehe -> l_zul in Port-Richtung -> Reduziermuffe
    tg = L["tank_gross"]; zh = U1["z_druck"]
    p8, _, _ = port(L["pumpe_gross"][0], "pumpe_gross", "druck"); p9, _, _ = port(L["pumpe_gross"][1], "pumpe_gross", "druck")
    zt, zo, _ = port(tg, "tank_gross", "zulauf"); rz, pbz = stutzen_red(zt, zo, 63, 50); neu["r_stuecke"].append(dict(id="R_ZUL", **rz))
    c1 = add(pbz, zo, U1["l_zul"]); t2 = (c1[0], c1[1], zh)
    k8 = [p8, (p8[0], p8[1], zh), (U1["x_k08"], p8[1], zh), (U1["x_k08"], t2[1], zh), t2]
    k9 = [p9, (p9[0], p9[1], zh), (p9[0], t2[1], zh), t2]
    neu["trassen"] += [
        {"id": "K08", "kante": "K08", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T2", "korridor": ["KS", "KH", "KH", "KH"], "anschluss": [L["pumpe_gross"][0]], "pfad": [rd(p) for p in k8],
         "notiz": "Druckstutzen -> Z %g -> -X westlich am Biofilter-Tank vorbei -> +Y -> +X ins T2" % zh},
        {"id": "K09", "kante": "K09", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T2", "korridor": ["KS", "KH", "KH"], "anschluss": [L["pumpe_gross"][1], tg], "pfad": [rd(p) for p in k9],
         "notiz": "Druckstutzen -> Z %g ueber die Montagetafel -> +Y unter dem Plattformrand hinaus -> -X ins T2" % zh},
        {"id": "K08-K09-Stamm", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T2", "ende": "r:R_ZUL", "korridor": ["KS", "KH"], "anschluss": [tg], "pfad": [rd(p) for p in (t2, c1, pbz)],
         "notiz": "T2 -> lotrecht auf Zulaufhoehe Z %.0f -> %g mm in Zulauf-Richtung zur Reduziermuffe d63/d50" % (zt[2], U1["l_zul"])}]
    neu["t_stuecke"].append({"id": "T2", "pos": rd(t2), "d": 50, "ports": [{"trasse": "K08", "ende": "ende", "d": 40}, {"trasse": "K09", "ende": "ende", "d": 40}, {"trasse": "K08-K09-Stamm", "ende": "start", "d": 50}],
                             "notiz": "T d50: K08 und K09 gegenueber (X), Stamm lotrecht nach oben"})
    ut, uo, _ = port(tg, "tank_gross", "ueberlauf"); ru, pbu = stutzen_red(ut, uo, 63, 50); neu["r_stuecke"].append(dict(id="R_UEB", **ru))
    neu["trassen"].append({"id": "K10", "kante": "K10", "dn": 50, "farbe": "dunkelblau", "start": "r:R_UEB", "ende": "offen", "korridor": ["KH"], "anschluss": [tg], "pfad": [rd(pbu), rd(add(pbu, uo, U1["l_ueb"]))],
        "notiz": "Ueberlauf d63 -> Reduziermuffe d63/d50 -> %g mm in Port-Richtung; Verteiler d50 folgt (M10-UMBAU Schritt 6)" % U1["l_ueb"]})
    # ---------------- Absetzerkreis: K03 unveraendert (Weltachsen), K04 und K05 neu
    ab = L["absetzer"]; pk = L["pumpe_klein"][0]
    ba = [p for p in G.pool_ports(P["sock_h"]) if p["name"] == "BA_Mitte"][0]; tipb = tuple(ba["ende"])
    saug, so, _ = port(pk, "pumpe_klein", "saug"); druck, _, _ = port(pk, "pumpe_klein", "druck"); R50 = r90(50)
    xr = P["lt_k03_riser_x"]; c4 = add(saug, so, (xr - saug[0]) / so[0]); c4 = (xr, saug[1], saug[2])
    cb = add(tipb, (0.0, 0.0, -1.0), R50); zt3 = cb[2]; t3 = (tipb[0], c4[1], zt3); c3 = (xr, c4[1], zt3)
    lr = lred(50, 40); din = tuple(-v for v in so); pos_b = (saug[0] - 120.0, saug[1], saug[2]); pos_a = (pos_b[0] - lr, saug[1], saug[2])
    stumpf = add(t3, (0.0, -1.0, 0.0), P["lt_l2_stub"])
    neu["r_stuecke"].append({"id": "R_K03", "pos_a": rd(pos_a), "dir": [1.0, 0.0, 0.0], "d_gross": 50, "d_klein": 40})
    neu["trassen"] += [
        {"id": "K03-Tief", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T3", "korridor": ["KS", "KG"], "anschluss": ["Zentralpool"], "pfad": [rd(tipb), rd(cb), rd(t3)], "notiz": "Bodenablauf -> Bogen -> unter dem Pool nach Sueden zum T d50"},
        {"id": "K03-Steig", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T3", "ende": "r:R_K03", "korridor": ["KG", "KS", "KH"], "anschluss": [], "pfad": [rd(t3), rd(c3), rd(c4), rd(pos_a)], "notiz": "T -> +X unter dem Pool hinaus -> Steiger auf Saughoehe -> Reduziermuffe d50/d40"},
        {"id": "K03", "kante": "K03", "dn": 40, "farbe": "dunkelblau", "start": "r:R_K03", "ende": "stutzen", "korridor": ["KH"], "anschluss": [pk, ab], "pfad": [rd(pos_b), rd(saug)], "notiz": "Reduziermuffe d50/d40 -> Saugstutzen %s" % pk},
        {"id": "K03-K19-Stumpf", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T3", "ende": "offen", "korridor": ["KG"], "anschluss": ["Zentralpool"], "pfad": [rd(t3), rd(stumpf)], "notiz": "Linie-2-Zweig bis zur Abzweigung (Netz K19)"}]
    neu["t_stuecke"].append({"id": "T3", "pos": rd(t3), "d": 50, "ports": [{"trasse": "K03-Tief", "ende": "ende", "d": 50}, {"trasse": "K03-Steig", "ende": "start", "d": 50}, {"trasse": "K03-K19-Stumpf", "ende": "start", "d": 50}],
                             "notiz": "T d50: Teilung des gemeinsamen Pool-Bodenablaufs auf Linie 1 und Linie 2"})
    zul, zo4, _ = port(ab, "tank_klein", "zulauf"); rk, pb4 = stutzen_red(zul, zo4, 50, 32); neu["r_stuecke"].append(dict(id="R_K04", **rk))
    c4b = add(pb4, zo4, U1["l_k04"]); z4 = U1["z_k04"]
    k4 = [druck, (druck[0], druck[1], z4), (c4b[0], druck[1], z4), (c4b[0], c4b[1], z4), c4b, pb4]
    neu["trassen"].append({"id": "K04", "kante": "K04", "dn": 32, "farbe": "dunkelblau", "start": "stutzen", "ende": "r:R_K04", "korridor": ["KS", "KH", "KH", "KS", "KH"], "anschluss": [pk, ab], "pfad": [rd(p) for p in k4],
        "notiz": "Druckstutzen -> Z %g -> -X -> -Y -> lotrecht auf Zulaufhoehe Z %.0f -> %g mm in Port-Richtung zur Reduziermuffe d50/d32 (tangentialer Zulauf)" % (z4, zul[2], U1["l_k04"])})
    aus5, ao5, _ = port(ab, "tank_klein", "auslauf"); pct = P["lt_k05_pct"] / 100.0
    a1 = add(aus5, ao5, R50 + P["lt_k05_vor"]); a1 = (a1[0], a1[1], aus5[2] - pct * (R50 + P["lt_k05_vor"]))
    z2 = U1["z_k05"]; xn = U1["x_k05"]; lx1 = xn - a1[0]; ly = t4[1] - a1[1]; lx2 = xn - t4[0]
    k5 = [aus5, a1, (a1[0], a1[1], z2), (xn, a1[1], z2 - pct * lx1), (xn, t4[1], z2 - pct * (lx1 + ly)), (t4[0], t4[1], z2 - pct * (lx1 + ly + lx2)), t4]
    if min(lx1, ly, lx2) < 300: raise SystemExit("K05: Laeufe zu kurz (lx1 %.0f, ly %.0f, lx2 %.0f)" % (lx1, ly, lx2))
    neu["trassen"].append({"id": "K05", "kante": "K05", "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T4", "gefaelle_pct": P["lt_k05_pct"], "korridor": ["KH", "KS", "KG", "KG", "KG", "KS"], "anschluss": [ab], "pfad": [rd(p) for p in k5],
        "notiz": "Auslauf -> Bogen -> Fallrohr auf Z %g -> +X %.0f, +Y %.0f, -X %.0f mm mit %.1f %% Gefaelle -> lotrecht hoch in T4 auf dem Heber" % (z2, lx1, ly, lx2, P["lt_k05_pct"])})
    neu["t_stuecke"].append({"id": "T4", "pos": rd(t4), "d": HD, "ports": [{"trasse": "K01-m", "ende": "ende", "d": HD}, {"trasse": "K01-b", "ende": "start", "d": HD}, {"trasse": "K05", "ende": "ende", "d": 50}],
                             "notiz": "T d75 im Heber, Zweig d50 (K05) lotrecht von unten: Rohrstueck d75 + Reduziermuffe d75/d50"})
    for t in neu["trassen"]:
        if not t.get("baender") and not t.get("band"): t["baender"] = baender_auto(t["pfad"])

# M10-UMBAU Schritt 4 (Runde 72): Linie 2 im Welt-Rahmen nach derselben Methode. Pumpen (161,9 Grad), Biofilter-Tank (-71,8), Absetzer (-176,3) und Feinfilter (-75) stehen schraeg:
# je schraegem Port hoechstens 300 mm in Port-Richtung (Ausnahme 2), dann Steiger, dann Weltachse. Der Feinfilter West steht dicht vor den Pumpen: der Stamm laeuft erst nach Sueden
# unter Pumpe 4 hindurch (Spur y_s), dann nach Osten zur Spur x der Pumpe-3-Steiger, dann nach Norden zum T11; K18 zweigt nach Westen ab und liegt >= 245 mm neben dem Stamm (Stamm-Hahn S2N).
U2 = {"z_stamm": 14.0,            # wie Linie 1: Filterauslauf Z 214 minus Etage 200
      "a_saug": 200.0,            # Pumpen-Saug: Steiger 200 mm vor der Stutzenspitze in Port-Richtung (Ausnahme 2)
      "y_s": -4150.0,             # Stamm-Suedspur: nach der Etage am Filterauslauf >= 300 mm Rohr bis zum naechsten Bogen (R4), suedlich des Pumpe-4-Steigers
      "y_t11": -3400.0,           # T11 auf der Stamm-Nordspur (K22 geradeaus nach Norden, K18 nach Westen)
      "x_t14": -1245.9,           # T14 (Bypass) auf der Stamm-Ostspur genau ueber der Bypass-Spur: der Bypass kommt lotrecht von unten (nur zwei Boegen, keine Kette R4)
      "l_zul": 290.0,             # Biofilter-Zulauf: Stamm-Laenge gegen die Port-Richtung (schraeg, <= 300)
      "z_t15n": 1320.0,           # Hoehe des Stamm-Nordlaufs (das schraege Zulaufstueck braucht davor einen lotrechten Steiger)
      "dy_t15": 500.0,            # Stamm-Nordlauf: T15 liegt 300 mm noerdlich des Steigers (Pumpe 4 steht fast unter dem Stutzen, K25 braucht >= 150 mm Lauf)
      "x_k24": 250.0,             # K24 laeuft 250 mm westlich am T15 vorbei und kommt von Westen
      "y_k24": -2650.0,           # K24 Nordspur ausserhalb von Tank und Plattform (Tankrand y -2869)
      "a_k19": 290.0,             # K19: Steiger 290 mm vor dem Saugstutzen der kleinen Pumpe (Reduziermuffe 120 + 59, Bogen 91)
      "z_k05": -40.0}             # K21 Grabenstrecke am Fallrohr (danach Gefaelle bis unter T12)

def kor_auto(pf):
    return ["KS" if abs(pf[i][2] - pf[i + 1][2]) > 1 and math.hypot(pf[i][0] - pf[i + 1][0], pf[i][1] - pf[i + 1][1]) < 1 else ("KG" if (pf[i][2] + pf[i + 1][2]) / 2 < 400 else "KH") for i in range(len(pf) - 1)]

def linie2_ordnung(L, neu, alt):
    G = L["G"]; z0 = U2["z_stamm"]
    pool_filter(L, neu, "K17")
    k17 = neu["trassen"][-1]; f = [tuple(p) for p in k17["pfad"]]; g0, g1 = f[2], f[3]; zu = g0[2]
    gh = unit((g1[0] - g0[0], g1[1] - g0[1], 0.0))
    t13 = add(g0, gh, s_alt(neu, "K17", g0, gh, P["lt_k57_s"])); t12 = add(g0, gh, s_alt(neu, "K17", g0, gh, P["lt_k21_s"]))
    # ---------------- Heber teilen wie Runde 70: K17 (Pool -> T13), K17-m (T13 -> T12), K17-b (T12 -> Filter); Pfad und Formstuecke unveraendert (Ausnahme 1)
    neu["trassen"].remove(k17)
    for nid, pf, st, en, bd in (("K17", f[:3] + [t13], k17["start"], "t:T13", ["W", "W", "U"]), ("K17-m", [t13, t12], "t:T13", "t:T12", ["U"]), ("K17-b", [t12] + f[3:], "t:T12", k17["ende"], ["U", "W", "W"])):
        e = dict(k17); e.update(id=nid, pfad=[rd(p) for p in pf], start=st, ende=en, baender=bd, korridor=kor_auto(pf))
        neu["trassen"].append(e)
    # ---------------- Stamm K22-T: Filterauslauf -> Bogen lotrecht -> Z z0 -> -Y (Suedspur) -> +X (T14) -> +X -> +Y (T11)
    aus, ao, _ = port(L["filter"], "feinfilter", "aus")
    p1 = add(aus, ao, r90(63)); p2 = (p1[0], p1[1], z0)
    s3, o3, _ = port(L["pumpe_gross"][0], "pumpe_gross", "saug"); s4, o4, _ = port(L["pumpe_gross"][1], "pumpe_gross", "saug")
    f3 = add(s3, o3, U2["a_saug"]); f4 = add(s4, o4, U2["a_saug"])        # Steiger-Fusspunkte (Saughoehe) vor den Stutzen
    ys, xc = U2["y_s"], f3[0]
    t14 = (U2["x_t14"], ys, z0); t11 = (xc, U2["y_t11"], z0)
    if not (f4[1] - ys >= 150 and p2[1] - ys >= 189): raise SystemExit("Linie 2: Suedspur zu nah (Pumpe-4-Steiger %.0f, Filter %.0f)" % (f4[1] - ys, p2[1] - ys))
    neu["trassen"] += [
        {"id": "K22-T", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T14", "anschluss": [L["filter"]], "pfad": [rd(p) for p in (aus, p1, p2, (p2[0], ys, z0), t14)],
         "notiz": "Filterauslauf (Az %.0f) -> Bogen d63 auf dem Stutzen lotrecht -> Etage auf Z %g -> -Y auf die Suedspur y %g -> +X zum T14 (Bypass)" % (ang(ao), z0, ys)},
        {"id": "K22-T-b", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "t:T14", "ende": "t:T11", "anschluss": [], "pfad": [rd(p) for p in (t14, (xc, ys, z0), t11)],
         "notiz": "T14 -> +X bis x %.0f (Spur der Pumpe-3-Steiger) -> +Y zum T11 (K22 geradeaus, K18 nach Westen)" % xc}]
    neu["trassen"] += [
        {"id": "K22", "kante": "K22", "dn": 50, "farbe": "dunkelblau", "start": "t:T11", "ende": "stutzen", "anschluss": [L["pumpe_gross"][0], L["tank_gross"]],
         "pfad": [rd(p) for p in (t11, (xc, f3[1], z0), (f3[0], f3[1], s3[2]), s3)],
         "notiz": "T11 -> +Y zum Steiger %g mm vor dem Saugstutzen -> lotrecht auf Z %.0f -> in Port-Richtung (161,9 Grad, Ausnahme 2) in den Stutzen %s" % (U2["a_saug"], s3[2], L["pumpe_gross"][0])},
        {"id": "K18", "kante": "K18", "dn": 50, "farbe": "dunkelblau", "start": "t:T11", "ende": "stutzen", "anschluss": [L["pumpe_gross"][1], L["tank_gross"]],
         "pfad": [rd(p) for p in (t11, (f4[0], t11[1], z0), (f4[0], f4[1], z0), (f4[0], f4[1], s4[2]), s4)],
         "notiz": "T11 -> -X %.0f mm -> -Y zum Steiger %g mm vor dem Saugstutzen -> lotrecht -> in Port-Richtung in den Stutzen %s; Achsabstand zur Stamm-Nordspur %.0f mm" % (t11[0] - f4[0], U2["a_saug"], L["pumpe_gross"][1], xc - f4[0])}]
    neu["t_stuecke"].append({"id": "T11", "pos": rd(t11), "d": 63, "ports": [{"trasse": "K22-T-b", "ende": "ende", "d": 63}, {"trasse": "K22", "ende": "start", "d": 50}, {"trasse": "K18", "ende": "start", "d": 50}],
                             "notiz": "T d63, K22 geradeaus (+Y), K18 nach Westen; je Abgang Rohrstueck d63 + Reduziermuffe d63/d50"})
    # ---------------- Bypass K57: T13 (Heber) -> Kugelhahn KH2 lotrecht -> Tiefleitung +X, -Y (unter der Filtergrube im Erdreich) -> lotrecht hoch -> -Y in T14
    lkh = LT.ports("lt_kugelhahn_d63")[1][1][2]; abz = ta(HD) + lred(HD, 63)
    pa = (t13[0], t13[1], zu - abz); pb = add(pa, (0.0, 0.0, -1.0), lkh); zc = pb[2] - P["lt_k56_tief"]
    neu["r_stuecke"].append({"id": "KH2", "art": "kugelhahn", "pos_a": rd(pa), "dir": [0.0, 0.0, -1.0], "d_gross": 63, "d_klein": 63,
                             "notiz": "Kugelhahn d63 K57 (Normalbetrieb zu, Stoerfall auf); Schacht in S2N/S6"})
    if abs(t14[0] - t13[0]) > 1: raise SystemExit("K57: T14 muss ueber der Bypass-Spur liegen")
    k57 = [pb, (t13[0], t13[1], zc), (t13[0], ys, zc), t14]   # -Y unter der Filtergrube (Erdreich), lotrecht von unten in T14 (Graben quer zum Stamm)
    neu["trassen"] += [
        {"id": "K57-a", "kante": "K57", "dn": 63, "farbe": "dunkelblau", "start": "t:T13", "ende": "r:KH2", "anschluss": [], "pfad": [rd(t13), rd(pa)], "notiz": "Abzweig vom T d75 auf K17 lotrecht nach unten bis zum Kugelhahn"},
        {"id": "K57-b", "kante": "K57", "dn": 63, "farbe": "dunkelblau", "start": "r:KH2", "ende": "t:T14", "anschluss": [], "pfad": [rd(p) for p in k57],
         "notiz": "Kugelhahn -> Tiefleitung Z %.0f -Y unter der Filtergrube bis y %g -> lotrecht von unten in T14 (Z %g)" % (zc, ys, z0)}]
    neu["t_stuecke"] += [
        {"id": "T13", "pos": rd(t13), "d": HD, "ports": [{"trasse": "K17", "ende": "ende", "d": HD}, {"trasse": "K17-m", "ende": "start", "d": HD}, {"trasse": "K57-a", "ende": "start", "d": 63}],
         "notiz": "T d75 auf K17, Zweig d63 lotrecht nach unten (Notbypass K57): Rohrstueck d75 + Reduziermuffe d75/d63"},
        {"id": "T14", "pos": rd(t14), "d": 63, "ports": [{"trasse": "K22-T", "ende": "ende", "d": 63}, {"trasse": "K22-T-b", "ende": "start", "d": 63}, {"trasse": "K57-b", "ende": "ende", "d": 63}],
         "notiz": "T d63 im Filter-Stamm, Zweig lotrecht nach unten (Notbypass K57)"}]
    # ---------------- Biofilter: K24/K25 Druckstutzen -> Z z_druck -> T15; Stamm lotrecht auf Zulaufhoehe -> l_zul gegen die Port-Richtung zur Reduziermuffe
    tg = L["tank_gross"]; zh = U1["z_druck"]
    p3, _, _ = port(L["pumpe_gross"][0], "pumpe_gross", "druck"); p4, _, _ = port(L["pumpe_gross"][1], "pumpe_gross", "druck")
    zt, zo, _ = port(tg, "tank_gross", "zulauf"); rz, pbz = stutzen_red(zt, zo, 63, 50); neu["r_stuecke"].append(dict(id="R_ZUL2", **rz))
    c1 = add(pbz, zo, U2["l_zul"]); cn = (c1[0], c1[1] + U2["dy_t15"], U2["z_t15n"]); t15 = (cn[0], cn[1], zh); xw = t15[0] - U2["x_k24"]
    k25 = [p4, (p4[0], p4[1], zh), (p4[0], t15[1], zh), t15]
    k24 = [p3, (p3[0], p3[1], zh), (xw, p3[1], zh), (xw, t15[1], zh), t15]   # -X unter dem Plattformrand, dann -Y neben dem Filter (R9: Spur y_k24 lag im Gang)
    if abs(p4[1] - t15[1]) < 150 or p4[0] - t15[0] < 150: raise SystemExit("K25: Laeufe zu kurz (%.0f / %.0f)" % (p4[1] - t15[1], p4[0] - t15[0]))
    neu["trassen"] += [
        {"id": "K24", "kante": "K24", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T15", "anschluss": [L["pumpe_gross"][0], tg], "pfad": [rd(p) for p in k24],
         "notiz": "Druckstutzen -> Z %g -> -X bis x %.0f -> -Y -> +X ins T15" % (zh, xw)},
        {"id": "K25", "kante": "K25", "dn": 40, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T15", "anschluss": [L["pumpe_gross"][1], tg], "pfad": [rd(p) for p in k25],
         "notiz": "Druckstutzen (unter dem Zulauf-Stutzen) -> Z %g -> +Y %.0f mm -> -X %.0f mm ins T15" % (zh, t15[1] - p4[1], p4[0] - t15[0])},
        {"id": "K24-K25-Stamm", "kante": None, "dn": 50, "farbe": "dunkelblau", "start": "t:T15", "ende": "r:R_ZUL2", "anschluss": [tg], "pfad": [rd(p) for p in (t15, cn, (c1[0], c1[1], U2["z_t15n"]), c1, pbz)],
         "notiz": "T15 -> lotrecht auf Z %g -> %g mm -Y -> lotrecht auf Zulaufhoehe Z %.0f -> %g mm gegen die Port-Richtung (-161,8 Grad, Ausnahme 2) zur Reduziermuffe d63/d50" % (U2["z_t15n"], U2["dy_t15"], zt[2], U2["l_zul"])}]
    neu["t_stuecke"].append({"id": "T15", "pos": rd(t15), "d": 50, "ports": [{"trasse": "K24", "ende": "ende", "d": 40}, {"trasse": "K25", "ende": "ende", "d": 40}, {"trasse": "K24-K25-Stamm", "ende": "start", "d": 50}],
                             "notiz": "T d50: K24 (von Westen) und K25 (von Osten) gegenueber (X), Stamm lotrecht nach oben"})
    ut, uo, _ = port(tg, "tank_gross", "ueberlauf"); ru, pbu = stutzen_red(ut, uo, 63, 50); neu["r_stuecke"].append(dict(id="R_UEB2", **ru))
    neu["trassen"].append({"id": "K26", "kante": "K26", "dn": 50, "farbe": "dunkelblau", "start": "r:R_UEB2", "ende": "offen", "anschluss": [tg], "pfad": [rd(pbu), rd(add(pbu, uo, U1["l_ueb"]))],
        "notiz": "Ueberlauf d63 -> Reduziermuffe d63/d50 -> %g mm in Port-Richtung; Verteiler d50 folgt (M10-UMBAU Schritt 6)" % U1["l_ueb"]})
    # ---------------- Absetzerkreis Linie 2: K19 ab dem Stumpf, K20, K21
    ab = L["absetzer"]; pk = L["pumpe_klein"][0]
    st = [t for t in alt.get("trassen", []) if t["id"] == "K03-K19-Stumpf"]
    if not st: raise SystemExit("Linie 1 fehlt: erst trassen_linie.py 1 laufen lassen (Stumpf K03-K19-Stumpf)")
    stumpf = tuple(st[0]["pfad"][-1]); zt3 = stumpf[2]
    saug, so, _ = port(pk, "pumpe_klein", "saug"); druck, _, _ = port(pk, "pumpe_klein", "druck")
    pos_b = add(saug, so, -LT.DEPTH[40]); pos_a = add(pos_b, so, lred(50, 40)); fk = add(saug, so, U2["a_k19"])   # Reduziermuffe d50/d40 direkt auf dem Saugstutzen (Ausnahme 2 gilt bis zum Steiger)
    neu["r_stuecke"].append({"id": "R_K19", "pos_a": rd(pos_a), "dir": [round(-v, 6) for v in so], "d_gross": 50, "d_klein": 40, "auf_stutzen": True})
    neu["trassen"] += [
        {"id": "K19", "kante": "K19", "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "r:R_K19", "anschluss": [pk, ab],
         "dn_abweichung": "M10-UMBAU: Zulauf d50 wie K03-Steig (Linie 1), Reduziermuffe d50/d40 direkt auf dem Saugstutzen; Netz-Kante K19 fuehrt d40",
         "pfad": [rd(p) for p in (stumpf, (stumpf[0], fk[1], zt3), (fk[0], fk[1], zt3), fk, pos_a)],
         "notiz": "ab dem Linie-2-Stumpf (Kupplung, Z %.0f): -Y unter dem Pool hinaus -> +X zum Steiger %g mm vor dem Saugstutzen -> lotrecht auf Z %.0f -> in Port-Richtung (Ausnahme 2) zur Reduziermuffe d50/d40 auf dem Saugstutzen %s" % (zt3, U2["a_k19"], saug[2], pk)}]
    zul, zo4, _ = port(ab, "tank_klein", "zulauf"); rk, pb4 = stutzen_red(zul, zo4, 50, 32); neu["r_stuecke"].append(dict(id="R_K20", **rk))
    c4b = add(pb4, zo4, U1["l_k04"]); z4 = U1["z_k04"]
    k20 = [druck, (druck[0], druck[1], z4), (c4b[0], druck[1], z4), (c4b[0], c4b[1], z4), c4b, pb4]
    neu["trassen"].append({"id": "K20", "kante": "K20", "dn": 32, "farbe": "dunkelblau", "start": "stutzen", "ende": "r:R_K20", "anschluss": [pk, ab], "pfad": [rd(p) for p in k20],
        "notiz": "Druckstutzen -> Z %g -> -X -> +Y -> lotrecht auf Zulaufhoehe Z %.0f -> %g mm in Port-Richtung zur Reduziermuffe d50/d32" % (z4, zul[2], U1["l_k04"])})
    aus5, ao5, _ = port(ab, "tank_klein", "auslauf"); pct = P["lt_k05_pct"] / 100.0; R50 = r90(50); l1 = R50 + P["lt_k05_vor"]
    a1 = add(aus5, ao5, l1); a1 = (a1[0], a1[1], aus5[2] - pct * l1)
    z2 = U2["z_k05"]; ly = t12[1] - a1[1]; lx = a1[0] - t12[0]
    if min(ly, lx) < 300: raise SystemExit("K21: Laeufe zu kurz (ly %.0f, lx %.0f)" % (ly, lx))
    k21 = [aus5, a1, (a1[0], a1[1], z2), (a1[0], t12[1], z2 - pct * ly), (t12[0], t12[1], z2 - pct * (ly + lx)), t12]
    neu["trassen"].append({"id": "K21", "kante": "K21", "dn": 50, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T12", "gefaelle_pct": P["lt_k05_pct"], "anschluss": [ab], "pfad": [rd(p) for p in k21],
        "notiz": "Auslauf -> Bogen -> Fallrohr auf Z %g -> +Y %.0f, -X %.0f mm mit %.1f %% Gefaelle -> lotrecht hoch in T12 auf dem Heber" % (z2, ly, lx, P["lt_k05_pct"])})
    neu["t_stuecke"].append({"id": "T12", "pos": rd(t12), "d": HD, "ports": [{"trasse": "K17-m", "ende": "ende", "d": HD}, {"trasse": "K17-b", "ende": "start", "d": HD}, {"trasse": "K21", "ende": "ende", "d": 50}],
                             "notiz": "T d75 im Heber, Zweig d50 (K21) lotrecht von unten: Rohrstueck d75 + Reduziermuffe d75/d50"})
    for t in neu["trassen"]:
        if not t.get("korridor"): t["korridor"] = kor_auto(t["pfad"])
        if not t.get("baender") and not t.get("band"): t["baender"] = baender_auto(t["pfad"])


# ======================================================================================================================
# M10-UMBAU Schritte 5 und 6 (05.11.2026): Schlammablass (M03) und Verteiler am Ueberlauf (M08) je Linie.
# Absetzer: Ablaufstutzen d40 an der Kegelspitze (tank.md: Zapfen, Ende lokal z 80) -> Federrueckzug-Kugelhahn lt_kugelhahn_feder_d40 -> Rohr d40 lotrecht in den Graben ->
# waagerecht in X/Y mit >= 1 % Gefaelle -> lotrecht in die Muffe d40 des Schlammfasses (T93) in einer Grube neben dem Absetzer.
# Weil der Hahnauslauf nur 4 mm ueber dem Flur liegt, sitzt das Fass tiefer als im Bauteilblatt (Oberkante unter Flur, Grube mit Abdeckung): Befund an Werkstatt/Ben.
# Biofilter-Tanks: Ablaufstutzen d50 -> Kugelhahn d50 -> Rohrstueck -> Kappe d50 (Wartungsablass, kein Netz-Knoten).
# Ueberlauf K10/K26: Verteiler d50 (W36) mit Muffe A auf dem Rohrende, Achse in Port-Richtung, Abgaenge nach oben; Abgang 3 (d20) und 4 (d50) mit Kappe,
# Abgang 1 (d40) und 2 (d32) offen: Kappe d40/d32 fehlt in der Bibliothek (OFFEN Werkstatt).
SCHLAMM = {1: {"tank": "Tank_klein:2", "fass": (3925.0, -1461.0), "kid": "K07", "folge": "XY"},     # Fass-Lage [A]: Abstandssuche 05.11. (Grube Oe 800 >= 30 mm frei von Graeben,
           2: {"tank": "Tank_klein:1", "fass": (1307.5, -3083.0), "kid": "K23", "folge": "YX"}}     # >= 30 mm von Bauteil-Kaesten, >= 100 mm vom Pool); naeher als 0,95 m ist belegt
BIO = {1: ("Tank_gross:1", "KB1"), 2: ("Tank_gross_t3:1", "KB2")}
S_PCT = 1.5          # Gefaelle K07/K23 [A] (Blatt: >= 1 %; 1,5 % = 0,86 Grad, Bogen-Toleranz 1 Grad wie K05)
S_H1 = 100.0         # sichtbares Rohr unter dem Federhahn bis zum Bogen
S_H2 = 50.0          # sichtbares Rohr vom letzten Bogen bis in die Fassmuffe
S_SAND = 70.0        # Sandbett unter dem Fass (schlammfass.md)
F_INNEN = 920.0      # Muffe d40 des Fasses, Lage lokal z (schlammfass.md Ports)
K_GAP = 10.0         # sichtbares Rohrstueck zwischen Kugelhahn und Kappe

def lt_ports(name):
    import leitung_w71 as W71
    return W71.ports(name)

def schlamm_verteiler(L, neu, linie):
    neu.setdefault("teile", []); neu.setdefault("gruben", [])
    dn = (0.0, 0.0, -1.0); up = (0.0, 0.0, 1.0)
    # ---------------- Absetzer -> Schlammfass
    cfg = SCHLAMM[linie]; m = MV[cfg["tank"]]
    tip = world(m, (0.0, 0.0, 80.0)); t40 = LT.DEPTH[40]
    lf = lt_ports("lt_kugelhahn_feder_d40")[1][1][2]
    pa = add(tip, up, t40); pb = add(pa, dn, lf)                     # Muffe A (Stutzen steckt t), Muffe B unten
    neu["teile"].append({"id": "FH%d" % linie, "datei": "lt_kugelhahn_feder_d40", "pos": rd(pa), "z": [0.0, 0.0, -1.0], "x": [1.0, 0.0, 0.0], "farbe": "dunkelblau",
                         "notiz": "Federrueckzug-Kugelhahn d40 auf dem Ablaufstutzen des Absetzers %s (Hebel quer = zu)" % cfg["tank"]})
    k40 = k90(40); fx, fy = cfg["fass"]
    h1 = pb[2] - S_H1 - k40
    ecke = (fx, pb[1]) if cfg["folge"] == "XY" else (pb[0], fy)
    l1 = math.hypot(ecke[0] - pb[0], ecke[1] - pb[1]); l2 = math.hypot(fx - ecke[0], fy - ecke[1]); g = S_PCT / 100.0
    if min(l1, l2) < 120: raise SystemExit("%s: Strecken zu kurz (%.0f / %.0f)" % (cfg["kid"], l1, l2))
    p1 = (pb[0], pb[1], h1); p2 = (ecke[0], ecke[1], h1 - g * l1); p3 = (fx, fy, h1 - g * (l1 + l2))
    zin = p3[2] - k40 - S_H2; p4 = (fx, fy, zin)
    neu["trassen"].append({"id": cfg["kid"], "kante": cfg["kid"], "dn": 40, "farbe": "grau", "start": "muffe", "ende": "muffe", "gefaelle_pct": S_PCT, "korridor": ["KS", "KG", "KG", "KS"],
                           "anschluss": [cfg["tank"], "schlammfass_%d" % linie], "pfad": [rd(p) for p in (pb, p1, p2, p3, p4)],
                           "notiz": "Schlammablass: Federhahn -> lotrecht in den Graben (Z %.0f) -> %.0f + %.0f mm mit %.1f %% Gefaelle -> lotrecht in die Muffe d40 des Schlammfasses" % (h1, l1, l2, S_PCT)})
    z0 = zin - F_INNEN
    neu["teile"].append({"id": "schlammfass_%d" % linie, "datei": "schlammfass", "pos": rd((fx, fy, z0)), "z": [0.0, 0.0, 1.0], "x": [1.0, 0.0, 0.0],
                         "notiz": "T93 Schlammfass Linie %d: Fassboden Z %.0f (flur-relativ %.0f), Oberkante flur-relativ %.0f; Grube Oe 800 mit Abdeckung [A]" % (linie, z0, z0 - 400, z0 + 880 - 400)})
    neu["gruben"].append({"id": "schlammfass_%d" % linie, "x": fx, "y": fy, "d": 800.0, "sohle": round(z0 - S_SAND, 1)})
    # ---------------- Biofilter-Tank: Wartungsablass mit Kugelhahn d50 und Kappe
    tg, kid = BIO[linie]; mg = MV[tg]; t50 = LT.DEPTH[50]
    tipg = world(mg, (0.0, 0.0, 134.0)); pga = add(tipg, up, t50); lh = LT.ports("lt_kugelhahn_d50")[1][1][2]; pgb = add(pga, dn, lh)
    neu["r_stuecke"].append({"id": kid, "art": "kugelhahn", "pos_a": rd(pga), "dir": [0.0, 0.0, -1.0], "d_gross": 50, "d_klein": 50,
                             "notiz": "Kugelhahn d50 am Schlammablass des Biofilter-Tanks %s (Wartungsablass, kein Netz-Knoten: Befund an den Orchestrator)" % tg})
    pk = add(pgb, dn, K_GAP)
    neu["trassen"].append({"id": kid + "-Kappe", "kante": None, "dn": 50, "farbe": "grau", "start": "r:" + kid, "ende": "muffe", "korridor": ["KS"], "anschluss": [tg],
                           "pfad": [rd(pgb), rd(pk)], "notiz": "Rohrstueck d50 zwischen Kugelhahn und Kappe (Wartungsablass)"})
    neu["teile"].append({"id": kid + "-Kappe", "datei": "lt_kappe_d50", "pos": rd(pk), "z": [0.0, 0.0, -1.0], "x": [1.0, 0.0, 0.0], "farbe": "grau", "notiz": "Kappe d50 unter dem Kugelhahn"})
    # ---------------- Verteiler d50 am Ende von K10/K26
    kid_u = "K10" if linie == 1 else "K26"
    tr = [t for t in neu["trassen"] if t["id"] == kid_u][0]; e = tuple(tr["pfad"][-1]); a0 = tuple(tr["pfad"][-2])
    xd = unit(sub(e, a0)); tr["ende"] = "muffe"
    tr["notiz"] = tr["notiz"].replace("; Verteiler d50 folgt (M10-UMBAU Schritt 6)", "; Rohr steckt in Muffe A des Verteilers d50 (M10-UMBAU Schritt 6)")
    neu["teile"].append({"id": "VT%d" % linie, "datei": "lt_verteiler_d50", "pos": rd(e), "z": [0.0, 0.0, 1.0], "x": [round(v, 6) for v in xd], "farbe": "dunkelblau",
                         "notiz": "Verteiler d50 (W36) auf dem Ende von %s: Abgaenge 1 Beete d40, 2 NFT d32, 3 Messkreis d20, 4 Bypass d50 nach oben" % kid_u})
    for nr, dk in ((3, 20), (4, 50)):
        lage = lt_ports("lt_verteiler_d50")[nr][1]
        top = add(add(e, xd, lage[0]), up, lage[2]); pos = add(top, up, -LT.DEPTH[dk])
        neu["teile"].append({"id": "VT%d-Kappe%d" % (linie, nr), "datei": "lt_kappe_d%d" % dk, "pos": rd(pos), "z": [0.0, 0.0, 1.0], "x": [round(v, 6) for v in xd], "farbe": "grau",
                             "notiz": "Kappe d%d auf Abgang %d des Verteilers (vorerst verschlossen bis S3)" % (dk, nr)})
    hp = add(e, xd, -50.0); hk = 4.0 + (50 + 6) / 2.0                 # Halter je Verteiler (R6: <= 300 mm daneben): Klemme d50 unter dem Rohr vor Muffe A
    neu["teile"].append({"id": "VT%d-Halter" % linie, "datei": "lt_klemme_d50", "pos": rd(add(hp, up, -hk)), "z": [0.0, 0.0, 1.0], "x": [round(v, 6) for v in xd], "farbe": "grau",
                         "notiz": "Rohrklemme d50 50 mm vor dem Verteiler (Konsole an der Tank-Plattform: OFFEN Werkstatt Halter)"})
    for t in neu["trassen"]:
        if not t.get("baender") and not t.get("band"): t["baender"] = baender_auto(t["pfad"])

def main(linie):
    if linie not in LINIEN: raise SystemExit("Linie 1 oder 2")
    import gen_dome as G
    L = dict(LINIEN[linie]); L["G"] = G
    neu = {"trassen": [], "t_stuecke": [], "r_stuecke": []}
    if linie == 1:
        linie1_ordnung(L, neu)   # M10-UMBAU: ersetzt linie1_s2a/_biofilter/_absetzer/_bypass (bleiben als Vorlage fuer Linie 2 stehen)
        schlamm_verteiler(L, neu, 1)
    else:
        alt = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {}
        linie2_ordnung(L, neu, alt)   # M10-UMBAU Schritt 4: ersetzt linie2_s2a/_biofilter/_absetzer/_bypass (bleiben als Vorlage stehen)
        schlamm_verteiler(L, neu, 2)
    doc = {"z_bezug": "absolut", "regeln": {}, "quelle": "scripts/trassen_linie.py (Ableitung); M10-S2: Linie 1 Ost, Linie 2 West (je Linie ein Lauf)"}
    doc = schreiben(doc, linie, neu)
    json.dump(doc, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(OUT, "a").write("\n")
    for t in neu["trassen"]:
        print(t["id"], "d%d" % t["dn"], [tuple(p) for p in t["pfad"]])
    print("R63 %.1f  R50 %.1f  T1 %s" % (r90(63), r90(50), neu["t_stuecke"][0]["pos"]))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
