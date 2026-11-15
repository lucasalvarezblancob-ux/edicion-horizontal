import cv2, numpy as np, sys
V="2026-10-07_GdnMPaRmpDI.mp4"
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS)
def fr(t):
    cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,int(round(t*fps))-2)); cap.read(); cap.read(); ok,f=cap.read(); return f
out=sys.argv[1]; cols=int(sys.argv[2]); cw=int(sys.argv[3]); cells=[]
for a in sys.argv[4:]:
    t,x0,y0,x1,y1=[float(x) for x in a.split(',')]
    f=fr(t); H,W=f.shape[:2]; c=f[int(y0*H):int(y1*H),int(x0*W):int(x1*W)]
    c=cv2.resize(c,(cw,int(cw*c.shape[0]/c.shape[1])),interpolation=cv2.INTER_AREA if cw<c.shape[1] else cv2.INTER_CUBIC)
    lab="%.1f"%t; cv2.rectangle(c,(0,0),(12*len(lab)+6,20),(0,0,0),-1); cv2.putText(c,lab,(3,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA); cells.append(c)
h=max(c.shape[0] for c in cells); cells=[cv2.copyMakeBorder(c,0,h-c.shape[0],0,0,cv2.BORDER_CONSTANT) for c in cells]
rows=[]
for i in range(0,len(cells),cols):
    r=cells[i:i+cols]
    while len(r)<cols: r.append(np.zeros_like(cells[0]))
    rows.append(np.hstack(r))
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,90]); print(out,len(cells))
