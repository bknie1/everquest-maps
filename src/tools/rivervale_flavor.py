"""rivervale_flavor.py -- Brandon's 2026-09-06 rivervale flavor pass.

Two jobs, one idempotent runner:

1. KNOCKOUTS: the margin sketches (four dome burrows, the pie basket, the
   honeycomb, the pond rocks, the cart, the hay row) were never knocked out --
   canopy hexagons are drawn straight over them. Tree components are grouped
   on EXACT shared vertices (round 0.01 -- see workflow lesson 9: rounding
   coarser chains touching trees into mega-components) and removed WHOLE
   wherever they intersect a padded reserve box; orphan interior dashes and
   trunks (small components inside a removed canopy's bbox) go with them.

2. MOTIFS: halfling-life sketches from src/kit/halfling_decor.py -- pie,
   beer mug, cheese wheel, wine jug -- placed in margin clearings away from
   exit labels, each with its own knockout box.

    python src/tools/rivervale_flavor.py          # apply
    python src/tools/rivervale_flavor.py --probe  # report only
"""
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

import halfling_decor as HD  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
P2 = os.path.join(MAPS, "rivervale_2.txt")

TREE_INKS = {(56, 74, 44), (78, 96, 58), (95, 70, 45)}

# existing margin sketches, probed 2026-09-06 (bbox), padded below
SKETCHES = [
    (-400, -338, -276, -228),   # burrow, left top
    (-342, 86, -218, 196),      # burrow, left bottom
    (816, 105, 940, 215),       # burrow, right (Moss Mouth)
    (329, 504, 453, 614),       # burrow, bottom
    (97, 514, 198, 588),        # pie basket, bottom
    (-269, -107, -218, -57),    # honeycomb (Merry-by-Water)
    (866, -176, 951, -143),     # hay row, right
    (-299, -413, -205, -358),   # pond rocks, left
    (-385, -1, -291, 54),       # pond rocks, left lower
    (843, -48, 900, 3),         # cart, right
]
PAD = 26

# new motifs: (fn, cx, cy, r, seed) -- clear of every exit label in _1/_3
MOTIFS = [
    (HD.pie, 598, 700, 42, 7),
    (HD.beer_mug, -180, 690, 40, 3),
    (HD.cheese_wheel, 880, 412, 38, 5),
    (HD.wine_bottle, -345, 298, 40, 9),
]
MOTIF_INKS = set(HD.PALETTE.values())


def parse(l):
    b = l[2:].replace(",", " ").split()
    x1, y1, _, x2, y2, _ = map(float, b[:6])
    return x1, y1, x2, y2, tuple(map(int, b[6:9]))


def main():
    probe = "--probe" in sys.argv
    raw = [l for l in open(P2, encoding="utf-8").read().splitlines() if l.strip()]

    # idempotence: strip any motif-ink strokes inside the motif boxes (a prior
    # run's stamps) so re-running replaces instead of double-stamping
    mboxes = []
    for fn, cx, cy, r, seed in MOTIFS:
        segs = fn(cx, cy, r, seed=seed)
        xs = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        mboxes.append((min(xs) - 40, min(ys) - 40, max(xs) + 40, max(ys) + 40))

    def in_mbox(x, y):
        return any(x0 < x < x1 and y0 < y < y1 for x0, y0, x1, y1 in mboxes)

    old = set()
    for i, l in enumerate(raw):
        if l[:1] == "L":
            s = parse(l)
            if s[4] in MOTIF_INKS and in_mbox((s[0] + s[2]) / 2, (s[1] + s[3]) / 2):
                old.add(i)
    if old:
        print(f"rivervale: replacing {len(old)} previously placed motif strokes")
        raw = [l for i, l in enumerate(raw) if i not in old]

    tree = {}
    for i, l in enumerate(raw):
        if l[:1] == "L":
            s = parse(l)
            if s[4] in TREE_INKS:
                tree[i] = s

    # exact-vertex union-find over tree strokes (round 0.01)
    parent = {}

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    vert = defaultdict(list)
    for i, (x1, y1, x2, y2, _) in tree.items():
        parent[i] = i
        vert[(round(x1, 2), round(y1, 2))].append(i)
        vert[(round(x2, 2), round(y2, 2))].append(i)
    for ids in vert.values():
        for k in ids[1:]:
            union(ids[0], k)

    comp = defaultdict(list)
    for i in tree:
        comp[find(i)].append(i)

    boxes = [(x0 - PAD, y0 - PAD, x1 + PAD, y1 + PAD) for x0, y0, x1, y1 in SKETCHES]
    new = []
    for fn, cx, cy, r, seed in MOTIFS:
        segs = fn(cx, cy, r, seed=seed)
        xs = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        boxes.append((min(xs) - 22, min(ys) - 22, max(xs) + 22, max(ys) + 22))
        for s in segs:
            new.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                       % (s[0], s[1], s[2], s[3], *s[4]))

    def hits(bx0, by0, bx1, by1):
        return any(bx0 < x1 and bx1 > x0 and by0 < y1 and by1 > y0
                   for x0, y0, x1, y1 in boxes)

    kill, killed_bbox = set(), []
    for ids in comp.values():
        xs = [v for i in ids for v in (tree[i][0], tree[i][2])]
        ys = [v for i in ids for v in (tree[i][1], tree[i][3])]
        if hits(min(xs), min(ys), max(xs), max(ys)):
            kill.update(ids)
            killed_bbox.append((min(xs) - 3, min(ys) - 3, max(xs) + 3, max(ys) + 28))
    n_canopy = len(kill)

    # orphan pass: dashes/trunks -- small components living inside a removed
    # canopy's bbox (extended down for trunks)
    for ids in comp.values():
        if ids[0] in kill or len(ids) > 4:
            continue
        xs = [v for i in ids for v in (tree[i][0], tree[i][2])]
        ys = [v for i in ids for v in (tree[i][1], tree[i][3])]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        if any(x0 < cx < x1 and y0 < cy < y1 for x0, y0, x1, y1 in killed_bbox):
            kill.update(ids)

    print(f"rivervale: {len(comp)} tree components; removing {len(kill)} strokes "
          f"({n_canopy} canopy + {len(kill) - n_canopy} orphan dashes/trunks); "
          f"adding {len(new)} motif strokes")
    if probe:
        return
    keep = [l for i, l in enumerate(raw) if i not in kill]
    open(P2, "w", newline="", encoding="utf-8").write(CRLF.join(keep + new) + CRLF)
    print(f"wrote {P2}: {len(raw)} -> {len(keep) + len(new)} lines")


if __name__ == "__main__":
    main()
