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

// Proxies 1080×1920 a 30 fps en public/rutina-hibrida/c<IMG>.mp4. Brutos en recursos/gym/{fisico,cardio,piernas,funcional}/2026-11-01_hibrido_…:
//   c6116 intro-sentado-cajon-nike-strength · c6370 skierg-lateral · c6369 zancadas-kettlebell-con-amigo
//   c6120 paseo-granjero-mancuernas · c6123 wall-balls-contrapicado · c6125 wall-balls-lateral · c6128 cinta-de-frente
const clip = (id: string) => staticFile(`rutina-hibrida/c${id}.mp4`);
const VOZ = staticFile("rutina-hibrida/voz.mp3"); // Alberto Rodríguez ×1,25 sin silencios
const VOZ_DESDE = 3;
const DURACION = 990;

type Plano = {
  name: string;
  c: string; // id del clip
  t: number; // segundo del clip donde empieza
  d: number; // frames
  zoom?: number;
  origen?: string;
  punch?: number;
  rate?: number;
};

// Cortes en los extremos del movimiento (arriba/abajo) para que la posición case.
const PLANOS: Plano[] = [
  // ── Gancho: "¿Qué pasa, perras? Esta es mi rutina híbrida para estar fuerte y aun así poder correr sin morir."
  { name: "Intro · sentado", c: "6116", t: 4.05, d: 64, punch: 0.15 },
  { name: "Gancho · wall ball (fuerte)", c: "6123", t: 4.0, d: 21 },
  { name: "Gancho · cinta (correr)", c: "6128", t: 10.0, d: 28, zoom: 1.2, origen: "50% 35%" },
  { name: "Gancho · bebe agua (sin morir)", c: "6116", t: 13.45, d: 18, zoom: 1.3, origen: "50% 50%" },
  // ── 1 SkiErg (tiempo continuo, cambia el encuadre en cada extremo)
  { name: "Ski · abierto", c: "6370", t: 4.37, d: 57 },
  { name: "Ski · brazos (remar de pie / truco)", c: "6370", t: 6.27, d: 44, zoom: 1.45, origen: "58% 30%" },
  { name: "Ski · cadera", c: "6370", t: 7.73, d: 40, zoom: 1.5, origen: "58% 55%" },
  // ── 2 Zancadas: alterna de espaldas / de frente
  { name: "Zancadas · de espaldas", c: "6369", t: 4.83, d: 45, zoom: 1.05 },
  { name: "Zancadas · rodilla al suelo (cerrado)", c: "6369", t: 39.77, d: 45, zoom: 1.5, origen: "60% 62%" },
  { name: "Zancadas · con un amigo", c: "6369", t: 41.27, d: 20, zoom: 1.1 },
  { name: "Zancadas · llegan a cámara", c: "6369", t: 41.94, d: 40, zoom: 1.3, origen: "50% 58%" },
  // ── 3 Paseo del granjero: alterna de frente / de espaldas
  { name: "Granjero · de frente", c: "6120", t: 22.57, d: 26, zoom: 1.1 },
  { name: "Granjero · espalda cerca (mancuernas)", c: "6120", t: 1.37, d: 30 },
  { name: "Granjero · de frente cerrado", c: "6120", t: 24.27, d: 29, zoom: 1.35, origen: "50% 58%" },
  { name: "Granjero · se aleja", c: "6120", t: 9.0, d: 17, zoom: 1.15, origen: "50% 55%" },
  { name: "Granjero · llega (sin carro)", c: "6120", t: 26.5, d: 17 },
  // ── 4 Wall balls: lateral (sentadilla) ↔ contrapicado (lanzamiento)
  { name: "WB lateral · arriba→sentadilla", c: "6125", t: 13.77, d: 37 },
  { name: "WB contrapicado · lanza 1", c: "6123", t: 5.87, d: 26 },
  { name: "WB lateral · recoge→sentadilla", c: "6125", t: 16.02, d: 23 },
  { name: "WB contrapicado · lanza 2", c: "6123", t: 7.6, d: 26 },
  { name: "WB lateral · recoge→sentadilla 2", c: "6125", t: 17.82, d: 23 },
  { name: "WB · cara (uf, cómo quema)", c: "6123", t: 36.3, d: 27 },
  // ── 5 Cinta
  { name: "Cinta · abierto", c: "6128", t: 20.0, d: 31 },
  { name: "Cinta · piernas", c: "6128", t: 21.03, d: 29, zoom: 1.6, origen: "50% 82%" },
  { name: "Cinta · cara", c: "6128", t: 22.0, d: 27, zoom: 1.45, origen: "50% 22%" },
  { name: "Cinta · abierto 2", c: "6128", t: 40.0, d: 29, zoom: 1.05 },
  // ── Ráfaga: "Fuerza y pulmones en el mismo entreno, que estar fuerte y ahogarte subiendo al metro no es un plan."
  { name: "Ráfaga · wall ball", c: "6125", t: 18.95, d: 17 },
  { name: "Ráfaga · ski", c: "6370", t: 10.0, d: 16, zoom: 1.2 },
  { name: "Ráfaga · zancadas", c: "6369", t: 41.3, d: 20, zoom: 1.3, origen: "50% 58%" },
  { name: "Ráfaga · lanza", c: "6123", t: 11.2, d: 18 },
  { name: "Ráfaga · cinta cara (ahogarte)", c: "6128", t: 60.0, d: 27, zoom: 1.4, origen: "50% 22%" },
  { name: "Se levanta del cajón", c: "6116", t: 16.9, d: 19 },
  // ── Cierre: "Sígueme para más, perra." — viene hacia cámara a cámara lenta
  { name: "Cierre · a cámara", c: "6116", t: 18.6, d: DURACION - 936, punch: 0.18, rate: 0.75 },
];

