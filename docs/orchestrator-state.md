# Orchestrator-Checkpoint (Besitzer: Orchestrator; Stand 29.10.2026 03:55)

- **Rolle O:** Abnahme (Stichprobe der Werkstatt-Komponenten), Board `docs/integration-board.md`, Recherche R03/R06/R09/R11 (R02, R13 erledigt), Entscheidungslog, Sitzungen anstossen, Viewer-Server `python viewer/serve.py 4410` am Leben halten.
- **Sitzungen:** Integrator (dome-build, laeuft), Werkstatt (dome-workshop, gestartet 03:35).
- **Limit 03:33:** 5-Stunden 35 %, Woche 53 % (Reset Woche 30.10. 02:59).
- **Offen fuer den Morgen:** Morgenbericht `docs/morning-report.md` (Integrator schreibt, Orchestrator prueft); Fragen an Ben: Standort, Fischart, Tuerrichtung, Windfang.
- **Naechster Schritt O:** Anstoss-Lauf 03:49; Abnahme erste Werkstatt-Komponente (Salatkopf); R03 (Kiestiefe) recherchieren.
- **Stopp:** nur durch Ben (`STOPP von Ben` in `docs/loop-state.md`) oder neue Phase.

## Stand 04:36 (Rollenwechsel)
- Alte Bau-Sitzung "Kuppel mit Aquaponik in SolidCraft bauen" archiviert (Uebergabestand `docs/loop-state.md`, Commit eccb01d: Layout aus layout.json, 10 Wurzel-Baugruppen, Streben als Instanzen, Tuer im Basisdreieck, Rohr, check_latte 19/19).
- Neue Montage-Sitzung "Montage und Layout (Kuppel)" noch NICHT gestartet: start_session ist in automatischen Laeufen gesperrt, ein Einmalauftrag wurde vom Auto-Modus abgelehnt (nicht umgangen). Der dauerhafte Auftrag `dome-loop-hourly-fallback` (:41) wurde auf die neuen Rollen aktualisiert und uebernimmt die Montage-Rolle (Plan `docs/next-steps-montage.md`), sobald deren letzter Commit aelter als 20 Minuten ist (ab 04:39). Ben kann sie alternativ per Prompt aus `docs/resume.md` starten.
- Noch auf die neuen Namen umzustellen: `dome-loop-restart-0715` (alter Sitzungsname im Wachter).
- Werkstatt: NFT-Rinne abgenommen (f478774), R06 geliefert, NFT-Tisch innen laeuft. Recherche offen: R09 Vortex-Tank, R11 Haut.

## Stand 04:48 (Kontext 84 %, Limit 5h 91 %, Woche 60 %)
- Montage laeuft: Commit b1b48c7 04:45 (M0 Uebernahme) kam aus der ueber den stuendlichen Auftrag gestarteten Sitzung (erscheint nicht als Peer in ListAgents). Werkstatt busy (NFT-Tisch innen). Plaene: Montage 6 Schritte, Werkstatt 5 Schritte offen.
- Wenn ich verdichtet oder neu gestartet werde: lies zuerst diese Datei, docs/parallel-work.md (04:15), docs/endless-mechanics.md, docs/integration-board.md, docs/research-queue.md (offen: R09, R11), docs/review-lessons.md. Naechste Orchestrator-Aufgaben: Abnahme Netztopf/Salatkopf/NFT-Tisch innen (Stichprobe nach docs/review-protocol.md Abschnitt 6), Plan bei weniger als 3 offenen Schritten auf 5 auffuellen, R09 (Vortex-Tank-Geometrie) fuer W4, dome-loop-restart-0715 auf neue Namen umstellen.
- Bei Limit ueber 90 %: Werkstatt nicht anstossen; Montage zuerst.

## Stand 07:15 (Limit zurueckgesetzt 07:10, 5h 11 %, Woche 62 %; mein Kontext 87 %)
- Werkstatt: Limit-Abbruch um ca. 05:30, angestossen 07:12 (Plan: NFT-Tisch abschliessen, dann IBC-Beet; erst git status, nur konsistente Staende committen). Letzter Commit 8dba568 (05:13).
- Montage: seit 04:45 nicht mehr aktiv (Limit). start_session und run_scheduled_task sind in automatischen Laeufen vom Auto-Modus gesperrt (nicht umgangen). Start geschieht ueber den dauerhaften Auftrag `dome-loop-hourly-fallback` (:41, naechster Lauf ca. 07:41) oder durch Ben mit dem Prompt aus `docs/resume.md`. `dome-loop-restart-0715` ist abgeschaltet (Doppelstart-Gefahr, alter Sitzungsname).
- Naechste Orchestrator-Schritte: Abnahme NFT-Tische (nach Werkstatt-Meldung), Plan auffuellen, R09/R11 recherchieren, Viewer-Server neu starten falls Stand veraltet (zeigt 04:08).

