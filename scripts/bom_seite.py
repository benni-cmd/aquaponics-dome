"""N-STUECKLISTE 3/3b: interaktive Einkaufsliste als EINE Datei (docs/einkaufsliste.html), offline, ohne externe Requests.

Wird von scripts/bom.py nach dem Schreiben von data/stueckliste.json aufgerufen (schreibe_seite(out)).
Einzeln: python -X utf8 scripts/bom_seite.py   (liest data/stueckliste.json)
Regel W45: gleiche Eingabe, gleiche Ausgabe (kein Laufzeit-Zeitstempel).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("BOM_ROOT") or os.path.dirname(HERE)
OUT_HTML = os.path.join(ROOT, "docs", "einkaufsliste.html")

GRUPPEN_REIHENFOLGE = ["Kuppel", "Fundament", "Becken und Tanks", "Filter", "Tische und Beete", "Leitungen", "Huelle", "Messtechnik und Elektrik"]


def daten(out):
    k = out["kopf"]
    zeilen = []
    staende = []
    for z in out["zeilen"]:
        p = z["preis"]
        gp = p["gesamtpreis_eur"] if p else None
        if p:
            staende.append(p["stand"])
        # Mengenanteil je Gruppe (gleiche Verteilung wie summe_je_gruppe in bom.py)
        je_gruppe = {}
        for u in z["verwendung"]:
            g = u["gruppe"]
            if g:
                je_gruppe[g] = je_gruppe.get(g, 0.0) + u["menge"]
        tot = sum(je_gruppe.values()) or 1.0
        komp_je_gruppe = {}
        for u in z["verwendung"]:
            if u["gruppe"]:
                komp_je_gruppe.setdefault(u["gruppe"], []).append(u["komponente"])
        gr = []
        for g in sorted(je_gruppe, key=lambda x: (GRUPPEN_REIHENFOLGE.index(x) if x in GRUPPEN_REIHENFOLGE else 99, x)):
            gr.append({"g": g, "menge": round(je_gruppe[g], 4), "preis": (round(gp * je_gruppe[g] / tot, 4) if (gp is not None and not z["nicht_platziert"]) else None),
                       "komp": sorted(set(komp_je_gruppe[g]))})
        kauf = z["kauf"]
        zeilen.append({
            "id": z["artikel_id"], "typ": z["typ"], "bez": z["bezeichnung"], "einheit": z["einheit"], "bedarf": z["bedarf"],
            "np": z["nicht_platziert"], "einmal": z["bedarf_wenn_je_komponente_einmal"],
            "kauf": kauf.get("kauf_menge"), "stangen": kauf.get("stangen"), "lager": kauf.get("lagerlaenge_mm"), "vq": kauf.get("verschnitt_quote"),
            "art": z["beschaffung_art"], "status": z["status"], "grund": z["status_grund"],
            "p": ({"e": p["einzelpreis_eur"], "b": p["bezug_einheit"], "g": p["gesamtpreis_eur"], "h": p["haendler"], "l": p["land"], "u": p["url"],
                   "s": p["stand"], "k": p["konfidenz"], "d": p["lieferung_de"], "a": p.get("alias_von")} if p else None),
            "alt": len(z["alternativen"]), "gr": gr, "hin": z["hinweise"],
            "pe": z.get("preis_wenn_je_komponente_einmal_eur"),
        })
    return {"kopf": {"summe": k["summe_eur_platziert"], "zeilen": k["zeilen"], "ohne_preis": k["zeilen_ohne_preis_platziert"], "np": k["zeilen_nicht_platziert"],
                     "np_einmal": k["nicht_platziert_je_einmal"], "modell": k["modell"]["instances_built"], "sc": k["modell"]["sc_sha256"], "drift": k["drift"],
                     "instanzen": k["instanzen"], "stand_preise": max(staende) if staende else None,
                     "summe_typ": k["summe_je_typ"], "summe_gruppe": k["summe_je_gruppe"]},
            "typen": out["typen"], "gruppen": [g for g in GRUPPEN_REIHENFOLGE if g in k["summe_je_gruppe"]] + [g for g in k["summe_je_gruppe"] if g not in GRUPPEN_REIHENFOLGE],
            "zeilen": zeilen}


def schreibe_seite(out):
    d = daten(out)
    js = json.dumps(d, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    html = VORLAGE.replace("__DATEN__", js)
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


VORLAGE = open(os.path.join(HERE, "bom_seite_vorlage.html"), encoding="utf-8").read() if os.path.exists(os.path.join(HERE, "bom_seite_vorlage.html")) else ""

if __name__ == "__main__":
    schreibe_seite(json.load(open(os.path.join(ROOT, "data", "stueckliste.json"), encoding="utf-8")))
    print("geschrieben:", OUT_HTML)
