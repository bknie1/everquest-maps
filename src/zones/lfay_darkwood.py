"""lfay_darkwood.py -- the Mirkwood pass for Lesser Faydark.

GFay is the safe wood; LFay is the dark one. This pass fills the interior with
what the base map's polite little crowns don't say: darkwood giants, a deep
understory of black-green firs, groves of giant toadstools, pale snags, and
fungus on the floor. Everything APPENDS to lfaydark_2.txt -- base, POIs and
history are never touched (zone_pass RULE 1/2), and the pass refuses to run
twice or to burst the 31k budget (RULE 3).

Keep-outs: POI labels (point + text run), the base trails and boundary walls,
and the content edge. The title band and compass live outside the grid, which
this pass never leaves.

    python src/zones/lfay_darkwood.py            # place + append
    python src/zones/lfay_darkwood.py --dry      # count, place, write nothing
"""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fix_title import content_bbox, parse  # noqa: E402
from layout import layout  # noqa: E402
import flora as F  # noqa: E402
import flora_hd as FH  # noqa: E402
from terrain import scatter  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
BUDGET = 31000
CEILING = 30800          # leave headroom under the client cap
ZONE = "lfaydark"

CANOPY_DEEP = (34, 58, 38)       # the Kithicor black-green
TRUNK_DK = (56, 48, 40)
SNAG = (84, 82, 76)              # pale dead wood, ghostly against the dark
FUNGUS = (120, 104, 122)
MOSS = (44, 74, 48)
MOSS_DK = (34, 60, 40)

WALL_INKS = {(64, 54, 44)}
TRAIL_INKS = {(140, 108, 60), (74, 56, 34)}
CROWN_INKS = {(48, 86, 52), (74, 116, 72)}


def load_L(path):
    if not os.path.exists(path):
        return []
    return [parse(l) for l in open(path, encoding="utf-8") if l.startswith("L")]


def load_P(path):
    out = []
    for l in open(path, encoding="utf-8"):
        if not l.startswith("P"):
            continue
        f = l[1:].split(",")
        out.append((float(f[0]), float(f[1]), f[7].strip()))
    return out


