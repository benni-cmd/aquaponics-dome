"""N-STUECKLISTE 1c: Test der Stueckliste (Pruefpunkte 1 bis 4 des Blatts docs/jobs/N-STUECKLISTE.md).

Aufruf:
  python -X utf8 scripts/check_bom.py            # Exit 0 = alle Pruefungen PASS; Stichprobe 6 Komponenten live per solidcraft-cli
  python -X utf8 scripts/check_bom.py --live-alle  # Massen-Gegenprobe ueber alle .sc (rund 15 min)
  python -X utf8 scripts/check_bom.py --ohne-live  # ohne CLI-Gegenprobe

Liest data/stueckliste.json (erzeugt von scripts/bom.py), viewer/instances.json, data/bom_koerper.json, data/katalog.json.
Determinismus und Aenderungstest laufen in einer Kopie im Temp-Ordner (BOM_ROOT), das Repo bleibt unveraendert.
"""
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import bom as BOM  # noqa: E402
import bom_artikel as BA  # noqa: E402
import bom_benennung as BN  # noqa: E402

ERG = []


def check(nr, text, ok, detail=""):
    ERG.append((nr, text, bool(ok), detail))
    print(("PASS " if ok else "FAIL ") + f"{nr:>2} {text}" + (f"  [{detail}]" if detail else ""))


def jl(p):
    return json.load(open(p, encoding="utf-8"))