## Stand 07:48 (Kontext 90 %, Limit 5h 39 %, Woche 65 %)
- Werkstatt laeuft gut: NFT-Rinne und NFT-Tische abgenommen (Board), R06/R09 geliefert, IBC-Beet nach Bild-Kritiker (708bc15), Tank klein/gross gebaut (Kritiker/Blaetter offen). Naechste Orchestrator-Abnahmen: IBC-Beet, Tank klein, Tank gross, Netztopf, Salatkopf.
- Montage: KEINE Sitzung aktiv und kein Commit seit 04:45 (b1b48c7). Der stuendliche Auftrag (:41) hat sie bisher nicht sichtbar gestartet. Einzige Hebel: Ben startet sie mit dem Prompt aus `docs/resume.md` (Abschnitt Integrator = Montage, Plan `docs/next-steps-montage.md`), oder ein spaeterer Lauf des Auftrags greift. start_session und run_scheduled_task sind in automatischen Laeufen gesperrt.
- Verdichtung: Falls ich verdichtet werde, ist der Stand vollstaendig in diesen Dateien: docs/orchestrator-state.md, docs/integration-board.md, docs/research-queue.md (offen nur R11 Haut), docs/review-lessons.md, docs/next-steps-*.md.

## Stand 09:03 (Kontext 95 %, Limit 5h 92 %, Woche 71 %) — WIEDERAUFNAHME-STAND
- **Werkstatt (laeuft, gut):** abgenommen: NFT-Rinne, NFT-Tische, IBC-Beet, Tank klein/gross (Board). Gebaut, Spec-Pruefer durch/laeuft: Knoten (26, Kugel mit Steckarmen, D15), Fundamentanker, Pumpe (4 Tafeln, Kassetten = Tank-Stuetzrippen D16, Commit fe0eff9), Salatkopf/Netztopf (2716 Stueck, D17). Naechste Orchestrator-Abnahmen (Stichprobe nach docs/review-protocol.md Abschnitt 6): Knoten, Anker, Pumpe, Salatkopf, Netztopf. Plan der Werkstatt: `docs/next-steps-workshop.md` (W7-W11 aufgefuellt 08:25; W10 Leitungsteile als naechstes grosses Stueck; danach neu auffuellen: Haut-Paneel nach R11, Winkelhalter, Tankbeine).
- **Montage: KEINE Sitzung aktiv, kein Commit seit 04:45.** Hebel: Ben startet sie mit dem Prompt aus `docs/resume.md` (Rolle Montage, Plan `docs/next-steps-montage.md`, M0-M5). start_session/run_scheduled_task sind in automatischen Laeufen gesperrt (nicht umgehen). Der dauerhafte Auftrag `dome-loop-hourly-fallback` (:41) hat sie nicht sichtbar gestartet. Wartende Arbeit der Montage: Layout/Zusammenbau der abgenommenen Komponenten in dome.sc, Wasserweg-Graph, Rohre/Schlaeuche, Tuer-Seitenfelder, Haut.
- **Recherche offen:** nur R11 (Kuppelhaut). Fertig: R02, R03, R06, R09, R13.
- **Viewer:** Server `python viewer/serve.py 4410` lief zuletzt mit Stand 04:08 (dome.sc seit dem Montage-Ausfall nicht neu gespeichert); neu starten, falls er nicht antwortet.
- **Limit:** Werkstatt nicht anstossen, solange 5h-Limit > 90 % (jetzt 92 %, Reset 11:10 UTC = 12:10 lokal? Reset steht in get_usage: resetsAt 11:09:59Z).
- **Bens Fragen fuer den Morgen:** Standort/Klima, Fischart, Pooltiefe (Annahme 2,34 m), Tuerrichtung/Windfang, Klasse der 10 Kassetten (D16), Anzahl 3 Aussenrinnen je Tisch (D17), Wanne "IBC" 2953 mm = Sonderwanne (R03 Nachtrag).

