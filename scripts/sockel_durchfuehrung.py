"""N-UNIFY-AUTOBAHN U9 (D146): Durchfuehrungen der Ruecklauf-Schlaeuche (e33/e34, e49 bis e56) durch den Fundamentring zu den Sumpftanks aussen.

Vorher kreuzten die Schlaeuche den Fundamentring (T3_Sockel, Oberkante 650, Flur 400) schraeg auf Flurhoehe und lagen an den Zehneck-Ecken
mitten im Ring (check_latte U9: rund 400 Treffer Schlauch x T3_Sockel). Jetzt: je Sumpf-Zulauf (3 je Sumpf) eine Aussparung senkrecht
durch die Wandflaeche, die dem Zulauf am naechsten liegt; der Schlauch laeuft in der Schlauchgasse (Apothem R_GASSE) bis vor die Aussparung,
radial hindurch, aussen auf dem Gelaende zum Anlaufpunkt 400 mm vor dem Zulauf und dort in einem kurzen Graben auf die Zulaufhoehe.

Benutzt von scripts/trassen_soll.py (Schlauchweg) und scripts/gen_dome.py (Aussparung im Fundamentring, Graben in der Erdflaeche).
Aufruf: python -X utf8 scripts/sockel_durchfuehrung.py   (druckt die sechs Durchfuehrungen)"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_P = json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8"))
_v = lambda k: _P[k]["value"] if isinstance(_P[k], dict) else _P[k]
COS18 = math.cos(math.radians(18))
AP_IN = _v("dome_base_d") / 2 * COS18                     # Innenflaeche Fundamentring (Apothem, 5706)
AP_OUT = (_v("dome_base_d") / 2 + _v("sock_w")) * COS18    # Aussenflaeche (5944)
R_GASSE = 5560.0                                           # [A] Schlauchgasse vor der Kuppelwand (Apothem; Aussenbeete enden bei r ~5480), wie trassen_soll.R_WAND
AUSSEN_MIN = 40.0                                          # [A] mindestens so weit hinter der Aussenflaeche
AUSSEN_VOR = 150.0                                         # [A] gerades Stueck hinter der Aussenflaeche, bevor der Schlauch zum Zulauf abbiegt
ANLAUF = 400.0                                             # gerades Stueck vor dem Zulauf (wie trassen_soll)
OEFFNUNG_B, OEFFNUNG_H = 80.0, 80.0                        # [A] Aussparung je Zulauf (Schlauch ID25, AD 32, mit Spiel; Kernbohrung/Leerrohr DN 70 in der Praxis)
GRABEN_B = 80.0                                            # [A] Grabenbreite fuer den letzten Anlauf unter Gelaende
PORTS = json.load(open(os.path.join(ROOT, "data", "becken-ports.json"), encoding="utf-8"))


def welt(fa, ap, t):
    """Punkt in Flaechenkoordinaten (Flaechennormale fa Grad, Apothem ap, tangential t) -> Welt (x, y)."""
    a = math.radians(fa)
    return (ap * math.cos(a) - t * math.sin(a), ap * math.sin(a) + t * math.cos(a))


def ecke(az, ap=R_GASSE):
    """Ecke des Zehnecks mit Apothem ap auf Azimut az (Ecken auf 18 + 36 k)."""
    r = ap / COS18
    return (r * math.cos(math.radians(az)), r * math.sin(math.radians(az)))


def fuer_zulauf(port, richtung):
    """Durchfuehrung fuer einen Sumpf-Zulauf: dict mit Flaeche fa, Tangente t, Innenpunkt (Gasse), Aussenpunkt, Anlaufpunkt zq (alle x, y)."""
    zq = (port[0] - richtung[0] * ANLAUF, port[1] - richtung[1] * ANLAUF)
    fa = 36.0 * round(math.degrees(math.atan2(zq[1], zq[0])) / 36.0)
    a = math.radians(fa)
    t = -zq[0] * math.sin(a) + zq[1] * math.cos(a)
    t_max = R_GASSE * math.tan(math.radians(18)) - 250.0      # [A] mindestens 250 mm von der Ecke (Basisknoten, Anker, Schere)
    t = max(-t_max, min(t_max, t))
    ap_zq = zq[0] * math.cos(a) + zq[1] * math.sin(a)
    ap_a = max(AP_OUT + AUSSEN_MIN, min(AP_OUT + AUSSEN_VOR, ap_zq))   # nie hinter den Anlaufpunkt (sonst wendet der Schlauch)
    return {"fa": fa, "t": round(t, 1), "ap_aussen": ap_a, "innen": welt(fa, R_GASSE, t), "aussen": welt(fa, ap_a, t), "zq": zq}


def liste():
    """Alle Sumpf-Zulaeufe der Quelle (data/becken-ports.json sumpf_zulaeufe), je eine Durchfuehrung."""
    out = []
    for z in PORTS["sumpf_zulaeufe"]:
        d = fuer_zulauf(z["port_mm"], z["richtung"]); d["name"] = z["name"]; d["port"] = tuple(z["port_mm"]); out.append(d)
    return out


def _abstand(ds):
    """Liegen zwei Durchfuehrungen derselben Flaeche naeher als ABSTAND (Klemmung an der Ecke), rueckt die spaetere zur Flaechenmitte."""
    for i, d in enumerate(ds):
        for e in ds[:i]:
            if e["fa"] == d["fa"] and abs(e["t"] - d["t"]) < ABSTAND:
                d["t"] = round(e["t"] - math.copysign(ABSTAND, e["t"]), 1)
                d["innen"], d["aussen"] = welt(d["fa"], R_GASSE, d["t"]), welt(d["fa"], d["ap_aussen"], d["t"])
    return ds


ABSTAND = 200.0   # [A] Mitte zu Mitte zweier Aussparungen


def fuer(port):
    """Durchfuehrung zum Zulauf mit dieser Port-Lage (nach Abstandsregel)."""
    return next(d for d in _abstand(liste()) if math.dist(d["port"][:2], port[:2]) < 1.0)


def schnitte(sock_z):
    """Quader (name, cx, cy, z0, az, laenge, breite, hoehe) fuer gen_dome.rect_body: Aussparung im Fundamentring und Graben vor dem Zulauf."""
    ring, graben = [], []
    for k, d in enumerate(_abstand(liste()), 1):
        cx, cy = welt(d["fa"], (AP_IN + AP_OUT) / 2, d["t"])
        ring.append((f"T3_Durchfuehrung_{k:02d}", round(cx, 1), round(cy, 1), sock_z - 10, d["fa"], AP_OUT - AP_IN + 40, OEFFNUNG_B, OEFFNUNG_H + 10))
        (x0, y0), (x1, y1, z1) = d["zq"], d["port"]
        L = math.hypot(x1 - x0, y1 - y0); az = math.degrees(math.atan2(y1 - y0, x1 - x0))
        z_unten = z1 - 16 - 20                                       # Schlauch AD 32 + 20 mm Bettung
        graben.append((f"T13_Graben_Sumpf_{k:02d}", round((x0 + x1) / 2, 1), round((y0 + y1) / 2, 1), round(z_unten, 1), az, round(L + GRABEN_B, 1), GRABEN_B, round(sock_z - z_unten + 5, 1)))
    return ring, graben


if __name__ == "__main__":
    for d in _abstand(liste()):
        print(d["name"], "Flaeche %+.0f Grad, t %+.0f mm, innen (%.0f, %.0f), aussen (%.0f, %.0f)" % (d["fa"], d["t"], *d["innen"], *d["aussen"]))
    r, g = schnitte(400.0)
    print(len(r), "Aussparungen im Fundamentring,", len(g), "Graeben; AP_IN %.0f AP_OUT %.0f" % (AP_IN, AP_OUT))
