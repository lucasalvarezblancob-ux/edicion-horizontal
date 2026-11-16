// "¿Qué crees que pesa más?" — Lucas hablando a cámara (selfie al sol, sin camiseta). Estilo por defecto V1+V3.
// Bruto: bruto terminado/2026-10-31_selfie-sin-camiseta_que-pesa-mas.MP4 (antes bruto/0CDFAD5E-….MP4) → public/mancuernas-maleta/proxy.mp4
// Petición de Lucas: cuando dice "mancuernas" o "maleta", sale una foto PEQUEÑA (él sigue viéndose) con efecto de sonido.
// Fotos: recursos/fotos/ (Wikimedia Commons, ver recursos/INDICE.md). Tiempos por palabra: Scribe → cortes.json.
import { Audio, Video } from "@remotion/media";
import React from "react";
import {
  AbsoluteFill,
  Composition,
  Easing,
  Img,
  interpolate,
  Series,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { ACENTO, Bloque, CamaraVirtual, Encuadre, F_FUERTE, Sfx, TextoBloques } from "../../comun/hablando";

// proxy-estable.mp4 = proxy estabilizado contra la cara (herramientas/estabilizar.py --seguir persona --radio 30 --zoom 1.1 --desde 2.6)
const SRC = staticFile("mancuernas-maleta/proxy-estable.mp4");
const VOZ = staticFile("mancuernas-maleta/voz.mp3");

// Tramos del bruto (frames a 30 fps). Se salta la colocación del móvil y "Vale,"; se quitan 2 pausas largas.
const TRAMOS = [
  { nombre: "Pregunta + A mancuernas + B maleta + C", desde: 82, dur: 133 },
  { nombre: "El peso de saber… comodidad… persona", desde: 225, dur: 200 },
  { nombre: "Que siempre quisiste ser", desde: 431, dur: 42 },
];
const DUR = TRAMOS.reduce((a, t) => a + t.dur, 0); // 375
export const bruto = (f: number) => {
  let ini = 0;
  for (const t of TRAMOS) {
    if (f < ini + t.dur) return f - ini + t.desde;
    ini += t.dur;
  }
  const u = TRAMOS[TRAMOS.length - 1];
  return u.desde + u.dur - 1;
};

const Base: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <Series>
      {TRAMOS.map((t) => (
        <Series.Sequence key={t.desde} name={t.nombre} durationInFrames={t.dur} premountFor={fps}>
          <Video src={SRC} trimBefore={t.desde} muted />
          <Audio src={VOZ} trimBefore={t.desde} />
        </Series.Sequence>
      ))}
    </Series>
  );
};

const Grade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{ filter: "contrast(1.08) saturate(0.92) brightness(0.97)" }}>{children}</AbsoluteFill>
);

// ------------------------------------------------------------------ foto pequeña con etiqueta A/B
const Foto: React.FC<{
  src: string;
  letra: string;
  entra: number;
  sale: number;
  cx: number;
  cy: number;
  ancho: number;
  giro: number;
}> = ({ src, letra, entra, sale, cx, cy, ancho, giro }) => {
  const frame = useCurrentFrame();
  if (frame < entra - 1 || frame > sale + 6) return null;
  const e = interpolate(frame, [entra - 1, entra + 6], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const s = interpolate(frame, [sale, sale + 6], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.in(Easing.cubic) });
  const flota = Math.sin((frame - entra) / 9) * 6;
  const k = e * s;
  return (
    <div
      style={{
        position: "absolute",
        left: cx,
        top: cy + flota,
        width: ancho,
        transform: `translate(-50%, -50%) scale(${k}) rotate(${giro + (1 - e) * -10}deg)`,
        opacity: Math.min(1, k * 1.6),
      }}
    >
      <Img src={staticFile(src)} style={{ width: "100%", filter: "drop-shadow(0 0 3px rgba(0,0,0,0.9)) drop-shadow(0 16px 26px rgba(0,0,0,0.7))" }} />
      <div
        style={{
          position: "absolute", left: -22, top: -26, width: 78, height: 78, borderRadius: 39, background: ACENTO,
          display: "flex", alignItems: "center", justifyContent: "center", fontFamily: F_FUERTE, fontSize: 52, color: "#111",
          boxShadow: "0 6px 16px rgba(0,0,0,0.45)", transform: `rotate(${-giro}deg)`,
        }}
      >
        {letra}
      </div>
    </div>
  );
};

