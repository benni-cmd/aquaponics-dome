# Änderungsprotokoll Netzliste (R40, Version 2, 31.10.2026)

Netzliste `data/leitungsnetz.json` von Version 1 (R28) auf den Modellstand gebracht: kleiner Puffer (D66, R37, T82), Drittbecken klein (T14k), Messstellen (D65, R39), Hauptstrom-Feinfilter (D55, W32), Linienteilung (D67). Prüfung: `python scripts/check_netz.py` (Schritt 6). Quelle je Zeile: R-/D-Nummer; Herkunftsbuchstabe wie in der Netzliste (Q/E/A).

## Schritt 1: Puffer klein (K35–K41, D66, R37 Befund 9, T82)
Der Stapel aus zwei IBC (Messtank oben, Vorrat unten) entfällt. Im Dom stehen die Messzelle (20 l), das Stammlösungsfass (120 l), der Eisen-Kanister (20 l) und die zwei Schlauchpumpen auf dem Stand T82. Frischwasser läuft über Aktivkohle direkt in den Pool, ohne Standvorrat.

| Element | alt | neu | Begründung / Quelle |
|---|---|---|---|
| Knoten `puffer_oben` | obere IBC, Messtank | `puffer_messzelle` (T82) | Messzelle 20 l Acryl, Messkreis 3 l/min = 6,7 min Verweilzeit; D66, R37 Befund 1 |
| Knoten `puffer_unten` | untere IBC, Vorrat/Frischwasser 2 Tage | `puffer_stammfass` (T82) | 120-l-HDPE-Fass mit Base-Stammlösung, 15–35 Tage Vorrat; R37 Befund 8 |
| Knoten `puffer_eisen` | — (neu) | Eisenchelat-Kanister 20 l | 74 g Fe alle 3 Wochen; R37 Befund 1, T82 |
| Knoten `dosierkonsole` | Bauteil `puffer_station` | Bauteil `puffer_klein` | Schlauchpumpen auf dem Regalboden T82 |
| Knoten `aktivkohle` | — (neu) | Aktivkohlefilter im Frischwasser | entfernt Chlor und Chloramin, ersetzt 2 Tage Standzeit; D66, R37 Befund 3 |
| Knoten `frischwasser` | „Chlor entweicht 2 Tage“ | Aktivkohle direkt | D66; Standort/Versorger kein offener Punkt mehr (D69) |
| Knoten `drittbecken` | Bauteil `becken_dritt` (0,94 m³) | `becken_dritt_klein` T14k, 0,4 m³ | D66, R37 Befund 10 |
| Knoten `biofilter_dritt` | ca. 85 l Bioballs | ca. 37 l Bioballs | 73 g Futter/Tag × 0,5 l/g; R37 Befund 10 |
| K35 | `verteiler_1` → `puffer_oben`, d20, 3 l/min, Förderhöhe ca. 3 m (Stapel 2,5 m) | → `puffer_messzelle`, d20, 3 l/min, Förderhöhe 1,5 m | Messpumpe 5,9 W → 2,9 W; R37 Befund 9 |
| K36 | `puffer_oben` → `puffer_unten` Schwerkraft | **entfällt** | kein Stapel |
| K37 | `puffer_unten` → `pool` d25 | `puffer_messzelle` → `pool` d25 | Ablaufstutzen d25 der Messzelle (T82-Port) |
| K38 | `dosierkonsole` → `pool`, d20, 0,4 l/min | d9 (Schlauch 6/9), 0,003 l/min | Base 4,3 l/Tag bei 100 g/l: 0,43 kg/Tag (D61, 130 g TAN/Tag); Pumpe 4,5–220 ml/min |
| K39 | `frischwasser` → `puffer_unten` d25 10 l/min | `frischwasser` → `aktivkohle` d25 10 l/min | Spitze 10 l/min beim Nachspeisen, Mittel 0,47 l/min (0,68 m³/Tag, SRAC 454) |
| K40 | `puffer_unten` → `pool` d20 0,5 l/min | `aktivkohle` → `pool` d25 10 l/min Spitze | Schwimmerventil am Pool; Spitze statt Mittel, damit d20 nicht bei 10 l/min 0,83 m/s fährt |
| K41 | `puffer_unten` → `drittbecken` d20 2 l/min | `aktivkohle` → `drittbecken` d20 2 l/min | Wasserwechsel Quarantäne aus der Frischwasserleitung; R37 Befund 9 |
| K50 | Luft → `puffer_unten` | **entfällt** | kein Standwasser, keine belüftete Vorratsstufe |
| K52 (neu) | — | `aktivkohle` → `puffer_stammfass` d25 | Ansetzen von Hand, kein Dauerfluss |
| K53 (neu) | — | `puffer_stammfass` → `dosierkonsole` d12 (Schlauch) 0,003 l/min | Entnahme Stammlösung zur Base-Pumpe; T82-Port „Entnahme“ |
| K54 (neu) | — | `puffer_eisen` → `dosierkonsole` d12 0,0004 l/min | Eisen-Pumpe saugt aus dem Kanister |
| K55 (neu) | — | `dosierkonsole` → `pool` d9 0,0004 l/min | Dosierleitung Eisen |
| Kabel `puffer_station` | 17 W | `puffer_klein` 11,5 W | R37 Befund 9: Messkreis nur 1,5 m, Umpumpen entfällt |
| `messstellen.json` | `puffer_oben`, `puffer_unten` | `puffer_messzelle`, `puffer_stammfass` (MS46–49, MS55, Pflichtliste); MS08 Text 2,8 g TAN/0,4 m³; MS49 Füllstand Stammlösung | damit `scripts/messstellen_plan.py` weiter besteht; zwei neue Einträge unter `ohne_messstelle` (`aktivkohle`, `puffer_eisen`) |

