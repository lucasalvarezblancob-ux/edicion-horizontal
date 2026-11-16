# Tramos del montaje con cortes en el SILENCIO real (energía), sin colar el arranque de una palabra repetida.
import json,sys,numpy as np,soundfile as sf
W=json.load(open('estudio/src/videos/rebajas-gymshark/palabras.json'))
x,sr=sf.read(sys.argv[1]); x=x if x.ndim==1 else x.mean(1)
hop=int(0.01*sr); E=np.array([np.sqrt(np.mean(x[i:i+hop]**2)+1e-12) for i in range(0,len(x)-hop,hop)]); dB=20*np.log10(E)
def quieto(a,b):
    # punto más silencioso entre a y b (s), suavizado 50 ms
    i,j=int(a*100),int(b*100)
    if j<=i+1: return (a+b)/2
    seg=np.convolve(dB[i:j],np.ones(5)/5,'same'); return (i+int(np.argmin(seg)))/100
# 2026-11-15 (corrección de Lucas: se colaba el arranque de palabras repetidas): fuera "Pero he dicho a lo mejor, así que yo," — va pegado al "así" repetido, sin silencio donde cortar.
R=[(12,40),(58,104),(105,119),(123,131),(162,191),(217,241),(275,290),(300,313)]
segs=[];keep=[]
for a,b in R:
    keep+=list(range(a,b+1))
    prev_end=W[a-1]['end'] if a>0 else 0
    s=max(quieto(max(prev_end,W[a]['start']-0.6),W[a]['start']),W[a]['start']-0.25)
    for i in range(a,b):
        if W[i+1]['start']-W[i]['end']>0.4:
            segs.append([s,min(W[i]['end']+0.15,quieto(W[i]['end'],W[i+1]['start']-0.1))]); s=max(W[i+1]['start']-0.25,quieto(W[i]['end']+0.1,W[i+1]['start']))
    nxt=W[b+1]['start'] if b+1<len(W) else W[b]['end']+0.5
    segs.append([s,min(W[b]['end']+0.2,quieto(W[b]['end'],nxt-0.03))])
for s,e in segs: print(round(s,2),round(e,2))
print('total',round(sum(e-s for s,e in segs),2))
json.dump({'segs':segs,'keep':keep},open('estudio/src/videos/rebajas-gymshark/montaje.json','w'),indent=1)
