## NTV盒子尺寸：
- 检查gro文件最后一行即可
- `11.10136  11.10136  11.10136`: 三维正方体盒子，边长11.10136nm

## NPT盒子尺寸&密度：
- 用NPT生成的edr文件： 
```bash
gmx energy -f 1y26_NPT_MD0.edr -o box_size.xvg
# 17 / 18 / 19 / 20 / ENTER / ENTER

gmx energy -f 1y26_NPT_MD0.edr -o box_xyz.xvg
# 17 / 18 / 19 / ENTER / ENTER

gmx energy -f 1y26_NPT_MD0.edr -o box_x.xvg
# 17 / ENTER / ENTER

gmx energy -f 1y26_NPT_MD0.edr -o box_y.xvg
# 18 / ENTER / ENTER

gmx energy -f 1y26_NPT_MD0.edr -o box_z.xvg
# 19 / ENTER / ENTER

gmx energy -f 1y26_NPT_MD0.edr -o box_volume.xvg
# 20 / ENTER / ENTER

gmx energy -f 1y26_NPT_MD0.edr -o density.xvg
# 21 / ENTER / ENTER

# 输入相应数字（Box-X/Box-Y/Box-Z/Box-Volume/Density）
# 可多选，空格分隔，输入两次空格结束
```

```bash
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./box_size.png -nxy box_size.xvg
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./box_x.png -nxy box_x.xvg
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./box_y.png -nxy box_y.xvg
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./box_z.png -nxy box_z.xvg
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./box_xyz.png -nxy box_xyz.xvg
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./box_volume.png -nxy box_volume.xvg
xmgrace -maxpath 50000 -hdevice PNG -hardcopy -printfile ./density.png -nxy density.xvg
```