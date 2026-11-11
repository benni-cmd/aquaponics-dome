"""N-VARIANTEN V1a: die EINE Stelle fuer die Kreislauf-Variante (`a_plus` | `ring_b2`), Blatt docs/jobs/N-VARIANTEN.md Abschnitt 1.

Schalter, in dieser Rangfolge:
  1. Kommandozeile `--variante <v>` oder `--variante=<v>`
  2. Umgebungsvariable KREISLAUF_VARIANTE
  3. Standard aus data/params.json `kreislauf_variante.value` (fehlt der Eintrag: a_plus)
Gebaut und exportiert wird nie durch Aendern von params.json; die Datei liefert nur den Standard.

Funktionen:
  aktiv(argv=None)          -> Name der aktiven Variante
  gilt(eintrag, v=None)     -> True, wenn der Eintrag (dict mit optionalem Feld `varianten`) fuer v gilt
  pfad(art, v=None, root=None) -> Ausgabepfad nach Tabelle 1.3 (a_plus: heutige Pfade, nie veraendert)
  filtere(eintraege, v=None)   -> Liste der Eintraege, die fuer v gelten
  variante_aus_pfad(...) gibt es nicht: kein Skript baut Pfade selbst zusammen.

Aufruf als Skript: `python -X utf8 scripts/variante.py [--variante v]` druckt die aktive Variante und alle Pfade.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("BOM_ROOT") or os.path.dirname(HERE)  # BOM_ROOT: Testkopie (check_bom.py, check_varianten.py)

VARIANTEN = ("a_plus", "ring_b2")
STANDARD = "a_plus"

# Tabelle 1.3: Art -> (Pfad A+, Pfad Ring B2), relativ zum Projektordner.
_PFADE = {
    "dome_script": ("scripts/dome-script.json", "scripts/dome-script-ring_b2.json"),
    "modell": ("designs/dome.sc", "designs/dome-ring_b2.sc"),
    "bilder_dir": ("renders", "renders/ring_b2"),
    "viewer_dir": ("viewer", "viewer/varianten/ring_b2"),
    "instances": ("viewer/instances.json", "viewer/varianten/ring_b2/instances.json"),
    "extras": ("viewer/extras.json", "viewer/varianten/ring_b2/extras.json"),
    "ansicht": ("viewer/ansicht.json", "viewer/varianten/ring_b2/ansicht.json"),
    "stueckliste_json": ("data/stueckliste.json", "data/stueckliste-ring_b2.json"),
    "stueckliste_md": ("docs/stueckliste.md", "docs/stueckliste-ring_b2.md"),
    "einkaufsliste": ("docs/einkaufsliste.html", "docs/einkaufsliste-ring_b2.html"),
    "system_specs": ("data/system-specs.json", "data/system-specs-ring_b2.json"),
}
# Nur eine Datei fuer beide Varianten (Vergleich) und Geometrie, die gemeinsam bleibt (kein Variantenpfad).
_GEMEINSAM = {
    "vergleich": "docs/varianten-vergleich.md",
    "defs_dir": "viewer/defs",
    "detail_dir": "viewer/detail",
    "params": "data/params.json",
}


def _pruefen(v):
    if v not in VARIANTEN:
        raise SystemExit("Unbekannte Kreislauf-Variante %r; erlaubt: %s" % (v, ", ".join(VARIANTEN)))
    return v


def _aus_params(root=None):
    p = os.path.join(root or ROOT, "data", "params.json")
    try:
        with open(p, encoding="utf-8") as f:
            return json.load(f).get("kreislauf_variante", {}).get("value", STANDARD)
    except (OSError, ValueError):
        return STANDARD


def aktiv(argv=None):
    argv = sys.argv if argv is None else argv
    for i, a in enumerate(argv):
        if a == "--variante" and i + 1 < len(argv):
            return _pruefen(argv[i + 1])
        if a.startswith("--variante="):
            return _pruefen(a.split("=", 1)[1])
    env = os.environ.get("KREISLAUF_VARIANTE")
    if env:
        return _pruefen(env)
    return _pruefen(_aus_params())


def gilt(eintrag, v=None):
    """Eintrag ohne Feld `varianten` gilt fuer alle; sonst nur, wenn v in der Liste steht. Steht v in `entfaellt_in`, gilt der Eintrag dort nicht (U5, D127)."""
    v = _pruefen(v or aktiv())
    if isinstance(eintrag, dict) and v in (eintrag.get("entfaellt_in") or ()):   # N-UNIFY U5 (D127): Eintrag entfaellt in dieser Variante (nichts geloescht, Grund im Feld `entfaellt_grund`)
        return False
    vs = eintrag.get("varianten") if isinstance(eintrag, dict) else None
    return True if not vs else v in vs


def filtere(eintraege, v=None):
    v = _pruefen(v or aktiv())
    return [e for e in eintraege if gilt(e, v)]


def parameter(v=None, root=None):
    """D119 (N-UNIFY U3): data/params.json als flaches Dict {name: wert} fuer die Variante v.
    Eintraege mit Liste `varianten` gelten nur dort (gilt()); `varianten_werte` {v: x} ueberschreibt `value`.
    a_plus liefert damit exakt die Werte vor U3; ring_b2 die Soll-Werte der Oasis-Quelle (data/oasis-soll.json)."""
    v = _pruefen(v or aktiv())
    with open(os.path.join(root or ROOT, "data", "params.json"), encoding="utf-8") as f:
        d = json.load(f)
    out = {}
    for k, e in d.items():
        if not isinstance(e, dict) or "value" not in e or not gilt(e, v):
            continue
        out[k] = e.get("varianten_werte", {}).get(v, e["value"])
    return out


def pfad(art, v=None, root=None):
    root = root or ROOT
    if art in _GEMEINSAM:
        return os.path.join(root, *_GEMEINSAM[art].split("/"))
    if art not in _PFADE:
        raise KeyError("Unbekannte Ausgabeart %r; bekannt: %s" % (art, ", ".join(sorted(list(_PFADE) + list(_GEMEINSAM)))))
    v = _pruefen(v or aktiv())
    rel = _PFADE[art][0 if v == "a_plus" else 1]
    return os.path.join(root, *rel.split("/"))


def alle_pfade(v):
    return {a: pfad(a, v) for a in list(_PFADE) + list(_GEMEINSAM)}


if __name__ == "__main__":
    v = aktiv()
    print("Variante:", v)
    for a, p in alle_pfade(v).items():
        print("  %-18s %s" % (a, os.path.relpath(p, ROOT)))
