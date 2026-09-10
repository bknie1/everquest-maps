"""nek_rebuild.py -- the real Nektulos pass (Brandon, 2026-09-08).

"Scrap all but the base, keep the fauna, completely redo the flora in a creepy
Nektulos way, maintain the halfling-green -> Neriak dark/purple/blue transition,
flip the upside-down gate, bring back Nektropos castle."

Purges EVERY old tree/crown ink (margin AND interior) and rebuilds one cohesive
creepy dead-forest. Grass, water, the bridge, the fauna_sil silhouettes, the
title, the compass, the frame and the Nektropos castle sketch all use other inks
/ live in kept regions, so they survive untouched.

  ADD  a creepy dead forest: bare clawing snags (dominant) + a few dark full
       trees, every tree coloured by a smooth green(south)->purple->blue(north)
       gradient. Dense round the margins, sparse in the interior, off the labels.
  ADD  real volcanoes by the "to Lavastorm" exit.
  ADD  the Neriak dolmen sketch in the RIGHT margin, RIGHT WAY UP.

    python src/zones/nek_rebuild.py --src <path> [--dry]
"""
import argparse
import collections
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

import flora as F          # noqa: E402
import terrain as TR       # noqa: E402
from terrain import scatter  # noqa: E402
from neriak_gate import neriak_gate_segs  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
P = os.path.join(MAPS, "nektulos_2.txt")
P1 = os.path.join(MAPS, "nektulos_1.txt")
CRLF = "\r\n"
CEILING = 30800

GX0, GX1, GY0, GY1 = -1656, 1440, -3423, 3023
FX0, FX1, FY0, FY1 = -2382, 2166, -4497, 3749
TITLE_Y = -3315
COMPASS = (1514.0, 2872.0, 300.0)

FRAME_INKS = {(90, 70, 110), (120, 115, 125), (45, 38, 55)}
NEW_LX, NEW_RX = -2170.0, 2130.0        # widened side borders (was ~-1990 / ~1780)
GATE_INK = (72, 66, 86)
DROP_INK = {(80, 58, 50), (210, 90, 25), (60, 45, 45), GATE_INK}   # lava peaks + gate blob
CASTLE_INKS = {(54, 44, 70), (86, 74, 104), (45, 38, 55), (90, 70, 110),
               (34, 28, 44), (128, 116, 150), (120, 115, 125)}
# every old foliage/crown/fir ink (green + Teir'Dal purple families) -> purged.
# excludes grass, water, bridge, fauna and castle inks.
TREE_INKS = {
    (34, 58, 38), (46, 72, 48), (54, 80, 46), (50, 76, 50), (58, 66, 46),
    (66, 90, 56), (70, 96, 58), (86, 104, 62), (32, 52, 36), (20, 42, 22),
    (34, 26, 18), (40, 60, 44), (30, 50, 34), (28, 48, 32), (54, 44, 44),
    (62, 52, 84), (66, 54, 88), (70, 58, 92), (52, 42, 58), (46, 40, 68),
    (82, 70, 104), (64, 54, 86), (104, 92, 126), (44, 38, 66), (42, 36, 64),
    (28, 22, 50), (26, 18, 36), (54, 48, 76), (48, 40, 58), (96, 90, 104),
    (44, 66, 46), (84, 82, 76), (52, 74, 59), (57, 49, 44),
    (52, 46, 74), (56, 48, 40),   # nek_hd_flora darkwood N_TREE / S_TRUNK (missed)
}
# fauna silhouette ground points -- kept as boxes so no silhouette stroke is
# purged even where a body ink coincides with a foliage ink.
FAUNA_PTS = [(108, -559), (461, -913), (75, -1809), (-383, -1290), (132, -651),
             (67, -404), (-825, 1133), (-272, 1593)]
FAUNA_R = 150.0

V_ROCK = (96, 78, 70); V_LAVA = (198, 92, 40)
SNAG_N = (78, 74, 92); SNAG_S = (110, 98, 74)
# wizard gate: the LOCKED-IN graphic (eqmap_toolkit.wizard_gate -- pseudo-3D
# ziggurat + portal swirl, inks stone 120,116,124 / dark 60,58,64 / portal
# 150,95,185) is kept as-is; we only fence trees off it. Extends below the base
# so nothing grows up into it (trees draw upward).
WIZ_KEEPOUT = (1280, 1840, -920, -160)


def parse(l):
    f = l[2:].split(",")
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def Lstr(a, b, c, d, ink):
    return "L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a, b, c, d, *ink)


def in_grid(x, y):
    return GX0 < x < GX1 and GY0 < y < GY1


def near_frame(x, y):
    return (abs(x - FX0) < 60 or abs(x - FX1) < 60 or
            abs(y - FY0) < 60 or abs(y - FY1) < 60)


