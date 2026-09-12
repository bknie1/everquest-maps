"""restd_compass.py -- rebuild a zone's rose at the STANDARD size.

The viewer fits a zone to the screen by its longer side, so a rose drawn at
a fixed number of map units reads tiny on a continent and huge in a closet.
Standard (2026-09-12 sweep, from Brandon's "everfrost is the standard"):
ring radius 24px when the map is fitted to a 900px viewport:

    R = px * max(frame_w, frame_h) / 900

Letters scale with the ring (h = clamp(0.75 R, 0.38 R, 24)) so a dungeon
rose no longer wears 24-unit letters (the soltemple giant-letter bug).
eqqms.py's `rose` column reports the same pixel figure and flags 14-40px.

    python src/tools/restd_compass.py <zone> [--px 24] [--ink r,g,b]
        [--center x,y] [--old-r R] [--reach 3.0] [--old-inks r,g,b ...]
        [--knock r,g,b ...] [--knock-pad 1.15] [--write]

--ink       ink of the rose to REMOVE and redraw (default 78,70,92, the ink
            fix_compass.py draws in; use the zone's own rose ink otherwise)
--center    rose center; default = centroid of the --ink strokes
--old-r     old ring radius (default: from the --ink strokes' extent)
--reach     delete --ink strokes within reach*old_r of the center (lower it
            when the rose ink is also decor nearby, e.g. rivervale 1.8)
--old-inks  extra inks whose strokes within 1.3*max(old_r,R) are old-rose
            fragments (arrows, arcs, shared-ink rings)
--knock     background inks (boulders, canopy) to clear from the new rose's
            footprint -- removed as WHOLE polygons welded at exact endpoints,
            because a cut hexagon reads as damage and a missing one as a
            clearing
NESW P-records within 2.5*max(old_r,R) are removed; stroke letters replace
them. Always dry-run first, then render the corner and look.
"""
import argparse
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
for p in (HERE, os.path.join(ROOT, "src", "kit")):
    sys.path.insert(0, p)
