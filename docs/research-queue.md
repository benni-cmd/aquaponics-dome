# Recherche-Warteschlange

Format je Auftrag: **R-ID** | Prioritaet (H = blockiert den Bau, M, N) | Frage | Warum | Akzeptanz | Zielparameter | Status. Ergebnis in `docs/research/<R-ID>.md`. Akzeptanz Standard: zwei unabhaengige, gelesene Quellen oder eigene Rechnung mit belegten Eingaben; Widersprueche notieren.

| ID | Prio | Frage | Warum | Zielparameter | Status |
|---|---|---|---|---|---|
| R01 | H | Welches Profil/Wanddicke tragen die Streben bei Schnee und Wind (Beispielstandorte)? Lastannahmen nach Eurocode 1 oder aehnlich | Profil bestimmt die Strebenmasse im Modell | `strut_profile`, `strut_wall`, `snow_load`, `wind_load` | offen |
| R02 | H | Welche Hub-Variante ist am billigsten und mit lokalen Mitteln baubar und tragfaehig (Vergleich mit Preisen, Quelle und Datum)? | Knoten muessen modelliert werden | `hub_variant`, Kosten | offen |
| R03 | H | Kiestiefe im Substratbeet, Flutzyklus, Glockensiphon-Auslegung (Quelle zu Medientiefe fehlt) | Beet-Modell und Gewicht | `media_depth`, `siphon_*` | offen |
| R04 | M | Fischart nach Klima (Tilapia warm, Forelle kalt): Temperatur, Sauerstoff, Besatzdichte, Futter | Biologie-Bilanz | `fish_species`, `stocking_density` | offen |
| R05 | M | Pool-Wassertiefe aus OBJ ableiten oder Standard; Volumen | Besatz, Umlauf | `pool_depth` | offen |
| R06 | M | NFT: Rinnenzahl je Beet, Gefaelle, Durchfluss, Topfabstand fuer Salat (zwei Quellen) | Rinnen im Modell, Hydraulik | `nft_channels_per_bed`, `nft_slope`, `nft_flow` | teilweise (hydraulics.md) |
| R07 | M | Pumpenauswahl: Foerderstrom und Hoehe je Linie, Leistung, Notbetrieb | Elektrik, Pumpen im Modell | `pump_flow`, `pump_head`, `pump_power` | offen |
| R08 | M | Elektrik: Solar-Inselanlage fuer Pumpen und Luft, Schutzvorschriften Nassbereich | Elektrikdokument | `solar_kwp`, `battery_kwh` | offen |
| R09 | M | Vortex- und Radialstrom-Absetzer: Auslegung an unseren Tankmassen (Zulauf tangential, Kegelwinkel) | Tanks mit Kegel und Ports | `vortex_*` | teilweise |
| R10 | N | Wasserqualitaet aus Fluss als Zulauf: Filterung, Hygiene | Betrieb | - | offen |
| R11 | N | Kuppelhaut: Folie oder Glas, Preis, UV, Befestigung an Streben | Haut T2 | `skin_material` | offen |
| R12 | N | Rutschsicherheit, Zugang, Frost, Schaedlinge (Betrieb) | `operations.md` | - | offen |
