# The Emoda Standard — target for 0.2-alpha

The bar every zone should clear. Set by the zones that got a full pass; this
document names it so the rest can be brought up to it.

## Reference zones (what "done" looks like)
- **New Sebilis** — overall quality bar (dungeon).
- **Estate of Unrest** — flagship dungeon: biome/mood, water & depth shading,
  floor z-calibration, hue-coded floors, POIs with mechanics, off-map legend,
  even themed margins.
- **Freeport trio, Grobb, Oggok, Halas** — city standard: building/roof shading
  (shade_city), race-specific motif kit, wiki-sourced POIs, living themed
  margins, a proper compass.
- **East Commonlands, the Karanas, Toxxulia** — wilderness standard: biome ground
  cover (meander grass / Faydwer forest floor / desert dashes), terrain shading,
  themed margins.

## The checklist every zone must pass
1. **Title** — clean, correctly lettered in its band; NO old-title artifacts,
   ghosts, stray carets/rules, or double-thick bands.
2. **Compass** — one proper rose (ring + rays + N/E/S/W), correctly placed; no
   scattered loose letters, no broken knockout, no leftover old compass.
3. **Frame** — intact border on all four sides.
4. **Margins** — complete and even on all four sides with zone-appropriate
   decoration; no bald patches, no broken/half-drawn shading pattern.
5. **Biome correctness** — treatment matches the real zone (Ak'Anon = cave +
   clockwork, NOT forest; deserts = sand; Faydwer = forest floor; ice = snow).
6. **Feature shading** — water filled AND CONTAINED (never bleeding into
   buildings/structures); mountains shaded; multi-level dungeons use a depth
   ramp; cities have shaded buildings/walkways.
7. **Race/faction motifs** — present where a race owns the zone.
8. **POIs** — accurate to the EQL wiki, correct positions and floor z.
9. **Budget** — under ~31k total strokes; base deduped.
10. **No broken shading patterns** — the recurring bad-scanline/partial-hatch
    bug (seen on Plane of Sky and others) must be gone.

## Pass categories (how a zone gets brought up)
- `city-pass` — full shade_city + motifs + POIs + margins (Qeynos, Ak'Anon, etc.)
- `dungeon-pass` — Unrest-style depth/water/floor/POI treatment
- `wilderness-pass` — biome ground cover + terrain shading + margins
- `plane-pass` — the outer planes (Fear/Hate/Sky) with their god symbolism
- `artifact-cleanup` — remove old title/compass artifacts
- `compass-fix` — rebuild/relocate the compass
- `water-fix` — contain overflowing water / add missing water
- `shading-fix` — repair broken shading pattern / add missing margin shading
- `biome-fix` — wrong biome (e.g. Ak'Anon forest → cave)
- `dedupe` — over-budget base needs deduplication
