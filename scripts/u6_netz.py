"""N-UNIFY-AUTOBAHN U6 Aufgabe 1: Netzliste data/leitungsnetz.json auf die Soll-Wege der Quelle umstellen.

Quelle der Wege: data/oasis-soll.json (77 Wege im Umfang, erzeugt von scripts/oasis_soll.py, nie von Hand).
Schreibt je Soll-Weg eine Kante `S-<weg>` (Feld `soll_weg`, Medium, Antrieb, Nennweite nach Quelle oder D106/D138, Durchfluss der Quelle)
und je beteiligtem Soll-Bauteil einen Knoten (id = Soll-ID). Seit N-UNIFY-AUTOBAHN U7 (D141) besteht das Netz nur noch aus diesen
Kanten und Knoten (Altbestand K01 bis K59 im Archiv data/archiv/leitungsnetz-altbestand.json); die Liste `kabel` bleibt unberuehrt.
Aufruf: python -X utf8 scripts/u6_netz.py [--schreiben]   (ohne Schalter: nur Zaehlung)"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NETZ_P = os.path.join(ROOT, "data", "leitungsnetz.json")
SOLL = json.load(open(os.path.join(ROOT, "data", "oasis-soll.json"), encoding="utf-8"))
CRLF = chr(13) + chr(10)   # Datei hat Windows-Zeilenenden; so bleibt der Diff klein
MEDIUM = {"water": "Wasser", "air": "Luft", "sludge": "Schlamm", "power": "Strom"}


def nennweite(w):
    """(dn Aussendurchmesser oder None, schlauch_id oder None, Herkunft). Quelle zuerst, sonst D106 (Planer) bzw. D138 (U6)."""
    i, med = w["id"], w["medium"]
    nw = (w.get("nennweite") or "").strip()
    if nw.startswith("Schlauch ID"):
        return None, int(nw.split("ID")[1]), "Quelle"
    if nw.startswith("d"):
        if "Ring d75" in nw:                      # e27 bis e30: Ring d75, Kupplungsstrecke d63 mit Kugelhahn
            return 75, None, "Quelle (Ring d75, Kupplungsstrecke d63)"
        return int(nw[1:3]), None, "Quelle"
    if med == "power":
        return None, None, "Kabel"
    if med == "air":
        return 20, None, "D106 (Luftleitungen d20)"
    if med == "sludge":
        if w["antrieb"] == "von-hand":
            return None, None, "D138 (von Hand, keine Leitung)"
        return 50, None, "D138 (Schlammleitung d50 vom Bodenablass)"
    if w["antrieb"] == "gleich" and w["nach"].startswith(("filterpumpe", "hauptpumpe")):
        return None, None, "D138 (Tauchpumpe im Becken, keine Leitung)"
    if w["nach"] in ("filterpumpe_1", "filterpumpe_2", "venturi_1", "venturi_2", "vortex_1", "vortex_2") or w["von"].startswith("venturi"):
        return 50, None, "D106 (Saug- und Druckleitung der Pumpen d50)"
    if i in ("e62", "e63", "e70", "e81", "e82", "e23", "e24"):
        return 63, None, "D106 (Ueberlaeufe der Becken und Notueberlauf d63)"
    if i == "e57":
        return None, 25, "D138 (Ruecklauf NFT Innen in den Fischtank, Schlauch ID25 wie die Sumpf-Zulaeufe D106)"
    if w["nach"].startswith("sump"):
        return None, 25, "D106 (Sumpf-Zulaeufe Schlauch ID25)"
    if i in ("e17", "e18", "e19"):
        return 25, None, "D138 (Nachspeisung d25)"
    return None, None, "offen"


def kanten_und_knoten():
    wege = [w for w in SOLL["wege"] if w.get("im_umfang")]
    bt = {b["id"]: b for b in SOLL["bauteile"]}
    kanten, ids = [], []
    for w in wege:
        dn, sid, herk = nennweite(w)
        k = dict(id="S-" + w["id"], soll_weg=w["id"], von=w["von"], nach=w["nach"], medium=MEDIUM[w["medium"]], antrieb=w["antrieb"],
                 dn=dn, schlauch_id=sid, nennweite_herkunft=herk, soll_l_min=w.get("durchfluss_l_min"),
                 quelle="Q oasis-soll.json " + w["id"], bemerkung=w.get("label", ""))
        if w["medium"] == "power":
            k["art"] = "kabel"
        elif herk.startswith("D138 (Tauchpumpe") or herk.startswith("D138 (von Hand"):
            k["art"] = "ohne_leitung"
        else:
            k["art"] = "leitung"
        kanten.append(k)
        for e in (w["von"], w["nach"]):
            if e not in ids:
                ids.append(e)
    knoten = []
    for i in ids:
        b = bt[i]
        knoten.append(dict(id=i, typ=b.get("art"), bauteil=i, name=b.get("name"), linie=b.get("linie"),
                           bemerkung="Soll-Bauteil der Quelle (data/oasis-soll.json)"))
    return knoten, kanten


def main():
    netz = json.load(open(NETZ_P, encoding="utf-8"))
    knoten, kanten = kanten_und_knoten()
    print("Soll-Kanten %d (Wasser %d, Luft %d, Schlamm %d, Strom %d), Soll-Knoten %d" % (
        len(kanten), *[sum(1 for k in kanten if k["medium"] == m) for m in ("Wasser", "Luft", "Schlamm", "Strom")], len(knoten)))
    for k in kanten:
        print("  %-6s %-14s -> %-14s %-8s %-11s dn %-4s ID %-4s %s" % (k["id"], k["von"], k["nach"], k["medium"], k["antrieb"], k["dn"], k["schlauch_id"], k["nennweite_herkunft"]))
    if "--schreiben" in sys.argv:
        netz["knoten"] = knoten
        netz["kanten"] = kanten
        netz["version"] = 4
        netz["stand"] = "11.11.2026"
        netz["hinweis_u6"] = ("Version 4 (N-UNIFY-AUTOBAHN U6): Kanten S-e17 bis S-e94 = die 77 Wege der Quelle (data/oasis-soll.json); "
                              "seit U7 (D141) ohne Altbestand. Erzeugt von scripts/u6_netz.py.")
        with open(NETZ_P, "w", encoding="utf-8", newline=CRLF) as f:
            json.dump(netz, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("geschrieben:", NETZ_P)


if __name__ == "__main__":
    main()
