"""R49: einfachstes natuerliches System -- Hoehen, Konzepte, Beet-Rueckfuehrung, Luftheber, Vergrabungs-Audit.
Nur lesen und rechnen (liest data/leitungsnetz.json und data/leitungstrassen.json, aendert nichts).
Z in mm relativ zum Innenboden (Skript-Z minus 400), wie R47/R48.
Aufruf: python -X utf8 scripts/r49_rechnung.py
Herkunft: [Q] Datei/Quelle, [E] Rechnung hier, [A] Annahme.
"""
import json, math, re
from collections import defaultdict

RHO, G, P0 = 1000.0, 9.81, 101325.0
netz = {k['id']: k for k in json.load(open('data/leitungsnetz.json', encoding='utf-8'))['kanten']}
trassen = json.load(open('data/leitungstrassen.json', encoding='utf-8'))['trassen']


def pump_w(q_lmin, h_m, eta):
    return RHO * G * (q_lmin / 60000) * h_m / eta


def hdr(t):
    print('\n' + '=' * 8, t)


# ---------------------------------------------------------------- 1. Hoehen
hdr('1. Hoehen (Z rel., mm) [Q Netzliste K01/K10/K12, R47, R48]')
POOL, HEBER_ENDE, BIO_UEBERLAUF, BIO_SPIEGEL = 515, 320, 1570, 1600
NFT_RINNE, NFT_ZULAUF, BEET_TROPF, BEET_ABLAUF = 1000, 1090, 650, -100
HALBRING_TIEF, HALBRING_HOCH = 660, 720
RING_UK, RING_ACHSE, RING_HOCH = 2100, 2145, 2245
print(f'Biofilter-Spiegel {BIO_SPIEGEL}; Druckkopf zur Rinne {BIO_SPIEGEL-NFT_RINNE}, zum Tisch-Zulauf {BIO_SPIEGEL-NFT_ZULAUF}, '
      f'zum Beet-Tropfrohr {BIO_SPIEGEL-BEET_TROPF} mm')
print(f'Beetablauf {BEET_ABLAUF} liegt {POOL-BEET_ABLAUF} mm unter Pool-Spiegel {POOL}, {HALBRING_TIEF-BEET_ABLAUF} mm unter Halbring-Tiefpunkt')
# kleinste Biofilter-Anhebung fuer Ring ueber Gang (Regel: nichts frei im Gang zwischen 0 und 2100)
for name, slope, od in (('R47c (1 %, d90)', 0.01, 90), ('flacher Ring 0,5 %, d90', 0.005, 90), ('0,3 %, d75', 0.003, 75)):
    halbring_l = 10700  # mm, Halbring r 3,4 m [Q R47]
    hoch = RING_UK + od + halbring_l * slope
    ueberlauf = hoch + 50 + 30   # +50 Luft, +30 Reibung Fallleitung [A]
    print(f'Ring {name}: Hochpunkt {hoch:.0f}, Biofilter-Ueberlauf >= {ueberlauf:.0f}, Anhebung gegen 1570: {ueberlauf-BIO_UEBERLAUF:.0f} mm')
# ohne Ring, Ring auf Tischhoehe (I5): Anhebung 0
RING_TISCH = 1000   # Ringachse auf Rinnenhoehe (wie K12 am Tischbein) [A]
print(f'Ring auf Tischhoehe (I5, Achse Z {RING_TISCH}): Kopf ab Ueberlauf {BIO_UEBERLAUF-RING_TISCH} mm >= 500 mm [Q K12] -> Anhebung 0 mm; '
      f'er kreuzt keinen Gang (Regel: frei nur ab Z 2100) und erreicht die Beete (Z 650) nicht ohne Graben')
# Tiefer statt hoeher: Tische / Biofilter
min_sp = NFT_RINNE + 500   # K12 Druckkopf > 500 mm
print(f'Biofilter-Spiegel nach unten: >= Rinne {NFT_RINNE} + 500 = {min_sp} -> hoechstens {BIO_SPIEGEL-min_sp} mm tiefer')
sammler_unten = HALBRING_HOCH + 0.015*3200 + 63 + 0   # Sektorsammler d63 muss ueber Halbring-Hochpunkt muenden [E]
print(f'Tische tiefer: Sektorsammler >= {sammler_unten:.0f} (Z ~900 heute) -> Tische hoechstens {900-sammler_unten:.0f} mm tiefer')

