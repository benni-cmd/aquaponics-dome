# Herkunft und Auslegung der Quellen (verbindlich ab 29.10.2026 04:05)

Ben: Jede Komponente wird sauber gebaut, immer mit Bezug auf die Bilder UND die Dateien; die Wahrheit steckt darin, muss aber ausgelegt werden, weil die Dateien teils unvollstaendig und alt sind.

## Was jede Quelle liefert und was nicht

| Quelle | Verlaesslich fuer | Luecken / Vorsicht |
|---|---|---|
| `Project_Oasis_Layout.obj` (via `data/layout.json`, `reference/oasis-obj-analysis.md`) | Anzahl, Lage, Hauptmasse der Klassen, die es enthaelt (Streben, Knoten, Beete, Tanks, Plattformen, Fittings, Pool, Rinnen-Beispiele) | alt und unvollstaendig: je NFT-Ring nur ein Beispiel; Rinnen ohne Toepfe; keine Schlaeuche/Rohre, keine Haut, keine Tuer; Details grob oder anders als die Bilder |
| Bilder `ref-4` (Haupt, Layout), `ref-5`, `ref-6`, `ref-2/3` | Aussehen, Anordnung, Details, die das OBJ nicht hat (Schlaeuche, Pflanzenbesatz, Rinnenoberseite, Zickzack, Haut) | Perspektive, kein Mass; Beleuchtung; manche Bauteile falsch (Ben: z. B. NFT-Rohre aussen nur zwei) |
| Bens Aussagen | alles, was er sagt (12 m/6 m, Boden Erde, Pool eingelassen) | nur was ausdruecklich gesagt wurde |
| Recherche (`docs/research/R*.md`) | Fachregeln, Masse von Normteilen, Konstruktionsprinzipien | je Wert Konfidenz beachten, Zweitquellen |
| `docs/hydraulics.md`, `docs/components.md`, `docs/scope-cards.md` | abgeleitete Festlegungen (mit Marken Q/E/A) | Annahmen sind Platzhalter |

## Rangfolge bei Widerspruch

Ben-Aussage > OBJ-Zahl (Anzahl/Lage/Mass) > Recherche mit Konfidenz mittel/hoch > Bild (Aussehen, Anordnung, Details) > Annahme. Bei Aussehen und fehlenden Teilen gewinnt das Bild vor dem OBJ, wo das OBJ nur ein Beispiel oder nichts hat.

## Auslegung bei Luecken (Pflicht)

Fehlt ein Merkmal oder ist es widerspruechlich: (1) im Bild nachsehen (Ausschnitt notieren), (2) im OBJ nachsehen (Gruppe/Name), (3) Fachregel/Recherche pruefen, (4) wenn nichts eindeutig ist, die plausibelste Auslegung waehlen und als **Annahme `A`** mit Grund markieren, (5) in `docs/review-lessons.md` oder `docs/decisions.md` festhalten, wenn die Auslegung eine Klasse betrifft. Nie raten ohne Markierung.

## Herkunftstabelle je Bauteilblatt (Pflicht, Abschnitt "Herkunft")

Jedes `docs/parts/<klasse>.md` enthaelt eine Tabelle: **Merkmal | Wert | Herkunft | Bezug | Konfidenz**.
Herkunft: `OBJ` (Gruppe, Datei `layout.json` Feld), `Bild` (Datei und Ausschnitt, z. B. ref-6 oben links), `R<NN>` (Recherche), `Ben`, `E` (eigene Rechnung mit Formel), `A` (Annahme mit Grund). Beispiel Rinne: Profil 130 x 100 | OBJ `hydro_tables` | Konfidenz hoch; EINE Lochreihe | Bild ref-6, Scope-Card | hoch; Lochabstand 150 mm | Bild ref-6 (geschaetzt aus 3 Reihen je Tisch) | niedrig, A. Merkmale ohne Herkunftseintrag gelten als Fehler (Spec-Pruefer meldet sie).

## Sichtbarer Stand

Der Stand je Klasse steht im Board `docs/integration-board.md` (Besitzer Orchestrator) und live im Viewer (`http://localhost:4410/`, Feld "Bauteil-Stand"). Jede Sitzung pflegt ausserdem ihre eigene sichtbare Aufgabenliste (`update_plan`) so, dass sie dem Stand entspricht (erledigte Schritte abgehakt, genau ein Schritt in Arbeit).
