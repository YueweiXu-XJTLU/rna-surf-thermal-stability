import numpy as np
import matplotlib.pyplot as plt

temps = [300, 360]
colors = ["#71b7ed", "#f2656f"]

fig, ax = plt.subplots(figsize=(8, 5))

for idx, (T, c) in enumerate(zip(temps, colors)):
    data_draft = np.loadtxt(f'rg_{T}K.xvg', comments=['#', '@'])
    data = data_draft[data_draft[:, 0] >= 1000]
    time = data[:, 0]
    Rg_total = data[:, 1]

    # 全局均值和标准差
    mean_total, std_total = np.mean(Rg_total), np.std(Rg_total)

    # 主曲线
    ax.plot(time, Rg_total, color=c, linewidth=1.2,
            label=f'{T}K (Mean={mean_total:.2f}±{std_total:.2f} nm)')

    # 均值虚线
    ax.axhline(mean_total, color=c, linestyle='--', linewidth=1.0, alpha=0.5)

    # 每个点 ± 全局 std 阴影
    ax.fill_between(time,
                    Rg_total - std_total,
                    Rg_total + std_total,
                    color=c, alpha=0.15)

ax.set_xlabel('Time (μs)')
ax.set_ylabel('Rg (nm)')
ax.set_title('Radius of Gyration at 300K & 360K')
ax.legend(loc='best', fontsize='small', frameon=True)
plt.tight_layout()
plt.grid(alpha=0.5, color='gray', linestyle='-')
plt.savefig('../img/3_2_1_rg_two_line.svg', dpi=300)
plt.show()