def _lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def grad(y):
    """foliage / trunk / dead-wood inks: south green -> mid purple -> north blue.
    t is QUANTIZED to a few discrete bands so the gradient reads smooth but the
    palette stays small (eqqms caps distinct inks) -- ~5 bands per half."""
    NF, MF, SF = (52, 56, 106), (64, 56, 88), (58, 96, 56)
    NT, MT, ST = (44, 40, 66), (52, 46, 54), (60, 50, 38)
    yN, yM, yS = -3100.0, 350.0, 3100.0
    q = lambda t: round(t * 4) / 4.0                       # 5 bands per segment
    if y <= yM:
        t = q(max(0.0, min(1.0, (y - yN) / (yM - yN))))
        return _lerp(NF, MF, t), _lerp(NT, MT, t), _lerp(SNAG_N, (94, 86, 82), t)
    t = q(max(0.0, min(1.0, (y - yM) / (yS - yM))))
    return _lerp(MF, SF, t), _lerp(MT, ST, t), _lerp((94, 86, 82), SNAG_S, t)


def load_pois():
    boxes = []
    for l in open(P1, encoding="utf-8"):
        if l[:1] != "P":
            continue
        f = l[1:].split(",")
        px, py = float(f[0]), float(f[1])
        lbl = f[7].strip() if len(f) > 7 else ""
        boxes.append((px - 90, px + 34 * max(1, len(lbl)) + 80, py - 70, py + 70))
    return boxes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", default=P)
    ap.add_argument("--dry", action="store_true")
    args = ap.parse_args()

    rows = [l.rstrip("\r\n") for l in open(args.src, encoding="utf-8") if l.strip()]
    head = [l for l in rows if l[:1] not in "L"]
    body = [l for l in rows if l[:1] == "L"]

    cx, cy, cr = COMPASS

    def in_fauna(x, y):
        return any((x - fx) ** 2 + (y - fy) ** 2 < FAUNA_R ** 2 for fx, fy in FAUNA_PTS)

    def old_side_border(mx, my, ink):
        # the worn side-border zigzags we are moving outward (not the title/bottom
        # borders, not the castle sketch)
        if ink not in FRAME_INKS or my <= TITLE_Y:
            return False
        if mx < -1500 and my > 700:                       # castle sketch
            return False
        if 1470 < mx < 1880 and -3320 < my < 3400:        # right side border
            return True
        if -2070 < mx < -1930 and -3320 < my < 760:       # left side border (upper)
            return True
        return False

    kept = []
    d_tree = d_art = d_frame = n_castle = 0
    for l in body:
        x1, y1, x2, y2, ink = parse(l)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if ink in DROP_INK:
            d_art += 1; continue
        if old_side_border(mx, my, ink):                  # remove; re-drawn wider
            d_frame += 1; continue
        if my <= TITLE_Y or (mx - cx) ** 2 + (my - cy) ** 2 < cr * cr:
            kept.append(l); continue
        if mx < -1500 and my > 700 and ink in CASTLE_INKS:
            kept.append(l); n_castle += 1; continue
        if ink in TREE_INKS and not in_fauna(mx, my):    # purge old flora
            d_tree += 1; continue
        kept.append(l)                                    # grass, water, bridge, fauna, frame

    # ---- keep-outs for the new flora ----
    pois = load_pois()
    KEEPOUTS = [(-2130, -1470, 720, 1560),                  # Nektropos castle (towers only)
                (int(cx - cr), int(cx + cr), int(cy - cr), int(cy + cr)),  # compass
                (1490, 2100, -2700, -1840),                 # Neriak gate footprint
                (-60, 940, -1040, -340),                    # wizard gate / Knowledge Portal / Minor Spires
                (-140, 300, -2020, -1680),                  # north obelisk ruin
                (-1380, -1030, 800, 1080),                  # Halfling Ruins gold statue
                WIZ_KEEPOUT]                                # redrawn wizard gate (right margin)

    def in_keepout(x, y):
        return (any(a < x < b and c < y < d for a, b, c, d in KEEPOUTS)
                or any(a < x < b and c < y < d for a, b, c, d in pois)
                or in_fauna(x, y))

    placed = []

    def far(x, y, r):
        return all((px - x) ** 2 + (py - y) ** 2 > r * r for px, py, _ in placed)

    new = []
    rnd = random.Random(9)

    def tree(x, y, dead):
        fol, trk, dw = grad(y)
        if dead:
            return F.dead_tree(x, y, rnd.uniform(150, 250), ink=dw,
                               seed=int(abs(x * 3 + y)))
        dk = (fol[0] - 8, fol[1] - 8, fol[2] - 8)
        return F.fir(x, y, rnd.uniform(120, 200), ink=dk, trunk=trk)

    def populate(region, n, seed, spacing, dead_frac=0.52, gap_below_grid=False):
        x0, x1, y0, y1 = region
        pts = scatter(x0, y0, x1, y1, n, spacing, seed=seed, tries_mult=500,
                      reject=lambda x, y: (in_keepout(x, y) or not far(x, y, spacing - 8)
                                           or (gap_below_grid and in_grid(x, y))
                                           or (gap_below_grid and GY1 < y < GY1 + 120)))
        for i, (x, y) in enumerate(pts):
            dead = random.Random(seed * 17 + i).random() < dead_frac
            new.extend(Lstr(*g) for g in tree(x, y, dead))
            placed.append((x, y, spacing))

    # ---- widened side borders (worn zigzag), so the margin has real room ----
    FRAME_INK = (90, 70, 110)

    def vzig(x, y0, y1, amp=38.0, wl=150.0):
        out = []
        n = max(2, int(abs(y1 - y0) / wl))
        px, py = x - amp, y0
        for k in range(n + 1):
            ny = y0 + (y1 - y0) * (k + 1) / (n + 1)
            nx = x + amp if px < x else x - amp
            out.append((px, py, nx, ny, FRAME_INK)); px, py = nx, ny
        return out
    border = vzig(NEW_RX, -3304, 3379) + vzig(NEW_LX, -3304, 700)
    border += [(1780, -3304, NEW_RX, -3304, FRAME_INK),      # top-right connector
               (1803, 3379, NEW_RX, 3379, FRAME_INK),        # bottom-right connector
               (-1990, -3304, NEW_LX, -3304, FRAME_INK),     # top-left connector
               (-1990, 700, NEW_LX, 700, FRAME_INK)]         # left border foot (by castle)
    new.extend(Lstr(*s) for s in border)

    # DENSE dark-wood margins (bare snags + gradient conifers) -- packed tight
    # (Brandon: "this is a dark wood"). Bare dead trees dominate so they pack
    # cleanly without blobbing; columns run to the NEW borders, off the keep-outs.
    populate((-2130, -1440, -3120, 1620), 205, 11, 70, dead_frac=0.58)    # left column
    populate((1150, 2090, -3120, 780), 180, 12, 70, dead_frac=0.58)       # right column
    populate((-1950, 1760, 960, 3360), 128, 41, 74, dead_frac=0.58, gap_below_grid=True)  # south U
    # a denser haunted wood INSIDE the grid too, held off the labels + structures
    populate((GX0 + 110, GX1 - 110, GY0 + 240, GY1 - 150), 74, 71, 196, dead_frac=0.64)

    # ---- volcanoes by the "to Lavastorm" exit ----
    volc = []
    for i, (vx, vy, w, h) in enumerate([(-880, -3120, 300, 250), (-560, -3060, 240, 205),
                                        (60, -3110, 320, 270), (470, -3055, 230, 195)]):
        volc += TR.volcano(vx, vy, w, h, ink=V_ROCK, lava=V_LAVA, seed=13 + i)
    new += [Lstr(*s) for s in volc]

    # ---- Neriak dolmen sketch, RIGHT margin, RIGHT WAY UP ----
    segs = neriak_gate_segs()
    lminx = min(min(s[0], s[2]) for s in segs); lmaxx = max(max(s[0], s[2]) for s in segs)
    lminy = min(min(s[1], s[3]) for s in segs); lmaxy = max(max(s[1], s[3]) for s in segs)
    # right margin is now ~690 wide (grid 1440 -> new border 2130); sit clearly
    # inside it by the "to Neriak" exit.
    tcx, tcy, tw, th = 1790.0, -2250.0, 560.0, 740.0
    sc = min(tw / (lmaxx - lminx), th / (lmaxy - lminy))
    nx0 = tcx - (lminx + lmaxx) / 2 * sc
    ny0 = tcy - (lminy + lmaxy) / 2 * sc

    def gx(x): return nx0 + x * sc
    def gy(y): return ny0 + y * sc          # no flip -> rock face on top, tunnel down
    gate = [Lstr(gx(a), gy(b), gx(c), gy(d), GATE_INK) for a, b, c, d in segs]
    new += gate

    def lc(suf):
        p = os.path.join(MAPS, "nektulos" + suf + ".txt")
        return sum(1 for l in open(p, encoding="utf-8") if l[:1] in "LP") \
            if os.path.exists(p) else 0
    others = sum(lc(s) for s in ("", "_1", "_3"))
    final_2 = len(kept) + len(new)
    total = others + final_2
    print(f"kept {len(kept)} (castle {n_castle}); purged {d_tree} tree + {d_art} artifact")
    print(f"added {len(new)} ({len(volc)} volcano, {len(gate)} gate, "
          f"{len(new) - len(volc) - len(gate)} creepy flora)")
    print(f"_2 -> {final_2}   ALL LAYERS -> {total}/{CEILING}")
    if args.dry:
        return
    if total > CEILING:
        sys.exit(f"ABORT {total}")
    open(P, "w", newline="", encoding="utf-8").write(CRLF.join(head + kept + new) + CRLF)
    print(f"wrote {P}")


if __name__ == "__main__":
    main()
