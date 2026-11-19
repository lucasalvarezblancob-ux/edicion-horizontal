import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";

// V4 de posing-gold (2026-11-19). Mismo bruto, proxy y canción que la V1 (PosingGold.tsx, ver su comentario).
// Lucas sobre la V3: "no tanto zoom, cortes está bien o más, mejores momentos". → Encuadre siempre el horizontal entero
// centrado con un zoom casi imperceptible (×1,00–1,02, alterna acercar / alejar), sin punch-ins. 25 planos (V3: 19):
// intro 1 por compás; después cada frase = 4 + 2·6 pulsos. Planos elegidos con hojas de contactos cada 0,5 s: solo poses
// en su punto (camisetas arriba, poses de lado, bíceps, brazo arriba, brazos detrás de la cabeza), nada de transiciones
// entre poses. El drop cae justo cuando Lucas se sube la camiseta (36,5 s del bruto).

const FPS = 25;
const s = (t: number) => Math.round(t * FPS);
const PULSO = 0.46235;
const p = (n: number) => Math.round(n * PULSO * FPS);
const DROP = 16;

const FRASE = [4, 2, 2, 2, 2, 2, 2];
const DURACIONES_PULSO = [4, 4, 4, 4, ...FRASE, ...FRASE, ...FRASE];
const CORTES_PULSO = DURACIONES_PULSO.reduce<number[]>((acc, d) => [...acc, acc[acc.length - 1] + d], [0]);
const CORTES = CORTES_PULSO.map(p);

// trim = segundo del bruto/proxy donde arranca cada plano (cronológico, sin repetir tramos).
const TRIMS: { name: string; t: number }[] = [
  // intro (subida al drop)
  { name: "1 · de frente, relajados", t: 24.0 },
  { name: "2 · relajados, chica izq. melena", t: 27.0 },
  { name: "3 · manos juntas, pecho", t: 30.2 },
  { name: "4 · manos juntas (zoom suave que acelera)", t: 33.6 },
  // frase 1 (drop)
  { name: "5 · DROP · Lucas se sube la camiseta", t: 36.5 },
  { name: "6 · camiseta arriba, abdominales", t: 38.6 },
  { name: "7 · camiseta arriba 2", t: 40.0 },
  { name: "8 · camiseta arriba, chica melena", t: 41.2 },
  { name: "9 · pecho, chica dcha. mano en la cadera", t: 46.5 },
  { name: "10 · pecho 2", t: 48.0 },
  { name: "11 · pose de lado", t: 51.0 },
  // frase 2
  { name: "12 · pose de lado, todos", t: 52.2 },
  { name: "13 · pose de lado, chicas", t: 55.0 },
  { name: "14 · pose de lado 2", t: 56.6 },
  { name: "15 · bíceps", t: 62.4 },
  { name: "16 · bíceps 2", t: 63.6 },
  { name: "17 · bíceps 3", t: 64.8 },
  { name: "18 · brazo arriba", t: 70.0 },
  // frase 3
  { name: "19 · brazo arriba, chicas de lado", t: 71.2 },
  { name: "20 · brazo arriba 2", t: 76.0 },
  { name: "21 · brazos detrás de la cabeza, chica dcha. de espaldas", t: 78.0 },
  { name: "22 · brazos detrás de la cabeza", t: 80.0 },
  { name: "23 · brazos detrás de la cabeza 2", t: 82.4 },
  { name: "24 · todos brazos detrás de la cabeza", t: 84.6 },
  { name: "25 · final, todos brazos detrás de la cabeza", t: 86.8 },
];
const PLANOS = TRIMS.map((x, i) => ({ ...x, trim: s(x.t), desde: CORTES[i], hasta: CORTES[i + 1], i }));
export const DURACION_V4 = CORTES[CORTES.length - 1];

const ALTO = Math.round((1080 * 9) / 16); // 608
const TOP = Math.round((1920 - ALTO) / 2);

const Plano: React.FC<{ trim: number; d: number; i: number }> = ({ trim, d, i }) => {
  const frame = useCurrentFrame();
  const acelera = i === 3;
  const [z0, z1] = acelera ? [1.0, 1.03] : i % 2 === 0 ? [1.0, 1.02] : [1.02, 1.0];
  const z = interpolate(frame, [0, d], [z0, z1], { easing: acelera ? Easing.in(Easing.cubic) : Easing.inOut(Easing.sin) });
  return (
    <AbsoluteFill style={{ transform: `scale(${z})`, transformOrigin: "50% 50%" }}>
      <Video src={staticFile("posing-gold/proxy.mp4")} trimBefore={trim} muted />
    </AbsoluteFill>
  );
};

export const PosingGoldV4: React.FC = () => {
  const frame = useCurrentFrame();
  const negro = Math.max(
    interpolate(frame, [0, 8], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
    interpolate(frame, [DURACION_V4 - 12, DURACION_V4], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
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
        volume={(f) => interpolate(f, [DURACION_V4 - 25, DURACION_V4], [0.36, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
      />
    </AbsoluteFill>
  );
};

export const PosingGoldV4Comp: React.FC = () => (
  <Composition id="PosingGoldV4" component={PosingGoldV4} durationInFrames={DURACION_V4} fps={FPS} width={1080} height={1920} />
);
