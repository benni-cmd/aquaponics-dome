# Paket: Umstieg SolidCraft 0.25.1 auf 0.30.1

**Problem:** Installiert ist SolidCraft 0.25.1; auf GitHub (`tangency-labs/solidcraft`) ist 0.30.1 die neueste stabile Version (02.11.2026), u. a. mit geschlossenem OBJ-Export gekrümmter Körper (#9213), 3D-Skizzen, Stücklisten-Typen und Sicherheitskorrekturen.
**Intent:** Neue Fähigkeiten und Fehlerkorrekturen nutzen, ohne das Modell zu beschädigen.
**Goal:** Gleiches Modell baut mit 0.30.1, gleiche Prüfergebnisse wie mit 0.25.1, keine neue Abweichung; dann Installation durch Ben.

## Plan
1. Portable 0.30.1 aus dem Release laden, SHA256 prüfen (Ben: "jo, umsteigen", 08.11.2026).
2. Repo-Kopie im Scratchpad, Skripte auf die portable CLI umgestellt, A+ Runde 77 bauen, `check_components`, `check_latte 77`.
3. Vergleich mit 0.25.1 (`renders/check_latte-77.txt`, Paket `n-verbinder.md` Punkt 6).
4. Ben installiert die MSI; danach alle Sitzungen auf 0.30.1. Kein Zurück: Ab 0.26 gespeicherte `.sc` öffnen nicht mehr in 0.25.1.

## Stand 08.11.2026 (Test in Kopie, Commit-Basis f4f0fb6)
| Prüfung | 0.25.1 | 0.30.1 |
|---|---|---|
| Bau A+ 5 77 (`sh scripts/build.sh 5 77`) | Exit 0, 11314 Befehle, 8:22 min | Exit 0, 11314 Befehle, 22:28 min |
| Snapshot `round-77.png` | Referenz | sichtbar gleich (909 x 766) |
| `check_components` | 4 PASS, 1 FAIL (14 statt 10 Baugruppen) | identisch |
| `check_latte 77` Score | 29/31 | 29/31 |
| L6 Kollisionen | 215 | 263 |
| L6 ungeprüfte Paare | 1186 | 298 |
| Dauer `check_latte` | 151 min | 128 min |
| Scheren x Sockel | 170 | 170 |

Deutung: 0.30.1 schneidet 888 Paare mehr exakt (ungeprüft 1186 -> 298); die 48 zusätzlichen Kollisionen stammen aus diesen bisher ungeprüften Paaren (Leitungsbögen, Wasserkörper), nicht aus geänderter Geometrie [A: Einzelliste der 263 nicht ausgegeben, Kategorien aus `.latte-cache.json`]. Bau 2,7-mal langsamer: Ursache offen (einmalig gemessen).
Betroffene API-Änderung `parameters.*`-Antworten (mm/Grad): Skripte lesen nur eigene `expression`-Werte, keine Antworten -> nicht betroffen (`grep parameters\. scripts/*.py`).

## DoD
- [x] Bau, Komponenten-Check, Latte mit 0.30.1 ohne neue Fehlschläge
- [ ] Ben installiert `solidcraft-0.30.1-windows-x64.msi`
- [ ] Bauzeit nach Installation erneut messen
- [ ] Erste Ring-B2-Runde mit 0.30.1 (Variante noch ungetestet)
