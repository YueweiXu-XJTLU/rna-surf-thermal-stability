# -*- coding: utf-8 -*-
"""
从 0.6 μs 开始，直接 Welch t 检验 → 可视化
配色：
- 300K 小提琴 & 右图（Δ+CI）：#71b7ed
- 360K 小提琴：#f2656f
- 组均值点：#fae69e
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# ========= 配置 =========
file300 = "pairing_basepair_annotate_300k_comma.csv"
file360 = "pairing_basepair_annotate_360k_comma.csv"
dt_step_ps = 0.002          # 积分步长（ps）= 2 fs
nsteps = 500_000_000        # 总步数（例：5e8）
t_start_ps = 600_000        # 只用 0.6 μs（600000 ps）之后
OUT_FIG = None              # 如需保存：Path("wcc_ttest_blocks10_python.pdf")

# 颜色
COLORS = {
    "k300": "#71b7ed",
    "k360": "#f2656f",
    "mean": "#fae69e",
    "normal": "#b8aeeb"
}

# ========= 工具函数 =========
def read_wcc_counts(path, target="WCc"):
    counts = []
    cur = None
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            if s.startswith("# Frame"):
                if cur is not None:
                    counts.append(cur)
                cur = 0
                continue
            parts = s.replace(",", " ").split()
            if len(parts) >= 3 and parts[-1] == target:
                cur += 1
    if cur is not None:
        counts.append(cur)
    return np.asarray(counts, dtype=float)

def welch_t_ci(arr1, arr2, alpha=0.05):
    mx, my = arr1.mean(), arr2.mean()
    vx, vy = arr1.var(ddof=1), arr2.var(ddof=1)
    nx, ny = len(arr1), len(arr2)
    se = np.sqrt(vx / nx + vy / ny)
    t_stat = (mx - my) / se
    df = (vx / nx + vy / ny) ** 2 / ((vx**2) / (nx**2 * (nx - 1)) + (vy**2) / (ny**2 * (ny - 1)))
    p = 2 * stats.t.sf(abs(t_stat), df)
    tcrit = stats.t.ppf(1 - alpha / 2, df)
    ci = ((mx - my) - tcrit * se, (mx - my) + tcrit * se)
    return (mx, my), (nx, ny), t_stat, df, p, ci, (vx, vy)

# ========= 主流程 =========
x_all = read_wcc_counts(file300)   # 300K 每帧 WCc
y_all = read_wcc_counts(file360)   # 360K 每帧 WCc
n_frames = min(len(x_all), len(y_all))
x_all, y_all = x_all[:n_frames], y_all[:n_frames]

total_ps = dt_step_ps * nsteps
dt_ps = total_ps / (n_frames - 1)
time_ps = np.arange(n_frames) * dt_ps

# 截取 0.6 μs 之后
mask = time_ps >= t_start_ps
x = x_all[mask]
y = y_all[mask]

# Welch t 检验
(means_x, means_y), (nx, ny), t_stat, df, pval, ci, (var_x, var_y) = welch_t_ci(x, y)
delta = (means_x - means_y)

print(f"Frames total: {n_frames}  dt_ps ≈ {dt_ps:.1f} ps")
print(f"Using t >= {t_start_ps} ps; frames kept: {len(x)}")
print(f"Mean(300K)={means_x:.3f}, Mean(360K)={means_y:.3f}")
print(f"Δ (300-360) = {delta:.3f}")
print(f"Welch t={t_stat:.2f}, df≈{df:.1f}, p={pval:.2e}")
print(f"95% CI for Δ: [{ci[0]:.3f}, {ci[1]:.3f}]")

# ========= 可视化 =========
fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.4))

# 左：两组分布
data = [x, y]
vparts = axes[0].violinplot(data, showmeans=False, showextrema=False, widths=0.9)
for i, body in enumerate(vparts['bodies']):
    body.set_facecolor(COLORS["k300"] if i == 0 else COLORS["k360"])
    body.set_alpha(0.25)
    body.set_edgecolor('none')

# 抖动散点
rng = np.random.default_rng(0)
for i, vals in enumerate(data, start=1):
    axes[0].scatter(np.full(len(vals), i) + rng.uniform(-0.08, 0.08, size=len(vals)),
                    vals, s=14, alpha=0.55, color=COLORS["normal"])

# 组均值点
axes[0].scatter([1, 2], [means_x, means_y], s=60, color=COLORS["mean"],
                edgecolor="grey", linewidth=0.4, zorder=3)

axes[0].set_title("WCc Distributions", fontsize=11)
axes[0].set_xticks([1, 2])
axes[0].set_xticklabels([
    f"300K \n Mean={means_x:.2f}±{var_x:.2f}",
    f"360K \n Mean={means_y:.2f}±{var_y:.2f}"
])
axes[0].set_ylabel("WCc Base Pairs")

# 右：均值差 + CI
axes[1].axhline(0, linestyle="--", color="black", linewidth=1)
yerr = np.array([[delta - ci[0]], [ci[1] - delta]])
axes[1].errorbar([1], [delta], yerr=yerr, fmt="o", capsize=6,
                 color=COLORS["k300"], ecolor=COLORS["k300"], elinewidth=2, markersize=6)
axes[1].set_title("Mean Difference", fontsize=11)
axes[1].set_xticks([1])
axes[1].set_xticklabels([
    f"Δ(300K−360K) \n Δ={delta:.2f}, 95% CI=[{ci[0]:.2f}, {ci[1]:.2f}]"
])
axes[1].set_ylabel("Mean Difference (95% CI)")

fig.suptitle(
    f"WCc Base Pair Distributions at 300K & 360K (0.6µs - 1.0µs)",
    fontsize=10, y=0.98
)

for ax in axes:
    ax.grid(True, linestyle='-', alpha=0.5)

plt.savefig("P_Value.svg", dpi=600)
plt.show()
