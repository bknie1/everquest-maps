"""rebuild_capture.py -- rebuild a zone's compass WITHOUT losing any motifs.

The lesson from Mistmoore: a from-scratch _2 throws away hand-made motifs (fog
borders, the grid, decoration, water). This does the opposite -- it KEEPS the
entire old _2 and only:

  1. detects the old compass (N/E/S/W letters, or an arrow-glyph cluster) and
     removes it (its short strokes + N/E/S/W point-records),
  2. draws a fresh rose in the emptiest margin corner,
  3. knocks out a soft halo behind the new rose so the border/fog reads clean.

Everything else -- title, grid, fog, decoration, water, frame -- is preserved.
Titles are left alone (they were already cleaned by the _3 arrow sweep).

    python src/tools/rebuild_capture.py najena --probe
    python src/tools/rebuild_capture.py najena
    python src/tools/rebuild_capture.py lfaydark --corner tr
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))

from fix_title import content_bbox, word_segs, parse  # noqa: E402
from fix_compass import find_center, find_cluster_compass  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def L(a, b, c, d, ink):
    return "L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a, b, c, d, *ink)


def rose(cx, cy, r, ink):
    out = []
    ring = [(cx + r * math.cos(t), cy + r * math.sin(t))
            for t in [i * 2 * math.pi / 16 for i in range(17)]]
    for i in range(16):
        out.append(L(*ring[i], *ring[i + 1], ink))
    for k in range(8):
        a = k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.55
        out.append(L(cx, cy, cx + rr * math.cos(a), cy + rr * math.sin(a), ink))
    h = max(24.0, r * 0.38); cw = h * 0.66; gap = h * 0.16
    for lbl, (lx, ly) in [("N", (cx - cw / 2, cy - r - 12)),
                          ("S", (cx - cw / 2, cy + r + 12 + h)),
                          ("E", (cx + r + 12, cy + h * 0.5)),
                          ("W", (cx - r - 12 - cw, cy + h * 0.5))]:
        for (a, b, c, d) in word_segs(lbl, lx, ly, cw, h, gap):
            out.append(L(a, b, c, d, ink))
    return out


def pick_corner(LO, segs, forced=None):
    """Emptiest margin corner (or forced tl/tr/bl/br). Returns (name, cx, cy)."""
    gx0, gx1, gy0, gy1 = LO["grid"]
    mx0, mx1, my0, my1 = LO["margin"]
    corners = {
        "tl": (mx0, gx0, my0, gy0), "tr": (gx1, mx1, my0, gy0),
        "bl": (mx0, gx0, gy1, my1), "br": (gx1, mx1, gy1, my1)}
    def dens(x0, x1, y0, y1):
        return sum(1 for s in segs
                   if x0 <= (s[0] + s[2]) / 2 <= x1 and y0 <= (s[1] + s[3]) / 2 <= y1)
    if forced:
        x0, x1, y0, y1 = corners[forced]
        return forced, (x0 + x1) / 2, (y0 + y1) / 2
    # titles live in the TOP margin, so default to a BOTTOM corner to avoid them
    best, bd = None, 1e18
    for name in ("bl", "br"):
        x0, x1, y0, y1 = corners[name]
        if x1 <= x0 or y1 <= y0:
            continue
        d = dens(x0, x1, y0, y1)
        if d < bd:
            bd, best = d, (name, (x0 + x1) / 2, (y0 + y1) / 2)
    if best is None:                       # degenerate margins -> fall back to any
        for name, (x0, x1, y0, y1) in corners.items():
            if x1 > x0 and y1 > y0:
                return name, (x0 + x1) / 2, (y0 + y1) / 2
    return best[0], best[1], best[2]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--corner", choices=["tl", "tr", "bl", "br"], default=None)
    ap.add_argument("--radius", type=float, default=None)
    ap.add_argument("--ink", default=None, help="r,g,b for the new rose")
    ap.add_argument("--clear-frac", type=float, default=1.4,
                    help="remove old compass short-strokes within this * old radius")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()

    path = os.path.join(MAPS, args.zone + "_2.txt")
    raw = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]

    det = find_center(args.zone, raw)
    mode = "letters"
    if not det:
        det = find_cluster_compass(args.zone, raw)
        mode = "cluster"
    if not det:
        print(f"{args.zone}: NO compass found (no N/E/S/W letters, no glyph cluster) "
              f"-- skip or pass a manual fix")
        return
    ocx, ocy, orad, _ = det
    orad = orad or 80.0

    segs = [parse(l) for l in raw if l.startswith("L")]
    LO = layout(content_bbox(args.zone))
    S = LO["S"]
    r = args.radius or max(55.0, min(orad, 150.0))
    cname, ncx, ncy = pick_corner(LO, segs, args.corner)
    ink = tuple(int(v) for v in args.ink.split(",")) if args.ink else (78, 70, 92)

    if args.probe:
        print(f"{args.zone}: old compass ({ocx:.0f},{ocy:.0f}) r={orad:.0f} mode={mode} "
              f"-> new rose in corner '{cname}' at ({ncx:.0f},{ncy:.0f}) r={r:.0f}")
        return

    # 1) remove old compass: N/E/S/W point-records + short strokes near old center
    keep, dropped = [], 0
    for l in raw:
        if l.startswith("P"):
            f = [v.strip() for v in l[2:].split(",")]
            if ",".join(f[7:]) in ("N", "E", "S", "W") and \
               math.hypot(float(f[0]) - ocx, float(f[1]) - ocy) < orad * 2.4:
                dropped += 1
                continue
        elif l.startswith("L"):
            s = parse(l)
            mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
            length = math.hypot(s[2] - s[0], s[3] - s[1])
            if math.hypot(mx - ocx, my - ocy) < orad * args.clear_frac and length < orad * 1.6:
                dropped += 1
                continue
        keep.append(l)

    # 2) draw the new rose
    new = rose(ncx, ncy, r, ink)

    # 3) knock out a soft halo behind the new rose (clear fog/decoration there)
    hk = r * 1.4
    kept2, knocked = [], 0
    for l in keep:
        if l.startswith("L"):
            s = parse(l)
            mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
            if (mx - ncx) ** 2 + (my - ncy) ** 2 < hk * hk:
                knocked += 1
                continue
        kept2.append(l)

    open(path, "w", newline="", encoding="utf-8").write(CRLF.join(kept2 + new) + CRLF)
    print(f"{args.zone}: removed old compass ({dropped}), knocked halo ({knocked}), "
          f"drew new rose in '{cname}' ({len(new)} strokes); everything else preserved")


if __name__ == "__main__":
    main()
