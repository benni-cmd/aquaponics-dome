"""Tuer komplett (W20, D36, R13) Schritt 1: Geometrie des Basisfeldes BBB 149,2 und der Tuerlage; schreibt data/components/tuer_komplett.json (Parameter, Geometrie, Pruefwerte).
Feld-KS (Tuer-KS, in der Ebene des Strebendreiecks): Ursprung = Mitte der Basiskante (Knoten 24 -> 22) auf Z 0 = Basisknotenhoehe (base_z), X tangential (Knoten 24 -> 22), Y' in der Feldebene hangaufwaerts zur Spitze (Knoten 6), Z' = Feldnormale nach aussen.
Entscheidung [A]: der rechteckige Rahmen liegt in der Feldebene (um den Winkel der Feldebene zur Senkrechten geneigt, R13 Befund 2: die Tuer steht nicht senkrecht); die Rahmenmasse (Lichte 1016 x 2008) werden in der Feldebene gemessen, der Tuerausschnitt im Paneel BBB liegt damit eben im Paneel.
Aufruf: python scripts/workshop/tuer_geom.py"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

DOOR_NODES = (24, 22, 6)             # Basisknoten links/rechts (Tuer-KS X), Spitzenknoten (D36: Feld BBB 149,2)

def local_nodes(lay):
    """Knoten des Feldes im Feld-KS (mm): ({nr: (x, y', z')}, Azimut der Achse, Neigung der Feldebene zur Senkrechten in Grad)."""
    N = lay["nodes_list"]
    a, b, c = (N[n] for n in DOOR_NODES)
    z0 = lay["base_z"]
    P0 = [(a["x"] + b["x"]) / 2, (a["y"] + b["y"]) / 2, z0]
    ex = [b["x"] - a["x"], b["y"] - a["y"], 0.0]
    L = math.hypot(ex[0], ex[1]); ex = [v / L for v in ex]
    sv = [c["x"] - P0[0], c["y"] - P0[1], c["z"] - z0]              # Basismitte -> Spitze
    S = math.sqrt(sum(v * v for v in sv)); ey = [v / S for v in sv]  # hangaufwaerts (Spitze liegt auf der Achse: ey senkrecht zu ex)
    ez = [ex[1] * ey[2] - ex[2] * ey[1], ex[2] * ey[0] - ex[0] * ey[2], ex[0] * ey[1] - ex[1] * ey[0]]
    if ez[0] * P0[0] + ez[1] * P0[1] < 0:                             # Feldnormale nach aussen
        ez = [-v for v in ez]
    out = {}
    for n in DOOR_NODES:
        q = N[n]
        d_ = [q["x"] - P0[0], q["y"] - P0[1], q["z"] - z0]
        out[n] = tuple(sum(d_[k] * e[k] for k in range(3)) for e in (ex, ey, ez))
    tilt = math.degrees(math.acos(max(-1, min(1, ey[2]))))             # Neigung der Hangrichtung zur Senkrechten (0 = senkrecht)
    return out, math.degrees(math.atan2(P0[1], P0[0])) % 360, tilt

def main():
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    P, _ = {}, None
    pth = os.path.join(sc.ROOT, "data", "components", "tuer_komplett.json")
    d = json.load(open(pth, encoding="utf-8")) if os.path.exists(pth) else {}
    P = {k: v["wert"] for k, v in d.get("parameter", {}).items()} or None
    return lay, d, pth

PARAM = {
    "blatt_w": ("mm", 1000, "[A] Normtuer 1000 x 2000 (docs/components.md, Auftrag W20)"),
    "blatt_h": ("mm", 2000, "[A] Normtuer 1000 x 2000"),
    "blatt_t": ("mm", 40, "[A] Tuerblatt 40 mm (Auftrag W20)"),
    "spiel": ("mm", 8, "[A] Spiel Blatt zu Zarge je Seite und oben (Normtuer-Praxis 5-10 mm)"),
    "rohr": ("mm", 30, "[A] Zarge aus Rechteckrohr 30 x 30 x 2 wie die Streben (Auftrag W20 Schritt 2)"),
    "rohr_wand": ("mm", 2, "[A] Wandstaerke Zargenrohr 2 mm"),
    "schwelle_h": ("mm", 30, "[A] Schwelle = Rohr 30 x 30 (ebenerdig, Blatt liegt auf der Schwelle auf, R13 Befund 8: kein Mass belegt)"),
}

def compute(lay, P):
    nl, az, tilt = local_nodes(lay)
    xa = nl[24][0]; xb = nl[22][0]; S = nl[6][1]
    base_w = xb - xa
    lichte_w = P["blatt_w"] + 2 * P["spiel"]
    lichte_h = P["blatt_h"] + P["spiel"]
    frame_w = lichte_w + 2 * P["rohr"]                              # Aussenbreite der Zarge
    s_sturz_o = P["schwelle_h"] + lichte_h + P["rohr"]               # Oberkante Sturz, in der Feldebene gemessen
    w = lambda s: base_w * (1 - s / S)                               # Feldbreite in Hangabstand s von der Basiskante
    return dict(az_achse=round(az, 1), neigung_feldebene_grad=round(tilt, 2), basis_w=round(base_w, 1), hang_laenge_spitze=round(S, 1), spitze_z=round(lay["nodes_list"][6]["z"] - lay["base_z"], 1),
                nodes_feld={str(n): [round(v, 1) for v in nl[n]] for n in nl},
                lichte_w=lichte_w, lichte_h=lichte_h, zarge_aussen_w=frame_w, zarge_hoehe=round(s_sturz_o, 1),
                senkrechte_hoehe_sturz=round(s_sturz_o * math.cos(math.radians(tilt)), 1),
                feldbreite_sturz_oben=round(w(s_sturz_o), 1), feldbreite_lichte_oben=round(w(P["schwelle_h"] + lichte_h), 1),
                reserve_je_seite_sturz=round((w(s_sturz_o) - frame_w) / 2, 1), reserve_je_seite_lichte_oben=round((w(P["schwelle_h"] + lichte_h) - lichte_w) / 2, 1))

if __name__ == "__main__":
    lay, d, pth = main()
    P = {k: v[1] for k, v in PARAM.items()}
    G = compute(lay, P)
    d.update({"klasse": "tuer", "teilenummer": "T50", "revision": "B",
              "beschreibung": "Tuer komplett (D36, R13): Zarge aus Rohr 30 x 30 (2 Pfosten, Sturz, Schwelle) mit Normtuerblatt 1000 x 2000 x 40 im Basisfeld BBB 149,2, nach aussen oeffnend, 3 Scharniere, Druecker, Dichtung",
              "quelle_masse": "docs/research/R13.md, docs/decisions.md D36, data/layout.json dome.nodes_list (Knoten 24, 22, 6), data/components/haut_paneel.json felder",
              "parameter": {k: {"wert": v[1], "einheit": v[0], "herkunft": v[2]} for k, v in PARAM.items()},
              "geometrie": G,
              "anzahl": {"soll": "1 (Feld BBB 149,2)", "quelle": "docs/decisions.md D36"},
              "bezugspunkt": "Feld-KS: Ursprung Mitte der Basiskante (Knoten 24 -> 22) auf Z 0 = Basisknotenhoehe, X tangential (24 -> 22), Y hangaufwaerts in der Feldebene zur Spitze (Knoten 6), Z Feldnormale nach aussen; Zarge liegt in der Feldebene (um ca. 10,8 Grad zur Senkrechten geneigt)"})
    json.dump(d, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(G, ensure_ascii=False, indent=1))
