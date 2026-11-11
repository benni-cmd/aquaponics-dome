"""N-UNIFY-AUTOBAHN L1: Soll-Lage der Draufsicht aus Leons Oasis-Showcase als Daten: `data/oasis-draufsicht.json`.

Aufruf (Projektordner):  python -I -X utf8 scripts/oasis_draufsicht.py             schreibt die Datei, druckt die Messwerte
                         python -I -X utf8 scripts/oasis_draufsicht.py --pruefen   schreibt nichts, Exit 1 bei einer gescheiterten Pruefung
Eingabe (nur lesen): docs/quellen/oasis-showcase-2026-11-10/index.html, SVG `#mainSvg`, Gruppe `#soll-plan` (Ansicht 2D-Flussschema -> Draufsicht).
Die Gruppe wird statisch gelesen (ElementTree ueber `oasis_soll.lade_plan`, Primitive ueber `oasis_soll.teil_geometrie`), nichts wird geraten.
`data/oasis-soll.json` bleibt unberuehrt; es dient nur der Gegenprobe (gleiche Mittelpunkte, gleiche Stueckzahlen).

Umrechnung (gleich wie `oasis_soll.py`, D95): Rahmen 1000 x 1000 Einheiten, Kuppelmitte (500, 480) = Modell (0, 0), r 480 Einheiten = 6000 mm
(12,5 mm je Einheit), Zeichnung-unten = Modell -Y, danach 18 Grad gegen den Uhrzeigersinn gedreht. Das Attribut `transform` der Gruppe
(`translate(107.5 86.7) scale(0.801)`) ist reine Bildschirm-Anordnung der Seite und aendert kein Mass.

Neu gegenueber `oasis_soll.py`: je Anbauring Radius, Bogen und Oeffnung (Bogen-Endpunkte aus dem Pfad `A r r 0 1 1`), Stueckzahl aus der Quelle,
Segment-Winkelmitten (ANNAHME D150), die Technik als eigene Liste mit Rechteck-Drehung und Kuppel-Innen/Aussen-Kennzeichen.
"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)   # `-I` nimmt das Skriptverzeichnis nicht auf
import oasis_soll as S      # noqa: E402  (Konstanten, mm(), lade_plan(), teil_geometrie(); kein Nebeneffekt beim Import)

OUT = os.path.join(ROOT, "data", "oasis-draufsicht.json")
SOLL_JSON = os.path.join(ROOT, "data", "oasis-soll.json")
PRUEF = []

# Anbauringe: Bauteil-Id der Quelle -> (Art, Anzahl Segmente laut Quelle `count`)
RINGE = ["nft_aussen", "fd_aussen", "nft_mitte", "fd_mitte", "nft_innen"]


def pruefe(name, ok, detail=""):
    PRUEF.append({"pruefung": name, "ok": bool(ok), "detail": detail})
    return ok


def runde(v, n=1):
    return round(v, n) + 0.0


def az_norm(a):
    return (a + 180.0) % 360.0 - 180.0


def bogen(prim):
    """Anbauring: Radius, Endpunkte, Oeffnung. Pfad `M x0 y0 A r r 0 1 1 x1 y1`: grosser Bogen im Uhrzeigersinn (Zeichnung), Oeffnung unten."""
    d = prim["d"]
    m = re.match(r"M\s*([\d.\-]+)\s+([\d.\-]+)\s*A\s*([\d.\-]+)\s+([\d.\-]+)\s+0\s+1\s+1\s+([\d.\-]+)\s+([\d.\-]+)", d)
    x0, y0, r, r2, x1, y1 = (float(v) for v in m.groups())
    abst = [math.hypot(x - S.MITTE[0], y - S.MITTE[1]) for x, y in ((x0, y0), (x1, y1))]
    return {"radius_zeichnung": r, "radius_mm": runde(r * S.MM_JE_EINHEIT), "start_zeichnung": [x0, y0], "ende_zeichnung": [x1, y1],
            "radius_gleich": abs(r - r2) < 1e-6 and all(abs(a - r) < 0.2 for a in abst), "pfad": d}


def baue():
    teile, _kanten, _profil = S.lade_plan()
    soll = {b["id"]: b for b in json.load(open(SOLL_JSON, encoding="utf-8"))["bauteile"]}
    out_teile, ringe = {}, {}
    for pid, (nid, p) in teile.items():
        prim, symb = S.teil_geometrie(p)
        sb = soll[pid]
        if pid in RINGE:
            b = bogen(prim[0])
            x0, y0 = S.mm(*b["start_zeichnung"]); x1, y1 = S.mm(*b["ende_zeichnung"])
            a0 = az_norm(math.degrees(math.atan2(y0, x0))); a1 = az_norm(math.degrees(math.atan2(y1, x1)))
            mitte_oeffnung = az_norm((a0 + a1) / 2.0)      # kurzer Weg zwischen den Endpunkten = die Oeffnung
            offen = abs(az_norm(a1 - a0))
            n = sb["anzahl"]
            erlaubt = 360.0 - offen
            start = az_norm(a1)                              # Bogen laeuft vom Ende der Oeffnung (a1) gegen den Uhrzeigersinn bis zu ihrem Anfang (a0)
            seg = [runde(az_norm(start + (k + 0.5) * erlaubt / n), 2) for k in range(n)]
            ringe[pid] = {"art": "nft" if pid.startswith("nft") else "fd", "ring": pid.split("_")[1], "radius_mm": b["radius_mm"], "radius_zeichnung": b["radius_zeichnung"],
                          "bogen_von_az_grad": runde(a0, 2), "bogen_bis_az_grad": runde(a1, 2), "oeffnung_mitte_az_grad": runde(mitte_oeffnung, 2),
                          "oeffnung_grad": runde(offen, 2), "stueckzahl": n, "stueckzahl_quelle": "flow-data count (oasis-soll.json) = Abzweigzahl der Zeichnung",
                          "segment_az_mitten_grad": seg, "segment_annahme": "D150: gleichmaessig ueber den Bogen verteilt, Quelle zeigt nur Bogen und Stueckzahl (A16)",
                          "stroke_breite_zeichnung": 10 if pid != "nft_innen" else 12, "radius_gleich_beide_enden": b["radius_gleich"], "pfad": b["pfad"],
                          "mittelpunkt_zeichnung": list(S.MITTE)}
            continue
        e = {"id": pid, "name": sb["name"], "im_umfang": sb["im_umfang"], "anzahl_quelle": sb["anzahl"]}
        zentrum = S.zentrum_von(prim, symb)
        if prim and prim[0]["typ"] == "kreis":
            q = prim[0]
            e.update(art="kreis", x_mm=q["x_mm"], y_mm=q["y_mm"], radius_mm=q["radius_mm"], durchmesser_mm=2 * q["radius_mm"], radius_zeichnung=q["radius_zeichnung"])
        elif prim and prim[0]["typ"] == "rechteck":
            q = prim[0]
            e.update(art="rechteck", x_mm=q["x_mm"], y_mm=q["y_mm"], breite_mm=q["breite_mm"], hoehe_mm=q["hoehe_mm"],
                     drehung_grad=S.DREHUNG_GRAD, breite_achse="Zeichnung-x = Modell-Richtung %.0f Grad" % S.DREHUNG_GRAD, zeichnung_rect=q["zeichnung_rect"])
        elif zentrum and (prim and prim[0]["typ"] == "linienzug"):
            e.update(art="linienzug", x_mm=zentrum["x_mm"], y_mm=zentrum["y_mm"], punkte=[{"x_mm": p["x_mm"], "y_mm": p["y_mm"]} for p in prim[0]["punkte"]])
        elif zentrum and symb and not prim:
            e.update(art="punkt", x_mm=zentrum["x_mm"], y_mm=zentrum["y_mm"], symbole=[s["typ"] for s in symb])
        elif prim and prim[0]["typ"] == "abzweig_punkt":
            e.update(art="abzweigpunkte", punkte=[{"x_mm": p["x_mm"], "y_mm": p["y_mm"], "az_grad": p["az_grad"], "r_mm": p["r_mm"]} for p in prim if p["typ"] == "abzweig_punkt"])
        else:
            e.update(art="ohne_geometrie")
        if "x_mm" in e:
            e["r_mm"] = runde(math.hypot(e["x_mm"], e["y_mm"])); e["az_grad"] = runde(math.degrees(math.atan2(e["y_mm"], e["x_mm"])), 2)
            ext = e.get("radius_mm") or (math.hypot(e["breite_mm"], e["hoehe_mm"]) / 2 if "breite_mm" in e else 0)
            e["ausserhalb_kuppel"] = bool(e["r_mm"] > S.KUPPEL_R_MM)
            e["liegt_in_kuppel_ganz"] = bool(e["r_mm"] + ext <= S.KUPPEL_R_MM)
        if e["art"] == "punkt" or (pid.startswith("filterpumpe") or pid.startswith("hauptpumpe")):
            e["hinweis"] = "Symbol der Zeichnung (A16: schematisch), Mass gilt nicht"
        out_teile[pid] = e

    # ---- Gegenproben
    for pid, e in out_teile.items():
        sb = soll[pid]
        if "x_mm" in e and sb["lage"].get("mittelpunkt_x_mm") is not None:
            ok = abs(e["x_mm"] - sb["lage"]["mittelpunkt_x_mm"]) < 0.6 and abs(e["y_mm"] - sb["lage"]["mittelpunkt_y_mm"]) < 0.6
            pruefe("Mittelpunkt %s = oasis-soll.json" % pid, ok, "%.1f/%.1f vs %.1f/%.1f" % (e["x_mm"], e["y_mm"], sb["lage"]["mittelpunkt_x_mm"], sb["lage"]["mittelpunkt_y_mm"]))
    for rid, rg in ringe.items():
        pruefe("Ring %s: Stueckzahl = oasis-soll.json (%d)" % (rid, rg["stueckzahl"]), rg["stueckzahl"] == soll[rid]["anzahl"])
        pruefe("Ring %s: beide Enden liegen auf dem Radius" % rid, rg["radius_gleich_beide_enden"], str(rg["radius_mm"]))
        pruefe("Ring %s: Oeffnung 120 Grad um Az -72 (Tuer-Achse)" % rid, abs(rg["oeffnung_grad"] - 120) < 0.5 and abs(rg["oeffnung_mitte_az_grad"] + 72) < 0.5,
               "%.2f Grad um %.2f" % (rg["oeffnung_grad"], rg["oeffnung_mitte_az_grad"]))
        pruefe("Ring %s: Segment-Mitten liegen im Bogen, nicht in der Oeffnung" % rid,
               all(abs(az_norm(a - rg["oeffnung_mitte_az_grad"])) > rg["oeffnung_grad"] / 2 for a in rg["segment_az_mitten_grad"]))
    f = out_teile["fish"]
    pruefe("Fischtank: Kreis r 180 Einheiten = Radius 2250 mm in der Kuppelmitte", f["art"] == "kreis" and abs(f["radius_mm"] - 2250) < 0.1 and abs(f["x_mm"]) < 0.1 and abs(f["y_mm"]) < 0.1,
           "r %s, Mitte %s/%s" % (f["radius_mm"], f["x_mm"], f["y_mm"]))
    pruefe("Kuppelkreis der Zeichnung: Mitte (500, 480), r 480 Einheiten = 6000 mm", abs(480 * S.MM_JE_EINHEIT - S.KUPPEL_R_MM) < 0.1)
    pruefe("Ringe aus der Quelle: 5 (NFT innen/mitte/aussen, Beete mitte/aussen)", len(ringe) == 5 and sorted(ringe) == sorted(RINGE), str(sorted(ringe)))
    pruefe("Sumpftank: Rechteck 1125 x 2975 mm", all(out_teile[i]["art"] == "rechteck" and out_teile[i]["breite_mm"] == 1125 and out_teile[i]["hoehe_mm"] == 2975 for i in ("sump_1", "sump_2")))
    # Technikbereich: Teile unterhalb des Fischtank-Rands, die in der Zeichnung keinen Ring haben
    tech = [i for i in ("nursery", "feed", "vortex_1", "vortex_2", "bio_1", "bio_2", "sludge_1", "sludge_2", "sump_1", "sump_2", "filterpumpe_1", "filterpumpe_2", "hauptpumpe_1",
                        "hauptpumpe_2", "venturi_1", "venturi_2", "schwimmer_1", "schwimmer_2", "nachspeise", "permakultur") if i in out_teile]
    azs = [out_teile[i]["az_grad"] for i in tech if "az_grad" in out_teile[i]]
    return {"teile": out_teile, "ringe": ringe, "tech_ids": tech, "tech_az_min": min(azs), "tech_az_max": max(azs)}


def main():
    nur = "--pruefen" in sys.argv
    d = baue()
    meta = {
        "titel": "Soll-Lage der Draufsicht nach Leons Oasis-Showcase (L1, N-UNIFY-AUTOBAHN, D117: die Quelle ist die Wahrheit)",
        "erzeugt_von": "scripts/oasis_draufsicht.py (python -I -X utf8 scripts/oasis_draufsicht.py)",
        "quelle": {"datei": "docs/quellen/oasis-showcase-2026-11-10/index.html", "sha256": S.SHA["index.html"], "svg": "#mainSvg > g#soll-plan", "ansicht": "2D-Flussschema -> Draufsicht"},
        "umrechnung": {"mm_je_zeichnungseinheit": S.MM_JE_EINHEIT, "kuppelmitte_zeichnung": list(S.MITTE), "kuppel_radius_zeichnung": 480, "kuppel_radius_mm": S.KUPPEL_R_MM,
                       "drehung_grad": S.DREHUNG_GRAD, "x_modell_mm": "dx = (x-500)*12,5, dy = -(y-480)*12,5, dann um 18 Grad gegen den Uhrzeigersinn gedreht",
                       "gruppen_transform_ignoriert": "translate(107.5 86.7) scale(0.801) ist Seitenlayout, kein Mass"},
        "tuer_achse_az_grad": -72,
    }
    daten = {"meta": meta, "kuppel": {"radius_mm": S.KUPPEL_R_MM, "mitte_mm": [0, 0]}, **d, "pruefungen": PRUEF}
    s = json.dumps(daten, ensure_ascii=False, indent=1) + "\n"
    if not nur:
        with open(OUT, "w", encoding="utf-8", newline="\n") as f:
            f.write(s)
    bad = [p for p in PRUEF if not p["ok"]]
    for p in PRUEF:
        if not p["ok"]:
            print("FAIL %s  [%s]" % (p["pruefung"], p["detail"]))
    print("Teile %d, Ringe %d: %s" % (len(d["teile"]), len(d["ringe"]), ", ".join("%s r %.1f n %d" % (k, v["radius_mm"], v["stueckzahl"]) for k, v in d["ringe"].items())))
    print("Pruefungen: %d OK, %d FAIL%s" % (len(PRUEF) - len(bad), len(bad), "" if nur else "  -> " + os.path.relpath(OUT, ROOT)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
