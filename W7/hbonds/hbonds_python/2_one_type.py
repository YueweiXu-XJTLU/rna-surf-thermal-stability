# 统计某个配对在轨迹中出现的频率（帧数）
from collections import Counter
import pandas as pd
import csv

target = 'WCc'
# target = 'WWc'
# target = 'WWt'
# target = 'GUc'
# target = 'HHc'
# target = 'HHt'
# target = 'HSc'
# target = 'HSt'
# target = 'HWc'
# target = 'HWt'
# target = 'SHc'
# target = 'SHt'
# target = 'SSc'
# target = 'SSt'
# target = 'SWc'
# target = 'SWt'
# target = 'WHc'
# target = 'WHt'
# target = 'WSc'
# target = 'WSt'
# target = 'XXX'

output_file = open("hbonds_one_type.csv", 'w', newline='')
csv_writer = csv.writer(output_file)

file = 'full_trajectory_pair_comma.csv'

frame_data = []

with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('# Frame'):
            frame_data.append([])
        elif line and not line.startswith('#'):
            if line.lower().startswith('res1'):
                continue
            parts = [x.strip() for x in line.split(',')]
            if len(parts) == 3:
                if not frame_data:
                    continue
                frame_data[-1].append(parts)

pair_counter = Counter()
for frame in frame_data:
    # 用set避免同一帧里重复统计同一个pair（如有重复可保留此处理）
    found_pairs = set()
    for res1, res2, type_ in frame:
        if type_ == target:  # 改成需要的配对类型
            pair = tuple(sorted([res1, res2]))
            found_pairs.add(pair)
    for pair in found_pairs:
        pair_counter[pair] += 1

print(f'{target}配对在轨迹中出现的帧数（频率）：')
for pair, count in pair_counter.most_common():
    prob = pair_counter[pair] / len(frame_data)
    prob_100 = prob * 100
    csv_writer.writerow([pair, count, prob_100])
    # print(f'{pair}: {count} frames ~ probability: {prob_100}%' )

