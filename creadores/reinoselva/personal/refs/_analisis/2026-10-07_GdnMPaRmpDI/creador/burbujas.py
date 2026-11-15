import cv2, numpy as np, json, sys
cap=cv2.VideoCapture(sys.argv[1]); fps=cap.get(cv2.CAP_PROP_FPS); n=0; out=[]
step=int(round(fps/2))
while True:
    if not cap.grab(): break
    if n%step==0:
        ok,f=cap.retrieve()
        if not ok: break
        f=cv2.resize(f,(640,360)); g=f.min(axis=2)
        w=(g>232).astype(np.uint8)
        k,lab,st,_=cv2.connectedComponentsWithStats(w,8)
        hits=[]
        for i in range(1,k):
            x,y,bw,bh,a=st[i]
            if a<1500 or a>25000: continue
            if bw/bh<1.3 or bw/bh>7: continue
            if a/(bw*bh)<0.45: continue
            m=(lab==i).astype(np.uint8)
            ring=cv2.dilate(m,np.ones((9,9),np.uint8))-cv2.dilate(m,np.ones((3,3),np.uint8))
            dark=(f.max(axis=2)<70)&(ring>0)
            fr=dark.sum()/max(1,ring.sum())
            if fr>0.45: hits.append([int(x),int(y),int(bw),int(bh),round(float(fr),2)])
        # color tortuga: amarillo-naranja muy saturado
        hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
        t=((hsv[...,0]>=12)&(hsv[...,0]<=26)&(hsv[...,1]>200)&(hsv[...,2]>215)).sum()
        out.append({"t":round(n/fps,2),"b":hits,"am":int(t)})
    n+=1
json.dump({"fps":fps,"frames":n,"d":out},open(sys.argv[2],"w"))
print(fps,n)
