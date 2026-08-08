import sys, re
sys.path.insert(0,'/home/claude/work')
# import data without running the render (guarded by __main__)
import importlib.util
spec=importlib.util.spec_from_file_location("ab","/home/claude/work/align_build.py")
ab=importlib.util.module_from_spec(spec); spec.loader.exec_module(ab)
ANT, ODUS = ab.ANT, ab.ODUS
# hypothetical zone names from hypo_map.py
src=open('/home/claude/work/hypo_map.py').read()
hy=re.findall(r'"([^"]+)":\(\d+,\d+,\'hy\'\)', src)

TIER={3:'Large (size 4)',2:'Medium (size 3)',1:'Small (size 2)'}
def zone_block(name, z):
    L=[f"#### {name}"]
    if z['note']:
        n=z['note'].replace('*** ','**').replace('***','**')
        L.append(f"> {n}\n" if not z['note'].startswith('***') else f"> ⚠️ {n}\n")
    if z['dia']:
        L.append("| On-map label | Tier |")
        L.append("|---|---|")
        for nm,t in z['dia']: L.append(f"| ◆ {nm} | {TIER[t]} |")
        L.append("")
    if z['arr']:
        L.append("| Margin signpost | Direction |")
        L.append("|---|---|")
        for nm,dr in z['arr']: L.append(f"| ← To {nm} | {dr} |")
        L.append("")
    if not z['dia'] and not z['arr']:
        L.append("_No labels — nothing to add._\n")
    return "\n".join(L)

nd=sum(len(z['dia']) for z in ANT.values())+sum(len(z['dia']) for z in ODUS.values())
na=sum(len(z['arr']) for z in ANT.values())+sum(len(z['arr']) for z in ODUS.values())

R=[]
R.append(f"""# EQOA → EQ1 Alignment Report
### Proposed `_3` easter-egg layer — for review before build

**Totals:** {nd} on-map diamonds · {na} margin signposts · across {len(ANT)} Antonica + {len(ODUS)} Odus zones.

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
""")
for k,v in ANT.items(): R.append(zone_block(k,v)); R.append("")
R.append("---\n\n## 7. Odus — per zone\n")
for k,v in ODUS.items(): R.append(zone_block(k,v)); R.append("")

R.append(f"""---

## 8. Appendix — hypothetical Tunaria zones

The EQOA-only areas (the ones becoming signposts) are drawn on `_tunaria_hypothetical_zone_map.png` as **proposed zones** wired into the classic connection graph — a planning sketch for carving out space for future development. Proposed links are geographic reads off the EQOA world map, **not canon adjacency**.

{len(hy)} proposed zones:

""")
for i in range(0,len(hy),3):
    R.append("- " + " · ".join(hy[i:i+3]))
R.append(f"""

---

## 9. Open questions for review

1. **Grid cell names** — the 20 suggested gap names are yours; the 77 EQOA names are mine. Any cell you'd rename, move, merge, or split?
2. **More paired signposts** — Kerplunk is the clear case. Others that may deserve the same treatment: Bandit Hills (between Gorge and North Karana), Bastable Village (between Highpass and West Commonlands), Merry-by-Water (between North Karana and Rivervale).
3. **Curving-path notation** — is `To Oggok (NE — path curves back W)` the right phrasing, or too wordy for a map label? Shorter option: `To Oggok (NE ↻W)`.
4. **Tiers** — anything mis-weighted?
5. **Lavastorm boundary wording** — "Age of Adventure NW Boundary" (yours) vs the EQOA original "NE Mountain Boundary."
6. **Density** — 6–9 per big zone, or push further on the largest (Everfrost, South Karana)?

_On your OK (with notes), the `_3` layers get regenerated across all listed zones._
""")
open('/mnt/user-data/outputs/EQOA_alignment_report.md','w',newline='').write("\n".join(R))
print("report written:", nd, "diamonds,", na, "arrows,", len(hy), "hypothetical zones")
