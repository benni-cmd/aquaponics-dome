"""W25a/W26 Blatt-Nachtrag (31.10.): aussen4 = Standard (D43: 4 Aussenrinnen, 674 Topfloecher, 2834 Netztoepfe, 76 Rinnen), Innenbeet-Ecken angefast (D44, W26). Zahlen aus tisch_geom; idempotent.
Aufruf (nach fix_w25_blatt.py-Stand, vor partsheet.py): python scripts/workshop/fix_w25a_blatt.py"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

def save(pth, d):
    json.dump(d, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

p, d = load("nft_tisch")
P = {k: v["wert"] for k, v in d["parameter"].items()}
cnt = {"innen": 10, "mitte": 6, "aussen": 8}
per = {t: sum(r["n_holes"] for r in TG.geometry(t, P, d["typen"][t])["rows"]) for t in cnt}
total = sum(per[t] * cnt[t] for t in cnt)
nrinnen = sum(d["typen"][t]["n"] * cnt[t] for t in cnt)
assert (per["aussen"], total, nrinnen) == (53, 674, 76), (per, total, nrinnen)

def rep(txt, pairs):
    for a, b in pairs:
        txt = txt.replace(a, b)
    return txt

# nft_tisch: Gewicht, Rinnenzahl, Altaussage W17
txt = json.dumps(d, ensure_ascii=False)
txt = rep(txt, [("aussen 3 x 4,0 = 12 kg", "aussen 4 x 4,0 = 16 kg (D43; vorher 3 x 4,0 = 12 kg)"),
                ("Rinnenzahl 2 / 4 / 3", "Rinnenzahl 2 / 4 / 4 (aussen 4 seit D43, vorher 3)"),
                ("W17: aussen 3 Rinnen (OBJ 2) bleibt Annahme; Reihen auf ap 4586", "W17 (bis D43): aussen 3 Rinnen (OBJ 2) bleibt Annahme; Reihen auf ap 4586")])
json.dump(json.loads(txt), open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# netztopf, nft_rinne
pth, dd = load("netztopf")
dd = json.loads(rep(json.dumps(dd, ensure_ascii=False), [("Rinnen 570 (Tische innen 10 x 7, Mitte 6 x 30, aussen 8 x 40; pitch 200, W18) = 2730 gesamt", f"Rinnen {total} (Tische innen 10 x 7, Mitte 6 x 30, aussen 8 x {per['aussen']} mit 4 Rinnen, D43; pitch 200, W18) = {2160 + total} gesamt")]))
save(pth, dd)
pth, dd = load("nft_rinne")
dd = json.loads(rep(json.dumps(dd, ensure_ascii=False), [("aussen 8 x 3 (OBJ 2, Annahme 3; docs/components.md)", "aussen 8 x 4 (OBJ 2, Annahme 3, seit D43 4; docs/components.md)")]))
dd["blatt"]["offen"] = [x for x in dd["blatt"]["offen"] if not x.startswith("W25a")] + [f"W25a (D43, 31.10.): Aussentisch hat 4 Rinnen (aussen_r1..r4: 2986 / 2844 / 2701 / 2558 mm, 14 / 14 / 13 / 12 Loecher), Rinnenzahl {nrinnen}, Topfloecher gesamt {total}; Varianten aussen_r1..r3 neu gerechnet (r2/r3 kuerzer als die 3-Reihen-Fassung)"]
save(pth, dd)
# ibc_beet: Fase
pth, dd = load("ibc_beet")
dd["blatt"]["offen"] = [x for x in dd["blatt"]["offen"] if not x.startswith("W26")] + ["W26 (D44, 31.10.): Innenbeet innen_933 hat 45-Grad-Eckenfasen 120 mm am Randwulst-Umriss (Medium/Siebboden/Wanne parallel versetzt: Medium-Fase 104,8); Beet x Beet Abstand benachbarter Innenbeete +36 mm (ohne Fase -35, check_nft_fit SAT); Medium-Volumen 469,7 l (check_ibc_beet gegen Flaechenrechnung); Eckstuetzen liegen innerhalb der Fase; Pflanzraster/Topfzahl der Innenbeete rechnet die Montage (M7) neu; Rueckfall Laenge 1790 nicht noetig"]
save(pth, dd)
# scope-cards
sp = os.path.join(sc.ROOT, "docs", "scope-cards.md")
s = open(sp, encoding="utf-8").read()
s = rep(s, [("aussen 2676-3051), 2 / 4 / 3 Rinnen", "aussen 2558-2986), 2 / 4 / 4 Rinnen (aussen 4 seit D43)"),
            ("NFT-Topfloecher gesamt 570 (innen 10 x 7, Mitte 6 x 30, aussen 8 x 40; D33)", f"NFT-Topfloecher gesamt {total} (innen 10 x 7, Mitte 6 x 30, aussen 8 x {per['aussen']}; D43, vorher 570)"),
            ("Gesamtzahl 2160 (Beete, altes Raster) + 570 (Rinnen) = 2730", f"Gesamtzahl 2160 (Beete, altes Raster) + {total} (Rinnen) = {2160 + total}")])
open(sp, "w", encoding="utf-8").write(s)
print(f"Topfloecher {total} (aussen je Tisch {per['aussen']}), Rinnen {nrinnen}, Netztoepfe {2160 + total}")
