"""eqqms.py -- EverQuest Quantitative Metrics: the atlas standards meter.

One command that measures every zone against the written standard and grades
it, so "needs a pass" is a number before it is an opinion:

    python src/tools/eqqms.py                 # scorecard for all zones
    python src/tools/eqqms.py qeynos halas    # just these
    python src/tools/eqqms.py --write         # also refresh docs/zones/*.md

Categories (each graded A-F, worst grade wins the headline):
  format   CRLF endings, parseable records, no blank-ink strokes
  budget   total strokes across all layers vs the 31k asset cap
  title    band present, letters legible-sized, inside the frame, not clipped
  dupes    exact duplicate strokes (free wins dedupe.py would reclaim)
  palette  ink discipline: distinct inks vs the pack norm, luminance range

The docs/zones/<zone>.md refresh preserves the hand-written "## Notes"
section verbatim; only the measured block above it is regenerated.
"""
import argparse
import collections
import glob
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src", "kit"))

from fix_title import parse, content_bbox  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.path.join(ROOT, "Emoda Legends Maps")
DOCS = os.path.join(ROOT, "docs", "zones")
BUDGET = 31000
LUM = lambda i: 0.299 * i[0] + 0.587 * i[1] + 0.114 * i[2]

# title-clipped exemptions, each verified by band plot 2026-09-05: the
# letters sit INSIDE the frame; the flag came from band decor the letter
# detector cannot separate (neriak trio: diagonal ribbon shading + corner
# hatch flourishes at letter-like sizes; felwitheb: title shares canopy ink
# and its stick letters split into disconnected strokes). ALL 15 clipped
# flags that day proved false -- measure overhanging strokes by ink/length
# before ever scaling a title. See docs/zones/<zone>.md.
NOCLIP = {"neriaka", "neriakb", "neriakc", "felwitheb"}

# the title style each zone carries, kept current by the campaign
STYLE = {
    "freporte": "extruded two-tier", "freportw": "extruded two-tier",
    "freportn": "extruded two-tier", "freeportsewers": "extruded (grime)",
    "qeynos": "stately", "qeynos2": "stately", "qcat": "stately (dark)",
    "erudnext": "refined", "erudnint": "refined",
    "halas": "runic", "grobb": "crude (troll)", "oggok": "crude (ogre)",
    "neriaka": "darkelf", "neriakb": "darkelf", "neriakc": "darkelf",
    "felwithea": "highelf", "felwitheb": "highelf",
    "rivervale": "rounded", "akanon": "clockwork", "qrg": "sylvan",
    "paineel": "3d-wireframe (restored)", "kerraridge": "3d-wireframe (restored)",
    "tox": "3d-wireframe (restored)",
    # exemplars named by docs/TITLES.md -- styled long before the city slate
    "unrest": "exemplar (the bar)", "soldungb": "exemplar (warm arc)",
    "najena": "exemplar (hatched cartouche)",
    "kaladima": "exemplar (chisel-cut)", "kaladimb": "exemplar (chisel-cut)",
}

# locked zones: never candidates for a style pass regardless of measurement
STYLE_LOCKED = {"unrest", "eastkarana"}

# the deprecated homogenized family's ink (docs/TITLES.md)
PALE = (120, 105, 85)


def declared_style(z):
    """The zone doc's recorded style class -- the source of truth per
    docs/TITLES.md. Automatic classification was tried and measured
    unreliable (the letter picker's recall varies wildly by style family),
    so verdicts come from a human looking at the map; the meter only keeps
    score. Returns None when the doc has no (or an 'unreviewed') class."""
    path = os.path.join(DOCS, z + ".md")
    if not os.path.exists(path):
        return None
    mm = re.search(r"\*\*Title style:\*\* (.+)", open(path, encoding="utf-8").read())
    if not mm:
        return None
    s = mm.group(1).strip()
    return None if s.lower().startswith("unreviewed") else s


def style_hint(band, lidx):
    """Cheap measured hint for prioritizing unreviewed zones: a single
    dominant ink near the deprecated pale family is a strong tell."""
    if not lidx:
        return ""
    inks = collections.Counter(band[i][4] for i in lidx)
    (top, n), total = inks.most_common(1)[0], sum(inks.values())
    if n / total >= 0.9 and sum(abs(a - b) for a, b in zip(top, PALE)) <= 45:
        return " (measured: pale?)"
    return ""


