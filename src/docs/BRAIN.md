# Emoda Legends Maps — project brain

Everything a fresh session needs. Read this first; it is the accumulated knowledge,
including the mistakes, because the mistakes are the expensive part.

---

## 1. What this is

A hand-drawn atlas pack for EverQuest Legends (EQL) / Project 1999, rendered in-game
by "Emoda Maps". ~79 Old World zones across Antonica, Faydwer, Odus and the Outer
Planes. Author: Brandon (bknie1), a .NET engineer who plays on EQL and verifies
everything in-game himself.

Repo: `everquest-maps` on GitHub. Ships as `maps.zip` → `D:\EverQuest Legends\maps\Emoda Maps`.

---

## 2. File format

Native EQ map text. Two record types:

```
L x1, y1, z1, x2, y2, z2, r, g, b          a line segment
P x, y, z, r, g, b, size, Label_With_Underscores
```

**CRLF line endings are mandatory.** Every file, every write. Verify after each pass:

```python
b = open(path, 'rb').read()
assert sum(1 for i, c in enumerate(b) if c == 10 and (i == 0 or b[i-1] != 13)) == 0
```

### Layers — never flatten, never merge

| file | holds |
|------|-------|
| `<zone>.txt` | base geometry: walls, water, terrain |
| `<zone>_1.txt` | POI markers and labels |
| `<zone>_2.txt` | decoration: frame, grid, title, compass, margin art, shading |
| `<zone>_3.txt` | EQOA-era places, muted violet `(150,90,150)`, set 500 years earlier |

`_1` is Brandon's work. **Never rebuild or overwrite it.** Base and `_2` are fair game.

---

## 3. The coordinate transform (critical, recurs constantly)

From an in-game `/loc` reading of `(a, b, z)`:

```
native = (-b, -a)
```

The same transform applies to wiki NPC "location" fields, which are also `/loc` values.

**Never use a raw `/loc` as-is.** This mistake has recurred across sessions —
Blackburrow's river, Toxxulia's hill. The in-game map panel *displays* raw `/loc`,
not native coordinates; the player arrow is drawn at the transformed position. Do not
be misled by the panel readout.

Always query feature coordinates from the data files. **Never estimate from image
pixels** — every wrong edit this session traced back to inferring a position from a
screenshot instead of measuring it.

---

## 4. Sources

| source | use for | never use for |
|--------|---------|---------------|
| `eqlwiki.com/[Zone]`, P1999 | POI — the only authority | — |
| Norrath Cartographers ("best") | geometry, water outlines | POI |
| Brewall's | geometry, water outlines, dungeon z-level colour convention | POI |
| `default_maps.zip` | clean bases for rebuilds | POI |

Reference packs target EverQuest Live and carry content that does not exist on EQL
or P1999. Geometry only.

**Water ink is not consistent between zones in the same source.** Toxxulia uses
`(0,0,240)`, Kerra uses `(0,0,255)`. Check per zone or a fill silently finds nothing.

---

## 5. The layout hierarchy — `kit/layout.py`

One source of truth for every boundary, so shading, grid, margin and frame cannot
disagree. This solved a whole class of bugs where shading stopped short on one side.

```
frame ⊃ margin ⊃ grid ⊃ content
```

- **content** — the base geometry's own extent. Nothing invented.
- **grid** — content plus a gap, so the map never touches the grid line.
- **margin** — where decoration lives: shading, sketches, compass, title.
- **frame** — the drawn border, outermost.

Current constants: `GAP 0.055`, `MARGIN 0.105`, `MARG_T 0.165`, `FRAME 0.020`,
as fractions of the map's long axis.

**Shading is bounded by the GRID, not by content.** Bounding by content lets the
margin motif bleed inside the grid. Brandon called this out explicitly: *"make the
grid the parent to the map content."*

Three distinct fill regions, which Brandon articulated better than I had:

1. **margin** — between grid and frame. Foliage, sketches. Solved.
2. **map interior** — inside the drawn map. Foliage on the playable area. Solved.
3. **grid space outside the map** — leftover room where tunnels run to the edge.
   *Not solved.* This is why Feerrott's grid gaps look empty.

---

## 6. Titles — the hardest problem in this project

Titles are drawn in the same ink as margin texture, so they cannot be found by
colour. Every attempt to remove one surgically took letters with it or left a ghost.

### The discriminator that works: CONNECTIVITY

**Letters connect end-to-end. Texture hatching is isolated strokes. Frame rules are
connected but far too long.**

`kit/titles.py`:

- `find_title(deco, grid)` — connected components, letter-sized, sharing a baseline
  and a height, evenly pitched.
- `verify(deco, grid, name)` — template match. Divide the title's span into as many
  columns as the name has letters; check strokes land in each. **Use as a gate.**
  54 of 74 zones verify. If it returns `ok=False`, do not touch that zone.
