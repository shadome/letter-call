# Letter Call Timer

A one-screen HIIT reaction timer for Android. It calls random letters (A–Z) in a British voice, with a 3‑2‑1 countdown, a beep between letters, a STOP cue and rest between cycles.

**Open it:** https://shadome.github.io/letter-call/

## Install on Android
1. Open the address above in Chrome.
2. Tap **Install** at the top of the timer, or Chrome menu ⋮ → **Install app**.
3. Start it from the home screen. It opens without the browser bar and works offline.

## What it does
- Before / After times around each letter, in steps of 0.05 s, always shown with two decimals (1.00). The random range option is switched off for now; its logic is kept in the code.
- Beep between letters (✓ / ✗ toggle, on by default): sounds when the Before gap starts.
- Pre-beep (0.5 s by default, can be Off or 0.1–3.0 s): the beep also sounds that long before each letter, so you can get ready. It sits inside the Before gap and never changes the Before/After timing. The first letter of a cycle has the 3‑2‑1 instead. With the beep between letters on, a pre-beep within 0.3 s of it is skipped; with it off, a pre-beep longer than the gap plays at the start of the gap.
- Letters per cycle, number of cycles (or endless), rest between cycles, and which letters are in the draw. Get ready (Start to the first letter) is a fixed 5 s.
- Two British voices, female ♀ and male ♂ (tap one to hear it).
- Repeats (✓ / ✗ toggle, ✓ by default): ✓ lets the same letter come twice in a row, ✗ never does.
- Defaults: letters A–D, repeats allowed, before 1.00 s, after 1.00 s, 12 letters per cycle, 8 cycles, 15 s rest, beep between letters on, pre-beep 0.5 s.
- Start, pause, reset. Keeps the screen on while a session runs and pauses itself if the app goes to the background.
- Settings are remembered on the phone.

## Project layout
| Path | What it is |
|---|---|
| `index.html`, `sw.js`, `manifest.webmanifest`, `icons/`, `fonts/` | The published app (generated, served by GitHub Pages) |
| `src/template.html` | The app source: layout, styles, timer engine, sounds |
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
- Beeps and other sound effects are synthesised live in the browser.
