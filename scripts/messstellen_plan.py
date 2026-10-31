"""Pruefung des Messstellenplans (R39, D65): data/messstellen.json gegen data/leitungsnetz.json und docs/walkway-map.md.
Aufruf: python scripts/messstellen_plan.py            (Pruefung + Zaehlung, Rueckgabewert 1 bei Fehlern)
        python scripts/messstellen_plan.py --tabelle  (Messstellen als Markdown-Tabelle fuer docs/research/R39.md)
        python scripts/messstellen_plan.py --json     (Zaehlung als JSON)
Pruefungen: (1) jeder Ort ist ein Knoten (oder Kante) der Netzliste bzw. ein bekannter Schaltschrank-Abgang; (2) jede Stelle der Pflichtliste hat
eine Pflicht-Messstelle mit dieser Groesse; (3) jeder Netzlisten-Knoten hat eine Messstelle oder steht begruendet unter ohne_messstelle;
(4) Sondentypen, Halter, Messknoten, Alarme existieren; (5) Zugang gegen die Laufwegkarte (Erreichbarkeit im Knie-Schnitt). Nur lesen, kein Modell."""
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAN = json.load(open(os.path.join(ROOT, "data", "messstellen.json"), encoding="utf-8"))
NETZ = json.load(open(os.path.join(ROOT, "data", "leitungsnetz.json"), encoding="utf-8"))
MAP_PFAD = os.path.join(ROOT, "docs", "walkway-map.md")

KNOTEN = {k["id"] for k in NETZ["knoten"]}
KANTEN = {k["id"]: k for k in NETZ["kanten"]}
EXTERN = {k[s] for k in NETZ["kabel"] for s in ("von", "nach")} | {"kuppel", "geblaese_luftpolster"}   # Abgaenge/Orte ausserhalb der Wassernetzliste
BUS_ADERN = 4   # RS-485 vom Messknoten zur Zentrale (signalweg.bus)


def erreichbarkeit():
    """Status je Bauteil aus dem Knie-Schnitt der Laufwegkarte (erreichbar / NICHT erreichbar)."""
    if not os.path.exists(MAP_PFAD):
        return {}
    text = open(MAP_PFAD, encoding="utf-8").read()
    knie = text.split("## Scheibe knie")[1].split("## Scheibe kopf")[0] if "## Scheibe knie" in text else ""
    out = {}
    for m in re.finditer(r"^- (NICHT erreichbar|erreichbar): (.+)$", knie, re.M):
        out[m.group(2).strip()] = m.group(1) == "erreichbar"
    return out


def preisspanne(typ, n):
    p = PLAN["sondentypen"][typ]["preis"]
    return (None, None) if p["min"] is None else (p["min"] * n, p["max"] * n)


def pruefen():
    fehler, hinweise = [], []
    ms = PLAN["messstellen"]
    ids = [m["id"] for m in ms]
    if len(ids) != len(set(ids)):
        fehler.append("doppelte Messstellen-IDs: " + ", ".join(i for i, c in Counter(ids).items() if c > 1))
    alarm_ids = {a["id"] for a in PLAN["alarmgrenzen"]}
    for m in ms:
        if m["knoten"] not in KNOTEN | EXTERN:
            fehler.append("%s: Knoten '%s' nicht in der Netzliste" % (m["id"], m["knoten"]))
        if m["kante"]:
            k = KANTEN.get(m["kante"])
            if not k:
                fehler.append("%s: Kante '%s' nicht in der Netzliste" % (m["id"], m["kante"]))
            elif m["knoten"] not in (k["von"], k["nach"]):
                hinweise.append("%s: Kante %s (%s -> %s) beruehrt Knoten '%s' nicht" % (m["id"], m["kante"], k["von"], k["nach"], m["knoten"]))
        if m["stufe"] not in PLAN["stufen"]:
            fehler.append("%s: unbekannte Stufe '%s'" % (m["id"], m["stufe"]))
        if m["messknoten"] not in PLAN["messknoten"]:
            fehler.append("%s: Messknoten '%s' fehlt" % (m["id"], m["messknoten"]))
        for typ in m["sonden"]:
            if typ not in PLAN["sondentypen"]:
                fehler.append("%s: Sondentyp '%s' fehlt" % (m["id"], typ))
            elif not set(PLAN["sondentypen"][typ]["groessen"]) & set(m["groessen"]):
                fehler.append("%s: Sondentyp %s misst keine der Groessen %s" % (m["id"], typ, m["groessen"]))
        for h, _ in m["halter"]:
            if h not in PLAN["halter"]:
                fehler.append("%s: Halter '%s' fehlt" % (m["id"], h))
        for a in m["alarm"]:
            if a not in alarm_ids:
                fehler.append("%s: Alarm '%s' fehlt" % (m["id"], a))
    # Pflichtliste
    pflicht = {(m["knoten"], g) for m in ms if m["stufe"] == "pflicht" for g in m["groessen"]}
    luecken = [(p["knoten"], p["groesse"]) for p in PLAN["pflichtliste"] if (p["knoten"], p["groesse"]) not in pflicht]
    for k, g in luecken:
        fehler.append("Pflichtliste: %s / %s hat keine Pflicht-Messstelle" % (k, g))
    for p in PLAN["pflichtliste"]:
        if p["knoten"] not in KNOTEN | EXTERN:
            fehler.append("Pflichtliste: Knoten '%s' nicht in der Netzliste" % p["knoten"])
    # Abdeckung der Netzliste
    belegt = {m["knoten"] for m in ms}
    for k in sorted(KNOTEN - belegt):
        if k not in PLAN["ohne_messstelle"]:
            fehler.append("Netzlisten-Knoten '%s' hat weder Messstelle noch Begruendung unter ohne_messstelle" % k)
    for k in PLAN["ohne_messstelle"]:
        if k in belegt:
            fehler.append("ohne_messstelle '%s' hat doch eine Messstelle" % k)
    return fehler, hinweise, luecken


