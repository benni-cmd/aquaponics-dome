"""Pruefung der Normteil-Benennung am Tisch (U3b Aufgabe 3, D136): baut einen Tisch mit dem AKTUELLEN, schon benannten `designs/components/winkelhalter.sc`
nach sc.TMP (nicht nach designs/), benennt mit `normteile_benennen.benennen` und vergleicht mit der eingecheckten Tischdatei.
PASS-Punkte: Umbenennen laeuft ohne Namenskollision (kein `another body is called ...`), kein Body<n> uebrig, kein Zwischenname uebrig, alle Koerpernamen eindeutig,
Koerperzahl wie die eingecheckte Datei, und jeder gleichnamige Koerper hat dieselbe Box (die Normteile des Tisches behalten ihre Namen aus dem Bau mit unbenanntem Winkelhalter).
Nicht gleich bleiben nur die Winkelhalter-Koerper selbst (eingecheckte Tische: `winkelhalter (n)`, aktueller Winkelhalter: `Winkel` und benannte Schrauben); das ist ein Befund (Paket n-unify-autobahn), kein FAIL.
Aufruf: python -X utf8 scripts/workshop/check_normteile_benennen.py [innen|mitte|aussen]   (innen etwa 2 min; Exit 1 bei FAIL)"""
import os, sys, re
sys.path.insert(0, os.path.dirname(__file__))
import sc
import nft_tisch
import normteile_benennen


def main(typ):
    os.chdir(sc.ROOT)                                   # component.insert_design nimmt den Pfad relativ zum Repo
    b, G = nft_tisch.build(typ)
    out = os.path.join(sc.TMP, f"check_normteile_nft_tisch_{typ}.sc")
    sc.run(b.write(f"check_normteile_nft_tisch_{typ}"), out)
    sc.assign_part_materials(out, "Stahl verzinkt", r"Body\d+|Winkel( \(\d+\))?|winkelhalter( \(\d+\))?")
    vor = sc.evaluate(out)["bodies"]
    n_body = sum(1 for x in vor if re.fullmatch(r"Body\d+", x["name"]))
    pl = normteile_benennen.benennen(out)               # beendet das Skript mit FEHLER, wenn ein Zielname schon vergeben ist
    neu = sc.evaluate(out)["bodies"]
    alt = sc.evaluate(os.path.join(sc.ROOT, "designs", "components", f"nft_tisch_{typ}.sc"))["bodies"]
    N = {x["name"]: x for x in neu}
    A = {x["name"]: x for x in alt}
    def box(x):
        return [round(v, 1) for v in x["bbox"]["min"] + x["bbox"]["max"]]
    ck = sc.Check("normteile_benennen")
    ck.eq(f"{typ} Body<n> vor dem Benennen {n_body}, umbenannt {len(pl)}", len(pl), n_body)
    ck.eq(f"{typ} kein Body<n> und kein Zwischenname uebrig", len([k for k in N if re.fullmatch(r"Body\d+", k) or k.startswith("__norm")]), 0)
    ck.eq(f"{typ} Koerpernamen eindeutig", len(N), len(neu))
    ck.eq(f"{typ} Koerperzahl wie die eingecheckte Datei", len(neu), len(alt))
    gleich = set(N) & set(A)
    ck.eq(f"{typ} gleichnamige Koerper mit anderer Box ({len(gleich)} gleichnamig)", len([k for k in gleich if box(N[k]) != box(A[k])]), 0)
    print("Befund (kein FAIL): nur in der neuen Datei", sorted(set(N) - set(A))[:6], "... nur in der eingecheckten", sorted(set(A) - set(N))[:3], "...")
    return ck.done()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "innen"))
