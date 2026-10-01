import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from matplotlib.patches import Patch
import matplotlib as mpl

# ===== 全局字体加粗加大设置 =====
# mpl.rcParams['svg.fonttype'] = 'none'    # 保留文字为文字
# mpl.rcParams['pdf.fonttype'] = 42        # PDF 用 TrueType
# mpl.rcParams['font.size'] = 14           # 全局字体大小
# mpl.rcParams['font.weight'] = 'bold'     # 全局加粗
# mpl.rcParams['axes.labelweight'] = 'bold'
# mpl.rcParams['axes.titleweight'] = 'bold'
# mpl.rcParams['legend.fontsize'] = 14
# mpl.rcParams['legend.title_fontsize'] = 14

# 配色
COLOR_MAP = {
    "WCc": "#71b7ed",
    "WWc": "#f2656f",
    "No_Pair": "white",
    "Other": "#fae69e"
}
PLOT_ORDER = ["WCc", "WWc", "Other", "No_Pair"]

def read_bp_file(file_path):
    bp_dict = {}
    current_frame = -1
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                if line.startswith("# Frame"):
                    current_frame += 1
                continue
            parts = [x.strip() for x in line.replace(",", " ").split()]
            if len(parts) != 3:
                continue
            bp1, bp2, bp_type = parts
            bp_pair = tuple((bp1, bp2))
            if bp_pair not in bp_dict:
                bp_dict[bp_pair] = {}
            bp_dict[bp_pair][current_frame] = bp_type

    wcc_bps = {bp for bp, frames in bp_dict.items() if any(tp == "WCc" for tp in frames.values())}
    max_frame = max(max(frames.keys()) for frames in bp_dict.values()) if bp_dict else 0

    bp_series = {}
    for bp_pair in sorted(bp_dict.keys()):
        if bp_pair in wcc_bps:
            series = []
            for f in range(max_frame + 1):
                tp = bp_dict[bp_pair].get(f, "No_Pair")
                if tp not in ("WCc", "WWc", "No_Pair"):
                    tp = "Other"
                series.append(tp)
            bp_series[bp_pair] = series
    return bp_series, max_frame + 1

def calc_wcc_percent(bp_series):
    return {bp: np.sum(np.array(series) == "WCc") / len(series) * 100
            for bp, series in bp_series.items()}

def draw_progress_matrix(bp_series, bp_order, wcc_percents, ax, title,
                         percent_side="left", show_legend=False, total_time_ps=1e6):
    n_bp = len(bp_order)
    n_frame = len(next(iter(bp_series.values()))) if n_bp > 0 else 0

    rgb_matrix = np.zeros((n_bp, n_frame, 3))
    for i, bp in enumerate(bp_order):
        for j, tp in enumerate(bp_series[bp]):
            rgb_matrix[i, j, :] = to_rgb(COLOR_MAP[tp])

    ax.imshow(rgb_matrix, aspect="auto", interpolation="nearest", origin="upper")

    # y 轴碱基对
    ax.set_yticks(np.arange(n_bp))
    ax.set_yticklabels([])
    ax.set_title(title)

    # 水平分隔线
    for y in range(1, n_bp):
        ax.axhline(y - 0.5, color="black", lw=1, alpha=0.28, linestyle='-')

    # ===== X轴映射到时间 =====
    time_vals = np.linspace(0, total_time_ps, n_frame)
    xtick_locs = np.linspace(0, n_frame - 1, 6, dtype=int)  # 6个刻度
    ax.set_xticks(xtick_locs)
    ax.set_xticklabels([f"{time_vals[i]/1e3:.0f}" for i in xtick_locs])  # 单位 ns
    ax.set_xlabel("Time (μs)")

    if show_legend:
        used_types = [tp for tp in PLOT_ORDER if any(tp in series for series in bp_series.values())]
        handles = [Patch(facecolor=COLOR_MAP[tp], edgecolor="black", linewidth=1.1, label=tp) for tp in used_types]
        ax.legend(handles=handles, bbox_to_anchor=(1.02, 1), loc="best",
                  title="Pair Type", frameon=True)

    # 外侧百分比
    xmin, xmax = ax.get_xlim()
    span = xmax - xmin
    if percent_side == "left":
        x_pos = xmin - 0.02 * span
        ha = "right"
    else:
        x_pos = xmax + 0.02 * span
        ha = "left"

    for i, bp in enumerate(bp_order):
        # ax.text(x_pos, i, f"{wcc_percents[bp]:5.2f}%",
        #         va='center', ha=ha, fontsize=14, fontweight='bold', color="black", clip_on=False)
        ax.text(x_pos, i, f"{wcc_percents[bp]:5.2f}%",
                va='center', ha=ha, fontsize=14, color="black", clip_on=False)


