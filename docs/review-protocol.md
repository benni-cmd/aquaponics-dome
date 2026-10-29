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
