# Wasserkreislauf, Filter und Bauplan (Konzept, recherchiert 29.10.2026)

> **Stand 30.10. (nach Fachrecherche R17–R22, Auftrag R23):** Pool-Tiefe ist 2,2 m (D26), nicht 0,5 m: die Pool-Zahlen in 2.4 sind veraltet. Aktuelle Rechnung und offene Punkte: `docs/system-concept.md`, Quellen: `docs/research/aquaponik-werte.md`. Geaendert gegenueber den Regeln unten: **NFT-Durchfluss 1 l/min je Rinne** (FAO 589: 1–2; nicht 0,5), **Flutzyklen 2 je Stunde jetzt belegt** (Fort Valley State Extension, 5–8 min), **Pumpenwirkungsgrad 25 %** (FAO 589: 16–33 %, nicht 35 %), **Futter je m² Pflanzflaeche 25–65 g** (SRAC 454: 25 % des Raft-Werts, FAO 589: 40–80), **Absetzer als Teilstrom ca. 12,5 l/min je Tank** (UVI-Klaerer ca. 20 min), **Hauptkreislauf 4 grosse Pumpen a 55 l/min = 220 l/min** (D38). Die Modellwerte 12/30 l/min in 2.3 und die Umwaelzung in 2.4 sind damit ersetzt; Pumpen-Rollen siehe D38.

Zweck: Grundlage fuer `data/system.json` (Graph), `scripts/check_hydraulics.py` und die 3D-Rohre. Jede Zahl traegt eine Herkunft:
**[Q]** = durch Quelle belegt (Link unten), **[E]** = eigene Rechnung aus Quellwerten, **[A]** = Annahme, von Ben nicht bestaetigt. Nichts hier ist eine statische oder fachliche Freigabe.

## 1. Rollen im System (wie einfache Aquaponik-Anlagen es machen)

| Bauteil | Aufgabe | Herkunft |
|---|---|---|
| Pumpen | halten das Wasser im Umlauf: Pool -> Filter -> Pflanzen -> zurueck. Eine Pumpe laeuft dauernd, die Beete fluten und entleeren per Glockensiphon | [Q] Scale and Stem, FarmHub |
| Mechanischer Filter, Absetzer | nimmt Feststoffe (Kot, Futterreste) vor dem Biofilter heraus; Radialstrom-Absetzer entfernt laut mehreren Quellen mehr als ein Drallabscheider (Studie: etwa das Doppelte) | [Q] FarmHub 2.2, Aquaponderings/ASC; Zahl nur aus einer Studie |
| Vortex/Drall (Sediment) | kegelfoermiger Tank, Wasser tritt tangential ein, Feststoffe sinken zur Kegelspitze und werden dort abgelassen. Passt zu den 4 Kegelboden-Tanks im OBJ | [Q] Open Source Ecology "Vortex Biofilter", ecofilms Radialfilter; Rolle der OBJ-Tanks [A] |
| Feinsiebung | Netze/Matten (z. B. Obstbaumnetz) fangen Schwebstoffe, die der Absetzer durchlaesst; verstopfen schnell, wenn oben nicht abgesetzt wird | [Q] FarmHub 2.2 |
| "Helixfilter" | Kunststoff-Biomedium in Schraubenform (z. B. Oase Hel-X): viel Oberflaeche, wenig Stroemungswiderstand, fuer Ammonium/Nitrit-Abbau, NICHT fuer Feststoffe. Eine Spezifikation fuer einen schraubenfoermigen Feststofffilter in einfachen Aquaponik-Anlagen habe ich nicht gefunden | [Q] Oase Hel-X Produktseite; Deutung "Helix = Biomedium" [A], Ben bestaetigen |
| Biofilter | Bakterien wandeln Ammoniak in Nitrat um; Medium-Volumen richtet sich nach der taeglichen Futtermenge | [Q] FAO/Somerville ueber Zweitquellen: 1 l Medium je g Tagesfutter (Zementschlacke/Kies im Beet), 0,5 l je g (Bioballs in NFT/DWC); nur aus Zusammenfassungen, FAO-PDF ging nicht |
| Substratbeete (halbe IBC) | Pflanzen im Kies/Blaehton; zugleich Biofilter-Flaeche; Fluten und Entleeren | [Q] SRAC 5007, Scale and Stem |
| NFT-Rinnen | duenner Wasserfilm in Rinnen, Pflanzen in Netztoepfen | [Q] FarmHub 2.4, Greenhouse Management, Atlas Scientific |
| Verteiler/Schlaeuche | Wasser gleichmaessig auf Rinnen und Beete verteilen | [E] Auslegung unten |