def main_ok():
    file_path1 = "pairing_basepair_annotate_300k_comma.csv"
    file_path2 = "pairing_basepair_annotate_360k_comma.csv"
    bp_series1, _ = read_bp_file(file_path1)
    bp_series2, _ = read_bp_file(file_path2)

    wcc_1 = calc_wcc_percent(bp_series1)
    wcc_2 = calc_wcc_percent(bp_series2)

    original_order = list(bp_series1.keys())
    common_bps = set(wcc_1.keys()) & set(wcc_2.keys())

    top15_1 = sorted(common_bps, key=lambda bp: wcc_1[bp], reverse=True)[:15]
    top15_2 = sorted(common_bps, key=lambda bp: wcc_2[bp], reverse=True)[:15]
    selected_set = set(top15_1) | set(top15_2)

    selected_bps = sorted(
        [bp for bp in original_order if bp in selected_set],
        key=lambda bp: abs(wcc_1[bp] - wcc_2[bp]),
        reverse=True
    )

    # 三列布局
    fig = plt.figure(figsize=(28, 13), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.25, 1.0])

    ax_left = fig.add_subplot(gs[0, 0])  # 左图
    ax_mid = fig.add_subplot(gs[0, 1])  # 中间列，不共享 y！
    ax_right = fig.add_subplot(gs[0, 2], sharey=ax_left)  # 右图共享左图的 y

    # 只各画一次
    draw_progress_matrix(bp_series1, selected_bps, wcc_1,
                         ax=ax_left, title="300K",
                         percent_side="left", show_legend=False)
    draw_progress_matrix(bp_series2, selected_bps, wcc_2,
                         ax=ax_right, title="360K",
                         percent_side="right", show_legend=True)

    # 中间列放碱基对名称
    ax_mid.set_xlim(0, 1)
    ax_mid.set_xticks([])
    ax_mid.set_frame_on(False)

    # 对齐 y 范围到左图，然后设置刻度与标签
    ax_mid.set_ylim(ax_left.get_ylim())
    ax_mid.set_yticks(np.arange(len(selected_bps)))
    # ax_mid.set_yticklabels([f"{bp[0][:-2]} → {bp[1][:-2]}" for bp in selected_bps],
    #                        fontsize=14, fontweight='bold')
    ax_mid.set_yticklabels([f"{bp[0][:-2]} → {bp[1][:-2]}" for bp in selected_bps],
                           fontsize=14)
    ax_mid.tick_params(axis='y', which='both', length=0)  # 去掉刻度线
    # ax_mid.set_title("Base Pair", pad=10, fontweight='bold', fontsize=16)
    ax_mid.set_title("Base Pair", pad=10, fontsize=16)


    # 左右图不显示 y 轴标签（防重复）
    ax_left.set_yticklabels([])
    ax_right.set_yticklabels([])
    #
    # fig.suptitle("WCc Base Pair Progression (Time 0–1e6 ps)",
    #              fontsize=20, fontweight='bold', y=0.98)
    fig.suptitle("WCc Base Pair Progression (Time 0–1e6 ps)",
                 fontsize=20, y=0.98)
    plt.show()


