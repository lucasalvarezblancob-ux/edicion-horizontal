// la-repeticion — calco del reel de adrianavmarquez (https://www.instagram.com/p/De4zm6Gh-4x/) con clips de Lucas.
// Audio hablado ("la repetición, la repetición… aprendió de sus errores") sobre 41 planos cortados en los MISMOS
// fotogramas que la referencia, mismos textos (palabra/sílaba, mismo fotograma de entrada y salida, color y posición)
// y mismo look de color por plano (pedido expreso de Lucas: "mismos filtros de colores por clip").
//
// Planos: seleccion.json (clip de recursos/ + instante de entrada de cada plano).
//   planos_base.sh N   → public/la-repeticion/base/NN.mp4 (SDR bt709 2160×3840 30 fps, HDR vía avconvert + hdr-pantalla.cube)
//   igualar_color.py   → public/la-repeticion/luts/NN.cube + planos/NN.mp4 (balance de blancos + brillo/contraste +
//                         saturación medidos contra el plano equivalente de la referencia)
// Audio: public/la-repeticion/audio.m4a (el de la referencia, tal cual). Al publicar en IG mejor usar el audio original del reel.
// Textos medidos en la referencia (1080×1920): altura de mayúscula ~60 px, centro de mayúscula y=345 arriba / 1405 abajo.
import { Audio, Video } from "@remotion/media";
import { loadFont } from "@remotion/google-fonts/Poppins";
import React, { useEffect, useState } from "react";
import { AbsoluteFill, Composition, continueRender, delayRender, Sequence, staticFile } from "remotion";

const { fontFamily, waitUntilDone } = loadFont("normal", { weights: ["700"], subsets: ["latin", "latin-ext"] });

const S = "la-repeticion";
const FPS = 30;
const DURACION = 573; // 19,1 s, igual que la referencia (acaba en "erro-" como el original: Lucas no quiere cola ni eco)

// Fotogramas de corte de la referencia (inicio de cada plano + final).
const CORTES = [
  0, 17, 41, 45, 49, 53, 57, 82, 95, 99, 103, 109, 114, 118, 123, 127, 160, 165, 189, 208, 217, 236, 246, 264, 283, 293,
  312, 340, 359, 369, 387, 416, 435, 444, 463, 491, 511, 520, 539, 549, 567, 573,
];

const AMARILLO = "#F7B434";
const AZUL = "#3642C1";
const BLANCO = "#EFE5F9";
type Color = typeof AMARILLO | typeof AZUL | typeof BLANCO;

// Centro de la mayúscula en px de 1080×1920.
const ARRIBA = { x: 540, y: 345 };
const ABAJO = { x: 540, y: 1405 };
const LA = [ { x: 240, y: 412 }, { x: 795, y: 485 }, { x: 543, y: 384 }, { x: 240, y: 705 } ];
const TI = [ { x: 537, y: 381 }, { x: 255, y: 573 }, { x: 831, y: 573 } ];

type Texto = { t: string; de: number; a: number; c: Color; p: { x: number; y: number } };
const Y = AMARILLO, B = AZUL, W = BLANCO;

