# 仅转换格式
# import re
#
# input_file = 'pairing_basepair_annotate_360k.csv'
# output_file = 'pairing_basepair_annotate_360k_comma.csv'
#
# with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
#     for line in fin:
#         line = line.rstrip('\n')
#         if not line.strip() or line.lstrip().startswith('#'):
#             fout.write(line + '\n')
#             continue
#         # 把任意数量的空格、Tab、逗号混合都替换成单个逗号
#         # 匹配：一个或多个空白（\s）、或者逗号，全部视为分隔
#         fields = re.split(r'[,\s]+', line.strip())
#         # 如果有内容就重组成逗号分隔
#         if fields:
#             fout.write(','.join(fields) + '\n')

#转换格式+去除ntv
import re

# 输入输出文件路径
input_file = 'pairing_basepair_annotate_400k.csv'
output_file = ('pairing_basepair_annotate_400k_comma.csv')

# 要删除的前 N 帧
remove_first_n_frames = 50

with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
    current_frame = None  # 当前帧编号（过滤时用）

    for line in fin:
        line = line.rstrip('\n')

        # 空行直接写出
        if not line.strip():
            fout.write(line + '\n')
            continue

        # 帧标识行
        if line.lstrip().startswith('# Frame'):
            frame_num = int(line.split()[2])

            # 跳过前 N 帧
            if frame_num < remove_first_n_frames:
                current_frame = None
                continue

            # 平移帧编号
            new_frame_num = frame_num - remove_first_n_frames
            fout.write(f"# Frame {new_frame_num}\n")
            current_frame = new_frame_num

        else:
            # 如果当前帧是保留的，处理该行
            if current_frame is not None:
                # 将空格/Tab/逗号混合分隔转为单个逗号
                fields = re.split(r'[,\s]+', line.strip())
                if fields:
                    fout.write(','.join(fields) + '\n')