- `find_ghosts(deco, grid, new_height, scale)` — old titles that bleed *below* the
  grid top, over the map. A wipe of the band above the grid cannot reach these.
  Found ghosts in 26 zones.

### The safety rule — `build.title_health()`

Connected strokes above the grid. **Measure before and after every pass. If it drops,
roll back rather than write.** This is the single most valuable check in the project.
Adding it ended a long run of title damage.

### When surgery fails: wipe and redraw

If a title is tangled with texture, do not try to extract it. Delete everything above
the grid, then redraw: **title first, reserve its box, then texture around it.**
Reserving the box *before* laying texture is what makes it clean.

### Sizing

Fit to grid width, never exceed it — a title wider than the grid reads as a muffin
top. Loop shrinking height by 0.86 until it fits under ~0.90 of grid width. Dungeon
titles land around height 90–150. Bottom gap to the grid ≈ 3.5% of scale.

---

## 7. Water

### Fill algorithm

1. Take the base's own water outline (check the ink per zone).
2. **Repair breaks**: stitch loose endpoints, but **only short ones — under ~70
   units.** Pairing every loose end by nearest neighbour drew a chord straight
   across Kerra's bay and cut it in half.
3. Even-odd scanline fill per row.
4. **Prove containment**: re-derive crossings for every run and drop any that does
   not sit inside a crossing pair. Target zero failures.

### Hard-won rules

- **Never use `both_axes` scanning in dungeon interiors.** It pairs crossings across
  unrelated chambers and invents water. New Sebilis had 700 spurious runs; the real
  answer was 73 in two pools.
- **Missing blocks come from unclosed boundaries**, not from the fill logic. An odd
  crossing count leaves a row unpaired. Stitch first, then fill.
- **Inverted rows**: if a short run sits inside the neighbouring rows' span, the
  pairing flipped and it is filling an island. Replace with the two flanking runs.
- Pre-coloured multi-level dungeons use teal/blue/gold where **blue is elevation, not
  water**. Kedge, Blackburrow, Butcherblock, Permafrost, Warrens, The Hole, the Sol
  dungeons. Restore a depth ramp instead of filling.
- Flora is land evidence: fill crossing trees is wrong regardless of the arithmetic.
- Clip under bridge decks horizontally within the deck's x-extent only. Do not drop
  whole rows.

---

## 8. The halo (exterior shading)

Makes tunnels pop and read as underground. Brandon: *"outline the tunnels… the
shading to be in the 'margin' outside space."*

1. Rasterise the map geometry to an occupancy grid.
2. **Flood-fill from the map edge** to mark what is genuinely outside.
3. Hatch only outside cells within ~3 cells of a wall.

Without the flood fill, chamber interiors get hatched too — the dilation has no
concept of inside vs outside. That fix cut it from ~5,000 stipple strokes to a clean
rim of ~1,000–2,500.

**Give the halo its own ink, distinct from the lined border.** They were identical on
eight zones, so the next border pass stripped the halo. Anything that shares an ink
with something else will eventually be deleted by a pass aimed at the other thing.

---

## 9. Kits

| module | contents |
|--------|----------|
| `flora.py` | 12 shapes, low fidelity (13–25 lines) — legacy |
| `flora_hd.py` | 12 shapes rebuilt with hatched fill (60–201 lines) |
| `fauna.py` | 15 races + 13 creatures, low fidelity (~20 lines) — **needs HD pass** |
| `terrain.py` | peak, hill, volcano, snowdrift, mudflat, ruin_arch, rock_band, cloud |
| `nse_decor.py` | Iksar: glyph, bookshelf, standard, wall_candle, root_drip/burst/bunch |
| `gnome_decor.py` | gear, gear_pair, pump, cog_tower, lantern, pipe_run |
| `civic_decor.py` | 23 shapes covering the other twelve races |
| `darkelf.py` | Neriak set: monolith, brazier, rune_panel, sigil, web_corner, gate |
| `races.py` | race → figure + decor + flora + terrain. `missing_decor()` returns [] |
| `sketches.py` | re-exports the general-purpose shapes |

### What makes a shape read well

The good ones — bookshelf 326 lines, root_bunch 262, iksar_glyph 164 — use:

- **hatched fill** via even-odd scanline inside the outline
- **tapered forms** drawn as two edges plus internal ticks, not single strokes
- **a shadow side**: a second darker ink on the lower or trailing edge
- **internal structure**: shelves, ribs, bark, ring scars

A single-stroke line reads as wire. Two offset strands read as a root.

### Still to do

`fauna_hd.py` — 15 races and 13 creatures at the same fidelity. The current ones are
~20 lines each and read as stick figures, which Brandon has rejected before.

---

## 10. Zone knowledge

