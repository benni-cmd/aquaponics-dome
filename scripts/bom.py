"""N-STUECKLISTE 1c/1d: Stueckliste aus dem Modellstand (Zaehlung, Zuschnitt, Preis-Zusammenfuehrung).

Aufruf:
  python -X utf8 scripts/bom.py            # schreibt data/stueckliste.json und docs/stueckliste.md
  python -X utf8 scripts/bom.py --stdout   # nur Kurzbericht, schreibt nichts

Eingaben (nur lesen):
  data/bom_koerper.json     Messcache der Koerper je Komponente (scripts/bom_artikel.py --ergaenzen)
  viewer/instances.json     Instanzen je Definition (Zaehlung)
  data/katalog.json         Artikelliste (erzeugt von scripts/bom_artikel.py)
  data/bom_regeln.json      Namensregeln, Gruppen, Zuschnitt, Aufschlag, Preis-Aliase
  data/beschaffung/*.json   Preise und Links der Recherche (Paket 2) - wird NIE geschrieben
Ausgaben (erzeugt, nie von Hand): data/stueckliste.json, docs/stueckliste.md

Regel W45: gleiche Eingabe, gleiche Ausgabe (kein Zeitstempel der Laufzeit; Stempel kommt aus dem Modellstand).
Die Zuordnung Koerper -> Artikel nutzt die getesteten Namensregeln aus scripts/bom_artikel.py (zuordnen, classify_lt).
"""
import glob
import json
import math
import os
import re
import sys
from collections import OrderedDict, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bom_artikel as BA  # noqa: E402
import bom_benennung as BN  # noqa: E402

ROOT = BA.ROOT
OUT_JSON = os.path.join(ROOT, "data", "stueckliste.json")
OUT_MD = os.path.join(ROOT, "docs", "stueckliste.md")
BESCH_DIR = os.path.join(ROOT, "data", "beschaffung")

EUROPA = {"DE", "AT", "NL", "FR", "PL", "CZ", "SK", "HU", "IE", "FI", "ES", "IT", "BE", "LU", "DK", "SE", "CH", "PT", "SI", "EU"}
KONF_RANG = {"Q": 0, "Q-Treffer": 1, "E": 2, "A": 3}


def jl(p):
    return json.load(open(p, encoding="utf-8"))


# ------------------------------------------------------------------ Zaehlung
def gruppe_von(comp, regeln):
    for pat, g in regeln["gruppen"]["regeln"]:
        if re.match(pat, comp):
            return g
    return None


def komp_artikel(comp, v):
    """Artikel einer Komponente fuer EINE Instanz: id -> dict(stueck, menge, stuecke, masse_g, art, namen, ausnahmen)"""
    agg = OrderedDict()
    ausn = defaultdict(lambda: [0, 0.0])
    ungeklaert = []

    def put(a, b, zaehlen, menge, benannt):
        e = agg.setdefault(a.id, {"art": a, "stueck": 0, "menge": 0.0, "stuecke": [], "masse_g": 0.0, "namen": defaultdict(int), "name_vergeben": 0})
        e["masse_g"] += b["mass_g"]
        if zaehlen:
            e["stueck"] += 1
            e["menge"] += menge
            if a.einheit == "m":
                e["stuecke"].append(menge)
        if benannt:
            e["name_vergeben"] += 1
            e["namen"][benannt] += 1

    lt = comp.startswith("lt_")
    lt_art = None
    if lt:
        benannte = [b for b in v["bodies"] if not BN.ist_unbenannt(b["name"])]
        lt_art = BA.classify_lt(comp, benannte or v["bodies"])
        if lt_art is None:
            return agg, ausn, [(comp, "lt-Art unbekannt", None)]
    first = True
    for b in v["bodies"]:
        if lt and not BN.ist_unbenannt(b["name"]):
            put(lt_art, b, first, lt_art.menge, None)
            first = False
            continue
        a, ex = BA.zuordnen(comp, b)
        if ex:
            ausn[ex][0] += 1
            ausn[ex][1] += b["mass_g"]
            continue
        if a is None:
            ungeklaert.append((comp, b["name"], b))
            continue
        bn = BN.benenne(comp, b) if BN.ist_unbenannt(b["name"]) else None
        put(a, b, not a.teil_von, a.menge, bn["name"] if bn else None)
    return agg, ausn, ungeklaert


