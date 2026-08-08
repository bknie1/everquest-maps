import os
V=(150,90,150); O='/mnt/user-data/outputs'
def Pl(x,y,label,z=0.0,s=3): return "P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,z,*V,s,label)
def Ll(x1,y1,x2,y2,z=0.0): return "L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,*V)
def doodle(x,y,r): return [Ll(x,y-r,x+r,y),Ll(x+r,y,x,y+r),Ll(x,y+r,x-r,y),Ll(x-r,y,x,y-r),Ll(x-r*0.5,y+r*1.4,x+r*0.5,y+r*1.4)]
def bbox(zone):
    xs=[];ys=[]
    for l in open(f'{O}/{zone}.txt',encoding='utf-8',errors='replace'):
        if l.startswith('L'):
            f=l[2:].split(',')
            try: xs+=[float(f[0]),float(f[3])];ys+=[float(f[1]),float(f[4])]
            except: pass
    return min(xs),max(xs),min(ys),max(ys)
def epts(zone):
    pts=[]
    for suf in ['_1','_3']:
        p=f'{O}/{zone}{suf}.txt'
        if os.path.exists(p):
            for l in open(p,encoding='utf-8',errors='replace'):
                if l.startswith('P'):
                    f=l[1:].split(',')
                    try: pts.append((float(f[0]),float(f[1])))
                    except: pass
    return pts
PAT={3:[(0.3,0.3),(0.62,0.5),(0.4,0.74)]}
ZL={'tox':['Sylhithis_Dwell','Arcadin','East_Plateau'],
    'stonebrunt':['North_Barren_Coast','The_Vastly_Deep','Cape_Dreg']}
for zone,labels in ZL.items():
    minx,maxx,miny,maxy=bbox(zone); w=maxx-minx;h=maxy-miny;span=max(w,h)
    r=max(40,int(span*0.018)); ex=epts(zone); mind=span*0.05; new=[]
    for i,lab in enumerate(labels):
        fx,fy=PAT[3][i]; x=minx+fx*w; y=miny+fy*h
        for _ in range(6):
            if all((x-px)**2+(y-py)**2>mind*mind for px,py in ex): break
            x+=span*0.06;y-=span*0.04
        ex.append((x,y)); new+=doodle(x,y,r); new.append(Pl(x+r*1.6,y,lab))
    p3=f'{O}/{zone}_3.txt'; old=open(p3,'rb').read() if os.path.exists(p3) else b''
    if old and not old.endswith(b'\r\n'): old+=b'\r\n'
    open(p3,'wb').write(old+('\r\n'.join(new)+'\r\n').encode())
    print(f"  {zone}_3.txt: {'APPEND' if old else 'NEW'} +{len(labels)} EQOA labels")
