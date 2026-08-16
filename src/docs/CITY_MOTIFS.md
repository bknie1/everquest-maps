# City motifs — source material for the city pass

Sourced from the EQL wiki (fallback: P1999 wiki) plus Brandon's direction. Each city
rebuild should draw its margin art, title styling, and shading from THIS list, not
from generic fantasy. Race packs of motif items go in `src/kit/` per race.

## Brandon's framing

- Cities are the weak third of the pack; non-city zones are ~99% there.
- Every city gets: clean title (title/subtitle where natural), building/walkway
  shading pulled from Norrath Cartographers-style bases, race-specific motif items,
  compass with breathing room, even border sizes.
- "City" includes: qeynos, qeynos2, qcat, freeport trio, paineel, gfaydark
  (Kelethin — wood elf city), rathemtn (froglok city), kerraridge (kerra city),
  oggok, grobb, halas, akanon, neriak trio, rivervale, felwithe, kaladim, erudin.

## Per-city notes

### Oggok (ogre)
- Rainforest jungle surroundings; ancient RUINED architecture — Greek/Roman
  inspired, from before the curse (Klingon-esque war-academic culture).
- Mostly underground/carved; degraded tribal carvings of heroic conquest.
- Structures: Fortress Craknek (warriors), Greenblood Rock (SK), shaman temple,
  Bouncer Keep at the Feerrott entrance, guard tower.
- WATER: the circular area with spokes + docks is DARK GREEN water.
- Mood: grimy, declining, controlled chaos.

### Grobb (troll)
- "Mud flows freely through their town" — mud pit more than a map (BRAIN).
- Underground cavern city; dark mines house SK + shaman guilds; warrior guild at
  entrance. Gunthak's Belch bar; TWO torture chambers (one hidden); prisons.
- Gruesome decor: scattered remains. Factions: Da Bashers, Dark Ones, Night Keep.
- Innothule swamp all around: islands, dark water.

### Halas (barbarian)
- Frosty Scottish warriors. Simple, blunt architecture; white rooftops, constant
  snow. Protective frigid lake with the raft ferry "The Gwenavyne" (draw the raft!).
- Pit of Doom (warriors), Temple of the Tribunal, Kennels with SLED DOGS,
  McQuaid's/McDonald's/Bonny Mermaid taverns, Mac's Kilts.
- Street brawls, drinking festivals. A "diversion" city built to look like a capital.

### Ak'Anon (gnome)
- Mountainside cavern: half fortress, half laboratory. NO TREES (BRAIN).
- Clockwork everything: mechanical guards/animals/cleaners, clockwork spiders,
  ticking and whirring. Massive pumps move a lake/river that dominates every area.
- Ak'Anon Palace, Abbey of Deep Musing, Library Mechanamagica, the ZOO, windmills,
  Mines of Malfunction (evil gnomes, polluted water in the north).
- Rebuild plan: central grid content is fine; borders/margins/title are a mash of
  two maps and need a full rebuild with gnome_decor (gears, pumps, cog towers;
  gear as the O in the title per BRAIN).

### Rivervale (halfling — Tolkien)
- Hidden valley around a small lake; river through an impassable gorge; waterfall
  in the north; tunnel entrances through rock; farms on one side.
- Halflings live in HOLES — burrow doors, round; hobbit hills all around the
  margins. Leatherfoot Hall, Fool's Gold pub, Weary Foot Rest inn, Vale Forge.
- Mood: quaint, warm hearth, ale.

### Qeynos / North Qeynos / Qeynos Catacombs (human — Camelot)
- Medieval port city, high walls, gnoll-besieged gates; paladins + Temple of Life
  vs a seamy underbelly (corrupt guards, smuggling, catacombs below).
- South: docks/harbor, Qeynos Hold, arena ("Grounds of Fate"), three taverns.
- North: Temple of Life, monk guild, Crow's Pub with secret tunnels, Reflecting
  Pond. Underground aqueducts connect everything.
- qcat title style: QEYNOS big, CATACOMBS subtitle beneath (unequal emphasis).

### Kelethin / Greater Faydark (wood elf)
- Platform city in the canopy: rope bridge networks, three lift towers (Newbie,
  PoD, Orc), guild/merchant/bank/tavern platforms at multiple levels.
- Perpetual twilight under the canopy; wooden tree-integrated structures.
- Kit: treehouse exists; NEED platform + rope bridge + lift shapes.

### Paineel (heretic erudite)
- Skeletal guards, portal network (teleporter hubs A/B/C), Darkglow Palace,
  Tabernacle of Terror / The Abbatoir / The Fell Blade, graveyard courtyard with
  dancing skeletons, Observatory above; built over Old Paineel in the chasm by
  The Hole; elemental-scarred terrain.
- Kit: skeleton, obelisk, tome exist; NEED portal ring + observatory dome.

### Neriak trio (dark elf)
- Carved from the mountain, no natural light, NEON magical glow accents.
- Foreign Quarter: trolls/ogres tolerated, specialty vendor clusters.
- Commons: bank "Neriak Down Under", caster + warrior guilds.
- Third Gate: deepest — Temple of Innoruuk dominates, white marble cleric
  temple ringed by water, red-skulled necromancer hall, library.
- Kit: darkelf.py is COMPLETE (gates, temple, library, lodge, webs, monoliths).

### Erudin (erudite)
- Practical pale architecture, Prexus/ocean theming, docks with ships, grand
  Library focal point, three guild towers, fountains, Toxxulia dark at its back.
- Kit: tome/orrery/obelisk/caravel exist; NEED lighthouse + fountain.

### Kaladim (dwarf)
- Carved into the mountain, winding deeper; Everhot Forge, kilns; guard posts,
  fortified feel; rough rock frames everything; function over ornament.
- Kit: anvil/forge/ore_cart exist. Legitimately has greenery (BRAIN) — keep.

### Felwithe (high elf)
- GOLDEN walls with a faint glow, rising out of the Faydark fog; mage tower
  suspended over a pool; a river runs through it; serene, grand, marble+gold.
- Kit: elf_spire exists; NEED golden arch/gate + suspended tower.

## Color + shading directive (Brandon, 2026-08-15)

A LOT of color. Hand-made cartographical maps with shading. Buildings get
detected algorithmically from base geometry and styled per city motif: tinted
roof fills + a darker shadow side, palette per city (see shade_city.py STYLES).

### Still to fetch from the wiki at build time
- Kelethin/Greater Faydark (wood elf platform city in the trees), Paineel
  (heretic necromancers, The Hole), Neriak trio (Teir'Dal — darkelf.py kit
  exists), Felwithe (high elf — gold and marble), Kaladim (dwarf), Erudin
  (Prexus, water motif — restrained), Freeport trio (Ottoman/Dornish mercantile,
  already in better shape), Surefall Glade (rangers, cavern entrance),
  Rathe Mountains (froglok city treatment), Kerra Isle (kerra village).

## EQOA historical layer

Coastal Ro zones: EQOA arrows must not point into the ocean — angle them along
the coast (what was southeast in EQOA may be south now). Applies to nro, sro,
oasis, freeport coast.
