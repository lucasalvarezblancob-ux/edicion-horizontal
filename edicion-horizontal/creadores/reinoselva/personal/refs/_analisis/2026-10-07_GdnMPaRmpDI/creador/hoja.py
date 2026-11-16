# uso: hoja.py salida.jpg t0 paso n cols ancho [x0 y0 x1 y1 en fraccion]
import cv2, sys, numpy as np
V="2026-10-07_GdnMPaRmpDI.mp4"
out=sys.argv[1]; t0=float(sys.argv[2]); paso=float(sys.argv[3]); n=int(sys.argv[4]); cols=int(sys.argv[5]); W=int(sys.argv[6])
box=[float(x) for x in sys.argv[7:11]] if len(sys.argv)>=11 else [0,0,1,1]
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS)
cells=[]
first=int(round(t0*fps)); cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,first-1)); cur=max(0,first-1)
want=[int(round((t0+i*paso)*fps)) for i in range(n)]
wi=0; f=None
while wi<n:
    ok,fr=cap.read()
    if not ok: break
    if cur>=want[wi]:
        h,w=fr.shape[:2]
        c=fr[int(box[1]*h):int(box[3]*h), int(box[0]*w):int(box[2]*w)]
        c=cv2.resize(c,(W,int(round(W*c.shape[0]/c.shape[1]))),interpolation=cv2.INTER_AREA)
        lab="%.2f"%(cur/fps)
        cv2.rectangle(c,(0,0),(12*len(lab)+6,20),(0,0,0),-1)
        cv2.putText(c,lab,(3,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
        cells.append(c)
        while wi<n and cur>=want[wi]: wi+=1
    cur+=1
rows=[]
for i in range(0,len(cells),cols):
    r=cells[i:i+cols]
    while len(r)<cols: r.append(np.zeros_like(cells[0]))
    rows.append(np.hstack(r))
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,88])
print(out,fps,len(cells))
