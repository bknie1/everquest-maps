# kithicor

**Title:** KITHICOR FOREST (15 chars)
**Title style:** darkwood (haunted forest)
**Title bbox:** x[-5844,2020] y[-2908,-2299] (h 610)
**Title inks:** (34, 58, 38) x544, (84, 74, 60) x115, (95, 70, 45) x90, (120, 140, 80) x67
**Frame width:** 8356
**Compass:** 1 rose(s), ring 17px at 900px fit
**Layers:** _1=0, _2=24991, _3=38, base=5925
**Total strokes:** 30954 (budget 31000) | POIs 43 | dupes 0 | inks 29
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

2026-09-08 (Opus 4.8): Dark haunted-forest title. New `darkwood` style in
src/titles/styles.py — gaunt gnarled caps (40,58,44) with a muted dead-branch
echo (84,74,60) and bare leafless twig-forks off the terminals; kin to Lesser
Faydark's Mirkwood, lean by design. Removal was the hard part: the title shares
its ink (34,58,38) with the scattered top-margin bushes AND the forest, at
similar x/y, and both component and ink_comp detection fragment this plain-cap
font. Added a new apply_title `mode="box"` (remove an ink within an explicit
(x0,x1,y0,y1) box, optional min_len) and bounded the title precisely
(box=(-3650,1300,-2820,-2440), min_len=45, letters are pure long strokes so the
short bush-hatch survives). Removed 76 letter strokes, drew 182. grow 0.85 / dy
-40. 30955/31000, grade A (tight). FIRST VERSION — Brandon's verdict pending.
