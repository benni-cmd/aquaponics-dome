# Integrations-Board (Besitzer: Orchestrator; Stand 31.10.2026 12:30)

Status je Bauteilklasse: `offen` · `in Arbeit` · `L2` · `L3` · `abgenommen` (Orchestrator hat Stichprobe gemacht) · `eingebaut` (Montage hat es im Dom verknuepft).
Zustaendig: I = Integrator/Montage, W = Werkstatt. Quelle der Anzahl: `data/layout.json`, `viewer/instances.json` (Build 51).

| Klasse | Anzahl | Zustaendig | Status | Datei | Letzte Meldung |
|---|---|---|---|---|---|
| Salatkopf | 1634 (Modell) | W | eingebaut, Einheitsmodell; Artenmodelle zuletzt (D27) | `designs/components/salatkopf.sc` | 31.10. Orchestrator: Innenbeete (6) tragen noch keine Toepfe (Befund), Zaehlung gegen system_specs abgleichen |
| Netztopf | 1634 (960 Aussenbeete + 674 NFT) | W | eingebaut | `designs/components/netztopf.sc` | 31.10. Orchestrator: Innenbeete ohne Toepfe, Specs zaehlen 2160 Beet-Toepfe (Abweichung, D52) |
| NFT-Rinne (aussen 4 Rinnen, Mitte 4, innen 2) | 76 | W | abgenommen (W24/W25a, check_nft_fit 48/48) | `designs/components/nft_rinne.sc` (+Varianten) | 31.10. Werkstatt: aussen4 Standard, 674 Toepfe |
| NFT-Tisch aussen (8), Mitte (6), innen (10) | 24 | W | eingebaut (Runde 51), Pruefer W17/W18/W25 gelaufen | `designs/components/nft_tisch_*.sc` | 31.10. Werkstatt: check_nft_tisch aussen 79/79 |
| IBC-Beet aussen (8), innen (6) | 14 | W | eingebaut, Innenbeet-Fase 120 (W26, D44) | `designs/components/ibc_beet_*.sc` | 31.10. Werkstatt: Beet x Beet +36 mm |
| Tank klein (Absetzer) | 2 | W | eingebaut, Stand verkleinert (W30, Plattform 619) | `designs/components/tank_klein.sc` | 31.10. Werkstatt: check_tank 114/114 |
| Tank gross (Biofilter) | 2 | W | eingebaut, Stand verkleinert (W30, Plattform 821) | `designs/components/tank_gross.sc` | 31.10. Werkstatt: Pumpentafeln jetzt seitlich (D51) |
| Pumpe (4 gross = Hauptkreislauf, 4 klein = Absetzer-Teilstrom, D38) | 8 | W | eingebaut, Blatt nach D38 (W25) | `designs/components/pumpe.sc` | 31.10. Werkstatt: Tafeln seitlich am Stand setzen (Montage, M10) |
| Puffer klein (T82: Fass 120 l, Messzelle 20 l, Kanister 20 l; 0,16 m3, Standard seit D66/D70) | 1 | W/I | eingebaut (M-SETZEN Runde 60), Lage r 2764 / Azimut -51 | `designs/components/puffer_klein.sc` | 01.11. Montage: Vorbau entfaellt (D70); Specs auf Puffer klein umgestellt (S01) |
| Puffer-Station (T81: 2 IBC gestapelt, Messplatz, Dosierkonsole), Variante | 1 | W/I | aus (Schalter `station_an` 0), Lage D48/D49 bleibt hinterlegt | `designs/components/puffer_station.sc` | 01.11. Montage: ersetzt durch Puffer klein (D70); als Variante erhalten |
| Drittbecken klein (T14k, Quarantaene, Wasser Ø 800 x 800 = 0,40 m3) | 1 | I | eingebaut (M-SETZEN Runde 60), Lage r 4966 / Azimut -30, Mass von Ben zu bestaetigen | `designs/components/becken_dritt_klein.sc` | 01.11. Montage: ersetzt Drittbecken Ø 1030 (D66/D70); Specs auf 0,40 m3 (S01) |
| Mensch-Referenz (1,80 m, messen/arbeiten) | 2 | W/I | eingebaut (M9), nicht in check_latte | `designs/components/mensch_referenz_*.sc` | 31.10. Montage: Build 51 |
| Strebe A / B | 30 / 34 | I | eingebaut (B 34: Tuerfeld teilt die Basisstrebe) | `designs/components/strebe_*.sc` | 31.10. Montage |
| Knoten 4/5/6-wertig (Kugel mit Steckarmen, D15) | 10 / 6 / 10 | W | eingebaut (26), 135/135 | `designs/components/knoten_*.sc` | 31.10. Montage: Querbolzen x Strebe 517 offen (Bohrungen) |
| Tuer komplett (Feld BBB 149,2, D36) | 1 | W/I | eingebaut (M3), check_tuer 30/30 | `designs/components/tuer_komplett.sc` | 31.10. Montage: Neigung 10,81 Grad |
| Fundamentanker, Fundamentring, Erdflaeche | 10 / 1 / 1 | W/I | eingebaut | | 31.10. Montage |
| Pool zentral, Zweitbecken | 2 | I | eingebaut (zentriert D35, Zweitbecken auf Tuerachse D36) | | 31.10. Montage |
| Feinfilter (R28, D51) | 2 | W | in Arbeit (W31) | `designs/components/feinfilter.sc` | 31.10. Orchestrator: Auftrag an Werkstatt-3 |
| Huelle als Plane (Keilschiene, Folie, Zargenanschluss, D39) | 65 / 40 / 1 | W | in Arbeit (W27 nach W31); Haut-Paneel ruht als Variante | | 31.10. Orchestrator |
| Rohrnetz, Schlaeuche, Kabel (M10) | - | I | offen: Plan vorab, Netzliste `data/leitungsnetz.json` liegt vor | | 31.10. Orchestrator: nach W31/W27 |
