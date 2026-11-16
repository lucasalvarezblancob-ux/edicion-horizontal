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

// Versión Hyrox de rutina-hibrida: mismos clips (proxies en public/rutina-hibrida/c<IMG>.mp4, brutos en
// recursos/gym/{fisico,cardio,piernas,funcional}/2026-11-01_hibrido_…), en el orden oficial de Hyrox con 1 km de carrera antes de cada estación:
// correr → SkiErg → correr → granjero → correr → zancadas → correr → wall balls.
const clip = (id: string) => staticFile(`rutina-hibrida/c${id}.mp4`);
const VOZ = staticFile("rutina-hyrox/voz.mp3"); // Alberto Rodríguez ×1,25 sin silencios
const VOZ_DESDE = 3;
const DURACION = 960;

type Plano = {
  name: string;
  c: string;
  t: number;
  d: number;
  zoom?: number;
  origen?: string;
  punch?: number;
  rate?: number;
};

const PLANOS: Plano[] = [
  // ── Gancho: "¿Qué pasa, perra? ¿Te estás preparando un Hyrox? Pues apúntate esta rutina."
  { name: "Intro · sentado", c: "6116", t: 4.05, d: 31, punch: 0.15 },
  { name: "Intro · sentado (jump cut)", c: "6116", t: 8.8, d: 40, zoom: 1.25, origen: "50% 50%", punch: 0.1 },
  { name: "Gancho · lanza", c: "6123", t: 4.1, d: 16 },
  { name: "Gancho · ski", c: "6370", t: 5.0, d: 19, zoom: 1.2 },
  // "Como en la competición, entre prueba y prueba toca correr."
  { name: "Gancho · granjero", c: "6120", t: 22.6, d: 28, zoom: 1.1 },
  { name: "Gancho · zancadas", c: "6369", t: 42.0, d: 24, zoom: 1.3, origen: "50% 58%" },
  { name: "Gancho · piernas corriendo", c: "6128", t: 21.0, d: 21, zoom: 1.6, origen: "50% 82%" },
  // ── KM 1 + SkiErg
  { name: "Km 1 · cinta abierto", c: "6128", t: 20.0, d: 30 },
  { name: "Ski · abierto", c: "6370", t: 4.8, d: 29 },
  { name: "Ski · cadera", c: "6370", t: 5.77, d: 18, zoom: 1.5, origen: "58% 55%" },
  { name: "Ski · brazos", c: "6370", t: 6.37, d: 26, zoom: 1.45, origen: "58% 30%" },
  // ── KM 2 + Paseo del granjero
  { name: "Km 2 · cinta cara", c: "6128", t: 40.0, d: 19, zoom: 1.4, origen: "50% 22%" },
  { name: "Granjero · de frente", c: "6120", t: 22.57, d: 32, zoom: 1.1 },
  { name: "Granjero · mancuernas (espalda)", c: "6120", t: 1.37, d: 30 },
  { name: "Granjero · pasos cortos", c: "6120", t: 24.3, d: 27, zoom: 1.35, origen: "50% 70%" },
  { name: "Granjero · se aleja", c: "6120", t: 9.0, d: 35, zoom: 1.15, origen: "50% 55%" },
  { name: "Granjero · llega (sin carro)", c: "6120", t: 26.5, d: 17 },
  // ── KM 3 + Zancadas
  { name: "Km 3 · cinta piernas", c: "6128", t: 50.0, d: 28, zoom: 1.5, origen: "50% 80%" },
  { name: "Zancadas · de espaldas", c: "6369", t: 4.83, d: 31, zoom: 1.05 },
  { name: "Zancadas · rodilla al suelo", c: "6369", t: 39.77, d: 47, zoom: 1.5, origen: "60% 62%" },
  { name: "Zancadas · con un amigo", c: "6369", t: 41.33, d: 20, zoom: 1.1 },
  { name: "Zancadas · llegan a cámara", c: "6369", t: 42.0, d: 41, zoom: 1.3, origen: "50% 58%" },
  // ── KM 4 + Wall balls (lateral = sentadilla, contrapicado = lanzamiento)
  { name: "Km 4 · cinta cara cansado", c: "6128", t: 65.0, d: 26, zoom: 1.35, origen: "50% 22%" },
  { name: "WB contrapicado · lanza (paso estrella)", c: "6123", t: 3.95, d: 25 },
  { name: "WB lateral · arriba", c: "6125", t: 13.4, d: 23 },
  { name: "WB lateral · bajas en sentadilla", c: "6125", t: 15.83, d: 34 },
  { name: "WB contrapicado · sube con las piernas", c: "6123", t: 7.6, d: 27 },
  { name: "WB lateral · recoge→sentadilla", c: "6125", t: 17.82, d: 24 },
  { name: "WB · cara (uf, cómo quema)", c: "6123", t: 36.3, d: 30 },
  // ── Repaso en el orden de Hyrox: "Mismo orden que en la competición, así que el día de la carrera nada te pilla por sorpresa."
  { name: "Repaso · corre", c: "6128", t: 30.0, d: 13 },
  { name: "Repaso · ski", c: "6370", t: 10.0, d: 13, zoom: 1.2 },
  { name: "Repaso · corre 2", c: "6128", t: 55.0, d: 13, zoom: 1.4, origen: "50% 22%" },
  { name: "Repaso · granjero", c: "6120", t: 25.0, d: 13, zoom: 1.2 },
  { name: "Repaso · corre 3", c: "6128", t: 45.0, d: 13, zoom: 1.5, origen: "50% 80%" },
  { name: "Repaso · zancadas", c: "6369", t: 43.0, d: 13, zoom: 1.2 },
  { name: "Repaso · corre 4", c: "6128", t: 35.0, d: 12 },
  { name: "Repaso · wall ball", c: "6125", t: 18.95, d: 13 },
  // ── Cierre: "Sígueme para más, perra." — viene hacia cámara a cámara lenta
  { name: "Cierre · a cámara", c: "6116", t: 18.6, d: DURACION - 901, punch: 0.18, rate: 0.75 },
];

