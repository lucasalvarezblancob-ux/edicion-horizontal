import React from "react";
import datos from "./capas.json";
import { ACENTO } from "../../comun/marca";
import { CapasBase, Item } from "../../comun/Graficos";
import { MapaSatelite, MapaCfg } from "../../comun/MapaSatelite";

// Capas gráficas de "ramon" (EJEMPLO de la skill). Título, capítulos, cifras, palabra-golpe, notas, subtítulos, rótulos
// con seguimiento y suscripción los pinta CapasBase desde capas.json; aquí solo va lo propio: el mapa de satélite.
export const TOTAL = datos.total;
export const FPS = datos.fps;
export const ANCHO = datos.ancho;
export const ALTO = datos.alto;

// Mapa de los cuatro grandes ecosistemas de Sudamérica. Base: NASA Blue Marble (dominio público), bajada con
//   python herramientas/mapa_satelite.py personal/<creador>/recursos/mapas/sudamerica.jpg -108 27 -18 -63 5
// y copiada a estudio/public/ramon/sudamerica.jpg. Contornos aproximados, a mano, en [lon, lat].
const MAPA: MapaCfg = {
  imagen: "ramon/sudamerica.jpg",
  base: { lon0: -108, lat0: 27, grados_por_px: 0.017578125, ancho: 5120, alto: 5120 },
  general: [-62, -17, 0.78],
  cabecera: "THE BIG ECOSYSTEMS OF SOUTH AMERICA",
  pie: "Approximate areas · imagery: NASA Blue Marble",
  regiones: {
  choco: { n: 1, nombre: "CHOCÓ", nota: "west of the Andes, up to Central America", color: "#63E6D8", cam: [-74, 3.5, 1.55],
    pol: [[-77.9, 8.6], [-76.6, 8.0], [-76.2, 5.5], [-76.7, 3.5], [-77.7, 1.6], [-78.8, 0.2], [-79.3, -1.6], [-80.6, -1.0], [-80.1, 0.6], [-78.9, 1.7], [-77.5, 4.0], [-77.6, 6.8]] },
  amazon: { n: 2, nombre: "AMAZON + GUIANAS", nota: "home of the caiman lizards", color: "#7BE38B", cam: [-60, -4, 0.92],
    pol: [[-77, -1], [-75, 3], [-70, 5], [-64, 8.3], [-60, 8.3], [-57, 6], [-52, 5], [-50, 1], [-47, -1], [-45, -4], [-48, -9], [-54, -13], [-60, -14], [-65, -16], [-70, -14], [-74, -11], [-77, -6]] },
  atlantic: { n: 3, nombre: "ATLANTIC FOREST", nota: "cut off from the Amazon by dry land", color: ACENTO, cam: [-46, -19, 1.0],
    pol: [[-35.2, -6], [-34.9, -8.5], [-37.5, -12], [-39, -15], [-39.6, -19], [-41, -22.6], [-45, -24], [-48.5, -26.5], [-49.6, -29.5], [-52, -31], [-55.5, -27], [-54.5, -24], [-50, -22], [-45, -20.5], [-42.5, -17], [-41, -13], [-38.5, -9.5], [-36.5, -6]] },
  chaco: { n: 4, nombre: "GRAN CHACO", nota: "the dry forest in between", color: "#FFA75C", cam: [-59, -25, 1.25],
    pol: [[-63.5, -17.5], [-58.5, -18.5], [-57.5, -22], [-57.8, -26], [-59.5, -30], [-62.5, -33], [-65, -31], [-65, -26], [-64.5, -21]] },
},
};

const extra = (it: Item, f: number, dur: number): React.ReactNode => {
  if (it.t === "mapa") return <MapaSatelite f={f} dur={dur} it={it} cfg={MAPA} />;
  return null;
};

export const Capas: React.FC = () => <CapasBase datos={datos as { items: Item[] }} extra={extra} />;
