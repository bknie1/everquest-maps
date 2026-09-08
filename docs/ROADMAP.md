# Emoda Maps — Living Roadmap

The single source of truth for outstanding work. **Every task lands here with a
status and an owner.** Detailed per-zone review notes live in
`REVIEW-2026-09-06.md`; this file is the tracker that says what's done, what's
running, and what's next. Update the status the moment something ships.

Status: ☐ todo · ◐ in-flight (session) · ☑ done+verified · ⏸ needs Brandon input

---

## P0 — Nektulos (closing 2026-09-08, the one that kept slipping)

- ☑ Neriak gate: was mirrored (tool's y-flip) in the SW corner. V-flipped +
  moved to top-left, native center (-1422,-2711), per Brandon's /loc target
  (2711,1422,-2737). Foliage keep-out applied. **place_neriak_gate.py is now
  guarded** so it can't re-dump the gate SW.
- ☑ Lavastorm mountains: volcanic peak range added along the north edge with
  lava-glow markers by the "to Lavastorm" exit.
- ☑ Nektropos castle: shifted right (2026-09-06). Brandon: "looks great."
- ☑ HD flora/fauna update (2026-09-08): the 15 old fauna.py wireframe figures
  (skeleton, halfling, dark elf) retired for fauna_sil silhouettes — curated to
  8 solid figures (3 Teir'Dal, 2 skeletons, 1 orc = Deathfist/orc-runner, 2
  Leatherfoot halflings), fill-decimated to fit budget (total 30,785/31k, was
  30,171). Spiders kept (no SIL spider). Flora confirmed HD: margins are dense
  flora_hd darkwood (9.5k strokes); interior stays deliberately light per the
  nek_color label-legibility doctrine, so no interior giants (they'd bury
  labels + burst budget). Tool: src/zones/nek_hd_fauna.py. Keep-outs untouched.
- ⏸ Stylized title (see Title Campaign below — themed, not plain).

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
- ☑ nektulos-hd — Nektulos HD flora/fauna (2026-09-08): wireframe figures →
  fauna_sil silhouettes; flora confirmed HD-darkwood margins.

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

## TODO — unowned, need scheduling

- ☐ **Titles-too-big shrink audit** (new doctrine: unrest is the size bar).
  Ak'Anon done as the first. Sweep every oversized title down to ~unrest scale
  and re-verify knockouts. Candidates: the soldung trio, guk pair, freeports,
  kerraridge, neriak trio, cauldron, oggok, najena — anything whose letters
  dominate the band.
- ☐ **Compass-size standardization** (everfrost = the standard). One pass to
  normalize any rose still off-standard.
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
| gfaydark | wood-elf |
| lfaydark | dark Mirkwood (with the biome session) |
| mistmoore | spooky vampire castle (unrest=haunted house, this=haunted castle) |
| permafrost | ice castle (Halas meets Mistmoore) |
| hateplane | Innoruuk / Prince of Hate (Neriak cleric kin) |
| innothule | swampy troll/froglok |
| lavastorm | lava/ember |
| misty | (theme TBD, wants stylized) |
| kithicor | dark forest (Kithicor kin to lfay) |
| nektulos | dark forest / Teir'Dal |
| neriak a/b/c | unify the three, Freeport-style two-tier, keep dark-elf styling |

### Plain-caps queue — ⏸ need a theme decision from Brandon
befallen, beholder, butcher, cauldron, crushbone, kedge, qey2hh1, oasis?, nro?,
sro?, stonebrunt?, everfrost?, blackburrow?, others flagged "plain".

Execution plan: batch the themed set into title sessions by family (forest
group, castle group, elemental group), history-check each, design in
`src/titles/styles.py` + `apply_title.py`, render at 900px, verify knockout,
update the zone doc. Plain-caps queue waits on Brandon picking themes.
