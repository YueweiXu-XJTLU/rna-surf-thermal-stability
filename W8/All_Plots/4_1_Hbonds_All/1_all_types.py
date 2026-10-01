import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = [
    ("pairing_basepair_annotate_300k_comma.csv", "300K"),
    ("pairing_basepair_annotate_320k_comma.csv", "320K"),
    ("pairing_basepair_annotate_340k_comma.csv", "340K"),
    ("pairing_basepair_annotate_360k_comma.csv", "360K"),
    ("pairing_basepair_annotate_380k_comma.csv", "380K"),
    ("pairing_basepair_annotate_400k_comma.csv", "400K"),
]
pair_type = 'WCc'
colors = ['#b8aeeb', '#71b7ed', '#84c3b7', '#fae69e', '#f2656f', '#f57c6e']

plt.figure(figsize=(10, 5))

for idx, (file, label) in enumerate(files):
    frame_data = []
    current_frame = []
    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.lower().startswith('res1'):
                continue
            if line.startswith('# Frame'):
                if current_frame:
                    frame_data.append(current_frame)
                    current_frame = []
            else:
                parts = [x.strip() for x in line.split(',')]
                if len(parts) == 3:
                    current_frame.append(parts)
        if current_frame:
            frame_data.append(current_frame)  # 最后一帧

    # 统计每帧的配对数量
    count_per_frame = []
    for frame in frame_data:
        df = pd.DataFrame(frame, columns=['res1', 'res2', 'type'])
        count_per_frame.append((df['type'] == pair_type).sum())
    y = np.array(count_per_frame)
    mean, std = y.mean(), y.std()

    total_time_ps = 1e6
    frames = len(y)
    time = np.linspace(0, total_time_ps, frames)  # 横轴时间（ps）

    plt.plot(time, y, label=f"{label} (Mean={mean:.2f}±{std:.2f})", color=colors[idx], linewidth=2)
    plt.axhline(mean, color=colors[idx], linestyle=':', alpha=1, linewidth=1.5)
    # plt.fill_between(time, y - std, y + std, color=colors[idx], alpha=0.1)

plt.xlabel('Time (μs)', fontsize=14)
plt.ylabel(f'{pair_type} Base Pairs', fontsize=14)
plt.title(f'WCc Base Pair Count Over Time at Different Temperatures', fontsize=16)
plt.tight_layout()
plt.legend(title='Temperature', frameon=True, loc='best', fontsize=8)
plt.grid(True)
plt.savefig('../img/4_1_1_hbonds_WCc_count.svg', dpi=300)
plt.show()