def hash_ohne_stempel(pfad):
    d = jl(pfad)
    d["kopf"].pop("modell_aktuell", None)
    d["kopf"].pop("drift", None)
    return hashlib.sha256(json.dumps(d, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def kopie_anlegen(tmp):
    for rel in ("data/bom_koerper.json", "data/katalog.json", "data/bom_regeln.json", "viewer/instances.json"):
        os.makedirs(os.path.join(tmp, os.path.dirname(rel)), exist_ok=True)
        shutil.copy(os.path.join(ROOT, rel), os.path.join(tmp, rel))
    shutil.copytree(os.path.join(ROOT, "data", "beschaffung"), os.path.join(tmp, "data", "beschaffung"))
    os.makedirs(os.path.join(tmp, "docs"), exist_ok=True)
    os.makedirs(os.path.join(tmp, "designs", "components"), exist_ok=True)


def main():
    sl = jl(os.path.join(ROOT, "data", "stueckliste.json"))
    inst = jl(BA.INST)
    cache = jl(BA.CACHE)
    kat = jl(BA.KATALOG)
    zeilen = sl["zeilen"]
    komp = {k["komponente"]: k for k in sl["komponenten"]}

    # ---- Punkt 1: Zaehlung
    n_inst_json = len(inst["instances"])
    je_def = Counter(i["d"] for i in inst["instances"])
    check(1, "Instanzen in der Stueckliste = Instanzen in viewer/instances.json", sl["kopf"]["instanzen"] == n_inst_json, f"{sl['kopf']['instanzen']} vs {n_inst_json}")
    diff = {d: (je_def[d], komp.get(d, {}).get("instanzen")) for d in je_def if komp.get(d, {}).get("instanzen") != je_def[d]}
    check(2, "Instanzen je Definition: Differenz 0", not diff, f"{len(je_def)} Definitionen, Abweichungen {list(diff.items())[:3]}")
    # Mengen je Zeile = Summe Instanzen x Menge je Instanz (unabhaengige Neurechnung aus verwendung)
    bad = []
    for z in zeilen:
        s = sum(u["instanzen"] * u["menge_je_instanz"] for u in z["verwendung"])
        if abs(s - z["bedarf"]) > 0.001 * max(1, abs(s)):
            bad.append(z["artikel_id"])
        for u in z["verwendung"]:
            if je_def.get(u["komponente"], 0) != u["instanzen"]:
                bad.append(z["artikel_id"] + ":" + u["komponente"])
    check(3, "Bedarf je Zeile = Summe (Instanzen x Menge je Instanz)", not bad, str(bad[:3]))
    # Masse: Summe aller Koerper (Cache x Instanzen) = gelistet + Ausnahmen + ungeklaert (Toleranz 0,5 %)
    m_cache = sum(sum(b["mass_g"] for b in v["bodies"]) * je_def.get(c, 0) for c, v in cache["komponenten"].items()) / 1000.0
    m_zeilen = sum(z["masse_kg"] for z in zeilen)
    m_ausn = sum(v["masse_kg"] for v in sl["ausnahmen"].values())
    m_ung = sum(k["masse_kg_ungeklaert"] * k["instanzen"] for k in sl["komponenten"])
    rest = abs(m_cache - (m_zeilen + m_ausn + m_ung)) / max(m_cache, 1)
    check(4, "Masse Cache = Zeilen + Ausnahmen + ungeklaert (0,5 %)", rest <= 0.005, f"{m_cache:.1f} kg vs {m_zeilen + m_ausn + m_ung:.1f} kg, Abw. {rest * 100:.3f} %")
    # Live-Gegenprobe gegen solidcraft-cli eval
    if "--ohne-live" not in sys.argv and os.path.exists(BA.CLI):
        alle = sorted(cache["komponenten"])
        if "--live-alle" in sys.argv:
            probe = alle
        else:
            wunsch = ["feinfilter", "tank_klein", "pumpe_klein", "winkelhalter", "lt_rohr_d63_L1000" if "lt_rohr_d63_L1000" in alle else None, "sonde_ph", "strebe_a", "knoten_4"]
            probe = [c for c in wunsch if c and c in cache["komponenten"]][:6]
        tmp = tempfile.mkdtemp()
        abw = []
        for c in probe:
            out = os.path.join(tmp, c + ".json")
            subprocess.run([BA.CLI, "eval", os.path.join(BA.COMP_DIR, c + ".sc"), "--json-out", out], capture_output=True, text=True)
            if not os.path.exists(out):
                abw.append((c, "eval ohne Ausgabe"))
                continue
            live = sum(b.get("mass_g") or 0 for b in jl(out).get("bodies", []))
            alt = sum(b["mass_g"] for b in cache["komponenten"][c]["bodies"])
            if abs(live - alt) > 0.005 * max(alt, 1):
                abw.append((c, round(live, 1), round(alt, 1)))
        shutil.rmtree(tmp, ignore_errors=True)
        check(5, f"Masse live (solidcraft-cli eval) = Cache, {len(probe)} Komponenten (0,5 %)", not abw, str(abw[:3]))
    # ---- Punkt 2: Vollstaendigkeit
    check(6, "ungeklaerte Koerper: 0", not sl["ungeklaert"], str(sl["ungeklaert"][:2]))
    unben = 0
    for c, v in cache["komponenten"].items():
        for b in v["bodies"]:
            if BN.ist_unbenannt(b["name"]):
                a, ex = BA.zuordnen(c, b)
                if a is None and not ex:
                    unben += 1
    check(7, "unbenannte Koerper ohne Regel (Body<n>): 0", unben == 0, f"{sl['kopf']['unbenannte_koerper_im_cache']} im Cache, {sl['kopf']['name_vergeben_summe']} per Regel benannt (je Instanz gezaehlt)")
    fehlt = []
    ausn_komp = {"salatkopf", "erdflaeche", "fundamentring"}
    kopf_komp = {z["komponente"] for z in sl["zeilen"] for z in z["verwendung"]}
    for d in je_def:
        if d not in kopf_komp and not (d in ausn_komp or d.startswith("mensch_referenz")):
            # Komponente nur aus Ausnahme-Koerpern?
            if komp.get(d, {}).get("masse_kg_gelistet", 0) > 0:
                fehlt.append(d)
            elif d not in komp:
                fehlt.append(d)
    check(8, "jede Komponente aus instances.json in der Liste oder Ausnahmeliste", not fehlt, str(fehlt[:5]))
    kein_typ = [z["artikel_id"] for z in zeilen if z["typ"] not in kat["typen"]]
    check(9, "Zeilen ohne Typ-Kuerzel aus der Typliste: 0", not kein_typ, str(kein_typ[:3]))
    check(10, "Komponenten ohne Bauteilgruppe: 0", not sl["komponenten_ohne_gruppe"], str(sl["komponenten_ohne_gruppe"][:3]))
    # ---- Punkt 3: Preiszeilen
    leer = []
    for z in zeilen:
        p = z["preis"]
        if p is not None:
            for f in ("stand", "haendler", "land", "url", "konfidenz", "einzelpreis_eur", "gesamtpreis_eur"):
                if p.get(f) in (None, ""):
                    leer.append((z["artikel_id"], f))
            if p.get("land") not in BOM.EUROPA:
                leer.append((z["artikel_id"], "land " + str(p.get("land"))))
        else:
            if not str(z["status"]).startswith("OFFEN") or not z.get("status_grund"):
                leer.append((z["artikel_id"], "OFFEN ohne Grund"))
    check(11, "Preiszeilen: Preis mit allen Feldern in Europa oder OFFEN mit Grund (leere Felder 0)", not leer, str(leer[:4]))
    # ---- Punkt 4: Determinismus in einer Kopie (BOM_ROOT); das Repo wird nicht geschrieben (Auflage A2)
    tmp = tempfile.mkdtemp()
    try:
        kopie_anlegen(tmp)
        hs = []
        for _ in range(2):
            subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "bom.py")], env=dict(os.environ, BOM_ROOT=tmp), capture_output=True, text=True)
            hs.append(hash_ohne_stempel(os.path.join(tmp, "data", "stueckliste.json")))
        gleich_repo = jl(os.path.join(tmp, "data", "stueckliste.json"))["zeilen"] == sl["zeilen"]
        check(12, "Determinismus: bom.py zweimal in einer Kopie, sha256 data/stueckliste.json (ohne Drift-Stempel) gleich", hs[0] == hs[1], hs[0][:12] + (", Zeilen = Repo" if gleich_repo else ", Zeilen weichen vom Repo ab (Modelldrift oder Liste nicht neu erzeugt)"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    aenderungstest()
    nf = [e for e in ERG if not e[2]]
    print(f"\n{len(ERG) - len(nf)} von {len(ERG)} Pruefungen PASS")
    sys.exit(1 if nf else 0)


def aenderungstest():
    tmp = tempfile.mkdtemp()
    try:
        kopie_anlegen(tmp)
        cache = jl(os.path.join(tmp, "data", "bom_koerper.json"))
        inst = Counter(i["d"] for i in jl(os.path.join(tmp, "viewer", "instances.json"))["instances"])
        kandidaten = [c for c, v in sorted(cache["komponenten"].items()) if c.startswith("lt_rohr_d") and inst.get(c, 0) > 0]
        alt = jl(os.path.join(ROOT, "data", "stueckliste.json"))
        orig = json.dumps(cache)

        def lauf(ziel, plus_mm):
            c2 = json.loads(orig)
            bb = max(c2["komponenten"][ziel]["bodies"], key=lambda x: x["mass_g"])
            bb["bbox_max"][2] += plus_mm
            json.dump(c2, open(os.path.join(tmp, "data", "bom_koerper.json"), "w", encoding="utf-8"), ensure_ascii=False)
            r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "bom.py")], env=dict(os.environ, BOM_ROOT=tmp), capture_output=True, text=True)
            neu = jl(os.path.join(tmp, "data", "stueckliste.json"))
            aid = "ROH-pvcu-d%d" % int(re.match(r"lt_rohr_d(\d+)", ziel).group(1))
            return r.returncode == 0, aid, next(z for z in alt["zeilen"] if z["artikel_id"] == aid), next(z for z in neu["zeilen"] if z["artikel_id"] == aid), neu

        ziel = kandidaten[0]
        ok, aid, za, zn, neu = lauf(ziel, 100.0)
        erwartet = round(inst[ziel] * 0.1, 3)
        check(13, f"Aenderungstest A: {ziel} +100 mm (Kopie) -> Bedarf {aid} +{erwartet} m", ok and abs((zn["bedarf"] - za["bedarf"]) - erwartet) < 0.002 and zn["kauf"]["bedarf_m"] > za["kauf"]["bedarf_m"],
              f"Bedarf {za['bedarf']} -> {zn['bedarf']}, Kauf {za['kauf'].get('kauf_menge')} -> {zn['kauf'].get('kauf_menge')} (Stangen gerundet)")
        # B: genug Zusatzlaenge, dass eine Stange mehr gekauft wird -> Summe steigt
        ziel = next(c for c in kandidaten if next((z for z in alt["zeilen"] if z["artikel_id"] == "ROH-pvcu-d%d" % int(re.match(r"lt_rohr_d(\d+)", c).group(1))), {}).get("preis"))
        za0 = next(z for z in alt["zeilen"] if z["artikel_id"] == "ROH-pvcu-d%d" % int(re.match(r"lt_rohr_d(\d+)", ziel).group(1)))
        plus = (za0["kauf"]["kauf_menge"] - za0["bedarf"] + 0.5) / inst[ziel] * 1000.0
        ok, aid, za, zn, neu = lauf(ziel, plus)
        check(14, f"Aenderungstest B: {ziel} +{plus:.0f} mm (Kopie) -> Kaufmenge und Summe steigen ohne weiteren Eingriff",
              ok and zn["kauf"]["kauf_menge"] > za["kauf"]["kauf_menge"] and neu["kopf"]["summe_eur_platziert"] > alt["kopf"]["summe_eur_platziert"],
              f"Kauf {za['kauf'].get('kauf_menge')} -> {zn['kauf'].get('kauf_menge')} m, Summe {alt['kopf']['summe_eur_platziert']} -> {neu['kopf']['summe_eur_platziert']}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
