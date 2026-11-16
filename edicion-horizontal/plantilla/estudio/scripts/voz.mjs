// Genera la voz en off con ElevenLabs (una sola toma) + tiempos por palabra.
//
// Uso (desde estudio/):
//   node --env-file=.env.local scripts/voz.mjs <guion.json|guion.txt> <salida_sin_extension> [voice_id]
// Escribe <salida>.mp3 y <salida>-palabras.json (sin acelerar ni quitar silencios:
// después pásalo por herramientas/apretar_voz.py).
//
// Por defecto: voz estilo Blair = Alberto Rodríguez, eleven_multilingual_v2, speed 1.2.
// Opcional: MODEL=eleven_v4 TAG="[relaxed, talking quickly]" SPEED=1.1 PREV="frase anterior"
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import fs from "node:fs";

const VOZ_BLAIR = "l1zE9xgNpUTaQCZzpNJa"; // Alberto Rodríguez - Serious, Narrative

const [guionPath, salida, voiceArg] = process.argv.slice(2);
if (!guionPath || !salida) {
  throw new Error("Uso: scripts/voz.mjs <guion.json|txt> <salida_sin_extension> [voice_id]");
}
const voiceId = voiceArg ?? VOZ_BLAIR;
const raw = fs.readFileSync(guionPath, "utf8");
const text = guionPath.endsWith(".json") ? JSON.parse(raw).text : raw.trim();

const model = process.env.MODEL ?? "eleven_multilingual_v2";
const speed = process.env.SPEED ? Number(process.env.SPEED) : model === "eleven_v4" ? undefined : 1.2;
const tag = process.env.TAG ? process.env.TAG + " " : ""; // solo eleven_v4 entiende etiquetas

const client = new ElevenLabsClient(); // lee ELEVENLABS_API_KEY del entorno
const res = await client.textToSpeech.convertWithTimestamps(voiceId, {
  text: tag + text,
  modelId: model,
  ...(model === "eleven_multilingual_v2" ? {} : { languageCode: "es" }),
  ...(process.env.PREV ? { previousText: process.env.PREV } : {}),
  outputFormat: "mp3_44100_128",
  voiceSettings: {
    stability: model === "eleven_v4" ? 0.4 : 0.5,
    similarityBoost: 0.8,
    ...(speed && model !== "eleven_v4" ? { speed } : {}),
  },
});

fs.writeFileSync(`${salida}.mp3`, Buffer.from(res.audioBase64, "base64"));

// Agrupa caracteres en palabras (se salta la etiqueta de dirección si la hay)
const a = res.alignment;
const words = [];
let cur = null;
a.characters.forEach((ch, i) => {
  if (/\s/.test(ch) || i < tag.length) {
    if (cur) words.push(cur);
    cur = null;
    return;
  }
  if (!cur) cur = { w: "", start: a.characterStartTimesSeconds[i], end: 0 };
  cur.w += ch;
  cur.end = a.characterEndTimesSeconds[i];
});
if (cur) words.push(cur);
fs.writeFileSync(`${salida}-palabras.json`, JSON.stringify(words, null, 1));
console.log(`ok ${salida}: ${words.length} palabras, ${words[words.length - 1].end.toFixed(2)} s`);
