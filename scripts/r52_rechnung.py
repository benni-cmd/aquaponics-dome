"""R52: Gegenprobe der Europa-Tanks gegen tank_klein (Absetzer, 12,5 l/min Teilstrom). Aufruf: python -X utf8 -I scripts/r52_rechnung.py"""
import math

Q_LMIN = 12.5
Q_M3H = Q_LMIN * 60 / 1000

# (Name, Koerper-Durchmesser mm, Kegelwinkel Grad ab Horizontal oder None, Nennvolumen l)
tanks = [
    ("tank_klein (Bauteil T40)", 623.0, 48.7, 254.0),
    ("Enduramaxx 250 l 45 Grad", 609.0, 45.0, 250.0),
    ("CGK TCO3/L 300 l (Grundflaeche 695, Kegel unbekannt)", 695.0, None, 300.0),
    ("tanksdirekt.de 200 l (568, Kegel unbekannt)", 568.0, None, 200.0),
]
print(f"Teilstrom {Q_LMIN} l/min = {Q_M3H:.2f} m3/h")
for name, d, ang, vol in tanks:
    r = d / 2000.0
    a = math.pi * r * r
    beschickung = Q_M3H / a
    verweil = vol / Q_LMIN
    line = f"{name}: Flaeche {a:.3f} m2, Beschickung {beschickung:.2f} m/h, Verweilzeit {verweil:.1f} min"
    if ang:
        h_k = r * math.tan(math.radians(ang))
        v_k = math.pi * r * r * h_k / 3 * 1000
        h_z = (vol - v_k) / (a * 1000) * 1000
        line += f", Kegelhoehe {h_k*1000:.0f} mm, Kegelvolumen {v_k:.1f} l, Zylinderhoehe fuer Nennvolumen {h_z:.0f} mm"
    print(line)
# Enduramaxx Gesamthoehe 1257 gegen berechnete Hoehe bis Nennvolumen
r = 609 / 2000.0
a = math.pi * r * r
v_k = a * r * math.tan(math.radians(45)) / 3 * 1000
print(f"Enduramaxx: Hoehe bis 250 l = {r*1000 + (250 - v_k)/(a*1000)*1000:.0f} mm, Gesamthoehe 1257 mm -> Rest {1257 - (r*1000 + (250 - v_k)/(a*1000)*1000):.0f} mm")
print(f"tank_klein Hoehe Rand-Spitze 1075 mm; Enduramaxx +{1257-1075} mm")
# Heber-Reserve und Plattformkegel: Kegel 45 statt 48,7 Grad
for ang in (48.7, 45.0):
    print(f"Kegelhoehe Koerper-D623 bei {ang} Grad: {311.5*math.tan(math.radians(ang)):.0f} mm")
