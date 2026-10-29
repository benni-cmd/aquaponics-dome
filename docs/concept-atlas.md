# Konzept-Atlas: Fachbereiche der Aquaponik-Kuppel (Plan v2, 29.10.2026)

Ziel: Das Modell ist nicht nur schoen, sondern **statisch, biologisch und technisch schluessig** und fuer ein NGO-Projekt mit lokalen Ressourcen baubar. Jeder Fachbereich hat: Fragen, Eingaben, Rechenweg, Pruefskript, Ergebnisdokument und einen **Fachkritiker** im Gauntlet (`docs/gauntlet.md`): ein getrennter Agent mit frischem Kontext und nur der Checkliste dieses Fachs, der die Luecken benennt.
Herkunftsmarken wie in `docs/hydraulics.md`: **[Q]** Quelle, **[E]** eigene Rechnung, **[A]** Annahme. Alles hier ist eine Plausibilitaetspruefung, kein Nachweis; fuer Statik und Elektrik ist die Freigabe durch eine Fachperson noetig.

## 0. Randbedingungen (Eingaben, ohne sie sind Fachrechnungen nur Beispiele)

| Eingabe | Stand | Wirkung |
|---|---|---|
| Standort, Klima (Temperaturen, Wind, Schnee, Hoehe) | UNBEKANNT; Bilder zeigen Wiese, Fluss, Nadel- und Laubwald, Hanglage | Statik (Schnee/Wind), Fischart, Heizung/Frostschutz |
| Wasserquelle | Fluss mit Wehr und Rohr (Bilder), [A] | Zulauf, Wasserqualitaet, Verdunstungsersatz |
| Strom | Solarfeld mit 5 Modulen in den Bildern, Groesse unbekannt [A] | Pumpen, Luft, Notstrom |
| Fischart | UNBEKANNT | Temperatur, Besatzdichte, Futter, Sauerstoff |
| Kulturen | Salat, Kraeuter, Gemuese (Bilder: Salat, Erdbeeren, Moehren, Bohnen, Tomaten) | Naehrstoffbedarf, NFT oder Beet |
| Ziel (Ertrag, Zahl Personen) | UNBEKANNT | Dimensionierung der Fischmenge |
| Material und Budget vor Ort | UNBEKANNT | Hub-Variante, Rohre, Beete |
Fragen an Ben (nicht blockierend, Standardannahme gilt bis zur Antwort): 1 Standort/Klima, 2 Fischart (Standard: Tilapia fuer warm, Forelle fuer kaltes Flusswasser, je nach Klima), 3 Wassertiefe des Pools, 4 Solar-Leistung, 5 Ertragsziel, 6 verfuegbare Baumaterialien, 7 Budgetrahmen, 8 Rollen der Pump-/Filtermodule.

## 1. Statik (Datei `docs/statics.md`, Skript `scripts/check_statics.py`)

