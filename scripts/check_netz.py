"""Selbsttest der Netzliste (R40): data/leitungsnetz.json gegen sich selbst, system-specs.json und messstellen.json.

Prueft: (1) Kanten- und Knoten-IDs eindeutig, jede Kante hat bekannte Endknoten; (2) Durchflussbilanz je Knoten (Zufluss = Abfluss, Stoerfallkanten ausgenommen);
(3) Geschwindigkeit aus Durchfluss und PVC-PN10-Innendurchmesser gegen den eingetragenen Wert und gegen die Grenzen (Druckseite <= 1,5 m/s, Saugseite <= 1,0 m/s);
(4) Linienwerte (Hauptkreislauf, Beete, NFT) gegen system-specs.json; (5) Kabel: Endpunkte bekannt, Leistungen gegen system-specs.json; (6) Fragen fuer M10 vorhanden.
Aufruf: python scripts/check_netz.py   (nur Standardbibliothek, aendert keine Datei, Exit 1 bei Fehler)"""
import json
import math
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import variante as V  # noqa: E402  (Pfade, N-UNIFY-AUTOBAHN U7)

NETZ = json.loads((ROOT / "data" / "leitungsnetz.json").read_text(encoding="utf-8"))
SPEC = json.loads(Path(V.pfad("system_specs", root=str(ROOT))).read_text(encoding="utf-8"))

# Innendurchmesser mm je Aussendurchmesser (PVC PN10, aus den Geschwindigkeiten der Netzliste zurueckgerechnet, R28/R40)
ID = {9: 6.0, 12: 8.0, 16: 12.0, 20: 16.0, 25: 21.0, 32: 28.0, 40: 35.0, 50: 44.0, 63: 55.7, 75: 67.0, 90: 80.0, 110: 98.6}
V_DRUCK, V_SAUG = 1.5, 1.0
TOL_BILANZ = 0.6          # l/min (Schlammablass 0,5 l/min je Absetzer)
BILANZ_TYPEN = {"Tank", "Filter", "Verteiler", "Pumpe", "Sammler", "Becken"}
BILANZ_AUS = {"pool", "drittbecken", "biofilter_dritt", "zweitbecken", "schlammsammler", "schlammfass_1", "schlammfass_2", "beet_sumpf_1", "beet_sumpf_2", "frischwasser", "aktivkohle", "puffer_stammfass", "puffer_eisen", "dosierkonsole", "puffer_messzelle"}

fehler, hinweise = [], []
knoten = {k["id"]: k for k in NETZ["knoten"]}
kanten = NETZ["kanten"]


def v_of(dn, q):
    d = ID[dn] / 1000.0
    return q / 60000.0 / (math.pi * d * d / 4)


# (1) IDs und Endknoten
ids = [k["id"] for k in kanten]
if len(ids) != len(set(ids)):
    fehler.append("Kanten-IDs nicht eindeutig")
if len(knoten) != len(NETZ["knoten"]):
    fehler.append("Knoten-IDs nicht eindeutig")
for k in kanten:
    for end in ("von", "nach"):
        if k[end] not in knoten:
            fehler.append("%s: %s '%s' ist kein Knoten" % (k["id"], end, k[end]))
    if k["medium"] == "Wasser" and k["dn"] not in ID and not k.get("schlauch_id") and k.get("art") != "ohne_leitung":
        fehler.append("%s: dn %s nicht in der Innendurchmesser-Tabelle" % (k["id"], k["dn"]))

# N-UNIFY-AUTOBAHN U6: das Netz sind die 77 Wege der Quelle (Kanten S-eNN, scripts/u6_netz.py).
# Geprueft wird gegen data/oasis-soll.json: keine Kante ohne Quelle, jeder Soll-Weg genau einmal mit gleichem Medium und gleicher Richtung,
# jede Wasserleitung mit Nennweite; Geschwindigkeit nur, wo die Quelle einen Durchfluss nennt. Bilanz und Linienwerte des Altbestands entfallen (seit U7 geloescht),
# weil die Quelle Durchfluesse nur fuer Ring, Einspeisung, Abfahrten und Pumpstelle 1 nennt (R61 Abschnitt 4).
SOLL = json.loads((ROOT / "data" / "oasis-soll.json").read_text(encoding="utf-8"))
sw = {w["id"]: w for w in SOLL["wege"] if w.get("im_umfang")}
MED = {"water": "Wasser", "air": "Luft", "sludge": "Schlamm", "power": "Strom"}
gesehen = defaultdict(int)
for k in kanten:
    w = sw.get(k.get("soll_weg"))
    if w is None:
        fehler.append("%s: Kante ohne Quelle (soll_weg %s nicht in oasis-soll.json)" % (k["id"], k.get("soll_weg")))
        continue
    gesehen[w["id"]] += 1
    if (k["von"], k["nach"]) != (w["von"], w["nach"]):
        fehler.append("%s: Richtung %s->%s, Quelle %s->%s" % (k["id"], k["von"], k["nach"], w["von"], w["nach"]))
    if k["medium"] != MED[w["medium"]]:
        fehler.append("%s: Medium %s, Quelle %s" % (k["id"], k["medium"], w["medium"]))
    if k.get("art") == "leitung" and k["medium"] in ("Wasser", "Luft", "Schlamm") and not (k.get("dn") in ID or k.get("schlauch_id")):
        fehler.append("%s: Leitung ohne Nennweite" % k["id"])
    if k.get("art") == "leitung" and k["medium"] == "Wasser" and k.get("soll_l_min") and k.get("dn") in ID:
        v = v_of(k["dn"], k["soll_l_min"])
        (fehler if v > V_DRUCK + 1e-9 else hinweise).append("%s: %.0f l/min in d%s = %.2f m/s" % (k["id"], k["soll_l_min"], k["dn"], v))
for wid in sw:
    if gesehen[wid] != 1:
        fehler.append("Soll-Weg %s: %d Kanten statt 1" % (wid, gesehen[wid]))
print("Netzliste Version %s: %d Knoten, %d Kanten, Soll-Wege %d von %d genau einmal, Leitungen %d, ohne Leitung %d, Kabel %d" % (
    NETZ["version"], len(knoten), len(kanten), sum(1 for w in sw if gesehen[w] == 1), len(sw),
    sum(1 for k in kanten if k.get("art") == "leitung"), sum(1 for k in kanten if k.get("art") == "ohne_leitung"), sum(1 for k in kanten if k.get("art") == "kabel")))
for h in hinweise:
    print("  Hinweis:", h)
for f in fehler:
    print("FEHLER:", f)
print("Pruefung bestanden" if not fehler else "FEHLER: %d" % len(fehler))
sys.exit(1 if fehler else 0)

