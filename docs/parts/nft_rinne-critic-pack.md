# Kontextpaket Kritiker: nft_rinne (Werkstatt, 29.10.2026)

## 1. Scope-Card (aus `docs/scope-cards.md`)
- **DRIN:** EINE Rinne: Profil 130 x 100 mm (Laenge 1304 / 1983 / 3232), gerippte Oberseite, **EINE Lochreihe** in der Mittellinie (Lochabstand `pitch` = 250, Loch D52 fuer den Netztopf D50), Endkappen: Zulauf-Tuelle am einen, Ablaufstutzen am anderen Ende (Tuelle Wand 3 mm), Profil-Wandstaerke 2,5 mm.
- **DRAUSSEN (andere Klasse, NICHT als Luecke melden, sondern unter "Hinweis fuer andere Klasse"):** Nachbarrinnen und der Versatz benachbarter Rinnen (Zickzack) = Tisch; Beine, Querstreben, Halter, Zulaufverteiler, Schlaeuche, Gefaelle als Einbaulage (Rinne ist gerade, 0,573 Grad Neigung kommt im Tisch) = Tisch; Netztopf, Salatkopf = eigene Klassen.
- **Anzahl je Tisch:** 2 (innen) / 4 (Mitte) / 2-3 (aussen). Hierarchie: Ring > Tisch > Rinne > Topf > Salatkopf.

## 2. System in fuenf Zeilen
Geodaetische Aquaponik-Kuppel (12 m, 2V). Wasserweg: Pool -> Pumpe -> Vortex-Tank -> Biofilter-Tank -> Verteiler -> NFT-Rinnen (duenner Naehrloesungsfilm, Gefaelle 1 cm/m) und Substratbeete -> Schwerkraft-Ruecklauf zum Pool. Die Rinne bekommt Wasser an der Zulauf-Tuelle (hohes Ende), die Pflanzen stehen in Netztoepfen in den Topflochern, ueberschuessiges Wasser verlaesst die Rinne am Ablaufstutzen (tiefes Ende). Darueber: Tisch mit 2-4 parallelen Rinnen auf Beinen; darunter: Substratbeet.

## 3. Bilder (Ordner `renders/components/nft_rinne/critic/`)
- `k1-referenz-gesamt-markiert.png`: ref-6 mit roter Markierung des Tisches, aus dem der Ausschnitt stammt.
- `k2-referenz-ausschnitt-tisch.png`: Referenzausschnitt eines Tisches (mehrere Rinnen nebeneinander; der Zickzack der Pflanzen entsteht zwischen Nachbarrinnen: je Rinne EINE Reihe). Beurteile eine einzelne Rinne dieses Tisches.
- `k3-modell-ausschnitt.png`: unsere Einzelrinne, Nahaufnahme Oberseite (3 Salatkoepfe stecken in den ersten Loechern, Netztoepfe darunter verdeckt). Pflanzen dienen nur der Sitzpruefung.
- `k4-modell-gesamt.png`: die ganze Rinne 3232 mm. Weitere Nahaufnahmen: `nft_rinne-02-zulauf-ende.png`, `nft_rinne-03-ablauf-ende.png`, `nft_rinne-06-schnitt-zulauf.png`, `nft_rinne-07-querschnitt.png` (eine Ebene hoeher).

## 4. Messwerte (Vorpruefung `scripts/workshop/check_nft_rinne.py`, Ergebnis `renders/components/nft_rinne/check.txt`: 93/93 PASS)
Laenge 3232 / 1983 / 1304; Breite 130; Hoehe 100; Wand 2,5; Lochreihen 1 (y = 0), Loecher 12 / 7 / 5 (= Laenge/pitch abgerundet), Lochabstand 250, Loch D52; Zulauf-Tuelle D16 (Achse z 70), Ablauf D32 (Achse z 20); Masse Profil 3232 mm: ca. 5,3 kg (PVC-U 1,4 g/cm3, Annahme).

## 5. Soll
`data/layout.json` hydro_tables: Breite 129-130, Hoehe 102-103, Laenge 1304 / 1983 / 3232. Rippenmasse, Lochabstand und Wandstaerke sind Annahmen [A]; ref-6 gibt kein Mass.

## 6. Bekannte Fehlinterpretationen (`docs/review-lessons.md`)
- Zwei versetzte Lochreihen in EINER Rinne (falsch; Zickzack kommt aus dem Versatz benachbarter Rinnen).
- Mittelrippe in der Rinne (nicht in der Referenz).
- Pflanzen neben statt in den Topfloechern.

## 7. Frage und Antwortformat
Siehe `docs/review-protocol.md` Abschnitt 4: A oder B, hoechstens fuenf Luecken, je mit gross/klein, Bezug und Sicherheit (sicher/vermutet); fremde Klassen unter "Hinweis fuer andere Klasse".
