"""Filtro por plano: lleva el plano base de Lucas al look del plano equivalente de la referencia.
Balance de blancos en lineal (gris medio) + brillo/contraste en L* + saturación sin girar el tono + resto de tinte suave,
horneada en un .cube 33³ y aplicada con ffmpeg lut3d. Pedido expreso de Lucas ("mismos filtros de colores por clip").
Uso: python igualar_color.py REF.mp4 N [EXPOSICION=0.9]  (desde edits/)
2026-11-03 — Lucas: "reducir un poco los filtros, parecen demasiado fuertes y brillantes; bajar un poco la exposición".
FUERZA = 0,6 del filtro medido y EXPOSICION (multiplica la imagen como CSS brightness) por plano, por defecto 0,9;
revisar_contraste.py la baja más en los planos donde un texto no se lee."""
import sys, subprocess, json, numpy as np
REF, N = sys.argv[1], int(sys.argv[2])
EXPOSICION = float(sys.argv[3]) if len(sys.argv) > 3 else 0.9
FUERZA = 0.6
D = 'estudio/src/videos/la-repeticion'; P = 'estudio/public/la-repeticion'
sel = json.load(open(f'{D}/seleccion.json'))[N-1]
a, b = sel['ref_ini'], sel['ref_fin']

def frames(path, times, w=270, h=480):
    out = []
    for t in times:
        raw = subprocess.run(['ffmpeg','-v','error','-ss',f'{t:.3f}','-i',path,'-frames:v','1','-vf',f'scale={w}:{h}','-f','rawvideo','-pix_fmt','rgb24','-'],capture_output=True).stdout
        if len(raw) == w*h*3: out.append(np.frombuffer(raw,np.uint8).reshape(h,w,3))
    return out

def srgb2lin(c): return np.where(c<=0.04045, c/12.92, ((c+0.055)/1.055)**2.4)
def lin2srgb(c): return np.where(c<=0.0031308, c*12.92, 1.055*np.clip(c,0,None)**(1/2.4)-0.055)
M = np.array([[0.4124,0.3576,0.1805],[0.2126,0.7152,0.0722],[0.0193,0.1192,0.9505]]); Mi = np.linalg.inv(M)
WP = np.array([0.95047,1.0,1.08883])
def f(t): return np.where(t>0.008856, np.cbrt(t), 7.787*t+16/116)
def fi(t): return np.where(t>0.206893, t**3, (t-16/116)/7.787)
def rgb2lab(rgb):
    xyz = srgb2lin(rgb) @ M.T / WP; fx,fy,fz = f(xyz[...,0]),f(xyz[...,1]),f(xyz[...,2])
    return np.stack([116*fy-16, 500*(fx-fy), 200*(fy-fz)],-1)
def lab2rgb(lab):
    fy=(lab[...,0]+16)/116; fx=fy+lab[...,1]/500; fz=fy-lab[...,2]/200
    xyz = np.stack([fi(fx),fi(fy),fi(fz)],-1)*WP
    return np.clip(lin2srgb(xyz @ Mi.T),0,1)

def stats(imgs, quitar_texto):
    px = []
    for im in imgs:
        im = im.astype(float)/255
        if quitar_texto:  # fuera las franjas donde la referencia lleva texto
            keep = np.ones(im.shape[0],bool); h=im.shape[0]
            keep[int(h*0.14):int(h*0.32)] = False; keep[int(h*0.69):int(h*0.77)] = False
            im = im[keep]
        px.append(im.reshape(-1,3))
    lab = rgb2lab(np.concatenate(px))
    return lab.mean(0), lab.std(0)

dur = b - a
ts = [a + dur*k for k in (0.25,0.5,0.75)]

def pix(imgs, quitar_texto):
    px = []
    for im in imgs:
        im = im.astype(float)/255
        if quitar_texto:  # fuera las franjas donde la referencia lleva texto
            keep = np.ones(im.shape[0],bool); h=im.shape[0]
            keep[int(h*0.14):int(h*0.32)] = False; keep[int(h*0.69):int(h*0.77)] = False
            im = im[keep]
        px.append(im.reshape(-1,3))
    return np.concatenate(px)

base = f'{P}/base/{N:02d}.mp4'
ref_px = pix(frames(REF, ts), True)
src_px = pix(frames(base, [dur*k for k in (0.25,0.5,0.75)]), False)
Y = np.array([0.2126,0.7152,0.0722])

# 1) balance de blancos (ganancias por canal en lineal, como un filtro "cálido/frío"), conserva la luminancia
lr, ls = srgb2lin(ref_px).mean(0), srgb2lin(src_px).mean(0)
gan = (lr/(lr@Y)) / (ls/(ls@Y))
gan = np.clip(gan, 0.45, 2.2) ** (0.9*FUERZA)
gan = gan / (gan@Y)  # no cambia el brillo medio
def wb(rgb): return lin2srgb(np.clip(srgb2lin(rgb)*gan, 0, 1))
# 2) brillo/contraste (L*) y 3) saturación (croma) sin girar el tono, + resto del tinte suave
labr, labs = rgb2lab(ref_px), rgb2lab(wb(src_px))
mL_r, sL_r, mL_s, sL_s = labr[:,0].mean(), labr[:,0].std(), labs[:,0].mean(), labs[:,0].std()
kL = 1 + (np.clip(sL_r/max(sL_s,1e-3), 0.7, 1.4) - 1)*FUERZA
dL = np.clip(mL_r - mL_s, -18, 18)*FUERZA
cr, cs = np.hypot(labr[:,1],labr[:,2]).mean(), np.hypot(labs[:,1],labs[:,2]).mean()
kC = 1 + (np.clip(cr/max(cs,1e-3), 0.65, 1.5) - 1)*FUERZA
tinte = np.clip(labr[:,1:].mean(0) - labs[:,1:].mean(0)*kC, -8, 8) * 0.35 * FUERZA
def transformar(rgb):
    lab = rgb2lab(wb(rgb))
    lab[...,0] = mL_s + dL + (lab[...,0]-mL_s)*kL
    lab[...,1:] = lab[...,1:]*kC + tinte
    return lab2rgb(lab) * EXPOSICION

g = np.linspace(0,1,33)
B,G,R = np.meshgrid(g,g,g,indexing='ij')   # .cube: R varía más rápido
out = transformar(np.stack([R,G,B],-1).reshape(-1,3))
cube = f'{P}/luts/{N:02d}.cube'
import os; os.makedirs(os.path.dirname(cube), exist_ok=True)
with open(cube,'w') as fh:
    fh.write('LUT_3D_SIZE 33\n'); fh.writelines(f'{r:.6f} {g_:.6f} {b_:.6f}\n' for r,g_,b_ in out)
subprocess.run(['ffmpeg','-v','error','-y','-i',base,'-vf',f'format=gbrp,lut3d={cube}:interp=tetrahedral,format=yuv420p,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv',
                '-c:v','libx264','-crf','14','-g','10','-color_primaries','bt709','-color_trc','bt709','-colorspace','bt709',f'{P}/planos/{N:02d}.mp4'],check=True)
print(N, 'expo', EXPOSICION, 'gan', np.round(gan,2), 'dL', round(dL,1), 'kL', round(kL,2), 'kC', round(kC,2), 'tinte', np.round(tinte,1))
