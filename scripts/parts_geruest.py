"""W60 Schritt 5-0: Teile-Geruest data/parts/<komp>.json fuer alle Komponenten (nutzt scripts/bom.py und bom_artikel.py).

Aufruf:
  python -X utf8 scripts/parts_geruest.py            # schreibt data/parts/<komp>.json fuer jede Komponente im Messcache
  python -X utf8 scripts/parts_geruest.py --stdout   # nur Kurzbericht

Quellen (nur lesen): data/bom_koerper.json (Koerper je Komponente), data/bom_regeln.json (Gruppen, Benennung),
                     data/katalog.json und data/stueckliste.json (Artikel-IDs muessen dort stehen).
Regel: Deterministisch (kein Zeitstempel). Handgepflegte Felder (alles ausser den Auto-Feldern, plus Gruppen)
werden nie ueberschrieben. Dateien ohne Marker `geruest` im Teil (Pilot: feinfilter, tank_klein) bekommen NUR `artikel_id`
(und artikel_ids bei Mischung) ergaenzt. Teile mit `geruest: true` gehoeren dem Geruest, bis 5a die Erklaertexte
ausgefuellt und den Marker entfernt hat.
"""
import json
import os
import re
import sys
from collections import OrderedDict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bom_artikel as BA  # noqa: E402
import bom_benennung as BN  # noqa: E402
import bom as BOM  # noqa: E402

ROOT = BA.ROOT
PARTS = os.path.join(ROOT, "data", "parts")

AUTO = ("id", "name", "koerper", "menge", "typ", "werkstoff", "masse_mm", "artikel_id", "artikel_einheit",
        "artikel_menge_je_instanz", "ausnahme", "geruest")
TYP_VON_ARTIKEL = {"PRF": "profil", "WNK": "profil", "BLE": "platte", "ROH": "rohr", "SRB": "normteil", "FIT": "kaufteil",
                   "ARM": "kaufteil", "SCH": "kaufteil", "BEH": "kaufteil", "PMP": "kaufteil", "MES": "kaufteil",
                   "ELE": "kaufteil", "FOL": "kaufteil", "GEW": "kaufteil", "TOP": "kaufteil", "SON": "sonderteil", "BET": "sonderteil"}
GRUPPE_VON_TYP = {"PRF": "Stahl- und Alu-Profile", "WNK": "Winkel, Flachstahl, Halter", "BLE": "Bleche und Platten", "ROH": "Rohre",
                  "FIT": "Fittings", "ARM": "Armaturen", "SCH": "Schlauch und Schellen", "SRB": "Schrauben",
                  "BEH": "Behaelter und Becken", "PMP": "Pumpen", "MES": "Messtechnik", "ELE": "Elektrik", "FOL": "Folien und Dichtungen",
                  "GEW": "Gewebe", "TOP": "Toepfe und Substrat", "SON": "Sonderteile (Eigenbau)", "BET": "Beton", None: "Nicht kaufbar (Ausnahme)"}


def stamm(name):
    """Gruppierschluessel eines Koerpernamens: Zahlen, Klammern und Eckenbuchstaben nach Zahl entfernen."""
    s = re.sub(r" \(\d+\)", "", name or "")
    s = re.sub(r"\d+[A-Za-z]?(?=_|$)", "", s)
    s = re.sub(r"(?<=[A-Za-z])\d+[A-Za-z]?$", "", s)
    s = re.sub(r"_+", "_", s).strip("_ ")
    return s or (name or "teil")


def slug(s):
    t = (s or "").lower()
    for a, b in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("ß", "ss")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_") or "teil"


def dims(b):
    return sorted(round(b["bbox_max"][i] - b["bbox_min"][i], 1) for i in range(3))


