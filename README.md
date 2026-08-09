# Custom EQ Atlas Maps by Emoda

Atlas-style in-game map files for **EverQuest Legends** and **Project 1999**, built zone
by zone. The look is a 2D contour map with 3D-effect features: parchment background,
color-coded points of interest, themed hand-crafted borders, etched titles, compasses,
and zone-appropriate decorative sketches.

It's just vector math. You can do cool vector art.

**79 zones · 274 files · 1,556 markers · 349 place and EQOA labels.**

---

External demo renders (pardon any visual issues; labels render differently in-game)

<img width="700" height="1074" alt="ak_full" src="https://github.com/user-attachments/assets/b6a0f60b-3fbb-4b8a-bd2d-ec686c11b75d" />

---

## What makes these different

Most map packs are wireframes with labels — accurate, and a bit lifeless. These are
drawn as **maps**, the way an in-world cartographer would have made them.

- **Terrain is shaded, not just outlined.** Rivers and lakes fill solid blue, forests
  carry canopies, rock shelves shade brown, grassland tints green. You can tell at a
  glance what you're looking at.
- **Every zone has a face.** A carved title, a grid, a compass, and margin sketches of
  things that actually stand in that zone — Neriak's gate with its trinity knot, the
  Lodge of the Dead under its red pagoda roof, Innoruuk's temple, the library colonnade.
- **The world is populated.** Zones carry small figures of the folk who live there:
  halflings in the southwest of Nektulos, Teir'Dal in the northeast, spiders and
  skeletons between them.
- **Color carries meaning.** Nektulos fades from green in halfling country to Teir'Dal
  purple as you approach Neriak. Feerrott is dark because it's a dense jungle. The
  color is telling you something.
- **An EQOA layer.** Five hundred years of history laid over the same ground — see below.

The one rule behind all of it: **color rather than crosshatch.** Dense hatching buries
labels and makes a map harder to read, so areas are tinted with colored detail that text
still sits on top of cleanly.

---

## Install

1. Download **`maps.zip`** from the [latest release](../../releases).
2. Extract it into your EverQuest maps folder:

   ```
   EverQuest Legends\maps
   ```

   The zip contains an **`Emoda Legends Maps`** folder, so extracting there gives you
   `maps\Emoda Legends Maps` — which is where it belongs. Extract *into* `maps`, not
   into a folder you've made yourself, or you'll end up one level too deep.
3. Restart the client, open the map (default **`M`**), and pick **Emoda Legends Maps**
   from the dropdown at the top-left.

On P1999 the maps folder is usually `EverQuest\maps`; the same steps apply.

Because everything lives in its own folder, your existing maps are untouched and you can
switch between packs from that dropdown at any time.

**Don't merge these into a folder that already has map files.** A recolored base replaces
the original `zonename.txt` — with both present every wall draws twice.

### Updating

Extract the new zip over the old folder and overwrite. Nothing is stored outside the map
folder, so there's no state to migrate, and uninstalling is just deleting the folder.

---

## How the files work

Each zone is drawn as up to four stacked layers the client overlays. Every one toggles
from the numbered buttons in the map window:

| File | Layer | Contents | Turn it off when |
|---|---|---|---|
| `zonename.txt` | **base** | Zone wall geometry. Some zones ship a **recolored** base, tinted by area or floor, water shaded. | never — this is the map |
| `zonename_1.txt` | **markers** | Color-coded POI: NPCs, vendors, quest givers, exits, danger flags. | you want a clean map for screenshots |
| `zonename_2.txt` | **decoration** | Border, grid, title, compass, terrain shading, themed margin sketches. | you prefer a plain functional map |
| `zonename_3.txt` | **extra** | Place names in cities, effect overflow, and the **EQOA easter-egg labels**. | the extra labels are more than you need |

Layers are independent, so you can run markers without decoration, decoration without
markers, or the bare base. Nothing depends on anything else being loaded.

**Format:** EQ native L/P line format with **mandatory CRLF (`\r\n`) line endings**.

- `L x1, y1, z1, x2, y2, z2, r, g, b` — a line segment.
- `P x, y, z, r, g, b, size, label` — a text label (underscores render as spaces).
- Colors are `0-255`. The paper cannot be colored — white is the base.

---

## Reading the map

### Marker colors

