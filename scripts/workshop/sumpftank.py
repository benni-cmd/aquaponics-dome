"""Sumpftank T101 (N-UNIFY-AUTOBAHN U2, D93, D105): Grube 1125 x 2975 x 500 innen, Betonwanne + EPDM-Folie, drei begehbare Deckelplatten, Wasserkoerper bis -250,
vier Pufferzonen zu 212 mm (Wand 1 und 3 bodenoffen, Wand 2 und 4 als Wehr), Pumpensockel, drei Zulauftuellen ID25, Schwimmerhalter bei -110, vier Zonenschilder.
KS: Mitte der Grube in X/Y, Z 0 = Fussboden (Deckel-Oberkante); Boden -500; Modell-Z = 400 + Z (D94). Pufferzonen am +Y-Ende.
Aufruf: python -X utf8 scripts/workshop/sumpftank.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import u2_lib as U

NAME = "sumpftank"
MAT = {"Beton": (2.4, "#9a9a96"), "EPDM schwarz": (1.1, "#2b2b2b"), "Wasser": (1.0, "#6fb6e8"), "PP weiss": (0.91, "#e8e5d8"),
       "Stahl verzinkt": (7.85, "#b8bcc2"), "PP grau": (0.91, "#9a9ea3")}


def zonen(p):
    """y-Mitten der vier Zonen und der vier Trennwaende; Hauptkammer endet bei y_h."""
    zl, tt = p["zone_l"], p["trenn_t"]
    y_ende = p["pit_l"] / 2
    y_h = y_ende - p["zone_n"] * zl - p["zone_n"] * tt                  # Ende der Hauptkammer = Vorderkante Wand 1
    wand = [y_h + tt / 2 + k * (zl + tt) for k in range(int(p["zone_n"]))]
    zone = [y_h + tt + zl / 2 + k * (zl + tt) for k in range(int(p["zone_n"]))]
    return y_h, wand, zone


def wand_z(p, k):
    """(z_unten, z_oben) der Trennwand k (0 bis 3): 0 und 2 bodenoffen, 1 und 3 Wehr."""
    boden = -p["pit_d"]
    return (boden + p["trenn_oeff"], p["trenn_oben"]) if k % 2 == 0 else (boden, p["wehr_oben"])


def build(ueber=None):
    p, d, b = U.start(NAME, ueber)
    U.material(b, MAT)
    root = "T101_Sumpftank"
    b.add("component.create", name=root, grounded=True)
    w, l, dp, lt, wt = p["pit_w"], p["pit_l"], p["pit_d"], p["liner_t"], p["wall_t"]
    z_top = -p["deckel_t"]                                   # Oberkante Wanne und Folie (unter dem Deckel)
    # Betonwanne: aussen = innen + 2 x (Folie + Wand); Boden bei -(dp + lt + wt)
    z_b = -(dp + lt + wt)
    U.box(b, "Sumpf_Wanne", (w + 2 * lt + 2 * wt, l + 2 * lt + 2 * wt, z_top - z_b), (0, 0, (z_top + z_b) / 2), "Beton")
    U.box(b, "Sumpf_Wanne", (w + 2 * lt, l + 2 * lt, 480), (0, 0, -(dp + lt) + 240), None, schneiden=["Sumpf_Wanne"])
    # EPDM-Folie: Schale innen, Oberkante -deckel_t
    U.box(b, "Sumpf_Folie", (w + 2 * lt, l + 2 * lt, z_top + dp + lt), (0, 0, (z_top - dp - lt) / 2), "EPDM schwarz")
    U.box(b, "Sumpf_Folie", (w, l, 480), (0, 0, -dp + 240), None, schneiden=["Sumpf_Folie"])
    # Wasserkoerper (Soll-Pegel), danach Trennwaende und Sockel herausgeschnitten
    h_w = p["wsp"] + dp
    U.box(b, "Wasser", (w, l, h_w), (0, 0, -dp + h_w / 2), "Wasser")
    y_h, wand, zone = zonen(p)
    for k, yw in enumerate(wand):
        zu, zo = wand_z(p, k)
        U.box(b, f"Trennwand_{k + 1}", (w, p["trenn_t"], zo - zu), (0, yw, (zu + zo) / 2), "PP weiss")
        U.box(b, f"Trennwand_{k + 1}", (w, p["trenn_t"], zo - zu), (0, yw, (zu + zo) / 2), None, schneiden=["Wasser"])
    sx, sy, sh, ss = p["sockel_x"], p["sockel_y"], p["sockel_h"], p["sockel_s"]
    U.box(b, "Pumpensockel", (ss, ss, sh), (sx, sy, -dp + sh / 2), "PP grau")
    U.box(b, "Pumpensockel", (ss, ss, sh), (sx, sy, -dp + sh / 2), None, schneiden=["Wasser"])
    # Zulauftuellen ID25 durch die -X-Wand (Bohrung durch Wanne und Folie, Tuelle passt ein)
    x_a = -(w / 2 + lt + wt)
    for i, yt in enumerate((-1100, -700, -300), start=1):
        U.cyl(b, f"Zulauf_{i}_Bohrung", p["tuelle_d"], wt + lt + 2, (x_a - 1, yt, p["tuelle_z"]), (1, 0, 0), None, schneiden=["Sumpf_Wanne", "Sumpf_Folie"])
        U.cyl(b, f"Zulauf_{i}", p["tuelle_d"], p["tuelle_l"], (x_a, yt, p["tuelle_z"]), (1, 0, 0), "PP grau")
        U.cyl(b, f"Zulauf_{i}_ID", p["tuelle_id"], p["tuelle_l"] + 2, (x_a - 1, yt, p["tuelle_z"]), (1, 0, 0), None, schneiden=[f"Zulauf_{i}"])
    # Schwimmerhalter an der +X-Folie (60 x 40 x 80), Mitte bei halter_z
    U.box(b, "Schwimmerhalter", (60, 40, 80), (w / 2 - 30, p["halter_y"], p["halter_z"]), "PP grau")
    # Deckel: drei Platten, Oberkante 0
    for i, yc in enumerate((-p["deckel_seg"], 0, p["deckel_seg"]), start=1):
        U.box(b, f"Deckel_{i}", (p["deckel_w"], p["deckel_seg"], p["deckel_t"]), (0, yc, -p["deckel_t"] / 2), "Stahl verzinkt")
    for k, yz in enumerate(zone, start=1):
        U.box(b, f"Zonenschild_{k}", (100, 40, 2), (0, yz, 1), "PP weiss")
    U.fertig(b, root, "T101", d, "Beton / EPDM / PP / Stahl verzinkt")
    return b


if __name__ == "__main__":
    U.main(NAME, build, [("01-schraeg", [0, 0, -250], 0.6, 0.55, 5200, None), ("02-laengsschnitt", [0, 0, -300], -1.5708, 0.0, 5000, "x=0"),
                         ("03-zonen", [0, 1250, -300], -1.5708, 0.0, 1500, "x=0"), ("04-querschnitt", [0, 0, -300], 3.1416, 0.0, 1900, "y=-500")])
