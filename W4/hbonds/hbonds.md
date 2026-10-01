## RMSF
- RMSF（Root Mean Square Fluctuation, 均方根波动）（nm）随RNA每个位点（残基）的变化
- 反映每一个原子（或残基）在整个MD轨迹期间的平均位置波动程度。描述单个原子/残基的局部柔性，表示在模拟期间各残基的空间波动幅度
- 作图
  ``` bash
  gmx rmsf -s 1y26_NPT_MD0.tpr -f 1y26_NPT_MD0_center.trr -o rmsf.xvg -res
  
  xmgrace -hdevice PNG -hardcopy -printfile ./rmsf.png rmsf.xvg
  ```

---
---
---

## H-Bonds
### GROMACS
1. 生成索引文件
- 目的：仅考虑WC BP间的氢键，忽略其他氢键
- 操作：
```bash
# 看所有氢键
gmx make_ndx -f 1y26_NPT_MD0.gro -o hbonds_all.ndx
# q

# 分别看AU/CG
gmx make_ndx -f 1y26_NPT_MD0.gro -o hbonds.ndx
# r A \ r U \ r C \ r G \ q

# 看局部
gmx make_ndx -f 1y26_NPT_MD0.gro -o hbonds_4555.ndx
# r 45-55 \ q
# 这个作xvg时选两个一样的组即可

# 看单点
gmx make_ndx -f 1y26_NPT_MD0.gro -o hbonds_2743.ndx
# r 27 \ r 43 \ q
```

2. 计算氢键
```bash
gmx hbond -f 1y26_NPT_MD0_center.trr -s 1y26_NPT_MD0.tpr -n hbonds.ndx -num hbonds_AU.xvg
gmx hbond -f 1y26_NPT_MD0_center.trr -s 1y26_NPT_MD0.tpr -n hbonds.ndx -num hbonds_CG.xvg
# hbond.xvg输出每一帧氢键对数（随时间变化）
# 运行后，你选择donor和acceptor group（氢键的供体和受体分子组）：A-U配对，G-G配对
# 正反都要试
# 其他可选参数：
# -contact XXX.xvg：计算非氢键型原子接触
# -life XXX.xvg：输出每个氢键的寿命
# -ac XXX.xvg：输出氢键自相关函数
# -dist XXX.xvg：输出供体-受体距离分布
# -ang XXX.xvg：输出氢键夹角分布
```

3. xvg文件

| 列数     | 含义 | 备注|
| ---------- | -------------------- | ------------------------------ |
| 第一列| 时间           | 皮秒，ps                |
| 第二列| 该时刻的氢键数              | 氢键严格定义（通常包含距离和角度条件）      |
| 第三列| 该时刻距离阈值（0.35 nm）内的对数 |只考虑距离，不管角度（反映接近但未必形成经典氢键的原子对）|

4. 画图查看
```bash
xmgrace -hdevice PNG -hardcopy -printfile ./hbonds_AU.png -nxy hbonds_AU.xvg
xmgrace -hdevice PNG -hardcopy -printfile ./hbonds_CG.png -nxy hbonds_CG.xvg
# -nxy：把第1列当作横坐标，后面每列都画成一条曲线（即多条数据集）
```

---

### VMD
1. 加载轨迹（gro+trr/xtc）

2. Extensions > Analysis > Hydrogen Bonds

3. 参数设置：
> Input options: <br>
> > Selection 1: <br>
> > > 如果看单点， 这里填`resid 27 and resname C` <br>
> > > 如果看局部， 这里填`resid 27 to 43` <br>
> > > 如果看整体， 这里填`nucleic` <br>
> >
> > Selection 2: <br>
> > > 如果看单点， 这里填`resid 43 and resname G` <br>
> > > 如果看局部， 这里不填 <br>
> > > 如果看整体， 这里不填 <br>
> >
> > Update selection every frame: `✔` <br>
> >
> > Donor-Acceptor distance: `3.5` <br>
> > Angle cutoff: `30` <br>
> > Calculate detailed info for: `Residue pairs` <br>
> 
> Output options: <br>
> > Output directory: `C:/Users/徐岳威/Desktop` <br>
> > Write output to files?: `✔` <br>

