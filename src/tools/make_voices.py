"""Regenerates src/voices.js (the spoken letters and cues) with the Kokoro TTS model, British voices.
Needs: pip install kokoro-onnx soundfile, ffmpeg on PATH, and the model files from
https://github.com/thewh1teagle/kokoro-onnx/releases (kokoro-v1.0.int8.onnx, voices-v1.0.bin) next to this script.
Add phrases to PHRASES, run:  python3 src/tools/make_voices.py   then  python3 src/build.py"""
import base64, json, os, subprocess, tempfile
import numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
VOICES = ["bf_emma", "bm_george"]
PHRASES = {c: c + "!" for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
PHRASES.update({"three": "Three!", "two": "Two!", "one": "One!", "stop": "Stop!", "rest": "Rest.", "ready": "Get ready!", "done": "Well done!"})

k = Kokoro(os.path.join(HERE, "kokoro-v1.0.int8.onnx"), os.path.join(HERE, "voices-v1.0.bin"))
out = {}
with tempfile.TemporaryDirectory() as tmp:
    for voice in VOICES:
        out[voice] = {}
        for key, text in PHRASES.items():
            a, sr = k.create(text, voice=voice, speed=1.05, lang="en-gb")
            a = np.asarray(a, dtype=np.float32)
            idx = np.where(np.abs(a) > 0.02 * np.abs(a).max())[0]           # trim silence
            a = a[max(0, idx[0] - int(0.012 * sr)): min(len(a), idx[-1] + int(0.06 * sr))]
            f = int(0.006 * sr); a[:f] *= np.linspace(0, 1, f); a[-f * 3:] *= np.linspace(1, 0, f * 3)
            a = a / max(1e-9, np.abs(a).max()) * 0.89                       # same peak level for every clip
            wav, mp3 = os.path.join(tmp, "c.wav"), os.path.join(tmp, "c.mp3")
            sf.write(wav, a, sr)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-ac", "1", "-ar", "24000", "-c:a", "libmp3lame", "-b:a", "40k", mp3], check=True)
            out[voice][key] = base64.b64encode(open(mp3, "rb").read()).decode()
open(os.path.join(HERE, "..", "voices.js"), "w").write("const VOICE_DATA=" + json.dumps(out, separators=(",", ":")) + ";")
print("wrote src/voices.js")
