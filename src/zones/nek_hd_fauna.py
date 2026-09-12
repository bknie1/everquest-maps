"""nek_hd_fauna.py -- retire Nektulos's low-fi interior figures for fauna_sil.

The interior creatures were placed long ago by the old fauna.py wireframes
(nek_color.py: FA.spider/skeleton/hobbit/darkelf). Brandon read them as the
last low-fi holdout in the zone. This pass REPLACES the humanoid wireframes
(skeleton, halfling, dark elf) with fauna_sil silhouettes -- the only figure
style that reads at map scale -- and repurposes one slot as an orc (the wiki's
Deathfist Legionnaire / orc runner). Spiders are left as-is: fauna_sil has no
spider, and the little webs read fine.

Budget is the hard constraint (~800 strokes of headroom under 31k), so this
thins 15 wireframes down to 8 curated silhouettes and decimates each figure's
sub-pixel solid-fill scanlines (invisible at map scale, ~halves the cost).
Everything else in _2 -- margins, grass, river, sketches, gate, lava peaks,
wizard gate, title, compass -- is preserved byte-for-byte.

    python src/zones/nek_hd_fauna.py --dry     # report, change nothing
    python src/zones/nek_hd_fauna.py           # apply
"""
import sys, os, collections, argparse

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))
from fauna_sil import SIL  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
P = os.path.join(MAPS, "nektulos_2.txt")
CRLF = "\r\n"

# old fauna.py figure inks present in _2 (spider kept, not listed here)
OLD = {"skeleton": (108, 104, 96), "halfling": (86, 70, 52), "dark_elf": (72, 58, 96)}

# curated replacement roster: (race, cx, ground_cy, height, face)
# positions reuse old, collision-vetted figure slots; the rest are left empty.
ROSTER = [
    # Teir'Dal (Neriak guards/dragoons) -- north, toward the Neriak gate
    ("dark_elf", 108, -559, 92, 1),
    ("dark_elf", 461, -913, 92, -1),
    ("dark_elf", 75, -1809, 92, -1),
    # undead (decaying / greater skeletons) -- wandering the woods
    ("skeleton", -383, -1290, 82, -1),
    ("skeleton", 132, -651, 82, 1),
    # the orc runner / Deathfist, central on the road
    ("orc", 67, -404, 100, -1),
    # Leatherfoot halflings -- the SW camp and druid ring
    ("halfling", -825, 1133, 70, 1),
    ("halfling", -272, 1593, 70, -1),
]


def parse(l):
    f = l[2:].split(",")
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def decimate_fill(segs, keep=2):
    """Drop (keep-1)/keep of the horizontal solid-fill scanlines; keep every
    outline/accent stroke. Scanlines are sub-pixel-dense at map scale, so this
    is invisible but roughly halves the stroke count."""
    fills = collections.defaultdict(list)   # rounded-y -> segs
    other = []
    for s in segs:
        if abs(s[1] - s[3]) < 1e-6:
            fills[round(s[1], 2)].append(s)
        else:
            other.append(s)
    out = list(other)
    for i, y in enumerate(sorted(fills)):
        if i % keep == 0:
            out += fills[y]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    rows = [l.rstrip("\r\n") for l in open(P, encoding="utf-8") if l.strip()]
    head = [l for l in rows if l[:1] not in "L"]
    body = [l for l in rows if l[:1] == "L"]

    old_inks = set(OLD.values())
    kept = [l for l in body if parse(l)[4] not in old_inks]
    removed = len(body) - len(kept)

    new = []
    for race, cx, cy, h, face in ROSTER:
        segs = decimate_fill(SIL[race](cx, cy, h, face=face), keep=2)
        for s in segs:
            new.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                       % (s[0], s[1], s[2], s[3], *s[4]))

    # total across all layers (budget is all-layers)
    def layer_count(suf):
        p = os.path.join(MAPS, "nektulos" + suf + ".txt")
        return sum(1 for l in open(p, encoding="utf-8") if l[:1] in "LP") \
            if os.path.exists(p) else 0
    others = sum(layer_count(s) for s in ("", "_1", "_3"))
    final_2 = len(kept) + len(new)
    total = others + final_2
    print(f"removed {removed} old wireframe strokes; added {len(new)} silhouette "
          f"strokes for {len(ROSTER)} figures")
    print(f"_2: {len(body)} -> {final_2}   ALL LAYERS total -> {total}/31000")
    if args.dry:
        return
    if total > 31000:
        sys.exit(f"ABORT: {total} bursts the 31000 budget")
    open(P, "w", newline="", encoding="utf-8").write(CRLF.join(head + kept + new) + CRLF)
    print(f"wrote {P}")


if __name__ == "__main__":
    main()
