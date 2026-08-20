"""ground_pois.py -- set POI z to the real floor beneath it.

POIs placed with a placeholder z (e.g. -1) can float above the actual dungeon
floor. The in-game "find / take me there" trail paths to the POI's (x,y,z), so a
wrong z can break it. This samples the nearest base geometry under each
placeholder POI and sets its z to that floor height. Zone lines and any POI
that already has a real z are left alone.

    python src/tools/ground_pois.py gukbottom          # apply
    python src/tools/ground_pois.py gukbottom --probe   # show what it would set
"""
import argparse
import math
import os
import sys

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"


def base_samples(zone):
    pts = []
    for l in open(os.path.join(MAPS, zone + ".txt"), encoding="utf-8"):
        if l.startswith("L"):
            f = l[2:].split(",")
            x1, y1, z1, x2, y2, z2 = (float(v) for v in f[:6])
            pts.append((x1, y1, z1))
            pts.append((x2, y2, z2))
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("zone")
    ap.add_argument("--placeholder", type=float, default=2.0,
                    help="treat |z| below this as a placeholder to ground")
    ap.add_argument("--radius", type=float, default=250.0)
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()

    pts = base_samples(args.zone)
    if not pts:
        sys.exit("no base geometry")
    cell = 120.0
    grid = {}
    for p in pts:
        grid.setdefault((int(p[0] // cell), int(p[1] // cell)), []).append(p)

    def floor_z(x, y):
        best, bd = None, args.radius
        gx, gy = int(x // cell), int(y // cell)
        rng = int(args.radius // cell) + 1
        for ix in range(gx - rng, gx + rng + 1):
            for iy in range(gy - rng, gy + rng + 1):
                for (px, py, pz) in grid.get((ix, iy), []):
                    d = math.hypot(px - x, py - y)
                    if d < bd:
                        bd, best = d, pz
        return best

    path = os.path.join(MAPS, args.zone + "_1.txt")
    raw = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    out, changed = [], 0
    for l in raw:
        if l.startswith("P"):
            f = [v.strip() for v in l[2:].split(",")]
            x, y, z = float(f[0]), float(f[1]), float(f[2])
            lbl = ",".join(f[7:])
            if abs(z) < args.placeholder:
                fz = floor_z(x, y)
                if fz is not None:
                    if args.probe:
                        print(f"  {lbl:40s} z {z:.1f} -> {fz:.1f}")
                    else:
                        out.append("P %s, %s, %.4f, %s, %s, %s, %s, %s"
                                   % (f[0], f[1], fz, f[3], f[4], f[5], f[6], lbl))
                        changed += 1
                        continue
        if l.strip():
            out.append(l)
    if not args.probe:
        open(path, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)
    print(f"{args.zone}: grounded {changed} POIs" if not args.probe else f"{args.zone}: probe done")


if __name__ == "__main__":
    main()