# ------------------------------------------------------------------ Zuschnitt (1D)
def pack(stuecke_mm, L, kerf):
    """First-Fit-Decreasing; Rueckgabe Zahl Stangen, Restlaengen"""
    bars = []
    for p in sorted(stuecke_mm, reverse=True):
        need = p + kerf
        for i, r in enumerate(bars):
            if r >= need:
                bars[i] -= need
                break
        else:
            bars.append(L + kerf - need)
    return len(bars), sum(bars)


def zuschnitt(stuecke_m, lager, kerf):
    """stuecke_m: Liste Stuecklaengen in m (je Instanz expandiert). Waehlt die Lagerlaenge mit kleinster Kaufmenge."""
    lmax = max(lager)
    teile, geteilt = [], 0
    vollstangen = 0
    for p in stuecke_m:
        mm = int(round(p * 1000))
        while mm > lmax:
            vollstangen += 1
            mm -= lmax
            geteilt += 1
        if mm > 0:
            teile.append(mm)
    best = None
    for L in sorted(lager):
        if teile and max(teile) > L:
            continue
        n, rest = pack(teile, L, kerf) if teile else (0, 0)
        kauf_mm = (n * L) if L != lmax else n * L
        # vollstangen laufen in der groessten Lagerlaenge
        gesamt = n * L + vollstangen * lmax
        key = (gesamt, n)
        if best is None or key < best[0]:
            best = (key, L, n, rest)
    if best is None:
        n, rest = (0, 0)
        L = lmax
        best = ((vollstangen * lmax, 0), L, 0, 0)
    (_, _), L, n, rest = best
    bedarf_mm = sum(int(round(p * 1000)) for p in stuecke_m)
    kauf_mm = n * L + vollstangen * lmax
    return {
        "lagerlaenge_mm": L, "stangen": n + (vollstangen if L == lmax else 0), "stangen_gross": vollstangen if L != lmax else 0,
        "grosse_lagerlaenge_mm": lmax if (L != lmax and vollstangen) else None,
        "gekauft_m": round(kauf_mm / 1000.0, 3), "bedarf_m": round(bedarf_mm / 1000.0, 3),
        "verschnitt_quote": round(1 - bedarf_mm / kauf_mm, 4) if kauf_mm else 0.0,
        "geteilte_stuecke": geteilt, "saegeschnitt_mm": kerf,
    }


# ------------------------------------------------------------------ Preise
def lade_beschaffung():
    res = {}
    quellen = {}
    for f in sorted(glob.glob(os.path.join(BESCH_DIR, "*.json"))):
        d = jl(f)
        a = d.get("artikel", {})
        items = a.items() if isinstance(a, dict) else [(x.get("id"), x) for x in a]
        for aid, v in items:
            if aid is None:
                continue
            res.setdefault(aid, {"angebote": [], "meta": {}})
            res[aid]["angebote"].extend(v.get("angebote", []) or [])
            for k, x in v.items():
                if k != "angebote":
                    res[aid]["meta"].setdefault(k, x)
            quellen.setdefault(aid, os.path.basename(f))
    return res, quellen


def land_code(s):
    if not s:
        return None
    m = re.match(r"([A-Z]{2})\b", s.strip())
    return m.group(1) if m else ("unbekannt" if s.lower().startswith("unbekannt") else s)


def einheit0(s):
    return (s or "").split(" ")[0].strip()


