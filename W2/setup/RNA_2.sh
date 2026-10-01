#!/bin/bash
#SBATCH -J  1y26_RNA_2
#SBATCH --partition=gpu4090         # Partition name
#SBATCH -n 1                         # Number of tasks (typically 1 if not using MPI)
#SBATCH --qos=2gpu              # Quality of Service (QOS) setting
#SBATCH --cpus-per-task=4       # 1:4 GPU:CPU ratio
#SBATCH --gres=gpu:2
#SBATCH -e  job.%j.err
#SBATCH -o  job.%j.out
#SBATCH --mail-user=Yuewei.Xu23@student.xjtlu.edu.cn
#SBATCH --mail-type=ALL


ml load gromacs/2023.2-gcc-9.5.0-jzxesel


##---- Do production at NPT -----------------------------
gmx_mpi grompp -f NPT.mdp -p 1y26.top -c 1y26_NTV_MD0.gro -o 1y26_NPT_MD0.tpr
gmx_mpi mdrun -deffnm 1y26_NPT_MD0 -v


