# nektulos

**Title:** NEKTULOS FOREST (15 chars)
**Title style:** plain caps (wants style) (Brandon verdict 2026-09-06)
**Title bbox:** x[-2037,1820] y[-3803,-3323] (h 481)
**Title inks:** (34, 58, 38) x72, (45, 38, 55) x43, (120, 115, 125) x12, (90, 70, 110) x6
**Frame width:** 4548
**Layers:** _1=0, _2=28599, _3=27, base=2003
**Total strokes:** 30629 (budget 31000) | POIs 45 | dupes 0 | inks 62
**eqqms:** overall B (format A, budget A, title B, dupes A, palette A)

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

STILL OPEN (next in this session): the margin trees are OLD ROUGH SKETCHES
(ink 46,40,68), same low-fi symptom as the Faydark maps — replace with HD
flora_hd darkwood (matching lfay/kithicor). Also stylized dark-forest / Teir'Dal
title (Title Campaign, ⏸).
