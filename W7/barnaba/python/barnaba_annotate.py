import barnaba as bb
import pandas as pd

gro_path = "1y26_system_em0.gro"
trr_path = "full_fit.trr"

# input_pairing_angle_cutoff=60
# input_my_dist_para_input=3.3
input_pairing_angle_cutoff=30
input_my_dist_para_input=3.5

# def annotate(filename,topology=None, stacking_rho_cutoff=2.5, stacking_angle_cutoff=40, pairing_angle_cutoff=60, my_dist_para_input=3.3):
result = bb.annotate(filename=trr_path, topology=gro_path, pairing_angle_cutoff=input_pairing_angle_cutoff, my_dist_para_input=input_my_dist_para_input)

stackings = result[0]
pairings = result[1]      # 或 result['pairings']，看返回类型
sequence = result[2]      # 或 result['sequence']

# print(pairings)

records = []
for frame_idx, frame in enumerate(pairings):
    pair_list, type_list = frame[0], frame[1]
    for (ij, typ) in zip(pair_list, type_list):
        i, j = int(ij[0]), int(ij[1])
        base_i = sequence[i]
        base_j = sequence[j]
        records.append({
            'frame': frame_idx,
            'base_i': base_i,
            'base_j': base_j,
            'pair_type': typ
        })

df = pd.DataFrame(records)
df.to_csv(f"pairings_{input_pairing_angle_cutoff}_{input_my_dist_para_input}.csv", index=False, encoding='utf-8')
print(df.head())
