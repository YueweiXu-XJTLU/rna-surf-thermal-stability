#!/bin/bash
#SBATCH -J 1y26_RNA_PCA
#SBATCH --partition=gpu4090
#SBATCH -n 1
#SBATCH --qos=1gpu
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH -e job.%j.err
#SBATCH -o job.%j.out
#SBATCH --mail-user=Yuewei.Xu23@student.xjtlu.edu.cn
#SBATCH --mail-type=ALL

# 加载 GROMACS
ml load gromacs/2023.2-gcc-9.5.0-jzxesel

# ----------- Step 1: 协方差分析（PCA）/ Covariance Analysis -----------
echo -e "1\n1" | gmx_mpi covar -s first_frame_300k.gro -f 1y26_NPT_MD0_center.trr -o eigenval_1.xvg -v eigenvec_1.trr

# ----------- Step 2: 主成分投影 / Principal Component Projection -----------
echo -e "1\n1" | gmx_mpi anaeig -v eigenvec_1.trr -s first_frame_300k.gro -f 1y26_NPT_MD0_center.trr -first 1 -last 2 -proj proj_1.xvg