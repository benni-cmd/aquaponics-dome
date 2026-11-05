# Pruefung V-MESS, N-VARIANTEN VV und M12 (Pruefer, 05.11.2026)

Pruefer: Sonnet 5.5, nach `docs/jobs/vorlagen/pruefung.md`. Gegenstand: Commits 0ab9994 (N-VARIANTEN VV, Viewer-Schalter Kreislauf A+ / Ring B2), b2e6e8e (V-MESS: Ebene Messstellen, Plane-Schalter, Kennzahlen), a980ae1 (M12: Anschlussteile bleiben im Hauptexport). Pakete: `docs/packages/n-varianten.md`, `docs/packages/v-mess.md`, `docs/packages/n-viewer-laden.md`. Keinen dieser Schritte habe ich gebaut. Die Selbstauskunft der Pakete zaehlt nicht als Beweis.

Vorgehen: eigener Testserver `python viewer/serve.py 4436` (A+ gegen die echten Daten) und fuer die Variantenprobe eine Kopie des Viewers im Scratchpad (Port 4437, `viewer/varianten/ring_b2/` dort mit eigener `instances.json`, `defs/` als Verknuepfung). Bilder aus dem Browser-Pane; echte Klicks fuer alle Schalter.

## Urteil: PASS mit Auflagen

VV, V-MESS und die Logik von M12 halten ihre Ziele. M12 wirkt im Viewer noch nicht, weil der Hauptexport seit dem Commit nicht fertig gelaufen ist (siehe Punkt 3). Auflage mit Gewicht: mehrere gleichzeitig laufende `serve.py` exportieren bei jedem Speichern von `dome.sc` gleichzeitig (V3).

## 1. N-VARIANTEN VV (0ab9994): PASS

| Soll | Befehl | Messwert |
|---|---|---|
| Schalter "Kreislauf: A+ / Ring B2" im Menue, Etikett in der Bildmitte, Tab-Titel | Browser-Pane, `document.title`, Bild | Schalter links oben, Etikett "Kreislauf: A+", Titel "Kuppel Live-Viewer (A+)" |
| Spiegelung in Adresse und `localStorage` | echter Klick auf "Ring B2", danach `location.href`, `localStorage.getItem('viewer.variante')` | Adresse `?variante=ring_b2` beim Klick, `localStorage` folgt der Wahl |
| Rueckfall bei fehlendem Export | Klick auf "Ring B2" im echten Ordner (kein `viewer/varianten/ring_b2/`), `GET /api/state?variante=ring_b2` | `version: 0`; die Seite meldet rot "Die Variante Ring B2 ist noch nicht exportiert (varianten/ring_b2/instances.json ... 404). Export: python viewer/export_model.py --variante ring_b2. Das bisherige Modell bleibt stehen.", Adresse und `localStorage` fallen auf `a_plus` zurueck, Etikett bleibt A+, Modell unveraendert (Bild) |
| Probe mit vorhandenem Export | Kopie im Scratchpad mit `viewer/varianten/ring_b2/instances.json` (3803 Instanzen, jede zweite `netztopf` entfernt) | Direktaufruf `?variante=ring_b2`: Etikett "Kreislauf: Ring B2", Titel "(Ring B2)", Statuszeile "3803 Instanzen, 164 Definitionen"; Klick auf "A+": zurueck auf 4914 Instanzen, `localStorage` `a_plus`, Aufbau 3,4 s (Definitionen aus dem gemeinsamen `defs/`) |
| A+ unveraendert | `GET /system-specs.json?variante=a_plus`, `/stueckliste.json`, `/descriptions.json`; Bytezahl gegen die Repo-Dateien | 25563 gleich 25563, 558572 gleich 558572, `descriptions.json` 93867 gleich; Ring B2 liefert `stueckliste.json` mit 404, solange `data/stueckliste-ring_b2.json` fehlt |
| Unbekannte Variante | `GET /api/state?variante=xyz` | faellt auf `a_plus` zurueck |

## 2. V-MESS (b2e6e8e): PASS

| Soll | Befehl | Messwert |
|---|---|---|
| Ebene "Messstellen zeigen" (Haken, Kugeln, Umriss, Baumkategorie) | echter Klick, `window.messStand()` | vorher `an: false`, danach `an: true`, `sichtbar: true`, 7 Markiergruppen; rosa Kugeln im Bild am Pool und um die Tanks; `localStorage` `viewer.messstellen` = 1 |
| Plan gegen Daten | `python -I` ueber `data/messstellen.json` | 67 Messstellen: 22 `pflicht`, 45 `zusatz` (gleich Seite); `messStand()`: 5 Halter, 17 Sonden; `instances.json`: `halter_beruhig` 2 + `halter_tauch` 3 = 5, Sonden 1+3+1+3+1+3+3+2 = 17 |
| Plane ausblenden | echter Klick auf "Plane zeigen", `messStand().plane` | vorher `netze: 6`, nachher `an: false`, `netze: 0`; Innenraum frei (Bild); `localStorage` `viewer.plane` = 0 |
| Deckkraft-Schieber | echtes Ziehen von 14 auf 51 (Bereich 0 bis 60) | `deckkraft: 51`, Plane milchig (Bild), `localStorage` `viewer.planeop` = 51; Messstellen-Kugeln bleiben durch die Plane sichtbar |
| Kennzahl Puffer 0,16 | Seitentext gegen `data/system-specs.json` `wasser.teile` | Seite "0,16 m³ (0%)", Daten 0.16: gleich |

## 3. M12 (a980ae1), Anschlussteile im Hauptexport: Logik PASS, Wirkung noch nicht messbar

