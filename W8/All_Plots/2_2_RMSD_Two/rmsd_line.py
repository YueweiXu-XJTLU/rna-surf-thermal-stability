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
            # 跳过ntv
            if float(parts[0]) < 3000.0000000:
                continue
            time.append(float(parts[0]) - 3000.0000000)
            # time.append(float(parts[0]))
            y.append(float(parts[1]))
    return np.array(time), np.array(y)

files = [
    ('rmsd_300k.xvg', '300K'),
    ('rmsd_360k.xvg', '360K'),
]
colors = ["#71b7ed", "#f2656f"]
plt.figure(figsize=(10, 6))

# NPT段：实线
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
    plt.fill_between(time[:],
                    rmsd[:] - std_npt,
                    rmsd[:] + std_npt,
                    alpha=0.15)


plt.xlabel('Time (μs)', fontsize=13)
plt.ylabel('RMSD (nm)', fontsize=13)
plt.title('Root-Mean-Square Deviation at 300K & 360K', fontsize=15)
plt.legend(title="Temperature", fontsize=8)
plt.tight_layout()
plt.grid(alpha=0.3)
plt.savefig('../img/2_2_1_rmsd_two_line.svg', dpi=300)
plt.show()
