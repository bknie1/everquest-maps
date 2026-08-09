import math, random
random.seed(5)

def najena_arch_segs():
    segs=[]
    def seg(x1,y1,x2,y2): segs.append((x1,y1,x2,y2))
    def poly(pts,close=False):
        for i in range(len(pts)-1): seg(*pts[i],*pts[i+1])
        if close: seg(*pts[-1],*pts[0])
    # cliff outline
    poly([(20,300),(30,160),(90,90),(150,120),(210,60),(280,30),(360,55),(430,110),(500,95),(540,180),(530,300)])
    seg(22,300,60,660); seg(532,300,500,660)
    for yy in range(320,650,34): seg(30,yy,64,yy+16); seg(500,yy,470,yy+16)
    for x0,x1,y0 in [(35,150,150),(410,525,150)]:
        for i in range(0,int(x1-x0),16): seg(x0+i,y0,x0+i+55,y0+95)
    # lintel + runes
    poly([(150,200),(410,200),(410,250),(150,250)],close=True)
    gx=166
    for r in ['tri','bars','eye','dia','eye','bars','tri']:
        gy=225
        if r=='tri': poly([(gx,gy+8),(gx+7,gy-8),(gx+14,gy+8)],close=True)
        elif r=='dia': poly([(gx+7,gy-9),(gx+14,gy),(gx+7,gy+9),(gx,gy)],close=True)
        elif r=='bars':
            for b in range(3): seg(gx+b*5,gy-8,gx+b*5,gy+8)
        else:
            poly([(gx,gy),(gx+4,gy-5),(gx+11,gy-5),(gx+15,gy),(gx+11,gy+5),(gx+4,gy+5)],close=True)
        gx+=34
    kx,ky=280,232
    poly([(kx-10,ky-2),(kx-9,ky-13),(kx,ky-16),(kx+9,ky-13),(kx+10,ky-2),(kx+6,ky+9),(kx-6,ky+9)],close=True)
    seg(kx-5,ky-2,kx-3,ky-2); seg(kx+3,ky-2,kx+5,ky-2); seg(kx,ky+1,kx,ky+5)
    for t in range(-4,6,3): seg(kx+t,ky+9,kx+t,ky+13)
    # pillars
    for px in (170,372):
        seg(px,250,px,600); seg(px+26,250,px+26,600); seg(px-6,250,px+32,250); seg(px-8,600,px+34,600)
        for by in range(280,596,32): seg(px,by,px+26,by)
        for hx in range(4,26,7): seg(px+hx,258,px+hx,594)
    # portal trapezoid
    def leftE(y): return 235-35*(y-250)/360
    def rightE(y): return 325+35*(y-250)/360
    seg(235,250,200,610); seg(325,250,360,610); seg(235,250,325,250)
    # --- standing broken door, hinged LEFT jamb, leaning INWARD (top recedes into dark) ---
    door=[(232,258),(300,282),(288,582),(204,598)]
    poly(door,close=True)
    for t in (0.22,0.42,0.62,0.82):  # planks across the leaning face
        hx=232+(204-232)*t; hy=258+(598-258)*t
        fx=300+(288-300)*t; fy=282+(582-282)*t
        seg(hx,hy,fx,fy)
    # dark opening: hatch the RIGHT part not covered by the door
    for y in range(268,606,15):
        lx=max(leftE(y),302); rx=rightE(y)
        if rx>lx: seg(lx,y,rx,y)
    for bx in (312,330,348):
        if bx<rightE(600): seg(bx,262,bx,606)
    # --- fallen door lying flat in foreground ---
    far=[(215,600),(345,600)]; near=[(170,690),(408,690)]
    poly([far[0],far[1],near[1],near[0]],close=True)
    for t in (0.2,0.4,0.6,0.8):
        fx=far[0][0]+(far[1][0]-far[0][0])*t; nx=near[0][0]+(near[1][0]-near[0][0])*t
        seg(fx,600,nx,690)
    seg(197,630,372,630); seg(184,660,392,660)
    for sx,sy in [(240,645),(320,645),(280,672)]: poly([(sx-4,sy),(sx,sy-4),(sx+4,sy),(sx,sy+4)],close=True)
    seg(120,692,470,692)
    for rx in (140,300,450): poly([(rx-11,692),(rx-4,684),(rx+5,686),(rx+11,692)])
    seg(150,300,178,362); seg(405,320,380,398)
    return segs

