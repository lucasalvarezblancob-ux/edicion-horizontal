import React from "react";
import datos from "./capas.json";
import { CapasBase, Item } from "../../comun/Graficos";
// import { MapaSatelite, MapaCfg } from "../../comun/MapaSatelite";

// Capas gráficas de "__SLUG__" (composición __COMP__). Los items salen de capas.json, que escribe
// herramientas/montaje/paso3_plan.py desde out/__SLUG__/plan.py. Título, capítulos, cifras, palabra-golpe, notas,
// subtítulos, rótulos con seguimiento y suscripción ya los pinta CapasBase; aquí solo va lo PROPIO de este vídeo.
export const TOTAL = datos.total;
export const FPS = datos.fps;
export const ANCHO = datos.ancho;
export const ALTO = datos.alto;

// --- Mapa de satélite (si el vídeo nombra regiones o un recorrido) ---
// 1) python herramientas/mapa_satelite.py personal/<creador>/recursos/mapas/<zona>.jpg LON_O LAT_N LON_E LAT_S [nivel]
// 2) copia el .jpg a estudio/public/__SLUG__/ y pega aquí los campos de su .json en `base`
// 3) define las regiones (contorno aproximado [lon, lat], a mano, o `ruta` para un recorrido) y descomenta
// const MAPA: MapaCfg = {
//   imagen: "__SLUG__/zona.jpg",
//   base: { lon0: -108, lat0: 27, grados_por_px: 0.017578125, ancho: 5120, alto: 5120 },
//   general: [-62, -17, 0.78],
//   cabecera: "TÍTULO DEL MAPA",
//   regiones: {
//     uno: { n: 1, nombre: "REGIÓN", nota: "una línea", color: "#63E6D8", cam: [-74, 3.5, 1.55], pol: [[-77.9, 8.6], [-76.6, 8.0], [-76.2, 5.5]] },
//   },
// };

const extra = (it: Item, f: number, dur: number): React.ReactNode => {
  // if (it.t === "mapa") return <MapaSatelite f={f} dur={dur} it={it} cfg={MAPA} />;
  void it; void f; void dur;
  return null;
};

export const Capas: React.FC = () => <CapasBase datos={datos as { items: Item[] }} extra={extra} />;
// Gráficos PROPIOS del creador (PROPIOS en plan.py): importa su función y úsala dentro de `extra`:
//   import { propios } from "../../personal/<creador>/Graficos";      →      return propios(it, f, dur) ?? null;
