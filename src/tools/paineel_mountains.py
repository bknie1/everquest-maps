"""paineel_mountains.py -- give the repetitive margin peaks variation/offset.

Brandon's 2026-09-06 review (optional, lowest priority): paineel's margin
mountains "could use variation/offset". They were four near-identical peaks
on a dead-flat baseline (all y -1388.5), evenly spaced every 260u, matching
widths -- a uniform sawtooth.

This replaces them with a layered range in the SAME inks and footprint: a
back tier of smaller, higher-set peaks and a front tier of larger ones,
each with its own baseline offset, summit height, off-center summit and
asymmetry, non-uniform spacing, and 2-4 shading ticks on the lee face.

Idempotent: strips the existing peak/hatch strokes in the mountain box, then
appends the new range.

    python src/tools/paineel_mountains.py          # apply
    python src/tools/paineel_mountains.py --probe  # report only
"""
import os
import random
import sys

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
P2 = os.path.join(MAPS, "paineel_2.txt")

OUTLINE = (90, 85, 80)
HATCH = (65, 60, 58)
# the original peaks' bounding box (with pad), for the idempotent strip
BOX = (-1010, -1600, 80, -1360)   # x0, y0, x1, y1

# per-peak: (base_x_left, width, height, base_y, summit_frac, seed)
# base_y less negative = lower on the page (front); more negative = set back.
# summit_frac = where along the width the summit sits (0.5 = centered).
PEAKS = [
    # back tier: smaller, set higher (more negative base_y), softer
    dict(x=-980, w=250, h=150, by=-1440, sf=0.62, seed=1, tier="back"),
    dict(x=-505, w=230, h=138, by=-1450, sf=0.38, seed=2, tier="back"),
    dict(x=-150, w=210, h=132, by=-1445, sf=0.55, seed=3, tier="back"),
    # front tier: larger, lower (less negative base_y), overlapping the back
    dict(x=-870, w=300, h=205, by=-1388, sf=0.44, seed=4, tier="front"),
    dict(x=-560, w=270, h=182, by=-1388, sf=0.60, seed=5, tier="front"),
    dict(x=-300, w=320, h=224, by=-1388, sf=0.40, seed=6, tier="front"),
    dict(x=-30,  w=250, h=168, by=-1388, sf=0.52, seed=7, tier="front"),
]


def peak(x0, w, h, by, sf, seed):
    """One jagged massif: rise to an off-center summit over a couple of
    shoulders, then a notch and a lower secondary bump before the descent.
    Returns (outline_segs, hatch_segs)."""
    r = random.Random(seed)
    sx = x0 + w * sf                                  # summit x
    sy = by - h                                       # summit y (up = -)
    # rising side: base -> shoulder -> summit
    shoulder_x = x0 + (sx - x0) * r.uniform(0.42, 0.58)
    shoulder_y = by - h * r.uniform(0.48, 0.62)
    pts = [(x0, by), (shoulder_x, shoulder_y), (sx, sy)]
    # falling side: summit -> notch -> secondary bump -> base
    notch_x = sx + (x0 + w - sx) * r.uniform(0.30, 0.42)
    notch_y = sy + h * r.uniform(0.22, 0.34)
    bump_x = sx + (x0 + w - sx) * r.uniform(0.55, 0.70)
    bump_y = notch_y - h * r.uniform(0.08, 0.20)
    pts += [(notch_x, notch_y), (bump_x, bump_y), (x0 + w, by)]
    out = [(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], OUTLINE)
           for i in range(len(pts) - 1)]
    # shading ticks on the lee (falling) face, parallel short diagonals
    hatch = []
    n = r.randint(2, 4)
    for k in range(n):
        t = 0.20 + 0.5 * k / max(1, n - 1)
        hx = sx + (notch_x - sx) * t
        hy = sy + (notch_y - sy) * t
        hatch.append((hx, hy, hx + w * 0.045, hy + h * 0.055, HATCH))
    return out, hatch


def main():
    probe = "--probe" in sys.argv
    raw = [l for l in open(P2, encoding="utf-8").read().splitlines() if l.strip()]

    x0, y0, x1, y1 = BOX
    kept, stripped = [], 0
    for l in raw:
        if l[:1] == "L":
            b = l[2:].replace(",", " ").split()
            ax, ay, _, bx, by_, _ = map(float, b[:6])
            ink = tuple(map(int, b[6:9]))
            mx, my = (ax + bx) / 2, (ay + by_) / 2
            if ink in (OUTLINE, HATCH) and x0 < mx < x1 and y0 < my < y1:
                stripped += 1
                continue
        kept.append(l)

    new = []
    for pk in PEAKS:
        o, hh = peak(pk["x"], pk["w"], pk["h"], pk["by"], pk["sf"], pk["seed"])
        for s in o + hh:
            new.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                       % (s[0], s[1], s[2], s[3], *s[4]))

    print(f"paineel: stripped {stripped} old peak strokes; adding "
          f"{len(new)} for {len(PEAKS)} varied peaks (3 back + 4 front)")
    if probe:
        return
    open(P2, "w", newline="", encoding="utf-8").write(CRLF.join(kept + new) + CRLF)
    print(f"wrote {P2}: {len(raw)} -> {len(kept) + len(new)} lines")


if __name__ == "__main__":
    main()
