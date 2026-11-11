"""N-STUECKLISTE 3/3b: interaktive Einkaufsliste als EINE Datei (docs/einkaufsliste.html), offline, ohne externe Requests.

Wird von scripts/bom.py nach dem Schreiben von data/stueckliste.json aufgerufen (schreibe_seite(out)).
Einzeln: python -X utf8 scripts/bom_seite.py   (liest data/stueckliste.json)
Regel W45: gleiche Eingabe, gleiche Ausgabe (kein Laufzeit-Zeitstempel).
"""
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("BOM_ROOT") or os.path.dirname(HERE)
sys.path.insert(0, HERE)
import variante as V  # noqa: E402

OUT_HTML = V.pfad("einkaufsliste", root=ROOT)

GRUPPEN_REIHENFOLGE = ["Kuppel", "Fundament", "Becken und Tanks", "Filter", "Tische und Beete", "Leitungen", "Huelle", "Messtechnik und Elektrik"]

# A4: Anzeigetexte mit echten Umlauten; Coding-Namen (Artikel-IDs, Komponenten) bleiben ASCII.
UML = {w.split("=")[0]: w.split("=")[1] for w in (
    "Ausruestung=Ausrüstung Beetfuellung=Beetfüllung Behaelter=Behälter Behaelterdurchfuehrung=Behälterdurchführung "
    "Behaelterfuellung=Behälterfüllung Belueftungsgitter=Belüftungsgitter Blaehton=Blähton Druckbehaelter=Druckbehälter "
    "Durchfuehrung=Durchführung Flaeche=Fläche Fuellkoerper=Füllkörper Fussplatte=Fußplatte Geblaese=Gebläse Gehaeuse=Gehäuse "
    "Gewaechshaus=Gewächshaus Gitterkaefig=Gitterkäfig Grosspackung=Großpackung Gummifuss=Gummifuß Haendler=Händler "
    "Haustuer=Haustür Hoehe=Höhe Huelle=Hülle Huelse=Hülse Kabeleinfuehrung=Kabeleinführung Laenge=Länge Lagerlaenge=Lagerlänge "
    "Mass=Maß Membrangeblaese=Membrangebläse Oesterreich=Österreich Rueckschlagventil=Rückschlagventil "
    "Scheibenbelueftung=Scheibenbelüftung Schlauchtuelle=Schlauchtülle Stueck=Stück Stueckzahl=Stückzahl Stuetze=Stütze "
    "Stuetzfuss=Stützfuß Stuetzrippe=Stützrippe Tuelle=Tülle Tuer=Tür Tuerblatt=Türblatt Tuerdichtung=Türdichtung "
    "Tuerdruecker=Türdrücker Tuerscharnier=Türscharnier Tuerzarge=Türzarge Uebergang=Übergang Verbindungsstueck=Verbindungsstück "
    "Verkaeufer=Verkäufer Zellkoerper=Zellkörper bestaendig=beständig fuer=für ueber=über gross=groß weiss=weiß tuerig=türig "
    "Anschweissband=Anschweißband tuerdruecker=türdrücker").split()}
_WORT = re.compile(r"[A-Za-z]+")


def uml(t):
    """Ersetzt ASCII-Umschreibungen ganzer Woerter durch echte Umlaute (nur Anzeige)."""
    if not isinstance(t, str):
        return t
    return _WORT.sub(lambda m: UML.get(m.group(0), m.group(0)), t)


def teile_je_artikel():
    """artikel_id -> [(komponente, teil_id, teil_name)] aus data/parts (Rueckverweis auf die Detailansicht des Viewers)."""
    res = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "data", "parts", "*.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        komp = os.path.splitext(os.path.basename(f))[0]
        for t in d.get("teile", []):
            if t.get("artikel_id"):
                res.setdefault(t["artikel_id"], []).append((komp, t["id"], (t.get("name") or t["id"]) + " in " + (d.get("titel") or komp).split(" (")[0]))
    return res


def daten(out):
    k = out["kopf"]
    je_art = teile_je_artikel()
    platziert = {c["komponente"] for c in out.get("komponenten", [])
                 if isinstance(c, dict) and c.get("instanzen")} if isinstance(out.get("komponenten"), list) else {
        n for n, c in out.get("komponenten", {}).items() if c.get("instanzen")}
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
            gr.append({"g": uml(g), "menge": round(je_gruppe[g], 4), "preis": (round(gp * je_gruppe[g] / tot, 4) if (gp is not None and not z["nicht_platziert"]) else None),
                       "komp": sorted(set(komp_je_gruppe[g]))})
        kauf = z["kauf"]
        zeilen.append({
            "id": z["artikel_id"], "typ": z["typ"], "bez": uml(z["bezeichnung"]), "einheit": z["einheit"], "bedarf": z["bedarf"],
            "np": z["nicht_platziert"], "einmal": z["bedarf_wenn_je_komponente_einmal"],
            "kauf": kauf.get("kauf_menge"), "stangen": kauf.get("stangen"), "lager": kauf.get("lagerlaenge_mm"), "vq": kauf.get("verschnitt_quote"),
            "art": z["beschaffung_art"], "status": z["status"], "grund": uml(z["status_grund"]),
            "p": ({"e": p["einzelpreis_eur"], "b": p["bezug_einheit"], "g": p["gesamtpreis_eur"], "h": uml(p["haendler"]), "l": p["land"], "u": p["url"],
                   "s": p["stand"], "k": p["konfidenz"], "d": p["lieferung_de"], "a": p.get("alias_von")} if p else None),
            "alt": len(z["alternativen"]), "gr": gr, "hin": [uml(x) for x in z["hinweise"]],
            "teile": [{"k": a, "t": b, "n": uml(c)} for a, b, c in sorted(je_art.get(z["artikel_id"], []), key=lambda x: (x[0] not in platziert, x[0], x[1]))[:6]],
            "pe": z.get("preis_wenn_je_komponente_einmal_eur"),
        })
    return {"kopf": {"summe": k["summe_eur_platziert"], "zeilen": k["zeilen"], "ohne_preis": k["zeilen_ohne_preis_platziert"], "np": k["zeilen_nicht_platziert"],
                     "np_einmal": k["nicht_platziert_je_einmal"], "modell": k["modell"]["instances_built"], "sc": k["modell"]["sc_sha256"], "drift": k["drift"],
                     "instanzen": k["instanzen"], "stand_preise": max(staende) if staende else None,
                     "summe_typ": k["summe_je_typ"], "summe_gruppe": {uml(a): b for a, b in k["summe_je_gruppe"].items()}},
            "typen": {a: uml(b) for a, b in out["typen"].items()}, "gruppen": [uml(g) for g in GRUPPEN_REIHENFOLGE if g in k["summe_je_gruppe"]] + [uml(g) for g in k["summe_je_gruppe"] if g not in GRUPPEN_REIHENFOLGE],
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
    schreibe_seite(json.load(open(V.pfad("stueckliste_json", root=ROOT), encoding="utf-8")))
    print("geschrieben:", OUT_HTML)
