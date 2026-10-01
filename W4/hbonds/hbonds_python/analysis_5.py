import matplotlib.pyplot as plt
import numpy as np

# 1. 读取xvg文件，自动跳过注释行
def read_hbond_xvg(filename):
    times = []
    hbonds = []
    pairs = []
    with open(filename, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#') or line.startswith('@') or line == '':
                continue
            items = line.split()
            if len(items) == 3:
                t, h, p = items
                times.append(float(t))
                hbonds.append(float(h))
                pairs.append(float(p))
    return np.array(times), np.array(hbonds), np.array(pairs)

# 2. 调用函数读取你的数据
times, hbonds, pairs = read_hbond_xvg("hbonds_C27G43.xvg")

# 3. 绘图
plt.figure(figsize=(8,5))
plt.plot(times, hbonds, label="Hydrogen bonds (H-bond criterion)", color="C0")
plt.plot(times, pairs, label="Pairs within 0.35 nm (distance only)", color="C1", linestyle='--')
plt.xlabel("Time (ps)")
plt.ylabel("Number")
plt.title("Hydrogen Bonds between C27 and G43")
plt.legend()
plt.tight_layout()
plt.show()
