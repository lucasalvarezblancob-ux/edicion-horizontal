// bici-nueva-trek — Lucas recoge su bici nueva (Trek Domane, Project One) en Trek Barcelona Centre. Colaboración con Trek.
// Tipo: vlog hablado (voz real de Lucas y de Álvaro, micros de corbata) + b-roll de la bici y la tienda mientras hablan (lo pidió Lucas:
//   "ir intercambiando con él hablando en plano y a veces rollo voice en off", "lo más dinámico posible", "un minuto como mucho").
// Brutos (4K HDR 60 fps, iPhone): bruto/IMG_13xx.MOV + IMG_0101 → al cerrar van a `bruto terminado/2026-11-10_bici-nueva-trek_NN-….MOV`.
//   Intro: IMG_1349 (pedido por Lucas) · presentación de la bici: IMG_1307 · cambios: 1309 · pedales: 1320 · calas: 1321 · casco: 1324 ·
//   portabidones: 0101 · prueba: 1337, 1339, 1340 · cierre: 1359 + 1362 · b-roll bici: 1310, 1311, 1313, 1315, 1316, 1317, 1319 · tienda: 1332.
// Proxies: solo la VENTANA usada de cada bruto (misma receta que herramientas/proxy.sh … 2160, con avconvert --start/--duration);
//   INI = s del bruto en que empieza cada proxy (1349 está entero). Render con --scale=2 (2160×3840).
// Voz y subtítulos: montar.py (tramos del bruto → voz.wav + montaje.json). Sin aislar (ruido −52 dB); highpass 80, ganancia fija por tramo.
// Música (pedida por Lucas: "juega con música de fondo"): ElevenLabs Music, funk/vlog 117 BPM, −14 LUFS; baja bajo la voz y sube en los huecos.
import { Audio, Video } from "@remotion/media";
import React from "react";
import { AbsoluteFill, Composition, Easing, Img, interpolate, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Sfx } from "../../comun/hablando";
import { ACENTO, CREMA, F_FUERTE, F_RELLENO } from "../../comun/hablando";
import { Rotulo, RotuloHandle, SOMBRA_ROTULO } from "../../comun/Rotulos";
import { Palabra, Subtitulos } from "../../comun/Subtitulos";
import montajeV1 from "./montaje.json";
import montajeV2 from "./montaje-v2.json";

const S = "bici-nueva-trek";
const FPS = 30;
const f = (s: number) => Math.round(s * FPS);
const MEZCLA = 0.7; // todo 3 dB bajo para que nada sature dentro del render; el volumen final se pone después con ganancia fija
const GAIN_VOZ = 0.71 * MEZCLA; // voz mono → +3 dB en el render estéreo

// s del bruto en que empieza cada proxy (ventanas)
const INI: Record<string, number> = {
  "1349": 0, "1307": 54, "1309": 76, "1320": 25, "1321": 5, "1337": 11, "1339": 4, "1340": 12, "1359": 7, "1362": 0,
  "1309a": 3, "1310": 0, "1311": 0, "1313": 0, "1315": 3, "1316": 0, "1317": 8, "1319": 0, "1324": 0, "0101": 0, "1332": 2, "1346": 0, "1330": 0, "1344": 0,
};

type Seg = { id: string; clip: string | null; a: number; b: number; t: number };
type Montaje = { dur: number; segs: Seg[]; palabras: (Palabra & { seg: string })[] };
// Versiones (2026-11-10, para presentar dos): v1 corta (60 s) · v2 larga (71 s: + saludo a Álvaro y "no tengo ni idea… que me asesoren… he elegido venir aquí")
const MONTAJES: Record<string, Montaje> = { v1: montajeV1 as Montaje, v2: montajeV2 as Montaje };

