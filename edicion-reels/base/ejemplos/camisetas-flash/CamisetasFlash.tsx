import { Audio, Video } from "@remotion/media";
import { loadFont as loadAnton } from "@remotion/google-fonts/Anton";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  Sequence,
  staticFile,
  useCurrentFrame,
} from "remotion";

// Elevaciones laterales con mancuerna cambiando de camiseta en cada subida/bajada.
// Bruto: recursos/gym/hombro/2026-11-01_elevaciones-laterales-9-camisetas.MOV (antes bruto/IMG_1056.MOV, 180 s, trípode fijo).
// Proxy 1080×1920 a 30 fps en public/camisetas-flash/proxy.mp4 → los números de abajo son frames del proxy.
//
// Cada media repetición dura exactamente medio pulso de la canción (corchea: 0,444 s = 13,33 frames, a ×1,0–1,3)
// y en cada corte hay destello de flash + disparo de cámara. Se corta en los extremos (arriba = brazos en cruz,
// abajo = brazos pegados), así la posición casa entre camisetas.
// Música: ElevenLabs Music (scripts/musica.mjs) → ralentizada al 90 % + reverb. musica.mp3 empieza medio pulso antes
// del drop, así el 1.er flash cae en el drop.

const { fontFamily: anton } = loadAnton();
const FPS = 30;
const PULSO = 13.333; // corchea de la canción ralentizada (67,5 BPM)

// [inicio, fin] en frames del proxy, marcados fotograma a fotograma (corrección "sobran frames", 2026-11-01):
// sube = de que arrancan los brazos al punto más alto · baja = de que empiezan a bajar a que llegan pegados al cuerpo.
// Nada de pausa arriba ni de balanceo de mancuernas abajo.
const CAMISETAS: { name: string; sube: [number, number]; baja: [number, number] }[] = [
  { name: "gris ajustada", sube: [74, 90], baja: [99, 115] },
  { name: "tirantes negra", sube: [776, 793], baja: [864, 877] },
  { name: "negra", sube: [1403, 1420], baja: [1531, 1547] },
  { name: "blanca oversize", sube: [2049, 2066], baja: [2137, 2153] },
  { name: "lila", sube: [2756, 2772], baja: [2781, 2795] },
  { name: "beige", sube: [3321, 3336], baja: [3344, 3360] },
  { name: "gris clara", sube: [4047, 4062], baja: [4072, 4087] },
  { name: "negra 2", sube: [4621, 4638], baja: [4646, 4660] },
  { name: "gris", sube: [5150, 5167], baja: [5174, 5190] },
];

// 2 vueltas a las 9 camisetas: cada una sale una vez subiendo y otra bajando. Acaba abajo con la última
// y el vídeo empieza abajo con la primera → bucle limpio.
const N = CAMISETAS.length * 2;
const CORTES = Array.from({ length: N + 1 }, (_, k) => Math.round(k * PULSO));
const PLANOS = Array.from({ length: N }, (_, k) => {
  const c = CAMISETAS[k % CAMISETAS.length];
  const fase = k % 2 === 0 ? "sube" : "baja";
  const [a, b] = c[fase];
  const d = CORTES[k + 1] - CORTES[k];
  return { name: `${k + 1} · ${c.name} · ${fase}`, desde: CORTES[k], d, trim: a, rate: (b - a) / d };
});
export const DURACION = CORTES[N];

const Plano: React.FC<{ trim: number; rate: number; primero: boolean }> = ({ trim, rate, primero }) => {
  const frame = useCurrentFrame();
  // golpe de cámara: entra un poco cerrado y se abre, luego acercamiento lento
  const punch = primero ? 0 : interpolate(frame, [0, 6], [0.07, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const escala = 1.02 + punch + frame * 0.0012;
  return (
    <AbsoluteFill style={{ transform: `scale(${escala})`, transformOrigin: "50% 35%" }}>
      <Video src={staticFile("camisetas-flash/proxy.mp4")} trimBefore={trim} playbackRate={rate} muted />
    </AbsoluteFill>
  );
};

// Destello de flash de cámara en cada corte: sube 1 frame antes, pico en el corte y se apaga en 4 frames (cortes cada 13 frames: más largo lava la imagen).
const Flash: React.FC = () => {
  const frame = useCurrentFrame();
  let o = 0;
  for (let k = 1; k < N; k++) {
    const c = CORTES[k];
    const v = interpolate(frame, [c - 1, c, c + 4], [0.25, 0.95, 0], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.quad),
    });
    o = Math.max(o, frame < c - 1 ? 0 : v);
  }
  return <AbsoluteFill style={{ backgroundColor: "#fff", opacity: o, pointerEvents: "none" }} />;
};

// Imagen base: colores originales del bruto, SIN etalonado ni viñeta (Lucas, 2026-11-01: "mantén los colores originales…
// sin tocar colores"). Antes se probaron contraste/gamma y ninguno le convenció.
const Base: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "#000" }}>
    <AbsoluteFill>
      {PLANOS.map((p, i) => (
        <Sequence key={i} name={p.name} from={p.desde} durationInFrames={p.d}>
          <Plano trim={p.trim} rate={p.rate} primero={i === 0} />
        </Sequence>
      ))}
    </AbsoluteFill>
  </AbsoluteFill>
);

// "GYMSHARK / BLACK FRIDAY" fijo encima de la cabeza (sin recorte, por delante de todo salvo el flash).
// La cabeza llega como mucho a y≈344 en su punto más alto → el bloque acaba en ≈340; empieza justo bajo la UI de arriba.
const TEXTO = { top: 206, etiqueta: 48, grande: 98 };
const Texto: React.FC = () => {
  const linea: React.CSSProperties = {
    fontFamily: anton,
    color: "#fff",
    textTransform: "uppercase",
    lineHeight: 0.92,
    textAlign: "center",
    textShadow: "0 4px 22px rgba(0,0,0,0.5)",
    whiteSpace: "nowrap",
  };
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: TEXTO.top }}>
      <div style={{ ...linea, fontSize: TEXTO.etiqueta, letterSpacing: TEXTO.etiqueta * 0.38, marginRight: -TEXTO.etiqueta * 0.38 }}>Gymshark</div>
      <div style={{ ...linea, fontSize: TEXTO.grande, letterSpacing: 2, marginTop: 4 }}>Black Friday</div>
    </AbsoluteFill>
  );
};

export const CamisetasFlash: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <Base />
      <Texto />
      <Flash />
      <Audio src={staticFile("camisetas-flash/musica.mp3")} volume={0.7} />
      {CORTES.slice(1, N).map((c, k) => (
        <Sequence key={`clic${k}`} name="disparo de cámara" from={c - 1} durationInFrames={20}>
          <Audio src={staticFile("sonidos/camara-foto-1.mp3")} volume={0.65} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const CamisetasFlashComp: React.FC = () => (
  <>
    <Composition id="CamisetasFlash" component={CamisetasFlash} durationInFrames={DURACION} fps={FPS} width={1080} height={1920} />
  </>
);