| Color | Meaning |
|---|---|
| Orange | Zone exits / succor & evacuate points |
| Teal | Landmarks, camps, special features (a pit, a storeroom) |
| Green | Merchants and key vendors |
| Amber / brown | Named loot NPCs (icon scaled by difficulty) · tradeskill stations |
| Dark red | Quest givers · hostile named NPCs |
| Purple | Dangerous high-level NPCs, bosses, guild halls |

Individual zones tune this to fit their content. **Dark interiors use darker variants of
the same scheme** — in Neriak the whole palette drops to near-black blues, reds and
purples, because bright labels wash out against a cavern city.

Marker **size** carries meaning too: bigger markers are more significant, and on named
NPCs the icon scales with difficulty.

### Terrain colors

| Color | Meaning |
|---|---|
| Solid blue | Water. Bridges, walkways and islands stay unshaded, so if it's blue you can't walk it. |
| Green | Grass and forest canopy. Denser green means denser forest. |
| Brown | Bare rock and stone shelf — nothing grows there. |
| Purple-green | Nektulos, shading toward Teir'Dal purple as you near Neriak. |
| Red / orange | Lava, in Lavastorm and Sol B. |

### Titles, grid and compass

Every zone carries an etched title, a coordinate grid, and a compass placed clear of the
map content. **North is up.** The margins hold sketches of real landmarks in that zone,
positioned on the side they actually stand — on Neriak Third Gate the Lodge of the Dead
sits top-left because it keeps hall in the north, and Innoruuk's temple bottom-left
because the shrine stands to the southwest.

Points of interest are sourced from **EverQuest Legends** and **Project 1999**. Where
other packs disagree, EQL and P1999 win — they're the servers these maps are for.

---

## EQOA easter-egg labels (`_3`)

EverQuest Online Adventures — the **Age of Adventure** — is set ~500 years before
EverQuest on the same continents (Antonica **and** Odus), so it names hundreds of places
EQ1 never labels. The `_3` layer sprinkles them on in muted violet. Faydwer gets nothing:
it was never in EQOA.

**25 on-map diamonds · 282 margin signposts · 32 zones · 349 labels in all.**

Every name resolves one of four ways:

| Case | Treatment |
|---|---|
| Terrain that persists (plains, valleys, hills, canyons, coasts) | on-map **diamond** |
| A real EQ1 feature sits there | on-map **diamond, snapped onto that feature** |
| Off-map, or nothing there to see | **margin signpost** `← To X`, sized by distance |
| Not in the game at all | dropped |

The hard test is simple: **if you walk to a diamond there must be something there.** An
empty field means it should have been a signpost — that test demoted 45 of the original 69.

- **Signpost sizing** — near = large (size 4), mid = 3, far = 2, so the arrows convey
  distance. Max 3 per compass direction, ≤12 per map. Broad geography never crowds out
  the characterful specific places.
- **Placement** — exact transformed `/loc` (`native = (-loc2, -loc1)`) where a real feature
  exists; otherwise matched to the terrain by eye, since EQOA's coordinate space does not
  map to EQL geometry.
