import numpy as np, sys
from PIL import Image
S=sys.argv[1]
def L(p): return np.asarray(Image.open(p).convert('RGB')).astype(np.float32)
codes=[];targets=[];caps=[]
for id in ['1061','1066','1071','1057']:
    code=L(f'{S}/code_{id}.png'); cp=L(f'{S}/c_proxy_{id}.png'); cr=L(f'{S}/c_raw_{id}.png')
    # geometría: probar anchos/desplazamientos
    best=None
    g=cp.mean(-1)
    for w in range(980,989,2):
        h=round(w*16/9)
        im=np.asarray(Image.fromarray(code.astype(np.uint8)).resize((w,h),Image.BILINEAR)).astype(np.float32).mean(-1)
        for dx in range(-4,5,1):
            for dy in range(-122,-109,1):
                ys=slice(150,850); xs=slice(100,880)
                a=g[ys,xs]; 
                yy0=150-dy; xx0=100-dx
                if yy0<0 or xx0<0: continue
                b=im[yy0:yy0+700, xx0:xx0+780]
                if b.shape!=a.shape: continue
                e=np.abs(np.argsort(np.argsort(a.ravel()))-np.argsort(np.argsort(b.ravel()))).mean() if False else np.mean(np.abs((a-a.mean())/a.std()-(b-b.mean())/b.std()))
                if best is None or e<best[0]: best=(e,w,dx,dy)
    e,w,dx,dy=best; print(id,'geom',best)
    h=round(w*16/9)
    im=np.asarray(Image.fromarray(code.astype(np.uint8)).resize((w,h),Image.BILINEAR)).astype(np.float32)
    H,W=cp.shape[:2]
    ys=[y for y in range(20,min(H,1580)) if not (880<=y<=1180)]
    ys=np.array([y for y in ys if 0<=y-dy<h]); xs=np.arange(20,min(W,w+dx)-20)
    A=im[np.ix_(ys-dy,xs-dx)]; P=cp[np.ix_(ys,xs)]; R=cr[np.ix_(ys,xs)]
    # suaviza para tolerar movimiento: bloques 8x8
    def blk(X,k=8):
        n0=(X.shape[0]//k)*k;n1=(X.shape[1]//k)*k
        return X[:n0,:n1].reshape(n0//k,k,n1//k,k,3).mean((1,3)).reshape(-1,3)
    codes.append(blk(A));caps.append(blk(P));targets.append(blk(R))
C=np.concatenate(codes);P=np.concatenate(caps);R=np.concatenate(targets)
# coherencia proxy capturado vs código: si el bloque se movió (P lejos de f2(C)) se descarta
bins=np.arange(0,257,4)
def curve(x,y):
    out=[]
    for i in range(len(bins)-1):
        m=(x>=bins[i])&(x<bins[i+1])
        out.append(np.median(y[m]) if m.sum()>20 else np.nan)
    c=(bins[:-1]+bins[1:])/2; o=np.array(out); ok=~np.isnan(o)
    return np.interp(np.arange(256),c[ok],np.maximum.accumulate(o[ok]))
# f2: código -> capturado (proxy)
f2=[curve(C[:,k],P[:,k]) for k in range(3)]
res=np.abs(np.stack([f2[k][np.clip(C[:,k].astype(int),0,255)] for k in range(3)],1)-P).mean(1)
keep=res<np.percentile(res,70)
print('bloques',len(C),'usados',keep.sum())
# código deseado = f2^-1(R)
D=np.stack([np.interp(R[:,k],f2[k],np.arange(256)) for k in range(3)],1)
g=[curve(C[keep,k],D[keep,k]) for k in range(3)]
for v in [16,32,48,64,96,128,160,192,224,240]:
    print(v,[round(g[k][v],1) for k in range(3)])
np.save(f'{S}/g.npy',np.stack(g))
# saturación: ¿queda diferencia de croma tras la curva?
Cg=np.stack([g[k][np.clip(C[keep,k].astype(int),0,255)] for k in range(3)],1); Dk=D[keep]
sat=lambda X:(X.max(1)-X.min(1))
print('croma media deseada/curva', np.median(sat(Dk)[sat(Cg)>8]/sat(Cg)[sat(Cg)>8]))