def compass_census(z, segs):
    """Count compass roses in the _2 layer: ring-shaped closed components
    (8-48 segments, radius 30-200, low radius variance) that either carry
    spokes through their center or sit by N/E/S/W point-records. Born from a
    real day: rivervale shipped two stacked compasses and crushbone had a
    leftover mini-rose; the meter now counts. Report-only -- webs and round
    ponds can masquerade, the human adjudicates. Returns (count, centers)."""
    import collections as _c
    idx = [i for i, s in enumerate(segs)
           if 6 <= math.hypot(s[2] - s[0], s[3] - s[1]) <= 120]
    parent = {i: i for i in idx}

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    pts = {}
    for i in idx:
        s = segs[i]
        for p in ((round(s[0] * 2) / 2, round(s[1] * 2) / 2),
                  (round(s[2] * 2) / 2, round(s[3] * 2) / 2)):
            if p in pts:
                a, b = find(pts[p]), find(i)
                if a != b:
                    parent[a] = b
            else:
                pts[p] = i
    comps = _c.defaultdict(list)
    for i in idx:
        comps[find(i)].append(i)

    nesw = []
    p2 = os.path.join(MAPS, z + "_2.txt")
    if os.path.exists(p2):
        for l in open(p2, encoding="utf-8", errors="ignore"):
            if l[:1] == "P" and l.strip()[-1:] in "NESW" and l.strip()[-2:-1] in ", ":
                f = [v.strip() for v in l[1:].lstrip().split(",")]
                try:
                    nesw.append((float(f[0]), float(f[1])))
                except ValueError:
                    pass

    # component stats once: centroid + bbox, reused for cardinal-letter test
    stats = []
    for c in comps.values():
        pts = [p for i in c for p in ((segs[i][0], segs[i][1]),
                                      (segs[i][2], segs[i][3]))]
        xs = [p[0] for p in pts]
        ys = [p[1] for p in pts]
        stats.append((c, sum(xs) / len(xs), sum(ys) / len(ys),
                      max(xs) - min(xs), max(ys) - min(ys), pts))

    # rose radius scales with the map: a dungeon's rose is r~30, feerrott's
    # r~150. Gate relative to the deco layer's extent.
    ext_x = [v for s in segs for v in (s[0], s[2])]
    W = (max(ext_x) - min(ext_x)) if ext_x else 0
    rmin, rmax = max(24, 0.012 * W), max(230, 0.10 * W)

    roses = []
    for c, cx, cy, w, h, pts in stats:
        if not 10 <= len(c) <= 90:
            continue
        rs = sorted(math.hypot(x - cx, y - cy) for x, y in pts)
        R = rs[int(len(rs) * 0.9)]
        if not rmin <= R <= rmax:
            continue
        rim = [(x, y) for x, y in pts if 0.8 * R <= math.hypot(x - cx, y - cy) <= 1.2 * R]
        if len(rim) < 10:
            continue
        angs = sorted(math.atan2(y - cy, x - cx) for x, y in rim)
        gaps = [b - a for a, b in zip(angs, angs[1:])]
        gaps.append(angs[0] + 2 * math.pi - angs[-1])
        if 2 * math.pi - max(gaps) < math.radians(300):
            continue                       # arc, not a ring
        # confirmation: N/E/S/W point-records, or small letter components
        # sitting in the annulus just outside the rim
        marked = any(math.hypot(px - cx, py - cy) < 2.0 * R for px, py in nesw)
        if not marked:
            card = 0
            for c2, x2, y2, w2, h2, _ in stats:
                if c2 is c or not (2 <= len(c2) <= 9):
                    continue
                # cardinal letters keep a near-absolute size on small roses
                if not (8 <= h2 <= 60 and w2 <= 70):
                    continue
                if 0.9 * R <= math.hypot(x2 - cx, y2 - cy) <= R + 90:
                    card += 1
            marked = card >= 2
        if marked:
            roses.append((cx, cy, R))
    # a lone NESW P-set with no detected ring still marks a compass
    if nesw and not any(any(math.hypot(px - r[0], py - r[1]) < 2.5 * r[2]
                            for r in roses) for px, py in nesw):
        gx = sum(p[0] for p in nesw) / len(nesw)
        gy = sum(p[1] for p in nesw) / len(nesw)
        roses.append((gx, gy, 0.0))
    # a rose is one-of-a-kind; decor circles come in families. Any group of
    # 3+ candidates sharing a radius (+-20%) is trees/gears/webs -- drop it.
    keep = []
    for r in roses:
        family = [o for o in roses if 0.8 * r[2] <= o[2] <= 1.25 * r[2]]
        if len(family) < 3:
            keep.append(r)
    # concentric circles and welded sub-rings of one rose read as several
    # detections: merge roses whose centers sit within each other's reach
    merged = []
    for r in sorted(keep, key=lambda r: -r[2]):
        if not any(math.hypot(r[0] - m[0], r[1] - m[1]) < 1.8 * max(r[2], m[2], 40)
                   for m in merged):
            merged.append(r)
    return len(merged), merged


