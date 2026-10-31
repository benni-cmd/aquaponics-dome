"""R36 Beete unter den Tischen: Weg 1 (Tische ueber den Beeten, Beete nur Blatt/Kraeuter) gegen Weg 2 (Tische und Beete trennen), nachvollziehbare Rechnung.

Aufruf: python scripts/bed_table_variants.py   (nur Standardbibliothek, schreibt auf stdout, aendert keine Datei)
Eingaben: data/components/nft_tisch.json (Rinnenlaengen je Reihe), data/system-specs.json (Gegenprobe der Summen),
Beet- und Tischlage aus docs/decisions.md D29/D30/D43 und data/components/nft_tisch.json (ap_c, rinnen_abstand), Futterwerte aus docs/research/R26.md.
system_specs.py importiert compute() und schreibt die Szenarien weg1/weg2 zusaetzlich in data/system-specs.json (Standard bleibt Weg 1 = D60).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---- Eingaben --------------------------------------------------------------------------------------------------------
# Tische (Ring -> Anzahl, Rinnenlaengen je Reihe in m, Rinnen je Tisch, Topfloecher je Tisch, Abstand, Mitte radial, Reihenversatz)
RINGS = {
    "aussen": dict(n=8, lengths=[2.986, 2.844, 2.701, 2.558], pots=53, pitch=220, ap_c=4874, offset=42),     # D43 aussen4; Topfliste W33
    "mitte": dict(n=6, lengths=[2.018, 1.847, 1.676, 1.505], pots=30, pitch=263, ap_c=3277, offset=0),
    "innen": dict(n=10, lengths=[0.928, 0.758], pots=7, pitch=262, ap_c=1864, offset=0),
}
# Beete (unter dem Tisch gleichen Namens): D29/D30 Radialbudget, Mitte der Beete
BEDS = {
    "aussen": dict(n=8, w=0.800, l=2.640, c=4973),     # liegen unter den Aussentischen
    "mitte": dict(n=6, w=0.933, l=1.865, c=3277),      # Innenbeete, liegen unter den Mitteltischen
}
NFT_AREA_BEN_M2, NFT_LEN_AUSSEN3_M = 42.41, 126.31       # Bens Tabellenflaeche bei aussen3-Laenge (R20/R26: auf die Rinnenlaenge skaliert [A])
CHANNEL_W, CHANNEL_H, BED_SURFACE = 130, 100, 400       # mm: Rinne, Substratoberflaeche Z (R35)
# g Futter je m2 und Tag nach R26: (obere, Mitte, untere FAO-Werte)
G_FRUIT = (80.0, 72.5, 50.0)
G_LEAF = (50.0, 45.0, 40.0)
G_NFT = (50.0, 45.0, 40.0)
SCEN_NAMES = ("obere FAO-Werte", "Mitte der FAO-Werte", "untere FAO-Werte")
FEED_PCT_BW = 0.01                                       # 1 % Koerpergewicht (R18)
FISH_END_KG = 0.7
FISH_WATER_M3 = 28.5                                     # Pool + Zweitbecken (R26, D45)
LEAF_DENSITY = 22.5                                      # Blatt 20-25 Pflanzen/m2 (FAO 589, R20)
FRUIT_MIX = [("Tomate", 9.0, 4.0), ("Paprika", 5.5, 3.5), ("Gurke", 5.0, 3.0), ("Suesskartoffel", 7.8, 8.0)]   # R26: Flaeche m2 (von 27,3), Pflanzen/m2
TARGET_KG = 475                                          # D40
R26_KG = (467, 422, 335)                                 # R26 Empfehlungsmix: obere / Mitte / untere FAO-Werte
LIGHT_JUNE, LIGHT_DEC = 34.5, 4.0                        # mol/m2/Tag in der Kuppel vor Tischschatten (R35)
DOME_R = 6000                                            # Kugelnaeherung (R35)
FLAT_PER_TABLE_M = {k: sum(v["lengths"]) for k, v in RINGS.items()}


def nft_area(rings_present, basis):
    """NFT-Pflanzflaeche m2: 'ben' = Bens Flaeche skaliert auf die Rinnenlaenge (R26), 'raster' = Rinnenlaenge x Rinnenabstand."""
    tot = 0.0
    for k, on in rings_present.items():
        if not on:
            continue
        r = RINGS[k]
        length = r["n"] * sum(r["lengths"])
        tot += length * (NFT_AREA_BEN_M2 / NFT_LEN_AUSSEN3_M) if basis == "ben" else length * r["pitch"] / 1000
    return tot


def compute(name, rings_present, bed_use, basis="ben"):
    """rings_present {'aussen','mitte','innen': bool}; bed_use {'aussen','mitte': 'frucht'|'blatt'}."""
    area_nft = nft_area(rings_present, basis)
    area_bed = {k: BEDS[k]["n"] * BEDS[k]["w"] * BEDS[k]["l"] for k in BEDS}
    feed = []
    for i in range(3):
        f = area_nft * G_NFT[i]
        for k, use in bed_use.items():
            f += area_bed[k] * (G_FRUIT[i] if use == "frucht" else G_LEAF[i])
        feed.append(f / 1000)
    fish = [f / FEED_PCT_BW for f in feed]
    fruit_area = sum(area_bed[k] for k, u in bed_use.items() if u == "frucht")
    leaf_area = sum(area_bed[k] for k, u in bed_use.items() if u == "blatt")
    mix_total = sum(a for _, a, _ in FRUIT_MIX)
    fruit_plants = {n: round(a / mix_total * fruit_area * d) for n, a, d in FRUIT_MIX} if fruit_area else {}
    return {
        "name": name, "rinnen": sum(RINGS[k]["n"] * len(RINGS[k]["lengths"]) for k, on in rings_present.items() if on),
        "tische": sum(RINGS[k]["n"] for k, on in rings_present.items() if on),
        "toepfe": sum(RINGS[k]["n"] * RINGS[k]["pots"] for k, on in rings_present.items() if on),
        "nft_m2": area_nft, "beet_frucht_m2": fruit_area, "beet_blatt_m2": leaf_area,
        "futter_kg": feed, "fisch_kg": fish, "fruchtpflanzen": fruit_plants, "blattpflanzen_beet": round(leaf_area * LEAF_DENSITY),
        "basis": basis,
    }


ALL = {"aussen": True, "mitte": True, "innen": True}
VARIANTS = [
    ("D40-Annahme (R26): Tische ueber allen Beeten, alle Beete Frucht", ALL, {"aussen": "frucht", "mitte": "frucht"}),
    ("Weg 1: Tische bleiben, alle 14 Beete Blatt/Kraeuter", ALL, {"aussen": "blatt", "mitte": "blatt"}),
    ("Weg 2a: Aussentische weg (Aussenbeete frei = Frucht), Innenbeete unter Mitteltischen = Blatt", {**ALL, "aussen": False}, {"aussen": "frucht", "mitte": "blatt"}),
    ("Weg 2b: Mitteltische weg (Innenbeete frei = Frucht), Aussenbeete unter Aussentischen = Blatt", {**ALL, "mitte": False}, {"aussen": "blatt", "mitte": "frucht"}),
    ("Weg 2c: Aussen- und Mitteltische weg (alle Beete frei = Frucht), nur Innentische ueber dem Pool", {"aussen": False, "mitte": False, "innen": True}, {"aussen": "frucht", "mitte": "frucht"}),
]


# ---- Licht: Himmelssicht des Beetes im Radialschnitt (Verfahren wie R35 scripts/table_height.py) -----------------------------
def channels(rings_present, z_lo=1000):
    out = []
    for k, on in rings_present.items():
        if not on:
            continue
        r = RINGS[k]
        n = len(r["lengths"])
        for i in range(n):
            y = (i - (n - 1) / 2) * r["pitch"] + r["offset"]          # Y radial nach INNEN
            c = r["ap_c"] - y
            out.append((c - CHANNEL_W / 2, c + CHANNEL_W / 2))
    return out


def sky_view(bed, rings_present, z_lo=1000, n=121):
    """Anteil des diffusen Himmelslichts, das ein Punkt der Beetoberflaeche (Z 400) ueber die Beetbreite sieht, nur Rinnenkoerper als Hindernis."""
    ch = channels(rings_present)
    z_hi = z_lo + CHANNEL_H
    c, w = BEDS[bed]["c"], BEDS[bed]["w"] * 1000
    ys = [c - w / 2 + w * k / (n - 1) for k in range(n)]
    tot = wsum = 0.0
    for th in [i * 5 + 2.5 for i in range(18)]:
        wt = math.sin(math.radians(th)) * math.cos(math.radians(th))
        free = cnt = 0
        for a in [i * 10 + 5 for i in range(36)]:
            t = math.tan(math.radians(th)) * math.sin(math.radians(a))
            for y0 in ys:
                ya, yb = y0 + (z_lo - BED_SURFACE) * t, y0 + (z_hi - BED_SURFACE) * t
                lo, hi = (ya, yb) if ya <= yb else (yb, ya)
                cnt += 1
                if not any(hi >= p and lo <= q for p, q in ch):
                    free += 1
        tot += wt * free / cnt
        wsum += wt
    return tot / wsum


def own_table_only(bed):
    return {k: (k == bed) for k in RINGS}


def dome_headroom(r_mm, z_from=BED_SURFACE):
    """freie Hoehe ab Substrat bis zur Kuppelhaut (Kugel R 6000) am Radius r, in mm."""
    return math.sqrt(DOME_R ** 2 - r_mm ** 2) - z_from


def main():
    spec = json.loads((ROOT / "data" / "system-specs.json").read_text(encoding="utf-8"))["pflanzen"]
    base = compute(*VARIANTS[0])
    assert base["toepfe"] == spec["nft"] and base["rinnen"] == spec["rinnen"] and round(base["nft_m2"], 1) == spec["flaeche_nft_m2"], "Eingaben weichen von system-specs.json ab"
    print(f"Gegenprobe system-specs.json: Rinnen {base['rinnen']}, Topfloecher {base['toepfe']}, NFT-Flaeche {base['nft_m2']:.1f} m2, Beete {sum(BEDS[k]['n']*BEDS[k]['w']*BEDS[k]['l'] for k in BEDS):.1f} m2 - stimmt")
    print(f"Beete: Aussen {BEDS['aussen']['n']*BEDS['aussen']['w']*BEDS['aussen']['l']:.2f} m2 (8 Stueck, unter Aussentischen), Innen {BEDS['mitte']['n']*BEDS['mitte']['w']*BEDS['mitte']['l']:.2f} m2 (6 Stueck, unter Mitteltischen)")
    print("Futter g/m2/Tag (R26): Frucht", G_FRUIT, "Blatt", G_LEAF, "NFT", G_NFT, "- obere / Mitte / untere FAO-Werte")

    for basis, label in (("ben", "NFT-Flaeche wie R26 (Bens Flaeche skaliert)"), ("raster", "NFT-Flaeche aus Rinnenraster (Laenge x Abstand), Gegenprobe")):
        print(f"\n=== 1. Vergleich ({label}) ===")
        res = [compute(n, r, b, basis) for n, r, b in VARIANTS]
        print(f"{'Variante':98s} {'Tische':>6} {'Rinnen':>6} {'Toepfe':>6} {'NFT m2':>7} {'Frucht m2':>9} {'Blatt m2':>8}   Fisch kg oben / Mitte / unten   Verlust gg. 475 (Mitte)")
        for r in res:
            f = r["fisch_kg"]
            print(f"{r['name'][:98]:98s} {r['tische']:6d} {r['rinnen']:6d} {r['toepfe']:6d} {r['nft_m2']:7.1f} {r['beet_frucht_m2']:9.1f} {r['beet_blatt_m2']:8.1f}   {f[0]:5.0f} / {f[1]:5.0f} / {f[2]:5.0f}   {f[1] - TARGET_KG:+5.0f}")
        if basis == "ben":
            assert [round(x) for x in res[0]["fisch_kg"]] == list(R26_KG), res[0]["fisch_kg"]
            print("  Kontrolle: Zeile 1 gleich R26 (467 / 422 / 335) - ja")
    print("\nPflanzen je Variante (R26-Mix skaliert auf die Fruchtflaeche; Blatt 22,5/m2):")
    for n, r, b in VARIANTS:
        c = compute(n, r, b)
        print(f"  {n[:60]:60s} Frucht {sum(c['fruchtpflanzen'].values()):3d} {c['fruchtpflanzen']}, Blatt im Beet {c['blattpflanzen_beet']}, NFT-Toepfe {c['toepfe']}")

    print("\n=== 2. Grenznutzen: ein Tisch weniger, das Beet darunter wird Frucht statt Blatt ===")
    for k in ("aussen", "mitte"):
        r = RINGS[k]
        len_t = sum(r["lengths"])
        bed_a = BEDS[k]["w"] * BEDS[k]["l"]
        for basis in ("ben", "raster"):
            a_nft = len_t * (NFT_AREA_BEN_M2 / NFT_LEN_AUSSEN3_M) if basis == "ben" else len_t * r["pitch"] / 1000
            gain = [bed_a * (G_FRUIT[i] - G_LEAF[i]) for i in range(3)]
            loss = [a_nft * G_NFT[i] for i in range(3)]
            net = [(gain[i] - loss[i]) / 1000 / FEED_PCT_BW for i in range(3)]
            be = 1 + a_nft * G_NFT[1] / (bed_a * G_LEAF[1])        # Faktor Frucht/Blatt je m2, ab dem der Tausch Fisch gewinnt (Mitte der FAO-Werte)
            print(f"  {k:7s} ({basis:6s}): NFT-Flaeche {a_nft:4.2f} m2 geht verloren (-{loss[0]:.0f}/{loss[1]:.0f}/{loss[2]:.0f} g Futter), Beet {bed_a:.2f} m2 Frucht statt Blatt (+{gain[0]:.0f}/{gain[1]:.0f}/{gain[2]:.0f} g) -> je Tisch {net[0]:+.0f}/{net[1]:+.0f}/{net[2]:+.0f} kg Fisch; Break-even Frucht/Blatt = {be:.1f}")
    print(f"  Quellenwert Frucht/Blatt: {G_FRUIT[0] / G_LEAF[0]:.2f} / {G_FRUIT[1] / G_LEAF[1]:.2f} / {G_FRUIT[2] / G_LEAF[2]:.2f} (obere / Mitte / untere FAO-Werte, R26) - unter dem Break-even: Weg 2 verliert je Tisch Fisch")
    sk_a = FRUIT_MIX[3][1]
    print(f"  Weg 1 mit Suesskartoffel auf {sk_a} m2 der Beete (Annahme Frucht-Gruppenwert, Lichtbedarf unter Tisch nicht belegt): +{sk_a * (G_FRUIT[0] - G_LEAF[0]) / 10:.0f} / +{sk_a * (G_FRUIT[1] - G_LEAF[1]) / 10:.0f} / +{sk_a * (G_FRUIT[2] - G_LEAF[2]) / 10:.0f} kg Fisch gegen Weg 1")

    print("\n=== 3. Licht am Beet (Radialschnitt, nur Rinnenkoerper bei Rinnenunterkante 1000 mm, Pflanzen/Plane-Rahmen nicht eingerechnet) ===")
    print(f"{'Beet':22s} {'Tische':44s} {'Himmelssicht':>12} {'Juni mol/m2/d':>14} {'Dez mol/m2/d':>13}")
    cases = [
        ("Aussenbeet", "nur eigener Tisch (R35-Vergleich)", own_table_only("aussen"), "aussen"),
        ("Aussenbeet", "unter Aussentisch + Nachbartische (Weg 1)", ALL, "aussen"),
        ("Aussenbeet", "kein Tisch darueber, Mitte+Innen bleiben (Weg 2a)", {**ALL, "aussen": False}, "aussen"),
        ("Aussenbeet", "kein Tisch darueber, nur Innen (Weg 2c)", {"aussen": False, "mitte": False, "innen": True}, "aussen"),
        ("Innenbeet", "nur eigener Tisch (R35-Vergleich)", own_table_only("mitte"), "mitte"),
        ("Innenbeet", "unter Mitteltisch + Nachbartische (Weg 1)", ALL, "mitte"),
        ("Innenbeet", "kein Tisch darueber, Aussen+Innen bleiben (Weg 2b)", {**ALL, "mitte": False}, "mitte"),
        ("Innenbeet", "kein Tisch darueber, nur Innen (Weg 2c)", {"aussen": False, "mitte": False, "innen": True}, "mitte"),
    ]
    sky = {}
    for bed, txt, rp, key in cases:
        s = sky_view(key, rp)
        sky[(bed, txt)] = s
        print(f"{bed:22s} {txt:44s} {s * 100:11.1f} % {LIGHT_JUNE * s:14.1f} {LIGHT_DEC * s:13.1f}")
    print("  Bedarf (R35): Salat 12-17, Tomate 20-30, hochdrahtig Tomate/Gurke 25-30 mol/m2/Tag; Dezember reicht fuer keine Kultur.")

    print("\n=== 4. Platz fuer Fruchtgemuese: Hoehe von der Substratoberflaeche (Z 400) bis zur Kuppelhaut am Beetradius (Kugel R 6000) ===")
    for k, c in (("Aussenbeet", BEDS["aussen"]["c"]), ("Innenbeet", BEDS["mitte"]["c"])):
        r_out = c + BEDS["aussen" if k == "Aussenbeet" else "mitte"]["w"] * 500
        print(f"  {k}: Mitte r {c} -> {dome_headroom(c):.0f} mm, Aussenkante r {r_out:.0f} -> {dome_headroom(r_out):.0f} mm; unter Tisch (Rinnenunterkante 1000): {1000 - BED_SURFACE} mm")

    print("\n=== 5. Laufweg B (D29): Aussentische weg -> Portal-Fuss entfaellt ===")
    print("  Portalrand = Beet-Aussenkante + 115 mm (45 Abstand + 70 Fussplatte, nft_tisch.json leg_clearance/foot_plate); Laufweg B 500,5 mm (D43) -> ca. 615 mm ohne Aussenportal [E], wenn nur das Portal die Engstelle ist")


if __name__ == "__main__":
    main()
