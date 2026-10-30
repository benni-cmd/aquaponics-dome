"""Haut-Paneel (W19, D35, R11) Schritt 1: Dreieckstypen aus data/layout.json (dome.nodes_list, strut_len_mm) bestimmen und in data/components/haut_paneel.json ablegen.
Kanten = Knotenpaare mit Abstand = einer Strebenlaenge (A 3279 / B 3708, Toleranz 15 mm; Anzahl muss dome.struts = 65 ergeben); Dreiecke = Tripel paarweise verbundener Knoten (Soll 40 fuer die Halbkugel 2V).
Tuer (D36): mittig im Basisfeld BBB 149,2; NUR dieses Feld traegt den Tuerausschnitt (Paneel haut_paneel_BBB_tuer), alle anderen Felder sind volle Paneele.
Aufruf: python scripts/workshop/haut_typen.py"""
import collections, itertools, json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

DOOR_AZ = 149.2                     # D36 (30.10.): Tuer mittig im Basisfeld BBB 149,2 (OBJ-Tuer bei Azimut 167 sass auf Basisknoten 22 und beruehrte zwei Felder)
TOL = 15.0

def main():
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    N = lay["nodes_list"]
    lens = sorted(set(lay["strut_len_mm"]))
    A, B = lens[0], lens[-1]
    dist = lambda i, j: math.dist((N[i]["x"], N[i]["y"], N[i]["z"]), (N[j]["x"], N[j]["y"], N[j]["z"]))
    kind = lambda d: "A" if abs(d - A) <= TOL else ("B" if abs(d - B) <= TOL else None)
    E = {}
    for i, j in itertools.combinations(range(len(N)), 2):
        k = kind(dist(i, j))
        if k:
            E[(i, j)] = (k, dist(i, j))
    assert len(E) == lay["struts"], (len(E), lay["struts"])
    adj = collections.defaultdict(set)
    for (i, j) in E:
        adj[i].add(j); adj[j].add(i)
    tris = []
    for i, j, k in itertools.combinations(range(len(N)), 3):
        if j in adj[i] and k in adj[i] and k in adj[j]:
            tris.append((i, j, k))
    base_z = lay["base_z"]
    az = lambda x, y: math.degrees(math.atan2(y, x)) % 360
    out, types = [], collections.defaultdict(list)
    for (i, j, k) in tris:
        es = sorted(E[tuple(sorted(p))][0] for p in ((i, j), (j, k), (i, k)))
        typ = "".join(es)
        cx = sum(N[n]["x"] for n in (i, j, k)) / 3
        cy = sum(N[n]["y"] for n in (i, j, k)) / 3
        cz = sum(N[n]["z"] for n in (i, j, k)) / 3
        nbase = sum(1 for n in (i, j, k) if abs(N[n]["z"] - base_z) < 5)
        out.append(dict(nodes=[i, j, k], typ=typ, edges=[round(E[tuple(sorted(p))][1], 1) for p in ((i, j), (j, k), (i, k))], az=round(az(cx, cy), 1), z=round(cz), basis=nbase == 2, door=False))
        types[typ].append(len(out) - 1)
    cand = [t for t in out if t["basis"]]
    door_f = min(cand, key=lambda t: abs(((t["az"] - DOOR_AZ + 180) % 360) - 180))
    for t in out:
        t["door"] = t is door_f
    door = dict(node=None, az=door_f["az"], felder=[door_f], typ=door_f["typ"])
    typen = {}
    for typ, idx in sorted(types.items()):
        ts = [out[n] for n in idx]
        paneele = [t for t in ts if not t["door"]]  # volle Paneele; tuerfelder = Paneel mit Tuerausschnitt
        e = [sorted(t["edges"]) for t in ts]
        typen[typ] = dict(anzahl_felder=len(ts), anzahl_voll=len(paneele), anzahl_mit_tuerausschnitt=len(ts) - len(paneele),
                          kanten_nominal=[{"A": A, "B": B}[c] for c in typ],
                          kanten_gemessen_min=[round(min(x[n] for x in e), 1) for n in range(3)], kanten_gemessen_max=[round(max(x[n] for x in e), 1) for n in range(3)],
                          basisfelder=sum(1 for t in ts if t["basis"]))
    return lay, A, B, out, typen, door

if __name__ == "__main__":
    lay, A, B, out, typen, door = main()
    p = os.path.join(sc.ROOT, "data", "components", "haut_paneel.json")
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    pan = sum(t["anzahl_voll"] for t in typen.values())
    tf = sum(t["anzahl_mit_tuerausschnitt"] for t in typen.values())
    d.update({
        "klasse": "haut_paneel", "teilenummer": "T40", "revision": "A",
        "beschreibung": "Haut-Paneele der Kuppel: dreieckige Doppelstegplatten 8 mm je Kuppelfeld (Halbkugel 2V), ein Bauteil je Dreieckstyp, mit Randprofil (Aluminium-Kappe) auf den Streben",
        "quelle_masse": "data/layout.json dome (nodes_list, strut_len_mm, struts 65), docs/research/R11.md (Doppelstegplatte 8 mm, Paneele enden 15 mm vor der Strebenachse), docs/decisions.md D35",
        "typen": typen,
        "felder": out,
        "anzahl": {"soll": f"{len(out)} Felder: {pan} volle Paneele + {tf} Paneel mit Tuerausschnitt (Basisfeld {door['typ']} {door['az']})", "quelle": "data/layout.json dome: 65 Streben, 26 Knoten -> 40 Dreiecke (V - E + F = 1); Tuerfeld nach D36 (docs/decisions.md)"},
    })
    json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Kanten A {A} / B {B}; Felder {len(out)}; volle Paneele {pan}; mit Tuerausschnitt {tf} (Feld az {door['az']} Typ {door['typ']})")
    for t, v in typen.items():
        print(t, v)
