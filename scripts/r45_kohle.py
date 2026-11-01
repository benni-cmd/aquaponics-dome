"""R45 Frage 5: Aktivkohle im Frischwasser (K39-K43, K52). Kontaktzeit, Bettvolumen, Tageslaufzeit, Last.

Aufruf: python -X utf8 scripts/r45_kohle.py   (reine Rechnung)
"""
import math

FT3_L = 28.317
GPM_L = 3.785
DI25 = 0.022      # m, PVC-U d25 x 1,5
print("== Kontaktzeit (EBCT) = Bettvolumen / Durchfluss ==")
print(f"Herstellerangabe katalytische Kohle 1,0 ft3 bis 3,75 gpm Chloramin: EBCT {FT3_L/(3.75*GPM_L):.1f} min (purewaterproducts.com Chloramine Catcher)")
for bett_l in (21, 42):
    for q in (2, 4, 10):
        print(f"Bett {bett_l} l bei {q:2d} l/min: EBCT {bett_l/q:5.1f} min")

print("\n== benoetigtes Bett fuer Ziel-EBCT ==")
for ebct in (1, 3, 5, 10):
    print(f"EBCT {ebct:2d} min: " + ", ".join(f"{q} l/min -> {ebct*q:3d} l" for q in (2, 4, 10)))

print("\n== Tagesbedarf und Laufzeit ==")
tag_l = 680.0  # 2 %/Tag von 34 m3? Netz: 0,68 m3/Tag
for q in (2, 4, 10):
    print(f"Nachspeisung {tag_l:.0f} l/Tag bei {q} l/min: {tag_l/q/60:.1f} h/Tag Laufzeit")
print("Quarantaene-Wasserwechsel 2 l/min nach Bedarf (Becken 0,4 m3)")

print("\n== Last und Rohr ==")
for c in (0.5, 2.0, 4.0):
    print(f"Chloramin {c} mg/l: {tag_l*c/1000:.2f} g/Tag, {tag_l*c/1000*365/1000:.2f} kg/Jahr (als Cl2)")
for q in (4, 10):
    print(f"d25 (Innen-Ø 22 mm) bei {q} l/min: {q/60000/(math.pi*DI25**2/4):.2f} m/s")
print(f"Ammoniak-Eintrag aus Chloramin 2 mg/l (als Cl2, NH2Cl -> NH3 1:1 molar, N = 14/71 von Cl2): {tag_l*2/1000*14/71:.2f} g N/Tag gegen 130 g TAN/Tag")
