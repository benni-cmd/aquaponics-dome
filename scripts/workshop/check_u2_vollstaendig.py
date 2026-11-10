"""Vollstaendigkeit der U2-Komponenten (N-UNIFY-AUTOBAHN): jede der elf neuen Komponenten hat .sc, Parameter-/Blatt-Daten, Teiledaten, Bauteilblatt, Generator, Check
und einen Eintrag in data/descriptions.json; jeder Koerper des .sc steht in genau einer Teilezeile (Anzahl aus data/parts gegen das .sc ueber check_parts.py).
Ersatz fuer die Zeile 'keine Komponente ohne Teiledatei oder Beschreibung' des Auftrags, denn scripts/check_components.py prueft nur designs/dome.sc (Baugruppen der Kuppel).
Aufruf: python -I -X utf8 scripts/workshop/check_u2_vollstaendig.py   (Exit 1 bei fehlender Datei)"""
import json, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
NAMEN = ("sumpftank podest_vortex podest_biofilter venturi_belueffter schwimmerschalter_hochstand notluftpumpe nachspeise_ventil schlamm_sammelbehaelter regentank_5m3 "
         "permakultur_modul tauchpumpe_modul").split()


def main():
    desc = {x["match"] for x in json.load(open(os.path.join(ROOT, "data", "descriptions.json"), encoding="utf-8"))["bauteile"]}
    fehlt = []
    for n in NAMEN:
        for rel in (f"designs/components/{n}.sc", f"data/components/{n}.json", f"data/parts/{n}.json", f"docs/parts/{n}.md", f"scripts/workshop/{n}.py", f"scripts/workshop/check_{n}.py"):
            if not os.path.exists(os.path.join(ROOT, rel)):
                fehlt.append(rel)
        if "^" + n not in desc:
            fehlt.append(f"data/descriptions.json: Eintrag ^{n}")
        teile = json.load(open(os.path.join(ROOT, "data", "parts", n + ".json"), encoding="utf-8"))
        if sum(len(t["koerper"]) for t in teile["teile"]) != teile["koerperzahl"]:
            fehlt.append(f"data/parts/{n}.json: Koerper der Teilezeilen gegen koerperzahl")
    print(f"{len(NAMEN)} Komponenten, fehlende Dateien oder Eintraege: {fehlt if fehlt else 'keine'}")
    return 1 if fehlt else 0


if __name__ == "__main__":
    sys.exit(main())