// [texto, desde (incl.), hasta (excl.), color, posición] — fotograma a fotograma de la referencia.
const TEXTOS: Texto[] = [
  { t: "RE", de: 0, a: 3, c: Y, p: ARRIBA },
  { t: "PE", de: 3, a: 6, c: Y, p: ARRIBA },
  { t: "TI", de: 6, a: 10, c: Y, p: ARRIBA },
  { t: "CIÓN", de: 10, a: 18, c: Y, p: ARRIBA },
  { t: "REPETICIÓN", de: 18, a: 36, c: Y, p: ABAJO },
  { t: "LA", de: 41, a: 56, c: Y, p: LA[0] },
  { t: "LA", de: 44, a: 56, c: Y, p: LA[1] },
  { t: "LA", de: 47, a: 56, c: Y, p: LA[2] },
  { t: "LA", de: 49, a: 56, c: Y, p: LA[3] },
  { t: "RE", de: 56, a: 61, c: W, p: ABAJO },
  { t: "PE", de: 61, a: 65, c: W, p: ABAJO },
  { t: "TI", de: 65, a: 69, c: W, p: ABAJO },
  { t: "CIÓN", de: 69, a: 80, c: W, p: ABAJO },
  { t: "LA", de: 80, a: 84, c: B, p: ARRIBA },
  { t: "REPETIT", de: 84, a: 95, c: B, p: ARRIBA },
  { t: "TI", de: 95, a: 109, c: Y, p: TI[0] },
  { t: "TI", de: 99, a: 109, c: Y, p: TI[1] },
  { t: "TI", de: 103, a: 109, c: Y, p: TI[2] },
  { t: "LA", de: 131, a: 134, c: Y, p: ARRIBA },
  { t: "REPETICIÓN", de: 134, a: 151, c: Y, p: ABAJO },
  { t: "DE", de: 151, a: 154, c: Y, p: ARRIBA },
  { t: "UNA", de: 154, a: 159, c: Y, p: ARRIBA },
  { t: "ACCIÓN", de: 159, a: 170, c: Y, p: ARRIBA },
  { t: "ES", de: 170, a: 174, c: Y, p: ARRIBA },
  { t: "LA", de: 174, a: 179, c: Y, p: ARRIBA },
  { t: "TÉCNICA", de: 179, a: 197, c: Y, p: ARRIBA },
  { t: "MÁS", de: 197, a: 208, c: Y, p: ARRIBA },
  { t: "EFECTIVA", de: 208, a: 229, c: B, p: ARRIBA },
  { t: "PARA", de: 240, a: 245, c: Y, p: ARRIBA },
  { t: "LA", de: 245, a: 248, c: Y, p: ARRIBA },
  { t: "PROLONGACIÓN", de: 248, a: 264, c: B, p: ARRIBA },
  { t: "POR ESO", de: 281, a: 290, c: Y, p: ARRIBA },
  { t: "SE REPITE", de: 290, a: 302, c: Y, p: ARRIBA },
  { t: "AUNQUE", de: 302, a: 311, c: Y, p: ARRIBA },
  { t: "SE", de: 311, a: 314, c: Y, p: ABAJO },
  { t: "ESTÉ", de: 314, a: 322, c: Y, p: ABAJO },
  { t: "ABURRIENDO", de: 322, a: 340, c: W, p: ABAJO },
  { t: "YA LLEVA", de: 352, a: 363, c: Y, p: ARRIBA },
  { t: "9500", de: 363, a: 389, c: W, p: ARRIBA },
  { t: "AÑOS", de: 389, a: 404, c: Y, p: ARRIBA },
  { t: "VIVIENDO", de: 404, a: 431, c: Y, p: ARRIBA },
  { t: "Y ES QUE", de: 431, a: 445, c: Y, p: ABAJO },
  { t: "YA NO PASA", de: 445, a: 463, c: Y, p: ARRIBA },
  { t: "POR PROBLEMAS", de: 463, a: 491, c: B, p: ARRIBA },
  { t: "MAYORES", de: 491, a: 500, c: Y, p: ARRIBA },
  { t: "DE TANTO", de: 500, a: 516, c: Y, p: ARRIBA },
  { t: "REPETIRSE", de: 516, a: 539, c: Y, p: ARRIBA },
  { t: "APRENDIÓ", de: 539, a: 553, c: Y, p: ARRIBA },
  { t: "DE SUS", de: 553, a: 557, c: Y, p: ARRIBA },
  { t: "ERRORES!", de: 557, a: 573, c: W, p: ARRIBA },
];

// Poppins Bold en mayúsculas. La referencia aprieta o abre el tracking en cada texto para que quepa a un ancho
// concreto ("POR PROBLEMAS" va mucho más junto que "REPETICIÓN"): ANCHO = ancho de tinta medido en la referencia
// (fotograma central de cada texto) y el tracking se calcula en el navegador para clavarlo.
const TAM = 86;
const PESO = 700;
const TRACKING_DEF = -0.03; // em, para los "LA"/"TI" repartidos
const SOMBRA_CLARO = "0 0 26px rgba(0,0,0,0.55), 0 2px 8px rgba(0,0,0,0.4)";
const HALO_AZUL = "0 0 22px rgba(255,236,214,0.9), 0 0 44px rgba(255,236,214,0.6), 0 0 6px rgba(255,236,214,0.7)";
// Centro de la mayúscula respecto a la caja de línea (line-height 1).
const AJUSTE_Y = -0.027; // em
const ANCHO: Record<string, number> = {
  "RE|0": 90, "PE|3": 88, "TI|6": 65, "CIÓN|10": 203, "REPETICIÓN|18": 454, "RE|56": 90, "PE|61": 86, "TI|65": 65,
  "CIÓN|69": 201, "LA|80": 92, "REPETIT|84": 282, "LA|131": 92, "REPETICIÓN|134": 454, "DE|151": 93, "UNA|154": 166,
  "ACCIÓN|159": 308, "ES|170": 82, "LA|174": 88, "TÉCNICA|179": 334, "MÁS|197": 171, "EFECTIVA|208": 351, "PARA|240": 206,
  "LA|245": 91, "PROLONGACIÓN|248": 618, "POR ESO|281": 314, "SE REPITE|290": 336, "AUNQUE|302": 321, "SE|311": 84,
  "ESTÉ|314": 166, "ABURRIENDO|322": 487, "YA LLEVA|352": 338, "9500|363": 192, "AÑOS|389": 218, "VIVIENDO|404": 364,
  "Y ES QUE|431": 315, "YA NO PASA|445": 455, "POR PROBLEMAS|463": 622, "MAYORES|491": 373, "DE TANTO|500": 369,
  "REPETIRSE|516": 371, "APRENDIÓ|539": 384, "DE SUS|553": 250, "ERRORES!|557": 354,
};

