# Emoda Maps — Living Roadmap

The single source of truth for outstanding work. **Every task lands here with a
status and an owner.** Detailed per-zone review notes live in
`REVIEW-2026-09-06.md`; this file is the tracker that says what's done, what's
running, and what's next. Update the status the moment something ships.

Status: ☐ todo · ◐ in-flight (session) · ☑ done+verified · ⏸ needs Brandon input

---

## P0 — Nektulos ☑ CLOSED 2026-09-09 (v0.2.2-alpha; patches .1 .2 .3)

- ☑ Neriak gate: was mirrored (tool's y-flip) in the SW corner. V-flipped
  upright and moved to the TOP-RIGHT beside its own "to Neriak" zone-line POI
  (native ~1108,-2272), gate center ~(1030,-2360). Rough margin trees knocked
  out behind it (clean clearing). **place_neriak_gate.py is now guarded** so it
  can't re-dump the gate SW.
- ☑ Lavastorm mountains: volcanic peak range added along the north edge with
  lava-glow markers by the "to Lavastorm" exit.
- ☑ Nektropos castle: shifted right (2026-09-06). Brandon: "looks great."
- ☑ Creepy-forest rebuild (2026-09-09, src/zones/nek_rebuild.py) — Brandon's
  real pass. Composed _2 fresh BY REGION (past the 34,58,38 shared-ink
  entanglement): kept interior + fauna_sil silhouettes + castle + title +
  compass; PURGED all old tree/crown flora. New flora = a CREEPY dead-forest of
  bare snags + dark conifers on a quantized green(south)→purple→blue(north)
  gradient (the halfling→Neriak transition Brandon loves). Neriak gate flipped
  right-way-up + reseated in the right margin; Nektropos castle RESTORED; frame
  WIDENED (borders -1990/1780 → -2170/2130) so the margin has room; volcanoes at
  the Lavastorm exit; keep-outs for the wizard gate / portals / ruins. 15,792/31k,
  grade B, 0 dupes. Superseded the 09-08 HD flora (darkwood) + fauna margin passes
  (the fauna silhouettes carried through; the darkwood flora was replaced).
- ☑ Stylized title (2026-09-08): `darkwood` with a Teir'Dal violet tint — kept
  through the rebuild (title band preserved by region). Done.
- ☑ Patch v0.2.2.1 → v0.2.2.2 (2026-09-09): the right-margin WIZARD GATE was
  buried in trees. It's a LOCKED-IN graphic (`eqmap_toolkit.wizard_gate` —
  ziggurat + portal swirl, the one that "looks like the gate"). v0.2.2.1 wrongly
  REDREW it; v0.2.2.2 reverts that and KEEPS the original, just fencing trees off
  it with a keep-out. (GFay's gate should reuse eqmap_toolkit.wizard_gate too — do
  not redraw.) Also purged two missed old darkwood inks (52,46,74 / 56,48,40).

## Meta-fix (why this file exists)

Things kept getting left behind because work was scattered across chat and a
long review doc with no completion tracking. Rule now: **nothing is "done"
until it's ☑ here with a commit.** A forked session isn't done — it's ◐ until
it reports back and its zones are verified.

---

## IN-FLIGHT sessions (verify + mark ☑ when each reports)

- ◐ crushbone-hd — Crushbone HD decor modernization.
- ◐ lfay-mirkwood — Lesser Faydark dark-wood identity (giant mushrooms/trees).
- ◐ felwithe — banner + entrance-facade archaeology, compass, trees, flora.
- ☑ nektulos-hd — Nektulos HD flora/fauna (2026-09-08): fauna (wireframes →
  fauna_sil silhouettes) + flora (rough margin crowns → darkwood Mirkwood). Done.

## DONE + verified (2026-09-06 → 09-08)

- ☑ Border-knockout sweep: airplane, everfrost, fearplane, halas, hole (full
  frame), innothule, lakerathe, misty, nro, oasis, oot, sro, stonebrunt,
  warrens (full frame), unrest, erudsxing, grobb grid line, guktop bald spot.
- ☑ Shading: everfrost N+W, halas top+left + compass, freeport trio → freporte
  density, freporte south sand, kerraridge sand + compass reseat.
- ☑ Artifacts/compasses: qeynos/kedge/erudnext/qrg/qcat artifacts, erudnext
  water-on-land, erud overlap, erudsxing/oot/paw?/misty compass, hateplane
  compass → b's, eastkarana arrow shrink, blackburrow/cazicthule overlaps,
  commons WEST COMMONLANDS beta title restored.
- ☑ Creatures: sro skeletons, stonebrunt+warrens silhouette kobolds,
  gukbottom undead frogloks, soltemple flames?, rivervale halfling motifs?.
- ☑ Compass verdicts: soltemple, runnyeye, grobb, newsebexp, najena, oggok,
  highkeep, gukbottom, tox, rivervale, misty.
