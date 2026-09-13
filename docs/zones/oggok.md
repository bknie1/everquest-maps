# oggok

**Title:** OGGOK (5 chars)
**Title style:** crude (ogre)
**Title bbox:** x[-1448,721] y[-1208,-903] (h 306)
**Title inks:** (86, 132, 70) x401, (122, 86, 54) x108, (56, 102, 40) x90, (110, 96, 66) x72
**Frame width:** 2176
**Compass:** 1 rose(s), ring 25px at 900px fit
**Layers:** _1=0, _2=13666, base=4545
**Total strokes:** 18211 (budget 31000) | POIs 28 | dupes 2 | inks 33
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

2026-09: crude ogre caps (mud). Letter inks (98,88,60)/(120,96,54) shared with crest/ladders -> x-window + crest protect band.

2026-09-13 (Brandon: "Oggok's object colors (yellowish) and yellow shading are
way too aggressive"): these were the ORIGINAL stock-map inks, present since the
very first commit (1f959c2) and never touched by any styling pass. Toned down
the two worst offenders and their paired highlight/shadow variants (base):
(150,138,110)->(132,124,108) [n=2185, the building-wall line network],
(176,146,74)->(128,100,64) [n=875 base / 32 deco, by far the most saturated ink
in the zone (sat 102) -- ground-level cross-tick shading covering the open city
square], (214,198,158)->(196,184,156), (202,186,146)->(184,172,144),
(150,126,88)->(132,112,86), (140,128,96)->(122,114,94) -- same offsets from the
new base tone as they held from the old one, so the shading relationship is
preserved. Title ink (122,86,54)/shade (70,50,34) and all canopy greens
untouched. Pure recolor, stroke count unchanged, still grade A.

2026-09-13 (Brandon, same session: "Oggok and some other zones have the same
[incomplete border] issue"): confirmed and fixed. The worn-zigzag border (ink
120,96,54) had three genuine gaps -- not stylistic dash spacing, verified by
endpoint-to-endpoint continuity, not midpoint distance (a zigzag's long teeth
make midpoint spacing look like a gap even when perfectly connected; that
distinction is why this was missed before): two ~270-unit holes on the BOTTOM
edge and one ~91-unit hole further along it, plus two small ~50-66 unit gaps
on TOP and one ~81-unit gap on LEFT. Filled each with matching zigzag teeth
at the locally-measured pitch, snapped to the exact surviving endpoints on
both sides. Verified closed (zero real gaps remain; RIGHT was already
intact). Grade A, stroke count 18,211 (+30).
