# 统计全过程中WC-pair的数量（画图）
import pandas as pd
import matplotlib.pyplot as plt

# 读取配对文件
# Read the basepair annotation file
df = pd.read_csv('basepair_annotate_ANNOTATE_pairing_out.csv', comment="#", delim_whitespace=True, names=["RES1", "RES2", "ANNO"])

# 构建Pair，无序处理
df['Pair'] = df.apply(lambda row: tuple(sorted([row['RES1'], row['RES2']])), axis=1)

# 假设每一帧的配对数量一致，否则需根据Frame编号分组！
# 下面是通用分帧方法：自动识别“# Frame N”分段
frame_indices = []
current_frame = -1
with open('basepair_annotate_ANNOTATE_pairing_out.csv', encoding='utf-8') as f:
    for line in f:
        if line.startswith("# Frame"):
            current_frame += 1
        elif not line.startswith("#") and line.strip():
            frame_indices.append(current_frame)
df['Frame'] = frame_indices

# 统计每一帧的Watson-Crick配对对数
wc_per_frame = df[df['ANNO'] == 'WCc'].groupby('Frame').size()

# 画图
plt.plot(wc_per_frame.index, wc_per_frame.values)
plt.xlabel("Frame")
plt.ylabel("Number of Watson-Crick pairs")
plt.title("Watson-Crick Base Pairs Over Time")
plt.tight_layout()
plt.show()