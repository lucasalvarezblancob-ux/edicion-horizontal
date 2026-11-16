import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

// Posing en grupo (Lucas + 3) delante del espejo de Gold's Gym, estilo David Laid (refs/posing/).
// Bruto: Sony horizontal 4K 25 fps SDR bt709, 97 s (horizontal/C5150.MP4).
// Proxy 1920×1080 a 25 fps (sin tocar el color) en public/posing-gold/proxy.mp4.
//
// Reel vertical con el vídeo HORIZONTAL tal cual, a todo el ancho y franjas negras arriba y abajo (Lucas: "un horizontal
// sin más, no girado"). Sin texto ni SFX.
// Composición a 25 fps (los fps del bruto) para que no haya tirones de 25→30.
//
// Música (elegida por Lucas): DYGO & Mxng0 – FUNK INFERNAL [Brazilian Phonk] (YouTube A8DLRWL9_Y8), tal cual, sin slowed.
// 129,2 BPM → pulso 0,46235 s; pulsos de la canción en 0,0429 + 0,46235·k; drop en el pulso 30 (13,93 s).
// funk-infernal.mp3 empieza en el pulso 14 (6,516 s) = 4 compases antes del drop → el drop cae en el pulso 16 del vídeo.

const FPS = 25;
const s = (t: number) => Math.round(t * FPS);
const PULSO = 0.46235;
const p = (n: number) => Math.round(n * PULSO * FPS); // pulso n del vídeo → frame
const DROP = 16;

// Cortes en pulsos: intro de 4 compases con un plano por compás; después del drop, un plano por compás y el último
// compás de cada frase (16 pulsos) partido en dos (2 + 2) para dar golpe.
const CORTES_PULSO = [0, 4, 8, 12, 16, 20, 24, 28, 30, 32, 36, 40, 44, 46, 48, 52, 56, 60, 62, 64];
const CORTES = CORTES_PULSO.map(p);

// Encuadre: z = zoom (1 = horizontal entero), f = punto que queda en el centro, en px del proxy 1920×1080.
// Corrección 2026-11-01: zoom máx. ~×1,5 y foco en el tronco (enseñar el físico), nunca en la cara; cabeza entera.
// z0 → z1 a lo largo del plano; punch = golpe de zoom al entrar (6 f); acelera = el zoom se acelera (subida al drop).
type Encuadre = { name: string; trim: number; z0: number; z1: number; f: [number, number]; punch?: number; acelera?: boolean };
const ENCUADRES: Encuadre[] = [
  // intro (subida al drop)
  { name: "1 · general, de frente", trim: s(24.0), z0: 1.0, z1: 1.06, f: [960, 540] },
  { name: "2 · medio chica izq., melena", trim: s(26.5), z0: 1.38, z1: 1.3, f: [420, 640] },
  { name: "3 · medio chicos, manos juntas", trim: s(30.2), z0: 1.3, z1: 1.38, f: [900, 620] },
  { name: "4 · general, zoom que acelera al drop", trim: s(44.2), z0: 1.0, z1: 1.3, f: [900, 600], acelera: true },
  // frase 1 (drop)
  { name: "5 · DROP · se sube la camiseta", trim: s(37.6), z0: 1.42, z1: 1.48, f: [760, 600], punch: 0.1 },
  { name: "6 · general, camisetas arriba", trim: s(39.5), z0: 1.15, z1: 1.0, f: [900, 600] },
  { name: "7 · medio chico de frente", trim: s(47.0), z0: 1.32, z1: 1.4, f: [850, 600], punch: 0.06 },
  { name: "8 · medio pecho de lado (2 pulsos)", trim: s(50.8), z0: 1.4, z1: 1.45, f: [820, 600], punch: 0.06 },
  { name: "9 · medio flexión chica dcha. (2 pulsos)", trim: s(55.0), z0: 1.4, z1: 1.45, f: [1400, 600], punch: 0.06 },
  // frase 2
  { name: "10 · general, bíceps", trim: s(61.0), z0: 1.0, z1: 1.06, f: [960, 540], punch: 0.08 },
  { name: "11 · medio bíceps chica dcha.", trim: s(63.4), z0: 1.35, z1: 1.42, f: [1340, 580], punch: 0.06 },
  { name: "12 · medio, brazo arriba", trim: s(67.6), z0: 1.28, z1: 1.38, f: [820, 580] },
  { name: "13 · medio calvo + chica dcha. (2 pulsos)", trim: s(71.0), z0: 1.38, z1: 1.42, f: [1220, 640], punch: 0.06 },
  { name: "14 · general, todos flexionando (2 pulsos)", trim: s(75.0), z0: 1.12, z1: 1.04, f: [960, 560], punch: 0.06 },
  // frase 3
  { name: "15 · medio chica izq. + chico", trim: s(77.0), z0: 1.32, z1: 1.4, f: [520, 620], punch: 0.06 },
  { name: "16 · general, suben los brazos", trim: s(79.8), z0: 1.0, z1: 1.08, f: [960, 560] },
  { name: "17 · medio chico, brazos arriba", trim: s(82.4), z0: 1.38, z1: 1.45, f: [820, 520], punch: 0.06 },
  { name: "18 · medio chica izq., brazos arriba (2 pulsos)", trim: s(84.5), z0: 1.4, z1: 1.45, f: [450, 600], punch: 0.06 },
  { name: "19 · general final, brazos arriba (2 pulsos)", trim: s(86.5), z0: 1.12, z1: 1.0, f: [960, 560], punch: 0.06 },
];
const PLANOS = ENCUADRES.map((e, i) => ({ ...e, desde: CORTES[i], hasta: CORTES[i + 1] }));
export const DURACION = CORTES[CORTES.length - 1];

