# R51 — Beet-Siphon und Siphon-Schutz (Standardteile, Schutzkorb, Reinigungszugang)

**Art:** Recherche, Rechnung und Spezifikation, KEIN Bau, kein Modell-Umbau. Auftrag Ben 03.11.2026 (vorbereitend nur 100 % sichere, vom Wasserplan unabhängige Teile; Standardgeräte bevorzugen, Selbstbau nur wenn super simpel).

## Problem
Das Beet-Bauteil `ibc_beet` hat drei offene Kleinigkeiten (W40-BEET: Medienschutz-Löcher 12 mm gegen Korn ab 8 mm, Reinigungszugang zum Wasserraum unter dem Siebboden, Körnung) und einen Widerspruch zwischen Bauteil d25 und Netz d40 (L03). Der Siphon-Schutz ist heute 12 Durchbrüche 12 × 12 mm; ein kaufbares Standardteil oder ein Fertigsiphon ist nicht geprüft.

## Intent
Die Werkstatt soll später die empfohlenen Teile nachbauen und Ben die Teile einfach kaufen können; vorbereitend, ohne auf den Wasserkreislauf-Entscheid (E20/E21) oder den Subtank zu warten.

## Goal
Ein Bericht `docs/research/R51-beet-siphon-und-schutz.md` mit: (1) Funktion, Auslegung, Fehlerarten und Wartung des Glockensiphons, (2) mindestens drei realen Siphon-Produkten mit Maßen und Passung zu d25/d40/d50 samt L03-Lösung, (3) Siphon-Schutz (Kaufteile, Selbstbau, Lochmaß gegen Korn, Reinigungszugang, „super simpel“ ja/nein), (4) Bewertung Kaufteil/Selbstbau/Bestand, (5) Modellier-Spezifikation je Teil als Tabelle. Alles mit [Q]/[E]/[A] markiert.

## Eingaben gelesen
`docs/parts/ibc_beet.md`, `scripts/workshop/ibc_beet.py`, Roadmap W40-BEET und L03, R45 (Abschnitte 1 und 3), R47 (Abschnitt 4), `data/leitungsnetz.json` K11/K14/K30/K58, `data/layout.json`, `docs/decisions.md` (Beete), `docs/pitch-besonderheiten.md`.

## Stand (03.11.2026, Recherche-Sitzung)
- **Fertig:** `docs/research/R51-beet-siphon-und-schutz.md` und Rechenskript `scripts/r51_rechnung.py`; Zeile B12 im Pitch-Register. Kein Bau; `gen_dome.py`, `data/*`, Netzliste, Roadmap und Bauteile unverändert.
- **Ergebnis:** (1) Siphon d25/d75 behalten, aus Standardrohren, super simpel; kein Zukauf-Kit (US-Zoll, kein Durchsatz in den Datenblättern, 1″ zu groß). (2) L03: eine PVC-U-Reduktion kurz d40 × d25 unter dem Bulkhead, Einzelabgang d40, Sammler d50. (3) Schutz: Korb aus Edelstahl-Lochblech 1,5 mm Rundloch 5 mm (Halbzeug kaufen, rollen), deckt Korn 8–16 und ab 12 mm; Selbstbohren (168 Löcher je Schutz) nicht super simpel. (4) Reinigungsschacht d110 aus Rohr und Kappe plus Standrohr ziehen (Wasserraum leer in 11–16 min). (5) Spezifikationstabelle T30e-1 bis T30e-7.
- **Befunde an den Orchestrator:** (a) Wasserraum unter dem Siebboden bleibt dauernd gefüllt (Glocke steht auf dem Sieb): 6,4 m³ Zielstand; widerspricht B08 und der Aussage „leert bis zur Bodenplatte“ in R47. (b) Beetablauf Z −100 liegt über dem Bauteil-Rohrende (Z −192) und über dem Wannenboden (Z −157). (c) „Flutzeit 4–6 min“ in der Beauftragung ist die Entleerzeit; Flutzeit 28–71 min. (d) Blähton 10–20 / 12–20 mm ist nicht Handelsware (nur 8–16); dann Siebloch d6.
- **Grenzen der Belege:** Kein Hersteller nennt einen Durchsatz; Seiten von Aquifarm (Fetch gesperrt), Ofera, Perth Aquaponics und Go Green waren nicht lesbar (nur Suchausschnitt); Anspringen bei 3,3 l/min Zulauf, Lochblech-Korb und Zeitangaben für das Bohren sind nicht am Muster geprüft.
- **Offen:** Entscheidung Wasserraum (akzeptieren oder ändern) und Körnung; Netz/Port-Höhen abgleichen (Orchestrator/Montage); Werkstatt-Blatt nach W40-BEET aus der Spezifikation; Muster mit Zulauf 3,3 und 8,3 l/min testen.

## DoD
- [x] Bericht mit Antwort zuerst und fünf Abschnitten
- [x] Mindestens drei reale Produkte mit Quelle (fünf genannt, drei gelesen)
- [x] Spezifikationstabelle mit Maßen, Höhen, Ports, Gewicht, Beschaffbarkeit
- [x] Kein Umbau, keine Änderung an Roadmap/Netzliste/Bauteilen
- [x] Pitch-Eintrag B12
