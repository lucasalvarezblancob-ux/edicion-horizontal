# uso: hoja.py VIDEO SALIDA T0 PASO N COLS ANCHO [x0 y0 x1 y1 (% recorte)]
import sys, cv2, numpy as np
v,out=sys.argv[1],sys.argv[2]; t0,paso=float(sys.argv[3]),float(sys.argv[4]); n,cols,w=int(sys.argv[5]),int(sys.argv[6]),int(sys.argv[7])
crop=[float(x) for x in sys.argv[8:12]] if len(sys.argv)>=12 else [0,0,100,100]
cap=cv2.VideoCapture(v); fps=cap.get(cv2.CAP_PROP_FPS)
cells=[]
# lectura secuencial desde t0 (precisa)
cap.set(cv2.CAP_PROP_POS_MSEC,max(0,(t0-1.0))*1000)
want=[t0+i*paso for i in range(n)]; k=0
while k<n:
    ok,fr=cap.read()
    if not ok: break
    t=cap.get(cv2.CAP_PROP_POS_MSEC)/1000.0 - 1.0/fps
    if t+0.5/fps>=want[k]:
        H,W=fr.shape[:2]
        x0,y0,x1,y1=int(crop[0]*W/100),int(crop[1]*H/100),int(crop[2]*W/100),int(crop[3]*H/100)
        c=fr[y0:y1,x0:x1]; h=int(w*c.shape[0]/c.shape[1]); c=cv2.resize(c,(w,h),interpolation=cv2.INTER_AREA)
        lab='%.2f'%want[k]
        cv2.rectangle(c,(0,0),(8+11*len(lab),20),(0,0,0),-1); cv2.putText(c,lab,(4,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
        cells.append(c); k+=1
cap.release()
if not cells: sys.exit('sin fotogramas')
h=cells[0].shape[0]
while len(cells)%cols: cells.append(np.zeros_like(cells[0]))
rows=[np.hstack(cells[i:i+cols]) for i in range(0,len(cells),cols)]
cv2.imwrite(out,np.vstack(rows),[cv2.IMWRITE_JPEG_QUALITY,88]); print(out,len(rows),'filas')