def read_layer(z, suffix):
    path = os.path.join(MAPS, z + suffix + ".txt")
    if not os.path.exists(path):
        return None
    raw = open(path, "rb").read()
    text = raw.decode("utf-8", "replace")
    lines = [l for l in text.splitlines() if l.strip()]
    segs, keys, pois, bad = [], [], 0, 0
    for l in lines:
        if l[:1] == "L":
            try:
                f = l[1:].lstrip().split(",")
                segs.append(parse(l))
                keys.append(tuple(round(float(v), 1) for v in f[:6])
                            + tuple(int(float(v)) for v in f[6:9]))
            except Exception:
                bad += 1
        elif l[:1] == "P":
            pois += 1
        else:
            bad += 1
    crlf_ok = b"\r\n" in raw or not lines
    return dict(segs=segs, keys=keys, pois=pois, bad=bad, crlf=crlf_ok)


def measure(z):
    layers = {sfx: read_layer(z, sfx) for sfx in ("", "_1", "_2", "_3")}
    layers = {k: v for k, v in layers.items() if v}
    total = sum(len(v["segs"]) for v in layers.values())
    pois = sum(v["pois"] for v in layers.values())
    bad = sum(v["bad"] for v in layers.values())
    crlf = all(v["crlf"] for v in layers.values())

    dupes = 0
    for v in layers.values():
        seen = set()
        for key in v["keys"]:
            if key in seen:
                dupes += 1
            seen.add(key)

    inks = collections.Counter()
    for v in layers.values():
        for s in v["segs"]:
            inks[s[4]] += 1

    m = dict(zone=z, total=total, pois=pois, bad=bad, crlf=crlf, dupes=dupes,
             n_inks=len(inks), layers={k or "base": len(v["segs"]) for k, v in layers.items()},
             title=None)
    try:
        lo = layout(content_bbox(z))
        gy0 = lo["grid"][2]
        fx0, fx1 = lo["frame"][0], lo["frame"][1]
    except Exception:
        return m
    deco = layers.get("_2")
    if not deco:
        return m
    try:
        m["compasses"] = compass_census(z, deco["segs"])[0]
    except Exception:
        m["compasses"] = None
    band = [s for s in deco["segs"] if (s[1] + s[3]) / 2 < gy0 + 40]
    letters = [s for s in band if math.hypot(s[2] - s[0], s[3] - s[1]) > 12]
    t = dict(band=len(band), letters=len(letters), frame_w=fx1 - fx0,
             bbox=None, height=0.0, clipped=False, inks=[])
    if letters:
        xs = [v for s in letters for v in (s[0], s[2])]
        ys = [v for s in letters for v in (s[1], s[3])]
        t["bbox"] = (min(xs), min(ys), max(xs), max(ys))
        t["height"] = max(ys) - min(ys)
        # clip is measured on LETTER COMPONENTS, not the raw len>12 bbox --
        # border ornaments, ridge sketches and banner zigzags in the band
        # share inks and lengths with letters and stretched the old bbox
        # past the frame on eleven innocent zones (2026-09-05).
        try:
            from scale_title import pick_letters
            lidx = pick_letters(z, band)
            if lidx:
                lxs = [v for i in lidx for v in (band[i][0], band[i][2])]
                t["clipped"] = (min(lxs) < fx0 - 60 or max(lxs) > fx1 + 60) \
                    and z not in NOCLIP
            if z in STYLE:
                t["style"] = STYLE[z]
            elif z in STYLE_LOCKED:
                t["style"] = "locked"
            else:
                t["style"] = declared_style(z) or \
                    "unreviewed" + style_hint(band, lidx)
        except Exception:
            t["clipped"] = (min(xs) < fx0 - 60 or max(xs) > fx1 + 60) \
                and z not in NOCLIP
            t["style"] = STYLE.get(z)
        cnt = collections.Counter(s[4] for s in letters)
        t["inks"] = cnt.most_common(4)
    m["title"] = t
    return m


