"""scale_title.py -- shrink a clipped title IN PLACE until it fits the frame.

Doctrine (docs/TITLES.md campaign + stylized-titles rule): a clipped title is
never redrawn in stick font; it is the zone's styled original, scaled about
its own center until it sits inside the frame. Letterforms, inks, spacing all
survive -- only the size changes, and only by the minimum needed.

Selection mirrors eqqms: band = _2 strokes with mid-y above grid_top+40;
letters = band strokes longer than 12u; the title set = band strokes whose
ink appears in the letters and whose midpoint lies inside the letters' bbox
(padded 30u). Everything else in the band -- margin texture, compasses,
sprites -- is untouched.

    python src/tools/scale_title.py <zone> [--pad 25] [--write]
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), "src", "kit"))
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fix_title import content_bbox  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--pad", type=float, default=25.0)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()

    lo = layout(content_bbox(a.zone))
    gy0 = lo["grid"][2]
    fx0, fx1 = lo["frame"][0], lo["frame"][1]

    path = os.path.join(MAPS, a.zone + "_2.txt")
    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines()
             if l.strip()]
    parsed = []
    for l in lines:
        if l[:1] != "L":
            parsed.append(None)
            continue
        f = [v.strip() for v in l[2:].split(",")]
        if len(f) < 9:
            parsed.append(None)
            continue
        parsed.append([float(f[0]), float(f[1]), float(f[2]),
                       float(f[3]), float(f[4]), float(f[5]), f[6], f[7], f[8]])

    band = [i for i, s in enumerate(parsed) if s and (s[1] + s[4]) / 2 < gy0 + 40]
    letters = [i for i in band
               if math.hypot(parsed[i][3] - parsed[i][0], parsed[i][4] - parsed[i][1]) > 12]
    if not letters:
        print("%s: no letters found" % a.zone)
        return
    inks = {(parsed[i][6], parsed[i][7], parsed[i][8]) for i in letters}
    xs = [v for i in letters for v in (parsed[i][0], parsed[i][3])]
    ys = [v for i in letters for v in (parsed[i][1], parsed[i][4])]
    bx0, bx1, by0, by1 = min(xs), max(xs), min(ys), max(ys)
    title = [i for i in band
             if (parsed[i][6], parsed[i][7], parsed[i][8]) in inks
             and bx0 - 30 <= (parsed[i][0] + parsed[i][3]) / 2 <= bx1 + 30
             and by0 - 30 <= (parsed[i][1] + parsed[i][4]) / 2 <= by1 + 30]

    avail = (fx1 - a.pad) - (fx0 + a.pad)
    width = bx1 - bx0
    s = min(1.0, avail / width) if width > 0 else 1.0
    cx = (bx0 + bx1) / 2
    cy = (by0 + by1) / 2
    # recenter so the scaled title also sits inside the frame
    ncx = min(max(cx, fx0 + a.pad + s * width / 2), fx1 - a.pad - s * width / 2)
    if s >= 0.999 and abs(ncx - cx) < 1:
        print("%s: fits already (width %.0f vs %.0f)" % (a.zone, width, avail))
        return

    for i in title:
        p = parsed[i]
        for k in (0, 3):
            p[k] = ncx + (p[k] - cx) * s
        for k in (1, 4):
            p[k] = cy + (p[k] - cy) * s
        lines[i] = ("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %s, %s, %s"
                    % (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8]))

    print("%s: scaled %d strokes by %.3f (width %.0f -> %.0f), recenter %+.0f%s"
          % (a.zone, len(title), s, width, width * s, ncx - cx,
             "  WRITTEN" if a.write else "  (dry run)"))
    if a.write:
        open(path, "w", newline="", encoding="utf-8").write(CRLF.join(lines) + CRLF)


if __name__ == "__main__":
    main()
