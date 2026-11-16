import cv2, numpy as np, sys
V="2026-10-07_GdnMPaRmpDI.mp4"
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS)
for a in sys.argv[1:]:
    t0,t1,side=a.split(':'); t0=float(t0); t1=float(t1)
    f0=int(round(t0*fps)); cap.set(cv2.CAP_PROP_POS_FRAMES,f0-1); cap.read(); n=f0
    print('==',a)
    line=[]
    while n/fps<=t1:
        ok,f=cap.read()
        if not ok: break
        if (n-f0)%6==0:
            H,W=f.shape[:2]
            roi=f[int(H*0.4):, (W//2 if side=='d' else 0):(W if side=='d' else W//2)]
            hsv=cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
            m=((hsv[...,0]>=10)&(hsv[...,0]<=28)&(hsv[...,1]>190)&(hsv[...,2]>200))
            ys=np.where(m.sum(axis=1)>8)[0]
            top=round(100*(ys.min()+H*0.4)/H) if m.sum()>800 else -1
            g=roi.min(axis=2); wm=(g>235).astype(np.uint8)
            k,lab,st,_=cv2.connectedComponentsWithStats(wm,8)
            bw=0;txt=0
            for i in range(1,k):
                x,y,w,h,ar=st[i]
                if ar<4000 or w/h<1.3 or w/h>7 or ar/(w*h)<0.4: continue
                bw=round(100*w/W); sub=roi[y+6:y+h-6,x+10:x+w-10]
                txt=int((sub.max(axis=2)<90).sum())
            line.append(f"{n/fps:.1f}:y{top}/b{bw}/t{txt}")
        n+=1
    print(' '.join(line))
