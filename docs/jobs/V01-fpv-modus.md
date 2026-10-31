# V01 FPV-Modus im Viewer (Ben 31.10., Side-Projekt, D48)
Problem: Ben will die Anlage als 1,80 m grosse Person durchlaufen, um Platz und Wege zu fuehlen. Der Viewer hat nur die Orbit-Kamera.
Intent: Schnelles Gefuehl fuer Masse und Laufwege, super simpel.
Ziel: Ein Knopf `FPV` in den Viewer-Steuerelementen; Klick = FPV-Modus: gesamte UI ausgeblendet (linke Spalte, Infopanel, Schnitt-Regler, alles) ausser EINEM Knopf `X` (oben rechts) zum Beenden; man laeuft in Augenhoehe 1,68 m (Person 1,80 m) durch die Kuppel.
Datei: nur `viewer/index.html` (three.js 0.160, Szene, Kamera, Sichtbarkeitslogik darin; per Grep `OrbitControls`, `camera`, `visible`, `hidden`/`toggle` finden, nur diese Bereiche lesen). Einheiten des Modells (mm oder m) aus dem Code ermitteln.
Verhalten:
1. Eingabe: WASD und Pfeiltasten gehen/drehen (Pfeil links/rechts drehen, Pfeil hoch/runter vor/zurueck), Maus: Pointer Lock beim Klick auf die Szene (Fallback: Ziehen mit der Maus dreht), Shift = 3x schneller, Gehgeschwindigkeit 1,4 m/s. Kein Springen, keine Kollisionen, Hoehe fest (Bodenhoehe aus dem Modell, Augen = Boden + 1,68 m). Q/E optional drehen. Blick nur horizontal drehen plus Neigen +-80 Grad.
2. Start: ausserhalb vor der Tuer (Azimut 149,2 Grad im Layout-KS, Abstand ca. 8 m vom Mittelpunkt, Blick zur Tuer; Achse: Tuer im Viewer anhand der Instanz `tuer_komplett` finden), damit man auf die Tuer zugeht.
3. Sichtbarkeit: Der Sichtbarkeitszustand aus der Liste (Bauteile ausgeblendet/eingeblendet) gilt im FPV unveraendert. Ist die Tuer (tuer_komplett, tuer, zarge, Beschlaege) ausgeblendet, fehlt sie auch im FPV und man kann hereinlaufen. Hover/Klick-Leuchten und Overlays im FPV aus.
4. Kamera: PerspectiveCamera FOV 75, near 0,05 m, far gross genug; beim Beenden (X-Knopf oder Esc) Orbit-Kamera, UI, Auswahl und Schnitt exakt wie vorher, Pointer Lock loesen.
5. Kein Autoupdate-Reload waehrend FPV, der Modell-Neuladen-Hinweis darf die Position nicht zuruecksetzen (Kamera behalten).
Pruefen im Browser-Pane (http://localhost:4410/): Knopf klicken, `read_page`/Screenshot: nur `X` sichtbar, per Tastatur-Ereignisse (javascript_tool `dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW'}))`) Kamera bewegt sich, Position/Hoehe auslesen (Augen 1,68 m), X beendet, UI zurueck; Tuer ausgeblendet -> im FPV nicht sichtbar. Konsole ohne Fehler (read_console_messages). Pointer Lock geht im Pane evtl. nicht: Fallback testen.
Nicht anfassen: alles ausser `viewer/index.html`; kein Server-Neustart noetig.
Commit nur mit Pfad: `git -C C:\Users\benkn\Claude\keel-harness\user-projects\aquaponics-dome commit -m "Viewer: FPV-Modus" -- viewer/index.html`, push. Fertig = Knopf, Bewegung, Beenden, Tuer-Sichtbarkeit nachgewiesen; Kurzmeldung (Geprueft gegen / Offen), dann sauber enden.
