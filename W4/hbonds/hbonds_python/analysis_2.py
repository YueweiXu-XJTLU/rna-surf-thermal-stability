# 统计某个配对在轨迹中出现的频率（帧数）
from collections import Counter
import pandas as pd

file = 'basepair_annotate_ANNOTATE_pairing_out.csv'
frame_data = []
current_frame = None

with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('# Frame'):
            current_frame = int(line.split()[2])
            frame_data.append([])
        elif line and not line.startswith('#'):
            parts = line.split()
            if len(parts) == 3:
                frame_data[-1].append(parts)
pair_counter = Counter()
for frame in frame_data:
    for res1, res2, type_ in frame:
        if type_ == "WCc": # 更改目标配对类型
            pair = tuple(sorted([res1, res2]))
            pair_counter[pair] += 1

print('WCc配对出现频次（所有帧）:')
for pair, count in pair_counter.most_common():
    print(f'{pair}: {count} frames')