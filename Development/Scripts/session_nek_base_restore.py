"""Rebuild the Nektulos base from the repo original, removing ONLY the tree blobs.

My earlier purges chased trees with broad rules and took structural detail with
them (78,74,92 went 99->18; 100,50,0 went 45->7). Trees live in the decoration
layer now, so the base should be the original minus the canopies and nothing else.
"""
import math, collections
O='/mnt/user-data/outputs'
REPO='/home/claude/work/maps_repo/Maps Repo/Emoda Legends Maps'
TREE_INKS={(58,60,78),(70,72,88)}

raw=[l.rstrip('\r\n') for l in open(f'{REPO}/nektulos.txt',encoding='utf-8',errors='replace') if l.strip()]
head=[l for l in raw if not l.startswith('L')]
lines=[l for l in raw if l.startswith('L')]
def parse(l):
    f=l[2:].split(',')
    return float(f[0]),float(f[1]),float(f[3]),float(f[4]),(int(f[6]),int(f[7]),int(f[8]))

# candidate tree strokes: short segments in the two tree inks
short=[(i,(parse(l)[0]+parse(l)[2])/2,(parse(l)[1]+parse(l)[3])/2)
       for i,l in enumerate(lines)
       if parse(l)[4] in TREE_INKS and math.hypot(parse(l)[2]-parse(l)[0],parse(l)[3]-parse(l)[1])<60]
G=40.0; cells=collections.defaultdict(list)
for i,x,y in short: cells[(int(x//G),int(y//G))].append((i,x,y))
seen=set(); drop=set(); blobs=0
for k in list(cells):
    if k in seen: continue
    st=[k]; comp=[]
    while st:
        d=st.pop()
        if d in seen or d not in cells: continue
        seen.add(d); comp+=cells[d]
        for dx in(-1,0,1):
            for dy in(-1,0,1):
                nn=(d[0]+dx,d[1]+dy)
                if nn in cells and nn not in seen: st.append(nn)
    xs=[p[1] for p in comp]; ys=[p[2] for p in comp]
    w=max(xs)-min(xs); h=max(ys)-min(ys)
    # a canopy blob: many strokes packed into a small, roughly round footprint
    if len(comp)>=14 and w<240 and h<240 and 0.45 < (w+1)/(h+1) < 2.2:
        drop.update(p[0] for p in comp); blobs+=1
keep=[l for i,l in enumerate(lines) if i not in drop]
open(f'{O}/nektulos.txt','w',newline='').write('\r\n'.join(head+keep)+'\r\n')
print(f"removed {blobs} canopy blobs ({len(drop)} lines)")
print(f"base: {len(lines)} -> {len(keep)} lines (was 352 after the over-purge)")
import collections as C
cc=C.Counter(parse(l)[4] for l in keep)
for ink,n in cc.most_common(8): print(f"   {ink}: {n}")
b=open(f'{O}/nektulos.txt','rb').read()
print("CRLF OK" if sum(1 for i,ch in enumerate(b) if ch==10 and (i==0 or b[i-1]!=13))==0 else "BAD")
