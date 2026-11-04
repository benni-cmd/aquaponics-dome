# Modell-Inventar (erzeugt, nicht von Hand)

Erzeugt von `scripts/model_inventar.py` (`python -X utf8 scripts/model_inventar.py`). Quelle: `viewer/instances.json` (Stand 2026-11-04 10:36:15), `designs/components/*.sc` je `solidcraft-cli eval`.

- Definitionen im Modell: **164** (davon ohne gleichnamige `.sc`: 0)
- Instanzen gesamt: 4914
- `.sc`-Dateien insgesamt: 316; davon ohne Instanz im Modell: **152**
- Eingesetzte Komponenten mit Werkstoff `Default` ausser Ausnahmeliste: **8**
- Eingesetzte Komponenten mit Werkstoff `Default` in der Ausnahmeliste: 1 (erdflaeche)
- Eingesetzte Komponenten mit unbenannten Koerpern `Body<n>`: 0

## Ausnahmeliste Werkstoff `Default`

- `mensch_referenz`: Menschfigur (Massstab, kein Bauteil)
- `erdflaeche`: Erde mit Grund (Bodenflaeche, kein Kaufteil)

## Komponenten ohne Instanz im Modell

| Datei | Koerper | Werkstoffe |
|---|---|---|
| `aktivkohle_station.sc` | 43 | AK Konsole (1), AK PP (2), AK Kopf (5), AK Komposit (2), AK Kohle (2), AK PVC (16), AK Hahn (12), AK Messing (3) |
| `becken_dritt.sc` | 2 | Default (2) |
| `geblaese_luft.sc` | 10 | GL Pumpe (1), GL Fuss (4), GL Kabel (1), GL PVC (3), GL Hahn (1) |
| `halter_box.sc` | 9 | PS grau (1), Acryl klar (1), Stahl verzinkt (3), PA schwarz (4) |
| `halter_druck.sc` | 2 | PVC grau (1), Edelstahl (1) |
| `halter_hahn.sc` | 3 | PVC grau (2), PVC blau (1) |
| `halter_inline_d32.sc` | 6 | PVC blau (2), PVC grau (3), Edelstahl (1) |
| `halter_inline_d50.sc` | 6 | PVC blau (2), PVC grau (3), Edelstahl (1) |
| `halter_mast.sc` | 3 | Stahl verzinkt (1), PVC grau (1), PP weiss (1) |
| `halter_zelle.sc` | 4 | PVC grau (3), PVC blau (1) |
| `haut_paneel_AAB.sc` | 1 | Polycarbonat (1) |
| `haut_paneel_BBB.sc` | 1 | Polycarbonat (1) |
| `haut_paneel_BBB_tuer.sc` | 1 | Polycarbonat (1) |
| `haut_profil.sc` | 1 | Aluminium (1) |
| `ibc_beet_aussen_933.sc` | 40 | HDPE weiss (1), PP grau (25), Medium Blaehton (1), PVC grau Beet (12), V2A Lochblech (1) |
| `ibc_beet_aussen_993.sc` | 0 | nicht ausgewertet (Zeit) (0) |
| `keilschiene.sc` | 3 | Schaumband EPDM (1), Aluminium Keilschiene (1), Federstahl Keilschiene (1) |
| `knoten_4.sc` | 22 | Stahl Knoten (22) |
| `knoten_5.sc` | 26 | Stahl Knoten (26) |
| `knoten_6.sc` | 31 | Stahl Knoten (31) |
| `lt_bogen45_d110.sc` | 1 | LT pvc (1) |
| `lt_bogen45_d20.sc` | 1 | LT pvc (1) |
| `lt_bogen45_d25.sc` | 1 | LT pvc (1) |
| `lt_bogen45_d32.sc` | 1 | LT pvc (1) |
| `lt_bogen45_d40.sc` | 1 | LT pvc (1) |
| `lt_bogen45_d75.sc` | 1 | LT pvc (1) |
| `lt_bogen90_d110.sc` | 1 | LT pvc (1) |
| `lt_bogen90_d20.sc` | 1 | LT pvc (1) |
| `lt_kabeleinfuehrung_dn100.sc` | 3 | LT pp (2), LT epdm (1) |
| `lt_kabeleinfuehrung_dn50.sc` | 3 | LT pp (2), LT epdm (1) |
| `lt_kappe_d20.sc` | 1 | LT pvc (1) |
| `lt_kappe_d50.sc` | 1 | LT pvc (1) |
| `lt_klemme_d110.sc` | 4 | LT stahl (4) |
| `lt_klemme_d20.sc` | 4 | LT stahl (4) |
| `lt_klemme_d25.sc` | 4 | LT stahl (4) |
| `lt_klemme_d32.sc` | 4 | LT stahl (4) |
| `lt_klemme_d40.sc` | 4 | LT stahl (4) |
| `lt_klemme_d50.sc` | 4 | LT stahl (4) |
| `lt_klemme_d63.sc` | 4 | LT stahl (4) |
| `lt_kugelhahn_d110.sc` | 3 | LT hahn (3) |
| `lt_kugelhahn_d20.sc` | 3 | LT hahn (3) |
| `lt_kugelhahn_d25.sc` | 3 | LT hahn (3) |
| `lt_kugelhahn_d32.sc` | 3 | LT hahn (3) |
| `lt_kugelhahn_d40.sc` | 3 | LT hahn (3) |
| `lt_kugelhahn_d50.sc` | 3 | LT hahn (3) |
| `lt_kupplung_d110.sc` | 1 | LT pvc (1) |
| `lt_kupplung_d20.sc` | 1 | LT pvc (1) |
| `lt_kupplung_d25.sc` | 1 | LT pvc (1) |
| `lt_kupplung_d32.sc` | 1 | LT pvc (1) |
| `lt_kupplung_d63.sc` | 1 | LT pvc (1) |
| `lt_kupplung_d75.sc` | 1 | LT pvc (1) |
| `lt_leerrohr_bogen45_dn100.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_bogen45_dn50.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_bogen90_dn100.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_bogen90_dn50.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_dn100.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_dn50.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_red_dn100_dn50.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_t_dn100.sc` | 1 | LT leerrohr (1) |
| `lt_leerrohr_t_dn50.sc` | 1 | LT leerrohr (1) |
| `lt_reduzierung_d110_d63.sc` | 1 | LT pvc (1) |
| `lt_reduzierung_d25_d20.sc` | 1 | LT pvc (1) |
| `lt_reduzierung_d32_d25.sc` | 1 | LT pvc (1) |
| `lt_reduzierung_d40_d20.sc` | 1 | LT pvc (1) |
| `lt_reduzierung_d40_d32.sc` | 1 | LT pvc (1) |
| `lt_rohr_d110.sc` | 1 | LT pvc (1) |
| `lt_rohr_d20.sc` | 1 | LT pvc (1) |
| `lt_rohr_d25.sc` | 1 | LT pvc (1) |
| `lt_rohr_d32.sc` | 1 | LT pvc (1) |
| `lt_rohr_d40.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L1184.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L1212.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L1228.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L1287.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L1451.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L2417.sc` | 1 | LT pvc (1) |
| `lt_rohr_d50_L258.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L1003.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L109.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L1316.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L139.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L1574.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L188.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L198.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L220.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L238.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L261.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L278.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L372.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L419.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L439.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L712.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L78.sc` | 1 | LT pvc (1) |
| `lt_rohr_d63_L913.sc` | 1 | LT pvc (1) |
| `lt_rohr_d75.sc` | 1 | LT pvc (1) |
| `lt_rueckschlagventil_d20.sc` | 1 | LT hahn (1) |
| `lt_rueckschlagventil_d25.sc` | 1 | LT hahn (1) |
| `lt_rueckschlagventil_d40.sc` | 1 | LT hahn (1) |
| `lt_schacht_kugelhahn_d63.sc` | 4 | LT pehd (2), LT epdm (2) |
| `lt_schelle_vk_d32.sc` | 11 | LT stahl (11) |
| `lt_schelle_vk_d63.sc` | 11 | LT stahl (11) |
| `lt_schlauch_id16.sc` | 1 | LT hellblau (1) |
| `lt_schlauch_id16_L100.sc` | 1 | LT hellblau (1) |
| `lt_schlauch_id25.sc` | 1 | LT dunkelblau (1) |
| `lt_schlauchbogen90_id16.sc` | 1 | LT hellblau (1) |
| `lt_schlauchbogen90_id25.sc` | 1 | LT dunkelblau (1) |
| `lt_schlauchschelle_id16.sc` | 2 | LT stahl (2) |
| `lt_schlauchschelle_id25.sc` | 2 | LT stahl (2) |
| `lt_t_d110.sc` | 1 | LT pvc (1) |
| `lt_t_d20.sc` | 1 | LT pvc (1) |
| `lt_t_d25.sc` | 1 | LT pvc (1) |
| `lt_t_d32.sc` | 1 | LT pvc (1) |
| `lt_t_d40.sc` | 1 | LT pvc (1) |
| `lt_uebergang_pe_pvc_d20.sc` | 3 | LT pp (2), LT pom (1) |
| `lt_verteiler_d32_n2.sc` | 1 | LT pvc (1) |
| `lt_verteiler_d32_n3.sc` | 1 | LT pvc (1) |
| `lt_verteiler_d32_n4.sc` | 1 | LT pvc (1) |
| `lt_verteiler_d50.sc` | 1 | LT pvc dunkelblau (1) |
| `luftverteiler_6.sc` | 0 | nicht ausgewertet (Zeit) (0) |
| `mensch_referenz.sc` | 14 | Weste orange (1), Haut (3), Kleidung blau (8), Geraet dunkel (2) |
| `nft_rinne.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_aussen_r1.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_aussen_r2.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_aussen_r3.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_aussen_r4.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_innen_r1.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_innen_r2.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_k_a.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_k_b.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_l_a.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_l_b.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_m_a.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_m_b.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_mitte_r1.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_mitte_r2.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_mitte_r3.sc` | 3 | PVC-U weiss (3) |
| `nft_rinne_mitte_r4.sc` | 3 | PVC-U weiss (3) |
| `pflanztisch.sc` | 1 | Default (1) |
| `puffer_ibc.sc` | 77 | HDPE Palette (4), Stahl verzinkt (62), PE Blase (2), PVC grau (6), PVC blau (2), Wasser (1) |
| `puffer_station.sc` | 230 | Stahl verzinkt (182), PVC grau (13), Becher PP (1), Kanal PVC (5), Sonde (4), Blech (3), Kanister HDPE (2), Pumpe Schlauch (2), HDPE Palette (8), PE Blase (4), PVC blau (4), Wasser (2) |
| `schrank_einfuehrung.sc` | 10 | SE Blech (2), Default (8) |
| `sonde_co2_scd41.sc` | 1 | Platine gruen (1) |
| `sonde_druck_schalter.sc` | 1 | Edelstahl (1) |
| `sonde_flow_12.sc` | 1 | Sonde schwarz (1) |
| `sonde_flow_gross.sc` | 1 | Sonde schwarz (1) |
| `sonde_par.sc` | 1 | Sonde gelb (1) |
| `sonde_strom_ct.sc` | 1 | Sonde schwarz (1) |
| `tuer.sc` | 9 | Default (9) |
| `tuer_zarge_planenausschnitt.sc` | 3 | Aluminium Zarge (2), EPDM Dichtband Zarge (1) |
| `winkelhalter.sc` | 7 | Stahl verzinkt (7) |

