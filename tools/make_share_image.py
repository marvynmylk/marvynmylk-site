"""Builds images/share.jpg (the link preview) from images/profile.webp and both cover images.
Run after changing any of them:  python3 tools/make_share_image.py"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); R=ROOT+"/images/"; FD=ROOT+"/tools/fonts/"
FR=lambda s: ImageFont.truetype(FD+"fraunces-latin-600-normal.woff", s)
W,H=1200,630
yy,xx=np.mgrid[0:H,0:W]
r=np.sqrt(((xx-930)/700)**2+((yy-180)/520)**2)
base=np.array([22,18,31],float); glow=np.array([70,40,98],float)
t=np.clip(1-r,0,1)[...,None]**1.6
arr=base+(glow-base)*t
arr+=np.random.default_rng(3).normal(0,5,(H,W,1))
im=Image.fromarray(np.clip(arr,0,255).astype(np.uint8)).convert("RGBA")

def shadowed(layer, pos, blur=18, off=(0,22), alpha=170):
    a=layer.getchannel("A"); sh=Image.new("RGBA",layer.size,(0,0,0,0)); sh.putalpha(a.point(lambda v: v*alpha//255))
    pad=60; big=Image.new("RGBA",(layer.width+2*pad,layer.height+2*pad),(0,0,0,0)); big.paste(sh,(pad,pad),sh)
    big=big.filter(ImageFilter.GaussianBlur(blur)); im.alpha_composite(big,(pos[0]-pad+off[0],pos[1]-pad+off[1])); im.alpha_composite(layer,pos)

def cover(fn,h,ang):
    c=Image.open(R+fn).convert("RGBA"); c=c.resize((round(c.width*h/c.height),h),Image.LANCZOS)
    return c.rotate(ang,expand=True,resample=Image.BICUBIC)
c1=cover("purple-south-cover.jpg",350,-4); c2=cover("monster-on-tv-cover.jpg",350,4)
shadowed(c1,(690,92)); shadowed(c2,(915,122))
p=Image.open(R+"profile.webp").convert("RGBA").resize((190,190),Image.LANCZOS)
shadowed(p,(628,405),blur=14,off=(0,16),alpha=200)

d=ImageDraw.Draw(im)
CREAM=(251,239,216)
lines=["Talking politics","with logic","& empathy","in the"]
y=122
for ln in lines:
    d.text((64,y),ln,font=FR(70),fill=CREAM); y+=80
# gradient last line
f=FR(74); txt="purple South."
bb=d.textbbox((0,0),txt,font=f); w,h=bb[2]+4,bb[3]+12
mask=Image.new("L",(w,h),0); ImageDraw.Draw(mask).text((0,0),txt,font=f,fill=255)
g=np.linspace(0,1,w)[None,:,None]
stops=[np.array(c,float) for c in [(201,167,232),(232,163,195),(243,179,122)]]
col=np.where(g<.55, stops[0]+(stops[1]-stops[0])*(g/.55), stops[1]+(stops[2]-stops[1])*((g-.55)/.45))
grad=Image.fromarray(np.repeat(col,h,0).astype(np.uint8)).convert("RGBA"); grad.putalpha(mask)
im.alpha_composite(grad,(64,y+6))
im.convert("RGB").save(R+"share.jpg",quality=88)
