# uso: frame.py VIDEO T SALIDA  -> fotograma completo exacto
import sys, cv2
cap=cv2.VideoCapture(sys.argv[1]); fps=cap.get(cv2.CAP_PROP_FPS); t=float(sys.argv[2])
cap.set(cv2.CAP_PROP_POS_MSEC,max(0,t-1)*1000)
while True:
    ok,fr=cap.read()
    if not ok: break
    if cap.get(cv2.CAP_PROP_POS_MSEC)/1000.0-0.5/fps>=t: break
cv2.imwrite(sys.argv[3],fr,[cv2.IMWRITE_JPEG_QUALITY,92]); print(sys.argv[3],fr.shape)
