# Emoda Legends Loot Filters

Curated loot-filter lists for the Emoda Legends server. The game reads these from
`D:\EverQuest Legends\userdata\` as `LF_<name>.ini`; the repo copy here is the source of truth.

## File format

```
#ITEM_ID^FILTER_ID^ICON_ID^ITEM_NAME
```

Filter IDs (column order in `EQUI_LootFiltersWnd.xml` — Loot / Merge / Store / Sell):

| ID | Action | Used for |
|----|--------|----------|
| 1  | Loot   | Always loot: motes, spell/song scrolls, elemental silk patterns |
| 2  | Merge  | Auto-merge: stackable tradeskill mats and quest turn-ins |
| 3  | Store  | Auto-store: hand-picked gear (preserved from in-game choices) |
| 4  | Sell   | Auto-sell: vendor trash (weapons, armor, body-part junk) |

## LF_Emoda_Legends.ini

Built from the old `LF_My_Loot_Filter.ini` (which had **everything** set to Sell,
including motes and spells) unioned with the live character filter. Categories rescued
from the sell pile:

- **Loot (1):** all Motes of Potential, every `Spell:`/`Song:` scroll, Elemental/Timeless Silk patterns
- **Merge (2):** research mats (Words of / Rune of / Tasarin / Salil / Velishoul / Magi`kot & Mastery pages),
  silks + spinneret fluids, pelts/skins/hides/furs/scales, ores + metal chunks + clay,
  jewelcraft gems (exact names only, so "Onyx Ring" still sells), baking mats (meats, eggs,
  milk, honey, nectar, mushrooms, fresh fish, grapes, hops), poison mats (glands, venom sacs,
  vials, consigned poison vials), essences, marrow, bone chips, feathers, reagents
  (Fire Beetle Eye, Fish Scales, Crystallized Sulfur, Roots), and classic XP quest turn-ins
  (Crushbone Belt/Shoulderpads, Deathfist Shoulderpads, Gnoll Fang, Bandit Sash)
- **Store (3):** the 28 items set to Store in-game on the character filter
- **Sell (4):** everything else (~3,370 items)

## Rebuilding

`build_loot_filter.ps1` regenerates the file from the two inis in `userdata` and contains
all the classification rules (gear exclusions, gem whitelist, material regexes). Edit the
rules there, run it, then copy the output to `userdata\LF_Emoda_Legends.ini`.