- **Style** — muted violet `(150, 90, 150)`, narrow diamond markers, **appended** to any
  existing `_3` content (e.g. Lavastorm's vents) rather than overwriting it.
- **Names** verified against the canonical zone index at `wiki.eqoa.live`.
- **Modern context** — EQOA cities are ruins five centuries on: *Ruins of Klik'Anon*,
  *Ruins of Fayspire*, *Ruins of Moradhim*, *Old Arcadin*, *Old Rogue Clockworks*.
- **Lavastorm** lies inside EQOA's **NE Mountain Boundary** — never a playable EQOA zone,
  so it carries signposts and a boundary marker only.

See `EQOA_alignment_report.md` and `_age_of_adventure_alignment.png`.

> **Orientation:** these maps are north-up in game.

---

## Zone catalog

**Status — the classic atlas is complete.** All **79 zones** ship a full base, markers
and decoration set across Antonica, Odus, Faydwer and the planes.

The **Extra layer** column says what `_3` carries in that zone, if anything:

- **EQOA** — Age of Adventure place names (32 zones)
- **places** — the city's own venue names: taverns, shops, guild halls (3 zones)
- **effects** — zone-specific overflow, such as Steamfont's dragon bones (1 zone)

`File` is the map file's name, which is what the client and any bug report will use.


### Antonica — 52 zones

| Zone | File | Type | Extra layer |
|---|---|---|---|
| Befallen | `befallen` | Dungeon |  |
| Blackburrow | `blackburrow` | Dungeon | EQOA |
| Cazic-Thule | `cazicthule` | Dungeon | EQOA |
| East Commonlands | `ecommons` | Outdoor | EQOA |
| East Freeport | `freporte` | City |  |
| East Karana | `eastkarana` | Outdoor | EQOA |
| Estate of Unrest | `unrest` | Dungeon |  |
| Everfrost Peaks | `everfrost` | Outdoor | EQOA |
| Freeport Sewers | `freeportsewers` | Dungeon |  |
| Gorge of King Xorbb | `beholder` | Outdoor | EQOA |
| Grobb | `grobb` | City |  |
| Halas | `halas` | City |  |
| High Keep | `highkeep` | Dungeon |  |
| Highpass Hold | `highpass` | Outdoor | EQOA |
| Innothule Swamp | `innothule` | Outdoor | EQOA |
| Kithicor Forest | `kithicor` | Outdoor | EQOA |
| Lake Rathetear | `lakerathe` | Outdoor | EQOA |
| Lavastorm Mountains | `lavastorm` | Outdoor | EQOA |
| Lower Guk | `gukbottom` | Dungeon |  |
| Misty Thicket | `misty` | Outdoor | EQOA |
| Nagafen's Lair (Sol B) | `soldungb` | Dungeon |  |
| Najena | `najena` | Dungeon |  |
| Nektulos Forest | `nektulos` | Outdoor | EQOA |
| Neriak — Commons | `neriakb` | City | places |
| Neriak — Foreign Quarter | `neriaka` | City | places |
| Neriak — Third Gate | `neriakc` | City | places |
| North Freeport | `freportn` | City |  |
| North Karana | `northkarana` | Outdoor | EQOA |
| North Qeynos | `qeynos2` | City |  |
| Northern Desert of Ro | `nro` | Outdoor | EQOA |
| Oasis of Marr | `oasis` | Outdoor | EQOA |
| Ocean of Tears | `oot` | Outdoor |  |
| Oggok | `oggok` | City |  |
| Permafrost Keep | `permafrost` | Dungeon |  |
| Qeynos Catacombs | `qcat` | Dungeon |  |
| Qeynos Hills | `qeytoqrg` | Outdoor | EQOA |
| Rathe Mountains | `rathemtn` | Outdoor | EQOA |
| Rivervale | `rivervale` | City | EQOA |
| Runnyeye | `runnyeye` | Dungeon |  |
| Solusek's Eye (Sol A) | `soldunga` | Dungeon |  |
| Solusek's Eye (lower) | `soldungc` | Dungeon |  |
| South Karana | `southkarana` | Outdoor | EQOA |
| South Qeynos | `qeynos` | City |  |
| Southern Desert of Ro | `sro` | Outdoor | EQOA |
| Splitpaw Lair | `paw` | Dungeon |  |
| Surefall Glade | `qrg` | Outdoor | EQOA |
| Temple of Solusek Ro | `soltemple` | Dungeon |  |
| The Feerrott | `feerrott` | Outdoor | EQOA |
| Upper Guk | `guktop` | Dungeon |  |
| West Commonlands | `commons` | Outdoor | EQOA |
| West Freeport | `freportw` | City |  |
| West Karana | `qey2hh1` | Outdoor | EQOA |


### Odus — 9 zones

| Zone | File | Type | Extra layer |
|---|---|---|---|
| Erud's Crossing | `erudsxing` | Outdoor | EQOA |
| Erudin | `erudnext` | City | EQOA |
| Erudin Palace | `erudnint` | City |  |
| Kerra Isle | `kerraridge` | Outdoor | EQOA |
| Paineel | `paineel` | City | EQOA |
| Stonebrunt Mountains | `stonebrunt` | Outdoor | EQOA |
| The Hole | `hole` | Dungeon |  |
| The Warrens | `warrens` | Dungeon | EQOA |
| Toxxulia Forest | `tox` | Outdoor | EQOA |


### Faydwer — 13 zones

| Zone | File | Type | Extra layer |
|---|---|---|---|
| Ak'Anon | `akanon` | City |  |
| Butcherblock Mountains | `butcher` | Outdoor |  |
| Castle Mistmoore | `mistmoore` | Dungeon |  |
| Crushbone | `crushbone` | Dungeon |  |
| Dagnor's Cauldron | `cauldron` | Outdoor |  |
| Greater Faydark | `gfaydark` | Outdoor |  |
| Kedge Keep | `kedge` | Dungeon |  |
| Lesser Faydark | `lfaydark` | Outdoor |  |
| North Kaladim | `kaladima` | City |  |
| Northern Felwithe | `felwithea` | City |  |
| South Kaladim | `kaladimb` | City |  |
| Southern Felwithe | `felwitheb` | City |  |
| Steamfont Mountains | `steamfont` | Outdoor | effects |


### The Planes — 4 zones

| Zone | File | Type | Extra layer |
|---|---|---|---|
| Plane of Fear | `fearplane` | Dungeon |  |
| Plane of Hate | `hateplane` | Dungeon |  |
| Plane of Hate (lower) | `hateplaneb` | Dungeon |  |
| Plane of Sky | `airplane` | Dungeon |  |


### Custom — 1 zone

| Zone | File | Type | Extra layer |
|---|---|---|---|
| New Sebilis (Expedition) | `newsebexp` | Dungeon |  |

### Featured zones — detailed treatment

A few zones received special base/decoration work worth documenting:

### Toxxulia Forest — *Complete*
Stylized forest atlas. Decoration finalized: rounded and angular hills with S-curve slope
contours, scattered grass tufts around tree bases, fish placed only in the **wide** west
river (never the narrow east river, to avoid reading as shore-hugging), skunks on the
southwest hill, and a corrected serpentine **S** title glyph.

### Paineel — *Complete*
Evil Erudite city. Dark, angular decoration with a custom diagonal-stroke title font
(sharp spines, jagged N, peaked A), a compass shrunk and repositioned to sit fully inside
the border, and a parchment-white background. Marker file expanded from 10 portal-only
entries to full POI coverage (guild halls, vendors, quest givers, high-level danger).

### The Warrens — *Complete*
Kobold underground cavern (Befallen used as the styling reference). Full two-file
treatment: kobold-face compass, jagged stone border, etched title, and 22 markers
validated against the geometry.

### New Sebilis (Expedition) — *Complete*
Iksar underground ancient civilization temple repurposed. **Base recolored by area** into six tinted regions (guild halls,
bazaar, west grotto, central passages, temple vaults, sunken caverns) with water kept
blue. Iksar-themed decoration (root-and-iron frame, hanging chains, bookcases, war
standards, emblems) and a full POI marker layer.

### Lavastorm — *Complete*
Volcanic zone. The base's red lava-pool outlines were clustered and **filled molten-red
with rising steam wisps**. Fire-themed doodle set: fire drakes, fire elementals, spotted
goblin huts, the Eye of Ro caldera, and the Temple of Solusek Ro, plus a flame-center
compass. 20 POI on the validated transform.

### Blackburrow — *Complete*
Three-floor gnoll warren (ravine on top, cave systems below, a deep underground lake).
- **Base recolored by floor** — three stacked Z-levels tinted sunlit ochre (top ravine),
  torchlit rust (mid dens), and cold slate-blue (deep lake level).
- **Water shaded** — extracted from the wiki floor maps, transformed to native, clipped to
  each floor's footprint, and hatch-filled blue with ripples (the water version of the
  Lavastorm lava fill). Covers the main lake, the Pit column, and upper pools.
