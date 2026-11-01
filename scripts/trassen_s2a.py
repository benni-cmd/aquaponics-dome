"""M10-S2a: Trassenliste data/leitungstrassen.json fuer K01, K02 und K06 (Linie 1 Ost, Pool -> Feinfilter Ost A -> Pumpe_gross:1 und :2).
Aufruf: python -X utf8 scripts/trassen_s2a.py            (schreibt data/leitungstrassen.json und druckt die Koordinaten)
Die Koordinaten kommen NICHT von Hand, sondern aus den Instanzmatrizen (scripts/dome-script.json) mal den Port-Tabellen der Bauteilblaetter:
  Feinfilter Einlauf  x -375 / y 0 / z 816, Oeffnung -X;  Auslauf x 385 / y 0 / z 310, Oeffnung +X   (docs/parts/feinfilter.md Zeilen 104/105)
  Pumpe_gross Saugstutzen x 196 / y 76 / z 120, Oeffnung +X                                             (docs/parts/pumpe.md Zeile 51)
  Pool-Seitenablauf SA_Ost_A: offenes Ende und Achse aus gen_dome.pool_ports()                          (docs/parts/leitungsteile.md, M10-S1b)
Bogenmasse (Schenkel k = Abstand Kreuzungspunkt - Muffenebene, Radius R = k - t) aus scripts/workshop/leitung.ports().
Absolut-Z; Flur 400. Das Skript ist die Ableitung, die Liste ist ihr Ergebnis: Aenderungen an Lage oder Hoehe gehen hier hinein."""
import json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import leitung as LT

