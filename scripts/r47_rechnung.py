"""R47: Rechnung Wasserkreislauf neu (Lasten, Ringkapazitaet, Pumpenleistung, Rohrmeter).

Nur lesen und rechnen: liest data/leitungsnetz.json, aendert nichts.
Aufruf: python -X utf8 scripts/r47_rechnung.py
Herkunft: [E] Rechnung, [A] Annahme, [Q] Quelle (siehe docs/research/R47-wasserkreislauf-neu.md).
"""
import json
import math

RHO, G = 1000.0, 9.81
netz = json.load(open('data/leitungsnetz.json', encoding='utf-8'))
kant = {k['id']: k for k in netz['kanten']}

# ---------- 1. Rohre: PVC-U PN10 SDR21 (EN 1452), Wand = d/21 gerundet [Q Engineering Toolbox, R45]
WAND = {32: 1.6, 40: 1.9, 50: 2.4, 63: 3.0, 75: 3.6, 90: 4.3, 110: 5.3}
SPAN_GF = {63: 1.8, 75: 2.0, 90: 2.2, 110: 2.4}      # [Q] Georg Fischer PVC-U Planning Fundamentals, <= 20 C
SPAN_UK = {63: 1.5, 75: 1.65, 90: 1.8, 110: 2.0}     # [Q] plasticpipeshop.co.uk Pipe Clip Spacing, 20 C
E_KURZ, E_LANG = 3000e6, 1000e6                      # [A] E-Modul PVC-U kurz / Dauerlast (Kriechen)


def rohr(d):
    t = WAND[d]
    di = d - 2 * t
    a_i = math.pi / 4 * di ** 2 * 1e-6              # m2
    a_w = math.pi / 4 * (d ** 2 - di ** 2) * 1e-6
    i_m = math.pi / 64 * (d ** 4 - di ** 4) * 1e-12  # m4
    return di, a_i, a_w, i_m


print('== 1. Last und Stuetzabstand (volles Rohr, Wasser 1000 kg/m3, PVC 1400 kg/m3)')
print('d   Di mm  kg/m  N/m   Span(min GF/UK) m  Durchhang mm bei Span_min: kurz / lang')
for d in (63, 75, 90, 110):
    di, ai, aw, im = rohr(d)
    kgm = ai * 1000 + aw * 1400
    w = kgm * G
    L = min(SPAN_GF[d], SPAN_UK[d])
    f = lambda e: 5 * w * L ** 4 / (384 * e * im) * 1000
    print(f'{d:3d} {di:5.1f} {kgm:5.2f} {w:5.1f}  {SPAN_GF[d]}/{SPAN_UK[d]} -> {L}   {f(E_KURZ):5.1f} / {f(E_LANG):5.1f}')

# ---------- 2. Ringkapazitaet (Manning, Vollrohr) und Druckring
print('\n== 2. Schwerkraftring: Vollrohr-Kapazitaet nach Manning (n 0,010 PVC [A]) in l/min; halbvoll = Haelfte')
for d in (63, 75, 90, 110):
    di, ai, _, _ = rohr(d)
    r_h = di / 4000
    row = []
    for s in (0.005, 0.01):
        q = 1 / 0.010 * ai * r_h ** (2 / 3) * math.sqrt(s) * 60000
        row.append(f's={s*100:.1f}%: {q:6.0f}')
    print(f'd{d}:', '  '.join(row))
print('Druckring: Geschwindigkeit bei Q (l/min) und d (<= 1,5 m/s Netzkonvention)')
for q in (110, 220):
    for d in (50, 63, 75, 90):
        di, ai, _, _ = rohr(d)
        print(f'  Q {q}: d{d} v = {q/60000/ai:4.2f} m/s', end='')
    print()