// ------------------------------------------------------------------ texto (palabra a palabra, sobre el pecho)
const P = (texto: string, desde: number, estilo: Bloque["palabras"][number]["estilo"] = "relleno", salto = false) => ({ texto, desde, estilo, salto });
const Y = 0.665;
const BLOQUES: Bloque[] = [
  { desde: 0, hasta: 34, y: Y, palabras: [P("¿qué crees que", 1), P("PESA MÁS?", 13, "fuerte", true)] },
  { desde: 34, hasta: 97, y: Y, palabras: [P("A,", 34, "remate"), P("unas mancuernas", 43), P("de", 66, "relleno", true), P("50 KILOS", 69, "fuerte")] },
  { desde: 97, hasta: 129, y: Y, palabras: [P("B,", 97, "remate"), P("una", 108), P("MALETA", 113, "fuerte", true)] },
  { desde: 129, hasta: 192, y: Y, palabras: [P("C,", 129, "remate"), P("el peso de saber", 135), P("que tenías el", 157, "relleno", true), P("POTENCIAL", 174, "fuerte", true)] },
  { desde: 192, hasta: 239, y: Y, palabras: [P("y el", 192), P("tiempo,", 198, "remate"), P("pero seguiste", 212, "relleno", true), P("eligiendo", 227, "relleno", true)] },
  { desde: 239, hasta: 289, y: Y, palabras: [P("la", 239), P("COMODIDAD", 242, "fuerte", true), P("en vez de tomar", 260, "relleno", true), P("acción", 276, "remate")] },
  { desde: 289, hasta: 335, y: Y, palabras: [P("y convertirte", 289), P("en la", 312, "relleno", true), P("persona", 320, "remate")] },
  { desde: 335, hasta: DUR, y: Y, palabras: [P("que siempre", 335), P("QUISISTE", 352, "fuerte", true), P("SER", 365, "fuerte")] },
];

// ------------------------------------------------------------------ cámara: entrada, empuje lento, reset en cortes, zoom largo al remate
const C1 = { cx: 556, cy: 889 }, C2 = { cx: 603, cy: 831 }, C3 = { cx: 596, cy: 793 };
const ENC: Encuadre[] = [
  // Centro FIJO por tramo (mediana de la cara en el proxy estabilizado), no por frame: seguir la cara
  // fotograma a fotograma metía temblor. Zooms más suaves (cualquier zoom amplía el pulso de la mano).
  { desde: 0, escala: 1.0, ...C1 },
  { desde: 2, escala: 1.14, suave: 27, empuje: 0.008, ...C1 }, // zoom de entrada 1,00→1,14 en 27 f
  { desde: 34, escala: 1.03, suave: 0, empuje: 0.012, ...C1 }, // se abre para dejar sitio a las fotos (A/B)
  { desde: 129, escala: 1.16, suave: 0, empuje: 0.015, ...C1 }, // C: el giro → más cerca, seco
  { desde: 133, escala: 1.12, suave: 0, empuje: 0.02, ...C2 }, // jump cut tapado con cambio de encuadre
  { desde: 218, escala: 1.34, suave: 24, ...C2 }, // zoom largo que aterriza en "COMODIDAD" (242)
  { desde: 260, escala: 1.1, suave: 0, empuje: 0.02, ...C2 },
  { desde: 333, escala: 1.2, suave: 0, empuje: 0.015, ...C3 }, // jump cut
  { desde: 350, escala: 1.3, suave: 10, ...C3 }, // "QUISISTE SER"
];

export const MancuernasMaleta: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    <Grade>
      <CamaraVirtual encuadres={ENC}>
        <Base />
      </CamaraVirtual>
    </Grade>
    {/* Fotos pequeñas por encima de los hombros, a los lados de la cabeza: A izquierda, B derecha */}
    <Foto src="mancuernas-maleta/mancuernas.png" letra="A" entra={52} sale={129} cx={235} cy={480} ancho={390} giro={-6} />
    <Foto src="mancuernas-maleta/maleta.png" letra="B" entra={113} sale={129} cx={880} cy={470} ancho={185} giro={5} />
    <TextoBloques bloques={BLOQUES} pop escala={0.82} />
    {/* Sonido: entrada + un pop por foto + golpe en el remate. Nada más. */}
    <Sfx en={1} src="whoosh-short.mp3" volumen={0.45} />
    <Sfx en={0} src="impact-bass-2.mp3" volumen={0.25} />
    <Sfx en={51} src="pop.mp3" volumen={0.55} />
    <Sfx en={112} src="pop.mp3" volumen={0.55} />
    <Sfx en={241} src="impact-bass-1.mp3" volumen={0.5} />
  </AbsoluteFill>
);

export const MancuernasMaletaComp = () => (
  <Composition id="MancuernasMaleta" component={MancuernasMaleta} durationInFrames={DUR} fps={30} width={1080} height={1920} />
);
