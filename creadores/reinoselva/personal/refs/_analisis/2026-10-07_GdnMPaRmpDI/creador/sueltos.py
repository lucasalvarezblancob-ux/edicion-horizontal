import cv2, sys, numpy as np
V="2026-10-07_GdnMPaRmpDI.mp4"
out=sys.argv[1]; cols=int(sys.argv[2]); W=int(sys.argv[3]); ts=[float(x) for x in sys.argv[4:]]
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS); cells=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_FRAMES,max(0,int(round(t*fps))-2)); cap.read(); cap.read(); ok,f=cap.read()
    if not ok: continue
    c=cv2.resize(f,(W,W*9//16),interpolation=cv2.INTER_AREA); lab="%.1f"%t
    cv2.rectangle(c,(0,0),(12*len(lab)+6,20),(0,0,0),-1); cv2.putText(c,lab,(3,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA); cells.append(c)
rows=[]
for i in range(0,len(cells),cols):
    r=cells[i:i+cols]
    while len(r)<cols: r.append(np.zeros_like(cells[0]))
    rows.append(np.hstack(r))
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,88]); print(out,len(cells))
