import cv2, numpy as np, json, sys, subprocess
W,H=640,360
p=subprocess.Popen(["ffmpeg","-nostdin","-v","error","-i","2026-10-07_GdnMPaRmpDI.mp4","-vf","fps=2,scale=640:360","-pix_fmt","bgr24","-f","rawvideo","-"],stdout=subprocess.PIPE)
out=[];n=0
k3=np.ones((3,3),np.uint8);k7=np.ones((7,7),np.uint8)
while True:
    b=p.stdout.read(W*H*3)
    if len(b)<W*H*3: break
    f=np.frombuffer(b,np.uint8).reshape(H,W,3)
    g=f.min(axis=2); mx=f.max(axis=2)
    wm=(g>225).astype(np.uint8)
    dark=(mx<60).astype(np.uint8)
    near=cv2.dilate(dark,k7)
    k,lab,st,_=cv2.connectedComponentsWithStats(wm,8)
    c=0; ys=[]; xs=[]
    for i in range(1,k):
        x,y,w,h,a=st[i]
        if a<12 or a>500 or h<7 or h>45 or w>60: continue
        m=(lab[y:y+h,x:x+w]==i)
        fr=near[y:y+h,x:x+w][m].mean()
        if fr>0.8:
            c+=1; ys.append(y+h/2); xs.append(x+w/2)
    r={"t":n/2,"c":c}
    if c>=5:
        r["y"]=[round(float(np.percentile(ys,10))/H*100),round(float(np.percentile(ys,90))/H*100)]
        r["x"]=[round(float(min(xs))/W*100),round(float(max(xs))/W*100)]
    out.append(r); n+=1
json.dump(out,open(sys.argv[1],"w"))
runs=[];cur=None
for r in out:
    if r["c"]>=6:
        if cur and r["t"]-cur[1]<=1.0: cur[1]=r["t"]; cur[2]=max(cur[2],r["c"])
        else:
            cur=[r["t"],r["t"],r["c"],r.get("x"),r.get("y")]; runs.append(cur)
for r in runs: print(r)
