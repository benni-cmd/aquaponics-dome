"""Nachtrag nach dem gemeinsamen Pruefer W17+W18 (29.10. ~23:00): alte Zahlen (Fussplatte 100, pitch 250, +-62,5, 5/7/12, 2716) in Blaettern/JSON bereinigen, Ports und Fussplatten neu aus der Geometrie, Scope-Card-Nachtrag. Idempotent.
Aufruf: python scripts/workshop/fix_w18_blatt2.py   (nach fix_tisch_blatt6.py, vor partsheet.py)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

def load(n):
    pth = os.path.join(sc.ROOT, "data", "components", n + ".json")
    return pth, json.load(open(pth, encoding="utf-8"))

pt = TG.rinne_pitch()
nL, nM, nK = int(3232 // pt), int(1983 // pt), int(1304 // pt)
# ---------------- nft_tisch: Ports (Zulauf/Ablauf/Stutzen/Fussplatten) neu aus der Geometrie
p, d = load("nft_tisch")
P = {k: v["wert"] for k, v in d["parameter"].items()}
bl = d["blatt"]
Gs = {t: TG.geometry(t, P, d["typen"][t]) for t in ("aussen", "mitte", "innen")}
zrow = lambda G, x: G["zc"] - (x - G["rows"][0]["xc"]) * G["slope"]
T18 = TG.T18
kk = math.sqrt(1 + T18 ** 2)
fmt = lambda v: f"{v:.0f}"
fp = int(P["foot_plate"])
ports = []
for t, G in Gs.items():
    zi = sum(zrow(G, r["xc"] - r["L"] / 2) + 70 for r in G["rows"]) / len(G["rows"])
    za = sum(zrow(G, r["xc"] + r["L"] / 2) + 20 for r in G["rows"]) / len(G["rows"])
    y1 = G["Wt"] / 2 + 60
    xh = -((G["apc"] - y1) * T18 - G["gap"]) + 12.5 * kk
    xs = ((G["apc"] - y1) * T18 - G["gap"]) - 25 * kk
    ports.append([f"{t}: Zulauf Tisch (Verteilerrohr D25 offen, +Y-Ende, schraeg)", "Rohr d25, Wand 3 (Anschluss Rohr/Schlauch)", f"x {fmt(xh)}, y {fmt(y1)}, z {fmt(zi)} (Achse laeuft schraeg: dx/dy = +tan 18 Grad, entlang der Sektorgrenze)", "Wasser tritt am +Y-Ende in das Rohr ein (Oeffnung zeigt nach +Y, 18 Grad zur Y-Achse geneigt); Rohr d25 (etwa DN20)"])
    ports.append([f"{t}: Ablauf Tisch (Sammelrohr d50 offen, +Y-Ende, schraeg)", "Rohr d50, Wand 3 (etwa DN40)", f"x {fmt(xs)}, y {fmt(y1)}, z {fmt(za)} (Achse dx/dy = -tan 18 Grad)", "Wasser verlaesst das Rohr am +Y-Ende (Oeffnung zeigt nach +Y); Rohr d50 (etwa DN40); Gefaelle des Sammelrohrs zum Port nicht modelliert (horizontal)"])
    xs_list = ", ".join(fmt(r["xc"] - r["L"] / 2 - 29 - P["hose_gap"]) for r in G["rows"])
    ports.append([f"{t}: Verteiler-Stutzen je Rinne (n={G['n']})", "Schlauch ID 16, Durchfluss je Rinne 0,5 l/min (R06)", f"x {xs_list} (Stutzenspitze je Reihe), y = Rinnenmitte, z ca. {fmt(zi)}", "aus Verteiler, Richtung +X"])
    legs = "; ".join(f"x {fmt(x)} / y {fmt(y)}" for (x, y) in G["legs"])
    ports.append([f"{t}: Fussplatten-Anker", f"M8, 2 Schrauben je Platte ({fp} x {fp} x 5), Loch D9, Diagonalversatz +-{fp / 2 - 15:g}", f"Fusspunkte z 5 an: {legs}", "Befestigung auf dem Boden/Betonpunkt, Richtung -Z"])
bl["ports"] = ports
FIND = "Pruefer W17/W18 (offen): Laufweg A am Innenpfosten nur 486 mm (Plattenaussenkante 2210 gegen Innenportal 2696; D29: nie unter 500) und die Fussplatten stehen wegen des exzentrischen Beckens (cx -36, cy 20) nur 4 mm vom Beckenrand; Abhilfe braucht Orchestrator/Montage: Innenbeete 40 mm nach aussen (inner_bed_shift 66 -> 26, dann A 526 / B 560) oder Becken zentrieren; check_nft_fit meldet beide als FAIL"
bl["offen"] = [x for x in bl["offen"] if not x.startswith("Pruefer W17/W18 (offen)")] + [FIND]
rows = d["herkunft_tabelle"]
for r in rows:
    if r[0].startswith("Lochraster je Reihe mit Phase 0"):
        r[0] = f"Lochraster je Reihe mit Phase 0 / pitch/2, n <= floor(L/{pt:g}) nach hole_plan"
        r[3] = r[3].replace("Loecher >= 46 mm vom Rinnenende", "Loecher >= 64 mm vom Rinnenende (Kragen 32 + Rippe 20 + Luft, W18)")
    if r[0].startswith("Zickzack Versatz pitch/2"):
        r[0], r[1] = f"Zickzack Versatz pitch/2 = {pt / 2:g}", f"{pt / 2:g} mm"
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------- nft_rinne
p, d = load("nft_rinne")
for r in d["herkunft_tabelle"]:
    if r[0].startswith("Lochabstand 250"):
        r[0], r[1] = f"Lochabstand {pt:g} mm, Master {nL}/{nM}/{nK} Loecher", f"{pt:g} mm"
        r[3] = f"D32 (Ben 29.10.): Iowa State 8 Zoll = 203 mm, HortTechnology 15 cm (R16); ref-6 zeigt Raster ohne Mass (ca. 2 Topfbreiten); Blattsalat NFT 150-250 mm (FarmHub 2.4)"
    if r[1] == "+-62,5 mm":
        r[1] = f"+-{pt / 4:g} mm"
note = "Zustaendigkeit Lochzahl: die Rinne liefert das Raster (pitch, Phase); die Lochzahl je Tischreihe bestimmt der Tisch (tisch_geom.hole_plan: n <= floor(L/pitch), Phasenzwang, Randabstand 64), daher weniger als floor(L/pitch) (Mitte 9/8/7/6 statt 9/9/8/7)"
if not any(x.startswith("Zustaendigkeit Lochzahl") for x in d["blatt"]["offen"]):
    d["blatt"]["offen"].append(note)
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------- ibc_beet, netztopf, salatkopf
for name, subs in (("ibc_beet", (("Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 100 = 2771", "Zehneck-Grenze 2 x 4573 x tan 18 - 2 x 60 = 2851 (corner_gap 60, W17; mit 100: 2771)"),)),
                   ("netztopf", (("(Loecher 5/7/12 je Rinne)", "(Loecher je Tischreihe aus tisch_geom.hole_plan, docs/parts/nft_tisch.md)"),
                                 ("docs/parts/nft_rinne.md (20 Rinnen x 5 + 24 x 7 + 24 x 12 Loecher)", "docs/parts/nft_tisch.md (Loecher je Tischreihe, W18)"))),
                   ("salatkopf", (("Budget bei 2716 Instanzen", "Budget bei 2746 Instanzen"),))):
    p, d = load(name)
    txt = json.dumps(d, ensure_ascii=False)
    for a, b in subs:
        txt = txt.replace(a, b)
    json.dump(json.loads(txt), open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
# ---------------- Scope-Cards: Nachtrag (Stand W17/W18)
sp = os.path.join(sc.ROOT, "docs", "scope-cards.md")
s = open(sp, encoding="utf-8").read()
MARK = "## Nachtrag W17/W18 (Werkstatt, 29.10. ~23:00)"
if MARK not in s:
    s += f"""

