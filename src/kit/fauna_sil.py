"""fauna_sil.py -- THE definitive race figures for map margins. Silhouette-first.

Why this module exists: hatched-wireframe figures (fauna_hd_*) turn into furry
blobs at map scale -- Brandon read the dark elves as gnolls. What survives map
scale is SILHOUETTE + POSTURE + one signature accent, exactly like the Najena
banner. So every figure here is built from a few SOLID-FILLED polygons with a
clean outline and one or two accents. Style reference: the classic Keith
Parkinson EverQuest box art -- strong silhouettes, flowing robes, signature gear.

Contract (same for every figure):
    fn(cx, cy, s, seed=0, face=-1) -> [(x1,y1,x2,y2,(r,g,b)), ...]
    (cx, cy) = ground point between the feet.  s = full height in map units.
    face=-1 looks left (default), face=1 looks right.  seed is accepted for API
    compatibility; silhouettes are deterministic.

Use the SIL registry:  from fauna_sil import SIL;  SIL['dark_elf'](x, y, s)
Aliases cover wiki words: skeleton/zombie/ghoul -> hooded_undead, human -> guard.

Rules of the style (KEEP THESE or figures degrade):
  * 3-6 solid polygons per figure, no interior hatching except fills
  * upright races stand UPRIGHT (hunched posture reads as gnoll/beast)
  * one exaggerated racial marker: elf ear spike, dwarf beard sheet, ogre belly,
    iksar tail, halfling bare feet, gnome goggles...
  * palette from fauna.PALETTE families; accents pale so they pop on parchment
"""
import math


def _solid(poly, ink, step):
    """Fill a polygon with tight horizontal runs -- reads as solid mass."""
    ys = [p[1] for p in poly]
    out = []
    y = min(ys)
    while y < max(ys):
        xs = []
        for i in range(len(poly)):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % len(poly)]
            if (y1 > y) != (y2 > y):
                xs.append(x1 + (y - y1) * (x2 - x1) / (y2 - y1))
        xs.sort()
        for i in range(0, len(xs) - 1, 2):
            if xs[i + 1] - xs[i] > 0.4:
                out.append((xs[i], y, xs[i + 1], y, ink))
        y += step
    return out


def _edge(poly, ink, out):
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        out.append((a[0], a[1], b[0], b[1], ink))


class _F:
    """Tiny helper: builds P()/L()/poly() in figure space (y up, face flip)."""
    def __init__(self, cx, cy, s, face):
        self.cx, self.cy, self.s, self.f = cx, cy, s, face
        self.out = []
        self.step = max(0.6, s * 0.012)          # fill pitch scales with size

    def P(self, pts):
        return [(self.cx + self.f * x * self.s, self.cy - y * self.s) for x, y in pts]

    def L(self, x1, y1, x2, y2, c):
        self.out.append((self.cx + self.f * x1 * self.s, self.cy - y1 * self.s,
                         self.cx + self.f * x2 * self.s, self.cy - y2 * self.s, c))

    def poly(self, pts, fill, line=None, pitch=1.0):
        pp = self.P(pts)
        self.out += _solid(pp, fill, self.step * pitch)
        _edge(pp, line or fill, self.out)

    def disc(self, x, y, r, fill, n=12):
        pts = [(x + r * math.cos(t * 2 * math.pi / n),
                y + r * 0.9 * math.sin(t * 2 * math.pi / n)) for t in range(n)]
        self.poly(pts, fill)


