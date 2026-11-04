# Bauteilblatt T4 tuer: ABGELOEST (Altmodell, nicht verbaut)

**Status:** abgeloest durch `tuer_komplett` (T50, Blatt `docs/parts/tuer_komplett.md`). `designs/components/tuer.sc` bleibt als Altbestand erhalten, nicht loeschen (Entscheidung Orchestrator 04.11.2026).

- Inhalt: 9 Koerper (Pfosten L/R, Sturz, Schwelle, Blatt, Scharnier, Griff `T4_Griff`), Werkstoff `Default`.
- Im Gesamtmodell: 0 Instanzen (`viewer/instances.json` fuehrt `tuer_komplett` 1, kein `tuer`; Befehl: `python -X utf8 scripts/model_inventar.py`, Zeile `tuer.sc` unter "ohne Instanz").
- Einkaufsliste: nicht doppelt gezaehlt. `data/stueckliste.json` Artikel `SON-tuer-modellvariante`: Bedarf 0, `nicht_platziert: true`, Hinweis `altmodell`.
- Teiledaten: `data/parts/tuer.json`, Feld `abgeloest`.
- Werkstoff `Default` bleibt hier bewusst (kein eingesetztes Bauteil), steht in der Inventur unter "ohne Instanz".
