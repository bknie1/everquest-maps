# 0.2-alpha pass checklist

Fresh visual triage of all 79 zones against [STANDARD.md](STANDARD.md), 2026-08-19.
Tiers: **A** ship as-is · **B** minor fix · **C** needs a real pass · **D** redo.

## Tally
- **A (10):** ecommons, freporte, grobb, kithicor, newsebexp, northkarana, oggok, oot, permafrost, unrest
- **D (2):** runnyeye, soltemple
- **C (27), B (40)** — see waves below.

## The two dominant, mechanical issues (fix these first — biggest lift)
- **compass-fix (~21):** broken/loose/arrow-only compass → rebuild as a rose.
  `fix_compass.py`. Zones: befallen, butcher, commons, crushbone, felwithea,
  felwitheb, gukbottom, guktop, highkeep, kaladima, kaladimb, kedge, lfaydark,
  mistmoore, najena, rathemtn, soldunga, soldungb, soldungc, steamfont, warrens
- **artifact-cleanup (~19):** stray title carets/arrows/ghosts/rules → delete.
  Zones: akanon, beholder, befallen, cauldron, cazicthule, eastkarana, erudnext,
  erudsxing, feerrott, innothule, lavastorm, nektulos, qcat, qey2hh1, qeynos2,
  qeytoqrg, southkarana, sro, stonebrunt

## Waves (execution order toward 0.2)
1. **Mechanical batch** — compass-fix + artifact-cleanup above. Lifts most B→A.
2. **Dungeon passes (8):** runnyeye (redo), soltemple (redo), gukbottom, guktop,
   soldungb, warrens, blackburrow, mistmoore — depth/floor shading, water, rose.
3. **City passes (10):** qeynos, qeynos2 (Camelot + shade_city), akanon
   (BIOME: cave+clockwork, not forest), rivervale, erudnext (+water-fix),
   erudnint, paineel, neriaka, neriakb, neriakc (dark-elf shade + motifs).
4. **Plane passes (4):** airplane (+broken-shading fix), fearplane, hateplane,
   hateplaneb — god symbolism + mood + depth.
5. **Bare-margin shading (8):** everfrost (top/left), lakerathe, nro, oasis, paw,
   freeportsewers, highpass, hole — themed margin decoration + depth.
6. **Label declutter (~22, systemic, LOWER priority):** POI clusters overlap on
   blackburrow, crushbone, feerrott, felwithe a/b, freportn, freportw, gfaydark,
   halas, kaladim a/b, kerraridge, qeynos, qrg, rathemtn, steamfont, tox,
   highpass, highkeep, warrens, innothule, erudsxing. NOTE: reference zones
   (newsebexp) also have label crowding, so this alone is not disqualifying —
   treat as polish, needs a leader-line/offset strategy, not a blocker for 0.2.

## One-offs
- **akanon** — wrong biome (forest → cave); part of its city pass.
- **misty** — sparse central ground cover; wilderness-pass (meander grass).
- **nektulos** — verify the stray green rectangle (may be a base zone-boundary line).
- **qcat** — two-line title overlaps the top frame; nudge down.
- **erudnext / qeynos** — water bleeds into structures; contain it.

## Full table
(zone | tier | categories | note — see scratchpad triage2/*.txt for full notes)
