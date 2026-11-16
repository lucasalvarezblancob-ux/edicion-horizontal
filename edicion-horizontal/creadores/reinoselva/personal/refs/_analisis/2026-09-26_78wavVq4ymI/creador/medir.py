import cv2, sys, numpy as np
v='2026-09-26_78wavVq4ymI.mp4'
cap=cv2.VideoCapture(v)
def bbox(m):
    ys,xs=np.where(m)
    if len(xs)<50: return None
    x0,x1=np.percentile(xs,[0.5,99.5]); y0,y1=np.percentile(ys,[0.5,99.5])
    return [round(x0/12.8,1),round(y0/7.2,1),round(x1/12.8,1),round(y1/7.2,1)]
for a,b in [(float(x.split('-')[0]),float(x.split('-')[1])) for x in sys.argv[1:]]:
    cap.set(cv2.CAP_PROP_POS_MSEC,(a-1)*1000)
    prev=None
    while True:
        ok,f=cap.read()
        if not ok: break
        t=cap.get(cv2.CAP_PROP_POS_MSEC)/1000
        if t<a: continue
        if t>b: break
        B,G,R=[f[:,:,i].astype(int) for i in range(3)]
        orange=(R>225)&(G>140)&(G<215)&(B<70)
        white=(R>248)&(G>248)&(B>248)
        no=int(orange.sum()); nw=int(white.sum())
        key=(no//800,nw//800)
        if key!=prev:
            print('%.2f orange=%d %s white=%d %s'%(t,no,bbox(orange),nw,bbox(white)))
            prev=key
    print('---')
