# Start-Auftrag: Montage Scherenknoten und Rundrohr-Streben (D91)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle Montage, einzige Sitzung, die das Gesamtmodell baut. Pflicht: `docs/designprinzipien.md` abhaken. Kontext ueber 35 % melden statt anfangen. RAM nur messen (D89).

1. Grundlage: `docs/jobs/N-VERBINDER.md` (Bauteil knoten_schere, Doppelplatte c901314, Pruefer a1ed36b plus Auflagen), `docs/research/R56-scherenknoten.md`, Entscheidung D91 (eine 6-Loch-Platte fuer alle Knoten, Streben Rundrohr 42,4 x 2,6, Laschen 8 mm).
2. Werkstatt-Anteil zuerst, falls noetig: Laschen auf 8 mm und Strebe als Rundrohr 42,4 x 2,6 (scripts/components/strebe.py parametrisch, Werkstoff Stahl verzinkt, Teiledaten, Bauteilblatt); Strebenlaenge so, dass Rohrende und Schere passen (r56_scherenknoten.py).
3. Montage: Kugelknoten im Modell durch Instanzen von knoten_schere ersetzen (je Knoten eine Platte, so viele Scheren wie Streben, Drehung je Schere), Streben einsetzen; beide Varianten bauen (A+ bzw. Zielbild-Basis dome.sc und dome-ring_b2.sc ueber die Varianten-Weiche); check_walkways, check_huelle (Folie auf Strebenebene!), check_latte in Kopie, Viewer-Export.
4. Paket `docs/packages/n-verbinder.md` (anlegen falls fehlt) und loop-state nachfuehren, Bilder. Commits nur per Pfad, Push, WIP alle 20 Minuten. Danach STOPP mit Kurzmeldung.
