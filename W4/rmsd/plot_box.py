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
            time.append(float(parts[0]))
            y.append(float(parts[1]))
    return np.array(time), np.array(y)

files = [
    ('rmsd_npt_300k.xvg', '300K'),
    ('rmsd_npt_320k.xvg', '320K'),
    ('rmsd_npt_340k.xvg', '340K'),
    ('rmsd_npt_360k.xvg', '360K'),
    ('rmsd_npt_380k.xvg', '380K'),
    ('rmsd_npt_400k.xvg', '400K')
]

all_rmsd = []
labels = []
for file, label in files:
    _, rmsd = read_xvg(file)
    all_rmsd.append(rmsd)
    labels.append(label)

plt.figure(figsize=(7, 5))
box = plt.boxplot(
    all_rmsd, labels=labels, patch_artist=True,
    boxprops=dict(linewidth=1.2),
    medianprops=dict(linewidth=2),
    whiskerprops=dict(linewidth=1),
    capprops=dict(color='black', linewidth=1),
    flierprops=dict(marker='o', markerfacecolor='white', markeredgecolor='black', markersize=4)
)
plt.xlabel('Temperature (K)')
plt.ylabel('RMSD (nm)', color='black')
plt.title('RMSD Distribution at Different Temperatures', color='black')
plt.grid(axis='y', alpha=0.3, color='gray', linestyle='--')
plt.tight_layout()

# save
plt.savefig('rmsd_box.png', dpi=300)
# plt.savefig('rmsd_box.pdf', dpi=300)

plt.show()
