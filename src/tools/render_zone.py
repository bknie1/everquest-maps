#!/usr/bin/env python3
"""Render Emoda map files to PNG for preview.

Composites a zone's layers (base, _1, _2, _3) onto parchment, the way the
client draws them: L segments as lines, P records as dots with labels.

Usage:
    python render_zone.py                        # render every zone
    python render_zone.py newsebexp halas        # just these zones
    python render_zone.py --maps "path" --out "path"
    python render_zone.py --layers 02            # base + deco only
    python render_zone.py --width 1600           # output width in px

Requires: pillow  (python -m pip install pillow)
"""
import argparse
import os
import re
import sys

from PIL import Image, ImageDraw, ImageFont

PARCHMENT = (232, 217, 185)
DEFAULT_MAPS = os.path.join(os.path.dirname(__file__), "..", "..", "Emoda Legends Maps")
DEFAULT_OUT = os.path.join(os.path.dirname(__file__), "..", "..", "renders")
SUPERSAMPLE = 2  # draw at 2x then downscale for antialiasing


def parse_file(path):
    """Return (lines, points). lines: (x1,y1,x2,y2,(r,g,b)); points: (x,y,(r,g,b),size,label)."""
    lines, points = [], []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for raw in f:
            raw = raw.strip()
            if not raw or raw[0] not in "LP":
                continue
            parts = [p.strip() for p in raw[1:].split(",")]
            try:
                if raw[0] == "L" and len(parts) >= 9:
                    x1, y1, _, x2, y2, _ = (float(v) for v in parts[:6])
                    rgb = tuple(int(float(v)) for v in parts[6:9])
                    lines.append((x1, y1, x2, y2, rgb))
                elif raw[0] == "P" and len(parts) >= 8:
                    x, y, _ = (float(v) for v in parts[:3])
                    rgb = tuple(int(float(v)) for v in parts[3:6])
                    size = int(float(parts[6]))
                    label = ",".join(parts[7:]).replace("_", " ").strip()
                    points.append((x, y, rgb, size, label))
            except ValueError:
                continue
    return lines, points


def zone_layers(maps_dir, zone):
    out = []
    for suffix in ("", "_1", "_2", "_3"):
        p = os.path.join(maps_dir, zone + suffix + ".txt")
        if os.path.isfile(p):
            out.append((suffix or "0", p))
    return out


def render(zone, maps_dir, out_dir, layers="0123", width=1400, label_points=True):
    files = [(s, p) for s, p in zone_layers(maps_dir, zone)
             if (s if s != "0" else "0")[-1] in layers]
    if not files:
        return None
    all_lines, all_points = [], []
    for _, path in files:
        ln, pt = parse_file(path)
        all_lines += ln
        all_points += pt
    if not all_lines and not all_points:
        return None

    # Bounds come from LINE geometry only: a single mis-set or off-map POI would
    # otherwise stretch the canvas and shrink the whole map (misty's Dread Corpses
    # marker sits legitimately outside the drawn base geometry).
    xs = [v for l in all_lines for v in (l[0], l[2])] or [p[0] for p in all_points]
    ys = [v for l in all_lines for v in (l[1], l[3])] or [p[1] for p in all_points]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    spanx, spany = max(maxx - minx, 1e-6), max(maxy - miny, 1e-6)

    pad = 0.02
    W = width * SUPERSAMPLE
    scale = (W * (1 - 2 * pad)) / spanx
    H = int(spany * scale + W * 2 * pad)

    def tx(x):
        return (x - minx) * scale + W * pad

    def ty(y):
        return (y - miny) * scale + W * pad

    img = Image.new("RGB", (W, H), PARCHMENT)
    draw = ImageDraw.Draw(img)
    lw = max(1, round(SUPERSAMPLE * width / 1400))
    for x1, y1, x2, y2, rgb in all_lines:
        draw.line((tx(x1), ty(y1), tx(x2), ty(y2)), fill=rgb, width=lw)

    if all_points:
        try:
            font = ImageFont.truetype("arial.ttf", 11 * SUPERSAMPLE)
        except OSError:
            font = ImageFont.load_default()
        r = 3 * SUPERSAMPLE
        for x, y, rgb, size, label in all_points:
            cx, cy = tx(x), ty(y)
            draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=rgb)
            if label_points and label:
                draw.text((cx + r + 2, cy - r - 2), label, fill=rgb, font=font)

    img = img.resize((W // SUPERSAMPLE, H // SUPERSAMPLE), Image.LANCZOS)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, zone + ".png")
    img.save(out_path)
    return out_path


def discover_zones(maps_dir):
    zones = set()
    for name in os.listdir(maps_dir):
        m = re.match(r"^(.*?)(?:_[123])?\.txt$", name)
        if m:
            zones.add(m.group(1))
    return sorted(zones)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("zones", nargs="*", help="zone short names; default = all")
    ap.add_argument("--maps", default=DEFAULT_MAPS)
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--layers", default="0123", help="which layers to composite, e.g. 012")
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--no-labels", action="store_true")
    args = ap.parse_args()

    maps_dir = os.path.abspath(args.maps)
    zones = args.zones or discover_zones(maps_dir)
    ok = 0
    for z in zones:
        try:
            path = render(z, maps_dir, args.out, args.layers, args.width,
                          label_points=not args.no_labels)
        except Exception as e:
            print(f"  FAIL {z}: {e}", file=sys.stderr)
            continue
        if path:
            ok += 1
            print(f"  {z} -> {path}")
        else:
            print(f"  skip {z} (no drawable records)")
    print(f"{ok}/{len(zones)} zones rendered")


if __name__ == "__main__":
    main()
