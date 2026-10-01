import matplotlib.pyplot as plt
import numpy as np


def normalize_input(s):
    # 支持 C/27 或 C_27_0，都能转成C_27_0
    s = s.strip().replace('/', '_')
    if not s.endswith('_0'):
        s = s + '_0'
    return s

file = 'full_trajectory_pair_comma.csv'

# 输入两个碱基
base1 = input("第一个碱基（如C/27）：").strip()
base2 = input("第二个碱基（如G/43）：").strip()
base1 = normalize_input(base1)
base2 = normalize_input(base2)
pair = tuple(sorted([base1, base2]))  # 自动排序，方便统一

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

# 检查输入的两个碱基顺序在数据中分别是否存在
has_forward = False  # (base1, base2)
has_reverse = False  # (base2, base1)
forward_types = set()
reverse_types = set()

for frame in frame_data:
    for res1, res2, type_ in frame:
        if (res1 == base1 and res2 == base2):
            has_forward = True
            forward_types.add(type_)
        if (res1 == base2 and res2 == base1):
            has_reverse = True
            reverse_types.add(type_)

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

all_types = set()
type_per_frame = []
for frame in frame_data:
    found_type = None
    for res1, res2, type_ in frame:
        p = tuple(sorted([res1, res2]))
        if p == pair:
            found_type = type_
            all_types.add(type_)
            break
    # 无配对情况标记为 'no_pair'
    type_per_frame.append(found_type if found_type is not None else 'No_Pair')

# 确保 'no_pair' 在最后
type_list = list(sorted(all_types)) + ['No_Pair']
type_to_code = {tp: i for i, tp in enumerate(type_list)}

# 颜色数组，最后一个为白色
default_colors = plt.get_cmap('tab10')(np.arange(len(type_list)-1))
colors = np.vstack([default_colors, [[1,1,1,1]]])  # 'no_pair'为白色

# 编码
code_array = [type_to_code[tp] for tp in type_per_frame]

plt.figure(figsize=(12, 1.3))
color_map_arr = np.array([colors[c] for c in code_array])
plt.imshow([color_map_arr], aspect='auto', interpolation='nearest')

plt.yticks([])
plt.xlabel('Frame')
plt.title(f'Base Pair Type Progress Bar for {pair}')

# 图例
import matplotlib.patches as mpatches
legend_handles = [mpatches.Patch(facecolor=colors[i], label=tp, edgecolor='black') for i, tp in enumerate(type_list)]
plt.legend(handles=legend_handles, bbox_to_anchor=(1.01, 0.5), loc='center left', fontsize=10, frameon=True)

plt.tight_layout()
plt.savefig("hbonds_bp_diff_types.png", bbox_inches='tight')
plt.show()
