# Custom EQ Atlas Maps by Emoda

Atlas-style in-game map files for **EverQuest Legends**, built zone by zone.
The look is a 2D contour map with 3D-effect features: parchment-white background,
color-coded points of interest, themed hand-crafted borders, etched titles, compasses,
and zone-appropriate decorative sketches.

It's just vector math. You can do cool vector art.

---

External demo renders (pardon any visual issues; labels render differently in-game)

<img width="300" height="356" alt="image" src="https://github.com/user-attachments/assets/58a39931-9d00-4f38-b057-95386dc934da" />

<img width="700" height="1074" alt="ak_full" src="https://github.com/user-attachments/assets/b6a0f60b-3fbb-4b8a-bd2d-ec686c11b75d" />

---

## How the files work

Each zone is drawn as up to three stacked layers that the client overlays:

| File | Layer | Contents |
|------|-------|----------|
| `zonename.txt`   | **base**       | The zone wall geometry. Some zones ship a **recolored** base (tinted by area or by floor, water shaded). |
| `zonename_1.txt` | **markers**    | Color-coded POI: NPCs, vendors, quest givers, exits, danger flags. |
| `zonename_2.txt` | **decoration** | Border, grid, title, compass, and themed margin sketches. |
| `zonename_3.txt` | **extra**      | Optional overflow/effect layer (e.g. Lavastorm vents) **and EQOA easter-egg labels** — see below. |

**Format:** EQ native L/P line format with **mandatory CRLF (`\r\n`) line endings**.

- `L x1, y1, z1, x2, y2, z2, r, g, b` — a line segment.
- `P x, y, z, r, g, b, size, label` — a text label (underscores render as spaces).
- Colors are `0–255`. The paper/background cannot be colored — white is the base.

**Install:** drop the files into your maps folder (e.g. `…\EverQuest Legends\maps\Emoda Maps`).
A **recolored base replaces** the original `zonename.txt` — don't load both, or every wall
draws twice. Always keep a backup of the original base.

---

## Marker color conventions

| Color | Meaning |
|-------|---------|
| Orange | Zone exits / succor & evacuate points |
| Teal | Landmarks, camps, special features (e.g. a pit, a storeroom) |
| Green | Merchants and key vendors |
| Amber / brown | Named loot NPCs (icon scaled by difficulty) |
| Dark red | Quest givers |
| Purple | Dangerous high-level NPCs / bosses |

(Individual zones tune this slightly to fit their content.)

---

## EQOA easter-egg labels (`_3`)

EverQuest Online Adventures — the **Age of Adventure** — is set ~500 years before
EverQuest on the same continents (Antonica **and** Odus), so it names hundreds of places
EQ1 never labels. The `_3` layer sprinkles them on in muted violet. Faydwer gets nothing:
it was never in EQOA.

**25 on-map diamonds · 283 margin signposts · 32 zones.**

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

## Coordinate & build methodology

- **Transform:** wiki coordinates `(a, b)` → native `(-b, -a)`, validated per zone against
  real wall geometry before any markers are placed. Holds across every Odus and
  Antonica zone tested so far.
- **`/loc` readings** give **size/extent**, not relocation targets — they are not used to
  reposition decoration. A zone-in `/loc` is only used as a landmark anchor once
  cross-checked against geometry.
- **SVG previews render Y-down** to match in-game display; stick-letter titles are
  vertically flipped before writing so they read right-side-up in game.
- Decoration order: **border → grid → title → compass → themed fill**, with a widened
  margin lane so sketches never straddle the frame or bleed into the map.

---

## Toolkit

- **`eqmap_toolkit.py`** — reusable core: `Canvas`, `frame`, `grid`, `title`, `compass`,
  the `LETTERS` glyph set, and a shared doodle library (paw prints, skulls, bones, lava
  pools, trees, tents, and more). Carries across all zones.
- **Per-zone decoration modules** — e.g. `nse_decor.py` (Iksar), `bb_decor.py` (gnoll):
  zone-specific sketches built on the toolkit.
- **`water.py`** — water-shading helper: calibrates wiki floor-map images and returns
  native-space water points for hatched fills.
- **Build scripts** (`build_base_colored.py`, `build_1.py`, `build_2.py`) — the
  end-to-end pipeline per zone, reusable as templates.

---

## Zone catalog

**Status — the classic atlas is complete.** All **79 zones** ship a full base + markers +
decoration set across Antonica, Odus, Faydwer, and the planes, plus EQOA easter-egg `_3`
layers on the 22+ outdoor zones. The featured write-ups below cover a few zones in depth;
the rest follow the same conventions.

✳ = carries an EQOA easter-egg `_3` layer.

**Antonica** — 52 zones

Befallen · Blackburrow · Cazic-Thule · East Commonlands ✳ · East Freeport · East Karana ✳ · Estate of Unrest · Everfrost Peaks ✳ · Freeport Sewers · Gorge of King Xorbb · Grobb · Halas · High Keep · Highpass Hold ✳ · Innothule Swamp ✳ · Kithicor Forest ✳ · Lake Rathetear ✳ · Lavastorm Mountains ✳ · Lower Guk · Misty Thicket ✳ · Nagafen's Lair (Sol B) · Najena · Nektulos Forest ✳ · Neriak — Commons · Neriak — Foreign Quarter · Neriak — Third Gate · North Freeport · North Karana ✳ · North Qeynos · Northern Desert of Ro ✳ · Oasis of Marr ✳ · Ocean of Tears · Oggok · Permafrost Keep · Qeynos Catacombs · Qeynos Hills ✳ · Rathe Mountains ✳ · Rivervale ✳ · Runnyeye · Solusek's Eye (Sol A) · Solusek's Eye (lower) · South Karana ✳ · South Qeynos · Southern Desert of Ro ✳ · Splitpaw Lair · Surefall Glade ✳ · Temple of Solusek Ro · The Feerrott ✳ · Upper Guk · West Commonlands ✳ · West Freeport · West Karana ✳

**Odus** — 9 zones

Erud's Crossing · Erudin · Erudin Palace · Kerra Isle · Paineel · Stonebrunt Mountains ✳ · The Hole · The Warrens · Toxxulia Forest ✳

**Faydwer** — 13 zones

Ak'Anon · Butcherblock Mountains · Castle Mistmoore · Crushbone · Dagnor's Cauldron · Greater Faydark · Kedge Keep · Lesser Faydark · North Kaladim · Northern Felwithe · South Kaladim · Southern Felwithe · Steamfont Mountains

**Planes** — 4 zones

Plane of Fear · Plane of Hate · Plane of Hate (lower) · Plane of Sky

**Custom** — 1 zone

New Sebilis (Expedition)

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

## Reference sources

- **EQOA / Tunaria & Odus world maps** — geography and place names for the `_3` layer.
- **`wiki.eqoa.live`** (EQOA: Sandstorm wiki) — canonical EQOA zone/POI name list, used to
  verify label spellings (caught e.g. *Box Canyons*, *Bobble-by-Water*, *Muniel’s Tea
  Garden*, *Mount Hatespike*).
- **EQL wiki / Project 1999 / the EverQuest Locations Key** — EQ1 zone connections, named
  NPCs (with levels), and landmark `/loc`s for the `_1` marker layer.
