"""Contraste de cada texto contra lo que tiene detrás (planos/NN.mp4 ya con su filtro).
Texto claro (amarillo/blanco): fondo p75 de luminancia; texto azul: fondo p25. Ratio WCAG; objetivo >= 3.
Uso: python revisar_contraste.py  (desde edits/)  → imprime una línea por texto y el peor ratio por plano."""
import re, subprocess, numpy as np
D='estudio/src/videos/la-repeticion'; P='estudio/public/la-repeticion'
src=open(f'{D}/LaRepeticion.tsx').read()
cortes=[int(x) for x in re.search(r'const CORTES = \[(.*?)\];',src,re.S).group(1).replace('\n','').split(',') if x.strip()]
pos={'ARRIBA':(540,341),'ABAJO':(540,1395)}
for nombre,arr in (('LA',re.search(r'const LA = \[(.*?)\];',src).group(1)),('TI',re.search(r'const TI = \[(.*?)\];',src).group(1))):
    for i,(x,y) in enumerate(re.findall(r'x: (\d+), y: (\d+)',arr)): pos[f'{nombre}[{i}]']=(int(x),int(y))
anchos={k:int(v) for k,v in re.findall(r'"([^"]+\|\d+)": (\d+)',src)}
col={'Y':(0xF7,0xB4,0x34),'B':(0x36,0x42,0xC1),'W':(0xEF,0xE5,0xF9)}
def lum(rgb):
    c=np.asarray(rgb,float)/255; c=np.where(c<=0.04045,c/12.92,((c+0.055)/1.055)**2.4); return c@[0.2126,0.7152,0.0722]
cache={}
def frame(plano,k):
    key=(plano,k)
    if key not in cache:
        raw=subprocess.run(['ffmpeg','-v','error','-i',f'{P}/planos/{plano:02d}.mp4','-vf',f'select=eq(n\\,{k}),scale=1080:1920','-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
        cache[key]=np.frombuffer(raw,np.uint8).reshape(1920,1080,3)
    return cache[key]
peor={}; necesita={}
for t,de,a,c,p in re.findall(r'\{ t: "([^"]+)", de: (\d+), a: (\d+), c: (\w), p: ([\w\[\]]+)',src):
    de,a=int(de),int(a); x,y=pos[p]; w=anchos.get(f'{t}|{de}',100)
    lt=lum(col[c]); res=[]
    for fr in sorted(set([de,(de+a)//2,a-1])):
        plano=next(i for i in range(len(cortes)-1) if cortes[i]<=fr<cortes[i+1])+1
        im=frame(plano,fr-cortes[plano-1])
        reg=im[max(0,y-50):y+50, max(0,x-w//2-25):x+w//2+25].reshape(-1,3)
        L=lum(reg)
        if c=='B': cr=(np.percentile(L,25)+0.05)/(lt+0.05); expo=1
        else:
            lb=np.percentile(L,75); cr=(lt+0.05)/(lb+0.05)
            lreq=(lt+0.05)/3-0.05; expo=min(1,(lreq/lb)**(1/2.2)) if lb>0 else 1
        res.append((round(cr,2),plano,expo))
    m=min(res); peor[m[1]]=min(peor.get(m[1],99),m[0])
    for r in res: necesita[r[1]]=min(necesita.get(r[1],1),r[2])
    print(f'{t:14s} {c} {p:7s} planos {sorted(set(r[1] for r in res))} ratio {m[0]}' + ('   <-- BAJO' if m[0]<3 else ''))
print('peor por plano:', {k:v for k,v in sorted(peor.items()) if v<3})
print('exposicion relativa necesaria (texto claro):', {k:round(v,2) for k,v in sorted(necesita.items()) if v<0.99})
