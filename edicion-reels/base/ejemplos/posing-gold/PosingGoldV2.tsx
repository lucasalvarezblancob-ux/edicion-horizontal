import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import golpes from "./golpes.json";

// V2 de posing-gold (2026-11-19). Mismo bruto, proxy y canción que la V1 (PosingGold.tsx, ver su comentario):
// bruto Sony horizontal 4K 25 fps (horizontal/C5150.MP4), proxy 1920×1080 en public/posing-gold/proxy.mp4,
// DYGO & Mxng0 – FUNK INFERNAL (funk-infernal.mp3, 129,2 BPM, drop en el pulso 16 del vídeo).
//
// Corrección de Lucas a la V1: "zooms no se vayan hacia los lados, que sean zooms pequeños y cortes. En ningún momento
// el zoom sea a una persona concreta, sino micro zooms para hacer más dinámico el vídeo, jugando con el ruido de la
// música y cortes". → Encuadre SIEMPRE el horizontal entero centrado (sin paneo ni punto de foco), zoom ×1,00–1,10:
//   · deriva lenta por plano (alterna acercar / alejar, ±4 %),
//   · golpe de zoom en cada corte (+4 % tras el drop, +2 % en la intro),
//   · micro golpes con la percusión de la canción (golpes.json: fuerza del golpe por fotograma, 0–1, de librosa con la
//     parte percusiva; ataque inmediato y caída ×0,55 por fotograma) → +3 % máx.,
//   · en la intro, zoom que acelera hacia el drop en el último plano.
// Cortes: 25 planos (V1: 19). Intro: 1 por compás. Tras el drop, cada frase de 16 pulsos = 4 + 2·6 (un compás y luego
// cortes cada 2 pulsos, 0,92 s).

const FPS = 25;
const s = (t: number) => Math.round(t * FPS);
const PULSO = 0.46235;
const p = (n: number) => Math.round(n * PULSO * FPS);
const DROP = 16;

const FRASE = [4, 2, 2, 2, 2, 2, 2];
const DURACIONES_PULSO = [4, 4, 4, 4, ...FRASE, ...FRASE, ...FRASE];
const CORTES_PULSO = DURACIONES_PULSO.reduce<number[]>((acc, d) => [...acc, acc[acc.length - 1] + d], [0]);
const CORTES = CORTES_PULSO.map(p);

// trim = segundo del bruto/proxy donde arranca cada plano (en orden cronológico, sin repetir tramos).
const TRIMS: { name: string; t: number }[] = [
  // intro (subida al drop)
  { name: "1 · de frente, relajados", t: 24.0 },
  { name: "2 · chica izq. se toca la melena", t: 26.5 },
  { name: "3 · manos juntas", t: 30.2 },
  { name: "4 · antes de subirse la camiseta (zoom que acelera)", t: 33.6 },
  // frase 1 (drop)
  { name: "5 · DROP · camisetas arriba", t: 37.6 },
  { name: "6 · camisetas arriba", t: 39.5 },
  { name: "7 · melena / flexión", t: 41.4 },
  { name: "8 · flexión", t: 43.2 },
  { name: "9 · chico de frente", t: 47.0 },
  { name: "10 · pecho de lado", t: 50.8 },
  { name: "11 · giro", t: 52.8 },
  // frase 2
  { name: "12 · flexión chica dcha.", t: 55.0 },
  { name: "13 · bíceps", t: 61.0 },
  { name: "14 · bíceps chica dcha.", t: 63.4 },
  { name: "15 · bíceps 2", t: 65.2 },
  { name: "16 · brazo arriba", t: 67.6 },
  { name: "17 · brazo arriba 2", t: 69.4 },
  { name: "18 · calvo + chica dcha.", t: 71.2 },
  // frase 3
  { name: "19 · todos flexionando", t: 74.8 },
  { name: "20 · suben los brazos", t: 77.4 },
  { name: "21 · brazos arriba", t: 79.8 },
  { name: "22 · brazos arriba 2", t: 82.4 },
  { name: "23 · brazos detrás de la cabeza", t: 84.5 },
  { name: "24 · brazos detrás de la cabeza 2", t: 86.4 },
  { name: "25 · final, brazos arriba", t: 88.4 },
];
const PLANOS = TRIMS.map((x, i) => ({ ...x, trim: s(x.t), desde: CORTES[i], hasta: CORTES[i + 1], i }));
export const DURACION_V2 = CORTES[CORTES.length - 1];

const ALTO = Math.round((1080 * 9) / 16); // 608
const TOP = Math.round((1920 - ALTO) / 2);
const G = golpes as number[];

const Plano: React.FC<{ trim: number; d: number; i: number; desde: number }> = ({ trim, d, i, desde }) => {
  const frame = useCurrentFrame();
  const intro = i < 4;
  // deriva lenta: alterna acercar / alejar
  const [z0, z1] = i === 3 ? [1.0, 1.09] : i % 2 === 0 ? [1.02, 1.05] : [1.05, 1.02];
  const deriva = interpolate(frame, [0, d], [z0, z1], { easing: i === 3 ? Easing.in(Easing.cubic) : Easing.inOut(Easing.sin) });
  const punch = interpolate(frame, [0, 5], [intro ? 0.02 : 0.04, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const golpe = intro ? 0 : 0.03 * (G[desde + frame] ?? 0);
  const z = Math.min(1.1, deriva + punch + golpe);
  return (
    <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: "50% 50%" }}>
      <Video src={staticFile("posing-gold/proxy.mp4")} trimBefore={trim} muted />
    </AbsoluteFill>
  );
};

export const PosingGoldV2: React.FC = () => {
  const frame = useCurrentFrame();
  const negro = Math.max(
    interpolate(frame, [0, 8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    interpolate(frame, [DURACION_V2 - 12, DURACION_V2], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  );
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
            <Plano trim={pl.trim} d={pl.hasta - pl.desde} i={pl.i} desde={pl.desde} />
          </Sequence>
        ))}
        <AbsoluteFill style={{ backgroundColor: "#fff", opacity: frame >= p(DROP) - 1 ? flash : 0 }} />
        <AbsoluteFill style={{ backgroundColor: "#000", opacity: negro }} />
      </div>
      <Audio
        src={staticFile("posing-gold/funk-infernal.mp3")}
        volume={(f) => interpolate(f, [DURACION_V2 - 25, DURACION_V2], [0.36, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
      />
    </AbsoluteFill>
  );
};

export const PosingGoldV2Comp: React.FC = () => (
  <Composition id="PosingGoldV2" component={PosingGoldV2} durationInFrames={DURACION_V2} fps={FPS} width={1080} height={1920} />
);
