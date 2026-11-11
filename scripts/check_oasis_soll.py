"""N-UNIFY-AUTOBAHN U1: misst die 16 Wasserspiegel des gebauten Modells gegen die Sollwerte der Quelle (+-50 mm) und prueft die Stufenreihenfolge.

Aufruf (Projektordner):
  python -I -X utf8 scripts/check_oasis_soll.py --liste                              die 16 Messpunkte mit Soll, Messart und Messbefehl (misst nichts)
  python -I -X utf8 scripts/check_oasis_soll.py --teil <becken|technik|ring|alle> [--variante ring_b2|a_plus]
  python -I -X utf8 scripts/check_oasis_soll.py --punkt <id> [--variante ring_b2]    ein Messpunkt (der Befehl steht in der Liste)
Exit 0: alle gewaehlten Punkte innerhalb +-50 mm und alle Stufen-Paare erfuellt; sonst Exit 1 (heute: Ausgangsmessung des Altmodells).

Sollwerte: data/oasis-soll.json `wasserspiegel_ueber_fussboden_mm` (Z-Bezug: Fussboden = Modell-Z 400, D94). Messvorschrift je Soll-ID: data/oasis-messung.json.
Ist: Instanz-Matrix aus dem Export (viewer/varianten/ring_b2/instances.json, Feld `built` nennt den Stand) + Koerper-Boxen aus viewer/detail/<komponente>.json
(lokale Boxen, nur lesen). Fehlt eine Komponente im Export (z. B. `sumpftank` vor U2), steht FEHLT; das gilt als Abweichung, nicht als Absturz.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLL = os.path.join(ROOT, "data", "oasis-soll.json")
MESS = os.path.join(ROOT, "data", "oasis-messung.json")
LAGE = os.path.join(ROOT, "data", "oasis-lage.json")
PARAMS = os.path.join(ROOT, "data", "params.json")
DETAIL = os.path.join(ROOT, "viewer", "detail")
TEIL_TITEL = {"becken": "Becken, Tische, Beete, Sumpf", "technik": "Vortex und Biofilter", "ring": "Wasserautobahn (Ring)"}


def load(p):
    return json.load(open(p, encoding="utf-8"))


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv and sys.argv.index(name) + 1 < len(sys.argv) else default


VARIANTE = arg("--variante", "ring_b2")
INST_PATH = os.path.join(ROOT, "viewer", "varianten", "ring_b2", "instances.json") if VARIANTE == "ring_b2" else os.path.join(ROOT, "viewer", "instances.json")


def detail_bodies(comp, fallback):
    for name in (comp, fallback, comp.replace("-ring_b2", ""), fallback.replace("-ring_b2", "")):
        p = os.path.join(DETAIL, name + ".json")
        if name and os.path.exists(p):
            return load(p)["koerper"]
    return None


def zrange(bodies, part):
    ks = [k for k in bodies if k["name"].startswith(part) or part in k["name"]]
    if not ks:
        return None
    return min(k["bbox"]["min"][2] for k in ks), max(k["bbox"]["max"][2] for k in ks)


def targets_for(ids):
    """Zielposition je Soll-ID: Bauplatz aus data/oasis-lage.json (U1), sonst Lage der gedrehten Zeichnung."""
    out = {}
    lage = {b["id"]: b for b in load(LAGE)["bauteile"]} if os.path.exists(LAGE) else {}
    soll = {b["id"]: b for b in load(SOLL)["bauteile"]}
    for i in ids:
        b = lage.get(i)
        if b and b.get("bauplatz"):
            out[i] = (b["bauplatz"]["x_mm"], b["bauplatz"]["y_mm"])
        elif soll[i]["lage"].get("mittelpunkt_x_mm") is not None:
            out[i] = (soll[i]["lage"]["mittelpunkt_x_mm"], soll[i]["lage"]["mittelpunkt_y_mm"])
    return out


def assign(insts, ids):
    """Zuordnung Instanzen -> Soll-IDs derselben Gruppe (vortex_1/_2, bio_1/_2, sump_1/_2) nach kleinster Gesamtentfernung."""
    tg = targets_for(ids)
    if len(insts) < len(ids):
        return {}
    import itertools
    best = None
    for perm in itertools.permutations(range(len(insts)), len(ids)):
        d = sum(math.hypot(insts[k]["m"][3] - tg[i][0], insts[k]["m"][7] - tg[i][1]) for k, i in zip(perm, ids))
        if best is None or d < best[0]:
            best = (d, perm)
    return {i: insts[k] for k, i in zip(best[1], ids)}


def measure(pt, instances, floor, soll_ids):
    """-> (Liste Ist-Werte ueber Fussboden in mm | None, Text)."""
    defs = pt["definition"].split("|")
    insts = [i for i in instances if i["d"] in defs]
    if not insts:
        return None, "FEHLT: Komponente `%s` nicht im Export" % pt["definition"]
    art = pt["art"]
    if art == "rohrachse":
        k = 1 if pt["zuordnung"] == "halbring_1" else 2
        sel = [i for i in insts if (-72 < math.degrees(math.atan2(i["m"][7], i["m"][3])) < 108) == (k == 1)]
        return [i["m"][11] - floor for i in sel], "%d Ring-Ecken, Rohrachse = Instanz-Z" % len(sel)
    bodies = detail_bodies(pt["definition"].split("|")[0], pt["detail"])
    if bodies is None:
        return None, "FEHLT: viewer/detail/%s.json (Koerper-Boxen) nicht vorhanden" % pt["detail"]
    zr = zrange(bodies, pt["koerper"])
    if zr is None:
        return None, "FEHLT: Koerper `%s` nicht in %s.json" % (pt["koerper"], pt["detail"])
    if pt["zuordnung"] == "naechste_lage":
        group = [i for i in soll_ids if i.rsplit("_", 1)[0] == pt["id"].rsplit("_", 1)[0]]
        sel = assign(insts, group).get(pt["id"])
        insts = [sel] if sel else []
        if not insts:
            return None, "FEHLT: weniger Instanzen als Soll-Teile (%s)" % ", ".join(group)
    elif pt["zuordnung"] == "einzeln":
        insts = insts[:1]
    P = MESSDATA["parameter"]
    vals = []
    for i in insts:
        z0 = i["m"][11]
        if art in ("koerper_oberkante", "standrohr_oberkante"):
            v = z0 + zr[1]
        elif art == "ueberlauf_mitte":
            v = z0 + (zr[0] + zr[1]) / 2
        elif art == "rinne_mitte_film":
            v = z0 + (zr[0] + zr[1] - P["nft_profilhoehe_mm"]) / 2 + P["nft_film_mm"]
        else:
            return None, "unbekannte Messart %s" % art
        vals.append(v - floor)
    return vals, "%d Instanz(en), Koerper `%s` Z %.0f..%.0f lokal" % (len(vals), pt["koerper"], zr[0], zr[1])


MESSDATA = load(MESS)


STUFEN_ZUSATZ = [["bio_1", "fish", "Stufe 4 > 0, Biofilter 1 ueber dem Fischtank (U5, Kette Vortex > Biofilter > Fischtank)"],
                 ["bio_2", "fish", "Stufe 4 > 0, Biofilter 2 ueber dem Fischtank"]]
# U5: Zaehlung der Technik im Export (Quelle: Technikgruppe der Oasis-Showcase, Paket n-unify-autobahn U5): (Beschriftung, Definitionen, Soll-Anzahl)
ZAEHLUNG_TECHNIK = [("Tauchpumpen (Pumpstelle 1 und 2)", ("tauchpumpe_modul",), 4), ("Venturi-Belueffter", ("venturi_belueffter",), 2),
                    ("Schwimmerschalter im Sumpf", ("schwimmerschalter_hochstand",), 2), ("Luftpumpen (2 Geblaese + Notluft)", ("geblaese_luft", "notluftpumpe"), 3),
                    ("Schlamm-Sammelbehaelter", ("schlamm_sammelbehaelter",), 2), ("Podeste Vortex", ("podest_vortex",), 2), ("Podeste Biofilter", ("podest_biofilter",), 2),
                    ("Luftverteiler (je 4 Arme)", ("luftverteiler_4",), 2), ("Nachspeise-Ventil", ("nachspeise_ventil",), 1), ("Regentank 5 m3", ("regentank_5m3",), 1),
                    ("Permakultur-Modul", ("permakultur_modul",), 1), ("Vortex (tank_klein)", ("tank_klein",), 2), ("Biofilter (tank_gross)", ("tank_gross", "tank_gross_t3"), 2)]
VERBOTEN_ALTBESTAND = ("feinfilter", "pumpe_klein", "pumpe_gross", "pegelschacht", "schlammfass")


def zaehlung_technik(instances):
    """U5: Anzahl je Definition im Export gegen die Soll-Zahl; Altbestand ohne Soll (D101) muss 0 sein. -> Anzahl Abweichungen."""
    import collections
    cnt = collections.Counter(i["d"].split("-ring_b2")[0] for i in instances)
    bad = 0
    print("Zaehlung der Technik im Export (Instanzen je Definition)")
    print("%-36s %5s %5s  %s" % ("Teil", "Soll", "Ist", "Urteil"))
    for name, defs, soll in ZAEHLUNG_TECHNIK:
        ist = sum(cnt.get(x, 0) for x in defs)
        bad += ist != soll
        print("%-36s %5d %5d  %s  (%s)" % (name, soll, ist, "OK" if ist == soll else "ABWEICHUNG", ", ".join(defs)))
    for pre in VERBOTEN_ALTBESTAND:
        ist = sum(n for k, n in cnt.items() if k.startswith(pre))
        bad += ist != 0
        print("%-36s %5d %5d  %s  (Altbestand ohne Soll, D101)" % ("entfallen: " + pre + "*", 0, ist, "OK" if ist == 0 else "ABWEICHUNG"))
    return bad


def komponenten_hoehen(soll):
    """U2 (Komponenten, nicht Gesamtmodell): Hoehenparameter der neuen Bauteile gegen die Soll-Datei. Gebaut als Komponente = 'Komponente ok';
    im Gesamtmodell sind sie erst nach U4/U5 -> 'ausstehend' (kein Fehler, aendert weder Exit-Code noch die Messung oben)."""
    def par(name):
        return {k: v["wert"] for k, v in load(os.path.join(ROOT, "data", "components", name + ".json"))["parameter"].items()}

    def h(i, k):
        return soll[i]["hoehen"][k]
    zeilen = []
    for nm, i, tank in (("podest_vortex", "vortex_1", 1323), ("podest_biofilter", "bio_1", 1570)):
        zeilen.append((nm, "%s_h Podesthoehe" % nm, par(nm)[nm + "_h"], h(i, "wsp_ueber_fussboden_mm") - tank, "Soll-Wsp %d minus Tank/Ueberlauf %d" % (h(i, "wsp_ueber_fussboden_mm"), tank)))
    s = par("sumpftank")
    zeilen += [("sumpftank", "Boden", -s["pit_d"], h("sump_1", "boden_ueber_fussboden_mm"), "sump_1"), ("sumpftank", "Soll-Pegel", s["wsp"], h("sump_1", "wsp_ueber_fussboden_mm"), "sump_1"),
               ("sumpftank", "Hochstand", s["hochstand"], h("sump_1", "hochstand_ueber_fussboden_mm"), "sump_1"),
               ("schwimmerschalter_hochstand", "Schaltpunkt", par("schwimmerschalter_hochstand")["schaltpunkt"], h("sump_1", "hochstand_ueber_fussboden_mm"), "schwimmer_1 = Hochstand Sumpf")]
    n = par("nachspeise_ventil")
    zeilen.append(("nachspeise_ventil", "Rohrachse ueber Spiegel", n["ventil_h"], h("fish", "rand_ueber_fussboden_mm") - h("fish", "wsp_ueber_fussboden_mm") + 60, "Rand - Wsp + 60"))
    zeilen.append(("notluftpumpe", "Schlauch-Schleife (>= Rand + 50)", par("notluftpumpe")["schleife_z"], h("fish", "rand_ueber_fussboden_mm") + 100, "Rand + 100"))
    zeilen.append(("venturi_belueffter", "Achse ueber Fischtank-Spiegel", par("venturi_belueffter")["achse_ueber_spiegel"], 1650 - 400 - h("fish", "wsp_ueber_fussboden_mm"), "Lage-Probe Modell-Z 1650 - Fussboden 400 - Wsp"))
    print("Komponenten (U2, Hoehenparameter der neuen Bauteile; Gesamtmodell ausstehend bis U4/U5, nicht Teil der Messung oben)")
    print("%-28s %-34s %8s %8s  %s" % ("Komponente", "Hoehenparameter", "Wert", "Soll", "Urteil"))
    for nm, was, ist, sl, why in zeilen:
        print("%-28s %-34s %8g %8g  %s (%s)" % (nm, was, ist, sl, "Komponente ok" if abs(ist - sl) < 1e-9 else "ABWEICHUNG Komponente", why))
    for nm in ("tauchpumpe_modul", "schlamm_sammelbehaelter", "regentank_5m3", "permakultur_modul"):
        print("%-28s %-34s %8s %8s  Komponente gebaut, Quelle legt keine Hoehe fest (stufe_status offen) / Hub aus Soll-Datei" % (nm, "-", "-", "-"))
    print("  Gesamtmodell: ausstehend (Komponenten in dome-ring_b2.sc erst ab U4/U5)")


def main():
    soll = {b["id"]: b for b in load(SOLL)["bauteile"]}
    tol = MESSDATA["toleranz_mm"]
    pts = MESSDATA["punkte"]
    for p in pts:
        p["soll_mm"] = soll[p["id"]]["wasserspiegel_ueber_fussboden_mm"]
        p["stufe"] = soll[p["id"]]["stufe"]
        p["befehl"] = "python -I -X utf8 scripts/check_oasis_soll.py --punkt %s --variante %s" % (p["id"], VARIANTE)
    if "--liste" in sys.argv:
        print("%d Messpunkte (Wasserspiegel ueber Fussboden, Z-Bezug 400, Toleranz +-%d mm)" % (len(pts), tol))
        for p in pts:
            print("%-10s Soll %5d mm  Stufe %d  Teil %-7s Messart %-20s Befehl: %s" % (p["id"], p["soll_mm"], p["stufe"], p["teil"], p["art"], p["befehl"]))
        return 0
    sel = pts
    if "--punkt" in sys.argv:
        sel = [p for p in pts if p["id"] == arg("--punkt")]
    elif "--teil" in sys.argv:
        t = arg("--teil", "alle")
        sel = pts if t == "alle" else [p for p in pts if p["teil"] == t or (t == "technik" and p["id"] == "fish")]   # U5: Fischtank als tiefste Stufe (0) der Technikkette mitmessen
        if t != "alle" and t not in TEIL_TITEL:
            print("unbekannter Teil %s (becken|technik|ring|alle)" % t)
            return 2
    else:
        print(__doc__)
        return 2
    d = load(INST_PATH)
    floor = float(load(PARAMS)["sock_h"]["value"])
    if d.get("walk_z", floor) != floor:
        print("WARNUNG: Fussboden params sock_h %s, Export walk_z %s" % (floor, d.get("walk_z")))
    print("Variante %s, Export %s (%d Instanzen), Fussboden Z %.0f, Toleranz +-%d mm" % (VARIANTE, d["built"], len(d["instances"]), floor, tol))
    print("%-10s %7s %9s %10s  %-10s %s" % ("Punkt", "Soll", "Ist", "Abweichung", "Urteil", "Messung"))
    ist, bad = {}, 0
    all_ids = [p["id"] for p in pts]
    for p in sel:
        vals, txt = measure(p, d["instances"], floor, all_ids)
        if not vals:
            print("%-10s %7d %9s %10s  %-10s %s" % (p["id"], p["soll_mm"], "-", "-", "FEHLT", txt))
            bad += 1
            continue
        mean = sum(vals) / len(vals)
        worst = max(vals, key=lambda v: abs(v - p["soll_mm"]))
        dev = worst - p["soll_mm"]
        ist[p["id"]] = mean
        ok = abs(dev) <= tol
        bad += 0 if ok else 1
        spread = "" if len(vals) == 1 else ", Streuung %.0f" % (max(vals) - min(vals))
        print("%-10s %7d %9.0f %+10.0f  %-10s %s%s" % (p["id"], p["soll_mm"], mean, mean - p["soll_mm"], "OK" if ok else "ABWEICHUNG", txt, spread))
    pairs = [q for q in MESSDATA["stufen_reihenfolge"]["paare"] + STUFEN_ZUSATZ if q[0] in [p["id"] for p in sel] and q[1] in [p["id"] for p in sel]]
    print("Stufenreihenfolge (Wasserspiegel faellt entlang der Wege der Quelle), %d Paare im gewaehlten Umfang" % len(pairs))
    for hi, lo, why in pairs:
        if hi in ist and lo in ist:
            ok = ist[hi] > ist[lo]
            bad += 0 if ok else 1
            print("  %-10s > %-10s Ist %6.0f > %6.0f  %-9s (%s)" % (hi, lo, ist[hi], ist[lo], "OK" if ok else "VERLETZT", why))
        else:
            bad += 1
            print("  %-10s > %-10s nicht pruefbar (Messwert fehlt)  (%s)" % (hi, lo, why))
    if arg("--teil", "") in ("technik", "alle"):
        bad += zaehlung_technik(d["instances"])
        komponenten_hoehen(soll)
    print("ERGEBNIS: %s (%d Abweichungen oder fehlende Werte)" % ("BESTANDEN" if not bad else "ABWEICHUNG", bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