Fragen: Tragen die Streben die Lasten? Halten Knoten und Verankerung Wind und Schnee? Traegt der Boden Wasser und Kies?
Lastfaelle: Eigengewicht, Schnee (Standort), Wind inkl. Abheben (Verankerung am Sockel), Zusatzlast Haut (Folie/Glas), Wasser/Kies/Tanks auf Boden und Plattformen, Betreten der Tische.
Rechenweg (je Lastfall in einer Zeile, Annahmen offen): Flaechenlast auf Kuppel -> Knotenlasten (26 Knoten) -> Stabkraefte (Naeherung oder kleines Stabwerksmodell im Skript) -> Knickpruefung je Strebe -> Knoten-/Schraubenpruefung -> Verankerung gegen Abheben -> Pressung am Fundament.
**Vorab-Rechnungen aus dem OBJ [E, Plausibilitaet]:**
- Streben: 30 Stueck 3279 mm und 35 Stueck 3708 mm, Profil 30 x 30 mm (Wanddicke im OBJ unbekannt, hier 2 mm Stahl angenommen). Knickkraft der laengsten Strebe (beidseitig gelenkig): F = pi^2 E I / L^2 mit I = (30^4 - 26^4)/12 = 29.419 mm^4 (= 2,94 cm^4), E = 210 GPa, L = 3708 mm ergibt etwa 4,4 kN ohne Sicherheitsfaktor. Bei einer Schneelast von 0,75 kN/m^2 (Beispielwert, Standort unbekannt) auf der projizierten Flaeche 113 m^2 entstehen etwa 85 kN, verteilt auf die obersten Streben: die Stabkraefte liegen wahrscheinlich im Bereich einiger kN. Ergebnis: **das Profil ist bei Schnee wahrscheinlich zu schwach, in schneefreier Gegend mit geringer Windlast knapp.** Statischer Nachweis zwingend, Alternative: groessere Profile (z. B. 40 x 40 x 3 oder 50 x 50 x 2,5) und Hub-Variante C/B.
- Boden: Kies wiegt nass etwa 1,6-1,8 t/m^3 [A]; ein Aussenbeet mit 30 cm Kies (2,95 x 0,99 x 0,3 = 0,88 m^3) wiegt etwa 1,5 t, acht Beete etwa 12 t, sechs Innenbeete (0,52 m^3 je) etwa 5 t, Pool etwa 6 t Wasser bei 0,5 m Tiefe [A], Tanks je 0,4-1,0 t. Gesamt grob 25-30 t auf dem Boden. Leichte Alternative: Blaehton (ca. 0,5-0,7 t/m^3), spart etwa zwei Drittel. Folge (korrigiert 29.10. nach Ben): Es gibt KEINE Bodenplatte; das Skelett ist im Erdboden verankert (Punktfundamente/Anker an den Basisknoten), alles andere steht auf verdichteter Erde. Statt Plattentragfaehigkeit zaehlt die zulaessige Bodenpressung (Erdboden, Verdichtung, Setzung unter Tank-Plattformen und Kies-Beeten); Beete eingelassen (im OBJ 160-210 mm unter dem Boden) mindert die Hoehe, nicht das Gewicht. Statik-Ausbau ruht derzeit (Phase reines Modell).
- Plattformen: Tank gross 930 mm gefuellt etwa 0,9-1,0 t auf Plattform 977 x 976 mm mit 4 Beinen 40 x 40 x 1008: Beinknickung und Plattformbiegung pruefen [E offen].
Quellen zu recherchieren (zwei unabhaengige je Wert): Schnee- und Windlastzonen nach Eurocode 1 (EN 1991-1-3/-1-4) oder lokale Norm, Knickformel/Profiltabellen, Knoten-Tragfaehigkeit von Conduit-Hubs, Lastannahmen Gewaechshaus (EN 13031-1).

## 2. Biologie (Datei `docs/biology.md`, Skript `scripts/check_biology.py`)

Fragen: Passt die Fischmenge zur Pflanzflaeche? Reicht die Biofilterflaeche? Stimmen Sauerstoff, Temperatur, pH, Nitrat? Welche Arten passen zum Standort?
Rechenkette (alles aus `data/layout.json` und Annahmen, im Skript):
1. Pflanzflaeche: Aussenbeete 8 x 2,95 x 0,99 = 23,3 m^2, Innenbeete 6 x 1,865 x 0,933 = 10,4 m^2 [E aus OBJ]; NFT-Rinnen kommen dazu (Rinnenflaeche aus layout.json).
2. Futtermenge: 40-50 g je m^2 und Tag fuer Blattgemuese, 50-80 g fuer Fruchtgemuese [Q FarmHub/FAO ueber Zweitquellen; FAO-Original nicht abrufbar]. Beispiel 33,7 m^2 Beete x 45 g = rund 1,5 kg Futter am Tag [E].
3. Fischbiomasse: bei 1-2 % Koerpergewicht Futter je Tag (Fische ueber 100 g) [Q] ergibt sich eine Biomasse von etwa 75-150 kg [E]; Besatzdichte im Pool (ca. 6 m^3, Tiefe unbestaetigt): 12-25 kg/m^3 [E]. Das ist ein gaengiger Bereich, hangt aber stark von Sauerstoff und Filterung ab.
4. Biofilter: 1 l Medium je g Tagesfutter bei Kies/Schlacke im Beet, 0,5 l je g bei Bioballs [Q Zweitquellen]. Bedarf rund 1.500 l; vorhanden sind bei 30 cm Kies etwa 10 m^3 [E]: **grosszuegig ueberdimensioniert**, die Beete sind also biologisch mehr als ausreichend. Die Kegeltanks mit Helix-Biomedium waeren dann nur Reserve.
5. Sauerstoff, Temperatur, pH, Nitrat: Zielbereiche je Fischart und Kultur, Luftpumpe dimensionieren, Frostschutz, Algen (Beetwasserstand 25 mm unter Medium [Q SRAC]).
Noch zu recherchieren (zwei Quellen je Wert): Artenwahl nach Klima, Sauerstoff-Mindestwert, pH-Kompromissbereich, Nitrat-Grenzen, Besatzdichten je Art, Krankheitsvorsorge/Quarantaene, Erntezyklen und Ertrag je m^2.

