# feerrott

**Title:** THE FEERROTT (12 chars)
**Title style:** unreviewed
**Title bbox:** x[-2908,2575] y[-2840,-2348] (h 492)
**Title inks:** (38, 62, 32) x122, (96, 104, 82) x107, (168, 148, 112) x105, (64, 72, 54) x93
**Frame width:** 9009
**Compass:** 1 rose(s), ring 21px at 900px fit
**Layers:** _1=0, _2=2445, _3=35, base=28351
**Total strokes:** 30831 (budget 31000) | POIs 44 | dupes 0 | inks 38
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
