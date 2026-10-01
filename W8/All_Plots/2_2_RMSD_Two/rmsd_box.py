import matplotlib.pyplot as plt
import numpy as np

def read_xvg(filename):
    """读取GROMACS .xvg文件，跳过注释"""
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
            y.append(float(parts[1]))
    return np.array(time), np.array(y)

files = [
    ('rmsd_300k.xvg', '300K'),
    ('rmsd_360k.xvg', '360K'),
]

all_rmsd = []
labels = []
for file, label in files:
    time, rmsd = read_xvg(file)
    all_rmsd.append(rmsd[:])
    labels.append(label)

plt.figure(figsize=(7, 5))
box = plt.boxplot(
    all_rmsd,
    tick_labels=labels,
    patch_artist=True,
    boxprops=dict(linewidth=1.5),
    medianprops=dict(linewidth=2, color='#f2656f'),
    whiskerprops=dict(linewidth=1),
    capprops=dict(color='black', linewidth=1),
    flierprops=dict(marker='o', markerfacecolor='#f57c6e', markeredgecolor='black'),
)
box_colors = ['#71b7ed', '#71b7ed']
for patch, color in zip(box['boxes'], box_colors):
    patch.set_facecolor(color)

plt.xlabel('Temperature (K)')
plt.ylabel('RMSD (nm)', color='black')
plt.title('Root-Mean-Square Deviation at 300K & 360K', color='black')
plt.grid(axis='y', alpha=0.3, color='gray', linestyle='--')
plt.tight_layout()
plt.savefig('../img/2_2_3_rmsd_two_box.svg', dpi=300)
plt.show()