# ---------------------------------------------------------------- 2. Konzepte
hdr('2. Konzepte: Pumpen, Foerderhoehe, Dauerstrom (4 Hauptpumpen a 55 l/min, Absetzer 2 x 17 W, Beet-Sumpf 2 x 54 W)')
REST = 0.72                 # Reibung + 20 % Reserve [Q R48 Abschn. 1]
STAT0 = (BIO_SPIEGEL - HEBER_ENDE) / 1000   # 1,28 m
H0 = STAT0 + REST           # 2,00 m
KLEIN, BEET = 34.0, 108.0   # W [Q R47 Abschn. 3]


def konzept(name, delta_mm, beetpumpen, extra=0.0, rest_plus=0.0, klein=KLEIN):
    h = H0 + delta_mm / 1000 + rest_plus
    p25 = 4 * pump_w(55, h, 0.25)
    p18 = 4 * pump_w(55, h, 0.18)
    b25 = BEET if beetpumpen else 0
    b18 = BEET * 0.25 / 0.18 if beetpumpen else 0
    tot25 = p25 + klein + b25 + extra
    tot18 = p18 + klein * 0.25 / 0.18 + b18 + extra
    print(f'{name:48s} H {h:.2f} m  Haupt {p25:4.0f}/{p18:4.0f} W  gesamt {tot25:4.0f} W ({tot18:4.0f} W bei eta 18 %)  {tot25*24/1000:4.1f} kWh/Tag')
    return h, tot25, tot18


konzept('(a) A+ / A+ mit Subtank V4 (Hoehen unveraendert)', 0, True)
konzept('(b1) B1 Biofilter +725 (R47c)', 725, True)
konzept('(b2) B1-min Biofilter +660 (flacher Ring)', 660, True)
konzept('(b3) I5 Ring auf Tischhoehe (Anhebung 0)', 0, True)
konzept('(b4) Tische/Biofilter 70 mm tiefer', -70, True)
sump_mean = -375    # Tiefsumpf T: Spiegel zwischen -600 (AUS) und -150 (EIN) [A]
dT = HEBER_ENDE - sump_mean
konzept('(c) T Tiefsumpf, Beet-Sumpf entfaellt', dT, False, rest_plus=0.10)
print(f'    (T: mittlerer Sumpfspiegel {sump_mean}, statische Mehrhoehe {dT} mm + 0,10 m laengerer Weg [A]; Beetablauf {BEET_ABLAUF} muss ueber Sumpf-EIN -150 liegen: ok)')
print(f'    Beet-Sumpf heute: Beetwasser wird 2 x gehoben (2,0 m x 110 + 1,47 m x 54,5 l/min = {2.0*110+1.47*54.5:.0f} m*l/min); T hebt 1 x '
      f'({(H0+dT/1000+0.1)*110:.0f} m*l/min)')

# Pool-Durchsatz im Konzept T (je Linie, l/min) [Q Netzliste Bilanz]
hdr('2b. Konzept T: Wasserbilanz je Linie und Pool-Austausch')
nft, byp, mess, beet, absz = 38.0, 14.5, 3.0, 54.5, 12.5
pool_in_heute = nft + byp + beet + mess   # K15 + K13 + K14 + Messkreis (K37)
pool_in_T = nft + byp + mess
print(f'Pool-Zufluss je Linie heute {pool_in_heute:.1f} l/min (ohne Zweitbecken-Teil), in T {pool_in_T:.1f} l/min -> Faktor {pool_in_T/pool_in_heute:.2f}')
vol_pool = 34.0  # m3 Systemwasser [Q Szenarien-Bericht]
for lab, qq in (('heute', pool_in_heute*2), ('T', pool_in_T*2)):
    print(f'  {lab}: {qq:.0f} l/min = {qq*1.44/vol_pool:.1f} Umwaelzungen/Tag des Systemwassers')
tan_prod = 130.0   # g/Tag [Q R47b]
for E in (0.3, 0.5):
    c_h = tan_prod / (pool_in_heute*2*1.44 * E); c_t = tan_prod / (pool_in_T*2*1.44 * E)
    print(f'  TAN-Gleichgewicht im Pool bei Biofilter-Wirkung je Durchgang E={E}: heute {c_h:.2f} mg/l, T {c_t:.2f} mg/l [E, Durchsatzmodell, E ist [A]]')
print(f'  Heber-Strom in T: Pumpen 110 - Beet {beet} - Absetzer {absz} = {110-beet-absz:.0f} l/min (heute 97,5) -> gedrosselt noetig')
head_heber = POOL - sump_mean
print(f'  Heber-Druckhoehe in T bei Sumpf {sump_mean}: {head_heber} mm (heute 195 mm); ohne Drossel wuerde der Sumpf bis ~Pool-Spiegel steigen')

