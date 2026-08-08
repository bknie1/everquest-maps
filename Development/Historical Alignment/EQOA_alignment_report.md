# EQOA → EQ1 Alignment Report
### Proposed `_3` easter-egg layer — for review before build

**Totals:** 74 on-map diamonds · 48 margin signposts · across 25 Antonica + 7 Odus zones.

Companion images:
- `_alignment_antonica_eq1.png` — labels keyed onto the EQ1 Antonica zone map
- `_alignment_odus_eq1.png` — same for Odus
- `_tunaria_hypothetical_zone_map.png` — EQOA-only areas drawn as *proposed future zones* on the classic connection graph

---

## 1. Method — the three fates

Every EQOA place resolves to exactly one treatment, decided by where it sits relative to the EQ1 zone being drawn:

| Case | Representation |
|---|---|
| Inside the matching EQ1 zone | on-map **narrow diamond** + label |
| In an adjacent area with **no EQ1 zone** | **margin signpost** — `← To X` arrow pointing its way |
| Not in the game at all | dropped |

Workflow: overlay the EQ1 zone footprints on the EQOA world map, key every place as diamond or arrow, **rule the arrows out first** — what remains are the on-map candidates.

**Placement.** Where an EQOA name matches a real EQ1 feature with a known `/loc`, the diamond goes on the **exact transformed loc** (`native = (-loc2, -loc1)`). Otherwise it's placed by **matching the terrain by eye** — EQOA's coordinate space doesn't map to EQL geometry, so a guesstimate on the right ground is the correct method, not a shortcut.

## 2. Rendering changes in this pass

- **Diamonds are 25% smaller** than the previous pass, so the layer can stay toggled **on full-time** rather than flipped on when needed.
- **Size tiers** carry hierarchy — Large (4) cities/forts/iconic, Medium (3) villages/named landmarks, Small (2) ruins/remnants/camps. The diamond scales with the tier too.
- **Density raised** to roughly one label per cardinal direction (6–9 on big outdoor zones) instead of the earlier cap of 3. Memorable ruins and remnants are explicitly included.

## 3. Key findings

1. **Lavastorm was never an EQOA zone.** On the EQOA world map "Lavastorm" is printed inside the grey **NE Mountain Boundary** band, not in a playable colored region. It gets a **boundary marker + signposts only — no on-map diamonds.** This validates the "Age of Adventure boundary" framing.
2. **Klik'Anon ≠ Ak'Anon.** Klik'Anon is the EQOA gnome city in the northeast; EQ1's Ak'Anon is its Faydwer cousin. Signposts read **"To Klik'Anon."** (Nothing was ever written to a map file under the wrong name.)
3. **Arcadin is pre-rebuild Erudin**, so it appears as a lore signpost `← To Old Arcadin`, never as a current place. **East Plateau** is dropped entirely (not in the game).
4. **West Toxxulia is not in EQ1.** The EQ1 zone covers **South Toxxulia** plus a strip of **North Toxxulia**; West/East Toxxulia become signposts.
5. **Name corrections** verified against `wiki.eqoa.live`: Box Canyons (not Fox), Bobble-by-Water, Muniel's Tea Garden, Mount Hatespike, Al Farak Ruins, South Crossroads (the EQOA name; "Fort Solitude" is the EQ1 label).
6. **Orientation:** these maps are **north-up in game.** Earlier previews rendered vertically flipped, which is why titles looked upside-down — a render artifact, now fixed.

## 4. Revisions from your review notes

**a. "On the way" signposts — the density mismatch.** EQ1 zones are *slices* of the EQOA world; EQOA is far denser. So a place can be genuinely absent from every EQ1 zone yet still sit meaningfully between two of them. Those become **paired signposts** pointing opposite directions from each neighbour, which conveys the distance:

| Place | From | Direction |
|---|---|---|
| Kerplunk Outpost | Innothule Swamp | ← W |
| Kerplunk Outpost | The Feerrott | → E |