// ---------------------------------------------------------------- planos
// Cada plano dura hasta el siguiente. Sin `clip` = el propio tramo, sincronizado con su voz. Con `clip` = b-roll (voz en off).
type Plano = { seg: string; v?: "v1" | "v2"; fuente?: string; off?: number; clip?: string; desde?: number; zoom?: number; origen?: string; empuje?: number; vel?: number; entrada?: boolean; nota: string };
const PLANOS: Plano[] = [
  { seg: "hook", entrada: true, origen: "50% 38%", nota: "Acompañadme a buscar mi bici nueva a Trek (fachada)" },
  { seg: "saludo", nota: "¿Qué pasa, Álvaro? ¿Cómo estamos? (apretón de manos)" },
  { seg: "venido", nota: "He venido a por la bici, que no la he visto aún (con Álvaro)" },
  { seg: "ensenas", zoom: 1.12, origen: "50% 38%", nota: "¿Me la enseñas? — ¿Preparado para conocerla?" },
  { seg: "paseo", clip: "1349", desde: 30.4, vel: 1.5, nota: "andando por la tienda (de espaldas)" },
  { seg: "paseo", off: 0.85, clip: "1332", desde: 4.0, empuje: 0.05, nota: "tienda: pared Project One" },
  { seg: "presento", nota: "Pues te presento" },
  { seg: "domane", nota: "la nueva Domane, que es tu bici (la bici al fondo)" },
  { seg: "project", nota: "un Project One" },
  { seg: "project", off: 1.28, clip: "1310", desde: 0.4, empuje: 0.05, nota: "con ruedas de carbono (rueda delantera)" },
  { seg: "locura", nota: "Es una locura, tío (Lucas sonríe)" },
  { seg: "mia", nota: "¿Esta es la mía? — Esta es la tuya" },
  { seg: "pintaza", v: "v1", nota: "yo no tengo ni idea de bicis" },
  { seg: "pintaza", v: "v1", off: 1.24, clip: "1311", desde: 0.3, empuje: 0.04, nota: "pero tiene una pintaza (bici entera)" },
  { seg: "pintaza", v: "v2", clip: "1311", desde: 0.3, empuje: 0.04, nota: "pero tiene una pintaza (bici entera)" },
  { seg: "historicos", nota: "uno de los modelos históricos de la marca Trek (Álvaro)" },
  { seg: "sram", clip: "1317", desde: 13.7, empuje: 0.04, nota: "cambio SRAM Force (bielas Force)" },
  { seg: "sram", off: 1.6, clip: "1316", desde: 1.5, empuje: 0.04, nota: "electrónico (cambio trasero)" },
  { seg: "comodo", nota: "muy cómodo (Álvaro)" },
  { seg: "comodo", off: 1.0, clip: "1315", desde: 5.4, empuje: 0.04, nota: "para estar muchas horas en bici (sillín)" },
  { seg: "ideal", clip: "1313", desde: 0.8, empuje: 0.04, nota: "ideal para gente que está empezando (manillar)" },
  { seg: "niidea", fuente: "1309a", nota: "como ya sabéis, no tengo ni idea de ciclismo (Lucas junto a la bici)" },
  { seg: "asesoraran", fuente: "1309a", zoom: 1.12, origen: "62% 30%", nota: "quería que me asesoraran" },
  { seg: "contodo", clip: "1321", desde: 10.2, empuje: 0.04, nota: "me van a asesorar con todo (atándose las zapatillas; en el casco 0–4 s se cruza una persona)" },
  // 2026-11-10 (Lucas): "algún plano más de la tienda, un poco más rápido, no solo uno" → 4 planos de ~0,5 s
  { seg: "elegido", clip: "1346", desde: 0.4, empuje: 0.06, nota: "he elegido venir aquí · tienda: plano general" },
  { seg: "elegido", off: 0.55, clip: "1344", desde: 1.0, empuje: 0.06, nota: "tienda: fila de bicis" },
  { seg: "elegido", off: 1.08, clip: "1330", desde: 0.3, empuje: 0.06, nota: "tienda: cartel \"Prueba una Trek hoy mismo\"" },
  { seg: "elegido", off: 1.62, clip: "1332", desde: 6.0, empuje: 0.06, nota: "tienda: pared Project One" },
  { seg: "aconsejar", fuente: "1309a", nota: "nosotros te aconsejaremos en todo (Álvaro)" },
  { seg: "derecha", nota: "la derecha es para subir (manetas)" },
  { seg: "izquierda", zoom: 1.12, origen: "40% 52%", nota: "y la izquierda para bajar. Y si aprietas los dos" },
  { seg: "plato", clip: "1319", desde: 1.6, empuje: 0.04, nota: "cambias el plato (platos)" },
  { seg: "pedales", nota: "le están montando los pedales (Lucas a cámara)" },
  { seg: "pedales", off: 1.62, clip: "1320", desde: 36.6, empuje: 0.04, nota: "y ahora nos subiremos (montando el pedal)" },
  { seg: "caigo", clip: "1320", desde: 38.4, zoom: 1.1, empuje: 0.04, nota: "a ver si no me caigo (pedal, más cerca)" },
  { seg: "bidon", clip: "0101", desde: 3.0, empuje: 0.05, nota: "portabidones" },
  { seg: "calas", nota: "La primera vez que me pongo unas calas" },
  { seg: "casco", clip: "1324", desde: 7.2, empuje: 0.05, nota: "casco" },
  { seg: "verdad", nota: "Y ahora la hora de la verdad" },
  { seg: "casi", nota: "Uy, ves, casi" },
  { seg: "vuelta", clip: "1339", desde: 6.3, nota: "rodando por la tienda" },
  { seg: "conseguido", nota: "he conseguido subir y dar la primera vuelta" },
  { seg: "nocaido", nota: "No me he caído, ¿eh?" },
  { seg: "tenemos", nota: "ya tenemos bici nueva gracias a Trek Barcelona Centre" },
  { seg: "seguidme", nota: "Y si queréis ver mis próximas salidas, seguidme" },
];
const Toma: React.FC<{ p: Plano; s: Seg }> = ({ p, s }) => {
  const frame = useCurrentFrame();
  const clip = p.clip ?? p.fuente ?? s.clip!;
  const desde = (p.desde ?? s.a + (p.off ?? 0)) - INI[clip];
  // entrada: zoom 1→1,12 con whoosh (primer plano del vídeo); empuje: acercamiento lento continuo en los b-roll (ya son a pulso: poco)
  const entrada = p.entrada ? interpolate(frame, [0, 20], [1, 1.12], { extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic) }) : 1;
  const empuje = p.empuje ? 1.02 + (p.empuje * frame) / FPS : 1;
  return (
    <AbsoluteFill style={{ transform: `scale(${(p.zoom ?? 1) * entrada * empuje})`, transformOrigin: p.origen ?? "50% 50%" }}>
      <Video src={staticFile(`${S}/${clip}.mp4`)} trimBefore={f(desde)} playbackRate={p.vel ?? 1} muted style={{ width: "100%", height: "100%" }} />
    </AbsoluteFill>
  );
};

