import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import uniform_filter1d

def read_xvg(filename):
    time, y = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.split()
            # 跳过ntv
            if float(parts[0]) < 3000.0000000:
                continue
            time.append(float(parts[0]) - 3000.0000000)
            # time.append(float(parts[0]))
            y.append(float(parts[1]))
    return np.array(time), np.array(y)

files = [
    ('rmsd_360k.xvg', '360K'),
    ('rmsd_300k.xvg', '300K'),
]

all_rmsd = []
for file, label in files:
    time, rmsd = read_xvg(file)
    avg = uniform_filter1d(rmsd[:], size=100)[::10]  # 平滑后每10帧采样
    all_rmsd.append(avg)

# 对齐长度
minlen = min(len(x) for x in all_rmsd)
all_rmsd = np.array([x[:minlen] for x in all_rmsd])


# 扩展渐变范围：深红 → 红 → 橙 → 黄 → 浅黄
colors_custom = ["#b30000", "#f57c6e", "#f2656f", "#fae69e", "#fff7c2"]
colors_custom = list(reversed(colors_custom))
cmap_custom = LinearSegmentedColormap.from_list("wide_red_orange_yellow", colors_custom)

plt.figure(figsize=(10,4))
sns.heatmap(
    all_rmsd,
    cmap=cmap_custom,
    vmin=all_rmsd.min(),  # 拉满低值到最浅色
    vmax=all_rmsd.max(),  # 拉满高值到最深色
    yticklabels=[l for _, l in files],
    cbar_kws={"label": "RMSD (nm)"}
)

plt.xlabel('Time Window')
plt.ylabel('Temperature (K)')
plt.title('Root-Mean-Square Deviation at 300K & 360K')
plt.tight_layout()
plt.savefig('../img/2_2_2_rmsd_two_heat_map.svg', dpi=300)
plt.show()
