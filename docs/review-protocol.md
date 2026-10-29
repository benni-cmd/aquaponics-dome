# Pruefprotokoll gegen Fehlinterpretation (verbindlich ab 29.10.2026 04:00)

Anlass (Ben, 29.10.): Der Kritiker bemaengelte an der EINZELNEN NFT-Rinne "fehlende versetzte Lochreihen", die Werkstatt baute zwei versetzte Reihen ein. In der Referenz hat aber jede Rinne nur EINE Lochreihe; der Zickzack entsteht, weil benachbarte Rinnen eines Tisches gegeneinander um den halben Topfabstand versetzt sind. Das ist Sache des Tisches, nicht der Rinne. Ursachen: (1) der Referenzausschnitt zeigte mehrere Rinnen, das Bauteil war eine; (2) die Zustaendigkeit (Rinne / Tisch / Ring) war nicht festgehalten; (3) die Kritik wurde ungeprueft umgesetzt.

## 1. Scope-Card VOR dem Bau (Spec-Gate)

Jede Bauteilklasse hat eine Scope-Card in `docs/scope-cards.md`: was ist DRIN, was ist DRAUSSEN (gehoert zu einer anderen Klasse), Anzahl je uebergeordnetem Teil, Masse mit Quelle, Referenzausschnitt, typische Fehlinterpretation, Pruefzahlen. Die Werkstatt baut erst, wenn die Card steht; aendert sie die Card, schreibt sie den Grund hinein und meldet es dem Orchestrator. Der Orchestrator liest die Card vor dem Bau (Spec-Gate).

## 2. Hierarchie und Zustaendigkeit

Ein Merkmal gehoert genau EINER Klasse. Regeln: Merkmale, die erst durch das Zusammenspiel mehrerer gleicher Teile entstehen (Versatz, Abstand, Zickzack, Ringschluss), gehoeren zur uebergeordneten Klasse (Tisch, Ring, Baugruppe). Merkmale, die jedes Einzelteil selbst hat (Profil, Rippen, Lochreihe, Stutzen), gehoeren zur Einzelklasse. Hierarchie: Ring > Tisch > Rinne > (Topf > Salatkopf); Beet > (Medium, Siphon, Topf-Instanzen); Tank > Plattform > Beine.

## 3. Referenzausschnitt passend zum Bauteil

Der Ausschnitt fuer den Kritiker zeigt genau diese Klasse im gleichen Massstab: bei der Rinne EINE Rinne mit eingezeichnetem Rahmen (aus ref-6 beschnitten), nicht den ganzen Tisch. Ist kein sauberer Ausschnitt moeglich, bekommt der Kritiker den Tisch und den Auftrag, nur die markierte Rinne zu beurteilen. Der Bauer schreibt in den Auftrag an den Kritiker die Scope-Card (DRIN/DRAUSSEN).

## 4. Kritiker-Auftrag (Vorlage)

```
Du bist ein strenger Kritiker mit frischem Kontext. Beurteile NUR die Klasse <Name>. Scope-Card: <DRIN ... / DRAUSSEN ...>.
Bild A und Bild B (zufaellig benannt) zeigen Referenz und Modell. Welches zeigt die Klasse genauer in Form, Proportionen, Anzahl
und Details? Rendering-Stil ignorieren. Antworte mit A oder B und hoechstens fuenf Luecken, nach Groesse sortiert, je mit
"gross" oder "klein". Zu JEDER Luecke: Bezug (Zeile der Scope-Card, Zahl aus layout.json/components.md oder sichtbarer Bildbereich)
und Sicherheit (sicher/vermutet). Merkmale, die zu einer anderen Klasse gehoeren oder erst mehrere Teile zusammen ergeben, nicht
als Luecke melden, sondern unter "Hinweis fuer andere Klasse".
```

## 5. Luecken-Triage durch den Bauer (Pflicht, bevor etwas geaendert wird)

Fuer jede gemeldete Luecke: (a) Bezug im Modell/Spec/OBJ/Referenz selbst nachpruefen, (b) einstufen: **gueltig** / **falsch gelesen** / **andere Klasse** / **unklar**, (c) mit Beleg in `docs/workshop-log.md` eintragen (Luecke, Einstufung, Beleg), (d) nur gueltige beheben; "andere Klasse" an die Scope-Card dieser Klasse weiterreichen, "unklar" beim Orchestrator melden. Ohne Triage-Eintrag zaehlt die Runde nicht.

