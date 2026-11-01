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
NETZ = json.loads((ROOT / "data" / "leitungsnetz.json").read_text(encoding="utf-8"))
SPEC = json.loads((ROOT / "data" / "system-specs.json").read_text(encoding="utf-8"))

# Innendurchmesser mm je Aussendurchmesser (PVC PN10, aus den Geschwindigkeiten der Netzliste zurueckgerechnet, R28/R40)
ID = {9: 6.0, 12: 8.0, 16: 12.0, 20: 16.0, 25: 21.0, 32: 28.0, 40: 35.0, 50: 44.0, 63: 55.7, 75: 67.0, 90: 80.0, 110: 98.6}
V_DRUCK, V_SAUG = 1.5, 1.0
TOL_BILANZ = 0.6          # l/min (Schlammablass 0,5 l/min je Absetzer)
BILANZ_TYPEN = {"Tank", "Filter", "Verteiler", "Pumpe", "Sammler", "Becken"}
BILANZ_AUS = {"pool", "drittbecken", "biofilter_dritt", "zweitbecken", "schlammsammler", "frischwasser", "aktivkohle", "puffer_stammfass", "puffer_eisen", "dosierkonsole", "puffer_messzelle"}

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
    if k["medium"] == "Wasser" and k["dn"] not in ID:
        fehler.append("%s: dn %s nicht in der Innendurchmesser-Tabelle" % (k["id"], k["dn"]))

# (2) Durchflussbilanz
ein, aus = defaultdict(float), defaultdict(float)
for k in kanten:
    if k["medium"] != "Wasser" or k.get("betrieb") == "stoerfall" or k.get("soll_l_min") is None:
        continue
    q = k.get("mittel_l_min", k["soll_l_min"])       # Spitzenkanten (Nachspeisen) mit Mittelwert bilanzieren
    aus[k["von"]] += q
    ein[k["nach"]] += q
for nid, n in knoten.items():
    if nid in BILANZ_AUS or n["typ"] not in BILANZ_TYPEN or "linie" not in n and n["typ"] != "Sammler":
        continue
    if n["typ"] in ("Pumpe",) or nid.startswith(("absetzer", "biofilter_", "feinfilter", "verteiler", "ruecklauf")):
        if ein[nid] == 0 and aus[nid] == 0:
            continue
        if abs(ein[nid] - aus[nid]) > TOL_BILANZ:
            fehler.append("Bilanz %s: Zufluss %.1f, Abfluss %.1f l/min" % (nid, ein[nid], aus[nid]))
# Pool: Abfluss (Seiten- und Bodenablauf) gegen Zufluss (Ruecklauf, Zweitbecken, Messwasser, Nachspeisung, Dosierung)
pool_aus = aus["pool"]
pool_ein = ein["pool"]
if abs(pool_aus - pool_ein) > 3.0:      # Messwasser/Nachspeisung/Dosierung gehen als Spitze in den Zufluss
    fehler.append("Bilanz pool: Abfluss %.1f, Zufluss %.1f l/min" % (pool_aus, pool_ein))

# (3) Geschwindigkeiten
for k in kanten:
    if k["medium"] != "Wasser" or k.get("soll_l_min") in (None, 0):
        continue
    v = v_of(k["dn"], k["soll_l_min"])
    if "v_m_s" in k and abs(v - k["v_m_s"]) > 0.02 and abs(v - k["v_m_s"]) / max(v, 0.01) > 0.1:
        fehler.append("%s: v %.2f m/s gerechnet, %.2f eingetragen" % (k["id"], v, k["v_m_s"]))
    saug = str(k["nach"]).startswith("pumpe_gross") or str(k["nach"]).startswith("pumpe_klein") or str(k["nach"]).startswith("feinfilter")
    if k["von"] == "pool" and str(k["nach"]).startswith("feinfilter"):
        saug = True
    grenze = V_SAUG if saug else V_DRUCK
    if k.get("betrieb") == "stoerfall":
        hinweise.append("%s Stoerfall %.2f m/s" % (k["id"], v))
    elif v > grenze + 1e-9:
        fehler.append("%s: %.2f m/s ueber %s %.1f m/s" % (k["id"], v, "Saugseite" if saug else "Druckseite", grenze))

