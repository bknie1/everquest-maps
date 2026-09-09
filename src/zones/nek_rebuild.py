"""nek_rebuild.py -- fresh compose of Nektulos _2, dropping the accumulated
artifacts (Brandon, 2026-09-08: "looks like a mess, gate isn't in the margin,
lavastorm has volcanos and you did little pointed triangles").

Rather than patch the tangled _2, this rebuilds it by REGION so the (34,58,38)
ink entanglement never bites:

  KEEP  the interior (inside the grid): grass, river, bridge, interior trees,
        and the fauna_sil silhouettes -- all the good stuff already sits here.
  KEEP  the title band, the compass disc, and the worn frame border.
  DROP  the two artifacts by ink: the crude Neriak gate blob (72,66,86) and the
        fake lava "peaks" (80,58,50 / 210,90,25 / 60,45,45), plus the gate's box
        tangle in its footprint.
  DROP  the whole old margin ring (rough crowns + the previous darkwood pass) and
        REGENERATE it fresh -- tuned darkwood Mirkwood, north purple / south green.
  ADD   real volcanoes (terrain.volcano) along the top by the "to Lavastorm" exit.
  ADD   the Neriak dolmen sketch (neriak_gate_segs) in the RIGHT margin beside the
        "to Neriak" exit -- in the margin, where it belongs.

    python src/zones/nek_rebuild.py --dry
    python src/zones/nek_rebuild.py
"""
import collections
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

import flora as F          # noqa: E402
import flora_hd as FH      # noqa: E402
import terrain as TR       # noqa: E402
from terrain import scatter  # noqa: E402
from neriak_gate import neriak_gate_segs  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
P = os.path.join(MAPS, "nektulos_2.txt")
P1 = os.path.join(MAPS, "nektulos_1.txt")
CRLF = "\r\n"
CEILING = 30800

GX0, GX1, GY0, GY1 = -1656, 1440, -3423, 3023        # grid rectangle
FX0, FX1, FY0, FY1 = -2382, 2166, -4497, 3749        # frame
TITLE_Y = -3315                                       # title band floor
COMPASS = (1514.0, 2872.0, 300.0)                    # cx, cy, keep-radius

GATE_INK = (72, 66, 86)
LAVA_ARTIFACT = {(80, 58, 50), (210, 90, 25), (60, 45, 45)}
GATE_BOX = (680, 1380, -2640, -2080)                 # gate footprint to scrub
GATE_BOX_INKS = {(124, 96, 68), (150, 124, 92), (122, 124, 138), (140, 132, 124)}

# Mirkwood palette (matches nek_hd_flora): north Teir'Dal purple / south green
N_TREE = (52, 46, 74); N_TRUNK = (48, 40, 58); N_FIR = (54, 48, 76)
S_TREE = (44, 66, 46); S_TRUNK = (56, 48, 40); S_FIR = (40, 60, 44)
SNAG = (84, 82, 76)
SPLIT_Y = 360.0

# volcano inks (match the lavastorm zone)
V_ROCK = (96, 78, 70); V_LAVA = (198, 92, 40)


def parse(l):
    f = l[2:].split(",")
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


def Lstr(a, b, c, d, ink):
    return "L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a, b, c, d, *ink)


def decimate(segs, keep=2):
    fills = collections.defaultdict(list)
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


def in_grid(x, y):
    return GX0 < x < GX1 and GY0 < y < GY1


