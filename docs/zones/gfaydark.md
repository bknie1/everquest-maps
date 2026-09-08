# gfaydark

**Title:** GREATER FAYDARK (15 chars)
**Title style:** woodelf
**Title bbox:** x[-3317,2963] y[-3817,-2955] (h 862)
**Title inks:** (70, 58, 44) x412, (46, 82, 52) x406, (38, 70, 46) x283, (74, 116, 62) x278
**Frame width:** 7322
**Layers:** _1=0, _2=16112, base=14832
**Total strokes:** 30944 (budget 31000) | POIs 34 | dupes 1 | inks 34
**eqqms:** overall A (format A, budget A, title A, dupes A, palette A)

## Notes

2026-09-08 (Opus 4.8): Wood-elf title. New `woodelf` style in
src/titles/styles.py — elegant slender green caps (54,98,50) over a faint bark
echo (104,76,44), small leaves budding from the cap tips, and a thin sprigged
branch beneath the word. Kelethin high-fantasy; distinct from Felwithe's gold
italic (highelf) and Surefall's rough ranger caps (sylvan). Applied via
apply_title (mode=ink on the dedicated title ink (90,60,34); removed all 61
plain-cap strokes, drew 206). Needed `band_pad=110` (new apply_title option):
four letter-feet dipped below the default grid_top+40 band cutoff and would have
been orphaned. grow 0.85 / dy -80 -> smaller than the sprawling plain original,
lifted clear of the grid. Budget is tight (30944/31000) -- if the pack needs
headroom later, the woodelf leaves/branch are the cheapest thing to thin.
NOTE: measured Title bbox is forest-contaminated (the whole top strip); the real
title is the centered wood-elf caps. FIRST VERSION — Brandon's verdict pending.
