"""W25 (D38, 31.10.): Pumpen-Blatt nach der Fachrecherche: pumpe_gross der Tanktafeln = Hauptkreislauf (4 x 55-60 l/min), pumpe_klein = Absetzer-Teilstrom (4 x 12-13 l/min); keine neue Komponente. Idempotent.
Zahlen aus docs/research/aquaponik-empfehlung.md (Zeilen Hauptkreislauf/Absetzer/Pumpenleistung) und der Rinnenzahl aus nft_tisch.json (D43).
Aufruf: python scripts/workshop/fix_w25_pumpe_blatt.py (danach partsheet.py pumpe)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

pj = os.path.join(sc.ROOT, "data", "components", "pumpe.json")
d = json.load(open(pj, encoding="utf-8"))
p, nt = sc.load_params("nft_tisch")
cnt = {"innen": 10, "mitte": 6, "aussen": 8}
n_rinnen = sum(nt["typen"][t]["n"] * cnt[t] for t in cnt)
q_gross = (55, 60)                                       # l/min je Pumpe (D38)
q_klein = (12, 13)
n_g, n_k = d["typen"]["pumpe_gross"]["anzahl"], d["typen"]["pumpe_klein"]["anzahl"]
sum_g = (n_g * q_gross[0], n_g * q_gross[1])
beete = 109                                              # Beetstrom l/min (aquaponik-empfehlung.md: 2 Zyklen/h)
nft_hi = (sum_g[1] - beete) / n_rinnen                   # mittlere Rinnenmenge bei 240 l/min Gesamt
nft_lo = (sum_g[0] - beete) / n_rinnen
d["typen"]["pumpe_gross"].update(rolle="Hauptkreislauf (je Linie 2 Pumpen parallel, D38)", foerderstrom_l_min=f"{q_gross[0]}-{q_gross[1]} je Pumpe, {sum_g[0]}-{sum_g[1]} gesamt, {sum_g[0] // 2}-{sum_g[1] // 2} je Linie", foerderstrom_herkunft="[E] D38/aquaponik-empfehlung.md Frage 5 (Hauptkreislauf 180-250 l/min gesamt, 90-125 je Linie); Fabrikat offen")
d["typen"]["pumpe_klein"].update(rolle="Absetzer-Teilstrom (D38)", foerderstrom_l_min=f"{q_klein[0]}-{q_klein[1]} je Pumpe", foerderstrom_herkunft="[E] D38: Teilstrom ca. 13 l/min je Tank (20 min Verweilzeit des Absetzers); ersetzt den Modellwert 12 l/min des kleinen Tanks als Kreislauf")
bl = d["blatt"]
bl["funktion"] = ("Pumpenmodul an den Tanks (Montagetafel mit Kreiselpumpe, Rolle ANNAHME fuer die Tafel, ENTSCHEIDUNG D38 30.10. fuer die Pumpen): pumpe_gross (4 Stueck, Tanktafeln 2/3) = HAUPTKREISLAUF, je Linie 2 parallel: "
                  f"{q_gross[0]}-{q_gross[1]} l/min je Pumpe, zusammen {sum_g[0]}-{sum_g[1]} l/min (Empfehlung 180-250 l/min gesamt, 90-125 je Linie) [E]; pumpe_klein (4 Stueck, Tanktafeln 1/4) = ABSETZER-TEILSTROM, {q_klein[0]}-{q_klein[1]} l/min je Pumpe [E]. "
                  f"Plausibilitaet [R]: Pflanzenstrom = Hauptkreislauf - Beete ({beete} l/min) = {sum_g[0] - beete}-{sum_g[1] - beete} l/min auf {n_rinnen} Rinnen (aussen mit 4 Rinnen, D43) = {nft_lo:.1f}-{nft_hi:.1f} l/min je Rinne (Soll 1-2). "
                  "Statische Hoehe ca. 1,3 m plus Reibung (hydraulics.md 2.8 [E]); elektrisch ca. 230-320 W fuer den Hauptkreislauf [E]. Die frueheren Modellwerte 12 / 30 l/min gelten nicht mehr als Kreislauf. "
                  "ENTSCHEIDUNG Orchestrator 29.10.: Die 10 Kassetten 384 x 44 x 419 (layout.json tanks 2/3) sind KEINE Filtermodule, sondern Stuetzrippen/Konsolen der Tankplattform (Klasse Tank, Annahme A); die Klasse filtermodul entfaellt.")
off = [x for x in bl["offen"] if not x.startswith(("Pumpenfabrikat, Leistung", "W25 (D38"))]
off.append("Pumpenfabrikat und Leistung offen (R07 pausiert); Foerderstrom 55-60 / 12-13 l/min nur [E] aus D38; Kennlinie (Foerderhoehe gegen Menge), Reserve-Paar und Trockenlaufschutz nicht festgelegt; reale Pumpe 4-9 kg [A]")
off.append("W25 (D38, 31.10.): Geometrie unveraendert (keine neue Komponente); Viewer-/system_specs-Kennzahlen (180-250 l/min statt 12/30) und hydraulics.md 2.3 fuehrt der Orchestrator nach; Pflanzenstrom je Rinne rechnet mit den 76 Rinnen aus D43")
bl["offen"] = off
json.dump(d, open(pj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"Rinnen {n_rinnen}, Hauptkreislauf {sum_g}, Pflanzenstrom je Rinne {nft_lo:.2f}-{nft_hi:.2f} l/min")
