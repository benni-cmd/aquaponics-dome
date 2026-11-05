"""N-AUTOBAHN-V2: Rechnung fuer das Planer-Blatt docs/jobs/N-AUTOBAHN-V2.md.

Nur lesend. Liest scripts/dome-script.json (Lage der Tische, Beete, Biofilter),
data/beschaffung/*.json (Preise) und rechnet Ring, Stelzen, Ausleger,
Schlauch-Fallleitungen, Ruecklauf-Schlauchrinnen, Booster-Leistung und den
Vergleich A+ gegen Wasserautobahn (Ring B2).

Aufruf: python -X utf8 scripts/n_autobahn_rechnung.py
Z-Werte relativ zum Innenboden (absolut = relativ + 400).
[Q] Quelle im Repo, [E] eigene Rechnung, [A] Annahme dieses Skripts.
"""
import json
import math
import glob
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- feste Werte mit Herkunft --------------------------------------------
AP = {"innen": 1864, "mitte": 3277, "aussen": 4874}   # [Q] docs/parts/nft_tisch.md Tischmitte ap_c
GANG = {"A": 600, "B": 500}                          # [Q] D29 Laufweg A/B
HALB = math.radians(18)                              # Zehneck: halber Sektorwinkel
Z_RING_ACHSE, Z_RING_UK, Z_HOCH = 2145, 2100, 2190   # [Q] N-VARIANTEN 2.1, R47c 7.3
Z_TISCH_ZULAUF, Z_BEET_ZULAUF = 1090, 650            # [Q] R47 Abschnitt 1
Z_PLATTFORM = 570                                    # [Q] R47c 7.3 Booster auf Plattform
SCHLAUFE = 300                                       # [A] Schlaufe/Reserve je Fallschlauch, mm
SCHLAUCH_HALTER = 400                                # [Q] Leitungsordnung R6 Schlauch <= 400 mm
RING_HALTER = 1000                                   # [Q] Leitungsordnung R6 d75 <= 1000 mm
Q_BOOSTER = 55.0                                     # [Q] N-VARIANTEN 2.2, l/min je Booster
N_BOOSTER = 4
ETA = (0.25, 0.18)                                   # [Q] R47c 7.1 Klammer
A_PLUS_W = 430                                       # [Q] R47c 7.5 / r47_rechnung.py
SCHACHT_PEGEL_UEBER_BODEN = 340                      # [Q] docs/parts/ring_b2.md Schwimmer EIN 340
SCHACHT_PODEST = 950                                 # [A] Fassboden erhoeht, Zulauf K10 frei aus Ueberlauf 1570
VERLUST_RESERVE = 0.40                               # [A] m: Reibung Steig/Ring + Regelhaehne
R_POOL_KRONE = 2050                                  # [A] Halbring K16 auf der Poolkrone (Wasserradius 1945 [Q nft_tisch.md])

# Linienzuordnung [A dieses Blatts, symmetrisch nach D67: je Linie 7 Beete, 12 Tische]
LINIE1_SEKTOREN = [0, 36, 72, 108]
LINIE2_SEKTOREN = [144, 180, -144, -108]
INNEN_EXTRA = {1: -36, 2: -72}


def az_norm(a):
    a = (a + 180) % 360 - 180
    return 180 if a == -180 else a


def lade_lagen():
    cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json"), encoding="utf8"))["commands"]
    lagen = {}
    for c in cmds:
        if c["command"] != "occurrence.move":
            continue
        name = c["params"]["occurrence"]
        m = c["params"]["matrix"]
        lagen[name] = (m[3], m[7], m[11])
    return lagen


def preise():
    p = {}
    for f in glob.glob(os.path.join(ROOT, "data", "beschaffung", "*.json")):
        d = json.load(open(f, encoding="utf8"))
        art = d if isinstance(d, list) else d.get("artikel", [])
        paare = art.items() if isinstance(art, dict) else [(x.get("id"), x) for x in art if isinstance(x, dict)]
        for i, x in paare:
            a = x.get("angebote") or []
            if a and isinstance(a[0], dict) and a[0].get("preis_eur") is not None:
                p[i] = a[0]["preis_eur"]
    return p