def koerper_artikel(comp, v):
    """je Koerper (Reihenfolge wie im .sc): (Koerper, Art|None, zaehlt, ausnahme|None) - spiegelt bom.komp_artikel"""
    res = []
    lt = comp.startswith("lt_")
    lt_art = None
    if lt:
        benannte = [b for b in v["bodies"] if not BN.ist_unbenannt(b["name"])]
        lt_art = BA.classify_lt(comp, benannte or v["bodies"])
    first = True
    for b in v["bodies"]:
        if lt and lt_art and not BN.ist_unbenannt(b["name"]):
            res.append((b, lt_art, first, None))
            first = False
            continue
        a, ex = BA.zuordnen(comp, b)
        if ex:
            res.append((b, None, False, ex))
        elif a is None:
            res.append((b, None, False, "ungeklaert"))
        else:
            res.append((b, a, not a.teil_von, None))
    return res


def bauteile(comp, v):
    """Koerper -> Teile (Gruppierung nach Namensstamm und Artikel)"""
    teile = OrderedDict()
    for b, a, zaehlt, ex in koerper_artikel(comp, v):
        unb = BN.ist_unbenannt(b["name"])
        bn = BN.benenne(comp, b) if unb else None
        sta = bn["name"] if bn else stamm(b["name"])
        if unb and not bn:
            sta = "unbenannt"
        aid = a.id if a else None
        key = (sta, aid, ex)
        t = teile.setdefault(key, {"stamm": sta, "art": a, "ex": ex, "koerper": [], "bodies": [], "menge": 0.0, "mass": 0.0})
        t["koerper"].append(b["name"])
        t["bodies"].append(b)
        t["mass"] += b["mass_g"]
        if zaehlt and a:
            t["menge"] += a.menge
    return list(teile.values())


def teil_zeile(t, benutzte):
    a = t["art"]
    base = slug(t["stamm"])
    tid = base
    if tid in benutzte:
        tid = f"{base}_{slug(a.id) if a else 'ausnahme'}"
        n = 2
        while tid in benutzte:
            tid = f"{base}_{n}"
            n += 1
    benutzte.add(tid)
    d = dims(t["bodies"][0])
    typ = TYP_VON_ARTIKEL.get(a.typ) if a else "sonderteil"
    masse = f"Masse {round(sum(b['mass_g'] for b in t['bodies']), 1)} g, Einzelkoerper {d[0]} x {d[1]} x {d[2]} mm (Modell-Bounding-Box)"
    werk = sorted({b["material"] for b in t["bodies"]})
    z = OrderedDict()
    z["id"] = tid
    z["name"] = t["stamm"].replace("_", " ")
    z["koerper"] = list(t["koerper"])
    z["menge"] = len(t["koerper"])
    z["typ"] = typ
    z["werkstoff"] = werk[0] if len(werk) == 1 else " / ".join(werk)
    z["masse_mm"] = masse
    z["artikel_id"] = a.id if a else None
    z["artikel_einheit"] = a.einheit if a else None
    z["artikel_menge_je_instanz"] = round(t["menge"], 4) if a else 0
    if t["ex"]:
        z["ausnahme"] = t["ex"]
    z["geruest"] = True
    return z


def bauen(comp, v, bg):
    teile, benutzt = [], set()
    for t in bauteile(comp, v):
        teile.append(teil_zeile(t, benutzt))
    gruppen = OrderedDict()
    art_typ = {t["id"]: (t["artikel_id"].split("-")[0] if t["artikel_id"] else None) for t in teile}
    for t in teile:
        gruppen.setdefault(GRUPPE_VON_TYP.get(art_typ[t["id"]], "Sonstige"), []).append(t["id"])
    gl = [{"id": slug(n), "name": n, "kurz": "", "teile": ids} for n, ids in gruppen.items()]
    return teile, gl


