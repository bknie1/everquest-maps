# nektulos

**Title:** NEKTULOS FOREST (15 chars)
**Title style:** darkwood (Teir'Dal forest)
**Title bbox:** x[-2037,1820] y[-3803,-3323] (h 481)
**Title inks:** (78, 66, 76) x115, (96, 74, 132) x73, (45, 38, 55) x43, (120, 115, 125) x12
**Frame width:** 4548
**Layers:** _1=30, _2=12994, _3=38, base=2003
**Total strokes:** 15065 (budget 31000) | POIs 45 | dupes 0 | inks 105
**eqqms:** overall B (title A — themed darkwood; palette B from 105 inks)

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

PATCH (2026-09-09): (a) the right-margin WIZARD GATE was buried under trees. It
is a LOCKED-IN graphic — `src/toolkit/eqmap_toolkit.py:wizard_gate` (a pseudo-3D
ziggurat with a front staircase + a portal swirl on the plateau; inks stone
120,116,124 / portal 150,95,185), the one that "actually looks like the gate"
(Brandon). v0.2.2.1 wrongly REPLACED it with a hand-drawn pillars-and-portal
version — that was reverted in v0.2.2.2: the original graphic is KEPT untouched
and simply fenced off with a flora keep-out (x[1280,1840] y[-920,-160], extended
below the base since trees draw upward). USE eqmap_toolkit.wizard_gate for GFay's
gate too — do NOT redraw it. (b) Purged two old nek_hd_flora darkwood inks that
TREE_INKS had MISSED — (52,46,74) N_TREE (470 strokes) and (56,48,40) S_TRUNK
(258) — so no old darkwood trees survive mixed into the new creepy forest.

eqqms may flag `compass:2` — a false positive from a ring-shaped spider web
(kept fauna), not a second rose.

Superseded tools (kept for history): nek_hd_fauna.py (fauna_sil silhouettes —
their placement/roster carried into the rebuild) and nek_hd_flora.py (the
darkwood-Mirkwood margin pass, now replaced by the creepy dead-forest).

Title (2026-09-08, Opus 4.8): dark Teir'Dal forest title, DONE. Uses the new
`darkwood` style (see [[title-campaign-progress]] / kithicor) with a Teir'Dal
violet tint — kw ink (96,74,132), branch (78,66,76) — so it reads as the dark-elf
sibling of Kithicor's green haunted wood. Gaunt gnarled caps with a dead-branch
echo and bare twig-forks. Applied via apply_title (mode=ink on the title ink
(34,58,38); the HD-flora session had already held the giants off the title band,
so the band was clean — removed all 72 plain-cap strokes, drew 188). The purple
frame brackets (45,38,55) and grey rules (120,115,125) are preserved, and the
mountain zigzag range sits below the band untouched. grow 0.85 / dy -25.
NOTE: eqqms overall is B only from `palette` (97 inks, from the HD-flora work) --
the title itself grades A. FIRST VERSION — Brandon's verdict pending.
