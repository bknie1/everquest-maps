"""fix_compass.py -- rebuild a zone's compass as a proper rose.

Many zones have a degenerate compass: loose scattered N/E/S/W letters, or just
an up-arrow in a circle, with no ring + rays. This finds the compass (from its
N/E/S/W point-records, or a supplied center) and redraws a clean rose: a
16-segment ring, 8 rays (long cardinals, short intercardinals), and stroke
letters N/E/S/W just outside the ring.

    python src/tools/fix_compass.py butcher                 # auto (uses N/E/S/W P-records)
    python src/tools/fix_compass.py soldunga --center 300,-1200 --radius 90
    python src/tools/fix_compass.py kaladima --ink 90,70,120

The old loose letters (P-records) and stray compass strokes within the rose
footprint are removed. Pass --probe to see what it detects without writing.
"""
import argparse
import collections
import math
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from fix_title import parse, word_segs, content_bbox

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def find_center(zone, raw):
    """Centroid + radius from N/E/S/W point-records, if present."""
    pts = {}
    for l in raw:
        if l.startswith("P"):
            f = [v.strip() for v in l[2:].split(",")]
            lbl = ",".join(f[7:])
            if lbl in ("N", "E", "S", "W"):
                pts[lbl] = (float(f[0]), float(f[1]))
    if len(pts) < 3:
        return None
    cx = sum(p[0] for p in pts.values()) / len(pts)
    cy = sum(p[1] for p in pts.values()) / len(pts)
    r = sum(math.hypot(p[0] - cx, p[1] - cy) for p in pts.values()) / len(pts)
    return cx, cy, r, pts


