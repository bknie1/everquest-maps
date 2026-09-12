# innothule

**Title:** INNOTHULE SWAMP (15 chars)
**Title style:** swamp (troll/froglok)
**Title bbox:** x[-2808,1769] y[-3508,-3089] (h 419)
**Title inks:** (82, 96, 52) x177, (50, 60, 36) x118, (70, 80, 50) x15, (122, 142, 68) x14
**Frame width:** 4801
**Layers:** _1=0, _2=639, _3=36, base=22853
**Total strokes:** 23528 (budget 31000) | POIs 44 | dupes 9 | inks 19
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

2026-09-08 (Opus 4.8): Swamp title. New `swamp` style in src/titles/styles.py —
thick lurching caps (crude jitter) in murky bog green (82,96,52) over a dark
muck shadow (50,60,36), with slime oozing off the lowest point of each letter
into a fat droplet (122,142,68). Crude and dripping; lettering treatment only,
no floating figures. Applied via apply_title (mode=ink on the title ink
(70,80,50)); removed the old plain caps + the decorative ~tildes~ (70 strokes,
drew ~324). The top border zigzag and its two corner descents share the title
ink and sit in the _2 band, so they are PROTECTED by region (see the innothule
protect boxes) — no border gap. grow 0.5, dy -110 -> compact centered title
(smaller doctrine), drips clear of the grid. NOTE: measured Title bbox is
border-contaminated (pick_letters grabs the protected frame zigzag); the real
title is the centered swamp caps. FIRST VERSION — Brandon's verdict pending.