// Transiciones en cada cambio de ejercicio (frame del corte → tipo)
type Tipo = "pan" | "zoom" | "giro";
const TRANS: [number, Tipo][] = [
  [131, "pan"],
  [272, "zoom"],
  [422, "pan"],
  [541, "giro"],
  [703, "pan"],
  [819, "zoom"],
  [936, "zoom"],
];
const FLASH = 936;

// Cada plano entra con punch-in y sigue empujando despacio: nunca está quieto.
const Shot: React.FC<{ children: React.ReactNode; punch?: number; zoom?: number; origen?: string }> = ({
  children,
  punch = 0.07,
  zoom = 1,
  origen = "50% 45%",
}) => {
  const frame = useCurrentFrame();
  const p = interpolate(frame, [0, 7], [punch, 0], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  const drift = frame * 0.0007;
  return (
    <AbsoluteFill style={{ transform: `scale(${zoom + p + drift})`, transformOrigin: origen }}>{children}</AbsoluteFill>
  );
};

// Efecto global alrededor de cada corte marcado
const efectoTransicion = (frame: number) => {
  let blur = 0;
  let scale = 0;
  let tx = 0;
  let rot = 0;
  for (const [c, tipo] of TRANS) {
    const d = frame - c + 0.5; // <0 antes del corte, >0 después
    const ad = Math.abs(d);
    const R = 5;
    if (ad >= R) continue;
    const k = 1 - ad / R; // 0→1→0
    const k2 = k * k;
    if (tipo === "zoom") {
      blur = Math.max(blur, 16 * k);
      scale = Math.max(scale, 0.16 * k);
    } else if (tipo === "pan") {
      // barrido lateral: lo de antes sale a la izquierda, lo nuevo entra desde la derecha
      blur = Math.max(blur, 18 * k);
      tx = Math.sign(-d) * -170 * k2;
      scale = Math.max(scale, 0.34 * k);
    } else {
      blur = Math.max(blur, 14 * k);
      rot = Math.sign(d) * 9 * k2;
      scale = Math.max(scale, 0.3 * k);
    }
  }
  return { blur, scale, tx, rot };
};

export const RutinaHibrida: React.FC = () => {
  const { fps, durationInFrames } = useVideoConfig();
  const frame = useCurrentFrame();
  const { blur, scale, tx, rot } = efectoTransicion(frame);

  const flash = interpolate(frame, [FLASH - 1, FLASH, FLASH + 6], [0, 0.85, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
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
          transform: `translateX(${tx}px) rotate(${rot}deg) scale(${1 + scale})`,
        }}
      >
        <Series>
          {PLANOS.map((p) => (
            <Series.Sequence key={p.name} name={p.name} durationInFrames={p.d} premountFor={fps}>
              <Shot punch={p.punch} zoom={p.zoom} origen={p.origen}>
                <Video
                  src={clip(p.c)}
                  trimBefore={Math.round(p.t * fps)}
                  playbackRate={p.rate ?? 1}
                  muted
                />
              </Shot>
            </Series.Sequence>
          ))}
        </Series>
      </AbsoluteFill>

      {/* Viñeta */}
      <AbsoluteFill
        style={{
          pointerEvents: "none",
          background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.55) 100%)",
        }}
      />
      <AbsoluteFill style={{ backgroundColor: "white", opacity: flash, pointerEvents: "none" }} />

      {/* Textos */}
      <Sequence name="Título" from={40} durationInFrames={91} layout="none">
        <Titulo titulo="rutina híbrida" sub="fuerza + cardio · 5 ejercicios" top={500} />
      </Sequence>
      <Sequence name="1 · ski erg" from={131} durationInFrames={141} layout="none">
        <Clave n={1} texto="ski erg" />
      </Sequence>
      <Sequence name="2 · zancadas" from={272} durationInFrames={150} layout="none">
        <Clave n={2} texto="zancadas con kettlebell" />
      </Sequence>
      <Sequence name="3 · granjero" from={422} durationInFrames={119} layout="none">
        <Clave n={3} texto="paseo del granjero" />
      </Sequence>
      <Sequence name="4 · wall balls" from={541} durationInFrames={162} layout="none">
        <Clave n={4} texto="wall balls" />
      </Sequence>
      <Sequence name="5 · cinta" from={703} durationInFrames={116} layout="none">
        <Clave n={5} texto="cinta" />
      </Sequence>

      <Subtitulos
        palabras={palabras as Palabra[]}
        offset={VOZ_DESDE / fps}
        claves={/^(híbrida|fuerte|morir|truco|cadera|rodilla|cobardes|granjero|carro|estrella|piernas|quema|muertas|pulmones|plan)$/i}
      />

      {/* Audio: voz + whoosh solo en los cambios de ejercicio */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={VOZ} volume={1} />
      </Sequence>
      {/* Título: brillo suave al aparecer */}
      <Sequence name="sfx título" from={38} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
      </Sequence>
      {TRANS.map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={c - 7} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RutinaHibridaComp = () => (
  <Composition
    id="RutinaHibrida"
    component={RutinaHibrida}
    durationInFrames={DURACION}
    fps={30}
    width={1080}
    height={1920}
  />
);
