# Kontextpaket Kritiker: nft_tisch (Werkstatt, 29.10.2026)

## 1. Scope-Card (aus `docs/scope-cards.md`)
- **DRIN:** n Rinnen parallel (Abstand 262-288), **Versatz der Lochmuster benachbarter Rinnen um pitch/2 (Zickzack wie ref-6)**, Beine mit Querstreben, Diagonalen, Fussplatten, Zulaufverteiler mit n Schlauchanschluessen (hellblau, ein Schlauch je Rinne), Sammelablauf, Gefaelle, Rinnenhalter, Normschrauben.
- **DRAUSSEN:** Anordnung im Zehneck-Ring und Azimut (Integrator), Beete darunter, Pflanzen (Netztopf, Salatkopf: eigene Klassen), Rohrnetz (Integrator).
- **Anzahl:** innen 10 (2 Rinnen, Laenge 1304), Mitte 6 (4 Rinnen, 1983), aussen 8 (2-3 Rinnen, 3232).
- **Abweichung von der Card:** Gefaelle 1,5 % statt 1 cm/m nach Recherche R06 (Orchestrator-Vorgabe 29.10.).

## 2. System in fuenf Zeilen
Geodaetische Aquaponik-Kuppel (12 m). Drei Zehneck-Ringe von NFT-Tischen (innen ueber dem Pool, Mitte ueber den Innenbeeten, aussen ueber den Aussenbeeten), darunter Substratbeete. Wasser kommt ueber Verteiler und Schlaeuche an das hohe Ende jeder Rinne, fliesst mit 1,5 % Gefaelle zum tiefen Ende, dort ueber den Sammelablauf zurueck. Pflanzen (Netztopf + Salatkopf) stehen in den Topfloechern der Rinnen. Hierarchie: Ring > Tisch > Rinne > Topf > Salatkopf.

## 3. Bilder (Ordner `renders/components/nft_tisch_aussen/critic/` und `renders/components/nft_tisch_aussen/`)
- `critic/k1-referenz-gesamt-markiert.png`: ref-6 mit Markierung des Referenztisches (mittlerer Tisch).
- `critic/k2-referenz-ausschnitt-tisch.png`: Referenzausschnitt dieses Tisches (ein Tisch mit drei Rinnen, Zickzack der Pflanzen, Beine, Schlaeuche am rechten und linken Ende).
- `nft_tisch_aussen-01-iso.png`: unser Tisch aussen (3 Rinnen, 3 Boecke) als Ganzes; ohne Pflanzen (Pflanzen sind eigene Klassen).
- `nft_tisch_aussen-02-zulauf.png`, `-03-bock.png`, `-04-ablauf.png`, `-05-oberseite.png`: Nahaufnahmen Zulauf mit Verteiler und Schlaeuchen, Bock mit Diagonalen, Ablauf mit Sammelrohr, Oberseite mit Zickzack der Topfloecher. Dasselbe fuer Mitte und innen in `renders/components/nft_tisch_mitte/` und `nft_tisch_innen/`.

## 4. Messwerte (Vorpruefung `scripts/workshop/check_nft_tisch.py`, Ergebnis `renders/components/nft_tisch_aussen/check.txt`)
Rinnenzahl 2 / 4 / 3, Rinnenabstand 262 / 263 / 288, Zickzack-Versatz benachbarter Rinnen 125 (= pitch/2), Gefaelle 1,5 %, Hoehe Rinnenboden bei x=0: 840 / 1300 / 1300, Auflage Holm = Rinnenunterkante je Bock, Boecke 2 / 2 / 3, Diagonalen 2 je Bock, Verteiler-Stutzen und Sammelrohr-Muffen je Rinne; Masse Stahl: siehe `docs/parts/nft_tisch.md`.

## 5. Soll
`data/layout.json` hydro_tables (Laenge, Abstand, Z), `docs/components.md` (NFT-Ringe), Scope-Card. Alle Rahmenmasse (Rohr 30x30x2, Fussplatten, Halter, Verteiler) sind Annahmen [A], ref-6 gibt keine Masse.

## 6. Bekannte Fehlinterpretationen (`docs/review-lessons.md`)
Zickzack gehoert dem Tisch (hier gebaut: benachbarte Rinnen um pitch/2 versetzt); Pflanzen gehoeren nicht zum Tisch; Ringlage/Azimut gehoert nicht zum Tisch.

## 7. Frage und Antwortformat
Siehe `docs/review-protocol.md` Abschnitt 4: Referenz oder Modell, hoechstens fuenf Luecken, je gross/klein, Bezug, Sicherheit; fremde Klassen unter "Hinweis fuer andere Klasse".