4. Find hydrogen bonds!

---

### Barnaba
1. 安装 Barnaba
```bash
pip install barnaba
```

2. 主命令：ANNOTATE（分析碱基对）
```bash
barnaba ANNOTATE --trj 1y26_NPT_MD0_center.trr --top 1y26_NPT_MD0.gro -o basepair_annotate.csv
# barnaba ANNOTATE -h 查看所有参数说明
```

4. 结果解释
- 输出pairing&stacking两个csv
- 每个Frame对应于轨迹文件中1帧的情况
- C_13_0：0号链上的第13个C
- pairing类型

| 缩写  | 释义                 | 解释           |
| :---:|:-------------------------:| :--------------: |
| WCc | 经典Watson-Crick (A-T; C-G)          | 主流二级结构稳定力      |
| GUc | G-U摇摆配对            | RNA中功能多样的非典型配对 |
| WWc | - |  经典Watson-Crick, WWc包括了所有WCc，但WCc通常特指A-U/G-C这些严格意义的“Watson-Crick碱基对”
| WHt |  -   | 常见于三链体/高级结构    |
| WSc | - |  回环/三维结构中偶见     |
| SS  | -|  仅见于特殊结构        |
| XXX | 未配对/无法识别            | -       | 碱基未成对或不在可识别类型中 |

> Watson-Crick边（W）
>> 传统配对区域，A、U、G、C都是在这侧形成经典的双螺旋配对氢键
>> 具体来说，A的N1和N6，U的O4和N3，G的O6和N1，C的N3和O2等都属于W边
>
> Hoogsteen边（H）
>> 在W边的另一侧（比如A的N7和C8，G的N7和C8），参与三链体、G四链体等配对
> 
> Sugar边（S）
>> 朝向糖环的边，涉及C6或C8邻近的基团

> c: cis 顺式
> t: trans 反式

- stacking类型

| 字段       | 解释               |
| -------- | ---------------- |
| >>       | 顺式堆叠（前->后）       |
| <<       | 顺式堆叠（后->前）       |
| <> 或 ><  | 反式堆叠             |

---

### 后续分析（python）
- 统计每帧中不同配对类型的数量
```python
# 统计每帧中不同配对类型的数量
import pandas as pd

file = 'basepair_annotate.csv'
frame_data = []
current_frame = None

with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('# Frame'):
            current_frame = int(line.split()[2])
            frame_data.append([])
        elif line and not line.startswith('#'):
            parts = line.split()
            if len(parts) == 3:
                frame_data[-1].append(parts)

# 每帧配对类型统计
for i, frame in enumerate(frame_data):
    df = pd.DataFrame(frame, columns=['res1', 'res2', 'type'])
    counts = df['type'].value_counts()
    print(f'Frame {i}:')
    print(counts)
    print('---')
```

- 统计某个配对在轨迹中出现的频率
```python
# 统计某个配对在轨迹中出现的频率（帧数）
from collections import Counter
import pandas as pd

file = 'basepair_annotate.csv'
frame_data = []
current_frame = None

with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('# Frame'):
            current_frame = int(line.split()[2])
            frame_data.append([])
        elif line and not line.startswith('#'):
            parts = line.split()
            if len(parts) == 3:
                frame_data[-1].append(parts)

# 特定配对类型总帧数统计              
pair_counter = Counter()
for frame in frame_data:
    for res1, res2, type_ in frame:
        if type_ == "WCc":
            pair = tuple(sorted([res1, res2]))
            pair_counter[pair] += 1

print('WCc配对出现频次（所有帧）:')
for pair, count in pair_counter.most_common():
    print(f'{pair}: {count} frames')
```

- 统计每对碱基Watson-Crick配对的保持概率
```python
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
```
- 统计全过程中WC-pair的数量（画图）
```python
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



(resid 27 and resname C) AND (resid 43 and resname G)