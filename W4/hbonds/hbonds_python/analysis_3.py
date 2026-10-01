# 统计某个配对在轨迹中出现的频率（概率）
import pandas as pd

# 读取配对文件（自动跳过#开头的注释行，自动分列）
df = pd.read_csv('basepair_annotate_ANNOTATE_pairing_out.csv', comment="#", sep='\s+', names=["RES1", "RES2", "ANNO"])

# 构建无序Pair列，方便统计（比如 ('A_1', 'U_2') 和 ('U_2', 'A_1') 视为同一对）
df['Pair'] = df.apply(lambda row: tuple(sorted([row['RES1'], row['RES2']])), axis=1)

# 统计每对碱基一共出现了多少帧
total_counts = df.groupby('Pair').size()

# 统计每对碱基为Watson-Crick（ANNO == "WCc"）的帧数
wc_counts = df[df['ANNO'] == 'WCc'].groupby('Pair').size()

# 计算每对碱基为Watson-Crick的保持概率（出现WCc的帧数 / 总帧数）
wc_prob = (wc_counts / total_counts).fillna(0).sort_values(ascending=False)

print("每对碱基Watson-Crick（WCc）保持概率：")
print(wc_prob)

# 额外：如果想要输出为csv
# wc_prob.to_csv('WCc_probability_per_pair.csv')
# print("\n每对的Watson-Crick保持概率已导出为 WCc_probability_per_pair.csv")