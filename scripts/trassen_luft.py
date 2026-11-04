"""M10-S5-LUFT Teil A: Lage von Pool-Verteiler (luftverteiler_4, T87), vier Scheibenbelueftungen (luft_scheibenbelueftung, T88), Schwimmerventil (schwimmerventil_pool, T84)
und die vier Luftrohre d25 (K44-S1..S4) im Dom. Rechnet aus Pool-Massen; gen_dome.luft_a() setzt die Instanzen, `python scripts/trassen_luft.py` traegt die Trassen
in data/leitungstrassen.json ein (idempotent: ersetzt nur Eintraege mit "linie": "luft"; ein Neulauf von trassen_linie.py loescht sie, dann diesen Aufruf wiederholen).
Alle Lagen sind Annahmen [A] (Azimut Verteiler, Scheibenkreis, Hoehe Scheibe); Teil B (Technikbereich, E13) und alles mit E20 sind nicht enthalten.

Rohrfuehrung je Scheibe (Rohr d25, Bibliothek lt_*): Abgang des Verteilers (Zapfen, +Z) -> Bogen direkt auf dem Zapfen -> waagerecht ueber den Beckenrand nach innen ->
Bogen -> senkrecht an der Innenwand hinab (im Wasser) -> Bogen -> waagerecht auf dem Beckenboden zur Scheibe -> Bogen direkt unter dem Anschluss der Scheibe -> Zapfen der Scheibe (Port A, Oeffnung -Z).
Zuordnung Abgang -> Scheibe: die Permutation mit dem groessten Mindestabstand zwischen den Rohren verschiedener Strecken."""
import itertools, json, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts")); sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop"))
import leitung as LT

D = 25                                   # Rohr d25 (Abgaenge des Verteilers, Anschluss der Scheibe)
AZ_VERT = -25.0                          # [A] Azimut des Pool-Verteilers auf dem Beckenrand (zwischen Tuer -54 und Schaltschrank 0, frei von Seitenablauf 11,9 und Messstellen 100/160)
SCHEIBEN_R = 1000.0                      # [A] Scheibenkreis um die Beckenmitte (Mitte hat den Bodenablauf)
SCHEIBEN_AZ = (45.0, 135.0, 225.0, 315.0)   # [A]
PA_H = 100.0                             # [A] Port A (Stutzenende) der Scheibe ueber dem Beckeninnenboden; darunter liegt der Bogen, das Rohr auf dem Boden
AZ_VENTIL = -10.0                        # [A] Azimut des Schwimmerventils
R_VENTIL_A = 2070.0                      # [A] Radius von Port A des Ventils (Muffe liegt ueber der Beckenrand-Aussenhaelfte; Hebelarm klar vom inneren Randrand: gerechnet 12 mm)
R_WAND = 40.0                            # Abstand der Rohrachse an der Innenwand zur Beckenwand-Innenflaeche
FARBE = "gruen"
Z_VENTIL_H = 195.0                       # Rohrachse ueber dem Spiegel (schwimmerventil_pool.json ventil_h)

def tangent():
    return LT.ports("lt_bogen90_d%d" % D)[1][1][0]          # Schenkel k (Kreuzungspunkt bis Muffenebene)

def dist_seg(p1, q1, p2, q2):
    """Mindestabstand zweier Strecken im Raum (Ericson, Real-Time Collision Detection 5.1.9)."""
    def sub(a, b): return [a[i] - b[i] for i in range(3)]
    def dot(a, b): return sum(a[i] * b[i] for i in range(3))
    d1, d2, r = sub(q1, p1), sub(q2, p2), sub(p1, p2)
    a, e, f = dot(d1, d1), dot(d2, d2), dot(d2, r)
    cl = lambda v: 0.0 if v < 0 else 1.0 if v > 1 else v
    c = dot(d1, r); b = dot(d1, d2); den = a * e - b * b
    s = cl((b * f - c * e) / den) if den > 1e-12 else 0.0
    t = (b * s + f) / e
    if t < 0: t = 0.0; s = cl(-c / a)
    elif t > 1: t = 1.0; s = cl((b - c) / a)
    dp = [r[i] + s * d1[i] - t * d2[i] for i in range(3)]
    return math.sqrt(dot(dp, dp))

