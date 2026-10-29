# aquaponics-dome

Parametrisches SolidCraft-Modell einer Geodaetischen Kuppel mit Aquaponik-System
(Fischtanks, Hydroponik-Ring, Substratbeete). Claude baut es per MCP und verfeinert
es in einer Schleife gegen Referenzbilder.

- `reference/` — Referenzbilder (aus Blender)
- `designs/` — SolidCraft-Designs (`.sc`) und Exporte (STEP)
- `renders/` — Screenshots je Verfeinerungsrunde
- `docs/packages/` — Arbeitspakete; `docs/loop-log.md` — Protokoll der Schleife

SolidCraft: v0.25.1, MCP-Server `solidcraft-cli mcp` (siehe `.mcp.json`, schreibt nur in `designs/` und `renders/`).
