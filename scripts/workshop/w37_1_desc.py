"""W37-1: Viewer-Beschreibungen fuer beet_sumpf und schlammfass in data/descriptions.json (vor ^puffer_klein einsortiert, Blatt W37-1; idempotent, CRLF wie die Datei).
Aufruf: python -X utf8 scripts/workshop/w37_1_desc.py [beet_sumpf] [schlammfass]"""
import json, os, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

DESC = {
    "beet_sumpf": {"match": "^beet_sumpf", "titel": "Beet-Sumpf (je Linie)",
        "was": "Eingegrabener 500-l-Tank, in den die Beete einer Linie leerlaufen; zwei Teichpumpen mit Rückschlagventil fördern das Wasser zurück zum Rücklauf, drei Schwimmer schalten.",
        "status": "gebaut (Werkstatt W37-1), Prüfung 33/33; Pumpen, Schwimmer und Deckel sind Platzhalter; Standort setzt die Montage (M10 S4)",
        "ablauf": ["Die Sammelleitung d50 der Beetabläufe (K14/K30) läuft mit Gefälle in den Tankverbinder, Sohle 800 mm über dem Tankboden.",
                   "Steigt der Pegel auf 320 mm, schaltet die Pumpe ein, bei 120 mm aus.",
                   "Bei 620 mm (ALARM) sperrt die Steuerung die Beet-Zufuhr und meldet; die zweite Pumpe ist Reserve.",
                   "Die Förderleitung d40 (K58/K59) führt durch den Deckel zum Rücklauf über dem Pool-Spiegel."],
        "aufbau": [{"t": "Teile", "p": ["PE-Rundtank Ø 800 × 1000 mit Schachtaufsatz 200 mm und begehbarem Deckel Ø 700", "Tankverbinder d50 (Zulauf)", "2 Teichpumpen mit je Rückschlagventil d40, Sammelrohr, Deckeldurchführung", "Schwimmerstange mit 3 Schwimmern, Entlüftung d32 mit Gitter, 2 Kabelverschraubungen M25"]}],
        "masse": {"Inhalt bis ALARM": "ca. 300 l", "Tankinhalt": "482 l", "Einbau": "Tankboden 1200 mm unter Flur", "Leistung": "60 W je Pumpe im Betrieb"},
        "grenzen": "Die Einbautiefe folgt aus dem Beetablauf (Sammler 6 m mit 1 % angenommen); die statische Förderhöhe steigt dadurch auf 1,4 bis 1,6 m, der Arbeitspunkt der Pumpe ist nachzurechnen. Fabrikate offen.",
        "quelle": "docs/parts/beet_sumpf.md, docs/research/R45-hydraulik-auslegung.md Abschnitt 3, docs/jobs/W37-1-sumpf-schlammfass.md"},
    "schlammfass": {"match": "^schlammfass", "titel": "Schlammfass (je Linie)",
        "was": "Spannringfass 220 l in einer Grube neben dem Absetzer; nimmt den Schlamm der Absetzer-Spülung auf und wird wöchentlich von Hand geleert.",
        "status": "gebaut (Werkstatt W37-1); Handelsmaß angenommen; Standort und Grube setzt die Montage (M10 S5)",
        "ablauf": ["Alle 2 bis 3 Tage wird der Federrückzug-Kugelhahn am Absetzer kurz geöffnet; 20 bis 40 l Spülwasser laufen über K07/K23 in den Stutzen d40 des Deckels.",
                   "Im Fass setzt sich der Schlamm ab; einmal pro Woche wird das Klarwasser abgehoben (zurück in den Pool) und der Dickschlamm zum Wurmkompost gebracht.",
                   "Es gibt keinen Auslass; entleert wird von oben."],
        "aufbau": [{"t": "Teile", "p": ["Spannringfass PE mit Deckel und Spannring", "Einlaufstutzen d40 in der Deckelmitte", "Bohrung Ø 8 für einen Luftschlauch, Entlüftung Ø 20"]}],
        "masse": {"Grube": "Ø 0,8 m, Tiefe 0,95 m", "Wochenmenge": "70 bis 105 l je Linie"},
        "grenzen": "Fassmaß als Handelsmaß angenommen; die Konzentration des Schlamms ist erst im Betrieb messbar.",
        "quelle": "docs/parts/schlammfass.md, docs/research/R45-hydraulik-auslegung.md Abschnitt 0"},
}

def main(keys):
    p = os.path.join(ROOT, "data", "descriptions.json")
    txt = open(p, "rb").read().decode("utf-8")
    anchor = '    {\r\n      "match": "^puffer_klein",'
    assert txt.count(anchor) == 1
    for k in keys:
        e = DESC[k]
        if '"match": ' + json.dumps(e["match"], ensure_ascii=False) + "," in txt:
            print("schon da:", k); continue
        body = json.dumps(e, indent=2, ensure_ascii=False).replace("\n", "\n    ").replace("\n", "\r\n")
        txt = txt.replace(anchor, "    " + body + ",\r\n" + anchor)
        print("eingefuegt:", k)
    json.loads(txt)
    open(p, "wb").write(txt.encode("utf-8"))

if __name__ == "__main__":
    main(sys.argv[1:] or list(DESC))
