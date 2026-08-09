# Conventions

## Coordinate transform
Every in-game `/loc` converts as `native = (-loc2, -loc1)`. This holds for NPC
positions taken from wikis too, since those are `/loc` values. The in-game map
panel displays the raw `/loc`, not native coordinates.

## Water
`darkelf.water_flood()` is the one to reach for on a real map. It rasterises every
line — shoreline and structure alike — as a wall, labels the open regions between
them, and calls a region water when enough of its border is shoreline.

Hard-won details, each of which produced a visible bug:
- Shorelines are often drawn two to four times over themselves. Coincident
  crossings must collapse before any even-odd test, or parity cancels out and
  moats and islands come out inverted.
- A bridge is a corridor open at both ends: structure on two opposite sides within
  a short reach means walkway, never water.
- Undersized bodies are artefacts, not puddles. Drop anything under ~24 runs.
- Solid fill (one continuous run per row) reads far better than hatching, and is
  cheaper.

## Orientation
The game renders maps in the same orientation as a plain top-down render with
`screen_y = native_y - min`. Sketches with an obvious up/down should be verified
against a known-good landmark rather than assumed.
