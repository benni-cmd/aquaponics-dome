"""Pruefung der Becken-, Tisch- und Beet-Parameter gegen data/oasis-soll.json (N-UNIFY-AUTOBAHN U3, D118 bis D122).
Fuenf Teile:
  A. Parameter (Toleranz 0 mm): Wasserspiegel 750 / 800 / 850, Rand 1200 / 1000 / 1000, Boden -1000 (Innenboden) / 0 / 0 (Standflaeche), NFT-Wasserspiegel 1050 / 900 / 1250, Flutstand 250
     in data/params.json (variante.parameter), data/layout.json (Block oasis) und den Komponentendateien data/components/*.json.
  B. Beckenkette: Wasserspiegel fallen von aussen nach innen, jede Stufe 50 mm (A13).
  (C. entfaellt seit N-UNIFY-AUTOBAHN U7, D141: kein zweiter Kreislauf mehr, der unveraendert bleiben muss.)
  D. Gebaute Komponenten (Wasserkoerper-Oberkante, Rand, Standflaeche, Ueberlauf-Tuellen) aus designs/components/*.sc (Toleranz 0,5 mm Messung; am Gesamtmodell gelten spaeter +-50 mm).
  (E. Hoehen der gebauten Tische und Beete: check_nft_tisch.py und check_ibc_beet.py; hier nur die Parameter in A.)
Aufruf: python -X utf8 scripts/workshop/check_pool_soll.py [--ohne-geometrie]   (exit 1 bei FAIL)"""
import json, math, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, ".."))
import sc
import variante as V

ROOT = sc.ROOT
FZ = 400                   # D94: Fussboden der Quelle = Modell-Z 400

def J(*pfad):
    return json.load(open(os.path.join(ROOT, *pfad), encoding="utf-8"))

def git(*args):
    r = subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout

