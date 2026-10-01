### === 基础：重命名与清理 ===
# 如果对象名不是 1y26，请替换
set_name 1y26, rna
hide everything, rna
hide spheres, rna
hide everything, solvent and rna

### === 主链 ===
show cartoon, rna
set cartoon_nucleic_acid_mode, 1
set cartoon_ladder_mode, 0
set cartoon_ring_mode, 0
color grey70, rna and polymer  # 主链浅灰

### === 侧链 sticks ===
select base_atoms, name c2+c4+c5+c6+c8+n1+n2+n3+n4+n6+n7+n9+o2+o4+o6
select bases, rna and base_atoms
show sticks, bases

# 彩色 AUCG sticks
color red,    bases and resn A
color yellow, bases and resn C
color blue,   bases and resn U
color green,  bases and resn G

# 主链 cartoon 跟对应碱基同色
# color red,    byres (rna and resn A)
# color yellow, byres (rna and resn C)
# color blue,   byres (rna and resn U)
# color green,  byres (rna and resn G)
# 定义颜色（RGB 分量是 0–1 之间的小数）
set_color myA, [245/255, 124/255, 110/255]   # #f57c6e
set_color myC, [250/255, 230/255, 158/255]   # #fae69e
set_color myU, [113/255, 183/255, 237/255]   # #71b7ed
set_color myG, [132/255, 195/255, 183/255]   # #84c3b7

# 用 byres 给主链和碱基一起上色
color myA, byres (rna and resn A)
color myC, byres (rna and resn C)
color myU, byres (rna and resn U)
color myG, byres (rna and resn G)

# 可选：让碱基和主链视觉相连
set cartoon_ladder_mode, 1
set cartoon_ring_mode, 1

### === 氢键（3.3 Å，60°，无 label） ===
# 设置氢键判定参数
set h_bond_cutoff_center, 3.3
set h_bond_max_angle, 60

# 删除已有氢键对象（避免重复）
delete hb_bases

# 创建氢键对象，同时关闭 label
distance hb_bases, bases, bases, 3.3, mode=2
cmd.hide("labels", "hb_bases")

# 氢键外观（亮橙色）
set dash_width, 5
set dash_gap, 0.25
set dash_round_ends, on
set dash_radius, 0.2
set dash_color, grey90

### === 自动检测并标注 5′ 与 3′ 端 ===
python
stored.resis = []
cmd.iterate("rna and polymer", "stored.resis.append((chain, int(resi)))")
first_last = {}
for chain, resi in stored.resis:
    if chain not in first_last:
        first_last[chain] = [resi, resi]
    else:
        first_last[chain][0] = min(first_last[chain][0], resi)
        first_last[chain][1] = max(first_last[chain][1], resi)
for ch, (first, last) in first_last.items():
    cmd.label(f"rna and chain {ch} and resi {first} and name P+O5'+O5*", "'5\\''")
    cmd.label(f"rna and chain {ch} and resi {last} and name O3'+O3*", "'3\\''")
python end
set label_color, black
set label_size, 24


# === 去掉 ADE 碱基 sticks + 氢键 ===

# 1) 选中 ADE 的碱基原子（不包含主链原子 P、O5'、C5'、C4'、C3'、O3' 等）
select ade_base, (resn ADE+A) and name C2+C4+C5+C6+C8+N1+N2+N3+N4+N6+N7+N9+O2+O4+O6

# 2) 隐藏侧链（碱基部分）
hide sticks, ade_base
hide lines, ade_base
hide spheres, ade_base
hide labels, ade_base

# 3) 删除与 ADE 碱基相关的氢键
delete hb_bases
distance hb_bases, (bases and not resn ADE+A), (bases and not resn ADE+A), 3.3, mode=2
cmd.hide("labels", "hb_bases")

# 4) 恢复氢键样式
set dash_width, 5
set dash_gap, 0.25
set dash_round_ends, on
set dash_radius, 0.2
set dash_color, grey90



### === 背景与导出 ===
bg_color white
set antialias, 2
set ray_opaque_background, off
