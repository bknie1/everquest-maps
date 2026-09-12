# felwithea

**Title:** NORTHERN FELWITHE (17 chars)
**Title style:** highelf
**Title bbox:** x[-577,1053] y[-649,-460] (h 190)
**Title inks:** (198, 152, 62) x112, (44, 92, 56) x75, (62, 104, 56) x52
**Frame width:** 1614
**Compass:** 1 rose(s), ring 29px at 900px fit
**Layers:** _1=0, _2=6500, base=4544
**Total strokes:** 11044 (budget 31000) | POIs 69 | dupes 0 | inks 30
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

2026-09: highelf italic w/ gold vine swash. Letters shared canopy ink -> component detection on len>=12 strokes only; canopy knocked out under new lettering.

2026-09-06 review pass: removed the old oversized compass (both rings, rays,
arrow, labels), the misplaced BL banner copy inside it, and the 6-stroke gold
parchment-curl remnant. Restored the four corner pennant banners (09d8579
geometry; BL/BR at their original stations, TL/TR dropped 190u below their
historical stations to clear the new title) and the 4dd2660 entrance-facade
arch (deduped, left margin). New compass at everfrost-standard proportion
(ring r~51, labels r~58) in the right margin, padded + knocked out. Trees
pass: exact-vertex component knockouts (0.5u endpoint rounding chains
overlapping canopies — do not repeat), open-chain scars closed/stub-cleared,
bald spots re-treed. Exterior fauna: two fauna_sil high_elf figures + two
flora_hd broadleaf accents. Title and interior shading untouched.

2026-09-06 second look (Brandon): title-band debris cleared (88 strokes of
broken tree chains, orphan dash rows, and a patchy y=-441 rule left by the
old canopy knockout under the lettering) — safety rule: only strokes present
VERBATIM in pre-title commit 69380bc were candidates, so title strokes were
untouchable. Worn parchment border finished: it had no top side; added a
6-segment zigzag at y~-372/-403 (dips point up, clearing the TL/TR pennants).
The small triangles riding the gold swash are post-title (not in 69380bc):
designed, keep them.