- **Gnoll decoration** — rocky border with a stalactite ceiling, etched **BLACKBURROW**
  title, gnoll-head compass, and margin sketches: Blackburrow Stout brewery casks, a clan
  totem with hide banner, a snarling gnoll face, giant snakes (double-line bodies),
  paw-print trails, bones, and a cutaway **hollow tree with a false floor** dropping to the
  level below.
- **23 POI**, each floor-tagged (e.g. `[F3-9]`) with Z sampled within its own floor band;
  bosses (Lord Elgnub, Sabertooth Overseer, Sharpshooter) as purple stars, the Everfrost
  zone-in placed from the in-game `/loc`.

---

---

## Troubleshooting

**`Emoda Legends Maps` isn't in the dropdown.**
The folder is in the wrong place. You should end up with:

```
EverQuest Legends\maps\Emoda Legends Maps\befallen.txt
```

The usual mistake is extracting into a folder you made yourself, which gives you
`maps\Emoda Legends Maps\Emoda Legends Maps\...` — one level too deep. Move the inner
folder up.

**The folder is listed but the map is blank.**
The `.txt` files have to sit directly inside the folder you select, not in a subfolder
of it.

**Every wall is drawn twice, or the map looks smeared.**
A recolored base is loaded alongside the original. Only one `zonename.txt` should exist
in the folder.

