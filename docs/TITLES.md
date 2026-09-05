# Title Campaign — Rules & Branch Instructions

The goal: every map's title is a piece of hand-drawn identity, distinct per zone.
The pale homogenized block-caps family is **deprecated**. The bar is **Unrest**
("dripping with style"); the floor is anything that reads as a stick font.

Per-zone facts (text, length, bbox, inks, style class, notes) live in
`docs/zones/<zone>.md`. These are dev-only and never ship in a release.

## The Rules

1. **Never replace a stylized title with the stick font.** `fix_title.py`'s
   letterforms are a downgrade, always. If a stylized title clips or collides,
   scale it IN PLACE (uniform, about its own center, re-anchored to its slot).
   This rule has been violated once (Nagafen's Lair) and the cost was an
   archaeology session.

2. **History first.** Before designing a new title, check whether a better one
   existed and was homogenized away:
   ```
   git log --oneline --follow -- "Emoda Legends Maps/<zone>_2.txt"
   git show <sha>:"Emoda Legends Maps/<zone>_2.txt" > old.txt   # then plot it
   ```
   Paineel, Kerra Isle, and Toxxulia all had 3D extruded wireframe titles at
   cf13a9a~1 / 871c51a; they were restored verbatim in 2026-09. The Freeport
   trio had a styled EAST/WEST FREEPORT two-tier treatment in the 871c51a beta
   that is still unrecovered — that is the first archaeology target.

3. **Verify the selection before transforming it.** Plot the strokes you
   believe are the title ALONE on a blank canvas and confirm it reads as
   exactly the letters — border waves, compasses, arrows, and rules share inks
   and stroke lengths with lettering. Two Befallen attempts moved letters
   because clustering chained figures into the T; ink-selection fixed it.

4. **Separate by ink when geometry lies.** If the title has its own ink
   (record it in the zone's .md), select by ink, not by bounding box.

5. **Title band = strokes with midpoint y above `grid_top + 40`** in the `_2`
   layer. When transplanting from history, replace only that band; everything
   below is live decor.

6. **Render before and after, every time.** `python src/tools/render_zone.py
   <zone> --out check.png`. A title change with no render is not done.

7. **Distinct means themed, not random.** The style should come from the zone:
   Najena's hatched cartouche, Sol B's warm arc, Kaladim's chisel-cut caps.
   Materials, curvature, and flourish are the levers; the parchment palette is
   not — stay inside the atlas's inks (no neon, luminance in the map's range).

8. **Keep the string.** The title text and its character count are recorded in
   the zone's .md. Never rename a zone while restyling it, and keep the new
   art inside the recorded frame width with ~30u clearance to the grid top.

9. **CRLF, native format, `_2` layer only.** Titles live in the decoration
   layer. `L x1,y1,z1,x2,y2,z2,r,g,b`, CRLF line endings, or the client drops
   the file.

10. **Update the zone's .md after any title change** — new bbox, inks, style
    class, and a one-line note on what was done and why.

## Deprecated family — how to recognize it

Single ink near (120,105,85), plain rectilinear caps, one stroke weight, no
extrusion/shadow/flourish. The zone .md files mark these as
`pale-caps (DEPRECATED family)`. They are candidates, not emergencies: replace
one only when you have a themed design or a historical original, never with a
different generic.

## Status (2026-09-05): the city slate is DONE

The lettering engine lives in `src/titles/` — `glyphs.py` (complete A-Z
skeleton with a selftest so no glyph ever ships broken again), `styles.py`
(the racial families), `apply_title.py` (band swap with per-zone removal
configs). 20 city maps done in one pass: the Freeport trio + sewers
(extruded two-tier, fresh design in the beta's spirit), Qeynos pair + qcat
(stately), Erudin pair (refined), Halas (runic), Grobb/Oggok (crude),
Neriak trio (darkelf), Felwithe pair (highelf), Rivervale (rounded),
Ak'Anon (clockwork), Surefall (sylvan). `src/tools/eqqms.py` measures the
pack and refreshes `docs/zones/*.md`.

## Remaining queue

1. Wilderness/dungeon zones whose .md says `plain caps` and whose theme
   suggests an obvious material (ice for Everfrost/Permafrost, lava for
   Lavastorm, vines for Faydark, coral for OOT/Erud's Crossing…) — add a
   family to `styles.py`, add a ZONES config to `apply_title.py`, dry-run,
   render, apply.
2. eqqms `title-clipped` flags: mostly band decor beyond the frame line
   (noise), but audit the dungeon ones (soldungb, gukbottom, newsebexp).

Locked zones (never touch): **unrest**, **eastkarana**. Exemplars to study
before drawing anything: unrest, soldungb, najena, kaladima/b, paineel.

## Workflow for one zone (for a lower model / branch)

1. Read `docs/zones/<zone>.md`. Note title text, bbox, inks, and warnings.
2. Run the history check (Rule 2). If a stylized original exists, restore it
   verbatim (band-swap per Rule 5) and stop — restoration beats redesign.
3. Otherwise design: sketch the letterforms as L-strokes in a script under
   `src/titles/<zone>_title.py` that emits the band; keep letter height close
   to the old band's, width within the frame.
4. Replace the band, render, and eyeball at full size AND at 900px width
   (in-game scale). Letters must survive both.
5. Update the .md, commit with a message that names the style
   ("freporte: EAST FREEPORT two-tier beta lettering restored"), deploy by
   copying the changed `_2.txt` to the live folder.