def angebot_norm(g):
    land = land_code(g.get("land"))
    lief = (g.get("lieferung_de") or "unbekannt")
    liefer = "ja" if lief.startswith("ja") else ("nein" if lief.startswith("nein") else "unbekannt")
    konf = (g.get("konfidenz") or "A")
    k0 = "Q-Treffer" if konf.startswith("Q-Treffer") else ("Q" if konf.startswith("Q") else konf[0])
    return {"preis_eur": g.get("preis_eur"), "bezug_einheit": einheit0(g.get("bezug_einheit")), "bezug_roh": g.get("bezug_einheit"), "stand": g.get("stand"),
            "haendler": g.get("haendler"), "land": land, "land_roh": g.get("land"), "url": g.get("url"), "lieferung_de": liefer,
            "konfidenz": k0, "bemerkung": g.get("bemerkung")}


def waehle_preis(angebote, einheit, aid, kaufdaten, alias):
    """Rueckgabe (gewaehlt|None, alternativen[], grund|None)"""
    norm = [angebot_norm(g) for g in angebote if isinstance(g.get("preis_eur"), (int, float))]
    if not norm:
        return None, [], "kein Angebot mit Preis in data/beschaffung"
    eu = [g for g in norm if g["land"] in EUROPA]
    uk = [g for g in norm if g["land"] in ("UK", "GB")]
    kand = []
    for g in eu:
        if g["lieferung_de"] == "nein":
            continue
        ok_einheit = g["bezug_einheit"] == einheit or (g["bezug_einheit"] == "Stange" and kaufdaten.get("stangen"))
        if not ok_einheit:
            continue
        kand.append(g)
    alt = [g for g in norm if g not in kand]
    if not kand:
        if eu and not any(g["bezug_einheit"] == einheit for g in eu):
            return None, norm, "Angebote in anderer Bezugseinheit (%s), Umrechnung offen" % "/".join(sorted({g["bezug_einheit"] for g in eu}))
        if uk and not eu:
            return None, norm, "nur UK-Angebot (OFFEN (Ben): UK als Europa)"
        if not eu:
            return None, norm, "kein Angebot in Europa mit bekanntem Land"
        return None, norm, "Angebot ohne Lieferung nach Deutschland"
    kand.sort(key=lambda g: (0 if g["lieferung_de"] == "ja" else 1, g["preis_eur"], KONF_RANG.get(g["konfidenz"], 9), g["haendler"] or ""))
    return kand[0], [g for g in norm if g is not kand[0]], None


def gesamtpreis(g, a):
    """Gesamtpreis (EUR) fuer die Kaufmenge `a` in Bezugseinheit des Angebots"""
    if g["bezug_einheit"] == "Stange":
        return round(g["preis_eur"] * a["stangen"], 2)
    if a.get("gekauft_m") is not None and a["einheit"] == "m":
        return round(g["preis_eur"] * a["gekauft_m"], 2)
    return round(g["preis_eur"] * a["kauf_menge"], 2)


