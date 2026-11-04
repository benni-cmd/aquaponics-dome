"""N-STUECKLISTE 1b: Benennung unbenannter Koerper (Body<n>) und Schrauben-Namen nach Gestalt.

Regeln stehen als Daten in data/bom_regeln.json (Schluessel `benennung`). Die Funktion benenne() ist rein:
gleiche Eingabe, gleiche Ausgabe. Sie aendert keine .sc-Datei.

Ergebnis je Koerper (dict) oder None, wenn keine Regel passt:
  kind     schraube | mutter | scheibe
  name     z. B. Schraube_M6x40, Mutter_M6, Scheibe_M12
  gewinde  z. B. M6
  laenge   mm unter dem Kopf (nur Schraube)
  art_id   Artikel-ID des Schraubensatzes (nur Schraube), z. B. SRB-satz-m6x40
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REGELN = os.path.join(ROOT, "data", "bom_regeln.json")

_cache = {}


def regeln():
    if "r" not in _cache:
        _cache["r"] = json.load(open(REGELN, encoding="utf-8"))
    return _cache["r"]


def ist_unbenannt(name):
    return bool(re.match(r"body\d+$", re.sub(r" \(\d+\)", "", (name or "").lower())))


def _dims(b):
    return sorted(b["bbox_max"][i] - b["bbox_min"][i] for i in range(3))


def _naechster(tab, x):
    """naechster Schluessel der Tabelle (Zahl als Text) innerhalb 12 %"""
    best = min(tab, key=lambda k: abs(float(k) - x))
    return tab[best] if abs(float(best) - x) <= 0.12 * float(best) else None


def _satz(gew, laenge):
    return f"SRB-satz-{gew.lower()}x{laenge}"


def benenne(comp, b):
    R = regeln()["benennung"]
    f, tol = R["sechskant_faktor"], R["toleranz"]
    d0, d1, d2 = _dims(b)
    m = b.get("mass_g") or 0.0

    # Knotenbauteile: Masseklassen [A]
    kn = R["knoten_nach_masse"]
    if comp.startswith(kn["komponenten_praefix"]):
        for k in kn["klassen"]:
            if m >= k["masse_g_ab"]:
                return _ergebnis(k["kind"], k["gewinde"], k.get("laenge_mm"))
        return None

    # Sechskantschraube: d1/d0 = 1,155 (Schluesselweite, Eckenmass), lang
    if d0 > 0 and abs(d1 / d0 - f) / f <= tol and d2 >= 1.5 * d1:
        gew = _naechster(R["sw_zu_gewinde"], d0)
        if gew:
            kopf = R["kopfhoehe_mm"][gew]
            return _ergebnis("schraube", gew, int(round(d2 - kopf)))
    # Sechskantmutter: d2/d1 = 1,155, flach
    if d1 > 0 and abs(d2 / d1 - f) / f <= tol and d0 <= 1.2 * d1:
        gew = _naechster(R["sw_zu_gewinde"], d1)
        if gew:
            return _ergebnis("mutter", gew, None)
    # Scheibe: zwei gleiche grosse Masse, flach
    if d1 > 0 and abs(d2 - d1) / d1 <= R["scheibe_rund_toleranz"] and d0 <= R["scheibe_max_hoehe_anteil"] * d1:
        gew = _naechster(R["scheibe_od_zu_gewinde"], d1)
        if gew:
            return _ergebnis("scheibe", gew, None)
    return None


def _ergebnis(kind, gew, laenge):
    if kind == "schraube":
        return {"kind": kind, "name": f"Schraube_{gew}x{laenge}", "gewinde": gew, "laenge": laenge, "art_id": _satz(gew, laenge)}
    return {"kind": kind, "name": f"{'Mutter' if kind == 'mutter' else 'Scheibe'}_{gew}", "gewinde": gew, "laenge": None, "art_id": None}


def benenne_schraube_benannt(b):
    """Benannte Schrauben (Schraube_<Platte>_<x> aus tank.name_bolts): Gestalt wie unbenannt."""
    return benenne("tank", b)