def find_cluster_compass(zone, raw):
    """Arrow-only compass: a compact isolated glyph sitting in a MARGIN corner.

    Proximity-clusters the deco strokes, then scores compact clusters that live
    outside the content but inside the frame -- the classic 'arrow in a circle'.
    """
    CX0, CX1, CY0, CY1 = content_bbox(zone)
    segs = [parse(l) for l in raw if l.startswith("L")]
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    if not xs:
        return None
    FX0, FX1, FY0, FY1 = min(xs), max(xs), min(ys), max(ys)
    span = max(FX1 - FX0, FY1 - FY0)
    thr = span * 0.02
    # union-find over endpoint proximity (grid-bucketed)
    cell = thr
    parent = {}
    def find(a):
        while parent.get(a, a) != a:
            parent[a] = parent.get(parent[a], parent[a]); a = parent[a]
        return a
    def union(a, b):
        parent.setdefault(a, a); parent.setdefault(b, b)
        parent[find(a)] = find(b)
    def key(x, y):
        return (round(x / cell), round(y / cell))
    for i, s in enumerate(segs):
        parent.setdefault(i, i)
        for (px, py) in ((s[0], s[1]), (s[2], s[3])):
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    parent.setdefault(("g", key(px, py)[0] + dx, key(px, py)[1] + dy),
                                      ("g", key(px, py)[0] + dx, key(px, py)[1] + dy))
            union(i, ("g",) + key(px, py))
    comps = collections.defaultdict(list)
    for i in range(len(segs)):
        comps[find(i)].append(i)
    best, best_score = None, -1
    for members in comps.values():
        if not (6 <= len(members) <= 90):
            continue
        cx2 = [v for i in members for v in (segs[i][0], segs[i][2])]
        cy2 = [v for i in members for v in (segs[i][1], segs[i][3])]
        w, h = max(cx2) - min(cx2), max(cy2) - min(cy2)
        d = max(w, h)
        if not (span * 0.03 < d < span * 0.14) or min(w, h) < d * 0.55:
            continue
        cx, cy = (min(cx2) + max(cx2)) / 2, (min(cy2) + max(cy2)) / 2
        in_margin = not (CX0 < cx < CX1 and CY0 < cy < CY1)
        near_frame = min(cx - FX0, FX1 - cx, cy - FY0, FY1 - cy) < span * 0.03
        if not in_margin or near_frame:
            continue
        score = (1.0 / (1 + abs(w - h))) + len(members) * 0.001
        if score > best_score:
            best_score, best = score, (cx, cy, d / 2, None)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--center", help="x,y (override auto-detect)")
    ap.add_argument("--radius", type=float, default=None)
    ap.add_argument("--ink", default=None, help="r,g,b (default: dark slate)")
    ap.add_argument("--clear-frac", type=float, default=0.6,
                    help="remove old compass strokes within this * radius of center; "
                         "keep LOW in dense margins (city zones) to spare decoration")
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()

    path = os.path.join(MAPS, args.zone + "_2.txt")
    raw = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]

    mode = "manual"
    if args.center:
        cx, cy = (float(v) for v in args.center.split(","))
        r = args.radius or 80.0
    else:
        det = find_center(args.zone, raw)
        mode = "letters"
        if not det:
            det = find_cluster_compass(args.zone, raw)
            mode = "cluster"
        if not det:
            sys.exit("no compass found (no N/E/S/W letters, no glyph cluster); pass --center x,y --radius r")
        cx, cy, rdet, _extra = det
        r = args.radius or max(55.0, min(rdet, 150.0))
    # cluster (arrow-only) glyphs are isolated in a sparse margin -> clear the old
    # glyph fully; letter/manual modes stay conservative to spare decoration
    clear = args.clear_frac if mode != "cluster" else max(args.clear_frac, 1.3)

    ink = tuple(int(v) for v in args.ink.split(",")) if args.ink else (78, 70, 92)
    CX0, CX1, CY0, CY1 = content_bbox(args.zone)
    in_margin = not (CX0 < cx < CX1 and CY0 < cy < CY1)

    if args.probe:
        print(f"{args.zone}: center ({cx:.0f},{cy:.0f}) r={r:.0f} "
              f"{'margin' if in_margin else 'INSIDE content'} mode={mode} clear={clear}")
        return

    # remove old compass: the N/E/S/W point letters + compass-ish strokes near center
    keep, dropped = [], 0
    for l in raw:
        if l.startswith("P"):
            f = [v.strip() for v in l[2:].split(",")]
            if ",".join(f[7:]) in ("N", "E", "S", "W") and math.hypot(float(f[0]) - cx, float(f[1]) - cy) < r * 2.2:
                dropped += 1
                continue
        elif l.startswith("L"):
            s = parse(l)
            mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
            length = math.hypot(s[2] - s[0], s[3] - s[1])
            near = math.hypot(mx - cx, my - cy) < r * clear
            # only strip short strokes near center; if the compass is inside the
            # content, be conservative (short strokes only) to spare map geometry
            if near and length < r * 1.6:
                dropped += 1
                continue
        keep.append(l)

    out = []

    def add(a, b, c, d):
        out.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a, b, c, d, *ink))

    ring = [(cx + r * math.cos(t), cy + r * math.sin(t)) for t in [i * 2 * math.pi / 16 for i in range(17)]]
    for i in range(16):
        add(*ring[i], *ring[i + 1])
    for k in range(8):
        a = k * math.pi / 4
        rr = r if k % 2 == 0 else r * 0.55
        add(cx, cy, cx + rr * math.cos(a), cy + rr * math.sin(a))
    h = max(24.0, r * 0.38)
    cw = h * 0.66
    gap = h * 0.16
    for lbl, (lx, ly) in [("N", (cx - cw / 2, cy - r - 12)),
                          ("S", (cx - cw / 2, cy + r + 12 + h)),
                          ("E", (cx + r + 12, cy + h * 0.5)),
                          ("W", (cx - r - 12 - cw, cy + h * 0.5))]:
        for (a, b, c, d) in word_segs(lbl, lx, ly, cw, h, gap):
            add(a, b, c, d)

    open(path, "w", newline="", encoding="utf-8").write(CRLF.join(keep + out) + CRLF)
    print(f"{args.zone}: rebuilt compass at ({cx:.0f},{cy:.0f}) r={r:.0f}; "
          f"removed {dropped}, drew {len(out)} strokes")


if __name__ == "__main__":
    main()