def grade(m):
    g = {}
    g["format"] = "A" if (m["crlf"] and m["bad"] == 0) else ("C" if m["bad"] < 5 else "F")
    r = m["total"] / BUDGET
    g["budget"] = "A" if r <= 1.0 else ("B" if r <= 1.15 else ("C" if r <= 1.5 else "D" if r <= 2 else "F"))
    t = m["title"]
    if not t or not t["band"]:
        g["title"] = "F"
    elif t["letters"] < 8:
        g["title"] = "D"
    elif t["clipped"]:
        g["title"] = "C"
    elif t.get("style") and ("plain" in t["style"].lower()
                             or "pale" in t["style"].lower()
                             and "measured" not in t["style"]):
        g["title"] = "B"        # declared plain/pale: a restyle candidate
    else:
        g["title"] = "A"
    dr = m["dupes"] / max(m["total"], 1)
    g["dupes"] = "A" if dr < 0.01 else ("B" if dr < 0.03 else ("C" if dr < 0.08 else "D"))
    g["palette"] = "A" if m["n_inks"] <= 90 else ("B" if m["n_inks"] <= 140 else "C")
    order = "FDCBA"
    g["overall"] = min(g.values(), key=order.index)
    return g


HEAD_RE = re.compile(r"^## Notes\s*$", re.M)


def write_doc(m, g):
    z = m["zone"]
    path = os.path.join(DOCS, z + ".md")
    notes = "(none yet)"
    old_title_line = ""
    if os.path.exists(path):
        old = open(path, encoding="utf-8").read()
        parts = HEAD_RE.split(old, maxsplit=1)
        if len(parts) == 2:
            notes = parts[1].strip() or notes
        mm = re.search(r"\*\*Title:\*\* (.+)", old)
        if mm:
            old_title_line = mm.group(1)
    t = m["title"] or {}
    style = t.get("style") or STYLE.get(z)
    lines = ["# %s" % z, ""]
    if old_title_line:
        lines.append("**Title:** %s" % old_title_line)
    if style:
        lines.append("**Title style:** %s" % style)
    if t.get("bbox"):
        bb = t["bbox"]
        lines += ["**Title bbox:** x[%.0f,%.0f] y[%.0f,%.0f] (h %.0f)"
                  % (bb[0], bb[2], bb[1], bb[3], t["height"]),
                  "**Title inks:** " + ", ".join("%s x%d" % (i, n) for i, n in t["inks"])]
    lines += ["**Frame width:** %.0f" % t.get("frame_w", 0) if t else "",
              "**Layers:** " + ", ".join("%s=%d" % kv for kv in sorted(m["layers"].items())),
              "**Total strokes:** %d (budget %d) | POIs %d | dupes %d | inks %d"
              % (m["total"], BUDGET, m["pois"], m["dupes"], m["n_inks"]),
              "**eqqms:** overall %s (format %s, budget %s, title %s, dupes %s, palette %s)"
              % (g["overall"], g["format"], g["budget"], g["title"], g["dupes"], g["palette"]),
              "", "## Notes", "", notes, ""]
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(l for l in lines if l is not None))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zones", nargs="*")
    ap.add_argument("--write", action="store_true", help="refresh docs/zones/*.md")
    a = ap.parse_args()
    zones = a.zones or sorted(
        os.path.basename(p)[:-4] for p in glob.glob(os.path.join(MAPS, "*.txt"))
        if "_" not in os.path.basename(p)[:-4])
    rows = []
    for z in zones:
        m = measure(z)
        g = grade(m)
        rows.append((z, m, g))
        if a.write:
            write_doc(m, g)
    order = "FDCBA"
    rows.sort(key=lambda r: (order.index(r[2]["overall"]), r[1]["total"]))
    print("%-15s %s  %6s %5s %5s  %-18s %s"
          % ("zone", "grade", "total", "dupes", "title", "style", "flags"))
    for z, m, g in rows:
        t = m["title"] or {}
        flags = []
        if m["total"] > BUDGET:
            flags.append("over-budget")
        if t.get("clipped"):
            flags.append("title-clipped")
        if not m["crlf"]:
            flags.append("no-CRLF")
        if m["bad"]:
            flags.append("%d bad lines" % m["bad"])
        nc = m.get("compasses")
        if nc is not None and nc != 1:
            flags.append("compass:%d" % nc)
        print("%-15s   %s    %6d %5d %5d  %-18s %s"
              % (z, g["overall"], m["total"], m["dupes"], t.get("letters", 0),
                 (t.get("style") or "?")[:18], " ".join(flags)))
    if a.write:
        print("\nrefreshed %d docs/zones/*.md" % len(rows))


if __name__ == "__main__":
    main()
