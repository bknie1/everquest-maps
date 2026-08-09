# EQ Legends Maps — handoff

Everything needed to pick this project up cold. Written for whoever continues it,
assuming access to the repo and nothing else.

---

## What this is

A hand-drawn atlas of classic EverQuest's Old World for **EverQuest Legends** and
**Project 1999** — 79 zones, 274 files, in the game's native map format. Built
entirely from Python; no map file is edited by hand.

Repo layout:

```
Emoda Legends Maps/     the shipping map files
src/kit/                reusable art modules
src/toolkit/            map primitives (canvas, frame, grid, title, compass)
src/zones/              per-zone build scripts
src/tools/              validation and cross-atlas sweeps
src/design/             review renders, kit sheets, EQOA report, source archive
src/docs/               conventions, lore source index
```

---

## Non-negotiables

**Coordinate transform.** `native = (-loc2, -loc1)`. An in-game `/loc` reads
`x, y, z`; the map's native coordinates are the second and first negated. Never
use a raw `/loc` as-is. This applies to wiki NPC positions too, since those are
`/loc` values.

**CRLF line endings are mandatory** on every map file. A lone `\n` breaks the file
in the client. `src/tools/validate_all.py` checks the whole pack. The repo has a
`.gitattributes` marking `"Emoda Legends Maps/*.txt" -text` so git stops
normalising them — the path needs the quotes, since git splits on whitespace.

**Layers are never flattened.** `zone.txt` base, `_1` markers, `_2` decoration,
`_3` places and EQOA. Each is independently toggleable in game; merging them
destroys that.

**Never rebuild the user's uploaded base work.** Recolour it, add to it, but the
geometry is theirs.

**POI authority is EQL and P1999.** Brewall's and Good's packs were consulted for
base geometry only. They target EverQuest Live and carry content that does not
exist on these servers. 334 POI were merged from them once and fully reverted.

---

## Validate the overlay, not just the files

`src/tools/validate_overlay.py` composites base and `_2` and checks they agree.
Layers are authored separately but the player sees them stacked, so a tree scattered
into a lake is wrong only in combination — nothing in either file is invalid, which
is exactly why it survives a per-file check. Run it after every decoration pass:

    python src/tools/validate_overlay.py          # report
    python src/tools/validate_overlay.py --fix    # remove offending clusters

It found 41 clusters standing in water on its first run, across ecommons, commons
and Kithicor. Judgement is per cluster, not per line, so a tree with its trunk on
the bank and canopy over the water survives while one sitting in the middle goes.

## Working method

The loop that works: **build → render → the user checks in game → correction
round.** Their screenshots are ground truth and beat any inference from geometry.
Their markup convention is red for remove, green for add or move here, orange for
already handled.

