"""nek_hd_flora.py -- retire Nektulos's rough-sketch margin trees for HD darkwood.

The left/right margin forest was old rough polygon-crown sketches (ink 46,40,68),
the same low-fi symptom the Faydark maps had. This pass REPLACES the big crown
blobs with the Mirkwood recipe Brandon approved for Lesser Faydark/Kithicor:
FH.darkwood giants as the hero trees over a dense black-green conifer understory,
with a few pale snags for the sinister note. North of the river the wood takes
the Teir'Dal purple (Nektulos's established convention); south stays green.

The small (46,40,68) clusters (interior undergrowth ticks) are KEPT -- only the
big crown blobs (>= 15 strokes) are removed. Removing them frees ~4.4k strokes,
so the HD forest fits under the client cap.

Keep-outs (never planted over): the Nektropos castle sketch (SW), the Neriak
gate (now top-right), the lavastorm peak band (north edge), the compass (SE),
the title band, POI labels, and the map grid interior (margins only).

    python src/zones/nek_hd_flora.py --dry     # count + place, write nothing
    python src/zones/nek_hd_flora.py           # apply
"""
import collections
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from terrain import scatter  # noqa: E402
import flora as F  # noqa: E402
import flora_hd as FH  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
P = os.path.join(MAPS, "nektulos_2.txt")
P1 = os.path.join(MAPS, "nektulos_1.txt")
CRLF = "\r\n"
CEILING = 30800
CROWN = (46, 40, 68)                    # the north (Teir'Dal) rough crowns
# the south (halfling country) rough crowns are the same sketch in green inks
GREEN = {(34, 58, 38), (46, 72, 48), (54, 80, 46), (50, 76, 50),
         (58, 66, 46), (66, 90, 56), (70, 96, 58), (86, 104, 62)}
GX0, GX1, GY0, GY1 = -1656, 1440, -3423, 3023   # grid rectangle

# Mirkwood palette -- north takes the Teir'Dal purple, south stays green
N_TREE = (52, 46, 74); N_TRUNK = (48, 40, 58); N_FIR = (54, 48, 76)
S_TREE = (44, 66, 46); S_TRUNK = (56, 48, 40); S_FIR = (40, 60, 44)
SNAG = (84, 82, 76)
SPLIT_Y = 360.0                       # ~the river: north purple / south green

# keep-out boxes (x0, x1, y0, y1), padded
KEEPOUTS = [
    (-2106, -1520, 700, 3400),        # Nektropos castle, SW
    (640, 1420, -2680, -2040),         # Neriak gate, top-right
    (-1200, 980, -3200, -2900),        # lavastorm peak band, north edge
    (1280, 1760, 2620, 3120),          # compass, SE
]


def parse(l):
    f = l[2:].split(",")
    return (float(f[0]), float(f[1]), float(f[3]), float(f[4]),
            (int(f[6]), int(f[7]), int(f[8])))


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


