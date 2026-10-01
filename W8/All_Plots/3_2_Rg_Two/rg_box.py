
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
            if float(parts[0]) < 1000.0000000:
                continue
            time.append(float(parts[0]) - 1000.0000000)
            y.append(float(parts[1]))
    return np.array(time), np.array(y)
import matplotlib.pyplot as plt

# 定义要画的文件和对应标签
files = [
    ('rg_300k.xvg', '300K'),
    # ('rg_320k.xvg', '320K'),
    # ('rg_340k.xvg', '340K'),
    ('rg_360k.xvg', '360K'),
    # ('rg_380k.xvg', '380K'),
    # ('rg_400k.xvg', '400K'),
]

colors = ['#71b7ed', '#f2656f']  # 你给的配色基准
box_face_colors = ['#71b7ed'] * len(files)  # 每个箱体的填充色

all_rmsd = []
labels = []

for file, label in files:
    time, rmsd = read_xvg(file)
    mask = time > 1000  # 去掉前 1000 ps
    all_rmsd.append(rmsd[mask])
    labels.append(label)

plt.figure(figsize=(7, 5))

box = plt.boxplot(
    all_rmsd,
    tick_labels=labels,               # tick_labels 改成 labels 避免版本警告
    patch_artist=True,
    boxprops=dict(linewidth=1.5),
    medianprops=dict(linewidth=2, color=colors[1]),  # 中位线用 #f2656f
    whiskerprops=dict(linewidth=1),
    capprops=dict(color='black', linewidth=1),
    flierprops=dict(marker='o', markerfacecolor='#f57c6e', markeredgecolor='black'),
)

# 给每个箱体填色
for patch, color in zip(box['boxes'], box_face_colors):
    patch.set_facecolor(color)

plt.xlabel('Temperature (K)')
plt.ylabel('Rg (nm)')
plt.title('Radius of Gyration at 300K & 360K')
plt.grid(axis='y', alpha=0.3, color='gray', linestyle='--')
plt.tight_layout()
plt.savefig('../img/3_2_2_rg_two_box.svg', dpi=300)
plt.show()
