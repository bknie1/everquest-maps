"""flame_decor.py -- fire and flame motifs for the Solusek Ro family.

Warm arc inks from soldungb's palette family: dark flame body, a bright
inner tongue, ember sparks. Hand-drawn curved tongues built from short
polyline arcs -- fewer, longer, stylized lines per the 2026-08-15 directive,
never tick fields.

Every shape returns [(x1, y1, x2, y2, ink)] in map coordinates.
fn(cx, cy, r, seed=0): (cx, cy) = base center, r = flame height.
"""
import math
import random

PALETTE = {
    'flame':  (158, 62, 28),      # dark outer tongue (soldungb family)
    'bright': (198, 92, 40),      # inner tongue
    'ember':  (164, 66, 32),      # sparks / ember bed
    'iron':   (92, 60, 44),       # brazier metal
}


def _tongue(cx, cy, h, w, lean, ink, rnd, n=5):
    """One curved flame tongue: base -> bulge -> tapered tip, as two arcs."""
    out = []
    # rising edge: bows outward, then leans to the tip
    px, py = cx - w * 0.5, cy
    for k in range(1, n + 1):
        t = k / n
        bow = math.sin(t * math.pi) * w * 0.55
        x = cx - w * 0.5 + bow * -1 + (lean * h * 0.5 + w * 0.5) * t \
            + rnd.uniform(-w, w) * 0.06
        y = cy - h * t
        out.append((px, py, x, y, ink))
        px, py = x, y
    tipx, tipy = px, py
    # falling edge back to the base
    px, py = cx + w * 0.5, cy
    for k in range(1, n + 1):
        t = k / n
        bow = math.sin(t * math.pi) * w * 0.55
        x = cx + w * 0.5 + bow + (lean * h * 0.5 - w * 0.5) * t \
            + rnd.uniform(-w, w) * 0.06
        y = cy - h * t * 0.96
        out.append((px, py, x, y, ink))
        px, py = x, y
    out.append((px, py, tipx, tipy, ink))
    return out


def flame(cx, cy, r, seed=0):
    """A standing fire: three curved tongues (center tall and bright inside),
    an ember bed arc at the base, two sparks drifting up."""
    rnd = random.Random(seed)
    out = []
    out += _tongue(cx - r * 0.30, cy, r * 0.55, r * 0.22, -0.25,
                   PALETTE['flame'], rnd)
    out += _tongue(cx + r * 0.28, cy, r * 0.60, r * 0.22, 0.30,
                   PALETTE['flame'], rnd)
    out += _tongue(cx, cy, r, r * 0.30, rnd.uniform(-0.12, 0.12),
                   PALETTE['flame'], rnd)
    out += _tongue(cx, cy, r * 0.55, r * 0.15, rnd.uniform(-0.08, 0.08),
                   PALETTE['bright'], rnd, n=4)
    # ember bed: shallow arc under the tongues
    px = cx - r * 0.45
    pyy = cy + r * 0.02
    for k in range(1, 5):
        t = k / 4
        x = cx - r * 0.45 + r * 0.9 * t
        y = cy + r * 0.02 + math.sin(t * math.pi) * r * 0.06
        out.append((px, pyy, x, y, PALETTE['ember']))
        px, pyy = x, y
    # sparks
    for k in range(2):
        sx = cx + rnd.uniform(-r * 0.5, r * 0.5)
        sy = cy - r * (1.02 + 0.12 * k)
        out.append((sx, sy, sx + rnd.uniform(-1, 1) * r * 0.05,
                    sy - r * 0.07, PALETTE['ember']))
    return out


def brazier(cx, cy, r, seed=0):
    """A tripod fire bowl with a flame burning in it. (cx, cy) = ground."""
    rnd = random.Random(seed)
    out = []
    bw = r * 0.55
    by = cy - r * 0.45                       # bowl rim height
    # bowl: shallow open trapezoid + rim line
    bowl = [(cx - bw, by), (cx - bw * 0.62, by + r * 0.28),
            (cx + bw * 0.62, by + r * 0.28), (cx + bw, by)]
    for a, b in zip(bowl, bowl[1:]):
        out.append((a[0], a[1], b[0], b[1], PALETTE['iron']))
    out.append((cx - bw, by, cx + bw, by, PALETTE['iron']))
    out.append((cx - bw * 0.8, by + r * 0.12, cx + bw * 0.8, by + r * 0.12,
                PALETTE['iron']))
    # tripod legs, splayed
    out.append((cx - bw * 0.55, by + r * 0.28, cx - bw * 0.85, cy, PALETTE['iron']))
    out.append((cx + bw * 0.55, by + r * 0.28, cx + bw * 0.85, cy, PALETTE['iron']))
    out.append((cx, by + r * 0.28, cx, cy, PALETTE['iron']))
    # the fire itself, seated at the rim
    out += flame(cx, by, r * 0.85, seed=seed + 1)
    return out


MOTIFS = {'flame': flame, 'brazier': brazier}