## 6. Pruefung durch den Orchestrator

Der Orchestrator prueft bei der Abnahme: stimmt die Scope-Card mit `data/layout.json`/`components.md` und der Referenz, steht fuer jede umgesetzte Luecke eine Triage, passt das Ergebnis zur Hierarchie (Versatz beim Tisch, nicht bei der Rinne). Findet er einen Fehler, geht die Klasse mit EINER Zeile Mangel zurueck.

## 7. Zahlen-Gegenprobe

Zu jeder Klasse gehoeren Pruefzahlen aus `layout.json` (Anzahl je Eltern, Masse, Abstaende). Der Pruefskript der Klasse stellt sie fest (z. B. Rinne: Lochreihen = 1; Tisch: Versatz benachbarter Rinnen = Topfabstand/2, Rinnenzahl und Abstand wie Ring).

## 8. Kontextpaket fuer den Kritiker (neu 29.10. 04:00, nach Bens Hinweis: "dem Kritiker fehlt vielleicht Kontext")

Der Bauer legt vor jedem Kritikerlauf `docs/parts/<klasse>-critic-pack.md` an und gibt es dem Kritiker mit. Inhalt:
1. **Scope-Card** der Klasse (DRIN / DRAUSSEN, Stelle in der Hierarchie, Anzahl je Eltern) aus `docs/scope-cards.md`.
2. **Systemueberblick in fuenf Zeilen:** geodaetische Aquaponik-Kuppel, Wasserweg, Rolle dieser Klasse darin, was darueber und darunter haengt.
3. **Vier Bilder:** (a) Referenz Gesamtansicht `ref-4` mit eingezeichneter Stelle der Klasse, (b) Referenzausschnitt NUR der Einzelklasse (Rahmen), (c) Modell-Render im gleichen Ausschnitt, (d) Modell-Render im Elternkontext (z. B. Rinne im Tisch). A/B weiterhin ohne Beschriftung und zufaellig benannt.
4. **Messwerte aus dem Modell** (Ausgabe des Vorpruefskripts, siehe 9): Masse, Anzahl Loecher/Reihen/Abstaende, Ports, Wandstaerken.
5. **Soll** aus `data/layout.json`, `docs/components.md`, `docs/scope-cards.md`.
6. **Bekannte Fehlinterpretationen** aus `docs/review-lessons.md`.
7. Frage und Antwortformat aus Abschnitt 4.

## 9. Maschinelle Vorpruefung (Zahlen) VOR jedem Kritiker

Je Klasse ein Pruefskript `scripts/workshop/check_<klasse>.py`, das am gespeicherten `.sc` misst (`solidcraft-cli`, z. B. Bounding-Box, `component.properties`, Anzahl Loecher und Reihen, Port-Positionen) und mit der Scope-Card vergleicht (PASS/FAIL mit Ist und Soll). Der Kritiker laeuft nur bei PASS. Beispiele: Rinne Lochreihen = 1, Loecher = Laenge/pitch, Profil 130 x 100; Tisch Versatz benachbarter Rinnen = pitch/2; Tank Kegel vorhanden, Fitting an Kegelspitze; Beet Medienoberflaeche Z 400.

## 10. Zwei Pruefer statt einem

- **Bild-Kritiker** (Aussehen, Abschnitt 4 mit Kontextpaket).
- **Spec-Pruefer** (kein Bild, nur Zahlen und Text): ein zweiter frischer Agent liest Scope-Card, Hierarchie und die Messwerte und nennt Widersprueche (z. B. Merkmal gehoert zu anderer Klasse, Zahl weicht vom OBJ ab, Anzahl falsch). Er hat die Hierarchie als Pflichtfrage: "Gehoert jedes Merkmal in dieser Klasse hierher oder in die Eltern- oder Kindklasse?"
Beide Ergebnisse gehen durch die Triage (Abschnitt 5).

## 11. Lernprotokoll

Jeder gefundene Fehler kommt in `docs/review-lessons.md` (Datum, Klasse, was schiefging, Ursache, neue Regel). Der Bauer fuegt "Bekannte Fehlinterpretationen" daraus ins Kontextpaket ein. Der Orchestrator ergaenzt die Datei bei Abnahme-Funden.