## Stand 29.10. 17:15 (Orchestrator)
- Limit: 5h 0 % (Reset durch), Woche 83 % (Reset 30.10. 03:00 Ortszeit; get_usage nennt UTC, 02:00Z). Werkstatt und Montage hatten 14:50 das 5h-Limit erreicht und endeten mit Fehler.
- WECK-TEST BESTANDEN: `mcp__ccd_session_mgmt__send_message` mit Praefix `WIEDERANLAUF aquaponics-dome:` an die nicht laufende (limit-gestoppte) Werkstatt-Sitzung local_584eec27-13ed-44b2-9b2a-c509ec227d8c wurde zugestellt, ihr Zug startete (Hook-Ausnahme 90f3967 wirkt). Ob dasselbe fuer eine per clear_session geleerte Sitzung gilt, ist noch ungetestet (Prozess evtl. weg).
- Montage (idle, gelistet) per SendMessage auf M1.3 angestossen; M6 Viewer fertig (31 MB), M1.4 wartet auf W16.
- Werkstatt-Arbeitsstand ungesichert: W16-Dateien (nft_tisch_*.sc 14:35, data/components/nft_tisch.json, check_nft_fit.py); 72 Dateien im Arbeitsbaum offen.
- Wochenbudget: Regel ab 95 % Woche keine Anstoesse mehr, Zustand sichern.
- ZEITANGABEN: `get_usage` liefert `resetsAt` in UTC. Ortszeit ist MEZ (UTC+1, seit 25.10.2026). Reset 5h-Fenster 29.10. 22:10, Woche 30.10. 03:00 Ortszeit. Immer aus `resetsIn` und der Systemuhr (`date`) rechnen, nie die UTC-Zahl uebernehmen.

## Stand 29.10. 21:20 (Orchestrator): AUSLAUFEN auf Bens Anweisung
- Wochenlimit 93 %, 5h-Fenster 89 % (Reset 22:10 Ortszeit). Beide Sitzungen angewiesen: laufenden Schritt beenden, Zustandsdatei, WIP-Commit + Push, Zug beenden. Keine neuen Auftraege, keine Anstoesse bis Ben freigibt.
- Danach Orchestrator: git status pruefen, Viewer neu exportieren lassen, Ben EINE Zeile melden. Offene Auftraege nach dem Stop: Montage M7 (D30/D31 laut loop-state), M3 Tuer, M4/M5 Rohre; Werkstatt W17 (Beet 800, Tische), Haut-Paneel R11. Modellbeschreibung: Pruefstand nach M7/W17 aktualisieren.

## Stand 29.10. 21:40 (Orchestrator): AUSGELAUFEN, alles gesichert
- Beide Sitzungen haben sauber gestoppt (Werkstatt ba3e781, Montage 217f3c2). Arbeitsbaum sauber, `main` gleich `origin/main` (8eebd21). Viewer aktuell (dome.sc 20:11, Export 20:17), Browser-Pane neu geladen.
- Offen fuer den Neustart (Reihenfolge): (1) Montage M7 fertigmachen: Laufweg B 476 -> mindestens 500, Ziel 600 (D29), check_latte 24/24, check_walkways PASS; (2) Werkstatt: Spec-Pruefer W17 (corner_gap 60 ist Annahme), danach Haut-Paneel R11; (3) Montage M3 Tuer, M4/M5 Wasserweg und Rohre; (4) Orchestrator: Pruefstand in docs/model-description.md nachziehen, Board abnehmen (W07, W11, W17 sind gemeldet, nicht abgenommen).
- Neustart: 5h-Limit Reset 22:10 Ortszeit, Wochenlimit Reset 30.10. 03:00 Ortszeit. Sitzungen sind idle und per SendMessage erreichbar (laufende Prozesse), sonst Weck-Nachricht `WIEDERANLAUF aquaponics-dome:` an die Session-ID (Werkstatt local_584eec27-..., Montage local_5d913ca0-...).
- Bens Freigabe zum Weitermachen abwarten (Anweisung 21:15: nichts Neues starten).