## Eingesetzte Komponenten

| Komponente | Instanzen | Koerper | Masse kg | Werkstoffe | Default | Body<n> |
|---|---:|---:|---:|---|---:|---:|
| `becken_dritt_klein` | 1 | 6 | 949.3 | Beton (1), Wasser (1), Stutzen PVC (4) | 0 | 0 |
| `erdflaeche` | 1 | 1 | 701782.1 | Default (1) | 1 | 0 |
| `feinfilter` | 2 | 55 | 40.5 | Stahl verzinkt Feinfilter (20), PP Feinfilter (3), Edelstahl Feinfilter (19), Netz Edelstahl Feinfilter (1), EPDM Feinfilter (1), PVC Feinfilter (11) | 0 | 0 |
| `fundamentanker` | 10 | 12 | 240.2 | Beton C25 (1), Stahl Anker (11) | 0 | 0 |
| `fundamentring` | 1 | 1 | 2810.7 | Default (1) | **1** | 0 |
| `halter_beruhig` | 2 | 5 | 1.2 | PVC grau (3), Stahl verzinkt (2) | 0 | 0 |
| `halter_tauch` | 3 | 3 | 1.8 | PVC grau (1), PA schwarz (1), Stahl verzinkt (1) | 0 | 0 |
| `huelle_folie_AAB` | 30 | 2 | 1.7 | PE Folie (2) | 0 | 0 |
| `huelle_folie_BBB` | 9 | 2 | 2.0 | PE Folie (2) | 0 | 0 |
| `huelle_folie_BBB_tuer` | 1 | 2 | 1.4 | PE Folie (2) | 0 | 0 |
| `ibc_beet_aussen_800` | 8 | 40 | 580.9 | HDPE weiss (1), PP grau (25), Medium Blaehton (1), PVC grau Beet (12), V2A Lochblech (1) | 0 | 0 |
| `ibc_beet_innen_933` | 6 | 31 | 469.0 | HDPE weiss (1), PP grau (16), Medium Blaehton (1), PVC grau Beet (12), V2A Lochblech (1) | 0 | 0 |
| `knoten_4_n17` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n18` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n19` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n20` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n21` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n22` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n23` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n24` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n25` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_4_n26` | 1 | 22 | 6.1 | Stahl Knoten (22) | 0 | 0 |
| `knoten_5_n02` | 1 | 26 | 5.7 | Stahl Knoten (26) | 0 | 0 |
| `knoten_5_n04` | 1 | 26 | 5.7 | Stahl Knoten (26) | 0 | 0 |
| `knoten_5_n06` | 1 | 26 | 5.7 | Stahl Knoten (26) | 0 | 0 |
| `knoten_5_n08` | 1 | 26 | 5.7 | Stahl Knoten (26) | 0 | 0 |
| `knoten_5_n12` | 1 | 26 | 5.7 | Stahl Knoten (26) | 0 | 0 |
| `knoten_5_n15` | 1 | 26 | 5.7 | Stahl Knoten (26) | 0 | 0 |
| `knoten_6_n01` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n03` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n05` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n07` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n09` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n10` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n11` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n13` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n14` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `knoten_6_n16` | 1 | 31 | 6.0 | Stahl Knoten (31) | 0 | 0 |
| `lt_bogen45_d50` | 3 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_bogen45_d63` | 4 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_bogen90_d25` | 16 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_bogen90_d32` | 8 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_bogen90_d40` | 14 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_bogen90_d50` | 19 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_bogen90_d63` | 7 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_bogen90_d75` | 8 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `lt_kugelhahn_d63` | 2 | 3 | 0.4 | LT hahn (3) | 0 | 0 |
| `lt_kupplung_d40` | 2 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_kupplung_d50` | 7 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_reduzierung_d50_d32` | 2 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_reduzierung_d50_d40` | 6 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_reduzierung_d63_d50` | 8 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_reduzierung_d75_d50` | 2 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_reduzierung_d75_d63` | 6 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L1671` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L2304` | 1 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L2353` | 4 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L2794` | 1 | 1 | 0.5 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L51` | 2 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L58` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L59` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d25_L941` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d32_L245` | 2 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d32_L471` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d32_L633` | 2 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d32_L83` | 2 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d32_L94` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L1021` | 4 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L1025` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L105` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L1157` | 1 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L140` | 2 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L304` | 2 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L547` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L557` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L857` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L96` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d40_L99` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L1211` | 1 | 1 | 0.6 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L1229` | 1 | 1 | 0.6 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L1260` | 1 | 1 | 0.6 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L130` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L151` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L1540` | 1 | 1 | 0.8 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L1543` | 1 | 1 | 0.8 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L1660` | 1 | 1 | 0.8 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L169` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L180` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L186` | 4 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L2035` | 2 | 1 | 1.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L208` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L2282` | 1 | 1 | 1.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L2311` | 1 | 1 | 1.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L239` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L271` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L277` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L312` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L365` | 2 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L396` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L475` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L481` | 2 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L488` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L55` | 1 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L62` | 4 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L694` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L906` | 1 | 1 | 0.5 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d50_L94` | 2 | 1 | 0.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L102` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L1313` | 1 | 1 | 1.0 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L143` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L192` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L195` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L199` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L223` | 1 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L337` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L361` | 2 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L455` | 1 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L708` | 1 | 1 | 0.6 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L72` | 2 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L75` | 6 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d63_L93` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L116` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L265` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L301` | 1 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L390` | 2 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L410` | 2 | 1 | 0.5 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L65` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L72` | 1 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L88` | 8 | 1 | 0.1 | LT pvc (1) | 0 | 0 |
| `lt_rohr_d75_L918` | 1 | 1 | 1.0 | LT pvc (1) | 0 | 0 |
| `lt_t_d50` | 3 | 1 | 0.2 | LT pvc (1) | 0 | 0 |
| `lt_t_d63` | 4 | 1 | 0.3 | LT pvc (1) | 0 | 0 |
| `lt_t_d75` | 4 | 1 | 0.4 | LT pvc (1) | 0 | 0 |
| `luft_scheibenbelueftung` | 4 | 4 | 1.5 | LV PP (3), LV EPDM (1) | 0 | 0 |
| `luftverteiler_4` | 1 | 1 | 0.5 | LV PVC (1) | 0 | 0 |
| `mensch_referenz_arbeiten` | 1 | 14 | 80.0 | Weste orange (1), Haut (3), Kleidung blau (8), Geraet dunkel (2) | 0 | 0 |
| `mensch_referenz_messen` | 1 | 15 | 80.2 | Weste orange (1), Haut (3), Kleidung blau (8), Geraet dunkel (3) | 0 | 0 |
| `netztopf` | 2222 | 1 | 0.0 | PP (1) | 0 | 0 |
| `nft_tisch_innen` | 10 | 54 | 16.4 | Stahl verzinkt (42), PVC blau (2), Schlauch hellblau (2), PVC grau (2), Default (6) | **6** | 0 |
| `pool_zentral` | 1 | 5 | 41775.0 | Default (5) | **5** | 0 |
| `puffer_klein` | 1 | 32 | 43.8 | Stahl verzinkt (21), PA schwarz (1), HDPE blau (3), Acryl klar (2), PP schwarz (1), Kanister HDPE (2), Pumpe Schlauch (2) | 0 | 0 |
| `pumpe_gross` | 4 | 15 | 8.7 | PP Tafel (1), Stahl Pumpe (8), Pumpe blau (1), PVC grau Pumpe (3), Kabel schwarz (2) | 0 | 0 |
| `pumpe_klein` | 4 | 15 | 5.4 | PP Tafel (1), Stahl Pumpe (8), Pumpe blau (1), PVC grau Pumpe (3), Kabel schwarz (2) | 0 | 0 |
| `salatkopf` | 2222 | 98 | 0.0 | Salat (98) | 0 | 0 |
| `schaltschrank` | 1 | 1 | 619.2 | Default (1) | **1** | 0 |
| `schwimmerventil_pool` | 1 | 5 | 0.4 | SV PVC (1), SV PP (3), SV Kugel (1) | 0 | 0 |
| `sonde_do_ind` | 1 | 1 | 0.1 | Sonde blau (1) | 0 | 0 |
| `sonde_do_mini` | 3 | 1 | 0.0 | Sonde blau (1) | 0 | 0 |
| `sonde_ec` | 1 | 1 | 0.0 | Sonde grau (1) | 0 | 0 |
| `sonde_leck` | 3 | 1 | 0.0 | Kontakt rot (1) | 0 | 0 |
| `sonde_level_druck` | 1 | 1 | 0.3 | Edelstahl (1) | 0 | 0 |
| `sonde_level_float` | 3 | 1 | 0.0 | Schwimmer orange (1) | 0 | 0 |
| `sonde_ph` | 3 | 1 | 0.0 | Sonde grau (1) | 0 | 0 |
| `sonde_temp_ds` | 2 | 1 | 0.0 | Edelstahl (1) | 0 | 0 |
| `strebe_a` | 30 | 1 | 24.7 | Default (1) | **1** | 0 |
| `strebe_b` | 34 | 1 | 28.3 | Default (1) | **1** | 0 |
| `tank_klein` | 2 | 33 | 37.4 | PE Tank (2), PVC grau Tank (5), Ventil blau (1), Stahl verzinkt (25) | 0 | 0 |
| `tuer_komplett` | 1 | 27 | 38.7 | Stahl verzinkt (22), Tuerblatt Sandwich (1), EPDM schwarz (4) | 0 | 0 |
| `zulaufrohr` | 1 | 1 | 130.1 | Default (1) | **1** | 0 |
| `zweitbecken` | 1 | 2 | 3559.6 | Default (2) | **2** | 0 |

## Nicht ausgewertet (eval ueber 90 s)

- `nft_tisch_aussen` (8 Instanzen)
- `nft_tisch_mitte` (6 Instanzen)
- `tank_gross` (1 Instanzen)
- `tank_gross_t3` (1 Instanzen)
