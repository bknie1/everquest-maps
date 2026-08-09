# EQOA / EQ1 zone map alignment

The `_3` layer carries EQOA place names positioned against EQ1 geography, so a
player who knows one world can find their bearings in the other.

Two forms are used:

- **diamond** — the terrain persists, or a real EQ1 feature stands on the spot
- **signpost** — an arrow and label pointing off-map toward somewhere that is not
  reachable in EQ1, sized by distance (near 4, mid 3, far 2)

A name that is a walkable EQ1 zone never becomes a signpost — pointing at
somewhere you can simply travel to is noise. `tools/eqoa_pos.py` holds that
`WALKABLE` set alongside the positions.

## Coverage — 36 zones carry a `_3` layer

| zone | labels | line work |
|---|---|---|
| beholder | 11 | 34 |
| blackburrow | 11 | 33 |
| cazicthule | 10 | 30 |
| commons | 11 | 34 |
| eastkarana | 11 | 34 |
| ecommons | 10 | 30 |
| erudnext | 4 | 12 |
| erudsxing | 3 | 9 |
| everfrost | 15 | 48 |
| feerrott | 12 | 38 |
| highpass | 11 | 34 |
| innothule | 11 | 34 |
| kerraridge | 10 | 9 |
| kithicor | 12 | 38 |
| lakerathe | 10 | 30 |
| lavastorm | 10 | 4839 |
| misty | 10 | 30 |
| nektulos | 10 | 30 |
| neriaka | 13 | 0 |
| neriakb | 12 | 0 |
| neriakc | 11 | 0 |
| northkarana | 10 | 30 |
| nro | 11 | 34 |
| oasis | 11 | 34 |
| paineel | 4 | 12 |
| qey2hh1 | 10 | 30 |
| qeytoqrg | 11 | 34 |
| qrg | 10 | 30 |
| rathemtn | 11 | 34 |
| rivervale | 10 | 30 |
| southkarana | 14 | 46 |
| sro | 12 | 38 |
| steamfont | 1 | 9156 |
| stonebrunt | 6 | 18 |
| tox | 7 | 23 |
| warrens | 3 | 9 |

**Totals:** 349 labels, 14904 lines of diamond and signpost geometry.

## Conventions

- Names verified against `wiki.eqoa.live`; modern renames kept (Ruins of
  Klik'Anon, Ruins of Fayspire, Old Rogue Clockworks, and so on).
- Ink is a muted violet, distinct from every EQ1 marker colour.
- The layer is never merged into base or `_2`.
- Label anchors sit at the arrow's tail, offset by `min(w,h)*0.028`.