// Caja del vídeo horizontal: 1080 de ancho, centrada.
const ALTO = Math.round((1080 * 9) / 16); // 608
const TOP = Math.round((1920 - ALTO) / 2);
const K = 1080 / 1920; // px del proxy → px de la caja

const Plano: React.FC<{ e: Encuadre; d: number }> = ({ e, d }) => {
  const frame = useCurrentFrame();
  const punch = e.punch ? interpolate(frame, [0, 6], [e.punch, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }) : 0;
  const z =
    interpolate(frame, [0, d], [e.z0, e.z1], { easing: e.acelera ? Easing.in(Easing.cubic) : Easing.inOut(Easing.sin) }) * (1 + punch);
  // el punto f al centro de la caja, sin dejar ver bordes
  const tx = Math.min(0, Math.max(1080 - z * 1080, 540 - z * e.f[0] * K));
  const ty = Math.min(0, Math.max(ALTO - z * ALTO, ALTO / 2 - z * e.f[1] * K));
  return (
    <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) scale(${z})`, transformOrigin: "0 0" }}>
      <Video src={staticFile("posing-gold/proxy.mp4")} trimBefore={e.trim} muted />
    </AbsoluteFill>
  );
};

export const PosingGold: React.FC = () => {
  const frame = useCurrentFrame();
  const negro = Math.max(
    interpolate(frame, [0, 8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    interpolate(frame, [DURACION - 12, DURACION], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  );
  // único destello del vídeo: en el drop
  const flash = interpolate(frame, [p(DROP) - 1, p(DROP), p(DROP) + 6], [0.3, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.quad),
  });
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <div style={{ position: "absolute", left: 0, top: TOP, width: 1080, height: ALTO, overflow: "hidden" }}>
        {PLANOS.map((pl) => (
          <Sequence key={pl.name} name={pl.name} from={pl.desde} durationInFrames={pl.hasta - pl.desde}>
            <Plano e={pl} d={pl.hasta - pl.desde} />
          </Sequence>
        ))}
        <AbsoluteFill style={{ backgroundColor: "#fff", opacity: frame >= p(DROP) - 1 ? flash : 0 }} />
        <AbsoluteFill style={{ backgroundColor: "#000", opacity: negro }} />
      </div>
      <Audio
        src={staticFile("posing-gold/funk-infernal.mp3")}
        volume={(f) => interpolate(f, [DURACION - 25, DURACION], [0.36, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
      />
    </AbsoluteFill>
  );
};

export const PosingGoldComp: React.FC = () => (
  <Composition id="PosingGold" component={PosingGold} durationInFrames={DURACION} fps={FPS} width={1080} height={1920} />
);