# ------------------------------------------------------------------ Hauptlauf
def main():
    regeln = jl(os.path.join(ROOT, "data", "bom_regeln.json"))
    cache = jl(BA.CACHE)
    kat = jl(BA.KATALOG)
    katalog = {a["id"]: a for a in kat["artikel"]}
    inst = defaultdict(int)
    inst_json = jl(BA.INST)
    for i in inst_json["instances"]:
        inst[i["d"]] += 1
    comps = cache["komponenten"]
    gesamt_inst = sum(inst.values())

    zeilen = OrderedDict()   # aid -> Zeile
    ausn_gesamt = defaultdict(lambda: {"koerper": 0, "masse_kg": 0.0, "komponenten": defaultdict(int)})
    ungeklaert = []
    unbenannt_gesamt = 0
    benannt_summe = defaultdict(int)
    komp_zeilen = []
    ohne_gruppe = []
    masse_koerper_kg = 0.0

    for comp in sorted(comps):
        v = comps[comp]
        n_inst = inst.get(comp, 0)
        g = gruppe_von(comp, regeln)
        if g is None:
            ohne_gruppe.append(comp)
        masse_comp = sum(b["mass_g"] for b in v["bodies"])
        agg, ausn, ung = komp_artikel(comp, v)
        for reason, (n, m) in ausn.items():
            e = ausn_gesamt[reason]
            e["koerper"] += n * max(n_inst, 1) if False else n
            e["masse_kg"] += m * n_inst / 1000.0
            e["komponenten"][comp] += n
        for c, name, b in ung:
            ungeklaert.append({"komponente": c, "koerper": name})
        masse_listet = 0.0
        for aid, e in agg.items():
            a = e["art"]
            z = zeilen.setdefault(aid, {
                "artikel_id": aid, "typ": a.typ, "bezeichnung": a.bez, "einheit": a.einheit, "werkstoff": a.werkstoff, "masse": a.mass,
                "beschaffung_art": a.art, "hinweise": [], "verwendung": [], "stuecke_m": [], "masse_kg": 0.0, "name_vergeben": 0})
            if a.flag and a.flag not in z["hinweise"]:
                z["hinweise"].append(a.flag)
            z["verwendung"].append({"komponente": comp, "gruppe": g, "instanzen": n_inst, "koerper_je_instanz": e["stueck"],
                                    "menge_je_instanz": round(e["menge"], 4), "menge": round(e["menge"] * n_inst, 4)})
            z["stuecke_m"].extend([s for s in e["stuecke"] for _ in range(n_inst)])
            z["masse_kg"] += e["masse_g"] * n_inst / 1000.0
            z["name_vergeben"] += e["name_vergeben"] * n_inst
            masse_listet += e["masse_g"]
            for nm, c in e["namen"].items():
                benannt_summe[nm] += c * n_inst
        masse_ausn = sum(m for (_, m) in ausn.values())
        masse_ung = sum(b["mass_g"] for _, _, b in ung if b)
        komp_zeilen.append({"komponente": comp, "gruppe": g, "instanzen": n_inst, "koerper": len(v["bodies"]),
                            "masse_kg_je_instanz": round(masse_comp / 1000.0, 4),
                            "masse_kg_gelistet": round(masse_listet / 1000.0, 4), "masse_kg_ausnahme": round(masse_ausn / 1000.0, 4),
                            "masse_kg_ungeklaert": round(masse_ung / 1000.0, 4)})
        masse_koerper_kg += masse_comp * n_inst / 1000.0
        unbenannt_gesamt += sum(1 for b in v["bodies"] if BN.ist_unbenannt(b["name"]))

    # Zuschnitt, Kaufmenge, Preis
    beschaffung, quellen = lade_beschaffung()
    kerf = regeln["zuschnitt"]["saegeschnitt_mm"]
    lager_typ = regeln["zuschnitt"]["lagerlaengen_mm"]
    aufschlag = regeln["aufschlag"]["je_einheit"]
    alias = regeln.get("preis_alias", {})
    liste = []
    summe = 0.0
    summe_typ = defaultdict(float)
    summe_gruppe = defaultdict(float)
    ohne_preis = 0
    summe_einmal = 0.0
    n_einmal = 0
    for aid in sorted(zeilen, key=lambda x: (zeilen[x]["typ"], x)):
        z = zeilen[aid]
        kt = katalog.get(aid, {})
        bedarf = sum(u["menge"] for u in z["verwendung"])
        z["bedarf"] = round(bedarf, 4)
        z["nicht_platziert"] = all(u["instanzen"] == 0 for u in z["verwendung"])
        einmal = sum(u["menge_je_instanz"] for u in z["verwendung"])
        z["bedarf_wenn_je_komponente_einmal"] = round(einmal, 4)
        lager = kt.get("lagerlaengen_mm") or (lager_typ.get(z["typ"]) if z["einheit"] == "m" else None)
        kauf = {"einheit": z["einheit"]}
        if z["einheit"] == "m" and lager and z["stuecke_m"]:
            zs = zuschnitt(z["stuecke_m"], lager, kerf)
            kauf.update(zs)
            kauf["kauf_menge"] = zs["gekauft_m"]
        elif z["einheit"] == "m":
            kauf["kauf_menge"] = math.ceil(bedarf * 10) / 10.0
            kauf["gekauft_m"] = None
        elif z["einheit"] in ("Stk", "Satz"):
            kauf["kauf_menge"] = int(math.ceil(round(bedarf * (1 + aufschlag.get(z["einheit"], 0) / 100.0), 6)))
        else:
            f = 1 + aufschlag.get(z["einheit"], 0) / 100.0
            kauf["kauf_menge"] = math.ceil(bedarf * f * 100) / 100.0
        kauf["aufschlag_prozent"] = aufschlag.get(z["einheit"], 0)
        # Preis
        b = beschaffung.get(aid)
        quelle = quellen.get(aid)
        alias_von = None
        if b is None and aid in alias and alias[aid] in beschaffung:
            b, quelle, alias_von = beschaffung[alias[aid]], quellen.get(alias[aid]), alias[aid]
        wahl, alt, grund = (None, [], "kein Eintrag in data/beschaffung")
        meta = {}
        if b is not None:
            meta = b["meta"]
            wahl, alt, grund = waehle_preis(b["angebote"], z["einheit"], aid, dict(kauf, einheit=z["einheit"]), alias)
        status = "OK"
        st_meta = meta.get("status") if isinstance(meta.get("status"), str) else ""
        offen_marke = None
        for m in re.findall(r"OFFEN \([^)]*\)", st_meta or ""):
            offen_marke = m
            break
        preis = None
        if wahl is not None:
            gp = gesamtpreis(wahl, dict(kauf, einheit=z["einheit"], stangen=kauf.get("stangen")))
            preis = {"einzelpreis_eur": wahl["preis_eur"], "bezug_einheit": wahl["bezug_einheit"], "gesamtpreis_eur": gp,
                     "stand": wahl["stand"], "haendler": wahl["haendler"], "land": wahl["land"], "url": wahl["url"],
                     "lieferung_de": wahl["lieferung_de"], "konfidenz": wahl["konfidenz"], "bemerkung": wahl["bemerkung"],
                     "alias_von": alias_von}
            status = offen_marke or "OK"
        else:
            gp = None
            status = offen_marke or "OFFEN (Quelle)"
            if z["typ"] == "SON" and z["beschaffung_art"] == "c" and b is not None and not b["angebote"]:
                grund = grund + "; Eigenbau, Rohmaterial in anderen Zeilen"
        zeile = {
            "artikel_id": aid, "typ": z["typ"], "bezeichnung": z["bezeichnung"], "werkstoff": z["werkstoff"], "masse": z["masse"],
            "beschaffung_art": z["beschaffung_art"], "einheit": z["einheit"],
            "bedarf": z["bedarf"], "nicht_platziert": z["nicht_platziert"], "bedarf_wenn_je_komponente_einmal": z["bedarf_wenn_je_komponente_einmal"],
            "kauf": kauf, "masse_kg": round(z["masse_kg"], 3),
            "verwendung": sorted(z["verwendung"], key=lambda u: u["komponente"]),
            "gruppen": sorted({u["gruppe"] for u in z["verwendung"] if u["gruppe"]}),
            "hinweise": sorted(z["hinweise"]), "name_vergeben": z["name_vergeben"],
            "preis": preis, "alternativen": [{k: a[k] for k in ("preis_eur", "bezug_einheit", "haendler", "land", "url", "lieferung_de", "konfidenz", "stand")} for a in alt],
            "status": status, "status_grund": None if wahl is not None and status == "OK" else (grund or st_meta or None),
            "quelle_preis": quelle,
        }
        if preis is not None and not z["nicht_platziert"]:
            summe += gp
            summe_typ[z["typ"]] += gp
            # Gruppenanteil nach Bedarfsanteil
            tot = sum(u["menge"] for u in z["verwendung"]) or 1.0
            for u in z["verwendung"]:
                if u["gruppe"]:
                    summe_gruppe[u["gruppe"]] += gp * u["menge"] / tot
        if preis is None and not z["nicht_platziert"]:
            ohne_preis += 1
        if z["nicht_platziert"] and preis is not None and preis["bezug_einheit"] == z["einheit"]:
            e1 = z["bedarf_wenn_je_komponente_einmal"]
            e1 = math.ceil(round(e1, 6)) if z["einheit"] in ("Stk", "Satz") else e1
            zeile["preis_wenn_je_komponente_einmal_eur"] = round(preis["einzelpreis_eur"] * e1, 2)
            if not all(u["komponente"].startswith("lt_") for u in z["verwendung"]):
                summe_einmal += zeile["preis_wenn_je_komponente_einmal_eur"]
                n_einmal += 1
        liste.append(zeile)

    nicht_platziert = [z["artikel_id"] for z in liste if z["nicht_platziert"]]
    out = OrderedDict()
    out["kopf"] = {
        "erzeugt_von": "scripts/bom.py",
        "modell": cache["stempel"],
        "modell_aktuell": BA.modellstempel(),
        "drift": cache["stempel"]["sc_sha256"] != BA.modellstempel()["sc_sha256"],
        "instanzen": gesamt_inst, "definitionen": len(inst),
        "zeilen": len(liste), "zeilen_ohne_preis_platziert": ohne_preis, "zeilen_nicht_platziert": len(nicht_platziert),
        "summe_eur_platziert": round(summe, 2), "waehrung": "EUR brutto",
        "nicht_platziert_je_einmal": {"zeilen_mit_preis": n_einmal, "summe_eur": round(summe_einmal, 2),
                                      "hinweis": "Richtgroesse: je 1 Stueck der nicht platzierten Komponenten (ohne lt_-Bibliotheksvarianten); gehoert NICHT in summe_eur_platziert, Entscheidung offen"},
        "summe_je_typ": {k: round(v, 2) for k, v in sorted(summe_typ.items())},
        "summe_je_gruppe": {k: round(v, 2) for k, v in sorted(summe_gruppe.items())},
        "masse_koerper_gesamt_kg": round(masse_koerper_kg, 1),
        "unbenannte_koerper_im_cache": unbenannt_gesamt,
        "name_vergeben_summe": sum(benannt_summe.values()),
        "entscheidungen": kat.get("artikel_stempel", {}).get("entscheidungen"),
        "regel_nicht_platziert": "Komponenten ohne Instanz in viewer/instances.json zaehlen Menge 0 und stehen unter nicht_platziert; Preis zaehlt nicht in die Summe (bedarf_wenn_je_komponente_einmal zeigt die Menge bei je einem Stueck).",
    }
    out["typen"] = kat["typen"]
    out["ausnahmen"] = {k: {"koerper": v["koerper"], "masse_kg": round(v["masse_kg"], 2), "komponenten": dict(sorted(v["komponenten"].items()))} for k, v in sorted(ausn_gesamt.items())}
    out["ungeklaert"] = ungeklaert
    out["komponenten_ohne_gruppe"] = ohne_gruppe
    out["benennung_vergeben"] = dict(sorted(benannt_summe.items()))
    out["komponenten"] = komp_zeilen
    out["zeilen"] = liste
    if "--stdout" in sys.argv:
        print(json.dumps(out["kopf"], ensure_ascii=False, indent=1))
        return out
    json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    schreibe_md(out)
    k = out["kopf"]
    print(f"Zeilen {k['zeilen']} (ohne Preis {k['zeilen_ohne_preis_platziert']}, nicht platziert {k['zeilen_nicht_platziert']}), Summe {k['summe_eur_platziert']} EUR, ungeklaert {len(ungeklaert)}, drift {k['drift']}")
    return out


