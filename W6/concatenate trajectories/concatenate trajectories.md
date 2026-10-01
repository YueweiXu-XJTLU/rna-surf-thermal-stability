## 合并ntv与npt轨迹

- 这样首帧（能量最小化后的gro）可以确保一致

- 合并轨迹 & 生成xvg：**使用：nvt轨迹文件（未处理pbc） & npt轨迹文件（已处理pbc） & 能量最小化后的结构文件**

```bash
gmx trjcat -f 1y26_NTV_MD0.trr 1y26_NPT_MD0.trr -o full_00.trr -settime
c \ c 
# c(ontinue), add 2nd file at end of 1st file continously

gmx rms -s 1y26_system_em0.gro -f full_00.trr -o rmsd_300k_00.xvg
1 \ 1
```

- python进一步画图