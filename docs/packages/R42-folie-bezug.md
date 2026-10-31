# Arbeitspaket R42: Plane — kaufbare Folie, Lieferform, Machbarkeit des Schnittmusters

**Problem:** R38 empfiehlt V2 (20 Rautenkissen) auf einer 8-m-Rolle, stuetzt sich aber nur auf einen Haendler fuer 8 m; Folienart, Zertifizierung und Lieferform sind offen (Ben, D69).
**Intent:** Der Bauplan soll auf realen, standardisierten Teilen stehen: eine kaufbare UV-bestaendige Gewaechshausfolie mit Normnachweis, bekannte Lieferform, Schnittmuster auf den echten Rollenbreiten.
**Goal:** `docs/research/R42.md` mit Hauptfolie und Ersatzfolie, Lieferformen, Machbarkeit je Variante und Rollenbreite, Naht-Beleg oder ausgewiesene Luecke, Einkaufsliste; `scripts/plane_nesting.py` und `data/plane-zuschnitt.json` auf reale Breiten umgestellt, Selbsttest behalten; R38 verweist auf R42. Modell unveraendert.

## Plan

1. [x] Auftrag, D69, R24, R38 gelesen
2. [x] Web: Hersteller/Haendler, Breiten, Preise, EN 13206, Konfektion, Naht
3. [x] Skript: reale Rollenbreiten je Produkt, Bahnen hintereinander, Breitentabelle, Produkttabelle
4. [x] R42.md schreiben, R38 verweisen
5. [x] Committen mit Pfad, pushen

## Status

31.10.2026 — Hauptfolie Folitec Folisol clear AF 200 µm (Ersatz AGRIplus UV5 200 µm); V2 auf 7,5 m Rolle 38,2 m je Lage, 16,7 % Verschnitt, 287,9 m Naht, 20 Kissen; Selbsttest 19/19. Naht fuer 200-µm-PE ist als Luecke ausgewiesen.

## Definition of Done

Geprueft gegen: Lauf `python scripts/plane_nesting.py --json --svg` (Selbsttest 19/19), Sichtpruefung nesting-v2.svg, Webseiten folitec.de, stretchfolie.eu, dm-folien.com, norhage.de (Volltext)
Offen:
1. Preis, Mindestmenge, Schweisseignung bei Folitec anfragen (Entwurf in R42.md) — DEINE HANDLUNG (Ben)
2. Probeschweissung 200-µm-PE — DEINE HANDLUNG (Ben)
3. Modell: Folie 0,2 mm, Schienen 65 → 45 — Werkstatt/Montage nach Entscheidung