# ------------------------------------------------------------------ elves
def dark_elf(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    VIOLET = (72, 58, 96); DEEP = (52, 42, 72); SKIN = (96, 84, 120)
    HAIR = (200, 196, 210); STEEL = (165, 165, 175)
    F.poly([(-0.045, 0.80), (-0.14, 0.76), (-0.16, 0.66), (-0.13, 0.55),
            (-0.16, 0.40), (-0.20, 0.20), (-0.22, 0.02),
            (0.15, 0.02), (0.12, 0.22), (0.095, 0.44), (0.12, 0.60),
            (0.10, 0.73), (0.045, 0.79)], VIOLET, DEEP)
    F.poly([(-0.035, 0.815), (-0.135, 0.845), (-0.155, 0.885), (-0.125, 0.935),
            (-0.06, 0.955), (-0.005, 0.93), (0.005, 0.86), (-0.005, 0.815)], SKIN, DEEP)
    F.poly([(-0.015, 0.90), (0.115, 0.965), (0.005, 0.865)], SKIN, DEEP)      # ear
    F.poly([(-0.09, 0.955), (-0.02, 0.975), (0.035, 0.94), (0.075, 0.86),
            (0.10, 0.70), (0.115, 0.52), (0.075, 0.52), (0.05, 0.70),
            (0.015, 0.84), (-0.045, 0.925)], HAIR, (168, 164, 184), pitch=1.2)
    F.L(-0.10, 0.905, -0.135, 0.897, DEEP)
    F.poly([(-0.13, 0.68), (-0.20, 0.62), (-0.235, 0.545), (-0.205, 0.525),
            (-0.165, 0.585), (-0.10, 0.635)], VIOLET, DEEP)                    # arm
    F.L(-0.225, 0.53, -0.27, 0.60, STEEL); F.L(-0.27, 0.60, -0.315, 0.72, STEEL)
    F.L(-0.315, 0.72, -0.335, 0.83, STEEL); F.L(-0.335, 0.83, -0.325, 0.845, STEEL)
    F.L(-0.205, 0.505, -0.245, 0.555, DEEP)
    return F.out


def high_elf(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    ROBE = (170, 168, 178); TRIM = (168, 138, 70); SKIN = (196, 180, 160)
    HAIR = (198, 172, 104); DEEP = (120, 118, 130)
    F.poly([(-0.04, 0.80), (-0.13, 0.76), (-0.145, 0.64), (-0.12, 0.52),
            (-0.15, 0.34), (-0.185, 0.02), (0.14, 0.02), (0.11, 0.30),
            (0.09, 0.52), (0.11, 0.68), (0.05, 0.79)], ROBE, DEEP)
    F.L(-0.185, 0.02, 0.14, 0.02, TRIM)                                       # gold hem
    F.L(-0.12, 0.52, 0.09, 0.53, TRIM)                                        # gold sash
    F.poly([(-0.03, 0.815), (-0.12, 0.845), (-0.14, 0.89), (-0.11, 0.94),
            (-0.045, 0.955), (0.005, 0.925), (0.01, 0.855), (0.0, 0.815)], SKIN, DEEP)
    F.poly([(-0.005, 0.90), (0.115, 0.955), (0.01, 0.862)], SKIN, DEEP)       # ear
    F.poly([(-0.08, 0.955), (0.0, 0.972), (0.05, 0.93), (0.085, 0.80),
            (0.10, 0.62), (0.065, 0.62), (0.04, 0.79), (-0.03, 0.925)], HAIR, TRIM, pitch=1.2)
    F.L(-0.095, 0.905, -0.125, 0.898, DEEP)
    # tall staff with orb, held vertical before the figure
    F.L(-0.20, 0.06, -0.20, 0.98, TRIM)
    F.disc(-0.20, 1.03, 0.045, (150, 180, 200))
    F.poly([(-0.12, 0.66), (-0.185, 0.60), (-0.21, 0.55), (-0.185, 0.53),
            (-0.15, 0.58), (-0.095, 0.62)], ROBE, DEEP)                       # arm to staff
    return F.out


def wood_elf(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    TUNIC = (70, 105, 60); DEEP = (48, 76, 44); SKIN = (172, 140, 108)
    HAIR = (140, 92, 50); WOODC = (110, 84, 52)
    # half-crouch archer: bent legs
    F.poly([(-0.10, 0.42), (0.02, 0.44), (0.10, 0.38), (0.16, 0.20), (0.10, 0.02),
            (0.02, 0.02), (0.06, 0.20), (-0.02, 0.30), (-0.12, 0.24),
            (-0.16, 0.02), (-0.24, 0.02), (-0.20, 0.26), (-0.14, 0.38)], TUNIC, DEEP)
    F.poly([(-0.10, 0.42), (-0.16, 0.52), (-0.14, 0.66), (-0.05, 0.72),
            (0.06, 0.70), (0.12, 0.60), (0.11, 0.46), (0.0, 0.40)], TUNIC, DEEP)  # torso
    F.poly([(-0.02, 0.73), (-0.10, 0.755), (-0.12, 0.80), (-0.09, 0.845),
            (-0.03, 0.858), (0.02, 0.83), (0.025, 0.765)], SKIN, DEEP)        # head
    F.poly([(0.005, 0.815), (0.10, 0.86), (0.02, 0.775)], SKIN, DEEP)         # ear
    F.poly([(-0.065, 0.858), (0.005, 0.868), (0.05, 0.82), (0.055, 0.72),
            (0.02, 0.72), (0.0, 0.80)], HAIR, DEEP, pitch=1.2)
    # drawn bow: limb arc + string + arrow
    n = 10
    for k in range(n):
        a0 = -0.9 + 1.8 * k / n; a1 = -0.9 + 1.8 * (k + 1) / n
        F.L(-0.24 + 0.10 * math.cos(a0), 0.58 + 0.30 * math.sin(a0),
            -0.24 + 0.10 * math.cos(a1), 0.58 + 0.30 * math.sin(a1), WOODC)
    F.L(-0.18, 0.855, -0.18, 0.305, (150, 146, 134))                          # string
    F.L(-0.30, 0.58, -0.02, 0.58, WOODC)                                       # arrow
    F.L(-0.30, 0.58, -0.27, 0.60, DEEP); F.L(-0.30, 0.58, -0.27, 0.56, DEEP)
    F.poly([(-0.02, 0.66), (-0.13, 0.60), (-0.20, 0.585), (-0.19, 0.555),
            (-0.10, 0.575), (0.0, 0.62)], TUNIC, DEEP)                        # bow arm
    return F.out


# ------------------------------------------------------------------ humans+
def erudite(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    ROBE = (60, 70, 110); DEEP = (42, 50, 84); SKIN = (88, 66, 52)
    # very tall, narrow, high-domed hooded robe
    F.poly([(-0.10, 0.02), (-0.115, 0.30), (-0.10, 0.55), (-0.115, 0.72),
            (-0.085, 0.88), (-0.02, 0.97), (0.05, 0.945), (0.09, 0.84),
            (0.075, 0.66), (0.09, 0.44), (0.075, 0.20), (0.09, 0.02)], ROBE, DEEP)
    F.poly([(-0.075, 0.80), (-0.10, 0.855), (-0.065, 0.895), (-0.015, 0.885),
            (-0.005, 0.83), (-0.03, 0.795)], SKIN, DEEP)                      # face in hood
    F.L(-0.06, 0.856, -0.085, 0.848, (40, 30, 26))
    F.disc(-0.135, 0.52, 0.035, (150, 180, 200))                              # held orb
    F.poly([(-0.09, 0.62), (-0.15, 0.57), (-0.165, 0.525), (-0.13, 0.50),
            (-0.09, 0.55)], ROBE, DEEP)                                       # sleeve
    return F.out


def guard(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    TAB = (78, 84, 110); DEEP = (54, 60, 84); MAIL = (128, 128, 138)
    STEEL = (160, 160, 170); WOODC = (120, 100, 72)
    F.poly([(-0.10, 0.02), (-0.115, 0.22), (-0.10, 0.42), (0.09, 0.42),
            (0.10, 0.22), (0.09, 0.02), (0.045, 0.02), (0.05, 0.20),
            (-0.005, 0.20), (-0.05, 0.02)], DEEP, DEEP)                       # legs
    F.poly([(-0.13, 0.40), (-0.145, 0.56), (-0.125, 0.72), (-0.05, 0.78),
            (0.05, 0.77), (0.115, 0.70), (0.13, 0.55), (0.11, 0.40)], TAB, DEEP)
    F.L(-0.02, 0.74, -0.02, 0.43, MAIL)                                        # heraldic bar
    F.L(-0.14, 0.55, 0.125, 0.56, DEEP)
    F.poly([(-0.02, 0.79), (-0.09, 0.815), (-0.11, 0.86), (-0.075, 0.90),
            (-0.01, 0.905), (0.03, 0.86), (0.025, 0.80)], MAIL, DEEP)         # helm+head
    F.L(-0.105, 0.855, -0.11, 0.815, MAIL)
    F.disc(-0.155, 0.55, 0.095, MAIL)                                          # round shield
    F.L(-0.155, 0.60, -0.155, 0.50, STEEL); F.L(-0.20, 0.55, -0.11, 0.55, STEEL)
    F.L(0.10, 0.40, 0.075, 1.02, WOODC)                                        # spear
    F.poly([(0.075, 1.02), (0.055, 1.12), (0.095, 1.12)], STEEL, STEEL)
    return F.out


def freeport_guard(cx, cy, s, seed=0, face=-1):
    """Freeport Militia: rust-red tabard, tall kite shield, halberd -- reads
    apart from the slate-blue round-shield Qeynos guard at a glance."""
    F = _F(cx, cy, s, face)
    TAB = (128, 54, 44); DEEP = (86, 38, 32); MAIL = (128, 128, 138)
    STEEL = (160, 160, 170); WOODC = (116, 96, 66); TRIM = (168, 138, 70)
    F.poly([(-0.10, 0.02), (-0.115, 0.22), (-0.10, 0.42), (0.09, 0.42),
            (0.10, 0.22), (0.09, 0.02), (0.045, 0.02), (0.05, 0.20),
            (-0.005, 0.20), (-0.05, 0.02)], DEEP, DEEP)                        # legs
    F.poly([(-0.13, 0.40), (-0.145, 0.56), (-0.125, 0.72), (-0.05, 0.78),
            (0.05, 0.77), (0.115, 0.70), (0.13, 0.55), (0.11, 0.40)], TAB, DEEP)
    F.L(-0.13, 0.62, 0.12, 0.63, TRIM)                                          # gold band
    F.poly([(-0.02, 0.79), (-0.09, 0.815), (-0.11, 0.86), (-0.075, 0.90),
            (-0.01, 0.905), (0.03, 0.86), (0.025, 0.80)], MAIL, DEEP)           # helm
    F.poly([(-0.04, 0.905), (-0.02, 0.96), (0.02, 0.90)], TAB, None)            # helm crest
    # tall KITE shield covering the leading side
    F.poly([(-0.21, 0.66), (-0.13, 0.68), (-0.115, 0.50), (-0.165, 0.30),
            (-0.235, 0.50)], MAIL, DEEP)
    F.L(-0.17, 0.64, -0.175, 0.36, TAB)                                         # shield stripe
    # halberd: tall haft + axe blade + spike
    F.L(0.10, 0.40, 0.075, 1.04, WOODC)
    F.poly([(0.075, 0.96), (0.16, 0.99), (0.155, 0.88), (0.08, 0.90)], STEEL, (110, 110, 120))
    F.poly([(0.075, 1.04), (0.055, 1.12), (0.095, 1.12)], STEEL, STEEL)
    return F.out


def barbarian(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    SKIN = (150, 118, 92); DEEP = (110, 84, 62); FUR = (92, 72, 50); STEEL = (150, 150, 160)
    F.poly([(-0.11, 0.02), (-0.12, 0.20), (-0.10, 0.36), (0.10, 0.36),
            (0.12, 0.18), (0.10, 0.02), (0.05, 0.02), (0.05, 0.18),
            (-0.01, 0.18), (-0.05, 0.02)], SKIN, DEEP)                        # legs
    F.poly([(-0.13, 0.34), (-0.14, 0.46), (0.13, 0.46), (0.12, 0.34)], FUR, DEEP)
    F.poly([(-0.15, 0.44), (-0.17, 0.62), (-0.13, 0.76), (-0.02, 0.82),
            (0.09, 0.78), (0.15, 0.64), (0.14, 0.46)], SKIN, DEEP)            # big torso
    F.poly([(-0.02, 0.83), (-0.085, 0.85), (-0.10, 0.895), (-0.06, 0.935),
            (0.005, 0.93), (0.035, 0.885), (0.02, 0.835)], SKIN, DEEP)
    F.poly([(-0.01, 0.935), (0.02, 0.99), (0.055, 0.975), (0.03, 0.92)], (80, 60, 44), None)  # topknot
    F.L(-0.07, 0.895, -0.10, 0.888, (60, 44, 34))
    F.L(0.10, 0.50, 0.24, 0.92, (110, 84, 56))                                 # axe haft
    F.poly([(0.20, 0.86), (0.30, 0.92), (0.30, 0.78), (0.22, 0.80)], STEEL, (110, 110, 120))
    return F.out


def halfling(cx, cy, s, seed=0, face=-1):
    """A small PERSON: trousers, waistcoat over a shirt, curly mop, big bare
    feet, short sword. Human proportions scaled down, not a blob."""
    F = _F(cx, cy, s, face)   # placer gives ~60% of human height
    PANTS = (96, 74, 48); VEST = (128, 84, 52); SHIRT = (186, 176, 152)
    DEEP = (70, 54, 38); SKIN = (180, 146, 110); HAIR = (110, 70, 40)
    STEEL = (162, 162, 172)
    # legs in trousers + big bare feet
    F.poly([(-0.10, 0.10), (-0.12, 0.24), (-0.10, 0.38), (0.09, 0.38),
            (0.11, 0.22), (0.09, 0.10), (0.04, 0.10), (0.045, 0.22),
            (-0.02, 0.22), (-0.045, 0.10)], PANTS, DEEP)
    F.poly([(-0.115, 0.10), (-0.185, 0.055), (-0.175, 0.02), (-0.04, 0.02),
            (-0.045, 0.09)], SKIN, DEEP)                                        # big foot fwd
    F.poly([(0.04, 0.09), (0.05, 0.02), (0.17, 0.02), (0.16, 0.06),
            (0.095, 0.10)], SKIN, DEEP)
    # shirt torso + waistcoat over it
    F.poly([(-0.10, 0.36), (-0.13, 0.48), (-0.10, 0.585), (0.0, 0.625),
            (0.09, 0.58), (0.12, 0.47), (0.10, 0.36)], SHIRT, DEEP)
    F.poly([(-0.11, 0.38), (-0.125, 0.50), (-0.09, 0.57), (-0.045, 0.585),
            (-0.05, 0.38)], VEST, DEEP)
    F.poly([(0.06, 0.58), (0.10, 0.56), (0.115, 0.46), (0.10, 0.375),
            (0.055, 0.375)], VEST, DEEP)
    # round friendly head + curly mop
    F.poly([(-0.015, 0.63), (-0.09, 0.655), (-0.105, 0.705), (-0.065, 0.75),
            (0.01, 0.755), (0.05, 0.71), (0.035, 0.645)], SKIN, DEEP)
    F.poly([(-0.10, 0.74), (-0.045, 0.785), (0.03, 0.785), (0.075, 0.74),
            (0.065, 0.69), (0.03, 0.735), (-0.03, 0.75), (-0.08, 0.70)], HAIR, DEEP, pitch=1.1)
    F.L(-0.06, 0.712, -0.085, 0.706, DEEP)                                      # eye
    # arm out with a short sword
    F.poly([(-0.09, 0.54), (-0.16, 0.50), (-0.20, 0.455), (-0.175, 0.435),
            (-0.13, 0.475), (-0.07, 0.505)], SHIRT, DEEP)
    F.L(-0.19, 0.445, -0.30, 0.50, STEEL)
    F.L(-0.175, 0.425, -0.21, 0.47, DEEP)                                       # guard
    return F.out


def gnome(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)   # placer gives ~50% human height
    CLOTH = (108, 88, 58); DEEP = (76, 62, 42); SKIN = (180, 148, 116)
    BEARD = (188, 182, 168); BRASS = (168, 138, 70)
    F.poly([(-0.11, 0.02), (-0.14, 0.24), (-0.10, 0.42), (0.10, 0.42),
            (0.14, 0.22), (0.11, 0.02), (0.05, 0.02), (0.06, 0.16),
            (-0.02, 0.16), (-0.05, 0.02)], CLOTH, DEEP)
    F.poly([(-0.05, 0.42), (-0.14, 0.46), (-0.17, 0.56), (-0.12, 0.66),
            (0.0, 0.70), (0.10, 0.64), (0.13, 0.53), (0.07, 0.44)], SKIN, DEEP)  # BIG head
    F.poly([(-0.15, 0.52), (-0.10, 0.40), (0.0, 0.36), (0.08, 0.40),
            (0.10, 0.50), (0.02, 0.44), (-0.08, 0.46)], BEARD, DEEP, pitch=1.1)
    F.L(-0.14, 0.62, 0.10, 0.645, BRASS)                                       # goggle band
    F.disc(-0.10, 0.63, 0.035, BRASS); F.disc(-0.02, 0.645, 0.035, BRASS)
    F.L(0.08, 0.30, 0.26, 0.62, (140, 140, 150))                               # big wrench
    F.poly([(0.23, 0.58), (0.30, 0.68), (0.34, 0.62), (0.27, 0.55)], (140, 140, 150), None)
    return F.out


# ------------------------------------------------------------------ big folk
def dwarf(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    CLOTH = (104, 76, 52); DEEP = (72, 52, 36); BEARD = (176, 156, 118)
    MAIL = (126, 122, 114); STEEL = (155, 155, 165)
    F.poly([(-0.13, 0.02), (-0.16, 0.20), (-0.14, 0.34), (0.13, 0.34),
            (0.16, 0.18), (0.13, 0.02), (0.06, 0.02), (0.06, 0.16),
            (-0.02, 0.16), (-0.06, 0.02)], CLOTH, DEEP)
    F.poly([(-0.17, 0.32), (-0.19, 0.50), (-0.14, 0.62), (0.0, 0.66),
            (0.13, 0.60), (0.18, 0.48), (0.16, 0.32)], CLOTH, DEEP)           # barrel torso
    F.poly([(-0.15, 0.58), (-0.19, 0.44), (-0.16, 0.30), (-0.06, 0.26),
            (0.04, 0.30), (0.06, 0.44), (0.0, 0.36), (-0.08, 0.34)], BEARD, DEEP, pitch=1.1)
    F.poly([(-0.03, 0.66), (-0.10, 0.685), (-0.12, 0.72), (-0.08, 0.755),
            (0.0, 0.755), (0.035, 0.715), (0.02, 0.67)], MAIL, DEEP)           # helm
    F.L(-0.12, 0.73, -0.19, 0.79, MAIL); F.L(0.03, 0.73, 0.10, 0.79, MAIL)     # horns
    F.L(-0.115, 0.695, -0.145, 0.688, DEEP)
    F.L(0.10, 0.40, -0.06, 0.82, (110, 84, 56))                                # hammer haft
    F.poly([(-0.11, 0.76), (-0.02, 0.80), (0.0, 0.90), (-0.09, 0.86)], STEEL, (100, 100, 110))
    return F.out


def troll(cx, cy, s, seed=0, face=-1):
    """Lanky green troll: pointed ears, LONG pointed nose, underbite tusks,
    gangly arms past the knees. Lean, not massive (that's the ogre)."""
    F = _F(cx, cy, s, face)
    SKIN = (74, 98, 60); DEEP = (50, 70, 42)
    # long slightly-bent legs + big feet
    F.poly([(-0.11, 0.02), (-0.16, 0.02), (-0.12, 0.05), (-0.09, 0.20),
            (-0.11, 0.38), (0.10, 0.38), (0.09, 0.20), (0.13, 0.05),
            (0.17, 0.02), (0.11, 0.02), (0.06, 0.07), (-0.02, 0.07),
            (-0.06, 0.04)], SKIN, DEEP)
    # lean torso, hunched a touch forward at the shoulders
    F.poly([(-0.12, 0.36), (-0.15, 0.50), (-0.13, 0.62), (-0.04, 0.68),
            (0.07, 0.66), (0.12, 0.56), (0.11, 0.42), (0.06, 0.36)], SKIN, DEEP)
    # gangly arms hanging past the knees, big hands
    F.poly([(-0.11, 0.60), (-0.17, 0.48), (-0.20, 0.30), (-0.22, 0.16),
            (-0.17, 0.14), (-0.15, 0.28), (-0.11, 0.44), (-0.07, 0.56)], SKIN, DEEP)
    F.L(-0.22, 0.16, -0.245, 0.10, DEEP); F.L(-0.20, 0.15, -0.215, 0.09, DEEP)  # claw fingers
    F.poly([(0.08, 0.60), (0.13, 0.48), (0.16, 0.30), (0.18, 0.16),
            (0.13, 0.14), (0.12, 0.28), (0.08, 0.44), (0.04, 0.56)], DEEP, DEEP)
    # head: narrow skull, LONG pointed nose spike, underbite jaw + tusks
    F.poly([(-0.02, 0.68), (-0.10, 0.70), (-0.135, 0.745), (-0.10, 0.795),
            (-0.03, 0.805), (0.025, 0.77), (0.02, 0.70)], SKIN, DEEP)
    F.poly([(-0.115, 0.77), (-0.30, 0.725), (-0.115, 0.715)], SKIN, DEEP)      # nose spike
    F.poly([(-0.135, 0.70), (-0.19, 0.685), (-0.135, 0.665), (-0.05, 0.675)], SKIN, DEEP)  # jaw
    F.L(-0.175, 0.69, -0.19, 0.735, (205, 200, 185))                            # tusk up
    F.L(-0.125, 0.675, -0.135, 0.715, (205, 200, 185))
    F.poly([(-0.02, 0.785), (0.09, 0.88), (0.035, 0.755)], SKIN, DEEP)          # tall pointed ear
    F.L(-0.095, 0.765, -0.12, 0.758, (26, 36, 22))                              # eye
    return F.out


def ogre(cx, cy, s, seed=0, face=-1):
    """Pale, bald, ROUND -- almost baby-like. No visible ears, clean dome head
    sitting on the shoulders, enormous drooping belly, thick limbs, club."""
    F = _F(cx, cy, s, face)
    SKIN = (168, 148, 112); DEEP = (124, 106, 76); CLOTH = (96, 74, 50)
    # thick stumpy legs
    F.poly([(-0.15, 0.02), (-0.19, 0.14), (-0.17, 0.26), (0.17, 0.26),
            (0.19, 0.12), (0.15, 0.02), (0.06, 0.02), (0.07, 0.12),
            (-0.03, 0.12), (-0.06, 0.02)], SKIN, DEEP)
    # ENORMOUS round belly-torso (one big egg)
    F.poly([(-0.22, 0.30), (-0.28, 0.46), (-0.24, 0.62), (-0.10, 0.71),
            (0.08, 0.71), (0.22, 0.63), (0.29, 0.47), (0.25, 0.31),
            (0.10, 0.24), (-0.08, 0.24)], SKIN, DEEP)
    F.L(-0.12, 0.30, 0.14, 0.31, DEEP)                                          # belly droop crease
    F.L(-0.16, 0.44, -0.06, 0.41, DEEP)                                         # navel-ish fold
    # loincloth strap across the gut
    F.poly([(-0.24, 0.52), (0.26, 0.56), (0.25, 0.49), (-0.23, 0.45)], CLOTH, None)
    # big ROUND bald dome head, directly on the shoulders, NO ears
    F.disc(-0.02, 0.79, 0.115, SKIN, n=16)
    F.L(-0.09, 0.80, -0.115, 0.795, (60, 48, 34))                               # tiny eye
    F.L(-0.115, 0.745, -0.05, 0.735, DEEP)                                      # wide mouth line
    F.L(-0.10, 0.74, -0.09, 0.765, (205, 200, 185))                             # lower tooth up
    F.L(-0.06, 0.737, -0.05, 0.76, (205, 200, 185))
    # thick arm + club over the shoulder
    F.poly([(0.16, 0.62), (0.24, 0.52), (0.28, 0.40), (0.22, 0.37),
            (0.17, 0.48), (0.11, 0.58)], SKIN, DEEP)
    F.L(0.26, 0.40, 0.38, 0.80, (104, 80, 52))
    F.poly([(0.33, 0.72), (0.45, 0.86), (0.38, 0.90), (0.29, 0.76)], (104, 80, 52), DEEP)
    return F.out


def iksar(cx, cy, s, seed=0, face=-1):
    """UPRIGHT lizardman: straight-backed, long tail sweeping to the ground
    behind, level snout, small crest, staff held vertical. No hunch."""
    F = _F(cx, cy, s, face)
    SCALE = (96, 104, 82); DEEP = (64, 72, 54); WOODC = (116, 92, 60)
    # tail: thick at hips, S-sweep to the ground behind
    F.poly([(0.06, 0.36), (0.20, 0.30), (0.30, 0.18), (0.34, 0.06),
            (0.40, 0.02), (0.30, 0.02), (0.24, 0.12), (0.14, 0.24),
            (0.04, 0.30)], SCALE, DEEP)
    # upright legs (digitigrade ankles, but posture vertical)
    F.poly([(-0.10, 0.02), (-0.14, 0.02), (-0.10, 0.06), (-0.08, 0.22),
            (-0.10, 0.40), (0.09, 0.40), (0.07, 0.22), (0.09, 0.06),
            (0.13, 0.02), (0.07, 0.02), (0.03, 0.07), (-0.03, 0.07)], SCALE, DEEP)
    # upright slim torso
    F.poly([(-0.10, 0.38), (-0.13, 0.54), (-0.11, 0.70), (-0.03, 0.76),
            (0.06, 0.74), (0.10, 0.62), (0.09, 0.46), (0.05, 0.38)], SCALE, DEEP)
    # level snout head on a straight neck
    F.poly([(-0.03, 0.76), (-0.05, 0.82), (-0.13, 0.845), (-0.26, 0.835),
            (-0.30, 0.81), (-0.22, 0.795), (-0.10, 0.795), (-0.02, 0.79)], SCALE, DEEP)
    F.L(-0.27, 0.818, -0.30, 0.813, DEEP)                                       # nostril
    F.L(-0.12, 0.825, -0.15, 0.82, (30, 36, 26))                                # eye
    # small crest fins on the skull + neck ridge
    F.poly([(-0.06, 0.845), (-0.02, 0.90), (0.005, 0.845)], DEEP, None)
    F.poly([(-0.005, 0.83), (0.035, 0.875), (0.05, 0.825)], DEEP, None)
    # staff held vertical in front
    F.L(-0.17, 0.06, -0.17, 0.92, WOODC)
    F.poly([(-0.17, 0.92), (-0.205, 0.97), (-0.14, 0.965)], DEEP, None)         # totem top
    F.poly([(-0.10, 0.62), (-0.155, 0.575), (-0.175, 0.53), (-0.145, 0.51),
            (-0.115, 0.555), (-0.07, 0.59)], SCALE, DEEP)                       # arm to staff
    return F.out


def froglok(cx, cy, s, seed=0, face=-1):
    """Frog-man, unmistakable next to an iksar: NO tail, deep frog crouch on
    folded legs, huge webbed feet, and two bulging eyes ON TOP of the head."""
    F = _F(cx, cy, s, face)
    SKIN = (88, 122, 70); DEEP = (58, 88, 48); PALE = (140, 168, 110)
    # folded frog legs splayed wide + big webbed feet
    F.poly([(-0.26, 0.02), (-0.34, 0.02), (-0.28, 0.05), (-0.22, 0.16),
            (-0.24, 0.28), (-0.12, 0.22), (-0.14, 0.10)], SKIN, DEEP)
    F.L(-0.34, 0.02, -0.30, 0.055, DEEP); F.L(-0.31, 0.02, -0.28, 0.05, DEEP)   # webbed toes
    F.poly([(0.22, 0.02), (0.30, 0.02), (0.25, 0.05), (0.20, 0.16),
            (0.22, 0.28), (0.10, 0.22), (0.12, 0.10)], SKIN, DEEP)
    F.L(0.30, 0.02, 0.26, 0.055, DEEP)
    # squat round body low to the ground
    F.poly([(-0.16, 0.16), (-0.20, 0.30), (-0.15, 0.44), (-0.02, 0.50),
            (0.11, 0.45), (0.17, 0.32), (0.14, 0.18), (0.0, 0.12)], SKIN, DEEP)
    F.poly([(-0.14, 0.24), (-0.10, 0.36), (0.02, 0.40), (0.08, 0.30),
            (0.02, 0.20), (-0.08, 0.18)], PALE, None, pitch=1.4)                # pale throat-belly
    # wide head = mostly mouth, eyes bulging ON TOP
    F.poly([(-0.04, 0.50), (-0.18, 0.535), (-0.28, 0.51), (-0.26, 0.46),
            (-0.10, 0.445), (0.03, 0.455)], SKIN, DEEP)
    F.L(-0.27, 0.478, -0.05, 0.468, DEEP)                                       # huge mouth line
    F.disc(-0.155, 0.565, 0.038, SKIN); F.disc(-0.155, 0.568, 0.016, (30, 40, 26))  # bulge eye L
    F.disc(-0.045, 0.575, 0.038, SKIN); F.disc(-0.045, 0.578, 0.016, (30, 40, 26))  # bulge eye R
    # short spear held across
    F.L(-0.10, 0.34, -0.40, 0.40, (150, 142, 118))
    F.poly([(-0.40, 0.40), (-0.47, 0.43), (-0.47, 0.37)], SKIN, DEEP)
    return F.out


# ------------------------------------------------------------------ beasts+
def gnoll(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    FUR = (120, 102, 74); DEEP = (86, 72, 50); BONE = (176, 168, 140)
    # digitigrade legs
    F.poly([(-0.14, 0.02), (-0.20, 0.02), (-0.15, 0.06), (-0.10, 0.16),
            (-0.13, 0.30), (-0.06, 0.44), (0.10, 0.44), (0.16, 0.30),
            (0.13, 0.16), (0.18, 0.06), (0.23, 0.02), (0.16, 0.02),
            (0.10, 0.10), (0.0, 0.10), (-0.08, 0.06)], FUR, DEEP)
    # sloped hyena torso: shoulder high forward, hip low
    F.poly([(-0.16, 0.42), (-0.20, 0.58), (-0.14, 0.72), (0.0, 0.76),
            (0.13, 0.68), (0.19, 0.52), (0.15, 0.42)], FUR, DEEP)
    for k in range(4):                                                          # crest
        x = -0.10 + 0.06 * k
        F.poly([(x, 0.74 - 0.02 * k), (x + 0.05, 0.82 - 0.02 * k), (x + 0.05, 0.72 - 0.02 * k)], DEEP, None)
    F.poly([(-0.12, 0.72), (-0.24, 0.77), (-0.36, 0.745), (-0.42, 0.705),
            (-0.33, 0.685), (-0.20, 0.685), (-0.12, 0.67)], FUR, DEEP)         # muzzle head
    F.poly([(-0.16, 0.76), (-0.13, 0.86), (-0.07, 0.83), (-0.10, 0.745)], FUR, DEEP)  # ear
    F.poly([(-0.10, 0.755), (-0.06, 0.855), (0.0, 0.825), (-0.04, 0.74)], FUR, DEEP)
    F.L(-0.38, 0.695, -0.40, 0.73, BONE)
    F.L(-0.245, 0.735, -0.28, 0.728, (40, 34, 24))
    F.L(-0.14, 0.52, -0.20, 1.00, BONE)                                        # spear up
    F.poly([(-0.20, 1.00), (-0.245, 1.09), (-0.165, 1.07)], FUR, DEEP)
    return F.out


def kobold(cx, cy, s, seed=0, face=-1):
    F = _F(cx, cy, s, face)
    HIDE = (104, 88, 70); DEEP = (74, 60, 46); STEEL = (150, 150, 160)
    F.poly([(0.10, 0.34), (0.24, 0.26), (0.34, 0.12), (0.30, 0.08),
            (0.20, 0.20), (0.08, 0.28)], DEEP, DEEP)                           # tail
    F.poly([(-0.13, 0.02), (-0.18, 0.02), (-0.13, 0.07), (-0.09, 0.16),
            (-0.12, 0.28), (-0.06, 0.42), (0.10, 0.42), (0.14, 0.28),
            (0.11, 0.16), (0.16, 0.07), (0.21, 0.02), (0.14, 0.02),
            (0.09, 0.09), (0.0, 0.09), (-0.07, 0.06)], HIDE, DEEP)
    F.poly([(-0.14, 0.40), (-0.17, 0.52), (-0.12, 0.62), (0.0, 0.66),
            (0.10, 0.60), (0.13, 0.48), (0.10, 0.40)], HIDE, DEEP)             # hunched torso
    F.poly([(-0.10, 0.60), (-0.22, 0.645), (-0.33, 0.62), (-0.37, 0.585),
            (-0.28, 0.565), (-0.16, 0.565), (-0.09, 0.555)], HIDE, DEEP)       # long snout
    F.poly([(-0.13, 0.635), (-0.09, 0.72), (-0.03, 0.69), (-0.07, 0.62)], HIDE, DEEP)  # ear
    F.L(-0.22, 0.615, -0.25, 0.608, (40, 34, 24))
    F.L(0.02, 0.50, -0.16, 0.84, (120, 96, 64))                                # pick
    F.L(-0.16, 0.84, -0.26, 0.80, STEEL); F.L(-0.16, 0.84, -0.085, 0.885, STEEL)
    return F.out


def skeleton(cx, cy, s, seed=0, face=-1):
    """Bare-bones skeleton of a playable race, carrying a rusty sword -- the
    classic EQ walking dead. No armor, no robes (Brandon's rule)."""
    F = _F(cx, cy, s, face)
    BONE = (182, 176, 158); DEEP = (96, 90, 78); RUST = (128, 96, 70)
    # skull: round with a dark eye socket + jaw notch
    F.poly([(-0.02, 0.80), (-0.095, 0.825), (-0.115, 0.875), (-0.075, 0.92),
            (0.0, 0.925), (0.04, 0.875), (0.025, 0.81)], BONE, DEEP)
    F.L(-0.065, 0.872, -0.095, 0.864, (40, 36, 30))                            # socket
    F.L(-0.10, 0.832, -0.05, 0.826, (40, 36, 30))                              # jaw line
    # spine
    F.L(-0.005, 0.80, 0.005, 0.44, DEEP)
    # ribcage: solid bone slab with dark rib lines over it
    F.poly([(-0.10, 0.74), (-0.13, 0.62), (-0.09, 0.52), (0.09, 0.52),
            (0.13, 0.62), (0.10, 0.74)], BONE, DEEP)
    for k in range(4):
        y = 0.70 - 0.05 * k
        F.L(-0.10 + 0.008 * k, y, 0.10 - 0.008 * k, y - 0.012, DEEP)
    # pelvis
    F.poly([(-0.07, 0.46), (-0.09, 0.38), (0.0, 0.35), (0.09, 0.38),
            (0.07, 0.46)], BONE, DEEP)
    # leg bones (thin polys so they stay visible at map scale)
    F.poly([(-0.075, 0.38), (-0.10, 0.20), (-0.085, 0.02), (-0.045, 0.02),
            (-0.055, 0.20), (-0.035, 0.36)], BONE, DEEP)
    F.poly([(0.045, 0.37), (0.07, 0.20), (0.10, 0.02), (0.055, 0.02),
            (0.035, 0.20), (0.015, 0.36)], BONE, DEEP)
    F.L(-0.10, 0.02, -0.035, 0.02, DEEP); F.L(0.045, 0.02, 0.115, 0.02, DEEP)  # feet
    # sword arm raised, other arm hanging
    F.poly([(-0.09, 0.70), (-0.17, 0.63), (-0.21, 0.56), (-0.185, 0.545),
            (-0.14, 0.60), (-0.07, 0.66)], BONE, DEEP)
    F.L(-0.20, 0.545, -0.255, 0.62, RUST); F.L(-0.255, 0.62, -0.31, 0.75, RUST)  # rusty blade
    F.L(-0.185, 0.53, -0.225, 0.575, DEEP)                                     # crossguard
    F.poly([(0.09, 0.70), (0.13, 0.58), (0.15, 0.44), (0.115, 0.435),
            (0.10, 0.56), (0.065, 0.68)], BONE, DEEP)
    return F.out


# ------------------------------------------------------------------ registry
SIL = {
    'dark_elf': dark_elf, 'high_elf': high_elf, 'wood_elf': wood_elf,
    'erudite': erudite, 'human': guard, 'guard': guard, 'qeynos_human': guard,
    'freeport_human': freeport_guard, 'freeport_guard': freeport_guard,
    'barbarian': barbarian, 'halfling': halfling,
    'gnome': gnome, 'dwarf': dwarf, 'troll': troll, 'ogre': ogre,
    'iksar': iksar, 'froglok': froglok, 'gnoll': gnoll, 'kobold': kobold,
    'skeleton': skeleton, 'zombie': skeleton, 'ghoul': skeleton,
}

# relative height per race so a mixed line-up scales believably (human=1.0)
HEIGHT = {
    'ogre': 1.35, 'troll': 1.30, 'barbarian': 1.15, 'iksar': 1.05,
    'human': 1.0, 'guard': 1.0, 'qeynos_human': 1.0, 'freeport_human': 1.0,
    'freeport_guard': 1.0,
    'erudite': 1.05, 'high_elf': 1.0, 'dark_elf': 0.95, 'wood_elf': 0.9,
    'skeleton': 1.0, 'zombie': 1.0, 'ghoul': 1.0,
    'gnoll': 1.05, 'kobold': 0.7, 'froglok': 0.7, 'dwarf': 0.75,
    'halfling': 0.6, 'gnome': 0.5,
}