| zone | notes |
|------|-------|
| Crushbone | a clearing in Faydark. Big dense trees pouring over the grid edge, claustrophobic. Not underground. |
| Oggok | ogre city deep in the Feerrott. Dense jungle around, city itself clear. Crumbling aqueducts, temple structures — Klingon-like before the curse. Water in the bottom-right quadrant, spiral shape, docks. |
| Grobb | troll city in Innothule swamp. Should read as a mud pit more than a map. |
| Halas | barbarian ice. Mountains treated like trees around the map. Two peaks inside the grid beside the entry tunnel. |
| Ak'Anon | gnome cave. **No trees.** Clockworks, pumps, green diamond checkpoint lanterns. The O in the title was a gear. |
| Erudin | Prexus / water motif, but the water was overdone — start from base. |
| Qeynos | Camelot, good-aligned humans, paladins. |
| Freeport | desert mercenary city, evil-tolerant, Ottoman/Dornish flavour. |
| Kaladim, Felwithe A/B | **legitimately have greenery.** Do not strip as "underground". |
| Kithicor | dark forest, redwoods, should be denser — look at Nektulos and Feerrott. |
| East Karana | eastern ~50% is rocky mountain, treacherous. Lean into mountains. |
| Oasis | the desert colouring Brandon likes most. Dune treatment. N.Ro / S.Ro are lower desert, less dunes. |
| Najena | dark elf and magic. Angular title curving down at both ends like a frown. Spiderweb motif. |
| New Sebilis | iksar. Base is clean; problems were all in `_2`. |
| Nagafen's Lair | big red dragon. |
| The Warrens | underground waterway caverns, kobolds. Links Paineel and Stonebrunt. |

---

## 11. Working method

**Snapshot before any multi-zone transform.** `cp -r "Emoda Legends Maps" snapN`.
This saved the project repeatedly.

**One zone at a time with a check before writing** beats a batch every time. Every
batch pass this session caused damage: 64 titles deleted, 27 dungeons stripped of
margin texture, Kaladim and Felwithe stripped of legitimate greenery.

**Guard clauses that earned their place:**

```python
if len(dropped) > len(all_lines) * 0.25:  raise   # strip too broad
if title_health_after < title_health_before: rollback
if containment_failures > 0: do not write
if shading_inside_grid > 0: do not write
```

**Ask what ink the thing actually is** rather than assuming. Steamfont's windmills
were found by matching an exact 18-segment signature after aspect-ratio filters kept
missing them. Ak'Anon's stray forest was `(62,104,56)` — Crushbone's ink, from a
batch that overreached.

**Validators to run after every pass:**

```
python src/tools/validate_titles.py      # 79/79 zones must have a title
python src/tools/validate_overlay.py --fix   # decoration standing in water
```

---

## 12. Outstanding work

**Highest value**
- `fauna_hd.py` — HD pass on 15 races + 13 creatures
- Fill region 3: grid space outside the tangible map (Feerrott's empty gaps)
- Erudin water: start from base, much less of it
- Oggok water in the bottom-right quadrant

**Zone-specific**
- Halas: mountains inside the grid by the entry tunnel
- Ak'Anon: gear as the O in the title
- Grobb: Innothule mud-pit treatment across the grid
- Crushbone: trees larger still, pouring further onto the grid
- Kithicor / Nektulos: denser border forest
- East Karana: mountain motif over the eastern half
- Unrest: hedge maze shading
- Everfrost, Gorge, Permafrost, Kedge, Felwithe: halo pass
- EQOA `_3` arrows: halve length, labels at the start, keep in the margin
- Dungeon interior shading (Guk-style rock between tunnels) on ~11 dungeons

**Not started**
- Plane of Fear: Cazic-Thule symbolism
- Plane of Hate A/B: Innoruuk symbolism

---

## 13. Things I got wrong, so you do not repeat them

1. **Inferring positions from screenshots.** Every wrong edit. Read coordinates from
   the file.
2. **Writing a rule that matched more than intended, then running it across 79 zones.**
   Deleted 64 titles once and 27 zones' margin texture another time.
3. **Assuming a title could be found by colour.** It cannot. Use connectivity.
4. **Filling every closed shape when asked to fill one.** Lavastorm: filled 26 pools
   when Solusek's Eye was the ask.
5. **Sharing an ink between two features.** The halo and the lined border were
   identical on eight zones; the border pass silently ate the halo.
6. **Trusting a validator that only checks what is easy to measure.** Line counts,
   CRLF and colour ranges all passed while 64 maps had no title at all.
7. **Declaring exhaustion instead of fixing the problem.** Brandon called this out
   and was right to.
8. **Drawing shapes inline in a build script.** That is how the original `nse_decor`
   was lost before it reached the repo. Anything used on a map goes in a kit.
