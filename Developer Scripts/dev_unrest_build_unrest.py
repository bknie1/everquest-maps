"""The Estate of Unrest — haunted dwarven manor overrun by the undead. Pre-colored multi-level
map (blue = Z-level, NOT water). Recolor to a muted, cold, haunted palette."""
def parse(path):
    out=[]
    for l in open(path,encoding='utf-8',errors='replace'):
        l=l.strip()
        if l.startswith('L'):
            f=l[2:].split(','); out.append((float(f[0]),float(f[1]),float(f[2]),float(f[3]),float(f[4]),float(f[5]),(int(f[6]),int(f[7]),int(f[8]))))
    return out
B=parse('unrest.txt'); out=[]
# haunted manor palette (cold, desaturated, sickly)
MAIN=(130,140,120)   # teal Z-level -> grey-sage manor stone
LOW =(80,98,112)     # blue Z-level -> cold dark slate (lower/basement)
ACC =(172,144,82)    # gold Z-level -> tarnished candlelight / trim
for x1,y1,z1,x2,y2,z2,c in B:
    if   c==(60,190,180): nc=MAIN
    elif c==(70,110,200): nc=LOW
    elif c==(225,175,70): nc=ACC
    else: nc=c
    out.append("L %.4f, %.4f, %.4f, %.4f, %.4f, %.4f, %d, %d, %d"%(x1,y1,z1,x2,y2,z2,nc[0],nc[1],nc[2]))
open('unrest_colored.txt','w',newline='').write('\r\n'.join(out)+'\r\n')
print('unrest recolored L=%d'%len(out))
