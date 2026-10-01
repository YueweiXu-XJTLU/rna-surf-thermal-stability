#!/bin/bash
# 运行目录: ~/Downloads/test2

# 1. PDB转GRO+TOP
gmx pdb2gmx -f 1y26.pdb -o 1y26.gro -p 1y26.top

# 2. 定义盒子
gmx editconf -f 1y26.gro -o 1y26_box.gro -bt cubic -d 2.0

# 3. 检查盒子
gmx check -f 1y26_box.gro

# 4. 能量极小化预处理
gmx grompp -f minim.mdp -c 1y26_box.gro -p 1y26.top -o 1y26_em0.tpr

# 5. 能量极小化
gmx mdrun -deffnm 1y26_em0

# 6. 加水
gmx solvate -cp 1y26_em0.gro -cs spc216.gro -p 1y26.top -o 1y26_wat.gro

# 7. 加水后再预处理（为加离子准备）
gmx grompp -f minim.mdp -p 1y26.top -c 1y26_wat.gro -o 1y26_genion.tpr

# 8. 加离子（Na+/Cl-，生理浓度0.15M，自动中和）
gmx genion -s 1y26_genion.tpr -o 1y26_system.gro -p 1y26.top -pname NA -nname CL -conc 0.15 -neutral

# 9. 离子后再做极小化
gmx grompp -f minim.mdp -p 1y26.top -c 1y26_system.gro -o 1y26_system_em0.tpr
gmx mdrun -deffnm 1y26_system_em0

echo "pre-processing finished!"
