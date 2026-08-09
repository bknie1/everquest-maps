"""Rebuild lavastorm_2 from the repo original (restores the bottom border that was
knocked out), then re-place the Najena archway and the Druid Ring.

Brandon reports the archway reads UPSIDE DOWN in game, so both perspective sketches
are placed with local-top -> native-large-y (the opposite of my previous convention).
"""
import sys, math, json
sys.path.insert(0,'/home/claude/work')
from druid_ring import druid_ring_segs
from arch_segs import najena_arch_segs

O='/mnt/user-data/outputs'
REPO='/home/claude/work/maps_repo/Maps Repo/Emoda Legends Maps'

def bbox_lines(lines):
    xs=[];ys=[]
    for l in lines:
        f=l[2:].split(',')
        xs+=[float(f[0]),float(f[3])]; ys+=[float(f[1]),float(f[4])]
    return min(xs),max(xs),min(ys),max(ys)

raw=[l.rstrip('\r\n') for l in open(f'{REPO}/lavastorm_2.txt',encoding='utf-8',errors='replace') if l.strip()]
head=[l for l in raw if not l.startswith('L')]
lines=[l for l in raw if l.startswith('L')]
fx0,fx1,fy0,fy1=bbox_lines(lines)
bl=[l.rstrip('\r\n') for l in open(f'{O}/lavastorm.txt',encoding='utf-8',errors='replace') if l.startswith('L')]
bx0,bx1,by0,by1=bbox_lines(bl)
print(f"frame x[{fx0:.0f},{fx1:.0f}] y[{fy0:.0f},{fy1:.0f}]  base x[{bx0:.0f},{bx1:.0f}] y[{by0:.0f},{by1:.0f}]")

def place(segs, ink, band, height_frac, bottom_pad_frac=0.0):
    """band = (mx0,mx1,my0,my1). FLIPPED: local top -> native large y."""
    lminx=min(min(s[0],s[2]) for s in segs); lmaxx=max(max(s[0],s[2]) for s in segs)
    lminy=min(min(s[1],s[3]) for s in segs); lmaxy=max(max(s[1],s[3]) for s in segs)
    mx0,mx1,my0,my1=band
    availw=(mx1-mx0)*0.80
    availh=(my1-my0)*(1.0-bottom_pad_frac)*0.80
    s=min(availw/(lmaxx-lminx), availh/(lmaxy-lminy), (by1-by0)*height_frac/(lmaxy-lminy))
    cx=(mx0+mx1)/2
    cy=(my0+my1)/2 - (my1-my0)*bottom_pad_frac*0.5      # lift off the bottom border
    NX0=cx-(lminx+lmaxx)/2*s
    def tx(x): return NX0+x*s
    def ty(y): return cy+((lmaxy+lminy)/2 - y)*(-s)      # FLIPPED
    out=[f"L {tx(a):.2f}, {ty(b):.2f}, 0.0000, {tx(c):.2f}, {ty(d):.2f}, 0.0000, {ink[0]}, {ink[1]}, {ink[2]}"
         for a,b,c,d in segs]
    nxs=[tx(x) for sg in segs for x in (sg[0],sg[2])]; nys=[ty(y) for sg in segs for y in (sg[1],sg[3])]
    return out,(min(nxs),max(nxs),min(nys),max(nys))

# Druid Ring -> NW margin band
ring,rb = place(druid_ring_segs(), (92,70,60), (fx0,bx0,fy0,by0), 0.12)
# Najena archway -> SE margin band, lifted for extra bottom margin
arch,ab = place(najena_arch_segs(), (80,58,50), (bx1,fx1,by1,fy1), 0.17, bottom_pad_frac=0.30)
print(f"  ring x[{rb[0]:.0f},{rb[1]:.0f}] y[{rb[2]:.0f},{rb[3]:.0f}]")
print(f"  arch x[{ab[0]:.0f},{ab[1]:.0f}] y[{ab[2]:.0f},{ab[3]:.0f}]   (frame bottom {fy1:.0f})")
open(f'{O}/lavastorm_2.txt','w',newline='').write('\r\n'.join(head+lines+ring+arch)+'\r\n')
b=open(f'{O}/lavastorm_2.txt','rb').read()
print("lavastorm_2 rebuilt:",len(lines),"original +",len(ring),"ring +",len(arch),"arch |",
      "CRLF OK" if sum(1 for i,c in enumerate(b) if c==10 and (i==0 or b[i-1]!=13))==0 else "BAD")

# same flip for the other two druid rings
for zone,ink,corner in [('feerrott',(70,86,58),'NE'),('misty',(78,92,60),'SW')]:
    p2=f'{O}/{zone}_2.txt'
    raw=[l.rstrip('\r\n') for l in open(p2,encoding='utf-8',errors='replace') if l.strip()]
    head2=[l for l in raw if not l.startswith('L')]
    ls=[l for l in raw if l.startswith('L') and tuple(int(v) for v in l[2:].split(',')[6:9])!=ink]
    f0,f1,g0,g1=bbox_lines(ls)
    bl2=[l.rstrip('\r\n') for l in open(f'{O}/{zone}.txt',encoding='utf-8',errors='replace') if l.startswith('L')]
    c0,c1,d0,d1=bbox_lines(bl2)
    band=((c1,f1,g0,d0) if corner=='NE' else (f0,c0,d1,g1))
    r2,rb2=place(druid_ring_segs(), ink, band, 0.12)
    open(p2,'w',newline='').write('\r\n'.join(head2+ls+r2)+'\r\n')
    print(f"  {zone}: ring re-placed flipped x[{rb2[0]:.0f},{rb2[1]:.0f}] y[{rb2[2]:.0f},{rb2[3]:.0f}]")