// Transiciones: cada cambio de bloque (con whoosh) y la entrada a cada estación (solo visual)
type Tipo = "pan" | "zoom" | "giro";
const TRANS: [number, Tipo, boolean][] = [
  [179, "pan", true],
  [209, "zoom", false],
  [282, "giro", true],
  [301, "zoom", false],
  [442, "pan", true],
  [470, "zoom", false],
  [609, "giro", true],
  [635, "zoom", false],
  [798, "pan", true],
  [901, "zoom", true],
];
const FLASH = 901;

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

export const RutinaHyrox: React.FC = () => {
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
      <Sequence name="Título" from={40} durationInFrames={66} layout="none">
        <Titulo titulo="rutina hyrox" sub="1 km corriendo antes de cada estación" top={500} />
      </Sequence>
      {[
        [179, 30, "km", "corre 1 km"],
        [209, 73, 1, "ski erg"],
        [282, 19, "km", "corre 1 km"],
        [301, 141, 2, "paseo del granjero"],
        [442, 28, "km", "corre 1 km"],
        [470, 139, 3, "zancadas con kettlebell"],
        [609, 26, "km", "corre 1 km"],
        [635, 163, 4, "wall balls"],
      ].map(([from, d, n, texto]) => (
        <Sequence key={String(from)} name={`${n} · ${texto}`} from={from as number} durationInFrames={d as number} layout="none">
          <Clave n={n as number | string} texto={texto as string} />
        </Sequence>
      ))}

      <Subtitulos
        palabras={palabras as Palabra[]}
        offset={VOZ_DESDE / fps}
        claves={/^(hyrox|rutina|correr|kilómetro|cadera|brazos|granjero|carro|rodilla|cobardes|estrella|piernas|quema|orden|sorpresa)$/i}
      />

      {/* Audio: voz + whoosh solo en los cambios de ejercicio */}
      <Sequence name="Voz" from={VOZ_DESDE} layout="none">
        <Audio src={VOZ} volume={1} />
      </Sequence>
      {/* Título: brillo suave al aparecer */}
      <Sequence name="sfx título" from={38} durationInFrames={55} layout="none">
        <Audio src={staticFile("sonidos/sparkle.mp3")} volume={0.22} />
      </Sequence>
      {TRANS.filter(([, , sfx]) => sfx).map(([c]) => (
        <Sequence key={c} name={`whoosh ${c}`} from={c - 7} durationInFrames={20} layout="none">
          <Audio src={staticFile("sonidos/whoosh.mp3")} volume={0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

export const RutinaHyroxComp = () => (
  <Composition
    id="RutinaHyrox"
    component={RutinaHyrox}
    durationInFrames={DURACION}
    fps={30}
    width={1080}
    height={1920}
  />
);