def zusammenfuehren(comp, v, bg, prev):
    """Pilotdatei (kein geruest-Marker): nur artikel_id ergaenzen. Sonst: Geruest neu, Handfelder bleiben."""
    teile_neu, gruppen_neu = bauen(comp, v, bg)
    bodies_art = {}
    for b, a, zaehlt, ex in koerper_artikel(comp, v):
        bodies_art[b["name"]] = (a.id if a else None, zaehlt)
    head = OrderedDict()
    if prev:
        head.update(prev)
        if not any(t.get("geruest") for t in prev.get("teile", [])) and prev.get("stand") != "geruest":
            # reine Pilotdatei
            for t in prev["teile"]:
                ids = [bodies_art[k][0] for k in t["koerper"] if k in bodies_art]
                zahl = [bodies_art[k][0] for k in t["koerper"] if k in bodies_art and bodies_art[k][1]]
                uniq = []
                for x in (zahl or ids):
                    if x not in uniq:
                        uniq.append(x)
                cand = [x for x in uniq if x]
                t["artikel_id"] = cand[0] if cand else None
                if len(cand) > 1:
                    t["artikel_ids"] = cand
            return prev
    # Geruest (neu oder erneuert)
    prev_teile = {t["id"]: t for t in (prev or {}).get("teile", [])}
    teile = []
    for t in teile_neu:
        p = prev_teile.get(t["id"])
        z = OrderedDict(t)
        if p:
            for k, val in p.items():
                if k not in AUTO:
                    z[k] = val
            if not p.get("geruest"):
                z.pop("geruest", None)
        teile.append(z)
    d = OrderedDict()
    d["komponente"] = comp
    d["datei"] = f"designs/components/{comp}.sc"
    d["bauteilgruppe"] = bg
    d["teilenummer"] = (prev or {}).get("teilenummer", "")
    d["stand"] = (prev or {}).get("stand", "geruest")
    d["titel"] = (prev or {}).get("titel", comp.replace("_", " "))
    d["kurz"] = (prev or {}).get("kurz", "")
    d["hinweis"] = (prev or {}).get("hinweis", "Geruest aus scripts/parts_geruest.py (W60 5-0): Koerper, Typ, artikel_id, Menge automatisch; Funktion, Erklaertext, Explosion und Gruppen folgen in 5a. Teile mit geruest: true sind noch nicht ausgefuellt.")
    d["koerperzahl"] = len(v["bodies"])
    d["gruppen"] = prev["gruppen"] if prev and prev.get("stand") != "geruest" and prev.get("gruppen") else gruppen_neu
    d["teile"] = teile
    return d


def main():
    nur_bericht = "--stdout" in sys.argv
    cache = json.load(open(BA.CACHE, encoding="utf-8"))
    regeln = json.load(open(os.path.join(ROOT, "data", "bom_regeln.json"), encoding="utf-8"))
    kat = {a["id"] for a in json.load(open(BA.KATALOG, encoding="utf-8"))["artikel"]}
    stl = {z["artikel_id"] for z in json.load(open(os.path.join(ROOT, "data", "stueckliste.json"), encoding="utf-8"))["zeilen"]}
    os.makedirs(PARTS, exist_ok=True)
    fehl_kat, fehl_stl, zahl, teile_n, korper_n = 0, 0, 0, 0, 0
    ohne_art = 0
    for comp, v in cache["komponenten"].items():
        if not v["bodies"]:
            continue
        bg = BOM.gruppe_von(comp, regeln)
        pfad = os.path.join(PARTS, comp + ".json")
        prev = json.load(open(pfad, encoding="utf-8"), object_pairs_hook=OrderedDict) if os.path.exists(pfad) else None
        d = zusammenfuehren(comp, v, bg, prev)
        for t in d["teile"]:
            a = t.get("artikel_id")
            for x in ([a] + t.get("artikel_ids", [])) if a else []:
                fehl_kat += x not in kat
                fehl_stl += x not in stl
            ohne_art += a is None
        zahl += 1
        teile_n += len(d["teile"])
        korper_n += d["koerperzahl"]
        if not nur_bericht:
            with open(pfad, "w", encoding="utf-8", newline="\n") as f:
                f.write(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    print(f"Komponenten {zahl}, Koerper {korper_n}, Teile {teile_n}, Teile ohne artikel_id (Ausnahme/ungeklaert) {ohne_art}, "
          f"artikel_id nicht im Katalog {fehl_kat}, nicht in stueckliste.json {fehl_stl}")


if __name__ == "__main__":
    main()
