# uso: multi.py VIDEO SALIDA COLS ANCHO T1 T2 ...  -> hoja con fotogramas completos en tiempos sueltos
import sys, cv2, numpy as np
v,out,cols,w=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4]); ts=[float(x) for x in sys.argv[5:]]
cap=cv2.VideoCapture(v); fps=cap.get(cv2.CAP_PROP_FPS); cells=[]
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC,max(0,t-1)*1000)
    while True:
        ok,fr=cap.read()
        if not ok or cap.get(cv2.CAP_PROP_POS_MSEC)/1000.0-0.5/fps>=t: break
    h=int(w*fr.shape[0]/fr.shape[1]); c=cv2.resize(fr,(w,h),interpolation=cv2.INTER_AREA)
    lab='%.2f'%t; cv2.rectangle(c,(0,0),(8+11*len(lab),20),(0,0,0),-1); cv2.putText(c,lab,(4,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
    cells.append(c)
while len(cells)%cols: cells.append(np.zeros_like(cells[0]))
cv2.imwrite(out,np.vstack([np.hstack(cells[i:i+cols]) for i in range(0,len(cells),cols)]),[cv2.IMWRITE_JPEG_QUALITY,90]); print(out)
