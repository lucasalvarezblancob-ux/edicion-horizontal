import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  interpolate,
  Sequence,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Clave, Palabra, Subtitulos, Titulo } from "../../comun/Subtitulos";
import palabras from "./voz-palabras.json";

// Archivos en public/jalon-espalda-dorito/
const SRC = staticFile("jalon-espalda-dorito/proxy.mp4"); // bruto: recursos/gym/espalda/2026-10-31_jalon-al-pecho_espalda-y-lateral.MOV
const MUSIC = staticFile("jalon-espalda-dorito/musica.mp3");
const VOZ = staticFile("jalon-espalda-dorito/voz.mp3"); // Alberto Rodríguez (ElevenLabs), cierre "Sígueme para más, perra."
const VOZ_DESDE = 3; // frames: la voz entra a los 0,1 s

// Cortes con transición "whip" (zoom + desenfoque) y destello
const WHIPS = [81, 695];
const FLASH = 695;
// "Uf, cómo quema" -> temblor de cámara
const SHAKE: [number, number] = [591, 614];

// Cada plano: entra con un punch-in y sigue empujando despacio para que nunca esté quieto.
const Shot: React.FC<{ children: React.ReactNode; punch?: number; zoom?: number }> = ({
  children,
  punch = 0.07,
  zoom = 1,
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 7], [punch, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const drift = frame * 0.0006;
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom + p + drift})`, transformOrigin: "50% 40%" }}>{children}</AbsoluteFill>
  );
};

export const JalonEspaldaDorito: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();

  // Whip: desenfoque + zoom alrededor de los cortes marcados
  let blur = 0;
  let whipScale = 0;
  for (const c of WHIPS) {
    const d = Math.abs(frame - c + 0.5);
    if (d < 4) {
      const k = 1 - d / 4;
      blur = Math.max(blur, 14 * k);
      whipScale = Math.max(whipScale, 0.12 * k);
    }
  }
  const flash = interpolate(frame, [FLASH - 1, FLASH, FLASH + 5], [0, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const enShake = frame >= SHAKE[0] && frame <= SHAKE[1];
  const shakeAmt = enShake
    ? interpolate(frame, SHAKE, [16, 2], { extrapolateRight: "clamp" })
    : 0;
  const sx = enShake ? Math.sin(frame * 2.7) * shakeAmt : 0;
  const sy = enShake ? Math.cos(frame * 3.3) * shakeAmt : 0;

  const fadeOut = interpolate(frame, [durationInFrames - 8, durationInFrames], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <AbsoluteFill
        style={{
          opacity: fadeOut,
          filter: `contrast(1.12) saturate(0.82) brightness(0.96) blur(${blur}px)`,
          transform: `translate(${sx}px, ${sy}px) scale(${1 + whipScale + (enShake ? 0.04 : 0)})`,
        }}
      >
        <Series>
          {/* Gancho: "¿Qué pasa, perras? Este es mi entreno..." */}
          <Series.Sequence name="Intro sudadera" durationInFrames={81} premountFor={fps}>
            <Shot punch={0.12}>
              <Video src={SRC} trimBefore={30} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "Empezamos con jalón al pecho" */}
          <Series.Sequence name="Espalda · baja 1" durationInFrames={66} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={837} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          <Series.Sequence name="Lado · sube 1" durationInFrames={34} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1540} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "El truco es agarrar..." */}
          <Series.Sequence name="Espalda · baja 2" durationInFrames={35} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={969} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          <Series.Sequence name="Lado · sube 2" durationInFrames={33} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1647} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "...tirar con los codos. Sacas pecho, bajas la barra" — plano cerrado */}
          <Series.Sequence name="Lado cerrado · baja 2" durationInFrames={80} premountFor={fps}>
            <Shot zoom={1.22} punch={0.1}>
              <Video src={SRC} trimBefore={1680} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          <Series.Sequence name="Espalda · sube 3" durationInFrames={53} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={904} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          <Series.Sequence name="Lado · baja 3" durationInFrames={43} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1497} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "Arriba estiras del todo" */}
          <Series.Sequence name="Espalda · sube 4" durationInFrames={61} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1004} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "Cero balanceo" — de lado se ve el torso */}
          <Series.Sequence name="Lado · baja 4" durationInFrames={61} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1862} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          <Series.Sequence name="Espalda · sube 5" durationInFrames={52} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1109} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "Uf, cómo quema" */}
          <Series.Sequence name="Lado · baja 5" durationInFrames={45} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1968} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "Así se construye una espalda..." */}
          <Series.Sequence name="Espalda · sube 6" durationInFrames={33} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={1209} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          <Series.Sequence name="Suelta la barra" durationInFrames={18} premountFor={fps}>
            <Shot>
              <Video src={SRC} trimBefore={2070} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
          {/* "Sígueme para más, perra." */}
          <Series.Sequence name="Cara a cámara" durationInFrames={durationInFrames - 695} premountFor={fps}>
            <Shot punch={0.15}>
              <Video src={SRC} trimBefore={2208} muted premountFor={fps} />
            </Shot>
          </Series.Sequence>
        </Series>
      </AbsoluteFill>

      {/* Viñeta */}
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          background:
            "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
        }}
      />
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      {/* Textos por encima */}
      <Sequence name="Título" from={24} durationInFrames={57} layout="none">
        <Titulo titulo="espalda dorito" sub="jalón al pecho · 4 claves" />
      </Sequence>
      <Sequence name="Clave 1" from={163} durationInFrames={59} layout="none">
        <Clave n={1} texto="agarre ancho" />
      </Sequence>
      <Sequence name="Clave 2" from={222} durationInFrames={150} layout="none">
        <Clave n={2} texto="codos abajo, pecho fuera" />
      </Sequence>
      <Sequence name="Clave 3" from={372} durationInFrames={100} layout="none">
        <Clave n={3} texto="estira arriba del todo" />
      </Sequence>
      <Sequence name="Clave 4" from={472} durationInFrames={119} layout="none">
        <Clave n={4} texto="cero balanceo" />
      </Sequence>

      <Subtitulos palabras={palabras as Palabra[]} offset={VOZ_DESDE / fps} />

      {/* Audio: voz delante, música por debajo */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={VOZ} volume={1} />
      </Sequence>
      <Audio src={MUSIC} volume={0.22} />
    </AbsoluteFill>
  );
};

export const JalonEspaldaDoritoComp = () => (
  <Composition
    id="JalonEspaldaDorito"
    component={JalonEspaldaDorito}
    durationInFrames={745}
    fps={30}
    width={1080}
    height={1920}
  />
);
