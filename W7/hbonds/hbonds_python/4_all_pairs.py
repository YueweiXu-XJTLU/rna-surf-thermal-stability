import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
import os

# 固定配色方案
type_colors = {
    'WCc':  '#1f77b4',
    'WWc':  '#2ca02c',
    'WWt':  '#d62728',
    'GUc':  '#ff7f0e',
    'HHc':  '#9467bd',
    'HHt':  '#8c564b',
    'HSc':  '#e377c2',
    'HSt':  '#7f7f7f',
    'HWc':  '#bcbd22',
    'HWt':  '#17becf',
    'SHc':  '#aec7e8',
    'SHt':  '#ffbb78',
    'SSc':  '#c5b0d5',
    'SSt':  '#c49c94',
    'SWc':  '#f7b6d2',
    'SWt':  '#c7c7c7',
    'WHc':  '#dbdb8d',
    'WHt':  '#9edae5',
    'WSc':  '#393b79',
    'WSt':  '#ff9896',
    'XXX':  '#b0b0b0',      # 杂类灰色
    'No_Pair': '#ffffff',   # 未配对白色
}

# 输出文件夹
outdir = "img"
os.makedirs(outdir, exist_ok=True)

# 目标配对表和全轨迹pair表
targets = "hbonds_one_type.csv"
file = "full_trajectory_pair_comma.csv"

targets_df = pd.read_csv(targets)

for row in targets_df.itertuples():
    pair_original = row[1]
    pair_original = pair_original.strip("()").replace("'", "")
    pair = tuple([x.strip() for x in pair_original.split(",")])
    base1 = pair[0]
    base2 = pair[1]

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

    # 检查两个顺序
    has_forward = False
    has_reverse = False
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
        all_types = forward_types | reverse_types
    elif has_forward:
        print(f"仅检测到 {base1} → {base2} 顺序，配对类型: {sorted(forward_types)}")
        all_types = forward_types
    elif has_reverse:
        print(f"仅检测到 {base2} → {base1} 顺序，配对类型: {sorted(reverse_types)}")
        all_types = reverse_types
    else:
        print("未检测到这对碱基有任何直接配对，后续统计为空。")
        all_types = set()

    # 统计每帧配对类型
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
        # 无配对情况标记为 'No_Pair'
        type_per_frame.append(found_type if found_type is not None else 'No_Pair')

    # 确保 'No_Pair' 在最后
    type_list = list(sorted(all_types))
    if 'XXX' in type_list:  # 保证XXX在No_Pair前
        type_list.remove('XXX')
        type_list.append('XXX')
    type_list.append('No_Pair')

    type_to_code = {tp: i for i, tp in enumerate(type_list)}

    # 颜色数组（与type_list顺序一致）
    colors = [mcolors.to_rgba(type_colors.get(tp, '#ffffff')) for tp in type_list]
    code_array = [type_to_code[tp] for tp in type_per_frame]
    color_map_arr = np.array([colors[c] for c in code_array])

    # 画进度条
    plt.figure(figsize=(12, 1.3))
    plt.imshow([color_map_arr], aspect='auto', interpolation='nearest')
    plt.yticks([])
    plt.xlabel('Frame')
    plt.title(f'Base Pair Type Progress Bar for {pair}')

    # 图例
    legend_handles = [mpatches.Patch(facecolor=colors[i], label=tp, edgecolor='black') for i, tp in enumerate(type_list)]
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.01, 0.5), loc='center left', fontsize=10, frameon=True)
    plt.tight_layout()
    plt.savefig(f"{outdir}/{base1}_{base2}.png", bbox_inches='tight', dpi=200)
    plt.close()
