import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d

def read_xvg(filename):
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
    ('rmsd_npt_400k.xvg', '400K'),
    ('rmsd_npt_380k.xvg', '380K'),
    ('rmsd_npt_360k.xvg', '360K'),
    ('rmsd_npt_340k.xvg', '340K'),
    ('rmsd_npt_320k.xvg', '320K'),
    ('rmsd_npt_300k.xvg', '300K')
]

all_rmsd = []
for file, label in files:
    _, rmsd = read_xvg(file)
    avg = uniform_filter1d(rmsd, size=100)[::10]  # 平滑后每10帧采样
    all_rmsd.append(avg)

# 对齐长度
minlen = min(len(x) for x in all_rmsd)
all_rmsd = np.array([x[:minlen] for x in all_rmsd])

plt.figure(figsize=(10,4))
sns.heatmap(all_rmsd, cmap='YlOrRd', yticklabels=[l for _,l in files])
plt.xlabel('Time Window')
plt.ylabel('Temperature')
plt.title('RMSD Evolution Heatmap')
plt.tight_layout()

# save
plt.savefig('rmsd_heat_map.png', dpi=300)
# plt.savefig('rmsd_heat_map.pdf', dpi=300)

plt.show()
