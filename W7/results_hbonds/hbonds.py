import pandas as pd
import matplotlib.pyplot as plt
import os

# 固定颜色映射
COLOR_MAP = {
    "No_Pair": "white",
    "WCc": "green",
    "WWc": "red",
    "WWt": "gold",
    "SHt": "#425643",
    "SHc": "#2d3a65",
    "WSc": "#03f700",
    "SSt": "#b9e900",
    "HWt": "#6c87da",
    "HHc": "#02f363",
    "WHc": "#73ef2f",
    "SWt": "#d41fcc",
    "GUc": "#e0856e",
    "SSc": "#a37deb",
    "HSt": "#1c030b",
    "HHt": "#6a7210",
    "WSt": "#80214d",
    "XXX": "#d78306",
    "SWc": "#be1fe3",
    "WHt": "#cafae8",
    "HSc": "#f051cb",
    "HWc": "#cbcc94",
}

def read_bp_file(file_path):
    """
    从 .pairing.out 文件中读取所有帧的碱基对信息
    返回: {bp_pair: [type per frame]}
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

    # 转换成每帧的序列（原来是“只保留第 0 帧存在的 bp”）
    # ---------- 修改开始 ----------
    max_frame = max(max(frames.keys()) for frames in bp_dict.values())
    # 改成：只保留在任意帧出现过 WCc 的 bp
    wcc_bps = {bp for bp, frames in bp_dict.items() if any(bp_type == "WCc" for bp_type in frames.values())}

    bp_series = {}
    for bp_pair, frames in bp_dict.items():
        if bp_pair in wcc_bps:  # 只保留在任意帧出现过 WCc 的 bp
            series = []
            for f in range(max_frame + 1):
                series.append(frames.get(f, "No_Pair"))
            bp_series[bp_pair] = series
    # ---------- 修改结束 ----------

    # 打印第一帧的碱基对数量（可选，调试用）
    frame0_bps = [bp for bp, frames in bp_dict.items() if 0 in frames]
    print(f"Frame 0 碱基对数量: {len(frame0_bps)}")
    return bp_series, max_frame + 1

def plot_bp_progress(bp_series, output_dir):
    """
    绘制每一对 bp 的进度条图
    """
    os.makedirs(output_dir, exist_ok=True)

    for bp_pair, series in bp_series.items():
        fig, ax = plt.subplots(figsize=(10, 1.5))

        for frame_idx, bp_type in enumerate(series):
            color = COLOR_MAP.get(bp_type, "grey")
            ax.axvspan(frame_idx, frame_idx + 1, color=color)

        ax.set_xlim(0, len(series))
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.set_xlabel("Frame")
        ax.set_title(f"Base Pair Type Progress Bar for {bp_pair}")

        # 图例（原来是全部类型，现在只显示当前图用到的类型）
        # ---------- 修改开始 ----------
        used_types = []
        for bp_type in series:
            if bp_type not in used_types:
                used_types.append(bp_type)

        handles = [plt.Line2D([0], [0], color=COLOR_MAP.get(bp_type, "grey"), lw=4, label=bp_type)
                   for bp_type in used_types]
        ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')
        # ---------- 修改结束 ----------

        output_path = os.path.join(output_dir, f"{bp_pair[0]}_{bp_pair[1]}.png")
        plt.tight_layout()
        plt.savefig(output_path, dpi=300)
        plt.close()

def main():
    # 修改为你的 iCloud 路径
    file_path = "basepair_annotate_pairing_300k.csv"
    output_dir = "bp_progress_plots"

    bp_series, total_frames = read_bp_file(file_path)
    print(f"共检测到 {len(bp_series)} 对碱基对，每个轨迹 {total_frames} 帧。")
    plot_bp_progress(bp_series, output_dir)
    print(f"所有图片已保存到: {output_dir}")

if __name__ == "__main__":
    main()