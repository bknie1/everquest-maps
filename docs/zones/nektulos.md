# nektulos

**Title:** NEKTULOS FOREST (15 chars)
**Title style:** plain caps (wants style) (Brandon verdict 2026-09-06)
**Title bbox:** x[-2037,1820] y[-3803,-3323] (h 481)
**Title inks:** (34, 58, 38) x72, (45, 38, 55) x43, (120, 115, 125) x12, (90, 70, 110) x6
**Frame width:** 4548
**Layers:** _1=0, _2=28759, _3=27, base=2003
**Total strokes:** 30785 (budget 31000) | POIs 45 | dupes 0 | inks 62
**eqqms:** overall B (format A, budget A, title B, dupes A, palette A)

## Notes

Neriak gate: HAND-PLACED, do not re-run place_neriak_gate.py (guarded). It is
v-flipped (mountains-on-top, tunnel opening south), top-left, native center
(-1422,-2711), per Brandon's /loc target (2711,1422,-2737). The old tool dumped
it mirrored in the SW corner -- recurring bug, now fixed at the data level.
Lavastorm volcanic peak range added along the north edge (rock ink 80,58,50 +
lava-glow 210,90,25) by the "to Lavastorm" exit. Nektropos castle shifted right
2026-09-06.

HD fauna (2026-09-08, src/zones/nek_hd_fauna.py): the interior creatures were
old fauna.py wireframes (nek_color.py placed FA.spider/skeleton/halfling/darkelf).
The 15 humanoid wireframes were retired for fauna_sil silhouettes — curated to 8
solid figures: 3 Teir'Dal (Neriak guards/dragoons, native violet 72,58,96), 2
skeletons (bare bones + rusty sword), 1 orc (Deathfist/orc-runner, green+gold),
2 Leatherfoot halflings. Each figure's sub-pixel solid-fill scanlines are
decimated (keep every other) — invisible at map scale, ~halves the cost — so the
swap lands at total 30,785/31k (was 30,171). Spiders kept as-is: fauna_sil has
no spider figure. Keep-outs untouched (Neriak gate ink 72,66,86 = 256 strokes
verified unchanged; Nektropos castle; lava peaks; wizard gate; title; compass).

Flora is HD: the margins are dense flora_hd darkwood (~9.5k strokes of 34,58,38)
framing the zone as one clearing in a larger dark forest. The interior is
deliberately kept light (nek_color doctrine — colour off the ground, not buried
crowns) so labels stay readable; interior darkwood giants are intentionally NOT
added (they'd bury labels and burst budget). Old low-fi interior conifers remain
light and read as sparse forest hints.

STILL OPEN: stylized dark-forest / Teir'Dal title (Title Campaign, ⏸).