def zaehlen():
    ms = PLAN["messstellen"]
    z = {"stellen": Counter(m["stufe"] for m in ms), "zusatz_prio": Counter(m["prio"] for m in ms if m["stufe"] == "zusatz")}
    je_typ = defaultdict(lambda: Counter())
    preis = defaultdict(lambda: defaultdict(lambda: [0.0, 0.0]))
    offen = Counter()
    zubehoer = defaultdict(float)
    for m in ms:
        for typ, n in m["sonden"].items():
            je_typ[typ][m["stufe"]] += n
            lo, hi = preisspanne(typ, n)
            if lo is None:
                offen[m["stufe"]] += n
            else:
                w = PLAN["sondentypen"][typ]["preis"]["waehrung"]
                preis[m["stufe"]][w][0] += lo
                preis[m["stufe"]][w][1] += hi
            for name, usd in PLAN["sondentypen"][typ]["zubehoer_usd"].items():
                zubehoer[m["stufe"]] += usd * n
    halter = defaultdict(lambda: Counter())
    for m in ms:
        for h, n in m["halter"]:
            halter[h][m["stufe"]] += n
    knoten = defaultdict(lambda: {"stellen": 0, "adern": 0, "leitungen": 0})
    for m in ms:
        k = knoten[m["messknoten"]]
        k["stellen"] += 1
        for typ, n in m["sonden"].items():
            k["adern"] += PLAN["sondentypen"][typ]["adern"] * n
            k["leitungen"] += n if PLAN["sondentypen"][typ]["adern"] else 0
    return z, je_typ, preis, offen, zubehoer, halter, knoten


def zugang():
    erreichbar = erreichbarkeit()
    ok, konflikt, offen, umgangen = [], [], [], []
    for m in PLAN["messstellen"]:
        b = m["bauteil"]
        if b is None:
            offen.append(m["id"])
        elif b not in erreichbar:
            offen.append(m["id"])
        elif erreichbar[b]:
            ok.append(m["id"])
        elif m["wartung_noetig"] or m["halter"]:
            konflikt.append((m["id"], b))
        else:
            umgangen.append((m["id"], b))   # Bauteil nicht erreichbar, aber Messung im Schaltschrank und ohne Wartung vor Ort
    return ok, konflikt, offen, umgangen, erreichbar


def tabelle():
    zeilen = ["| ID | Ort (Knoten / Kante) | Groesse | Sonde(n) | Preis (Spanne) | Stufe |", "|---|---|---|---|---|---|"]
    for m in PLAN["messstellen"]:
        sonden = ", ".join("%d x %s" % (n, t) for t, n in m["sonden"].items())
        spannen = defaultdict(lambda: [0.0, 0.0])
        offen = False
        for typ, n in m["sonden"].items():
            lo, hi = preisspanne(typ, n)
            if lo is None:
                offen = True
            else:
                w = PLAN["sondentypen"][typ]["preis"]["waehrung"]
                spannen[w][0] += lo
                spannen[w][1] += hi
        preis = "; ".join(("%g" % lo if lo == hi else "%g-%g" % (lo, hi)) + " " + w for w, (lo, hi) in spannen.items()) or "offen"
        if offen and spannen:
            preis += " + offen"
        stufe = "Pflicht" if m["stufe"] == "pflicht" else "Zusatz %d" % m["prio"]
        ort = m["knoten"] + (" / " + m["kante"] if m["kante"] else "")
        zeilen.append("| %s | %s: %s | %s | %s | %s | %s |" % (m["id"], ort, m["ort"], "/".join(m["groessen"]), sonden, preis, stufe))
    return "\n".join(zeilen)