def load_pois():
    boxes = []
    if not os.path.exists(P1):
        return boxes
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

    # guard: don't run twice (our darkwood trunk_dark north ink is a marker)
    if any(l.rstrip().endswith("52, 46, 74") for l in body):
        sys.exit("nek_hd_flora: north darkwood ink already present -- pass ran. Abort.")

    def in_grid(x, y):
        return GX0 < x < GX1 and GY0 < y < GY1

    def in_south_margin(x, y):
        # the south margin ring: outside the grid, lower half. The grid edge is
        # the safe divider -- (34,58,38) is shared with the interior forest,
        # which clusters into the margin crowns if we reach past the border, so
        # we stop at it and leave interior-edge trees alone.
        return y > 950 and not in_grid(x, y)

    # cluster the rough-crown blobs; drop big ones, keep small ticks. North
    # crowns are the purple ink anywhere; south crowns are the same sketch in
    # green, only in the south margin U-band so the interior is never touched.
    idx = []
    for i, l in enumerate(body):
        x1, y1, x2, y2, ink = parse(l)
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        if ink == CROWN:
            idx.append(i)
        elif ink in GREEN and in_south_margin(mx, my):
            idx.append(i)
    G = 55.0
    cells = collections.defaultdict(list)
    for i in idx:
        x1, y1, x2, y2, _ = parse(body[i])
        cells[(int(((x1 + x2) / 2) // G), int(((y1 + y2) / 2) // G))].append(i)
    seen = set()
    drop = set()
    for k in list(cells):
        if k in seen:
            continue
        st = [k]
        comp = []
        while st:
            d = st.pop()
            if d in seen or d not in cells:
                continue
            seen.add(d)
            comp += cells[d]
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    nn = (d[0] + dx, d[1] + dy)
                    if nn in cells and nn not in seen:
                        st.append(nn)
        if len(comp) >= 15:
            drop.update(comp)
    kept = [l for i, l in enumerate(body) if i not in drop]
    removed = len(drop)

    # occupancy of everything kept, so new trees don't sit on labels/sketches
    pois = load_pois()

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

    # the two margin columns where the crowns were (left + right), upper zone.
    # Top floor is -2880 so the tall giants (drawn upward) never grow into the
    # title band (y < -3323) -- RULE 5. The top corners stay clear by the title.
    LEFT = (-2060, -1430, -2880, 900)
    RIGHT = (1150, 2010, -2880, 780)
    new = []
    rnd = random.Random(7)

    def reject(x, y):
        return in_keepout(x, y) or not far(x, y, 150)

    # ---- darkwood giants: the hero trees, spread down both columns ----
    for region, seed, n in ((LEFT, 11, 8), (RIGHT, 12, 6)):
        x0, x1, y0, y1 = region
        gs = scatter(x0, y0, x1, y1, n, 360.0, seed=seed, tries_mult=400,
                     reject=reject)
        for i, (gx, gy) in enumerate(gs):
            tree, trunk, _ = pal(gy)
            s = rnd.uniform(260, 330)
            new += decimate(FH.darkwood(gx, gy, s, ink=tree, trunk=trunk,
                                        seed=300 + seed + i))
            placed.append((gx, gy, s))

    # ---- black-green conifer understory: filler between the giants ----
    for region, seed, n in ((LEFT, 21, 42), (RIGHT, 22, 30)):
        x0, x1, y0, y1 = region
        fs = scatter(x0, y0, x1, y1, n, 118.0, seed=seed, tries_mult=300,
                     reject=lambda x, y: in_keepout(x, y) or not far(x, y, 84))
        for i, (fx, fy) in enumerate(fs):
            _, _, fir = pal(fy)
            s = random.Random(500 + seed + i).uniform(120, 180)
            new += F.fir(fx, fy, s, ink=fir, trunk=(fir[0] - 8, fir[1] - 8, fir[2] - 8))
            placed.append((fx, fy, s * 0.45))

    # ---- a few pale snags for the sinister note (north) ----
    for region, seed, n in ((LEFT, 31, 8), (RIGHT, 32, 6)):
        x0, x1, y0, y1 = region
        ss = scatter(x0, y0, x1, y1, n, 260.0, seed=seed, tries_mult=300,
                     reject=lambda x, y: in_keepout(x, y) or not far(x, y, 120))
        for i, (sx, sy) in enumerate(ss):
            s = random.Random(700 + seed + i).uniform(150, 230)
            new += F.dead_tree(sx, sy, s, ink=SNAG, seed=i)
            placed.append((sx, sy, s * 0.4))

    # ---- SOUTH margins: the same Mirkwood, in green (halfling country). The
    # crowns here wrap the lower grid in a U (lower flanks + bottom band); we
    # scatter across that whole bbox and reject the grid interior + keep-outs so
    # trees land only in the margin ring where the rough crowns were.
    SOUTH = (-1950, 1750, 960, 3320)
    sx0, sx1, sy0, sy1 = SOUTH

    def s_reject(x, y, r):
        return in_keepout(x, y) or not in_south_margin(x, y) or not far(x, y, r)

    gs = scatter(sx0, sy0, sx1, sy1, 10, 300.0, seed=41, tries_mult=500,
                 reject=lambda x, y: s_reject(x, y, 150))
    for i, (gx, gy) in enumerate(gs):
        s = rnd.uniform(260, 330)
        new += decimate(FH.darkwood(gx, gy, s, ink=S_TREE, trunk=S_TRUNK,
                                    seed=440 + i))
        placed.append((gx, gy, s))
    fs = scatter(sx0, sy0, sx1, sy1, 46, 120.0, seed=42, tries_mult=400,
                 reject=lambda x, y: s_reject(x, y, 84))
    for i, (fx, fy) in enumerate(fs):
        s = random.Random(560 + i).uniform(120, 180)
        new += F.fir(fx, fy, s, ink=S_FIR,
                     trunk=(S_FIR[0] - 8, S_FIR[1] - 8, S_FIR[2] - 8))
        placed.append((fx, fy, s * 0.45))
    ss = scatter(sx0, sy0, sx1, sy1, 8, 260.0, seed=43, tries_mult=400,
                 reject=lambda x, y: s_reject(x, y, 120))
    for i, (px, py) in enumerate(ss):
        s = random.Random(760 + i).uniform(150, 220)
        new += F.dead_tree(px, py, s, ink=SNAG, seed=50 + i)
        placed.append((px, py, s * 0.4))

    # ---- budget + write ----
    def layer_count(suf):
        p = os.path.join(MAPS, "nektulos" + suf + ".txt")
        return sum(1 for l in open(p, encoding="utf-8") if l[:1] in "LP") \
            if os.path.exists(p) else 0
    others = sum(layer_count(s) for s in ("", "_1", "_3"))
    final_2 = len(kept) + len(new)
    total = others + final_2
    print(f"crowns removed: {removed} strokes; HD flora added: {len(new)} strokes")
    print(f"giants={sum(1 for p in placed)}  (see counts)  _2: {len(body)} -> {final_2}")
    print(f"ALL LAYERS total -> {total} (ceiling {CEILING})")
    if dry:
        print("(dry run: nothing written)")
        return
    if total > CEILING:
        sys.exit(f"ABORT: {total} passes the {CEILING} ceiling -- trim counts")
    out_lines = ["L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                 % (s[0], s[1], s[2], s[3], *s[4]) for s in new]
    open(P, "w", newline="", encoding="utf-8").write(
        CRLF.join(head + kept + out_lines) + CRLF)
    print(f"wrote {P}")


if __name__ == "__main__":
    main()
