// "Reto 50 ml exactos a ojo" — vlog/reto con 3 personas en Honest Greens (Madrid), cámara en mano.
// Bruto: bruto terminado/2026-10-31_reto-50ml-vasos_3-chicos_honest-greens.MOV (2:25; empieza de verdad en el s ~20). Mucho ruido de fondo → audio = voces aisladas
// (ElevenLabs) + algo de original SOLO mientras hablan (herramientas/mezclar_voces.py); silencio entre frases.
// Montaje: tomas.json → herramientas/montar_tomas.py --hablante todos → montaje.json (acciones aceleradas y mudas).
import React from "react";
import { AbsoluteFill, Composition, Easing, interpolate, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { Audio, Video } from "@remotion/media";
import { ACENTO, Bloque, F_FUERTE, F_RELLENO, Sfx, TextoBloques } from "../../comun/hablando";
import { Subtitulos } from "../../comun/Subtitulos";
import montaje from "./montaje.json";

const RATE = 1.1; // todo un pelín más rápido (sin huecos)
const SRC = staticFile("tres-personas/proxy.mp4");
const VOZ = staticFile("tres-personas/voz-x1.1.mp3");

type T = { desde: number; hasta: number; vel?: number; nota: string };
const TRAMOS = (() => {
  let acc = 0;
  return (montaje.tramos as T[]).map((t) => {
    const vel = t.vel ?? 1;
    const dur = Math.round((((t.hasta - t.desde) / vel) * 30) / RATE);
    const r = { ...t, vel, ini: acc, dur };
    acc += dur;
    return r;
  });
})();
const DUR = TRAMOS[TRAMOS.length - 1].ini + TRAMOS[TRAMOS.length - 1].dur + 10;

// segundo del bruto → frame del edit
const enEdit = (raw: number) => {
  const t = TRAMOS.find((x) => raw >= x.desde && raw < x.hasta) ?? TRAMOS[TRAMOS.length - 1];
  return Math.round(t.ini + (((raw - t.desde) / t.vel) * 30) / RATE);
};

// subtítulos: tiempos del montaje (s a ×1) → s del edit; nombre del sitio corregido
const PALABRAS = montaje.palabras.map((p) => ({
  w: p.w.replace(/^Owles$/, "Honest").replace(/^Grinch$/, "Greens"),
  start: p.start / RATE,
  end: p.end / RATE,
}));
const CLAVES = /^(cincuenta|sesenta|tres|doble|exactos|máquina|reto|pesos|macros|pasado|chupito)$/i;

// ---- lecturas de la báscula (leídas en el bruto ampliando la pantalla de la báscula)
type Lectura = { raw: number; hasta?: number; ml: number; extra?: string; cx: number; cy: number; ok?: boolean };
const LECTURAS: Lectura[] = [
  { raw: 85.9, ml: 63, cx: 700, cy: 900 },
  { raw: 93.4, ml: 60, cx: 689, cy: 1081 },
  { raw: 94.9, ml: 99, extra: "EL DOBLE", cx: 702, cy: 1000 },
  { raw: 104.6, ml: 46, extra: "se pasa bebiendo", cx: 702, cy: 1203 },
  { raw: 120.8, ml: 33, extra: "un chupito", cx: 648, cy: 1188 },
  { raw: 135.6, ml: 50, extra: "EXACTO", cx: 657, cy: 1210, ok: true },
];
const EV = LECTURAS.map((l, i) => {
  const desde = enEdit(l.raw);
  const sig = i < LECTURAS.length - 1 ? enEdit(LECTURAS[i + 1].raw) : Infinity;
  return { ...l, desde, hasta: Math.min(sig, desde + 50) };
});

// ---- cámara: zoom de entrada + acercamiento a la báscula en cada lectura
const camara = (f: number) => {
  if (f < 24) return { s: interpolate(f, [0, 20], [1, 1.15], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }), ox: 540, oy: 650 };
  const e = EV.find((x) => f >= x.desde - 2 && f < x.hasta);
  if (e) return { s: interpolate(f, [e.desde - 2, e.desde + 10], [1, 1.35], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) }), ox: e.cx, oy: e.cy };
  if (f < 100) return { s: 1.15, ox: 540, oy: 650 }; // sigue cerrado durante el gancho
  return { s: 1, ox: 540, oy: 960 };
};