The pair brackets it, so a player reading either map understands something lies between. Same principle drives the new Odus sea signposts.

**b. Odus rebuilt.** Stonebrunt runs down the **middle** of Odus, which means the Barren Coast, Cape Dreg and the Vasty Deep all lie **east of its in-game footprint** — every one becomes a signpost, not an on-map label. Added:

| Zone | Signposts |
|---|---|
| Erudin | ← Old Arcadin (SE), ← Grand Plateau (NW) |
| Toxxulia Forest | ← Old Arcadin (NE), ← West Toxxulia (NW), ← Grand Plateau (N) |
| Kerra Isle | ← The Abysmal Sea (W) |
| Paineel | ← The Abysmal Sea (W) |
| The Warrens | ← Gulf of Uzun (S) |
| Erud's Crossing | ← The Vasty Deep (SE) |

The Erudin SE arrow deliberately mirrors Toxxulia's NE arrow — the two point at the same place from opposite sides. **The Hole is dropped**: it didn't exist in the EQOA era.

**c. Curving paths.** The connection graph and the physical map genuinely disagree in places — Feerrott connects to Oggok on its *north* side even though Oggok sits east, almost back the way you came from Innothule. The compass is never contradicted: if the game says north, the signpost says north. Where the route bends, the direction gets a parenthetical, e.g. **`To Oggok (NE — path curves back W)`**, so the map admits the invisible path rather than looking wrong.

**d. Nektulos — Leatherfoot Camp `/loc` bug found.** Your reading (`106.22, 560.77`) transforms to native **(-560.77, -106.22)**. The stored Captain marker was at **(-560, -1016)** — X matched to within a unit, Y was off by ~910, a digit-transcription error. Corrected the Captain to your exact loc and shifted the Deputy and Sergeant by the same delta to preserve the camp's shape. They now sit beside the Leatherfoot Medic (y ≈ -58), which corroborates the fix. **This is an EQ1 POI (`_1` layer), not an EQOA label.**

---

## 5. The EQOA-style grid  (`_norrath_eqoa_grid.png`)

Your cell approach translated to a full canvas: every EQ1 zone as a cell, gaps filled with EQOA names and your suggested names, so the naming space for future zones is visible at a glance.

