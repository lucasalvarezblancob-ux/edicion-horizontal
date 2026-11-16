// Transcripción precisa con tiempos por palabra (ElevenLabs Scribe v2).
// Mejor que Whisper local para sincronizar textos palabra a palabra en vídeos hablando a cámara.
//
// Uso (desde estudio/):
//   node --env-file=.env.local scripts/transcribir-scribe.mjs <audio_o_video> <salida.json> [idioma=spa|eng|auto]
// Salida: [{ "w": "palabra", "start": s, "end": s, "hablante": "speaker_0" }, ...] en tiempo del archivo original.
// (Para vídeos: extrae antes el audio con ffmpeg a .mp3/.wav — se hace solo si pasas un vídeo.)
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";

const [entrada, salida, idioma = "spa"] = process.argv.slice(2); // idioma: "spa", "eng"… o "auto"
if (!entrada || !salida) throw new Error("Uso: scripts/transcribir-scribe.mjs <audio_o_video> <salida.json>");

let audio = entrada;
if (!/\.(mp3|wav|m4a)$/i.test(entrada)) {
  audio = path.join(os.tmpdir(), `scribe-${process.pid}-${Date.now()}-${Math.random().toString(36).slice(2)}.mp3`);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", entrada, "-vn", "-ac", "1", "-ar", "44100", "-b:a", "128k", audio]);
}

const client = new ElevenLabsClient();
const res = await client.speechToText.convert({
  file: fs.createReadStream(audio),
  modelId: "scribe_v2",
  ...(idioma === "auto" ? {} : { languageCode: idioma }),
  timestampsGranularity: "word",
  tagAudioEvents: false,
  diarize: true, // separa hablantes (p. ej. quien dicta el guion fuera de plano)
});

const palabras = (res.words ?? [])
  .filter((w) => w.type === "word")
  .map((w) => ({ w: w.text, start: w.start, end: w.end, hablante: w.speakerId }));
fs.writeFileSync(salida, JSON.stringify(palabras, null, 1));
console.log(res.text);
console.log(`ok: ${palabras.length} palabras -> ${salida}`);
