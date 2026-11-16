// Quita el ruido de fondo y deja solo las voces (ElevenLabs Voice Isolator).
// Mantiene la duración y los tiempos del original (los cortes del montaje siguen valiendo).
//
// Uso (desde estudio/):
//   node --env-file=.env.local scripts/aislar-voz.mjs <audio_o_video> <salida.mp3>
import { ElevenLabsClient } from "@elevenlabs/elevenlabs-js";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { Readable } from "node:stream";
import { pipeline } from "node:stream/promises";

const [entrada, salida] = process.argv.slice(2);
if (!entrada || !salida) throw new Error("Uso: scripts/aislar-voz.mjs <audio_o_video> <salida.mp3>");

let audio = entrada;
if (!/\.(mp3|wav|m4a)$/i.test(entrada)) {
  audio = path.join(os.tmpdir(), `aislar-${process.pid}-${Date.now()}-${Math.random().toString(36).slice(2)}.wav`);
  execFileSync("ffmpeg", ["-v", "error", "-y", "-i", entrada, "-vn", "-ac", "1", "-ar", "44100", audio]);
}

const client = new ElevenLabsClient();
const stream = await client.audioIsolation.convert({ audio: fs.createReadStream(audio) });
await pipeline(Readable.fromWeb(stream), fs.createWriteStream(salida));

const dur = (f) => Number(execFileSync("ffprobe", ["-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f]).toString());
console.log(`ok: ${salida} (${dur(salida).toFixed(2)} s; original ${dur(audio).toFixed(2)} s)`);
