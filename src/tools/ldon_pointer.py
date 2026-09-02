"""ldon_pointer.py -- speculative off-map pointers to Lost Dungeons of Norrath.

EQL is reportedly adding Rujarkian Hills. In retail, LDoN is reached from five
adventure camps, one per zone. Nothing about EQL's implementation is known --
these are GUESSES from retail, and they are drawn to look like guesses: their
own teal ink, a doubled shaft with a hollow head, and a '?' in every label.

    python src/tools/ldon_pointer.py --probe
    python src/tools/ldon_pointer.py
"""
import argparse
import os
import sys

HERE = os.path.dirname(__file__)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "kit"))
from fix_title import content_bbox  # noqa: E402
from layout import layout  # noqa: E402

MAPS = os.environ.get("EQ_MAPS", "Emoda Legends Maps")
CRLF = "\r\n"
LDON = (0, 150, 140)          # teal: used by nothing else in the pack

# zone -> (dungeon, edge, position along that edge as a fraction of the span)
# Retail's five adventure camps. Confidence noted in the commit message.
CAMPS = {
    "sro":       ("Rujarkian_Hills", "w", 0.42),
    "nro":       ("Takish-Hiz", "w", 0.60),
    "innothule": ("Deepest_Guk", "e", 0.45),
    "everfrost": ("Miraguls_Menagerie", "e", 0.38),
    "butcher":   ("Mistmoore_Catacombs", "e", 0.62),
}


def pointer(zone, dungeon, edge, frac):
    """Label + doubled arrow in the margin, pointing off the map."""
    X0, X1, Y0, Y1 = content_bbox(zone)
    lo = layout((X0, X1, Y0, Y1))
    gx0, gx1, gy0, gy1 = lo["grid"]
    mx0, mx1, my0, my1 = lo["margin"]
    S = lo["S"]
    shaft = S * 0.070          # deliberately shorter than the historical arrows
                               # (theirs run ~S*0.078); these are guesses, so they
                               # should sit under the real pointers, not over them
    gap = S * 0.011                      # separation of the two shaft lines
    if edge in ("w", "e"):
        y = gy0 + (gy1 - gy0) * frac
        if edge == "w":
            xl, tip = gx0, gx0 - shaft
        else:
            xl, tip = gx1, gx1 + shaft
        lab = (xl, y + S * 0.017)
        d = -1 if edge == "w" else 1
        segs = []
        for off in (-gap, gap):
            segs.append((xl, y + off, tip, y + off))
        head = shaft * 0.20
        segs += [(tip, y, tip + d * head, y - head * 0.62),
                 (tip, y, tip + d * head, y + head * 0.62),
                 (tip + d * head, y - head * 0.62, tip + d * head, y + head * 0.62)]
    else:
        raise ValueError(edge)
    return lab, segs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", action="store_true")
    args = ap.parse_args()
    for zone, (dungeon, edge, frac) in CAMPS.items():
        if not os.path.exists(os.path.join(MAPS, zone + ".txt")):
            print("%-11s no such map, skipped" % zone)
            continue
        lab, segs = pointer(zone, dungeon, edge, frac)
        name = "To_%s_(LDoN?)" % dungeon
        print("%-11s %-34s label (%8.0f,%8.0f)  %d arrow strokes"
              % (zone, name, lab[0], lab[1], len(segs)))
        if args.probe:
            continue
        p1 = os.path.join(MAPS, zone + "_1.txt")
        out = [l.strip() for l in open(p1, encoding="utf-8") if l.strip()]
        out = [l for l in out if not l.rstrip().endswith(name)]
        out.append("P %.4f, %.4f, 0.0000, %d, %d, %d, 2, %s"
                   % (lab[0], lab[1], LDON[0], LDON[1], LDON[2], name))
        open(p1, "w", newline="", encoding="utf-8").write(CRLF.join(out) + CRLF)
        p2 = os.path.join(MAPS, zone + "_2.txt")
        raw = [l for l in open(p2, encoding="utf-8").read().splitlines() if l.strip()]
        raw = [l for l in raw if not l.endswith("%d, %d, %d" % LDON)]
        raw += ["L %.4f, %.4f, 0.0000, %.4f, %.4f, 0.0000, %d, %d, %d"
                % (a, b, c, d, *LDON) for (a, b, c, d) in segs]
        open(p2, "w", newline="", encoding="utf-8").write(CRLF.join(raw) + CRLF)


if __name__ == "__main__":
    main()
