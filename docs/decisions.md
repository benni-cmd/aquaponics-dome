# Entscheidungslog (autonom, Ben liest morgen mit)

Format: **D-ID** | Datum | Frage | Optionen | Wahl | Grund | Rueckgaengig. Nachts getroffen ohne Rueckfrage; Ben prueft im Morgenbericht, welche er aendern will.

| ID | Datum | Frage | Optionen | Wahl | Grund | Rueckgaengig |
|---|---|---|---|---|---|---|
| D01 | 29.10. | Quellenrangfolge | Bilder zuerst / OBJ zuerst | Ben > OBJ-Zahlen > Bilder (Look) | Ben: Bilder sind das Ziel fuer Aussehen, aber einzelne Bauteile dort falsch | Parameter `source_priority` |
| D02 | 29.10. | Tuer und Drehung des Layouts | Tuer im OBJ unbekannt | Tuer bei Azimut 167 im OBJ (Mitte der Luecke zwischen Aussenbeeten 149/185, zweites Becken davor); `layout_rot = door_az - 167` | nur Indiz, keine direkte Tuer im OBJ | `layout_rot` aendern |
| D03 | 29.10. | Die 2160 Toepfe | NFT-Ring / Pflanzen in Aussenbeeten | Pflanzen in den 8 Aussenbeeten (Z 407-506, Beet-Oberkante 475) | Hoehen und Lage passen exakt | in `layout.json` neu zuordnen |
| D04 | 29.10. | NFT | OBJ zeigt je Typ ein Beispiel | Rinnen ueber den Beeten, Zahl je Beet so, dass die Beetbreite gedeckt ist (Aussen 3, Mitte 4, Abstand 263-288) | Ben: nur Beispiele im OBJ | `nft_channels_per_bed` |
| D05 | 29.10. | "Helixfilter" | schraubenfoermiges Biomedium / Feststofffilter | Biomedium (Hel-X-artig) im grossen Kegeltank | keine Spezifikation eines Helix-Feststofffilters gefunden | `filter_role` |
| D06 | 29.10. | Rollen der 4 Tanks | alle gleich / zwei Linien | Zwei Linien: kleiner Kegeltank = Vortex-Absetzer, grosser = Biofilter/Sump; Pumpenmodule an den Tanks | Lage, Kegelboden, Fittings an der Spitze | `data/system.json` |
| D07 | 29.10. | Fischart und Klima | Tilapia / Forelle | beide als Variante rechnen (`fish_species`), Standard Tilapia | Standort unbekannt, NGO entfernte Regionen eher warm; Forelle bei kaltem Flusswasser | `fish_species` |
| D08 | 29.10. | Pool-Wassertiefe | 0,5 m / tiefer | 0,5 m (Wasserspiegel Z 515, Boden Z 0) | OBJ-Wasserscheibe bei Z 515 | `pool_depth` |
| D09 | 29.10. | Strebenprofil | OBJ 30x30 beibehalten / groesser | im Modell 30x30 (Treue zum OBJ), Statik meldet "zu schwach bei Schnee", Vorschlag groesseres Profil | Ben-Quelle ist das OBJ | `strut_profile` |
| D10 | 29.10. | Hub-Variante (vorlaeufig) | A flachgedrueckt, B geschweisst, C Huelse, D Holz | C (Rohrhuelsen an Mittelplatte) als Modellvorgabe, bis R02 entschieden | Rohr bleibt rund, kein Flachdruck, einfach genug | `hub_variant` |
| D11 | 29.10. | Zulaufrohr | durch die Kuppel / aussen | nur aussen, bis zur Wand; Innenanschluss als Schlauch aus dem Graphen | Bilder, Bens Hinweis (blauer Stab) | Teil `T10` |
| D12 | 29.10. | Bauweise | lose Koerper / Komponenten | wiederkehrende Bauteile als Komponenten, Platzierung aus `layout.json` | Bens Wunsch: eine Aenderung wirkt ueberall | - |
