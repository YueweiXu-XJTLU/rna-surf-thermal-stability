#!/bin/bash

# NPT生产相模拟
gmx_mpi grompp -f NPT.mdp -p 1y26.top -c 1y26_NTV_MD0.gro -o 1y26_NPT_MD0.tpr
gmx_mpi mdrun -deffnm 1y26_NPT_MD0 -v