def eur(x):
    return "%s EUR" % ("{:,.2f}".format(x).replace(",", "X").replace(".", ",").replace("X", "."))


def schreibe_md(out):
    k = out["kopf"]
    L = []
    L.append("# Stueckliste (erzeugt, nicht von Hand)\n")
    L.append("Erzeugt von `scripts/bom.py` aus dem Modellstand (`viewer/instances.json` built %s, sc_sha256 %s). Preise brutto, Richtwerte mit Datum, keine Angebote. Quelle der Preise: `data/beschaffung/*.json`.\n" % (k["modell"]["instances_built"], k["modell"]["sc_sha256"]))
    if k["drift"]:
        L.append("**Drift:** die `.sc` haben sich seit der Koerpermessung geaendert (aktuell %s). Nachmessen: `python -X utf8 scripts/bom_artikel.py --ergaenzen`.\n" % k["modell_aktuell"]["sc_sha256"])
    L.append("## Kopf\n")
    L.append("1. Zeilen: %d (Preis fehlt bei %d platzierten, %d Zeilen nur in nicht platzierten Komponenten)" % (k["zeilen"], k["zeilen_ohne_preis_platziert"], k["zeilen_nicht_platziert"]))
    L.append("2. Summe der Zeilen mit Preis (platziert): %s" % eur(k["summe_eur_platziert"]))
    L.append("2b. Nicht platzierte Komponenten (ohne lt_-Bibliothek), je 1 Stueck gerechnet, %d Zeilen mit Preis: %s (nicht in der Summe, Entscheidung offen)" % (k["nicht_platziert_je_einmal"]["zeilen_mit_preis"], eur(k["nicht_platziert_je_einmal"]["summe_eur"])))
    L.append("3. Instanzen im Modell: %d in %d Definitionen" % (k["instanzen"], k["definitionen"]))
    L.append("4. Unbenannte Koerper (Body<n>) in der Messung: %d, davon per Regel benannt: %d, ungeklaert: %d" % (k["unbenannte_koerper_im_cache"], k["name_vergeben_summe"], len(out["ungeklaert"])))
    L.append("")
    L.append("## Summe je Typ\n")
    L.append("| Typ | Bedeutung | Summe |\n|---|---|---|")
    for t, v in k["summe_je_typ"].items():
        L.append("| %s | %s | %s |" % (t, out["typen"].get(t, ""), eur(v)))
    L.append("")
    L.append("## Summe je Bauteilgruppe\n")
    L.append("| Gruppe | Summe |\n|---|---|")
    for t, v in k["summe_je_gruppe"].items():
        L.append("| %s | %s |" % (t, eur(v)))
    L.append("")
    L.append("## Nicht in der Liste (Ausnahmen)\n")
    L.append("| Grund | Koerper | Masse (kg, mit Instanzen) |\n|---|---|---|")
    for g, v in out["ausnahmen"].items():
        L.append("| %s | %d | %s |" % (g, v["koerper"], v["masse_kg"]))
    L.append("")
    for t in out["typen"]:
        zs = [z for z in out["zeilen"] if z["typ"] == t]
        if not zs:
            continue
        L.append("## %s %s\n" % (t, out["typen"][t]))
        L.append("| Artikel | Bezeichnung | Bedarf | Kauf | Stueck | Gesamt | Status |\n|---|---|---|---|---|---|---|")
        for z in zs:
            p = z["preis"]
            kauf = z["kauf"]
            kt = "%s %s" % (kauf["kauf_menge"], z["einheit"])
            if kauf.get("stangen"):
                kt += " (%d x %d mm)" % (kauf["stangen"], kauf["lagerlaenge_mm"])
            bed = "%s %s" % (z["bedarf"], z["einheit"]) if not z["nicht_platziert"] else "nicht platziert (je 1: %s)" % z["bedarf_wenn_je_komponente_einmal"]
            L.append("| `%s` | %s | %s | %s | %s | %s | %s |" % (
                z["artikel_id"], z["bezeichnung"].replace("|", "/"), bed, kt,
                ("%s/%s" % (p["einzelpreis_eur"], p["bezug_einheit"])) if p else "-", eur(p["gesamtpreis_eur"]) if p else "-",
                z["status"] + ("" if p else " - " + (z["status_grund"] or ""))))
        L.append("")
    open(OUT_MD, "w", encoding="utf-8", newline="\n").write("\n".join(L))


if __name__ == "__main__":
    main()
