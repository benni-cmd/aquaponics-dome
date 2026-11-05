# N-PREIS-PRUEF Schritt 2 Werkstatt: Notiz (05.11.2026)

Rolle Werkstatt: nur Skripte ausgefuehrt, keine Recherche. Befehle und Zahlen stehen im Paket `docs/packages/n-preis-pruef.md`.

## Messlauf nach 1A bis 1E
Befehl: `python -X utf8 scripts/check_links.py` (273 Zeilen, 168 mit Link, 289 Links, 241 URLs).
- FEHLER: 0 (vorher 6).
- GESPERRT: 13 (vorher 32).
- VERDACHT: 87 (vorher 127).
- OK: 189 (vorher 124).

## Platzierte Zeilen, Hauptangebot (Rang 1) nicht OK: 26
Messung: `python -c` ueber `data/preis_pruefung_links.json` `link_liste`, `rang == "1"`, platziert nach `data/stueckliste.json` (`nicht_platziert` leer). Ergebnis: 67 OK, 22 VERDACHT, 4 GESPERRT, 0 FEHLER. Gruppe B Leitung hat 0.
VERDACHT heisst "Kennmass fehlt in Titel/URL" oder Bemerkung ERSATZ, ist also ein Filter und kein Urteil. Die Fachrecherche hat alle bis auf eine Zeile in ihrer Gruppen-Notiz.

### A Stahl, `stahl.json`: 15 VERDACHT (alle in der Notiz stahl)
1. BLE-blech-st-3 (Bemerkung NICHT 3)
2. BLE-fussplatte-100x100x6, BLE-fussplatte-70x70x5, BLE-fussplatte-80x80x6
3. BLE-platte-250x250x15
4. BLE-pp-blende-290x260, BLE-pp-tafel-502x345x5, BLE-pp-tafel-693x463x7
5. BLE-v2a-3mm-korbflansch, BLE-v2a-lochblech-medienschutz
6. PRF-pvcu-rinne-130x100 (Mass 130 nicht auf der Seite; Kabelkanal ist weg, Pruefpunkt 2 vom Pruefer messen)
7. PRF-st-rr40x40x2.5 (Bemerkung Ersatz)
8. WNK-flach-14x3, WNK-rinnenhalter-25, WNK-winkel-36x60x60

### C Behaelter, `behaelter.json`: 2 VERDACHT (in der Notiz behaelter)
1. BEH-drittbecken-klein
2. BEH-fass-hdpe

### D Mess und Elektrik, `mess_elektrik.json`: 4 GESPERRT (HTTP 403), 3 VERDACHT
1. GESPERRT, in der Notiz mess: MES-do-mini, MES-ec, MES-ph
2. **GESPERRT, NEU (nicht in der Notiz mess): ELE-schaltschrank-500x800x1200** — Hauptangebot HTTP 403, von Hand lesen. Pruefer: Stichprobe.
3. VERDACHT, in der Notiz mess: MES-leck, MES-level-float, MES-temp-ds

### E Huelle, `huelle_pflanze.json`: 2 VERDACHT (in der Notiz huelle)
1. FOL-epdm-dichtung-630x440
2. SON-tuerblatt-1000x2000

## Neue Artikel ohne Angebot (Folge der neuen Modellteile, nicht der Recherche)
`beet_sumpf` und `schlammfass` (W37-1) bringen neue Artikel-IDs ohne Eintrag in `data/beschaffung/*.json`: BEH-pe-schachtaufsatz-600x200, PMP-teichpumpe-5300, ARM-rsv-d40, MES-schwimmerschalter, FIT-entlueftung-d32, ELE-kabelverschraubung-m25, ARM-bulkhead-d50 und weitere. Beide Komponenten haben 0 Instanzen im Modell (nicht platziert). Die Recherche legt sie an, sobald die Komponenten platziert sind.

## Fehlerbehebung check_bom.py
Erster Lauf: Exit 1, 3 FAIL (Pruefungen 2, 5, 8). Ursache und Behebung stehen im Paket.
