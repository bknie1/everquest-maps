"""Neriak labels: darken the palette so they read, name the landmarks, and add the
city's own places on the _3 layer as toggleable flavour.

Transform throughout: native = (-loc2, -loc1)
"""
O = '/mnt/user-data/outputs'

# ---- darker palette -------------------------------------------------------
# The bright variant washed out against the pale map. Dark blacks, purples,
# reds and blues instead — high contrast on paper, still colour-coded by kind.
DARK = {
    (96, 180, 116): (24, 62, 78),    # merchants          -> dark teal-blue
    (35,  95,  55): (24, 62, 78),
    (96, 184, 206): (28, 48, 112),   # landmarks/services -> dark blue
    (30,  80,  95): (28, 48, 112),
    (214, 84, 132): (122, 20, 52),   # hostile named      -> dark red
    (110,  0,  60): (122, 20, 52),
    (214,164,  86): (104, 56, 26),   # tradeskill         -> dark brown-red
    (150, 90,  40): (104, 56, 26),
    (226,168,  60): (112, 68, 20),   # succor             -> dark amber
    (160,105,   0): (112, 68, 20),
    (224,124,  72): (112, 38, 34),   # named NPC          -> dark maroon
    (165, 60,  20): (112, 38, 34),
    ( 90, 35, 110): ( 62, 24,  92),  # guildmasters       -> deep purple
    (150,  0, 200): ( 96,  0, 140),  # zone lines         -> dark violet
}

VENUE   = (40, 26, 58)     # near-black plum: the city's own places
AREA    = (70, 22, 96)     # dark purple: area names
LANDMARK= (28, 48, 112)

def wn(l1, l2): return (-l2, -l1)

# ---- 1. darken every label on the three Neriak marker layers ---------------
for z in ['neriaka', 'neriakb', 'neriakc']:
    p = f'{O}/{z}_1.txt'
    raw = [l.rstrip('\r\n') for l in open(p, encoding='utf-8', errors='replace') if l.strip()]
    out = []; n = 0
    for l in raw:
        if l.startswith('P'):
            f = l[1:].split(',')
            try: ink = (int(f[3]), int(f[4]), int(f[5]))
            except: out.append(l); continue
            if ink in DARK:
                d = DARK[ink]
                f[3] = ' %d' % d[0]; f[4] = ' %d' % d[1]; f[5] = ' %d' % d[2]
                out.append('P' + ','.join(f)); n += 1; continue
        out.append(l)
    open(p, 'w', newline='').write('\r\n'.join(out) + '\r\n')
    print(f"{z}_1: darkened {n} labels")

# ---- 2. name the landmarks -------------------------------------------------
p = f'{O}/neriakc_1.txt'
raw = [l.rstrip('\r\n') for l in open(p, encoding='utf-8', errors='replace') if l.strip()]
raw = [l.replace('Necromancer+SK_Guild_(Hall_of_the_Dead)',
                 'Lodge_of_the_Dead_(Necromancer+SK_Guild)') for l in raw]
open(p, 'w', newline='').write('\r\n'.join(raw) + '\r\n')
print("neriakc_1: Hall of the Dead -> Lodge of the Dead")

# ---- 3. the city's own places, on the _3 layer -----------------------------
PLACES = [
    # name,                              loc1,     loc2,     z,      ink
    ("The_Rock",                         772.72,  -1517.85, -80.15,  VENUE),
    ("Cuisine_Excelsior",                761.99,  -1447.97, -80.15,  VENUE),
    ("The_Bauble",                       823.87,  -1420.25, -80.15,  VENUE),
    ("The_Maiden's_Fancy",               883.23,  -1452.40, -80.15,  VENUE),
    ("Underground_Brothel",              868.46,  -1444.17, -108.15, VENUE),
    ("Furrier_Royale",                   764.16,  -1322.26, -80.15,  VENUE),
    ("The_Ebon_Mask",                    701.37,  -1336.61, -80.15,  VENUE),
    ("Library",                          857.69,  -1315.01, -66.15,  LANDMARK),
    ("Third_Gate",                       762.64,  -1199.55, -80.15,  LANDMARK),
    ("Temple_of_Hate",                   465.61,   -812.40, -52.15,  AREA),
]
lines = []
for name, l1, l2, lz, ink in PLACES:
    nx, ny = wn(l1, l2)
    size = 3 if ink in (AREA, LANDMARK) else 2
    lines.append("P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s" % (nx, ny, lz, *ink, size, name))
    print(f"   {name:34} -> native ({nx:8.2f}, {ny:9.2f})")

# the Embassy: the guarded pocket in the north-east, named for its Meeting Hall
lines.append("P 1640.0000, -1320.0000, -80.1500, %d, %d, %d, 3, Embassy" % AREA)
print("   Embassy (area label over the north-east compound)")

open(f'{O}/neriakc_3.txt', 'w', newline='').write('\r\n'.join(lines) + '\r\n')
b = open(f'{O}/neriakc_3.txt', 'rb').read()
assert sum(1 for i, ch in enumerate(b) if ch == 10 and (i == 0 or b[i-1] != 13)) == 0
print(f"\nneriakc_3: {len(lines)} place labels | CRLF OK")
