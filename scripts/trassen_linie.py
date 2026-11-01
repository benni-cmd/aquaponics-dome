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
def lred(dg, dk): return LT.ports("lt_reduzierung_d%d_d%d" % (dg, dk))[1][1][2]

def port(inst, klasse, name):
    """Weltpunkt der Stutzenspitze, Richtung nach aussen, Aussen-d eines Bauteil-Ports."""
    p, o, d = PORTS[klasse][name]; m = MV[inst]
    return world(m, p), unit(wdir(m, o)), d

def stutzen_red(tip, o, d_stutzen, d_rohr):
    """Reduziermuffe auf einem Stutzen d_stutzen fuer ein Rohr d_rohr (d_rohr < d_stutzen): Muffenebene A liegt t hinter der Spitze, B um die Muffenlaenge weiter aussen.
    Gibt (r_stueck ohne id, Trassenpunkt auf Ebene B) zurueck."""
    pa = add(tip, o, -LT.DEPTH[d_stutzen]); pb = add(pa, o, lred(d_stutzen, d_rohr))
    return {"pos_a": rd(pa), "dir": [round(v, 6) for v in o], "d_gross": d_stutzen, "d_klein": d_rohr}, pb

def schreiben(doc, linie, neu):
    """Mischt die Trassen der Linie in die bestehende Liste (Trassen der anderen Linie bleiben); S2a-Eintraege ohne Feld linie gelten als Linie 1."""
    alt = json.load(open(OUT, encoding="utf-8")) if os.path.exists(OUT) else {"z_bezug": "absolut", "regeln": {}, "trassen": []}
    gehoert = lambda e: e.get("linie", 1) == linie
    for key in ("trassen", "t_stuecke", "r_stuecke"):
        doc[key] = [e for e in alt.get(key, []) if not gehoert(e)] + neu.get(key, [])
        for e in neu.get(key, []): e["linie"] = linie
    if not doc["r_stuecke"]: del doc["r_stuecke"]
    return doc

def linie1_s2a(L, neu):
    """K01 Pool -> Feinfilter-Einlauf (unterflur, Heber), Stamm K06-T Filterauslauf -> T, K06/K02 T -> Pumpen-Saugstutzen (M10-S2a, unveraendert)."""
    ein, ein_o, _ = port(L["filter"], "feinfilter", "ein"); aus, aus_o, _ = port(L["filter"], "feinfilter", "aus")
    pump = {i: port(L["pumpe_gross"][i - 1], "pumpe_gross", "saug") for i in (1, 2)}
    sa = [p for p in L["G"].pool_ports(P["sock_h"]) if p["name"] == L["pool_sa"]][0]
    tip_pool, u = sa["ende"], sa["axis"]
    R63 = r90(63)
    # ---------------- K01: Pool-Seitenablauf (d63) -> Feinfilter-Einlauf, unterflur im Heber
    zu = P["lt_k01_z_u"]
    v1 = add(tip_pool, u, R63)                                              # Bogen 1 direkt auf den Stutzen gesteckt
    c_in = add(ein, ein_o, R63)                                             # Bogen 4 direkt auf den Einlaufstutzen gesteckt
    pf = [tip_pool, v1, (v1[0], v1[1], zu), (c_in[0], c_in[1], zu), c_in, ein]
    neu["trassen"].append({"id": "K01", "kante": "K01", "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "stutzen", "heber": True,
        "baender": ["W", "W", "U", "W", "W"], "anschluss": ["Zentralpool", L["filter"]], "pfad": [rd(p) for p in pf],
        "notiz": "Seitenablauf Z 740 (Pool-Stutzen %s, Az %.1f) -> Bogen runter -> Graben Z %g (Heber, Rohr oben %.1f unter Spiegel 915) -> Bogen hoch -> Bogen in den Einlauf Z %.0f (Stutzenspitze x %.1f y %.1f)" % (L["pool_sa"], ang(u), zu, 915 - (zu + 31.5), ein[2], ein[0], ein[1])})
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

def main(linie):
    if linie not in LINIEN: raise SystemExit("Linie 1 oder 2")
    if linie == 2: raise SystemExit("Linie 2: Trassen folgen in M10-S2c")
    import gen_dome as G
    L = dict(LINIEN[linie]); L["G"] = G
    neu = {"trassen": [], "t_stuecke": [], "r_stuecke": []}
    linie1_s2a(L, neu)
    linie1_biofilter(L, neu)
    doc = {"z_bezug": "absolut", "regeln": {}, "quelle": "scripts/trassen_linie.py (Ableitung); M10-S2: Linie 1 Ost"}
    doc = schreiben(doc, linie, neu)
    json.dump(doc, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(OUT, "a").write("\n")
    for t in neu["trassen"]:
        print(t["id"], "d%d" % t["dn"], [tuple(p) for p in t["pfad"]])
    print("R63 %.1f  R50 %.1f  T1 %s" % (r90(63), r90(50), neu["t_stuecke"][0]["pos"]))

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