P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
MV = {c["params"]["occurrence"]: c["params"]["matrix"] for c in json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"] if c["command"] == "occurrence.move"}
OUT = os.path.join(ROOT, "data", "leitungstrassen.json")

def world(m, p): return tuple(m[4 * r] * p[0] + m[4 * r + 1] * p[1] + m[4 * r + 2] * p[2] + m[4 * r + 3] for r in range(3))
def wdir(m, d): return tuple(m[4 * r] * d[0] + m[4 * r + 1] * d[1] + m[4 * r + 2] * d[2] for r in range(3))
def h(deg): return (math.cos(math.radians(deg)), math.sin(math.radians(deg)), 0.0)
def add(a, b, s=1.0): return tuple(a[i] + s * b[i] for i in range(3))
def rd(p): return [round(v, 1) for v in p]

def k90(d): return LT.ports("lt_bogen90_d%d" % d)[1][1][0]          # Schenkel Bogen 90
def r90(d): return k90(d) - LT.DEPTH[d]                              # Abstand Stutzenspitze -> Kreuzungspunkt bei direkt aufgestecktem Bogen

def main():
    import gen_dome as G
    f = MV["Feinfilter:1"]
    ein = world(f, (-375, 0, 816)); ein_o = wdir(f, (-1, 0, 0))          # Einlauf-Stutzenspitze, Richtung nach aussen
    aus = world(f, (385, 0, 310)); aus_o = wdir(f, (1, 0, 0))
    pump = {}
    for i in (1, 2):
        m = MV["Pumpe_gross:%d" % i]; pump[i] = (world(m, (196, 76, 120)), wdir(m, (1, 0, 0)))
    sa = [p for p in G.pool_ports(P["sock_h"]) if p["name"] == "SA_Ost_A"][0]
    tip_pool, u = sa["ende"], sa["axis"]
    R63, R50 = r90(63), r90(50)
    ang = lambda v: math.degrees(math.atan2(v[1], v[0]))
    doc = {"z_bezug": "absolut", "regeln": {}, "quelle": "scripts/trassen_s2a.py (Ableitung); M10-S2a, Linie 1 Ost: K01, K02, K06", "trassen": []}
    # ---------------- K01: Pool-Seitenablauf Ost A (d63) -> Feinfilter-Einlauf, unterflur im Heber
    zu = P["lt_k01_z_u"]
    v1 = add(tip_pool, u, R63)                                              # Bogen 1 direkt auf den Stutzen gesteckt
    c_in = add(ein, ein_o, R63)                                             # Bogen 4 direkt auf den Einlaufstutzen gesteckt
    pf = [tip_pool, v1, (v1[0], v1[1], zu), (c_in[0], c_in[1], zu), c_in, ein]
    doc["trassen"].append({"id": "K01", "kante": "K01", "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "stutzen", "heber": True,
        "baender": ["W", "W", "U", "W", "W"], "anschluss": ["Zentralpool", "Feinfilter:1"], "pfad": [rd(p) for p in pf],
        "notiz": "Seitenablauf Z 740 (Pool-Stutzen Ost A, Az %.1f) -> Bogen runter -> Graben Z %g (Heber, Rohr oben %.1f unter Spiegel 915) -> Bogen hoch -> Bogen in den Einlauf Z %.0f (Stutzenspitze x %.1f y %.1f)" % (ang(u), zu, 915 - (zu + 31.5), ein[2], ein[0], ein[1])})
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
    doc["trassen"].append({"id": "K06-T", "kante": None, "dn": 63, "farbe": "dunkelblau", "start": "stutzen", "ende": "t:T1", "band": "U", "anschluss": ["Feinfilter:1"],
        "pfad": [rd(p) for p in pf], "notiz": "Stamm d63 zwischen Filterauslauf und T (gehoert zu K02 und K06: Netz fuehrt dort d50, T-Stueck d63/d50/d50 laut Netz-Bemerkung K06); Winkel %.0f/%.0f/%.0f/%.0f Grad im 15-Grad-Gitter des Filters; Laengen v2-v3 %.0f, v3-v4 %.0f, v4-T %.0f" % (h2, h3, h4, h5, l3, l4, s5)})
    # ---------------- Abgaenge d50 vom T zu den Pumpen: je Riser (unterflur -> Saugstutzenhoehe) und Zulauf in den Stutzen
    # Pumpe_gross:1 (Sued) geradeaus (h5), Pumpe_gross:2 (Nord) links 90 Grad (h5 + 90, Richtung Ost)
    for kid, pi, dirdeg in (("K06", 1, h5), ("K02", 2, h5 + 90)):
        tip, o = pump[pi]; dv = h(dirdeg)
        s = (tip[1] - t0[1]) / dv[1]; r = add(t0, dv, s)                      # Fusspunkt des Risers: Strahl vom T bei y der Saugstutzenachse
        r = (r[0], tip[1], z); up = (r[0], tip[1], tip[2])
        doc["trassen"].append({"id": kid, "kante": kid, "dn": 50, "farbe": "dunkelblau", "start": "t:T1", "ende": "stutzen", "baender": ["U", "W", "W"],
            "anschluss": ["Pumpe_gross:%d" % pi] + (["Tank_gross:1"] if kid == "K02" else []), "pfad": [rd(t0), rd(r), rd(up), rd(tip)],
            "notiz": "T -> Fuss des Risers (Z %.0f) -> Riser auf Saugstutzenhoehe Z %.0f -> Zulauf in den Saugstutzen Pumpe_gross:%d (Stutzenspitze x %.1f y %.1f, Oeffnung -X)" % (z, tip[2], pi, tip[0], tip[1])})
    doc["t_stuecke"] = [{"id": "T1", "pos": rd(t0), "ein": "K06-T", "aus": ["K06", "K02"], "d_ein": 63, "d_aus": 50,
                         "notiz": "T d63 aus lt_t_d63 + je Ausgang Rohrstueck d63 (2 t) + Reduziermuffe d63/d50 (die Muffen eines T und einer Reduziermuffe passen nicht Muffe auf Muffe)"}]
    json.dump(doc, open(OUT, "w", encoding="utf-8"), indent=1, ensure_ascii=False); open(OUT, "a").write("\n")
    for t in doc["trassen"]:
        print(t["id"], "d%d" % t["dn"], [tuple(p) for p in t["pfad"]])
    print("R63 %.1f  R50 %.1f  T1 %s" % (R63, R50, rd(t0)))

if __name__ == "__main__":
    main()