class Hash:
    """Point hash for 'is anything of this class within r of (x,y)'."""

    def __init__(self, cell=64.0):
        self.cell = cell
        self.d = {}

    def add_seg(self, x1, y1, x2, y2):
        n = int(max(abs(x2 - x1), abs(y2 - y1)) / 28.0) + 1
        for i in range(n + 1):
            t = i / n
            x, y = x1 + (x2 - x1) * t, y1 + (y2 - y1) * t
            self.d.setdefault((int(x // self.cell), int(y // self.cell)), []).append((x, y))

    def near(self, x, y, r):
        c = self.cell
        for gx in range(int((x - r) // c), int((x + r) // c) + 1):
            for gy in range(int((y - r) // c), int((y + r) // c) + 1):
                for px, py in self.d.get((gx, gy), ()):
                    if (px - x) ** 2 + (py - y) ** 2 < r * r:
                        return True
        return False


def main():
    dry = "--dry" in sys.argv
    base = load_L(os.path.join(MAPS, ZONE + ".txt"))
    p2 = os.path.join(MAPS, ZONE + "_2.txt")
    raw2 = [l for l in open(p2, encoding="utf-8").read().splitlines() if l.strip()]
    pois = load_P(os.path.join(MAPS, ZONE + "_1.txt"))
    total = len(base) + len(pois) + len(raw2)

    if any(l.startswith("L") and l.rstrip().endswith("124, 92, 134") for l in raw2):
        sys.exit(f"{ZONE}: shroom-cap ink already in _2 -- the darkwood pass ran. "
                 f"Not appending twice.")

    LO = layout(content_bbox(ZONE))
    cx0, cx1, cy0, cy1 = LO["content"]
    pad = 60.0
    x0, x1, y0, y1 = cx0 + pad, cx1 - pad, cy0 + pad, cy1 - pad

    walls, trails, crowns = Hash(), Hash(), Hash()
    for s in base:
        h = (walls if s[4] in WALL_INKS else
             trails if s[4] in TRAIL_INKS else
             crowns if s[4] in CROWN_INKS else None)
        if h is not None:
            h.add_seg(s[0], s[1], s[2], s[3])

    poi_boxes = [(px - 80, px + 42 * len(lbl) + 100, py - 80, py + 80)
                 for px, py, lbl in pois]

    def in_poi(x, y, pad=0.0):
        return any(a - pad < x < b + pad and c - pad < y < d + pad
                   for a, b, c, d in poi_boxes)

    def clear(x, y, wall_r, trail_r, crown_r, poi_pad=0.0):
        if not (x0 < x < x1 and y0 < y < y1):
            return False
        return not (in_poi(x, y, poi_pad) or walls.near(x, y, wall_r)
                    or trails.near(x, y, trail_r)
                    or (crown_r and crowns.near(x, y, crown_r)))

    new = []
    counts = {}

    def emit(name, segs):
        counts[name] = counts.get(name, 0) + len(segs)
        new.extend(segs)

    placed = Hash(cell=128.0)

    # ---- darkwood giants: the old trees, spread wide -----------------------
    giants = scatter(x0 + 280, y0 + 540, x1 - 280, y1 - 60, 11, 900.0,
                     seed=11, tries_mult=400,
                     reject=lambda x, y: not clear(x, y, 80, 60, 70, poi_pad=240))
    for i, (gx, gy) in enumerate(giants):
        s = random.Random(100 + i).uniform(360, 460)
        emit("darkwood", FH.darkwood(gx, gy, s, seed=300 + i))
        placed.add_seg(gx, gy, gx, gy)

    # ---- giant toadstool groves -------------------------------------------
    rnd = random.Random(23)
    grove_centers = scatter(x0 + 200, y0 + 150, x1 - 200, y1 - 150, 6, 1300.0,
                            seed=29, tries_mult=400,
                            reject=lambda x, y: not clear(x, y, 90, 70, 0)
                            or placed.near(x, y, 500))
    shroom_n = 0
    for gi, (gx, gy) in enumerate(grove_centers):
        k = rnd.randint(4, 6)
        pts = scatter(gx - 420, gy - 260, gx + 420, gy + 260, k, 170.0,
                      seed=41 + gi, tries_mult=300,
                      reject=lambda x, y: y < y0 + 240 or not clear(x, y, 60, 50, 45, poi_pad=80))
        for j, (sx, sy) in enumerate(pts):
            s = rnd.uniform(120, 215)
            emit("giant_mushroom", FH.giant_mushroom(sx, sy, s, seed=gi * 31 + j))
            placed.add_seg(sx, sy, sx, sy)
            shroom_n += 1

    # ---- understory: black-green firs between the base crowns -------------
    firs = scatter(x0, y0 + 170, x1, y1, 250, 155.0, seed=53, tries_mult=300,
                   reject=lambda x, y: not clear(x, y, 45, 35, 25)
                   or placed.near(x, y, 160))
    for i, (fx, fy) in enumerate(firs):
        s = random.Random(500 + i).uniform(85, 150)
        emit("understory_fir", F.fir(fx, fy, s, ink=CANOPY_DEEP, trunk=TRUNK_DK))

    # ---- pale snags ---------------------------------------------------------
    snags = scatter(x0, y0 + 240, x1, y1, 18, 550.0, seed=67, tries_mult=300,
                    reject=lambda x, y: not clear(x, y, 55, 45, 40)
                    or placed.near(x, y, 200))
    for i, (sx, sy) in enumerate(snags):
        s = random.Random(700 + i).uniform(130, 200)
        emit("snag", F.dead_tree(sx, sy, s, ink=SNAG, seed=i))

    # ---- floor fungus + moss around the set-pieces -------------------------
    anchors = giants + [(x, y) for x, y in snags]
    fungus = scatter(x0, y0, x1, y1, 26, 400.0, seed=71, tries_mult=250,
                     reject=lambda x, y: not clear(x, y, 40, 35, 0))
    for i, (fx, fy) in enumerate(fungus):
        s = random.Random(900 + i).uniform(38, 68)
        emit("floor_fungus", F.mushrooms(fx, fy, s, ink=FUNGUS, seed=i))
    emit("moss", FH.faydwer_floor(anchors, seed=83, clumps=(2, 3), spread=90.0,
                                  size=(14.0, 26.0), ink=MOSS, dark=MOSS_DK,
                                  reject=lambda x, y: not clear(x, y, 35, 30, 0)
                                  or not (x0 < x < x1 and y0 < y < y1)))

    # ---- budget gate, then append ------------------------------------------
    grand = total + len(new)
    print(f"{ZONE}: existing {total}, adding {len(new)} -> {grand}/{BUDGET}")
    for k, v in counts.items():
        print(f"   {k:16} {v}")
    print(f"   giants={len(giants)} groves={len(grove_centers)} shrooms={shroom_n} "
          f"firs={len(firs)} snags={len(snags)}")
    if grand > CEILING:
        sys.exit(f"{ZONE}: {grand} would pass the {CEILING} ceiling -- trim counts")
    if dry:
        print("(dry run: nothing written)")
        return
    lines = ["L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
             % (s[0], s[1], s[2], s[3], *s[4]) for s in new]
    open(p2, "w", newline="", encoding="utf-8").write(CRLF.join(raw2 + lines) + CRLF)
    print(f"{ZONE}: APPENDED {len(lines)} strokes to {p2}. "
          f"Now: python src/tools/render_zone.py {ZONE}")


if __name__ == "__main__":
    main()
