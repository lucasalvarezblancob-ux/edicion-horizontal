import React from "react";
import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";
import { ACENTO, F_MANO as MANO } from "./marca";

// Nombre a mano tipo Ariana (ref refs/voice en off/ariannarosv_DXL9LK4CH8b.mp4) para los vídeos que empiezan con
// "Este es Lucas": las letras llegan desordenadas (giradas, grandes, desde fuera) y se colocan con muelle (~0,5 s);
// pegatina con borde blanco grueso + sombra de color desplazada + sombra suave; dos rayitas de destello arriba a la
// izquierda y una flecha blanca a mano que baja hasta la cabeza.
//
// USO (patrón fijo, ver refs/voice en off/CONTEXTO.md):
//   - Sequence desde el frame EXACTO en que la voz dice el nombre (start de la palabra en voz-palabras.json + VOZ_DESDE)
//     hasta el corte del plano (~1 s), + pop.mp3 a 0,45 en ese mismo frame ("un poco más presente").
//   - En los subtítulos se quita la palabra del nombre y la anterior lleva coma ("es,") para cerrar el bloque.
//   - `cabeza` = centro horizontal y parte de arriba de la cabeza en ese plano (px del vídeo 1080×1920).

const DESORDEN = [
  { dx: -260, dy: -120, r: -40, s: 1.6 },
  { dx: 180, dy: -200, r: 35, s: 1.5 },
  { dx: -140, dy: 160, r: -25, s: 1.7 },
  { dx: 240, dy: 120, r: 160, s: 1.4 },
  { dx: 320, dy: -60, r: -30, s: 1.6 },
  { dx: -200, dy: -180, r: 50, s: 1.5 },
  { dx: 150, dy: 190, r: -60, s: 1.6 },
];
const PASO = 88; // px entre letras con fontSize 200

export const NombrePegatina: React.FC<{ nombre: string; cabeza: { x: number; y: number }; color?: string }> = ({
  nombre,
  cabeza,
  color = ACENTO,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const letras = nombre.split("");
  const ancho = letras.length * PASO + 30;
  // el nombre va encima de la cabeza, un poco a la izquierda (como Ariana)
  const left = cabeza.x - ancho / 2 - 60;
  const top = cabeza.y - 290;
  const fin = { x: left + ancho + 100, y: top + 140 }; // de donde sale la flecha
  const punta = { x: cabeza.x + 140, y: cabeza.y + 20 };

  const flecha = interpolate(frame, [10, 18], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const chispa = spring({ frame: frame - 9, fps, config: { damping: 10, stiffness: 220 } });
  const letra = (txt: string, extra: React.CSSProperties) => (
    <span style={{ position: "absolute", left: 0, top: 0, fontFamily: MANO, fontWeight: 700, fontSize: 200, lineHeight: 1, ...extra }}>
      {txt}
    </span>
  );
  const sx = left, sy = top + 30; // destellos

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <div style={{ position: "absolute", left, top, width: ancho, height: 210, transform: "rotate(-4deg)" }}>
        {letras.map((l, i) => {
          const p = DESORDEN[i % DESORDEN.length];
          const k = spring({ frame: frame - i * 1.5, fps, config: { damping: 11, stiffness: 170, mass: 0.7 } });
          return (
            <div
              key={i}
              style={{
                position: "absolute",
                left: i * PASO,
                top: 0,
                width: 110,
                height: 210,
                opacity: interpolate(k, [0, 0.15], [0, 1], { extrapolateRight: "clamp" }),
                transform: `translate(${(1 - k) * p.dx}px, ${(1 - k) * p.dy}px) rotate(${(1 - k) * p.r}deg) scale(${1 + (1 - k) * (p.s - 1)})`,
              }}
            >
              {letra(l, { color: "white", WebkitTextStroke: "26px white", filter: "drop-shadow(0 6px 10px rgba(0,0,0,0.45))" })}
              {letra(l, { color: "#55601A", transform: "translate(6px, 7px)" })}
              {letra(l, { color })}
            </div>
          );
        })}
      </div>
      <svg width={1080} height={1920} style={{ position: "absolute", left: 0, top: 0 }}>
        <g stroke="white" strokeWidth={9} strokeLinecap="round" opacity={chispa} transform={`translate(${sx} ${sy}) scale(${chispa}) translate(${-sx} ${-sy})`}>
          <line x1={sx - 12} y1={sy - 12} x2={sx - 42} y2={sy - 46} />
          <line x1={sx + 18} y1={sy - 30} x2={sx + 12} y2={sy - 72} />
        </g>
        <path
          d={`M ${fin.x - 50} ${fin.y} C ${fin.x} ${fin.y + 60}, ${fin.x - 40} ${punta.y - 30}, ${punta.x} ${punta.y}`}
          fill="none"
          stroke="white"
          strokeWidth={9}
          strokeLinecap="round"
          pathLength={1}
          strokeDasharray={1}
          strokeDashoffset={flecha}
        />
        <path
          d={`M ${punta.x + 32} ${punta.y - 35} L ${punta.x - 2} ${punta.y + 1} L ${punta.x + 44} ${punta.y + 18}`}
          fill="none"
          stroke="white"
          strokeWidth={9}
          strokeLinecap="round"
          strokeLinejoin="round"
          opacity={flecha < 0.05 ? 1 : 0}
        />
      </svg>
    </AbsoluteFill>
  );
};
