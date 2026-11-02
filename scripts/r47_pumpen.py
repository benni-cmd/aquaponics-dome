"""R47c: Pumpenfrage (Foerderhoehe 2,0 / 2,83 / 3,2 m bei 55 l/min) und Varianten-Leistung.

Nur rechnen, liest nichts. Aufruf: python -X utf8 scripts/r47_pumpen.py
Herkunft: [Q] Datenblatt, [E] Rechnung, [A] Annahme (siehe docs/research/R47-wasserkreislauf-neu.md Abschnitt 7).
"""
RHO, G = 1000.0, 9.81
Q = 55 / 60000.0  # m3/s je Pumpe

# [Q] Oase Aquarius Universal Premium 6000 (Datenblatt 02.08.2017): 110 W, 6000 l/h max, 5,0 m max
# [Q] Oase Aquamax Eco Classic 5500 / Pontec PondoMax Eco 5000: 60 W, 5300 bzw. 5000 l/h, 2,8 bzw. 2,6 m max (Haendlerangaben)
# [A] Kennlinie als Parabel H = H0 * (1 - (Q/Qmax)^2), Qmax = Datenblatt "max l/h" bei H = 0
PUMPEN = {'Aquarius Premium 6000': (5.0, 6000, 110), 'Aquamax Eco Classic 5500': (2.8, 5300, 60),
          'PondoMax Eco 5000': (2.6, 5000, 60)}


def h_bei(h0, qmax, q_lh):
    return h0 * (1 - (q_lh / qmax) ** 2)


print('== 1. Kennlinie (Parabel-Naeherung) bei 55 l/min = 3300 l/h')
for n, (h0, qm, p) in PUMPEN.items():
    print(f'{n}: H bei 3300 l/h = {h_bei(h0, qm, 3300):.2f} m (Nennleistung {p} W)')
# Gegenprobe gegen R45: Sumpfpumpe 5300 l/h / 2,8 m / 60 W, Arbeitspunkt 61 l/min bei 1,47 m
print(f'Gegenprobe R45: Eco Classic 5500 bei 3660 l/h: {h_bei(2.8, 5300, 3660):.2f} m (R45: 1,47 m)')

print('\n== 2. Hydraulische und elektrische Leistung je Pumpe')
for h in (2.0, 2.83, 3.2):
    ph = RHO * G * Q * h
    print(f'H {h:.2f} m: hydraulisch {ph:.1f} W; elektrisch bei Gesamt-Wirkungsgrad 18 % / 25 % / 30 %: '
          + ' / '.join(f'{ph / e:.0f}' for e in (0.18, 0.25, 0.30)) + ' W')
# Wirkungsgrad der Teichpumpen am besten Punkt (halber Qmax, H = 0,75 H0 der Parabel)
for n, (h0, qm, p) in PUMPEN.items():
    q_ = qm / 2 / 3.6e6
    h_ = h_bei(h0, qm, qm / 2)
    print(f'{n}: hydraulisch am Punkt Qmax/2 = {RHO*G*q_*h_:.1f} W gegen {p} W Nenn -> eta ca. {RHO*G*q_*h_/p*100:.0f} %')

print('\n== 3. Mehrleistung Ring gegen heute (4 Hauptpumpen), kWh/Tag')
for eta in (0.18, 0.25):
    for h in (2.83, 3.2):
        d = 4 * RHO * G * Q * (h - 2.0) / eta
        print(f'eta {eta:.0%}, H {h:.2f}: +{d:.0f} W = +{d*24/1000:.1f} kWh/Tag')

print('\n== 4. B2 / B3: Booster nach dem Biofilter, GANZER Linienstrom 110 l/min (EINHEIT)')
qb = 110 / 60000.0
for hb in (0.725 + 0.3, 0.725 + 0.3 + 0.35):   # B2: 0,725 Hub + 0,3 Reibung; B3: + Fuellstandsreserve Hochbehaelter [A]
    ph = RHO * G * qb * hb
    print(f'Booster H {hb:.2f} m: hydraulisch {ph:.1f} W je Linie; el. bei 18 %/25 %: {ph/0.18:.0f}/{ph/0.25:.0f} W; beide Linien: {2*ph/0.18:.0f}/{2*ph/0.25:.0f} W')

print('\n== 5. B1: Hoehen (relativ, mm)')
UE, ZU = 1570, 1420
RING_HOCH = 2245
print(f'Ueberlauf-Mindesthoehe {RING_HOCH+50}: Anhebung {RING_HOCH+50-UE} mm; Zulauf neu {ZU+RING_HOCH+50-UE}; Deckel neu {1676+RING_HOCH+50-UE}; Plattform neu {570+RING_HOCH+50-UE}; Beinlaenge neu {1008+RING_HOCH+50-UE}')