# ---------- 3. Hoehenbilanz und Pumpenleistung (relative Z, mm)
print('\n== 3. Hoehenbilanz und Pumpenleistung')
POOL, HEBER, BIO_IN, BIO_UE, RINNE = 515, 195, 1420, 1570, 1000
RING_UNTERK = 2100                      # Gang frei >= 2100: Rohr-Unterkante
RING_ACHSE = RING_UNTERK + 90 // 2      # d90
RING_HOCH = RING_ACHSE + 100            # Hochpunkt mit Gefaelle 1 % ueber halben Ring (ca. 107 mm) -> aufgerundet
spiegel_saug = POOL - HEBER             # schlechtester Saugspiegel am Feinfilter-Auslauf [E, R45 Heber]
stat_A = (BIO_IN - spiegel_saug) / 1000
H_A = 2.0                               # Netzliste K08 / D38: Foerderhoehe ca. 2,0 m
rest = H_A - stat_A                     # Reibung + 20 % Reserve [E]
stat_B = (RING_HOCH - spiegel_saug) / 1000
H_B = stat_B + rest
eta = 0.25                              # Netzliste: Wirkungsgrad 25 %
q_pumpe = 55 / 60000


def p_el(q, h, e=eta):
    return RHO * G * q * h / e


print(f'Saugspiegel (Pool minus Heberverlust): Z {spiegel_saug}; Biofilter-Zulauf Z {BIO_IN}, Ueberlauf Z {BIO_UE}; Rinne Z {RINNE}')
print(f'Netz-Skript-Z Ueberlauf 1970 = relativ {1970-400}  (Skript-Z minus 400)')
print(f'A: statisch {stat_A:.2f} m, Rest {rest:.2f} m, H {H_A:.2f} m -> je Pumpe {p_el(q_pumpe,H_A):.0f} W (Netz: 72 W)')
print(f'Ring: Unterkante {RING_UNTERK}, Achse {RING_ACHSE}, Hochpunkt {RING_HOCH}; Ueberlauf liegt {RING_UNTERK-BIO_UE} mm UNTER der Ring-Unterkante')
print(f'B/C-Hauptstufe: statisch {stat_B:.2f} m, H {H_B:.2f} m -> je Pumpe {p_el(q_pumpe,H_B):.0f} W')
print(f'Biofilter-Anhebung fuer Schwerkraftspeisung: Ueberlauf muss >= Z {RING_HOCH+50} -> +{RING_HOCH+50-BIO_UE} mm gegen heute')

# Beet-Sumpf: Teichpumpe 60 W (R45), Laufanteil 90 %
sumpf_w = 60 * 0.9
# Booster (Variante C): Ueberlauf 1570 -> Ring-Hochpunkt, nur Beetstrom 54,5 l/min je Linie
h_boost = (RING_HOCH + 50 - BIO_UE) / 1000 + 0.3
boost = p_el(54.5 / 60000, h_boost)
klein = 17 * 2                          # kleine Pumpen: zwei in Betrieb [Netz kabel]
mess = 2.9
A_haupt = 4 * p_el(q_pumpe, H_A)
B_haupt = 4 * p_el(q_pumpe, H_B)
print(f'\nSumme elektrisch (W), Mittel: ')
# A-heute: Hauptpumpen + Absetzer klein + 2 Sumpfpumpen
A_heute = A_haupt + klein + 2 * sumpf_w
# Idee 'Beet-Sumpf als Saugsumpf der Hauptpumpen' verworfen: Hauptpumpen saugen auf Z 120 (geflutet vom Pool),
# der eingegrabene Sumpf steht tiefer (Pegel unter Z 0) -> Saughoehe, keine Selbstansaugung belegt.
sp_sumpf = None
B_ges = B_haupt + klein + 2 * sumpf_w
C_ges = A_haupt + 2 * boost + klein + 2 * sumpf_w
print(f'A heute (Netz v3):        {A_heute:5.0f} W  (Haupt {A_haupt:.0f} + klein {klein} + Sumpf {2*sumpf_w:.0f})')
print(f'B Ring:                   {B_ges:5.0f} W  (Haupt {B_haupt:.0f} + klein {klein} + Sumpf {2*sumpf_w:.0f})')
print(f'C Hybrid (Booster Beete): {C_ges:5.0f} W  (Booster je Linie {boost:.0f} W bei H {h_boost:.2f} m)')
print('kWh/Tag:', {k: round(v * 24 / 1000, 2) for k, v in dict(A=A_heute, B=B_ges, C=C_ges).items()})

