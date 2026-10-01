import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as mpatches

# 读目标配对表
targets = "hbonds_one_type.csv"
targets_df = pd.read_csv(targets, header=None)

# 读全轨迹配对帧文件
file = "pairings_30_3.5.csv"
df = pd.read_csv(file)

# 检查输出文件夹
outdir = "img2"
os.makedirs(outdir, exist_ok=True)

# 批量遍历所有配对
for row in targets_df.itertuples():
    pair_str = row[1]
    # tuple字符串变成两个碱基
    pair_original = pair_str.strip("()").replace("'", "")
    base1, base2 = [x.strip() for x in pair_original.split(",")]

    # 所有帧编号
    frames = df['frame'].unique()
    frames.sort()

    # 收集该pair在每一帧的配对类型
    type_per_frame = []
    all_types = set()

    # 构造映射表以加速查找
    df_pair = df[((df['base_i'] == base1) & (df['base_j'] == base2)) |
                 ((df['base_i'] == base2) & (df['base_j'] == base1))]
    # 每帧的配对类型（可能为空）
    frame_type_dict = dict(zip(zip(df_pair['frame'], df_pair['base_i'], df_pair['base_j']), df_pair['pair_type']))

    for frame in frames:
        # 查找两种方向
        tp1 = df_pair[(df_pair['frame'] == frame) & (df_pair['base_i'] == base1) & (df_pair['base_j'] == base2)]
        tp2 = df_pair[(df_pair['frame'] == frame) & (df_pair['base_i'] == base2) & (df_pair['base_j'] == base1)]
        found_type = None
        if not tp1.empty:
            found_type = tp1.iloc[0]['pair_type']
        elif not tp2.empty:
            found_type = tp2.iloc[0]['pair_type']
        if found_type is not None:
            all_types.add(found_type)
            type_per_frame.append(found_type)
        else:
            type_per_frame.append('No_Pair')

    # 画进度条
    type_list = sorted(all_types) + ['No_Pair']
    type_to_code = {tp: i for i, tp in enumerate(type_list)}
    default_colors = plt.get_cmap('tab10')(np.arange(len(type_list)-1))
    colors = np.vstack([default_colors, [[1,1,1,1]]])  # 'No_Pair'为白色
    code_array = [type_to_code[tp] for tp in type_per_frame]

    plt.figure(figsize=(12, 1.3))
    color_map_arr = np.array([colors[c] for c in code_array])
    plt.imshow([color_map_arr], aspect='auto', interpolation='nearest')
    plt.yticks([])
    plt.xlabel('Frame')
    plt.title(f'Base Pair Type Progress Bar for {base1} + {base2}')
    legend_handles = [mpatches.Patch(facecolor=colors[i], label=tp, edgecolor='black') for i, tp in enumerate(type_list)]
    plt.legend(handles=legend_handles, bbox_to_anchor=(1.01, 0.5), loc='center left', fontsize=10, frameon=True)
    plt.tight_layout()
    plt.savefig(f"{outdir}/{base1}_{base2}.png", bbox_inches='tight')
    plt.close()
    print(f"已输出：{outdir}/{base1}_{base2}.png")

print("全部pair的进度条图已批量输出。")
