import cv2, numpy as np, sys
V="2026-10-07_GdnMPaRmpDI.mp4"
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS)
for a in sys.argv[1:]:
    t,name=a.split(':')
    t=float(t); cap.set(cv2.CAP_PROP_POS_FRAMES,int(round(t*fps))-1); cap.read(); ok,f=cap.read()
    H,W=f.shape[:2]
    if name!='-': cv2.imwrite(f"_analisis/2026-10-07_GdnMPaRmpDI/creador/{name}.jpg",f,[cv2.IMWRITE_JPEG_QUALITY,92])
    hsv=cv2.cvtColor(f,cv2.COLOR_BGR2HSV)
    m=((hsv[...,0]>=10)&(hsv[...,0]<=28)&(hsv[...,1]>190)&(hsv[...,2]>200)).astype(np.uint8)
    m=cv2.morphologyEx(m,cv2.MORPH_CLOSE,np.ones((25,25),np.uint8))
    k,lab,st,_=cv2.connectedComponentsWithStats(m,8)
    tb=None
    if k>1:
        i=1+np.argmax(st[1:,4]); x,y,w,h,ar=st[i]
        tb=[round(100*(x-6)/W,1),round(100*(y-6)/H,1),round(100*min(W,x+w+6)/W,1),round(100*min(H,y+h+6)/H,1),int(ar)]
    g=f.min(axis=2); wm=(g>235).astype(np.uint8)
    k,lab,st,_=cv2.connectedComponentsWithStats(wm,8)
    bb=[]
    for i in range(1,k):
        x,y,w,h,ar=st[i]
        if ar<5000 or w/h<1.3 or w/h>7 or ar/(w*h)<0.4: continue
        mm=(lab==i).astype(np.uint8)
        ring=cv2.dilate(mm,np.ones((15,15),np.uint8))-cv2.dilate(mm,np.ones((3,3),np.uint8))
        fr=((f.max(axis=2)<70)&(ring>0)).sum()/max(1,ring.sum())
        if fr>0.35: bb.append([round(100*(x-5)/W,1),round(100*(y-5)/H,1),round(100*(x+w+5)/W,1),round(100*(y+h+5)/H,1),round(float(fr),2)])
    print(t,name,'tortuga',tb,'burbuja',bb)