**Labels overlap and I can't read anything.**
Turn off layer **3** first — that's places and EQOA. If it's still busy, turn off **1**
and keep the drawn map.

**The map is too dark / too busy in a city.**
Cities are dense by nature — Neriak's geometry alone is tens of thousands of segments.
Turning off **2** drops the decoration and leaves the streets bare.

**A marker is in the wrong place.**
Please report it with a `/loc` — see below. That's the single most useful thing you can
send.

---

## Contributing

**The most useful contribution is a screenshot with notes drawn on it.** A good share of
the corrections in this atlas came from someone standing in the zone saying *the water is
on the bridge*, or circling four spots in red — which no render will ever tell you.

Useful to include:

- **A `/loc`** for anything positional. One `/loc` is worth a paragraph of description.
  Several around a shape are even better — that's how the fallen logs got their outline.
- **The zone name** as the map window reports it, since city quarters are easy to mix up.
- **Which layers were on**, if something looked wrong.

Marked-up screenshots beat descriptions. Color-coding them helps: one convention that
has worked well is red for *remove*, green for *add or move here*, orange for *already
handled*.

---

## For developers

Everything here is generated from Python — no map file is edited by hand. The build
sources live in the developer folder, which has its own README. In brief:

| | |
|---|---|
| `kit/` | reusable art: `terrain` (peaks, rock, grass, canopy), `flora` (trees and undergrowth), `fauna` (every playable race plus creatures), the Teir'Dal set, and fallen logs |
| `toolkit/` | map primitives: canvas, frame, grid, title, compass, doodles |
| `zones/` | per-zone build scripts |
| `tools/` | cross-atlas utilities: validation, compass placement, alignment |
| `design/` | catalogue sheets, a render of all 79 zones, the EQOA report, source archive |

Zones are **composed from kits** rather than drawn one-off, so a fix to a tree or a race
silhouette propagates everywhere it appears.

Things worth knowing before touching anything:

- **The coordinate transform** is `native = (-loc2, -loc1)`. Never use a raw `/loc`.
- **Layers are never flattened together.** Base, markers, decoration and places stay in
  separate files, always.
- **CRLF line endings are mandatory.** A lone `\n` will break the file in the client.
  `tools/validate_all.py` checks this across the pack.
- **Don't thin a dense city.** Those thousands of tiny segments are buildings, not
  texture. Readability comes from a color hierarchy, not from deleting geometry.
- **The water system** has several ways to go wrong, all documented — coincident
  shorelines that cancel out parity, bridges reading as water, islands filling in.

---

## Reference sources

Other people's work that informed this pack, and deserves the credit.

- **Norrath Cartographers** — the original community traces the base geometry comes from.
- **Brewall's EverQuest Maps** — <https://www.eqmaps.info/eq-map-files/>
- **Good's EverQuest Map Pack (Goodurden)** —
  <https://www.redguides.com/community/resources/goods-everquest-map-pack.303/>

  Both consulted for base geometry and feature color-coding only. **No points of
  interest are taken from them** — those packs target *EverQuest Live*, which carries
  NPCs and content that don't exist on EQL or P1999.

**EQOA / Age of Adventure**

- **EQOA / Tunaria & Odus world maps** — geography and place names for the `_3` layer.
- **`wiki.eqoa.live`** (EQOA: Sandstorm wiki) — canonical EQOA zone and POI index, used
  to verify every label spelling (caught *Box Canyons*, *Bobble-by-Water*, *Muniel's Tea
  Garden*, *Mount Hatespike*).
- **EQL wiki / Project 1999 / the EverQuest Locations Key** — EQ1 zone connections, named
  NPCs with levels, and landmark `/loc`s for the `_1` marker layer.
