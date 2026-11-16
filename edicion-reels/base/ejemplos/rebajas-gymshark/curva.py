import numpy as np,sys
from PIL import Image
SP=sys.argv[1]; OUT=sys.argv[2]
def L(p): return np.asarray(Image.open(p).convert('RGB')).astype(np.float32)
def zona(X):
    X=X[20:1600,10:970].copy(); m=np.ones(X.shape[:2],bool); m[1110-20:1340-20,:]=False
    return X,m
def blk2(X,Y,m,k=6):
    out=[]
    n0=(X.shape[0]//k)*k;n1=(X.shape[1]//k)*k
    M=m[:n0,:n1].reshape(n0//k,k,n1//k,k).all((1,3))
    BX=X[:n0,:n1].reshape(n0//k,k,n1//k,k,3); BY=Y[:n0,:n1].reshape(n0//k,k,n1//k,k,3)
    ok=M&(BX.std((1,3)).max(-1)<4)&(BY.std((1,3)).max(-1)<4)
    return BX.mean((1,3))[ok],BY.mean((1,3))[ok]
P=[];R=[]
for t in sys.argv[3].split(','):
    b,m=zona(L(f'{SP}/qb_{t}.png')); p,_=zona(L(f'{SP}/qp_{t}.png'))
    a1,a2=blk2(p,b,m); P.append(a1);R.append(a2)
P=np.concatenate(P);R=np.concatenate(R)
xs=np.arange(256); curvas=[]
for c in range(3):
    cx=[];cy=[]
    for lo in range(0,256,8):
        s=(P[:,c]>=lo)&(P[:,c]<lo+8)
        if s.sum()>=15: cx.append(np.median(P[s,c])); cy.append(np.median(R[s,c]))
    cx=np.array([0]+cx+[255]); sl=(cy[-1]-cy[-4])/(cx[-2]-cx[-5]); cy=np.array([0]+cy+[min(255,cy[-1]+(255-cx[-2])*sl)])
    cy=np.maximum.accumulate(cy)
    curvas.append(np.clip(np.interp(xs,cx,cy),0,255)); print('canal',c,list(zip(np.round(cx).astype(int),np.round(cy).astype(int))))
N=33; g=np.linspace(0,255,N)
with open(OUT,'w') as f:
    f.write(f'LUT_3D_SIZE {N}\n')
    for bb in g:
        for gg in g:
            for rr in g:
                v=[np.interp(rr,xs,curvas[0]),np.interp(gg,xs,curvas[1]),np.interp(bb,xs,curvas[2])]
                f.write(' '.join(f'{x/255:.6f}' for x in v)+'\n')
