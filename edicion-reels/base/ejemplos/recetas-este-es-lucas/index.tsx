import { crearComps, Version } from "../rutinas-este-es-lucas/Rutinas";
import versiones from "./versiones.json";
import voces from "./voces.json";
import paradas from "./paradas.json";
import { Palabra } from "../../comun/Subtitulos";

// 12 recetas / "lo que come en un día" con objetivo (ganar músculo, perder grasa…), "Este es Lucas y hoy te va a enseñar…"
// (2026-11-05). Misma plantilla que las rutinas. Stock de Pexels en public/recetas-este-es-lucas/stock/ (catalogo.json);
// clips de Lucas (proxy.sh 2160) en public/recetas-este-es-lucas/<id>.mp4 — l2880 café chiringuito, r5007 correr amanecer,
// r1847 correr dunas, r8005 dunas sonriendo, r0313 run club lata, f6116 cajón Nike, d2019 garrafa Devant, k1020 ducha spa,
// c1037/c1048/c1085/c1086/c1092/p7629 (enlaces a los de rutinas-este-es-lucas). Guiones en guiones.json → construir.py → versiones.json.
export const RecetasEsteEsLucasComps = () => (
  <>{crearComps("Recetas", "recetas-este-es-lucas", versiones as unknown as Record<string, Version>, voces as Record<string, Palabra[]>, paradas, ["cocina-a.mp3", "cocina-b.mp3", "cocina-c.mp3"])}</>
);
