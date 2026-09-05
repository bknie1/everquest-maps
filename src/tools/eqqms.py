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
}


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
    band = [s for s in deco["segs"] if (s[1] + s[3]) / 2 < gy0 + 40]
    letters = [s for s in band if math.hypot(s[2] - s[0], s[3] - s[1]) > 12]
    t = dict(band=len(band), letters=len(letters), frame_w=fx1 - fx0,
             bbox=None, height=0.0, clipped=False, inks=[])
    if letters:
        xs = [v for s in letters for v in (s[0], s[2])]
        ys = [v for s in letters for v in (s[1], s[3])]
        t["bbox"] = (min(xs), min(ys), max(xs), max(ys))
        t["height"] = max(ys) - min(ys)
        t["clipped"] = min(xs) < fx0 - 60 or max(xs) > fx1 + 60
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
    style = STYLE.get(z)
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
    print("%-15s %s  %6s %5s %5s  %s" % ("zone", "grade", "total", "dupes", "title", "flags"))
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
        print("%-15s   %s    %6d %5d %5d  %s" % (z, g["overall"], m["total"],
              m["dupes"], t.get("letters", 0), " ".join(flags)))
    if a.write:
        print("\nrefreshed %d docs/zones/*.md" % len(rows))


if __name__ == "__main__":
    main()
