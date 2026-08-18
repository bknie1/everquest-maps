# EQ Legends Maps — build sources

*Drops into the repo's `Developer/` folder.*

Hand-drawn atlas of the classic EverQuest Old World, rendered in the EQ native
`L`/`P` line format for Emoda Maps. Files are CRLF; every layer is written
separately and never flattened.

## Layout

| folder | what lives there |
|---|---|
| `kit/` | reusable art assets — the pieces any zone can draw from |
| `toolkit/` | map primitives: canvas, frame, grid, title, compass, doodles |
| `zones/` | per-zone build scripts |
| `tools/` | cross-atlas utilities: validation, sweeps, alignment, EQOA layer |
| `docs/` | conventions, and an index of lore sources |
| `design/` | review renders, kit catalogues, EQOA alignment, source archive |

`docs/LORE_SOURCES.md` indexes the History of Norrath archive by age, race, zone and
god, so a sketch or a race silhouette can be checked against the lore before it is drawn.

## Previewing maps

Two ways to see a map without launching the game:

- **`preview.html`** (at the repo root) — open it in any browser (no server, no
  install), click *Open maps folder…* and point it at `Emoda Legends Maps`. Zone list
  with filter, per-layer toggles (base / POI / deco / EQOA), labels on/off, pan with
  drag, zoom with the wheel, double-click to re-fit. Everything stays local; nothing
  is uploaded.
- **`tools/render_zone.py`** — batch-render zones to PNG on parchment:

  ```
  python src/tools/render_zone.py                  # all zones -> renders/
  python src/tools/render_zone.py halas oggok      # just these
  python src/tools/render_zone.py --layers 02      # base + deco only
  ```

  Requires `pillow`. Used to produce the gallery renders and review sheets.

## `kit/`

- **`terrain.py`** — `peak()` broken rocky summit · `rock_band()` brown rock over a
  region · `grass_field()` ground colour that labels still read over ·
  `canopy_shade()` deepen a crown · `foliage_margin()` packed forest for margins ·
  `scatter()` collision-aware placement, used by all of them
- **`flora.py`** — fir, broadleaf, willow, dead tree, redwood, palm; bush, fern,
  reeds, mushrooms, flowers, grass tuft. All interchangeable in a scatter.
- **`fauna.py`** — every playable race as a side-on silhouette: dark/high/wood
  elf, halfling, gnome, dwarf, barbarian, troll, ogre, Qeynos and Freeport
  humans, kerran, erudite, **froglok**, **iksar**; plus spider, skeleton, wolf,
  bat and **ratman** (Chetari and kin). `HOMELANDS` maps a city to its folk so a
  zone can be populated plausibly.
- **`darkelf.py`** — the Teir'Dal set: arched gate, triquetra, crest, Innoruuk
  star and mask, rune wall and panels, barred gate, graffiti, library facade,
  Lodge of the Dead, bastion, brazier, candelabra, torch, waterfall, monolith,
  cavern edge, webs — and the water system (`water_flood`, `water_fill`).
- **`log_module.py`** — fallen log from two `/loc` readings; infers orientation,
  length, taper, end grain and branch stubs.

## Conventions

- **Coordinates.** `native = (-loc2, -loc1)`. Never use a raw `/loc` as-is.
- **Layers.** base = geometry · `_1` = markers · `_2` = decoration · `_3` = places
  and the EQOA layer. Never flattened.
- **Colour, not crosshatch.** Tint an area with coloured assets; dense hatching
  buries labels. Grass and rock stay open enough to read text over.
- **Density belongs where it is true.** Feerrott is a rainforest and earns a solid
  canopy; Nektulos is temperate, so its density goes in the margins and its colour
  comes off the ground.
- **POI authority** is EverQuest Legends and P1999. Other packs are consulted for
  base geometry only.

## Size note

`design/` holds 83 PNGs and the upstream source packs — about 66 MB in total, most
of it `design/sources/`. If that is heavier than you want in git history, those two
archives are the things to move to LFS or to an external release; everything else in
the repo is text and small.
