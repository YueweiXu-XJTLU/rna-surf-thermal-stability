import matplotlib.pyplot as plt
import numpy as np

def read_xvg(filename):
    """读取GROMACS .xvg文件，跳过注释行。"""
    time, y = [], []
    with open(filename) as f:
        for line in f:
            if line.startswith(('#', '@')):
                continue
            parts = line.split()
            # 跳过ntv （实际是跳了5000ps）
            if float(parts[0]) < 3000.0000000:
                continue
            time.append(float(parts[0]) - 3000.0000000)
            # time.append(float(parts[0]))
            y.append(float(parts[1]))
    return np.array(time), np.array(y)

files = [
    ('rmsd_300k.xvg', '300K'), # 先降
    ('rmsd_320k.xvg', '320K'),
    ('rmsd_340k.xvg', '340K'),
    ('rmsd_360k.xvg', '360K'), # 先降
    ('rmsd_380k.xvg', '380K'), # no no no
    ('rmsd_400k.xvg', '400K'),
]
colors = ['#b8aeeb', '#71b7ed', '#84c3b7', '#fae69e', '#f2656f', '#f57c6e']
plt.figure(figsize=(10, 6))

for idx, (file, label) in enumerate(files):
    time, rmsd = read_xvg(file)

    color = colors[idx]

    mean_npt = np.mean(rmsd[:])
    std_npt = np.std(rmsd[:])
    plt.plot(time[:], rmsd[:],
             linestyle='-', linewidth=1.5, alpha=1.0,
             color=color,
             label=f"{label} (Mean={mean_npt:.2f}±{std_npt:.2f} nm)")

    # 均值
    plt.axhline(mean_npt, linestyle=':', linewidth=1.5, alpha=1.0, color=color)

    # 每个点 ± 全局 std 阴影


plt.xlabel('Time (μs)', fontsize=13)
plt.ylabel('RMSD (nm)', fontsize=13)
plt.title('Root-Mean-Square Deviation at Different Temperatures', fontsize=15)
plt.legend(title="Temperature", fontsize=8)
plt.tight_layout()
plt.grid(alpha=0.3)
plt.savefig('../img/2_1_1_rmsd_all_line.svg', dpi=300)
plt.show()