**Ask rather than guess when geometry is ambiguous.** Several long failures in this
project came from inferring what a zone looked like instead of asking. One
sentence from the user ("the traced border encloses water, the interior object is
the island") resolved something six algorithmic attempts could not.

**Preview before writing.** Render the result and inspect it before committing it
to the file. Keep a restore path from `src/design/sources/default_maps.zip` or the
repo copy.

**Deliver complete batches.** Don't pause mid-task for confirmation on mechanical
steps.

---

## The water system — read this before touching water

Water caused more failures than everything else combined. Four distinct styles
appear in these maps, each needing a different tool. All live in `src/kit/darkelf.py`.

### Pick the right function

| The zone draws water as… | Use | Example |
|---|---|---|
| closed pool outlines | `water_fill()` | Paineel's 23 pools |
| borders, any shape, open or closed | **`water_scanline()`** | Toxxulia rivers, Lake Rathetear |
| shoreline with structures to avoid | `water_flood()` | Neriak city water |
| an existing fill needing land subtracted | `water_knockout()` | Kerra Isle island |

**`water_scanline()` is the general answer and should be tried first.** Walk each
row left to right; every border crossing is either entering or leaving water, so
fill between the 1st and 2nd crossing, 3rd and 4th, and so on. No distance limit,
no bank pairing, no closed loops required. Two rivers on one row give four
crossings and fill as two spans correctly. `both_axes=True` repeats the sweep down
each column and unions the result, which is what fixes **right-angle bends**: a row
entering a corner finds only one crossing and contributes nothing, while the column
through it finds its pair.

### Traps that each cost hours

**Borders are drawn two to four times over themselves.** Duplicate crossings flip
parity an even number of times and cancel out. Symptoms differ wildly: inverted
moats in Neriak, empty pools in Paineel, banded lakes. Every parity pass must
collapse coincident crossings first (`eps ≈ cell*0.75`). This bug appeared three
times in three disguises.

**Don't split shoreline from fill by orientation.** Island outlines contain
horizontal edges; filtering them out breaks the loops open so islands are never
recognised and get drowned. Correct approach: take the non-horizontal segments as
the outline, then add back the horizontal segments **whose both endpoints coincide
with outline endpoints**. That repairs loops without dragging in the fill hatch.

**A bridge is a corridor open at both ends.** Structure on two opposite sides
within ~34 units means walkway, never water. A plain clearance gutter wide enough
to clear a bridge also eats narrow moats, because moats have shoreline banks and
structure on only one side — the two-sided test distinguishes them.

**When the ink data is ambiguous, ask for a painted mask.** The fastest and most
reliable fix in this whole project: render the zone's outlines to a clean white PNG
with thick round-capped strokes, have the user paint-bucket the water, then read the
blue pixels straight back through the same transform. No ink heuristics, no parity,
no bank pairing. Lake Rathetear took six algorithmic attempts and was solved in one
pass this way. `src/tools/` has the render step; the mapping is
`native_x = mnx + px/W*(mxx-mnx)` using the same padded extent the render used.

**Brewall's full pack is the fallback base source.** When our own trace of a water
body is fragmentary or open, check `brewall-*.zip` — it usually carries the same
body as a clean closed outline in pure blue `(0,0,255)`, in the same coordinate
space, so `water_scanline()` over it just works. This solved Lake Rathetear and the
Qeynos Hills Fishing Pond after several failed attempts each. Geometry only; POI
authority stays with EQL and P1999.

**When your own base's shoreline is fragmentary, check the upstream trace.**
Lake Rathetear's shoreline is split across inks in our base and defeated every
border rule. The upstream pack carries it as one clean 910-segment blue outline;
running the scanline over that solved in one pass what six attempts could not.
Geometry only — POI authority stays with EQL and P1999.

**Undersized bodies are artefacts.** Anything under ~24 runs is a leak, not a
puddle. Real bodies run to dozens or hundreds.

**Solid fill beats hatching** and is cheaper: one continuous run per row, rows
tight enough to read solid.

**Ground texture is not an obstacle.** When placing anything with a clearance test,
exclude grass, rock stipple and canopy shading, or a colour-passed map will reject
every candidate position. A figure stands *on* grass.

### Current water state

| zone | status |
|---|---|
| Paineel | done, 23 pools |
| Toxxulia | done, both rivers, beach ink preserved |
| Kerra Isle | done, channel and bay, island knocked out |
| Lake Rathetear | derived from a painted mask (see below); the reliable method |
| Nektulos river | still the old envelope method, not redone |

---

## The kits

**`src/kit/terrain.py`** — `peak()` broken rocky summit (irregular ridgeline,
subsidiary crag, spurs, hachures, rubble foot; reads as rock rather than a
triangle symbol) · `rock_band()` · `grass_field()` · `canopy_shade()` ·
`foliage_margin()` · `scatter()` collision-aware placement.

**`src/kit/flora.py`** — fir, broadleaf, willow, dead tree, redwood, palm; bush,
fern, reeds, mushrooms, flowers, grass tuft. Interchangeable in a scatter.

**`src/kit/fauna.py`** — 15 playable races plus spider, skeleton, wolf, bat,
ratman. Ears are the through-line: dark elf longest at 0.34, high and wood elf
shorter, halflings smallest but still pointed, gnomes deliberately round, kerrans
on top of the head. Each race carries one silhouette cue that survives at 60 units.
`HOMELANDS` maps a city to its folk.

**`src/kit/darkelf.py`** — ~27 Teir'Dal pieces and the entire water system.

**`src/kit/log_module.py`** — fallen log from two `/loc` readings.

**Zones are composed from kits, never drawn one-off**, so a fix to a tree or a race
propagates everywhere.

---

## Design principles

**Colour rather than crosshatch.** Dense hatching buries labels. Tint areas with
coloured detail that text still sits on cleanly.

**Density belongs where it is true.** Feerrott is a rainforest and earns 2,247
lines per million square units of solid canopy. Nektulos is temperate and open, so
its density goes in the **margins** — selling "one clearing in a vast dark forest"
— while its colour comes off the ground. Copying Feerrott's canopy into Nektulos
would read as jungle. Nektulos reached the same 2,494 density by that route.

**Colour carries meaning.** Nektulos fades green to Teir'Dal purple approaching
Neriak, applied probabilistically by latitude so it blends rather than bands.

**Labels must be dark** — near-black blues, reds, purples. Bright labels wash out,
especially in cavern cities. Everything under luma 76.

**Margin sketches sit on the side the building actually stands.** Third Gate: Lodge
of the Dead top-left because it keeps hall in the north; Innoruuk's temple
bottom-left because the shrine is south-west.

**No stick figures.** Filled or outlined sketch shapes.

**Verify orientation geometrically**, not by eye — the Nektulos stump was upside
down for weeks. Growth rings above the midline; narrow end up for peaks and gates.

---

## Restoring hand-drawn assets from the default pack

The stock pack contains individually sketched items (fallen logs, felled trees)
that procedural rebuilds lose. **Diff per line, not per cluster** — a partly-copied
asset passes a cluster test while still missing half its lines. That mistake left
one Nektulos log with 15 of its 46 lines. Full sweep restored 68 assets to
Nektulos, 23 to ecommons, 5 to commons.

**Logs beat trees**: clear any decoration tree standing on a restored log, whole
cluster at a time so nothing is left half-drawn.

---

## Outstanding work

**Qeynos maps: repaired.** They had carried an old region-fill that ignored geometry
— flat all-horizontal runs in `(188,180,160)` and `(198,190,170)` covering a
rectangle rather than following the coast, plus a hatch flooding the catacombs.
Stripped 3,759 bad lines across the three and re-derived water from Brewall's clean
blue outlines. The tell for this failure mode: an ink whose lines are ALL horizontal
with a long median length and a rectangular bounding box.


**Swept but not yet fixed** (heuristic scan, not verified in game):
- *Water*: filled across 16 zones in the final batch. **`permafrost` and `warrens`
  were reverted** — their walls are drawn in a blue ink, so the water test misfired
  and flooded the whole dungeon. Guard against this: if the blue-ish ink is more
  than ~35% of ALL the zone's lines it is structure, not water. But do not apply
  that rule blindly either — Ocean of Tears is legitimately 47% blue. Spot-render
  before trusting a batch.
- *Near-empty decoration*: `felwitheb` (177 lines), `felwithea`, `kaladima`,
  `runnyeye`, `highkeep`.
- *Sparse zones*: done. `southkarana`, `qey2hh1`, `qeytoqrg`, `rathemtn`,
  `stonebrunt`, `sro`, `nro`, `commons`, `ecommons` all populated by biome —
  temperate gets broadleaf/fir/willow plus grass, upland gets fir and rock, desert
  gets palms and no grass. Still bare: `erudsxing` (mostly open ocean, so arguably
  correct as-is).
- *One ink dominating*: `eastkarana` is 84% one ink at density 125 — sparse and
  monotone. The dungeon entries in that list are probably just wall geometry.


1. **Lake Rathetear** southern shore — verify in game.
2. **Nektulos river** water — still the old method.
3. **Paineel** newbie area (east side) needs a tree pass; its base is also still
   the raw default palette while every other featured zone is recoloured.
4. **Kithicor** — done. The default base has only walls, logs, stumps and water, so
   the procedural discs and rings were removed from the base (48,898 → 5,860 lines),
   normal trees scattered at readable density, and the redwood mass moved to the
   margins. Note the discs had been written into the BASE layer, not decoration.
5. **Fauna additions**: kobold, gnoll, sprite, mushroom man, snake, rat, skunk,
   drake. Racial motifs per zone where appropriate.
6. **Nektulos rock shelf** boundary is estimated, not surveyed.
7. **Margin foliage** overlaps the frame border in places.
8. `wq1` — an unrecognised zone shortname the user mentioned re: Chetari. The Hole
   is `hole`. May be EQL-specific; confirm before using.

---

## Reference

- POI: `eqlwiki.com/[Zone]`, Project 1999
- EQOA names: `wiki.eqoa.live`
- Lore: `lorenorrath.free.fr` — History of Norrath, indexed by age, race, zone and
  god in `src/docs/LORE_SOURCES.md`. Cite, don't reproduce.
