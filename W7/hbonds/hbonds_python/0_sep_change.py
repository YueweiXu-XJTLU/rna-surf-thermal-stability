import re

input_file = 'full_trajectory_pair.csv'
output_file = 'full_trajectory_pair_comma.csv'

with open(input_file, 'r', encoding='utf-8') as fin, open(output_file, 'w', encoding='utf-8') as fout:
    for line in fin:
        line = line.rstrip('\n')
        if not line.strip() or line.lstrip().startswith('#'):
            fout.write(line + '\n')
            continue
        # 把任意数量的空格、Tab、逗号混合都替换成单个逗号
        # 匹配：一个或多个空白（\s）、或者逗号，全部视为分隔
        fields = re.split(r'[,\s]+', line.strip())
        # 如果有内容就重组成逗号分隔
        if fields:
            fout.write(','.join(fields) + '\n')
