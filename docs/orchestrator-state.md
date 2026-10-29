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
