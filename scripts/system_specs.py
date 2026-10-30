#!/usr/bin/env python3
"""Rechnet die Kuppel-Kennzahlen (Wasser, Pflanzen, Fluesse, Pumpenleistung, Filterkapazitaet, Heizung) aus den Modellmassen und
schreibt data/system-specs.json (der Viewer zeigt sie, solange nichts ausgewaehlt ist) und die Konsistenzpruefung.
Auslegung nach der Fachrecherche R17-R24 (docs/research/aquaponik-empfehlung.md, aquaponik-werte.md, R24.md Huelle) und Entscheidung D40
(Biomasse 475 kg, Spanne 450-500); Bens Tabellenwerte
(reference/Kuppelberechnung-neu-2.xlsx, R15) bleiben als zweiter Wert unter "tabelle_ben" stehen.
Jede Zahl traegt eine Herkunft: Q = Quelle (R-Nummer in docs/research), E = eigene Rechnung aus Modellmassen oder Quellwerten,
A = Annahme, B = Bens Tabelle.
Aufruf: python scripts/system_specs.py"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
pi = math.pi

# ---- Eingaben (Modell) ------------------------------------------------------------------------------------------------
POOL_D, POOL_DEPTH = 3.890, 2.200                      # E/B: OBJ-Durchmesser, Tiefe nach Ben-Tabelle (D26)
BASIN2_D, BASIN2_DEPTH = 1.747, 1.0                    # E aus OBJ; Tiefe 1,0 m aus Zuchtbecken der Ben-Tabelle [A]
TANK_KLEIN = dict(D=0.673, H=1.075, n=2)               # OBJ
TANK_GROSS = dict(D=0.930, H=1.444, n=2)
RIM_BELOW_WATER = 0.100                                # Auslass 100 mm unter dem Rand (R09)
BEDS = dict(outer=dict(n=8, w=0.800, l=2.640), inner=dict(n=6, w=0.933, l=1.865))   # nach D29/D34
SUBSTRATE_DEPTH, POROSITY = 0.300, 0.40                # Substrattiefe (Beet-Blatt), Porositaet Kies/Blaehton [A 0,35-0,45]
AUSSEN_RINNEN = 4                                      # Szenario-Schalter: 4 = Standard seit D43 (W24/W25a, 674 Toepfe), 3 = Alternative aussen3 (570 Toepfe)
OUTER_3 = [2.986, 2.799, 2.612]                        # nft_tisch.json typen.aussen3 (D37, Rinnenlaenge je Reihe)
OUTER_4 = [2.986, 2.844, 2.701, 2.558]                 # nft_tisch.json typen.aussen (aussen4, D43)
NFT_CHANNELS_BASE = {"aussen": (8, OUTER_3), "mitte": (6, [2.018, 1.847, 1.676, 1.505]), "innen": (10, [0.928, 0.758])}  # W17/W18
NFT_CHANNELS = {**NFT_CHANNELS_BASE, "aussen": (8, OUTER_4 if AUSSEN_RINNEN == 4 else OUTER_3)}
NFT_FILM_L_PER_M = 1.0                                 # Wasserfilm in der Rinne ca. 1 l je Meter [A]
NFT_FLOW_PER_CHANNEL = 1.0                             # l/min je Rinne [Q R21: FAO 589 1-2, Salat 1-1,5; vorher 0,5]
POTS_BEDS = 2160                                       # Modell (OBJ, D33)
POTS_NFT3, POTS_NFT4 = 570, 674                        # NFT-Topfloecher aussen3 / aussen4 [D43, nft_tisch.json]
POTS_NFT = POTS_NFT4 if AUSSEN_RINNEN == 4 else POTS_NFT3
POTS_TABLE = 609                                       # B Ben-Tabelle Gesamt
PLANT_AREA_SUBSTRATE_TABLE, PLANT_AREA_NFT = 37.97, 42.41   # B Ben-Tabelle m2 (NFT-Flaeche nicht gegengemessen)
PIPE_WATER_L = 225                                     # Rohre/Schlaeuche, Annahme: 150 m, im Mittel 1,5 l/m [A]
FLOOD_CYCLES_PER_H = 2                                 # Beete [Q R21: Fort Valley State Extension, TCF Freshwater Institute, 5-8 min]
HEAD_M = 2.0                                           # statisch 1,3 + Reibung + 20 % Reserve (hydraulics.md 2.8), FAO nennt 1,5 m [E]
PUMP_EFF = 0.25                                        # Netz-zu-Wasser Kleinpumpe [Q R21: FAO 589, 16-33 %; vorher 0,35]
# Pumpenkonzept D38: 4 pumpe_gross = Hauptkreislauf (je Linie 2 parallel), 4 pumpe_klein = Absetzer-Teilstrom (je Absetzer-Tank 1 in Betrieb)
PUMP_GROSS_N, PUMP_GROSS_L_MIN = 4, 55                 # D38: je 55-60 l/min
PUMP_KLEIN_N, PUMP_KLEIN_L_MIN = 4, 12.5               # D38: 12-13 l/min
PUMP_KLEIN_IN_BETRIEB = 2                              # eine je Absetzer-Tank, die zweite Pumpe als Reserve [A]

# Fische und Futter: Auslegung aus der Pflanzflaeche (R20), Bens Tabelle als Vergleich
FISH_KG_DESIGN = 475                                   # D40 (Ben): 450-500 kg; Bedingung: viel Fruchtgemuese und 4. Aussenrinne (ohne: ca. 380-420 kg tragbar)
FISH_END_WEIGHT = 0.7                                  # kg Endgewicht [Q R17: FAO 0,5 kg, SRAC 454 0,81 kg]
FEED_PCT_BW = 0.01                                     # 1 % Koerpergewicht/Tag [Q R18: FAO 589, bei >100 g]
TABLE_FISH_N, TABLE_FISH_KG = 1839, 0.7                # B Ben-Tabelle Tilapia
TABLE_FEED_KG_DAY = 321.255 / 30                       # B Fischfutter pro Monat
TAN_FRACTION = 0.0375                                  # TAN je kg Futter [Q R18/R19: SRAC 451 3 %, FAO 3,75 %, Losordo 3,84 %; Spanne 3-5 %]
O2_FISH_MG_KG_H = (80, 135, 190)                       # Tilapia Grow-out Tagesmittel [Q R22: Kim & Jo 1999a/b, Aly 2007], unten/Mitte/oben
O2_PEAK_FACTOR = 1.5                                   # Fuetterungsspitze +40-60 % [Q R22]
O2_NITRIF_PER_G_TAN = 4.57                             # g O2 je g TAN (Stoechiometrie) [A, Quelle nicht gelesen]
AIR_W_PER_KG_FISH = 0.59                               # UVI-Fischgeblaese 1,1 kW fuer 1900 kg [Q R22: SRAC 454]
AIR_KG_O2_PER_KWH = 1.0                                # Feld-SAE [A; Norm-SAE feine Diffusoren 1,2-2,0, Colt & Orwicz sekundaer]
FEED_RULE_MEDIA_L_PER_G = {"kies": 1.0, "bioball": 0.5}   # Faustregel [Q R19: FAO 589, ca. 3-fach Reserve]
FEED_G_PER_L_FAO = {"bioball": 6.0, "substrat_min": 2.3, "substrat_max": 3.8}   # g Futter/l Medium/Tag [Q R19: FAO 589 Anh. 4, SSA 400 / 150 / 200-250]
LOSORDO_VTR_G_TAN_M3 = 350                             # Moving-Bed [Q R19: Losordo/DeLong 2015]
PLANT_FEED_G_M2 = (25, 45, 65)                         # g Futter je m2 und Tag: SRAC 454 (25 % Raft), Mitte, FAO Frucht [Q R20]
LEAF_G, FRUIT_G = 45, 72.5                             # Blatt (FAO 40-50), Frucht/Knolle (FAO 50-80, Mitte) [Q R20/R24]
FRUIT_SHARE_MIX = 0.35                                 # Bens Pflanzliste: 62 Tomaten + 151 Suesskartoffeln von 609 = 35 % [B]
SUBSTRATE_PER_KG_FISH_L = 32.5                         # l Kies je kg Fisch bei 1 : 2 und 61,5 kg/m3 [Q R20: SRAC 454]
TAN_TARGET_MG_L, BIOFILTER_EFF = 1.5, 0.5              # Durchflussrechnung [Q R21: Losordo/DeLong 2015, rekonstruiert]
SETTLER_MIN_RESIDENCE = 20                             # min, UVI-Klaerer [Q R19: SRAC 454]
# Huelle = Plane (D39), Empfehlung R24: doppelte luftgepolsterte UV-PE-Folie 6 mil mit IR-Sperre und Anti-Drip/Anti-Fog
AAB_M2, BBB_M2 = 5.014, 5.954                          # Dreiecksflaechen (Heron aus 3279/3279/3708 bzw. 3708) [E]
HULL_AREA = 30 * AAB_M2 + 10 * BBB_M2 - 2.0            # 40 ebene Dreiecke minus Tuerfeld = 208 m2 [E]
HULL_U = (2.8, 4.0, 5.7)                               # W/m2K PE doppelt mit IR-Sperre, Mitte, oben [Q R24: Purdue CEA 0,5/0,7 BTU, KSU 0,5-1,0]
GT_KD = 3500                                           # Gradtagzahl Gt20/15 Mitteleuropa [Q R24: DWD ueber Rechnerportal, Berlin 3542, Hamburg 3518], Standort offen
DT_DESIGN = 30                                         # K: innen 20, aussen -10 [A Mitteleuropa, Standort offen]
KEIL_M = 30 * 3.279 + 35 * 3.708                       # Keilschiene auf allen 65 Streben [E]
BLOWER_FILM_W = (60, 80, 100)                          # Geblaese Luftpolster [A, R24 ohne Datenblatt]
CONTROL_W = 40                                         # Steuerung [A]
MAX_FISH_KG_M3 = 20                                    # FAO 589 Tab. 8.1 [Q R17]


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
substrate_area = sum(v["n"] * v["w"] * v["l"] for v in BEDS.values())
def nft_len_of(ch): return sum(n * sum(c) for n, c in ch.values())
substrate_total = substrate_area * SUBSTRATE_DEPTH
beds_water = substrate_total * POROSITY
nft_len = sum(n * sum(ch) for n, ch in NFT_CHANNELS.values())
nft_channels = sum(n * len(ch) for n, ch in NFT_CHANNELS.values())
nft_water = nft_len * NFT_FILM_L_PER_M / 1000
pipes = PIPE_WATER_L / 1000
parts = [("Hauptbecken (Pool)", pool), ("Zweites Becken", basin2), ("Tanks (2 Absetzer, 2 Biofilter)", tanks),
         ("Beete (Porenwasser bei Flutung)", beds_water), ("NFT-Rinnen (Wasserfilm)", nft_water), ("Rohre und Schläuche", pipes)]
total = sum(v for _, v in parts)

# ---- Fische, Futter, Ammonium ----------------------------------------------------------------------------------------
fish_water = pool + basin2
biomass = FISH_KG_DESIGN
fish_n = round(biomass / FISH_END_WEIGHT)
feed_kg_day = biomass * FEED_PCT_BW
density = biomass / fish_water
tan_g = feed_kg_day * 1000 * TAN_FRACTION
table_biomass = TABLE_FISH_N * TABLE_FISH_KG
table_density = table_biomass / fish_water
table_tan_g = TABLE_FEED_KG_DAY * 1000 * TAN_FRACTION
table_tan_g_alt = TABLE_FEED_KG_DAY * 1000 * 0.35 * 0.092   # frueherer Ansatz 3,2 %

# ---- Filterkapazitaet --------------------------------------------------------------------------------------------------
media_biofilter_m3 = TANK_GROSS["n"] * pi * 0.40 ** 2 * 0.52          # Biomediumkorb Ø~0,8 m, 520 mm hoch [E]
cap_bio = media_biofilter_m3 * 1000 / FEED_RULE_MEDIA_L_PER_G["bioball"] / 1000   # kg Futter/Tag, Faustregel
cap_sub = substrate_total * 1000 / FEED_RULE_MEDIA_L_PER_G["kies"] / 1000
cap_media = cap_bio + cap_sub
cap_bio_fao = media_biofilter_m3 * FEED_G_PER_L_FAO["bioball"]          # kg Futter/Tag (m3 x g/l)
cap_bio_losordo = media_biofilter_m3 * LOSORDO_VTR_G_TAN_M3 / TAN_FRACTION / 1000
cap_sub_fao = (substrate_total * FEED_G_PER_L_FAO["substrat_min"], substrate_total * FEED_G_PER_L_FAO["substrat_max"])
nft_len3 = nft_len_of({**NFT_CHANNELS_BASE, "aussen": (8, OUTER_3)})
nft_len4 = nft_len_of({**NFT_CHANNELS_BASE, "aussen": (8, OUTER_4)})
nft_area_of = lambda ln: PLANT_AREA_NFT * ln / nft_len3          # Bens NFT-Flaeche auf die Rinnenlaenge skaliert [A]
plant_area = substrate_area + nft_area_of(nft_len)


def plant_scenario(ln):
    area = substrate_area + nft_area_of(ln)
    g_need = feed_kg_day * 1000 / area
    share = (g_need - LEAF_G) / (FRUIT_G - LEAF_G)               # noetiger Fruchtanteil bei Blatt 45 / Frucht 72,5 g
    mix_g = FRUIT_SHARE_MIX * FRUIT_G + (1 - FRUIT_SHARE_MIX) * LEAF_G
    return {"rinnen_aussen": 3 if ln == nft_len3 else 4, "rinnenlaenge_m": round(ln, 1), "nft_topf": POTS_NFT3 if ln == nft_len3 else POTS_NFT4,
            "nft_flaeche_m2": round(nft_area_of(ln), 1), "flaeche_gesamt_m2": round(area, 1), "noetig_g_m2": round(g_need),
            "noetiger_fruchtanteil": round(share, 2), "tragbar_bens_mix_kg": round(area * mix_g / 1000 / FEED_PCT_BW),
            "tragbar_blatt_kg": round(area * LEAF_G / 1000 / FEED_PCT_BW), "tragbar_frucht_kg": round(area * FRUIT_G / 1000 / FEED_PCT_BW)}


scen3, scen4 = plant_scenario(nft_len3), plant_scenario(nft_len4)
sc = scen4 if AUSSEN_RINNEN == 4 else scen3
mix_g = FRUIT_SHARE_MIX * FRUIT_G + (1 - FRUIT_SHARE_MIX) * LEAF_G
cap_mix = plant_area * mix_g / 1000
# ---- Pflanzmix (R26): Beete = Frucht/Knollen, NFT = Blatt/Kraeuter ----------------------------------------------------------
# Beete (Flaeche m2, Pflanzen je m2): FAO 589 Pflanzenblaetter (Tomate 3-5, Paprika 3-4, Gurke 2-5), Suesskartoffel 8/m2 [A aus Mortley u. a. 1991: 25 x 38 cm]
MIX_BEETE = [("Tomate", 9.0, 4.0), ("Paprika", 5.5, 3.5), ("Gurke (Rankhilfe)", 5.0, 3.0), ("Süßkartoffel", 7.8, 8.0)]
MIX_NFT = [("Salat", 250), ("Mangold", 100), ("Spinat", 80), ("Basilikum", 130), ("Petersilie", 70), ("Kräuter (Schnittlauch, Minze, Koriander)", 44)]
MIX_SCENARIOS = [("Empfehlungsmix, obere FAO-Werte", 80, 50), ("Mitte der FAO-Werte", 72.5, 45), ("Bens Mix gleichmäßig (35 % Frucht)", None, None),
                 ("untere FAO-Werte", 50, 40), ("SRAC-NFT (25 g)", 65, 25)]     # g Futter/m2/Tag Beete / NFT
nft_area_now = nft_area_of(nft_len)
mix_beete_area = sum(a for _, a, _ in MIX_BEETE)
mix_beete = [{"art": n, "flaeche_m2": a, "pflanzen_je_m2": d, "pflanzen": round(a * d)} for n, a, d in MIX_BEETE]
mix_nft_pots = sum(n for _, n in MIX_NFT)
mix_rows = []
for name, gb, gn in MIX_SCENARIOS:
    if gb is None:
        gb = gn = FRUIT_SHARE_MIX * FRUIT_G + (1 - FRUIT_SHARE_MIX) * LEAF_G
    feed = (substrate_area * gb + nft_area_now * gn) / 1000
    mix_rows.append({"szenario": name, "beete_g_m2": round(gb, 1), "nft_g_m2": round(gn, 1), "futter_kg_tag": round(feed, 2), "fisch_kg": round(feed / FEED_PCT_BW)})
mix_best = mix_rows[0]
cap_plants = tuple(plant_area * g / 1000 for g in PLANT_FEED_G_M2)      # kg Futter/Tag (niedrig, Mitte, hoch)
fish_kg_supported_by_substrate = substrate_total * 1000 / SUBSTRATE_PER_KG_FISH_L
fish_fit = min(cap_media, cap_plants[1]) / feed_kg_day
table_plants_cover = cap_plants[1] / TABLE_FEED_KG_DAY

# ---- Fluesse, Pumpen, Strom -------------------------------------------------------------------------------------------
nft_flow = nft_channels * NFT_FLOW_PER_CHANNEL                         # l/min
nft_flow_high = nft_channels * 2.0
bed_flow = beds_water * 1000 * FLOOD_CYCLES_PER_H / 60
circuit = nft_flow + bed_flow                                          # Bedarf Pflanzenstrom
circuit_high = nft_flow_high + bed_flow
pumps_main = PUMP_GROSS_N * PUMP_GROSS_L_MIN                           # D38 Hauptkreislauf
per_line = pumps_main / 2
p_hyd_main = 1000 * 9.81 * (pumps_main / 60000) * HEAD_M               # W gesamt
p_el_main = p_hyd_main / PUMP_EFF
settler_flow = PUMP_KLEIN_IN_BETRIEB * PUMP_KLEIN_L_MIN                # l/min, Teilstrom ueber beide Absetzer
p_el_small = 1000 * 9.81 * (settler_flow / 60000) * HEAD_M / PUMP_EFF
resid_small = t_klein * 1000 / PUMP_KLEIN_L_MIN                        # min je Absetzer-Tank mit einer Pumpe
resid_small_both = t_klein * 1000 / (2 * PUMP_KLEIN_L_MIN)             # beide Pumpen am Tank
tan_flow_l_min = tan_g * 1000 / (TAN_TARGET_MG_L * BIOFILTER_EFF) / 1440   # l/min, Durchfluss nach TAN
tan_flow_table = table_tan_g * 1000 / (TAN_TARGET_MG_L * BIOFILTER_EFF) / 1440
tan_feed_at_main = pumps_main * 1440 * TAN_TARGET_MG_L * BIOFILTER_EFF / 1000 / TAN_FRACTION / 1000   # kg Futter/Tag, die der Hauptkreislauf traegt
turnover_fish_h = fish_water * 1000 / pumps_main / 60

o2_fish = tuple(biomass * mg * 24 / 1e6 for mg in O2_FISH_MG_KG_H)     # kg O2/Tag
o2_nitrif = tan_g / 1000 * O2_NITRIF_PER_G_TAN
o2_total = tuple(x + o2_nitrif for x in o2_fish)
air_w = AIR_W_PER_KG_FISH * biomass                                    # Auslegung nach UVI-Geblaese
air_supply_kg = air_w * 24 / 1000 * AIR_KG_O2_PER_KWH                  # kg O2/Tag, die diese Leistung bei Feld-SAE liefert
air_w_by_o2 = o2_total[1] / AIR_KG_O2_PER_KWH * 1000 / 24              # nur aus dem Sauerstoffbedarf (Mitte)
blower_w = BLOWER_FILM_W[1]                                            # Geblaese Luftpolster der Doppelfolie
power_w = p_el_main + p_el_small + air_w + CONTROL_W + blower_w
p_hyd_small = 1000 * 9.81 * (settler_flow / 60000) * HEAD_M
power_lo = (p_hyd_main + p_hyd_small) / 0.33 + o2_total[0] / 2.0 * 1000 / 24 + CONTROL_W + BLOWER_FILM_W[0]      # Pumpen 33 %, SAE 2,0
power_hi = (p_hyd_main + p_hyd_small) / 0.16 + max(air_w, o2_total[2] * O2_PEAK_FACTOR / AIR_KG_O2_PER_KWH * 1000 / 24) + CONTROL_W + BLOWER_FILM_W[2]   # Pumpen 16 %
heat_w_per_k = tuple(round(HULL_AREA * u) for u in HULL_U)             # Doppelfolie: IR-Sperre, Mitte, oben
heat_kw_dt = [round(w * DT_DESIGN / 1000, 1) for w in heat_w_per_k]
heat_mwh_year = [round(w / 1000 * 24 * GT_KD / 1000) for w in heat_w_per_k]

checks = [
    ("Pflanzenzahl und Bepflanzung", POTS_BEDS + POTS_NFT >= POTS_TABLE, f"{POTS_BEDS + POTS_NFT} Topfplätze im Modell gegen mindestens {POTS_TABLE} (Kapazität); bepflanzt werden im Mix {sum(m['pflanzen'] for m in mix_beete)} Pflanzen in den Beeten ({sum(m['pflanzen'] for m in mix_beete) / substrate_area:.1f}/m², FAO Frucht 4–8) und {mix_nft_pots} in den NFT-Rinnen ({mix_nft_pots / nft_area_now:.1f}/m²)"),
    (f"Besatzdichte höchstens {MAX_FISH_KG_M3} kg/m³ (FAO 589)", density <= MAX_FISH_KG_M3, f"{density:.0f} kg/m³ im Beckenwasser {fish_water:.1f} m³ ({biomass} kg); Bens Tabelle {table_density:.0f} kg/m³ ({table_biomass:.0f} kg) liegt darüber und ist nur mit UVI-Technik (bis 60 kg/m³) belegt"),
    ("Biofilter-/Substratvolumen deckt das Futter (Faustregel)", cap_media >= feed_kg_day, f"deckt {cap_media:.1f} von {feed_kg_day:.1f} kg Futter/Tag ({cap_media / feed_kg_day:.0%}); nach FAO-Tabelle Bioballs {cap_bio_fao:.1f}, Substrat {cap_sub_fao[0]:.0f}–{cap_sub_fao[1]:.0f} kg/Tag (Faustregel hat ca. 3-fach Reserve)"),
    (f"Pflanzmix trägt die Auslegung (D40: {biomass} kg, {AUSSEN_RINNEN} Außenrinnen)", mix_best["futter_kg_tag"] >= 4.5, f"Empfehlungsmix (Beete {mix_best['beete_g_m2']:g} g/m², NFT {mix_best['nft_g_m2']:g} g/m², obere FAO-Werte) liefert {mix_best['futter_kg_tag']:.2f} kg Futter/Tag = {mix_best['fisch_kg']} kg Fisch gegen Ziel {feed_kg_day:.2f} (Spanne 4,5–5,0); Mitte der FAO-Werte {mix_rows[1]['fisch_kg']} kg, Bens Mix {mix_rows[2]['fisch_kg']} kg, untere FAO-Werte {mix_rows[3]['fisch_kg']} kg, SRAC-NFT {mix_rows[4]['fisch_kg']} kg (Rückfall)"),
    ("Substratvolumen trägt die Fischmenge (SRAC 1 : 2)", fish_kg_supported_by_substrate >= biomass, f"{substrate_total:.1f} m³ Substrat tragen nach SRAC 454 etwa {fish_kg_supported_by_substrate:.0f} kg Fisch gegen {biomass} kg Auslegung (Raft-/NFT-Flächen zusätzlich, nicht angerechnet)"),
    ("Bens Tabellenfutter gegen Pflanzfläche", cap_plants[1] >= TABLE_FEED_KG_DAY, f"Pflanzfläche deckt bei 45 g/m² nur {table_plants_cover:.0%} von Bens {TABLE_FEED_KG_DAY:.1f} kg Futter/Tag; nötig wären {TABLE_FEED_KG_DAY * 1000 / PLANT_FEED_G_M2[1]:.0f} m² statt {plant_area:.0f} m² (Frage 1 an Ben)"),
    ("Hauptkreislauf deckt den Pflanzenstrom (D38)", pumps_main >= circuit, f"4 Pumpen gross × {PUMP_GROSS_L_MIN} = {pumps_main} l/min gegen Bedarf {circuit:.0f} l/min (NFT {NFT_FLOW_PER_CHANNEL:g} l/min je Rinne); bei 2 l/min je Rinne {circuit_high:.0f} l/min ({'gedeckt' if pumps_main >= circuit_high else 'nicht gedeckt'})"),
    ("Hauptkreislauf trägt das Futter (TAN-Durchfluss)", pumps_main >= tan_flow_l_min, f"Bedarf {tan_flow_l_min:.0f} l/min bei {feed_kg_day:.1f} kg Futter (TAN {TAN_TARGET_MG_L:g} mg/l, Biofilter {BIOFILTER_EFF:.0%}); {pumps_main} l/min tragen bis {tan_feed_at_main:.1f} kg Futter/Tag; für Bens {TABLE_FEED_KG_DAY:.1f} kg wären {tan_flow_table:.0f} l/min nötig"),
    (f"Absetzer-Verweilzeit mindestens {SETTLER_MIN_RESIDENCE} min (UVI)", resid_small >= SETTLER_MIN_RESIDENCE, f"{t_klein * 1000:.0f} l je Absetzer bei {PUMP_KLEIN_L_MIN:g} l/min (eine kleine Pumpe je Tank) = {resid_small:.0f} min; mit beiden Pumpen {resid_small_both:.0f} min"),
    ("Belüftung deckt den Sauerstoffbedarf", air_supply_kg >= o2_total[2] * O2_PEAK_FACTOR, f"{air_w:.0f} W liefern bei {AIR_KG_O2_PER_KWH:g} kg O₂/kWh {air_supply_kg:.1f} kg/Tag gegen Bedarf {o2_total[0]:.1f}–{o2_total[2]:.1f} kg/Tag (Spitze ×{O2_PEAK_FACTOR:g}: {o2_total[2] * O2_PEAK_FACTOR:.1f})"),
    ("Hülle (Plane, D39) und Heizlast: Standort", False, f"PE doppelt {HULL_AREA:.0f} m²: {heat_w_per_k[1] / 1000:.2f} kW je Kelvin ({heat_w_per_k[0] / 1000:.2f}–{heat_w_per_k[2] / 1000:.2f}); bei ΔT {DT_DESIGN} K (Annahme Mitteleuropa −10/20 °C) {heat_kw_dt[1]} kW Spitze, Jahres-Obergrenze {heat_mwh_year[1]} MWh ohne Sonnengewinn; Standort offen, Heizung nicht in den Stromwerten"),
]

specs = {
    "stand": "30.10.2026",
    "hinweis": "Auslegung nach Fachrecherche R17–R24 und Entscheidung D40 (Biomasse 475 kg, Spanne 450–500, nur mit viel Fruchtgemüse und 4. Außenrinne voll gedeckt); Hülle = Plane (D39). Bens Tabellenwerte stehen daneben (tabelle_ben). Schätzung aus Modellmaßen und Literaturwerten, Standort offen. Keine fachliche Freigabe.",
    "wasser": {"gesamt_m3": round(total, 1), "teile": [(n, round(v, 2), f"{v / total:.0%}") for n, v in parts], "in_tanks_m3": round(tanks, 2),
               "tabelle_systemwasser_m3": 25, "fischwasser_m3": round(fish_water, 1)},
    "pflanzen": {"beete": POTS_BEDS, "nft": sc["nft_topf"], "gesamt": POTS_BEDS + sc["nft_topf"], "tabelle": POTS_TABLE, "rinnen": nft_channels,
                 "rinnenlaenge_m": round(nft_len, 1), "substrat_m3": round(substrate_total, 1),
                 "flaeche_substrat_m2": round(substrate_area, 1), "flaeche_substrat_tabelle_m2": PLANT_AREA_SUBSTRATE_TABLE,
                 "flaeche_nft_m2": round(nft_area_of(nft_len), 1), "flaeche_gesamt_m2": round(plant_area, 1),
                 "noetig_g_m2": sc["noetig_g_m2"], "noetiger_fruchtanteil": sc["noetiger_fruchtanteil"], "tragbar_bens_mix_kg": sc["tragbar_bens_mix_kg"],
                 "toepfe_je_m2_beet": round(POTS_BEDS / substrate_area), "dichte_empfohlen": "Blatt 20-25, Frucht 4-8 je m2 (FAO 589)"},
    "fische": {"anzahl": fish_n, "biomasse_kg": round(biomass), "futter_kg_tag": round(feed_kg_day, 2), "dichte_kg_m3": round(density), "tan_g_tag": round(tan_g),
               "spanne": {"biomasse_kg": [450, 500], "futter_kg_tag": [4.5, 5.0], "dichte_kg_m3": [16, 18]},
               "obergrenze_fao_kg": round(MAX_FISH_KG_M3 * fish_water), "substrat_traegt_kg": round(fish_kg_supported_by_substrate),
               "bedingung": f"{sc['noetiger_fruchtanteil']:.0%} Fruchtgemüse nötig bei {sc['rinnen_aussen']} Außenrinnen; Bens Mix {FRUIT_SHARE_MIX:.0%} trägt {sc['tragbar_bens_mix_kg']} kg (D40)",
               "tabelle_ben": {"anzahl": TABLE_FISH_N, "biomasse_kg": round(table_biomass), "futter_kg_tag": round(TABLE_FEED_KG_DAY, 1),
                               "dichte_kg_m3": round(table_density), "tan_g_tag": round(table_tan_g), "tan_g_tag_frueherer_ansatz": round(table_tan_g_alt)}},
    "fluesse": {"nft_l_min": round(nft_flow), "beete_l_min": round(bed_flow), "kreislauf_l_min": round(circuit), "kreislauf_m3_h": round(circuit * 0.06, 1),
                "je_linie_l_min": round(per_line), "umwaelzzeit_h": round(total * 1000 / pumps_main / 60, 1), "pumpe_hoehe_m": HEAD_M,
                "bedarf_nft_2_l_min": round(circuit_high), "hauptkreislauf_l_min": pumps_main, "hauptkreislauf_pumpen": f"{PUMP_GROSS_N} x {PUMP_GROSS_L_MIN} l/min (D38)",
                "absetzer_teilstrom_l_min": round(settler_flow, 1), "fischwasser_umlauf_h": round(turnover_fish_h, 1),
                "tan_durchfluss_l_min": round(tan_flow_l_min), "tan_durchfluss_tabelle_l_min": round(tan_flow_table),
                "tabelle_ben": {"kreislauf_modell_l_min": 143, "hinweis": "Bens Tabelle nennt nur 2 Pumpen ohne Daten; 143 l/min war die erste Rechnung (NFT 0,5 l/min)"}},
    "leistung": {"pumpe_hydraulisch_w": round(p_hyd_main / 2), "pumpe_elektrisch_w": round(p_el_main / 2), "pumpe_klein_w": round(p_el_small),
                 "belueftung_w": round(air_w), "steuerung_w": CONTROL_W, "geblaese_luftpolster_w": blower_w,
                 "gesamt_w": round(power_w), "kwh_tag": round(power_w * 24 / 1000, 1), "kwh_monat": round(power_w * 24 * 30 / 1000),
                 "spanne_w": [int(round(power_lo, -1)), int(round(power_hi, -1))], "hinweis_pumpe": "je Linie (2 Linien), 'pumpe_klein_w' = beide Absetzerpumpen zusammen",
                 "heizung": {"huelle_m2": round(HULL_AREA), "w_je_k": list(heat_w_per_k), "w_je_k_reihenfolge": "IR-Sperre, Mitte, oben",
                             "beispiel_dT30_kw": heat_kw_dt, "jahr_obergrenze_mwh": heat_mwh_year, "dT_k": DT_DESIGN, "gradtagzahl_kd": GT_KD,
                             "wasser_speicher_kwh_je_k": round(total * 1.163, 1),
                             "hinweis": "Huelle = Plane PE doppelt luftgepolstert (R24), 208 m2 aus 40 Facetten; Standort offen (Annahme Mitteleuropa -10/20 C), Jahreswert ohne Sonnengewinn, Infiltration und Thermoschirm; nicht in 'gesamt_w' enthalten"},
                 "tabelle_ben": {"strom_eur_monat": 219, "hinweis": "Bens Tabelle rechnet 219 EUR/Monat Strom (inkl. Heizung?), Zusammensetzung unbekannt"}},
    "sauerstoff": {"fisch_kg_tag": [round(x, 1) for x in o2_fish], "nitrifikation_kg_tag": round(o2_nitrif, 1), "gesamt_kg_tag": [round(x, 1) for x in o2_total],
                   "spitze_faktor": O2_PEAK_FACTOR, "belueftung_aus_bedarf_w": round(air_w_by_o2)},
    "filter": {"absetzer_klein_l": round(t_klein * 1000), "biofilter_gross_l": round(t_gross * 1000), "medium_biofilter_m3": round(media_biofilter_m3, 2),
               "kapazitaet_biofilter_kg_futter": round(cap_bio, 1), "kapazitaet_substrat_kg_futter": round(cap_sub, 1), "verweilzeit_absetzer_min": round(resid_small, 1),
               "kapazitaet_biofilter_fao_kg_futter": round(cap_bio_fao, 1), "kapazitaet_biofilter_losordo_kg_futter": round(cap_bio_losordo, 1),
               "kapazitaet_substrat_fao_kg_futter": [round(x) for x in cap_sub_fao], "absetzer_teilstrom_je_tank_l_min": PUMP_KLEIN_L_MIN,
               "anteil_am_fischwasser": f"{tanks / fish_water:.0%} (FAO: 10-30 %)"},
    "kapazitaet": {"medien_kg_futter_tag": round(cap_media, 1), "pflanzen_kg_futter_tag": round(cap_plants[1], 1),
                   "pflanzen_kg_futter_tag_spanne": [round(x, 1) for x in cap_plants], "passender_fischanteil": round(fish_fit, 2), "pflanzen_kg_futter_tag_bens_mix": round(cap_mix, 1),
                   "passender_fischanteil_bens_mix": round(min(cap_media, cap_mix) / feed_kg_day, 2),
                   "substrat_traegt_fisch_kg": round(fish_kg_supported_by_substrate)},
    "huelle": {"material": "PE-Folie doppelt luftgepolstert, UV-stabil, 6 mil (ca. 150 um), IR-Sperre, Anti-Drip/Anti-Fog (Empfehlung R24; Entscheidung D39: Plane)",
               "flaeche_m2": round(HULL_AREA), "u_w_m2k": {"ir_sperre": HULL_U[0], "mitte": HULL_U[1], "oben": HULL_U[2]},
               "befestigung": f"Alu-Keilschiene mit Federdraht auf allen 65 Streben, ca. {KEIL_M:.0f} m; Zuschnitt je Dreieck mit Ueberlappung",
               "lebensdauer_jahre": 4, "lichtdurchlass_prozent": "75-80 (doppelt), 90 (einlagig)", "geblaese_luftpolster_w": list(BLOWER_FILM_W),
               "paneele": "Doppelstegplatten (W19/W20, D35) bleiben als Variante, nicht eingerechnet", "standort": "offen (Frage an Ben)"},
    "pflanzmix": {"beete": mix_beete, "beete_pflanzen": sum(m["pflanzen"] for m in mix_beete), "beete_flaeche_m2": round(mix_beete_area, 1),
                  "nft": [{"art": n, "toepfe": k} for n, k in MIX_NFT], "nft_toepfe": mix_nft_pots, "nft_flaeche_m2": round(nft_area_now, 1),
                  "topfplaetze": {"gesamt": POTS_BEDS + POTS_NFT, "bepflanzt": sum(m["pflanzen"] for m in mix_beete) + mix_nft_pots,
                                  "anteil_beete": round(sum(m["pflanzen"] for m in mix_beete) / POTS_BEDS, 2), "anteil_nft": round(mix_nft_pots / POTS_NFT, 2)},
                  "szenarien": mix_rows, "empfehlung": mix_best, "ziel_futter_kg_tag": [4.3, 5.0], "rueckfall_fisch_kg": [mix_rows[3]["fisch_kg"], mix_rows[1]["fisch_kg"]],
                  "regel": "Besatz stufenweise erhoehen, Nitrat 5-150 mg/l halten (FAO 589: unter 5 Futter erhoehen, ueber 150 Wasser wechseln)",
                  "hinweis": "Futter je m2 aus FAO 589 (Blatt 40-50, Frucht 50-80), SRAC 454 NFT nur 25 % des Raft-Werts; Kohlrabi/Sellerie aus Bens Liste nur als Zwischenkultur, nicht im Hauptmix"},
    "szenario": {"aussen_rinnen": AUSSEN_RINNEN, "drei_rinnen": scen3, "vier_rinnen": scen4,
                 "hinweis": "aussen4 ist Standard (D43, W24 check_nft_fit 48/48): Rinnenlaengen und Toepfe aus nft_tisch.json; NFT-Flaeche aus Bens Tabellenflaeche (42,41 m2 bei aussen3-Laenge) auf die Rinnenlaenge skaliert [A]",
                 "frucht_blatt_g_m2": [FRUIT_G, LEAF_G], "bens_mix_frucht_anteil": FRUIT_SHARE_MIX},
    "offene_fragen": ["Standort und Aussenklima (Heizlast, Jahresenergie)", "4. Aussenrinne machbar (W24)?", "Anteil Fruchtgemuese/Knollen im Pflanzplan (nötig ca. 60-85 %, Bens Mix 35 %)",
                      "Zweites Becken: Besatz oder Brut/Quarantaene", "Notstrom und Alarm fuer die Belueftung", "Geblaese und Windlast der Plane"],
    "konsistenz": [{"pruefung": n, "ok": bool(ok), "detail": d} for n, ok, d in checks],
    "herkunft": {
        "biomasse_475_kg": "B/Entscheidung D40 (Ben: 450-500 kg); Obergrenze Q FAO 589 (20 kg/m3 = 570 kg), tragbar aus Pflanzflaeche E R20/R24: 380-420 kg",
        "huelle_plane": "Entscheidung D39; Material, U, Befestigung Q R24 (Kentucky State Univ., Purdue CEA, Domerama); Standort/Gradtage A",
        "vierte_rinne": "A Staffel fortgesetzt, Flaeche anteilig skaliert; bis W24-Zahlen da sind",
        "futter_1_prozent": "Q FAO 589 (R18)", "tan_3_75_prozent": "Q SRAC 451, FAO 589, Losordo/DeLong (R18/R19)",
        "nft_1_l_min": "Q FAO 589, HortTech (R21)", "flutzyklus_2_je_h": "Q Fort Valley State Extension (R21)", "pumpe_wirkungsgrad_25": "Q FAO 589 (R21), Spanne 16-33 %",
        "pumpen_d38": "A/E Entscheidung D38 (4 x 55 l/min Hauptkreislauf, 4 x 12,5 l/min Absetzer)",
        "futter_je_m2": "Q SRAC 454 (25), FAO 589 (45-65) (R20)", "o2_fisch": "Q Kim & Jo 1999a/b, Aly 2007 (R22)", "belueftung": "Q SRAC 454 UVI 0,59 W/kg (R22)",
        "o2_je_g_tan_4_57": "A Stoechiometrie, nicht aus Quelle gelesen", "heizung": "E aus Purdue CEA / KSU U-Werten fuer die Plane (R24), 208 m2, Standort offen",
        "tabelle_ben": "B reference/Kuppelberechnung-neu-2.xlsx (R15)"},
}
(ROOT / "data" / "system-specs.json").write_text(json.dumps(specs, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(specs, ensure_ascii=False, indent=1)[:6500])
