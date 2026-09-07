"""gukbottom_frogloks.py -- undead froglok sketches for Lower Guk margins.

Brandon's 2026-09-06 review: gukbottom wants undead froglok sketches. The
figure is fauna_sil.froglok_skeleton (bare bones of the race + a rusty
trident, never armored -- the skeleton style law). The margins are a dense
dash-hatch, so zone_pass's append-only path would stamp figures INTO the
texture; this runner clears a padded knockout box in the hatch behind each
figure first (the guktop bald-spot rule in reverse: a deliberate clearing,
not a scar).

Idempotent: re-running strips its own bone/rust strokes inside the figure
boxes and re-stamps.

    python src/tools/gukbottom_frogloks.py          # apply
    python src/tools/gukbottom_frogloks.py --probe  # report only
"""
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fauna_sil import froglok_skeleton  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
P2 = os.path.join(MAPS, "gukbottom_2.txt")

# margin dash-hatch ink families (probed 2026-09-06)
HATCH = {(52, 64, 46), (62, 72, 56), (82, 92, 74), (54, 94, 66),
         (64, 82, 56), (78, 120, 88), (132, 150, 120)}
# inks the figure itself uses (for the idempotence strip)
FIG = {(182, 176, 158), (96, 90, 78), (128, 96, 70), (40, 36, 30)}

H = 100                    # figure height in map units
PAD = 34                   # clearing pad around the figure bbox

# (cx, cy_feet, face) -- margins: left x~-935, right x~1394, bottom y~400;
# clear of the title band (top), the big bottom-left compass (y -30..350 on
# the left flank) and every exit label
SPOTS = [
    (-935, -1450, 1), (-935, -600, 1),
    (1394, -1200, -1), (1394, -300, -1),
    (-100, 445, 1), (700, 445, -1),
]


def parse(l):
    b = l[2:].replace(",", " ").split()
    x1, y1, _, x2, y2, _ = map(float, b[:6])
    return x1, y1, x2, y2, tuple(map(int, b[6:9]))


def main():
    probe = "--probe" in sys.argv
    raw = [l for l in open(P2, encoding="utf-8").read().splitlines() if l.strip()]

    figs, boxes, new = [], [], []
    for i, (cx, cy, face) in enumerate(SPOTS):
        segs = froglok_skeleton(cx, cy, H, seed=i, face=face)
        xs = [v for s in segs for v in (s[0], s[2])]
        ys = [v for s in segs for v in (s[1], s[3])]
        boxes.append((min(xs) - PAD, min(ys) - PAD, max(xs) + PAD, max(ys) + PAD))
        for s in segs:
            new.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                       % (s[0], s[1], s[2], s[3], *s[4]))

    def boxed(x, y):
        return any(x0 < x < x1 and y0 < y < y1 for x0, y0, x1, y1 in boxes)

    kill_old = kill_hatch = 0
    keep = []
    for l in raw:
        if l[:1] == "L":
            x1, y1, x2, y2, ink = parse(l)
            # a dash counts as inside if either end or its middle lands in a box
            inside = (boxed((x1 + x2) / 2, (y1 + y2) / 2) or boxed(x1, y1)
                      or boxed(x2, y2))
            if ink in FIG and inside:
                kill_old += 1
                continue
            if ink in HATCH and inside:
                kill_hatch += 1
                continue
        keep.append(l)

    print(f"gukbottom: {len(SPOTS)} froglok skeletons ({len(new)} strokes); "
          f"clearing {kill_hatch} hatch strokes"
          + (f"; replacing {kill_old} prior figure strokes" if kill_old else ""))
    if probe:
        return
    open(P2, "w", newline="", encoding="utf-8").write(CRLF.join(keep + new) + CRLF)
    print(f"wrote {P2}: {len(raw)} -> {len(keep) + len(new)} lines")


if __name__ == "__main__":
    main()
