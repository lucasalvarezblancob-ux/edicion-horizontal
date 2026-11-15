import cv2, numpy as np
V="2026-10-07_GdnMPaRmpDI.mp4"
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS)
def fr(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,int(round(t*fps))-2)); cap.read(); cap.read(); ok,f=cap.read(); return f
# boton
f=fr(176.0); H,W=f.shape[:2]
hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
red=(((hsv[...,0]<6)|(hsv[...,0]>174))&(hsv[...,1]>200)&(hsv[...,2]>180)).astype(np.uint8)
k,lab,st,_=cv2.connectedComponentsWithStats(red,8); i=1+np.argmax(st[1:,4]); x,y,w,h,a=st[i]
print('boton rojo %',[round(100*x/W,1),round(100*y/H,1),round(100*(x+w)/W,1),round(100*(y+h)/H,1)],a)
wh=(f.min(axis=2)>240).astype(np.uint8); wh[:int(H*0.5)]=0
k,lab,st,_=cv2.connectedComponentsWithStats(wh,8); i=1+np.argmax(st[1:,4]); x,y,w,h,a=st[i]
print('boton barra blanca %',[round(100*x/W,1),round(100*y/H,1),round(100*(x+w)/W,1),round(100*(y+h)/H,1)],a)
# alturas de rotulos: componentes blancos con borde oscuro
def letras(t,y0=0.0,y1=1.0,x0=0.0,x1=1.0,thr=225):
    f=fr(t); g=f.min(axis=2); mx=f.max(axis=2)
    wm=(g>thr).astype(np.uint8); near=cv2.dilate((mx<70).astype(np.uint8),np.ones((9,9),np.uint8))
    k,lab,st,_=cv2.connectedComponentsWithStats(wm,8); hs=[];bx=[]
    for i in range(1,k):
        x,y,w,h,a=st[i]
        if a<40 or h<14 or h>160 or w>200: continue
        if not (y0*H<=y<=y1*H and x0*W<=x<=x1*W): continue
        m=(lab[y:y+h,x:x+w]==i)
        if near[y:y+h,x:x+w][m].mean()>0.5: hs.append(h); bx.append((x,y,x+w,y+h))
    if not hs: print(t,'nada'); return
    b=np.array(bx); print(t,'n',len(hs),'alto mediana px',np.median(hs),'= %.1f%%'%(100*np.median(hs)/H),'caja %',[round(100*b[:,0].min()/W,1),round(100*b[:,1].min()/H,1),round(100*b[:,2].max()/W,1),round(100*b[:,3].max()/H,1)])
for t,a in [(6.2,(0.5,1)),(342.2,(0.3,1)),(381,(0.4,1)),(423.2,(0.4,1)),(479.2,(0.4,1)),(482.5,(0,0.6)),(494.8,(0.4,1)),(680,(0.6,1)),(1022.8,(0.3,1)),(1079,(0.4,1)),(1166.5,(0.4,1)),(1168.1,(0.3,1)),(1264.6,(0.4,1))]:
    letras(t,a[0],a[1])
# logo intro
f=fr(22.5); hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
m=((hsv[...,0]>=10)&(hsv[...,0]<=28)&(hsv[...,1]>170)&(hsv[...,2]>190)).astype(np.uint8)
ys,xs=np.where(m>0); print('logo intro tortuga amarilla %',[round(100*xs.min()/W,1),round(100*ys.min()/H,1),round(100*xs.max()/W,1),round(100*ys.max()/H,1)])
# outro: bucle?
sig=[]
ts=np.arange(1366.0,1385.8,0.25)
for t in ts:
    g=cv2.cvtColor(cv2.resize(fr(float(t)),(64,36)),cv2.COLOR_BGR2GRAY).astype(np.float32); sig.append(g)
sig=np.array(sig)
for i in range(0,len(ts),4):
    d=[(float(np.abs(sig[i]-sig[j]).mean()),float(ts[j])) for j in range(len(ts)) if abs(j-i)>6]
    d.sort(); print('outro t=%.2f parecido a'%ts[i],[(round(a,1),b) for a,b in d[:3]])
