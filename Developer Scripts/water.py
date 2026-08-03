from PIL import Image
import numpy as np

# shared calibration (px -> wiki), from detected gridlines
def px_to_wiki(px,py):
    x = 450 + (px-56)*(-750.0/411.0)     # px56->450 , px467->-300
    y = 300 + (py-81)*(-450.0/246.0)     # py81->300 , py327->-150
    return x,y
def wiki_to_native(a,b):   # validated (-b,-a)
    return (-b,-a)

FLOOR_Z={'f1':0.0,'f2':-50.0,'f3':-142.0}

def water_mask(nm):
    im=np.asarray(Image.open(nm+'.png').convert('RGB')).astype(int)
    R,G,B=im[:,:,0],im[:,:,1],im[:,:,2]
    return (B>120)&(B>R+25)&(B>G+15)

def native_water_points(nm):
    m=water_mask(nm); ys,xs=np.where(m)
    pts=[]
    for px,py in zip(xs,ys):
        a,b=px_to_wiki(px,py); nx,ny=wiki_to_native(a,b); pts.append((nx,ny))
    return np.array(pts) if len(pts) else np.zeros((0,2))

if __name__=='__main__':
    for nm in ['f1','f2','f3']:
        p=native_water_points(nm)
        if len(p): print(nm,'water native bbox x[%.0f,%.0f] y[%.0f,%.0f] n=%d'%(p[:,0].min(),p[:,0].max(),p[:,1].min(),p[:,1].max(),len(p)))
