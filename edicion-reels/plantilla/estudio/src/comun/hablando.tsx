// Componentes para vídeos HABLANDO A CÁMARA (ver refs/hablando a camara/CONTEXTO.md).
import { Audio } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Easing,
  Img,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ACENTO, CREMA, F_FUERTE, F_RELLENO, F_REMATE, F_SUB } from "./marca";

// Color y fuentes en ./marca.ts (local de cada carpeta). Se reexportan para los vídeos que los importan de aquí.
export { ACENTO, CREMA, F_FUERTE, F_RELLENO, F_REMATE, F_SUB };

// ---------------------------------------------------------------- palabras
export type Palabra = { w: string; start: number; end: number };
export type Estilo = "relleno" | "fuerte" | "remate" | "clave";

// Una palabra en pantalla: aparece en su frame (seco o con pop) y se queda hasta que acaba su bloque.
export type PalabraEnBloque = { texto: string; desde: number; estilo: Estilo; salto?: boolean };
export type Bloque = { desde: number; hasta: number; palabras: PalabraEnBloque[]; y?: number };

const estiloCss = (e: Estilo, escala: number, color: { fuerte: string; remate: string; relleno: string }): React.CSSProperties => {
  switch (e) {
    case "fuerte":
      return { fontFamily: F_FUERTE, fontSize: 150 * escala, color: color.fuerte, textTransform: "uppercase", lineHeight: 0.95, letterSpacing: 0 };
    case "remate":
      return { fontFamily: F_REMATE, fontStyle: "italic", fontSize: 130 * escala, color: color.remate, lineHeight: 0.95 };
    case "clave":
      return { fontFamily: F_RELLENO, fontWeight: 800, fontSize: 110 * escala, color: color.relleno, letterSpacing: -2, lineHeight: 1 };
    default:
      return { fontFamily: F_RELLENO, fontWeight: 600, fontSize: 62 * escala, color: color.relleno, letterSpacing: -1, lineHeight: 1.05 };
  }
};

// Texto que se construye palabra a palabra (estilo refs: entrada seca o pop de 3 frames).
export const TextoBloques: React.FC<{
  bloques: Bloque[];
  pop?: boolean;
  escala?: number;
  colores?: { fuerte: string; remate: string; relleno: string };
  sombra?: string;
  interlinea?: number; // px extra entre líneas (Anton con lineHeight 0,95 pisa la línea pequeña de encima)
}> = ({ bloques, pop = false, escala = 1, colores = { fuerte: ACENTO, remate: "white", relleno: CREMA }, sombra = "0 4px 22px rgba(0,0,0,0.55), 0 2px 4px rgba(0,0,0,0.5)", interlinea = 0 }) => {
  const frame = useCurrentFrame();
  const b = bloques.find((x) => frame >= x.desde && frame < x.hasta);
  if (!b) return null;
  // líneas separadas por `salto`
  const lineas: PalabraEnBloque[][] = [[]];
  b.palabras.forEach((p) => {
    if (p.salto && lineas[lineas.length - 1].length) lineas.push([]);
    lineas[lineas.length - 1].push(p);
  });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
      <div style={{ position: "absolute", top: `${(b.y ?? 0.5) * 100}%`, transform: "translateY(-50%)", width: 1000, textAlign: "center" }}>
        {lineas.map((l, i) => (
          <div key={i} style={{ display: "flex", justifyContent: "center", alignItems: "baseline", gap: 18 * escala, flexWrap: "wrap", marginTop: i ? interlinea : 0 }}>
            {l.map((p, j) => {
              const visible = frame >= p.desde;
              const s = pop ? interpolate(frame - p.desde, [0, 3], [0.6, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) }) : 1;
              return (
                <span key={j} style={{ ...estiloCss(p.estilo, escala, colores), opacity: visible ? 1 : 0, transform: `scale(${s})`, display: "inline-block", textShadow: sombra }}>
                  {p.texto}
                </span>
              );
            })}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- cámara virtual
// Encuadre por tramos: escala y centro (en px del vídeo 1080×1920). `suave` = frames de transición (0 = corte seco).
export type Encuadre = { desde: number; escala: number; cx?: number; cy?: number; suave?: number; empuje?: number };

export const CamaraVirtual: React.FC<{
  encuadres: Encuadre[];
  cara?: number[][]; // [cx,cy,w,h] por frame del bruto (seguir_cara.py)
  frameBruto?: (f: number) => number; // mapea frame del edit → frame del bruto (para la cara)
  shake?: { desde: number; hasta: number; px: number }[];
  children: React.ReactNode;
}> = ({ encuadres, cara, frameBruto, shake = [], children }) => {
  const frame = useCurrentFrame();
  let i = 0;
  for (let k = 0; k < encuadres.length; k++) if (frame >= encuadres[k].desde) i = k;
  const e = encuadres[i];
  const prev = encuadres[Math.max(0, i - 1)];
  const k = e.suave && i > 0 ? interpolate(frame, [e.desde, e.desde + e.suave], [0, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 1;
  const empuje = 1 + (e.empuje ?? 0) * (frame - e.desde) / 30; // empuje lento continuo (por segundo)
  const escala = (prev.escala + (e.escala - prev.escala) * k) * empuje;
  const f = frameBruto ? frameBruto(frame) : frame;
  const c = cara ? cara[Math.min(cara.length - 1, Math.max(0, Math.round(f)))] : null;
  const ccx = e.cx ?? (c ? c[0] : 540);
  const ccy = e.cy ?? (c ? c[1] : 960);
  const pcx = prev.cx ?? (c ? c[0] : 540);
  const pcy = prev.cy ?? (c ? c[1] : 960);
  const cx = pcx + (ccx - pcx) * k;
  const cy = pcy + (ccy - pcy) * k;
  // Lleva el punto (cx,cy) hacia el centro según la escala, sin dejar bordes vacíos.
  const tx = Math.max(Math.min((540 - cx) * (escala - 1), (escala - 1) * 540), -(escala - 1) * 540);
  const ty = Math.max(Math.min((760 - cy) * (escala - 1), (escala - 1) * 960), -(escala - 1) * 960);
  let sx = 0, sy = 0;
  for (const s of shake) {
    if (frame >= s.desde && frame <= s.hasta) {
      const a = interpolate(frame, [s.desde, s.hasta], [s.px, 0]);
      sx += Math.sin(frame * 2.7) * a;
      sy += Math.cos(frame * 3.3) * a;
    }
  }
  return (
    <AbsoluteFill style={{ transform: `translate(${tx + sx}px, ${ty + sy}px) scale(${escala})`, transformOrigin: "50% 50%" }}>
      {children}
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- persona por delante del texto
export const PersonaEncima: React.FC<{ carpeta: string; frameBruto: (f: number) => number; ancho?: number }> = ({ carpeta, frameBruto }) => {
  const frame = useCurrentFrame();
  const f = Math.round(frameBruto(frame));
  return <Img src={staticFile(`${carpeta}/f${String(f).padStart(5, "0")}.png`)} style={{ width: 1080, height: 1920, position: "absolute" }} />;
};

// ---------------------------------------------------------------- efectos de sonido
export const Sfx: React.FC<{ en: number; src: string; volumen?: number }> = ({ en, src, volumen = 0.6 }) => {
  const { fps } = useVideoConfig();
  return (
    <Sequence from={Math.max(0, en)} durationInFrames={fps * 3} layout="none" name={`SFX ${src}`}>
      <Audio src={staticFile(`sonidos/${src}`)} volume={volumen} />
    </Sequence>
  );
};
