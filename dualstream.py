import sounddevice as sd
import numpy as np
import sys

SAMPLE_RATE = 44100
BLOCK_SIZE  = 512

call_vol  = 0.8
music_vol = 0.8

def callback(indata, outdata, frames, time, status):
    if status:
        print(status, file=sys.stderr)

    # indata channels come from the Aggregate Device in order:
    # channels 0-1 = BlackHole 2ch  → call audio (Google Meet / WhatsApp)
    # channels 2-3 = BlackHole 16ch → music audio (Apple Music / YouTube)

    call_audio  = indata[:, 16] * call_vol
    music_audio = indata[:, 0] * music_vol

    outdata[:, 0] = call_audio   # LEFT  ear ← call
    outdata[:, 1] = music_audio  # RIGHT ear ← music

def find(keyword, kind):
    for i, d in enumerate(sd.query_devices()):
        if keyword.lower() in d['name'].lower():
            if kind == 'in'  and d['max_input_channels']  > 0: return i
            if kind == 'out' and d['max_output_channels'] > 0: return i
    return None

aggregate = find('DualStream Input', 'in')
sony      = find('WH-CH720N', 'out')

if aggregate is None:
    print("DualStream Input aggregate device not found.")
    print("Create it in Audio MIDI Setup first.")
    sys.exit(1)

if sony is None:
    print("Sony headphones not found. Connect via Bluetooth.")
    print("\nAvailable outputs:")
    for i, d in enumerate(sd.query_devices()):
        if d['max_output_channels'] > 0:
            print(f"  [{i}] {d['name']}")
    sys.exit(1)

print(f"Input  → DualStream Input [{aggregate}]")
print(f"Output → Sony WH-CH720N  [{sony}]")
print("\ncall+ / call- / music+ / music- / q\n")

with sd.Stream(device=(aggregate, sony),
               samplerate=SAMPLE_RATE,
               blocksize=BLOCK_SIZE,
               channels=(18, 2),
               dtype='float32',
               callback=callback):
    print("DualStream running 🎧")
    while True:
        cmd = input().strip().lower()
        if cmd == 'q':
            break
        elif cmd in ('call+', 'call-'):
            call_vol = round(min(1.0, max(0.0, call_vol + (0.1 if '+' in cmd else -0.1))), 1)
            print(f"Call volume: {call_vol}")
        elif cmd in ('music+', 'music-'):
            music_vol = round(min(1.0, max(0.0, music_vol + (0.1 if '+' in cmd else -0.1))), 1)
            print(f"Music volume: {music_vol}")