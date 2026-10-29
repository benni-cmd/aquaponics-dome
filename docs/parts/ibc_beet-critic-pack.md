# Kontextpaket Kritiker: ibc_beet (Werkstatt, 29.10.2026)

## 1. Scope-Card (aus `docs/scope-cards.md`)
- **DRIN:** Wanne (halbe IBC, Wandstaerke 3-4 mm), Medium (EIN Koerper, Oberflaeche Z 400, Tiefe 300 mm), Siebboden, Standrohr D25, Glocke D75 x 250, Medienschutz D110 x 320, Ablauf-Fitting im Beetboden, Zulaufrohr quer (Z 450). Quelle R03.
- **DRAUSSEN:** Pflanzen (Netztopf + Salatkopf als Instanzen aus layout.json, 288 je Aussenbeet), NFT-Tische darueber, Rohrnetz.
- **Anzahl:** 8 aussen (2953 x 933-993 x 637), 6 innen (1865 x 933 x 649); eingelassen (Unterkante Z -160...-210).
- **Fehlinterpretation:** Pflanzen als Teil der Wanne bauen; Medium als Einzelkoerner.

## 2. System in fuenf Zeilen
Geodaetische Aquaponik-Kuppel (12 m). 14 Substratbeete (8 aussen, 6 innen) aus halben IBC-Wannen stehen eingelassen im Boden unter den NFT-Tischen. Wasser kommt ueber das Tropfrohr zu, der Glockensiphon laesst das Beet periodisch fluten und entleeren; Pflanzen in Netztoepfen wachsen im Medium (Blaehton/Kies). Ablauf per Schwerkraft durch den Boden zum Sammelrohr. Hierarchie: Beet > (Medium, Siphon, Topf-Instanzen).

## 3. Bilder (`renders/components/ibc_beet_aussen_933/critic/` und `renders/components/ibc_beet_aussen_933/`)
- `critic/k1-referenz-gesamt-markiert.png`: ref-5 mit roter Markierung des Referenzbeets (links vorn).
- `critic/k2b-referenz-ausschnitt-beet-ref5.png` und `k2-referenz-ausschnitt-beet-ref6.png`: Referenzausschnitte weisser Beet-Wannen mit Erde/Pflanzen (die Pflanzen gehoeren NICHT zur Klasse).
- `ibc_beet_aussen_933-01-iso.png`: unser Beet als Ganzes; `-02-siphon.png` Glockensiphon im Medium; `-03-zulauf.png` Zulaufdurchfuehrung; `-04-medium.png` Medienoberflaeche; `-05-schnitt.png` Laengsschnitt (Wasserraum, Siebboden, Medium, Siphon); `-06-schnitt-quer.png` Querschnitt.

## 4. Messwerte (`scripts/workshop/check_ibc_beet.py`, `renders/components/ibc_beet_aussen_933/check.txt`: 66/66 PASS)
Aussenmass 2953 x 933 (und 993) x 637 bzw. 1865 x 933 x 649 (Abweichung 0), Wand 4, Boden 5, Medium 1 Koerper 300 mm tief mit Oberflaeche 75 mm unter dem Rand (absolut Z 400), Siebboden 5 mm unter dem Medium, Standrohr D25 (220 ueber Medienunterkante), Glocke D75 x 250, Medienschutz D110 x 320 (20 mm ueber der Medienoberflaeche), Zulaufrohr D20 auf Z 450 absolut.

## 5. Soll
`data/layout.json` ibc_beds, `docs/research/R03.md`, Scope-Card. Rand, Eckenradius, Bulkhead, Siebboden-Raster, Stuetzen und Wasserraum unter dem Medium sind Annahmen [A].

## 6. Bekannte Fehlinterpretationen
Pflanzen und Netztoepfe gehoeren nicht zum Beet (Instanzen). Quadratische Seitenloecher/Tropfloecher sind eine bewusste Vereinfachung (Rechenzeit). Im OBJ ist nur die Huelle der Wanne modelliert; der Innenaufbau stammt aus R03.

## 7. Frage und Antwortformat
Siehe `docs/review-protocol.md` Abschnitt 4: Referenz oder Modell, hoechstens fuenf Luecken, je gross/klein, Bezug, Sicherheit; fremde Klassen unter "Hinweis fuer andere Klasse".