## 2. Bemessungsregeln (mit Spannweite, weil Quellen sich unterscheiden)

1. **Absetzer-Verweilzeit:** 30 min, wenn der Absetzer die einzige Feststoffstufe ist; Auslegungsstroemung 5 gpm (klein) bzw. 25 gpm (gross). [Q] FarmHub 2.2 (aelterer Kentucky-Leitfaden).
2. **Radialstrom-Flaechenbelastung:** 4 gpm je ft2 Zylinderflaeche bei 45 Grad Kegel, Einzelfolie eines Praesentators; unbestaetigt. [Q] JD Sawyer / Aquaponics Source.
3. **Unsere zwei Tankgroessen:** Volumen kleiner Tank ca. 0,3-0,4 m3, grosser ca. 0,9-1,0 m3 [E aus 673 x 1075 und 930 x 1444 mm]. Bei 30 min Verweilzeit: kleiner Tank ca. 0,7 m3/h = 12 l/min, grosser ca. 1,8 m3/h = 30 l/min [E].
4. **Pool-Umlauf:** viele Anleitungen nennen mindestens ein Volumen je Stunde; der Pool hat bei Wasserspiegel Z 515 und Boden auf Z 0 nur ca. 6 m3 [E aus 3,89 m Durchmesser, Tiefe 0,5 m, Tiefe nicht bestaetigt]. Zwei Linien mit je 12 l/min ergeben 24 l/min = 1,4 m3/h, also Umwaelzung nur etwa alle 4 h. Die Beete und der Pool-Umlauf koennen ueber getrennte Teilstroeme laufen. Entscheidung offen, im Graphen als Annahme markieren [A].
5. **NFT:** Gefaelle 1 cm/m (FarmHub) bis 1,2-3 % (Greenhouse Management), Atlas nennt 1:100 und anderswo 1:30-1:40: Quellen widersprechen sich, Vorschlag 1 %; Durchfluss 1-2 l/min je Rinne, bei Salat eher weniger; Rohr 7,5 cm fuer Blattgemuese, Rinnenlaenge hoechstens 12 m. [Q] FarmHub 2.4, Greenhouse Management, Atlas Scientific. Unsere Rinnen (130 x 100 mm, 1,3-3,2 m) liegen im zulaessigen Bereich.
6. **Glockensiphon (Substratbeet):** Ablaufrohr 40-50 mm, Glocke 75-100 mm; Wasserstand bis 1 Zoll (ca. 25 mm) unter der Mediumoberkante, damit keine Algen wachsen. [Q] Scale and Stem, Mississippi State SRAC 5007. Zahl der Flutzyklen und Medientiefe: keine belastbare Quelle gefunden, [A].
7. **Futtermenge je m2 Pflanzflaeche und Tag:** Blattgemuese 40-50 g (zwei Zusammenfassungen; ein Handout nennt 20-50), Fruchtgemuese 50-80 g; 60-100 g ist ein Wert fuer Raft/DWC (Rakocy/UVI). [Q] FarmHub Rechenseite, Zweitquellen. Die FAO-Originalseite ging nicht, daher Spannweite.
8. **Pumpenhoehe:** statisch (Kegelspitze oder Pool bis hoechste Rinne, ca. 1,3 m + Rohrfuehrung) plus Reibung plus 20 % Reserve [E]; Fabrikat offen.
9. **Sicherheit:** kein Auslass unter dem Poolspiegel ohne Siphonbrecher oder Ventil; Notueberlauf; Ablassventile an den Tiefpunkten [E, gaengige Praxis].

