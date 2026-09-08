# nektulos

**Title:** NEKTULOS FOREST (15 chars)
**Title style:** darkwood (Teir'Dal forest)
**Title bbox:** x[-2037,1820] y[-3803,-3323] (h 481)
**Title inks:** (78, 66, 76) x115, (96, 74, 132) x73, (45, 38, 55) x43, (120, 115, 125) x12
**Frame width:** 4548
**Layers:** _1=0, _2=26653, _3=27, base=2003
**Total strokes:** 28683 (budget 31000) | POIs 45 | dupes 0 | inks 97
**eqqms:** overall B (format A, budget A, title A, dupes A, palette B)

## Notes

Neriak gate: HAND-PLACED, do not re-run place_neriak_gate.py (guarded). It is
v-flipped (mountains-on-top, tunnel opening south), top-RIGHT by its own 'to Neriak' zone-line POI (native ~1108,-2272) and
'Neriak Gate' POI (990,-2324) -- gate center ~(1030,-2360). (Brandon's /loc
target mapped to top-left but the POIs are the ground truth: top-right.) The old tool dumped
it mirrored in the SW corner -- recurring bug, now fixed at the data level.
Lavastorm volcanic peak range added along the north edge (rock ink 80,58,50 +
lava-glow 210,90,25) by the "to Lavastorm" exit. Nektropos castle shifted right
2026-06 (gate now top-right with a tree keep-out clearing, per origin/main).

HD fauna (2026-09-08, src/zones/nek_hd_fauna.py): the interior creatures were
old fauna.py wireframes (nek_color.py placed FA.spider/skeleton/halfling/darkelf).
The 15 humanoid wireframes were retired for fauna_sil silhouettes — curated to 8
solid figures: 3 Teir'Dal (Neriak guards/dragoons, native violet 72,58,96), 2
skeletons (bare bones + rusty sword), 1 orc (Deathfist/orc-runner, green+gold),
2 Leatherfoot halflings. Each figure's sub-pixel solid-fill scanlines are
decimated (keep every other) — invisible at map scale, ~halves the cost. Spiders
kept as-is: fauna_sil has no spider figure. Keep-outs untouched (Neriak gate ink
72,66,86 = 256 strokes verified unchanged; Nektropos castle; lava peaks; wizard
gate; title; compass).

HD flora (2026-09-08, src/zones/nek_hd_flora.py): the margin forest was old
rough polygon-crown sketches (the Faydark low-fi symptom) — north in Teir'Dal
purple (ink 46,40,68), south in green. Both were retired for the Mirkwood recipe
Brandon approved for lfay/kithicor: FH.darkwood giants over a black-green conifer
understory (old F.fir recoloured dark) plus a few pale snags. North keeps the
Teir'Dal purple; south stays green (halfling country), per the nek_purple
convention. 6,873 rough-crown strokes removed, ~4,811 HD strokes added (net −2k;
darkwood giant fills decimated). Placement guards every keep-out (castle, gate,
lava band, compass, title band, POI labels) and the giants are held off the
title band. A few interior-edge green crowns in halfling country remain: they are
interior forest (not margin) and cluster into the south forest, so they are left
alone rather than risk stripping it.

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
