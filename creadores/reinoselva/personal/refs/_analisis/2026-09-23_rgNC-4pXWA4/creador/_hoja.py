# Hoja de contactos con OpenCV (sin drawtext). Uso: _hoja.py SALIDA T0 PASO N COLS ANCHO [x y w h recorte en px de 1280x720]
import cv2, sys, numpy as np
V=r"C:/Users/Lucas/Desktop/Horizontal/personal/reinoselva/refs/2026-09-23_rgNC-4pXWA4.mp4"
out=sys.argv[1]; t0=float(sys.argv[2]); paso=float(sys.argv[3]); n=int(sys.argv[4]); cols=int(sys.argv[5]); W=int(sys.argv[6])
crop=[int(x) for x in sys.argv[7:11]] if len(sys.argv)>=11 else None
cap=cv2.VideoCapture(V); fps=cap.get(cv2.CAP_PROP_FPS)
f0=int(round(t0*fps)); cap.set(cv2.CAP_PROP_POS_FRAMES, max(0,f0-1))
want=[int(round((t0+i*paso)*fps)) for i in range(n)]
cells=[]; cur=int(cap.get(cv2.CAP_PROP_POS_FRAMES)); wi=0
while wi<n:
    ok,fr=cap.read()
    if not ok: break
    if cur>=want[wi]:
        if crop: x,y,w,h=crop; fr=fr[y:y+h,x:x+w]
        H=int(fr.shape[0]*W/fr.shape[1]); im=cv2.resize(fr,(W,H),interpolation=cv2.INTER_AREA)
        t=cur/fps; s="%d:%05.2f"%(int(t//60),t%60)
        cv2.rectangle(im,(0,0),(92,20),(0,0,0),-1); cv2.putText(im,s,(3,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
        cells.append(im); wi+=1
    cur+=1
rows=(len(cells)+cols-1)//cols; H=cells[0].shape[0]
sheet=np.zeros((rows*H,cols*W,3),np.uint8)
for i,im in enumerate(cells): sheet[(i//cols)*H:(i//cols)*H+H,(i%cols)*W:(i%cols)*W+W]=im
cv2.imwrite(out,sheet,[cv2.IMWRITE_JPEG_QUALITY,88]); print(out,len(cells),sheet.shape)
