from collections import Counter
import pandas as pd

file = 'pairings.csv'  # 或你的文件名
df = pd.read_csv(file)

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

pair_counter = Counter()
n_frames = df['frame'].max() + 1

# 统计每一帧中所有pair，避免重复计数
for f in range(n_frames):
    sub = df[(df['frame'] == f) & (df['pair_type'] == target)]
    found_pairs = set(tuple(sorted([row['base_i'], row['base_j']])) for _, row in sub.iterrows())
    for pair in found_pairs:
        pair_counter[pair] += 1

print(f'{target}配对在轨迹中出现的帧数（频率）：')
for pair, count in pair_counter.most_common():
    prob = count / n_frames * 100
    print(f'{pair}: {count} frames ~ probability: {prob}%')