import matplotlib.pyplot as plt
import numpy as np

def read_xvg(filename):
    """
    Read GROMACS .xvg file, skipping comments.
    """
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
    ('rmsd_npt_400k.xvg', '400k')
]

plt.figure(figsize=(8, 5))
for file, label in files:
    time, rmsd = read_xvg(file)
    mean_val = np.mean(rmsd)
    std_val = np.std(rmsd)
    line, = plt.plot(time, rmsd, label=f"{label} (Mean={mean_val:.2f}±{std_val:.2f} nm)", linewidth=1.5)
    color = line.get_color()
    plt.axhline(mean_val, linestyle='--', linewidth=1, alpha=1, color=color)

plt.xlabel('Time (ps)', fontsize=13)
plt.ylabel('RMSD (nm)', fontsize=13)
plt.title('RMSD at Different Temperatures', fontsize=15)
plt.legend(title="Temperature", fontsize=6)
plt.tight_layout()
plt.grid(alpha=0.3)

# save
plt.savefig('rmsd_line.png', dpi=300)
# plt.savefig('rmsd_line.pdf', dpi=300)

plt.show()

