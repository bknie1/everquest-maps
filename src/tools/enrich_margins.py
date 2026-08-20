"""enrich_margins.py -- add wiki-driven, race/creature-appropriate decoration to
a zone's margin ring, using the flora/fauna/terrain kit. Preserves the whole _2.

The workflow Brandon built and I kept skipping: read the zone's wiki page, see
which creatures/races actually live there, and place THOSE in the margins with
the detailed kit -- gnolls ring Blackburrow, kobolds ring the Warrens, and so on.

    python src/tools/enrich_margins.py warrens --probe
    python src/tools/enrich_margins.py warrens

Only the margin ring is touched (build.place keeps decoration out of the grid and
away from reserved boxes); everything already in _2 is kept.
"""
import argparse
import collections
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fix_title import content_bbox  # noqa: E402
from layout import layout  # noqa: E402
import build as B  # place, ring_slots, _fa, _fl, _tr  # noqa: E402
import fauna as FA, flora as FL, terrain as TR  # noqa: E402
import fauna_hd_gnoll, fauna_hd_troll, fauna_hd_zombie, fauna_hd_ghoul  # noqa: E402
import fauna_hd_kobold, fauna_hd_darkelf, fauna_hd_iksar  # noqa: E402

# detailed HD figures where they exist (feet at cx,cy; s = height; take face+seed)
HD_FIG = {
    "gnoll": fauna_hd_gnoll.gnoll, "troll": fauna_hd_troll.troll,
    "kobold": fauna_hd_kobold.kobold, "dark_elf": fauna_hd_darkelf.dark_elf,
    "iksar": fauna_hd_iksar.iksar, "zombie": fauna_hd_zombie.zombie,
    "skeleton": fauna_hd_zombie.zombie, "ghoul": fauna_hd_ghoul.ghoul,
}


def _hd(fn, frac=0.058):
    """Wrap an HD figure as a build.place shape (x,y,S) -> strokes."""
    def g(x, y, S, _fn=fn):
        h = S * frac
        face = -1 if int(abs(x)) % 2 == 0 else 1
        return _fn(x, y + h * 0.5, h, seed=int(abs(x) + abs(y)), face=face)
    return g

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
WIKI = os.path.join(HERE, "..", "data", "wiki")
CRLF = "\r\n"

# wiki words -> a kit figure key. Aliases map real EQ mobs onto what the kit draws.
ALIAS = {
    "gnoll": "gnoll", "splitpaw": "gnoll", "sabertooth": "wolf", "kobold": "kobold",
    "goblin": "kobold", "skeleton": "skeleton", "spider": "spider", "bat": "bat",
    "snake": "snake", "serpent": "snake", "rat": "rat", "ratman": "ratman",
    "wolf": "wolf", "bear": "wolf", "drake": "drake", "dragon": "drake",
    "sprite": "sprite", "pixie": "sprite", "faerie": "sprite", "myconid": "myconid",
    "mushroom": "myconid", "froglok": "froglok", "frog": "froglok", "skunk": "skunk",
    "dark elf": "dark_elf", "high elf": "high_elf", "wood elf": "wood_elf",
    "gnome": "gnome", "dwarf": "dwarf", "ogre": "ogre", "troll": "troll",
    "orc": "kobold", "minotaur": "ogre", "ghoul": "ghoul", "zombie": "zombie",
    "undead": "skeleton", "shadowknight": "skeleton", "lizardman": "iksar",
    "lizard": "iksar", "froglok": "froglok",
}

# biome flora/terrain by a coarse tag, chosen per zone below
BIOME = {
    "cave":   dict(flora=[], terrain=[(TR.rock_band, "peak")]),
    "forest": dict(flora=[FL.broadleaf, FL.fern], terrain=[]),
    "snow":   dict(flora=[FL.fir], terrain=[(TR.snowdrift, None)]),
    "swamp":  dict(flora=[FL.reeds, FL.dead_tree], terrain=[]),
    "desert": dict(flora=[FL.palm], terrain=[]),
}


def wiki_motifs(zone, top=3):
    """Ranked kit-figure keys present in the zone's wiki page."""
    p = os.path.join(WIKI, zone + ".md")
    if not os.path.exists(p):
        return [], collections.Counter()
    text = open(p, encoding="utf-8").read().lower()
    hits = collections.Counter()
    for word, key in ALIAS.items():
        c = text.count(word)
        if c:
            hits[key] += c
    ranked = [k for k, _ in hits.most_common() if (k in FA.CREATURES or k in FA.RACES)]
    return ranked[:top], hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--biome", default="cave", choices=list(BIOME))
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()

    motifs, hits = wiki_motifs(args.zone)
    if not motifs:
        print(f"{args.zone}: no kit-drawable creatures found in wiki")
        return
    if args.probe:
        print(f"{args.zone}: wiki motifs -> {motifs}   (top hits: "
              f"{', '.join('%s:%d' % (k, v) for k, v in hits.most_common(6))})")
        return

    LO = layout(content_bbox(args.zone))
    shapes = [(_hd(HD_FIG[m]) if m in HD_FIG else B._fa(m)) for m in motifs]  # HD where we have it
    b = BIOME[args.biome]
    for fl in b["flora"]:
        shapes.append(B._fl(fl, FL.PALETTE.get("broadleaf"), FL.PALETTE.get("trunk"), 0.020, 0.030))
    for (fn, _) in b["terrain"]:
        if fn in (TR.snowdrift,):
            shapes.append(B._tr(fn, 0.026, 0.036))

    placed, n = B.place(shapes, LO, reserved=[])
    if not placed:
        print(f"{args.zone}: nothing placed (margins too tight)")
        return
    new = ["L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (s[0], s[1], s[2], s[3], *s[4])
           for s in placed]
    path = os.path.join(MAPS, args.zone + "_2.txt")
    old = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    open(path, "w", newline="", encoding="utf-8").write(CRLF.join(old + new) + CRLF)
    print(f"{args.zone}: placed {n} kit figures/props ({len(new)} strokes) round the margin "
          f"from wiki motifs {motifs}; everything else kept")


if __name__ == "__main__":
    main()