{MARK}
Stand der Parameter nach W17/W18/D32-D34; aeltere Zeilen oben (Laengen 1304/1983/3232, pitch 250, 125 mm, 2716/556, Beet 2953 x 933-993, Gefaelle 1 cm/m) gelten nicht mehr.
- **nft_rinne:** `pitch` {pt:g} mm (einstellbar 150..250), Zickzack = pitch/2 = {pt / 2:g}, Phase +-{pt / 4:g}; Master-Konfigurationen L/M/K {nL}/{nM}/{nK} Loecher; Lochzahl je Tischreihe bestimmt der Tisch (hole_plan: n <= floor(L/pitch), Phasenzwang, Randabstand 64).
- **nft_tisch:** Rinnenlaenge je Reihe (innen 758/928, Mitte 1505-2018, aussen 2676-3051), 2 / 4 / 3 Rinnen, Tischmitte ap_c innen 1864, Mitte 3277, aussen 4973, `corner_gap` 60 (D34), Portalrand = Beet + 115 (Fussplatte 70, leg_clearance 45), Gefaelle 1,5 %, Winkelhalter je Bein; NFT-Topfloecher gesamt 586 (innen 10 x 7, Mitte 6 x 30, aussen 8 x 42; D33).
- **ibc_beet:** Aussenbeet `aussen_800` = 800 x 2640 x 637 (D29), Innenbeet 933 x 1865 x 649; Pflanzraster im Aussenbeet rechnet die Montage (M7).
- **netztopf:** Gesamtzahl 2160 (Beete, altes Raster) + 586 (Rinnen) = 2746 ist Sache des Integrators/Layouts, nicht der Klasse.
"""
    open(sp, "w", encoding="utf-8").write(s)
print("Nachtrag gepflegt")
