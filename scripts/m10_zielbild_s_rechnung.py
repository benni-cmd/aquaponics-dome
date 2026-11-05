"""M10-ZIELBILD-S: Rechnung fuer das Planer-Blatt docs/jobs/M10-ZIELBILD-S.md.

Nur lesend. Liest data/leitungstrassen.json, data/params.json, data/layout.json,
scripts/dome-script.json und rechnet Rueckbau, Pool-Lage nach D88, Beet-Anhebung,
Platz fuer Gelaender, Gefaelle Beet-Ruecklauf und Stern gegen Strang ab der Wasserstation.

Aufruf: python -X utf8 scripts/m10_zielbild_s_rechnung.py
Z relativ zum Flur (absolut = relativ + 400). [Q] Quelle, [E] Rechnung, [A] Annahme.
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf8"))
FLUR = 400

# Kanten und Zusatzteile, die im Zielbild S entfallen [Q R57 Abschnitt 2, G2 bis G7, G13]
ENTFALLEN = {"K01", "K02", "K03", "K04", "K05", "K06", "K07", "K17", "K18", "K19", "K20", "K21",
             "K22", "K23", "K56", "K57", "REV1", "REV2", "SP1", "SP2", "KSP1_1", "KSP1_2", "KSP2_1",
             "KSP2_2", "KB1", "KB2"}
NEU_ALS_SCHLAUCH = {"K08", "K09", "K24", "K25"}                       # Pumpe -> Biofilter wird Art B [Q R57 1]
LUFT_FRISCH = {"K39", "K40", "K41", "K44", "K45", "K46", "K49", "K51", "K52"}  # aus dem Graben [Q R57 G18/G19]

D88 = {"ruhepegel": -150, "rand": 0, "aufkantung": 150, "boden_wasser": -2350}  # [Q R57 Nachtrag D88]


def laenge(p, nur_unter=False):
    s = 0.0
    for a, b in zip(p, p[1:]):
        if not nur_unter or (a[2] + b[2]) / 2 < FLUR:
            s += math.dist(a, b)
    return s


def main():
    t = J("data", "leitungstrassen.json")
    print("== 1. Rueckbau gebauter Trassen (Variante a_plus/gemeinsam) [E data/leitungstrassen.json]")
    summen = {"entfallen": [0, 0.0, 0.0], "schlauch": [0, 0.0, 0.0], "luft_frisch": [0, 0.0, 0.0]}
    for tr in t["trassen"]:
        if "ring_b2" in (tr.get("varianten") or []):
            continue
        k = str(tr.get("kante") or tr.get("id")).split("-")[0]
        p = tr.get("pfad") or []
        if not p or not isinstance(p[0], (list, tuple)):
            continue
        for key, menge in (("entfallen", ENTFALLEN), ("schlauch", NEU_ALS_SCHLAUCH), ("luft_frisch", LUFT_FRISCH)):
            if k in menge:
                s = summen[key]
                s[0] += 1
                s[1] += laenge(p)
                s[2] += laenge(p, True)
    for key, (n, l, u) in summen.items():
        print(f"{key}: {n} Trassen, {l/1000:.1f} m, davon unter Flur {u/1000:.1f} m")
    teile = [x for x in t.get("teile", []) if str(x.get("kante") or x.get("id", "")).split("-")[0] in ENTFALLEN | {"SCH", "schlammfass_1", "schlammfass_2", "FH1", "FH2"}]
    gruben = t.get("gruben", [])
    tst = [x for x in t.get("t_stuecke", []) if "ring_b2" not in (x.get("varianten") or [])]
    rst = [x for x in t.get("r_stuecke", []) if "ring_b2" not in (x.get("varianten") or [])]
    print(f"Zusatzteile in Rueckbau-Kanten: {len(teile)} von {len(t.get('teile', []))}; Gruben {len(gruben)}; "
          f"T-Stuecke gesamt {len(tst)}, R-Stuecke gesamt {len(rst)} (Montage prueft je Eintrag)")

    print("\n== 2. Pool nach D88 [E params.json, layout.json]")
    P = {k: v["value"] for k, v in J("data", "params.json").items() if isinstance(v, dict) and "value" in v}
    L = J("data", "layout.json")
    wz = L["pool"]["water_z"]
    boden_heute = wz - P["pool_depth"] + 120  # Innenboden = z_bot + POOL_BODEN (gen_dome.py)
    tiefe_wasser = wz - boden_heute
    print(f"heute: Spiegel Z {wz}, Rand Z {P['pool_rim']}, Innenboden Z {boden_heute}, Wassertiefe {tiefe_wasser} mm, d {L['pool']['d']}")
    neu_boden = D88["ruhepegel"] - tiefe_wasser
    neu_depth = D88["ruhepegel"] - neu_boden + 120
    print(f"D88: Spiegel Z {D88['ruhepegel']}, Rand Z {D88['rand']} + Aufkantung {D88['aufkantung']}, Innenboden Z {neu_boden} "
          f"(R57: {D88['boden_wasser']}); Parameter: layout pool.water_z {D88['ruhepegel']}, pool_rim {D88['aufkantung']}, "
          f"pool_depth {neu_depth} (water_z - z_bot), Absenkung {wz - D88['ruhepegel']} mm")
    vol = math.pi * (L["pool"]["d"] / 2000) ** 2 * tiefe_wasser / 1000
    print(f"Wasser {vol:.1f} m3 bleibt (gleicher Durchmesser und Tiefe)")
    print(f"Zweitbecken: Spiegel Z {L['pool2']['water_z']} bleibt; Ueberlauf in den Pool faellt {L['pool2']['water_z'] - D88['ruhepegel']} mm")

    print("\n== 3. Beete auf den Flur [E layout.json ibc_beds]")
    beds = L.get("ibc_beds") or []
    zs = sorted({b["z0"] for b in beds})
    print(f"{len(beds)} Beete, Unterkante heute Z {zs[0]} bis {zs[-1]} -> neu Z 0; Anhebung {-zs[-1]} bis {-zs[0]} mm; "
          f"Taschen im Erdkoerper entfallen (gen_dome erde_fn T9_Tasche)")

    print("\n== 4. Platz fuer das Gelaender am Pool [E params, nft_tisch.json]")
    r_aussen = L["pool"]["d"] / 2 + P["wall"]
    nt = J("data", "components", "nft_tisch.json")
    holm = 60
    for k, v in nt.get("parameter", {}).items() if isinstance(nt.get("parameter"), dict) else []:
        if k == "holm_h":
            holm = v.get("value", 60) if isinstance(v, dict) else v
    unter_kragarm = 1000 - holm
    print(f"Pool-Aussenradius {r_aussen:.0f} mm; Innentisch-Fussplatte ab {r_aussen + 30:.0f} (leg_clearance_innen 30 [Q nft_tisch.md]); "
          f"Gelaender passt nur AUF die Aufkantung (Wandkrone {P['wall']} mm breit)")
    print(f"freie Hoehe unter dem Kragarm der Innentische: Z {unter_kragarm} (Rinne 1000 minus Holm {holm}); "
          f"Gelaender ueber der Aufkantung hoechstens {unter_kragarm - D88['aufkantung'] - 40} mm (40 mm Luft [A]), Oberkante Z {unter_kragarm - 40}")
    tische = []
    for c in J("scripts", "dome-script.json")["commands"]:
        if c["command"] == "occurrence.move" and c["params"]["occurrence"].startswith("Tisch_innen"):
            m = c["params"]["matrix"]
            tische.append(math.degrees(math.atan2(m[7], m[3])))
    seite_innen = 2 * 1864 * math.tan(math.radians(18))
    print(f"{len(tische)} Innentische umschliessen den Pool; Laenge je Tisch {seite_innen:.0f} mm entlang Zehneck-Seite")

    print("\n== 5. Gefaelle Beet-Ruecklauf (Art C) bis zur Pool-Einmuendung [E, A]")
    ablauf = 62        # [Q R57 G11] Ablauf auf dem Flur
    einm = -60         # [A] Einmuendung durch die Wand ueber dem Ruhepegel -150, unter Flur
    for name, r_beet in (("Aussenbeet", 5074), ("Innenbeet", 3377)):
        weg = (r_beet - r_aussen) * 1.3 + 1500   # Umweg 1,3 und 1,5 m am Beetfuss [A]
        noetig = weg * 0.01
        print(f"{name}: Weg etwa {weg/1000:.1f} m, Gefaelle 1 % braucht {noetig:.0f} mm; verfuegbar {ablauf - einm} mm "
              f"(Ablauf Z {ablauf} bis Einmuendung Z {einm}) -> {'reicht' if noetig <= ablauf - einm else 'reicht NICHT'}")
    print(f"Stromausfall Planfall: Pegel -150 + 111 = Z -39 -> Einmuendung Z {einm} liegt dann unter Wasser: Belueftungsloch (Siphonbrecher, hydraulics 2.9) Pflicht")

    print("\n== 6. Wasserstation: Stern (Hahn je Abnehmer an der Station) gegen Strang [E dome-script.json, A Umweg 1,25]")
    lagen = {}
    for c in J("scripts", "dome-script.json")["commands"]:
        if c["command"] == "occurrence.move":
            m = c["params"]["matrix"]
            lagen[c["params"]["occurrence"]] = (m[3], m[7])
    bio = {1: lagen["Tank_gross:1"], 2: lagen["Tank_gross_t3:1"]}
    sek = {1: [0, 36, 72, 108], 2: [144, 180, -144, -108]}
    extra = {1: -36, 2: -72}
    for linie in (1, 2):
        ziele = []
        for name, (x, y) in lagen.items():
            typ = name.split(":")[0]
            if typ not in ("Tisch_innen", "Tisch_mitte", "Tisch_aussen", "Beet_innen_933", "Beet_aussen_800"):
                continue
            az = round(math.degrees(math.atan2(y, x)))
            az = 180 if az == -180 else az
            if az in sek[linie] or (typ == "Tisch_innen" and az == extra[linie]):
                ziele.append((x, y))
        bx, by = bio[linie]
        stern = sum((abs(x - bx) + abs(y - by)) for x, y in ziele) * 1.25 / 1000
        rest, pos, strang = list(ziele), (bx, by), 0.0
        while rest:
            n = min(rest, key=lambda q: math.dist(q, pos))
            strang += math.dist(n, pos)
            pos = n
            rest.remove(n)
        strang = strang * 1.25 / 1000
        print(f"Linie {linie}: {len(ziele)} Abnehmer; Stern {stern:.0f} m Leitung, Strang {strang:.0f} m (Faktor {stern/strang:.1f})")


if __name__ == "__main__":
    main()
