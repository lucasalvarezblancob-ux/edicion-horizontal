# uso: voz.py T0 T1 [T0 T1 ...] -> palabras dichas en cada ventana (con 1,5 s de margen)
import json,sys,os
tr=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','transcripcion.json'),encoding='utf-8'))
fr=tr['frases']
if len(sys.argv)==1:
    print(json.dumps(fr[0],ensure_ascii=False)[:500]); sys.exit()
ws=[]
for f in fr:
    for w in f.get('palabras',[]): ws.append(w)
a=[float(x) for x in sys.argv[1:]]
k=list(ws[0].keys())
ini=[x for x in k if x in('t','ini','inicio','t0','start','desde')][0]; txt=[x for x in k if x in('palabra','texto','word','w','p')][0]
for i in range(0,len(a),2):
    t0,t1=a[i],a[i+1]
    print('%.1f-%.1f: '%(t0,t1)+' '.join('%s[%.1f]'%(w[txt].strip(),w[ini]) for w in ws if t0-1.5<=w[ini]<=t1+1.5))
