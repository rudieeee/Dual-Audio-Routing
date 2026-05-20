import sounddevice as sd
import numpy as np

# find aggregate device
agg_id = None
for i, d in enumerate(sd.query_devices()):
    print(f"[{i}] {d['name']} — in:{d['max_input_channels']} out:{d['max_output_channels']}")
    if 'aggregate' in d['name'].lower() or 'dualstream' in d['name'].lower():
        agg_id = i

print(f"\nAggregate device ID: {agg_id}")
print(f"Total input channels: {sd.query_devices(agg_id)['max_input_channels']}")
