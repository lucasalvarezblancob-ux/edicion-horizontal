import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
im = np.asarray(Image.open(sys.argv[1]).convert("RGB")).astype(np.float32)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
rojez = R - G  # rojo, naranja y el morado del borde: alto; azul, blanco: <=0; amarillo: ~40
duro = rojez > 95
# solo el rojo conectado con el borde (no toca sombras naranjas dentro del interrogante)
lab, n = ndi.label(rojez > 42)
borde = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
fondo = np.isin(lab, borde[borde > 0]) | (rojez > 120)
alpha = np.where(fondo, 1 - np.clip((rojez - 42) / 40, 0, 1), 1.0)
# descontaminar: en los píxeles tocados por el fondo, el color es el del píxel opaco más cercano
opaco = ndi.binary_erosion(alpha > 0.98, iterations=2)
idx = ndi.distance_transform_edt(~opaco, return_distances=False, return_indices=True)
rgb = im[idx[0], idx[1]]
rgb = np.where((~opaco)[..., None], rgb, im)
out = np.dstack([rgb, alpha * 255]).round().astype(np.uint8)
ys, xs = np.where(alpha > 0.02)
out = out[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
Image.fromarray(out, "RGBA").save(sys.argv[2])
print(out.shape, round(float((alpha < 0.5).mean()), 3))
# previas sobre gris y sobre negro
for nombre, c in (("gris", 120), ("verde", (40, 160, 60))):
    bg = Image.new("RGBA", (out.shape[1], out.shape[0]), (c, c, c, 255) if isinstance(c, int) else c + (255,))
    bg.alpha_composite(Image.fromarray(out, "RGBA")); bg.convert("RGB").save(sys.argv[2].replace(".png", f"-{nombre}.jpg"))