## 3. Flussbild (Annahme, Rollen der Tanks aus Lage und Form im OBJ abgeleitet, [A])

Zwei gleiche Linien, jede mit einem kleinen und einem grossen Tank (Azimut 108/123 und 213/229):

Pool -> Bodenablauf (Pool-Mitte) -> Pumpe A -> kleiner Kegeltank (Vortex-Absetzer, Schlammablass an der Spitze) -> Feinsieb/Netz -> grosser Kegeltank (Biofilter mit Helix-/Biomedium, Belueftung) -> Pumpe B -> Verteiler -> NFT-Rinnen (Gefaelle) und Substratbeete (Glockensiphon) -> Sammelrinne -> Schwerkraft-Ruecklauf zum Pool und zum zweiten Becken (vor der Tuer, Wasserspiegel gleich) -> Pool.
Dazu: Luftpumpe mit Ausstroemern im Pool und im Biofilter; Frischwasser (blaues Rohr von aussen) mit Schwimmerventil am zweiten Becken; Notueberlauf; Strom aus dem Schaltschrank. Die Fittings an den Kegelspitzen der Tanks sind im OBJ die Anschluss-Ports.

## 4. Kuppel-Knoten (Hubs), billig und lokal baubar

Optionen mit Befund aus der Recherche (Preise nicht gefunden, nur Rangfolge nach Aufwand):
- **A flachgedrueckte Rohrenden + Schraube (Conduit-Dome):** guenstigste Variante, nur Bohrer, Schraubstock und Schrauben; Nachteil: flachgedrueckte Enden verlieren deutlich an Festigkeit, Streben muessen laenger sein. [Q] Patentschrift/Foren, anekdotisch.
- **B geschweisste Stahl-Hubs mit Flachstahl-Armen:** stabiler, braucht Schweissen, Zink entfernen, Kaltverzinkung. [Q] Builder-Bericht (Instructables/Foren).
- **C Rohrhuelsen an einer Mittelplatte, Rohr steckt und wird verstiftet:** Rohr bleibt rund, teurer in der Fertigung. [Q] Forum.
- **D Holz mit Bandstahl/Edelstahlband-Nabe:** einfach, gut verpackbar; Kostenangabe stammt von einer Herstellerseite, unbestaetigt. [Q] Domerama.
- **E Kunststoffrohr/Bambus mit Seil:** sehr einfach, geringe Last.
Empfehlung als Startpunkt: A oder C fuer Stahlrohr (kein Schweissen, vor Ort baubar), D wenn Holz lokal ist. Die Entscheidung trifft die Matrix in `docs/hubs.md`. Wichtig: Das OBJ-Profil 30 x 30 mm bei 12 m Spannweite ist statisch ungeprueft; ein Nachweis durch eine Fachperson ist noetig. Ein Forenpost zu einer 25-m-Kuppel empfiehlt bei duennen Rohren dicke Waende (mindestens 3,5-4 mm), das ist anekdotisch.

## 5. Bauteil-Bibliothek (Komponenten, Instanzen) und Render-Qualitaet

