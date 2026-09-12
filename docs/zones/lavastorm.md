# lavastorm

**Title:** LAVASTORM MOUNTAINS (19 chars)
**Title style:** lava (molten)
**Title bbox:** x[-2042,1719] y[-2008,-1539] (h 468)
**Title inks:** (74, 54, 46) x246, (196, 84, 30) x100, (155, 65, 30) x40, (226, 150, 48) x12
**Frame width:** 3915
**Compass:** 1 rose(s), ring 25px at 900px fit
**Layers:** _1=0, _2=2428, _3=4837, base=2885
**Total strokes:** 10150 (budget 31000) | POIs 34 | dupes 0 | inks 38
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

2026-09-08 (Opus 4.8): Lava/ember title. New `lava` style in
src/titles/styles.py — heavy dark-basalt caps (74,54,46) over a hot lava-glow
echo (196,84,30), a few ember cracks (226,150,48) across the strokes, and lava
dripping from the low edges with a bright bead. Applied via apply_title
(mode=ink on the rock title ink (80,58,50); removed 83 plain-cap strokes, drew
~376). The red zigzag border (155,65,30) shares the band but a different ink, so
it is preserved. grow 0.9; the lava letters are less condensed than the wide
plain original, so the title reads narrower and centered (smaller doctrine) with
~68u clearance above the grid. NOTE: the measured Title bbox above is
border-contaminated (pick_letters grabs the red frame zigzag); the real title is
the centered molten caps. FIRST VERSION — open to iteration on glow/drip
intensity per Brandon's verdict.
