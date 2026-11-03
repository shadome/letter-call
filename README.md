# Letter Call Timer

A one-screen HIIT reaction timer for Android. It calls random letters (A–Z) in a British voice, with a 3‑2‑1 countdown, a beep between letters, a STOP cue, rest between cycles and synthesised workout music.

**Open it:** https://shadome.github.io/letter-call/

## Install on Android
1. Open the address above in Chrome.
2. Tap **Install** at the top of the timer, or Chrome menu ⋮ → **Install app**.
3. Start it from the home screen. It opens without the browser bar and works offline.

## What it does
- Before / After times around each letter, in tenths of a second, with an optional random range (the second value is always strictly higher).
- Optional pre-beep (off by default): the beep also sounds a set time before each letter (0.1–3.0 s), so you can get ready. The first letter of a cycle has the 3‑2‑1 instead, and a pre-beep that would fall within 0.3 s of the beep between letters is skipped.
- Letters per cycle, number of cycles (or endless), rest between cycles, get-ready time, and which letters are in the draw.
- Two British voices (Emma, George), five original music loops (house, hardstyle, drum & bass, synthwave, trap).
- Start, pause, reset. Keeps the screen on while a session runs and pauses itself if the app goes to the background.
- Settings are remembered on the phone.

## Project layout
| Path | What it is |
|---|---|
| `index.html`, `sw.js`, `manifest.webmanifest`, `icons/`, `fonts/` | The published app (generated, served by GitHub Pages) |
| `src/template.html` | The app source: layout, styles, timer engine, music engine |
| `src/voices.js` | The spoken letters and cues, as embedded MP3 clips |
| `src/sw.template.js` | Offline service worker template |
| `src/build.py` | Builds `index.html` and `sw.js` from the sources |
| `src/tools/` | Scripts that regenerate the voice clips and the icons |

## Making a change
Edit `src/template.html`, then run:

```sh
python3 src/build.py
```

Commit and push. GitHub Pages republishes within a minute or two. Installed copies update the next time they are opened with a connection.

## Credits
- Voices generated with [Kokoro](https://github.com/hexgrad/kokoro) (Apache 2.0) via [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx).
- Fonts: Big Shoulders Display and Barlow Semi Condensed, SIL Open Font License.
- Music and sound effects are synthesised live in the browser.
