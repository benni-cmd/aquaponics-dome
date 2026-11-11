"""Feste Ausgabepfade und Parameter des EINEN Kreislaufs nach Leons Oasis-Quelle (D93).

N-UNIFY-AUTOBAHN U7 (D141): Der Variantenschalter von N-VARIANTEN (zwei Kreislaeufe, Schalter auf der Kommandozeile,
in der Umgebung und in params.json) ist abgeloest. Der Modulname bleibt, damit die Aufrufer nur die Pfade lesen.
Die Daten tragen keine Variantenmarken mehr (Umstellung U7, Stand im Paket docs/packages/n-unify-autobahn.md).

Funktionen (das Argument v frueherer Aufrufe wird nicht mehr gebraucht und entfaellt):
  pfad(art, root=None) -> Ausgabepfad
  parameter(root=None) -> data/params.json als flaches Dict {name: wert}
  filtere(eintraege)   -> Liste der Eintraege (Kopie; Daten ohne Marken gelten alle)

Aufruf als Skript: `python -X utf8 scripts/variante.py` druckt alle Pfade.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("BOM_ROOT") or os.path.dirname(HERE)  # BOM_ROOT: Testkopie (check_bom.py)

_PFADE = {
    "dome_script": "scripts/dome-script.json",
    "modell": "designs/dome.sc",
    "bilder_dir": "renders/oasis",
    "viewer_dir": "viewer",
    "instances": "viewer/instances.json",
    "extras": "viewer/extras.json",
    "ansicht": "viewer/ansicht.json",
    "stueckliste_json": "data/stueckliste.json",
    "stueckliste_md": "docs/stueckliste.md",
    "einkaufsliste": "docs/einkaufsliste.html",
    "system_specs": "data/system-specs.json",
    "nft_pots": "data/nft_pots.json",
    "walkway_map": "docs/walkway-map.md",
    "defs_dir": "viewer/defs",
    "detail_dir": "viewer/detail",
    "params": "data/params.json",
    # Eingefrorene Bezugsgeometrie des Altbestands (Archiv, nie neu erzeugt): der Ring-Bau rechnet die Lage der Ueberlauf-Stutzen
    # (R_UEB/R_UEB2) aus dem alten Bauskript und den alten Trassen, wie in U6 (trassen_ring.einspeisung_u6).
    "dome_script_altbestand": "designs/archiv/dome-script-altbestand.json",
    "trassen_altbestand": "data/archiv/leitungstrassen-altbestand.json",
}


def pfad(art, root=None):
    if art not in _PFADE:
        raise KeyError("Unbekannte Ausgabeart %r; bekannt: %s" % (art, ", ".join(sorted(_PFADE))))
    return os.path.join(root or ROOT, *_PFADE[art].split("/"))


def filtere(eintraege):
    return list(eintraege)


def parameter(root=None):
    """D119 (N-UNIFY U3): data/params.json als flaches Dict {name: wert}; seit U7 stehen die Soll-Werte der Quelle direkt in `value`."""
    with open(os.path.join(root or ROOT, "data", "params.json"), encoding="utf-8") as f:
        d = json.load(f)
    return {k: e["value"] for k, e in d.items() if isinstance(e, dict) and "value" in e}


def alle_pfade():
    return {a: pfad(a) for a in _PFADE}


if __name__ == "__main__":
    for a, p in alle_pfade().items():
        print("  %-18s %s" % (a, os.path.relpath(p, ROOT)))
