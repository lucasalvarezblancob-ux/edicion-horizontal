import cv2, sys, numpy as np
# uso: mosaico.py SALIDA COLS ANCHO t1 t2 ...
cap=cv2.VideoCapture('2026-09-26_78wavVq4ymI.mp4')
out=sys.argv[1]; cols=int(sys.argv[2]); W=int(sys.argv[3]); H=W*9//16
ts=[float(x) for x in sys.argv[4:]]
cells=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC,t*1000); ok,f=cap.read()
    if not ok: f=np.zeros((720,1280,3),np.uint8)
    f=cv2.resize(f,(W,H),interpolation=cv2.INTER_AREA)
    cv2.rectangle(f,(0,0),(92,20),(0,0,0),-1)
    cv2.putText(f,'%.2f'%t,(3,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
    cells.append(f)
while len(cells)%cols: cells.append(np.zeros((H,W,3),np.uint8))
rows=[np.hstack(cells[i:i+cols]) for i in range(0,len(cells),cols)]
cv2.imwrite('_analisis/2026-09-26_78wavVq4ymI/creador/'+out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,88])