def main():
    # ===== 读数据 =====
    file_path1 = "pairing_basepair_annotate_300k_comma.csv"
    file_path2 = "pairing_basepair_annotate_360k_comma.csv"
    bp_series1, _ = read_bp_file(file_path1)
    bp_series2, _ = read_bp_file(file_path2)

    # ===== 计算 WCc 百分比 =====
    wcc_1 = calc_wcc_percent(bp_series1)
    wcc_2 = calc_wcc_percent(bp_series2)

    # ===== 选择要展示的 bp（两个温度各自 Top15 的并集，按差异度降序）=====
    original_order = list(bp_series1.keys())
    common_bps = set(wcc_1.keys()) & set(wcc_2.keys())
    top15_1 = sorted(common_bps, key=lambda bp: wcc_1[bp], reverse=True)[:15]
    top15_2 = sorted(common_bps, key=lambda bp: wcc_2[bp], reverse=True)[:15]
    selected_set = set(top15_1) | set(top15_2)
    selected_bps = sorted(
        [bp for bp in original_order if bp in selected_set],
        key=lambda bp: abs(wcc_1[bp] - wcc_2[bp]),
        reverse=True
    )

    # ===== 三列布局 =====
    fig = plt.figure(figsize=(28, 13), constrained_layout=True)
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.25, 1.0])

    ax_left  = fig.add_subplot(gs[0, 0])                 # 左图
    ax_mid   = fig.add_subplot(gs[0, 1])                 # 中间列（不 sharey）
    ax_right = fig.add_subplot(gs[0, 2], sharey=ax_left) # 右图 sharey 左图

    # ===== 绘制左右热图（各一次）=====
    draw_progress_matrix(bp_series1, selected_bps, wcc_1,
                         ax=ax_left, title="300K",
                         percent_side="left", show_legend=False, total_time_ps=1e6)
    draw_progress_matrix(bp_series2, selected_bps, wcc_2,
                         ax=ax_right, title="360K",
                         percent_side="right", show_legend=True, total_time_ps=1e6)

    # ===== 中间列：只显示一列碱基对名称，并与左右像素格心对齐 =====
    ax_mid.set_xlim(0, 1)
    ax_mid.set_xticks([])
    ax_mid.set_frame_on(False)
    # 用左图的 y 边界，保证格心一致
    ax_mid.set_ylim(ax_left.get_ylim())
    y_pos = np.arange(len(selected_bps))  # 与 imshow 的格心一致：0,1,2,...
    ax_mid.set_yticks(y_pos)
    # ax_mid.set_yticklabels([f"{bp[0][:-2]} → {bp[1][:-2]}" for bp in selected_bps],
    #                        fontsize=14, fontweight='bold')
    ax_mid.set_yticklabels([f"{bp[0][:-2]} → {bp[1][:-2]}" for bp in selected_bps],
                           fontsize=14)
    ax_mid.tick_params(axis='y', which='both', length=0)
    # ax_mid.set_title("Base Pair", pad=10, fontweight='bold', fontsize=16)
    ax_mid.set_title("Base Pair", pad=10, fontsize=16)

    # 左右图不显示 y 轴标签（避免重复）
    ax_left.set_yticklabels([])
    ax_right.set_yticklabels([])

    # ===== 在两侧百分比列上方加列标题 “WCc %” =====
    # 左侧
    xmin_l, xmax_l = ax_left.get_xlim()
    span_l = xmax_l - xmin_l
    x_left_col = xmin_l - 0.02 * span_l
    # ax_left.text(x_left_col, -1.2, "WCc %",
    #              ha="right", va="center", fontsize=14, fontweight="bold",
    #              color="black", clip_on=False)
    ax_left.text(x_left_col, -1.2, "WCc %",
                 ha="right", va="center", fontsize=14,
                 color="black", clip_on=False)
    # 右侧
    xmin_r, xmax_r = ax_right.get_xlim()
    span_r = xmax_r - xmin_r
    x_right_col = xmax_r + 0.02 * span_r
    # ax_right.text(x_right_col, -1.2, "WCc %",
    #               ha="left", va="center", fontsize=14, fontweight="bold",
    #               color="black", clip_on=False)

    ax_right.text(x_right_col, -1.2, "WCc %",
                  ha="left", va="center", fontsize=14,
                  color="black", clip_on=False)

    # ===== 总标题 =====
    # fig.suptitle("WCc Base Pair Progression at 300K & 360K: Top 15 ΔWCc%",
    #              fontsize=20, fontweight='bold', y=0.98)
    fig.suptitle("WCc Base Pair Progression at 300K & 360K: Top 15 ΔWCc%",
                 fontsize=20, y=0.98)

    # 保存或展示
    plt.savefig("../img/4_3_hbonds_Wcc_details_merged_top15.svg",
                format="svg", bbox_inches="tight")
    plt.show()



if __name__ == "__main__":
    main()
