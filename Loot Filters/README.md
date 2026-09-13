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
| 4  | Sell   | Auto-sell: true vendor trash only (no equipment — see below) |

**Anything not on the list is simply not filtered** — the game handles it normally.
This matters because equipment is deliberately *left off the list entirely* rather
than assigned a filter ID (see below).

## LF_Emoda_Legends.ini

Built from the old `LF_My_Loot_Filter.ini` (which had **everything** set to Sell,
including motes, spells, and every weapon/armor drop) unioned with the live character
filter. Categories rescued from the sell pile:

- **Loot (1):** all Motes of Potential, every `Spell:`/`Song:` scroll, Elemental/Timeless Silk patterns
- **Merge (2):** research mats (Words of / Rune of / Tasarin / Salil / Velishoul / Magi`kot & Mastery pages),
  silks + spinneret fluids, pelts/skins/hides/furs/scales, ores + metal chunks + clay,
  jewelcraft gems (exact names only, so "Onyx Ring" still sells), baking mats (meats, eggs,
  milk, honey, nectar, mushrooms, fresh fish, grapes, hops), poison mats (glands, venom sacs,
  vials, consigned poison vials), essences, marrow, bone chips, feathers, reagents
  (Fire Beetle Eye, Fish Scales, Crystallized Sulfur, Roots), and classic XP quest turn-ins
  (Crushbone Belt/Shoulderpads, Deathfist Shoulderpads, Gnoll Fang, Bandit Sash)
- **Store (3):** the 28 items set to Store in-game on the character filter
- **Omitted (not on the list at all):** every weapon, piece of armor, jewelry item, and
  bard instrument — ~2,090 items. The filter is keyed by item ID, not by the magical
  modifier a drop rolls (a "Rusty Mining Pick" can drop as "Rusty Mining Pick +1"), so
  equipment never gets auto-sold by this list, full stop — no exceptions, no "but this
  one's obviously junk." Detected by weapon/armor/jewelry/instrument keywords in the
  name (plain substring for compounds like "Legplates"/"Warhammer", boundary-guarded
  for short/common words like "Cap"/"Harp" so they don't false-match inside unrelated
  names), extended by icon correlation (this itemization draws every item of one
  weapon/armor TYPE with the same icon, so an exotic proper-noun weapon the keywords
  miss — "Gladius", "Ghoulbane", "Devlas Ilkvel" — still gets caught via a keyword-matched
  icon-sibling), and topped off with a short exact-name list for the handful of unique-icon
  exotics neither pass can reach. When in doubt, an item is left off the list rather than
  sold — a handful of genuine junk items with gear-sounding or coincidentally-overlapping
  names (a "Barbed Leather Whip"-shaped material, ammunition-adjacent trophies) end up
  omitted too; that costs nothing since omission just means "not auto-sold," never
  "wrongly sold."
- **Sell (4):** everything else — true non-equipment trash (~1,280 items): body parts,
  keys, quest fluff, tomes/pages, runes, discs/bars/ingots, totems, potions, and the like.

## Rebuilding

`build_loot_filter.ps1` regenerates the file from the two inis in `userdata` and contains
all the classification rules (gear-detection keyword/icon passes, gem whitelist, material
regexes). Edit the rules there, run it, then copy the output to `userdata\LF_Emoda_Legends.ini`.
