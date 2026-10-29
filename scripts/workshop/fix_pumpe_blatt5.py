"""Blatt pumpe nach Spec-Pruefer Runde 3 (W12, 29.10. ~14:40): Konsole = Winkel (Schenkel haengt nach unten), Pumpenschrauben M6x30, Normteil-Stahl, Pumpe B am grossen Tank, 384er-Reste raus, Beleg-Datei neu.
Aufruf: python scripts/workshop/fix_pumpe_blatt5.py <Anzahl-PASS>   (Zahl aus check_pumpe.py, z. B. 32); danach partsheet.py pumpe."""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

n = sys.argv[1]
p = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
s = open(p, encoding="utf-8").read()

def rep(old, new):
    global s
    assert s.count(old) >= 1, old[:60]
    s = s.replace(old, new)

rep("Tafel- und Tafelnmasse stimmen auf <= 1 mm (OBJ 501/502 x 5 x 345, 693 x 7 x 463, 384 x 43/44 x 418/419; Bauteil 502/693/384 mit Dicke 5/7/44)", "Tafelmasse stimmen auf <= 1 mm (OBJ 501/502 x 5 x 345, 693 x 7 x 463; Bauteil 502 x 5 bzw. 693 x 7)")
rep("je 2 Tafeln 693 x 7 x 463 (Duplikate zusammengefasst), Pumpe A", "je 2 Tafeln 693 x 7 x 463 (Duplikate zusammengefasst), Pumpe B (hydraulics.md 3: Pumpe B hinter dem grossen Tank, Annahme)")
rep("4 Schrauben M6x20 mit Mutter und Scheibe (nicht modelliert) [A]", "4 Schrauben M6x30 mit Mutter und Scheibe (Klemmlaenge Sockel 11 + Konsole 5 + 2 Scheiben 3,2 + Mutter 5,2 = 24,4 mm; nicht modelliert) [A]")
rep("4 Schrauben M6x20 mit Mutter und Scheibe fuer die Pumpe", "4 Schrauben M6x30 mit Mutter und Scheibe fuer die Pumpe")
rep("Schrauben der Pumpe auf dem Sockel (4 x M6x20)", "Schrauben der Pumpe auf dem Sockel (4 x M6x30)")
rep("Konsole Winkel 5 mm: Horizontalschenkel 150 x 117 (klein) / 137 (gross) x 5, Vertikalschenkel 150 x 40 x 5", "Konsole Winkel 5 mm: Horizontalschenkel (Platte) 150 x 117 (klein) / 137 (gross) x 5, Vertikalschenkel 150 x 40 x 5 haengt von der Plattenoberkante nach unten an der Tafel")
rep("Vertikalschenkel 150 x 40) 1", "Vertikalschenkel 150 x 40 haengt nach unten, Konsole = Winkel) 1")
rep("Konsole an der Tafel: je 2 Schrauben M6x20 ISO 4017 mit Mutter ISO 4032 (im Modell;", "Konsole an der Tafel: je 2 Schrauben M6x20 ISO 4017 mit Mutter ISO 4032 mittig im haengenden Vertikalschenkel (im Modell, Bohrungen in Konsole/Tafel nicht modelliert: der Schaft liegt im Blech;")
rep("keine Durchdringung", "ohne Durchdringung")
rep("Volumen x 1,5 g/cm3", "Motor 1,5, Kopf PVC 1,4 g/cm3")
rep("Spec-Pruefer Runde 1 (FAIL, behoben, 29.10. ~08:50) und Runde 2 (FAIL, 5 Befunde, eingearbeitet;", "Spec-Pruefer Runde 1 (FAIL, behoben, 29.10. ~08:50), Runde 2 (FAIL, 5 Befunde, eingearbeitet) und Runde 3 (FAIL knapp, 5 Befunde, eingearbeitet;")
rep("check_pumpe.py: 30/30 PASS fuer beide Varianten", f"check_pumpe.py: {n}/{n} PASS fuer beide Varianten")
rep("inkl. Kopf/Konsole ohne Durchdringung", "inkl. Konsole = Winkel und Kopf/Konsole ohne Durchdringung; Normteile (Schrauben, Muttern) auf Stahl 7,85")

d = json.loads(s)
# Offene Fragen: Schrauben-Bohrungen und Hydraulik-Reste
d["blatt"]["offen"].append("Bohrungen fuer die Konsolenschrauben (M6, 2 je Konsole) sind nicht modelliert; Schaft und Kopf liegen am Blech, Kopf ausserhalb der Platte")
d["blatt"]["offen"].append("docs/hydraulics.md 5 fuehrt weiter 'Filtermodul' bzw. 'Pump-/Filtermodule' als Klasse (D16-Rest, Orchestrator)")
d["herkunft_tabelle"].append(["Zuordnung Pumpentafel gross = Pumpe B, klein = Pumpe A", "A / B", "A", "hydraulics.md 3: Pumpe A vor dem kleinen Tank, Pumpe B hinter dem grossen Tank; Tafel-Rolle bleibt Annahme", "niedrig"])
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("pumpe.json aktualisiert (Pruefzahl", n, ")")
