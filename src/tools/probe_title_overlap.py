"""Diagnostic: what sits in each zone's TITLE BAND, per layer.

The title band is decoration space above the content. Anything from the base or
the _3 (EQOA historical) layer that lands there is an artifact overlapping the
title. This reports, per zone, how many strokes/points each layer puts in the
band, so we can tell a _3-overlap (tiny fix) from a broken-_2 (rebuild).
"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "kit"))
from fix_title import content_bbox
from layout import layout

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")


def band_hits(zone):
    b = content_bbox(zone)
    lo = layout(b)
    bx0, bx1, byt, byb = lo["title_band"]
    # widen band to grid width and up to the frame so we catch anything over title
    fx0, fx1, fy0, fy1 = lo["frame"]
    def inband(x, y):
        return bx0 <= x <= bx1 and fy0 <= y <= byb
    res = {}
    for suf in ("", "_3"):
        p = os.path.join(MAPS, zone + suf + ".txt")
        if not os.path.exists(p):
            res[suf or "base"] = None
            continue
        n = 0
        for l in open(p, encoding="utf-8"):
            if l[:1] == "L":
                f = l[2:].split(",")
                mx = (float(f[0]) + float(f[3])) / 2
                my = (float(f[1]) + float(f[4])) / 2
                if inband(mx, my):
                    n += 1
            elif l[:1] == "P":
                f = l[2:].split(",")
                if inband(float(f[0]), float(f[1])):
                    n += 1
        res[suf or "base"] = n
    return res, (round(byt), round(byb))


if __name__ == "__main__":
    zones = sys.argv[1:] or [
        "akanon", "beholder", "befallen", "cauldron", "cazicthule", "eastkarana",
        "erudnext", "erudsxing", "feerrott", "innothule", "lavastorm", "nektulos",
        "qcat", "qey2hh1", "qeynos2", "qeytoqrg", "southkarana", "sro", "stonebrunt",
        "misty", "everfrost", "oasis", "nro"]
    print(f"{'zone':14s} {'base':>6s} {'_3':>6s}   title-band y")
    for z in zones:
        try:
            r, band = band_hits(z)
            flag = "  <-- _3 overlaps title" if (r.get("_3") or 0) > 0 else ""
            print(f"{z:14s} {str(r.get('base')):>6s} {str(r.get('_3')):>6s}   {band}{flag}")
        except Exception as e:
            print(f"{z:14s} ERROR {e}")