const Planos: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <>
      {TRAMOS.map((t, i) => (
        <Sequence key={i} name={`${i} ${t.vel > 1 ? `×${t.vel} ` : ""}${t.nota}`} from={t.ini} durationInFrames={t.dur} premountFor={fps}>
          <Video src={SRC} trimBefore={Math.round(t.desde * 30)} playbackRate={RATE * t.vel} muted premountFor={fps} />
        </Sequence>
      ))}
    </>
  );
};

// voz limpia: solo los tramos hablados (los acelerados van mudos)
const Voz: React.FC = () => (
  <>
    {TRAMOS.filter((t) => t.vel === 1).map((t, i) => (
      <Sequence key={i} name={`Voz ${t.nota}`} from={t.ini} durationInFrames={t.dur} layout="none">
        <Audio src={VOZ} trimBefore={Math.round((t.desde * 30) / RATE)} />
      </Sequence>
    ))}
  </>
);

const Camara: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const f = useCurrentFrame();
  const c = camara(f);
  return (
    <AbsoluteFill style={{ transform: `scale(${c.s})`, transformOrigin: `${c.ox}px ${c.oy}px` }}>{children}</AbsoluteFill>
  );
};

// cifra grande arriba cuando la báscula marca
const Cifras: React.FC = () => {
  const f = useCurrentFrame();
  const e = EV.find((x) => f >= x.desde && f < x.hasta);
  if (!e) return null;
  const d = f - e.desde;
  const k = interpolate(d, [0, 5], [0.7, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const ox = interpolate(d, [0, 2], [0, 1], { extrapolateRight: "clamp" });
  const kExtra = interpolate(d, [7, 11], [0.7, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 250 }}>
      <div style={{ opacity: ox, transform: `scale(${k})`, textAlign: "center" }}>
        <div style={{ fontFamily: F_FUERTE, fontSize: 260, lineHeight: 0.9, color: e.ok ? ACENTO : "white", textShadow: "0 6px 30px rgba(0,0,0,0.6)" }}>
          {e.ml}
          <span style={{ fontSize: 110, marginLeft: 12 }}>ml</span>
        </div>
        {e.extra && (
          <div style={{ marginTop: 10, transform: `scale(${kExtra})`, opacity: d >= 7 ? 1 : 0, fontFamily: e.ok || e.extra === "EL DOBLE" ? F_FUERTE : F_RELLENO, fontWeight: 800, fontSize: e.ok || e.extra === "EL DOBLE" ? 120 : 64, color: e.ok || e.extra === "EL DOBLE" ? ACENTO : "white", letterSpacing: e.ok ? 2 : -1, textShadow: "0 4px 22px rgba(0,0,0,0.7)" }}>
            {e.extra}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

// gancho: palabra a palabra, 3 formatos
const BLOQUES: Bloque[] = [
  {
    desde: 2,
    hasta: 100,
    y: 0.19,
    palabras: [
      { texto: "llenar un vaso a", desde: 2, estilo: "relleno" },
      { texto: "50 ML EXACTOS", desde: 16, estilo: "fuerte", salto: true },
      { texto: "a ojo", desde: 34, estilo: "remate", salto: true },
    ],
  },
];

// ---- relleno sonoro de las acciones mudas (Lucas: los huecos sin audio hay que rellenarlos)
// Efectos generados con ElevenLabs (scripts/sfx.mjs), guardados en recursos/sonidos/.
const tramo = (nota: string) => TRAMOS.find((t) => t.nota.startsWith(nota))!;
const SfxTramo: React.FC<{ desde: number; dur: number; src: string; vol: number; offset?: number; fundido?: number }> = ({ desde, dur, src, vol, offset = 0, fundido = 6 }) => (
  <Sequence from={desde} durationInFrames={dur} layout="none" name={`SFX ${src}`}>
    <Audio
      src={staticFile(`sonidos/${src}`)}
      trimBefore={offset}
      volume={(f) => vol * interpolate(f, [0, 3, dur - fundido, dur], [0, 1, 1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" })}
    />
  </Sequence>
);
const Relleno: React.FC = () => {
  const llenar = ["ACCIÓN: llena el 1.º", "ACCIÓN: llena el 2.º", "ACCIÓN: llena el 3.º"].map(tramo);
  const bebeAzul = tramo("ACCIÓN: bebe el de azul");
  const bebeTirantes = tramo("ACCIÓN: bebe el de tirantes");
  const celebra = tramo("ACCIÓN: celebra");
  return (
    <>
      {/* agua del grifo al vaso en cada llenado (offset distinto para que no suene idéntico) */}
      {llenar.map((t, i) => (
        <SfxTramo key={i} desde={t.ini} dur={t.dur} src="agua-grifo-vaso-2.mp3" vol={0.5} offset={i * 8} />
      ))}
      {/* tragos tipo poción de escudo */}
      <SfxTramo desde={bebeAzul.ini} dur={bebeAzul.dur} src="beber-pocion-2.mp3" vol={0.7} />
      <SfxTramo desde={bebeTirantes.ini} dur={bebeTirantes.dur} src="beber-pocion-1.mp3" vol={0.7} />
      {/* el de blanco bebe a sorbos (debajo de la voz, más bajo) */}
      <SfxTramo desde={enEdit(127.0)} dur={30} src="beber-pocion-2.mp3" vol={0.3} offset={20} />
      <SfxTramo desde={enEdit(131.0)} dur={28} src="beber-pocion-1.mp3" vol={0.3} offset={30} />
      {/* pitido de báscula en cada lectura; redoble antes del 50 */}
      {EV.map((e, i) => (
        <SfxTramo key={i} desde={e.desde} dur={15} src="bascula-pitido.mp3" vol={0.35} fundido={2} />
      ))}
      <SfxTramo desde={EV[5].desde - 40} dur={40} src="redoble-corto.mp3" vol={0.4} offset={5} fundido={2} />
      {/* victoria */}
      <SfxTramo desde={celebra.ini - 4} dur={60} src="victoria-jingle.mp3" vol={0.45} fundido={12} />
    </>
  );
};

const Reto50ml: React.FC = () => {
  const f = useCurrentFrame();
  const oscuro = interpolate(f, [90, 104], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      <Camara>
        <AbsoluteFill style={{ filter: "contrast(1.06) saturate(0.95)" }}>
          <Planos />
        </AbsoluteFill>
      </Camara>
      {/* oscurecer arriba solo durante el gancho */}
      <AbsoluteFill style={{ opacity: oscuro, background: "linear-gradient(180deg, rgba(0,0,0,0.6) 0%, rgba(0,0,0,0.35) 24%, rgba(0,0,0,0) 40%)" }} />
      <TextoBloques bloques={BLOQUES} pop escala={1.05} />
      <Cifras />
      <Subtitulos palabras={PALABRAS} offset={0} claves={CLAVES} top={1360} maxHueco={0.5} />
      <Voz />
      {/* sonido: entrada, el doble y el relleno de las acciones */}
      <Sfx en={0} src="whoosh.mp3" volumen={0.45} />
      <Sfx en={EV[2].desde + 7} src="impact-bass-1.mp3" volumen={0.3} />
      <Relleno />
    </AbsoluteFill>
  );
};

export const Reto50mlComp: React.FC = () => (
  <Composition id="Reto50ml" component={Reto50ml} durationInFrames={DUR} fps={30} width={1080} height={1920} />
);
