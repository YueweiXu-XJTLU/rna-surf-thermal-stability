import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

sns.set(style="whitegrid", font_scale=1.18)
plt.rcParams['axes.titlesize'] = 17
plt.rcParams['axes.labelsize'] = 14

files = [
    ('pairing_basepair_annotate_300k_comma.csv', '300K'),
    ('pairing_basepair_annotate_360k_comma.csv', '360K'),
]
target = 'WCc'

all_pairs = set()
pair2count_by_temp = {}

def parse_frame_csv(file, target_type):
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
        found_pairs = set()
        for res1, res2, type_ in frame:
            if type_ == target_type:
                pair = (res1, res2)  # 不排序，正反视为不同
                found_pairs.add(pair)
        for pair in found_pairs:
            pair_counter[pair] += 1
    all_pairs.update(pair_counter.keys())
    return pair_counter, len(frame_data)

# 统计
for file, label in files:
    pair_counter, total_frames = parse_frame_csv(file, target)
    pair2count_by_temp[label] = (pair_counter, total_frames)

# 组装DataFrame
all_pairs = sorted(all_pairs)
plot_df = pd.DataFrame(index=['{} → {}'.format(pair[0][:-2], pair[1][:-2]) for pair in all_pairs])

for idx, (file, label) in enumerate(files):
    pair_counter, total_frames = pair2count_by_temp[label]
    probs = []
    for pair in all_pairs:
        count = pair_counter[pair]
        prob = 100 * count / total_frames
        probs.append(prob)
    plot_df[label] = probs

# 只画频率>0%的pair（自调）
mask = (plot_df > -10).any(axis=1)
plot_df = plot_df[mask]

# 按碱基对名称字母表顺序排序
plot_df = plot_df.sort_index()

# 作图
fig, ax = plt.subplots(figsize=(min(2 + 0.4 * len(plot_df), 14), 7))
width = 0.36
x = np.arange(len(plot_df))

colors = ["#71b7ed", "#f2656f"]

for idx, label in enumerate(plot_df.columns):
    ax.bar(x + (idx - 0.5) * width, plot_df[label], width=width,
           label=label, color=colors[idx], alpha=0.92)

ax.set_xticks(x)
ax.set_xticklabels(plot_df.index, rotation=55, ha='right', fontsize=12)
ax.set_ylabel(f'Frequency of {target} (%)')
ax.set_xlabel('Base Pair')
ax.set_title(f'Frequency of {target} Base Pairs at 300K & 360K')
ax.legend(title='Temperature')
ax.set_ylim(0, plot_df.values.max() * 1.22)
ax.grid(axis='y', alpha=0.25)

plt.tight_layout()
plt.savefig(f'../img/4_2_2_hbonds_{target}_frequency.png', dpi=320)
plt.show()
