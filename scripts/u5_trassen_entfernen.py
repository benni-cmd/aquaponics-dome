"""N-UNIFY-AUTOBAHN U5 (D127): blendet die Altbestand-Leitungen in `ring_b2` aus, die an entfernten oder versetzten Teilen haengen. Nichts wird geloescht.

Aufruf (Projektordner):  python -I -X utf8 scripts/u5_trassen_entfernen.py [--pruefen]
  ohne Schalter: schreibt data/leitungstrassen.json (idempotent); --pruefen: nur zaehlen, nichts schreiben.

Regeln:
  1. Gemeinsame Eintraege (ohne Feld `varianten`, Altbestand A+) bekommen `varianten: ["a_plus"]` und gelten damit nur noch in A+ (A+ bleibt unveraendert).
     Ausnahme (bleiben gemeinsam): K39 (Hausanschluss -> Aktivkohle-Station) und K52 samt Zapfhahn KH_K52 (Station -> Puffer klein); beide Enden bleiben stehen.
  2. Eintraege nur fuer ring_b2, die an Pegelschacht, Booster, Feinfilter, Pumpen klein/gross oder an den alten Tankorten hingen, bekommen `entfaellt_in: ["ring_b2"]`
     und `entfaellt_grund` (gelesen in scripts/variante.py gilt()). Die Steigleitungen RB1-K63/RB2-K63 bleiben fuer U6 (Einspeisung) stehen, ihr Anfang wird `offen`.
Quelle der Entscheidung: D101 (Entfallene Teile), D127; Paket docs/packages/n-unify-autobahn.md Abschnitt C."""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PFAD = os.path.join(ROOT, "data", "leitungstrassen.json")
LISTEN = ("trassen", "t_stuecke", "r_stuecke", "teile", "gruben")
BLEIBT_GEMEINSAM = {"K39", "K52", "KH_K52"}
GRUND = "N-UNIFY U5 (D101, D127): Pegelschacht, Booster, Feinfilter, Pumpen klein/gross oder der alte Tankort entfallen; U6 verlegt die Wege neu"
ENTFAELLT_RB2 = {
    "trassen": {"K06", "K02", "K06-T", "K03-Steig", "K05", "K22", "K18", "K22-T", "K19", "K21", "K22-T-b", "K57-b",
                "RB1-K60", "RB1-K61", "RB1-K62", "RB1-Da1", "RB1-Da2", "RB1-Da3", "RB1-Db1", "RB1-Db2", "RB1-Db3", "RB1-K67",
                "RB2-K60", "RB2-K69", "RB2-K70", "RB2-Da1", "RB2-Da2", "RB2-Da3", "RB2-Db1", "RB2-Db2", "RB2-Db3", "RB2-K67"},
    "t_stuecke": {"T3", "T14", "RB1-TB", "RB2-TB"},
    "r_stuecke": {"RB1-REDa", "RB1-RSVa", "RB1-REDb", "RB1-RSVb", "RB2-REDa", "RB2-RSVa", "RB2-REDb", "RB2-RSVb"},
}
STEIGLEITUNG = {"RB1-K63", "RB2-K63"}


def main():
    pruefen = "--pruefen" in sys.argv
    doc = json.load(open(PFAD, encoding="utf-8"))
    n_a_plus = n_entf = n_offen = 0
    for key in LISTEN:
        for e in doc.get(key, []):
            if not e.get("varianten"):
                if e["id"] in BLEIBT_GEMEINSAM:
                    continue
                e["varianten"] = ["a_plus"]
                n_a_plus += 1
            elif e["varianten"] == ["ring_b2"]:
                if e["id"] in ENTFAELLT_RB2.get(key, ()) and "ring_b2" not in e.get("entfaellt_in", []):
                    e["entfaellt_in"] = ["ring_b2"]
                    e["entfaellt_grund"] = GRUND
                    n_entf += 1
                elif key == "trassen" and e["id"] in STEIGLEITUNG and e.get("start") != "offen":
                    e["start"] = "offen"
                    e["notiz"] = e.get("notiz", "") + " [U5: Booster entfaellt, Anfang offen; U6 ersetzt die Einspeisung durch den Ueberlauf d63 des Biofilters]"
                    n_offen += 1
    # Zaehlung der in ring_b2 geltenden Eintraege (Probe)
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import variante
    gelten = {k: len(variante.filtere(doc.get(k, []), "ring_b2")) for k in LISTEN}
    gelten_a = {k: len(variante.filtere(doc.get(k, []), "a_plus")) for k in LISTEN}
    print("neu a_plus-only: %d, entfaellt_in ring_b2: %d, Steigleitung Anfang offen: %d" % (n_a_plus, n_entf, n_offen))
    print("gelten in ring_b2:", gelten)
    print("gelten in a_plus: ", gelten_a)
    if not pruefen:
        with open(PFAD, "w", encoding="utf-8", newline="\n") as f:
            f.write(json.dumps(doc, ensure_ascii=False, indent=1) + "\n")
        print("geschrieben:", os.path.relpath(PFAD, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