def main():
    ck = sc.Check("pool_soll")
    soll = {b["id"]: b for b in J("data", "oasis-soll.json")["bauteile"]}
    P2 = V.parameter()
    LAY = J("data", "layout.json")
    R2 = LAY["oasis"]
    comp = {n: J("data", "components", n + ".json") for n in ("pool_zentral", "zweitbecken", "becken_dritt_klein", "nft_tisch", "ibc_beet")}
    cp = lambda n, k: comp[n]["parameter"][k]["wert"]
    H = lambda sid, k: soll[sid]["hoehen"][k]
    # ------------------------------------------------------------------ A. Parameter gegen die Quelle
    # Wasserspiegel
    for sid, pk, lk, ck_, cwsp in (("fish", "pool_wsp", "pool", "pool_zentral", cp("pool_zentral", "wsp")),
                                   ("nursery", "pool2_wsp", "pool2", "zweitbecken", cp("zweitbecken", "wsp")),
                                   ("feed", "pool3_wsp", "pool3", "becken_dritt_klein", cp("becken_dritt_klein", "boden") + cp("becken_dritt_klein", "wasser_tiefe"))):
        w = H(sid, "wsp_ueber_fussboden_mm")
        ck.eq(f"A Wasserspiegel {sid}: params.json {pk} = Quelle {w}", P2[pk], w)
        ck.eq(f"A Wasserspiegel {sid}: layout.json oasis.{lk}.water_z = Quelle {w}", R2[lk]["water_z"], w)
        ck.eq(f"A Wasserspiegel {sid}: Komponente {ck_} = Quelle {w}", cwsp, w)
    # Rand
    for sid, pk, ck_, crand in (("fish", "pool_rim", "pool_zentral", cp("pool_zentral", "rand")),
                                ("nursery", "pool2_rim", "zweitbecken", cp("zweitbecken", "rand")),
                                ("feed", "pool3_rim", "becken_dritt_klein", cp("becken_dritt_klein", "boden") + cp("becken_dritt_klein", "wasser_tiefe") + cp("becken_dritt_klein", "rand_ueber_wasser"))):
        r = H(sid, "rand_ueber_fussboden_mm")
        ck.eq(f"A Rand {sid}: params.json {pk} = Quelle {r}", P2[pk], r)
        ck.eq(f"A Rand {sid}: Komponente {ck_} = Quelle {r}", crand, r)
    # Boden: Fischtank = Innenboden (Wasserspiegel - Tiefe + Bodenplatte), Anzucht und Lebendfutter = Standflaeche (Wasserspiegel - Tiefe), D118
    BODEN = 120
    ck.eq(f"A Boden fish (Innenboden) = Quelle {H('fish', 'boden_ueber_fussboden_mm')}: pool_wsp - pool_depth + {BODEN}", P2["pool_wsp"] - P2["pool_depth"] + BODEN, H("fish", "boden_ueber_fussboden_mm"))
    ck.eq(f"A Boden nursery (Standflaeche auf dem Boden) = Quelle {H('nursery', 'boden_ueber_fussboden_mm')}: pool2_wsp - pool2_depth", P2["pool2_wsp"] - P2["pool2_depth"], H("nursery", "boden_ueber_fussboden_mm"))
    ck.eq(f"A Boden feed (Standflaeche auf dem Boden) = Quelle {H('feed', 'boden_ueber_fussboden_mm')}: pool3_wsp - pool3_depth", P2["pool3_wsp"] - P2["pool3_depth"], H("feed", "boden_ueber_fussboden_mm"))
    ck.eq("A Komponente pool_zentral: Tiefe = pool_depth", cp("pool_zentral", "tiefe"), P2["pool_depth"])
    ck.eq("A Komponente zweitbecken: Tiefe = pool2_depth", cp("zweitbecken", "tiefe"), P2["pool2_depth"])
    ck.eq("A Komponente becken_dritt_klein: Boden + Wassertiefe = pool3_depth", cp("becken_dritt_klein", "boden") + cp("becken_dritt_klein", "wasser_tiefe"), P2["pool3_depth"])
    ck.eq("A Bodenplatte Komponenten = 120 (POOL_BODEN)", 1 if cp("pool_zentral", "boden") == cp("zweitbecken", "boden") == cp("becken_dritt_klein", "boden") == BODEN else 0, 1)
    # Durchmesser (Innen): Fischtank bleibt 3890 (D96), die anderen nach der Quelle
    ck.eq(f"A Durchmesser nursery = Quelle {soll['nursery']['masse_text_mm']['durchmesser']} (layout oasis.pool2.d, Komponente)", 1 if R2["pool2"]["d"] == cp("zweitbecken", "wasser_d") == soll["nursery"]["masse_text_mm"]["durchmesser"] else 0, 1)
    ck.eq(f"A Durchmesser feed = Quelle {soll['feed']['masse_text_mm']['durchmesser']} (layout oasis.pool3.d, params pool3_d, Komponente)", 1 if R2["pool3"]["d"] == P2["pool3_d"] == cp("becken_dritt_klein", "wasser_d") == soll["feed"]["masse_text_mm"]["durchmesser"] else 0, 1)
    ck.eq("A Durchmesser fish bleibt 3890 = A+-Wert layout.json pool.d (D96; Quelle 4000, Abweichung -110, Radialbudget)", 1 if R2["pool"]["d"] == LAY["pool"]["d"] == cp("pool_zentral", "wasser_d") == 3890 else 0, 1)
    ck.eq(f"A Wand Fischtank = params.json wall ({P2['wall']})", cp("pool_zentral", "ring"), P2["wall"])
    # NFT
    for typ, sid, pk in (("aussen", "nft_aussen", "nft_wsp_aussen"), ("mitte", "nft_mitte", "nft_wsp_mitte"), ("innen", "nft_innen", "nft_wsp_innen")):
        w = H(sid, "wsp_ueber_fussboden_mm")
        T = comp["nft_tisch"]["typen"][typ]
        ck.eq(f"A NFT {typ}: params.json {pk} = Quelle {w}", P2[pk], w)
        ck.eq(f"A NFT {typ}: nft_tisch.json wsp_soll = Quelle {w}", T["wsp_soll"], w)
        ck.eq(f"A NFT {typ}: Rinnenunterkante z_rinne_mitte {T['z_rinne_mitte']} + Film {cp('nft_tisch', 'rinne_film')} = Wasserspiegel {w}", T["z_rinne_mitte"] + cp("nft_tisch", "rinne_film"), w)
    ck.eq("A NFT: Film in params.json = Komponente", P2["nft_film"], cp("nft_tisch", "rinne_film"))
    # Beete
    for sid in ("fd_aussen", "fd_mitte"):
        ck.eq(f"A Flutstand {sid}: params.json beet_flutstand = Quelle {H(sid, 'wsp_ueber_fussboden_mm')}", P2["beet_flutstand"], H(sid, "wsp_ueber_fussboden_mm"))
        ck.eq(f"A Beetboden {sid}: params.json beet_boden = Quelle {H(sid, 'boden_ueber_fussboden_mm')}", P2["beet_boden"], H(sid, "boden_ueber_fussboden_mm"))
    ck.eq("A Beet: ibc_beet.json a21_flutstand = 250 und a21_boden = 70 wie params.json", 1 if cp("ibc_beet", "a21_flutstand") == P2["beet_flutstand"] and cp("ibc_beet", "a21_boden") == P2["beet_boden"] else 0, 1)
    ck.eq(f"A Beet: Standrohr-Oberkante a21_boden {cp('ibc_beet', 'a21_boden')} + standpipe_over {cp('ibc_beet', 'standpipe_over')} = Flutstand {P2['beet_flutstand']}", cp("ibc_beet", "a21_boden") + cp("ibc_beet", "standpipe_over"), P2["beet_flutstand"])
    ck.eq("A Beet: standpipe_over = a21_standrohr_h", cp("ibc_beet", "standpipe_over"), cp("ibc_beet", "a21_standrohr_h"))
    ty = comp["ibc_beet"]["typen"]
    ck.eq(f"A Beet aussen_800: Wannenhoehe {ty['aussen_800']['hoehe']} = Quelle-Rand {H('fd_aussen', 'rand_ueber_fussboden_mm')} (Wanne auf dem Flur, z0 {R2['ibc_beds_z0']})", ty["aussen_800"]["hoehe"] + R2["ibc_beds_z0"], H("fd_aussen", "rand_ueber_fussboden_mm"))
    ck.eq(f"A Beet innen_933: Wannenhoehe {ty['innen_933']['hoehe']} = Quelle-Rand {H('fd_mitte', 'rand_ueber_fussboden_mm')}", ty["innen_933"]["hoehe"] + R2["ibc_beds_z0"], H("fd_mitte", "rand_ueber_fussboden_mm"))
    ck.eq("A Beet: layout.json oasis Hoehen und z0 passen zu den Typen", 1 if R2["ibc_beds_hoehe"] == {"aussen": ty["aussen_800"]["hoehe"], "innen": ty["innen_933"]["hoehe"]} else 0, 1)
    # ------------------------------------------------------------------ B. Beckenkette
    ws = [P2["pool_wsp"], P2["pool2_wsp"], P2["pool3_wsp"]]
    ck.eq(f"B Beckenkette fish {ws[0]} < nursery {ws[1]} < feed {ws[2]}: Wasser laeuft von aussen nach innen", 1 if ws[0] < ws[1] < ws[2] else 0, 1)
    ck.eq("B Stufe Anzuchtbecken - Fischtank = 50 mm (A13)", ws[1] - ws[0], 50)
    ck.eq("B Stufe Lebendfutterbecken - Anzuchtbecken = 50 mm (A13)", ws[2] - ws[1], 50)
    ck.eq("B Rand aller drei Becken >= Wasserspiegel + 150 (Freibord)", 1 if all(P2[r] - w >= 150 for r, w in (("pool_rim", ws[0]), ("pool2_rim", ws[1]), ("pool3_rim", ws[2]))) else 0, 1)
    # ------------------------------------------------------------------ D. Gebaute Komponenten
    if "--ohne-geometrie" not in sys.argv:
        ev = {n: {b["name"]: b for b in sc.evaluate(os.path.join(ROOT, "designs", "components", n + ".sc"))["bodies"]} for n in ("pool_zentral", "zweitbecken", "becken_dritt_klein")}
        z = lambda b, k, off=0: b["bbox"][k][2] - off
        F = ev["pool_zentral"]
        ck.eq("D Fischtank Wasser-Oberkante = Wasserspiegel 750 (Z 400 + 750)", z(F["T5_Wasser"], "max", FZ), 750, 0.5)
        ck.eq("D Fischtank Innenboden (Wasser-Unterkante) = -1000", z(F["T5_Wasser"], "min", FZ), -1000, 0.5)
        ck.eq("D Fischtank Rand (Wannen-Oberkante) = 1200", z(F["T5_Zentraltank"], "max", FZ), 1200, 0.5)
        ck.eq("D Fischtank Aussenunterkante = -1120", z(F["T5_Zentraltank"], "min", FZ), -1120, 0.5)
        ck.eq("D Fischtank Innendurchmesser 3890 (Aussen 4190)", F["T5_Zentraltank"]["bbox"]["max"][0] - F["T5_Zentraltank"]["bbox"]["min"][0], 4190, 0.5)
        ck.eq("D Fischtank Wassertiefe 1750 mm, Volumen m3 20,7", F["T5_Wasser"]["volume_mm3"] / 1e9, math.pi / 4 * 3.88 ** 2 * 1.75, 0.05)
        ck.eq("D Fischtank ohne Wanddurchfuehrungen (nur Wanne und Wasser, D102)", len(F), 2)
        N = ev["zweitbecken"]
        ck.eq("D Anzuchtbecken Wasser-Oberkante = 800", z(N["T6_Wasser"], "max", FZ), 800, 0.5)
        ck.eq("D Anzuchtbecken Standflaeche (Wannen-Unterkante) = 0 (steht auf dem Boden)", z(N["T6_Zweitbecken"], "min", FZ), 0, 0.5)
        ck.eq("D Anzuchtbecken Rand = 1000", z(N["T6_Zweitbecken"], "max", FZ), 1000, 0.5)
        ck.eq("D Anzuchtbecken Aussendurchmesser 2120 (Innen 2000)", N["T6_Zweitbecken"]["bbox"]["max"][0] - N["T6_Zweitbecken"]["bbox"]["min"][0], 2120, 0.5)
        D_ = ev["becken_dritt_klein"]
        ck.eq("D Lebendfutterbecken Wasser-Oberkante = 850 (lokal, Z 0 = Standflaeche)", z(D_["Wasser"], "max"), 850, 0.5)
        ck.eq("D Lebendfutterbecken Rand = 1000", z(D_["T14k_Wanne"], "max"), 1000, 0.5)
        ck.eq("D Lebendfutterbecken Standflaeche = 0", z(D_["T14k_Wanne"], "min"), 0, 0.5)
        ck.eq("D Lebendfutterbecken Aussendurchmesser 1120 (Innen 1000)", D_["T14k_Wanne"]["bbox"]["max"][0] - D_["T14k_Wanne"]["bbox"]["min"][0], 1120, 0.5)
        # Ueberlauf-Tuellen: Rohr-Innenunterkante = Wasserspiegel der eigenen Stufe (Weg e63 und e70), Achse + 28,5
        inv = lambda b, off: (b["bbox"]["min"][2] + b["bbox"]["max"][2]) / 2 - 57 / 2.0 - off
        iv_n = inv(N["T6_Ueberlauf"], FZ); iv_f = inv(D_["T14k_Ueberlauf"], 0)
        ck.eq("D Ueberlauf Anzuchtbecken -> Fischtank (e70): Rohr-Innenunterkante = Wasserspiegel Anzucht 800", iv_n, 800, 0.5)
        ck.eq("D Ueberlauf Lebendfutter -> Anzuchtbecken (e63): Rohr-Innenunterkante = Wasserspiegel Lebendfutter 850", iv_f, 850, 0.5)
        ck.eq("D Ueberlauf-Kette: Lebendfutter-Ueberlauf 50 mm ueber dem Anzucht-Ueberlauf, dieser 50 mm ueber dem Fischtank-Wasserspiegel", 1 if abs(iv_f - iv_n - 50) < 0.6 and abs(iv_n - z(F["T5_Wasser"], "max", FZ) - 50) < 0.6 else 0, 1)
        ck.eq("D Ueberlauf-Tuellen d63 (D106): Aussendurchmesser = Muffe d63", N["T6_Ueberlauf"]["bbox"]["max"][2] - N["T6_Ueberlauf"]["bbox"]["min"][2], 72.15, 0.3)
    # E. Hoehe der gebauten Tische und Beete: check_nft_tisch.py (Rinne Mitte = z_rinne_mitte) und check_ibc_beet.py (Standrohr absolut 250, Rand, Beetboden)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
