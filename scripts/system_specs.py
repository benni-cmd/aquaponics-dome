#!/usr/bin/env python3
"""Rechnet die Kuppel-Kennzahlen (Wasser, Pflanzen, Fluesse, Pumpenleistung, Filterkapazitaet, Heizung) aus den Modellmassen und
schreibt data/system-specs.json (der Viewer zeigt sie, solange nichts ausgewaehlt ist) und die Konsistenzpruefung.
Auslegung nach der Fachrecherche R17-R24 (docs/research/aquaponik-empfehlung.md, aquaponik-werte.md, R24.md Huelle) und Entscheidung D61
(Weg 1 nach R36: Tische ueber den Beeten, Beete nur Blatt/Kraeuter, Biomasse 346 kg, Spanne 308-385; D40 hatte 475 kg mit Fruchtgemuese);
Bens Tabellenwerte
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
FISH_KG_DESIGN = 346                                   # D61 (Ben): Weg 1 nach R36, Spanne 308-385 kg (untere / obere FAO-Werte); D40 hatte 475 kg mit Fruchtgemuese in den Beeten
D40_FISH_KG = 475                                      # frueherer Zielwert D40, nur als Vergleich
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
# D46 (Ben 31.10.): Drittbecken und 2 gestapelte IBC als Puffer-Station (R27)
PUFFER_N, PUFFER_L = 2, 1000                           # 2 IBC a 1000 l uebereinander, Stapelhoehe <= 2,5 m [D46]
THIRD_D, THIRD_H = 1.03, 1.13                          # Drittbecken Ø x Tiefe (Designer-Modell, Maß offen) [D46/E]
SYSTEM_LOSS_PCT_DAY = 0.02                             # Wasserverlust/Tag: weniger als 2 % [Q SRAC 454 / SRAC 451]
ALK_G_PER_G_TAN = 7.14                                 # g Alkalinitaet (als CaCO3) je g TAN-N nitrifiziert [Q Boyd 2016 (GAA), Timmons u. a. 2018 ueber Suchzusammenfassung]
ALK_PRACTICAL = 0.5                                    # praktischer Verbrauch gegen Theorie (Brune: 250 gegen 500 g NaHCO3/kg Futter) [A, eine Zusammenfassung]
EQ_G = {"Ca(OH)2": 37.05, "KOH": 56.11, "NaHCO3": 84.0}   # g je Aequivalent Alkalinitaet
QUARANTINE_FISH_PER_M3, QUARANTINE_FISH_G = 77, 79     # Besatz UVI Nile-Tilapia (SRAC 454 Tab. 1) [Q]
JUVENILE_FEED_PCT = 0.03                               # Jungfische 3 % KG/Tag [Q FAO 589]
SAMPLE_FLOW_L_MIN, STACK_HEAD_M = 3.0, 3.0             # Messkreis ueber den Stapel [A], Foerderhoehe 2,5 m Stapel + Reibung [E]
FILL_FLOW_L_MIN, FILL_H_PER_DAY = 17.0, 2.0            # Umpumpen/Fuellen 1 m3 in ca. 1 h, zwei Stunden am Tag [A]
SENSORS_W = {"pH EZO": 5 * 0.0183, "EC EZO": 5 * 0.050, "DO EZO": 5 * 0.050}   # Atlas Scientific Datenblaetter pH 18,3 mA, EC 50 mA bei 5 V; DO wie EC angenommen [Q/A]
DOSE_PUMP_W, DOSE_PUMP_N, DOSE_DUTY = 6.0, 2, 0.25     # 12-V-Schlauchpumpe 5-10 W (Kamoer, Haendler), 2 Stueck, 25 % Laufzeit [A]
PI_W = 5.0                                             # Messrechner/Steuerung der Station [A]
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
total_circuit = sum(v for _, v in parts)                               # Wasser im Kreislauf ohne Puffer und Drittbecken
puffer_m3 = PUFFER_N * PUFFER_L / 1000
third_m3 = pi * (THIRD_D / 2) ** 2 * THIRD_H
parts += [("Puffertanks (2 IBC gestapelt)", puffer_m3), ("Drittbecken", third_m3)]
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
K1_FILL = 0.67                                         # Fuellgrad lose K1-Traeger [Q Oedegaard 2006; D55]
K1_SSA_M2_M3 = 500                                     # m2 je m3 Schuettvolumen [Q Oedegaard 2006/WST 2009, Suchzusammenfassung, R30]
NITRI_RATE_FAO = 0.57                                  # g TAN/m2/Tag, FAO 589 konservativ [Q R19]
SIM_SAFETY = 2.5                                       # Simulator-Sicherheitsfaktor, nur Vergleich [R30]
media_biofilter_m3 = TANK_GROSS["n"] * t_gross * K1_FILL            # lose K1-Traeger in beiden Tanks, 67 % der Wasserfuellung [D55]
media_area_m2 = media_biofilter_m3 * K1_SSA_M2_M3                      # Traegerflaeche [E]
cap_bio = media_area_m2 * NITRI_RATE_FAO / SIM_SAFETY / TAN_FRACTION / 1000   # kg Futter/Tag, FAO-Rate mit Faktor 2,5
cap_sub = substrate_total * 1000 / FEED_RULE_MEDIA_L_PER_G["kies"] / 1000
cap_media = cap_bio + cap_sub
cap_bio_fao = media_area_m2 * NITRI_RATE_FAO / TAN_FRACTION / 1000      # kg Futter/Tag, FAO-Rate ohne Reserve
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
# ---- Pflanzmix (R26, seit D61/R36 Weg 1): Beete UND NFT = Blatt/Kraeuter (unter den Tischen kein Fruchtgemuese) ----------------------------------------------------------
# Beete (Flaeche m2, Pflanzen je m2): FAO 589 Pflanzenblaetter (Tomate 3-5, Paprika 3-4, Gurke 2-5), Suesskartoffel 8/m2 [A aus Mortley u. a. 1991: 25 x 38 cm]
MIX_BEETE = [("Salat", 9.0, 22.5), ("Mangold", 6.0, 17.5), ("Spinat", 4.3, 20.0), ("Petersilie", 4.0, 12.5), ("Kräuter (Basilikum, Schnittlauch, Minze, Koriander)", 4.0, 20.0)]   # Flaeche m2, Pflanzen/m2: FAO 589 Salat 20-25, Mangold 15-20, Petersilie 10-15; Spinat/Kraeuter 20 [A]
MIX_NFT = [("Salat", 250), ("Mangold", 100), ("Spinat", 80), ("Basilikum", 130), ("Petersilie", 70), ("Kräuter (Schnittlauch, Minze, Koriander)", 44)]
MIX_SCENARIOS = [("Obere FAO-Werte (Blatt 50 g)", 50, 50), ("Mitte der FAO-Werte (Blatt 45 g)", 45, 45),
                 ("Untere FAO-Werte (Blatt 40 g)", 40, 40), ("SRAC-NFT (25 g)", 45, 25)]     # g Futter/m2/Tag Beete / NFT
nft_area_now = nft_area_of(nft_len)
mix_beete_area = sum(a for _, a, _ in MIX_BEETE)
mix_beete = [{"art": n, "flaeche_m2": a, "pflanzen_je_m2": d, "pflanzen": round(a * d)} for n, a, d in MIX_BEETE]
mix_nft_pots = sum(n for _, n in MIX_NFT)
mix_rows = []
for name, gb, gn in MIX_SCENARIOS:
    feed = (substrate_area * gb + nft_area_now * gn) / 1000
    mix_rows.append({"szenario": name, "beete_g_m2": round(gb, 1), "nft_g_m2": round(gn, 1), "futter_kg_tag": round(feed, 2), "fisch_kg": round(feed / FEED_PCT_BW)})
mix_best = mix_rows[1]                                                  # Mitte der FAO-Werte = Auslegung D61 (346 kg)
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
# ---- Puffer-Station und Drittbecken (R27) -----------------------------------------------------------------------------------
loss_m3_day = total_circuit * SYSTEM_LOSS_PCT_DAY
puffer_days = puffer_m3 / loss_m3_day                                  # Tage Wasserverlust, die der Puffer deckt
alk_g_day = tan_g * ALK_G_PER_G_TAN                                    # g CaCO3/Tag theoretisch
alk_eq_day = alk_g_day / 50.0
alk_eq_pract = alk_eq_day * ALK_PRACTICAL
base_kg = {k: round(alk_eq_day * g / 1000, 2) for k, g in EQ_G.items()}
base_kg_pract = {k: round(alk_eq_pract * g / 1000, 2) for k, g in EQ_G.items()}
base_mix_kg = round(alk_eq_pract / 2 * (EQ_G["Ca(OH)2"] + EQ_G["KOH"]) / 1000, 2)   # je halb Ca(OH)2 und KOH (UVI wechselt ab)
third_fish = round(QUARANTINE_FISH_PER_M3 * third_m3)
third_kg = third_fish * QUARANTINE_FISH_G / 1000
third_max_kg = MAX_FISH_KG_M3 * third_m3
third_feed = third_kg * JUVENILE_FEED_PCT
third_tan_g = third_feed * 1000 * TAN_FRACTION
third_exchange_m3 = third_tan_g / 1.0                                 # m3/Tag bei TAN-Ziel 1 mg/l (g/m3 = mg/l), reiner Wasserwechsel
third_biofilter_l = third_feed * 1000 * FEED_RULE_MEDIA_L_PER_G["bioball"]    # l Bioballs nach Faustregel
puffer_pump_hyd = 1000 * 9.81 * (SAMPLE_FLOW_L_MIN / 60000) * STACK_HEAD_M
puffer_pump_el = puffer_pump_hyd / PUMP_EFF
fill_hyd = 1000 * 9.81 * (FILL_FLOW_L_MIN / 60000) * STACK_HEAD_M
fill_el_avg = fill_hyd / PUMP_EFF * FILL_H_PER_DAY / 24
sensors_w = sum(SENSORS_W.values())
dose_w_avg = DOSE_PUMP_W * DOSE_PUMP_N * DOSE_DUTY
puffer_w = sensors_w + PI_W + dose_w_avg + puffer_pump_el + fill_el_avg   # mittlere Leistung der Station
blower_w = BLOWER_FILM_W[1]                                            # Geblaese Luftpolster der Doppelfolie
power_w = p_el_main + p_el_small + air_w + CONTROL_W + blower_w + puffer_w
p_hyd_small = 1000 * 9.81 * (settler_flow / 60000) * HEAD_M
power_lo = (p_hyd_main + p_hyd_small) / 0.33 + o2_total[0] / 2.0 * 1000 / 24 + CONTROL_W + BLOWER_FILM_W[0] + puffer_w * 0.5      # Pumpen 33 %, SAE 2,0
power_hi = (p_hyd_main + p_hyd_small) / 0.16 + max(air_w, o2_total[2] * O2_PEAK_FACTOR / AIR_KG_O2_PER_KWH * 1000 / 24) + CONTROL_W + BLOWER_FILM_W[2] + puffer_w * 1.5   # Pumpen 16 %
heat_w_per_k = tuple(round(HULL_AREA * u) for u in HULL_U)             # Doppelfolie: IR-Sperre, Mitte, oben
heat_kw_dt = [round(w * DT_DESIGN / 1000, 1) for w in heat_w_per_k]
heat_mwh_year = [round(w / 1000 * 24 * GT_KD / 1000) for w in heat_w_per_k]

checks = [
    ("Pflanzenzahl und Bepflanzung", POTS_BEDS + POTS_NFT >= POTS_TABLE, f"{POTS_BEDS + POTS_NFT} Topfplätze im Modell gegen mindestens {POTS_TABLE} (Kapazität); bepflanzt werden im Mix {sum(m['pflanzen'] for m in mix_beete)} Pflanzen in den Beeten ({sum(m['pflanzen'] for m in mix_beete) / substrate_area:.1f}/m², Blatt/Kräuter, FAO 20–25 für Salat) und {mix_nft_pots} in den NFT-Rinnen ({mix_nft_pots / nft_area_now:.1f}/m²)"),
    (f"Besatzdichte höchstens {MAX_FISH_KG_M3} kg/m³ (FAO 589)", density <= MAX_FISH_KG_M3, f"{density:.0f} kg/m³ im Beckenwasser {fish_water:.1f} m³ ({biomass} kg); Bens Tabelle {table_density:.0f} kg/m³ ({table_biomass:.0f} kg) liegt darüber und ist nur mit UVI-Technik (bis 60 kg/m³) belegt"),
    ("Biofilter-/Substratvolumen deckt das Futter (Faustregel)", cap_media >= feed_kg_day, f"deckt {cap_media:.1f} von {feed_kg_day:.1f} kg Futter/Tag ({cap_media / feed_kg_day:.0%}); Biofilter mit K1-Traegern {media_biofilter_m3:.2f} m³ = {media_area_m2:.0f} m² (FAO-Rate {cap_bio_fao:.1f} kg/Tag, mit Faktor 2,5 {cap_bio:.1f}), Substrat nach FAO-Tabelle {cap_sub_fao[0]:.0f}–{cap_sub_fao[1]:.0f} kg/Tag (Substrat-Faustregel hat ca. 3-fach Reserve)"),
    (f"Pflanzmix trägt die Auslegung (D61: {biomass} kg, Weg 1 Blatt/Kräuter, {AUSSEN_RINNEN} Außenrinnen)", mix_best["futter_kg_tag"] >= feed_kg_day, f"Mitte der FAO-Werte (Beete {mix_best['beete_g_m2']:g} g/m², NFT {mix_best['nft_g_m2']:g} g/m²) liefert {mix_best['futter_kg_tag']:.2f} kg Futter/Tag = {mix_best['fisch_kg']} kg Fisch gegen Ziel {feed_kg_day:.2f}; obere FAO-Werte {mix_rows[0]['fisch_kg']} kg, untere {mix_rows[2]['fisch_kg']} kg, SRAC-NFT {mix_rows[3]['fisch_kg']} kg (Rückfall); Rinnenraster als NFT-Fläche gäbe etwa 20–25 % weniger (R36)"),
    ("Substratvolumen trägt die Fischmenge (SRAC 1 : 2)", fish_kg_supported_by_substrate >= biomass, f"{substrate_total:.1f} m³ Substrat tragen nach SRAC 454 etwa {fish_kg_supported_by_substrate:.0f} kg Fisch gegen {biomass} kg Auslegung (Raft-/NFT-Flächen zusätzlich, nicht angerechnet)"),
    ("Bens Tabellenfutter gegen Pflanzfläche", cap_plants[1] >= TABLE_FEED_KG_DAY, f"Pflanzfläche deckt bei 45 g/m² nur {table_plants_cover:.0%} von Bens {TABLE_FEED_KG_DAY:.1f} kg Futter/Tag; nötig wären {TABLE_FEED_KG_DAY * 1000 / PLANT_FEED_G_M2[1]:.0f} m² statt {plant_area:.0f} m² (Frage 1 an Ben)"),
    ("Hauptkreislauf deckt den Pflanzenstrom (D38)", pumps_main >= circuit, f"4 Pumpen gross × {PUMP_GROSS_L_MIN} = {pumps_main} l/min gegen Bedarf {circuit:.0f} l/min (NFT {NFT_FLOW_PER_CHANNEL:g} l/min je Rinne); bei 2 l/min je Rinne {circuit_high:.0f} l/min ({'gedeckt' if pumps_main >= circuit_high else 'nicht gedeckt'})"),
    ("Hauptkreislauf trägt das Futter (TAN-Durchfluss)", pumps_main >= tan_flow_l_min, f"Bedarf {tan_flow_l_min:.0f} l/min bei {feed_kg_day:.1f} kg Futter (TAN {TAN_TARGET_MG_L:g} mg/l, Biofilter {BIOFILTER_EFF:.0%}); {pumps_main} l/min tragen bis {tan_feed_at_main:.1f} kg Futter/Tag; für Bens {TABLE_FEED_KG_DAY:.1f} kg wären {tan_flow_table:.0f} l/min nötig"),
    (f"Absetzer-Verweilzeit mindestens {SETTLER_MIN_RESIDENCE} min (UVI)", resid_small >= SETTLER_MIN_RESIDENCE, f"{t_klein * 1000:.0f} l je Absetzer bei {PUMP_KLEIN_L_MIN:g} l/min (eine kleine Pumpe je Tank) = {resid_small:.0f} min; mit beiden Pumpen {resid_small_both:.0f} min"),
    ("Belüftung deckt den Sauerstoffbedarf", air_supply_kg >= o2_total[2] * O2_PEAK_FACTOR, f"{air_w:.0f} W liefern bei {AIR_KG_O2_PER_KWH:g} kg O₂/kWh {air_supply_kg:.1f} kg/Tag gegen Bedarf {o2_total[0]:.1f}–{o2_total[2]:.1f} kg/Tag (Spitze ×{O2_PEAK_FACTOR:g}: {o2_total[2] * O2_PEAK_FACTOR:.1f})"),
    ("Puffertanks decken Wasserverlust und Frischwasser-Ruhe (R27)", puffer_days >= 2, f"{puffer_m3:.1f} m³ Puffer decken {puffer_days:.1f} Tage Wasserverlust bei {SYSTEM_LOSS_PCT_DAY:.0%}/Tag ({loss_m3_day:.2f} m³/Tag, SRAC 454: unter 2 %) und lassen Frischwasser 2 Tage stehen (Chlor, FAO 589); {puffer_m3 / total * 100:.0f} % des Systemwassers (UVI-Sumpf + Basentank: 0,7 %)"),
    ("Drittbecken als Quarantäne (R27)", False, f"{third_m3:.2f} m³ nehmen nach UVI-Besatz {third_fish} Fische à {QUARANTINE_FISH_G} g ({third_kg:.1f} kg; FAO-Max {third_max_kg:.0f} kg); Futter {third_feed * 1000:.0f} g/Tag → {third_tan_g:.1f} g TAN/Tag: reiner Wasserwechsel bräuchte {third_exchange_m3:.1f} m³/Tag (TAN 1 mg/l), also eigener kleiner Biofilter (ca. {third_biofilter_l:.0f} l Bioballs) und Belüftung nötig; FAO: Neufische 45 Tage isolieren"),
    ("Hülle (Plane, D39) und Heizlast: Standort", False, f"PE doppelt {HULL_AREA:.0f} m²: {heat_w_per_k[1] / 1000:.2f} kW je Kelvin ({heat_w_per_k[0] / 1000:.2f}–{heat_w_per_k[2] / 1000:.2f}); bei ΔT {DT_DESIGN} K (Annahme Mitteleuropa −10/20 °C) {heat_kw_dt[1]} kW Spitze, Jahres-Obergrenze {heat_mwh_year[1]} MWh ohne Sonnengewinn; Standort offen, Heizung nicht in den Stromwerten"),
]

# ---- Puffer klein (R37, D63): Fass-Varianten im Dom, nur zusaetzlich; Standard bleibt Puffer-Station 2 IBC (D46) bis zur Entscheidung -------
# Fass-Masse [Q Haendler: Kaufland/denios/toom 120 l Weithals Ø 470-500 x 795-800 mm; freshdi 200 l Ø 570-600 x 930-1000 mm, zweite Quelle fehlt]
BARREL_120 = dict(l=120, d=0.47, h=0.80, raster=0.50)
BARREL_200 = dict(l=200, d=0.60, h=0.95, raster=0.60)
STOCK_G_L = {"KOH": 100, "NaHCO3": 96, "Ca(OH)2": 100}   # Arbeitsloesung g/l: NaHCO3 96 g/l Loeslichkeit 20 C [Q Merck SDB]; KOH 100 [A, Loeslichkeit nicht gelesen]; Ca(OH)2 loest nur 1,7 g/l [Q Merck/VWR, Wikipedia] -> Kalkmilch 100 g/l [A]
DOSE_TANK_L, MEASURE_CELL_L, IRON_L = 120, 20, 20      # Stammloesungsfass, Messzelle (3 l/min -> ca. 7 min Verweilzeit), Eisenchelat-Kanister (74 g Fe je 3 Wochen)
CISTERN_L = 3000                                       # Erdtank aussen [Q Haendlerpreise 899-1097 EUR nur Tank, 1649-2469 EUR Komplettsets]
MEASURE_HEAD_M = 1.5                                   # Messzelle neben dem Verteiler statt 2,5-m-Stapel [A]
third_small_m3 = pi * 0.4 ** 2 * 0.8                   # Drittbecken klein Ø 0,8 x 0,8 m [A]
ts_fish = round(QUARANTINE_FISH_PER_M3 * third_small_m3)
ts_kg = ts_fish * QUARANTINE_FISH_G / 1000
ts_feed = ts_kg * JUVENILE_FEED_PCT
ts_tan = ts_feed * 1000 * TAN_FRACTION
water_without_puffer = total - puffer_m3 - third_m3
stock_days = {k: round(DOSE_TANK_L / (base_kg_pract[k] * 1000 / STOCK_G_L[k]), 1) for k in STOCK_G_L}
meas_w = 1000 * 9.81 * (SAMPLE_FLOW_L_MIN / 60000) * MEASURE_HEAD_M / PUMP_EFF
fill_w_b = 1000 * 9.81 * (FILL_FLOW_L_MIN / 60000) * MEASURE_HEAD_M / PUMP_EFF * FILL_H_PER_DAY / 24


def puffer_variant(key, name, fresh_n, cistern_l, rolle):
    dom_l = DOSE_TANK_L + MEASURE_CELL_L + IRON_L + fresh_n * BARREL_200["l"]
    area = BARREL_120["raster"] ** 2 + 0.30 * 0.25 + 0.25 * 0.25 + fresh_n * BARREL_200["raster"] ** 2   # Raster-Grundflaeche m2 (Fass + Messzelle + Kanister)
    fresh_l = fresh_n * BARREL_200["l"] + cistern_l
    strom = sensors_w + PI_W + dose_w_avg + meas_w + (fill_w_b if fresh_n else 0)
    return {"key": key, "name": name, "im_dom_l": dom_l, "im_dom_m3": round(dom_l / 1000, 2), "anteil_wasser_prozent": round(dom_l / 10 / (water_without_puffer + dom_l / 1000), 2),
            "frischwasser_l": fresh_l, "frischwasser_tage_bei_verlust": [round(fresh_l / 1000 / (loss_m3_day * f), 1) for f in (1.0, 0.5)],
            "grundflaeche_m2": round(area, 2), "grundflaeche_gespart_gegen_station_m2": round(2.42 * 1.92 - area, 1), "strom_w": round(strom, 1), "rolle": rolle,
            "fass_zahl": {"fass_120": 1, "fass_200": fresh_n}, "zisterne_aussen_l": cistern_l}


puffer_klein = {
    "standard": "puffer_station_2_ibc (D46) bis Entscheidung Ben", "pflicht": ["Messzelle (Sonden pH, EC, Temperatur, O2, Nitrat) im Messkreis 3 l/min", "Stammloesungsfass Base (Ca(OH)2/KOH/NaHCO3)", "Eisenchelat-Kanister", "entchlortes Nachfuellwasser (Quelle, nicht Menge)"],
    "komfort": ["2 Tage stehendes Frischwasser (FAO 589: 1,4 m3 bei 0,68 m3/Tag)", "Notvorrat ueber Stunden hinaus", "Stapel-Schwerkraft"],
    "bedarf": {"verlust_m3_tag_2prozent": round(loss_m3_day, 2), "verlust_m3_tag_1prozent": round(loss_m3_day / 2, 2), "uvi_anteil_m3": round(0.007 * total, 2), "stammloesung_tage_je_120l": stock_days},
    "optionen": [puffer_variant("A", "A Minimal im Dom: Dosierfass 120 l + Messzelle + Eisen, Nachfuellwasser direkt ueber Aktivkohle", 0, 0, "Mess-, Dosier-, Eisenstation; kein Vorrat"),
                 puffer_variant("B", "B Fass-Station mit Tagesreserve: wie A + 3 x 200-l-Fass belueftet", 3, 0, "wie A + 0,6 m3 Nachfuell- und Notvorrat im Dom"),
                 puffer_variant("C", "C Minimal im Dom (wie A) + Zisterne 3 m3 aussen (Erdtank, Regenwasser)", 0, CISTERN_L, "wie A + Frischwasser/Notvorrat aussen")],
    "drittbecken_klein": {"durchmesser_m": 0.8, "tiefe_m": 0.8, "volumen_m3": round(third_small_m3, 2), "fische_uvi": ts_fish, "kg": round(ts_kg, 1), "fao_max_kg": round(MAX_FISH_KG_M3 * third_small_m3, 1),
                          "futter_g_tag": round(ts_feed * 1000), "tan_g_tag": round(ts_tan, 1), "wasserwechsel_m3_tag_ohne_biofilter": round(ts_tan, 1), "biofilter_bioballs_l": round(ts_feed * 1000 * FEED_RULE_MEDIA_L_PER_G["bioball"]),
                          "grundflaeche_m2_mit_60mm": round(pi * (0.4 + 0.06) ** 2, 2), "grundflaeche_gespart_m2": round(pi * (THIRD_D / 2 + 0.06) ** 2 - pi * (0.4 + 0.06) ** 2, 2),
                          "notbecken": f"nur Zuchttiere/Kranke (max. {MAX_FISH_KG_M3 * third_small_m3:.0f} kg bei 20 kg/m3); Notaufnahme des Pools (346 kg) nicht moeglich, das Zweitbecken (2,4 m3, max. 48 kg) uebernimmt nur Teile"},
    "hinweis": "Zahlen R37; Fass-Masse und Preise sind Haendlerangaben (Snapshot), Stammloesungs-Konzentrationen KOH/Kalkmilch Annahmen; keine Layoutaenderung, Standard bleibt Puffer-Station 2 IBC bis zur Entscheidung (D63)."}

# ---- Beete unter den Tischen (R36, D60): Weg 1 = Standard, Weg 2 = Pruefszenarien; Rechnung in scripts/bed_table_variants.py ----
import bed_table_variants as btv
assert len(NFT_CHANNELS["aussen"][1]) == 4 and POTS_NFT == 674, "Szenarien weg1/weg2 gelten fuer aussen4 (D43)"
beete_tische = {"standard": "weg1", "szenarien": [
    {"name": n, "tische": c["tische"], "rinnen": c["rinnen"], "nft_toepfe": c["toepfe"], "nft_flaeche_m2": round(c["nft_m2"], 1),
     "beet_frucht_m2": round(c["beet_frucht_m2"], 1), "beet_blatt_m2": round(c["beet_blatt_m2"], 1),
     "fisch_kg_oben_mitte_unten": [round(x) for x in c["fisch_kg"]], "verlust_gegen_475_kg_mitte": round(c["fisch_kg"][1] - D40_FISH_KG),
     "fruchtpflanzen": sum(c["fruchtpflanzen"].values()), "blattpflanzen_beet": c["blattpflanzen_beet"]}
    for key, (n, r, b) in zip(("d40_annahme", "weg1", "weg2a", "weg2b", "weg2c"), btv.VARIANTS) for c in [btv.compute(n, r, b)]],
    "hinweis": "Planungsstand Weg 1 (D60). Futter je m2 aus R26 (obere / Mitte / untere FAO-Werte), NFT-Flaeche wie R26 aus Bens Tabelle skaliert; mit Rinnenraster als NFT-Flaeche 20-25 % weniger Fisch in allen Varianten (R36). Seit D61 gilt Weg 1: Pflanzmix, Fischmenge (346 kg) und Konsistenzpruefungen rechnen mit Beeten Blatt/Kraeuter; die Zeile D40-Annahme (475 kg) bleibt als Vergleich."}

specs = {
    "stand": "31.10.2026",
    "hinweis": "Auslegung nach Fachrecherche R17–R24 und Entscheidung D61 (Weg 1 nach R36: Tische über den Beeten, Beete nur Blatt/Kräuter, Biomasse 346 kg, Spanne 308–385; D40 hatte 475 kg mit Fruchtgemüse); Hülle = Plane (D39). Bens Tabellenwerte stehen daneben (tabelle_ben). Schätzung aus Modellmaßen und Literaturwerten, Standort offen. Keine fachliche Freigabe.",
    "wasser": {"gesamt_m3": round(total, 1), "teile": [(n, round(v, 2), f"{v / total:.0%}") for n, v in parts], "in_tanks_m3": round(tanks, 2), "im_kreislauf_m3": round(total_circuit, 1),
               "tabelle_systemwasser_m3": 25, "fischwasser_m3": round(fish_water, 1)},
    "pflanzen": {"beete": POTS_BEDS, "nft": sc["nft_topf"], "gesamt": POTS_BEDS + sc["nft_topf"], "tabelle": POTS_TABLE, "rinnen": nft_channels,
                 "rinnenlaenge_m": round(nft_len, 1), "substrat_m3": round(substrate_total, 1),
                 "flaeche_substrat_m2": round(substrate_area, 1), "flaeche_substrat_tabelle_m2": PLANT_AREA_SUBSTRATE_TABLE,
                 "flaeche_nft_m2": round(nft_area_of(nft_len), 1), "flaeche_gesamt_m2": round(plant_area, 1),
                 "noetig_g_m2": sc["noetig_g_m2"], "noetiger_fruchtanteil": sc["noetiger_fruchtanteil"], "tragbar_bens_mix_kg": sc["tragbar_bens_mix_kg"],
                 "toepfe_je_m2_beet": round(POTS_BEDS / substrate_area), "dichte_empfohlen": "Blatt 20-25, Frucht 4-8 je m2 (FAO 589)"},
    "fische": {"anzahl": fish_n, "biomasse_kg": round(biomass), "futter_kg_tag": round(feed_kg_day, 2), "dichte_kg_m3": round(density), "tan_g_tag": round(tan_g),
               "spanne": {"biomasse_kg": [mix_rows[2]["fisch_kg"], mix_rows[0]["fisch_kg"]], "futter_kg_tag": [mix_rows[2]["futter_kg_tag"], mix_rows[0]["futter_kg_tag"]], "dichte_kg_m3": [round(mix_rows[2]["fisch_kg"] / fish_water), round(mix_rows[0]["fisch_kg"] / fish_water)]},
               "obergrenze_fao_kg": round(MAX_FISH_KG_M3 * fish_water), "substrat_traegt_kg": round(fish_kg_supported_by_substrate),
               "bedingung": f"Weg 1 (D61): Beete unter den Tischen nur Blatt/Kräuter, kein Fruchtanteil nötig; {sc['rinnen_aussen']} Außenrinnen, Auslegung = Mitte der FAO-Werte, Spanne untere bis obere FAO-Werte; D40 (475 kg) setzte ca. 61 % Fruchtgemüse voraus",
               "tabelle_ben": {"anzahl": TABLE_FISH_N, "biomasse_kg": round(table_biomass), "futter_kg_tag": round(TABLE_FEED_KG_DAY, 1),
                               "dichte_kg_m3": round(table_density), "tan_g_tag": round(table_tan_g), "tan_g_tag_frueherer_ansatz": round(table_tan_g_alt)}},
    "fluesse": {"nft_l_min": round(nft_flow), "beete_l_min": round(bed_flow), "kreislauf_l_min": round(circuit), "kreislauf_m3_h": round(circuit * 0.06, 1),
                "je_linie_l_min": round(per_line), "umwaelzzeit_h": round(total_circuit * 1000 / pumps_main / 60, 1), "pumpe_hoehe_m": HEAD_M,
                "bedarf_nft_2_l_min": round(circuit_high), "hauptkreislauf_l_min": pumps_main, "hauptkreislauf_pumpen": f"{PUMP_GROSS_N} x {PUMP_GROSS_L_MIN} l/min (D38)",
                "absetzer_teilstrom_l_min": round(settler_flow, 1), "fischwasser_umlauf_h": round(turnover_fish_h, 1),
                "tan_durchfluss_l_min": round(tan_flow_l_min), "tan_durchfluss_tabelle_l_min": round(tan_flow_table),
                "tabelle_ben": {"kreislauf_modell_l_min": 143, "hinweis": "Bens Tabelle nennt nur 2 Pumpen ohne Daten; 143 l/min war die erste Rechnung (NFT 0,5 l/min)"}},
    "leistung": {"pumpe_hydraulisch_w": round(p_hyd_main / 2), "pumpe_elektrisch_w": round(p_el_main / 2), "pumpe_klein_w": round(p_el_small),
                 "belueftung_w": round(air_w), "steuerung_w": CONTROL_W, "puffer_station_w": round(puffer_w), "geblaese_luftpolster_w": blower_w,
                 "gesamt_w": round(power_w), "kwh_tag": round(power_w * 24 / 1000, 1), "kwh_monat": round(power_w * 24 * 30 / 1000),
                 "spanne_w": [int(round(power_lo, -1)), int(round(power_hi, -1))], "hinweis_pumpe": "je Linie (2 Linien), 'pumpe_klein_w' = beide Absetzerpumpen zusammen",
                 "heizung": {"huelle_m2": round(HULL_AREA), "w_je_k": list(heat_w_per_k), "w_je_k_reihenfolge": "IR-Sperre, Mitte, oben",
                             "beispiel_dT30_kw": heat_kw_dt, "jahr_obergrenze_mwh": heat_mwh_year, "dT_k": DT_DESIGN, "gradtagzahl_kd": GT_KD,
                             "wasser_speicher_kwh_je_k": round(total * 1.163, 1),
                             "hinweis": "Huelle = Plane PE doppelt luftgepolstert (R24), 208 m2 aus 40 Facetten; Standort offen (Annahme Mitteleuropa -10/20 C), Jahreswert ohne Sonnengewinn, Infiltration und Thermoschirm; nicht in 'gesamt_w' enthalten"},
                 "tabelle_ben": {"strom_eur_monat": 219, "hinweis": "Bens Tabelle rechnet 219 EUR/Monat Strom (inkl. Heizung?), Zusammensetzung unbekannt"}},
    "sauerstoff": {"fisch_kg_tag": [round(x, 1) for x in o2_fish], "nitrifikation_kg_tag": round(o2_nitrif, 1), "gesamt_kg_tag": [round(x, 1) for x in o2_total],
                   "spitze_faktor": O2_PEAK_FACTOR, "belueftung_aus_bedarf_w": round(air_w_by_o2)},
    "filter": {"absetzer_klein_l": round(t_klein * 1000), "biofilter_gross_l": round(t_gross * 1000), "medium_biofilter_m3": round(media_biofilter_m3, 2), "medium_biofilter_flaeche_m2": round(media_area_m2), "medium_biofilter_art": "lose K1-Traeger, Fuellgrad 67 % (D55)",
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
    "puffer": {"volumen_m3": puffer_m3, "anteil_wasser": f"{puffer_m3 / total:.0%}", "deckt_wasserverlust_tage": round(puffer_days, 1), "wasserverlust_m3_tag": round(loss_m3_day, 2),
               "stapel": {"ibc": PUFFER_N, "hoehe_max_m": 2.5, "obere": "Messtank mit Schwerkraftablauf in die untere IBC", "foerderhoehe_m": STACK_HEAD_M,
                          "messkreis_l_min": SAMPLE_FLOW_L_MIN, "messpumpe_w": round(puffer_pump_el, 1), "umpumpen_l_min": FILL_FLOW_L_MIN, "umpumpen_w_mittel": round(fill_el_avg, 1)},
               "rollen": ["Messstation (pH, EC, Temperatur, O2, Nitrat)", "Basenzugabe und Naehrstoffausgleich (K, Ca, Fe) wie UVI-Basentank", "Frischwasser stehen lassen (2 Tage) und Wasserwechsel-Reserve", "Notvorrat"],
               "messgroessen": {"pH": "7,0-7,5 (UVI, Fort Valley State; FAO-Kompromiss 6-7)", "Nitrat": "5-150 mg/l (FAO 589)", "O2": "4-8 mg/l", "Nitrit": "unter 0,25 mg/l"},
               "dosierung": {"alkalinitaet_g_caco3_tag_theorie": round(alk_g_day), "aequivalente_tag_theorie": round(alk_eq_day, 1), "praktisch_faktor": ALK_PRACTICAL,
                             "theorie_kg_tag": base_kg, "praktisch_kg_tag": base_kg_pract, "mix_halb_ca_halb_koh_praktisch_kg_tag": base_mix_kg,
                             "eisen": f"Fe-Chelat 2 mg/l alle ca. 3 Wochen = {2 * total:.0f} g Fe je Gabe, ca. {2 * total / 21:.1f} g Fe/Tag",
                             "hinweis": "Nitrifikation verbraucht 7,14 g Alkalinitaet je g TAN (Boyd 2016); K-Bedarf der Pflanzen (ca. 0,4 g/m2/Tag, Graber/Junge, Abstract) ist viel kleiner als die KOH-Menge: Verhaeltnis Ca(OH)2/KOH nach Messung (EC, K) einstellen"},
               "strom_w": {"sensoren": round(sensors_w, 2), "rechner": PI_W, "dosierpumpen_mittel": round(dose_w_avg, 1), "messpumpe": round(puffer_pump_el, 1), "umpumpen_mittel": round(fill_el_avg, 1), "summe": round(puffer_w, 1)}},
    "drittbecken": {"durchmesser_m": THIRD_D, "tiefe_m": THIRD_H, "volumen_m3": round(third_m3, 2), "mass_status": "Designer-Modell, Maß von Ben offen (D46)",
                    "rolle": "Quarantaene und Krankenbecken (Neufische 45 Tage isolieren, FAO 589), zugleich Notbecken; Zweitbecken (2,4 m3) bleibt Aufzucht (D45 d)",
                    "besatz_uvi": {"fische": third_fish, "einzelgewicht_g": QUARANTINE_FISH_G, "kg": round(third_kg, 1), "fao_max_kg": round(third_max_kg, 1)},
                    "futter_g_tag": round(third_feed * 1000), "tan_g_tag": round(third_tan_g, 1), "wasserwechsel_m3_tag_ohne_biofilter": round(third_exchange_m3, 1), "biofilter_bioballs_l": round(third_biofilter_l),
                    "noetig": "eigene Belueftung und kleiner Biofilter, Wasserwechsel aus dem Puffer"},
    "pflanzmix": {"beete": mix_beete, "beete_pflanzen": sum(m["pflanzen"] for m in mix_beete), "beete_flaeche_m2": round(mix_beete_area, 1),
                  "nft": [{"art": n, "toepfe": k} for n, k in MIX_NFT], "nft_toepfe": mix_nft_pots, "nft_flaeche_m2": round(nft_area_now, 1),
                  "topfplaetze": {"gesamt": POTS_BEDS + POTS_NFT, "bepflanzt": sum(m["pflanzen"] for m in mix_beete) + mix_nft_pots,
                                  "anteil_beete": round(sum(m["pflanzen"] for m in mix_beete) / POTS_BEDS, 2), "anteil_nft": round(mix_nft_pots / POTS_NFT, 2)},
                  "szenarien": mix_rows, "empfehlung": mix_best, "ziel_futter_kg_tag": [mix_rows[2]["futter_kg_tag"], mix_rows[0]["futter_kg_tag"]], "rueckfall_fisch_kg": [mix_rows[3]["fisch_kg"], mix_rows[2]["fisch_kg"]],
                  "regel": "Besatz stufenweise erhoehen, Nitrat 5-150 mg/l halten (FAO 589: unter 5 Futter erhoehen, ueber 150 Wasser wechseln)",
                  "hinweis": "Futter je m2 aus FAO 589 (Blatt 40-50), SRAC 454 NFT nur 25 % des Raft-Werts; Beete unter den Tischen nur Blatt/Kraeuter (D61, R36): Tomate, Paprika, Gurke und Suesskartoffel entfallen; Kohlrabi/Sellerie nur als Zwischenkultur"},
    "puffer_klein": puffer_klein,
    "beete_tische": beete_tische,
    "szenario": {"aussen_rinnen": AUSSEN_RINNEN, "drei_rinnen": scen3, "vier_rinnen": scen4,
                 "hinweis": "aussen4 ist Standard (D43, W24 check_nft_fit 48/48): Rinnenlaengen und Toepfe aus nft_tisch.json; NFT-Flaeche aus Bens Tabellenflaeche (42,41 m2 bei aussen3-Laenge) auf die Rinnenlaenge skaliert [A]",
                 "frucht_blatt_g_m2": [FRUIT_G, LEAF_G], "bens_mix_frucht_anteil": FRUIT_SHARE_MIX},
    "offene_fragen": ["Standort und Aussenklima (Heizlast, Jahresenergie)", "4. Aussenrinne machbar (W24)?", "Fruchtgemuese: ausserhalb der Tische gaebe es keinen Platz (D61 Weg 1); Weg 2b (Mitteltische weg) nur auf Bens Wunsch (R36)",
                      "Drittbecken: Maß 1,03 x 1,13 m bestätigen (D46); Puffer-Station Lage und Stapelhöhe", "Notstrom und Alarm fuer die Belueftung", "Geblaese und Windlast der Plane"],
    "konsistenz": [{"pruefung": n, "ok": bool(ok), "detail": d} for n, ok, d in checks],
    "herkunft": {
        "biomasse_346_kg": "Entscheidung D61 (Weg 1, R36): Pflanzflaeche Mitte der FAO-Werte, Spanne 308-385; frueher D40 475 kg (setzte Fruchtgemuese voraus); Obergrenze Q FAO 589 (20 kg/m3 = 570 kg)",
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
