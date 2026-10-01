#!/bin/bash

# NTV生产相模拟
gmx grompp -f NTV.mdp -p 1y26.top -c 1y26_system_em0.gro -o 1y26_NTV_MD0.tpr
gmx mdrun -deffnm 1y26_NTV_MD0 -v