def main():
    if "--tabelle" in sys.argv:
        print(tabelle())
        return 0
    fehler, hinweise, luecken = pruefen()
    z, je_typ, preis, offen, zubehoer, halter, knoten = zaehlen()
    ok, konflikt, ungeprueft, umgangen, erreichbar = zugang()
    if "--json" in sys.argv:
        print(json.dumps({"stellen": dict(z["stellen"]), "zusatz_prio": {str(k): v for k, v in z["zusatz_prio"].items()},
                          "je_typ": {t: dict(c) for t, c in je_typ.items()}, "zugang_konflikt": konflikt, "fehler": fehler}, indent=1))
        return 1 if fehler else 0
    print("Messstellen gesamt: %d  (Pflicht %d, Zusatz %d; Zusatz nach Prioritaet %s)" % (
        len(PLAN["messstellen"]), z["stellen"]["pflicht"], z["stellen"]["zusatz"], dict(sorted(z["zusatz_prio"].items()))))
    print("Pflichtliste: %d Eintraege, %d ohne Pflicht-Messstelle" % (len(PLAN["pflichtliste"]), len(luecken)))
    print("\nSonden je Typ (Pflicht / Zusatz / gesamt):")
    for typ in PLAN["sondentypen"]:
        c = je_typ.get(typ, Counter())
        print("  %-18s %3d / %3d / %3d  %s" % (typ, c["pflicht"], c["zusatz"], c["pflicht"] + c["zusatz"], PLAN["sondentypen"][typ]["name"][:60]))
    for stufe in ("pflicht", "zusatz"):
        teile = ["%s %s-%s" % (w, "%.0f" % lo, "%.0f" % hi) for w, (lo, hi) in preis[stufe].items()]
        print("\nPreisspanne %s: %s; Atlas-Zubehoer (Schaltkreis + Isolator) %.0f USD; ohne Preis (offen): %d Stueck" % (stufe, ", ".join(teile), zubehoer[stufe], offen[stufe]))
    print("\nHalter (W35) Pflicht / Zusatz:")
    for h, c in sorted(halter.items()):
        print("  %-10s %2d / %2d  %s" % (h, c["pflicht"], c["zusatz"], PLAN["halter"][h][:70]))
    print("  H_BOX      %2d Messknoten-Gehaeuse (je Messknoten eines)" % len(PLAN["messknoten"]))
    print("\nMessknoten (Stellen, Stichleitungen/Adern zu den Sonden; Trunk zur Zentrale %d Adern Bus + 2 Adern 24 V; Leistung W):" % BUS_ADERN)
    for k, v in sorted(knoten.items()):
        print("  %-10s %2d Stellen, %2d Stichleitungen, %2d Adern, %2d W  %s" % (k, v["stellen"], v["leitungen"], v["adern"], PLAN["messknoten"][k]["leistung_w"], PLAN["messknoten"][k]["ort"][:45]))
    print("  Gesamt Messnetz: %d W (davon mk_puffer 5 W bereits in R27 enthalten)" % sum(v["leistung_w"] for v in PLAN["messknoten"].values()))
    print("\nZugang (Laufwegkarte Knie, %d Bauteile bekannt): erreichbar %d, KONFLIKT %d, umgangen %d, nicht pruefbar %d" % (len(erreichbar), len(ok), len(konflikt), len(umgangen), len(ungeprueft)))
    for i, b in konflikt:
        print("  KONFLIKT %s: Bauteil %s ist in der Laufwegkarte nicht erreichbar" % (i, b))
    for i, b in umgangen:
        print("  umgangen %s: Bauteil %s nicht erreichbar, Messung im Schaltschrank ohne Wartung vor Ort" % (i, b))
    nicht = [b for b, e in erreichbar.items() if not e]
    if nicht:
        print("  Hinweis: laut Karte nicht erreichbar: %s" % ", ".join(nicht))
    print("  nicht pruefbar (Bauteil nicht in der Karte oder ohne Bauteilbezug): %s" % ", ".join(ungeprueft))
    for h in hinweise:
        print("HINWEIS", h)
    for f in fehler:
        print("FEHLER", f)
    print("\n%s" % ("FEHLER: %d" % len(fehler) if fehler else "Pruefung bestanden"))
    return 1 if fehler else 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    sys.exit(main())
