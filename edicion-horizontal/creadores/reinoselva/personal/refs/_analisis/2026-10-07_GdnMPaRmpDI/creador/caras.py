import cv2, numpy as np, json, subprocess
W,H=640,360
a=json.load(open('_analisis/2026-10-07_GdnMPaRmpDI/audio.json',encoding='utf-8'))
v=a['por_segundo']['voz_db']
cf=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
cp=cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_profileface.xml')
p=subprocess.Popen(["ffmpeg","-nostdin","-v","error","-i","2026-10-07_GdnMPaRmpDI.mp4","-vf","fps=1,scale=640:360","-pix_fmt","gray","-f","rawvideo","-"],stdout=subprocess.PIPE)
res=[]
while True:
    b=p.stdout.read(W*H)
    if len(b)<W*H: break
    g=np.frombuffer(b,np.uint8).reshape(H,W)
    f=cf.detectMultiScale(g,1.1,5,minSize=(28,28))
    pr=cp.detectMultiScale(g,1.1,5,minSize=(28,28)); pr2=cp.detectMultiScale(cv2.flip(g,1),1.1,5,minSize=(28,28))
    res.append([len(f),len(pr)+len(pr2)])
n=len(res); voz=[t for t in range(min(n,len(v))) if v[t]>-35]
fr=sum(1 for r in res if r[0]>0); anyf=sum(1 for r in res if r[0]+r[1]>0)
print('seg',n,'con cara frontal',round(100*fr/n,1),'cara cualquiera',round(100*anyf/n,1))
print('seg con voz',len(voz),'de ellos cara frontal',round(100*sum(1 for t in voz if res[t][0]>0)/len(voz),1),'cualquiera',round(100*sum(1 for t in voz if sum(res[t])>0)/len(voz),1))
json.dump(res,open('_analisis/2026-10-07_GdnMPaRmpDI/creador/caras.json','w'))
for m in range(0,n,60):
    s=res[m:m+60]; print(m//60, round(100*sum(1 for r in s if sum(r)>0)/len(s)), end=' | ')
print()
ac=a['acentos']; iso=[x for i,x in enumerate(ac) if (i==0 or x-ac[i-1]>1.6) and (i==len(ac)-1 or ac[i+1]-x>1.6)]
print('acentos aislados',len(iso),iso)
c=json.load(open('_analisis/2026-10-07_GdnMPaRmpDI/cortes.json',encoding='utf-8')); ts=[x['t'] for x in c['cortes']]
print('aislados sobre corte',[x for x in iso if min(abs(x-t) for t in ts)<0.2])
