# Work package: M-BEET-TAUSCH die 14 Beete im Dom auf `ibc_beet` (V3 Sperrboden)

**Problem:** Der Dom (Build Runde 66) enthaelt die 14 Beete noch im Bauteilstand vor W40-BEET (Siebboden mit Wasserraum, Schlitz-Glocke); die Werkstatt hat `ibc_beet_{aussen_800,innen_933}.sc` auf V3 umgebaut, Pruefer PASS mit Auflagen (2dd81ff).
**Intent:** Modell und Messungen zeigen das Beet, das Ben gewaehlt hat (D77, Beet leert sich ganz); die Folgen (Gaenge, Kollision, Wasserbilanz) sind belegt.
**Goal:** Neuer Build Stufe 5 mit 8 `Beet_aussen_800` + 6 `Beet_innen_933`; `check_walkways` PASS auf den Runde-66-Werten; `check_latte` 0 echte Kollisionen (auch Netztopf x Reinigungsschacht); Viewer-Export neu; Bilanz-Folgen (6280 l) mit Eigentuemer benannt. Blatt: `docs/jobs/M-BEET-TAUSCH.md`.

## Plan

1. [x] Werkstatt-Vorlauf 0a: Bauteilblatt-Artikel Schachtrohr DN100 und Dichtband "nicht beschafft (Mass offen)" (Auflage 3)
2. [x] Werkstatt-Vorlauf 0b: Check-Text Standrohrflaeche 346 auf 380 mm2 / Schachtlaenge im Blatt (Auflage 4)
3. [x] Werkstatt-Vorlauf 0c: Schacht auf Topfraster-Zellmitte legen (Befund Netztopf x Schacht), Check-Zeile Abstand >= 87 mm
4. [x] Pruefung Auflage 5: Reduzierhuelse 22 mm und Flansch D50 gegen Datenblatt und Modell
5. [x] Montage: Neubau Runde 67 (Nummer aus `renders/` ablesen), `check_walkways`, `check_latte`, `check_walkways_voll`, Renders
6. [x] Montage: Viewer-Export (`viewer/export_model.py`), `loop-state.md`-Abschnitt
7. [ ] Pruefer: `docs/jobs/pruefung/M-BEET-TAUSCH.md` nach fuenf Pruefpunkten
8. [ ] Orchestrator: Bilanz-Dateien nachfuehren (Liste im Blatt, Schritt 3)

## Stand

04.11.2026 (Nacht), Planer (Sonnet 5.5): Blatt geschrieben. Aktualitaet: **angepasst**. Kernbefunde: (1) `t9()` setzt die Komponenten schon unter dem Namen `ibc_beet_aussen_800/innen_933`, der Tausch ist ein Neubau, kein Skript-Umbau; (2) Aussenmasse unveraendert, Erdtasche (200 mm unter Wanne) deckt die `Reduktion` bis Z -80, Gangwerte also erwartbar unveraendert; (3) **Netztoepfe liegen im Reinigungsschacht** (Gerechnet: 2 Toepfe je Aussenbeet, 1 bis 2 je Innenbeet, Abstand 76 / 36 mm gegen Soll 87; Groessenordnung 22 Kollisionen), Werkstatt-Check und Pruefer haben das nicht erfasst, weil Toepfe in `10_Pflanzen` liegen; Planer-Entscheidung: Schacht auf Zellmitte verschieben (Schritt 0c), Topfzahl 2222 bleibt. Nicht gebaut, nichts am Modell geaendert.

04.11.2026 (Werkstatt/Montage-Sitzung): **Schritt 0 fertig** (Commit b361159): 0a Artikelzeile Schachtrohr "Artikel nicht nachgewiesen" (KG-Rohr DN/OD 110, Ostendorf KG 2000 nur als Treffer), Dichtband "nicht beschafft (Mass offen)"; 0b Standrohr 25 x 1,5 (ID 22,0, 380 mm2, Bevo Art. 0309025), Check-Text zieht den Wert aus dem Parameter, `grep -c 346 check_ibc_beet.py` = 0; 0c Schacht auf Zellmitte des Topfrasters (Abstand Schachtachse zu jedem Topf 91,9 mm, Soll >= 87; x aussen_800 / innen_933 auf Rasterzelle nahe der alten Lage, y 65 bzw. 65), `check_ibc_beet.py` 194/194 PASS (190 + 4 Zeilen).

