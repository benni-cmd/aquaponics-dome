# Paket W33 — Tischhoehe 1000 mm fuer alle Ringe (Werkstatt, Auftrag docs/jobs/W33-tischhoehe-1000.md, R35, D60)

## PIG
- **Problem:** Die NFT-Tische stehen auf Rinnenunterkante 1300 mm (Mitte, Aussen) und 840 mm (Innen), uebernommen aus dem OBJ ohne Begruendung. R35 zeigt: 1300 ist fuer 1,55-1,75 m zu hoch (Topfebene ueber Schulter), 840 fuer 1,75-1,90 m zu niedrig, die aeusserste Rinne liegt nur 21 mm von der Kuppelhaut.
- **Intent:** eine ergonomisch begruendete Hoehe (R35, Ben: R35 entscheidet), gleich fuer alle drei Ringe: weniger Stahl, mehr Abstand zur Haut, ein Wert statt zwei.
- **Goal:** `z_rinne_mitte` = 1000 in allen vier Typen (innen, mitte, aussen, aussen3); Tische neu gebaut, `check_nft_tisch.py` und `check_nft_fit.py` gruen, `data/nft_pots.json` neu, Bauteilblatt und `descriptions.json` mit R35-Herkunft, ein Render Seitenansicht mit Figur 1,80 m.

## Plan (ein WIP-Commit je Schritt)
1. Parameter und Geometrie: `z_rinne_mitte` 1000 in `nft_tisch.json`; Querstrebe `strut_z` pruefen (Diagonalenwinkel, Pflanzenhoehe); Beinlaenge und Knicklast neu rechnen; Tische bauen (`nft_tisch.py`).
2. Checks: `check_nft_tisch.py` (alle drei Typen), `check_nft_fit.py` (aussen, aussen3), Topfliste neu (`extract_nft_pots.py` nur ausfuehren, nicht aendern).
3. Blatt: `docs/parts/nft_tisch.md` (Herkunft R35, Ellbogenwerte), `data/descriptions.json` (Masse), Render Seitenansicht mit Figur 1,80 m.

## Hinweis Beetzugang (R35 Befund 6)
Tischunterkante = Rinne - Holm (Modell: 60 mm, R35 rechnete mit 50) = 940 mm; Beetrand Z 475: 465 mm Luft. Das Beet unter dem Tisch ist nur an den Kanten erreichbar (Unterarme). Entscheidung zu den Beeten (Weg 1/2) liegt bei Ben/Orchestrator, nicht in diesem Paket.

## Stand
31.10.: Tische neu gebaut (innen/mitte/aussen, 1000 mm), check_nft_tisch 204/204, check_nft_fit 50/50 (aussen3 49/49), Kuppelhaut-Abstand 121 mm, nft_pots 674, Blatt und descriptions nachgefuehrt, Bild `renders/components/nft_tisch_mitte/nft_tisch_mitte-07-hoehe-quer.png` und `-laengs.png` (Figur 1,80 m; archiviert). Eigene Annahme: Querstrebe Z 650 statt 800 (Diagonalen 12,5-15,5 Grad). Offen: Montage baut Tische neu; Beete-Weg 1/2 und strut_z bei Ben/Orchestrator; Statik der kuerzeren Beine.

## DoD
Checks gruen (Zahlen im Stand), Topfliste neu, Blatt und descriptions nachgefuehrt, Render im Bildverlauf, WIP-Commits gepusht, `docs/workshop-state.md` und `docs/workshop-log.md` nachgefuehrt.
