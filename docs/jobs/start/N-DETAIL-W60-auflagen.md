# Start-Auftrag: Werkstatt/Viewer Auflagen Detailansicht W60 (A1 bis A4, A6)

PROJEKT: aquaponics-dome (user-projects/aquaponics-dome). Rolle: Werkstatt fuer Daten plus Viewer. Kontext mit Fenster 1.000.000 Token rechnen; ueber 35 % melden statt anfangen.

1. Grundlage: `docs/jobs/pruefung/N-DETAIL-W60.md` Abschnitt Auflagen (2206c26).
2. A1: `data/parts/feinfilter.json` und `tank_klein.json` bekommen `artikel_menge_je_instanz` wie die anderen 306 Dateien; Detailansicht zeigt dann Preis und Menge. A2: Viewer-Filter `klartext` um `[A]`-Marker, Pfade wie `data/beschaffung`, Register-Kuerzel (R42, W43) erweitern; Katalog-Bezeichnungen (`data/katalog.json` `artikel`) und "Einzelkoerper" mit Umlauten, Dezimalkomma in Anzeigetexten. A3: Teile mit Artikelverweis auf ein uebergeordnetes Kaufteil (z. B. Spindel, Hebel im `lt_kugelhahn_d63`) nicht als "ohne Preis" zaehlen. A4: `stand: geruest` und `geruest: true` bei den genannten 19 Dateien nachziehen, wo die Texte gefuellt sind; Menschfiguren bleiben bewusst Geruest. A6: Kopfzeile "Modell gespeichert - -" zeigt Zeit aus `instances.json`, wenn kein Export lief.
3. A5 (Strebe-Material) NICHT: das loest die neue Strebe (Sitzung werkstatt-strebe).
4. Parallel laufen fuenf Recherchen (nur `data/beschaffung/*.json`, `docs/session-notes/`) und `check_latte 69`. Nicht anfassen: `data/beschaffung/`, `designs/`, `scripts/components/`, `gen_dome.py`; kein Viewer-Vollexport.
5. Messen: `check_parts.py` ueber alle Komponenten (Exit 0 bis auf strebe_a/b), Anzeigetexte-Zaehlung mit Kuerzel/Pfad/[A] = 0 (Befehl daneben), Screenshot Feinfilter-Detailansicht mit Preis gegen `..\..\docs\ui-standard.md`. Paket `docs/packages/n-stueckliste.md` nachfuehren. Commits nur per Pfad, Push, WIP alle 20 Minuten. Danach STOPP.
