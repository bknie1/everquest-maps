# THE PLAYBOOK — how to work on these maps without breaking them

Read this whole page before touching a zone. Every rule here was paid for with a
broken map. If an instruction conflicts with your instincts, follow the
instruction.

## The five laws

1. **The base map (`<zone>.txt`) is the map.** Rooms, terrain, water polygons.
   You almost never edit it (exceptions: shade_city writes roof fills there;
   approved water restyles). `_1` = POIs (append/z-fix only). `_2` = decoration.
   `_3` = EQOA history (violet 150,90,150).
2. **Never delete what you can't redraw.** Old `_2` layers hold hand-made
   motifs: fog borders, grids, banners, spiderwebs. Stripping them "to clean up"
   destroyed Blackburrow's flavor and Mistmoore's fog. Enrich by APPENDING;
   rebuild from scratch only when a human confirms the layer is junk.
3. **Budget ≈ 31,000 strokes per zone, all layers.** Over it, the client stops
   drawing at distance. Check first; if a zone is over, it needs DEDUP, not art.
4. **The title band and compass are sacred.** Nothing gets placed in the top
   margin, and the compass lives in a clear corner (bottom preferred).
5. **CRLF line endings on every write** or the game won't read the file.

## The one command

```
python src/tools/zone_pass.py <zone> --probe     # ALWAYS probe first
python src/tools/zone_pass.py <zone>             # wiki-driven figure pass
python src/tools/render_zone.py <zone>           # then LOOK at the render
```

`zone_pass` enforces the laws: appends only, refuses over-budget or
already-rich margins, keeps out of the title band and compass, picks races from
`src/data/wiki/<zone>.md`, and uses the silhouette figures.

## Figures: fauna_sil.py only

`from fauna_sil import SIL, HEIGHT` — solid-silhouette race figures, the only
style that reads at map scale (hatched wireframes blur into blobs; Brandon read
hatched dark elves as gnolls). All classic races exist: dark_elf, high_elf,
wood_elf, erudite, human/guard, barbarian, halfling, gnome, dwarf, troll, ogre,
iksar, froglok, gnoll, kobold, skeleton (bare bones + weapon — NEVER armored or
robed). Scale figures with `HEIGHT[name]` so ogres tower and gnomes stay small.

Adding a figure? Copy the style: 3–6 solid polygons, upright posture for
upright races, ONE exaggerated racial marker, palette accent that pops on
parchment. Render a contact sheet AND a ~50px map-scale strip before shipping.

## Zone-type recipes

- **Dungeon:** figures from wiki + `--flora dead_tree` where fitting. Depth
  ramps (color per level) live in the base — don't recolor without approval.
- **City:** `shade_city <zone> --walls <ink>` (writes into the BASE — commit
  both files), then zone_pass with the owner race + `civic_decor` props via
  build.place. Reference: Qeynos, Neriak.
- **Wilderness:** biome flora + wildlife figures. Sparse margins only.
- **Water:** never a scanline rectangle. Restyle = keep ~45%, sine-wave the
  lines, break into dashes (see Qeynos/Erudin commits). Ponds = flood-fill the
  enclosed polygon at Brandon's /loc, native = (−loc_b, −loc_a).
- **Signature motifs:** in-game captures become bespoke decor modules
  (najena_decor.banner). Ask for a screenshot when a zone has known heraldry.

## Verify or it didn't happen

Render before and after. Compare. If anything you didn't intend changed, revert
(`git checkout -- <file>`) and rethink. Deploy = copy changed txts to
`D:\EverQuest Legends\maps\Emoda Maps` (the live folder). Commit small, push,
and let the timelapse/wiki Actions rebase you (`git pull --rebase`).