# ---------- 4. Geometrie: Rohrmeter Zulauf-Verteilung (Polarkoordinaten, Konzept)
print('\n== 4. Rohrmeter Verteilung (Konzept, +-25 %, Routing-Faktor 1,25 [A])')


def xy(r, az):
    return r * math.cos(math.radians(az)), r * math.sin(math.radians(az))


def dist(p, q):
    return math.hypot(p[0] - q[0], p[1] - q[1])


R_MITTE, R_POOL_KRONE = 3400, 2000
sektoren = {1: [-35.7, 0.3, 36.3, 72.3, 108.3], 2: [144.3, -179.7, -143.7, -107.7, -71.7]}
tech = {1: -8.0, 2: -100.0}      # Technikgruppe je Linie: Linie 2 aus loop-state (K26 bei az -92, Pumpe 4 bei -101); Linie 1 gespiegelt an der Tuerachse -54 [A]
FAK = 1.25
res = {}
for L in (1, 2):
    t = xy(R_MITTE, tech[L])
    az = sektoren[L]
    aussen = [xy(5200, a) for a in az[:4]]        # 4 Aussenbeete (r ca. 5200) je Linie [layout.md]
    innen = [xy(3340, a) for a in az[1:4]]        # 3 Innenbeete (r ca. 3340)
    beete = aussen + innen
    k11 = sum(dist(t, b) for b in beete) * FAK
    bogen = math.radians(abs(az[-1] - az[0])) * R_MITTE
    k12 = bogen * 1.0                                # Strang durch die 5 Sektoren, d32
    k14 = sum(dist(t, b) for b in beete) * FAK       # Beetablaeufe zum Sumpf an der Technikgruppe, d50
    k15 = 5 * 3.2e3                                  # 5 Sektorsammler d63, radial ca. 3,2 m [A]
    k16 = math.pi * R_POOL_KRONE                     # Halbring d110 auf der Wandkrone
    cen = (sum(b[0] for b in beete) / 7, sum(b[1] for b in beete) / 7)
    k14c = sum(dist(cen, b) for b in beete) * FAK
    res.setdefault('k14c', {})[L] = k14c / 1e3
    res[L] = dict(K11=k11 / 1e3, K12=k12 / 1e3, K14=k14 / 1e3, K15=k15 / 1e3, K16=k16 / 1e3)
    print(f'Linie {L}: ' + ', '.join(f'{k} {v:5.1f} m' for k, v in res[L].items()))
k14c = res.pop('k14c')
tot = {k: sum(res[L][k] for L in res) for k in res[1]}
supply_A = tot['K11'] + tot['K12']
ret = tot['K14'] + tot['K15'] + tot['K16'] + 2 * 4
print('K14 mit Sumpf im Schwerpunkt der Beete (statt an der Technikgruppe):', {L: round(v,1) for L,v in k14c.items()})
print(f'Summe beide Linien: ' + ', '.join(f'{k} {v:.1f}' for k, v in tot.items()))
print(f'Zulauf-Verteilung A (K11+K12): {supply_A:.1f} m;  Ruecklauf-Seite (K14+K15+K16+K58/59 je 4 m): {ret:.1f} m')

