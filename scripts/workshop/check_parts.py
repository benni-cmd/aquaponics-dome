"""Pruefung der Teiledaten (N-DETAIL-PILOT): data/parts/<komponente>.json gegen das .sc und data/katalog.json.
Aufruf: python -X utf8 scripts/workshop/check_parts.py feinfilter tank_klein
Pruefsatz: jeder Koerper des .sc steht in genau einer Teilezeile; Menge = Zahl der Koerpernamen; keine Namen der Form Body<n>."""
import sys, os, json, re
sys.path.insert(0, os.path.dirname(__file__))
import sc

TYPEN = {"profil", "platte", "rohr", "normteil", "kaufteil", "sonderteil"}
KONF = {"belegt", "gerechnet", "angenommen"}
LEBENSMITTEL = {"ja", "nein", "offen"}
PFLICHT = ("id", "name", "koerper", "menge", "typ", "werkstoff", "masse_mm", "funktion", "eigenschaften", "norm", "norm_konfidenz",
           "lebensmittelkontakt", "lebensmittelkontakt_konfidenz", "konfidenz", "quelle")

def leer(v):
    return v is None or (isinstance(v, (str, list)) and len(v) == 0)

def explosion_ok(t, ids):
    ex = t.get("explosion")
    if ex is None:
        return True
    r = ex.get("richtung")
    ok_r = r == "radial" or (isinstance(r, list) and len(r) == 3 and all(isinstance(x, (int, float)) for x in r) and any(r))
    ok_a = isinstance(ex.get("abstand_mm"), (int, float))
    f = ex.get("folgt")
    return ok_r and ok_a and (f is None or (f in ids and f != t["id"]))

def folgt_zyklus(teile):
    nxt = {t["id"]: (t.get("explosion") or {}).get("folgt") for t in teile}
    for start in nxt:
        seen, cur = set(), start
        while cur is not None:
            if cur in seen:
                return start
            seen.add(cur)
            cur = nxt.get(cur)
    return None

def main(komps):
    kat = json.load(open(os.path.join(sc.ROOT, "data", "katalog.json"), encoding="utf-8"))
    werk = {w["id"]: w for w in kat["werkstoffe"]}
    kat_ids = {e["id"] for k in ("werkstoffe", "profile", "rohre", "normteile") for e in kat[k]}
    sc_zu_werk = {m: w["id"] for w in kat["werkstoffe"] for m in w.get("sc_material", [])}
    rc = 0
    for komp in komps:
        d = json.load(open(os.path.join(sc.ROOT, "data", "parts", komp + ".json"), encoding="utf-8"))
        ck = sc.Check("parts " + komp)
        path = os.path.join(sc.ROOT, d["datei"])
        ev = sc.evaluate(path)
        bodies = {b["name"]: b for b in ev["bodies"]}
        teile = d["teile"]
        ids = [t["id"] for t in teile]
        zeile = {}
        doppelt = []
        for t in teile:
            for k in t["koerper"]:
                if k in zeile:
                    doppelt.append(k)
                zeile[k] = t["id"]
        print(f"{komp}: {len(bodies)} Koerper im .sc, {len(teile)} Teile, Kopf koerperzahl {d['koerperzahl']}")
        ck.eq("Koerper im .sc (eval)", len(bodies), d["koerperzahl"])
        ck.eq("Summe der Koerper je Teilezeile", sum(len(t["koerper"]) for t in teile), len(bodies))
        ck.eq("Koerper des .sc ohne Teilezeile", len([n for n in bodies if n not in zeile]), 0)
        ck.eq("Koerpernamen in Teilezeilen, die es im .sc nicht gibt", len([n for n in zeile if n not in bodies]), 0)
        ck.eq("Koerpername in mehr als einer Teilezeile (oder doppelt)", len(doppelt), 0)
        ck.eq("Namen der Form Body<Zahl> im .sc", len([n for n in bodies if re.fullmatch(r"Body\d+", n)]), 0)
        ck.eq("Teil-IDs doppelt", len(ids) - len(set(ids)), 0)
        ck.eq("menge ungleich Laenge von koerper", len([t for t in teile if t["menge"] != len(t["koerper"])]), 0)
        ck.eq("Teile mit leerem Pflichtfeld", len([t for t in teile if any(leer(t.get(f)) for f in PFLICHT)]), 0)
        ck.eq("Teile mit unbekanntem typ", len([t for t in teile if t["typ"] not in TYPEN]), 0)
        ck.eq("Teile mit unbekannter konfidenz", len([t for t in teile if t["konfidenz"] not in KONF or t["norm_konfidenz"] not in KONF or t["lebensmittelkontakt_konfidenz"] not in KONF]), 0)
        ck.eq("Teile mit lebensmittelkontakt ausser ja/nein/offen", len([t for t in teile if t["lebensmittelkontakt"] not in LEBENSMITTEL]), 0)
        ck.eq("Teile mit Werkstoff ausserhalb des Katalogs", len([t for t in teile if t["werkstoff"] not in werk]), 0)
        ck.eq("katalog-Verweise ohne Eintrag", len([t for t in teile if t.get("katalog") and t["katalog"] not in kat_ids]), 0)
        ck.eq("Normteil/Kaufteil ohne bezug (D76)", len([t for t in teile if t["typ"] in ("normteil", "kaufteil") and leer(t.get("bezug"))]), 0)
        falsch = [(k, b["material"]) for t in teile for k in t["koerper"] if k in bodies for b in [bodies[k]] if sc_zu_werk.get(b["material"]) != t["werkstoff"]]
        for x in falsch[:5]:
            print("   Werkstoff-Abweichung (Koerper, .sc-Material):", x)
        ck.eq("Koerper, deren .sc-Material nicht zum Werkstoff der Zeile passt", len(falsch), 0)
        ck.eq("explosion fehlerhaft (richtung, abstand_mm, folgt)", len([t for t in teile if not explosion_ok(t, ids)]), 0)
        ck.eq("folgt-Kette mit Zyklus", 0 if folgt_zyklus(teile) is None else 1, 0)
        in_gruppen = [i for g in d["gruppen"] for i in g["teile"]]
        ck.eq("Teile ohne Gruppe oder in mehreren Gruppen", len(set(ids) ^ set(in_gruppen)) + len(in_gruppen) - len(set(in_gruppen)), 0)
        rc |= ck.done()
    return rc

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Aufruf: check_parts.py <komponente>...")
    sys.exit(main(sys.argv[1:]))