// Ancho de tinta y desplazamiento del centro de la tinta respecto al centro de la caja de avance (sin tracking).
const tinta = (t: string) => {
  const ctx = document.createElement("canvas").getContext("2d")!;
  ctx.font = `${PESO} ${TAM}px ${fontFamily}`;
  const m = ctx.measureText(t);
  return { w: m.actualBoundingBoxLeft + m.actualBoundingBoxRight, centro: (m.actualBoundingBoxRight - m.actualBoundingBoxLeft) / 2 - m.width / 2 };
};

const Rotulo: React.FC<{ t: string; c: Color; p: { x: number; y: number }; w?: number }> = ({ t, c, p, w }) => {
  const [listo, setListo] = useState(false);
  const [handle] = useState(() => delayRender(`fuente ${t}`));
  useEffect(() => {
    waitUntilDone()
      .then(() => document.fonts.ready)
      .then(() => {
        setListo(true);
        continueRender(handle);
      });
  }, [handle]);
  if (!listo) return null;
  const n = [...t].length;
  const base = tinta(t);
  // CSS letter-spacing se añade tras cada carácter (también el último): la tinta crece (n-1)·ls y la caja n·ls,
  // así que la tinta queda ls/2 a la izquierda del centro de la caja.
  const ls = w && n > 1 ? (w - base.w) / (n - 1) : TRACKING_DEF * TAM;
  const dx = -base.centro + ls / 2;
  return (
    <div
      style={{
        position: "absolute",
        left: p.x,
        top: p.y,
        transform: `translate(-50%, -50%) translate(${dx}px, ${AJUSTE_Y * TAM}px)`,
        fontFamily,
        fontWeight: PESO,
        fontSize: TAM,
        lineHeight: 1,
        letterSpacing: ls,
        color: c,
        // 2026-11-03 — Lucas: "revisa que los textos se puedan leer bien". Sombra oscura difusa en amarillo/blanco
        // (apenas se nota en fondo oscuro) y halo claro cálido en el azul, que en los planos oscuros del gym no se leía.
        textShadow: c === AZUL ? HALO_AZUL : SOMBRA_CLARO,
        whiteSpace: "nowrap",
      }}
    >
      {t}
    </div>
  );
};

export const LaRepeticion: React.FC = () => (
  <AbsoluteFill style={{ backgroundColor: "black" }}>
    {CORTES.slice(0, -1).map((de, i) => (
      <Sequence key={i} name={`plano ${i + 1}`} from={de} durationInFrames={CORTES[i + 1] - de} premountFor={30}>
        <Video src={staticFile(`${S}/planos/${String(i + 1).padStart(2, "0")}.mp4`)} muted style={{ width: "100%", height: "100%" }} />
      </Sequence>
    ))}
    {TEXTOS.map((x, i) => (
      <Sequence key={`t${i}`} name={x.t} from={x.de} durationInFrames={x.a - x.de} layout="none">
        <Rotulo t={x.t} c={x.c} p={x.p} w={ANCHO[`${x.t}|${x.de}`]} />
      </Sequence>
    ))}
    <Audio src={staticFile(`${S}/audio.m4a`)} />
  </AbsoluteFill>
);

export const LaRepeticionComp: React.FC = () => (
  <Composition id="LaRepeticion" component={LaRepeticion} durationInFrames={DURACION} fps={FPS} width={1080} height={1920} />
);