- ☑ Steamfont windmills (drakes → pinwheels). Ak'Anon title shrink + top border
  + artifacts. Befallen runaways removed. Brogdog relocated. Feerrott.

## FINAL SWEEP ☑ 2026-09-12 (Fable 5.1, on main + deployed)

Pack-wide "same page" pass driven by eqqms, which gained two report-only
columns: **t-px** (title band height) and **rose** (compass ring radius),
both in pixels at a 900px fit — the size the viewer actually shows, and the
only scale a dungeon and a continent can be compared on. A rose outside
14–40px is flagged.

- ☑ **Titles-too-big shrink audit** — 15 titles scaled in place by ink+window
  (`scale_title_ink.py`, band plot verified before every write): highkeep
  (0.75, + its lost G restored from 69380bc), guktop 0.75, gukbottom 0.85,
  highpass 0.70, kaladima 0.75, kedge 0.80, cauldron 0.80, rivervale 0.80,
  beholder 0.70, neriakb 0.60 (was 2× its siblings), soldunga 0.70, soldungb
  0.80, soldungc 0.80, crushbone 0.75, fearplane 0.80. Left alone on purpose:
  the freeport trio + sewers (already the two-tier style, letters 59–62px),
  neriaka/c (in line with neriakb now), kerraridge/paineel/tox (restored
  verbatim wireframes), oggok/najena/grobb/qeynos pair (city-slate fits, in
  Brandon's queues). qeynos2's ghost stick title (17 strokes below the band
  cut) deleted.
- ☑ **Compass-size standardization** — 19 roses rebuilt at ring 24px@fit by
  `restd_compass.py` (letters scale with the ring): crushbone, highkeep,
  kedge, soldungb, soldungc, paineel, guktop, gukbottom, rathemtn, commons,
  butcher, steamfont, neriakc, soltemple, kaladima, kaladimb, hateplane,
  highpass, rivervale. Boulder/canopy polygons knocked out of the footprint
  as whole components (butcher, steamfont, kaladim pair). Census now scales
  its gates so it can see them; it still misses spokes-only roses (gfaydark,
  lfaydark — both fine on render) and reads nektulos's guard-post sketch as a
  second rose. Report-only.
- ☑ **Dupes → 0** on every non-locked zone: `dedupe.py --near` (1dp, folds
  <0.05u twins eqqms counts) over 28 zones, 1,244 strokes. unrest (53) and
  eastkarana (248) left — LOCKED; free win when Brandon unlocks.
- Baseline after: 78/79 A or B (feerrott F by doctrine); every B is a plain-caps
  style verdict waiting on a theme.

## TODO — unowned, need scheduling

- ⏸ paineel margin mountains — variation/offset (lowest priority, "already good").
- ⏸ kaladim a/b — freeport-inspired title separation treatment.
- ☐ Rechecks after viewer refresh (Brandon): runnyeye, tox title clipping,
  crushbone overlap.

---

## TITLE CAMPAIGN — the standing miss, now tracked per zone

Doctrine: every zone gets a themed title; the pale block-caps family is dead;
unrest is the quality + size bar; **no icons/figures in titles**; keep the
string; scale in place, never restyle to stick font; history-check first
(`git log --follow`), restore a good original before designing new.

### Themed (brief already given by Brandon) — ◐ ready to build
| zone | theme |
|---|---|
| gfaydark | wood-elf — ☑ `woodelf` 2026-09-08 |
| lfaydark | dark Mirkwood (with the biome session) |
| mistmoore | spooky vampire castle — ☑ `gothic` (prior session; verified 2026-09-08, reads well — flagging only that it sits on the larger end vs the smaller-title doctrine, Brandon to verdict) |
| permafrost | ice castle (Halas meets Mistmoore) — ☑ `ice` 2026-09-08 |
| hateplane | Innoruuk / Prince of Hate (Neriak cleric kin) — ☑ `hate` 2026-09-08 |
| innothule | swampy troll/froglok — ☑ `swamp` 2026-09-08 |
| lavastorm | lava/ember — ☑ `lava` 2026-09-08 |
| misty | (theme TBD, wants stylized) |
| kithicor | dark forest (Kithicor kin to lfay) — ☑ `darkwood` 2026-09-08 |
| nektulos | dark forest / Teir'Dal — ☑ `darkwood` (violet Teir'Dal tint) 2026-09-08 |
| neriak a/b/c | unify the three, Freeport-style two-tier, keep dark-elf styling |

### Plain-caps queue — ⏸ need a theme decision from Brandon
befallen, beholder, butcher, cauldron, crushbone, kedge, qey2hh1, oasis?, nro?,
sro?, stonebrunt?, everfrost?, blackburrow?, others flagged "plain".

Execution plan: batch the themed set into title sessions by family (forest
group, castle group, elemental group), history-check each, design in
`src/titles/styles.py` + `apply_title.py`, render at 900px, verify knockout,
update the zone doc. Plain-caps queue waits on Brandon picking themes.
