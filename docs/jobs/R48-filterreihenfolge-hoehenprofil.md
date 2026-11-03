# R48 — Filterreihenfolge und Hoehenprofil (Vortex, Feinfilter, Pumpe, Biofilter)

**Art:** Recherche und Variantenrechnung, KEIN Bau, kein Modell-Umbau. Wunsch W54 (Ben 03.11.2026).

## Problem
Heute: Pool -> Heber -> Feinfilter (Grube) -> 2 Pumpen -> Biofilter (Ueberlauf Z 1570) -> Verteiler; der Absetzer (Vortex, 267 l) haengt nur am Bodenablauf (11 %) mit kleiner Pumpe und laeuft per Schwerkraft in den Feinfilter-Einlauf. Zwischen Feinfilter und Biofilter sitzen die Pumpen, dort ist kein Ueberlauf moeglich. Ben fragt, ob eine andere Reihenfolge und Hoehenlage besser (wartbarer) ist.

## Intent
Eine belegte Empfehlung, ob die Filterkette umgebaut werden soll, bevor die Verlegung (M10 S3) startet; Teil der Entscheidung E20/E21.

## Goal
Ein Bericht `docs/research/R48-filterreihenfolge.md` mit Vergleichstabelle der Varianten, je Variante: Wasserweg mit Hoehen (Z), Foerderhoehe und Pumpenleistung (Annahme kennzeichnen), Wartung (was liegt wo, Zugang, Schlammablass), Ausfallverhalten, Umbauumfang gegen den gebauten Stand, Verstoss gegen den einheitlichen Fluss (alles durch den Biofilter). Am Ende Empfehlung mit Rangfolge. Alles Behauptete mit zwei unabhaengigen Quellen oder als [Annahme] markiert.

## Varianten (mindestens)
- V0 heute: Feinfilter -> Pumpen -> Biofilter (Absetzerkreis nur Teilstrom).
- V1 Ben: Pool -> Subtank (Sumpf) mit Pumpe -> Vortex HOCH ueber dem Biofilter -> Ueberlauf -> Biofilter. Wo sitzt dann der Feinfilter? (vor dem Vortex, im Vortex-Auslauf, oder im Subtank als Siebkorb am Einlauf)
- V2 Vortex zuerst im Hauptstrom, tief (Grube) per Schwerkraft vom Heber, danach Feinfilter, dann Pumpen, dann Biofilter (nur Reihenfolge der gebauten Teile getauscht).
- V3 Kaskade: einmal pumpen an die hoechste Stelle (Vortex), danach alles per Ueberlauf nach unten (Vortex -> Feinfilter -> Biofilter -> Verteiler).
- V4 wie V0, aber Feinfilter-Siebkorb im Sumpf statt in der Grube.

## Zu pruefen (Fragen)
1. Reihenfolge grob vor fein: Ist Vortex vor Feinfilter Stand der Technik in Kreislaufanlagen? Auslegungswerte eines Swirl-Separators im Vollstrom (Verweilzeit bei 110 l/min und 267 l ca. 2,4 min [Rechnung], Abscheidegrad, Mindestdurchfluss), Quellen z. B. Davidson/Summerfelt, Timmons/Ebeling.
2. Pumpe vor der Feststoffabscheidung: Zerschlagen der Partikel in der Pumpe (Scherung), Verstopfungsrisiko der Pumpe; Regel "Feststoffe vor der Pumpe entfernen" gegen Bens Idee (Pumpe im Sumpf) abwaegen.
3. Hoehenbilanz je Variante aus `data/leitungsnetz.json` und `scripts/dome-script.json`: Zulauf Biofilter Z 1420, Ueberlauf Z 1570, Plattform Z 570, Feinfilter-Grube Z -496, Heber (Pool 515, Seitenablauf Z 340, Filter-Einlauf Z 320). Foerderhoehe heute 2,0 m; je Variante neu. Bodenablauf Z -1685 (11 %): fliesst per Schwerkraft in einen Sumpf unter Poolspiegel? Dann entfaellt die kleine Pumpe.
4. Tragfaehigkeit/Aufbau: Vortex 267 l (ca. 270 kg + Tank) ueber dem Biofilter (857 kg gefuellt auf Plattform Z 570): noetig? Konstruktion grob.
5. Schlammablass: Schlammfass heute in Grube 0,95 m tief (K07). Wird die Grube bei hohem Vortex unnoetig?
6. Wartung: pro Variante wo ist Zugang (Pumpe, Siebkorb, Vortex, Schlamm), Handgriffe je Woche.
7. Einheitlicher Fluss (W53): bleibt in jeder Variante alles Wasser durch den Biofilter?

