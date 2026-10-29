# Paket W16 — NFT-Tische: Passung an den Zehneck-Ecken, Beine ausserhalb der Beete (Werkstatt, Auftrag docs/jobs/W16-nft-tisch-passung.md, D18)

## PIG
- **Problem:** Rinnen laenger als die Zehneck-Seite ihrer Reihe (innen 1733: 1126 gegen 1304; 1995: 1296; mitte 2987: 1941 gegen 1983; aussen 4888: 3176 gegen 3232) -> Tische kollidieren an den Ecken; Tischbeine (Abstand ~600 mm) stehen in den Beeten (Breite 933/993).
- **Intent:** real baubare Tische; Beete duerfen sich aendern, Tische folgen ueber Parameter.
- **Goal:** `check_nft_fit.py` PASS fuer alle 24 Tische (Footprints benachbarter Tische je Ring >= `corner_gap` 100 mm Abstand; Beinpunkte ausserhalb jedes Beet-Rechtecks + `leg_clearance` 60; Bein-Pool-Abstand), Bild-Kritiker Ecke und Beet-Querschnitt, Spec-Pruefer, Blatt-Nachtrag.

## Plan (Entwurf 29.10. 16:10, Annahmen A)
1. Geometrie je Reihe: Tisch-KS X = Rinnenachse (tangential), Y = radial nach AUSSEN (ap = ap_c + y); Reihen y_k = (k-(n-1)/2)*rp; Zehneck-Seite s_k = 2*ap_k*tan 18 Grad. Tischmitte ap_c: innen 1864 (Mittel OBJ-Reihen 1733/1995, E), mitte 3381 (Mittel 2987/3248/3514/3775, E), aussen 5176 (Reihen 4888/5176/5464: 4888/5176 OBJ, 5464 = 3. Rinne Ben/A, ap_c ~ Beetmitte 5188-5276).
2. Rinnenlaenge je Reihe: L_k = 2*(ap_k*tan18 - corner_gap) - E_in - E_out; E_in 169 (Tuelle 29 + Schlauch 70 + Stutzen 45 + Verteilerrohr D25), E_out 79 (Stutzen 34 + Sammelrohr D50); Rinne um (E_in - E_out)/2 = +45 mm nach +X verschoben; n_holes = floor(L/250); Zickzack-Versatz pitch/2 bleibt (shift +-62,5).
3. Zulaufverteiler und Sammelrohr laufen SCHRAEG (+-18 Grad) entlang der Sektorgrenze, damit jede Reihe mit eigener Laenge gleichen Abstand zur Grenze hat; Schlauchlaenge je Reihe gleich (70).
4. Mitte/Aussen: Portalbock, 2 Beine ausserhalb des Beets bei y = +-(bed_outer_w/2 + leg_clearance + leg_w/2) (bed_outer_w aus `data/components/ibc_beet.json` typen breite), Querholm 60x40x3 (A, Biegung 50 kg mittig auf 1,2 m: ca. 15 % der Streckgrenze), Querstrebe und Diagonalen UEBER der Pflanzen (strut_z 800, Beet-OK 475, Pflanzen bis ~560), Laengsstreben auf strut_z.
5. Innen (ueber dem Pool, Wasserradius 1945): ein Ausleger-Pfosten je Bock AUSSERHALB des Beckenrands (Rand Z 650), Kragarm ueber das Wasser mit Diagonalstuetze; Fussplatte M10 auf Fundament.
6. Neue Rinnenvarianten je Reihe (9 Dateien) aus `nft_rinne.sc` (`len_l`, `n_holes`, `shift`).
7. `check_nft_fit.py`, Render Draufsicht Ecke + Querschnitt Beet/Tisch, Spec-Pruefer, Bild-Kritiker, Blatt-Nachtrag, Fertigmeldung `docs/session-notes/orchestrator.md`.

## Stand
- 16:10 Entwurf; noch nichts gebaut. Folge fuer den Orchestrator: Rinnen werden kuerzer (innen 678/848, mitte 1493-2005, aussen 2728-3103) -> weniger Toepfe als im OBJ; Zahlen kommen aus `check_nft_fit.py`.

## DoD
check_nft_fit PASS, check_nft_tisch angepasst PASS, 3 Tischdateien + 9 Rinnenvarianten, Bilder im Bildverlauf, Spec-Pruefer ohne gueltigen Befund, Blatt-Nachtrag, Fertigmeldung.