from fix_title import content_bbox, word_segs  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", os.path.join(ROOT, "Emoda Legends Maps"))
CRLF = "\r\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--px", type=float, default=24.0)
    ap.add_argument("--ink", default="78,70,92")
    ap.add_argument("--center")
    ap.add_argument("--old-r", type=float)
    ap.add_argument("--old-inks", nargs="*", default=[])
    ap.add_argument("--knock", nargs="*", default=[])
    ap.add_argument("--knock-pad", type=float, default=1.15)
    ap.add_argument("--reach", type=float, default=3.0)
    ap.add_argument("--write", action="store_true")
    a = ap.parse_args()
    z = a.zone
    ink = tuple(int(v) for v in a.ink.split(","))
    old_inks = {tuple(int(v) for v in t.split(",")) for t in a.old_inks}
    knock = {tuple(int(v) for v in t.split(",")) for t in a.knock}

    lo = layout(content_bbox(z))
    fw = lo["frame"][1] - lo["frame"][0]
    fh = lo["frame"][3] - lo["frame"][2]
    R = a.px * max(fw, fh) / 900.0

    path = os.path.join(MAPS, z + "_2.txt")
    lines = [l for l in open(path, encoding="utf-8", errors="ignore").read().splitlines() if l.strip()]
    segs = []
    for i, l in enumerate(lines):
        if l[:1] == "L":
            f = [v.strip() for v in l[1:].lstrip().split(",")]
            segs.append((i, float(f[0]), float(f[1]), float(f[3]), float(f[4]),
                         (int(float(f[6])), int(float(f[7])), int(float(f[8])))))
    rose = [s for s in segs if s[5] == ink]
    if a.center:
        cx, cy = (float(v) for v in a.center.split(","))
    else:
        if not rose:
            sys.exit("no strokes of ink %s; pass --center" % (ink,))
        pts = [(s[1], s[2]) for s in rose] + [(s[3], s[4]) for s in rose]
        cx = sum(p[0] for p in pts) / len(pts)
        cy = sum(p[1] for p in pts) / len(pts)
    if a.old_r:
        old_r = a.old_r
    elif rose:
        old_r = max(math.hypot(s[1] - cx, s[2] - cy) for s in rose) / 1.6
    else:
        old_r = R
    reach = 1.3 * max(old_r, R)

    drop = set()
    for s in rose:
        if math.hypot((s[1] + s[3]) / 2 - cx, (s[2] + s[4]) / 2 - cy) <= a.reach * old_r:
            drop.add(s[0])
    for s in segs:
        if s[5] in old_inks and math.hypot((s[1] + s[3]) / 2 - cx, (s[2] + s[4]) / 2 - cy) <= reach:
            drop.add(s[0])
    h = max(min(24.0, 0.75 * R), 0.38 * R)
    foot = R + 12 + h * 1.1          # letters sit at R+12 .. R+12+h
    nk = 0
    if knock:
        ks = [s for s in segs if s[5] in knock]
        parent = {s[0]: s[0] for s in ks}

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        bypt = {}
        for s in ks:
            for p in ((round(s[1], 1), round(s[2], 1)), (round(s[3], 1), round(s[4], 1))):
                if p in bypt:
                    ra, rb = find(bypt[p]), find(s[0])
                    if ra != rb:
                        parent[ra] = rb
                else:
                    bypt[p] = s[0]
        hit = set()
        for s in ks:
            d = min(math.hypot(s[1] - cx, s[2] - cy), math.hypot(s[3] - cx, s[4] - cy),
                    math.hypot((s[1] + s[3]) / 2 - cx, (s[2] + s[4]) / 2 - cy))
            if d <= foot * a.knock_pad:
                hit.add(find(s[0]))
        for s in ks:
            if find(s[0]) in hit:
                drop.add(s[0])
                nk += 1
    np_ = 0
    keep = []
    for i, l in enumerate(lines):
        if i in drop:
            continue
        if l[:1] == "P":
            f = [v.strip() for v in l[1:].lstrip().split(",")]
            if len(f) >= 8 and f[-1] in ("N", "E", "S", "W") and \
               math.hypot(float(f[0]) - cx, float(f[1]) - cy) < 2.5 * max(old_r, R):
                np_ += 1
                continue
        keep.append(l)

    out = []

    def add(a_, b, c, d):
        out.append("L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d" % (a_, b, c, d, *ink))

    ring = [(cx + R * math.cos(t), cy + R * math.sin(t)) for t in [i * 2 * math.pi / 16 for i in range(17)]]
    for i in range(16):
        add(*ring[i], *ring[i + 1])
    for k in range(8):
        ang = k * math.pi / 4
        rr = R if k % 2 == 0 else R * 0.55
        add(cx, cy, cx + rr * math.cos(ang), cy + rr * math.sin(ang))
    cw, gap = h * 0.66, h * 0.16
    for lbl, (lx, ly) in [("N", (cx - cw / 2, cy - R - 12)),
                          ("S", (cx - cw / 2, cy + R + 12 + h)),
                          ("E", (cx + R + 12, cy + h * 0.5)),
                          ("W", (cx - R - 12 - cw, cy + h * 0.5))]:
        for (p, q, r_, s_) in word_segs(lbl, lx, ly, cw, h, gap):
            add(p, q, r_, s_)
    print("%s: center (%.0f,%.0f) old R~%.0f -> new R %.0f (%.0fpx@fit), letters h %.0f; "
          "removed %d rose/old strokes + %d knocked + %d P-letters; drew %d%s"
          % (z, cx, cy, old_r, R, a.px, h, len(drop) - nk, nk, np_, len(out),
             "  WRITTEN" if a.write else "  (dry run)"))
    if a.write:
        open(path, "w", newline="", encoding="utf-8").write(CRLF.join(keep + out) + CRLF)


if __name__ == "__main__":
    main()
