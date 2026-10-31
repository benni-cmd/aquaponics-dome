# Paket: Bauanleitung, Teileliste, Detailansicht (Roadmap, Ben 31.10.2026)

## PIG
- **Problem:** Das Modell zeigt die Kuppel, aber nicht, wie man sie baut, woraus jedes Teil besteht und was man einkaufen muss. Teile sind teils Sonderformen, die Streben haben zwei Laengen, Becken und Beete sind ungeklaert (kaufen oder bauen).
- **Intent:** Aus dem Modell soll eine echte Bauanleitung mit Teileliste und Funktionserklaerung entstehen; moeglichst wenige verschiedene Kaufteile (Meterware, Normprofile, Normschrauben), minimaler Verschnitt, lebensmittelechte Werkstoffe wo Wasser oder Futter beruehrt wird, Selbstbau statt Sonderanfertigung.
- **Goal:** (1) Detailansicht im Viewer: Rechtsklick auf ein Teil -> Menue "Detailansicht" -> Explosionsdarstellung aller Einzelteile (jede Scheibe, jeder Winkel, jedes Rohr), Teileliste, Klick auf Einzelteil -> Erklaerung (was, Material, Funktion, Eigenschaften, Norm). (2) Stueckliste je Systembestandteil und gesamt, umgerechnet auf Meterware mit minimalem Verschnitt. (3) Entscheidungsgrundlagen fuer Becken, Tanks, Beete und Streben. (4) Bauanleitung (Reihenfolge der Montageschritte).

## Grundsaetze (D56)
1. Standard vor Sonderlosung: genormte Profile, Rohre, Schrauben, Winkel; was man im Handel findet.
2. Wenige Querschnitte und Durchmesser: Profile, Rohr-DN, Schlauch, Schrauben (z. B. M8/M10) bewusst reduzieren; sich an der laengsten Variante orientieren und Meterware zuschneiden.
3. Verschnitt minimieren: Lagerlaenge und Zuschnittplan (1D-Verschnittoptimierung, Saegeschnitt 3 mm) gemeinsam waehlen.
4. Lebensmittelecht, wo Wasser, Fisch oder Pflanzen beruehren; Zertifizierungen in Deutschland klaeren (R31).
5. Selbstbau, wenn guenstiger und machbar; keine Spezialanfertigung ohne Grund.
6. Jedes sichtbare Einzelteil im Modell ist eine Zeile in der Teileliste (Zahl Koerper = Zahl Teile).

## Arbeitspakete (nur Roadmap, noch nicht begonnen; Reihenfolge nach Nutzen)
| Nr | Paket | Wer | Ergebnis |
|---|---|---|---|
| B9 | Strebenkonzept (R34): Varianten V1 zwei Laengen zuschneiden (A 3039, B 3468 mm), V2 EINE Rohrlaenge 3468 fuer alle 65 Streben, die Knotenarme der A-Streben stecken 214 mm tiefer ins Rohr, V3 gleiche Rohre mit Bohrbild und Ueberstand; Verschnitt, Kosten, Montage, Praezision | Fachrecherche + Montage | Vergleich, Empfehlung, Entscheidung Ben |
| B4 | Normteil- und Profilkatalog (`data/katalog.json`): erlaubte Profile, Rohre, Schlaeuche, Schrauben, Winkel; Umstellungsliste fuer Tische, Staende, Rahmen | Werkstatt + Fachrecherche | Katalog, Regeln, Umbauliste |
| B1 | Teile-Datenmodell: `data/parts/<komponente>.json` je Komponente: Einzelteile mit Name, Koerpername im `.sc`, Typ (Profil, Platte, Rohr, Normteil, Sonderteil), Werkstoff, Masse/Laenge, Menge, Funktion, Eigenschaften, Norm, Lebensmittelkontakt, Explosionsrichtung/-abstand | Werkstatt (je Komponente) | Daten + Check (Koerperzahl = Teilezahl) |
| B2 | Export mit benannten Einzelkoerpern, Detailmodell nur bei Bedarf laden (`viewer/detail/<komponente>`) | Montage/Viewer | Export-Skript |
| B3 | Viewer-Detailansicht: Rechtsklick-Menue "Detailansicht", Explosionsanimation mit Schieber, Teileliste, Klick auf Teil oder Zeile -> Infokarte, Zurueck | Viewer-Sitzung | Funktion im Viewer |
| B5 | Stueckliste und Meterware: je Systembestandteil (Kuppel, Becken, Tische, Beete, Technik, Leitungen) einzeln geprueft, dann Gesamt; Zuschnittplan, Einkaufsliste mit Menge/Laenge, Verschnittquote | Orchestrator/Fachrecherche | `data/stueckliste.json`, `docs/stueckliste.md` |
| B6 | Material und Zertifizierung (R31): lebensmittelechte Werkstoffe (Edelstahl, PP, PE-HD, PVC-U, EPDM, Teichfolie, Kleber), noetige Nachweise in Deutschland (u. a. VO (EG) 1935/2004, VO (EU) 10/2011, LFGB, KTW/DVGW W270 bei Trinkwasserkontakt, UBA-Bewertungsgrundlagen; was fuer Fischhaltung/Pflanzen wirklich gilt) | Fachrecherche | R31, Materialtabelle |
| B7 | Beckenkonzept (R32): Pool D 3,89 x 2,2 m tief und Tanks: kaufen oder bauen (Betonringe, Ortbeton, Stahlwand mit Folie, GFK, IBC-Batterie, Standardbehaelter), Unterbau/Fundament, Abfluesse, Bodenablauf, Lagerung, Kosten, Selbstbaufaehigkeit | Fachrecherche | R32, Empfehlung |
| B8 | Substratbeete (R33): fertige Wannen in 2640 x 800 / 1865 x 933 gibt es kaum; Selbstbau (Holzrahmen mit EPDM/Teichfolie, Betonwanne, halbierte IBC, Standardtroege, lokale Ressourcen), Lebensmittelechtheit, Kosten | Fachrecherche | R33, Empfehlung, ggf. Umbau `ibc_beet` |
| B10 | Bauanleitung: Montageschritte in Reihenfolge (Fundament, Knoten/Streben, Becken, Beete, Tische, Technik, Leitungen, Huelle), Teilelisten je Schritt, Werkzeuge, Hinweise | Orchestrator | `docs/bauanleitung.md` (aus Daten erzeugt) |

