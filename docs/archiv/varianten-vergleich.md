# Vergleich Kreislauf A+ und Ring B2 (W70)

Erzeugt von `scripts/bom_vergleich.py` aus `data/stueckliste.json` und `data/stueckliste-ring_b2.json` (Mehr und Weniger von Ring B2 gegen A+). Nicht von Hand aendern.

**Stand: Ring B2 noch nicht gebaut.** Es fehlt: data/stueckliste-ring_b2.json. Die Stueckliste von Ring B2 entsteht mit `python -X utf8 scripts/bom.py --variante ring_b2`, sobald `viewer/varianten/ring_b2/instances.json` existiert (Montage R1/R2).

## Kennzahlen (`data/system-specs*.json`, Block `kreislauf`)

| Kennzahl | A+ | Ring B2 |
|---|---|---|
| Pumpstufen Linienwasser | 1 | 2 |
| Pumpenleistung elektrisch eta 25 % (W) | 430 | 577 |
| Pumpenleistung elektrisch eta 18 % (W) | - | 635 |
| Foerderhoehe Hauptpumpe (m) | 2.0 | 2.0 |
| Foerderhoehe Booster (m) | - | 1.0 |
| Graeben Zulauf zu Beeten | ja | nein |
| Ring ueber Kopf, Nennlaenge (m) | 0.0 | 21.4 |
| Rohr ueber Kopf, gemessen (m) | 0.0 | 0.0 |
| Rohrlaenge gesamt, gemessen (m) | 72.4 | 72.4 |
| Wasser in Rohren, gemessen (l) | 101.4 | 101.4 |

Herkunft: Q docs/research/R47-wasserkreislauf-neu.md Tabelle Pumpenleistung (A+ 430 W, Ring B2 577 W bei eta 25 %, 635 W bei 18 %), Rechnung scripts/r47_pumpen.py

Solange V1b die Trassen nicht mit `varianten` markiert hat, sind die gemessenen Werte beider Varianten gleich; der Ring (Trassen ring_b2) entsteht erst mit Schritt R1.
