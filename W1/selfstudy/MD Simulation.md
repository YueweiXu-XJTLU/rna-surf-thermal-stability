# MD Simulation
|顺序|步骤|输入文件|输出文件|代码|备注|
|---|---|---|---|---|---|
|1|pdb 预处理|1y26.pdb|1y26.pdb|txt直接编辑|仅保留RNA主链|
|2|力场，水分子加入|1y26.pdb|conf.gro & posre.itp & topol.top|`gmx pdb2gmx -f 1y26.pdb`|选择`amber14sb_OL15"` & `TIP3P`;.gro：分子结构文件 .top: 系统的体系文件 & .itp: 分子的体系文件|
|3|建立盒子|conf.gro|boxed.gro|`gmx editconf -f conf.gro -o boxed.gro -c -d 1.0 -bt cubic`|`-c`  分子居中； `-d` 分子与盒边缘最小距离；`-bt` 盒子形状|
|4|溶剂化|boxed.gro & spc216.gro|solvated.gro & topol.top|`gmx solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p topol.top`|spc216.gro：TIP3P水分子模型; #topol.top.1#：文件备份|
|5.1|离子平衡1|em.mdp & solvated.gro & topol.top|ions.tpr|`gmx grompp -f em.mdp -c solvated.gro -p topol.top -o ions.tpr -maxwarn 1`|随便输入一个mdp文件（动力学模拟参数文件，指示软件怎么模拟），这里选择em.mdp；`-maxwarn 1`：允许最多1个警告，这里警告体系例子不平衡，下一步会解决，故先允许一个警告|
|5.2|离子平衡2|ions.tpr & topol.top|solv_ions.gro|`gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral -conc 0.15`|`-pname`：阳离子名称；`-nname`：阴离子名称；`-neutral`：自动平衡电荷；`-conc`：电离平衡浓度控制；选`SOL`，替换为离子|
|6.1|能量极小化1|em.mdp & solv_ions.gro & topol.top|em.tpr|`gmx grompp -f em.mdp -c solv_ions.gro -p topol.top -o em.tpr`|tpr：拓扑与参数综合运行文件（二进制文件）|
|6.2|能量极小化2|自动输入|em.trr & em.log & em.gro & em.edr|`gmx mdrun -deffnm em`|运行tpr，生成一系列以em开头的结果文件；trr：轨迹文件（完整精度）；edr：能量文件|
|7.1|平衡相模拟-等温等压1|nvt.mdp & em.gro & topol.top|nvt.tpr|`gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -o nvt.tpr`|Constant Number, Volume, and Temperature：NVT；MD时长控制:dt-每步时间步长（ps）; nsteps-总步数；总模拟时间（ps） = nsteps × dt；（1 s=1E-9 ns=1E-12 ps）|
|7.2|平衡相模拟-等温等压2|自动输入|nvt.trr & nvt.log & nvt.gro & nvt.edr & nvt.cpt|`gmx mdrun -deffnm nvt`||
|8.1|平衡相模拟-等温等体积1|npt.mdp & nvt.gro & topol.top|npt.tpr|`gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -p topol.top -o npt.tpr`|Constant Number, Pressure, and Temperature：NPT|
|8.2|平衡相模拟-等温等体积2|自动输入|npt.trr & npt.log & npt.gro & npt.edr & npt.cpt|`gmx mdrun -deffnm npt`||
|9.1|查看体系能量，确认体系平衡1|npt.edr|energy.xvg|`gmx energy -f npt.edr -o energy.xvg`|可直接Enter，或选择参数|
|9.2|查看体系能量，确认体系平衡2|energy.xvg|体系能量图|`xmgrace -hdevice PNG -hardcopy -printfile ./energy.png energy.xvg`|用xmgrace看体系能量图：无系统性趋势（明显的整体上升或下降），能量上下小幅波动，表明体系已基本处于平衡态；-hdevice：输出格式；-hardcopy：直接print，不在GUI显示；-printfile：输出路径；`xdg-open energy.png`查看png|
|10.1|产生相模拟1|production.mdp & npt.gro & topol.top|production.tpr|`gmx grompp -f production.mdp -c npt.gro -r npt.gro -p topol.top -o production.tpr`||
|10.2|产生相模拟2|自动输入|production.xtc & production.trr & production.log & production.gro & production.edr & production.cpt|`gmx mdrun -deffnm production`|xtc：轨迹文件（压缩精度）|
|11.1|处理PBC隐含问题1|production.tpr & production.xtc|production_nojump.xtc|`gmx trjconv -s production.tpr -f production.xtc -o production_nojump.xtc -pbc nojump`|PBC-Periodic Boundary Conditions（周期性边界条件）：通过在模拟盒子的各个方向复制体系，模拟无限大体系，消除边缘效应，使模拟更接近真实物理环境；PBC可能导致分子在轨迹动画中出现被强行拉直、断裂或分裂的现象；解决步骤1：解开分子在周期性盒子里的跳跃轨迹；选择output group: 0 (System)|
|11.2|处理PBC隐含问题2|production.tpr & production_nojump.xtc|production_center.xtc|`gmx trjconv -s production.tpr -f production_nojump.xtc -o production_center.xtc -pbc mol -center`|解决步骤2：把分子重新放回盒子中心；选择centering group: 1 (RNA) & output group: 0 (System)|
|12|可视化|production.gro & production.xtc|可视化画面|先加载分子（gro），再在分子上加载轨迹（xtc），`pbc box`显示盒子|可选择只显示核酸，停止旋转：Extensions → Analysis → RMSD Trajectory Tool → 选择参考帧和对齐原子（nucleic） → Align|
|13|RMSD计算|production.tpr & production.xtc|rmsd.xvg|`gmx rms -s production.tpr -f production.xtc -o rmsd.xvg`|选择两次Group 1 (RNA)|
|14|部分提取trr|1y26_NPT_MD0.trr & 1y26_NPT_MD0.tpr|NPT_partial.trr|`gmx check -f 1y26_NPT_MD0.trr` & `gmx trjconv -s 1y26_NPT_MD0.tpr -f 1y26_NPT_MD0.trr -o NPT_partial.trr -b 0 -e 800`|第一条命令查看当前完成帧数，第二条部分截取，-b 0：起始时间（ps）；-e 80000：终止时间（ps）