def near_frame(x, y):
    # thin: only the worn border line itself, not the crown blobs sitting inboard
    return (abs(x - FX0) < 60 or abs(x - FX1) < 60 or
            abs(y - FY0) < 60 or abs(y - FY1) < 60)


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
    dry = "--dry" in sys.argv
    rows = [l.rstrip("\r\n") for l in open(P, encoding="utf-8") if l.strip()]
    head = [l for l in rows if l[:1] not in "L"]
    body = [l for l in rows if l[:1] == "L"]

    # ---- classify: keep interior + title + compass + frame; drop artifacts + margin
    kept = []
    drop_art = drop_margin = 0
    cx, cy, cr = COMPASS
    for l in body:
        x1, y1, x2, y2, ink = parse(l)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if ink == GATE_INK or ink in LAVA_ARTIFACT:
            drop_art += 1
            continue
        if (GATE_BOX[0] < mx < GATE_BOX[1] and GATE_BOX[2] < my < GATE_BOX[3]
                and ink in GATE_BOX_INKS):
            drop_art += 1
            continue
        if my <= TITLE_Y:                                   # title band + top frame
            kept.append(l); continue
        if (mx - cx) ** 2 + (my - cy) ** 2 < cr * cr:       # compass disc
            kept.append(l); continue
        if in_grid(mx, my):                                 # interior (+ fauna)
            kept.append(l); continue
        if near_frame(mx, my):                              # worn border
            kept.append(l); continue
        drop_margin += 1                                    # old margin ring -> regen

    # ---- regenerate margins: darkwood Mirkwood, tuned lighter than before ----
    pois = load_pois()
    KEEPOUTS = [(-2106, -1520, 700, 3400),                  # Nektropos castle SW
                (int(cx - cr), int(cx + cr), int(cy - cr), int(cy + cr)),  # compass
                (1430, 2110, -2680, -1830)]                 # Neriak gate footprint (right margin)

    def in_keepout(x, y):
        for a, b, c, d in KEEPOUTS:
            if a < x < b and c < y < d:
                return True
        for a, b, c, d in pois:
            if a < x < b and c < y < d:
                return True
        return False

    placed = []

    def far(x, y, r):
        return all((px - x) ** 2 + (py - y) ** 2 > r * r for px, py, _ in placed)

    def pal(y):
        return (N_TREE, N_TRUNK, N_FIR) if y < SPLIT_Y else (S_TREE, S_TRUNK, S_FIR)

    new = []
    rnd = random.Random(7)
    LEFT = (-2060, -1470, -2820, 900)
    RIGHT = (1170, 2000, -2820, 780)
    SOUTH = (-1950, 1750, 960, 3300)

    def place_col(region, gseed, gn, fseed, fn_, sseed, sn, green_only=False):
        # A dark CONIFER wood -- clean tiered pines, not the scribbly broadleaf
        # giants (those read as blobs at map scale). A few big HD firs as accents,
        # a bulk of small side-on pines, and a couple of pale snags.
        x0, x1, y0, y1 = region

        def rej(x, y, r):
            if in_keepout(x, y) or not far(x, y, r):
                return True
            if green_only:                                  # south: stay out of grid,
                if in_grid(x, y):                           # and leave a clean gap
                    return True                             # below the grid so pines
                if GY1 < y < GY1 + 130:                     # don't collide with the
                    return True                             # interior-edge crowns
            return False
        # big accent pines -- clean side-on conifers (F.fir), well spaced
        gs = scatter(x0, y0, x1, y1, gn, 380.0, seed=gseed, tries_mult=500,
                     reject=lambda x, y: rej(x, y, 215))
        for i, (gx, gy) in enumerate(gs):
            _, _, fir = pal(gy)
            s = rnd.uniform(230, 285)
            new.extend(Lstr(*seg) for seg in
                       F.fir(gx, gy, s, ink=fir,
                             trunk=(fir[0] - 12, fir[1] - 12, fir[2] - 12)))
            placed.append((gx, gy, s * 0.55))
        # bulk understory pines, two-tone by seed for depth
        fs = scatter(x0, y0, x1, y1, fn_, 150.0, seed=fseed, tries_mult=400,
                     reject=lambda x, y: rej(x, y, 142))
        for i, (fx, fy) in enumerate(fs):
            _, _, fir = pal(fy)
            dk = (fir[0] - 10, fir[1] - 10, fir[2] - 10) if i % 3 == 0 else fir
            s = random.Random(fseed * 11 + i).uniform(105, 175)
            new.extend(Lstr(*seg) for seg in
                       F.fir(fx, fy, s, ink=dk,
                             trunk=(fir[0] - 12, fir[1] - 12, fir[2] - 12)))
            placed.append((fx, fy, s * 0.5))
        ss = scatter(x0, y0, x1, y1, sn, 320.0, seed=sseed, tries_mult=400,
                     reject=lambda x, y: rej(x, y, 150))
        for i, (px, py) in enumerate(ss):
            s = random.Random(sseed * 13 + i).uniform(150, 210)
            new.extend(Lstr(*seg) for seg in F.dead_tree(px, py, s, ink=SNAG, seed=i))
            placed.append((px, py, s * 0.4))

    place_col(LEFT, 11, 6, 21, 26, 31, 5)
    place_col(RIGHT, 12, 5, 22, 20, 32, 4)
    place_col(SOUTH, 41, 7, 42, 30, 43, 5, green_only=True)

    # ---- volcanoes along the top, by the "to Lavastorm" exit ----
    volc = []
    for i, (vx, vy, w, h) in enumerate([(-880, -3120, 300, 250),
                                        (-560, -3060, 240, 205),
                                        (60, -3110, 320, 270),
                                        (470, -3055, 230, 195)]):
        volc += TR.volcano(vx, vy, w, h, ink=V_ROCK, lava=V_LAVA, seed=13 + i)
    new += [Lstr(*s) for s in volc]

    # ---- Neriak dolmen sketch, RIGHT margin beside the "to Neriak" exit ----
    segs = neriak_gate_segs()
    lminx = min(min(s[0], s[2]) for s in segs); lmaxx = max(max(s[0], s[2]) for s in segs)
    lminy = min(min(s[1], s[3]) for s in segs); lmaxy = max(max(s[1], s[3]) for s in segs)
    # target box: right margin, centered near the Neriak exit y (~-2300)
    tcx, tcy, tw, th = 1770.0, -2250.0, 620.0, 760.0
    sc = min(tw / (lmaxx - lminx), th / (lmaxy - lminy))
    nx0 = tcx - (lminx + lmaxx) / 2 * sc

    def gx(x): return nx0 + x * sc
    def gy(y): return tcy - (y - (lminy + lmaxy) / 2) * sc   # in-game y-flip
    gate = [Lstr(gx(a), gy(b), gx(c), gy(d), GATE_INK) for a, b, c, d in segs]
    new += gate

    # ---- assemble + budget ----
    def layer_count(suf):
        p = os.path.join(MAPS, "nektulos" + suf + ".txt")
        return sum(1 for l in open(p, encoding="utf-8") if l[:1] in "LP") \
            if os.path.exists(p) else 0
    others = sum(layer_count(s) for s in ("", "_1", "_3"))
    final_2 = len(kept) + len(new)
    total = others + final_2
    print(f"dropped: {drop_art} artifact + {drop_margin} old-margin strokes")
    print(f"added:   {len(new)} strokes ({len(volc)} volcano, {len(gate)} gate, "
          f"{len(new) - len(volc) - len(gate)} flora)")
    print(f"_2: {len(body)} -> {final_2}   ALL LAYERS -> {total}/{CEILING}")
    if dry:
        return
    if total > CEILING:
        sys.exit(f"ABORT: {total} over ceiling")
    payload = CRLF.join(head + kept + new) + CRLF   # build first; never truncate on error
    open(P, "w", newline="", encoding="utf-8").write(payload)
    print(f"wrote {P}")


if __name__ == "__main__":
    main()