- **147 cells** — 35 EQ1 zones · 10 dungeons · 20 suggested gap names · 77 EQOA names · 3 water · Lavastorm (boundary) · The Hole (didn't exist yet).
- **Dungeons are drawn as short cells.** They sit under or beside a zone, so they shouldn't consume surface real estate — Permafrost, Blackburrow, Runnyeye, Splitpaw, Befallen, Arena, Guk, Cazic Thule, Najena, the Warrens.
- **Cell adjacency is geographic, not connective.** Two touching cells are neighbours in space; the EQ1 zone links laid over that can curve (see 4c).

---

## 6. Antonica — per zone

#### Everfrost Peaks
> Huge zone; EQOA names the whole northern icefield.

| On-map label | Tier |
|---|---|
| ◆ Snowblind Plains | Medium (size 3) |
| ◆ Anu Village | Medium (size 3) |
| ◆ Frosteye Valley | Medium (size 3) |
| ◆ Snowfist | Small (size 2) |
| ◆ Greyvax's Caves | Small (size 2) |
| ◆ Freezeblood Village | Small (size 2) |
| ◆ Diren Hold | Small (size 2) |
| ◆ Goldfeather Eyrie | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Unkempt North | W |
| ← To Zantar's Keep | W |
| ← To Fayspire Gate | NE |


#### Blackburrow
> EQOA name = the EQ1 zone name. Nothing to add.

_No labels — nothing to add._


#### Surefall Glade
> EQOA "Surefall Glade" = same place. Tiny zone -> signposts only.

| Margin signpost | Direction |
|---|---|
| ← To Jethro's Cast | W |
| ← To Wymondham | E |


#### Qeynos Hills
> Dense EQOA cluster NE of Qeynos maps almost 1:1 onto this zone.

| On-map label | Tier |
|---|---|
| ◆ Bear Cave | Medium (size 3) |
| ◆ Mayfly Glade | Medium (size 3) |
| ◆ Forkwatch | Medium (size 3) |
| ◆ Druid's Watch | Small (size 2) |
| ◆ Spider Mine | Small (size 2) |
| ◆ Blakedown | Small (size 2) |
| ◆ Hagley | Small (size 2) |
| ◆ Qeynos Prison | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Wyndhaven | W |
| ← To Crethley Manor | NW |


#### West Karana
> Jared's Blight = Dorvar Manor on the EQOA map.

| On-map label | Tier |
|---|---|
| ◆ Jared's Blight | Medium (size 3) |
| ◆ Alseop's Wall | Medium (size 3) |
| ◆ Strag's Rest | Medium (size 3) |
| ◆ Al-Karad Ruins | Small (size 2) |
| ◆ Salt Mine | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Fog Marsh | W |
| ← To Wymondham | NW |


#### North Karana
> Merry-by-Water is the halfling town feuding with Bobble-by-Water (Great Pie Crisis).

| On-map label | Tier |
|---|---|
| ◆ Merry-by-Water | Medium (size 3) |
| ◆ Blakedown | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Spirit Talker's Wood | NW |


#### East Karana
| On-map label | Tier |
|---|---|
| ◆ Saerk Towers | Medium (size 3) |
| ◆ Mu Lin's Reach | Medium (size 3) |
| ◆ Moss Mouth Cavern | Small (size 2) |
| ◆ The Green Rift | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Hodstock and Temby | E |
| ← To Bobble-by-Water | E |


#### Beholders Maze
> Gorge of King Xorbb. EQOA has no beholder analog; Bandit Hills is the nearest fit.

| On-map label | Tier |
|---|---|
| ◆ Bandit Hills | Small (size 2) |


#### South Karana
> South Crossroads = "Fort Solitude" on some maps; EQOA name preferred. Aviak Village + Centaur Valley have real EQ1 locs.

| On-map label | Tier |
|---|---|
| ◆ Aviak Village | Large (size 4) |
| ◆ South Crossroads | Large (size 4) |
| ◆ Centaur Valley | Medium (size 3) |
| ◆ Urglunt's Wall | Medium (size 3) |
| ◆ Urglunt's Gate | Medium (size 3) |
| ◆ Widow's Peak | Medium (size 3) |
| ◆ Wktaan's 4th Talon | Small (size 2) |
| ◆ Serpent Hills | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Highbourne | W |
| ← To Stoneclaw | NW |


#### Misty Thicket
> Mount Hatespike (The Lost Isle) sits NW, outside the zone.

| On-map label | Tier |
|---|---|
| ◆ Baga Village | Medium (size 3) |

| Margin signpost | Direction |
|---|---|
| ← To Mount Hatespike | NW |
| ← To Moradhin | N |


#### Rivervale
> EQOA "Rivervale" = same. The two -by-Water halfling towns are a lore pair.

| Margin signpost | Direction |
|---|---|
| ← To Merry-by-Water | NW |
| ← To Bobble-by-Water | E |


#### Highpass Hold
> EQOA labels "Highpass Hold" in the same spot - strongest 1:1 anchor on the continent.

| On-map label | Tier |
|---|---|
| ◆ Ferran's Hope | Medium (size 3) |
| ◆ Trail's End | Medium (size 3) |
| ◆ Bastable Village | Medium (size 3) |
| ◆ Dshinn's Redoubt | Small (size 2) |


#### Kithicor Wood
| On-map label | Tier |
|---|---|
| ◆ North Kithicor | Medium (size 3) |
| ◆ The Green Rift | Small (size 2) |


#### West Commonlands
| On-map label | Tier |
|---|---|
| ◆ Tomb of Kings | Medium (size 3) |
| ◆ Desert Hate | Small (size 2) |


#### East Commonlands
| On-map label | Tier |
|---|---|
| ◆ Temple of Light | Medium (size 3) |
| ◆ Deathfist Forge | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Bobble-by-Water | NE |


#### Nektulos Forest
> Castle Feister = Fort Barick. Foggy witch-woods styling (see tree study).

| On-map label | Tier |
|---|---|
| ◆ Collinridge Cemetery | Medium (size 3) |
| ◆ Thedruk | Medium (size 3) |
| ◆ Castle Feister | Medium (size 3) |

| Margin signpost | Direction |
|---|---|
| ← To Klik'Anon | NE |


#### Lavastorm Mountains
> ⚠️ **NOT an EQOA zone -- sits in the grey "NE Mountain Boundary" band. Boundary marker + signposts only, no on-map diamonds.

| Margin signpost | Direction |
|---|---|
| ← To Kara Village | SW |
| ← To Klik'Anon | S |
| ← To Fayspire | SW |
| ← To Rogue Clockworks | NE |


#### Northern Desert of Ro
| On-map label | Tier |
|---|---|
| ◆ Deathfist Citadel | Medium (size 3) |
| ◆ Muniel's Tea Garden | Medium (size 3) |
| ◆ Northwestern Ro | Small (size 2) |


#### Southern Desert of Ro
> Box Canyons (not "Fox") per wiki.eqoa.live.

| On-map label | Tier |
|---|---|
| ◆ Box Canyons | Medium (size 3) |
| ◆ Al Farak Ruins | Medium (size 3) |
| ◆ Sycamore Joy's Rest | Small (size 2) |
| ◆ Eternal Desert | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Great Waste | E |
| ← To Takish-Hiz | SE |


#### Oasis of Marr
> EQOA "Oasis" sits in the same spot.

| On-map label | Tier |
|---|---|
| ◆ Oasis | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Sea of Lions | E |
| ← To Great Waste | NE |


#### Innothule Swamp
> EQ1 shows only ONE SLICE of the EQOA swamp - Kerplunk Outpost sits outside it, so it becomes a signpost (W from here, E from Feerrott).

| On-map label | Tier |
|---|---|
| ◆ Lake Noregard | Small (size 2) |
| ◆ Burial Mounds | Small (size 2) |
| ◆ Ant Colonies | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Kerplunk Outpost | W |
| ← To Broken Skull Rock | S |


#### Feerrott
> Paired signpost: Kerplunk lies E of Feerrott and W of Innothule - the two arrows bracket it.

| On-map label | Tier |
|---|---|
| ◆ West Feerrott | Medium (size 3) |
| ◆ Envar | Small (size 2) |
| ◆ Ogre Ruins | Small (size 2) |
| ◆ Dead Hills | Small (size 2) |
| ◆ Moggok's Gate | Small (size 2) |

| Margin signpost | Direction |
|---|---|
| ← To Kerplunk Outpost | E |
| ← To Gerotar's Mines | E |
| ← To Oggok | NE (path curves back W) |


#### Rathe Mountains
| On-map label | Tier |
|---|---|
| ◆ Cyclops' Fortress | Medium (size 3) |
| ◆ Sphinx Pyramid | Medium (size 3) |
| ◆ Geomancer's Citadel | Medium (size 3) |
| ◆ Geomancer's Pass | Small (size 2) |


#### Lake Rathetear
> EQOA "Lake Rathe" = same lake.

| On-map label | Tier |
|---|---|
| ◆ Kelinar | Small (size 2) |
| ◆ Fort Alliance | Small (size 2) |


#### Cazic Thule
> EQOA "Cazic Thule" = same name.

| Margin signpost | Direction |
|---|---|
| ← To Stone Watchers | S |
| ← To Dinbak | SE |


---

## 7. Odus — per zone

#### Toxxulia Forest
> EQ1 covers South Toxxulia + a strip of North. Arcadin = pre-rebuild Erudin -> lore signpost. East Plateau dropped (not in game).

| On-map label | Tier |
|---|---|
| ◆ South Toxxulia | Medium (size 3) |
| ◆ North Toxxulia | Medium (size 3) |

| Margin signpost | Direction |
|---|---|
| ← To West Toxxulia | NW |
| ← To Old Arcadin | NE |
| ← To Grand Plateau | N |


#### Stonebrunt Mtns
> ⚠️ **Stonebrunt runs down the MIDDLE of Odus - the Barren Coast and Vasty Deep all lie EAST of its in-game footprint, so they are all signposts, not on-map labels.

| Margin signpost | Direction |
|---|---|
| ← To North Barren Coast | NE |
| ← To South Barren Coast | SE |
| ← To Cape Dreg | SE |
| ← To The Vasty Deep | E |


#### Erudin
> Erudin IS Arcadin rebuilt - the SE signpost mirrors the NE one on Toxxulia.

| Margin signpost | Direction |
|---|---|
| ← To Old Arcadin | SE |
| ← To Grand Plateau | NW |


#### Kerra Isle
> Your own POI layer kept untouched; only an "on the way" sea signpost added.

| Margin signpost | Direction |
|---|---|
| ← To The Abysmal Sea | W |


#### Paineel
> Sea signpost gives a sense of what lies beyond the western cliffs.

| Margin signpost | Direction |
|---|---|
| ← To The Abysmal Sea | W |


#### The Warrens
> Southward signpost toward the gulf.

| Margin signpost | Direction |
|---|---|
| ← To Gulf of Uzun | S |


#### Erud's Crossing
> EQOA name matches; one open-water signpost.

| Margin signpost | Direction |
|---|---|
| ← To The Vasty Deep | SE |


---

## 8. Appendix — hypothetical Tunaria zones

The EQOA-only areas (the ones becoming signposts) are drawn on `_tunaria_hypothetical_zone_map.png` as **proposed zones** wired into the classic connection graph — a planning sketch for carving out space for future development. Proposed links are geographic reads off the EQOA world map, **not canon adjacency**.

39 proposed zones:


- Zantar's Keep · Unkempt North · Snowfist
- Fayspire Gate · Mariel Village · Twisted Tower
- Freezeblood Village · Fayspire · Tethelin
- Klik'Anon · Rogue Clockworks · Unkempt Glade
- Guardian Forest · Moradhin · Kara Village
- Wyndhaven · Jethro's Cast · Wymondham
- Merry-by-Water · Castle Feister · Whale Hill
- Crethley Manor · Fog Marsh · Collinridge Cemetery
- Hodstock and Temby · Highbourne · Stoneclaw
- Bobble-by-Water · Geomancer's Citadel · Urglunt's Gate
- Muniel's Tea Garden · Takish'Hiz · Brog Fens
- Great Waste · Stone Watchers · Karplunk Outpost
- Sslathis · Hazinak · Basher's Enclave


---

## 9. Open questions for review

1. **Grid cell names** — the 20 suggested gap names are yours; the 77 EQOA names are mine. Any cell you'd rename, move, merge, or split?
2. **More paired signposts** — Kerplunk is the clear case. Others that may deserve the same treatment: Bandit Hills (between Gorge and North Karana), Bastable Village (between Highpass and West Commonlands), Merry-by-Water (between North Karana and Rivervale).
3. **Curving-path notation** — is `To Oggok (NE — path curves back W)` the right phrasing, or too wordy for a map label? Shorter option: `To Oggok (NE ↻W)`.
4. **Tiers** — anything mis-weighted?
5. **Lavastorm boundary wording** — "Age of Adventure NW Boundary" (yours) vs the EQOA original "NE Mountain Boundary."
6. **Density** — 6–9 per big zone, or push further on the largest (Everfrost, South Karana)?

_On your OK (with notes), the `_3` layers get regenerated across all listed zones._
