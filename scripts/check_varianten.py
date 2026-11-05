"""N-VARIANTEN: Pruefung des Zusammenspiels der Kreislauf-Varianten (Blatt docs/jobs/N-VARIANTEN.md, Pruefpunkte P1 bis P3).

Aufruf:
  python -X utf8 scripts/check_varianten.py                    # V1a-Pruefungen (Schalter, Pfade, Filter, Kennzahlen) + Ausgaben-Stand je Variante
  python -X utf8 scripts/check_varianten.py --a-plus-gleich    # P1: bom.py ohne Schalter = bom.py --variante a_plus (Kopie, BOM_ROOT), byte-gleich
  python -X utf8 scripts/check_varianten.py --streng           # P2: auch fehlende Ausgaben von Ring B2 (Modell noch nicht gebaut) sind FAIL
Exit 0 = alle Pruefungen PASS. Ausgaben von Ring B2, die erst die Montage R1/R2 erzeugt, stehen ohne --streng als OFFEN (kein FAIL).
Das Repo wird nicht veraendert (alle Laeufe in einer Kopie im Temp-Ordner).
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import variante as V  # noqa: E402

ROOT = os.path.dirname(HERE)
ERG = []
STRENG = "--streng" in sys.argv
HEUTE = {"dome_script": "scripts/dome-script.json", "modell": "designs/dome.sc", "instances": "viewer/instances.json", "extras": "viewer/extras.json",
         "ansicht": "viewer/ansicht.json", "stueckliste_json": "data/stueckliste.json", "stueckliste_md": "docs/stueckliste.md",
         "einkaufsliste": "docs/einkaufsliste.html", "system_specs": "data/system-specs.json"}


def check(nr, text, ok, detail="", offen=False):
    ERG.append((nr, text, bool(ok), offen))
    print(("PASS " if ok else ("OFFEN " if offen else "FAIL ")) + f"{nr:>2} {text}" + (f"  [{detail}]" if detail else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def jl(p):
    return json.load(open(p, encoding="utf-8"))


def rel(p):
    return os.path.relpath(p, ROOT).replace("\\", "/")


def schalter():
    # Rangfolge: Kommandozeile > Umgebung > params.json
    alt = os.environ.pop("KREISLAUF_VARIANTE", None)
    try:
        std = V.aktiv(["x"])
        a = V.aktiv(["x", "--variante", "ring_b2"])
        b = V.aktiv(["x", "--variante=ring_b2"])
        os.environ["KREISLAUF_VARIANTE"] = "ring_b2"
        e = V.aktiv(["x"])
        vorrang = V.aktiv(["x", "--variante", "a_plus"])
        try:
            V.aktiv(["x", "--variante", "quatsch"])
            unbekannt = False
        except SystemExit:
            unbekannt = True
    finally:
        os.environ.pop("KREISLAUF_VARIANTE", None)
        if alt is not None:
            os.environ["KREISLAUF_VARIANTE"] = alt
    p = jl(os.path.join(ROOT, "data", "params.json"))["kreislauf_variante"]
    check(1, "Schalter: Kommandozeile vor Umgebung vor params.json; unbekannter Wert bricht ab",
          std == p["value"] == "a_plus" and a == b == "ring_b2" and e == "ring_b2" and vorrang == "a_plus" and unbekannt,
          f"Standard {std}, --variante {a}, Umgebung {e}, Vorrang {vorrang}, unbekannt abgelehnt {unbekannt}")


def pfade():
    abw = [(k, rel(V.pfad(k, "a_plus", root=ROOT))) for k, r in HEUTE.items() if rel(V.pfad(k, "a_plus", root=ROOT)) != r]
    check(2, "Pfade A+ = heutige Pfade (nichts bricht)", not abw, str(abw))
    b = {k: rel(V.pfad(k, "ring_b2", root=ROOT)) for k in HEUTE}
    eigen = len(set(b.values())) == len(b) and not set(b.values()) & set(HEUTE.values())
    check(3, "Pfade Ring B2: alle eigen, keiner gleich einem A+-Pfad", eigen, f"{len(set(b.values()))} verschiedene von {len(b)}")


def filter_():
    e = [{"id": 1}, {"id": 2, "varianten": ["a_plus"]}, {"id": 3, "varianten": ["ring_b2"]}, {"id": 4, "varianten": ["a_plus", "ring_b2"]}]
    ok = [x["id"] for x in V.filtere(e, "a_plus")] == [1, 2, 4] and [x["id"] for x in V.filtere(e, "ring_b2")] == [1, 3, 4]
    check(4, "gilt/filtere: ohne Feld beide, sonst nur Listenwerte", ok)
    t = jl(os.path.join(ROOT, "data", "leitungstrassen.json"))["trassen"]
    n = jl(os.path.join(ROOT, "data", "leitungsnetz.json"))["kanten"]
    gem = len(V.filtere(t, "a_plus")), len(V.filtere(t, "ring_b2")), len(V.filtere(n, "a_plus")), len(V.filtere(n, "ring_b2"))
    markiert = sum(1 for x in t + n if x.get("varianten"))
    check(5, "Filter auf den echten Daten: ohne Markierung gelten alle Trassen und Kanten in beiden Varianten",
          markiert > 0 or (gem[0] == gem[1] == len(t) and gem[2] == gem[3] == len(n)),
          f"Trassen {gem[0]}/{gem[1]} von {len(t)}, Kanten {gem[2]}/{gem[3]} von {len(n)}, markiert {markiert}")


def kennzahlen():
    pa, pb = V.pfad("system_specs", "a_plus", root=ROOT), V.pfad("system_specs", "ring_b2", root=ROOT)
    if not (os.path.exists(pa) and os.path.exists(pb)):
        check(6, "Kennzahlen: system-specs.json und system-specs-ring_b2.json mit Block kreislauf", False, "Datei fehlt: scripts/system_specs.py [--variante ring_b2] ausfuehren")
        return
    a, b = jl(pa), jl(pb)
    ka, kb = a.pop("kreislauf", None), b.pop("kreislauf", None)
    ok = ka and kb and ka["variante"] == "a_plus" and kb["variante"] == "ring_b2" and ka["pumpenleistung_el_w_eta25"] == 430 and kb["pumpenleistung_el_w_eta25"] == 577
    check(6, "Kennzahlen: Block kreislauf je Variante (A+ 430 W, Ring B2 577 W)", ok, "" if ok else "Block fehlt oder Werte falsch")
    check(7, "Kennzahlen: ausser dem Block sind beide Dateien gleich (kein zweiter Rechenweg)", a == b)


def ausgaben():
    mod_t = {}
    for v in V.VARIANTEN:
        p = V.pfad("modell", v, root=ROOT)
        mod_t[v] = os.path.getmtime(p) if os.path.exists(p) else None
    for v in V.VARIANTEN:
        fehlt, alt = [], []
        for art in ("dome_script", "modell", "instances", "extras", "ansicht", "stueckliste_json", "einkaufsliste", "system_specs"):
            p = V.pfad(art, v, root=ROOT)
            if not os.path.exists(p):
                fehlt.append(art)
            elif mod_t[v] and art not in ("dome_script", "modell", "system_specs") and os.path.getmtime(p) < mod_t[v] - 1:
                alt.append(art)
        ok = not fehlt and not alt
        detail = ("fehlt: " + ", ".join(fehlt) if fehlt else "") + ("; aelter als das Modell: " + ", ".join(alt) if alt else "")
        check("8a" if v == "a_plus" else "8b", f"Ausgaben {v}: alle 8 Ausgaben aus Tabelle 1.3 vorhanden und nicht aelter als das Modell", ok, detail,
              offen=(v == "ring_b2" and not STRENG and bool(fehlt) and mod_t[v] is None))


def a_plus_gleich():
    """P1 (Teil bom): bom.py ohne Schalter und mit --variante a_plus erzeugen in einer Kopie dieselben Bytes; die Zeilen gleichen dem Repo."""
    import check_bom as CB  # nur kopie_anlegen; main() laeuft nicht
    tmps = []
    try:
        ergebnisse = []
        for argv in ([], ["--variante", "a_plus"]):
            tmp = tempfile.mkdtemp()
            tmps.append(tmp)
            CB.kopie_anlegen(tmp)
            env = {k: v for k, v in os.environ.items() if k != "KREISLAUF_VARIANTE"}
            env["BOM_ROOT"] = tmp
            r = subprocess.run([sys.executable, "-X", "utf8", os.path.join(HERE, "bom.py")] + argv, env=env, capture_output=True, text=True)
            h = {}
            for k, rp in (("json", "data/stueckliste.json"), ("md", "docs/stueckliste.md"), ("html", "docs/einkaufsliste.html")):
                pp = os.path.join(tmp, *rp.split("/"))
                if os.path.exists(pp):
                    h[k] = sha(pp)
            ergebnisse.append((r.returncode, h))
        gleich = ergebnisse[0] == ergebnisse[1] and ergebnisse[0][0] == 0 and len(ergebnisse[0][1]) == 3
        check(9, "P1: bom.py ohne Schalter = bom.py --variante a_plus (stueckliste.json, stueckliste.md, einkaufsliste.html byte-gleich, Kopie)", gleich,
              ", ".join(f"{k} {v[:10]}" for k, v in ergebnisse[0][1].items()))
        tmp = tmps[0]
        repo = jl(V.pfad("stueckliste_json", "a_plus", root=ROOT))["zeilen"]
        neu = jl(os.path.join(tmp, "data", "stueckliste.json"))["zeilen"]
        check(10, "P1: Zeilen der Kopie = Zeilen im Repo (sonst Modelldrift oder Liste nicht neu erzeugt)", repo == neu, f"{len(neu)} Zeilen")
        kopf = jl(os.path.join(tmp, "data", "stueckliste.json"))["kopf"]
        check(11, "P1: A+-Kopf traegt kein Feld `variante`", "variante" not in kopf)
    finally:
        for t in tmps:
            shutil.rmtree(t, ignore_errors=True)


def main():
    print("Aktive Variante (Standard):", V.aktiv())
    schalter()
    pfade()
    filter_()
    kennzahlen()
    ausgaben()
    if "--a-plus-gleich" in sys.argv:
        a_plus_gleich()
    nf = [e for e in ERG if not e[2] and not e[3]]
    offen = [e for e in ERG if not e[2] and e[3]]
    print(f"\n{sum(1 for e in ERG if e[2])} PASS, {len(offen)} OFFEN, {len(nf)} FAIL von {len(ERG)} Pruefungen")
    sys.exit(1 if nf else 0)


if __name__ == "__main__":
    main()
