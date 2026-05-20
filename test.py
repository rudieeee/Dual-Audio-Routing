import sounddevice as sd
import numpy as np

# Find Sony headphones
sony_id = None
for i, d in enumerate(sd.query_devices()):
    if 'WH-CH720N' in d['name'] and d['max_output_channels'] > 0:
        sony_id = i
        break

print(f"Sony device ID: {sony_id}")

sr = 44100
t = np.linspace(0, 2, sr * 2)
tone = np.sin(2 * np.pi * 440 * t).astype(np.float32)

# Test LEFT ear only
stereo = np.zeros((len(tone), 2), dtype=np.float32)
stereo[:, 0] = tone
print("Playing in LEFT ear...")
sd.play(stereo, samplerate=sr, device=sony_id)
sd.wait()

# Test RIGHT ear only
stereo2 = np.zeros((len(tone), 2), dtype=np.float32)
stereo2[:, 1] = tone
print("Playing in RIGHT ear...")
sd.play(stereo2, samplerate=sr, device=sony_id)
sd.wait()