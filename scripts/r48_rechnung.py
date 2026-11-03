"""R48: Filterreihenfolge und Hoehenprofil (Vortex, Feinfilter, Pumpe/Sumpf, Biofilter).

Nur rechnen, liest nichts. Aufruf: python -X utf8 scripts/r48_rechnung.py
Z in mm relativ zum Innenboden (Skript-Z minus 400). Herkunft: [Q] Netzliste/Bauteilblatt, [E] Rechnung, [A] Annahme.
Abschnittsnummern: docs/research/R48-filterreihenfolge.md.
"""
import math

RHO, G = 1000.0, 9.81
Q_PUMPE = 55 / 60000.0   # m3/s je Hauptpumpe [Q Netzliste]
Q_LINIE = 110 / 60000.0  # m3/s Hauptstrom je Linie [Q K10]
Q_TEIL = 12.5 / 60000.0  # m3/s Bodenablauf-Teilstrom je Linie [Q K03]

# [Q] Bauteilblatt tank.md, Variante klein (Vortex)
V_RAND_ZU_SPITZE = 1075   # Tankhoehe inkl. Kegel
V_ZULAUF_UNTER_RAND = 250
V_AUSLASS_UNTER_RAND = 100
V_HAHN_UNTER_SPITZE = 92  # Spitze 172, Stutzenende 80
V_PLATTFORM_ueber_SPITZE = 256  # Plattform 428, Spitze 172
V_D_INNEN = 0.623         # Koerperdurchmesser
V_INHALT_RAND_L = 254     # Wasser bis Rand
V_GEWICHT_GEFUELLT_KG = 300

# [Q] Biofilter: Spiegel 1600 laut K10 ("Tankspiegel ca. Z 1600"), Zulauf 1420, Ueberlauf-Rohr 1570, Deckel 1676
BIO_SPIEGEL = 1600
SAUG = 320            # Spiegel am Heber-Ende / Filter-Einlauf [Q K01, S2R]
POOL = 515
H_HEUTE = 2.0         # m [Q Netzliste K08/K09]
STATIK_HEUTE = (BIO_SPIEGEL - SAUG) / 1000.0
REST = H_HEUTE - STATIK_HEUTE   # Reibung + Reserve, hier unveraendert uebernommen [A]


def p_el(h, eta):
    return RHO * G * Q_PUMPE * h / eta


print('== 1. Vortex im Teilstrom (heute) gegen Vollstrom')
a = math.pi / 4 * V_D_INNEN ** 2
for name, q in (('Teilstrom 12,5 l/min', Q_TEIL), ('Vollstrom 110 l/min', Q_LINIE)):
    sor = q / a
    print(f'{name}: Flaeche {a:.3f} m2, Oberflaechenbeschickung {sor*1000:.2f} mm/s = {sor*3600:.1f} m/h; '
          f'Verweilzeit {V_INHALT_RAND_L / (q * 60000):.1f} min (254 l bis Rand)')
d50_i = 50 - 2 * 2.4  # PVC-U d50 SDR 21 [A Wand 2,4]
for name, q in (('Teilstrom', Q_TEIL), ('Vollstrom', Q_LINIE)):
    v = q / (math.pi / 4 * (d50_i / 1000) ** 2)
    print(f'Eintritt d50 (Di {d50_i:.1f} mm) {name}: {v:.2f} m/s')
print(f'Vergleich Davidson/Summerfelt-Versuch: 0,0031 m/s = 3,1 mm/s; Vollstrom heute = {Q_LINIE/a/0.0031:.1f}-fach')

print('\n== 2. Hoehenprofil Vortex je Variante (Z mm)')


def vortex(spiegel):
    rand = spiegel + V_AUSLASS_UNTER_RAND
    spitze = rand - V_RAND_ZU_SPITZE
    return dict(spiegel=spiegel, rand=rand, zulauf=rand - V_ZULAUF_UNTER_RAND, spitze=spitze,
                hahn=spitze - V_HAHN_UNTER_SPITZE, plattform=spitze + V_PLATTFORM_ueber_SPITZE)


