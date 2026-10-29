#!/usr/bin/env python3
"""Rechnet die Kuppel-Kennzahlen (Wasser, Pflanzen, Fluesse, Pumpenleistung, Filterkapazitaet) aus den Modellmassen und
schreibt data/system-specs.json (der Viewer zeigt sie, solange nichts ausgewaehlt ist) und die Konsistenzpruefung.
Jede Zahl traegt eine Herkunft: Q = Quelle (Ben-Tabelle R15 / docs/hydraulics.md), E = eigene Rechnung aus Modellmassen, A = Annahme.
Aufruf: python scripts/system_specs.py"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pi = math.pi

# ---- Eingaben (Modell) ------------------------------------------------------------------------------------------------
POOL_D, POOL_DEPTH = 3.890, 2.200                      # E/Q: OBJ-Durchmesser, Tiefe nach Ben-Tabelle (D26)
BASIN2_D, BASIN2_DEPTH = 1.747, 1.0                    # E aus OBJ; Tiefe 1,0 m aus Zuchtbecken der Ben-Tabelle [A]
TANK_KLEIN = dict(D=0.673, H=1.075, n=2)               # OBJ
TANK_GROSS = dict(D=0.930, H=1.444, n=2)
RIM_BELOW_WATER = 0.100                                # Auslass 100 mm unter dem Rand (R09)
BEDS = dict(outer=dict(n=8, w=0.800, l=2.640), inner=dict(n=6, w=0.933, l=1.865))   # nach D29/D34
SUBSTRATE_DEPTH, POROSITY = 0.300, 0.40                # Substrattiefe (Beet-Blatt), Porositaet Kies/Blaehton [A 0,35-0,45]
NFT_CHANNELS = {"aussen": (8, [3.051, 2.864, 2.676]), "mitte": (6, [2.018, 1.847, 1.676, 1.505]), "innen": (10, [0.928, 0.758])}  # W17/W18
NFT_FILM_L_PER_M = 1.0                                 # Wasserfilm in der Rinne ca. 1 l je Meter [A]
NFT_FLOW_PER_CHANNEL = 0.5                             # l/min je Rinne (nft_rinne-Blatt, Bereich 0,5-2)
POTS_BEDS, POTS_NFT = 2160, 586                        # Modell (OBJ, D33)
POTS_TABLE = 609                                       # Ben-Tabelle Gesamt
FISH_N, FISH_KG = 1839, 0.7                            # Ben-Tabelle Tilapia
FEED_KG_DAY = 321.255 / 30                             # Ben-Tabelle Fischfutter pro Monat
PLANT_AREA_SUBSTRATE, PLANT_AREA_NFT = 37.97, 42.41    # Ben-Tabelle m2
PIPE_WATER_L = 225                                     # Rohre/Schlaeuche, Annahme: 150 m, im Mittel 1,5 l/m [A]
FLOOD_CYCLES_PER_H = 2                                 # Beete [A, keine belastbare Quelle, hydraulics.md 2.6]
HEAD_M = 2.0                                           # statisch 1,3 + Reibung + 20 % Reserve (hydraulics.md 2.8)
PUMP_EFF = 0.35                                        # kleine Kreiselpumpe [A]
O2_PER_KG_FEED = 0.25                                  # kg O2 je kg Futter fuer Fische [A, Faustregel]
O2_NITRIF_PER_G_TAN = 4.57                             # g O2 je g TAN (Nitrifikation, Stoechiometrie) [Q Lehrbuch]
TAN_FRACTION = 0.35 * 0.092                            # TAN je g Futter bei 35 % Protein (Faustregel) [A]
AIR_KG_O2_PER_KWH = 1.0                                # Belueftung [A, 0,8-2 je nach System]
FEED_RULE_MEDIA_L_PER_G = {"kies": 1.0, "bioball": 0.5}  # hydraulics.md Regel Biofilter [Q FAO ueber Zweitquellen]
PLANT_FEED_G_M2 = (40, 50)                             # Blattgemuese g Futter je m2 und Tag (hydraulics.md 2.7)


def cyl_cone(D, H, below):
    r = D / 2
    cone = r                                           # 45 Grad
    cyl = H - cone - below
    return pi * r * r * cyl + pi * r * r * cone / 3


# ---- Wasser -----------------------------------------------------------------------------------------------------------
pool = pi * (POOL_D / 2) ** 2 * POOL_DEPTH
basin2 = pi * (BASIN2_D / 2) ** 2 * BASIN2_DEPTH
t_klein = cyl_cone(TANK_KLEIN["D"], TANK_KLEIN["H"], RIM_BELOW_WATER)
t_gross = cyl_cone(TANK_GROSS["D"], TANK_GROSS["H"], RIM_BELOW_WATER)
tanks = TANK_KLEIN["n"] * t_klein + TANK_GROSS["n"] * t_gross
bed_vol = {k: v["n"] * v["w"] * v["l"] * SUBSTRATE_DEPTH for k, v in BEDS.items()}
substrate_total = sum(bed_vol.values())
beds_water = substrate_total * POROSITY
nft_len = sum(n * sum(ch) for n, ch in NFT_CHANNELS.values())
nft_channels = sum(n * len(ch) for n, ch in NFT_CHANNELS.values())
nft_water = nft_len * NFT_FILM_L_PER_M / 1000
pipes = PIPE_WATER_L / 1000
parts = [("Hauptbecken (Pool)", pool), ("Zweites Becken", basin2), ("Tanks (2 Absetzer, 2 Biofilter)", tanks),
         ("Beete (Porenwasser bei Flutung)", beds_water), ("NFT-Rinnen (Wasserfilm)", nft_water), ("Rohre und Schläuche", pipes)]
total = sum(v for _, v in parts)

# ---- Fische, Futter, Filterkapazitaet --------------------------------------------------------------------------------
biomass = FISH_N * FISH_KG
fish_water = pool + basin2
density = biomass / fish_water
tan_g = FEED_KG_DAY * 1000 * TAN_FRACTION
media_biofilter_m3 = TANK_GROSS["n"] * pi * 0.40 ** 2 * 0.52          # Biomediumkorb Ø~0,8 m, 520 mm hoch [E]
cap_bio = media_biofilter_m3 * 1000 / FEED_RULE_MEDIA_L_PER_G["bioball"] / 1000   # kg Futter/Tag
cap_sub = substrate_total * 1000 / FEED_RULE_MEDIA_L_PER_G["kies"] / 1000
cap_media = cap_bio + cap_sub
cap_plants = (PLANT_AREA_SUBSTRATE + PLANT_AREA_NFT) * PLANT_FEED_G_M2[1] / 1000
fish_fit = min(cap_media, cap_plants) / FEED_KG_DAY

# ---- Fluesse, Pumpen, Strom -------------------------------------------------------------------------------------------
nft_flow = nft_channels * NFT_FLOW_PER_CHANNEL                         # l/min
bed_flow = sum(v["n"] * v["w"] * v["l"] * SUBSTRATE_DEPTH * POROSITY for v in BEDS.values()) * 1000 * FLOOD_CYCLES_PER_H / 60
circuit = nft_flow + bed_flow
per_line = circuit / 2
p_hyd = 1000 * 9.81 * (per_line / 60000) * HEAD_M                      # W
p_el = p_hyd / PUMP_EFF
o2_kg_day = FEED_KG_DAY * O2_PER_KG_FEED + tan_g / 1000 * O2_NITRIF_PER_G_TAN
air_w = o2_kg_day / AIR_KG_O2_PER_KWH * 1000 / 24
control_w = 40
power_w = 2 * p_el + air_w + control_w
vortex_flow = 2 * 12                                                    # l/min, Modell-Pumpe klein (Verweilzeit-Auslegung)
resid_small = t_klein * 1000 / 12

checks = [
    ("Pflanzenzahl gegen Ben-Tabelle", POTS_BEDS + POTS_NFT >= POTS_TABLE, f"{POTS_BEDS + POTS_NFT} im Modell gegen mindestens {POTS_TABLE}"),
    ("Besatzdichte höchstens 150 kg/m³ (Tabellenobergrenze)", density <= 150, f"{density:.0f} kg/m³ im Beckenwasser {fish_water:.1f} m³ (Tabellenbereich 60–150, also eher locker besetzt)"),
    ("Biofilter-/Substratvolumen deckt das Futter", cap_media >= FEED_KG_DAY, f"deckt {cap_media:.1f} von {FEED_KG_DAY:.1f} kg Futter/Tag ({cap_media / FEED_KG_DAY:.0%})"),
    ("Pflanzfläche deckt das Futter (50 g/m²/Tag)", cap_plants >= FEED_KG_DAY, f"deckt {cap_plants:.1f} von {FEED_KG_DAY:.1f} kg Futter/Tag ({cap_plants / FEED_KG_DAY:.0%})"),
    ("Pumpen im Modell reichen für den Hauptkreislauf", vortex_flow >= circuit, f"Modell-Pumpen klein 2 × 12 l/min = {vortex_flow:.0f} gegen Bedarf {circuit:.0f} l/min"),
]

specs = {
    "stand": "30.10.2026",
    "hinweis": "Schätzung aus den Modellmaßen und Bens Tabelle; Annahmen (A) stehen im Text. Keine fachliche Freigabe.",
    "wasser": {"gesamt_m3": round(total, 1), "teile": [(n, round(v, 2), f"{v / total:.0%}") for n, v in parts], "in_tanks_m3": round(tanks, 2),
               "tabelle_systemwasser_m3": 25},
    "pflanzen": {"beete": POTS_BEDS, "nft": POTS_NFT, "gesamt": POTS_BEDS + POTS_NFT, "tabelle": POTS_TABLE, "rinnen": nft_channels,
                 "rinnenlaenge_m": round(nft_len, 1), "substrat_m3": round(substrate_total, 1)},
    "fische": {"anzahl": FISH_N, "biomasse_kg": round(biomass), "futter_kg_tag": round(FEED_KG_DAY, 1), "dichte_kg_m3": round(density), "tan_g_tag": round(tan_g)},
    "fluesse": {"nft_l_min": round(nft_flow), "beete_l_min": round(bed_flow), "kreislauf_l_min": round(circuit), "kreislauf_m3_h": round(circuit * 0.06, 1),
                "je_linie_l_min": round(per_line), "umwaelzzeit_h": round(total * 1000 / circuit / 60, 1), "pumpe_hoehe_m": HEAD_M},
    "leistung": {"pumpe_hydraulisch_w": round(p_hyd), "pumpe_elektrisch_w": round(p_el), "belueftung_w": round(air_w), "steuerung_w": control_w,
                 "gesamt_w": round(power_w), "kwh_tag": round(power_w * 24 / 1000, 1), "kwh_monat": round(power_w * 24 * 30 / 1000)},
    "filter": {"absetzer_klein_l": round(t_klein * 1000), "biofilter_gross_l": round(t_gross * 1000), "medium_biofilter_m3": round(media_biofilter_m3, 2),
               "kapazitaet_biofilter_kg_futter": round(cap_bio, 1), "kapazitaet_substrat_kg_futter": round(cap_sub, 1), "verweilzeit_absetzer_min": round(resid_small, 1)},
    "kapazitaet": {"medien_kg_futter_tag": round(cap_media, 1), "pflanzen_kg_futter_tag": round(cap_plants, 1), "passender_fischanteil": round(fish_fit, 2)},
    "konsistenz": [{"pruefung": n, "ok": bool(ok), "detail": d} for n, ok, d in checks],
}
(ROOT / "data" / "system-specs.json").write_text(json.dumps(specs, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(specs, ensure_ascii=False, indent=1)[:4500])
