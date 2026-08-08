import cairosvg, math, random
random.seed(11)
W,Ht=620,400
# desaturated, foggy Nektulos palette
FIR=(88,104,86); DEAD=(104,104,98); WILLOW=(96,110,82); WEB=(150,154,148); FOG=(176,180,174); TRUNK=(84,80,74)
def P(pts,col,w=1.6,close=False,dash=None):
    d=' '.join(f'{"M" if i==0 else "L"}{x:.1f},{y:.1f}' for i,(x,y) in enumerate(pts))
    if close:d+=' Z'
    da=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" fill="none" stroke="rgb{col}" stroke-width="{w}"{da} stroke-linecap="round"/>'
S=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{Ht}" viewBox="0 0 {W} {Ht}">',
   f'<rect width="{W}" height="{Ht}" fill="#eef0ea"/>']  # pale foggy ground

# --- 1) normal FIR (Faydark shape, desaturated) ---
def fir(cx,base,h,col):
    out=[P([(cx,base),(cx,base-h*0.15)],TRUNK,2)]  # trunk
    tiers=4
    for i in range(tiers):
        ty=base-h*0.12-(h*0.82)*i/tiers
        wv=h*0.30*(1-i/tiers*0.7)
        out.append(P([(cx-wv,ty),(cx,ty-h*0.9/tiers),(cx+wv,ty)],col,1.5,close=True))
    return out
S+=fir(150,300,190,FIR)
S+=fir(95,315,120,FIR)          # smaller one behind, same shape

# --- 2) DEAD / broken tree (a few, mixed in) ---
def dead(cx,base,h):
    out=[P([(cx,base),(cx,base-h)],DEAD,2)]
    for (fy,ang,ln) in [(0.55,-0.6,0.42),(0.4,0.7,0.5),(0.72,0.5,0.3),(0.3,-0.9,0.34),(0.62,-0.3,0.26)]:
        by=base-h*fy
        ex=cx+math.cos(-math.pi/2+ang)*h*ln; ey=by+math.sin(-math.pi/2+ang)*h*ln
        out.append(P([(cx,by),(ex,ey)],DEAD,1.4))
        # a snapped fork
        out.append(P([(ex,ey),(ex+random.uniform(-8,8),ey-random.uniform(6,14))],DEAD,1.1))
    return out
S+=dead(330,300,170)

# --- 3) WILLOW (drooping, muted olive) ---
def willow(cx,base,h):
    out=[P([(cx,base),(cx,base-h*0.6)],TRUNK,2)]
    crown=base-h*0.6
    out.append(f'<ellipse cx="{cx}" cy="{crown}" rx="{h*0.32}" ry="{h*0.16}" fill="none" stroke="rgb{WILLOW}" stroke-width="1.4"/>')
    for k in range(9):
        sx=cx-h*0.30+ k*(h*0.60/8)
        sway=random.uniform(-6,8)
        out.append(P([(sx,crown+2),(sx+sway*0.5,crown+h*0.22),(sx+sway,crown+h*0.42)],WILLOW,1.1))
    return out
S+=willow(500,300,175)

# --- 4) SPIDER WEB strung between the fir and the dead tree ---
ax,ay=185,150; bx,by=305,165   # anchors up in the branches
cx2,cy2=(ax+bx)/2+6,(ay+by)/2+55
# frame
S.append(P([(ax,ay),(cx2,cy2)],WEB,1)); S.append(P([(bx,by),(cx2,cy2)],WEB,1))
S.append(P([(ax,ay),(ax-6,ay+70)],WEB,1)); S.append(P([(bx,by),(bx+8,by+72)],WEB,1))
# radial spokes
import math as m
spokes=[(ax,ay),(bx,by),(ax-6,ay+70),(bx+8,by+72),(cx2,cy2)]
for sx,sy in spokes: S.append(P([(cx2-(cx2-sx)*0.02,cy2-(cy2-sy)*0.02),(sx,sy)],WEB,0.8))
# spiral rings
for r in (0.28,0.5,0.72,0.9):
    ring=[]
    for sx,sy in spokes+[spokes[0]]:
        ring.append((cx2+(sx-cx2)*r, cy2+(sy-cy2)*r))
    S.append(P(ring,WEB,0.8))

# --- fog: faint horizontal wisps low across the scene ---
for fy in (250,285,320):
    pts=[(x, fy+8*m.sin(x/55.0)) for x in range(20,W-20,14)]
    S.append(P(pts,FOG,1.0))

# labels
def txt(x,y,t,col,sz=13):
    return f'<text x="{x}" y="{y}" font-size="{sz}" font-family="serif" fill="rgb{col}">{t}</text>'
S.append(txt(120,340,'fir (normal shape)',FIR)); S.append(txt(300,340,'dead / broken',DEAD))
S.append(txt(470,340,'willow',WILLOW)); S.append(txt(210,120,'spider web',WEB))
S.append('</svg>')
cairosvg.svg2png(bytestring=''.join(S).encode(),write_to='/mnt/user-data/outputs/_nektulos_tree_study.png',output_width=W*2,output_height=Ht*2)
print("nektulos tree study rendered")