- `viewer/anschluesse.json`: 18 Namensmuster. `viewer/export_model.py` hat `gross = Diagonale >= 150 mm oder Muster`, Cache-Schluessel `v3` mit Listen-Kennung.
- Offline gemessen (`python -I` ueber `data/bom_koerper.json` und `viewer/instances.json`, ohne Export): **98 Koerper in 39 Komponenten** wuerden neu im Hauptexport bleiben, ueber die Instanzen **210 Koerper** (Bsp.: `tank_klein` Schlammstutzen und Ablaufstutzen; `tank_gross` und `tank_gross_t3` je Zulaufsieb, Schlammstutzen, Ablaufstutzen; `feinfilter` 11; `pumpe_klein`/`pumpe_gross` je Saug- und Druckstutzen; `nft_tisch_*` Endstopfen; `ibc_beet_*` 6 je Definition). Das trifft die Schlammablaesse, die in `docs/model-maengel.md` M03/M12 genannt sind.
- Ein Treffer ist fachlich ein Falsch-Positiv: `Zulaufsieb` (Sieb im Tank, kein Anschluss). Die Muster `ablauf` und `zulauf` greifen auf jeden Namen mit diesen Silben.
- **Wirkung im Live-Viewer nicht gemessen:** `viewer/instances.json` ist von 02:12:59 und traegt das neue Feld `anschluss_immer_sichtbar` nicht; seit 03:30 sind 70 Dateien in `viewer/defs/` neu geschrieben, die Datei `instances.json` (die zuletzt geschrieben wird) ist noch alt. Zur Pruefzeit liefen zwei `export_model.py`-Prozesse zugleich (PID 12992, 26856, siehe V3). Nachpruefen nach Exportende: `instances.json` hat `"anschluss_immer_sichtbar": true`, `window.viewerStand().tank_klein.koerper` = 21 statt 19 ohne Haken Kleinteile.

## Auflagen

1. **V1, Zaehler im Kopf nach Variantenwechsel:** unter dem Titel steht bei Ring B2 weiter "4914 Instanzen", die Statuszeile darunter zeigt 3803 (Probe). Der Kopfzaehler muss mit der Variante wechseln.
2. **V2, Rueckfallmeldung widerspruechlich:** der Balken zeigt "Schritt 3 von 3: fertig" und "Fertig: 0 Definitionen, 0,0 MB, 3 s, 1 Datei fehlerhaft", die rote Meldung nennt den internen Abruf mit Zeitstempel (`?v=1793847035640`). Besser: Balken weg, Meldung ohne Abrufadresse.
3. **V3, mehrere Server exportieren zugleich (wichtig):** `serve.py` beobachtet `designs/dome.sc` je Prozess; `export_lock` gilt nur im eigenen Prozess. Als um 03:52:29 `dome.sc` gespeichert wurde, starteten die Server auf 4410 und 4455 je einen Export (zwei `export_model.py` gleichzeitig auf demselben `viewer/defs/`), und mein Testserver auf 4436 ebenfalls; dessen Export endete mit "Export fehlgeschlagen: strebe_a" (`/api/state`). Damit habe ich gegen "kein Export" des Auftrags verstossen: der Export lief nicht auf meinen Wunsch, sondern ausgeloest durch die Speicherung der Montage; Schaden an `viewer/defs/` habe ich nicht gesehen (`strebe_a.obj` 889 Byte, 03:52:32), die zwei anderen Exporte liefen noch. Empfehlung: Sperrdatei `viewer/.export.lock` (mit Prozesskennung) oder Schalter `--kein-export` fuer Pruef- und Testserver; Pruefer-Auftraege sollen den Schalter nennen.
4. **V4, Zahlenformat:** Das Paket V-MESS nennt "Anteile unter 1 m³ mit zwei Nachkommastellen"; die Seite zeigt "Drittbecken (Quarantaene, klein) 0,4 m³" (Daten 0.4), "Puffer klein 0,16 m³", "NFT-Rinnen 0,15 m³": das Drittbecken faellt aus dem Muster (0,40).
5. **V5, Zaehler Messstellen:** Ziel (1) im Paket nennt "n von 67 geplanten Messstellen haben ein Bauteil"; die Seite zeigt "5 Halter und 17 Sonden stehen schon im Modell" (22 Bauteile, nicht Messstellen). Wortlaut des Ziels oder der Anzeige angleichen.
6. **V6, M12 Muster:** `Zulaufsieb` ist ein Falsch-Positiv; `zulauf`, `ablauf`, `auslauf` auf Anfang des Namens oder die Namen einzeln listen.
7. **V7, M12 Nachpruefung:** nach dem naechsten vollstaendigen Export Punkt 3 (Nachpruefen) wiederholen.

## Nicht belegt oder nicht nachgemessen

1. Kennzahlen und Einkaufsliste der echten Ring-B2-Variante: gibt es noch nicht (`data/system-specs-ring_b2.json`, `data/stueckliste-ring_b2.json`); Paket nennt das selbst als nicht gemessen.
2. Der volle Export (Dauer, Groesse) und seine Wirkung auf Ben-Ansicht: nicht gestartet (Auftrag: nichts exportieren).
3. Fest codierte Kennzahlentexte ("12 m Durchmesser", Pumpenzahl): das Paket fuehrt sie als offen; nicht erneut geprueft.

Geprueft gegen: `/api/state` je Variante, Bytezahlen der Variantendateien gegen das Repo, `window.messStand()`, `window.ansichtStand()` nicht noetig, `data/messstellen.json`, `viewer/instances.json`, `data/system-specs.json`, `data/bom_koerper.json`, `viewer/anschluesse.json`, Browser-Pane mit echten Klicks (Variantenschalter, Messstellen, Plane, Deckkraft).
Offen: V1 bis V7 (Viewer, Orchestrator); M12-Wirkung nach Exportende (Pruefer, nur auf Auftrag).