def geometrie(fz, pool_d, wall, pool_rim, water_z, pool_depth, pool_boden=120):
    """Alle Lagen im Modellrahmen (Z absolut). Rueckgabe: dict mit verteiler, scheiben, ventil, trassen."""
    ri = pool_d / 2.0; rc = ri + wall / 2.0
    k = tangent(); t = LT.DEPTH[D]; dkt = k - t                  # Abstand Bogen direkt auf dem Zapfen: Kreuzungspunkt k - t von der Zapfenspitze
    a = math.radians(AZ_VERT)
    X = (math.sin(a), -math.cos(a))                             # Sammlerachse +X: im Uhrzeigersinn (Muffe A oeffnet nach -X, zum Technikbereich bei Az 0)
    yaw = AZ_VERT - 90.0
    z_rim = fz + pool_rim
    z_axis = z_rim + 24.0                                       # Sammler Ø 48 liegt auf der Beckenrandflaeche
    c = (rc * math.cos(a), rc * math.sin(a))
    origin = (c[0] - 255.0 * X[0], c[1] - 255.0 * X[1], z_axis)
    tips = []
    for i in range(4):
        x_i = 75.0 + 120.0 * i
        tips.append((origin[0] + x_i * X[0], origin[1] + x_i * X[1], z_axis + 74.0))
    z_in = fz + water_z - pool_depth + pool_boden               # Beckeninnenboden (Z absolut)
    z_pa = z_in + PA_H; z_low = z_pa - dkt
    scheiben = [(SCHEIBEN_R * math.cos(math.radians(w)), SCHEIBEN_R * math.sin(math.radians(w)), z_pa) for w in SCHEIBEN_AZ]
    best = None
    for perm in itertools.permutations(range(4)):
        pf = []
        for j in range(4):
            tip = tips[j]; sx, sy, _ = scheiben[perm[j]]
            p1 = (tip[0], tip[1], tip[2] + dkt)
            r1 = math.hypot(p1[0], p1[1]); f = (ri - R_WAND) / r1
            p2 = (p1[0] * f, p1[1] * f, p1[2]); p3 = (p2[0], p2[1], z_low); p4 = (sx, sy, z_low); p5 = (sx, sy, z_pa)
            pf.append([tip, p1, p2, p3, p4, p5])
        dmin = 1e9
        for i in range(4):
            for j in range(i + 1, 4):
                for s1 in range(5):
                    for s2 in range(5):
                        dmin = min(dmin, dist_seg(pf[i][s1], pf[i][s1 + 1], pf[j][s2], pf[j][s2 + 1]))
        if best is None or dmin > best[0]: best = (dmin, perm, pf)
    dmin, perm, pf = best
    trassen = []
    for j in range(4):
        trassen.append({"id": "K44-S%d" % (j + 1), "kante": "K44", "dn": D, "dn_abweichung": "Pool-Verteiler luftverteiler_4 teilt die Hauptleitung d40 (K44) in vier Abgaenge d25 (R45 Abschnitt 4, Bauteilblatt T87)",
                        "farbe": FARBE, "start": "stutzen", "ende": "stutzen", "baender": ["W", "W", "W", "UT", "UT"], "anschluss": ["Zentralpool"],
                        "pfad": [[round(v, 2) for v in p] for p in pf[j]], "linie": "luft",
                        "notiz": "Luft Pool-Verteiler Abgang %d -> Scheibe %d (Az %g), Rohr d25: Zapfen des Verteilers, ueber den Beckenrand, an der Innenwand hinab, auf dem Boden, Bogen unter dem Anschluss der Scheibe [A]" % (j + 1, perm[j] + 1, SCHEIBEN_AZ[perm[j]])})
    # Schwimmerventil: Port A (Muffe) nach aussen, Rohrachse +X radial nach innen, Rohrachse 195 ueber dem Spiegel
    av = math.radians(AZ_VENTIL)
    z_v = fz + water_z + Z_VENTIL_H
    ventil = (R_VENTIL_A * math.cos(av), R_VENTIL_A * math.sin(av), z_v, AZ_VENTIL + 180.0)
    return {"verteiler": (origin[0], origin[1], origin[2], yaw), "tips": tips, "scheiben": scheiben, "perm": perm, "dmin": dmin, "ventil": ventil, "trassen": trassen, "z_in": z_in, "z_pa": z_pa, "z_low": z_low}

def lade_params():
    P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
    lay = json.load(open(os.path.join(ROOT, "data", "layout.json"), encoding="utf-8"))
    return P, lay

if __name__ == "__main__":
    P, lay = lade_params()
    g = geometrie(P["sock_h"], lay["pool"]["d"], P["wall"], P["pool_rim"], lay["pool"]["water_z"], P["pool_depth"])
    pfad = os.path.join(ROOT, "data", "leitungstrassen.json")
    doc = json.load(open(pfad, encoding="utf-8"))
    doc["trassen"] = [t for t in doc["trassen"] if t.get("linie") != "luft"] + g["trassen"]
    txt = json.dumps(doc, ensure_ascii=False, indent=1) + chr(10)
    open(pfad, "w", encoding="utf-8", newline="").write(txt)
    print("Zuordnung Abgang -> Scheibe", [p + 1 for p in g["perm"]], "kleinster Rohrabstand %.1f mm" % g["dmin"], "Verteiler", [round(v, 1) for v in g["verteiler"]], "Ventil", [round(v, 1) for v in g["ventil"]])
    for t in g["trassen"]: print(t["id"], t["pfad"])
