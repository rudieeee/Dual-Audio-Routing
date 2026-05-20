# DualStream 🎧

> Route call audio to your left ear and music to your right ear — simultaneously, with independent volume control.

---

## The Problem

Every time a call comes in, your music stops. You either take the call and lose the music, or ignore the call to keep listening. There's no middle ground.

## The Solution

DualStream splits your audio by ear:

- **Left ear** → Google Meet · WhatsApp · any call
- **Right ear** → YouTube · Spotify · Apple Music · any music
- **Independent volume** → control each ear separately while both play

---

## Demo

```
DualStream running 🎧

Input  → DualStream Input [5]
Output → Sony WH-CH720N  [0]

call+  / call-   → call volume up / down
music+ / music-  → music volume up / down
q                → quit
```

---

## How It Works

```
Google Meet / WhatsApp  ──→  BlackHole 2ch   (ch 16-17) ─┐
                                                           ├─→  Python mixer  ──→  LEFT  ear
YouTube / Apple Music   ──→  BlackHole 16ch  (ch 0-15)  ─┘                   ──→  RIGHT ear
                                                                                      ↓
                                                                              WH-CH720N (Bluetooth)
```

BlackHole creates two virtual audio cables on your Mac. Apps pipe audio into them. The Python script reads both streams simultaneously via an Aggregate Device, splits them into left and right stereo channels, and sends the mixed output to your headphones.

No audio is recorded. No internet connection required. Fully offline.

---

## Requirements

- macOS
- Python 3.8+
- [BlackHole 2ch](https://existential.audio/blackhole/) — virtual audio driver (free)
- [BlackHole 16ch](https://existential.audio/blackhole/) — virtual audio driver (free)
- Bluetooth headphones

---

## Installation

### 1. Install BlackHole

Download and install both **BlackHole 2ch** and **BlackHole 16ch** from [existential.audio/blackhole](https://existential.audio/blackhole). Restart your Mac after installing.

### 2. Create Aggregate Device

1. Open **Audio MIDI Setup** (search in Spotlight)
2. Click **+** → **Create Aggregate Device**
3. Check **BlackHole 16ch** and **BlackHole 2ch**
4. Enable **Drift Correction** on BlackHole 2ch
5. Rename the device to **`DualStream Input`**

### 3. Set Up Python

```bash

python3 -m venv venv
source venv/bin/activate
pip install sounddevice numpy
```

### 4. Route Your Apps

Go to **System Settings → Sound → Apps** (play audio in each app first so it appears in the list):

| App | Output Device |
|---|---|
| WhatsApp | BlackHole 2ch |
| Google Meet (Safari) | BlackHole 2ch |
| YouTube | BlackHole 16ch |
| Spotify | BlackHole 16ch |
| Apple Music | BlackHole 16ch |

---

## Usage

```bash
source venv/bin/activate
python3 dualstream.py
```

### Controls

| Command | Action |
|---|---|
| `music+` | Music volume +10% |
| `music-` | Music volume -10% |
| `call+` | Call volume +10% |
| `call-` | Call volume -10% |
| `q` | Quit |

---

## Troubleshooting

**Both ears getting the same audio**
Make sure each app is routed to the correct BlackHole in System Settings → Sound → Apps.

**Crackling or stuttering**
Increase the buffer size in `dualstream.py`:
```python
BLOCK_SIZE = 2048  # default is 1024
```

**Headphones not detected**
Connect your headphones via Bluetooth before running the script.

**App not showing in Sound → Apps**
The app must be actively playing audio to appear. Play something in it first, then return to Sound settings.

---

## Why Not Regular Phone Calls?

Android's telephony stack handles cellular call audio at the OS level — below where any app can intercept it. This prototype uses VoIP calls (Meet, WhatsApp) which output through the app layer, making them capturable via BlackHole.

A native Android app that owns the call (built with WebRTC) would solve this completely and work with any headphones on any device. That's the next version.

---

## Roadmap

- [x] Core audio routing — call left, music right
- [x] Independent volume control per ear
- [ ] Menu bar app with GUI sliders
- [ ] Auto-duck music when call starts
- [ ] Keyboard shortcuts for volume control
- [ ] Native Android app (WebRTC + AudioTrack stereo routing)

---

## Tech Stack

- **Python 3** — audio processing
- **sounddevice** — real-time audio stream I/O
- **numpy** — PCM sample manipulation
- **BlackHole** — virtual audio driver for macOS
- **macOS Aggregate Device** — combines multiple audio inputs into one stream

---

## License

MIT — do whatever you want with it.

---

*Built by Rudra Yadav*