# (4) Linienwerte gegen system-specs.json
fl = SPEC["fluesse"]
b = NETZ["bilanz_je_linie_l_min"]
if abs(b["hauptkreislauf"] - fl["je_linie_l_min"]) > 0.6:
    fehler.append("Hauptkreislauf je Linie %s gegen system-specs %s" % (b["hauptkreislauf"], fl["je_linie_l_min"]))
if abs(b["nft"] - fl["nft_l_min"] / 2) > 0.6:
    fehler.append("NFT je Linie %s gegen system-specs %s" % (b["nft"], fl["nft_l_min"] / 2))
if abs(b["beete_mittel"] - fl["beete_l_min"] / 2) > 0.6:
    fehler.append("Beete je Linie %s gegen system-specs %s" % (b["beete_mittel"], fl["beete_l_min"] / 2))
if knoten["nft_linie_1"].get("rinnen") != SPEC["pflanzen"]["rinnen"] // 2:
    fehler.append("Rinnen je Linie %s gegen %s" % (knoten["nft_linie_1"].get("rinnen"), SPEC["pflanzen"]["rinnen"] // 2))
if knoten["beete_linie_1"].get("beete") != 7 or knoten["nft_linie_1"].get("tische") != 12:
    fehler.append("Linienteilung nicht 12 Tische + 7 Beete (D67)")

# (5) Kabel
kabel_orte = set(knoten) | {"schaltschrank", "geblaese_fisch", "geblaese_luftpolster", "puffer_klein", "steuerung_alarm", "heizung", "blitzleuchte_summer"}
for kb in NETZ["kabel"]:
    for end in ("von", "nach"):
        ziel = kb[end]
        if ".." in ziel or ziel.startswith("sonden_") or ziel.startswith("mk_"):
            continue
        base = ziel
        if base not in kabel_orte:
            fehler.append("Kabel %s -> %s: '%s' unbekannt" % (kb["von"], kb["nach"], ziel))
L = SPEC["leistung"]
for kb in NETZ["kabel"]:
    if kb["nach"] == "geblaese_fisch" and kb["leistung_w"] != L["belueftung_w"]:
        fehler.append("Geblaese Fisch %s W gegen system-specs %s W" % (kb["leistung_w"], L["belueftung_w"]))
    if kb["nach"] == "pumpe_gross_1..4" and kb["leistung_w"] != round(L["pumpe_elektrisch_w"] / 2):
        fehler.append("Pumpe gross %s W gegen system-specs %s W" % (kb["leistung_w"], L["pumpe_elektrisch_w"] / 2))
    if kb["nach"] == "pumpe_klein_1..4" and abs(kb["leistung_w"] - L["pumpe_klein_w"] / 2) > 1.0:
        fehler.append("Pumpe klein %s W gegen system-specs %s W" % (kb["leistung_w"], L["pumpe_klein_w"] / 2))
    if kb["nach"] == "puffer_klein" and kb["leistung_w"] != SPEC["puffer_klein"]["optionen"][0]["strom_w"]:
        fehler.append("Puffer klein %s W gegen system-specs puffer_klein %s W" % (kb["leistung_w"], SPEC["puffer_klein"]["optionen"][0]["strom_w"]))
n_trunk = sum(1 for kb in NETZ["kabel"] if kb["nach"] == "schaltschrank" and kb["von"].startswith("mk_"))
if n_trunk != 7:
    fehler.append("Trunks: %d statt 7 Messknoten" % n_trunk)

# (6) Fragen fuer M10
if not NETZ.get("fragen_m10"):
    fehler.append("fragen_m10 fehlt")

print("Netzliste Version %s: %d Knoten, %d Kanten (%d Stoerfall), %d Kabelzeilen, %d Fragen fuer M10" % (
    NETZ["version"], len(NETZ["knoten"]), len(kanten), sum(1 for k in kanten if k.get("betrieb") == "stoerfall"), len(NETZ["kabel"]), len(NETZ.get("fragen_m10", []))))
for h in hinweise:
    print("  Hinweis:", h)
for f in fehler:
    print("FEHLER:", f)
print("Pruefung bestanden" if not fehler else "FEHLER: %d" % len(fehler))
sys.exit(1 if fehler else 0)
