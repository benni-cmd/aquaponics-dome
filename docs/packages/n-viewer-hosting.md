# N-VIEWER-HOSTING: Viewer auf Vercel hosten

Stand 05.11.2026, Viewer-Werkstatt. Status: statische Ausgabe gebaut und lokal geprüft; Deployment wartet auf Bens Login.

## PIG
- **Problem:** Der Kuppel-Viewer läuft nur lokal über `viewer/serve.py` auf Bens PC. Ben und Leon können das Modell unterwegs nicht ansehen, und der Export ist 1.325 MB groß.
- **Intent:** Ben und Leon sehen das Modell mit allen Anzeige-Funktionen von überall, ohne dass der PC läuft.
- **Goal:** `viewer/dist/` läuft ohne `serve.py` auf einem statischen Server und ist unter `aquaponics-dome-viewer` auf Vercel erreichbar, mit Zugangsschutz, wenn der Tarif ihn kann.

## Grenzen (je zwei Quellen, gelesen 05.11.2026)
| Frage | Befund | Quellen |
|---|---|---|
| Vercel Größe statisch | Tabelle "Static File uploads": Hobby 100 MB, Pro 1 GB (Text: bei CLI-Deploy Quelldateien). Der Changelog vom 17.06.2026 "CLI deployment limits removed" sagt, CLI-spezifische Grenzen seien entfallen; die Doku-Tabelle wurde nicht angepasst. **Widerspruch, ungeklärt bis zum echten Deploy.** Dateianzahl bei CLI-Quelldateien 15.000. | vercel.com/docs/limits.md (Zeilen 65, 97-99, 149); vercel.com/changelog/cli-deployment-limits-removed.md |
| Vercel Zugangsschutz | Vercel Authentication ("All Deployments", schützt auch die Produktionsadresse) ist seit 09.09.2026 auf **jedem Tarif kostenlos**; Besucher melden sich mit einem Vercel-Konto an, das Zugriff auf das Projekt hat. Passwortschutz: **nicht auf Hobby**, Pro 20 $ je Projekt und Monat. | vercel.com/docs/deployment-protection.md (Zeilen 54-62); vercel.com/changelog/protect-production-deployments-for-free-on-every-plan.md |
| Folge für Leon | Auf Hobby gibt es nur ein Konto je Team; Leon hätte kein Konto mit Projektzugriff. Mit Vercel Authentication braucht Leon ein Mitglied-Konto im Team (Pro) oder Bens Konto. **Entscheidung für Ben.** | wie oben (Hobby-Plan-Hinweis nicht eigens geprüft: [A]) |
| GitHub Pages (Rückfall) | Veröffentlichte Seite höchstens 1 GB; 100 MB je Datei (Git-Grenze); Soft-Bandbreite 100 GB/Monat. Privat nur mit bezahltem Tarif. | docs.github.com Pages-Grenzen (Suchtreffer); Zweitquelle nur Drittartikel [A] |
| Cloudflare Pages (Rückfall) | 25 MiB je Datei, 20.000 Dateien je Seite (kostenlos). Unsere größte Datei 2,9 MB, 1.472 Dateien: passt. Zugangsschutz über Cloudflare Access. | developers.cloudflare.com/pages/platform/limits; Zweitquelle Drittartikel [A] |

## Messung (Befehle daneben)
| Größe | Wert | Befehl |
|---|---|---|
| Quelle `viewer/defs` | 601 MB | `du -sh viewer/defs` |
| Quelle `viewer/detail` | 667 MB | `du -sh viewer/detail` |
| OBJ-Dateien roh (833 Stück) | 1.324,7 MB | `python -X utf8 scripts/viewer_dist.py` (Zeile "OBJ-Dateien") |
| OBJ gzip -9, Koordinaten 0,01 mm | 168,8 MB (Faktor 7,8) | dasselbe |
| `viewer/dist` gesamt | 169 MB, 1.472 Dateien, größte Datei 2,9 MB | `du -sm viewer/dist; find viewer/dist -type f \| wc -l` |
| Bauzeit | 69 s | `time python -X utf8 scripts/viewer_dist.py` |

**Bewertung:** 169 MB liegt unter der Pro-Grenze (1 GB) und über der Hobby-Tabellengrenze (100 MB). Ob die Tabellengrenze noch gilt, zeigt nur der Deploy-Versuch. Fällt Hobby aus, gibt es zwei Wege: (a) Cloudflare Pages (kein Gesamtlimit, Datei 2,9 MB < 25 MiB) oder (b) ein binäres Format mit Quantisierung, das nach Schätzung etwa 2- bis 3-fach kleiner wird (nicht gebaut, nicht gemessen).

## Plan und Umsetzung
1. Grenzen recherchieren: erledigt (Tabelle oben).
2. `scripts/viewer_dist.py`: wandelt OBJ in kompaktes OBJ-gzip (Koordinaten 0,01 mm, Normalen 0,001), kopiert JSON-Daten, schreibt `statik.json` und `vercel.json` (noindex). Gleiche Eingabe gibt gleiche Bytes (`mtime=0`). Wahl gegen GLB/Meshopt: kein Bibliotheks-Zugriff offline, der Viewer-Ladeweg (`OBJLoader`) bleibt unverändert, Gewinn gemessen 7,8-fach.
3. `viewer/index.html`: erkennt den statischen Modus an `<meta name="viewer-modus" content="statisch">` (nur in `dist/index.html`). Dann gilt: `fetch` bildet `.obj` auf `.obj.gz` ab (Entpacken per `DecompressionStream`), Varianten-Dateien auf feste Namen, `/api/*` entfällt; Status-Zeile, Auto-Update, Board und Bildverlauf sind ausgeblendet; Ring B2 ist nur sichtbar, wenn exportiert. Im Live-Betrieb mit `serve.py` ändert sich nichts.
4. Lokaler Test mit `python -m http.server 4425` in `viewer/dist`.
5. Deployment: `vercel whoami`, dann `vercel deploy --prod` im Ordner `viewer/dist` als Projekt `aquaponics-dome-viewer`; Zugangsschutz "All Deployments".

## Stand
- Lokal geprüft (Browser-Pane, 05.11.2026): Modell lädt (296 Definitionen, 0 Fehler, 12 s), Kleinteile (113 Dateien nachgeladen), Messstellen (rosa Marker sichtbar), Ansicht Visuell/Technisch, Detailansicht `aktivkohle_station` mit Einkauf (140,46 €), keine Konsolenfehler. Stil: Sätze statt Fragmente, nichts Neues ausser der Statuszeile.
- Variantenschalter: **Ring B2 ist nicht exportiert** (`viewer/varianten/` fehlt), deshalb zeigt die statische Ausgabe nur A+ und blendet den Schalter aus. Der Schalter-Code ist über `statik.json` vorbereitet, aber mit Ring B2 nicht getestet.
- Deployment: `vercel whoami` meldet "Logged out". Ben muss `vercel login` ausführen.

## DoD
- [x] Paket mit PIG, Plan, DoD
- [x] Grenzen mit je zwei Quellen (zwei Zweitquellen für GitHub und Cloudflare sind Drittartikel: [A])
- [x] `scripts/viewer_dist.py` baut `viewer/dist/` reproduzierbar
- [x] Größen vorher und nachher mit Befehl
- [x] Lokal getestet mit Screenshot
- [ ] Ring B2 in der statischen Ausgabe geprüft (wartet auf Export)
- [ ] Deployment (wartet auf Login und Entscheidung zum Tarif)
