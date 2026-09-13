"""border_check.py -- pack-wide border-completeness scanner.

Born 2026-09-13: Brandon caught that Feerrott's fixed outer border still had
a second (inner) border ring that had ALWAYS been incomplete -- it just used
to be hidden under dense margin canopy. That was found by hand; this tool
makes the check automatic and repeatable, and would have caught Oggok's
three genuine gaps (~270/270/91 units on the bottom edge) before shipping.

Method: for every zone's _2 layer, find inks that are DEDICATED to the
perimeter (most of their strokes sit within ~2% of the deco bbox of some
edge, on at least 3 of the 4 sides) and drawn as a short, consistent dash/
zigzag rhythm (not a solid line, not thousands of strokes -- that's margin
canopy/grass fill, which has naturally irregular tree-spacing and is
excluded). For each such ink, walk its strokes along each edge and measure
ENDPOINT-to-endpoint distance, not midpoint spacing -- a zigzag's long teeth
make midpoint spacing look broken even when perfectly connected, which is
exactly how the first pass at fixing Feerrott's outer border still left a
gap (it used an approximate vertex instead of the exact surviving one). A
real gap is an endpoint jump far past the local dash pitch.

    python src/tools/border_check.py                 # scan every zone
    python src/tools/border_check.py feerrott oggok   # just these

This flags CANDIDATES -- always isolate the flagged ink and look at it
before trusting a finding (see isolate_ink in this file, or just eyeball
the render). It cannot see borders drawn as a few long continuous strokes
(no dash rhythm to measure), so a clean report is not a guarantee, only
the absence of this specific, previously-real failure mode.
"""
import argparse
import glob
import os
from collections import defaultdict

MAPS = os.environ.get("EQ_MAPS", os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "Emoda Legends Maps"))


def load(path):
    segs = []
    if not os.path.exists(path):
        return segs
    for l in open(path, encoding="utf-8", errors="ignore"):
        if l[:1] != "L":
            continue
        f = [v.strip() for v in l[1:].lstrip().split(",")]
        if len(f) < 9:
            continue
        try:
            segs.append((float(f[0]), float(f[1]), float(f[3]), float(f[4]),
                         (int(float(f[6])), int(float(f[7])), int(float(f[8])))))
        except ValueError:
            pass
    return segs


def dist(a, b):
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5


def edge_of(s, x0, x1, y0, y1):
    mx, my = (s[0] + s[2]) / 2, (s[1] + s[3]) / 2
    d = {"TOP": abs(my - y0), "BOTTOM": abs(my - y1), "LEFT": abs(mx - x0), "RIGHT": abs(mx - x1)}
    return min(d, key=d.get), min(d.values())


def scan_zone(zone):
    segs = load(os.path.join(MAPS, zone + "_2.txt"))
    if not segs:
        return None
    xs = [v for s in segs for v in (s[0], s[2])]
    ys = [v for s in segs for v in (s[1], s[3])]
    x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    edge_tol = max(30.0, max(x1 - x0, y1 - y0) * 0.02)

    by_ink = defaultdict(list)
    for s in segs:
        by_ink[s[4]].append(s)

    findings = []
    for ink, strokes in by_ink.items():
        if len(strokes) < 15 or len(strokes) > 1500:
            continue  # a real thin border line is never thousands of strokes
        near_edge = defaultdict(list)
        near_total = 0
        for s in strokes:
            e, d = edge_of(s, x0, x1, y0, y1)
            if d < edge_tol:
                near_edge[e].append(s)
                near_total += 1
        # a genuine border ink is DEDICATED to the perimeter, not scattered
        # as general fill (margin canopy/grass reused the same green ink)
        if near_total < 0.6 * len(strokes):
            continue
        sides_present = [e for e in ("TOP", "BOTTOM", "LEFT", "RIGHT") if len(near_edge[e]) >= 10]
        if len(sides_present) < 3:
            continue

        for e in sides_present:
            axis = 0 if e in ("TOP", "BOTTOM") else 1
            ss_sorted = sorted(near_edge[e], key=lambda s: (s[0] + s[2]) / 2 if axis == 0 else (s[1] + s[3]) / 2)
            pitches, gaps, prev_end = [], [], None
            for i, s in enumerate(ss_sorted):
                p1, p2 = (s[0], s[1]), (s[2], s[3])
                if prev_end is not None:
                    d1, d2 = dist(p1, prev_end), dist(p2, prev_end)
                    near, far = (p1, p2) if d1 < d2 else (p2, p1)
                    gap = min(d1, d2)
                    if i > 1:  # skip the corner-adjacent first comparison (benign false read)
                        pitches.append(gap)
                    if gap > 15:
                        gaps.append((gap, prev_end, near))
                    prev_end = far
                else:
                    prev_end = p2
            if len(pitches) < 6:
                continue  # not enough of a rhythm to trust
            pitches.sort()
            med_pitch = pitches[len(pitches) // 2]
            if med_pitch < 3 or med_pitch > 120:
                continue  # not a short dash rhythm
            consistent = sum(1 for p in pitches if p <= med_pitch * 2.2)
            if consistent / len(pitches) < 0.6:
                continue
            thresh = max(80.0, med_pitch * 5)
            real_gaps = [g for g in gaps if g[0] > thresh]
            if real_gaps:
                findings.append((ink, e, len(strokes), med_pitch, real_gaps))
    return dict(zone=zone, findings=findings)


def isolate_ink(zone, ink, out_png):
    """Render one ink's strokes alone (black on white) -- the fastest way to
    tell a real broken border from a false-positive fill/decoration cluster."""
    from PIL import Image, ImageDraw
    segs = load(os.path.join(MAPS, zone + "_2.txt"))
    m = [s for s in segs if s[4] == ink]
    if not m:
        return 0
    xs = [v for s in m for v in (s[0], s[2])]
    ys = [v for s in m for v in (s[1], s[3])]
    x0, x1, y0, y1 = min(xs) - 20, max(xs) + 20, min(ys) - 20, max(ys) + 20
    sc = min(1600 / (x1 - x0), 1600 / (y1 - y0))
    im = Image.new("RGB", (int((x1 - x0) * sc) + 1, int((y1 - y0) * sc) + 1), (250, 250, 250))
    d = ImageDraw.Draw(im)
    for s in m:
        d.line([((s[0] - x0) * sc, (s[1] - y0) * sc), ((s[2] - x0) * sc, (s[3] - y0) * sc)], fill=(0, 0, 0), width=2)
    im.save(out_png)
    return len(m)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zones", nargs="*")
    a = ap.parse_args()
    zones = a.zones or sorted(os.path.basename(p)[:-4] for p in glob.glob(os.path.join(MAPS, "*.txt"))
                               if "_" not in os.path.basename(p)[:-4])
    hits = 0
    for z in zones:
        r = scan_zone(z)
        if not r or not r["findings"]:
            continue
        hits += 1
        print("--- %s ---" % z)
        for ink, edge, n, pitch, gaps in r["findings"]:
            print("  ink %s on %s (%d strokes, pitch~%.1f): %d gap(s)" % (ink, edge, n, pitch, len(gaps)))
            for g, pa, pb in gaps:
                print("    gap %.0f  from (%.0f,%.0f) to (%.0f,%.0f)" % (g, pa[0], pa[1], pb[0], pb[1]))
    print("\n%d / %d zones flagged -- isolate_ink() each candidate before trusting it." % (hits, len(zones)))


if __name__ == "__main__":
    main()
