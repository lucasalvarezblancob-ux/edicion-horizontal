import sys, subprocess, numpy as np, json
v=sys.argv[1]; W,H=320,180
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',v,'-vf','fps=2,scale=320:180','-f','rawvideo','-pix_fmt','rgb24','-'],stdout=subprocess.PIPE)
out=[]; i=0
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    a=np.frombuffer(b,np.uint8).reshape(H,W,3).astype(int)
    r,g,bl=a[...,0],a[...,1],a[...,2]
    yel=(r>225)&(g>150)&(g<215)&(bl<70)          # amarillo-naranja saturado de la tortuga
    wh=(r>245)&(g>245)&(bl>245)                   # blanco puro (burbuja)
    red=(r>215)&(g<40)&(bl<40)                    # rojo boton YT
    q=lambda m:[int(m[:90,:160].sum()),int(m[:90,160:].sum()),int(m[90:,:160].sum()),int(m[90:,160:].sum())]
    out.append({'t':i/2,'yel':q(yel),'wh':q(wh),'red':q(red)})
    i+=1
json.dump(out,open(sys.argv[2],'w'))
print(len(out))
