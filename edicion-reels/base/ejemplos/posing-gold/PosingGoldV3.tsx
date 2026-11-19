import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

// V3 de posing-gold (2026-11-19). Mismo bruto, proxy, canción, cortes y planos que la V1 (PosingGold.tsx, ver su comentario).
// Lucas: "como la v1 pero elimina los zooms a las personas, que sea más chill". → Encuadre SIEMPRE el horizontal entero
// centrado (sin punto de foco ni paneo) y solo un zoom lento y suave por plano (alterna acercar / alejar, ×1,00–1,06),
// sin punch-ins ni golpes. Se queda el zoom que acelera en el último plano de la intro y el destello del drop.

const FPS = 25;
const s = (t: number) => Math.round(t * FPS);
const PULSO = 0.46235;
const p = (n: number) => Math.round(n * PULSO * FPS);
const DROP = 16;

// Los mismos cortes que la V1: intro 1 plano por compás; después 1 por compás y el último compás de cada frase en 2 + 2.
const CORTES_PULSO = [0, 4, 8, 12, 16, 20, 24, 28, 30, 32, 36, 40, 44, 46, 48, 52, 56, 60, 62, 64];
const CORTES = CORTES_PULSO.map(p);

// Los mismos trims que la V1.
const TRIMS: { name: string; t: number }[] = [
  { name: "1 · general, de frente", t: 24.0 },
  { name: "2 · chica izq., melena", t: 26.5 },
  { name: "3 · chicos, manos juntas", t: 30.2 },
  { name: "4 · general, zoom que acelera al drop", t: 44.2 },
  { name: "5 · DROP · se sube la camiseta", t: 37.6 },
  { name: "6 · general, camisetas arriba", t: 39.5 },
  { name: "7 · chico de frente", t: 47.0 },
  { name: "8 · pecho de lado (2 pulsos)", t: 50.8 },
  { name: "9 · flexión chica dcha. (2 pulsos)", t: 55.0 },
  { name: "10 · general, bíceps", t: 61.0 },
  { name: "11 · bíceps chica dcha.", t: 63.4 },
  { name: "12 · brazo arriba", t: 67.6 },
  { name: "13 · calvo + chica dcha. (2 pulsos)", t: 71.0 },
  { name: "14 · todos flexionando (2 pulsos)", t: 75.0 },
  { name: "15 · chica izq. + chico", t: 77.0 },
  { name: "16 · suben los brazos", t: 79.8 },
  { name: "17 · chico, brazos arriba", t: 82.4 },
  { name: "18 · chica izq., brazos arriba (2 pulsos)", t: 84.5 },
  { name: "19 · final, brazos arriba (2 pulsos)", t: 86.5 },
];
const PLANOS = TRIMS.map((x, i) => ({ ...x, trim: s(x.t), desde: CORTES[i], hasta: CORTES[i + 1], i }));
export const DURACION_V3 = CORTES[CORTES.length - 1];

const ALTO = Math.round((1080 * 9) / 16); // 608
const TOP = Math.round((1920 - ALTO) / 2);

const Plano: React.FC<{ trim: number; d: number; i: number }> = ({ trim, d, i }) => {
  const frame = useCurrentFrame();
  const acelera = i === 3;
  const [z0, z1] = acelera ? [1.0, 1.08] : i % 2 === 0 ? [1.0, 1.05] : [1.05, 1.0];
  const z = interpolate(frame, [0, d], [z0, z1], { easing: acelera ? Easing.in(Easing.cubic) : Easing.inOut(Easing.sin) });
  return (
    <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: "50% 50%" }}>
      <Video src={staticFile("posing-gold/proxy.mp4")} trimBefore={trim} muted />
    </AbsoluteFill>
  );
};

export const PosingGoldV3: React.FC = () => {
  const frame = useCurrentFrame();
  const negro = Math.max(
    interpolate(frame, [0, 8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    interpolate(frame, [DURACION_V3 - 12, DURACION_V3], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
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
            <Plano trim={pl.trim} d={pl.hasta - pl.desde} i={pl.i} />
          </Sequence>
        ))}
        <AbsoluteFill style={{ backgroundColor: "#fff", opacity: frame >= p(DROP) - 1 ? flash : 0 }} />
        <AbsoluteFill style={{ backgroundColor: "#000", opacity: negro }} />
      </div>
      <Audio
        src={staticFile("posing-gold/funk-infernal.mp3")}
        volume={(f) => interpolate(f, [DURACION_V3 - 25, DURACION_V3], [0.36, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
      />
    </AbsoluteFill>
  );
};

export const PosingGoldV3Comp: React.FC = () => (
  <Composition id="PosingGoldV3" component={PosingGoldV3} durationInFrames={DURACION_V3} fps={FPS} width={1080} height={1920} />
);
