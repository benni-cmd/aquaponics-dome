"""Blatt nft_tisch nach W17 (D28/D29/D30, 29.10.): Radialbudget, corner_gap 60, Fussplatte 70, leg_clearance 45, ap_c 4973/3277, Laufwege, NFT-Summe. Idempotent (rechnet alle Zahlen aus tisch_geom neu); nach fix_tisch_blatt5.py, vor partsheet.py.
Aufruf: python scripts/workshop/fix_tisch_blatt6.py <check_nft_tisch-Zeile> <check_nft_fit-Zeile>"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

p = os.path.join(sc.ROOT, "data", "components", "nft_tisch.json")
d = json.load(open(p, encoding="utf-8"))
P = {k: v["wert"] for k, v in d["parameter"].items()}
bl = d["blatt"]
Gs = {t: TG.geometry(t, P, d["typen"][t]) for t in ("aussen", "mitte", "innen")}
cnt = {"innen": 10, "mitte": 6, "aussen": 8}
PITCH = TG.rinne_pitch()
holes = {t: sum(r["n_holes"] for r in G["rows"]) for t, G in Gs.items()}
total = sum(holes[t] * cnt[t] for t in cnt)
_P100 = dict(P, corner_gap=100)
total100 = sum(sum(r["n_holes"] for r in TG.geometry(t, _P100, d["typen"][t])["rows"]) * cnt[t] for t in cnt)
zrow = lambda G, x: G["zc"] - (x - G["rows"][0]["xc"]) * G["slope"]
kk = math.sqrt(1 + TG.T18 ** 2)
fmt = lambda v: f"{v:.0f}"
half = lambda G: G["bed_w"] / 2.0 + P["leg_clearance"] + P["foot_plate"]
Gm, Ga = Gs["mitte"], Gs["aussen"]
pool_r = TG.pool_outer_r()
A = Gm["apc"] - half(Gm) - pool_r
B = (Ga["apc"] - half(Ga)) - (Gm["apc"] + half(Gm))
C = 5706 - (Ga["apc"] + half(Ga))
fp = int(P["foot_plate"])

for t, G in Gs.items():
    d["typen"][t]["laenge"] = " / ".join(str(r["L"]) for r in G["rows"]) + " (je Reihe)"
# --- Stueckliste (Laengen je Typ neu)
lines = []
for t in ("aussen", "mitte", "innen"):
    G = Gs[t]
    x1, x2 = G["xb"]
    zb = [zrow(G, x) - P["holm_h"] - P["foot_t"] for x in G["xb"]]
    if G["art"] == "portal":
        lines.append(f"{t}: Beine 4 x 40x40x3: Laenge {fmt(zb[0])} / {fmt(zb[1])}, Beinabstand y {fmt(2 * G['yl'])}; Querholm 40x60x3 x 2: Laenge {fmt(2 * G['yl'] + P['leg_w'])}; Querstrebe 40x40x3 x 2: Laenge {fmt(2 * G['yl'] - P['leg_w'])}; Laengsstreben 40x40x3 x 2: Laenge {fmt(x2 - x1 - P['leg_w'])}; Diagonalen 25x3 x 4; Laengsdiagonalen 25x3 x 2; Fussplatten {fp}x{fp}x5 x 4")
    else:
        y_in = G["Wt"] / 2 + P["holm_overhang"]
        lines.append(f"{t}: Pfosten 2 x 40x40x3: Laenge {fmt(zb[0])} / {fmt(zb[1])}; Kragarm 40x60x3 x 2: Laenge {fmt(y_in - G['yl'] + P['leg_w'] / 2)}; Laengsstrebe 40x40x3 x 1: Laenge {fmt(x2 - x1 - P['leg_w'])} (Z 400); Laengsdiagonale 25x3 x 1; Fussplatten {fp}x{fp}x5 x 2")
    lines.append(f"   Rinnen ({G['n']}): " + ", ".join(f"{r['L']} mm / {r['n_holes']} Loecher" for r in G["rows"]) + f"; Verteiler d25 schraeg: Laenge {fmt((G['Wt'] + 120) * kk)}; Sammelrohr d50 schraeg: Laenge {fmt((G['Wt'] + 120) * kk)}")
rest = [x for x in bl["stueckliste"] if not (x.startswith("Pro Tisch je Typ") or x.startswith("  "))]
bl["stueckliste"] = ["Pro Tisch je Typ (Laengen in mm, Stand W17):"] + ["  " + x for x in lines] + rest
bl["stueckliste"] = [x.replace("Fussplatten 100x100x5", f"Fussplatten {fp}x{fp}x5") for x in bl["stueckliste"]]
# --- Texte
bl["querschnitt"] = bl["querschnitt"].replace("Fussplatten 100x100x5", f"Fussplatten {fp}x{fp}x5")
bl["toleranzen"] = bl["toleranzen"].replace("corner_gap (100 mm; gemessen 171-190 mm)", f"corner_gap ({P['corner_gap']:.0f} mm; gemessen ca. 95-114 mm)").replace("Beine/Fussplatten >= 30 mm von jedem Beet-Rechteck (leg_clearance 60 mm sollwert)", f"Beine/Fussplatten >= 30 mm von jedem Beet-Rechteck (leg_clearance {P['leg_clearance']:.0f} mm sollwert)")
ab = bl["abweichung"]
i0, i1 = ab.index("Rev. B folgt D18"), ab.index("Die Tisch-Beine des OBJ")
bl["abweichung"] = ab[:i0] + (
    f"Rev. B folgt D18, Stand W17 (D28/D29/D30, Radialbudget): Rinnenlaenge je Reihe = Zehneck-Seite - 2 x corner_gap ({P['corner_gap']:.0f}) - Ueberstaende (Zulaufseite 169, Ablaufseite 79); Ergebnis innen {'/'.join(str(r['L']) for r in Gs['innen']['rows'][::-1])}, Mitte {'/'.join(str(r['L']) for r in Gm['rows'][::-1])}, aussen {'/'.join(str(r['L']) for r in Ga['rows'][::-1])} mm. "
    f"Topfloecher je Tisch innen {holes['innen']}, Mitte {holes['mitte']}, aussen {holes['aussen']}; gesamt {total} (Mindestzahl NFT 459, R15/D27; Lochabstand {PITCH:.0f}, W18/D32; mit corner_gap 100 waeren es {total100}). Tischmitte = Beetmitte nach der radialen Verschiebung (Aussen {Ga['apc']:.0f}, Innenbeet {Gm['apc']:.0f}; OBJ-Beete weichen einzeln um bis ca. 70 mm ab, Layout/Integrator). ") + ab[i1:]
bl["offen"] = [x for x in bl["offen"] if not x.startswith(("Rinnenlaenge je Reihe ist die Folge von D18", "aussen 3 Rinnen (OBJ 2)", "Beine ausserhalb der Beete stehen im Gehweg", "Tischmitte = Beetmitte ist Annahme", "W17:"))] + [
    f"W17/W18: corner_gap von 100 auf {P['corner_gap']:.0f} mm gesenkt (Annahme A, W17); mit Lochabstand {PITCH:.0f} (W18/D32) ergibt das {total} Topfloecher (Mindestzahl 459, Soll ca. 580); mit corner_gap 100 waeren es nur {total100}",
    f"W17: Portalrand = Beet-Aussenkante + {P['leg_clearance'] + P['foot_plate']:.0f} mm (Fussplatte {fp}, leg_clearance {P['leg_clearance']:.0f}); Laufwege nach check_nft_fit: A (Beckenrand-Innenportal) {A:.0f} mm, B (Innen-Aussenportal) {B:.0f} mm, Wandluft {C:.0f} mm; Aussenkante Tisch in 1,3 m Hoehe gegen Strebenabstand: Montage rechnet nach (D29)",
    "W17: aussen 3 Rinnen (OBJ 2) bleibt Annahme; Reihen auf ap " + ", ".join(fmt(r["ap"]) for r in Ga["rows"][::-1]) + f" (Mitte {Ga['apc']:.0f} +- {Ga['rp']:.0f})",
    "W17: Tischmitte folgt den Beeten nach Verschiebung (outer_bed_shift 236 / inner_bed_shift 66, M7); die OBJ-Beete liegen einzeln bis ca. 70 mm daneben, daher Beine-Beet-Abstand im Check ab 30 mm"]
rows = d["herkunft_tabelle"]
def setrow(prefix, new):
    for i, r in enumerate(rows):
        if r[0].startswith(prefix):
            rows[i] = new
            return
    rows.append(new)
setrow("Rinnenlaenge je Reihe", [f"Rinnenlaenge je Reihe {'/'.join(str(r['L']) for r in Gs['innen']['rows'][::-1])} (innen), {Gm['rows'][-1]['L']}-{Gm['rows'][0]['L']} (Mitte), {Ga['rows'][-1]['L']}-{Ga['rows'][0]['L']} (aussen)", "je Reihe", "E", f"Zehneck-Seite 2 x ap x tan 18 Grad (ap aus ap_c +- Reihenabstand) - 2 x corner_gap {P['corner_gap']:.0f} - Ueberstaende 169/79; D18 + W17", "mittel"])
setrow("Tischmitte auf der Beetmitte", [f"Tischmitte = Beetmitte: ap_c aussen {Ga['apc']:.0f}, Mitte {Gm['apc']:.0f}, innen {Gs['innen']['apc']:.0f}", "mm", "E + A", "Radialbudget D28/D29/D30 (Aussenportal 4458..5488, Innenportal 2695..3858); innen Mittel der OBJ-Reihen; vorher 5209 / 3343", "mittel"])
setrow("Fussplatten", [f"Fussplatten {fp}x{fp}x5, M8", f"{fp}x{fp}x5", "A", f"Kippmoment der Ausleger; Portalrand = 115 mm ausserhalb des Beets (Radialbudget D29), Plattenkante-Abstand {P['leg_clearance']:.0f} mm zum Beet", "niedrig"])
setrow("corner_gap", [f"corner_gap {P['corner_gap']:.0f} mm je Seite der Sektorgrenze", f"{P['corner_gap']:.0f} mm", "A", f"W17: vorher 100 (D18); {P['corner_gap']:.0f} gewaehlt fuer die NFT-Mindestzahl 459 (R15, W17) und das Soll ca. 580 (W18/D32); Abstand zwischen zwei Tischen ca. 95-114 mm (check_nft_fit)", "niedrig"])
setrow("leg_clearance", [f"leg_clearance {P['leg_clearance']:.0f} mm zwischen Beet-Aussenbreite und Fussplattenkante", f"{P['leg_clearance']:.0f} mm", "A", "W17/D29: Portalrand 115 mm (45 + Fussplatte 70); vorher 60 (D18); Beet-Aussenbreite aus ibc_beet.json (aussen 800)", "niedrig"])
setrow("Beine ausserhalb der Beet-Aussenbreite", [f"Beine ausserhalb der Beet-Aussenbreite (Portal): y = +-(bed_outer_w/2 + {P['leg_clearance']:.0f} + {fp // 2})", f"y +-{Ga['yl']:.0f} (aussen), +-{Gm['yl']:.0f} (Mitte)", "E + A", "bed_outer_w aus ibc_beet.json (aussen_800 = 800, innen_933 = 933), leg_clearance, Fussplatte/2; Portalrand = Beet + 2 x 115", "mittel"])
setrow("Laufwege", [f"Laufwege radial: A {A:.0f}, B {B:.0f}, Wandluft {C:.0f}", "mm", "Ben + E", "D29: Laufweg A/B >= 600, nie unter 500; Rechnung check_nft_fit (Portalrand = Beet-Halbbreite + 115); Wand-Apothem 5706", "mittel"])
setrow("NFT-Topfloecher gesamt", [f"NFT-Topfloecher gesamt {total} (Mindestzahl 459, Soll ca. 580)", str(total), "OBJ + R15 + E", f"R15/D27: NFT >= 459; D32: Lochabstand {PITCH:.0f}; Summe 10 x innen + 6 x Mitte + 8 x aussen aus hole_plan (Randabstand 64)", "mittel"])
bl["pruefung"] = [x for x in bl["pruefung"] if "check_nft_fit.py" not in x and "check_nft_tisch.py" not in x] + sys.argv[1:3]
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"nft_tisch.json gepflegt: Summe {total}, Laufweg A {A:.0f}, B {B:.0f}, Wandluft {C:.0f}")
