#!/usr/bin/env bash
# md_pipeline.sh — 一体化 MD 模拟流水线脚本 / Integrated MD Simulation Pipeline Script
# 学术说明：本脚本依次完成 PDB 预处理检查、力场赋予、盒子构建、溶剂化、电荷中和、能量最小化、NVT/NPT 平衡（中途暂停等待确认）、生产相 MD 及后处理提示
# Academic note: This script sequentially performs PDB preprocessing check, force field setup, box definition, solvation, ion neutralization, energy minimization, NVT/NPT equilibration (with pause), production MD, and final visualization hints.

set -euo pipefail

#### 用户可编辑参数 / User‐editable parameters ####
PDB_IN="1y26.pdb"             # 输入 PDB 文件 / input PDB
PREP_PDB="processed.pdb"      # 预处理后 PDB（仅保留 RNA 主链等）/ preprocessed PDB
FORCEFIELD="amber03"          # 力场选项 / force field
WATER_MODEL="tip3p"           # 水模型 / water model
BOX_DISTANCE=1.0              # 盒边距 (nm) / distance to box edge
ION_CONC=0.15                 # 离子浓度 (M) / ion concentration
EM_MDP="em.mdp"               # 能量最小化 MDP / energy minimization MDP
NVT_MDP="nvt.mdp"             # NVT 平衡 MDP / NVT equilibration MDP
NPT_MDP="npt.mdp"             # NPT 平衡 MDP / NPT equilibration MDP
PROD_MDP="production.mdp"     # 生产相 MD MDP / production MD MDP

#### 1. PDB 预处理检查 / Check preprocessed PDB ####
if [ ! -f "${PREP_PDB}" ]; then
  echo "错误：未找到 ${PREP_PDB}。请先手动或脚本完成 PDB 预处理（仅保留 RNA 主链等），生成 ${PREP_PDB}。" >&2
  exit 1
fi
echo "✔ 已找到预处理文件 ${PREP_PDB}，开始后续流程…"  

#### 2. 力场赋予与拓扑生成 / Force field assignment & topology ####
echo "==> 力场赋予 / Running pdb2gmx"
gmx pdb2gmx \
    -f "${PREP_PDB}" \
    -o conf.gro \
    -p topol.top \
    -i posre.itp \
    -ff "${FORCEFIELD}" \
    -water "${WATER_MODEL}"

#### 3. 盒子构建 / Define simulation box ####
echo "==> 盒子构建 / Running editconf"
gmx editconf \
    -f conf.gro \
    -o boxed.gro \
    -c -d "${BOX_DISTANCE}" \
    -bt cubic

#### 4. 溶剂化 / Solvation ####
echo "==> 溶剂化 / Running solvate"
gmx solvate \
    -cp boxed.gro \
    -cs spc216.gro \
    -o solvated.gro \
    -p topol.top

#### 5. 离子中和 / Ion neutralization ####
echo "==> 离子中和 / Generating ions.tpr"
gmx grompp \
    -f "${EM_MDP}" \
    -c solvated.gro \
    -p topol.top \
    -o ions.tpr \
    -maxwarn 1

echo "==> 添加离子 / Running genion"
echo "SOL" | gmx genion \
    -s ions.tpr \
    -o solv_ions.gro \
    -p topol.top \
    -pname NA -nname CL \
    -neutral \
    -conc "${ION_CONC}"

#### 6. 能量最小化 / Energy Minimization ####
echo "==> 能量最小化 / Running energy minimization"
gmx grompp -f "${EM_MDP}" -c solv_ions.gro -p topol.top -o em.tpr
gmx mdrun   -deffnm em

#### 7. NVT 平衡（等温等体积）/ NVT Equilibration ####
echo "==> NVT 平衡 / Running NVT"
gmx grompp -f "${NVT_MDP}" -c em.gro -r em.gro -p topol.top -o nvt.tpr
gmx mdrun   -deffnm nvt

#### 8. NPT 平衡（等温等压）/ NPT Equilibration ####
echo "==> NPT 平衡 / Running NPT"
gmx grompp -f "${NPT_MDP}" -c nvt.gro -r nvt.gro -p topol.top -o npt.tpr
gmx mdrun   -deffnm npt

# 在 NPT 平衡后暂停，等待用户确认再继续生产相模拟
echo
read -p "✔ NPT 平衡完成。按 [回车] 键继续进行生产相 MD…" _

#### 9. 生产相 MD / Production MD ####
echo "==> 生产相 MD / Running production MD"
gmx grompp -f "${PROD_MDP}" -c npt.gro -r npt.gro -p topol.top -o production.tpr
gmx mdrun   -deffnm production

#### 10. 后处理提示 / Final visualization hint ####
echo
echo "完成：MD 全流程已结束。"
echo "🔹 可使用 xmgrace energy.xvg 查看能量曲线"
echo "🔹 或使用 VMD 加载 production_center.xtc 进行可视化分析"