import sys, subprocess, numpy as np, cv2, json
W,H=320,180; fps=20
p=subprocess.Popen(['ffmpeg','-nostdin','-v','error','-i',sys.argv[1],'-vf','fps=%d,scale=%d:%d'%(fps,W,H),'-f','rawvideo','-pix_fmt','gray','-'],stdout=subprocess.PIPE)
v=[]
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H: break
    v.append(cv2.Laplacian(np.frombuffer(b,np.uint8).reshape(H,W),cv2.CV_32F).var())
v=np.array(v); out=[]
for i in range(len(v)):
    a=max(0,i-fps); b=min(len(v),i+fps)
    ref=np.median(np.r_[v[a:max(a,i-3)],v[min(b,i+4):b]]) if b-a>8 else v[i]
    if ref>150 and v[i]<0.22*ref: out.append(round(i/fps,2))
runs=[]
for t in out:
    if runs and t-runs[-1][1]<=0.3: runs[-1][1]=t
    else: runs.append([t,t])
print(len(v), runs)
