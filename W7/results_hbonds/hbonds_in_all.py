import matplotlib.pyplot as plt
import numpy as np
import os

# --------- 1. 配对类型与颜色映射 ---------
COLOR_MAP = {
    "No_Pair": "white",
    "XXX": "#7f7f7f",
    "WCc": "#1f77b4",
    "WWc": "#d62728",
    "WWt": "#ff7f0e",
    # "SHt": "#425643",
    # "SHc": "#2d3a65",
    "WSc": "#e377c2",
    # "SSt": "#b9e900",
    "HWt": "#9467bd",
    # "HHc": "#02f363",
    # "WHc": "#73ef2f",
    # "SWt": "#d41fcc",
    # "GUc": "#e0856e",
    # "SSc": "#a37deb",
    # "HSt": "#1c030b",
    # "HHt": "#6a7210",
    # "WSt": "#80214d",
    "SWc": "#8c564b",
    # "WHt": "#cafae8",
    "HSc": "#2ca02c",
    # "HWc": "#cbcc94",
}

# --------- 2. 读取pairing.out格式文件，获得所有bp的全帧类型序列 ---------
def read_bp_file(file_path):
    """
    读取pairing.out格式的配对信息文件，返回每对bp全帧的配对类型序列
    返回：bp_series: {bp_pair: [type1, type2, ...]}
    """
    bp_dict = {}
    current_frame = -1
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("# Frame"):
                current_frame += 1
                continue
            parts = line.split()
            if len(parts) != 3:
                continue
            bp1, bp2, bp_type = parts
            bp_pair = tuple(sorted((bp1, bp2)))
            if bp_pair not in bp_dict:
                bp_dict[bp_pair] = {}
            bp_dict[bp_pair][current_frame] = bp_type

    # 找到所有出现过WCc的bp，只保留这些bp
    wcc_bps = {bp for bp, frames in bp_dict.items() if any(tp == "WCc" for tp in frames.values())}
    max_frame = max(max(frames.keys()) for frames in bp_dict.values())

    bp_series = {}
    for bp_pair in sorted(bp_dict.keys()):
        if bp_pair in wcc_bps:
            series = []
            for f in range(max_frame + 1):
                series.append(bp_dict[bp_pair].get(f, "No_Pair"))
            bp_series[bp_pair] = series
    return bp_series, max_frame + 1

# --------- 3. 拼接所有bp的配对序列，绘制总览进度条大图 ---------
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb

def draw_progress_matrix(bp_series, output_img="all_progress.png"):
    """
    绘制所有bp的全帧配对类型拼接热图（总览图），每两条bp之间加横线
    """
    bp_list = list(bp_series.keys())
    n_bp = len(bp_list)
    n_frame = len(next(iter(bp_series.values())))

    # 构建RGB三维矩阵 (n_bp, n_frame, 3)
    rgb_matrix = np.zeros((n_bp, n_frame, 3))
    for i, bp in enumerate(bp_list):
        for j, tp in enumerate(bp_series[bp]):
            rgb_matrix[i, j, :] = to_rgb(COLOR_MAP.get(tp, "grey"))

    fig, ax = plt.subplots(figsize=(max(10, n_frame/40), n_bp/2))
    ax.imshow(rgb_matrix, aspect="auto", interpolation="nearest")

    # Y轴：bp名称
    ax.set_yticks(np.arange(n_bp))
    ax.set_yticklabels([f"{bp[0]}-{bp[1]}" for bp in bp_list], fontsize=8)
    ax.set_xlabel("Frame", fontsize=12)
    ax.set_ylabel("Base Pair", fontsize=12)
    ax.set_title("Base Pair Type Progress Overview", fontsize=14)

    # 每条之间加横线（注意只加bp之间，不包括最上/最下）
    for y in range(1, n_bp):
        ax.axhline(y-0.5, color="black", lw=1, alpha=0.3, linestyle='-')

    # 图例（只显示实际用到的类型）
    from matplotlib.patches import Patch
    used_types = sorted(set(tp for series in bp_series.values() for tp in series))
    handles = [Patch(color=COLOR_MAP.get(tp, "grey"), label=tp) for tp in used_types]
    ax.legend(handles=handles, bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=8)

    plt.tight_layout()
    plt.savefig(output_img, dpi=300)
    plt.close()
    print(f"success: {output_img}")


# --------- 4. 主函数入口 ---------
def main():
    # 修改为你的配对文件路径
    file_path = "basepair_annotate_pairing_300k.csv"
    bp_series, total_frames = read_bp_file(file_path)
    print(f"共检测到 {len(bp_series)} 对碱基对，每个轨迹 {total_frames} 帧。")
    draw_progress_matrix(bp_series, "all_progress_plots.png")

if __name__ == "__main__":
    main()
