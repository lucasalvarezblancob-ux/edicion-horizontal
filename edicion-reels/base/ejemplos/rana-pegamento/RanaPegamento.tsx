// "Así se aparean las ranas de lluvia (con pegamento)" — creador hablando a cámara, agachado junto a un terrario.
// Bruto: bruto terminado/2026-11-01_ranas-de-lluvia-pegamento_terrario.MOV (antes bruto/IMG_2570.MOV) → public/rana-pegamento/proxy.mp4
// ⚠️ Bruto con APUNTADOR: otra persona le dicta el guion fuera de plano. Scribe con diarización (speaker_0 = el de cámara,
// 7 dB más fuerte; speaker_1 = apuntador) → tomas buenas en tomas.json → herramientas/montar_tomas.py --hablante speaker_0.
// Ninguna palabra del apuntador entra en el montaje. voz.mp3 = las tomas ya concatenadas y a −14 LUFS (una sola pista).
// Estilo por defecto hablando a cámara (V1 + V3): gancho tipográfico detrás de la cabeza + zooms a los remates.
import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  Img,
  interpolate,
  Series,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Bloque, CamaraVirtual, Encuadre, F_REMATE, PersonaEncima, Sfx, TextoBloques } from "../../comun/hablando";
import cara from "./cara.json";
import tramos from "./tramos.json";

const SRC = staticFile("rana-pegamento/proxy.mp4");
const VOZ = staticFile("rana-pegamento/voz.mp3");
const CARAS = cara.caras as number[][];

// Tramos del bruto (frames a 30 fps) en orden de montaje — de tramos.json (montar_tomas.py)
const TRAMOS = tramos as { desde: number; dur: number; nota: string }[];
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0); // 571
const INICIOS = TRAMOS.reduce<number[]>((acc, t, i) => [...acc, i === 0 ? 0 : acc[i - 1] + TRAMOS[i - 1].dur], []);
export const bruto = (f: number) => {
  for (let i = 0; i < TRAMOS.length; i++) if (f < INICIOS[i] + TRAMOS[i].dur) return f - INICIOS[i] + TRAMOS[i].desde;
  const u = TRAMOS[TRAMOS.length - 1];
  return u.desde + u.dur - 1;
};
// Centro de cara FIJO por tramo (mediana), no por frame: el detector mete temblor.
const med = (xs: number[]) => [...xs].sort((a, b) => a - b)[Math.floor(xs.length / 2)];
const CENTRO = TRAMOS.map((t) => {
  const r = CARAS.slice(t.desde, t.desde + t.dur);
  return { cx: med(r.map((c) => c[0])), cy: med(r.map((c) => c[1])) };
});

const Base: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      {TRAMOS.map((t) => (
        <Series.Sequence key={t.desde} name={t.nota.slice(0, 40)} durationInFrames={t.dur} premountFor={fps}>
          <Video src={SRC} trimBefore={t.desde} muted />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const Grade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ filter: "contrast(1.08) saturate(0.92) brightness(0.97)" }}>{children}</AbsoluteFill>
);

// Doble flash de sección: 4 f blanco · 1 f imagen · 3 f blanco
const DobleFlash: React.FC<{ en: number }> = ({ en }) => {
  const d = useCurrentFrame() - en;
  return (d >= 0 && d < 4) || (d >= 5 && d < 8) ? <AbsoluteFill style={{ backgroundColor: "white" }} /> : null;
};

