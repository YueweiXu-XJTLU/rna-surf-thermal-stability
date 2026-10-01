# 统计每帧中不同配对类型的数量
import pandas as pd

file = 'basepair_annotate_ANNOTATE_pairing_out.csv'
frame_data = []
current_frame = None

with open(file, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('# Frame'):
            current_frame = int(line.split()[2])
            frame_data.append([])
        elif line and not line.startswith('#'):
            parts = line.split()
            if len(parts) == 3:
                frame_data[-1].append(parts)

# 每帧配对类型统计
for i, frame in enumerate(frame_data):
    df = pd.DataFrame(frame, columns=['res1', 'res2', 'type'])
    counts = df['type'].value_counts()
    print(f'Frame {i}:')
    print(counts)
    print('---')