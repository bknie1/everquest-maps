# nektulos

**Title:** NEKTULOS FOREST (15 chars)
**Title style:** plain caps (wants style) (Brandon verdict 2026-09-06)
**Title bbox:** x[-2037,1820] y[-3803,-3323] (h 481)
**Title inks:** (34, 58, 38) x72, (45, 38, 55) x43, (120, 115, 125) x12, (90, 70, 110) x6
**Frame width:** 4548
**Layers:** _1=30, _2=13605, _3=38, base=2003
**Total strokes:** 15676 (budget 31000) | POIs 45 | dupes 0 | inks 104
**eqqms:** overall B (title B — plain caps, restyle candidate; palette B)

## Notes

CREEPY-FOREST REBUILD (2026-09-09, src/zones/nek_rebuild.py) — the real pass
Brandon signed off. The _2 decoration had accreted artifacts across many
sessions (crude gate blob, fake triangle "lava peaks", rough polygon-crown
flora, stray tangle). This composes _2 fresh BY REGION so the shared-ink
entanglement (34,58,38 spans crowns + interior + title) never bites:

- KEEP the interior wholesale (grass, river, bridge, the fauna_sil silhouettes),
  the title band, compass, and the Nektropos castle sketch (SW, by region + its
  sketch inks). PURGE every old tree/crown ink (margin AND interior).
- FLORA, completely redone: a CREEPY dead-forest — bare clawing snags (dominant)
  + dark full conifers, every tree coloured by a QUANTIZED green(south) ->
  purple -> blue(north) gradient (the halfling->Neriak transition Brandon loves,
  ~like West Commonlands). Dense round the margins, a lighter haunted scatter
  inside the grid, all held off the labels + structures. Fauna, grass, water,
  bridge untouched.
- Neriak gate: the dolmen sketch (neriak_gate_segs), RIGHT WAY UP (rock face on
  top, tunnel opening down), in the right margin by the "to Neriak" exit.
- Nektropos castle: RESTORED (an earlier rebuild had wrongly dropped it as
  "margin"); kept by SW region + sketch inks.
- FRAME WIDENED: the worn side borders were tight (x ~ -1990 / 1780) so flora +
  gate spilled past them; moved out to -2170 / 2130 with corner connectors so the
  margin has real room.
- Volcanoes (terrain.volcano — cones, lava tongues, plumes) by the "to Lavastorm"
  exit, replacing the fake triangle range.
- Keep-outs: castle towers, compass, gate footprint, wizard gate / Knowledge
  Portal / Minor Spires + the obelisk & gold-statue ruins, title band, POI labels.

eqqms may flag `compass:2` — a false positive from a ring-shaped spider web
(kept fauna), not a second rose.

Superseded tools (kept for history): nek_hd_fauna.py (fauna_sil silhouettes —
their placement/roster carried into the rebuild) and nek_hd_flora.py (the
darkwood-Mirkwood margin pass, now replaced by the creepy dead-forest).

STILL OPEN: stylized dark-forest / Teir'Dal title (Title Campaign, ⏸).