## 3. Hydraulik und Elektrik (`docs/hydraulics.md` vorhanden; neu `docs/electrical.md`, `scripts/check_power.py`)

Hydraulik: Konzept und Regeln stehen in `docs/hydraulics.md`; es fehlt der Graph (`data/system.json`) und `check_hydraulics.py`.
Elektrik: Pumpen (Leistung aus Foerderstrom und Hoehe: P = rho g Q H / eta), Luftpumpe, Beleuchtung/Steuerung, Gesamtleistung und Tagesenergie -> Solarleistung, Batterie fuer Nacht und **Notstrom**: bei Pumpenausfall muessen Fische Luft behalten (separate Luftpumpe mit Batterie), Pflanzen halten Stunden aus. Schutz: FI-Schutzschalter und Schutzart (Nassbereich), Schaltschrank aussen am Sockel. Quellen zu recherchieren: Pumpenkennlinien (Datenblaetter), Auslegung kleiner Inselanlagen, Schutzvorschriften (IEC 60364-7-702/-7-705 sinngemaess).

## 4. Bau und Logistik (`docs/bom.md`, `docs/assembly.md`, `scripts/bom.py`)

Stueckliste aus dem Modell (Streben nach Laenge, Knoten, Rohre nach DN, Fittings, Tanks, IBC, Toepfe); Montagefolge (Fundament, Sockel, Streben/Knoten bodenweise, Haut, Technik, Beete, Pflanzen); Werkzeugliste; Materialien nach Verfuegbarkeit vor Ort (Stahl, Holz, Bambus, HDPE, IBC aus Recycling); Preise nur mit Quelle und Datum. Hub-Optionen siehe `docs/hydraulics.md` Abschnitt 4.

## 5. Betrieb und Sicherheit (`docs/operations.md`)

Wartung (Schlammablass der Absetzer, Siebe, Biofilter, Pumpen), Ausfall-Szenarien (Pumpe, Strom, Rohrbruch, Sauerstoff, Hitze/Frost, Algen, Krankheit) mit Folge und Gegenmassnahme (FMEA-Tabelle), Hygiene und Lebensmittelsicherheit (Wasser aus dem Fluss, Krankheitserreger, Zugang), Rutsch-/Stolper-Sicherheit, Zugang zu allen Ventilen, Notablass.

## 6. Gestaltung und Render (Farben, Materialien, Schlauchverlauf)

Regeln in `docs/hydraulics.md` Abschnitt 5; Foto-Render ueber ControlNet am Ende (`docs/gauntlet.md`, Foto-Latte).

## Fachkritiker im Gauntlet

Zusaetzlich zum Bildkritiker je Meilenstein ein Fachkritiker (frischer Kontext, ein Agent zur Zeit): **Statik-Kritiker** (liest `statics.md` und das Modell, sucht fehlende Lastfaelle, unplausible Annahmen), **Biologie-Kritiker** (Bilanz Fisch-Pflanze-Filter-Wasserqualitaet), **Technik-Kritiker** (Wasserweg, Pumpen, Strom, Notfaelle). Jeder nennt hoechstens fuenf Luecken (gross/klein), keine Note.

## Reihenfolge der Arbeit

1. Randbedingungen eintragen, Fragen an Ben stellen (laufend).
2. `docs/statics.md` + `check_statics.py` (Plausibilitaet, Knickung, Lasten, Fundament).
3. `docs/biology.md` + `check_biology.py` (Bilanz aus `layout.json`).
4. `data/system.json` + `check_hydraulics.py`, dann `docs/electrical.md` + `check_power.py`.
5. `docs/bom.md`, `docs/assembly.md`, `docs/operations.md`.
6. Danach die Bauteil-Verfeinerung im Gauntlet; die Fachwerte steuern Dimensionen (z. B. Strebenprofil, Kiestiefe, Pumpengroesse).
Rechenergebnisse fliessen zurueck ins Modell: wenn die Statik ein groesseres Profil verlangt, aendert sich `P` und alle Instanzen.
