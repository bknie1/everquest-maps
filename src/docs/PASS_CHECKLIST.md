# 0.2-alpha pass checklist

Fresh visual triage of all 79 zones against [STANDARD.md](STANDARD.md), 2026-08-19.
Tiers: **A** ship as-is · **B** minor fix · **C** needs a real pass · **D** redo.

## Tally
- **A (10):** ecommons, freporte, grobb, kithicor, newsebexp, northkarana, oggok, oot, permafrost, unrest
- **D (2):** runnyeye, soltemple
- **C (27), B (40)** — see waves below.

## The two dominant, mechanical issues (fix these first — biggest lift)
- **compass-fix (~21):** broken/loose/arrow-only compass → rebuild as a rose.
  `fix_compass.py` (auto-detects N/E/S/W letters OR an arrow glyph cluster).
  - DONE (13): butcher, commons, kedge, steamfont, crushbone, gukbottom, guktop,
    highkeep, mistmoore, soldunga, soldungb, soldungc, warrens
  - residual stray arrow to clean in their full pass: crushbone, soldungb
  - TODO: najena (bare "+", pass --center), lfaydark + rathemtn (compass is
    INSIDE content — relocate to a margin), felwithe a/b + kaladim a/b (do in
    their city passes, low --clear-frac to spare dense margins)
- **artifact-cleanup — DONE (2026-08-19):** the "title carets/arrows" were NOT
  in _2 at all. They were bare EQOA up-arrows in the **_3 historical layer**,
  ink (150,90,150), parked in the top margin over the title (base=0 title-band
  strokes pack-wide; _2 titles were already clean). `clear_title_artifacts.py`
  removes _3 violet strokes above the grid top UNLESS a _3 "To X" label sits
  within 380u (spares real north-exits: blackburrow, rivervale kept theirs).
  Stripped 121 strokes across 23 zones. **eastkarana skipped (LOCKED)** — 3
  strokes await Brandon's ok. Zones whose flag was really biome/shading/compass
  (akanon, beholder, befallen, cauldron, erudnext, erudsxing, qcat, qeynos2,
  lavastorm, oasis) had no title arrow — fix those in their real pass.
- NOTE: `rebuild_zone.py` (from-source _2 composer: frame+title+compass+biome
  from clean base) exists + works, but is for genuinely broken _2 zones. Do NOT
  run it on rich zones (qeytoqrg proved this — its _2 was already good).

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