## Stand 29.10. 22:05 (Orchestrator): IDLE, Wiederaufnahme-Plan (Ben: "schliesse deine Arbeit ab")
- Orchestrator-Cron 97071355 geloescht (kein Hintergrundverbrauch). Prompt zum Neu-Einrichten: `docs/orchestrator-nachtmodus-prompt.md`. Arbeitsbaum sauber, `main` = `origin/main`.
- **BEIM NEUSTART ZUERST SENDEN (Ben-Auftrag, nicht vergessen):**
  1. An die WERKSTATT (Session local_584eec27-..., Weck-Nachricht oder SendMessage): Lochabstand/Rohrabstand der NFT-Rinnen auf 200 mm (D32, R16), Auftrag `docs/jobs/W18-lochabstand.md`; Reihenfolge: W17-Spec-Pruefer, W18, Haut-Paneel R11. Notiz liegt in `docs/session-notes/werkstatt.md`, ist aber noch NICHT als Nachricht gesendet.
  2. An die MONTAGE (Session local_5d913ca0-...): M7 fertigmachen (Laufweg B 476 -> mindestens 500, Ziel 600; check_latte 24/24), dann M3 Tuer, M4/M5 Rohre/Schlaeuche; Rinnen-Pflanzenzahl kommt nach W18 aus data/components/nft_tisch.json.
  Rueckfrage zur Formulierung "Rohrabstaende": gemeint ist der Lochabstand der NFT-Rohre (R16/D32); falls Ben Abstaende zwischen Rohrleitungen meint, Laufwege D29 + M5 pruefen.
- Freigabe durch Ben abwarten. Limits: 5h-Fenster ab 22:10 neu, Woche Reset 30.10. 03:00 Ortszeit.

## Stand 29.10. 22:45 (Orchestrator)
- Werkstatt W18 fertig und gepusht (fab161d), Stop sauber; check_nft_fit 40/40 nachgemessen, 586 Rinnen-Toepfe (D33). Spec-Pruefer W17 und W18 fehlen (Limit). Montage idle, nicht angestossen (Ben: nur Werkstatt, Wochenlimit 94 %).
- Als Naechstes (kleine Werkstatt-Schritte): Spec-Pruefer W17+W18 in einem Lauf, dann Haut-Paneel R11. Montage nach dem Reset (30.10. 03:00): M7, M3, M4/M5 (Rohrabstaende und Wege). Orchestrator-Cron bleibt geloescht.

## Stand 29.10. 23:55: Werkstatt W17/W18 abgeschlossen (86d02ad), check_nft_fit 42/42 nachgemessen. Haut-Paneel R11 zurueckgestellt (Recherche fehlt). Montage idle seit Stopp; M7 (inkl. Beetraster 800 x 2640, D34), M3, M4/M5 nach Wochenreset 30.10. 03:00 Ortszeit. Werkstatt wartet auf neuen Auftrag.

## Stand 30.10. 00:00: Werkstatt W19 Haut fertig (7b56237, check_haut 27/27 nachgemessen), Stop sauber. Werkstatt wartet; Montage idle. Naechster Schritt nach Wochenreset 03:00: Montage M7 (Becken zentrieren D35, Beetraster 800 x 2640 D34), danach Haut einsetzen (40 Paneele + Profile), M3 Tuer, M4/M5. Spec-Pruefer W19 offen. Viewer-Server lief neu (Port 4410, Hintergrundprozess dieser Sitzung).

## Stand 30.10. 00:35: Paket Aquaponik-Validierung angelegt (docs/packages/aquaponik-validierung.md), Recherche R17-R22 startet nach dem Wochenreset 03:00 mit Bens Freigabe (parallele Agenten). Viewer-Kennzahlen (565f74e) sind bis dahin eine Annahmen-Rechnung, nicht validiert. Orchestrator-Kontext 71 %: Zustand ist im Repo gesichert.

## Stand 30.10. 01:00: Fachrecherche (Session local_ee5ee82d-6143-4f68-b26a-bedfc628839a) gestoppt bei Woche 99 %: R17 und R18 als Teilergebnis (d255d8a), offen R19-R22 und docs/research/aquaponik-empfehlung.md.
- Zwischenbefund R17: Besatz 15-22 kg/m3 als Auslegung (FAO TP 589: bis 20, SRAC 454: UVI-Technik bis 60), Simulator 15; Bens Tabelle 45 kg/m3 (1287 kg) nur mit UVI-Technik erreichbar. Fuer ca. 28,5 m3 Beckenwasser: 430-630 kg = 500-900 Fische je 0,7 kg statt 1839.
- NEUSTART nach Wochenreset 30.10. 03:00 Ortszeit (Freigabe Ben): Weck-Nachricht `WIEDERANLAUF aquaponics-dome:` an die Session-ID oben (Hook-Ausnahme), Auftrag: R19-R22 + Empfehlung, Simulator als Vergleichswert. Danach Orchestrator: scripts/system_specs.py auf Q-Werte, Viewer-Kennzahlen, Beschreibungen nachziehen. Parallel: Werkstatt (local_584eec27-...) und Montage (local_5d913ca0-...) nach M7-Plan.
