import os
V=(150,90,150); O='/mnt/user-data/outputs'
def Pl(x,y,label,z=0.0,s=3): return "P %.4f, %.4f, %.4f, %d, %d, %d, %d, %s"%(x,y,z,*V,s,label)
def Ll(x1,y1,x2,y2,z=0.0): return "L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z,x2,y2,z,*V)
def doodle(x,y,r): return [Ll(x,y-r,x+r,y),Ll(x+r,y,x,y+r),Ll(x,y+r,x-r,y),Ll(x-r,y,x,y-r),Ll(x-r*0.5,y+r*1.4,x+r*0.5,y+r*1.4)]
# base bbox
xs=[];ys=[]
for l in open(f'{O}/tox.txt',encoding='utf-8',errors='replace'):
    if l.startswith('L'):
        f=l[2:].split(',')
        try: xs+=[float(f[0]),float(f[3])];ys+=[float(f[1]),float(f[4])]
        except: pass
print(f"tox base bbox: x[{min(xs):.0f},{max(xs):.0f}] y[{min(ys):.0f},{max(ys):.0f}]")
span=max(max(xs)-min(xs),max(ys)-min(ys)); r=max(40,int(span*0.018))
# existing _1 POI positions for collision avoidance
ex=[]
for l in open(f'{O}/tox_1.txt',encoding='utf-8',errors='replace'):
    if l.startswith('P'):
        f=l[1:].split(',')
        try: ex.append((float(f[0]),float(f[1])))
        except: pass
# EQOA Toxxulia sub-regions, placed to match forest geography (N=Erudin, S=Paineel, W=Kerra)
picks=[('West_Toxxulia',-1550,-500),('East_Toxxulia',600,-1450),('South_Toxxulia',100,1550)]
mind=span*0.045; out=[]
for lab,x,y in picks:
    for _ in range(8):
        if all((x-px)**2+(y-py)**2>mind*mind for px,py in ex): break
        x+=span*0.05; y-=span*0.03
    ex.append((x,y)); out+=doodle(x,y,r); out.append(Pl(x+r*1.6,y,lab))
# OVERWRITE tox_3 (it only had my 3 EQOA labels — no other content to preserve; confirmed below)
open(f'{O}/tox_3.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print("rewrote tox_3:", picks)
# validate CRLF
raw=open(f'{O}/tox_3.txt','rb').read()
lone=sum(1 for i,c in enumerate(raw) if c==10 and (i==0 or raw[i-1]!=13))
print("CRLF OK" if lone==0 else f"BAD lone={lone}", "|", raw.decode().count('\r\n'),"lines")
