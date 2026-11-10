"""Traegt den Stand des Europa-Bezugs (D76) und des Lebensmittel-Nachweises (D85) je Komponente aus data/beschaffung/u2_wasserkreislauf.json in blatt.offen der Komponenten-Daten ein (idempotent).
Aufruf: python -X utf8 scripts/workshop/u2_bezug.py   (danach u2_parts.py und partsheet.py laufen lassen)"""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

KOPF = "Bezug Europa und Lebensmittel (D76, D85), Stand 10.11.2026 aus data/beschaffung/u2_wasserkreislauf.json: "
MAP = {
    "sumpftank": ["MAT-epdm-teichfolie", "MAT-gitterrost-deckel"],
    "venturi_belueffter": ["ARM-venturi-mazzei-1583", "ARM-rueckschlagventil-luft"],
    "schwimmerschalter_hochstand": ["ARM-schwimmerschalter-hochstand"],
    "notluftpumpe": ["PMP-luftpumpe-notluft", "ARM-luftstein-notluft", "ARM-rueckschlagventil-luft"],
    "nachspeise_ventil": ["ARM-schwimmerventil-nachspeise"],
    "schlamm_sammelbehaelter": ["BEH-schlammbehaelter-350"],
    "regentank_5m3": ["BEH-regentank-5000"],
    "tauchpumpe_modul": ["PMP-tauchpumpe-oase-8000", "ARM-rueckschlagventil-d50"],
}


def zeile(aid, a):
    ang = a.get("angebote", [])
    if ang:
        o = ang[0]
        bezug = f"{o.get('haendler')} ({o.get('land')}), Konfidenz {o.get('konfidenz')}"
    else:
        bezug = "kein Angebot in Europa gefunden"
    m = re.search(r"Lebensmittel:[^.]*", a.get("bemerkung_artikel", ""))
    lm = m.group(0) if m else "Lebensmittel: offen"
    return f"{aid}: {bezug}; {lm}; Rueckfall: {str(a.get('alternative'))[:140]}"


ALLE = ["sumpftank", "podest_vortex", "podest_biofilter", "venturi_belueffter", "schwimmerschalter_hochstand", "notluftpumpe", "nachspeise_ventil", "schlamm_sammelbehaelter", "regentank_5m3", "permakultur_modul", "tauchpumpe_modul"]
REFERENZ = "kein OBJ-Bild (Bauteil neu nach der Quelle): docs/quellen/oasis-showcase-2026-11-10/ (Draufsicht, Seitenprofil) und data/oasis-soll.json"


if __name__ == "__main__":
    for name in ALLE:       # Referenz im Blatt: kein Fremdbild aus dem Standardtext des Blattgenerators
        pfad = os.path.join(sc.ROOT, "data", "components", name + ".json")
        d = json.load(open(pfad, encoding="utf-8"))
        d["blatt"]["referenz"] = REFERENZ
        open(pfad, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + chr(10))
    besch = json.load(open(os.path.join(sc.ROOT, "data", "beschaffung", "u2_wasserkreislauf.json"), encoding="utf-8"))["artikel"]
    for name, ids in MAP.items():
        pfad = os.path.join(sc.ROOT, "data", "components", name + ".json")
        d = json.load(open(pfad, encoding="utf-8"))
        off = [x for x in d["blatt"]["offen"] if not x.startswith(KOPF)]
        off.append(KOPF + " | ".join(zeile(i, besch[i]) for i in ids if i in besch))
        d["blatt"]["offen"] = off
        open(pfad, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + chr(10))
        print(name, "ok", len(off), "offene Punkte")
