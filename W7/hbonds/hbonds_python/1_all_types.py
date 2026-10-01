import pandas as pd
import matplotlib.pyplot as plt

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
                    print("检测到无Frame标签的配对行，已跳过:", line)
                    input("Just let you know~ Type anything: ")
                    continue
                frame_data[-1].append(parts)

# 控制台输出
for i, frame in enumerate(frame_data):
    df = pd.DataFrame(frame, columns=['res1', 'res2', 'type'])
    counts = df['type'].value_counts()
    print(f'Frame {i}:')
    print(counts)
    print('---')

# 统计所有配对类型
all_types = set()
for frame in frame_data:
    df = pd.DataFrame(frame, columns=['res1', 'res2', 'type'])
    all_types.update(df['type'].unique())
all_types = sorted(all_types)
print("所有配对类型:", all_types)

# 统计每种配对类型每帧数量
type_counts = {tp: [] for tp in all_types}
for frame in frame_data:
    df = pd.DataFrame(frame, columns=['res1', 'res2', 'type'])
    for tp in all_types:
        cnt = (df['type'] == tp).sum()
        type_counts[tp].append(cnt)

# 画图，可按需注释/取消注释
plt.figure(figsize=(10, 5))

# plt.plot(range(len(frame_data)), type_counts['GUc'], label='GUc')
# plt.plot(range(len(frame_data)), type_counts['HHc'], label='HHc')
# plt.plot(range(len(frame_data)), type_counts['HHt'], label='HHt')
# plt.plot(range(len(frame_data)), type_counts['HSc'], label='HSc')
# plt.plot(range(len(frame_data)), type_counts['HSt'], label='HSt')
# plt.plot(range(len(frame_data)), type_counts['HWc'], label='HWc')
# plt.plot(range(len(frame_data)), type_counts['HWt'], label='HWt')
# plt.plot(range(len(frame_data)), type_counts['SHc'], label='SHc')
# plt.plot(range(len(frame_data)), type_counts['SHt'], label='SHt')
# plt.plot(range(len(frame_data)), type_counts['SSc'], label='SSc')
# plt.plot(range(len(frame_data)), type_counts['SSt'], label='SSt')
# plt.plot(range(len(frame_data)), type_counts['SWc'], label='SWc')
# plt.plot(range(len(frame_data)), type_counts['SWt'], label='SWt')
# plt.plot(range(len(frame_data)), type_counts['WHc'], label='WHc')
# plt.plot(range(len(frame_data)), type_counts['WHt'], label='WHt')
# plt.plot(range(len(frame_data)), type_counts['WSc'], label='WSc')
# plt.plot(range(len(frame_data)), type_counts['WSt'], label='WSt')
# plt.plot(range(len(frame_data)), type_counts['XXX'], label='XXX')
plt.plot(range(len(frame_data)), type_counts['WCc'], label='WCc')
plt.plot(range(len(frame_data)), type_counts['WWc'], label='WWc')
plt.plot(range(len(frame_data)), type_counts['WWt'], label='WWt')

plt.xlabel('Frame')
plt.ylabel('Count')
plt.title('Numbers of Base Pairs Per Frame')
plt.tight_layout()
plt.legend()
plt.savefig("hbonds_all_diff_types.png")
plt.show()