Prinzip (Ben): jedes wiederkehrende Bauteil EINMAL definieren, die Kopien sind Instanzen; wird die Definition geaendert, aendern sich alle Kopien. Bibliothek in `designs/components/`, Platzierungen in `data/layout.json`. Klassen und Anzahl: Strebe A/B (30/35), Knoten (3 Arten, 26), Aussenbeet (8), Innenbeet (6), Pflanztopf (2160), NFT-Rinne (3 Laengen), Tank klein/gross (2/2) mit Plattform, Beinen, Kegel und Fittings, Pumpe, Filtermodul, Rohrstueck, Bogen, T-Stueck, Ventil, Schlauchstueck, Schlauchhalter, Salatkopf, Glockensiphon.
Stufen der Verfeinerung je Bauteil: 1 Grundform mit richtigen Massen, 2 Details (Rippen, Raender, Beine, Anschluesse), 3 Farbe und Material (SolidCraft `appearance.assign`: Farbe, Deckkraft; Rauheit/Metall nur wenn der Befehl es kann), 4 Einsetzen in das Modell und Pruefung.
Schlaeuche und Rohre fuer schoene Renders: nach Funktion einheitlich gefaerbt (Frischwasser hellblau, Filterlinie dunkelblau, Ruecklauf grau, Luft schwarz oder gruen); Biegeradius mindestens fuenf Schlauchdurchmesser; waagerechte Strecken parallel mit festem Abstand und Halter alle 0,5-1 m; senkrechte Strecken gerade; keine Kreuzung des Tuerzugangs; Verbindungen nur mit Standardteilen (Bogen, T, Ventil, Kupplung), jedes als Bauteil; Rohrverlauf kommt aus dem Graphen, nicht von Hand.

## 6. Luecken (offen, nicht erfunden)

1. FAO-Originalpaper (TP 589) war nicht abrufbar (HTTP 403); Zahlen stammen aus Zweitquellen mit Abweichungen.
2. Keine Quelle zu Medientiefe und Flutzyklen im Substratbeet gefunden.
3. Keine Spezifikation zu einem Helix-Feststofffilter gefunden; "Helixfilter" als Biomedium gedeutet.
4. Keine Preise fuer Hubs; Rangfolge nur nach Aufwand.
5. Wassertiefe des Pools, Rolle der Pump-/Filtermodule und Pumpendaten sind Annahmen.

## Quellen

- FarmHub Aquaponics Production Manual, 2.2 Solids filtration: https://learn.farmhub.ag/resources/aquaponics-production-manual/2-structure-and-design/2-2-solids-filtration/
- FarmHub 2.4 Plant culture or hydroponic subsystem: https://learn.farmhub.ag/resources/aquaponics-production-manual/2-structure-and-design/2-4-plant-culture-or-hydroponic-subsystem
- FarmHub Component calculations and ratios: https://learn.farmhub.ag/resources/small-scale-aquaponic-food-production/8-management-and-troubleshooting/component-calculations-and-ratios/
- FAO Fisheries and Aquaculture Technical Paper 589 (Somerville et al. 2014), nur Zweitquellen: https://openknowledge.fao.org/server/api/core/bitstreams/2ca21047-390f-42cd-bd1d-0c2ebc9c1df2/content
- Scale and Stem, media bed with bell siphon: https://scaleandstem.pages.dev/articles/building-media-bed-aquaponics/
- SRAC 5007 Principles of Small-Scale Aquaponics: https://www.srac.msstate.edu/pdfs/Fact%20Sheets/5007%20Principles%20of%20Small-Scale%20Aquaponics.pdf
- Greenhouse Management, Nutrient film technique: https://greenhouse-management.com/greenhouse_management/greenhouse_production_systems/nutrient_film_technique.htm
- Atlas Scientific, NFT system: https://atlas-scientific.com/blog/nft-system-hydroponics/
- Oase Hel-X Biomedium: https://aquagardening.com.au/oase-hel-x-bio-medium
- Open Source Ecology, Vortex Biofilter: https://wiki.opensourceecology.org/wiki/Vortex_Biofilter_Assembly
- ecofilms, DIY Radial Flow Filter: https://ecofilms.com.au/diy-radial-flow-filter-for-aquaponics
- Domerama, Geodesic hub connectors: https://www.domerama.com/dome-basics/geodesic-dome-hub-connectors/
- Instructables, Geodesic dome greenhouse: https://www.instructables.com/Building-a-Geodesic-Dome-Greenhouse-Part-2
- Forum zu 8V-Kuppel (anekdotisch): https://groups.google.com/g/GeodesicHelp/c/2nXgLzJs50Y
