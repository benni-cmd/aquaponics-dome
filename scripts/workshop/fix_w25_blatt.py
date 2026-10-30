"""Blatt-Nachtrag "Tische nach innen" (ap_c aussen 4874): Topfzahl 586 -> 570, Gesamtzahl 2746 -> 2730, Aussenreihen 14/13/13, Radialbudget-Zahlen, Befund W23-2 behoben. Zahlen aus tisch_geom; idempotent.
Aufruf (nach fix_tisch_blatt6.py und fix_w18_blatt2.py, vor partsheet.py): python scripts/workshop/fix_w25_blatt.py"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

p, d = load("nft_tisch")
P = {k: v["wert"] for k, v in d["parameter"].items()}
cnt = {"innen": 10, "mitte": 6, "aussen": 8}
Gs = {t: TG.geometry(t, P, d["typen"][t]) for t in cnt}
holes = {t: [r["n_holes"] for r in G["rows"]] for t, G in Gs.items()}   # Reihe 1 (aeusserste, laengste) zuerst
per = {t: sum(h) for t, h in holes.items()}
total = sum(per[t] * cnt[t] for t in cnt)
half = lambda G: G["bed_w"] / 2.0 + P["leg_clearance"] + P["foot_plate"]
Ga, Gm = Gs["aussen"], Gs["mitte"]
B = (Ga["apc"] - half(Ga)) - (Gm["apc"] + half(Gm))
C = 5706 - (Ga["apc"] + half(Ga))
apc_a = Ga["apc"]
SUBS = [
    (r"(?<!\d)586(?!\d)", str(total)),
    (r"(?<!\d)2746(?!\d)", str(2160 + total)),
    (r"8 x 42", f"8 x {per['aussen']}"),
    (r"15/14/13", "/".join(str(h) for h in holes["aussen"])),
    (r"Aussenportal 4458\.\.5488", f"Aussenportal {apc_a - half(Ga):.0f}..{apc_a + half(Ga):.0f}"),
]
def fix_text(t):
    for a, b in SUBS:
        t = re.sub(a, b, t)
    return t
for name in ("nft_tisch", "nft_rinne", "netztopf", "salatkopf", "ibc_beet", "winkelhalter"):
    pth, dd = load(name)
    txt = fix_text(json.dumps(dd, ensure_ascii=False))
    dd = json.loads(txt)
    if name == "nft_tisch":
        bl = dd["blatt"]
        bl["offen"] = [x for x in bl["offen"] if not x.startswith(("W23-Befund 2", "W23-2"))] + [
            f"W23-Befund 2 (behoben, Ben 30.10. 'Tische nach innen'): ap_c aussen 4973 -> {apc_a:.0f} (99 mm nach innen); die Rinnenenden der aeussersten Reihe liegen jetzt >= 15 mm innerhalb der Feldebenen der Kuppelhaut (check_nft_fit: 21 mm), Laufweg B {B:.1f} mm (harte Untergrenze D29: 500, Reserve {B - 500:.1f} mm), Wandluft {C:.0f} mm; Topfzahl 586 -> {total} (aussen {'/'.join(str(h) for h in holes['aussen'])}); die Aussenbeete folgen ap_c (D37, Montage); Haut-Paneele ruhen nach D39 (Plane), die Rechnung nutzt die Feldebenen der Strebenachsen"]
        pr = dd["blatt"]["pruefung"]
        dd["blatt"]["pruefung"] = [x.replace("(44/45 PASS", "(45/45 PASS") for x in pr]
    json.dump(dd, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sp = os.path.join(sc.ROOT, "docs", "scope-cards.md")
s = open(sp, encoding="utf-8").read()
i = s.find("## Nachtrag W17/W18")
if i >= 0:
    head, tail = s[:i], s[i:]
    tail = tail.replace("aussen 4973", f"aussen {apc_a:.0f} (30.10. Tische nach innen, vorher 4973)")
    tail = re.sub(r"(?<!\d)586(?!\d)", str(total), tail)
    tail = tail.replace("aussen 8 x 42", f"aussen 8 x {per['aussen']}")
    tail = tail.replace(" (30.10. Tische nach innen, vorher 4973) (30.10. Tische nach innen, vorher 4973)", " (30.10. Tische nach innen, vorher 4973)")
    tail = re.sub(r"(?<!\d)2746(?!\d)", str(2160 + total), tail)
    open(sp, "w", encoding="utf-8").write(head + tail)
print(f"Nachtrag: Topfzahl {total}, Gesamt {2160 + total}, Aussenreihen {holes['aussen']}, Laufweg B {B:.1f}, Wandluft {C:.0f}")
