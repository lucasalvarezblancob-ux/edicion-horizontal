import cv2, sys, numpy as np
cap=cv2.VideoCapture('2026-09-26_78wavVq4ymI.mp4')
def bbox(m):
    ys,xs=np.where(m)
    if len(xs)<50: return None
    x0,x1=np.percentile(xs,[0.5,99.5]); y0,y1=np.percentile(ys,[0.5,99.5])
    return [float(round(x0/12.8,1)),float(round(y0/7.2,1)),float(round(x1/12.8,1)),float(round(y1/7.2,1))]
for arg in sys.argv[1:]:
    a,b=map(float,arg.split('-'))
    cap.set(cv2.CAP_PROP_POS_MSEC,(a-1)*1000)
    rows=[]
    while True:
        ok,f=cap.read()
        if not ok: break
        t=cap.get(cv2.CAP_PROP_POS_MSEC)/1000
        if t<a: continue
        if t>b: break
        B,G,R=[f[:,:,i].astype(int) for i in range(3)]
        o=(R>225)&(G>140)&(G<215)&(B<70); w=(R>248)&(G>248)&(B>248)
        rows.append((t,int(o.sum()),int(w.sum()),bbox(o),bbox(w)))
    base_w=min(r[2] for r in rows)
    def edges(idx,thr,name):
        on=[r[0] for r in rows if r[idx]>thr]
        if on: print(name,'primer %.2f ultimo %.2f'%(on[0],on[-1]))
    edges(1,400,'naranja'); 
    on=[r[0] for r in rows if r[2]>base_w+4000]
    if on: print('blanco primer %.2f ultimo %.2f'%(on[0],on[-1]))
    mo=max(r[1] for r in rows); mw=max(r[2] for r in rows)
    full=[r for r in rows if r[1]>0.9*mo]
    if full and mo>400: print('naranja pleno desde %.2f hasta %.2f'%(full[0][0],full[-1][0]))
    fw=[r for r in rows if r[2]>0.85*mw]
    print('blanco pleno desde %.2f hasta %.2f'%(fw[0][0],fw[-1][0]))
    for r in rows[::30]: print('  %.2f o=%d w=%d %s %s'%r)
    print('---')
