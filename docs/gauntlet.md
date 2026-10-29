# Gauntlet-Loop fuer dieses Projekt (hohe Messlatte)

## Kurzfassung (nach der Vorlage des Skills; GILT ZUERST, der Rest unten ist Anhang)

```
Baue ein parametrisches SolidCraft-Modell der Aquaponik-Kuppel (12 m, 2V-Halbkugel), das aussieht wie die Referenz und technisch stimmt: Wasserkreislauf, wiederkehrende Bauteile als Komponenten mit Instanzen.

Die Messlatte sind Bens Blender-Renders `reference/ref-4` bis `ref-6` und das OBJ-Layout `data/layout.json`. Hol sie dir und vergleiche direkt damit, nicht mit einer Beschreibung davon. Die messbare Haelfte sind `check_fidelity.py` und `check_hydraulics.py`.

Teile die Arbeit in die kleinsten Stuecke, die einzeln verbessert und beurteilt werden koennen. Pro Stueck: ein Bauer und ein getrennter Kritiker mit frischem Kontext. Der Kritiker oeffnet das echte Ergebnis, legt es ohne Beschriftung neben die Referenz, sagt welches die Anlage genauer zeigt und nennt die eine groesste Luecke. Dann zurueck zum Bauer.

Der Kritiker ist hart. Lob ist nicht nuetzlich. Gewinnt unser Stueck nicht, geht es weiter.

/loop pro Stueck, bis der Kritiker unseres waehlt. Nicht vorher aufhoeren. Nur Bens "stopp" beendet.

Nur ein Agent zur Zeit wegen des gemeinsamen Limits.
```

Offen und ungeprueft (29.10.2026): kein Kritiker ist bisher gelaufen; die Abweichungen vom Skill (Zahlengrenzen, ein Agent zur Zeit, nicht streng blind) stehen im Anhang.

## Anhang: ausfuehrliches Protokoll (meine Zutaten, nicht Teil des Skills)

Technik: Matt Shumer, Skill: robonuggets/gauntlet-loop (`.claude/skills/gauntlet-loop/`, siehe `SOURCE.md` dort). Kern: eine **echte Messlatte** (benannt, abrufbar, vergleichbar), kleine einzeln beurteilbare Stuecke, je Stueck ein **Bauer** und ein **getrennter, strenger Kritiker mit frischem Kontext**, der blind vergleicht und EINE Entscheidung trifft (nie eine Note), Schleife bis der Kritiker "ours" waehlt. Kein Ende nach fester Rundenzahl; nur Bens "stopp" beendet.

## Unsere Messlatte (drei Teile, alle muessen halten)

1. **Bild-Latte (Aussehen und Form):** `reference/ref-4-dome-clean.jpg`, `ref-5-dome-closeup.jpg`, `ref-6-grow-tables-detail.jpg` (Blender-Renders von Ben, das Ziel). Benannt, im Repo abrufbar, gleiche Kamera erzeugbar.
2. **Zahlen-Latte (Wahrheit):** `data/layout.json` aus dem OBJ (Anzahl, Maße, Lage) plus `docs/hydraulics.md` (Wasserkreislauf). Geprueft von `scripts/check_fidelity.py` und `scripts/check_hydraulics.py`.
3. **Foto-Latte (Endziel):** ControlNet-Foto-Render des Modells gegen `ref-4`: der Kritiker kann nicht zuverlaessig den Originalrender nennen.

## Hohe Latte, messbar

Ein Stueck gilt als bestanden, wenn gleichzeitig:
- `check_latte.py`, `check_hydraulics.py`: alles PASS; `check_fidelity.py`: Anzahl exakt, mittlere Lageabweichung <= 50 mm, Maßabweichung <= 5 %.
- Kritiker-Urteil (siehe unten): keine Luecke der Stufe "gross" und hoechstens zwei der Stufe "klein", in zwei Runden hintereinander.
- Kein Check wurde gegenueber der Vorrunde schlechter.

## Die Stuecke (klein, einzeln beurteilbar), in dieser Reihenfolge

Streben-Knoten (Hub) -> Aussenbeet mit Kies und Toepfen -> NFT-Rinne -> Vortex-Tank (Kegel, Plattform, Fittings) -> Pool mit Rand -> zweites Becken -> Pumpe/Filtermodul -> Rohr- und Schlauchverlauf (aus `data/system.json`) -> Farben/Materialien -> Gesamtansicht. Jedes Stueck ist ein Bauteil in `designs/components/` (eine Definition, viele Instanzen).

## Ablauf je Stueck

1. **Bauer** (die Hauptsitzung): Stueck bauen, Kamera wie in der passenden Referenz stellen (Ausschnitt von ref-4/5/6), Render nach `renders/gauntlet/<stueck>-NN.png`, Checks laufen lassen.
2. **Kritiker** (ein getrennter Unter-Agent mit frischem Kontext, ein Agent zur Zeit, nie parallel zu anderem Bau, um das Limit zu schonen): bekommt nur zwei Bilder `A.png` und `B.png` (Referenzausschnitt und unser Render in zufaelliger Reihenfolge, Dateinamen ohne Hinweis), die Frage "Welches Bild zeigt die echte Anlage genauer in Form, Proportionen, Anzahl und Details? Rendering-Stil (Licht, Schatten, Material) ignorieren." und die Teileliste mit Soll-Zahlen aus `layout.json`. Antwort-Pflicht: A oder B, dann hoechstens fuenf konkrete Luecken, nach Groesse sortiert, je mit "gross" oder "klein". Keine Note, kein Lob.
3. **Auswertung:** Benenne die Zuordnung A/B erst nach der Antwort. Waehlt der Kritiker unseren Render nicht, oder nennt er eine grosse Luecke: der Bauer behebt NUR die groesste Luecke, neue Runde mit neuem frischen Kritiker (nicht dem alten fortsetzen).
4. **Regressionsschutz:** wird ein Check schlechter, wird nicht committet.
5. Commit+Push mit Stueckname und Stand, eine Zeile in `docs/loop-log.md`, dann naechstes Stueck. Sind alle Stuecke bestanden: Gesamtansicht, dann Foto-Latte, danach erneut von vorn mit schaerferem Blick (Detailtiefe erhoehen).

## Warum der Kritiker nicht blind im strengen Sinn sein kann

Unser Render ist eine CAD-Ansicht, das Original ein Raytracing-Bild; ein Kritiker erkennt den Unterschied immer. Deshalb vergleicht er hier **Genauigkeit der Anlage**, nicht Bildstil. Streng blind wird erst die Foto-Latte (Teil 3), weil dort beide Bilder gleich fotorealistisch aussehen. Der Kritiker bekommt dort die Aufgabe "Welches ist der Originalrender?"; die Latte ist erreicht, wenn er in drei Paaren hintereinander nicht zuverlaessig trifft.

## Sparmassnahmen (Limit)

Kritiker nur je Stueck-Meilenstein, nicht je Mikro-Schritt; Kritiker mit mittlerem Modell (`sonnet`) und nur zwei Bildern plus kurzer Teileliste; Rundenprotokoll kurz; nach jedem Schritt Commit.

## Stand

29.10.2026 — Skill eingebaut, Loop-Beschreibung angelegt. Noch kein Kritiker gelaufen.
