# Live Captions

Real-time speech-to-text captions running **entirely in your browser**
— no cloud, no API key, no data leaves your machine.

**Live**: https://ohiomathteacher.github.io/applet-library/live-captions/

## How it works

Uses [transformers.js](https://huggingface.co/docs/transformers.js)
to run a local Whisper model in your browser. The model downloads
once (~40 MB for tiny.en), then transcribes audio from your
microphone in real time, displaying the words as captions on screen.

## Features

- **Three Whisper model sizes** — tiny.en (fast, ~40 MB), base.en
  (better, ~150 MB), small.en (great, ~480 MB)
- **Adjustable chunk size** — trade latency for accuracy
- **Caption font size** 24–120px
- **OBS overlay mode** — toggle transparent background to drop
  captions cleanly over video in OBS as a Browser Source
- **Keyboard shortcuts**:
  - `Space` — start/stop listening
  - `C` — clear captions
  - `O` — toggle OBS overlay mode
  - `+` / `−` — adjust font size

## Privacy

This page makes **no network calls during transcription**. Audio is
processed by a WASM build of Whisper running in your browser tab.
The only network activity is the one-time model download from
Hugging Face's CDN when you first click "Start listening."

## Recommended OBS workflow

Add as a Browser Source in OBS, toggle OBS overlay mode for
transparency, position over your camera feed. Live closed-captions
for any recording — accessibility win, classroom win, demo win.
