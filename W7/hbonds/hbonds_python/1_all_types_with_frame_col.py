import pandas as pd
import matplotlib.pyplot as plt

# 1. 读取数据
file = 'pairings_60_3.3.csv'  # 换成你的文件名
df = pd.read_csv(file)

# 2. 按 frame 和 pair_type 统计数量
type_counts = df.groupby(['frame', 'pair_type']).size().unstack(fill_value=0)

# 3. 按照你想要的方式画图（只画部分pair type，可以随意增删）
plt.figure(figsize=(10, 5))
x = type_counts.index  # 所有frame编号

# if 'GUc' in type_counts: plt.plot(x, type_counts['GUc'], label='GUc')
# if 'HHc' in type_counts: plt.plot(x, type_counts['HHc'], label='HHc')
# if 'HHt' in type_counts: plt.plot(x, type_counts['HHt'], label='HHt')
# if 'HSc' in type_counts: plt.plot(x, type_counts['HSc'], label='HSc')
# if 'HSt' in type_counts: plt.plot(x, type_counts['HSt'], label='HSt')
# if 'HWc' in type_counts: plt.plot(x, type_counts['HWc'], label='HWc')
# if 'HWt' in type_counts: plt.plot(x, type_counts['HWt'], label='HWt')
# if 'SHc' in type_counts: plt.plot(x, type_counts['SHc'], label='SHc')
# if 'SHt' in type_counts: plt.plot(x, type_counts['SHt'], label='SHt')
# if 'SSc' in type_counts: plt.plot(x, type_counts['SSc'], label='SSc')
# if 'SSt' in type_counts: plt.plot(x, type_counts['SSt'], label='SSt')
# if 'SWc' in type_counts: plt.plot(x, type_counts['SWc'], label='SWc')
# if 'SWt' in type_counts: plt.plot(x, type_counts['SWt'], label='SWt')
# if 'WHc' in type_counts: plt.plot(x, type_counts['WHc'], label='WHc')
# if 'WHt' in type_counts: plt.plot(x, type_counts['WHt'], label='WHt')
# if 'WSc' in type_counts: plt.plot(x, type_counts['WSc'], label='WSc')
# if 'WSt' in type_counts: plt.plot(x, type_counts['WSt'], label='WSt')
# if 'XXX' in type_counts: plt.plot(x, type_counts['XXX'], label='XXX')
if 'WCc' in type_counts: plt.plot(x, type_counts['WCc'], label='WCc')
if 'WWc' in type_counts: plt.plot(x, type_counts['WWc'], label='WWc')
if 'WWt' in type_counts: plt.plot(x, type_counts['WWt'], label='WWt')

plt.xlabel('Frame')
plt.ylabel('Count')
plt.title('Numbers of Base Pairs Per Frame')
plt.tight_layout()
plt.legend()
plt.savefig("hbonds_all_diff_types_with_frame_col_60_3.3.png")
plt.show()