## Abhaengigkeiten
B9 vor Knoten/Streben-Aenderung; B4 vor B1 (Katalog bestimmt Teilenamen und Profile); B1 vor B2, B3, B5; B6 vor Materialfestlegung in B1; B7/B8 vor Finale der Becken-/Beet-Komponenten; B5 nach B1 und B4; B10 zuletzt.

## Erste Einschaetzung zur Strebenfrage (E, noch zu pruefen)
Strebe = Knoten zu Knoten minus 2 x 120 mm Steckaufnahme: A 3039, B 3468 (siehe `strut_end_offset`). Mit EINER Rohrlaenge 3468 fuer alle 65 Streben waeren die A-Streben 429 mm zu lang; ausgleichbar, indem die Steckarme der Knoten an den A-Streben je 214,5 mm tiefer ins Rohr reichen (im Rohr verdeckt, mit Querbolzen gesichert). Dann reicht eine Meterware (z. B. 3,5 m: Verschnitt B 32 mm, ab Haendler zugeschnitten), kein Zuschnitt auf der Baustelle. Aus 6-m-Stangen waeren es mit B nur 1 Stueck je Stange (Rest 2532 mm, ca. 42 % Verschnitt) und mit A+A 6078 mm (passt nicht in 6000). Das gilt es in B9 mit echten Lagerlaengen, Preisen und Toleranzen zu pruefen; Knoten mit verschieden langen Armen sind ohnehin Sonderteile (Knoten-Kugel mit Steckarmen, D15).

## Offene Fragen an Ben
1. Strebenidee richtig verstanden: gleiche Rohrlaenge fuer alle Streben, Genauigkeit ueber Bohrungen/Steckarme der Knoten? (Empfehlung: ja, als Variante V2 pruefen.)
2. Bezugsland und Region der Beschaffung: Deutschland (Haendler, Normen)? Standort fuer Baurecht/Heizlast noch offen.
3. Wie sehr darf die Optik der Detailansicht an eine technische Produktpraesentation erinnern (Animation, Linien, Beschriftung) gegen Einfachheit zuerst? (Empfehlung: erst Funktion, dann Politur.)

## Stand
- 31.10.2026: Roadmap angelegt, nichts begonnen; laufende Arbeit (W32, Montage Laufwegkarte, Leitungen) geht vor. Start der ersten Pakete nach dem Zwischencheck (Empfehlung: B9 und B4).

## DoD (je Paket, nachgefuehrt bei Abschluss)
Datei vorhanden, gegen Modell geprueft (Zahlen aus dem Repo), Quellen genannt, Entscheidungen in `docs/decisions.md`, WIP-Commit gepusht.