VAR = {
    # Spiegel Vortex, Pumpen-Saugspiegel, Zusatz-Rohrweg-Reserve m
    'V0 heute (Teilstrom-Absetzer)': dict(vortex=1147, saug=SAUG, ziel=BIO_SPIEGEL, extra=0.0),
    'V1 Vortex hoch, Pumpe im Sumpf': dict(vortex=BIO_SPIEGEL + 100, saug=SAUG, ziel=BIO_SPIEGEL + 100, extra=0.10),
    'V3 Kaskade (= V1b): Vortex hoch -> Feinfilter hoch -> Biofilter': dict(vortex=1900, saug=SAUG, ziel=1900, extra=0.10),
    'V2 Vortex tief (Grube) im Hauptstrom': dict(vortex=300, saug=200, ziel=BIO_SPIEGEL, extra=0.0),
    'V4 Sieb im Sumpf, Pumpe im Sumpf': dict(vortex=1147, saug=SAUG, ziel=BIO_SPIEGEL, extra=0.0),
}
for n, v in VAR.items():
    vt = vortex(v['vortex'])
    h = (v['ziel'] - v['saug']) / 1000.0 + REST + v['extra']
    p25, p18 = 4 * p_el(h, 0.25), 4 * p_el(h, 0.18)
    print(f'{n}\n  Vortex: Spiegel {vt["spiegel"]}, Rand {vt["rand"]}, Zulauf {vt["zulauf"]}, Spitze {vt["spitze"]}, '
          f'Hahn {vt["hahn"]}, Plattform {vt["plattform"]}')
    print(f'  Hauptpumpe: statisch {(v["ziel"]-v["saug"])/1000:.2f} m, Rest {REST+v["extra"]:.2f} m -> H {h:.2f} m; '
          f'4 Pumpen {p25:.0f} W (eta 25 %) / {p18:.0f} W (eta 18 %); gegen V0 {p25-4*p_el(H_HEUTE,0.25):+.0f} / '
          f'{p18-4*p_el(H_HEUTE,0.18):+.0f} W')
    # Gegenprobe Premium 6000 (Parabel-Naeherung R47c): H bei 3300 l/h
    h_par = 5.0 * (1 - (3300 / 6000) ** 2)
    print(f'  Premium-6000-Naeherung liefert {h_par:.2f} m bei 55 l/min -> {"reicht" if h_par>=h else "reicht NICHT"}')

print('\n== 3. Kleine Pumpen (Bodenablauf-Teilstrom)')
print(f'Heute: 17 W x 2 in Betrieb = 34 W [Q R47]; Hub Pool {POOL} -> Vortex-Zulauf 997 = {(997-POOL)/1000:.2f} m')
for sp in (400, 455):
    vt = vortex(sp)
    print(f'Bodenablauf (Poolboden -1685) per Schwerkraft nur wenn Vortex-Spiegel < Pool {POOL}: bei Spiegel {sp} '
          f'Druckhoehe am Ablauf {POOL-sp} mm, Rand {vt["rand"]}, Spitze {vt["spitze"]}, Hahn {vt["hahn"]}')
print('Fenster fuer Schwerkraft-Teilstrom UND Schwerkraft zum Filter-Einlauf 320: Spiegel ca. 340 bis 455 (Rest: Rohr-/Ventilverlust 60 mm [A])')

print('\n== 4. Gestell Vortex hoch: Knicken und Kippen (Ueberschlag)')
E = 210000.0   # N/mm2 Stahl
for name, spiegel in (('V1', 1700), ('V3', 1900)):
    vt = vortex(spiegel)
    L = vt['plattform']
    i_ = (30 ** 4 - 26 ** 4) / 12.0   # 30x30x2 [A, Wand 2 mm; Bauteilblatt nennt 30 mm Querschnitt]
    last_n = (V_GEWICHT_GEFUELLT_KG + 40) / 4.0 * G
    for k, kn in ((1.0, 'gelenkig'), (2.0, 'Kragarm')):
        pcr = math.pi ** 2 * E * i_ / (k * L) ** 2
        print(f'{name} Beinlaenge {L} mm ({kn}): Knicklast {pcr/1000:.1f} kN je Bein, Last {last_n/1000:.2f} kN -> Faktor {pcr/last_n:.0f}')
    cog = vt['plattform'] + 270   # Schwerpunkt gefuellt ca. 270 mm ueber Plattform [E]
    half = 294.0                   # Fusspunkt +-294 mm [Q tank.md]
    print(f'{name} Schwerpunkt Z {cog}, Kippen ab {half/cog:.2f} g Seitenlast (Biofilter heute: Z ~1700, 0,23 g [Q R47c])')

print('\n== 5. Schlammfass (Spannringfass 0,95 m, K07)')
for name, spiegel in (('V0', 1147), ('V1', 1700), ('V3', 1900), ('V2', 300)):
    vt = vortex(spiegel) if name != 'V0' else dict(hahn=80, spitze=172)
    fass_oben_max = vt['hahn'] - 100 - 50   # Fallrohr/Bogen 100 mm + 50 mm Luft [A]
    boden = fass_oben_max - 950
    print(f'{name}: Hahn {vt["hahn"]} -> Fass-Oberkante hoechstens {fass_oben_max}, Fass-Boden {boden}; '
          f'Grube noetig: {max(0, -boden)} mm unter Boden')

print('\n== 6. Mehrmasse Vortex hoch auf Techniktafel')
print('Biofilter gefuellt ca. 857 kg auf Plattform Z 570 [Q tank.md]; Vortex gefuellt ca. 300 kg [Q tank.md]; Feinfilter gefuellt ca. 175 kg [Q feinfilter.md]')
print(f'V3: oben zusaetzlich Vortex 300 + Feinfilter 175 = {300+175} kg neben dem Biofilter (857 kg) = {(300+175)/857*100:.0f} % mehr Last in der Hoehe')

print('\n== 7. Vergrabene Rohrmeter, die V4 entfallen lassen wuerde (R47b-Tabelle 6.1)')
stamm = 3.4 + 2.1 + 0.7 + 0.9
print(f'K06/K22 (3,4 + 2,1) + K02/K18 (0,7 + 0,9) = {stamm:.1f} m von 30,3 m = {stamm/30.3*100:.0f} %')
