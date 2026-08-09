"""Neriak rebuild — the base, from the clean source, in a shared Dark Elf palette.

The previous version failed because I treated the map's own geometry as texture and
deleted it. Neriak is a dense capital; the answer is not fewer lines, it is a colour
HIERARCHY so the eye can separate wall from floor from water.

Shared Dark Elf palette (reusable for any Teir'Dal / cavern zone):
    OBSIDIAN   structural walls and buildings   - deepest, carries the drawing
    BASALT     secondary structure, interiors   - a step back
    STONE      floors, terraces, steps          - quiet mid tone
    ARCANE     water and glow                   - the one cool accent
    LAMP       lamplight, gold fittings         - the one warm accent
"""
import shutil, collections
SRC='/home/claude/work/neriak_ref'
O='/mnt/user-data/outputs'

# ---- the shared Dark Elf palette ----
OBSIDIAN=(44,34,58)      # walls / main structure
BASALT  =(92,70,108)     # secondary structure
STONE   =(120,112,134)   # floors, steps, terraces
ARCANE  =(58,84,150)     # water, glow
LAMP    =(168,132,72)    # lamplight, gold
ZONELINE=(150,0,200)

MAP={(0,0,0):OBSIDIAN,
     (100,50,0):BASALT,
     (128,128,128):STONE,
     (0,0,255):ARCANE,
     (160,120,60):LAMP,
     (255,215,0):LAMP,
     (150,0,200):ZONELINE}

for z in ['neriaka','neriakb','neriakc']:
    src=f'{SRC}/{z}.txt'
    raw=[l.rstrip('\r\n') for l in open(src,encoding='utf-8',errors='replace') if l.strip()]
    out=[]; seen=collections.Counter()
    for l in raw:
        if not l.startswith('L'):
            out.append(l); continue
        f=l[2:].split(',')
        c=(int(f[6]),int(f[7]),int(f[8]))
        nc=MAP.get(c,STONE); seen[nc]+=1
        out.append("L %s,%s,%s,%s,%s,%s, %d, %d, %d"%(f[0],f[1],f[2],f[3],f[4],f[5],*nc))
    open(f'{O}/{z}.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
    names={OBSIDIAN:'obsidian',BASALT:'basalt',STONE:'stone',ARCANE:'arcane',LAMP:'lamp',ZONELINE:'zoneline'}
    print(f"{z}: {len(out)} lines restored  " + "  ".join(f"{names[k]}={v}" for k,v in seen.most_common()))
    b=open(f'{O}/{z}.txt','rb').read()
    assert sum(1 for i,ch in enumerate(b) if ch==10 and (i==0 or b[i-1]!=13))==0
print("\nbase restored from the clean source and recoloured; CRLF OK")
