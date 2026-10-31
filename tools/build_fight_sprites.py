#!/usr/bin/env python3
"""Pack the side-view fight frames (fr/*.png + meta.json from tools/fight/rend.js) into img/sk/fight.webp/json.
Same key-colour normalisation and dark outline as the skating atlas, so getKit() recolours it for each team.
Frame = [x,y,w,h, footX,footY, rHandX,rHandY, headX,headY] in atlas pixels."""
import json,sys,os
import numpy as np
from PIL import Image, ImageFilter
SRC,OUT=sys.argv[1],sys.argv[2]; PPM=float(sys.argv[3]) if len(sys.argv)>3 else 0.6
Q=int(sys.argv[4]) if len(sys.argv)>4 else 0
REF=np.array([245,240,190],dtype=np.float32)
meta=json.load(open(os.path.join(SRC,'meta.json')))
def classify(a):
    r,g,b=[a[...,i].astype(np.float32) for i in range(3)]
    mx=np.maximum(np.maximum(r,g),b); mn=np.minimum(np.minimum(r,g),b); dl=np.maximum(mx-mn,1e-6)
    h=np.where(mx==r,((g-b)/dl)%6,np.where(mx==g,(b-r)/dl+2,(r-g)/dl+4))*60
    ok=(mx>=40)&((mx-mn)>=.38*mx)&(a[...,3]>8)
    cls=np.full(r.shape,-1); cls[ok&(h>=242)&(h<345)]=0; cls[ok&(h>=150)&(h<242)]=1; cls[ok&(h>=70)&(h<150)]=2
    return cls
frames=[]
for name,m in meta.items():
    im=Image.open(os.path.join(SRC,name+'.png')).convert('RGBA')
    pts=[m['anchor'],m['hand'][0],m['head']]
    bb=im.getchannel('A').point(lambda v:255 if v>20 else 0).getbbox(); pad=8
    bb=(bb[0]-pad,bb[1]-pad,bb[2]+pad,bb[3]+pad); im=im.crop(bb)
    w,h=im.size; nw,nh=round(w*PPM),round(h*PPM); im=im.resize((nw,nh),Image.LANCZOS)
    pts=[((x-bb[0])*nw/w+4,(y-bb[1])*nh/h+4) for x,y in pts]
    a=np.array(im); cls=classify(a); af=a.astype(np.float32)
    for c in range(3):
        k=cls==c; af[k,:3]*=REF[c]/255.0
    im=Image.fromarray(np.clip(af,0,255).astype(np.uint8),'RGBA')
    al=im.getchannel('A').point(lambda v:255 if v>40 else 0).filter(ImageFilter.MaxFilter(5))
    ol=Image.new('RGBA',im.size,(12,10,16,255)); ol.putalpha(al); big=Image.new('RGBA',(nw+8,nh+8),(0,0,0,0)); big.alpha_composite(ol,(4,4)); big.alpha_composite(im,(4,4))
    frames.append((name,big,pts))
frames.sort(key=lambda f:-f[1].height)
W=2048; x=y=rowh=0; place={}
for name,im,pts in frames:
    if x+im.width>W: x=0; y+=rowh+1; rowh=0
    place[name]=[x,y,im.width,im.height]+[round(v,1) for p in pts for v in p]; x+=im.width+1; rowh=max(rowh,im.height)
H=y+rowh+1; atlas=Image.new('RGBA',(W,H),(0,0,0,0))
for name,im,_ in frames: atlas.paste(im,tuple(place[name][:2]))
if Q: atlas.save(os.path.join(OUT,'fight.webp'),quality=Q,method=6,alpha_quality=90)
else: atlas.save(os.path.join(OUT,'fight.webp'),lossless=True,method=6)
json.dump({'frames':place,'ppm':PPM,'ppmSrc':900/2.9},open(os.path.join(OUT,'fight.json'),'w'),separators=(',',':'))
print(W,H,len(place),os.path.getsize(os.path.join(OUT,'fight.webp'))//1024,'KB')