### Auflage 5 (Schritt 1, Ergebnis)
Quellen: Bevo-Katalogzeile Art. 7002656 und Georg-Fischer-Reduzierstueck 32 x 25 "Length 22 mm" (RS-Suchtreffer, Seite 403, nicht gelesen); Royal Brinkman, Epco, Pipestock, Bevo VDL 0100560 (Tankverbinder). **Kein Datenblatt gelesen** (Bevo-Datenblatt zu 7002656 nicht auffindbar; Tankverbinder-Flanschmass in keiner Quelle).
| Mass | Modell | Quelle | Ergebnis |
|---|---|---|---|
| Reduzierhuelse 32/25 Baulaenge | Platte 15 mm, Boden 39 mm | 22 mm (Bevo-Zeile, GF-Treffer: zwei Quellen, beide nur Katalogzeile) | Platte weicht um 7 mm ab, Boden um 17 mm (Modell Boden laenger): **ueber 3 mm**, aber nur Katalogzeile: Status "Datenblatt nicht gelesen, [A]", **kein Blocker** (1c) |
| Flansch D50 des Tankverbinders | D50 [A] | nicht gefunden (Royal Brinkman 32 x 1 1/2 Zoll: D 54, anderes Teil) | **offen, [A]** |
| Tankverbinder-Typ | 32 mm x 1 Zoll | VDL/Bevo fuehrt 32 mm x 1 1/4 Zoll (0100560); 32 x 1 Zoll nur UK (Epco, Pipestock) | **Risiko**: Bevo-Art. 7018227 gegen Katalog pruefen |
**DEINE ENTSCHEIDUNG/HANDLUNG (Ben oder N-BESCHAFFUNG):** Datenblaetter Tankverbinder (Flansch, Gewinde 1 Zoll oder 1 1/4 Zoll) und Reduzierhuelse beim Bevo-Kundendienst anfordern; bei Abweichung ueber 3 mm Nachbesserung `ibc_beet.py` (Huelsenlaengen).

04.11.2026 (Montage, Runde 67): **Schritt 2 fertig**, Details in `docs/loop-state.md` Abschnitt M-BEET-TAUSCH. Messwerte: Build Exit 0; 8 + 6 Beete, 2222 Netztoepfe; `check_walkways` unveraendert PASS; `check_walkways_voll` 60/82/2/4 unveraendert; `check_latte` 29/31 mit 115 KOLL nur Leitungsteile (nicht Beete), Netztopf x Schacht 91,9 mm gemessen (0 Verstoesse); Viewer-Export neu.
**Befund an die Werkstatt:** Medienschutz im Innenbeet (6 Beete): ein Netztopf sitzt 6,5 mm neben der Schutzachse, 5 mm Z-Luft (Kappe Z 800, Topfboden Z 805). Keine Kollision, aber unglaubwuerdig; Loesung wie 0c waere Siphon-x auf Zellmitte, beruehrt den Ablauf (E20), daher nicht still geaendert.
**Befund Orchestrator:** `check_latte` FAIL L6 (115 KOLL Leitungen M10, 71 Paare nicht vollstaendig geprueft) ist ein Leitungs-Thema, kein Beet-Thema; Salatkoepfe 2222 statt 2626 im Blatt.

OFFEN (E20, Entscheidung 05.11.): Ablaufleitungen K14/K30, Beet-Sumpf-Einlauf, Anschluss der `Reduktion` (offenes Ende bleibt). Nicht geplant.

## Definition of Done

Geprueft gegen: `docs/jobs/W40-BEET.md`, `docs/jobs/pruefung/W40-BEET.md`, `docs/packages/w40-beet.md`, `scripts/gen_dome.py` (Grep Beet-Stellen), `data/layout.json` `ibc_beds`, `docs/loop-state.md`, D77/D78, Python-Abstandsrechnung Topf/Schacht.
Offen:
1. Pruefer M-BEET-TAUSCH (Pruefpunkte 1 bis 5): Orchestrator.
2. Medienschutz x Netztopf innen_933 (6,5 mm, 5 mm Z-Luft): Werkstatt, Entscheidung wegen E20.
3. Datenblaetter Reduzierhuelse und Tankverbinder (Auflage 5): Ben/N-BESCHAFFUNG.
3. Bilanz-Dateien nachfuehren (6280 l, Gewichte): Orchestrator.
4. Ablaufleitungen und Beet-Sumpf: OFFEN (E20), Ben 05.11.
5. Dichtband-Mass, Metallbauer-Anfrage Schutzkorb, Datenblaetter: Ben.