def main():
    lagen = lade_lagen()
    print("== 1. Abnehmer aus dem Modell [E, scripts/dome-script.json]")
    abn = []
    for name, (x, y, z) in sorted(lagen.items()):
        typ = name.split(":")[0]
        if typ not in ("Tisch_innen", "Tisch_mitte", "Tisch_aussen", "Beet_innen_933", "Beet_aussen_800"):
            continue
        az = az_norm(round(math.degrees(math.atan2(y, x))))
        zone = {"Tisch_innen": "innen", "Tisch_mitte": "mitte", "Tisch_aussen": "aussen",
                "Beet_innen_933": "mitte", "Beet_aussen_800": "aussen"}[typ]
        art = "beet" if typ.startswith("Beet") else "tisch"
        if az in LINIE1_SEKTOREN or (zone == "innen" and az == INNEN_EXTRA[1]):
            linie = 1
        elif az in LINIE2_SEKTOREN or (zone == "innen" and az == INNEN_EXTRA[2]):
            linie = 2
        else:
            linie = 0
        ecke = az_norm(az - 18)  # Zulauf am -X-Ende = Sektorgrenze im Uhrzeigersinn [Q nft_tisch.md]
        abn.append(dict(name=name, az=az, zone=zone, art=art, linie=linie, ecke=ecke))
    for l in (1, 2):
        b = sum(1 for a in abn if a["linie"] == l and a["art"] == "beet")
        t = sum(1 for a in abn if a["linie"] == l and a["art"] == "tisch")
        print(f"Linie {l}: {b} Beete, {t} Tische")
    ohne = [a["name"] for a in abn if a["linie"] == 0]
    print("ohne Linie:", ohne or "keine")

    print("\n== 2. Ring (Zehneck ueber der Mittelzone) [E]")
    r_ecke = AP["mitte"] / math.cos(HALB)
    seite = 2 * AP["mitte"] * math.tan(HALB)
    print(f"Eckradius {r_ecke:.0f} mm, Seitenlaenge {seite:.0f} mm, Umfang {10*seite/1000:.2f} m")
    ecken = sorted({a["ecke"] for a in abn})
    print("Ecken mit Abgang:", ecken)
    ring_linie = 4 * seite / 1000
    kupplung = 2 * seite / 1000
    print(f"je Linie 4 Seiten = {ring_linie:.2f} m; Kupplungsstrecken 2 Seiten = {kupplung:.2f} m; gesamt {2*ring_linie+kupplung:.2f} m")
    mitteltische = {a["az"] for a in abn if a["name"].startswith("Tisch_mitte")}
    joch, eigen = [], []
    for e in range(-162, 181, 36):
        nachbarn = {az_norm(e - 18), az_norm(e + 18)}
        (joch if nachbarn & mitteltische else eigen).append(e)
    print(f"Ecken mit Mitteltisch-Portal (Joch): {len(joch)} {joch}; eigene Stelze: {len(eigen)} {eigen}")
    print(f"freie Spannweite zwischen Ecken {seite/1000:.2f} m > 1,65 m (R47 d75) -> Montageschiene als Traeger, Rohrschellen alle <= 1,0 m: {math.ceil(10*seite/RING_HALTER)} Schellen")
    steig = (Z_RING_ACHSE - Z_PLATTFORM) / 1000 + 0.5
    print(f"Steigleitung d63 je Linie {steig:.2f} m (Plattform Z {Z_PLATTFORM} bis Achse {Z_RING_ACHSE} + 0,5 m waagerecht [A])")

    print("\n== 3. Ausleger und Schlauch-Fallleitungen [E]")
    r_inlet = {z: AP[z] / math.cos(HALB) for z in AP}
    ausleger = {}
    schlauch = {"id25": 0.0, "id16": 0.0}
    n_direkt = 0
    for a in abn:
        horiz = abs(r_inlet[a["zone"]] - r_ecke)
        z_ziel = Z_BEET_ZULAUF if a["art"] == "beet" else Z_TISCH_ZULAUF
        lang = horiz + (Z_RING_ACHSE - z_ziel) + SCHLAUFE
        a["schlauch_m"] = lang / 1000
        schlauch["id25" if a["art"] == "beet" else "id16"] += lang / 1000
        if a["zone"] == "mitte":
            n_direkt += 1
        else:
            richtung = "innen" if a["zone"] == "innen" else "aussen"
            ausleger.setdefault((a["ecke"], richtung), horiz)
    n_aus_i = sum(1 for k in ausleger if k[1] == "innen")
    n_aus_a = sum(1 for k in ausleger if k[1] == "aussen")
    l_aus_i = r_ecke - r_inlet["innen"]
    l_aus_a = r_inlet["aussen"] - r_ecke
    print(f"Fallschlaeuche direkt unter dem Ring (Mittelzone): {n_direkt}")
    print(f"Ausleger innen {n_aus_i} x {l_aus_i/1000:.2f} m, aussen {n_aus_a} x {l_aus_a/1000:.2f} m (radial ab Ringecke)")
    halter_aus = n_aus_i * math.ceil(l_aus_i / SCHLAUCH_HALTER) + n_aus_a * math.ceil(l_aus_a / SCHLAUCH_HALTER)
    print(f"Schlauchhalter-Plaetze an Auslegern (<= 400 mm): {halter_aus}")
    print(f"Schlauch ID25 (Beete) {schlauch['id25']:.1f} m, ID16 (Tische) {schlauch['id16']:.1f} m, je Abnehmer {min(a['schlauch_m'] for a in abn):.2f} bis {max(a['schlauch_m'] for a in abn):.2f} m")
    print(f"Ueberbrueckte Gaenge an den Auslegern: A {GANG['A']} mm (innen), B {GANG['B']} mm (aussen); Schlauch dort auf Ausleger >= Z {Z_RING_UK}")

    print("\n== 4. Ruecklauf-Autobahn (NFT, Schwerkraft, Schlauch in Tragrinne) [E, A]")
    seiten = {z: 2 * AP[z] * math.tan(HALB) for z in AP}
    rl = 0.0
    boden = 0
    for l, sek in ((1, LINIE1_SEKTOREN), (2, LINIE2_SEKTOREN)):
        n = {"innen": len(sek) + 1, "mitte": sum(1 for s in sek if s in mitteltische), "aussen": len(sek)}
        sam_m = n["mitte"] * seiten["mitte"] / 1000
        sam_a = n["aussen"] * seiten["aussen"] / 1000
        rad_m = (AP["mitte"] - R_POOL_KRONE) / 1000 + 0.5
        rad_a = (AP["aussen"] - R_POOL_KRONE) / 1000 + 0.5
        innen = n["innen"] * 0.5
        summe = sam_m + sam_a + rad_m + rad_a + innen
        rl += summe
        boden += 3
        print(f"Linie {l}: Sammler Mitte {sam_m:.1f} m + aussen {sam_a:.1f} m, Radialen {rad_m:.1f} + {rad_a:.1f} m, Innentische {innen:.1f} m = {summe:.1f} m")
    br_len = 2 * ((GANG["A"] + 600) + (GANG["B"] + 600) + (GANG["A"] + 600)) / 1000
    print(f"Ruecklauf-Schlauch d50 gesamt {rl:.1f} m (A+ K15 starr: 32,0 m, R47 [Q]); Bodenrinnen mit Rost an Gangquerungen: {boden} Stueck, {br_len:.1f} m")
    gefaelle_mm = (rad_a + 3 * seiten["aussen"] / 1000) * 1000 * 0.01
    print(f"Gefaellebedarf laengster Weg bei 1 %: {gefaelle_mm:.0f} mm; verfuegbar Rinnenende Z 955 bis Poolkrone Z 650..730: >= 225 mm")

    print("\n== 5. Booster-Foerderhoehe und Leistung [E]")
    rho_g = 1000 * 9.81
    q = Q_BOOSTER / 60000
    for titel, pegel in (("Pegelschacht erhoeht (Podest)", SCHACHT_PODEST + SCHACHT_PEGEL_UEBER_BODEN),
                         ("Pegelschacht am Boden", SCHACHT_PEGEL_UEBER_BODEN)):
        h = (Z_HOCH - pegel) / 1000 + VERLUST_RESERVE
        w = [N_BOOSTER * rho_g * q * h / e for e in ETA]
        print(f"{titel}: Pegel Z {pegel}, H {h:.2f} m, 4 Booster {w[0]:.0f} W (eta 25 %) / {w[1]:.0f} W (eta 18 %); "
              f"gesamt {A_PLUS_W + w[0]:.0f} W, {(A_PLUS_W + w[0])*24/1000:.1f} kWh/Tag (A+ {A_PLUS_W} W, {A_PLUS_W*24/1000:.1f})")

    print("\n== 6. Kosten der Unterschiede (Einkaufsliste-Preise, brutto) [E aus data/beschaffung]")
    p = preise()
    stahl_m = len(joch) * 3.3 + len(eigen) * 2.4 + n_aus_i * (l_aus_i / 1000 + 0.6) + n_aus_a * (l_aus_a / 1000 + 0.6)
    mehr = [
        ("Booster (Pumpe gross)", N_BOOSTER, "PMP-pumpe-gross"),
        ("Ringrohr d75 [m]", 2 * ring_linie + kupplung, "ROH-pvcu-d75"),
        ("Steigleitung d63 [m]", 2 * steig, "ROH-pvcu-d63"),
        ("Kugelhahn d63 (Ende, Entleerung, Kupplung)", 6, "ARM-kugelhahn-d63"),
        ("Stahl 40x40x3 Joche/Ausleger/Stelzen [m]", stahl_m, "PRF-st-rr40x40x3"),
        ("Schlauch ID25 [m]", schlauch["id25"], "SCH-schlauch-id25"),
        ("Schlauch ID16 [m]", schlauch["id16"], "SCH-schlauch-id16"),
        ("Pegelschacht-Fass 60 l", 2, "BEH-fass-60"),
        ("Montageschiene 41x41 [m]", 10 * seite / 1000, "PRF-montageschiene-41"),
        ("Schnellkupplung je Abnehmer", len(abn), "SCH-schnellkupplung"),
    ]
    weniger = [
        ("Verteilrohr d40 K11 [m]", 58.9, "ROH-pvcu-d40"),
        ("Verteilrohr d32 K12 [m]", 21.4, "ROH-pvcu-d32"),
        ("Verteiler d50", 2, "FIT-verteiler-d50"),
    ]
    def summe(liste, titel):
        s, offen = 0.0, []
        print(titel)
        for txt, n, i in liste:
            if i in p:
                s += n * p[i]
                print(f"  {txt}: {n:.1f} x {p[i]:.2f} = {n*p[i]:.0f} EUR ({i})")
            else:
                offen.append(txt)
                print(f"  {txt}: {n:.1f} x OFFEN (kein Preis fuer {i})")
        return s, offen
    s_m, o_m = summe(mehr, "Mehr in der Autobahn:")
    s_w, o_w = summe(weniger, "Weniger in der Autobahn (A+-Teile, die entfallen):")
    print(f"Saldo bepreist: +{s_m:.0f} - {s_w:.0f} = +{s_m - s_w:.0f} EUR; ohne Preis: {len(o_m) + len(o_w)} Posten")

    print("\n== 7. Teilezahl der Zulauf-Verteilung (Stueck, ohne Meterware) [E, A]")
    je_abn_gleich = 4  # T/Anbohrstelle, 2 Reduzierungen, Hahn: in beiden Varianten [Q R47: 214 gegen 220]
    ap_teile = 214 + 2 + math.ceil((58.9 + 21.4) * 0.5 / 0.8)
    b2_schlauch = len(abn) * 6   # 2 Tuellen, 2 Schellen, Kupplungspaar
    b2_trag = len(joch) + len(eigen) + n_aus_i + n_aus_a + math.ceil(10 * seite / RING_HALTER) + halter_aus + 10
    b2_tech = N_BOOSTER + 2 + 2 + 6 + 2 + 2 + 2  # Booster, Schacht, Entluefter, Haehne, Rueckschlag, Schwimmer, Steig-T
    b2 = len(abn) * je_abn_gleich + b2_schlauch + b2_trag + b2_tech
    print(f"A+: 214 Formteile/Armaturen (R47) + 2 Verteiler + {math.ceil((58.9 + 21.4) * 0.5 / 0.8)} Halter (Haelfte der 80,3 m ueber Flur, 800 mm) = {ap_teile}")
    print(f"Autobahn: {len(abn)} x {je_abn_gleich} Abzweig + {b2_schlauch} Schlauchteile + {b2_trag} Tragwerk/Halter + {b2_tech} Technik = {b2}")

    print("\n== 8. Grabenmeter Zulauf (Gangquerung nur im Graben KG, Leitungsordnung R9) [E, A]")
    q_a = (GANG["A"] + 600) / 1000   # Gang + 2 x 300 mm Uebergang [A]
    q_b = (GANG["B"] + 600) / 1000
    n_aussen = sum(1 for a in abn if a["zone"] == "aussen")
    n_innen = sum(1 for a in abn if a["zone"] == "innen")
    gebuendelt = 2 * (q_a + q_b)
    einzeln = n_aussen * q_b + n_innen * q_a
    print(f"A+: gebuendelt je Linie 1 Querung Gang A + 1 Gang B = {gebuendelt:.1f} m; je Abnehmer einzeln ({n_aussen} aussen, {n_innen} innen) = {einzeln:.1f} m")
    print("Autobahn: 0 m (Gaenge werden auf Auslegern ueber Z 2100 gequert)")
    print("Gemeinsam in beiden: 30,3 m vergrabenes Rohr vor dem Verteiler/Pegelschacht [Q R47b 6.0]")

    print("\n== 9. Wartung und Ausfall [E Zaehlung]")
    print(f"Handgriffe ueber Kopf (Leiter): A+ 0; Autobahn {len(abn)} Abzweig-Koepfe + 2 Entluefter + {2*ring_linie+kupplung:.1f} m Ring")
    print("Aktive Glieder nach dem Biofilter je Linie: A+ 0 (Schwerkraft); Autobahn 2 Booster + 1 Schwimmerschalter + 1 Rueckschlagventil-Paar")
    print(f"Schlauchverbindungen unter Druck ueber Pflanzen: A+ 0; Autobahn {len(abn) * 2}")
    print("Stromausfall: A+ Zulauf steht mit den Hauptpumpen; Autobahn ebenso, Ring laeuft leer in den Pegelschacht/Notueberlauf")


if __name__ == "__main__":
    main()
