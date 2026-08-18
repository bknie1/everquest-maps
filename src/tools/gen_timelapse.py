"""gen_timelapse.py -- render a per-commit flip-book of every zone's evolution.

For each zone it walks the commits that touched that zone's map files (oldest
first), renders a small PNG of the map as it stood at each commit, and writes
them to src/design/timelapse/<zone>/NNNN.png plus a timelapse-index.json the
player (timelapse.html) reads.

Framing is fixed to the zone's CURRENT extent so the map fills in place instead
of jumping around. Frames are small and palette-reduced to stay cheap.

    python src/tools/gen_timelapse.py            # all zones
    python src/tools/gen_timelapse.py unrest      # just one (for testing)

Requires: pillow.
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(__file__)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
FOLDER = "Emoda Legends Maps"
OUT = os.path.join(REPO, "src", "design", "timelapse")
WIDTH = 380
PARCHMENT = (232, 217, 185)
SUFFIXES = [("0", ""), ("1", "_1"), ("2", "_2"), ("3", "_3")]


def git(args, binary=False):
    r = subprocess.run(["git"] + args, cwd=REPO, capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")


def zone_paths(zone):
    """Layer files that currently exist for a zone."""
    out = []
    for _k, suf in SUFFIXES:
        p = os.path.join(REPO, FOLDER, f"{zone}{suf}.txt")
        if os.path.isfile(p) and os.path.getsize(p) > 0:
            out.append(f"{FOLDER}/{zone}{suf}.txt")
    return out


def discover_zones():
    zones = set()
    for f in os.listdir(os.path.join(REPO, FOLDER)):
        if not f.endswith(".txt"):
            continue
        base = f[:-4]
        for suf in ("_1", "_2", "_3"):
            if base.endswith(suf):
                base = base[:-2]
                break
        zones.add(base)
    return sorted(zones)


def commits_for(paths):
    out = git(["log", "--reverse", "--format=%H|%ct|%s", "--"] + paths)
    if not out:
        return []
    rows = []
    for line in out.splitlines():
        if "|" not in line:
            continue
        sha, ts, msg = line.split("|", 2)
        rows.append((sha, int(ts), msg))
    return rows


def file_at(sha, path):
    return git(["show", f"{sha}:{path}"], binary=True)


def parse(text):
    lines, points = [], []
    for raw in text.splitlines():
        t = raw.strip()
        if not t:
            continue
        if t[0] == "L":
            p = t[1:].split(",")
            if len(p) >= 9:
                try:
                    lines.append((float(p[0]), float(p[1]), float(p[3]), float(p[4]),
                                  (int(float(p[6])), int(float(p[7])), int(float(p[8])))))
                except ValueError:
                    pass
        elif t[0] == "P":
            p = t[1:].split(",")
            if len(p) >= 8:
                try:
                    points.append((float(p[0]), float(p[1]),
                                   (int(float(p[3])), int(float(p[4])), int(float(p[5])))))
                except ValueError:
                    pass
    return lines, points


def current_bounds(zone):
    xs, ys = [], []
    for _k, suf in SUFFIXES:
        p = os.path.join(REPO, FOLDER, f"{zone}{suf}.txt")
        if not os.path.isfile(p):
            continue
        ln, pt = parse(open(p, encoding="utf-8", errors="replace").read())
        for x1, y1, x2, y2, _c in ln:
            xs += [x1, x2]; ys += [y1, y2]
        for x, y, _c in pt:
            xs.append(x); ys.append(y)
    if not xs:
        return None
    return min(xs), max(xs), min(ys), max(ys)


def render(frame_layers, bounds, width=WIDTH):
    minx, maxx, miny, maxy = bounds
    spanx, spany = max(maxx - minx, 1e-6), max(maxy - miny, 1e-6)
    pad = 0.03
    W = width
    scale = (W * (1 - 2 * pad)) / spanx
    H = int(spany * scale + W * 2 * pad)
    img = Image.new("RGB", (W, max(H, 8)), PARCHMENT)
    d = ImageDraw.Draw(img)

    def tx(x):
        return (x - minx) * scale + W * pad

    def ty(y):
        return (y - miny) * scale + W * pad

    for ln, pt in frame_layers:
        for x1, y1, x2, y2, c in ln:
            d.line((tx(x1), ty(y1), tx(x2), ty(y2)), fill=c, width=1)
        for x, y, c in pt:
            cx, cy = tx(x), ty(y)
            d.ellipse((cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5), fill=c)
    return img.convert("P", palette=Image.ADAPTIVE, colors=96)


def main():
    zones = sys.argv[1:] or discover_zones()
    os.makedirs(OUT, exist_ok=True)
    index_path = os.path.join(REPO, "timelapse-index.json")
    index = {}
    if os.path.isfile(index_path):
        try:
            index = json.load(open(index_path, encoding="utf-8")).get("zones", {})
        except Exception:
            index = {}
    total_frames = 0
    for zone in zones:
        paths = zone_paths(zone)
        if not paths:
            continue
        bounds = current_bounds(zone)
        if not bounds:
            continue
        commits = commits_for(paths)
        if not commits:
            continue
        zdir = os.path.join(OUT, zone)
        os.makedirs(zdir, exist_ok=True)
        # clear stale frames
        for f in os.listdir(zdir):
            if f.endswith(".png"):
                os.remove(os.path.join(zdir, f))
        meta = []
        i = 0
        for sha, ts, msg in commits:
            frame_layers = []
            for _k, suf in SUFFIXES:
                blob = file_at(sha, f"{FOLDER}/{zone}{suf}.txt")
                if blob is None:
                    continue
                frame_layers.append(parse(blob.decode("utf-8", "replace")))
            if not frame_layers:
                continue
            i += 1
            img = render(frame_layers, bounds)
            img.save(os.path.join(zdir, f"{i:04d}.png"), optimize=True)
            meta.append({"sha": sha[:7], "date": ts, "msg": msg[:80]})
        index[zone] = {"frames": i, "commits": meta}
        total_frames += i
        print(f"  {zone}: {i} frames")
    json.dump({"width": WIDTH, "zones": index},
              open(index_path, "w", newline="\n", encoding="utf-8"), separators=(",", ":"))
    kb = 0
    for root, _dirs, fs in os.walk(OUT):
        for f in fs:
            kb += os.path.getsize(os.path.join(root, f))
    print(f"{len(index)} zones, {total_frames} frames, {kb/1024/1024:.1f} MB on disk")


if __name__ == "__main__":
    main()