// ---------------------------------------------------------------- rótulos
const Pop: React.FC<{ top: number; children: React.ReactNode; dur?: number }> = ({ top, children, dur }) => {
  const frame = useCurrentFrame();
  const sale = dur ? interpolate(frame, [dur - 5, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }) : 1;
  const o = interpolate(frame, [0, 5], [0, 1], { extrapolateRight: "clamp" }) * sale;
  const sc = interpolate(frame, [0, 8], [0.8, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2)) });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: top }}>
      <div style={{ opacity: o, transform: `scale(${sc})` }}>{children}</div>
    </AbsoluteFill>
  );
};

// Pin de ubicación (pedido por Lucas, 2026-11-10): al decir "gracias a Trek Barcelona Centre" → pin + nombre de la tienda y la dirección debajo.
// Dirección de la ficha oficial de Trek (trekbikes.com/es/es_ES/retail/barcelona_centre): Carrer de Bailèn 86, 08009 Barcelona.
const Ubicacion: React.FC = () => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
      <svg width={70} height={84} viewBox="0 0 24 29" style={{ filter: "drop-shadow(0 4px 12px rgba(0,0,0,0.6))" }}>
        <path d="M12 0.8C5.8 0.8 0.8 5.8 0.8 12c0 8.2 11.2 16.2 11.2 16.2S23.2 20.2 23.2 12C23.2 5.8 18.2 0.8 12 0.8z" fill={ACENTO} />
        <circle cx={12} cy={12} r={4.4} fill="#1a1a1a" />
      </svg>
      <div style={{ fontFamily: F_FUERTE, fontSize: 82, color: ACENTO, textTransform: "uppercase", lineHeight: 0.95, whiteSpace: "nowrap", textShadow: SOMBRA_ROTULO }}>Trek Barcelona Centre</div>
    </div>
    <div style={{ fontFamily: F_RELLENO, fontWeight: 600, fontSize: 40, color: CREMA, letterSpacing: -0.5, marginTop: 10, textShadow: SOMBRA_ROTULO }}>Carrer de Bailèn 86 · Barcelona</div>
  </div>
);

