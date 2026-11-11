"""N-UNIFY-AUTOBAHN U6 Aufgabe 4: die Wege der Quelle ausserhalb des Rings, Lage aus dem Bauskript und den Komponenten.

Rohre (Leitungsbibliothek lt_*, Eintraege in data/leitungstrassen.json mit quelle "trassen_soll", Feld soll_weg):
  e21/e22 Pumpstelle 1 Fischtank -> Vortex (d50, ueber Kopf), e23/e24 Vortex -> Biofilter (d63, Schwerkraft), e59/e61 Pumpstelle 2 Sumpf -> Venturi (d50),
  e71/e72 Venturi -> Fischtank (d50), e62 Biofilter 1 -> Lebendfutterbecken, e63 Lebendfutter -> Anzucht, e70 Anzucht -> Fischtank (d63, Ueberlaeufe),
  e81/e82 Notueberlauf Biofilter -> Sumpf (d63), e64 bis e67 Schlamm Vortex/Biofilter -> Sammelbehaelter (d50), e17/e18/e19 Nachspeisung (d25),
  Luft e77, e86 bis e89, e91 bis e94 (d20, ueber dem hoechsten Wasserspiegel gefuehrt).
Schlaeuche (Komponente designs/components/ring_ruecklauf.sc in Weltlage, Darstellung wie die Fallleitungen):
  e33/e34 Ring-Ende-Hahn -> Sumpf, e49 bis e56 Rueckläufe Beete und Tische -> Sumpf der eigenen Linie, e57 NFT Innen -> Fischtank (ID25).
Aufruf: python -X utf8 scripts/trassen_soll.py [--bericht] [--schreiben] [--bauen]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "workshop"))
import trassen_ring as TR
import autobahn_s as AS
from trassen_ring import add, sub, mul, dot, unit, world, wdir, rd

QUELLE = "trassen_soll"
FZ = TR.FZ
MV = TR.MV
Z_UE = FZ + 2150.0                  # [A] Ueberkopf-Ebene fuer lange Druck- und Luftleitungen (Band UE >= 2100 rel), ueber Ring-Tragwerk (1702 rel) und Tischen
L_STUB = 150.0                      # [A] gerades Stueck ab Stutzen
PORTS = json.load(open(os.path.join(ROOT, "data", "becken-ports.json"), encoding="utf-8"))
LINIE = {1: dict(vortex="Tank_klein:1", bio="Tank_gross:1", pumpe1="Tauchpumpe_Modul:1", pumpe2="Tauchpumpe_Modul:3", venturi="Venturi_Belueffter:1", sump="Sumpftank:1",
                 sludge="Schlamm_Sammelbehaelter:1", geblaese="Luftverteiler_4:1", scheibe="Luft_Scheibenbelueftung:1"),
         2: dict(vortex="Tank_klein:2", bio="Tank_gross_t3:1", pumpe1="Tauchpumpe_Modul:2", pumpe2="Tauchpumpe_Modul:4", venturi="Venturi_Belueffter:2", sump="Sumpftank:2",
                 sludge="Schlamm_Sammelbehaelter:2", geblaese="Luftverteiler_4:2", scheibe="Luft_Scheibenbelueftung:3")}


def P(occ, loc): return world(MV[occ], loc)
def D(occ, d): return unit(wdir(MV[occ], d))
def hz(v): v = (v[0], v[1], 0.0); return unit(v)


def ortho(p0, d0, p1, d1=None, zu=None, a=None, dn=50):
    """Rohrweg nur mit 90-Grad-Boegen (Bibliothek lt_bogen90): ab p0 optional senkrecht auf die Ebene zu, dann waagerecht in zwei Achsen (a = waagerechter Anteil
    von d1 bzw. d0 bzw. vorgegeben, b senkrecht dazu), dann senkrecht auf die Hoehe von p1. Stutzen-Richtungen gehen nur in die Wahl der Achsen ein (offene Enden, [A]).
    Teilstuecke kuerzer als zwei Bogenschenkel entfallen; das Rohrende rueckt dann hoechstens um diese Laenge vom Zielpunkt ab (Darstellung)."""
    import leitungen as LTG
    kmin = 2 * LTG.tangent("bogen90", dn) + 10.0
    ref = d1 if (d1 is not None and abs(d1[2]) < 0.5) else (d0 if abs(d0[2]) < 0.5 else None)
    a = hz(ref) if ref is not None else (a or (1.0, 0.0, 0.0)); b = (-a[1], a[0], 0.0)
    pts = [tuple(p0)]; cur = tuple(p0)
    z = cur[2] if zu is None else zu
    if abs(z - cur[2]) >= kmin: cur = (cur[0], cur[1], z); pts.append(cur)
    dl = sub((p1[0], p1[1], cur[2]), cur)
    ta, tb = dot(dl, a), dot(dl, b)
    if abs(ta) >= kmin: cur = add(cur, a, ta); pts.append(cur)
    if abs(tb) >= kmin: cur = add(cur, b, tb); pts.append(cur)
    if abs(p1[2] - cur[2]) >= kmin: cur = (cur[0], cur[1], p1[2]); pts.append(cur)
    if len(pts) == 1: pts.append(tuple(p1))
    return [rd(p) for p in pts]


def trasse(tid, weg, dn, pfad, farbe, band, notiz, linie=None, anschluss=(), **kw):
    return dict(id=tid, kante="S-" + weg, soll_weg=weg, dn=dn, farbe=farbe, start="offen", ende="offen", pfad=pfad, band=band, linie=linie,
                anschluss=list(anschluss), quelle=QUELLE, notiz=notiz, **kw)


# ------------------------------------------------------------------ Anschlusspunkte (lokal aus viewer/detail/tank_klein.json, tank_gross.json; Komponenten-Parameter)
VX_ZULAUF = ((282.0, -351.0, 997.0), (0.0, -1.0, 0.0))        # Vortex Zulaufrohr (Pumpe), Oeffnung -Y
VX_AUSLAUF = ((442.0, 0.0, 1147.0), (1.0, 0.0, 0.0))          # Vortex Auslaufrohr d50 zum Biofilter (Wsp 1900 rel, Achse 1724 rel)
VX_SCHLAMM = ((0.0, 0.0, 80.0), (0.0, 0.0, -1.0))             # Vortex Ablaufstutzen unten (Schlamm)
BF_ZULAUF = ((403.0, -395.0, 1420.0), (0.0, -1.0, 0.0))       # Biofilter Zulaufrohr, Oeffnung -Y
BF_NOT = ((-465.0, 0.0, 1620.0), (-1.0, 0.0, 0.0))            # [A] Notueberlauf: Stutzen d63 50 mm ueber dem Ueberlauf (1570 lokal), Gegenseite (D140)
BF_SCHLAMM = ((0.0, 0.0, 134.0), (0.0, 0.0, -1.0))            # Biofilter Ablaufstutzen unten
PUMPE_DRUCK = (0.0, 0.0, 389.0)                               # Tauchpumpe: Druckrohr d50 senkrecht, Z +389 ueber dem Standpunkt (U5)
VENTURI_L = 2 * 60.0 + 150.0                                  # Muffe + Injektor + Muffe (venturi_belueffter: muffe_l 60, inj_l 150), Stroemung +X


def rohre():
    tr = []
    for l, o in LINIE.items():
        s = "_%d" % l
        # e21/e22 Pumpstelle 1: Tauchpumpe im Fischtank -> ueber Kopf -> Vortex-Zulauf (Druck, d50)
        p0 = P(o["pumpe1"], PUMPE_DRUCK); pz, dz = VX_ZULAUF
        tr.append(trasse("S%d-e2%d" % (l, l), "e21" if l == 1 else "e22", 50, ortho(p0, (0, 0, 1), P(o["vortex"], pz), D(o["vortex"], dz), zu=Z_UE),
                         "dunkelblau", "UE", "Pumpstelle 1 Linie %d: Druckrohr d50 der Tauchpumpe im Fischtank, senkrecht ueber Kopf (Z %.0f rel), in den Vortex-Zulauf (Hub 1,15 m, Quelle)" % (l, Z_UE - FZ),
                         linie=l, anschluss=[o["vortex"], "Zentralpool"]))
        # e23/e24 Vortex -> Biofilter (Schwerkraft, d63 nach D106)
        pa, da = VX_AUSLAUF; pb, db = BF_ZULAUF
        tr.append(trasse("S%d-e2%d" % (l, 2 + l), "e23" if l == 1 else "e24", 63, ortho(P(o["vortex"], pa), D(o["vortex"], da), P(o["bio"], pb), D(o["bio"], db), dn=63),
                         "dunkelblau", "WH", "Vortex -> Biofilter Linie %d: Auslauf %.0f rel -> Zulauf %.0f rel, Schwerkraft (Quelle e23/e24)" % (l, P(o["vortex"], pa)[2] - FZ, P(o["bio"], pb)[2] - FZ),
                         linie=l, anschluss=[o["vortex"], o["bio"]]))
        # e59/e61 Pumpstelle 2: Tauchpumpe im Sumpf -> ueber Kopf -> Venturi Port A (Achse +X)
        p0 = P(o["pumpe2"], PUMPE_DRUCK); mv = MV[o["venturi"]]; vo = (mv[3], mv[7], mv[11]); vx = unit((mv[0], mv[4], mv[8]))
        tr.append(trasse("S%d-e%s" % (l, "59" if l == 1 else "61"), "e59" if l == 1 else "e61", 50, ortho(p0, (0, 0, 1), vo, mul(vx, -1), zu=Z_UE),
                         "dunkelblau", "UE", "Pumpstelle 2 Linie %d: Druckrohr d50 aus dem Sumpf ueber Kopf zum Venturi (Hub 1,00 m, Quelle)" % l, linie=l, anschluss=[o["sump"], o["venturi"]]))
        # e71/e72 Venturi Port B -> Fischtank (unter den Wasserspiegel, Fischtank Wsp 750 rel)
        vb = add(vo, vx, VENTURI_L); fz = FZ + 750 - 250
        r_in = 1945.0 - 250.0; c = (0.0, 0.0)
        u = hz(vx); tt = dot(sub((c[0], c[1], 0), (vb[0], vb[1], 0)), u)
        ziel = add(vb, u, max(150.0, tt - (math.sqrt(max(r_in ** 2 - (dot(sub((c[0], c[1], 0), (vb[0], vb[1], 0)), (-u[1], u[0], 0))) ** 2, 0)))))
        tr.append(trasse("S%d-e%s" % (l, "71" if l == 1 else "72"), "e71" if l == 1 else "e72", 50, [rd(vb), rd(ziel), rd((ziel[0], ziel[1], fz))],
                         "dunkelblau", "WH", "Venturi -> Fischtank Linie %d: weiter in Stroemungsrichtung bis in den Fischtank, senkrecht unter den Spiegel (Austritt 250 unter Wsp)" % l,
                         linie=l, anschluss=[o["venturi"], "Zentralpool", "Tisch_innen"]))
        # e81/e82 Notueberlauf Biofilter -> Sumpf (d63, faellt ueber 2 m)
        pn, dn_ = BF_NOT; zz = PORTS["sumpf_zulaeufe"][(l - 1) * 3 + 1]
        zp = tuple(zz["port_mm"]); zr = tuple(zz["richtung"])
        tr.append(trasse("S%d-e8%d" % (l, l), "e81" if l == 1 else "e82", 63, ortho(P(o["bio"], pn), D(o["bio"], dn_), (zp[0], zp[1], FZ + 60), mul(zr, -1), dn=63),
                         "grau", "W", "Notueberlauf Biofilter %d -> Sumpf %d (d63, Quelle e81/e82): Stutzen 50 ueber dem Ueberlauf, senkrecht auf 60 rel, waagerecht zum Sumpf (Einmuendung ueber dem Deckel)" % (l, l),
                         linie=l, anschluss=[o["bio"], o["sump"]], gefaelle_pct=None))
        # e64/e65 Schlamm Vortex -> Sammelbehaelter, e66/e67 Biofilter -> Sammelbehaelter (d50, Kugelhahn von Hand am Stutzen)
        ms = MV[o["sludge"]]; sc_ = (ms[3], ms[7], ms[11])
        for occ, (pl, dl), weg, z_end in ((o["vortex"], VX_SCHLAMM, "e64" if l == 1 else "e65", FZ + 575 + 15 + 60), (o["bio"], BF_SCHLAMM, "e66" if l == 1 else "e67", FZ + 300)):
            p0 = P(occ, pl); zk = min(p0[2] - 150.0, z_end) if weg in ("e64", "e65") else p0[2] - 150.0
            ziel = (sc_[0], sc_[1], z_end) if weg in ("e64", "e65") else add((sc_[0], sc_[1], z_end), hz(sub(p0, sc_)), 450.0)
            pfad = ortho(p0, (0, 0, -1), ziel, None if weg in ("e64", "e65") else hz(sub(p0, sc_)), zu=zk)
            tr.append(trasse("S%d-%s" % (l, weg), weg, 50, pfad, "grau", "W", "Schlamm %s -> Sammelbehaelter %d (d50, Schwerkraft, Kugelhahn von Hand am Stutzen)" % (occ.split(":")[0], l),
                             linie=l, anschluss=[occ, o["sludge"]]))
    # Beckenkette: e62 Biofilter 1 -> Lebendfutterbecken, e63 Lebendfutter -> Anzucht, e70 Anzucht -> Fischtank (Ueberlauf-Tuellen d63 aus U3)
    mf = MV["Becken_Dritt:1"]; feed = (mf[3], mf[7], mf[11])
    pb = P(LINIE[1]["bio"], (0.0, 465.0, 1500.0)); db = D(LINIE[1]["bio"], (0.0, 1.0, 0.0))     # [A] Abgang d63 an der +Y-Seite unter dem Spiegel (D140)
    tr.append(trasse("S1-e62", "e62", 63, ortho(pb, db, (feed[0], feed[1], FZ + 1000 + 100), None, dn=63), "dunkelblau", "WH",
                     "Biofilter 1 -> Lebendfutterbecken (d63, Schwerkraft 1800 -> 850): Abgang unter dem Spiegel, frei auslaufend 100 ueber dem Beckenrand", linie=1,
                     anschluss=[LINIE[1]["bio"], "Becken_Dritt:1"]))
    for u in PORTS["ueberlaeufe"]:
        p0 = tuple(u["port_mm"]); r = tuple(u["richtung"])
        if u["weg"] == "e63":
            mz = None
            for n, m in MV.items():
                if n.startswith("Zweitbecken") or n.startswith("Becken_Zweit"): mz = m
            tz = (2797.0, -3476.0) if mz is None else (mz[3], mz[7])
            dist = math.hypot(tz[0] - p0[0], tz[1] - p0[1]) - 1000.0
        else:
            dist = math.hypot(p0[0], p0[1]) - 1945.0
        tr.append(trasse("S0-" + u["weg"], u["weg"], 63, [rd(p0), rd(add(p0, r, dist))], "dunkelblau", "W",
                         "Ueberlauf %s (d63, U3-Tuelle) gerade in das naechste Becken, Wandeinfuehrung ueber dessen Spiegel (Quelle %s)" % (u["name"], u["weg"]),
                         anschluss=["Zweitbecken", "Becken_Dritt:1", "Zentralpool"]))
    # Nachspeisung e17 (Regen), e18 (Frischwasser ueber die Aktivkohle-Station), e19 (Ventil -> Fischtank), d25
    mn = MV["Nachspeise_Ventil:1"]; nv = (mn[3], mn[7], mn[11]); nx = unit((mn[0], mn[4], mn[8]))
    mr = MV["Regentank_5m3:1"]; rt = (mr[3], mr[7], mr[11])
    d_r = hz(sub(nv, rt)); p_r = add((rt[0], rt[1], FZ + 150), d_r, 850.0)
    tr.append(trasse("S0-e17", "e17", 25, ortho(p_r, d_r, add(nv, nx, -120.0), None, zu=Z_UE, dn=25), "hellblau", "UE",
                      "Regenwasser 5 m3 -> Nachspeise-Ventil (d25, Auslauf 150 ueber Tankboden; Antrieb offen wie in der Quelle: Ventil liegt hoeher als der Tank, Bedenken B16)", anschluss=["Regentank_5m3:1", "Nachspeise_Ventil:1"]))
    ma = MV["Aktivkohle_Station:1"]; pa = world(ma, (900.0, 0.0, 800.0)); da = unit(wdir(ma, (1.0, 0.0, 0.0)))
    tr.append(trasse("S0-e18", "e18", 25, ortho(pa, da, add(nv, nx, -60.0), None, zu=Z_UE + 60, dn=25), "hellblau", "UE",
                      "Frischwasser (Hahn) ueber die Aktivkohle-Station -> Nachspeise-Ventil (d25, zweiter Eingang, D107)", anschluss=["Aktivkohle_Station:1", "Nachspeise_Ventil:1"]))
    u_f = hz(mul(nv, -1)); e19a = add(nv, u_f, max(150.0, math.hypot(nv[0], nv[1]) - 1800.0))
    tr.append(trasse("S0-e19", "e19", 25, [rd(nv), rd(e19a), rd((e19a[0], e19a[1], FZ + 900))], "hellblau", "WH",
                      "Nachspeise-Ventil -> Fischtank (d25, frei auslaufend 150 ueber dem Spiegel)", anschluss=["Nachspeise_Ventil:1", "Zentralpool", "Tisch_innen"]))
    # Luft d20: je Geblaese-Verteiler 4 Arme (Biofilter, Sumpf, Becken, Fischtank), ueber Kopf, senkrecht hinab bis kurz ueber den Boden des Ziels
    ziele = {1: [("e86", P(LINIE[1]["bio"], (212.0, 150.0, 300.0))), ("e87", add(P(LINIE[1]["sump"], (0.0, 600.0, 0.0)), (0, 0, 1), -420.0)),
                 ("e88", None), ("e89", None)],
             2: [("e91", P(LINIE[2]["bio"], (212.0, 150.0, 300.0))), ("e92", add(P(LINIE[2]["sump"], (0.0, 600.0, 0.0)), (0, 0, 1), -420.0)),
                 ("e93", (feed[0] + 200.0, feed[1], FZ + 100.0)), ("e94", None)]}
    mz2 = (2797.0, -3476.0)
    for l, liste in ziele.items():
        mv_ = MV[LINIE[l]["geblaese"]]; vx_ = unit((mv_[0], mv_[4], mv_[8]))
        for i, (weg, ziel) in enumerate(liste):
            if ziel is None:
                if weg == "e88": ziel = (mz2[0] + 300.0, mz2[1], FZ + 100.0)
                else:
                    ms_ = MV[LINIE[l]["scheibe"]]; ziel = (ms_[3] * 0.85, ms_[7] * 0.85, ms_[11] + 60.0)
            arm = world(mv_, (75.0 + 120.0 * i, 0.0, 24.0))
            tr.append(trasse("S%d-%s" % (l, weg), weg, 20, ortho(arm, (0, 0, 1), ziel, None, zu=Z_UE + 120 + 30 * i, dn=20), "gruen", "UE",
                             "Luft Linie %d Arm %d (d20): Verteiler -> ueber Kopf -> senkrecht in das Ziel bis kurz ueber den Boden" % (l, i + 1), linie=l,
                             anschluss=[LINIE[l]["geblaese"], LINIE[l]["bio"], LINIE[l]["sump"], "Zentralpool", "Zweitbecken", "Becken_Dritt:1", "Tisch_innen", "Luft_Scheibenbelueftung"]))
    mnl = MV["Notluftpumpe:1"]; pn = world(mnl, (0.0, 0.0, 300.0))
    tr.append(trasse("S0-e77", "e77", 20, ortho(pn, (0, 0, 1), (pn[0] * 0.25, pn[1] * 0.25, FZ - 900.0), None, zu=Z_UE + 260, dn=20), "gruen", "UE",
                      "Notluft (d20): Notluftpumpe -> ueber Kopf (Schleife ueber dem Rand) -> Luftstein im Fischtank (Befund U5: Komponente reicht nicht ins Wasser)",
                      anschluss=["Notluftpumpe:1", "Zentralpool", "Tisch_innen"]))
    return tr


# ------------------------------------------------------------------ Schlaeuche: Rueckläufe in den Sumpf der eigenen Linie, NFT Innen in den Fischtank, Ring-Ende -> Sumpf
HOSE_ID = 25
R_WAND = 5560.0                     # [A] Schlauchgasse vor der Kuppelwand (Aussenbeete enden bei r ~5480)
Z_BODEN = FZ + AS.HOSE[HOSE_ID]["ad"] / 2 + 2.0
SOLL_RUECK = {(1, "beet", "aussen"): "e49", (1, "beet", "mitte"): "e50", (2, "beet", "aussen"): "e51", (2, "beet", "mitte"): "e52",
              (1, "tisch", "aussen"): "e53", (1, "tisch", "mitte"): "e54", (2, "tisch", "aussen"): "e55", (2, "tisch", "mitte"): "e56"}
AUSLASS = {"Beet_aussen_800": ((1360.0, 0.0, 28.0), (1.0, 0.0, 0.0)), "Beet_innen_933": ((973.0, 65.0, 28.0), (1.0, 0.0, 0.0)),   # U3b: Schlauchtuelle +X-Stirnwand, Achse z 28
          "Tisch_aussen": ((1484.0, 505.0, 1029.0), (0.0, 1.0, 0.0)), "Tisch_mitte": ((979.0, 527.0, 887.0), (0.0, 1.0, 0.0)), "Tisch_innen": ((519.0, 264.0, 1244.0), (0.0, 1.0, 0.0))}   # Sammelrohr +Y-Ende (viewer/detail)


def _kante_az(a):
    """naechste Sektorgrenze (Fuge zwischen zwei Abnehmern): Azimut 18 + 36 k."""
    return 18.0 + 36.0 * round((a - 18.0) / 36.0)


def _polar(r, a): return (r * math.cos(math.radians(a)), r * math.sin(math.radians(a)))


def schlauch_weg_rueck(o_pt, o_dir, ziel, ziel_dir, z_ziel):
    """Ab dem Auslass: kurzer Anlauf, senkrecht auf den Boden, zur naechsten Sektorgrenze, radial in die Schlauchgasse vor der Wand, entlang der Wand
    (Ecken auf den Zehneck-Ecken) zum Ziel-Azimut, radial zum Zulauf; Z faellt stetig (Boden: von Z_BODEN + 8 auf Z_BODEN)."""
    R = AS.hose_R(HOSE_ID)
    s0 = add(o_pt, o_dir, R + 30.0)                                  # Anlauf so lang wie ein Bogen (Rb), dann senkrecht
    a0 = math.degrees(math.atan2(s0[1], s0[0])); r0 = math.hypot(s0[0], s0[1]); ak = _kante_az(a0)
    zq = (ziel[0] - ziel_dir[0] * 400, ziel[1] - ziel_dir[1] * 400)
    az_z = math.degrees(math.atan2(zq[1], zq[0]))
    pts = [o_pt, s0, (s0[0], s0[1], Z_BODEN + 8)]
    k = _polar(r0, ak)
    if math.hypot(k[0] - s0[0], k[1] - s0[1]) > 2 * R + 20: pts.append((k[0], k[1], Z_BODEN + 7))   # zur Fuge, sonst radial auf dem eigenen Azimut
    else: ak = a0
    w0 = _polar(R_WAND, ak); pts.append((w0[0], w0[1], Z_BODEN + 6))
    d = ((az_z - ak + 180) % 360) - 180; n = int(abs(d) // 36); sg = 1 if d > 0 else -1
    for i in range(1, n + 1):
        c = _polar(R_WAND / math.cos(math.radians(18)), ak + sg * (36 * i - 18)); pts.append((c[0], c[1], Z_BODEN + 5))
    w1 = _polar(R_WAND, az_z); pts.append((w1[0], w1[1], Z_BODEN + 2))
    pts.append((zq[0], zq[1], Z_BODEN)); pts.append((ziel[0], ziel[1], z_ziel))
    out = [tuple(pts[0])]
    for j, p in enumerate(pts[1:], 1):
        if math.dist(p, out[-1]) > (5.0 if j == len(pts) - 1 else 60.0): out.append(tuple(p))   # Zwischenpunkte unter 60 mm Abstand entfallen (kein Platz fuer einen Bogen)
    i = 1                                                          # gerade Zwischenpunkte entfernen (kein Bogen mit 0 Grad)
    while i < len(out) - 1:
        if dot(unit(sub(out[i], out[i - 1])), unit(sub(out[i + 1], out[i]))) > 0.99999: out.pop(i)
        else: i += 1
    return out


def schlaeuche():
    """[(name, soll_weg, idd, punkte)]"""
    ab = {a["name"]: a for a in TR.abnehmer()}
    sz = {1: PORTS["sumpf_zulaeufe"][0:3], 2: PORTS["sumpf_zulaeufe"][3:6]}
    out, zaehl = [], {1: 0, 2: 0}
    for n, a in sorted(ab.items()):
        cls = n.split(":")[0]; loc, dl = AUSLASS[cls]; m = MV[n]
        o_pt = world(m, loc); o_dir = unit(wdir(m, dl))
        if a["zone"] == "innen":                                   # e57: NFT Innen -> Fischtank: Schlauch vom Sammelrohr nach innen ueber den Rand, frei auslaufend ueber dem Spiegel
            r = math.hypot(o_pt[0], o_pt[1]); u = hz(mul(o_pt, -1))
            p1 = add(o_pt, o_dir, 60.0); p2 = add((p1[0], p1[1], o_pt[2] - 10), u, max(250.0, r - 1700.0))
            out.append((n, "e57", HOSE_ID, [o_pt, p1, p2, (p2[0], p2[1], FZ + 950.0)]))
            continue
        l = a["linie"]; zz = sz[l][zaehl[l] % 3]; zaehl[l] += 1
        out.append((n, SOLL_RUECK[(l, a["art"], a["zone"])], HOSE_ID, schlauch_weg_rueck(o_pt, o_dir, tuple(zz["port_mm"]), tuple(zz["richtung"]), zz["port_mm"][2])))
    eint = TR.leitungen_eintraege()[0]
    for t in eint["trassen"]:
        if t["id"].startswith("RB-H") and t["id"].endswith("-ab") and "ringende" in t["id"]:
            l = t["linie"]; p0 = tuple(t["pfad"][-1]); zz = sz[l][1]
            out.append((t["id"], "e33" if l == 1 else "e34", HOSE_ID, schlauch_weg_rueck(p0, (0.0, 0.0, -1.0), tuple(zz["port_mm"]), tuple(zz["richtung"]), zz["port_mm"][2])))
    return out


def radius(pts, idd):
    """groesster Biegeradius (Rb, Rb/2, Rb/4, Rb/8), mit dem der Weg als Schlauch aufgeht; kleiner als Rb ist ein Befund (Biegeradius nicht eingehalten)."""
    for f in (1, 2, 4, 8):
        try:
            AS.hose_layout([list(p) for p in pts], AS.hose_R(idd) / f); return AS.hose_R(idd) / f
        except ValueError:
            continue
    raise SystemExit("kein Schlauchweg")


def schlauch_soll_wege():
    out = {}
    for _, w, _, _ in schlaeuche(): out[w] = out.get(w, 0) + 1
    return out


def hochpunkte(pts, tol=0.5):
    """Zahl der Stellen, an denen der Schlauch gegen die Fliessrichtung steigt (Rueckläufe: kein Hochpunkt, Leitungsordnung v2)."""
    return sum(1 for i in range(len(pts) - 1) if pts[i + 1][2] > pts[i][2] + tol)


DATEI = "ring_ruecklauf"   # U7 (D141): Name ohne Variantenkuerzel


def bauen(out_sc=None):
    import sc
    b = sc.Build(); nm = "U6_Ring_B2_Ruecklauf"
    AS.mats(b, ["SCH schwarz"]); b.add("component.create", name=nm, grounded=True)
    laengen = []
    for i, (n, w, idd, pts) in enumerate(schlaeuche(), 1):
        Rb = AS.hose_R(idd); ad = AS.HOSE[idd]["ad"]
        Rb = radius(pts, idd)
        _, L, _ = TR.hose_einfach(b, "R%02d_%s" % (i, w), pts, Rb, ad, idd)
        laengen.append((n, w, round(L), Rb))
    b.add("solid.list", ) if False else None
    b.add("design.set_meta", name=nm, description="U6: Rueckläufe (Schlauch ID25) der Beete und Tische in den Sumpf der eigenen Linie, NFT Innen in den Fischtank, Ring-Ende in den Sumpf; Darstellungsgeometrie wie ring_schlauchwege (trassen_soll.py)") if False else None
    sc.run(b.write(DATEI), out_sc or TR.comp(DATEI))
    return laengen


def schreiben():
    p = os.path.join(ROOT, "data", "leitungstrassen.json")
    doc = json.load(open(p, encoding="utf-8"))
    doc["trassen"] = [e for e in doc["trassen"] if e.get("quelle") != QUELLE] + rohre()
    for key in ("trassen", "r_stuecke"):                         # Frischwasser K39 entfaellt (U6: Nachspeisung nach der Quelle S0-e17/e18/e19, D107; seit U7 geloescht); Stammloesung K52 ist kein Kreislauf-Weg
        doc[key] = [e for e in doc[key] if e["id"] != "K39"]
        for e in doc[key]:
            if e["id"] in ("K52", "KH_K52"):
                e["soll_bauteil"] = "puffer_klein"; e["soll_hinweis"] = "Messtechnik, begruendet behalten (D101), kein Weg der Quelle"
    json.dump(doc, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1); open(p, "a").write("\n")
    print("geschrieben:", len(rohre()), "Rohr-Trassen")


def bericht():
    from collections import Counter
    rs = rohre(); hs = schlaeuche()
    print("Rohre: %d (%s)" % (len(rs), dict(Counter(t["soll_weg"] for t in rs))))
    print("Schlaeuche: %d (%s)" % (len(hs), dict(Counter(w for _, w, _, _ in hs))))
    hp = [(n, hochpunkte(p)) for n, _, _, p in hs if hochpunkte(p)]
    print("Hochpunkte in Schlauch-Rücklaeufen:", sum(x for _, x in hp), hp[:5])


if __name__ == "__main__":
    if "--schreiben" in sys.argv: schreiben()
    if "--bauen" in sys.argv: print(bauen())
    if "--bericht" in sys.argv or len(sys.argv) == 1: bericht()
