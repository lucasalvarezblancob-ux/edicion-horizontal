import { crearComps, Version } from "./Rutinas";
import versiones from "./versiones.json";
import voces from "./voces.json";
import paradas from "./paradas.json";
import { Palabra } from "../../comun/Subtitulos";

// 12 rutinas de espalda y pecho "Este es Lucas…" (2026-11-05). Composiciones Rutinas-v01-… a Rutinas-v12-…
export const RutinasEsteEsLucasComps = () => (
  <>{crearComps("Rutinas", "rutinas-este-es-lucas", versiones as unknown as Record<string, Version>, voces as Record<string, Palabra[]>, paradas, ["gym-a.mp3", "gym-b.mp3", "gym-c.mp3"])}</>
);