// Foto pequeña recortada (la rana de lluvia) junto a la cabeza: pop en la palabra y se va al acabar el gancho.
const Foto: React.FC<{ src: string; entra: number; sale: number; cx: number; cy: number; ancho: number; giro: number; etiqueta?: { texto: string; desde: number } }> = ({ src, entra, sale, cx, cy, ancho, giro, etiqueta }) => {
  const frame = useCurrentFrame();
  if (frame < entra - 1 || frame > sale + 6) return null;
  const e = interpolate(frame, [entra - 1, entra + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const s = interpolate(frame, [sale, sale + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const k = e * s;
  const flota = Math.sin((frame - entra) / 9) * 6;
  return (
    <div style={{ position: "absolute", left: cx, top: cy + flota, width: ancho, transform: `translate(-50%, -50%) scale(${k}) rotate(${giro + (1 - e) * -10}deg)`, opacity: Math.min(1, k * 1.6) }}>
      <Img src={staticFile(src)} style={{ width: "100%", filter: "drop-shadow(0 0 3px rgba(0,0,0,0.9)) drop-shadow(0 16px 26px rgba(0,0,0,0.7))" }} />
      {etiqueta && frame >= etiqueta.desde ? (
        <div
          style={{
            position: "absolute", left: "50%", top: "100%", whiteSpace: "nowrap", fontFamily: F_REMATE, fontStyle: "italic", fontSize: 70, color: "white",
            lineHeight: 1, textShadow: "0 4px 22px rgba(0,0,0,0.7), 0 2px 4px rgba(0,0,0,0.6)",
            transform: `translate(-50%, -12px) rotate(${-giro}deg) scale(${interpolate(frame - etiqueta.desde, [0, 3], [0.6, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) })})`,
          }}
        >
          {etiqueta.texto}
        </div>
      ) : null}
    </div>
  );
};

const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });

// ------------------------------------------------------------------ gancho (texto, no hablado): dice de qué va desde el frame 0
// El bruto empieza en "El macho es mucho más pequeño…" sin decir de qué animal habla → el título da el contexto.
const FIN_GANCHO = INICIOS[1]; // 112: acaba la primera frase
const GANCHO: Bloque[] = [
  // 2 líneas ENCIMA de la cabeza (el pelo apenas roza la de abajo). "con pegamento" va de etiqueta de la foto de la rana:
  // en una 3.ª línea la cabeza tapaba justo "pegamento".
  { desde: 2, hasta: FIN_GANCHO, y: 0.2, palabras: [P("así se aparean las", 2), P("RANAS DE LLUVIA", 12, "fuerte", true)] },
];

// ------------------------------------------------------------------ lo que dice, palabra a palabra, sobre la tierra del terrario
const Y = 0.715;
const BLOQUES: Bloque[] = [
  { desde: 3, hasta: 69, y: Y, palabras: [P("el macho es", 3), P("mucho más", 23), P("PEQUEÑO", 37, "fuerte", true), P("que la hembra", 48, "relleno", true)] },
  { desde: 69, hasta: 114, y: Y, palabras: [P("y no consigue", 69), P("abrazarla", 90, "remate", true)] },
  { desde: 114, hasta: 175, y: Y, palabras: [P("así que los dos", 114), P("sueltan una", 138, "relleno", true), P("secreción", 154, "remate")] },
  { desde: 175, hasta: 202, y: Y, palabras: [P("PEGAJOSA", 175, "fuerte")] },
  { desde: 202, hasta: 238, y: Y, palabras: [P("y se quedan", 202), P("PEGADOS", 219, "fuerte", true)] },
  { desde: 238, hasta: 286, y: Y, palabras: [P("en un estudio de", 238), P("2022", 259, "fuerte", true)] },
  { desde: 286, hasta: 333, y: Y, palabras: [P("se midió este", 286), P("PEGAMENTO", 313, "fuerte", true)] },
  { desde: 333, hasta: 404, y: Y, palabras: [P("en otra especie", 333), P("de rana del", 359, "relleno", true), P("mismo género", 377, "remate")] },
  { desde: 404, hasta: 449, y: Y, palabras: [P("es más fuerte", 404), P("entre la", 422, "relleno", true), P("PRIMERA", 435, "fuerte")] },
  { desde: 449, hasta: 481, y: Y, palabras: [P("y la", 449), P("TERCERA HORA", 455, "fuerte", true)] },
  { desde: 481, hasta: DUR, y: Y, palabras: [P("y casi", 481), P("desaparece", 499, "remate"), P("a los", 521, "relleno", true), P("3 DÍAS", 530, "fuerte")] },
];

// ------------------------------------------------------------------ cámara (trípode): entrada, empuje lento, reset seco en cada jump cut, zooms largos a los remates
const C = CENTRO;
const ENC: Encuadre[] = [
  { desde: 0, escala: 1.0, ...C[0] },
  { desde: 2, escala: 1.2, suave: 27, empuje: 0.012, ...C[0] }, // zoom de entrada 1,00→1,20 en 27 f + whoosh
  { desde: INICIOS[1], escala: 1.1, empuje: 0.03, ...C[1] }, // 112 jump cut → reset
  { desde: INICIOS[2], escala: 1.4, suave: 19, ...C[2] }, // 200 zoom largo que aterriza en "PEGADOS" (219)
  { desde: INICIOS[3], escala: 1.08, empuje: 0.03, ...C[3] }, // 236 doble flash: empieza el estudio
  { desde: 255, escala: 1.24, suave: 10, empuje: 0.01, ...C[3] }, // golpe corto en "2022"
  { desde: INICIOS[4], escala: 1.12, empuje: 0.03, ...C[4] }, // 283 jump cut
  { desde: INICIOS[5], escala: 1.15, empuje: 0.03, ...C[5] }, // 402 jump cut
  { desde: INICIOS[6], escala: 1.08, empuje: 0.02, ...C[6] }, // 479 jump cut
  { desde: 506, escala: 1.36, suave: 24, empuje: 0.006, ...C[6] }, // zoom largo que aterriza en "3 DÍAS" (530)
];

export const RanaPegamento: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Grade>
      <CamaraVirtual encuadres={ENC} shake={[{ desde: 219, hasta: 230, px: 8 }]}>
        <Base />
        {/* Gancho DETRÁS de la cabeza: techo blanco oscurecido arriba (se desvanece antes de la cara) + persona recortada encima */}
        <Sequence durationInFrames={FIN_GANCHO} layout="none" name="Gancho detrás de la cabeza">
          <AbsoluteFill style={{ background: "linear-gradient(180deg, rgba(0,0,0,0.66) 0%, rgba(0,0,0,0.5) 20%, rgba(0,0,0,0) 36%)" }} />
          <TextoBloques bloques={GANCHO} pop escala={0.78} />
          {/* Solo la franja de arriba (cabeza): el recorte mete manchas rojizas en el antebrazo y abajo no hay texto detrás */}
          <AbsoluteFill style={{ clipPath: "inset(0 0 55% 0)" }}>
            <PersonaEncima carpeta="rana-pegamento/persona" frameBruto={bruto} />
          </AbsoluteFill>
        </Sequence>
      </CamaraVirtual>
    </Grade>
    <Foto src="rana-pegamento/rana.png" entra={18} sale={FIN_GANCHO} cx={835} cy={770} ancho={280} giro={6} etiqueta={{ texto: "con pegamento", desde: 30 }} />
    <TextoBloques bloques={BLOQUES} pop escala={0.88} />
    <DobleFlash en={INICIOS[3] - 3} />
    <Audio src={VOZ} />
    {/* Sonido con moderación: entrada, título, foto, remate, cambio de sección, remate final */}
    <Sfx en={1} src="whoosh.mp3" volumen={0.45} />
    <Sfx en={0} src="impact-bass-2.mp3" volumen={0.25} />
    <Sfx en={12} src="sparkle.mp3" volumen={0.22} />
    <Sfx en={17} src="pop.mp3" volumen={0.5} />
    <Sfx en={218} src="impact-bass-1.mp3" volumen={0.5} />
    <Sfx en={INICIOS[3] - 5} src="whoosh.mp3" volumen={0.4} />
    <Sfx en={INICIOS[3] - 3} src="impact-bass-2.mp3" volumen={0.3} />
    <Sfx en={529} src="impact-bass-1.mp3" volumen={0.35} />
  </AbsoluteFill>
);

export const RanaPegamentoComp = () => (
  <Composition id="RanaPegamento" component={RanaPegamento} durationInFrames={DUR} fps={30} width={1080} height={1920} />
);

// Auxiliar (no se publica): el proxy tal cual lo decodifica Chrome, para dar a los PNG del recorte exactamente los mismos
// colores que el vídeo (el bruto es HLG/BT.2020 y OpenCV lo decodifica más cálido → se notaba la costura en la cara).
const ProxyCrudo: React.FC = () => <Video src={SRC} trimBefore={192} muted />;
export const RanaPegamentoCrudoComp = () => (
  <Composition id="RanaPegamentoCrudo" component={ProxyCrudo} durationInFrames={118} fps={30} width={1080} height={1920} />
);
