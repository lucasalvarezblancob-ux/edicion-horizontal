#!/usr/bin/env python3
"""mapa_satelite.py SALIDA.jpg LON_OESTE LAT_NORTE LON_ESTE LAT_SUR [nivel=5]
Baja la base de SATÉLITE para un mapa animado (estudio/src/comun/MapaSatelite.tsx): imagen NASA Blue Marble con relieve y
batimetría, servida por GIBS (dominio público, sin clave). Proyección equirectangular: grados por píxel constantes, así que
pasar de lon/lat a píxel es una resta y una división.
Escribe SALIDA.jpg y SALIDA.json = {lon0, lat0, grados_por_px, ancho, alto, fuente}: son los campos `base` del componente.

nivel: 3 = 0,0703 °/px (continentes enteros), 4 = 0,0352, 5 = 0,0176 (un continente a 4K: Sudamérica = 5120x5120 px),
       6 = 0,0088 (un país), 7 = 0,0044, 8 = 0,0022 (una región; máximo de esta capa, ~250 m/px).
Elige el nivel para que la zona más cerrada que vayas a enseñar tenga al menos tantos píxeles como el vídeo de ancho.
La caja se redondea hacia fuera a teselas enteras de 512 px. Ejemplo (Sudamérica):
  mapa_satelite.py personal/<creador>/recursos/mapas/sudamerica.jpg -108 27 -18 -63 5
Después copia el .jpg a estudio/public/<slug>/ y apúntalo en personal/<creador>/recursos/INDICE.md (sirve para más vídeos)."""
import json, math, sys, time, urllib.request
import numpy as np, cv2

if len(sys.argv) < 6: raise SystemExit(__doc__)
sal = sys.argv[1]; lo0, la0, lo1, la1 = map(float, sys.argv[2:6]); z = int(sys.argv[6]) if len(sys.argv) > 6 else 5
if not 0 <= z <= 8: raise SystemExit("nivel entre 0 y 8")
CAPA, FECHA = "BlueMarble_ShadedRelief_Bathymetry", "2004-08"
URL = "https://gibs.earthdata.nasa.gov/wmts/epsg4326/best/{capa}/default/{fecha}/500m/{z}/{r}/{c}.jpeg"
gpp = 0.5625 / 2 ** z; lado = 512 * gpp                  # grados por px y por tesela
c0, c1 = math.floor((lo0 + 180) / lado), math.ceil((lo1 + 180) / lado)
r0, r1 = math.floor((90 - la0) / lado), math.ceil((90 - la1) / lado)
n = (c1 - c0) * (r1 - r0)
if n > 400: raise SystemExit(f"{n} teselas: demasiado; baja el nivel o cierra la caja")
print(f"{c1 - c0} x {r1 - r0} teselas -> {(c1 - c0) * 512} x {(r1 - r0) * 512} px")
im = np.zeros(((r1 - r0) * 512, (c1 - c0) * 512, 3), np.uint8)
for r in range(r0, r1):
    for c in range(c0, c1):
        u = URL.format(capa=CAPA, fecha=FECHA, z=z, r=r, c=c)
        for intento in range(3):
            try:
                raw = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "mapa-satelite/1.0"}), timeout=30).read(); break
            except Exception as e:
                if intento == 2: raise SystemExit(f"no se pudo bajar {u}: {e}")
                time.sleep(2)
        t = cv2.imdecode(np.frombuffer(raw, np.uint8), cv2.IMREAD_COLOR)
        im[(r - r0) * 512:(r - r0 + 1) * 512, (c - c0) * 512:(c - c0 + 1) * 512] = t
cv2.imwrite(sal, im, [cv2.IMWRITE_JPEG_QUALITY, 92])
meta = {"lon0": -180 + c0 * lado, "lat0": 90 - r0 * lado, "grados_por_px": gpp, "ancho": im.shape[1], "alto": im.shape[0], "fuente": f"NASA GIBS {CAPA} {FECHA} (dominio público)"}
json.dump(meta, open(sal.rsplit(".", 1)[0] + ".json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(sal, meta)