# Variante B: ein Ring r=3400 plus Steigleitungen und Abgaenge
ring = 2 * math.pi * R_MITTE / 1e3
anz_beete, anz_tische = 14, 24
drop_beet = (RING_ACHSE - 650) / 1e3          # Ring-Achse bis Tropfrohr Z ~650 (Bauteil Zulauf 612-624 + Randhoehe)
drop_tisch = (RING_ACHSE - 1090) / 1e3        # bis Tischzulauf Z ~1090
dr_beet = (4 * abs(5200 - R_MITTE) + 3 * abs(3340 - R_MITTE)) / 7 / 1e3    # mittlere radiale Strecke je Beet
dr_tisch = (abs(2000 - R_MITTE) + abs(3400 - R_MITTE) + abs(5000 - R_MITTE)) / 3 / 1e3
abg_beet = anz_beete * (drop_beet + dr_beet)
abg_tisch = anz_tische * (drop_tisch + dr_tisch)
steig = 2 * (RING_ACHSE - 1570) / 1e3 * 2     # zwei Linien, je Hin- und Zufuhr am Biofilter
supply_B = ring + abg_beet + abg_tisch + steig
print(f'\nB: Ring {ring:.1f} m (d90), Abgaenge Beete {abg_beet:.1f} m, Tische {abg_tisch:.1f} m, Steigleitungen {steig:.1f} m -> {supply_B:.1f} m (gegen A {supply_A:.1f} m)')
# Variante C: zwei Halbringe nur fuer Beete (7 je Linie), NFT-Strang K12 bleibt
ring_c = ring                                  # zwei Halbringe, zusammen ein Umfang
supply_C = ring_c + abg_beet + steig + tot['K12']
print(f'C: Halbringe {ring_c:.1f} m + Abgaenge Beete {abg_beet:.1f} m + NFT-Strang K12 {tot["K12"]:.1f} m + Steig {steig:.1f} m -> {supply_C:.1f} m')

# Teile (Formteile + Armaturen), ohne Rohrstuecke: je Abgang T + 2 Bogen + Kugelhahn + Reduzierung
def teile_abgang(n):
    return n * 5
teile_A = teile_abgang(anz_beete) + teile_abgang(anz_tische) + 2 * 12            # Strang K12: Bogen/Verbinder ca. 12 je Linie [A]
teile_B = teile_abgang(anz_beete) + teile_abgang(anz_tische) + 2 * 6 + math.ceil(ring / 1.8) * 1 + 2 * 3   # Ring: 1 Bogen je Stuetzfeld (1,8 m), Hochpunkt-Entlueftung, Entleerung
teile_C = teile_abgang(anz_beete) + teile_abgang(anz_tische) + 2 * 12 + math.ceil(ring / 1.8) + 2 * 3
print(f'Formteile+Armaturen Zulauf: A {teile_A}, B {teile_B}, C {teile_C}')
stelzen = math.ceil(ring / min(SPAN_GF[90], SPAN_UK[90]))
print(f'Stuetzen Ring (Abstand {min(SPAN_GF[90], SPAN_UK[90])} m): {stelzen} Stueck')
w90 = rohr(90)[1] * 1000 + rohr(90)[2] * 1400
print(f'Ringlast d90 voll: {w90:.1f} kg/m * {ring:.1f} m = {w90*ring:.0f} kg; je Stuetze {w90*min(SPAN_GF[90],SPAN_UK[90]):.0f} kg')

# ---------- 5. Beet: Medienschutz-Loecher und Siebboden gegen Korn
print('\n== 5. Beet-Bauteil')
print('Siebboden 8 mm PP, Loch real D8 (Bauteil: 12 vereinfacht); Medienschutz d110 mit 12 x 12 mm Durchbruechen; Korn Blaehton/Kies 8-20 mm [Quelle R03]')
print('Wasserraum unter Siebboden 640 l (aussen_933); Abflussdauer 234 l: 4,3-6,1 min (R45)')
tropf = (200, 500)
print(f'Zulauf Tropfrohr {tropf[0]}-{tropf[1]} l/h = {tropf[0]/60:.1f}-{tropf[1]/60:.1f} l/min gegen Siphon-Spitze 38-54 l/min -> Faktor {38/(tropf[1]/60):.1f}')