# ---------------------------------------------------------------- 3. Beet-Rueckfuehrung
hdr('3(i). Schwerkraft-Rueckfuehrung der Beete: noetige Ablaufhoehe und Anhebung')
for ziel_name, ziel in (('Halbring-Tiefpunkt 660', HALBRING_TIEF), ('Wanddurchfuehrung 540 (25 mm ueber Spiegel)', POOL + 25)):
    for laenge_m, label in ((3.5, 'Beet direkt zum Pool'), (9.0, 'ueber Sammelring-Segment')):
        slope = 0.01 if laenge_m < 5 else 0.005
        z = ziel + 1000 * laenge_m * slope + 90 + 50   # + d90 + Einzelabgang/Standrohr-Luft [A]
        print(f'  Ziel {ziel_name}, {label} ({laenge_m} m, {slope*100:.1f} %): Ablauf >= {z:.0f}; Beet muss {z-BEET_ABLAUF:.0f} mm hoeher (Ablauf {BEET_ABLAUF}) '
              f'bzw. {z-(-192):.0f} mm (Port -192 aus Bauteilblatt)')
heb = 900
rim_neu = 475 + heb
print(f'  mit Anhebung {heb}: Beetrand {rim_neu}, Medium-Oberflaeche {400+heb}')
R_DOM = 6000.0   # Kuppel Scheitel 5986, Basis -14 -> R ~ 6,0 m [Q layout.md] ; Kugel angenommen [A]
for r_in, r_out in ((5188, 5188+470+60), (3344, 3344+470)):
    hdom = math.sqrt(max(R_DOM**2 - r_out**2, 0))
    print(f'  Beet bei r {r_in}: Dom-Innenhoehe am Aussenrand r {r_out}: {hdom:.0f}; Platz ueber Beetrand (Anhebung {heb}): {hdom-rim_neu:.0f} mm; heute: {hdom-475:.0f} mm')
gew = 8 * 1311 + 6 * 1065
print(f'  Gewicht aller Beete (8 aussen_800 ~1311 kg [A, 0,8 x aussen_933 Wasser], 6 innen 1065 [Q]) = {gew/1000:.1f} t auf Gestellen {heb} mm hoch')

hdr('3(iii). Luftheber (Mammutpumpe): Luftbedarf fuer Beet-Rueckfuehrung (je Linie, 61 l/min) und fuer Absetzer-Teilstrom (12,5 l/min)')


def airlift(label, q_lmin, lift_m, sub_m):
    pw = RHO * G * (q_lmin/60000) * lift_m
    s = sub_m / (sub_m + lift_m)
    e_iso = P0 * math.log(1 + RHO*G*sub_m/P0)      # J je m3 Luft isotherm
    print(f'  {label}: Hub {lift_m:.2f} m, Eintauchtiefe {sub_m:.2f} m -> Eintauchverhaeltnis {s*100:.0f} % (Leitfaden: > 80 %, Hub <= 0,305 m); Wasserleistung {pw:.1f} W')
    for eta in (0.45, 0.25, 0.10):
        qa = pw / eta / e_iso * 60000
        print(f'     Wirkungsgrad {eta*100:.0f} %: Luft {qa:6.0f} l/min  = {qa/q_lmin:4.1f} : 1 Luft:Wasser; el. bei 0,5..1,0 W je l/min: {qa*0.5:.0f}..{qa*1.0:.0f} W')


airlift('Beet-Sumpf Linie, Sumpf 1,0 m tief', 61, 1.0, 0.8)
airlift('Beet-Sumpf Linie, Hub 0,8 m (Sumpf-Spiegel -140 bis 660)', 61, 0.8, 0.8)
airlift('Beet-Sumpf, damit Eintauchverhaeltnis 80 %', 61, 1.0, 4.0)
airlift('Absetzer-Teilstrom: K03-Steig bis Zulauf 997', 12.5, (997-POOL)/1000, (POOL+2035)/1000)
print('  Luft Gesamtanlage (Mittel/Spitze) 130/205 l/min, el. 100..215 W [Q Netzliste K44, Szenarien-Bericht]')
print(f'  Strahlpumpe/Ejektor aus dem Treibwasser der Beet-Zufuhr: Treibhoehe {BIO_SPIEGEL-HALBRING_TIEF} mm < Hub {HALBRING_TIEF-(-300)} mm -> Foerderverhaeltnis ~ 0 [E]')

