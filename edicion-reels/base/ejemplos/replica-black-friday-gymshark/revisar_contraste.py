"""Contraste de los textos blancos contra lo que tienen detrás (plano base con su zoom, sin textos ni efectos).
Fondo = p75 de luminancia en la caja de cada línea; ratio WCAG; objetivo >= 3 (preferencias.md, la-repeticion).
Imprime el peor ratio por plano y la exposición (brightness) que haría falta para llegar a 3.
Uso: herramientas/.venv/bin/python -I estudio/src/videos/replica-black-friday-gymshark/revisar_contraste.py [exposiciones.json]"""
import json, subprocess, sys, numpy as np
P='estudio/public/replica-black-friday-gymshark/planos'
SEL={x['n']:x for x in json.load(open('estudio/src/videos/replica-black-friday-gymshark/seleccion.json'))}
EXPO=json.load(open(sys.argv[1])) if len(sys.argv)>1 else {}
ZOOM={11:(1.12,.5,.35),13:(1.4,.5,.30),18:(1.8,.5,.62),20:(1.3,.5,.30)}
# (texto, y centro, ancho, alto, color, desde, hasta) en coordenadas 1080x1920
T=[('STAY TUNED',215,340,40,(255,255,255),118,214),('GYMSHARK',858,600,95,(236,231,228),74,217),('BLACK FRIDAY',983,780,95,(236,231,228),74,217),
   ('15/11/2026',1062,300,50,(255,255,255),118,214),('-50% off',930,380,70,(255,255,255),268,414),('+ ALVAREZ10',1008,560,70,(255,255,255),268,414),
   ('for an extra -10%',1070,580,60,(255,255,255),268,414)]
PL=[(11,74,217),(13,240,297),(14,294,340),(15,340,349),(16,349,393),(17,393,416)]
def lum(rgb):
    c=np.asarray(rgb,float)/255; c=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4); return c@[0.2126,0.7152,0.0722]
def frame(n,t):
    raw=subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',f'{P}/{n:02d}.mp4','-vf','scale=1080:1920','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
    im=np.frombuffer(raw,np.uint8).reshape(1920,1080,3).astype(float)
    if n in ZOOM:  # escala alrededor del origen como el transform CSS
        z,ox,oy=ZOOM[n]; X0=ox*1080; Y0=oy*1920
        xs=np.clip(((np.arange(1080)-X0)/z+X0).astype(int),0,1079); ys=np.clip(((np.arange(1920)-Y0)/z+Y0).astype(int),0,1919)
        im=im[ys][:,xs]
    return im*EXPO.get(str(n),1.0)
for n,de,a in PL:
    peor=99; expo=1
    for f in np.linspace(max(de,74),a-1,5).astype(int):
        im=frame(n,(f-SEL[n]['de'])/30)
        for t,y,w,h,col,d0,d1 in T:
            if not (d0<=f<=d1 and (n!=11 or f>=105 or True)): continue
            reg=im[y-h//2:y+h//2,540-w//2:540+w//2].reshape(-1,3); lb=np.percentile(lum(np.clip(reg,0,255)),75); lt=lum(col)
            cr=(lt+0.05)/(lb+0.05)
            if cr<peor: peor,quien=cr,(t,int(f))
            lreq=(lt+0.05)/3-0.05; expo=min(expo,(lreq/lb)**(1/2.2) if lb>0 else 1)
    print(f'plano {n:2d}: peor ratio {peor:.2f} en {quien}  → exposición necesaria {min(1,expo):.2f}')