const CLAVES = /^(trek|domane|project|one|carbono|locura|pintaza|históricos|sram|force|electrónico|cómodo|plato|pedales|calas|casi|centre|seguidme)$/i;

// Gancho B (test 2026-11-10, v1.2 / v2.2, pedido por Lucas): el rótulo "voy a por mi bici nueva" está desde el fotograma 0
// (mientras dice "Acompañadme a buscar mi") y al decir "bici nueva" salta la bici misteriosa (imagen de Lucas sin el fondo rojo:
// herramientas/quitar_fondo_rojo.py "Mystery Road Bike Reveal Burst.png" public/bici-nueva-trek/bici-misterio.png).
const BiciMisterio: React.FC<{ dur: number }> = ({ dur }) => {
  const frame = useCurrentFrame();
  const sc = interpolate(frame, [0, 9], [0.3, 1], { extrapolateRight: "clamp", easing: Easing.out(Easing.back(2.2)) });
  const o = interpolate(frame, [0, 3], [0, 1], { extrapolateRight: "clamp" }) * interpolate(frame, [dur - 4, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const giro = interpolate(frame, [0, 9], [-8, 0], { extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: MISTERIO.top }}>
      <Img src={staticFile(`${S}/bici-misterio.png`)} style={{ width: MISTERIO.ancho, opacity: o, transform: `scale(${sc * (1 + 0.012 * Math.sin(frame / 4))}) rotate(${giro}deg)`, filter: "drop-shadow(0 10px 30px rgba(0,0,0,0.45))" }} />
    </AbsoluteFill>
  );
};
const MISTERIO = { top: 880, ancho: 520 }; // sobre el pecho: no tapa la cara (y 650–890) ni entra en la zona de UI (1500+)

const BiciNuevaTrek: React.FC<{ version: "v1" | "v2"; ganchoB?: boolean }> = ({ version, ganchoB }) => {
  const frame = useCurrentFrame();
  const M = MONTAJES[version];
  const SEGS = M.segs;
  const seg = (id: string) => SEGS.find((s) => s.id === id)!;
  const T = (id: string, off = 0) => seg(id).t + off; // s del edit
  const DUR = f(M.dur);
  const TODAS = M.palabras;
  const palabra = (re: RegExp) => TODAS.find((p) => re.test(p.w))!.start;
  const MI = palabra(/^mi$/);
  const BICI = palabra(/^bici$/);
  // gancho B: la bici misteriosa ocupa el sitio del subtítulo → sin subtítulo mientras está ("bici nueva" ya lo dice el rótulo)
  const PALABRAS = ganchoB ? TODAS.filter((p) => !(p.seg === "hook" && p.start >= BICI)) : TODAS;
  const DOMANE = palabra(/^Domane/);
  const SEGUIDME = palabra(/^seguidme/);
  const GRACIAS = palabra(/^gracias$/);
  const HUECOS = SEGS.filter((s) => !s.clip);
  const CORTES = SEGS.map((s) => s.t);
  const planos = PLANOS.filter((p) => (!p.v || p.v === version) && SEGS.some((s) => s.id === p.seg));
  const EN = (p: Plano) => T(p.seg, p.off ?? 0);
  // música: baja bajo la voz, sube en los huecos sin voz y en la cola
  const BAJA = 0.11, ALTA = 0.42;
  let m = BAJA;
  for (const h of HUECOS) m = Math.max(m, interpolate(frame, [f(h.t) - 4, f(h.t) + 2, f(h.t + h.b) - 4, f(h.t + h.b) + 2], [BAJA, ALTA, ALTA, BAJA], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  const finVoz = f(T("seguidme") + seg("seguidme").b - seg("seguidme").a);
  m = Math.max(m, interpolate(frame, [finVoz - 2, finVoz + 6], [BAJA, 0.34], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }));
  m *= interpolate(frame, [DUR - 14, DUR], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {planos.map((p, i) => {
        const ini = f(EN(p));
        const fin = i < planos.length - 1 ? f(EN(planos[i + 1])) : DUR;
        return (
          <Sequence key={i} name={p.nota} from={ini} durationInFrames={fin - ini} premountFor={FPS}>
            <Toma p={p} s={seg(p.seg)} />
          </Sequence>
        );
      })}
      <Subtitulos palabras={PALABRAS} offset={0} claves={CLAVES} cortes={CORTES} maxHueco={0.5} />
      {/* Gancho: entra cuando lo dice ("mi bici nueva"), encima de la cabeza */}
      <Sequence name="Rótulo gancho" from={ganchoB ? 0 : f(MI)} durationInFrames={f(SEGS[1].t) - (ganchoB ? 0 : f(MI))}>
        <Pop top={370}>
          <Rotulo arriba="voy a por" texto="mi bici nueva" size={132} />
        </Pop>
      </Sequence>
      {ganchoB ? (
        <Sequence name="Pop · bici misteriosa" from={f(BICI)} durationInFrames={f(SEGS[1].t) - f(BICI)}>
          <BiciMisterio dur={f(SEGS[1].t) - f(BICI)} />
        </Sequence>
      ) : null}
      <Sequence name="Rótulo Trek Domane" from={f(DOMANE)} durationInFrames={f(T("locura")) - f(DOMANE)}>
        <Pop top={1300} dur={f(T("locura")) - f(DOMANE)}>
          <Rotulo arriba="mi bici nueva" texto="Trek Domane" size={120} />
        </Pop>
      </Sequence>
      <Sequence name="Pin · Trek Barcelona Centre" from={f(GRACIAS)} durationInFrames={f(T("seguidme")) - f(GRACIAS)}>
        <Pop top={250}>
          <Ubicacion />
        </Pop>
      </Sequence>
      <Sequence name="CTA · @lucasalvarez.x" from={f(SEGUIDME)}>
        <Pop top={1300}>
          <RotuloHandle size={84} />
        </Pop>
      </Sequence>
      {/* Sonido: SFX solo en cambios completos de lo que enseña la cámara */}
      <Sfx en={0} src="whoosh.mp3" volumen={0.4 * MEZCLA} />
      {ganchoB ? <Sfx en={f(BICI)} src="pop.mp3" volumen={0.4 * MEZCLA} /> : <Sfx en={f(MI)} src="sparkle.mp3" volumen={0.22 * MEZCLA} />}
      <Sfx en={f(T("paseo")) - 3} src="whoosh-short.mp3" volumen={0.4 * MEZCLA} />
      <Sfx en={f(DOMANE)} src="sparkle.mp3" volumen={0.3 * MEZCLA} />
      <Sfx en={f(T("bidon")) - 2} src="whoosh-short.mp3" volumen={0.3 * MEZCLA} />
      <Sfx en={f(GRACIAS)} src="pop.mp3" volumen={0.3 * MEZCLA} />
      <Sfx en={f(SEGUIDME)} src="pop.mp3" volumen={0.35 * MEZCLA} />
      <Audio src={staticFile(`${S}/${version === "v2" ? "voz-v2" : "voz"}.wav`)} volume={GAIN_VOZ} />
      <Audio src={staticFile(`${S}/musica.mp3`)} volume={() => m * MEZCLA} />
    </AbsoluteFill>
  );
};

export const BiciNuevaTrekComp: React.FC = () => (
  <>
    <Composition id="BiciNuevaTrek" component={BiciNuevaTrek} defaultProps={{ version: "v1" as const }} durationInFrames={f(MONTAJES.v1.dur)} fps={FPS} width={1080} height={1920} />
    <Composition id="BiciNuevaTrekV12" component={BiciNuevaTrek} defaultProps={{ version: "v1" as const, ganchoB: true }} durationInFrames={f(MONTAJES.v1.dur)} fps={FPS} width={1080} height={1920} />
    <Composition id="BiciNuevaTrekV22" component={BiciNuevaTrek} defaultProps={{ version: "v2" as const, ganchoB: true }} durationInFrames={f(MONTAJES.v2.dur)} fps={FPS} width={1080} height={1920} />
    <Composition id="BiciNuevaTrekV2" component={BiciNuevaTrek} defaultProps={{ version: "v2" as const }} durationInFrames={f(MONTAJES.v2.dur)} fps={FPS} width={1080} height={1920} />
  </>
);
