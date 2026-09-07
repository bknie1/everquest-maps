"""soltemple_flames.py -- fire and flame motifs for the Temple of Solusek Ro.

Brandon's 2026-09-06 review: soltemple "wants more fire and flame", in warm
arc inks like soldungb's family. Figures come from src/kit/flame_decor.py
(curved flame tongues + tripod braziers, soldungb palette). Placed in eight
verified-clear pockets flanking the temple hall, symmetric left/right, so the
fire lines the approach to the fire-god's sanctum.

Every spot is guarded: the real motif footprint is bbox-tested against every
non-grid stroke in the base map, POIs (_1) and decoration (_2); grid lines
(152,142,120) are background and may be overdrawn. A blocked spot is skipped,
never forced. Idempotent: re-running strips its own flame strokes first.

    python src/tools/soltemple_flames.py          # apply
    python src/tools/soltemple_flames.py --probe  # report only
"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

import flame_decor as FD  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
P2 = os.path.join(MAPS, "soltemple_2.txt")
GRID_INK = (152, 142, 120)
FLAME_INKS = set(FD.PALETTE.values())

# (kind, cx, cy_base, r) -- symmetric flanks of the temple hall, four levels;
# top pair are braziers (temple-entrance anchors), the rest standing flames.
SPOTS = [
    ("flame", -130, -610, 40), ("flame", 134, -610, 40),
    ("flame", -130, -510, 38), ("flame", 134, -510, 38),
    ("flame", -130, -390, 42), ("flame", 134, -390, 42),
    ("flame", -130, -280, 38), ("flame", 134, -280, 38),
]


def load_obstacles():
    segs = []
    for suf in ("", "_1", "_2"):
        p = os.path.join(MAPS, "soltemple" + suf + ".txt")
        if not os.path.exists(p):
            continue
        for l in open(p, encoding="utf-8").read().splitlines():
            if l[:1] != "L":
                continue
            b = l[2:].replace(",", " ").split()
            x1, y1, _, x2, y2, _ = map(float, b[:6])
            ink = tuple(map(int, b[6:9]))
            if ink == GRID_INK or ink in FLAME_INKS:
                continue                       # grid = background; flames = ours
            segs.append((x1, y1, x2, y2))
    return segs


def main():
    probe = "--probe" in sys.argv
    raw = [l for l in open(P2, encoding="utf-8").read().splitlines() if l.strip()]

    # idempotence: drop any previously placed flame strokes
    before = len(raw)
    kept = []
    for l in raw:
        if l[:1] == "L":
            b = l[2:].replace(",", " ").split()
            if tuple(map(int, b[6:9])) in FLAME_INKS:
                continue
        kept.append(l)
    if before - len(kept):
        print(f"soltemple: stripped {before - len(kept)} prior flame strokes")
    raw = kept

    obst = load_obstacles()

    def clear(bx0, by0, bx1, by1):
        return not any(min(x1, x2) < bx1 and max(x1, x2) > bx0 and
                       min(y1, y2) < by1 and max(y1, y2) > by0
                       for x1, y1, x2, y2 in obst)

    new, placed, skipped = [], 0, []
    for kind, cx, cy, r in SPOTS:
        segs = FD.MOTIFS[kind](cx, cy, r)
        xs = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        if not clear(min(xs) - 5, min(ys) - 5, max(xs) + 5, max(ys) + 5):
            skipped.append((kind, cx, cy))
            continue
        for s in segs:
            new.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                       % (s[0], s[1], s[2], s[3], *s[4]))
        placed += 1

    print(f"soltemple: placing {placed}/{len(SPOTS)} motifs ({len(new)} strokes)"
          + (f"; SKIPPED (blocked): {skipped}" if skipped else ""))
    if probe:
        return
    open(P2, "w", newline="", encoding="utf-8").write(CRLF.join(raw + new) + CRLF)
    print(f"wrote {P2}: {before} -> {len(raw) + len(new)} lines")


if __name__ == "__main__":
    main()
