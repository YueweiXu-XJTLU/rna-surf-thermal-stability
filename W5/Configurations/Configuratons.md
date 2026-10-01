# Comparison Between Initial and Final Configuration

1. 用GROMACS导出首末帧结构
```bash
# 查看最后一帧时间
gmx check -f 1y26_NPT_MD0_center.trr
# 输出中包含：Last frame        500 time 1000000.000
# 则下面填1000000.000

# 提取首帧
gmx trjconv -f 1y26_NPT_MD0_center.trr -s 1y26_NPT_MD0.tpr -o first_frame_300k.gro -b 0 -e 0
# 0 System

# 提取末帧
gmx trjconv -f 1y26_NPT_MD0_center.trr -s 1y26_NPT_MD0.tpr -o last_frame_300k.gro -b 1000000.000 -e 1000000.000
# 0 System
```

2. 定量分析用
- VMD进行结构可视化对比

3. 定性分析
- 主成分分析（PCA, Principal Component Analysis）
- PCA 用于提取轨迹中最主要的协同运动模式（主成分），揭示分子的主要动力学变化
- 可以比较首末帧在主成分空间的分布，判断结构大幅度变化
- 代码
- 
```bash
# 1. 对齐
gmx covar -s first_frame_300k.gro -f 1y26_NPT_MD0_center.trr -o eigenval_1.xvg -v eigenvec_1.trr
# 1 RNA / 1 RNA

#第一个 1：选择用于协方差分析的原子组（比如 RNA 或 Backbone），通常是你要做PCA分析的对象。
#第二个 1：用于对齐的原子组，一般和上面一样选同一组（如 RNA 主链），保证运动分析时不因整体移动而混淆。
```

```bash
# 2. 投影
gmx anaeig -v eigenvec_1.trr -s first_frame_300k.gro -f 1y26_NPT_MD0_center.trr -first 1 -last 2 -proj proj_1.xvg
# 1 RNA / 1 RNA

# 第一个 1：选择分析主成分时的原子组（与covar一致）。
# 第二个 1：选择用于拟合对齐的原子组（通常同上）。
# -first 1 -last 2 选择主成分
# proj.xvg为投影分布
```

```bash
# 3. 绘图
xmgrace -hdevice PNG -hardcopy -printfile ./eigenval_1.png -nxy eigenval_1.xvg
xmgrace -hdevice PNG -hardcopy -printfile ./proj_1.png -nxy proj_1.xvg
```
