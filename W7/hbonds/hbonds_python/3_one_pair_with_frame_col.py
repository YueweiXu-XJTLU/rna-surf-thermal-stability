import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def normalize_input(s):
    s = s.strip().replace('/', '_')
    if not s.endswith('_0'):
        s = s + '_0'
    return s

# 读取数据
file = 'pairings_60_3.3.csv'  # 或你的文件名
df = pd.read_csv(file, header=0)

# 输入两个碱基
base1 = input("第一个碱基（如C/27）：").strip()
base2 = input("第二个碱基（如G/43）：").strip()
base1 = normalize_input(base1)
base2 = normalize_input(base2)
pair = tuple(sorted([base1, base2]))  # 统一顺序

# 检查方向
has_forward = not df[(df['base_i']==base1)&(df['base_j']==base2)].empty
has_reverse = not df[(df['base_i']==base2)&(df['base_j']==base1)].empty

forward_types = set(df.loc[(df['base_i']==base1)&(df['base_j']==base2), 'pair_type'])
reverse_types = set(df.loc[(df['base_i']==base2)&(df['base_j']==base1), 'pair_type'])

if has_forward and has_reverse:
    print(f"注意：你输入的两种顺序均存在！\n  {base1} → {base2} 配对类型: {sorted(forward_types)}\n  {base2} → {base1} 配对类型: {sorted(reverse_types)}")
elif has_forward:
    print(f"仅检测到 {base1} → {base2} 顺序，配对类型: {sorted(forward_types)}")
    all_types = forward_types
elif has_reverse:
    print(f"仅检测到 {base2} → {base1} 顺序，配对类型: {sorted(reverse_types)}")
    all_types = reverse_types
else:
    print("未检测到这对碱基有任何直接配对，后续统计为空。")
    all_types = set()

input("Just let you know~ Type anything: ")

# 统计每帧出现的类型（无则为No_Pair）
n_frames = df['frame'].max() + 1
type_per_frame = []
all_types_set = set()
for f in range(n_frames):
    sub = df[df['frame']==f]
    found_type = None
    for _, row in sub.iterrows():
        p = tuple(sorted([row['base_i'], row['base_j']]))
        if p == pair:
            found_type = row['pair_type']
            all_types_set.add(found_type)
            break
    type_per_frame.append(found_type if found_type is not None else 'No_Pair')

# 颜色
type_list = list(sorted(all_types_set)) + ['No_Pair']
type_to_code = {tp: i for i, tp in enumerate(type_list)}
default_colors = plt.get_cmap('tab10')(np.arange(len(type_list)-1))
colors = np.vstack([default_colors, [[1,1,1,1]]])  # 'No_Pair'为白色

code_array = [type_to_code[tp] for tp in type_per_frame]
plt.figure(figsize=(12, 1.3))
color_map_arr = np.array([colors[c] for c in code_array])
plt.imshow([color_map_arr], aspect='auto', interpolation='nearest')

plt.yticks([])
plt.xlabel('Frame')
plt.title(f'Base Pair Type Progress Bar for {pair}')

import matplotlib.patches as mpatches
legend_handles = [mpatches.Patch(facecolor=colors[i], label=tp, edgecolor='black') for i, tp in enumerate(type_list)]
plt.legend(handles=legend_handles, bbox_to_anchor=(1.01, 0.5), loc='center left', fontsize=10, frameon=True)

plt.tight_layout()
plt.savefig("hbonds_bp_diff_types_with_frame_col_60_3.3.png", bbox_inches='tight')
plt.show()
