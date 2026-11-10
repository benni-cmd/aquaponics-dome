"""Stahlrahmen-Podest aus Vierkantrohr 40 x 40 x 3 (U2): 4 Fussplatten, 4 Stuetzen, Fussrahmen und Kopfrahmen aus je 4 Stuecken, 8 Knotenbleche (je Ecke oben und unten, aussen an der X-Seite).
KS: Mitte der Standflaeche in X/Y, Z 0 = Boden; Oberkante Kopfrahmen = Auflage = Hoehe h (Parameter podest_vortex_h bzw. podest_biofilter_h). Die Tankstandflaeche (tank_klein, tank_gross) liegt auf Z = h.
Benutzt von podest_vortex.py und podest_biofilter.py."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U

MAT = {"Stahl verzinkt": (7.85, "#b8bcc2")}
PROFIL = 40           # Vierkantrohr 40 x 40 x 3 (data/katalog.json vierkantrohr_40x40x3)
FUSS, KNOTEN, T = 100, 100, 6


def bauen(name, root, teilenummer, hkey, ueber=None):
    p, d, b = U.start(name, ueber)
    U.material(b, MAT)
    b.add("component.create", name=root, grounded=True)
    h, s = p[hkey], p["span"]
    q = PROFIL
    xs = (-1, 1)
    leg_c = s / 2 - q / 2                                   # Mitte der Stuetzen
    z0 = T                                                  # Stuetzen stehen auf den Fussplatten
    n = 0
    for sx in xs:
        for sy in xs:
            n += 1
            U.box(b, f"Fussplatte_{n}", (FUSS, FUSS, T), (sx * leg_c, sy * leg_c, T / 2), "Stahl verzinkt")
            U.box(b, f"Stuetze_{n}", (q, q, h - z0), (sx * leg_c, sy * leg_c, (h + z0) / 2), "Stahl verzinkt")
    # Rahmen: zwischen den Stuetzen, Laenge s - 2q
    ln = s - 2 * q
    for ring, zc in (("Fussrahmen", z0 + q / 2), ("Kopfrahmen", h - q / 2)):
        i = 0
        for sy in xs:       # entlang X
            i += 1
            U.box(b, f"{ring}_{i}", (ln, q, q), (0, sy * leg_c, zc), "Stahl verzinkt")
        for sx in xs:       # entlang Y
            i += 1
            U.box(b, f"{ring}_{i}", (q, ln, q), (sx * leg_c, 0, zc), "Stahl verzinkt")
    # Knotenbleche aussen an den X-Seiten: oben (Ecke h) und unten (Ecke z0), je Ecke eines
    k = 0
    for zb, zc in (("oben", h - KNOTEN / 2), ("unten", z0 + KNOTEN / 2)):
        for sx in xs:
            for sy in xs:
                k += 1
                U.box(b, f"Knotenblech_{k}", (T, KNOTEN, KNOTEN), (sx * (s / 2 + T / 2), sy * (s / 2 - KNOTEN / 2), zc), "Stahl verzinkt")
    U.fertig(b, root, teilenummer, d, "Stahl verzinkt")
    return b
