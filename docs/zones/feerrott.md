# feerrott

**Title:** THE FEERROTT (12 chars)
**Title style:** unreviewed
**Title bbox:** x[-4546,4196] y[-3340,-2004] (h 1336)
**Title inks:** (96, 104, 82) x107, (168, 148, 112) x105, (64, 72, 54) x93, (124, 106, 76) x56
**Frame width:** 9009
**Compass:** 1 rose(s), ring 21px at 900px fit
**Layers:** _1=0, _2=2368, _3=35, base=28351
**Total strokes:** 30754 (budget 31000) | POIs 44 | dupes 0 | inks 38
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

Title drawn in CANOPY ink in the band -- any canopy strip must keep-out the title box.

DENSITY DOCTRINE (Brandon, 2026-09-05): the tree population is ONE EVEN FIELD across
the full map -- no per-area densities, no interior/ring split, no fades. Density is
shaped only by knockouts (river, paths, clearings, title box). Equalized via thin-only
per-cell cap: canopy strokes per 100u cell (base+_2 combined) capped at 14, random
in-cell drops, deterministic; cells at/below cap untouched so knockouts keep their
exact shape; title box out of scope by bbox-intersect. Result: interior and ring both
median 14/cell, max 14 -- seamless at the boundary. 126,176 -> 90,251. A graded ring
fade was tried and REVERTED same day (broke the even-field look). T=8/T=11 renders
rejected: too sparse, and the untouched title band pops as a dense stripe. Dedupe is
exhausted (exact 0, colinear -7, int near-dupe -1, no cross-layer overlap).

2026-09-12 (Brandon: "way too tree dense to render everything, revert to when we just
filled the grid with rainforest ... could also just remove it from the margin"): the
per-cell-cap doctrine above (T=14 across base+_2 combined) still landed at 90,251 --
2.9x over budget -- because _2 was layering a SECOND full interior canopy pass on top
of base's own (25,706 extra interior strokes) plus a dense margin ring (32,215
strokes, more than the entire budget by itself). Reverted: dropped every _2 canopy
stroke (all 4 tree inks) EXCEPT the ~150 sharing the title's ink inside its own tight
bbox (found by isolating that one ink's strokes and locating the locally-dense glyph
cluster -- title still shares canopy ink with decor, per the note above, so a plain
ink-strip would have deleted "THE FEERROTT" too). Base (the original one-field
interior, unchanged) plus the surviving non-tree _2 (frame/compass/grid/margin
statues/title) landed at 32,450 -- close enough that a further ~7% uniform
deterministic stroke-level thin of the base canopy (never whole tufts, per the
existing doctrine) closed the last 1,650 to land at 30,831, grade A. Margin is now
bare parchment (frame + corner statues only, no tree ring) -- Brandon explicitly
sanctioned this. Interior pattern is visually unchanged from the prior "one even
field" look at any normal zoom.

2026-09-13 (Brandon: "lost some of the outer border and there are some artifacts
above the title"): both were fallout from the 2026-09-12 canopy strip, not new
damage -- (1) the title-preservation box was a generously-padded rectangle
around the letters; incidental background-canopy specks of the same title ink
(38,62,32) that happened to fall inside the padding came along for the ride,
and with the surrounding margin canopy gone they read as stray squiggles above
the clean text. Tightened the box (x[-1567,1150] y[-2680,-2275], found by
histogramming stroke density -- the noise was a locally dense band right above
a much sparser true letter band) -- verified render is pixel-clean. (2) the
worn-zigzag border ink (40,58,36) never actually wrapped the top edge, even
before any of this session's changes -- it only ran left/right/bottom, stopping
at y=-1601 on each side (confirmed against the pre-strip file); the top margin
was ALWAYS solid canopy standing in as the visual border, which no longer
exists post-strip. Extended the same zigzag (measured period 402.7, outer/inner
x -4546.0/-4450 left, 4195.9/4110 right) up both sides to the frame-top corners
and across the top with a matching amplitude, so all four sides are now a
consistent drawn border like every other zone. 30,754 total, grade A, 0 dupes.