# ---------------------------------------------------------------- 4. Vergrabungs-Audit
hdr('4. Vergrabungs-Audit (Segment-Mitte Z abs < 400) aus data/leitungstrassen.json')
GRUPPEN = [('Heber (K01/K17)', r'K01|K17'), ('Filter-Stamm (K06/K22 + T-Stuecke)', r'K06|K22'), ('Zweigstuecke 2. Pumpe (K02/K18)', r'K02|K18'),
           ('Notbypass (K56/K57)', r'K56|K57'), ('Bodenablauf-Kreis (K03/K19 inkl. Tief/Steig/Stumpf)', r'K03|K19'),
           ('Absetzer-Auslauf (K05/K21)', r'K05|K21')]
tot = 0.0
summen = {}
for name, pat in GRUPPEN:
    u = 0.0
    for t in trassen:
        if re.match(pat, t['id']):
            p = t['pfad']
            for a, b in zip(p, p[1:]):
                if (a[2] + b[2]) / 2 < 400:
                    u += math.dist(a, b) / 1000
    summen[name] = u
    tot += u
    print(f'  {name:55s} {u:5.1f} m')
print(f'  Summe {tot:.1f} m')
b = summen
heber, stamm, zweig, bypass, boden, absz_aus = (b[g[0]] for g in GRUPPEN)
print(f'  V4 (Stamm, Zweigstuecke, Bypass entfallen):                  {tot-stamm-zweig-bypass:.1f} m')
print(f'  V4 und K05/K21 direkt in den Subtank (oberirdisch):          {tot-stamm-zweig-bypass-absz_aus:.1f} m')
print(f'  zusaetzlich Absetzerkreis ganz weg (R44 Kandidat A):         {heber:.1f} m')
print('  Kuenftige Graeben [Q R47 Abschn. 2, E +-25 %]: K14 Beet-Ablaeufe 58,9 m, K58/K59 8 m, K11 Gangkreuzungen ~8 x 1,5 = 12 m [A]')
print(f'  -> mit allen kuenftigen Graeben A+: {tot+58.9+8+12:.0f} m; V4 + K05 direkt + K14 im Bodenkanal: unterflur-erdvergraben {tot-stamm-zweig-bypass-absz_aus+12:.0f} m, Rest im Kanal/Rost')
for t in trassen:
    if t['id'] in ('K01', 'K03-Steig', 'K05'):
        zs = [q[2] - 400 for q in t['pfad']]
        print(f"  {t['id']}: Z rel {min(zs):.0f}..{max(zs):.0f}")
print(f'  Bodenablauf-Stutzen real Z rel {-1575-400} (abs -1575) statt -1685 in Netzliste/R48: Druckhoehe zum Pool-Spiegel {POOL+1975} mm')

# ---------------------------------------------------------------- 5. Inventar je Konzept (Teilearten, Pumpen, Einzelpfade) [A, Zaehlung hier]
hdr('5. Inventar je Konzept (gesamte Anlage, 2 Linien) [A: Zaehlung nach Netzliste/R47b/R48]')
basis = {'Pool', 'Heber', 'Biofilter', 'Verteiler', 'Beet+Siphon', 'NFT-Tisch', 'Hauptpumpe', 'Rueckl.-Halbring'}
absetzer = {'Absetzer', 'Kleinpumpe', 'Schlammfass'}
A_PLUS = basis | absetzer | {'Feinfilterbox', 'Beet-Sumpf+Pumpe', 'Notbypass'}
V4 = (basis | absetzer | {'Subtank+Siebkorb', 'Beet-Sumpf+Pumpe'})
V4K = V4                                      # K05 direkt: kein neues Teil
T = basis | absetzer | {'Subtank+Siebkorb', 'Heber-Schwimmerventil'}
B1 = A_PLUS | {'Ring', 'Stuetzen', 'Biofilter-Gestell hoch'}
inv = [
    # name, teilearten, pumpen laufend, pumpstufen Beetwasser, Einzelpfade (R47b-Zaehlung + Beet-Kette)
    ('A+ heute', A_PLUS, 8, 2, 10 + 2),
    ('(a) A+ mit Subtank V4 (+K05 direkt)', V4, 8, 2, 4 + 2),
    ('(b1) B1 Biofilter hoch + Ring', B1, 8, 2, 10 + 2),
    ('(c) T Tiefsumpf', T, 6, 1, 4),
]
for n, ta, pl, st, ep in inv:
    print(f'  {n:40s} Teilearten {len(ta):2d}  Pumpen laufend {pl}  Pumpstufen Beetwasser {st}  Einzelpfade {ep}')
