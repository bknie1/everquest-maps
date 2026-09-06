# feerrott

**Title:** THE FEERROTT (12 chars)
**Title style:** unreviewed
**Title bbox:** x[-4593,4232] y[-3197,-2057] (h 1140)
**Title inks:** (38, 62, 32) x6324, (50, 78, 42) x4062, (44, 72, 36) x1718, (56, 86, 44) x1646
**Frame width:** 9009
**Layers:** _1=0, _2=60215, _3=35, base=30001
**Total strokes:** 90251 (budget 31000) | POIs 44 | dupes 0 | inks 38
**eqqms:** overall F (format A, budget F, title A, dupes A, palette A)

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