## Grenzen
Kein Umbau, keine Aenderung an `gen_dome.py` oder `data/*`. Scope D69 beachten (keine Ertrags-, Kosten-, Standort-, Verschattungsrechnung). Ergebnis nur als Bericht plus Eintrag "Besonderheit:" fuer `docs/pitch-besonderheiten.md` falls es eine gibt. Kontextgrenzen nach `docs/arbeitsweise-sitzungen.md` Abschnitt 4. Abschluss mit "Geprueft gegen: ... Offen: ..." und Beschaffbarkeit jedes genannten Teils als Standardteil/Selbstbau.

## Ergaenzung 03.11.2026 (Ben, nach Start der Recherche)
- Eigene Frage 8: Ist es unsinnig, den Feinfilter VOR den Vortex zu setzen (grob vor fein)? Mit zwei Quellen beantworten. Beachten: heute haengt der Vortex nur am Bodenablauf (11 %), sein Auslauf geht in den Feinfilter-Einlauf; der Hauptstrom (89 %) geht ueber den Heber direkt in den Feinfilter. Gegenargument pruefen: Pumpe vor der Feststoffabscheidung zerschlaegt Partikel.
- Bewertung: Komplexitaet und Menge des Vergrabenen (Wartung) bei jeder Variante ausdruecklich mitgewichten, nicht nur Foerderhoehe und Strom.

## Stand (03.11.2026, Fachrecherche)
- **Fertig:** `docs/research/R48-filterreihenfolge.md` (Vergleichstabelle V0 bis V5, 7 Prüffragen, Rangfolge, Beschaffbarkeit, Belegstand je Aussage) und Rechenskript `scripts/r48_rechnung.py`. Kein Bau, `gen_dome.py`, `data/*`, Netzliste und Roadmap unverändert.
- **Ergebnis:** Rang 1 V0 behalten (Teilstrom-Absetzer am Bodenablauf, Sieb im Hauptstrom vor der Pumpe, entspricht SRAC 453, Davidson/Summerfelt und Khater). Rang 2 V4 (Subtank mit Siebkorb und Tauchpumpen: -7,1 m vergrabenes Rohr, Höhen unverändert), Rang 3 V5 (Bodenablauf per Schwerkraft, kleine Pumpen entfallen), danach V2, V1, V3. Bens V1/V3: Pumpe vor dem Feinfilter (Rohwasser), 2,2 bis 2,4 m Förderhöhe, bis 475 kg in der Höhe; kein Wartungsgewinn.
- **Subtank gelesen als** Zwischen-/Sumpftank mit Tauchpumpen, Spiegel gleich Heber-Ende (Z 320).
- **Neuer Befund:** Filterbehälter ohne Rückstausicherung (Oberkante Z 364 gegen Pool 515); Vorschlag: Hoch-Schwimmer schließt den Heber-Absperrhahn.
- **Grenzen der Belege:** Wirbelabscheider-Auslegung (Veerapen 2005) nicht im Volltext gelesen; Pumpen-Scherung stützt sich auf zwei Dokumente mit gemeinsamem Primärbeleg (McMillan 2003, nicht gelesen).
- **Offen:** E21 Entscheidung Ben (V0 behalten, V4 als Option); Montage: Heber-Messung und Rückstausicherung; Standort: Grube tiefer als Poolboden nur bei V2/V5.
