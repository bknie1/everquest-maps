"""place_neriak_gate.py -- (re)place the Neriak entrance sketch in Nektulos.

The sketch (dolmen, leaning monoliths, tunnel mouth, Teir'Dal sigil) is defined
in src/zones/neriak_gate.py. This drops it into Nektulos's southwest margin in
the cool dark ink, replacing any previous copy. Idempotent.

    python src/tools/place_neriak_gate.py
"""
import os
import sys

HERE = os.path.dirname(__file__)
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src", "zones"))
from neriak_gate import neriak_gate_segs

INK = (72, 66, 86)
NEK2 = os.path.join(REPO, "Emoda Legends Maps", "nektulos_2.txt")
NEKB = os.path.join(REPO, "Emoda Legends Maps", "nektulos.txt")


def bbox(lines):
    xs, ys = [], []
    for l in lines:
        f = l[2:].split(",")
        xs += [float(f[0]), float(f[3])]
        ys += [float(f[1]), float(f[4])]
    return min(xs), max(xs), min(ys), max(ys)


def main():
    segs = neriak_gate_segs()
    lminx = min(min(s[0], s[2]) for s in segs); lmaxx = max(max(s[0], s[2]) for s in segs)
    lminy = min(min(s[1], s[3]) for s in segs); lmaxy = max(max(s[1], s[3]) for s in segs)

    raw = [l.rstrip("\r\n") for l in open(NEK2, encoding="utf-8", errors="replace") if l.strip()]
    head = [l for l in raw if not l.startswith("L")]
    # keep every non-gate line (drops any prior placement of this ink)
    lines = [l for l in raw if l.startswith("L")
             and tuple(int(float(v)) for v in l[2:].split(",")[6:9]) != INK]
    fx0, fx1, fy0, fy1 = bbox(lines)
    bl = [l.rstrip("\r\n") for l in open(NEKB, encoding="utf-8", errors="replace") if l.startswith("L")]
    bx0, bx1, by0, by1 = bbox(bl)

    # southwest margin band (bottom-left corner), clear of title/compass
    mx0, mx1 = fx0, bx0
    my0, my1 = by1, fy1
    padx = (mx1 - mx0) * 0.10; pady = (my1 - my0) * 0.12
    s = min(((mx1 - mx0) - 2 * padx) / (lmaxx - lminx),
            ((my1 - my0) - 2 * pady) / (lmaxy - lminy))
    cx = (mx0 + mx1) / 2; cy = (my0 + my1) / 2
    nx0 = cx - (lminx + lmaxx) / 2 * s

    def tx(x): return nx0 + x * s
    def ty(y): return cy - (y - (lminy + lmaxy) / 2) * s      # in-game y-up convention

    new = ["L %.2f, %.2f, 0.0000, %.2f, %.2f, 0.0000, %d, %d, %d"
           % (tx(a), ty(b), tx(c), ty(d), *INK) for (a, b, c, d) in segs]
    nxs = [tx(x) for g in segs for x in (g[0], g[2])]
    nys = [ty(y) for g in segs for y in (g[1], g[3])]
    open(NEK2, "w", newline="", encoding="utf-8").write("\r\n".join(head + lines + new) + "\r\n")
    print("Neriak gate placed x[%.0f,%.0f] y[%.0f,%.0f]  (%d lines)"
          % (min(nxs), max(nxs), min(nys), max(nys), len(new)))


if __name__ == "__main__":
    main()
